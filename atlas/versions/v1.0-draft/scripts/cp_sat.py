"""Satelitní reference hlavního města (S-03): zástavba z plánu CP-01 (bloky, ulice, prostory, klíčové budovy) pro `render_sat.render`.

Souřadnice plánu (lokální metry, počátek v SZ rohu okna) přesně odpovídají pixelům S-03 (okno = okno plánu), takže 1 px = `mpp` m.
Stavby vznikají procedurálně v blocích podle využití (perimetrová zástavba starého města, řadové a rodinné domy, desky Východního nábřeží,
státní budovy); stíny padají na sever (slunce z jihu). Vše je simulace a pracovní návrh.
"""
from __future__ import annotations

import json
import math

import numpy as np
from PIL import Image, ImageDraw

import cp_geom as G
import geom
from canon import ATLAS

CAP = ATLAS / "current" / "capital"

ROW = {"R1": 22.0, "A": 22.0, "B": 20.0, "S": 14.0, "P": 18.0, "C": 10.0, "L": 5.0}
STREET_COL = {"R1": ((116, 114, 116), (182, 178, 170)), "A": ((112, 112, 116), (182, 178, 170)), "B": ((114, 114, 118), (182, 178, 170)), "S": ((116, 114, 118), (182, 178, 170)),
              "P": ((214, 198, 164), (226, 214, 184)), "C": ((124, 122, 122), (178, 174, 166)), "L": ((156, 150, 142), (156, 150, 142))}
GROUND = {"old_town_mixed": (152, 142, 126), "promenade_retail": (160, 150, 136), "retail_main": (150, 146, 138), "civic_mixed": (170, 160, 146), "transit_mixed": (146, 142, 130),
          "residential_mid": (120, 140, 94), "residential_low": (112, 144, 86), "school": (126, 152, 102), "new_waterfront": (136, 142, 124), "hotel_premium": (150, 140, 126)}
ROOFS = {
    "old_town_mixed": [(172, 96, 70), (160, 84, 62), (186, 112, 82), (126, 86, 70), (196, 140, 104), (104, 104, 110)],
    "promenade_retail": [(186, 112, 82), (200, 150, 112), (172, 96, 70), (214, 206, 190), (150, 84, 66)],
    "retail_main": [(168, 98, 74), (150, 84, 64), (196, 186, 170), (120, 118, 122), (176, 120, 92)],
    "transit_mixed": [(168, 98, 74), (112, 112, 118), (186, 178, 166), (92, 94, 100)],
    "residential_mid": [(168, 98, 74), (150, 84, 64), (112, 112, 118), (186, 178, 166), (92, 94, 100), (176, 120, 92)],
    "residential_low": [(168, 98, 74), (150, 84, 64), (112, 112, 118), (190, 182, 170), (92, 94, 100)],
    "civic_mixed": [(150, 140, 150), (176, 164, 160), (120, 118, 130), (196, 186, 176)],
    "school": [(96, 124, 164), (176, 164, 156)],
    "new_waterfront": [(206, 206, 208), (170, 176, 186), (228, 224, 218), (150, 158, 170), (190, 150, 130)],
    "hotel_premium": [(170, 100, 80)],
}
KEY_ROOF = {"parliament": (92, 102, 128), "admin": (150, 122, 112), "museum": (100, 114, 130), "church": (98, 84, 78), "market_hall": (164, 124, 74), "hotel_premium": (176, 104, 84),
            "school": (80, 118, 164), "harbour_office": (130, 130, 128), "ferry_terminal": (120, 120, 124)}
HEIGHT = {"old_town_mixed": (9, 3), "promenade_retail": (12, 3), "retail_main": (12, 3), "transit_mixed": (14, 4), "residential_mid": (13, 4), "residential_low": (6.5, 1.5),
          "civic_mixed": (16, 4), "school": (9, 1), "new_waterfront": (24, 8), "hotel_premium": (18, 2)}


def load_plan():
    def fc(name):
        return json.loads((CAP / f"cp_{name}.geojson").read_text(encoding="utf-8"))["features"]
    return {k: fc(k) for k in ("blocks", "streets", "spaces", "buildings")}


