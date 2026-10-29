"""Silnice, stezky a cyklotrasy (F3). NÁVRH (proposed): kanon určuje okružní pobřežní silnici s odbočkami na vyhlídky/pláže/lesy
a hustou síť cyklotras a pěších tras s přístupy k pramenům. Trasy hledá A* nad skutečným terénem (sklon, voda, pobřeží).
"""
from __future__ import annotations

import math

import numpy as np

import geom
import h_rail as hr
import pathfind
import raster


def _along(poly, step):
    pts = [poly[0]]
    acc = 0.0
    for a, b in zip(poly, poly[1:] + [poly[0]]):
        L = math.dist(a, b)
        acc += L
        if acc >= step:
            pts.append(b)
            acc = 0.0
    return pts


def r1_anchors(world, step_km=3.1, inset=0.30):
    poly = world.o["main"]
    n = len(poly)
    c02 = world.pos("C-02")
    i_start = min(range(n), key=lambda i: math.dist(poly[i], c02))
    i_inlet = min(range(n), key=lambda i: math.dist(poly[i], (19.95, 12.0)))
    i_p01 = min(range(n), key=lambda i: math.dist(poly[i], world.pos("P-01")))
    seq = []
    i = i_start
    while i != i_inlet:
        seq.append(i)
        i = (i + 1) % n
    seq.append(i_inlet)
    # vybrané kotvy po ~step_km
    anchors, acc = [], 0.0
    prev = seq[0]
    anchors.append(seq[0])
    for idx in seq[1:]:
        acc += math.dist(poly[prev], poly[idx])
        prev = idx
        if acc >= step_km:
            anchors.append(idx)
            acc = 0.0
    if anchors[-1] != i_inlet:
        anchors.append(i_inlet)
    pts = []
    for idx in anchors:
        p = poly[idx]
        nrm = hr.inward_normal_at(poly, p)
        pts.append((p[0] + nrm[0] * inset, p[1] + nrm[1] * inset))
    # šíje poloostrova: z dna zátoky na jižní břeh u P-01
    p01 = world.pos("P-01")
    n01 = hr.inward_normal_at(poly, poly[i_p01])
    pts.append((poly[i_p01][0] + n01[0] * 0.25, poly[i_p01][1] + n01[1] * 0.25))
    pts.append(pts[0])
    return pts, {"start": i_start, "inlet": i_inlet, "p01": i_p01}


def build_roads(world, forest_mask):
    env = world.env
    roads = []
    road_mask = np.zeros(env.z.shape, dtype=bool)

    def add(rid, name, cls, pts, island="main", note="", status="proposed"):
        roads.append({"id": rid, "name": name, "class": cls, "island": island, "pts": pts, "note": note, "status": status})
        pathfind.mark_path(env, road_mask, pts, 1)

    # ---- R1: okružní pobřežní silnice
    anchors, info = r1_anchors(world)
    cost_r1 = pathfind.road_cost(env, coast_target=0.30, coast_w=3.0, forest_mask=forest_mask, max_slope=13.0, zmax=300.0, tunnel_slope=55.0)
    r1 = pathfind.route(env, cost_r1, anchors, smooth_iters=2, simplify_m=10.0)
    add("RD-R1", "Okružní pobřežní silnice R1", "R1", r1, note="kanon: dlouhá okružní pobřežní silnice (approved); v útesovém SZ vede vnitrozemím a krátkými tunely")

    cost2 = lambda: pathfind.road_cost(env, bonus_mask=road_mask, forest_mask=forest_mask)
    P = world.pos
    spots = hr.best_spot
    capN = spots(world, 15.95, 10.65, 0.3, 4.0)
    capE = spots(world, 17.95, 11.80, 0.3, 4.0)
    capW = spots(world, 14.00, 11.70, 0.3, 4.0)
    praha = spots(world, P("T-01")[0], P("T-01")[1] + 0.15, 0.3, 4.0)
    aokawa = spots(world, P("T-05")[0], P("T-05")[1] + 0.2, 0.3, 5.0)
    oru = spots(world, P("T-04")[0] + 0.1, P("T-04")[1] + 0.3, 0.3, 4.0)
    hoshi = spots(world, 19.30, 4.30, 0.3, 4.0)
    t02 = spots(world, P("T-02")[0], P("T-02")[1] + 0.1, 0.3, 4.0)
    t03 = spots(world, P("T-03")[0] + 0.1, P("T-03")[1] + 0.25, 0.4, 7.0)
    airport = spots(world, 19.60, 6.90, 0.3, 3.0)
    i01 = spots(world, 19.30, 8.90, 0.3, 4.0)
    i02 = spots(world, 20.80, 9.45, 0.3, 4.0)
    i03 = spots(world, 22.10, 10.15, 0.3, 4.0)
    horska = spots(world, 9.35, 6.55, 0.4, 5.0)

    # ---- hlavní spojnice (třída R2)
    conn = [
        ("RD-01", "Larpington – Praha", [capN, praha]),
        ("RD-02", "Praha – Aokawa", [praha, aokawa]),
        ("RD-03", "Aokawa – Ōru Maito", [aokawa, oru]),
        ("RD-04", "Aokawa – Hoshimachi", [aokawa, hoshi]),
        ("RD-05", "Praha – letiště – Zelená zóna", [praha, airport, i01]),
        ("RD-06", "Zelená zóna – závod – nákladní přístav", [i01, i02, i03]),
        ("RD-07", "Larpington Východ – Zelená zóna", [capE, i01]),
        ("RD-08", "Larpington Západ – Čimprlichovo Hradiště", [capW, t02]),
        ("RD-09", "Čimprlichovo Hradiště – přehrada – Horská stanice", [t02, spots(world, 12.55, 10.35, 0.3, 5.0), spots(world, 10.9, 8.9, 0.4, 7.0), horska]),
        ("RD-10", "Čimprlichovo Hradiště – Havlišovo Doupě", [t02, t03]),
        ("RD-11", "Larpington – hlavní tepna západ–východ", [capW, spots(world, 16.08, 12.16, 0.3, 4.0), capE]),
        ("RD-12", "Larpington – tepna sever–jih k přístavu", [capN, spots(world, 16.08, 12.16, 0.3, 4.0), spots(world, 16.30, 13.65, 0.3, 4.0)]),
    ]
    for rid, name, pts in conn:
        path = pathfind.route(env, cost2(), pts, smooth_iters=2, simplify_m=10.0)
        add(rid, name, "R2", path)
    return roads, road_mask, {"anchors": anchors, "info": info, "r1_n_anchors": len(anchors)}


