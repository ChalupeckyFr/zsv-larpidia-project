"""Sídla a jejich půdorysy (F3). Půdorysy vznikají z hladkých „bloků“ (blobs), terénu a pobřeží, ne z čtverců.

NÁVRH (proposed): kanon určuje jen povinná města (Praha, Cimprlichovo Hradiště, Havlišovo Doupě, Ōru Maito), roli hlavního města,
průmyslovou zónu a Paraland (historické městečko, hrad/zámeček, zřícenina, resorty, aquapark, marina). Velikosti jsou modelové:
rozdělení 32 000 obyvatel je pracovní model, ne sčítání.
"""
from __future__ import annotations

import math

import numpy as np

import geom
import raster

# id, název, druh, obyvatelé (model), cílová plocha km², bloky (cx, cy, rx, ry, rot°), stav existence, stav jména, poznámka
SETTLEMENTS = [
    {"id": "C-01", "name": "Larpington", "kind": "capital", "pop": 12000, "area": 4.8,
     "blobs": [(16.08, 12.16, 1.65, 1.00, 0), (14.45, 12.05, 1.05, 0.85, 0), (15.90, 11.10, 1.00, 0.75, 8),
               (17.45, 12.10, 1.05, 0.85, 0), (16.10, 13.00, 1.15, 0.65, 0)],
     "exist": "approved", "name_status": "proposed", "ref": "C-01 + C-03..C-06"},
    {"id": "T-01", "name": "Praha", "kind": "town", "pop": 4500, "area": 1.7,
     "blobs": [(16.80, 7.84, 0.95, 0.75, 15), (16.15, 8.20, 0.55, 0.40, 0)], "exist": "approved", "name_status": "approved", "ref": "T-01"},
    {"id": "T-02", "name": "Cimprlichovo Hradiště", "kind": "town", "pop": 2000, "area": 0.9,
     "blobs": [(11.52, 11.52, 0.75, 0.55, -20), (11.95, 11.15, 0.40, 0.30, 0)], "exist": "approved", "name_status": "approved", "ref": "T-02"},
    {"id": "T-03", "name": "Havlišovo Doupě", "kind": "village", "pop": 700, "area": 0.30,
     "blobs": [(4.08, 9.60, 0.42, 0.20, 55), (4.40, 9.25, 0.28, 0.16, 40)], "exist": "approved", "name_status": "approved", "ref": "T-03"},
    {"id": "T-04", "name": "Ōru Maito", "name_ja": "オールマイト", "kind": "town", "pop": 2300, "area": 0.9,
     "blobs": [(13.44, 3.68, 0.80, 0.50, 0), (13.65, 3.05, 0.40, 0.25, 0)], "exist": "approved", "name_status": "approved", "ref": "T-04"},
    {"id": "T-05", "name": "Aokawa", "name_ja": "青川", "kind": "town", "pop": 2600, "area": 1.0,
     "blobs": [(17.52, 4.24, 0.85, 0.55, 20), (18.10, 3.85, 0.45, 0.30, 25)], "exist": "proposed", "name_status": "proposed", "ref": "T-05"},
    {"id": "T-06", "name": "Hoshimachi", "name_ja": "星町", "kind": "town", "pop": 1600, "area": 0.7,
     "blobs": [(19.30, 4.00, 0.65, 0.40, 0), (18.75, 3.75, 0.35, 0.22, 20)], "exist": "proposed", "name_status": "proposed", "ref": "bible other_towns"},
    {"id": "I-01", "name": "Zelená průmyslová zóna", "kind": "industry", "pop": 600, "area": 3.6,
     "blobs": [(19.68, 8.48, 1.25, 0.80, -10), (21.00, 9.55, 0.95, 0.50, -20)], "exist": "approved", "name_status": "proposed", "ref": "I-01 + I-02"},
    {"id": "I-03", "name": "Nákladní přístav (areál)", "kind": "port_area", "pop": 0, "area": 0.45,
     "blobs": [(22.20, 10.05, 0.55, 0.32, 20)], "exist": "proposed", "name_status": "proposed", "ref": "I-03"},
]

# Paraland (lokální u,v vůči těžišti): název, druh, obyvatelé, plocha, bloky
PARA_SETTLEMENTS = [
    {"id": "PL-01", "name": "Staré městečko Paralandu (pracovní)", "kind": "old_town", "pop": 900, "area": 0.20,
     "blobs": [(0.00, -1.25, 0.38, 0.20, 0), (0.30, -1.15, 0.25, 0.16, 10)], "exist": "approved", "name_status": "proposed", "ref": "bible tourism_island"},
    {"id": "PL-03", "name": "Resorty jih (pracovní)", "kind": "resort", "pop": 300, "area": 0.38,
     "blobs": [(-0.55, 1.00, 0.55, 0.22, 0), (0.45, 1.12, 0.40, 0.18, 8)], "exist": "approved", "name_status": "proposed", "ref": "bible tourism_island"},
    {"id": "PL-05", "name": "Marina a přístavní vesnice (pracovní)", "kind": "village", "pop": 200, "area": 0.14,
     "blobs": [(-2.05, 0.05, 0.22, 0.28, 0)], "exist": "approved", "name_status": "proposed", "ref": "bible paraland_connection / GEOGRAPHY"},
]

POP_TOTAL_MODEL = 32000


