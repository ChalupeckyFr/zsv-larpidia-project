"""Build the compact, offline height-field payload used by the browser's 3D atlas view.

Run from the project root with the existing atlas Python dependencies:
    python atlas/scripts/build_terrain_3d.py

The 20 m model is sampled every 5 cells (100 m mesh spacing) to keep WebGL
smooth on ordinary computers. Heights are model values, not surveyed data.
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
SAMPLE_EVERY = 5


def main() -> None:
    meta = json.loads((RELIEF / "dem_meta.json").read_text(encoding="utf-8"))
    max_m = float(meta["max_m"])
    dem_u16 = np.asarray(Image.open(RELIEF / "dem_20m_u16.png"), dtype=np.uint16)
    landcover = np.asarray(Image.open(RELIEF / "landcover_20m.png"), dtype=np.uint8)
    heights_m = dem_u16.astype(np.float32) / 100.0

    height_sample = heights_m[::SAMPLE_EVERY, ::SAMPLE_EVERY]
    cover_sample = landcover[::SAMPLE_EVERY, ::SAMPLE_EVERY].copy()
    # The landcover raster has no river class, so rasterize the atlas waterway
    # vectors onto the coarser mesh. Sampling each segment at half a mesh cell
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
    heights_u8 = np.clip(np.rint(height_sample / max_m * 255.0), 0, 255).astype(np.uint8)
    packed = np.empty((*heights_u8.shape, 2), dtype=np.uint8)
    packed[..., 0] = heights_u8
    packed[..., 1] = cover_sample

    payload = {
        "width": int(heights_u8.shape[1]),
        "height": int(heights_u8.shape[0]),
        "sample_m": int(round(float(meta["cell_km"]) * 1000 * SAMPLE_EVERY)),
        "max_elevation_m": max_m,
        "packed": base64.b64encode(packed.tobytes()).decode("ascii"),
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