def ring(feature):
    return [tuple(p) for p in feature["geometry"]["coordinates"][0][:-1]]


def inside_all(rect, poly):
    return all(G.point_in_poly(p, poly) for p in rect)


def orientation(poly):
    """Úhel (°) nejdelší hrany polygonu – směr uliční fronty bloku."""
    best, ang = 0.0, 0.0
    for a, b in zip(poly, poly[1:] + poly[:1]):
        L = math.dist(a, b)
        if L > best:
            best, ang = L, math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    return ang


class Occ:
    """Obsazenost bloku (1 m) – zamezuje překryvu budov."""

    def __init__(self, poly):
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        self.x0, self.y0 = min(xs) - 2, min(ys) - 2
        self.w, self.h = int(max(xs) - min(xs)) + 5, int(max(ys) - min(ys)) + 5
        self.img = Image.new("L", (self.w, self.h), 0)
        self.d = ImageDraw.Draw(self.img)

    def free(self, rect, tol=0.08):
        m = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(m).polygon([(p[0] - self.x0, p[1] - self.y0) for p in rect], fill=255)
        a = np.asarray(m) > 127
        if not a.any():
            return False
        return (a & (np.asarray(self.img) > 127)).sum() <= tol * a.sum()

    def take(self, rect):
        self.d.polygon([(p[0] - self.x0, p[1] - self.y0) for p in rect], fill=255)


def perimeter(poly, depth, wmin, wmax, setback, rng, gap=1.0, occ=None):
    """Řada budov podél obvodu bloku (hloubka depth dovnitř od uliční hrany)."""
    sgn = 1.0 if G.signed_area(poly) > 0 else -1.0
    out = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        L = math.dist(a, b)
        if L < wmin + 2 * setback:
            continue
        t = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        n = (-t[1] * sgn, t[0] * sgn)                       # dovnitř bloku
        if G.point_in_poly((a[0] + t[0] * L / 2 + n[0] * 3, a[1] + t[1] * L / 2 + n[1] * 3), poly) is False:
            n = (-n[0], -n[1])
        s = setback
        while s < L - setback - wmin:
            w = min(rng.uniform(wmin, wmax), L - setback - s)
            dep = depth * rng.uniform(0.85, 1.1)
            c = (a[0] + t[0] * (s + w / 2) + n[0] * (1.2 + dep / 2), a[1] + t[1] * (s + w / 2) + n[1] * (1.2 + dep / 2))
            r = G.oriented_rect(c[0], c[1], w - gap, dep, math.degrees(math.atan2(t[1], t[0])))
            if inside_all(r, poly) and (occ is None or occ.free(r)):
                out.append(r)
                if occ is not None:
                    occ.take(r)
            s += w
    return out


def detached(poly, ang, rng, plot=(24.0, 28.0), occ=None):
    """Rodinné domy na mřížce parcel natočené podle bloku."""
    c = G.centroid(poly)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [((p[0] - c[0]) * ca + (p[1] - c[1]) * sa, -(p[0] - c[0]) * sa + (p[1] - c[1]) * ca) for p in poly]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    out = []
    x = min(xs) + plot[0] / 2
    while x < max(xs):
        y = min(ys) + plot[1] / 2
        while y < max(ys):
            w, h = rng.uniform(9, 13), rng.uniform(8, 11)
            jx, jy = rng.uniform(-3, 3), rng.uniform(-3, 3)
            ux, uy = x + jx, y + jy
            cx, cy = c[0] + ux * ca - uy * sa, c[1] + ux * sa + uy * ca
            r = G.oriented_rect(cx, cy, w, h, ang)
            big = G.oriented_rect(cx, cy, w + 6, h + 6, ang)
            if inside_all(big, poly) and (occ is None or occ.free(r)):
                out.append(r)
                if occ is not None:
                    occ.take(r)
            y += plot[1]
        x += plot[0]
    return out


