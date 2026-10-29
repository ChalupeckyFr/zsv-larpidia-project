"""Hydrografie Larpidie a Paralandu: toky, vodopád N-03, přehrada N-04 s hrází. NÁVRH (proposed), výšky jsou modelové.

Koryta se odvozují z terénu (nikdy neteče do kopce): bed = terén − zářez, vyhlazeno a vynuceno monotónní klesání.
Vodopád a hráz jsou skokové úseky profilu. Hladina přehrady je plochá.
"""
from __future__ import annotations

import math

import numpy as np

import geom
import raster
from raster import smoothstep

# id, pracovní název, druh, zdroj a průchozí body (km), typ konce ("coast" = napojit na nejbližší pobřeží)
RIVER_DEFS = [
    {"id": "W-01", "name": "Hlavní horská řeka (pracovní)", "kind": "main", "end": "coast", "island": "main",
     "pts": [(9.60, 5.70), (9.85, 6.40), (10.05, 7.15), (10.22, 7.95), (10.32, 8.62), (10.60, 8.95), (10.90, 9.25)],
     "after_dam": [(12.18, 10.65), (12.00, 11.05), (11.72, 11.35), (11.68, 11.75), (11.66, 12.20), (11.70, 12.70)]},
    {"id": "W-02", "name": "Aokawa – Modrá řeka (pracovní)", "kind": "river", "end": "coast", "island": "main",
     "pts": [(14.90, 6.30), (15.90, 5.50), (16.80, 4.75), (17.50, 4.25), (18.15, 3.80), (18.70, 3.55)]},
    {"id": "W-03", "name": "Severní potok (pracovní)", "kind": "stream", "end": "coast", "island": "main",
     "pts": [(8.05, 5.00), (8.05, 4.55)]},
    {"id": "W-04", "name": "Potok Havlišova Doupěte (pracovní)", "kind": "stream", "end": "coast", "island": "main",
     "pts": [(4.95, 8.35), (4.45, 9.00), (4.05, 9.55)]},
    {"id": "W-05", "name": "Pražský potok (pracovní)", "kind": "stream", "end": "coast", "island": "main",
     "pts": [(15.00, 7.00), (16.20, 7.60), (17.20, 8.50), (18.40, 9.90), (19.30, 11.00)]},
]
WATERFALL = {"id": "N-03", "drop_m": 36.0, "length_km": 0.16}
DAM = {"drop_m": 24.0, "length_km": 0.14, "crest_above_lake_m": 5.0}
LAKE_CENTERLINE = [(10.90, 9.25, 0.10), (11.20, 9.52, 0.38), (11.55, 9.80, 0.56), (11.90, 10.05, 0.44), (12.12, 10.30, 0.18)]


def bilinear(z: np.ndarray, grid: raster.Grid, xs, ys):
    xs, ys = np.asarray(xs, dtype=np.float64), np.asarray(ys, dtype=np.float64)
    fx = (xs - grid.x0) / grid.dx - 0.5
    fy = (ys - grid.y0) / grid.dx - 0.5
    j0 = np.clip(np.floor(fx).astype(int), 0, grid.nx - 2)
    i0 = np.clip(np.floor(fy).astype(int), 0, grid.ny - 2)
    tx, ty = fx - j0, fy - i0
    return (z[i0, j0] * (1 - tx) * (1 - ty) + z[i0, j0 + 1] * tx * (1 - ty)
            + z[i0 + 1, j0] * (1 - tx) * ty + z[i0 + 1, j0 + 1] * tx * ty)


def smooth1d(v: np.ndarray, sigma_pts: float) -> np.ndarray:
    if sigma_pts < 0.5:
        return v
    r = int(3 * sigma_pts)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma_pts) ** 2)
    k /= k.sum()
    pad = np.pad(v, r, mode="edge")
    return np.convolve(pad, k, mode="valid")


def path_length(pts):
    d = [0.0]
    for a, b in zip(pts, pts[1:]):
        d.append(d[-1] + math.dist(a, b))
    return np.array(d)


def snap_to_coast(pt, main_poly, para_poly):
    d1 = geom.nearest_on_poly(pt, main_poly)
    d2 = geom.nearest_on_poly(pt, para_poly)
    return d1[1] if d1[0] <= d2[0] else d2[1]


