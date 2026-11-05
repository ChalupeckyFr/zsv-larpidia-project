"""Build the compact, offline height-field payload used by the browser's 3D atlas view.

Run from the project root with the existing atlas Python dependencies:
    python atlas/scripts/build_terrain_3d.py

The 20 m model is sampled every 2 cells (40 m source spacing). Heights are
model values, not surveyed data.
"""
from __future__ import annotations

import base64
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
RELIEF = ROOT / "atlas" / "current" / "relief"
OUT = ROOT / "atlas" / "current" / "viewer" / "terrain-3d-data.js"
HUMAN = ROOT / "atlas" / "current" / "human"
SAMPLE_EVERY = 2


def point_segment_distance(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> tuple[float, float]:
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    t = 0.0 if length2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length2))
    return math.hypot(px - (ax + dx * t), py - (ay + dy * t)), t


def inside_polygon(x: float, y: float, polygon: list[list[float]]) -> bool:
    inside = False
    previous = polygon[-1]
    for current in polygon:
        if (current[1] > y) != (previous[1] > y):
            crossing_x = (previous[0] - current[0]) * (y - current[1]) / (previous[1] - current[1]) + current[0]
            if x < crossing_x:
                inside = not inside
        previous = current
    return inside


def distance_to_polygon(x: float, y: float, polygon: list[list[float]]) -> float:
    return min(
        point_segment_distance(x, y, *polygon[i], *polygon[(i + 1) % len(polygon)])[0]
        for i in range(len(polygon))
    )


def sample_grid(values: np.ndarray, x: float, y: float, origin_x: float, origin_y: float, cell: float) -> float:
    gx = max(0.0, min(values.shape[1] - 1.0, (x - origin_x) / cell))
    gy = max(0.0, min(values.shape[0] - 1.0, (y - origin_y) / cell))
    col, row = min(values.shape[1] - 2, int(gx)), min(values.shape[0] - 2, int(gy))
    tx, ty = gx - col, gy - row
    a, b = float(values[row, col]), float(values[row, col + 1])
    c, d = float(values[row + 1, col]), float(values[row + 1, col + 1])
    return a * (1 - tx - ty) + b * tx + c * ty if ty <= 1 - tx else b * (1 - ty) + d * (tx + ty - 1) + c * (1 - tx)


def r3(point: list[float]) -> list[float]:
    return [round(float(point[0]), 3), round(float(point[1]), 3)]


def transport_paths(path: Path, *, rail: bool = False) -> list[dict]:
    """Keep source line geometry in atlas kilometres; the browser applies the shared transform."""
    collection = json.loads(path.read_text(encoding="utf-8"))
    out: list[dict] = []
    for feature in collection.get("features", []):
        props = feature.get("properties") or {}
        geometry = feature.get("geometry") or {}
        lines = geometry.get("coordinates", [])
        if geometry.get("type") == "LineString":
            lines = [lines]
        elif geometry.get("type") != "MultiLineString":
            continue
        for part, points in enumerate(lines, 1):
            if len(points) < 2:
                continue
            if rail:
                out.append({
                    "id": str(props.get("id") or f"{props.get('line', 'rail')}-{part}"),
                    "line": str(props.get("line") or ""),
                    "name": str(props.get("name_cs") or props.get("line") or "Železnice"),
                    "section": str(props.get("section") or "surface"),
                    "length_m": float(props.get("length_m") or 0),
                    "points": [r3(p) for p in points],
                })
            else:
                out.append({
                    "id": str(props.get("id") or f"road-{part}"),
                    "class": str(props.get("class") or "R3"),
                    "section": str(props.get("section") or "surface"),
                    "name": str(props.get("name_cs") or props.get("id") or "Silnice"),
                    "length_m": float(props.get("length_m") or 0),
                    "points": [r3(p) for p in points],
                })
    return out