def slabs(poly, ang, rng, occ=None):
    c = G.centroid(poly)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [((p[0] - c[0]) * ca + (p[1] - c[1]) * sa, -(p[0] - c[0]) * sa + (p[1] - c[1]) * ca) for p in poly]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    out = []
    y = min(ys) + 14
    while y < max(ys) - 8:
        x = min(xs) + 10
        while x < max(xs) - 20:
            w, h = rng.uniform(36, 54), 14.0
            cx, cy = c[0] + (x + w / 2) * ca - y * sa, c[1] + (x + w / 2) * sa + y * ca
            r = G.oriented_rect(cx, cy, w, h, ang)
            if inside_all(G.oriented_rect(cx, cy, w + 8, h + 8, ang), poly) and (occ is None or occ.free(r)):
                out.append(r)
                if occ is not None:
                    occ.take(r)
            x += w + rng.uniform(8, 16)
        y += 28.0
    return out


def civic(poly, ang, rng, occ=None):
    c = G.centroid(poly)
    out = []
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)):
        w, h = rng.uniform(36, 56), rng.uniform(20, 28)
        cx, cy = c[0] + dx * 30, c[1] + dy * 22
        r = G.oriented_rect(cx, cy, w, h, ang)
        if inside_all(G.oriented_rect(cx, cy, w + 6, h + 6, ang), poly) and (occ is None or occ.free(r)):
            out.append(r)
            if occ is not None:
                occ.take(r)
    return out


def buildings_for(block, rng):
    poly = ring(block)
    use = block["properties"]["land_use"]
    occ = Occ(poly)
    ang = orientation(poly)
    if use in ("old_town_mixed", "promenade_retail", "transit_mixed"):
        return perimeter(poly, 13.0, 8.0, 14.0, 1.5, rng, occ=occ)
    if use == "retail_main":
        return perimeter(poly, 15.0, 12.0, 20.0, 1.5, rng, gap=1.0, occ=occ)
    if use == "residential_mid":
        return perimeter(poly, 11.0, 7.0, 10.0, 3.0, rng, gap=1.6, occ=occ)
    if use == "residential_low":
        return detached(poly, ang, rng, occ=occ)
    if use == "new_waterfront":
        return slabs(poly, ang, rng, occ=occ)
    if use == "civic_mixed":
        return civic(poly, ang, rng, occ=occ)
    if use == "school":
        return civic(poly, ang, rng, occ=occ)[:2]
    return []