def lake_polygon(centerline, seed=7):
    """Břeh přehrady: nepravidelný pás kolem osy; šířka (km) v bodech osy."""
    rng = np.random.default_rng(seed)
    left, right = [], []
    P = [(x, y) for x, y, _ in centerline]
    W = [w for _, _, w in centerline]
    dense = geom.catmull_rom_open(P, spacing=0.05)
    # šířka interpolovaná podle nejbližšího řídicího bodu (lineárně v oblouku)
    s_ctrl = path_length(P)
    s_dense = path_length(dense)
    wd = np.interp(s_dense, s_ctrl * (s_dense[-1] / s_ctrl[-1]), W)
    for i, (x, y) in enumerate(dense):
        a, b = dense[max(i - 1, 0)], dense[min(i + 1, len(dense) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / L, tx / L
        wl = 0.5 * wd[i] * (1 + 0.28 * rng.uniform(-1, 1))
        wr = 0.5 * wd[i] * (1 + 0.28 * rng.uniform(-1, 1))
        left.append((x + nx * wl, y + ny * wl))
        right.append((x - nx * wr, y - ny * wr))
    poly = left + [dense[-1]] + list(reversed(right)) + [dense[0]]
    poly = [p for k, p in enumerate(poly) if k == 0 or p != poly[k - 1]]
    sm = geom.catmull_rom_closed(geom.ensure_clockwise_on_map(poly)[::3], spacing=0.03)
    return geom.ensure_clockwise_on_map([(x, y) for x, y, _, _ in sm])


def build_hydro(T, z: np.ndarray):
    """Vrací (z_nové, hydro) – hydro obsahuje toky (hustá polyline + koryto), jezero, hráz, vodopád, masky."""
    g = T.g
    z = z.copy()
    rivers = []
    main_poly, para_poly = T.o["main"], T.o["para"]

    # --- Paraland: dva krátké toky z východních kopců (lokální souřadnice → svět)
    import relief_model as rm
    c = T.para_centroid
    pw = lambda u, v: rm.para_to_world(u, v, c)
    defs = list(RIVER_DEFS) + [
        {"id": "W-06", "name": "Paralandský potok sever (pracovní)", "kind": "stream", "end": "coast", "island": "para",
         "pts": [pw(1.10, -0.10), pw(0.55, -0.70), pw(0.00, -1.15)]},
        {"id": "W-07", "name": "Paralandský potok jih (pracovní)", "kind": "stream", "end": "coast", "island": "para",
         "pts": [pw(1.05, 0.35), pw(0.60, 0.95), pw(0.30, 1.30)]},
    ]

    lake_poly = lake_polygon(LAKE_CENTERLINE)
    lake_mask = raster.rasterize(g, [lake_poly])
    zs = raster.gauss(z, 4)                       # vyhlazený terén pro koryta

    out_rivers = []
    lake_level = None
    for rd in defs:
        pts = list(rd["pts"])
        poly_end = main_poly if rd["island"] == "main" else para_poly
        if rd["end"] == "coast" and "after_dam" not in rd:
            pts.append(geom.nearest_on_poly(pts[-1], poly_end)[1])
        if "after_dam" in rd:
            # horní část (zdroj → jezero) + dolní část (hráz → ústí); mezi nimi jezero
            up = geom.catmull_rom_open(pts, 0.025)
            dn_pts = list(rd["after_dam"]) + [geom.nearest_on_poly(rd["after_dam"][-1], poly_end)[1]]
            dn = geom.catmull_rom_open(dn_pts, 0.025)
            segs = [("up", up), ("down", dn)]
        else:
            segs = [("all", geom.catmull_rom_open(pts, 0.025))]
        for part, dense in segs:
            P = np.array(dense, dtype=np.float64)
            s = path_length(dense)
            zt = bilinear(zs, g, P[:, 0], P[:, 1])
            # meandry: jen v nížinách a s nulovou výchylkou na koncích (kotvy zůstávají na místě)
            if rd["kind"] in ("river", "stream") and len(P) > 12:
                rng = np.random.default_rng(abs(hash(rd["id"])) % (2 ** 31) if False else sum(map(ord, rd["id"])))
                ph1, ph2 = rng.uniform(0, 6.28, 2)
                tx = np.gradient(P[:, 0]); ty = np.gradient(P[:, 1]); L = np.hypot(tx, ty) + 1e-9
                nx_, ny_ = -ty / L, tx / L
                low = 1 - smoothstep(35, 110, zt)
                taper = np.minimum(1.0, np.minimum(s, s[-1] - s) / 0.35)
                off = 0.10 * (0.65 * np.sin(2 * np.pi * s / 0.95 + ph1) + 0.35 * np.sin(2 * np.pi * s / 0.38 + ph2)) * low * taper
                P = np.stack([P[:, 0] + nx_ * off, P[:, 1] + ny_ * off], axis=1)
                dense = [tuple(p) for p in P]
                s = path_length(dense)
                zt = bilinear(zs, g, P[:, 0], P[:, 1])
            inc = 3.0 + 4.0 * smoothstep(60, 250, zt)
            bed = smooth1d(zt - inc, 12)
            bed = np.maximum(np.minimum.accumulate(bed), 0.3)
            out_rivers.append({"def": rd, "part": part, "P": P, "s": s, "bed": bed})

    # --- vodopád N-03 na W-01 (horní část): skok profilu v místě N-03
    wf_xy = T.pos("N-03")
    for r in out_rivers:
        if r["def"]["id"] == "W-01" and r["part"] == "up":
            P, s, bed = r["P"], r["s"], r["bed"]
            k = int(np.argmin(np.hypot(P[:, 0] - wf_xy[0], P[:, 1] - wf_xy[1])))
            top = float(bed[k])
            step = WATERFALL["drop_m"] * smoothstep(s[k], s[k] + WATERFALL["length_km"], s)
            bed2 = np.minimum.accumulate(bed - step)
            r["bed"] = bed2
            lake_level = float(bed2[-1])                  # řeka vtéká do jezera na úrovni hladiny
            waterfall = {"x": float(P[k, 0]), "y": float(P[k, 1]), "top_m": top, "bottom_m": float(bed2[min(len(bed2) - 1, k + int(WATERFALL['length_km'] / 0.025) + 1)]),
                         "drop_m": WATERFALL["drop_m"]}
    # --- dolní tok pod hrází: skok o výšku hráze a návaz na terén
    for r in out_rivers:
        if r["def"]["id"] == "W-01" and r["part"] == "down":
            bed = r["bed"]
            foot = lake_level - DAM["drop_m"]
            bed = np.minimum(bed, foot - 0.0 * bed)               # pod hrází nejvýše úroveň paty hráze
            bed = np.minimum.accumulate(np.minimum(bed, foot))
            # plynulý sestup z paty hráze k terénu dál po proudu
            r["bed"] = bed

    # --- karvování údolí (kromě plochy jezera)
    for r in out_rivers:
        P, bed = r["P"], r["bed"]
        x0, y0 = P.min(axis=0) - 1.3
        x1, y1 = P.max(axis=0) + 1.3
        i0, j0 = max(0, int((y0 - g.y0) / g.dx)), max(0, int((x0 - g.x0) / g.dx))
        i1, j1 = min(g.ny, int((y1 - g.y0) / g.dx) + 1), min(g.nx, int((x1 - g.x0) / g.dx) + 1)
        Xw, Yw = T.X[i0:i1, j0:j1], T.Y[i0:i1, j0:j1]
        flat = np.stack([Xw.ravel(), Yw.ravel()], axis=1).astype(np.float32)
        best = np.full(len(flat), np.inf, dtype=np.float32)
        arg = np.zeros(len(flat), dtype=np.int32)
        Pf = P.astype(np.float32)
        for a in range(0, len(Pf), 60):
            d2 = (flat[:, None, 0] - Pf[None, a:a + 60, 0]) ** 2 + (flat[:, None, 1] - Pf[None, a:a + 60, 1]) ** 2
            jn = np.argmin(d2, axis=1)
            m = d2[np.arange(len(flat)), jn]
            better = m < best
            best = np.where(better, m, best)
            arg = np.where(better, jn + a, arg)
        dist_m = np.sqrt(best).reshape(Xw.shape) * 1000.0
        bz = bed[arg].reshape(Xw.shape)
        k = 0.10 + 0.22 * smoothstep(80, 300, bz)
        valley = bz + k * np.maximum(0.0, dist_m - 9.0)
        win = z[i0:i1, j0:j1]
        # vrcholy se nekarvují: váha 0 do 0,5 km od vrcholu, plná od 1,1 km
        dpk = np.full(Xw.shape, 9.0, dtype=np.float32)
        for pk in ("M-01", "M-02", "M-03"):
            px_, py_ = T.pos(pk)
            dpk = np.minimum(dpk, np.hypot(Xw - px_, Yw - py_))
        w_pk = smoothstep(0.5, 1.1, dpk)
        cut = np.maximum(0.0, win - valley) * w_pk
        new = np.where(T.land[i0:i1, j0:j1], win - cut, win)
        z[i0:i1, j0:j1] = new
        r["dist_m_win"] = None

    # --- přehrada: dno a bankování
    if lake_level is not None:
        ys, xs = np.nonzero(lake_mask)
        i0, i1, j0, j1 = ys.min() - 40, ys.max() + 40, xs.min() - 40, xs.max() + 40
        sub = lake_mask[i0:i1, j0:j1]
        # vzdálenost od břehu uvnitř (hrubě přes polyline břehu)
        bank = raster.resample_polyline(lake_poly, 0.03)
        Xs, Ys = T.X[i0:i1, j0:j1], T.Y[i0:i1, j0:j1]
        flat = np.stack([Xs.ravel(), Ys.ravel()], axis=1)
        d = np.full(len(flat), np.inf, dtype=np.float32)
        for a in range(0, len(bank), 80):
            dd = np.hypot(flat[:, None, 0] - bank[None, a:a + 80, 0], flat[:, None, 1] - bank[None, a:a + 80, 1])
            d = np.minimum(d, dd.min(axis=1))
        d = d.reshape(Xs.shape) * 1000.0                      # m od břehu
        depth = 2.0 + 11.0 * smoothstep(0, 140, d)
        win = z[i0:i1, j0:j1]
        inside = sub
        win = np.where(inside, lake_level - depth, win)
        bankz = lake_level + DAM["crest_above_lake_m"] * smoothstep(0, 60, d) * 0 + 0.07 * d
        outside_bank = (~inside) & (d < 260)
        win = np.where(outside_bank, np.maximum(win, lake_level + 0.5 + 0.07 * d), win)
        z[i0:i1, j0:j1] = win

    z = np.where(T.land, z, 0.0).astype(np.float32)
    z = np.maximum(z, 0.0)
    return z, {"rivers": out_rivers, "lake_poly": lake_poly, "lake_mask": lake_mask, "lake_level": lake_level,
               "waterfall": waterfall if lake_level is not None else None}