def main() -> None:
    meta = json.loads((RELIEF / "dem_meta.json").read_text(encoding="utf-8"))
    max_m = float(meta["max_m"])
    dem_u16 = np.asarray(Image.open(RELIEF / "dem_20m_u16.png"), dtype=np.uint16)
    landcover = np.asarray(Image.open(RELIEF / "landcover_20m.png"), dtype=np.uint8)
    heights_m = dem_u16.astype(np.float32) / 100.0

    height_sample = heights_m[::SAMPLE_EVERY, ::SAMPLE_EVERY]
    cover_sample = landcover[::SAMPLE_EVERY, ::SAMPLE_EVERY].copy()
    # The landcover raster has no river class, so rasterize the atlas waterway
    # vectors onto the terrain mesh. Sampling each segment at half a mesh cell
    # keeps narrow streams visible after the 20 m terrain is reduced to 100 m.
    hydro = json.loads((RELIEF / "hydrography.geojson").read_text(encoding="utf-8"))
    origin_x, origin_y = map(float, meta["origin_xy_km"])
    mesh_cell_km = float(meta["cell_km"]) * SAMPLE_EVERY
    mesh_h, mesh_w = cover_sample.shape
    for feature in hydro["features"]:
        geometry = feature.get("geometry") or {}
        lines = geometry.get("coordinates", [])
        if geometry.get("type") == "LineString":
            lines = [lines]
        elif geometry.get("type") != "MultiLineString":
            continue
        for points in lines:
            for start, end in zip(points, points[1:]):
                x0, y0 = map(float, start[:2])
                x1, y1 = map(float, end[:2])
                distance = math.hypot(x1 - x0, y1 - y0)
                steps = max(1, math.ceil(distance / (mesh_cell_km * 0.5)))
                for step in range(steps + 1):
                    t = step / steps
                    col = round(((x0 + (x1 - x0) * t) - origin_x) / mesh_cell_km)
                    row = round(((y0 + (y1 - y0) * t) - origin_y) / mesh_cell_km)
                    if 0 <= row < mesh_h and 0 <= col < mesh_w and cover_sample[row, col] != 0:
                        cover_sample[row, col] = 9

    water_features = []
    lake_polygon = None
    river_widths = {"main": 18.0, "river": 11.0, "stream": 5.5}
    for feature in hydro["features"]:
        geometry = feature.get("geometry") or {}
        properties = feature.get("properties") or {}
        if geometry.get("type") == "Polygon" and properties.get("id") == "W-lake-N04":
            lake_polygon = geometry["coordinates"][0][:-1]
            water_features.append({
                "id": properties["id"],
                "kind": "lake",
                "level_m": float(properties.get("level_m_model", 67.6)),
                "points": geometry["coordinates"][0],
            })
        elif geometry.get("type") == "LineString" and str(properties.get("id", "")).startswith("W-"):
            kind = str(properties.get("kind", "stream"))
            water_features.append({
                "id": properties["id"],
                "part": properties.get("part", "all"),
                "kind": kind,
                "width_m": river_widths.get(kind, 5.5),
                "bed_start_m": float(properties.get("bed_start_m", 0.0)),
                "bed_end_m": float(properties.get("bed_end_m", 0.0)),
                "points": geometry["coordinates"],
            })

    # Lower the terrain under the reservoir, then slope its rim back into the
    # surrounding hills. The water surface is drawn at level_m above this basin.
    if lake_polygon:
        level = next(feature["level_m"] for feature in water_features if feature["kind"] == "lake")
        for row in range(mesh_h):
            y = origin_y + row * mesh_cell_km
            for col in range(mesh_w):
                x = origin_x + col * mesh_cell_km
                inside = inside_polygon(x, y, lake_polygon)
                distance_m = distance_to_polygon(x, y, lake_polygon) * 1000
                if inside:
                    target = level - min(24.0, max(2.0, distance_m * 0.28))
                elif distance_m < 120:
                    target = level + distance_m * 0.27
                else:
                    continue
                height_sample[row, col] = min(height_sample[row, col], target)

    # Cut shallow, model-scale river channels into the 40 m mesh. River beds
    # follow the lower of the mapped bed grade and the local DEM, capped at a
    # 20 m cut so imperfect source elevations cannot create impossible ravines.
    for feature in water_features:
        if feature["kind"] == "lake":
            continue
        points = feature["points"]
        lengths = [0.0]
        for a, b in zip(points, points[1:]):
            lengths.append(lengths[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
        total = lengths[-1] or 1.0
        start, end = float(feature["bed_start_m"]), float(feature["bed_end_m"])
        reference = []
        for x, y in points:
            t = lengths[len(reference)] / total
            mapped_bed = start + (end - start) * t
            local_ground = sample_grid(height_sample, x, y, origin_x, origin_y, mesh_cell_km)
            reference.append(max(local_ground - 20.0, min(mapped_bed, local_ground - 1.5)))
        feature["_reference_m"] = reference
        radius_km = 0.10
        min_col = max(0, int((min(p[0] for p in points) - radius_km - origin_x) / mesh_cell_km))
        max_col = min(mesh_w - 1, int((max(p[0] for p in points) + radius_km - origin_x) / mesh_cell_km) + 1)
        min_row = max(0, int((min(p[1] for p in points) - radius_km - origin_y) / mesh_cell_km))
        max_row = min(mesh_h - 1, int((max(p[1] for p in points) + radius_km - origin_y) / mesh_cell_km) + 1)
        for row in range(min_row, max_row + 1):
            y = origin_y + row * mesh_cell_km
            for col in range(min_col, max_col + 1):
                x = origin_x + col * mesh_cell_km
                for i, (a, b) in enumerate(zip(points, points[1:])):
                    distance, t = point_segment_distance(x, y, *a, *b)
                    if distance > radius_km:
                        continue
                    bed = reference[i] + (reference[i + 1] - reference[i]) * t
                    bank_target = max(0.0, bed - 3.0 + distance / radius_km * 4.0)
                    height_sample[row, col] = min(height_sample[row, col], bank_target)

        # Water follows the carved DEM profile and sits just above the channel bed.
        feature["surface_m"] = [sample_grid(height_sample, x, y, origin_x, origin_y, mesh_cell_km) + 1.5 for x, y in points]
        feature.pop("_reference_m", None)

    # Preserve slope detail in a 16-bit height channel. A single 8-bit channel
    # quantizes 560 m terrain in 2.2 m steps and creates visible terrace bands.
    heights_u16 = np.clip(np.rint(height_sample / max_m * 65535.0), 0, 65535).astype(np.uint16)
    packed = np.empty((*heights_u16.shape, 3), dtype=np.uint8)
    packed[..., 0] = (heights_u16 >> 8).astype(np.uint8)
    packed[..., 1] = (heights_u16 & 255).astype(np.uint8)
    packed[..., 2] = cover_sample

    payload = {
        "width": int(heights_u16.shape[1]),
        "height": int(heights_u16.shape[0]),
        "sample_m": int(round(float(meta["cell_km"]) * 1000 * SAMPLE_EVERY)),
        "origin_xy_km": [float(v) for v in meta["origin_xy_km"]],
        "height_encoding": "u16be-normalized-to-max-elevation",
        "cover_encoding": "u8",
        "max_elevation_m": max_m,
        "packed": base64.b64encode(packed.tobytes()).decode("ascii"),
        "water_features": water_features,
        "roads": transport_paths(HUMAN / "roads.geojson"),
        "railways": transport_paths(HUMAN / "rail_lines.geojson", rail=True),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "/* Generated from atlas/current/relief; run build_terrain_3d.py to refresh. */\n"
        "window.LARPIDIA_TERRAIN_DATA = "
        + json.dumps(payload, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT.relative_to(ROOT)} · {payload['width']}×{payload['height']} mesh samples")


if __name__ == "__main__":
    main()
