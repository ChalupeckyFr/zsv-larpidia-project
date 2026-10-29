"""Satelitní reference hlavního města (S-03): zástavba z plánu CP-01 (domy, bloky, ulice, prostory, klíčové budovy) pro `render_sat.render`.

Souřadnice plánu (lokální metry, počátek v SZ rohu okna) přesně odpovídají pixelům S-03 (okno = okno plánu), takže 1 px = `mpp` m.
Domy se nečtou z generátoru, ale z `cp_houses.geojson`, takže plán, satelit a šikmé pohledy ukazují tytéž budovy. Bloky v rezervě rozvoje
zůstávají přírodní krajinou, plánované ulice v rezervě jsou jen polní cesty. Stíny padají na sever (slunce z jihu). Vše je simulace a pracovní návrh.
"""
from __future__ import annotations

import json
import math

import numpy as np
from PIL import Image, ImageDraw

import cp_geom as G
import cp_houses as HS
import geom
from canon import ATLAS

CAP = ATLAS / "current" / "capital"

STREET_COL = {"R1": ((116, 114, 116), (182, 178, 170)), "A": ((112, 112, 116), (182, 178, 170)), "B": ((114, 114, 118), (182, 178, 170)), "S": ((116, 114, 118), (182, 178, 170)),
              "P": ((214, 198, 164), (226, 214, 184)), "C": ((124, 122, 122), (178, 174, 166)), "L": ((156, 150, 142), (156, 150, 142))}
TRACK_COL = (170, 152, 122)                                   # plánovaná ulice v rezervě: polní cesta
GROUND = {"old_town_mixed": (152, 142, 126), "promenade_retail": (160, 150, 136), "retail_main": (150, 146, 138), "civic_mixed": (170, 160, 146), "transit_mixed": (146, 142, 130),
          "residential_mid": (120, 140, 94), "residential_low": (112, 144, 86), "school": (126, 152, 102), "new_waterfront": (136, 142, 124), "hotel_premium": (150, 140, 126)}
KEY_ROOF = {"parliament": (92, 102, 128), "admin": (150, 122, 112), "museum": (100, 114, 130), "church": (98, 84, 78), "market_hall": (164, 124, 74), "hotel_premium": (176, 104, 84),
            "school": (80, 118, 164), "harbour_office": (130, 130, 128), "ferry_terminal": (120, 120, 124)}


def load_plan():
    def fc(name):
        p = CAP / f"cp_{name}.geojson"
        return json.loads(p.read_text(encoding="utf-8"))["features"] if p.exists() else []
    return {k: fc(k) for k in ("blocks", "streets", "spaces", "buildings", "houses")}


def ring(feature):
    return [tuple(p) for p in feature["geometry"]["coordinates"][0][:-1]]


def houses_of(plan):
    return [HS.house_from_feature(f) for f in plan["houses"]]


def key_buildings(plan):
    return [(ring(f), HS.KEY_H.get(f["properties"]["subtype"], 10.0)) for f in plan["buildings"] if f["properties"]["type"] == "building"]


def height_raster(shape_hw, mpp, plan=None):
    """Výškové pole budov (m nad terénem) na rastru okna plánu: sedlové střechy domů a ploché klíčové budovy."""
    plan = plan or load_plan()
    return HS.height_field(houses_of(plan), key_buildings(plan), shape_hw, mpp)


def _mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def lit_half(r):
    """Polovina sedlové střechy přivrácená ke slunci (jih = větší v): hřeben leží podél delší strany."""
    a, b, c, d = r
    if math.dist(a, b) >= math.dist(b, c):
        h1, h2 = [a, b, _mid(b, c), _mid(a, d)], [_mid(a, d), _mid(b, c), c, d]
    else:
        h1, h2 = [b, c, _mid(c, d), _mid(a, b)], [_mid(a, b), _mid(c, d), d, a]
    return h1 if sum(p[1] for p in h1) >= sum(p[1] for p in h2) else h2


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

    # --- základ zastavěných bloků (rezerva rozvoje zůstává krajinou; zahrádkové okraje splývají s okolím; dvory starého města střídavě dlážděné a zahradní)
    for f in plan["blocks"]:
        pr = f["properties"]
        if pr.get("build_state") == "reserve":
            continue
        use = pr["land_use"]
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
            if not HS.inside_all(G.oriented_rect(c[0], c[1], w + 40, h + 40, ang), wp):
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
    # --- ulice: zastavěné (chodník + vozovka) a plánované v rezervě (polní cesta)
    order = ["L", "C", "P", "S", "B", "A", "R1"]
    edges = sorted(plan["streets"], key=lambda f: order.index(f["properties"]["cls"]))
    for f in edges:
        pr = f["properties"]
        cls = pr["cls"]
        pts = P(f["geometry"]["coordinates"])
        if pr.get("state") == "planned":
            wt = max(1, int(round(3.0 * k)))
            d.line(pts, fill=TRACK_COL, width=wt, joint="curve")
            dm.line(pts, fill=255, width=wt, joint="curve")
            continue
        row = pr["row_m"]
        asphalt, walk = STREET_COL[cls]
        w_out = max(1, int(round(row * k)))
        w_in = max(1, int(round((row - (0 if cls in ("L", "P") else 4.0)) * k)))
        d.line(pts, fill=walk, width=w_out, joint="curve")
        d.line(pts, fill=asphalt, width=w_in, joint="curve")
        dm.line(pts, fill=255, width=w_out, joint="curve")
    # --- budovy: zahrady chat, stíny, pak střechy
    houses = houses_of(plan)
    rects, roofs, heights, gable = [], [], [], []
    for h in houses:
        if h["kind"] == "fringe":                                       # chata v rezervě: malá zahrada kolem domu
            gar = G.oriented_rect(h["c"][0], h["c"][1], h["w"] + 14.0, h["d"] + 12.0, h["ang"])
            d.polygon(P(gar), fill=(118, 148, 92))
            dm.polygon(P(gar), fill=255)
        rects.append(h["poly"])
        roofs.append(HS.hex_rgb(h["roof_col"]))
        heights.append(h["height_m"] + 0.5 * h["ridge_m"])
        gable.append(h["ridge_m"] > 0)
    for f in plan["buildings"]:
        pr = f["properties"]
        if pr["type"] != "building":
            continue
        rects.append(ring(f))
        roofs.append(KEY_ROOF.get(pr["subtype"], (120, 110, 104)))
        heights.append(HS.KEY_H.get(pr["subtype"], 10.0))
        gable.append(False)
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
    for r, c_, gb in zip(rects, roofs, gable):
        sh_c = int(rng.integers(-8, 9))
        d.polygon(P(r), fill=(max(0, min(255, c_[0] + sh_c)), max(0, min(255, c_[1] + sh_c)), max(0, min(255, c_[2] + sh_c))))
        if gb and len(r) == 4:                             # sedlová střecha: polovina přivrácená ke slunci je světlejší
            d.polygon(P(lit_half(r)), fill=(min(255, c_[0] + 16 + sh_c), min(255, c_[1] + 16 + sh_c), min(255, c_[2] + 16 + sh_c)))
        dm.polygon(P(r), fill=255)
    # --- stromy: podél zastavěných tepen a v parcích
    for f in plan["streets"]:
        pr = f["properties"]
        if pr["cls"] not in ("A", "B", "S", "P", "R1") or pr.get("state") == "planned":
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