class SubGrid:
    def __init__(self, g, i0, i1, j0, j1):
        self.x0 = g.x0 + j0 * g.dx
        self.y0 = g.y0 + i0 * g.dx
        self.dx = g.dx
        self.i0, self.i1, self.j0, self.j1 = i0, i1, j0, j1


def _blob_field(X, Y, blobs, k):
    s = np.zeros(X.shape, dtype=np.float32)
    for (cx, cy, rx, ry, rot) in blobs:
        a = math.radians(rot)
        c, sn = math.cos(a), math.sin(a)
        u = (X - cx) * c + (Y - cy) * sn
        v = -(X - cx) * sn + (Y - cy) * c
        s = np.maximum(s, np.exp(-((u / (rx * k)) ** 2 + (v / (ry * k)) ** 2)))
    return s


def footprint(world, noise, blobs, target_km2, slope_max=13.0, min_ring_km2=0.02):
    """Vrací největší okruh půdorysu (km), plocha ≈ target. Respektuje souš, jezero a sklon."""
    g = world.g
    xs = [b[0] for b in blobs]
    ys = [b[1] for b in blobs]
    pad = 2.4
    j0, j1 = max(0, int((min(xs) - pad - g.x0) / g.dx)), min(g.nx, int((max(xs) + pad - g.x0) / g.dx))
    i0, i1 = max(0, int((min(ys) - pad - g.y0) / g.dx)), min(g.ny, int((max(ys) + pad - g.y0) / g.dx))
    sg = SubGrid(g, i0, i1, j0, j1)
    X = (g.x0 + (np.arange(j0, j1) + 0.5) * g.dx).astype(np.float32)[None, :] * np.ones((i1 - i0, 1), dtype=np.float32)
    Y = (g.y0 + (np.arange(i0, i1) + 0.5) * g.dx).astype(np.float32)[:, None] * np.ones((1, j1 - j0), dtype=np.float32)
    ok = world.land[i0:i1, j0:j1] & ~world.lake[i0:i1, j0:j1] & (world.S[i0:i1, j0:j1] < slope_max)
    okf = raster.gauss(ok.astype(np.float32), 4)
    nz = noise[i0:i1, j0:j1]
    best = None
    lo, hi = 0.4, 2.6
    for _ in range(9):
        k = (lo + hi) / 2
        field = _blob_field(X, Y, blobs, k) * (1.0 + 0.22 * nz) * okf
        rings = raster.contour_lines(sg, field, 0.5)
        areas = [(geom.area(r[:-1]) if r[0] == r[-1] and len(r) > 4 else 0.0, r) for r in rings]
        areas = [a for a in areas if a[0] >= min_ring_km2]
        total = sum(a[0] for a in areas)
        best = areas
        if total < target_km2:
            lo = k
        else:
            hi = k
    if not best:
        return []
    out = []
    for A, r in sorted(best, key=lambda a: -a[0]):
        pts = raster.simplify(r, 0.008)
        pts = raster.chaikin(pts[:-1], closed=True, iters=1)
        out.append(pts)
    return out


def build_settlements(world, seed=11):
    rng = np.random.default_rng(seed)
    noise = raster.fbm(world.g, 4242, [(0.9, 1.0), (0.35, 0.5)])
    noise = (noise / (np.abs(noise).max() + 1e-6)).astype(np.float32)
    res = []
    for s in SETTLEMENTS:
        rings = footprint(world, noise, s["blobs"], s["area"])
        res.append({**s, "rings": rings, "area_km2": round(sum(geom.area(r) for r in rings), 3)})
    for s in PARA_SETTLEMENTS:
        blobs = [(*world.para(u, v), rx, ry, rot + 24.0) for (u, v, rx, ry, rot) in s["blobs"]]
        rings = footprint(world, noise, blobs, s["area"], slope_max=11.0)
        s2 = {**s, "blobs": blobs}
        res.append({**s2, "rings": rings, "area_km2": round(sum(geom.area(r) for r in rings), 3)})
    # osady v polích (bez názvu)
    centers = [(q["blobs"][0][0], q["blobs"][0][1]) for q in res]
    farm = np.argwhere(((world.cls == 3) | (world.cls == 4)) & (world.S < 5.0) & (world.D > 0.7) & world.land)
    order = rng.permutation(len(farm))
    ham = []
    for idx in order:
        i, j = farm[idx]
        x, y = world.g.x0 + (j + 0.5) * world.g.dx, world.g.y0 + (i + 0.5) * world.g.dx
        if all(math.dist((x, y), c) > 1.6 for c in centers + [(h["x"], h["y"]) for h in ham]) and not world.in_lake(x, y):
            ham.append({"x": float(x), "y": float(y)})
        if len(ham) >= 6:
            break
    for k, h in enumerate(ham, 1):
        blobs = [(h["x"], h["y"], 0.22, 0.14, float(rng.uniform(0, 180)))]
        rings = footprint(world, noise, blobs, 0.07, slope_max=9.0, min_ring_km2=0.01)
        res.append({"id": f"HM-{k:02d}", "name": "osada (bez názvu)", "kind": "hamlet", "pop": 200, "area": 0.07, "blobs": blobs, "rings": rings,
                    "area_km2": round(sum(geom.area(r) for r in rings), 3), "exist": "proposed", "name_status": "needs_decision", "ref": "atlas_new"})
    return res
