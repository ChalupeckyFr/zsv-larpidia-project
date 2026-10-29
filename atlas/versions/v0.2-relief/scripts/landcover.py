"""Pokryv krajiny a třídy pobřeží. NÁVRH (proposed): kanon určuje jen typy prvků (lesy, louky, pláže, útesy, rýže na terasách).

Třídy rastru (uint8): 0 moře · 1 les · 2 louka · 3 pole · 4 rýžové terasy (historické, O17) · 5 křoviny/trávy · 6 skála ·
7 pláž · 8 jezero · 9 řeka · (10+ zástavba a průmysl doplní F3).
"""
from __future__ import annotations

import math

import numpy as np

import geom
import raster
from raster import smoothstep

CLASSES = {0: "sea", 1: "forest", 2: "meadow", 3: "farmland", 4: "terraces", 5: "scrub", 6: "rock", 7: "beach", 8: "lake", 9: "river"}
CLASS_NAMES_CS = {0: "moře", 1: "les", 2: "louka", 3: "pole", 4: "rýžové terasy (historické)", 5: "křoviny a travnatá plocha",
                  6: "skála", 7: "písčitá pláž", 8: "jezero", 9: "řeka"}
LC_COLORS = {1: "#b9d19e", 2: "#dfe8b4", 3: "#f1e4b0", 4: "#e6d49a", 5: "#e3e1c2", 6: "#c9c1b0", 7: "#f4e8bd"}
SEED = 20261030


def compute_landcover(T, z, hy, override: dict | None = None):
    """Vrací uint8 rastr tříd a pomocná pole. `override` = {třída: maska} (např. zástavba z F3)."""
    g = T.g
    X, Y = T.X, T.Y
    E = z
    S = raster.slope_deg(z, g.dx * 1000.0)
    nA = raster.fbm(g, SEED, [(1.3, 1.0), (0.55, 0.5)])
    nB = raster.fbm(g, SEED + 1, [(1.0, 1.0), (0.45, 0.5)])
    nA = nA / (np.abs(nA).max() + 1e-6)
    nB = nB / (np.abs(nB).max() + 1e-6)
    wx = 1.0 - smoothstep(5.0, 18.0, X)
    m3 = T.pos("M-03")
    d_m3 = np.hypot(X - m3[0], Y - m3[1])

    forest = smoothstep(30.0, 150.0, E) * (0.78 + 0.22 * smoothstep(5.0, 20.0, S)) * (0.55 + 0.45 * wx) * (1 + 0.30 * nA) * 1.45
    forest = np.maximum(forest, 0.50 * smoothstep(0.35, 0.75, nB) * (1.0 - 0.5 * smoothstep(0, 60, E)))   # remízky a lesíky v nížině
    # Paraland: les hlavně na východě a na kopcích
    c = T.para_centroid
    para = T.para_mask
    east = smoothstep(-0.2, 1.6, (X - c[0]) * math.cos(math.radians(24)) + (Y - c[1]) * math.sin(math.radians(24)))
    forest = np.where(para, (0.25 + 0.95 * east) * (1 + 0.3 * nA) * (0.5 + 0.5 * smoothstep(8, 60, E)), forest)

    def reg(cx, cy, sx, sy, a):
        return a * np.exp(-(((X - cx) / sx) ** 2 + ((Y - cy) / sy) ** 2))

    region_farm = (reg(8.5, 11.2, 4.6, 2.4, 1.0) + reg(15.0, 9.0, 3.0, 2.5, 0.55) + reg(20.5, 8.0, 2.2, 3.0, 0.45)
                   + reg(15.5, 4.7, 3.5, 1.5, 0.45) + 0.30)
    farm = (smoothstep(3.0, 15.0, E) * (1.0 - smoothstep(110.0, 200.0, E)) * (1.0 - smoothstep(4.0, 14.0, S)) * region_farm
            * (0.7 + 0.3 * nB))
    farm = np.where(para, 0.18 * (1 + 0.3 * nB) * (1 - east) * (E > 3), farm)
    meadow = (smoothstep(120.0, 240.0, E) * (1.0 - smoothstep(450.0, 560.0, E)) * (0.30 + 2.4 * np.exp(-(d_m3 / 1.7) ** 2))
              * (1 + 0.45 * nB) * (1.0 - smoothstep(24.0, 36.0, S)))
    scrub = 0.42 + 0.35 * (1.0 - smoothstep(0.0, 0.45, T.D)) + 0.05 * nA
    scores = np.stack([forest, meadow, farm, scrub], axis=0)
    cls = np.array([1, 2, 3, 5], dtype=np.uint8)[np.argmax(scores, axis=0)]

    # terasy (historické rýžové) – v JZ podhůří na mírném svahu, jen kde je pole
    sw = (X < 12.8) & (Y > 8.6) & (~para)
    terr = (cls == 3) & (S > 4.5) & (S < 19.0) & sw
    cls = np.where(terr, 4, cls).astype(np.uint8)
    # skála: příkré svahy
    rock = (S > 34.0) | ((E > 380) & (S > 26.0))
    cls = np.where(rock, 6, cls).astype(np.uint8)
    # vodstva a pláže
    cls = np.where(~T.land, 0, cls).astype(np.uint8)
    if hy is not None:
        cls = np.where(hy["lake_mask"], 8, cls).astype(np.uint8)
    if override:
        for k, mask in override.items():
            cls = np.where(mask, k, cls).astype(np.uint8)
    return cls, {"slope": S}