def paint_capital(col, mpp, seed, plan=None, ss=2):
    """Vymaluje městskou zástavbu plánu do barevného pole `col` (H, W, 3; float32); vrací (col, painted 0..1)."""
    plan = plan or load_plan()
    H, W = col.shape[:2]
    rng = np.random.default_rng(seed + 303)
    k = ss / mpp                                           # px superrastru na metr plánu
    cw, ch = W * ss, H * ss
    base = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), "RGB").resize((cw, ch), Image.BICUBIC)
    mask = Image.new("L", (cw, ch), 0)
    d = ImageDraw.Draw(base)
    dm = ImageDraw.Draw(mask)

    def P(pts):
        return [(p[0] * k, p[1] * k) for p in pts]

    # --- základ bloků (zahrádkové okraje splývají s okolní krajinou; dvory starého města střídavě dlážděné a zahradní)
    for f in plan["blocks"]:
        use = f["properties"]["land_use"]
        poly = ring(f)
        g0 = GROUND[use]
        if use in ("old_town_mixed", "promenade_retail", "transit_mixed") and rng.random() < 0.35:
            g0 = (112, 138, 92)
        v = int(rng.integers(-5, 6))
        gcol = (g0[0] + v, g0[1] + v, g0[2] + v)
        if use in ("residential_low", "residential_mid", "school"):
            cx, cy = G.centroid(poly)
            nat = col[min(H - 1, max(0, int(cy / mpp))), min(W - 1, max(0, int(cx / mpp)))]
            gcol = tuple(int(0.45 * gcol[i] + 0.55 * nat[i]) for i in range(3))
        d.polygon(P(poly), fill=gcol)
        dm.polygon(P(poly), fill=255)
    # --- prostory
    for f in plan["spaces"]:
        pr = f["properties"]
        if pr["type"] == "harbor":
            continue
        sub = pr["subtype"]
        col_s = {"park": (96, 138, 76), "green_wedge": (126, 152, 92), "square": (196, 186, 168), "civic_plaza": (190, 180, 162), "station_plaza": (190, 182, 166), "promenade": (216, 200, 166)}.get(sub, (190, 182, 166))
        d.polygon(P(ring(f)), fill=col_s)
        dm.polygon(P(ring(f)), fill=255 if sub != "green_wedge" else 0)
    # --- zelené klíny: sady, zahrádky a hřiště (menší záplaty uvnitř luk)
    patches = []                                                     # (polygon, druh)
    for f in plan["spaces"]:
        if f["properties"].get("subtype") != "green_wedge":
            continue
        wp = ring(f)
        xs, ys = [p[0] for p in wp], [p[1] for p in wp]
        for _ in range(int(G.area(wp) / 45000.0) + 2):
            c = (rng.uniform(min(xs), max(xs)), rng.uniform(min(ys), max(ys)))
            w, h = rng.uniform(110, 210), rng.uniform(80, 140)
            ang = rng.uniform(-12, 12)
            rect = G.oriented_rect(c[0], c[1], w, h, ang)
            if not inside_all(G.oriented_rect(c[0], c[1], w + 40, h + 40, ang), wp):
                continue
            kind = rng.choice(["orchard", "allot", "sport"], p=[0.5, 0.3, 0.2])
            patches.append((rect, str(kind), (c, w, h, ang)))
    for rect, kind, (c, w, h, ang) in patches:
        dm.polygon(P(rect), fill=255)
        if kind == "orchard":
            d.polygon(P(rect), fill=(112, 142, 84))
            ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            for gx in np.arange(-w / 2 + 5, w / 2 - 3, 7.5):
                for gy in np.arange(-h / 2 + 5, h / 2 - 3, 7.5):
                    px_, py_ = (c[0] + gx * ca - gy * sa) * k, (c[1] + gx * sa + gy * ca) * k
                    r_ = 1.9 * k
                    d.ellipse([px_ - r_, py_ - r_, px_ + r_, py_ + r_], fill=(70, 116, 62))
        elif kind == "allot":
            ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            for gx in np.arange(-w / 2, w / 2 - 10, 14.0):
                for gy in np.arange(-h / 2, h / 2 - 10, 20.0):
                    cc = [(122, 150, 84), (150, 150, 92), (108, 132, 76), (160, 132, 96)][int(rng.integers(0, 4))]
                    r2 = G.oriented_rect(c[0] + (gx + 7) * ca - (gy + 10) * sa, c[1] + (gx + 7) * sa + (gy + 10) * ca, 12.0, 18.0, ang)
                    d.polygon(P(r2), fill=cc)
        else:
            d.polygon(P(rect), fill=(92, 150, 80))
            inner = G.oriented_rect(c[0], c[1], min(w, 100.0) * 0.8, min(h, 64.0) * 0.8, ang)
            d.line(P(inner + [inner[0]]), fill=(236, 240, 228), width=max(1, int(0.9 * k)))
    # --- ulice (chodník + vozovka)
    order = ["L", "C", "P", "S", "B", "A", "R1"]
    edges = sorted(plan["streets"], key=lambda f: order.index(f["properties"]["cls"]))
    for f in edges:
        pr = f["properties"]
        cls = pr["cls"]
        row = pr["row_m"]
        asphalt, walk = STREET_COL[cls]
        pts = P(f["geometry"]["coordinates"])
        w_out = max(1, int(round(row * k)))
        w_in = max(1, int(round((row - (0 if cls in ("L", "P") else 4.0)) * k)))
        d.line(pts, fill=walk, width=w_out, joint="curve")
        d.line(pts, fill=asphalt, width=w_in, joint="curve")
        dm.line(pts, fill=255, width=w_out, joint="curve")
    # --- budovy: stíny, pak střechy
    rects, roofs, heights = [], [], []
    for f in plan["blocks"]:
        use = f["properties"]["land_use"]
        pal = ROOFS.get(use, ROOFS["residential_mid"])
        hm, hs = HEIGHT.get(use, (10, 2))
        for r in buildings_for(f, rng):
            rects.append(r)
            roofs.append(pal[int(rng.integers(0, len(pal)))])
            heights.append(max(4.0, rng.normal(hm, hs)))
    for f in plan["buildings"]:
        pr = f["properties"]
        if pr["type"] != "building":
            continue
        rects.append(ring(f))
        roofs.append(KEY_ROOF.get(pr["subtype"], (120, 110, 104)))
        heights.append({"parliament": 22, "admin": 18, "museum": 16, "church": 20, "market_hall": 10, "hotel_premium": 20}.get(pr["subtype"], 10))
    shadow = Image.new("L", (cw, ch), 0)
    ds = ImageDraw.Draw(shadow)
    for r, h in zip(rects, heights):
        Lh = 1.1 * h                                       # slunce 42° nad obzorem, stín k severu
        hull = geom.convex_hull([tuple(p) for p in r] + [(p[0], p[1] - Lh) for p in r])
        ds.polygon(P(hull), fill=255)
        dm.polygon(P(hull), fill=255)
    sh = np.asarray(shadow) > 127
    arr = np.asarray(base).copy()
    arr[sh] = (arr[sh] * 0.66).astype(np.uint8)
    base = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(base)
    for r, c_ in zip(rects, roofs):
        sh_c = int(rng.integers(-8, 9))
        d.polygon(P(r), fill=(max(0, min(255, c_[0] + sh_c)), max(0, min(255, c_[1] + sh_c)), max(0, min(255, c_[2] + sh_c))))
        if len(r) == 4:                                    # sedlová střecha: jedna polovina o něco světlejší
            d.polygon(P([r[0], r[1], ((r[1][0] + r[2][0]) / 2, (r[1][1] + r[2][1]) / 2), ((r[0][0] + r[3][0]) / 2, (r[0][1] + r[3][1]) / 2)]),
                      fill=(min(255, c_[0] + 14 + sh_c), min(255, c_[1] + 14 + sh_c), min(255, c_[2] + 14 + sh_c)))
        dm.polygon(P(r), fill=255)
    # --- stromy: podél tepen a v parcích
    for f in plan["streets"]:
        pr = f["properties"]
        if pr["cls"] not in ("A", "B", "S", "P", "R1"):
            continue
        pts = [tuple(p) for p in f["geometry"]["coordinates"]]
        rs = G.resample(pts, 15.0)
        for i in range(1, len(rs) - 1):
            t = (rs[i + 1][0] - rs[i - 1][0], rs[i + 1][1] - rs[i - 1][1])
            L = math.hypot(*t) or 1.0
            n = (-t[1] / L, t[0] / L)
            for side in (-1, 1):
                if rng.random() < 0.8:
                    off = pr["row_m"] / 2 + 2.0
                    cx, cy = (rs[i][0] + n[0] * off * side) * k, (rs[i][1] + n[1] * off * side) * k
                    r_ = rng.uniform(1.8, 2.6) * k
                    d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=(62, 104, 62))
    for f in plan["spaces"]:
        pr = f["properties"]
        if pr["subtype"] not in ("park",):
            continue
        poly = ring(f)
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        n_tr = int(G.area(poly) / 70.0)
        for _ in range(n_tr):
            p = (rng.uniform(min(xs), max(xs)), rng.uniform(min(ys), max(ys)))
            if G.point_in_poly(p, poly):
                r_ = rng.uniform(2.2, 4.2) * k
                gc = [(58, 102, 58), (70, 112, 62), (50, 92, 54)][int(rng.integers(0, 3))]
                cx, cy = p[0] * k, p[1] * k
                d.ellipse([cx - r_ * 0.8, cy - r_ * 1.9, cx + r_ * 0.9, cy - r_ * 0.2], fill=(36, 60, 40))
                d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=gc)
    # --- sloučení se základem
    painted = np.asarray(mask.resize((W, H), Image.BOX)).astype(np.float32) / 255.0
    new = np.asarray(base.resize((W, H), Image.BOX)).astype(np.float32)
    a = np.clip(painted * 1.0, 0, 1)[..., None]
    out = col * (1 - a) + new * a
    return out, painted
