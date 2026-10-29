"""Plán hlavního města (F9): půdorysy domů ve stavu zástavby, který odpovídá modelové populaci (ilustrativní, pracovní návrh).

Plán CP-01 vymezuje 874 bloků (4,5 km²). Kdyby se všechny zastavěly podle svého využití, měly by kapacitu bydlení kolem 44 000 obyvatel,
tedy víc než schválený strop 40 000 pro celou zemi (bible: population_range). Domy proto vznikají takto:

1. V každém bloku se podle využití vytvoří *kandidáti* (perimetrová zástavba, řadové a rodinné domy, desky nábřeží, státní budovy)
   bez překryvů a mimo klíčové budovy.
2. Bloky se zastavují od jader (Náměstí čtyř, přístavní náměstí, stanice) směrem ven; hranice zastavění se bisekcí doladí tak, aby
   kapacita bydlení odpovídala modelové populaci Larpingtonu (`population_model` v atlasu, 12 000). Bloky u hranice jsou zastavěné
   jen z části, ostatní zůstávají *rezervou rozvoje*; v rezervě stojí jen řídké chaty.
3. Výška (okap, hřeben) a barva střechy vycházejí z využití a podlaží; z toho se skládá výškové pole pro šikmé pohledy.

Vše je deterministické (pevná semínka). Polohy a tvary jsou návrh, ne skutečné budovy; čísla kapacity jsou modelová, ne sčítání.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

import cp_geom as G

PERSON_M2 = 38.0              # m² podlahové plochy bydlení na obyvatele (model)
EFF = 0.82                    # podíl užitné plochy
FLOOR_H = 3.1                 # m na podlaží
BASE_H = 0.5                  # m sokl
ALWAYS = ("civic_mixed", "school", "hotel_premium")          # bez obyvatel, stojí vždy (instituce)
BAND = 0.07                   # šířka měkké hranice zastavění (podíl prahu)

# typologie: druh, rozměry (m), podlaží, podíl bydlení, podíl obsazených parcel (zbytek = proluky a zahrady), střecha, váha růstu (menší = zastavuje se dřív)
SPEC = {
    "old_town_mixed": dict(kind="perimeter", depth=11.5, w=(7.0, 12.0), setback=1.2, gap=1.0, floors=(2, 3, 0.45), resi=0.55, fill=0.90, roof="gable", growth=0.80),
    "promenade_retail": dict(kind="perimeter", depth=13.0, w=(9.0, 14.0), setback=1.2, gap=1.0, floors=(2, 3, 0.55), resi=0.30, fill=0.92, roof="gable", growth=0.85),
    "retail_main": dict(kind="perimeter", depth=14.0, w=(12.0, 20.0), setback=1.5, gap=1.0, floors=(2, 3, 0.60), resi=0.35, fill=0.88, roof="gable", growth=0.90),
    "transit_mixed": dict(kind="perimeter", depth=12.0, w=(8.0, 14.0), setback=1.5, gap=1.2, floors=(3, 4, 0.30), resi=0.50, fill=0.85, roof="gable", growth=0.95),
    "residential_mid": dict(kind="perimeter", depth=10.5, w=(7.0, 10.0), setback=3.0, gap=1.6, floors=(2, 3, 0.45), resi=1.0, fill=0.80, roof="gable", growth=1.00),
    "residential_low": dict(kind="detached", plot=(24.0, 28.0), floors=(1, 2, 0.40), resi=1.0, fill=0.75, roof="gable", growth=1.30),
    "civic_mixed": dict(kind="civic", floors=(3, 4, 0.40), resi=0.0, fill=1.0, roof="flat", growth=1.0, max_n=5),
    "school": dict(kind="none", floors=(2, 3, 0.5), resi=0.0, fill=0.0, roof="gable", growth=1.0),
    "new_waterfront": dict(kind="slabs", floors=(4, 6, 0.50), resi=0.90, fill=0.90, roof="flat", growth=1.25),
    "hotel_premium": dict(kind="none", floors=(3, 3, 0.0), resi=0.0, fill=0.0, roof="gable", growth=1.0),
}
ROOF_PAL = {
    "old_town_mixed": ["#ac6046", "#a05440", "#ba7052", "#7e5646", "#c48c68", "#68686e"],
    "promenade_retail": ["#ba7052", "#c89670", "#ac6046", "#d6cebe", "#96546a"],
    "retail_main": ["#a86248", "#96543e", "#c4baaa", "#78767a", "#b0785c"],
    "transit_mixed": ["#a86248", "#70707a", "#bab2a6", "#5c5e64"],
    "residential_mid": ["#a86248", "#96543e", "#70707a", "#bab2a6", "#5c5e64", "#b0785c"],
    "residential_low": ["#a86248", "#96543e", "#70707a", "#beb6aa", "#5c5e64"],
    "civic_mixed": ["#968c96", "#b0a4a0", "#787682", "#c4bab0"],
    "new_waterfront": ["#cecece", "#aab0ba", "#e4e0da", "#96a0aa", "#be9682"],
}
# klíčové budovy (cp_buildings): výška okapu a tvar střechy
KEY_H = {"parliament": 22.0, "admin": 18.0, "museum": 16.0, "church": 20.0, "market_hall": 10.0, "hotel_premium": 20.0, "school": 10.0, "harbour_office": 9.0, "ferry_terminal": 7.0}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def orientation(poly):
    """Úhel (°) nejdelší hrany polygonu – směr uliční fronty bloku."""
    best, ang = 0.0, 0.0
    for a, b in zip(poly, poly[1:] + poly[:1]):
        L = math.dist(a, b)
        if L > best:
            best, ang = L, math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    return ang


def inside_all(rect, poly):
    return all(G.point_in_poly(p, poly) for p in rect)


class Occ:
    """Obsazenost bloku (rastr 1 m): zamezuje překryvu domů a klíčových budov."""

    def __init__(self, poly, keepout=()):
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        self.x0, self.y0 = min(xs) - 2, min(ys) - 2
        self.w, self.h = int(max(xs) - min(xs)) + 5, int(max(ys) - min(ys)) + 5
        self.arr = np.zeros((self.h, self.w), dtype=bool)
        for k in keepout:
            kx, ky = [p[0] for p in k], [p[1] for p in k]
            if max(kx) < min(xs) - 4 or min(kx) > max(xs) + 4 or max(ky) < min(ys) - 4 or min(ky) > max(ys) + 4:
                continue
            m = Image.new("L", (self.w, self.h), 0)
            dm = ImageDraw.Draw(m)
            pts = [(p[0] - self.x0, p[1] - self.y0) for p in k]
            dm.polygon(pts, fill=255)
            dm.line(pts + [pts[0]], fill=255, width=5)                  # odstup 2 m
            self.arr |= np.asarray(m) > 127

    def _mask(self, rect):
        m = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(m).polygon([(p[0] - self.x0, p[1] - self.y0) for p in rect], fill=255)
        return np.asarray(m) > 127

    def free(self, rect, tol=0.08):
        a = self._mask(rect)
        return bool(a.any()) and (a & self.arr).sum() <= tol * a.sum()

    def take(self, rect):
        self.arr |= self._mask(rect)


def _rect(c, w, d, ang):
    return {"c": (round(c[0], 2), round(c[1], 2)), "w": round(w, 2), "d": round(d, 2), "ang": round(ang, 2)}


def perimeter(poly, spec, rng, occ):
    """Řada domů podél obvodu bloku (hloubka dovnitř od uliční hrany)."""
    sgn = 1.0 if G.signed_area(poly) > 0 else -1.0
    out = []
    wmin, wmax = spec["w"]
    for a, b in zip(poly, poly[1:] + poly[:1]):
        L = math.dist(a, b)
        if L < wmin + 2 * spec["setback"]:
            continue
        t = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        n = (-t[1] * sgn, t[0] * sgn)                          # dovnitř bloku
        if not G.point_in_poly((a[0] + t[0] * L / 2 + n[0] * 3, a[1] + t[1] * L / 2 + n[1] * 3), poly):
            n = (-n[0], -n[1])
        s = spec["setback"]
        ang = math.degrees(math.atan2(t[1], t[0]))
        while s < L - spec["setback"] - wmin:
            w = min(rng.uniform(wmin, wmax), L - spec["setback"] - s)
            dep = spec["depth"] * rng.uniform(0.85, 1.1)
            c = (a[0] + t[0] * (s + w / 2) + n[0] * (1.2 + dep / 2), a[1] + t[1] * (s + w / 2) + n[1] * (1.2 + dep / 2))
            r = G.oriented_rect(c[0], c[1], w - spec["gap"], dep, ang)
            if inside_all(r, poly) and occ.free(r):
                out.append((r, _rect(c, w - spec["gap"], dep, ang)))
                occ.take(r)
            s += w
    return out


def detached(poly, spec, rng, occ):
    """Rodinné domy na mřížce parcel natočené podle bloku."""
    ang = orientation(poly)
    c = G.centroid(poly)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [((p[0] - c[0]) * ca + (p[1] - c[1]) * sa, -(p[0] - c[0]) * sa + (p[1] - c[1]) * ca) for p in poly]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    plot = spec["plot"]
    out = []
    x = min(xs) + plot[0] / 2
    while x < max(xs):
        y = min(ys) + plot[1] / 2
        while y < max(ys):
            w, d = rng.uniform(9, 13), rng.uniform(8, 11)
            ux, uy = x + rng.uniform(-3, 3), y + rng.uniform(-3, 3)
            cx, cy = c[0] + ux * ca - uy * sa, c[1] + ux * sa + uy * ca
            r = G.oriented_rect(cx, cy, w, d, ang)
            if inside_all(G.oriented_rect(cx, cy, w + 6, d + 6, ang), poly) and occ.free(r):
                out.append((r, _rect((cx, cy), w, d, ang)))
                occ.take(r)
            y += plot[1]
        x += plot[0]
    return out


def slabs(poly, spec, rng, occ):
    """Desky Východního nábřeží v řadách."""
    ang = orientation(poly)
    c = G.centroid(poly)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [((p[0] - c[0]) * ca + (p[1] - c[1]) * sa, -(p[0] - c[0]) * sa + (p[1] - c[1]) * ca) for p in poly]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    out = []
    y = min(ys) + 14
    while y < max(ys) - 8:
        x = min(xs) + 10
        while x < max(xs) - 20:
            w, d = rng.uniform(36, 54), 14.0
            cx, cy = c[0] + (x + w / 2) * ca - y * sa, c[1] + (x + w / 2) * sa + y * ca
            r = G.oriented_rect(cx, cy, w, d, ang)
            if inside_all(G.oriented_rect(cx, cy, w + 8, d + 8, ang), poly) and occ.free(r):
                out.append((r, _rect((cx, cy), w, d, ang)))
                occ.take(r)
            x += w + rng.uniform(8, 16)
        y += 28.0
    return out


def civic(poly, spec, rng, occ):
    """Instituce státní čtvrti: čtyři až pět větších budov kolem středu bloku."""
    ang = orientation(poly)
    c = G.centroid(poly)
    out = []
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)):
        w, d = rng.uniform(36, 56), rng.uniform(20, 28)
        cx, cy = c[0] + dx * 30, c[1] + dy * 22
        r = G.oriented_rect(cx, cy, w, d, ang)
        if inside_all(G.oriented_rect(cx, cy, w + 6, d + 6, ang), poly) and occ.free(r):
            out.append((r, _rect((cx, cy), w, d, ang)))
            occ.take(r)
    return out[: spec.get("max_n", 5)]


GEN = {"perimeter": perimeter, "detached": detached, "slabs": slabs, "civic": civic}


def _floors(spec, rng):
    lo, hi, p_hi = spec["floors"]
    return int(hi if (hi > lo and rng.random() < p_hi) else lo)


def candidates(blocks, keepout=(), foci=(), seed=20261025):
    """Kandidáti domů pro všechny bloky (bez překryvů při plném zastavění).

    `blocks`: seznam slovníků s `poly`, `use`, `c`. U každého domu je `u` = pořadí od nejbližšího jádra (0 = nejblíž), takže se blok při
    částečném zastavění plní od strany jádra, a `v` = náhodné číslo pro proluky (porovnává se s podílem obsazených parcel)."""
    out = []
    for i, b in enumerate(blocks):
        spec = SPEC.get(b["use"])
        if not spec or spec["kind"] == "none":
            continue
        rng = np.random.default_rng(seed + (i + 1) * 7919)
        poly = b["poly"]
        rects = GEN[spec["kind"]](poly, spec, rng, Occ(poly, keepout))
        if not rects:
            continue
        pal = ROOF_PAL.get(b["use"], ROOF_PAL["residential_mid"])
        dist = [min(math.dist(r[1]["c"], (f[0], f[1])) * f[2] for f in foci) if foci else 0.0 for r in rects]
        rank = np.argsort(np.argsort(dist))
        n = len(rects)
        for k, (corners, rc) in enumerate(rects):
            fl = _floors(spec, rng)
            out.append({"poly": corners, **rc, "block": i, "use": b["use"], "floors": fl, "roof_col": pal[int(rng.integers(0, len(pal)))], "roof": spec["roof"],
                        "u": float(np.clip((rank[k] + 0.5) / n + rng.normal(0.0, 0.07), 0.0, 1.0)), "v": float(rng.random()), "area": G.area(corners), "kind": "core"})
    return out


def fringe(blocks, seed=20261026, p=0.30):
    """Řídké chaty a zahrádkářské domky v rezervních blocích (jeden dům v bloku, s pravděpodobností p)."""
    out = []
    for i, b in enumerate(blocks):
        if b["use"] not in ("residential_mid", "residential_low"):
            continue
        rng = np.random.default_rng(seed + (i + 1) * 104729)
        if rng.random() > p:
            continue
        poly = b["poly"]
        if G.area(poly) < 1800.0:
            continue
        ang = orientation(poly)
        c = G.centroid(poly)
        for _ in range(12):                                         # hledání místa uvnitř bloku s odstupem
            xs, ys = [q[0] for q in poly], [q[1] for q in poly]
            pt = (rng.uniform(min(xs), max(xs)), rng.uniform(min(ys), max(ys)))
            w, d = rng.uniform(8.5, 12.0), rng.uniform(7.0, 9.5)
            if inside_all(G.oriented_rect(pt[0], pt[1], w + 16, d + 16, ang), poly):
                r = G.oriented_rect(pt[0], pt[1], w, d, ang)
                fl = 1 if rng.random() < 0.7 else 2
                pal = ROOF_PAL["residential_low"]
                out.append({"poly": r, **_rect(pt, w, d, ang), "block": i, "use": b["use"], "floors": fl, "roof_col": pal[int(rng.integers(0, len(pal)))], "roof": "gable",
                            "u": 0.0, "v": 0.0, "area": G.area(r), "kind": "fringe"})
                break
    return out


def capacity(h):
    """Modelová kapacita bydlení (osob): půdorys × podlaží × podíl bydlení × užitná plocha / m² na obyvatele."""
    resi = 1.0 if h["kind"] == "fringe" else SPEC[h["use"]]["resi"]
    return h["area"] * h["floors"] * resi * EFF / PERSON_M2


def eave_height(h):
    return BASE_H + h["floors"] * (4.2 if h["use"] in ("civic_mixed",) else FLOOR_H)


def ridge_height(h):
    if h["roof"] != "gable":
        return 0.0
    return round(0.30 * min(h["w"], h["d"]), 2)


def priority(blocks, foci, seed=20261027):
    """Vzdálenost bloku od nejbližšího jádra (vážená využitím, s mírným šumem); čím menší, tím dřív se zastavuje."""
    rng = np.random.default_rng(seed)
    noise = rng.random(len(blocks))
    out = []
    for i, b in enumerate(blocks):
        d = min(math.dist(b["c"], (f[0], f[1])) * f[2] for f in foci)
        out.append(d * SPEC[b["use"]]["growth"] * (1.0 + 0.16 * (noise[i] - 0.5)))
    return out


def block_fill(blocks, prio, T):
    f = []
    for i, b in enumerate(blocks):
        if b["use"] in ALWAYS:
            f.append(1.0)
        else:
            v = float(np.clip((T * (1.0 + BAND) - prio[i]) / (T * BAND), 0.0, 1.0))
            f.append(v if v >= 0.05 else 0.0)                     # pod 5 % je blok čistá rezerva
    return f


def build(blocks, foci, target, keepout=(), tol=0.01):
    """Zastaví bloky od jader tak, aby kapacita bydlení odpovídala `target`. Vrací domy, stav bloků a statistiku.

    `foci`: seznam (x, y, váha vzdálenosti); váha > 1 jádro zeslabuje (menší dosah)."""
    cands = candidates(blocks, keepout, foci)
    fr = fringe(blocks)
    prio = priority(blocks, foci)
    by_block = {}
    for h in cands:
        by_block.setdefault(h["block"], []).append(h)
    fr_by = {h["block"]: h for h in fr}
    full_cap = sum(capacity(h) for h in cands if h["v"] < SPEC[h["use"]]["fill"])

    def accepted(h, f):
        return h["u"] < f and h["v"] < SPEC[h["use"]]["fill"]

    def cap_at(T):
        fills = block_fill(blocks, prio, T)
        cap = 0.0
        for i, f in enumerate(fills):
            if f > 0.0:
                cap += sum(capacity(h) for h in by_block.get(i, ()) if accepted(h, f))
            if f < 0.05 and i in fr_by:
                cap += capacity(fr_by[i])
        return cap

    lo, hi = 50.0, 8000.0
    T = hi
    for _ in range(60):
        T = (lo + hi) / 2
        cap = cap_at(T)
        if abs(cap - target) <= tol * target:
            break
        if cap < target:
            lo = T
        else:
            hi = T
    fills = block_fill(blocks, prio, T)
    houses = []
    for i, f in enumerate(fills):
        if f > 0.0:
            houses += [h for h in by_block.get(i, ()) if accepted(h, f)]
        if f < 0.05 and i in fr_by:
            houses.append(fr_by[i])
    for k, h in enumerate(houses, 1):
        h["id"] = f"CP-H-{k:05d}"
        h["height_m"] = round(eave_height(h), 2)
        h["ridge_m"] = ridge_height(h)
        h["capacity"] = round(capacity(h), 2)
    state, info = [], []
    nb = {}
    for h in houses:
        a = nb.setdefault(h["block"], [0, 0.0, 0.0])
        a[0] += 1
        a[1] += h["area"]
        a[2] += h["capacity"]
    for i, (b, f) in enumerate(zip(blocks, fills)):
        if b["use"] in ALWAYS:
            st = "civic" if b["use"] != "hotel_premium" else "civic"
        elif f >= 0.85:
            st = "built"
        elif f >= 0.05:
            st = "partial"
        else:
            st = "reserve"
        n, fp, cp = nb.get(i, (0, 0.0, 0.0))
        info.append({"fill": round(f, 3), "state": st, "houses": n, "footprint_m2": round(fp, 1), "capacity": round(cp, 1)})
    cap_total = sum(h["capacity"] for h in houses)
    per_use = {}
    for h in houses:
        a = per_use.setdefault(h["use"], {"houses": 0, "footprint_ha": 0.0, "capacity": 0.0})
        a["houses"] += 1
        a["footprint_ha"] += h["area"] / 1e4
        a["capacity"] += h["capacity"]
    for a in per_use.values():
        a["footprint_ha"] = round(a["footprint_ha"], 2)
        a["capacity"] = round(a["capacity"])
    count = lambda s: sum(1 for x in info if x["state"] == s)
    area = lambda s: round(sum(blocks[i]["area"] for i, x in enumerate(info) if x["state"] == s) / 1e4, 1)
    stats = {
        "target_population": target, "capacity": round(cap_total), "ratio": round(cap_total / target, 3), "full_buildout_capacity": round(full_cap),
        "full_buildout_ratio": round(full_cap / target, 2), "threshold_m": round(T, 1), "houses": len(houses), "houses_core": sum(1 for h in houses if h["kind"] == "core"),
        "houses_fringe": sum(1 for h in houses if h["kind"] == "fringe"), "footprint_ha": round(sum(h["area"] for h in houses) / 1e4, 1),
        "blocks": {"built": count("built"), "partial": count("partial"), "reserve": count("reserve"), "civic": count("civic")},
        "block_area_ha": {"built": area("built"), "partial": area("partial"), "reserve": area("reserve"), "civic": area("civic")},
        "coverage_of_built_blocks": round(sum(h["area"] for h in houses if info[h["block"]]["state"] in ("built", "partial")) / max(1.0, sum(blocks[i]["area"] for i, x in enumerate(info) if x["state"] in ("built", "partial"))), 3),
        "per_use": per_use,
        "assumptions": {"person_m2": PERSON_M2, "usable_share": EFF, "floor_height_m": FLOOR_H},
    }
    return {"houses": houses, "blocks": info, "stats": stats}


# ------------------------------------------------------------------ výstupy
def features(houses, blocks_ids, to_km=None):
    """GeoJSON Features domů (lokální metry, nebo km atlasu, je-li zadáno `to_km`)."""
    fs = []
    for h in houses:
        pts = [to_km(p) if to_km else p for p in h["poly"]]
        nd = 4 if to_km else 2
        pts = [[round(p[0], nd), round(p[1], nd)] for p in pts]
        props = {"id": h["id"], "type": "house", "subtype": h["use"], "kind": h["kind"], "block": blocks_ids[h["block"]], "floors": h["floors"], "height_m": h["height_m"], "ridge_m": h["ridge_m"],
                 "roof": h["roof"], "roof_color": h["roof_col"], "footprint_m2": round(h["area"], 1), "capacity_model": h["capacity"], "exist_status": "proposed", "pos_status": "proposed",
                 "origin": "plan_new", "illustrative": True}
        fs.append({"type": "Feature", "properties": props, "geometry": {"type": "Polygon", "coordinates": [pts + [pts[0]]]}})
    return fs


def house_from_feature(f):
    """Zpětné čtení domu z GeoJSON (lokální metry) pro vykreslování."""
    pr = f["properties"]
    ring = [tuple(p) for p in f["geometry"]["coordinates"][0][:-1]]
    c = G.centroid(ring)
    a, b, d = ring[0], ring[1], ring[2]
    w, dd = math.dist(a, b), math.dist(b, d)
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    return {"poly": ring, "c": c, "w": w, "d": dd, "ang": ang, "use": pr["subtype"], "kind": pr["kind"], "floors": pr["floors"], "height_m": pr["height_m"], "ridge_m": pr["ridge_m"],
            "roof": pr["roof"], "roof_col": pr["roof_color"], "id": pr["id"], "block": pr["block"]}


def height_field(houses, keys, shape_hw, mpp, x0=0.0, y0=0.0):
    """Výškové pole budov (m nad terénem) na rastru `mpp` m/px s počátkem (x0, y0) m: sedlové střechy domů a ploché klíčové budovy.

    `houses`: slovníky s c, w, d, ang, height_m, ridge_m; `keys`: seznam (polygon, výška)."""
    H, W = shape_hw
    z = np.zeros((H, W), dtype=np.float32)
    for h in houses:
        cx, cy = h["c"]
        rad = 0.5 * math.hypot(h["w"], h["d"]) + mpp
        c0, c1 = max(0, int((cx - rad - x0) / mpp)), min(W - 1, int((cx + rad - x0) / mpp) + 1)
        r0, r1 = max(0, int((cy - rad - y0) / mpp)), min(H - 1, int((cy + rad - y0) / mpp) + 1)
        if c1 < c0 or r1 < r0:
            continue
        xs = x0 + (np.arange(c0, c1 + 1) + 0.5) * mpp - cx
        ys = y0 + (np.arange(r0, r1 + 1) + 0.5) * mpp - cy
        X, Y = np.meshgrid(xs, ys)
        ca, sa = math.cos(math.radians(h["ang"])), math.sin(math.radians(h["ang"]))
        lx, ly = X * ca + Y * sa, -X * sa + Y * ca
        inside = (np.abs(lx) <= h["w"] / 2 + 0.25 * mpp) & (np.abs(ly) <= h["d"] / 2 + 0.25 * mpp)
        if h["ridge_m"] > 0:
            span_half = min(h["w"], h["d"]) / 2
            cross = np.abs(ly) if h["w"] >= h["d"] else np.abs(lx)
            top = h["height_m"] + h["ridge_m"] * np.clip(1.0 - cross / span_half, 0.0, 1.0)
        else:
            top = np.full(X.shape, h["height_m"], dtype=np.float32)
        sub = z[r0:r1 + 1, c0:c1 + 1]
        z[r0:r1 + 1, c0:c1 + 1] = np.where(inside, np.maximum(sub, top), sub)
    for poly, hh in keys:
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon([((p[0] - x0) / mpp, (p[1] - y0) / mpp) for p in poly], fill=255)
        a = np.asarray(m) > 127
        z[a] = np.maximum(z[a], hh)
    return z


def block_id_raster(blocks, shape_hw, mpp, x0=0.0, y0=0.0):
    """Rastr čísel bloků (index + 1, 0 = mimo blok) – pro určení stavu zástavby u ulic."""
    H, W = shape_hw
    img = Image.new("I", (W, H), 0)
    d = ImageDraw.Draw(img)
    for i, b in enumerate(blocks):
        d.polygon([((p[0] - x0) / mpp, (p[1] - y0) / mpp) for p in b["poly"]], fill=i + 1)
    return np.asarray(img)


def street_states(edges, blocks, info, shape_hw=(2100, 2970), mpp=2.0, always=("R1", "A", "B", "S", "P")):
    """Stav uličních hran: `built` (vozovka stojí – velké třídy nebo hranice se zastavěným blokem) / `planned` (jen plánovaná ulice v rezervě)."""
    rid = block_id_raster(blocks, shape_hw, mpp)
    H, W = shape_hw
    out = []
    for e in edges:
        if e["cls"] in always:
            out.append("built")
            continue
        pts = G.resample(e["pts"], 30.0) if len(e["pts"]) > 1 else e["pts"]
        off = e.get("row_m", e.get("row", 10.0)) / 2.0 + 4.0
        st = "planned"
        for k in range(len(pts)):
            a = pts[max(0, k - 1)]
            b = pts[min(len(pts) - 1, k + 1)]
            tx, ty = b[0] - a[0], b[1] - a[1]
            L = math.hypot(tx, ty) or 1.0
            n = (-ty / L, tx / L)
            for sgn in (-1.0, 1.0):
                x, y = pts[k][0] + n[0] * off * sgn, pts[k][1] + n[1] * off * sgn
                px, py = int(x / mpp), int(y / mpp)
                if 0 <= px < W and 0 <= py < H:
                    bi = int(rid[py, px]) - 1
                    if bi >= 0 and info[bi]["state"] != "reserve":
                        st = "built"
                        break
            if st == "built":
                break
        out.append(st)
    return out