# ---------------------------------------------------------------- vektorizace tříd
def class_polygons(g, cls, class_id, sigma_px=3.0, simplify_m=14.0, min_area_km2=0.01):
    """Polygony jedné třídy (kruhy; díry řeší even-odd) z vyhlazené masky přes marching squares."""
    mask = (cls == class_id).astype(np.float32)
    if mask.sum() == 0:
        return []
    field = raster.gauss(mask, sigma_px)
    rings = []
    for line in raster.contour_lines(g, field, 0.5):
        if len(line) < 5:
            continue
        pts = raster.simplify(line, simplify_m / 1000.0)
        if len(pts) < 4:
            continue
        if pts[0] != pts[-1]:
            pts = pts + [pts[0]]
        if geom.area(pts[:-1]) < min_area_km2:
            continue
        rings.append(raster.chaikin(pts[:-1], closed=True, iters=1))
    return rings


# ---------------------------------------------------------------- pobřeží: útesy, pláže
def _outward_normals_open(pts):
    n = len(pts)
    out = []
    for i in range(n):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        out.append((ty / L, -tx / L))
    return out


def coast_classes(outline: dict, seed=SEED):
    """Úseky pobřeží podle typu: pláže jako pásy (polygony), útesy a skalnaté pobřeží jako polyline."""
    rng = np.random.default_rng(seed)
    beaches, cliffs, rocky = [], [], []
    for isl, key in (("main", "main"), ("para", "para")):
        poly = outline[key]
        types = outline[f"{key}_types"]
        n = len(poly)
        # souvislé úseky stejného typu (cyklicky)
        start = 0
        while start < n and types[start] == types[(start - 1) % n]:
            start += 1
            if start >= n:
                break
        i = start
        count = 0
        while count < n:
            t = types[i % n]
            j = i
            seg = []
            while count < n and types[j % n] == t:
                seg.append(poly[j % n])
                j += 1
                count += 1
            if t == "beach" and len(seg) > 8:
                nrm = _outward_normals_open(seg)
                L = len(seg)
                inner = []
                for k, ((x, y), (nx, ny)) in enumerate(zip(seg, nrm)):
                    taper = smoothstep(0, 12, k) * smoothstep(0, 12, L - 1 - k)
                    w = (0.055 + 0.050 * (0.5 + 0.5 * math.sin(k * 0.11 + i))) * taper
                    inner.append((x - nx * w, y - ny * w))
                beaches.append({"island": isl, "ring": seg + list(reversed(inner))})
            elif t == "cliff" and len(seg) > 6:
                cliffs.append({"island": isl, "line": seg})
            elif t == "rocky" and len(seg) > 6:
                rocky.append({"island": isl, "line": seg})
            i = j
    return {"beaches": beaches, "cliffs": cliffs, "rocky": rocky}