def road_sections(world, pts, max_slope=13.0, min_tunnel_m=110):
    """Úseky silnice: surface / tunnel (strmý terén) / bridge (přes tok nebo jezero)."""
    d = hr.dense(pts, 0.025)
    S = np.array([world.slope_at(x, y) for x, y in d])
    k = 5
    Sm = np.array([np.median(S[max(0, i - k):i + k + 1]) for i in range(len(S))])
    riv = []
    for x, y in d:
        i, j = world.g.cell_of(x, y)
        riv.append(bool(world.river[max(0, i - 1):i + 2, max(0, j - 1):j + 2].any()))
    lab = ["tunnel" if s > max_slope else ("bridge" if r else "surface") for s, r in zip(Sm, riv)]
    runs, start = [], 0
    for i in range(1, len(lab) + 1):
        if i == len(lab) or lab[i] != lab[start]:
            L = sum(math.dist(d[q], d[q + 1]) for q in range(start, min(i, len(d) - 1))) * 1000.0
            runs.append([start, i - 1, lab[start], L])
            start = i
    for r_ in runs:
        if r_[2] == "tunnel" and r_[3] < min_tunnel_m:
            r_[2] = "surface"
    merged = []
    for r_ in runs:
        if merged and merged[-1][2] == r_[2]:
            merged[-1][1] = r_[1]
            merged[-1][3] += r_[3]
        else:
            merged.append(list(r_))
    return [{"section": m[2], "pts": d[m[0]:m[1] + 1], "length_m": round(m[3])} for m in merged if m[1] > m[0]]


def nearest_on_polyline(pts, p):
    best = (1e9, None)
    for a, b in zip(pts, pts[1:]):
        d, q = geom.dist_point_seg(p, a, b)
        if d < best[0]:
            best = (d, q)
    return best


def spur(world, road_pts, target, road_mask, forest_mask, rid, name, note="", cls="R3", island="main"):
    env = world.env
    d, q = nearest_on_polyline(road_pts, target)
    cost = pathfind.road_cost(env, bonus_mask=road_mask, forest_mask=forest_mask, max_slope=20.0)
    path = pathfind.route(env, cost, [q, target], smooth_iters=2, simplify_m=8.0)
    return {"id": rid, "name": name, "class": cls, "island": island, "pts": path, "note": note, "status": "proposed"}


