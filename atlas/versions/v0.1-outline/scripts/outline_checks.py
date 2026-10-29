"""Kontroly obrysu: body tabulky vůči pobřeží, silueta (zátoky, mys, poloostrov), průliv, plochy."""
from __future__ import annotations

import math

import canon
import geom

# Očekávání pro body tabulky: ("inland", min_km) = uvnitř a ≥ min_km od pobřeží;
# ("coast", max_km) = uvnitř a ≤ max_km od pobřeží (přístav, vyhlídka, napojení).
EXPECT = {
    "M-01": ("inland", 0.8), "M-02": ("inland", 1.2), "M-03": ("inland", 1.5),
    "N-01": ("coast", 0.40), "N-02": ("inland", 2.0), "N-03": ("inland", 2.0), "N-04": ("inland", 2.0),
    "C-01": ("inland", 0.8), "C-02": ("coast", 0.25),
    "C-03": ("inland", 0.4), "C-04": ("inland", 0.4), "C-05": ("inland", 0.4), "C-06": ("inland", 0.3),
    "T-01": ("inland", 2.0), "T-02": ("inland", 1.0), "T-03": ("inland", 0.55),
    "T-04": ("inland", 0.35), "T-05": ("inland", 0.6),
    "I-01": ("inland", 1.0), "I-02": ("inland", 0.35), "I-03": ("coast", 0.25),
    "A-01": ("inland", 0.6), "P-01": ("coast", 0.45),
}


def check_points(main, rows=None):
    rows = rows or canon.geo_ref_table()
    out = []
    for r in rows:
        p = (r["x_km"], r["y_km"])
        inside = geom.point_in_poly(p, main)
        d, q, _ = geom.nearest_on_poly(p, main)
        kind, lim = EXPECT[r["id"]]
        if kind == "inland":
            ok = inside and d >= lim
        else:                       # pobřežní bod: na hraně nebo těsně uvnitř
            ok = (inside or d < 1e-6) and d <= lim
        out.append({"id": r["id"], "inside": inside, "d_coast_km": round(d, 3), "rule": f"{kind} {lim}", "ok": bool(ok),
                    "nearest_coast": (round(q[0], 3), round(q[1], 3))})
    return out


def peninsula_width(main, tip, toward_dir, back_km=1.5):
    """Šířka souše kolmo k ose poloostrova ve vzdálenosti back_km od hrotu."""
    ux, uy = toward_dir                     # směr od hlavního ostrova k hrotu
    cx, cy = tip[0] - ux * back_km, tip[1] - uy * back_km
    px, py = -uy, ux
    step = 0.02
    # vyhledej nejbližší vnitřní bod osy a rozšiř oběma směry
    t0 = None
    for k in range(0, 80):
        for s in (1, -1):
            q = (cx + px * k * step * s, cy + py * k * step * s)
            if geom.point_in_poly(q, main):
                t0 = k * step * s
                break
        if t0 is not None:
            break
    if t0 is None:
        return 0.0
    lo = hi = t0
    while geom.point_in_poly((cx + px * (hi + step), cy + py * (hi + step)), main) and hi - t0 < 12:
        hi += step
    while geom.point_in_poly((cx + px * (lo - step), cy + py * (lo - step)), main) and t0 - lo < 12:
        lo -= step
    return hi - lo


def silhouette(main, para_dir_deg, rows=None):
    """Ověření siluety z GEOGRAPHY_AND_CANON.md (PROPOSED): pocket analýza + mys + poloostrov."""
    pk = geom.pockets(main, min_depth=0.35)
    north = [p for p in pk if p["centroid"][1] < 7.0 and p["depth_km"] >= 0.45]
    tb = {r["id"]: r for r in (rows or canon.geo_ref_table())}
    harbor = tb["C-02"]
    south = [p for p in pk if math.dist(p["centroid"], (harbor["x_km"], harbor["y_km"])) < 3.8 and p["depth_km"] >= 0.45]
    west = min(main, key=lambda p: p[0])
    n01 = tb["N-01"]
    ux, uy = math.cos(math.radians(para_dir_deg)), math.sin(math.radians(para_dir_deg))
    tip = max(main, key=lambda p: p[0] * ux + p[1] * uy)
    return {
        "pockets": [{"depth_km": round(p["depth_km"], 2), "mouth_km": round(p["mouth_km"], 2),
                     "centroid": (round(p["centroid"][0], 2), round(p["centroid"][1], 2)),
                     "area_km2": round(p["area_km2"], 2)} for p in pk[:8]],
        "north_bays": len(north), "north_bays_ok": len(north) >= 2,
        "south_bay_depth_km": round(max([p["depth_km"] for p in south], default=0.0), 2), "south_bay_ok": bool(south),
        "west_cape": {"x": round(west[0], 2), "y": round(west[1], 2),
                      "dist_to_N-01_km": round(math.dist(west, (n01["x_km"], n01["y_km"])), 2),
                      "ok": math.dist(west, (n01["x_km"], n01["y_km"])) < 1.2},
        "se_tip": (round(tip[0], 2), round(tip[1], 2)),
        "peninsula_width_km": round(peninsula_width(main, tip, (ux, uy), 1.5), 2),
    }


def bbox_report(poly):
    x0, y0, x1, y1 = geom.bbox(poly)
    return {
        "x_km": [round(x0, 2), round(x1, 2)], "y_km": [round(y0, 2), round(y1, 2)],
        "w_km": round(x1 - x0, 2), "h_km": round(y1 - y0, 2),
        "x_pct": [round(x0 / canon.FRAME_W_KM * 100, 1), round(x1 / canon.FRAME_W_KM * 100, 1)],
        "y_pct": [round(y0 / canon.FRAME_H_KM * 100, 1), round(y1 / canon.FRAME_H_KM * 100, 1)],
        "fill_of_bbox": round(geom.area(poly) / ((x1 - x0) * (y1 - y0)), 3),
    }
