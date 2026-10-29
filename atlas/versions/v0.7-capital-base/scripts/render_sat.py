"""F6 (druhé kolo): pseudo-satelitní podklady z DEM, pokryvu, sídel a vektorových tras – kolmé i šikmé pohledy.

Obraz je SIMULOVANÁ satelitní vizualizace fiktivního ostrova (ne skutečná družicová data) a slouží jako tvarově přesná reference
pro externí generátor obrázků. Bez textu. Geometrie = zmrazený obrys (current/geometry/outline_coast.json).

Spuštění:  python atlas/scripts/render_sat.py [S-01|S-02|S-00|obliques|all]
Výstup:    atlas/current/renders/S-0x_base.png/.jpg (+ masky, georeference), S-00_overview.jpg, S-0x_oblique_*.jpg, *_clouds.jpg
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
INTERNAL = {"X-pen": {"canvas": {"x0": 17.6, "y0": 10.6, "w": 6.4, "h": 5.0}, "mpp": 3.0, "exag": 2.8, "internal": True,
                      "title": "interní okno 3 m/px: jihovýchodní poloostrov a průliv (zdroj pro šikmý pohled)"}}
WORK_SAT = ATLAS / "work" / "sat"
OVERVIEW = {"canvas": {"x0": -0.2, "y0": -1.0, "w": 29.7, "h": 21.0}, "mpp": 10.0, "exag": 2.3, "title": "Larpidie a Paraland – přehled (simulovaná vizualizace, návrh)"}

# šikmé pohledy: kamera v km (x východ, y jih, počátek SZ roh rámce 24×16 km), výška v m n. m., heading ve stupních od severu po směru hodin,
# horizon = poloha obzoru jako zlomek výšky obrazu (kamera s posunutým objektivem, bez naklopení → svislice zůstávají svislé)
OBLIQUES = {
    "S-01_oblique_S": {"x": 16.4, "y": 21.6, "h": 3000.0, "heading": 1.0, "horizon": 0.13, "fov": 62.0, "dmax": 50000.0, "sources": ["S-02", "S-00"],
                       "desc": "z moře jižně od hlavního města k severu: historický přístav, město, pláže, pole a hory na severozápadě"},
    "S-01_oblique_NW": {"x": -6.0, "y": 3.2, "h": 2600.0, "heading": 99.0, "horizon": 0.12, "fov": 64.0, "dmax": 50000.0, "sources": ["S-00"],
                        "desc": "z moře severozápadně od ostrova k východu: útesy severozápadu, hory, přehrada, jihovýchodní poloostrov"},
    "S-02_oblique_SW": {"x": 21.8, "y": 20.3, "h": 1000.0, "heading": 47.0, "horizon": 0.16, "fov": 60.0, "dmax": 40000.0, "sources": ["S-02", "S-00"],
                        "desc": "z moře jihozápadně od Paralandu: resorty a aquapark na jihu, východní les a pláže"},
    "S-02_oblique_strait": {"x": 19.7, "y": 12.0, "h": 900.0, "heading": 131.0, "horizon": 0.22, "fov": 62.0, "dmax": 40000.0, "sources": ["S-02", "X-pen", "S-00"],
                            "desc": "z jihovýchodního poloostrova hlavního ostrova přes průliv 1,5 km na Paraland"},
}
OBLIQUE_ZEXAG = 1.35         # svislé převýšení šikmých pohledů (jinak by 560 m hory vypadaly jako pahorky)

SEA_STOPS = [(0.0, (104, 196, 196)), (0.10, (70, 176, 196)), (0.35, (40, 146, 188)), (0.9, (24, 106, 164)), (2.5, (16, 72, 136)), (8.0, (10, 46, 104))]
ROOFS = [(160, 88, 64), (92, 96, 104), (190, 180, 168), (150, 74, 56), (214, 210, 200), (118, 112, 106)]
CROPS = np.array([(168, 154, 100), (128, 150, 84), (108, 132, 76), (182, 166, 112), (138, 114, 84), (150, 160, 96)], dtype=np.float32)
TOWN_ANGLE = {"C-01": 12, "T-01": -14, "T-02": 22, "T-03": 35, "T-04": 4, "T-05": -24, "T-06": 8, "I-01": 6, "I-03": 6, "PL-01": 18, "PL-03": -10, "PL-05": 0}


TOWN_STYLES = {
    "old": {"salt": 11, "roofs": [(172, 96, 70), (160, 84, 62), (186, 112, 82), (126, 86, 70), (196, 140, 104), (104, 104, 110)],
            "yards": [(146, 138, 126), (140, 134, 122), (132, 136, 110)], "street": (160, 156, 148), "plot": (0.013, 0.017), "n": (5, 2), "sw": 0.0050,
            "margin": (0.10, 0.12), "fill": (0.30, 0.65), "green": 0.04},
    "mid": {"salt": 23, "roofs": [(168, 98, 74), (150, 84, 64), (112, 112, 118), (186, 178, 166), (92, 94, 100), (176, 120, 92), (204, 198, 188)],
            "yards": [(128, 138, 100), (136, 138, 112), (122, 134, 96)], "street": (158, 154, 146), "plot": (0.017, 0.022), "n": (4, 2), "sw": 0.0065,
            "margin": (0.14, 0.16), "fill": (0.25, 0.65), "green": 0.06},
    "resort": {"salt": 37, "roofs": [(222, 216, 204), (186, 114, 84), (232, 226, 216), (168, 98, 72), (204, 198, 188)],
               "yards": [(108, 136, 86), (112, 138, 92), (136, 140, 120)], "street": (162, 158, 150), "plot": (0.022, 0.026), "n": (3, 2), "sw": 0.0070,
               "margin": (0.18, 0.20), "fill": (0.20, 0.60), "green": 0.14},
    "industry": {"salt": 53, "roofs": [(178, 184, 192), (206, 208, 206), (92, 124, 88), (72, 86, 112), (150, 156, 160), (96, 128, 92)],
                 "yards": [(96, 134, 84), (96, 134, 84), (104, 138, 90), (122, 124, 126)], "street": (118, 120, 120), "plot": (0.060, 0.040), "n": (2, 2), "sw": 0.0090,
                 "margin": (0.12, 0.16), "fill": (0.35, 0.40), "green": 0.28, "industrial": True},
    "port": {"salt": 71, "roofs": [(150, 70, 56), (60, 86, 128), (186, 150, 60), (84, 116, 84), (172, 172, 170), (124, 84, 60), (70, 76, 90)],
             "yards": [(112, 114, 116), (104, 106, 108)], "street": (92, 94, 96), "plot": (0.026, 0.014), "n": (3, 3), "sw": 0.0080,
             "margin": (0.06, 0.12), "fill": (0.80, 0.10), "green": 0.0, "industrial": True},
}


HARBOR_LINKS = [("C-02", "C-01"), ("H-02", "PL-05"), ("H-01", "T-04")]


def style_of(pr):
    if pr["kind"] == "port_area":
        return "port"
    if pr["kind"] == "industry":
        return "industry"
    if pr["kind"] in ("capital", "old_town") or pr["id"] == "T-02":
        return "old"
    if pr["kind"] == "resort":
        return "resort"
    return "mid"


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


def nrm(a):
    return a / (np.abs(a).max() + 1e-6)


def hash2(iu, iv, salt=0):
    return (((iu + salt) * 73856093) ^ (iv * 19349663)) & 0xFFFF


# ------------------------------------------------------------------ parcely a zástavba
def parcels(g, X, Y, n1, mpp, farm_w):
    """Mozaika polí: pootočená mřížka (~150 m), část parcel půlená, živé ploty; parcela je pole podle váhy pole ve svém středu.
    Vrací (barva, alfa pole). Řádky plodin jen v jemném okně."""
    k = np.floor((n1 + 1.0) * 1.5).astype(int) % 3
    th = np.radians(np.array([8.0, 38.0, -22.0], dtype=np.float32))[k]
    cs = 0.15
    ct, st = np.cos(th), np.sin(th)
    u = (X * ct + Y * st) / cs
    v = (-X * st + Y * ct) / cs
    iu, iv = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
    fu, fv = u - iu, v - iv
    h = hash2(iu, iv, 311)
    cx = ((iu + 0.5) * cs) * ct - ((iv + 0.5) * cs) * st
    cy = ((iu + 0.5) * cs) * st + ((iv + 0.5) * cs) * ct
    jx = np.clip(((cx - g.x0) / g.dx).astype(np.int64), 0, g.nx - 1)
    iy = np.clip(((cy - g.y0) / g.dx).astype(np.int64), 0, g.ny - 1)
    wc = farm_w[iy, jx]
    alpha = (wc > 0.22 + 0.62 * ((h >> 10) & 63) / 63.0).astype(np.float32)
    split = ((h >> 4) & 3) == 0
    cut = 0.35 + 0.30 * ((h >> 6) & 7) / 7.0
    pid = (h + (split & (fu > cut)).astype(np.int64) * 7919) & 0xFFFF
    col = CROPS[(pid >> 3) % 6] * (0.93 + 0.14 * ((pid >> 9) & 7)[..., None] / 7.0)
    green_house = (pid % 53) == 0
    col = np.where(green_house[..., None], np.array([196, 200, 196], dtype=np.float32), col)
    hedge = (fu < 0.030) | (fv < 0.030) | (split & (np.abs(fu - cut) < 0.022))
    col = np.where(hedge[..., None], np.array([74, 100, 60], dtype=np.float32), col)
    if mpp <= 6.0:
        rows = 0.5 + 0.5 * np.sin(2 * np.pi * (v * cs) / 0.014)
        col = col * (0.95 + 0.10 * rows[..., None])
    return col, alpha


def box_cov(f, lo, hi, w):
    """Měkké pokrytí intervalu <lo, hi> (pro antialiasing hran budov a ulic)."""
    return smoothstep(lo - w, lo + w, f) * (1.0 - smoothstep(hi - w, hi + w, f))


def town_texture(X, Y, theta, mpp, seed, style):
    """Zástavba po blocích: ulice, parcely, budovy, parky a stíny (slunce z jihu → stín k severu). Vrací vrstvy zvlášť, aby se
    daly míchat podle hustoty. Měřítko prvků se drží ≥ ~3 px (bez moaré)."""
    px = mpp / 1000.0
    plot, n, margin, fill_ = style["plot"], style["n"], style["margin"], style["fill"]
    pu, pv = max(plot[0], 3.0 * px), max(plot[1], 3.4 * px)
    sw = max(style["sw"], 0.9 * px)
    bu, bv = pu * n[0] + sw, pv * n[1] + sw
    c_, s_ = np.cos(theta), np.sin(theta)
    u = X * c_ + Y * s_
    v = -X * s_ + Y * c_
    iu, iv = np.floor(u / bu).astype(np.int64), np.floor(v / bv).astype(np.int64)
    lu, lv = u - iu * bu, v - iv * bv
    hb = hash2(iu, iv, seed)
    w = 0.55 * px
    du = np.abs(((lu - sw / 2) + bu / 2) % bu - bu / 2)
    dv = np.abs(((lv - sw / 2) + bv / 2) % bv - bv / 2)
    street_a = np.maximum(1.0 - smoothstep(sw / 2 - w, sw / 2 + w, du), 1.0 - smoothstep(sw / 2 - w, sw / 2 + w, dv))
    qu, qv = lu - sw, lv - sw
    ju = np.clip(np.floor(qu / pu).astype(np.int64), 0, n[0] - 1)
    jv = np.clip(np.floor(qv / pv).astype(np.int64), 0, n[1] - 1)
    fu, fv = qu - ju * pu, qv - jv * pv
    hp = hash2(iu * 7 + ju, iv * 5 + jv, seed + 17)
    mu = (margin[0] + 0.12 * ((hp >> 3) & 7) / 7.0) * pu
    mv = (margin[1] + 0.12 * ((hp >> 6) & 7) / 7.0) * pv
    green_blk = ((hb >> 5) & 31) < int(style["green"] * 32)
    present = ((hp / 65535.0) < 1.0) & ~green_blk
    bld = box_cov(fu, mu, pu - mu, w) * box_cov(fv, mv, pv - mv, w) * present * (1.0 - street_a)
    rnd = hp / 65535.0
    rf = np.array(style["roofs"], dtype=np.float32)
    base = rf[(hb >> 2) % len(rf)]
    alt = (((hp >> 13) & 7) < 5)[..., None]
    base = np.where(alt, rf[(hp >> 3) % len(rf)], base)
    roof = base * (0.88 + 0.24 * ((hp >> 9) & 15)[..., None] / 15.0)
    yc = np.array(style["yards"], dtype=np.float32)[(hb >> 9) % len(style["yards"])]
    park = green_blk.astype(np.float32)
    ground = yc * (1.0 - park[..., None]) + np.array([86, 124, 68], dtype=np.float32) * park[..., None]
    sh = max(1, int(round(9.0 / mpp)))
    shadow = np.clip(np.roll(bld, -sh, axis=0) - bld, 0.0, 1.0)
    return {"ground": ground, "street": street_a, "roof": roof, "bld": bld, "shadow": shadow, "rnd": rnd, "fill": fill_}


def arc_samples(coords, step, rng, jitter=0.5):
    """Body podél lomené čáry (km) po cca `step` km: (x, y, tx, ty)."""
    out = []
    acc = step * rng.uniform(0.2, 1.0)
    for (x0, y0), (x1, y1) in zip(coords[:-1], coords[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        if L < 1e-9:
            continue
        tx, ty = (x1 - x0) / L, (y1 - y0) / L
        pos = 0.0
        while acc <= L - pos:
            pos += acc
            out.append((x0 + tx * pos, y0 + ty * pos, tx, ty))
            acc = step * rng.uniform(1.0 - jitter, 1.0 + jitter)
        acc -= (L - pos)
    return out


# ------------------------------------------------------------------ mraky
def add_clouds(rgb, g, land, Dsea, seed, mpp):
    """Volitelná varianta s mraky jen nad otevřeným mořem (pobřeží a ostrov zůstanou čisté); mraky vrhají stín na hladinu."""
    n = raster.fbm(g, seed, [(3.2, 1.0), (1.4, 0.65), (0.6, 0.42), (0.25, 0.28), (0.09, 0.16)])
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    thr = float(np.quantile(n, 0.87))
    cov = smoothstep(thr, thr + 0.05, n)
    core = smoothstep(thr + 0.02, thr + 0.16, n)
    open_sea = (1.0 - np.clip(raster.gauss(land.astype(np.float32), 450.0 / mpp) * 4.0, 0.0, 1.0)) * smoothstep(0.6, 1.6, Dsea)
    alpha = cov * open_sea
    tone = 0.82 + 0.18 * core
    sh = max(1, int(0.30 * 1000 / mpp))
    shadow = np.roll(np.roll(alpha, sh, axis=1), int(sh * 0.9), axis=0) * (1.0 - alpha)
    out = rgb * (1.0 - 0.28 * shadow[..., None])
    cloud_col = np.array([250, 252, 255], dtype=np.float32)[None, None, :] * tone[..., None]
    return out * (1.0 - alpha[..., None]) + cloud_col * alpha[..., None]


# ------------------------------------------------------------------ nadir
def render(name, spec, D, W, clouds=False):
    t0 = time.time()
    g = raster.Grid(spec["mpp"] / 1000.0, canvas=spec["canvas"])
    H, Wd = g.ny, g.nx
    full = W.g
    X, Y = g.mesh()
    mpp = spec["mpp"]
    seed = 20261101 + {"S-01": 0, "S-02": 1, "S-00": 2}.get(name, 0)
    main, para = D.o["main"], D.o["para"]
    land = raster.rasterize(g, [main]) | raster.rasterize(g, [para])
    c = spec["canvas"]
    has_lake = c["x0"] < 13 and c["x0"] + c["w"] > 11
    lake = raster.rasterize(g, [[tuple(p) for p in W.lake_poly]]) if has_lake else np.zeros_like(land)
    # --- výška a třídy
    z = crop_resize(W.z, full, g)
    z = np.where(land, np.maximum(z, 0.0), 0.0)
    ids = [0, 1, 2, 3, 4, 5, 6]
    stack_raw = np.stack([crop_resize((W.cls == i).astype(np.float32), full, g, mode="F", resample=Image.BICUBIC) for i in ids], axis=0)
    stack = np.stack([raster.gauss(s, 1.2) for s in stack_raw], axis=0)
    cls = np.array(ids, dtype=np.uint8)[np.argmax(stack, axis=0)]
    micro = raster.fbm(g, seed + 1, [(0.12, 2.4), (0.045, 1.1), (0.02, 0.5)])
    zshade = raster.gauss(z + micro * (0.35 + 0.65 * smoothstep(8, 120, z)) * land, 1.0)
    hs = raster.hillshade(zshade, mpp, az_deg=205.0, alt_deg=42.0, exag=spec.get("exag", 2.1))
    pts = np.vstack([raster.resample_polyline(main, 0.04), raster.resample_polyline(para, 0.04)])
    Dsea = raster.coarse_nearest(g, pts, factor=6)
    # --- šum
    n1 = nrm(raster.fbm(g, seed + 2, [(0.5, 1.0), (0.18, 0.6)]))
    n2 = nrm(raster.fbm(g, seed + 3, [(0.06, 1.0), (0.025, 0.6)]))
    n3 = nrm(raster.fbm(g, seed + 4, [(0.012, 1.0)]))
    nf = nrm(raster.fbm(g, seed + 12, [(0.35, 1.0), (0.12, 0.5)]))
    nclear = nrm(raster.fbm(g, seed + 13, [(0.25, 1.0)]))

    # ========== moře
    beach_pts = [raster.resample_polyline(b["ring"], 0.04) for b in coast_beaches(D)]
    if beach_pts:
        shelf = 0.42 + 0.58 * np.exp(-raster.coarse_nearest(g, np.vstack(beach_pts), factor=6) / 1.5)     # u pláží široký šelf, u útesů hluboká voda hned u břehu
    else:
        shelf = np.full_like(Dsea, 0.6)
    sea = interp_stops(Dsea / shelf, SEA_STOPS)
    wave = nrm(raster.fbm(g, seed + 5, [(0.030, 1.0), (0.010, 0.6)]))
    sea = sea * (1.0 + 0.06 * wave[..., None]) + 4.0 * wave[..., None]
    beaches = raster.rasterize(g, [tuple(map(tuple, b["ring"])) for b in coast_beaches(D)]) if coast_beaches(D) else np.zeros_like(land)
    bl = raster.gauss(beaches.astype(np.float32), 14.0 / (mpp / 5.0))
    shoal = np.clip(bl * 2.0, 0, 1) * (1.0 - smoothstep(0.0, 0.22, Dsea))
    sea = sea * (1 - 0.40 * shoal[..., None]) + np.array([228, 214, 168], dtype=np.float32) * 0.40 * shoal[..., None]
    # kalné vody (plumy) u ústí řek
    for f in D.hydro:
        gm, pr = f["geometry"], f["properties"]
        if gm["type"] == "LineString" and pr["part"] in ("all", "down"):
            mx, my = gm["coordinates"][-1]
            if c["x0"] - 0.5 < mx < c["x0"] + c["w"] + 0.5 and c["y0"] - 0.5 < my < c["y0"] + c["h"] + 0.5:
                plume = np.exp(-(((X - mx) ** 2 + (Y - my) ** 2) / (0.20 ** 2))) * (1.0 - land)
                sea = sea * (1 - 0.55 * plume[..., None]) + np.array([84, 148, 160], dtype=np.float32) * 0.55 * plume[..., None]
    foam = np.exp(-((Dsea * 1000.0 / (12.0 + 5.0 * (n3 + 1))) ** 2)) * (0.50 + 0.35 * (n2 + 1) / 2)
    sea = sea * (1 - 0.75 * foam[..., None]) + 255.0 * 0.75 * foam[..., None]

    # ========== souš: albedo podle pokryvu (měkké přechody mezi třídami)
    blur = 38.0 / mpp
    w = np.stack([raster.gauss(s, blur) for s in stack_raw], axis=0)
    w = w / (w.sum(axis=0, keepdims=True) + 1e-6)
    # zubatá hranice lesa a remízky: hranice se rozbije šumem a lesní váha se přerozdělí ostatním třídám
    nedge = raster.fbm(g, seed + 15, [(0.14, 1.0), (0.055, 0.8), (0.020, 0.5)])
    nedge = nedge / (np.abs(nedge).max() + 1e-6)
    ncop = nrm(raster.fbm(g, seed + 16, [(0.030, 1.0), (0.012, 0.6)]))
    forest_a = smoothstep(0.40, 0.60, w[1] + 0.85 * nedge)
    near_f = np.clip(raster.gauss(w[1], 160.0 / mpp) * 1.6, 0.0, 1.0)
    copse = smoothstep(0.60 - 0.20 * near_f, 0.74 - 0.20 * near_f, ncop) * (w[2] + w[5] + w[0]) * 0.8   # remízky v lukách a křovinách, hustší u lesa
    copse = copse * (0.55 + 0.45 * smoothstep(-0.2, 0.6, nedge))                    # členité okraje, ne hladké elipsy
    forest_a = np.clip(np.maximum(forest_a, copse * 0.8), 0.0, 1.0)
    rest = w.copy()
    rest[1] = 0.0
    rest = rest / (rest.sum(axis=0, keepdims=True) + 1e-6)
    w = rest * (1.0 - forest_a)[None]
    w[1] = forest_a
    col = np.zeros((H, Wd, 3), dtype=np.float32)
    canopy = (n3 * 15.0 + n2 * 13.0)[..., None]
    clump = (0.82 + 0.38 * smoothstep(-0.4, 0.8, n2))[..., None]
    broad = np.array([50, 92, 52], dtype=np.float32)
    conif = np.array([34, 66, 42], dtype=np.float32)
    young = np.array([76, 112, 58], dtype=np.float32)
    f_base = conif + (broad - conif) * smoothstep(-0.3, 0.3, nf)[..., None]
    f_base = f_base + (young - f_base) * (0.55 * smoothstep(0.45, 0.8, nrm(raster.fbm(g, seed + 14, [(0.22, 1.0)]))))[..., None]
    f_col = (f_base + canopy * np.array([0.6, 1.0, 0.5], dtype=np.float32)) * clump
    pc, farm_alpha = parcels(g, X, Y, n1, mpp, w[3])
    dry = smoothstep(0.1, 0.7, nrm(raster.fbm(g, seed + 17, [(0.30, 1.0), (0.10, 0.5)])))[..., None]
    meadow_col = np.array([116, 142, 70], dtype=np.float32) + (n1 * 24.0 + n2 * 14.0 + n3 * 8.0)[..., None] * np.array([0.8, 1.0, 0.4], dtype=np.float32)
    meadow_col = meadow_col * (1 - 0.30 * dry) + np.array([156, 150, 88], dtype=np.float32) * 0.30 * dry
    meadow_col = meadow_col * 0.80 + pc * 0.20 * np.array([1.0, 1.0, 0.9], dtype=np.float32)
    clearing = smoothstep(0.60, 0.72, nclear)[..., None]
    f_col = f_col * (1 - 0.8 * clearing) + meadow_col * 0.8 * clearing
    col += w[1][..., None] * f_col
    col += w[2][..., None] * meadow_col
    col += w[3][..., None] * (pc * farm_alpha[..., None] + meadow_col * (1.0 - farm_alpha[..., None]))
    stripe = 0.5 + 0.5 * np.sin(2 * np.pi * z / 5.5 + n1 * 2.0)
    col += w[4][..., None] * (np.array([118, 140, 74], dtype=np.float32) * (0.86 + 0.28 * stripe[..., None]))
    s_col = np.array([116, 130, 74], dtype=np.float32) + (n1 * 20.0)[..., None] * np.array([0.9, 1.0, 0.4], dtype=np.float32) + (n2 * 9.0 + n3 * 6.0)[..., None]
    col += (w[5] + w[0])[..., None] * s_col
    col += w[6][..., None] * (np.array([128, 120, 108], dtype=np.float32) + (n3 * 16.0)[..., None])
    col = np.where(beaches[..., None], np.array([226, 214, 172], dtype=np.float32) + (n3 * 8)[..., None], col)
    shore = np.exp(-((Dsea * 1000.0 / 10.0) ** 2))
    col = col * (1 - 0.30 * shore[..., None] * land[..., None])
    if lake.any():
        col = np.where(lake[..., None], np.array([30, 92, 112], dtype=np.float32) + (n2 * 8)[..., None], col)

    # ========== zástavba a průmysl
    urb_main = np.zeros_like(land)
    ind = np.zeros_like(land)
    id_masks = {}
    theta0 = np.full((H, Wd), math.radians(14.0), dtype=np.float32)
    style_masks = {k: np.zeros_like(land) for k in TOWN_STYLES}
    for f in D.settle:
        pr = f["properties"]
        r = A.ring(f["geometry"]["coordinates"][0])
        xs = [p[0] for p in r]
        ys = [p[1] for p in r]
        if max(xs) < c["x0"] or min(xs) > c["x0"] + c["w"] or max(ys) < c["y0"] or min(ys) > c["y0"] + c["h"]:
            continue
        m = raster.rasterize(g, [r])
        if pr["kind"] in ("industry", "port_area"):
            ind |= m
        else:
            urb_main |= m
        id_masks[pr["id"]] = id_masks.get(pr["id"], np.zeros_like(land)) | m
        style_masks[style_of(pr)] |= m
        theta0 = np.where(m, math.radians(TOWN_ANGLE.get(pr["id"], 14)), theta0)
    # silnice (rastr): stuhová zástavba podél komunikací
    road_img = Image.new("L", (Wd, H), 0)
    rdd = ImageDraw.Draw(road_img)
    for f in D.roads:
        if f["properties"]["section"] != "tunnel":
            rdd.line([g.to_px(*q) for q in f["geometry"]["coordinates"]], fill=255, width=3)
    road_near = raster.gauss((np.asarray(road_img) > 0).astype(np.float32), 22.0 / mpp) > 0.12
    # přístavy napojené na sídla: pás zástavby kolem pánve a koridor k sídlu
    style_extra = {k: np.zeros_like(land) for k in TOWN_STYLES}
    for hid, tid in HARBOR_LINKS:
        if tid not in id_masks:
            continue
        basin = [A.ring(f["geometry"]["coordinates"][0]) for f in D.pa if f["properties"]["id"] == hid and f["properties"].get("kind") == "harbor_basin"]
        if not basin:
            continue
        bm = raster.rasterize(g, [basin[0]])
        if not bm.any():
            continue
        ring_m = (raster.gauss(bm.astype(np.float32), 150.0 / mpp) > 0.10) & land & ~bm
        ys_b, xs_b = np.nonzero(bm)
        by_, bx_ = float(ys_b.mean()), float(xs_b.mean())
        ty_, tx_ = np.nonzero(id_masks[tid])
        k_ = int(np.argmin((ty_ - by_) ** 2 + (tx_ - bx_) ** 2))
        if math.hypot(ty_[k_] - by_, tx_[k_] - bx_) * mpp > 1500.0:
            continue
        cimg = Image.new("L", (Wd, H), 0)
        ImageDraw.Draw(cimg).line([(bx_, by_), (float(tx_[k_]), float(ty_[k_]))], fill=255, width=max(2, int(round(150.0 / mpp))))
        corr = (np.asarray(cimg) > 0) & land & ~bm
        sty_t = [s for s, m_ in style_masks.items() if (m_ & id_masks[tid]).any()][0]
        style_extra[sty_t] |= (ring_m | corr)
        urb_main |= (ring_m | corr)
    nz = raster.fbm(g, seed + 31, [(0.22, 1.0), (0.09, 0.7), (0.035, 0.45)])
    nz = nz / (np.abs(nz).max() + 1e-6)
    nlow = nrm(raster.fbm(g, seed + 34, [(0.80, 1.0), (0.30, 0.5)]))
    nzl = nrm(raster.fbm(g, seed + 35, [(0.90, 1.0), (0.45, 0.5)]))
    district = np.array([-0.30, 0.0, 0.34], dtype=np.float32)[np.clip(np.floor((nlow + 1.0) * 1.5).astype(int), 0, 2)]
    gs_all = {s: raster.gauss(m_.astype(np.float32), 150.0 / mpp) for s, m_ in style_masks.items()}
    names = list(style_masks)
    which = np.argmax(np.stack([gs_all[s] for s in names], axis=0), axis=0)
    ribbon = road_near & (np.max(np.stack(list(gs_all.values()), axis=0), axis=0) > 0.10) & land
    zone_any = np.zeros_like(land)
    for si, sty in enumerate(names):
        sm = style_masks[sty] | (ribbon & (which == si))
        ex = style_extra[sty]
        if not (sm.any() or ex.any()):
            continue
        smf = sm.astype(np.float32)
        exf = ex.astype(np.float32)
        zs = (((raster.gauss(smf, 170.0 / mpp) + 0.55 * nz + 0.30 * nzl) > 0.40) | ((raster.gauss(exf, 40.0 / mpp) + 0.30 * nz) > 0.32)) & land
        dens = np.clip(np.maximum(raster.gauss(smf, 70.0 / mpp) * 1.5, raster.gauss(exf, 30.0 / mpp) * 1.4) + 0.35 * nz - 0.15, 0.0, 1.0) * zs
        ys_, xs_ = np.nonzero(zs)
        if len(ys_) == 0:
            continue
        i0, i1, j0, j1 = max(0, ys_.min() - 4), min(H, ys_.max() + 5), max(0, xs_.min() - 4), min(Wd, xs_.max() + 5)
        stl = TOWN_STYLES[sty]
        sl = (slice(i0, i1), slice(j0, j1))
        th = theta0[sl] + (0.0 if stl.get("industrial") else district[sl])
        tex = town_texture(X[sl], Y[sl], th, mpp, seed + stl["salt"], stl)
        dn = dens[sl]
        sel = zs[sl]
        ga = (smoothstep(0.06, 0.45, dn) * sel)[..., None]
        sa = (tex["street"] * smoothstep(0.05, 0.30, dn) * sel)[..., None]
        present = (tex["rnd"] < (tex["fill"][0] + tex["fill"][1] * dn)) & sel
        ba = (tex["bld"] * present)[..., None]
        sh_ = (np.clip(np.roll(tex["bld"] * present, -max(1, int(round(9.0 / mpp))), axis=0) - tex["bld"] * present, 0, 1) * sel)[..., None]
        cc = col[sl]
        cc = cc * (1 - ga) + tex["ground"] * ga
        cc = cc * (1 - sa) + np.array(stl["street"], dtype=np.float32) * sa
        cc = cc * (1 - 0.34 * sh_)
        cc = cc * (1 - ba) + tex["roof"] * ba
        col[sl] = cc
        zone_any |= zs & (dens > 0.15)

    # ========== osvětlení, mraky v podobě stínů, barevné ladění
    shade = (0.46 + 0.72 * hs)[..., None]
    shade = np.where(zone_any[..., None], 0.84 + 0.18 * shade, shade)
    col = np.clip(col * shade, 0, 255)
    rgb = np.where(land[..., None], col, sea)
    cshadow = smoothstep(0.35, 0.78, nrm(raster.fbm(g, seed + 11, [(2.4, 1.0), (0.9, 0.4)])))
    rgb = rgb * (1.0 - 0.11 * cshadow[..., None])
    lum = rgb.mean(axis=2, keepdims=True)
    rgb = lum + (rgb - lum) * 0.95
    rgb = (rgb - 128.0) * 1.05 + 128.0 + (2.0 * n1)[..., None]
    grain = raster.fbm(g, seed + 10, [(0.004, 1.0)])
    rgb = np.clip(rgb + 2.2 * grain[..., None], 0, 255)
    img = Image.fromarray(rgb.astype(np.uint8), "RGB")

    # ========== vektorové detaily (supersampling 2×)
    ss = 2
    big_img = img.resize((Wd * ss, H * ss), Image.BICUBIC)
    d = ImageDraw.Draw(big_img, "RGBA")
    P2 = lambda pts: [(x * ss, y * ss) for x, y in poly_px(g, pts)]
    rng = np.random.default_rng(seed + 99)

    def line(pts, w_px, fill):
        if len(pts) > 1:
            d.line(P2(pts), fill=fill, width=max(1, int(round(w_px * ss))), joint="curve")

    def in_win(x, y, pad=0.2):
        return c["x0"] - pad <= x <= c["x0"] + c["w"] + pad and c["y0"] - pad <= y <= c["y0"] + c["h"] + pad

    for f in D.hydro:
        if f["geometry"]["type"] == "LineString":
            kind = f["properties"]["kind"]
            line([tuple(q) for q in f["geometry"]["coordinates"]], {"main": 2.4, "river": 2.0, "stream": 1.3}[kind] * 5.0 / mpp + 0.4, (66, 128, 176, 235))
    for f in D.trails:
        pr_ = f["properties"]
        cc = [tuple(q) for q in f["geometry"]["coordinates"]]
        if pr_["id"].startswith("TR"):
            line(cc, max(1.0, 2.2 / mpp), (176, 150, 112, 150))
        elif pr_["id"] == "SK-01":
            line(cc, max(2.0, 40.0 / mpp), (150, 176, 104, 170))
            line(cc, max(1.0, 3.0 / mpp), (70, 70, 72, 190))
    for f in D.roads:
        cc = [tuple(q) for q in f["geometry"]["coordinates"]]
        cl = f["properties"]["class"]
        if f["properties"]["section"] == "tunnel":
            continue
        wpx = max({"R1": 9.0, "R2": 7.0, "R3": 4.8}[cl] / mpp, {"R1": 2.0, "R2": 1.7, "R3": 1.3}[cl])
        line(cc, wpx + 1.0, (70, 66, 60, 130))
        line(cc, wpx, (222, 218, 208, 255) if cl != "R3" else (196, 190, 178, 255))
    for f in D.rail:
        pr = f["properties"]
        if pr["line"] == "L3" or pr["section"] in ("tunnel", "cave", "undersea", "glass_gallery"):
            continue
        cc = [tuple(q) for q in f["geometry"]["coordinates"]]
        line(cc, 4.0 / mpp + 0.6, (50, 50, 52, 255))
        line(cc, 1.5 / mpp + 0.2, (220, 220, 216, 255))
    # samoty podél silnic (rozptýlená populace): 2–3 budovy s dvorem v lukách a polích
    rng2 = np.random.default_rng(seed + 123)
    for f in D.roads:
        pr_ = f["properties"]
        if pr_["class"] == "R1" or pr_["section"] == "tunnel":
            continue
        for (sx, sy, tx, ty) in arc_samples([tuple(q) for q in f["geometry"]["coordinates"]], 0.55, rng2):
            if rng2.random() > 0.55:
                continue
            nx_, ny_ = -ty, tx
            off = rng2.uniform(0.028, 0.060) * (1 if rng2.random() < 0.5 else -1)
            fx, fy = sx + nx_ * off, sy + ny_ * off
            if not in_win(fx, fy, 0.0):
                continue
            pxx, pyy = g.to_px(fx, fy)
            ix_, iy_ = int(pxx), int(pyy)
            if not (0 <= ix_ < Wd and 0 <= iy_ < H) or not land[iy_, ix_] or cls[iy_, ix_] not in (0, 2, 3, 5) or zone_any[iy_, ix_] or ind[iy_, ix_] or lake[iy_, ix_]:
                continue
            k = ss / mpp
            ang = math.atan2(ty, tx)
            ca_, sa_ = math.cos(ang), math.sin(ang)
            cx0, cy0 = pxx * ss, pyy * ss

            def quad(cu, cv, lu_, lv_):
                """Obdélník o polovičních stranách lu_, lv_ (m), střed posunutý o (cu, cv) m, pootočený podél silnice."""
                return [(cx0 + (cu + a_) * k * ca_ - (cv + b_) * k * sa_, cy0 + (cu + a_) * k * sa_ + (cv + b_) * k * ca_)
                        for a_, b_ in ((-lu_, -lv_), (lu_, -lv_), (lu_, lv_), (-lu_, lv_))]
            d.polygon(quad(0, 0, 24, 17), fill=(150, 146, 116, 255))
            for bx2, by2, lu2, lv2 in ((-9, -4, 8, 5), (9, 5, 7, 4)):
                d.polygon(quad(bx2 - 1, by2 + 4, lu2, lv2), fill=(40, 40, 34, 70))
                d.polygon(quad(bx2, by2, lu2, lv2), fill=[(166, 98, 74, 255), (118, 116, 120, 255), (190, 182, 170, 255)][int(rng2.integers(0, 3))])
    if mpp <= 6.0:
        spacing = 0.024
        gx_ = np.arange(c["x0"], c["x0"] + c["w"], spacing)
        gy_ = np.arange(c["y0"], c["y0"] + c["h"], spacing)
        TX, TY = np.meshgrid(gx_, gy_)
        TX = TX + rng2.uniform(-0.011, 0.011, TX.shape)
        TY = TY + rng2.uniform(-0.011, 0.011, TY.shape)
        grove = nrm(raster.fbm(g, seed + 41, [(0.25, 1.0), (0.09, 0.6)]))
        tpx = np.clip(((TX - g.x0) / g.dx).astype(np.int64), 0, Wd - 1)
        tpy = np.clip(((TY - g.y0) / g.dx).astype(np.int64), 0, H - 1)
        okc = np.isin(cls[tpy, tpx], (0, 2, 5)) & land[tpy, tpx] & ~zone_any[tpy, tpx] & ~road_near[tpy, tpx] & ~beaches[tpy, tpx] & ~lake[tpy, tpx] & (Dsea[tpy, tpx] > 0.03)
        prob = 0.05 + 0.50 * smoothstep(0.15, 0.75, grove[tpy, tpx])
        keep = okc & (rng2.random(TX.shape) < prob)
        for qx, qy in zip(TX[keep], TY[keep]):
            cx_, cy_ = g.to_px(float(qx), float(qy))
            cx_, cy_ = cx_ * ss, cy_ * ss
            r_ = rng2.uniform(3.5, 7.0) / mpp * ss
            d.ellipse([cx_ - r_ * 0.8, cy_ - r_ * 1.9, cx_ + r_ * 0.9, cy_ - r_ * 0.2], fill=(30, 40, 26, 70))
            gcol = [(52, 96, 54, 255), (64, 106, 58, 255), (44, 84, 50, 255), (76, 112, 60, 255)][int(rng2.integers(0, 4))]
            d.ellipse([cx_ - r_, cy_ - r_, cx_ + r_, cy_ + r_], fill=gcol)
            if r_ > 3.4:
                d.ellipse([cx_ - r_ * 0.55, cy_ - r_ * 0.55, cx_ + r_ * 0.1, cy_ + r_ * 0.1], fill=(gcol[0] + 14, gcol[1] + 18, gcol[2] + 10, 255))
    basins, piers = [], []
    for f in D.pa:
        pr, gm = f["properties"], f["geometry"]
        if pr.get("kind") == "harbor_basin":
            basins.append(A.ring(gm["coordinates"][0]))
        elif pr.get("kind") == "breakwater":
            line([tuple(q) for q in gm["coordinates"]], 20.0 / mpp, (170, 172, 170, 255))
        elif pr.get("kind") == "pier":
            r_ = A.ring(gm["coordinates"][0])
            piers.append((pr["id"], r_))
            d.polygon(P2(r_), fill=(160, 160, 158, 255))
        elif pr.get("part") == "runway" and pr["id"] in ("A-01", "A-02"):
            d.polygon(P2(A.ring(gm["coordinates"][0])), fill=(86, 86, 90, 255) if pr["id"] == "A-01" else (104, 140, 76, 255))
        elif pr.get("part") == "apron":
            d.polygon(P2(A.ring(gm["coordinates"][0])), fill=(176, 176, 174, 255))
        elif pr.get("part") == "terminal":
            d.polygon(P2(A.ring(gm["coordinates"][0])), fill=(210, 206, 198, 255))
    a01 = D.reg["A-01"]
    line([(a01["x_km"] - 0.85, a01["y_km"]), (a01["x_km"] + 0.85, a01["y_km"])], 1.0 / mpp + 0.4, (240, 240, 236, 220))
    # lodě v přístavních pánvích
    for ring_ in basins:
        xs = [p[0] for p in ring_]
        ys = [p[1] for p in ring_]
        if not in_win((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, 0.0):
            continue
        n_boats = int(np.clip(geom.area(ring_) * 900, 5, 40))
        placed = 0
        tries = 0
        while placed < n_boats and tries < 400:
            tries += 1
            px_, py_ = rng.uniform(min(xs), max(xs)), rng.uniform(min(ys), max(ys))
            if not geom.point_in_poly((px_, py_), ring_):
                continue
            cx, cy = g.to_px(px_, py_)
            cx, cy = cx * ss, cy * ss
            L = max(2.2, 9.0 / mpp) * ss
            Wb = max(1.2, 3.2 / mpp) * ss
            ang = rng.uniform(0, math.pi)
            dx, dy = math.cos(ang) * L / 2, math.sin(ang) * L / 2
            colb = [(244, 244, 240, 255), (232, 236, 244, 255), (210, 70, 60, 255), (60, 100, 170, 255)][int(rng.integers(0, 4))]
            d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=colb, width=max(1, int(round(Wb))))
            placed += 1
    # nákladní loď u mola (kontejnerový areál je ve výplni zástavby)
    for pid, r_ in piers[:3]:
        if pid != "I-03":
            continue
        xs = [p[0] for p in r_]
        ys = [p[1] for p in r_]
        cx_, cy_ = sum(xs) / len(xs), sum(ys) / len(ys)
        if not in_win(cx_, cy_):
            continue
        # loď podél mola: obdélník 170 × 26 m posunutý od mola
        ax = (r_[2][0] - r_[0][0], r_[2][1] - r_[0][1])
        L = math.hypot(*ax) or 1.0
        px = (-(ax[1]) / L, ax[0] / L)
        cxm, cym = g.to_px(cx_ + px[0] * 0.030, cy_ + px[1] * 0.030)
        dirx, diry = (r_[1][0] - r_[0][0], r_[1][1] - r_[0][1])
        dl = math.hypot(dirx, diry) or 1.0
        pass
        hull = 170.0 / mpp * ss / 2
        wid = max(1.6, 26.0 / mpp) * ss / 2
        ang = math.atan2(ax[1], ax[0])
        ux, uy = math.cos(ang), math.sin(ang)
        vx, vy = -uy, ux
        corners = [(cxm * ss - ux * hull - vx * wid, cym * ss - uy * hull - vy * wid), (cxm * ss + ux * hull - vx * wid, cym * ss + uy * hull - vy * wid),
                   (cxm * ss + ux * hull + vx * wid, cym * ss + uy * hull + vy * wid), (cxm * ss - ux * hull + vx * wid, cym * ss - uy * hull + vy * wid)]
        d.polygon(corners, fill=(46, 52, 62, 255))
        d.polygon([(cxm * ss - ux * hull * 0.9 - vx * wid * 0.55, cym * ss - uy * hull * 0.9 - vy * wid * 0.55), (cxm * ss + ux * hull * 0.1 - vx * wid * 0.55, cym * ss + uy * hull * 0.1 - vy * wid * 0.55),
                   (cxm * ss + ux * hull * 0.1 + vx * wid * 0.55, cym * ss + uy * hull * 0.1 + vy * wid * 0.55), (cxm * ss - ux * hull * 0.9 + vx * wid * 0.55, cym * ss - uy * hull * 0.9 + vy * wid * 0.55)], fill=(186, 70, 54, 255))
        break
    # Paraland: aquapark, hrad, zřícenina (rozměry v metrech)
    for pid, kind in (("PL-04", "aqua"), ("PL-02", "castle"), ("PL-06", "ruin")):
        o = D.reg[pid]
        if not in_win(o["x_km"], o["y_km"], 0.0):
            continue
        cx, cy = g.to_px(o["x_km"], o["y_km"])
        cx, cy = cx * ss, cy * ss
        k = ss / mpp                                    # metry → pixely supersamplovaného obrazu
        if kind == "aqua":
            for dx, dy, rx_, ry_, colr in ((-70, -18, 34, 20, (40, 204, 224, 255)), (-8, 20, 42, 24, (30, 176, 214, 255)), (56, -10, 26, 18, (86, 218, 228, 255))):
                d.ellipse([cx + (dx - rx_) * k, cy + (dy - ry_) * k, cx + (dx + rx_) * k, cy + (dy + ry_) * k], fill=colr, outline=(236, 236, 230, 255))
            d.rectangle([cx + 84 * k, cy - 28 * k, cx + 104 * k, cy + 10 * k], fill=(220, 214, 200, 255))
        elif kind == "castle":
            d.polygon([(cx - 46 * k, cy - 26 * k), (cx + 46 * k, cy - 26 * k), (cx + 46 * k, cy + 26 * k), (cx - 46 * k, cy + 26 * k)], fill=(168, 160, 146, 255), outline=(98, 92, 84, 255))
            d.rectangle([cx - 24 * k, cy - 14 * k, cx + 24 * k, cy + 14 * k], fill=(122, 112, 100, 255))
            d.rectangle([cx - 14 * k, cy - 8 * k, cx + 14 * k, cy + 8 * k], fill=(168, 84, 64, 255))
            for sx in (-1, 1):
                for sy in (-1, 1):
                    d.ellipse([cx + sx * 46 * k - 8 * k, cy + sy * 26 * k - 8 * k, cx + sx * 46 * k + 8 * k, cy + sy * 26 * k + 8 * k], fill=(190, 182, 168, 255), outline=(98, 92, 84, 255))
            d.polygon([(cx - 46 * k, cy + 26 * k), (cx + 46 * k, cy + 26 * k), (cx + 52 * k, cy + 36 * k), (cx - 40 * k, cy + 36 * k)], fill=(60, 64, 56, 120))
        else:
            d.polygon([(cx - 30 * k, cy + 16 * k), (cx - 10 * k, cy - 20 * k), (cx + 24 * k, cy - 6 * k), (cx + 12 * k, cy + 20 * k)], fill=(150, 140, 126, 255), outline=(96, 90, 80, 255))
            d.polygon([(cx - 22 * k, cy + 12 * k), (cx - 8 * k, cy - 12 * k), (cx + 16 * k, cy - 2 * k), (cx + 8 * k, cy + 14 * k)], fill=(112, 124, 80, 255))
    img = big_img.resize((Wd, H), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))

    # ========== uložení
    if spec.get("internal"):
        WORK_SAT.mkdir(parents=True, exist_ok=True)
        img.save(WORK_SAT / f"{name}.png", optimize=True)
        print(f"{name}: {Wd}×{H} px @ {mpp} m (interní), za {time.time() - t0:.0f}s")
        return
    OUT.mkdir(parents=True, exist_ok=True)
    stem = "S-00_overview" if name == "S-00" else f"{name}_base"
    img.save(OUT / f"{stem}.png", optimize=True)
    img.save(OUT / f"{stem}.jpg", quality=94, subsampling=0, optimize=True)
    if clouds:
        cl_img = add_clouds(np.asarray(img).astype(np.float32), g, land, Dsea, seed + 21, mpp)
        Image.fromarray(np.clip(cl_img, 0, 255).astype(np.uint8)).save(OUT / f"{stem}_clouds.jpg", quality=92, optimize=True)
    Image.fromarray((land.astype(np.uint8) * 255), "L").save(OUT / f"{name}_mask_land.png", optimize=True)
    cmap = np.zeros((H, Wd), dtype=np.uint8)
    cmap[land] = cls[land]
    cmap[land & (urb_main | zone_any) & ~ind] = 10
    cmap[land & ind] = 11
    cmap[lake] = 8
    cm = Image.fromarray(cmap, "L")
    pal = [0] * 768
    for k, hx in {0: "#0a3a70", 1: "#224a26", 2: "#96ac54", 3: "#b0a05c", 4: "#76904a", 5: "#74824a", 6: "#80786c", 7: "#e2d6ac", 8: "#1c5c70", 10: "#a08070", 11: "#9a9c9a"}.items():
        pal[k * 3:k * 3 + 3] = [int(hx[i:i + 2], 16) for i in (1, 3, 5)]
    cm.putpalette(pal)
    cm.save(OUT / f"{name}_mask_classes.png", optimize=True)
    geo = {"id": name, "title": spec["title"], "status": "proposed", "px": [Wd, H], "meters_per_pixel": mpp, "window_km": spec["canvas"],
           "pixel_to_km": "x_km = x0 + (px + 0.5) * mpp/1000 ; y_km = y0 + (py + 0.5) * mpp/1000 (sever nahoře, východ vpravo)", "orientation": "kolmý pohled shora (nadir), sever nahoře",
           "land_area_km2": round(float(land.sum() * (mpp / 1000.0) ** 2), 2), "disclaimer": "SIMULOVANÁ satelitní vizualizace fiktivního ostrova, ne skutečná družicová data",
           "atlas_version": canon.ATLAS_VERSION, "coast_sha256": D.fro["coast_sha256"]}
    (OUT / f"{name}_georef.json").write_text(json.dumps(geo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{name}: {Wd}×{H} px @ {mpp} m, za {time.time() - t0:.0f}s; souš {geo['land_area_km2']} km²")


# ------------------------------------------------------------------ šikmý pohled (voxelový renderer)
def bilinear(arr, g, fx, fy):
    """Bilineární vzorek z pole arr (ny, nx[, 3]) ve zlomkových indexech (fx, fy)."""
    j0 = np.clip(np.floor(fx).astype(int), 0, g.nx - 2)
    i0 = np.clip(np.floor(fy).astype(int), 0, g.ny - 2)
    tx, ty = fx - j0, fy - i0
    if arr.ndim == 3:
        tx, ty = tx[:, None], ty[:, None]
    return arr[i0, j0] * (1 - tx) * (1 - ty) + arr[i0, j0 + 1] * tx * (1 - ty) + arr[i0 + 1, j0] * (1 - tx) * ty + arr[i0 + 1, j0 + 1] * tx * ty


def vnoise(x, y, cell, salt):
    """Hladký hodnotový šum 0..1 (x, y v metrech, cell = velikost buňky v metrech)."""
    u, v = x / cell, y / cell
    iu, iv = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
    fu, fv = u - iu, v - iv
    fu, fv = fu * fu * (3 - 2 * fu), fv * fv * (3 - 2 * fv)

    def hv(a, b):
        return hash2(a, b, salt) / 65535.0
    return (hv(iu, iv) * (1 - fu) + hv(iu + 1, iv) * fu) * (1 - fv) + (hv(iu, iv + 1) * (1 - fu) + hv(iu + 1, iv + 1) * fu) * fv


def far_sea(D):
    """Barva moře na velkém hrubém plátně (100 m/px) stejnou funkcí jako nadirové rendery – pro oblast mimo okno S-00 u šikmých pohledů."""
    g = raster.Grid(0.1, canvas={"x0": -25.0, "y0": -25.0, "w": 80.0, "h": 70.0})
    pts = np.vstack([raster.resample_polyline(D.o["main"], 0.04), raster.resample_polyline(D.o["para"], 0.04)])
    Dsea = raster.coarse_nearest(g, pts, factor=6)
    beach_pts = [raster.resample_polyline(b["ring"], 0.04) for b in coast_beaches(D)]
    shelf = 0.42 + 0.58 * np.exp(-raster.coarse_nearest(g, np.vstack(beach_pts), factor=6) / 1.5) if beach_pts else np.full_like(Dsea, 0.6)
    return {"rgb": interp_stops(Dsea / shelf, SEA_STOPS).astype(np.float32), "grid": g}


def load_source(name, spec, D, W):
    """Nadirový obraz (PNG), výška a sklon pro okno `name` – zdroj pro šikmý pohled."""
    g = raster.Grid(spec["mpp"] / 1000.0, canvas=spec["canvas"])
    path = WORK_SAT / f"{name}.png" if spec.get("internal") else OUT / ("S-00_overview.png" if name == "S-00" else f"{name}_base.png")
    rgb = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    land = raster.rasterize(g, [D.o["main"]]) | raster.rasterize(g, [D.o["para"]])
    z = np.where(land, np.maximum(crop_resize(W.z, W.g, g), 0.0), 0.0).astype(np.float32)
    slope = np.hypot(*np.gradient(z, spec["mpp"])).astype(np.float32)
    return {"rgb": rgb, "z": z, "slope": slope, "grid": g}


def sample_srcs(srcs, px, py, far):
    """Vzorek (výška, barva, sklon). Základ: dálkové moře `far` (mimo okna je jen moře); nejhrubší zdroj (poslední) ho překrývá uvnitř svého okna,
    jemnější zdroje se kladou přes něj s měkkým okrajem 0,6 km."""
    n = px.shape[0]
    zz = np.zeros(n, dtype=np.float32)
    sl = np.zeros(n, dtype=np.float32)
    gf = far["grid"]
    fxf = np.clip((px - gf.x0) / gf.dx - 0.5, 0, gf.nx - 1.001)
    fyf = np.clip((py - gf.y0) / gf.dx - 0.5, 0, gf.ny - 1.001)
    cc = bilinear(far["rgb"], gf, fxf, fyf).astype(np.float32)
    for s in reversed(srcs):
        g = s["grid"]
        fx = (px - g.x0) / g.dx - 0.5
        fy = (py - g.y0) / g.dx - 0.5
        ins = (fx >= 0) & (fx < g.nx - 1) & (fy >= 0) & (fy < g.ny - 1)
        if not ins.any():
            continue
        edge = np.minimum.reduce([fx, g.nx - 1 - fx, fy, g.ny - 1 - fy])[ins] * g.dx
        a = smoothstep(0.0, 0.6, edge)
        zs_ = bilinear(s["z"], g, fx[ins], fy[ins])
        cs_ = bilinear(s["rgb"], g, fx[ins], fy[ins])
        ss_ = bilinear(s["slope"], g, fx[ins], fy[ins])
        zz[ins] = zz[ins] * (1 - a) + zs_ * a
        cc[ins] = cc[ins] * (1 - a[:, None]) + cs_ * a[:, None]
        sl[ins] = sl[ins] * (1 - a) + ss_ * a
    return zz, cc, sl


def render_oblique(srcs, far, cam, name, size=(1800, 1000), ss=2, zexag=OBLIQUE_ZEXAG):
    """Šikmý pohled z DEM a nadirového obrazu (voxel-space, zepředu dozadu). Kamera má posunutý objektiv: svislice zůstávají svislé,
    obzor leží v řádku horizon·výška. Mimo okna zdrojů je hluboké moře, daleko haze, za dmax kreslí obloha a mořská dálka."""
    t0 = time.time()
    Wo, Ho = size[0] * ss, size[1] * ss
    f = (Wo / 2) / math.tan(math.radians(cam["fov"]) / 2)
    yh = cam["horizon"] * Ho
    hd = math.radians(cam["heading"])
    hx, hy = math.sin(hd), -math.cos(hd)
    rx, ry = -hy, hx
    lat = (np.arange(Wo) - Wo / 2) / f
    cam_h = cam["h"]
    haze_c = np.array([186, 210, 228], dtype=np.float32)
    hmax = 0.90                                      # haze nikdy nepřekryje moře úplně → pod obzorem zůstane znatelné moře
    deepc = np.array(SEA_STOPS[-1][1], dtype=np.float32)
    sky_hor = np.array([200, 220, 236], dtype=np.float32)
    sky_top = np.array([86, 136, 202], dtype=np.float32)
    rock = np.array([112, 102, 90], dtype=np.float32)
    rows = np.arange(Ho)[:, None]
    img = np.zeros((Ho, Wo, 3), dtype=np.float32)
    ybuf = np.full(Wo, Ho, dtype=np.int32)
    d = 0.9 * f * max(cam_h - 650.0, 60.0) / max(Ho - yh, 1.0)
    while d < cam["dmax"]:
        px = cam["x"] + (hx * d + rx * lat * d) / 1000.0
        py = cam["y"] + (hy * d + ry * lat * d) / 1000.0
        zz, cc, sl = sample_srcs(srcs, px, py, far)
        rw = (smoothstep(0.55, 1.4, sl) * 0.65)[:, None]
        cc = cc * (1 - rw) + rock * rw
        cc = cc * (1 - 0.18 * rw)
        amp = 0.11 * max(0.0, 1.0 - d / 9000.0)
        if amp > 0.003:
            nn = 0.4 * vnoise(px * 1000.0, py * 1000.0, 1.4, 3) + 0.35 * vnoise(px * 1000.0, py * 1000.0, 3.5, 5) + 0.25 * vnoise(px * 1000.0, py * 1000.0, 11.0, 9)
            cc = cc * (1.0 + amp * (nn - 0.5)[:, None] * 2.0)
        hz = hmax * (1.0 - math.exp(-((d / 24000.0) ** 1.4)))
        cc = cc * (1 - hz) + haze_c * hz
        top = np.clip(np.floor(yh + f * (cam_h - zz * zexag) / d).astype(np.int32), 0, Ho)
        active = top < ybuf
        if active.any():
            span = ybuf - top
            idx = np.nonzero(active)[0]
            for k in range(int(span[idx].max())):
                ii = idx[span[idx] > k]
                if len(ii) == 0:
                    break
                img[top[ii] + k, ii] = cc[ii]
            ybuf = np.where(active, top, ybuf)
        d += max(1.5, min(0.8 * d * d / (f * max(cam_h, 1.0)), 0.004 * d))
    und = rows < ybuf[None, :]
    tt = np.clip((yh - rows) / max(yh, 1.0), 0.0, 1.0)
    sky = sky_hor[None, None, :] * (1 - tt[..., None]) + sky_top[None, None, :] * tt[..., None]
    dr = f * cam_h / np.maximum(rows - yh, 1.0)                    # vzdálenost rovinného moře v daném řádku (za dmax)
    hzr = (hmax * (1.0 - np.exp(-((dr / 24000.0) ** 1.4))))[..., None]
    far = deepc[None, None, :] * (1 - hzr) + haze_c[None, None, :] * hzr
    fill = np.where((rows >= yh)[..., None], far, sky)
    img = np.where(und[..., None], fill, img)
    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").resize(size, Image.LANCZOS)
    out.save(OUT / f"{name}.jpg", quality=93, optimize=True)
    meta = {"id": name, "status": "proposed", "type": "šikmý pohled z DEM (simulace, ne družicová data)", "description": cam["desc"],
            "camera": {k: v for k, v in cam.items() if k not in ("desc", "sources")}, "sources": cam["sources"], "vertical_exaggeration": zexag,
            "size_px": list(size), "atlas_version": canon.ATLAS_VERSION,
            "camera_note": ("x, y v km (x východ, y jih, počátek SZ roh rámce 24×16 km); heading ve stupních od severu po směru hodin; h = výška kamery v m n. m.; "
                            "horizon = poloha obzoru jako zlomek výšky obrazu; kamera s posunutým objektivem (bez naklopení); fov = vodorovné zorné pole ve stupních; "
                            f"výška terénu je zvětšena {zexag}× (jinak by 560 m hory vypadaly jako pahorky)")}
    (OUT / f"{name}_camera.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{name}: {size[0]}×{size[1]} px, za {time.time() - t0:.0f}s")


def build_obliques(D, W):
    specs = {"S-00": OVERVIEW, "S-01": WINDOWS["S-01"], "S-02": WINDOWS["S-02"], **INTERNAL}
    cache = {}
    far = far_sea(D)
    for nm, cam in OBLIQUES.items():
        srcs = []
        for sname in cam["sources"]:
            if sname not in cache:
                cache[sname] = load_source(sname, specs[sname], D, W)
            srcs.append(cache[sname])
        render_oblique(srcs, far, cam, nm)


_BEACH_CACHE = {}


def coast_beaches(D):
    if "b" not in _BEACH_CACHE:
        _BEACH_CACHE["b"] = [{"ring": A.ring(f["geometry"]["coordinates"][0])} for f in D.coast if f["properties"]["class"] == "beach"]
    return _BEACH_CACHE["b"]


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    D = A.Data()
    W = he.World()
    if which in ("all", "S-01"):
        render("S-01", WINDOWS["S-01"], D, W, clouds=True)
    if which in ("all", "S-02"):
        render("S-02", WINDOWS["S-02"], D, W)
    if which in ("all", "S-00"):
        render("S-00", OVERVIEW, D, W, clouds=True)
    if which in ("all", "X-pen") or (which == "obliques" and not (WORK_SAT / "X-pen.png").exists()):
        render("X-pen", INTERNAL["X-pen"], D, W)
    if which in ("all", "obliques"):
        build_obliques(D, W)


if __name__ == "__main__":
    main()
