"""F6: pseudo-satelitní podklady S-01 (Larpidie) a S-02 (Paraland) z DEM, pokryvu, sídel a vektorových tras.

Obraz je SIMULOVANÁ satelitní vizualizace fiktivního ostrova (ne skutečná družicová data) a slouží jako tvarově přesná reference
pro externí generátor obrázků. Bez textu. Geometrie = zmrazený obrys (current/geometry/outline_coast.json).

Spuštění:  python atlas/scripts/render_sat.py [S-01|S-02|all]
Výstup:    atlas/current/renders/S-0x_base.png/.jpg, S-0x_mask_land.png, S-0x_mask_classes.png, S-0x_georef.json
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))

import atlas_svg as A
import canon
import geom
import human_env as he
import raster
from canon import ATLAS
from raster import smoothstep

CUR = ATLAS / "current"
OUT = CUR / "renders"

WINDOWS = {
    "S-01": {"canvas": {"x0": 1.4, "y0": 0.0, "w": 22.4, "h": 16.2}, "mpp": 10.0, "exag": 2.3, "title": "Larpidie – simulovaná satelitní vizualizace (návrh)"},
    "S-02": {"canvas": {"x0": 22.1, "y0": 14.4, "w": 7.0, "h": 5.6}, "mpp": 5.0, "exag": 3.0, "title": "Paraland – simulovaná satelitní vizualizace (návrh)"},
}

SEA_STOPS = [(0.0, (116, 208, 200)), (0.15, (74, 184, 198)), (0.50, (38, 146, 188)), (1.2, (22, 100, 160)), (3.0, (14, 68, 132)), (8.0, (9, 44, 102))]
ROOFS = [(160, 88, 64), (92, 96, 104), (190, 180, 168), (150, 74, 56), (214, 210, 200), (118, 112, 106)]


def interp_stops(d, stops):
    xs = [s[0] for s in stops]
    out = np.zeros(d.shape + (3,), dtype=np.float32)
    for c in range(3):
        out[..., c] = np.interp(d, xs, [s[1][c] for s in stops])
    return out


def crop_resize(arr, full_grid, win_grid, mode="F", resample=Image.BICUBIC):
    """Výřez z celoplátnové mřížky (20 m) do okna s jemnější mřížkou."""
    x0 = (win_grid.x0 - full_grid.x0) / full_grid.dx
    y0 = (win_grid.y0 - full_grid.y0) / full_grid.dx
    x1 = x0 + win_grid.nx * win_grid.dx / full_grid.dx
    y1 = y0 + win_grid.ny * win_grid.dx / full_grid.dx
    im = Image.fromarray(arr.astype(np.float32 if mode == "F" else np.uint8), mode=mode)
    return np.asarray(im.resize((win_grid.nx, win_grid.ny), resample, box=(x0, y0, x1, y1)))


def poly_px(g, pts):
    return [g.to_px(*p) for p in pts]


def render(name, spec, D, W):
    t0 = time.time()
    g = raster.Grid(spec["mpp"] / 1000.0, canvas=spec["canvas"])
    H, Wd = g.ny, g.nx
    full = W.g
    X, Y = g.mesh()
    rng_seed = 20261101 + (1 if name == "S-02" else 0)
    main, para = D.o["main"], D.o["para"]
    land = raster.rasterize(g, [main]) | raster.rasterize(g, [para])
    lake = raster.rasterize(g, [[tuple(p) for p in W.lake_poly]]) if spec["canvas"]["x0"] < 13 and spec["canvas"]["x0"] + spec["canvas"]["w"] > 11 else np.zeros_like(land)
    # --- výška (bikubicky) + mikroreliéf jen pro stínování
    z = crop_resize(W.z, full, g)
    z = np.where(land, np.maximum(z, 0.0), 0.0)
    ids = [0, 1, 2, 3, 4, 5, 6]
    stack = np.stack([crop_resize((W.cls == i).astype(np.float32), full, g, mode="F", resample=Image.BICUBIC) for i in ids], axis=0)
    stack_raw = stack
    stack = np.stack([raster.gauss(s, 1.2) for s in stack], axis=0)
    cls = np.array(ids, dtype=np.uint8)[np.argmax(stack, axis=0)]
    micro = raster.fbm(g, rng_seed + 1, [(0.12, 2.4), (0.045, 1.1), (0.02, 0.5)])
    zshade = z + micro * (0.35 + 0.65 * smoothstep(8, 120, z)) * land
    zshade = raster.gauss(zshade, 1.0)
    hs = raster.hillshade(zshade, spec["mpp"], az_deg=205.0, alt_deg=42.0, exag=spec.get("exag", 2.1))
    # --- vzdálenost od pobřeží (moře)
    pts = np.vstack([raster.resample_polyline(main, 0.04), raster.resample_polyline(para, 0.04)])
    Dsea = raster.coarse_nearest(g, pts, factor=6)
    # --- šumová pole
    n1 = raster.fbm(g, rng_seed + 2, [(0.5, 1.0), (0.18, 0.6)]); n1 /= (np.abs(n1).max() + 1e-6)
    n2 = raster.fbm(g, rng_seed + 3, [(0.06, 1.0), (0.025, 0.6)]); n2 /= (np.abs(n2).max() + 1e-6)
    n3 = raster.fbm(g, rng_seed + 4, [(0.012, 1.0)]); n3 /= (np.abs(n3).max() + 1e-6)
    rgb = np.zeros((H, Wd, 3), dtype=np.float32)

    # ========== moře
    sea = interp_stops(Dsea, SEA_STOPS)
    wave = raster.fbm(g, rng_seed + 5, [(0.030, 1.0), (0.010, 0.6)]); wave = wave / (np.abs(wave).max() + 1e-6)
    sea = sea * (1.0 + 0.06 * wave[..., None]) + 4.0 * wave[..., None]
    beaches = raster.rasterize(g, [tuple(map(tuple, b["ring"])) for b in coast_beaches(D)]) if coast_beaches(D) else np.zeros_like(land)
    bl = raster.gauss(beaches.astype(np.float32), 14.0 / (spec["mpp"] / 5.0))
    shoal = np.clip(bl * 2.0, 0, 1) * (1.0 - smoothstep(0.0, 0.22, Dsea))
    sea = sea * (1 - 0.45 * shoal[..., None]) + np.array([228, 214, 168], dtype=np.float32) * 0.45 * shoal[..., None]
    foam = np.exp(-((Dsea * 1000.0 / (14.0 + 6.0 * (n3 + 1))) ** 2)) * (0.55 + 0.35 * (n2 + 1) / 2)
    sea = sea * (1 - 0.8 * foam[..., None]) + 255.0 * 0.8 * foam[..., None]

    # ========== souš: albedo podle pokryvu (měkké přechody mezi třídami)
    blur = 38.0 / spec["mpp"]
    w = np.stack([raster.gauss(s, blur) for s in stack_raw], axis=0)
    w = w / (w.sum(axis=0, keepdims=True) + 1e-6)
    patt = np.floor((n1 + 1) * 2.0 + (n2 + 1) * 0.9).astype(int) % 5
    crop_pal = np.array([(176, 160, 92), (122, 152, 72), (98, 128, 62), (198, 180, 112), (142, 112, 72)], dtype=np.float32)
    canopy = (n3 * 15.0 + n2 * 13.0)[..., None]
    clump = (0.82 + 0.38 * smoothstep(-0.4, 0.8, n2))[..., None]
    col = np.zeros((H, Wd, 3), dtype=np.float32)
    # les
    f_col = (np.array([48, 88, 50], dtype=np.float32) + canopy * np.array([0.6, 1.0, 0.5], dtype=np.float32)) * clump
    col += w[1][..., None] * f_col
    # louka
    m_col = np.array([128, 152, 74], dtype=np.float32) + (n1 * 16.0 + n2 * 10.0)[..., None] * np.array([0.8, 1.0, 0.4], dtype=np.float32)
    col += w[2][..., None] * m_col
    # pole (mozaika parcel s tmavými mezemi)
    farm_col = crop_pal[patt]
    edge = np.abs(np.gradient(patt.astype(np.float32), axis=1)) + np.abs(np.gradient(patt.astype(np.float32), axis=0))
    farm_col = np.where((edge > 0.01)[..., None], farm_col * 0.82, farm_col)
    col += w[3][..., None] * farm_col
    # rýžové terasy: pruhy podél vrstevnic
    stripe = 0.5 + 0.5 * np.sin(2 * np.pi * z / 5.5 + n1 * 2.0)
    terr_col = np.array([118, 140, 74], dtype=np.float32) * (0.86 + 0.28 * stripe[..., None])
    col += w[4][..., None] * terr_col
    # křoviny a travnaté plochy (+ třída 0 = nedefinováno na souši)
    s_col = np.array([116, 130, 74], dtype=np.float32) + (n1 * 20.0)[..., None] * np.array([0.9, 1.0, 0.4], dtype=np.float32) + (n2 * 9.0 + n3 * 6.0)[..., None]
    col += (w[5] + w[0])[..., None] * s_col
    # skála
    r_col = np.array([128, 120, 108], dtype=np.float32) + (n3 * 16.0)[..., None]
    col += w[6][..., None] * r_col
    # pláž
    beach_mask = beaches
    col = np.where(beach_mask[..., None], np.array([226, 214, 172], dtype=np.float32) + (n3 * 8)[..., None], col)
    # mokrý písek a skalní břeh
    shore = np.exp(-((Dsea * 1000.0 / 10.0) ** 2))
    col = col * (1 - 0.30 * shore[..., None] * land[..., None])
    # jezero
    if lake.any():
        lc_ = np.array([30, 92, 112], dtype=np.float32) + (n2 * 8)[..., None]
        col = np.where(lake[..., None], lc_, col)

    # ========== zástavba a průmysl (rastr z půdorysů)
    urb_main = np.zeros_like(land)
    ind = np.zeros_like(land)
    for f in D.settle:
        pr = f["properties"]
        r = A.ring(f["geometry"]["coordinates"][0])
        m = raster.rasterize(g, [r])
        if pr["kind"] in ("industry", "port_area"):
            ind |= m
        else:
            urb_main |= m
    theta = np.radians(14.0) * np.ones_like(X)            # pevný úhel ulic (bez moaré)

    def lattice(cs, dens_field, p_build, roofs, yard_cols, street_col, seed_shift=0):
        u = (X * np.cos(theta) + Y * np.sin(theta)) / cs
        v = (-X * np.sin(theta) + Y * np.cos(theta)) / cs
        iu, iv = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
        fu, fv = u - iu, v - iv
        hsh = (((iu + seed_shift) * 73856093) ^ (iv * 19349663)) & 0xFFFF
        rnd = hsh / 65535.0
        shrink = 0.10 + 0.14 * ((hsh >> 3) & 7) / 7.0
        building = (fu > shrink) & (fu < 1 - shrink) & (fv > shrink + 0.04) & (fv < 1 - shrink - 0.04) & (rnd < p_build[0] + p_build[1] * dens_field)
        rf = np.array(roofs, dtype=np.float32)[(hsh >> 5) % len(roofs)]
        rf = rf * (0.92 + 0.16 * ((hsh >> 9) & 7)[..., None] / 7.0)
        yc = np.array(yard_cols, dtype=np.float32)[(hsh >> 11) % len(yard_cols)]
        c = np.where(building[..., None], rf, yc)
        on_street = (fu < 0.07) | (fv < 0.07)
        c = np.where(on_street[..., None] & ~building[..., None], np.array(street_col, dtype=np.float32), c)
        return c

    dens_u = np.clip(raster.gauss(urb_main.astype(np.float32), 34.0 / spec["mpp"]) + 0.30 * n2, 0.0, 1.0)
    urb_col = lattice(4.0 * spec["mpp"] / 1000.0, dens_u, (0.40, 0.60), ROOFS, [(138, 130, 118), (138, 130, 118), (136, 158, 104), (88, 116, 68)], (104, 100, 94))
    dens_i = np.clip(raster.gauss(ind.astype(np.float32), 40.0 / spec["mpp"]) + 0.15 * n2, 0.0, 1.0)
    ind_col = lattice(9.0 * spec["mpp"] / 1000.0, dens_i, (0.55, 0.40), [(214, 216, 214), (176, 182, 190), (230, 230, 226), (150, 156, 160), (196, 170, 150)],
                      [(122, 124, 126), (122, 124, 126), (84, 120, 72)], (96, 98, 100), seed_shift=977)
    cellB = raster.fbm(g, rng_seed + 7, [(0.040, 1.0)]); cellB /= (np.abs(cellB).max() + 1e-6)
    ind_col = np.where((cellB > 0.5)[..., None], np.array([78, 114, 66], dtype=np.float32) + (n3 * 10)[..., None], ind_col)
    soft_u = np.clip(dens_u * 3.0, 0.0, 1.0)[..., None] * urb_main[..., None]
    col = np.where(urb_main[..., None], col * (1 - soft_u) + urb_col * soft_u, col)
    soft_i = np.clip(dens_i * 3.0, 0.0, 1.0)[..., None] * ind[..., None]
    col = np.where(ind[..., None], col * (1 - soft_i) + ind_col * soft_i, col)

    # ========== osvětlení
    shade = (0.46 + 0.72 * hs)[..., None]
    shade = np.where((urb_main | ind)[..., None], 0.82 + 0.20 * shade, shade)
    col = np.clip(col * shade, 0, 255)
    rgb = np.where(land[..., None], col, sea)
    # lehký kontrastní tón a zrno
    grain = raster.fbm(g, rng_seed + 10, [(0.004, 1.0)])
    rgb = np.clip(rgb + 2.2 * grain[..., None], 0, 255)
    img = Image.fromarray(rgb.astype(np.uint8), "RGB")

    # ========== vektorové detaily (supersampling 2×)
    ss = 2
    big_img = img.resize((Wd * ss, H * ss), Image.BICUBIC)
    d = ImageDraw.Draw(big_img, "RGBA")
    P2 = lambda pts: [(x * ss, y * ss) for x, y in poly_px(g, pts)]

    def line(pts, w_px, fill):
        if len(pts) > 1:
            d.line(P2(pts), fill=fill, width=max(1, int(round(w_px * ss))), joint="curve")

    for f in D.hydro:
        if f["geometry"]["type"] == "LineString":
            kind = f["properties"]["kind"]
            line([tuple(c) for c in f["geometry"]["coordinates"]], {"main": 2.4, "river": 2.0, "stream": 1.3}[kind] * 5.0 / spec["mpp"] * 1.0 + 0.4, (66, 128, 176, 235))
    for f in D.roads:
        c = [tuple(q) for q in f["geometry"]["coordinates"]]
        cl = f["properties"]["class"]
        if f["properties"]["section"] == "tunnel":
            continue
        wpx = {"R1": 9.0, "R2": 7.0, "R3": 4.8}[cl] / spec["mpp"]
        line(c, wpx + 1.0, (70, 66, 60, 150))
        line(c, wpx, (226, 222, 212, 255) if cl != "R3" else (200, 196, 186, 255))
    for f in D.rail:
        p = f["properties"]
        if p["line"] == "L3" or p["section"] in ("tunnel", "cave", "undersea", "glass_gallery"):
            continue
        c = [tuple(q) for q in f["geometry"]["coordinates"]]
        line(c, 4.0 / spec["mpp"] + 0.6, (50, 50, 52, 255))
        line(c, 1.5 / spec["mpp"] + 0.2, (220, 220, 216, 255))
    for f in D.pa:
        p, gm = f["properties"], f["geometry"]
        if p.get("kind") == "breakwater":
            line([tuple(c) for c in gm["coordinates"]], 20.0 / spec["mpp"], (170, 172, 170, 255))
        elif p.get("kind") == "pier":
            d.polygon(P2(A.ring(gm["coordinates"][0])), fill=(160, 160, 158, 255))
        elif p.get("kind") in ("regional_airport", "light_airstrip") and p.get("part") == "runway":
            col_ = (86, 86, 90, 255) if p["id"] == "A-01" else (104, 140, 76, 255)
            d.polygon(P2(A.ring(gm["coordinates"][0])), fill=col_)
            ring_ = A.ring(gm["coordinates"][0])
            cx, cy = geom.centroid(ring_)
        elif p.get("part") == "apron":
            d.polygon(P2(A.ring(gm["coordinates"][0])), fill=(176, 176, 174, 255))
        elif p.get("part") == "terminal":
            d.polygon(P2(A.ring(gm["coordinates"][0])), fill=(210, 206, 198, 255))
    # označení dráhy A-01 (osová čára)
    a01 = D.reg["A-01"]
    c = (a01["x_km"], a01["y_km"])
    line([(c[0] - 0.85, c[1]), (c[0] + 0.85, c[1])], 1.0 / spec["mpp"] + 0.4, (240, 240, 236, 220))
    # Paraland: aquapark, hrad, hotely
    for pid, kind in (("PL-04", "aqua"), ("PL-02", "castle"), ("PL-06", "ruin")):
        o = D.reg[pid]
        if not (spec["canvas"]["x0"] <= o["x_km"] <= spec["canvas"]["x0"] + spec["canvas"]["w"]):
            continue
        cx, cy = g.to_px(o["x_km"], o["y_km"])
        s = ss
        if kind == "aqua":
            for dx, dy, rr, colr in ((-60, -20, 38, (40, 200, 220, 255)), (10, 25, 46, (30, 170, 210, 255)), (70, -10, 30, (80, 215, 225, 255))):
                k = 5.0 / spec["mpp"]
                d.ellipse([(cx + dx * k / 5 - rr * k / 5) * s, (cy + dy * k / 5 - rr * k / 7) * s, (cx + dx * k / 5 + rr * k / 5) * s, (cy + dy * k / 5 + rr * k / 7) * s], fill=colr)
        elif kind == "castle":
            k = 5.0 / spec["mpp"]
            d.rectangle([(cx - 34 * k) * s, (cy - 22 * k) * s, (cx + 34 * k) * s, (cy + 22 * k) * s], fill=(176, 168, 154, 255), outline=(90, 84, 76, 255))
            d.rectangle([(cx - 12 * k) * s, (cy - 12 * k) * s, (cx + 12 * k) * s, (cy + 12 * k) * s], fill=(142, 90, 70, 255))
        else:
            k = 5.0 / spec["mpp"]
            d.polygon([((cx - 26 * k) * s, (cy + 14 * k) * s), ((cx - 8 * k) * s, (cy - 18 * k) * s), ((cx + 22 * k) * s, (cy - 4 * k) * s), ((cx + 10 * k) * s, (cy + 18 * k) * s)], fill=(150, 140, 126, 255))
    img = big_img.resize((Wd, H), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))

    # ========== uložení: obraz, masky, georeference
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / f"{name}_base.png", optimize=True)
    img.save(OUT / f"{name}_base.jpg", quality=94, subsampling=0, optimize=True)
    Image.fromarray((land.astype(np.uint8) * 255), "L").save(OUT / f"{name}_mask_land.png", optimize=True)
    cmap = np.zeros((H, Wd), dtype=np.uint8)
    cmap[land] = cls[land]
    cmap[land & urb_main] = 10
    cmap[land & ind] = 11
    cmap[lake] = 8
    cm = Image.fromarray(cmap, "L")
    pal = [0] * 768
    for k, hx in {0: "#0a3a70", 1: "#224a26", 2: "#96ac54", 3: "#b0a05c", 4: "#76904a", 5: "#74824a", 6: "#80786c", 7: "#e2d6ac", 8: "#1c5c70", 10: "#a08070", 11: "#9a9c9a"}.items():
        pal[k * 3:k * 3 + 3] = [int(hx[i:i + 2], 16) for i in (1, 3, 5)]
    cm.putpalette(pal)
    cm.save(OUT / f"{name}_mask_classes.png", optimize=True)
    geo = {"id": name, "title": spec["title"], "status": "proposed", "px": [Wd, H], "meters_per_pixel": spec["mpp"], "window_km": spec["canvas"],
           "pixel_to_km": "x_km = x0 + (px + 0.5) * mpp/1000 ; y_km = y0 + (py + 0.5) * mpp/1000 (sever nahoře, východ vpravo)", "orientation": "kolmý pohled shora (nadir), sever nahoře",
           "land_area_km2": round(float(land.sum() * (spec["mpp"] / 1000.0) ** 2), 2), "disclaimer": "SIMULOVANÁ satelitní vizualizace fiktivního ostrova, ne skutečná družicová data",
           "atlas_version": canon.ATLAS_VERSION, "coast_sha256": D.fro["coast_sha256"]}
    (OUT / f"{name}_georef.json").write_text(json.dumps(geo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{name}: {Wd}×{H} px @ {spec['mpp']} m, za {time.time() - t0:.0f}s; souš {geo['land_area_km2']} km²")
    return img, land


_BEACH_CACHE = {}


def coast_beaches(D):
    if "b" not in _BEACH_CACHE:
        _BEACH_CACHE["b"] = [{"ring": A.ring(f["geometry"]["coordinates"][0])} for f in D.coast if f["properties"]["class"] == "beach"]
    return _BEACH_CACHE["b"]


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    D = A.Data()
    W = he.World()
    for name, spec in WINDOWS.items():
        if which in ("all", name):
            render(name, spec, D, W)


if __name__ == "__main__":
    main()