def build_trails(world):
    env = world.env
    tcost = pathfind.trail_cost(env)
    trails = []

    def add(tid, name, kind, pts, note="", island="main", surface="stezka"):
        path = pathfind.route(env, tcost, pts, smooth_iters=2, simplify_m=8.0)
        trails.append({"id": tid, "name": name, "kind": kind, "pts": path, "note": note, "island": island, "surface": surface, "status": "proposed"})

    P = world.pos
    spot = lambda x, y, r=0.4, s=14.0: hr.best_spot(world, x, y, r, s, 0.04)
    t03 = spot(P("T-03")[0], P("T-03")[1] - 0.1)
    n01 = spot(2.95, 6.55, 0.4, 20.0)
    m03 = spot(*P("M-03"), 0.2, 25.0)
    m01 = spot(*P("M-01"), 0.2, 28.0)
    m02 = spot(*P("M-02"), 0.2, 28.0)
    horska = spot(9.45, 6.45)
    fall = spot(10.5, 8.5, 0.5, 18.0)
    dam = spot(12.3, 10.3, 0.4, 14.0)
    add("TR-01", "Útesová stezka k vyhlídce N-01", "hiking", [t03, n01], "bezpečná stezka k vyhlídce N-01 s oplocením")
    add("TR-02", "Stezka na zaoblený vrch M-03", "hiking", [t03, m03], "louky, značené trasy; start paraglidingu")
    add("TR-03", "Hřebenovka M-03 – M-01", "hiking", [m03, m01])
    add("TR-04", "Hřebenovka M-01 – M-02", "hiking", [m01, m02])
    add("TR-05", "Stezka k pramenům a na M-02", "hiking", [horska, spot(9.6, 5.8), m02], "prameny a studánky")
    add("TR-06", "Vodní stezka: vodopád – přehrada", "hiking", [fall, spot(11.2, 9.0, 0.4, 16.0), dam])
    add("TR-07", "Z Horské stanice k M-03", "hiking", [horska, spot(7.6, 7.2, 0.5, 18.0), m03])
    return trails


def build_para_roads(world, forest_mask):
    env = world.env
    cost = pathfind.road_cost(env, forest_mask=forest_mask, max_slope=16.0, coast_target=0.30, coast_w=1.5)
    mask = np.zeros(env.z.shape, dtype=bool)
    spot = lambda u, v, r=0.25, s=5.0: hr.best_spot(world, *world.para(u, v), r, s, 0.04)
    marina = spot(-2.05, 0.05)
    old = spot(0.0, -1.15)
    east_n = spot(1.55, -0.75)
    east_s = spot(1.55, 0.85)
    south = spot(0.35, 1.10)
    resort = spot(-0.7, 1.02)
    roads = []
    ring = pathfind.route(env, cost, [marina, old, east_n, east_s, south, resort, marina], smooth_iters=2, simplify_m=8.0)
    roads.append({"id": "RD-PL1", "name": "Okružní servisní silnice Paralandu", "class": "R3", "island": "para", "pts": ring,
                  "note": "omezený provoz (rezervace a ochrana místních); bez autopřevozu z hlavního ostrova", "status": "proposed"})
    pathfind.mark_path(env, mask, ring, 1)
    cost2 = pathfind.road_cost(env, bonus_mask=mask, forest_mask=forest_mask, max_slope=14.0)
    for rid, name, a, b in [
        ("RD-PL2", "Přístup k hradu", spot(-0.6, -1.0), spot(-1.35, -1.20, 0.3, 9.0)),
        ("RD-PL3", "Přístup k aquaparku", spot(0.0, 0.95), spot(0.1, 0.60)),
        ("RD-PL4", "Přístup k přistávací ploše", spot(-1.0, 0.75), spot(-1.15, 0.62)),
    ]:
        p = pathfind.route(env, cost2, [a, b], smooth_iters=2, simplify_m=6.0)
        roads.append({"id": rid, "name": name, "class": "R3", "island": "para", "pts": p, "note": "", "status": "proposed"})
    tcost = pathfind.trail_cost(env)
    trails = []
    loop = pathfind.route(env, tcost, [spot(1.0, -0.5, 0.4, 14.0), spot(1.55, -0.1, 0.4, 16.0), spot(1.35, 0.55, 0.4, 16.0), spot(0.7, 0.3, 0.4, 14.0), spot(0.9, -0.45, 0.4, 14.0)], smooth_iters=2)
    trails.append({"id": "TR-PL1", "name": "Pěší okruh východními lesy Paralandu", "kind": "hiking", "pts": loop, "island": "para", "surface": "stezka",
                   "note": "kanon: východ Paralandu – lesy, menší kopce, pěší okruh", "status": "proposed"})
    trail2 = pathfind.route(env, tcost, [spot(0.0, -1.1), spot(0.5, -0.95, 0.4, 14.0), spot(-1.35, -1.2, 0.3, 14.0)], smooth_iters=2)
    trails.append({"id": "TR-PL2", "name": "Staré městečko – zřícenina – hrad", "kind": "hiking", "pts": trail2, "island": "para", "surface": "stezka",
                   "note": "historická památková stezka", "status": "proposed"})
    return roads, trails
