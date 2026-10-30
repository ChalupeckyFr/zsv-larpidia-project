"""Plán hlavního města (F7), krok 3: generování uliční sítě (pracovní návrh).

Hierarchie: tepny z atlasu (RD-11, RD-12, R1 a další; geometrie beze změny) → okružní komunikace Náměstí čtyř → čtyři diagonální bulváry
(hranice čtvrtí) → uliční mřížky čtvrtí (každá s vlastním natočením) → staré město u přístavu (uličky podél pobřeží a kolmé průchody)
→ nábřeží. Všechny úseky se nakonec spojí do grafu (uzly, hrany, délky).
"""
from __future__ import annotations

import math
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw

import cp_data as C
import cp_geom as G
import cp_layout as LY
import raster
from cp_context import DID_INDEX
from cp_data import CELL, NX, NY, to_px
from cp_graph import StreetGraph

ROW = {"R1": 22.0, "A": 22.0, "B": 20.0, "S": 14.0, "P": 18.0, "C": 10.0, "L": 5.0}
DISTRICT_LATTICE = {
    # Čtvrti mají odlišné měřítko i natočení; rozteč se navíc lokálně vlní.
    "C-03": (9.0, 132.0, 82.0),
    "C-04": (-7.0, 144.0, 104.0),
    "C-05": (17.0, 122.0, 76.0),
    "C-06": (-2.0, 92.0, 68.0),
}
DISTRICT_GRID_STYLE = {
    "C-03": (0.30, 0.20, 3),
    "C-04": (0.34, 0.28, 4),
    "C-05": (0.32, 0.24, 3),
    "C-06": (0.27, 0.17, 3),
}
DISTRICT_STREET_NAMES = {
    "C-03": ("Javorová ulice", "Západní alej"),
    "C-04": ("Školní třída", "Severní sadová"),
    "C-05": ("Klimečkova třída", "Skleněná ulice"),
    "C-06": ("Muzejní třída", "Parková ulice"),
}
OLD_TOWN_DQ = 650.0                    # hloubka starého města od pobřeží (m)


def in_mask(mask, u, v):
    j = np.clip((np.asarray(u) / CELL).astype(int), 0, NX - 1)
    i = np.clip((np.asarray(v) / CELL).astype(int), 0, NY - 1)
    inside = (np.asarray(u) >= 0) & (np.asarray(u) < C.W_M) & (np.asarray(v) >= 0) & (np.asarray(v) < C.H_M)
    return mask[i, j] & inside


def runs_in_mask(pts, mask, step=4.0, min_len=28.0, simplify_tol=1.0):
    """Souvislé úseky polyline ležící v masce (vzorkováno po `step` m), zjednodušené."""
    rs = G.resample(pts, step)
    P = np.asarray(rs)
    ok = in_mask(mask, P[:, 0], P[:, 1])
    out = []
    d = np.diff(np.concatenate(([0], ok.astype(int), [0])))
    for s, e in zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]):
        seg = [tuple(p) for p in P[s:e]]
        if len(seg) >= 2 and G.length(seg) >= min_len:
            out.append(raster.simplify(seg, simplify_tol))
    return out


def clip_by_ring(pts, O, r):
    """Zahodí část polyline uvnitř kruhu (O, r); vrací 0–2 úseky."""
    if G.nearest_on_polyline(O, pts)[0] >= r:
        return [pts]
    rs = G.resample(pts, 3.0)
    out, cur = [], []
    for p in rs:
        if math.dist(p, O) >= r:
            cur.append(p)
        else:
            if len(cur) > 1:
                out.append(cur)
            cur = []
    if len(cur) > 1:
        out.append(cur)
    return [raster.simplify(c, 0.8) for c in out]


def generate(ctx, L, seed=20261024):
    rng = np.random.default_rng(seed)
    city = ctx.city
    O = ctx.O
    g = StreetGraph()
    names = {}
    # ---- rezervovaná území (bez uliční mřížky): parky, náměstí, státní čtvrť
    res_polys = [LY.circle(O, LY.CIVIC_R, 64), LY.rect_poly(L["park_central"]), LY.rect_poly(L["park_north"]), LY.rect_poly(L["park_east"]),
                 LY.rect_poly(L["park_west"]), LY.rect_poly(L["park_c05"]), LY.rect_poly(L["harbor_sq"]), LY.rect_poly(L["market_sq"]), LY.rect_poly(L["church_sq"]),
                 LY.rect_poly(L["museum"])]
    for k in ("hotel", "harbor_office", "ferry_terminal"):                   # budovy u přístavu: ulice se jim vyhnou (rezerva 10 m)
        s = dict(L[k])
        s["w"] += 20.0
        s["h"] += 20.0
        res_polys.append(LY.rect_poly(s))
    res = G.draw_mask((NY, NX), to_px, polys=res_polys)
    ctx.res = res
    # ---- tepny z atlasu (okraj okružní komunikace ořízneme)
    art_lines = []
    for r in city.roads:
        cls = {"R1": "R1", "R2": "A", "R3": "C"}[r["class"]]
        for part in clip_by_ring(r["pts"], O, LY.RING_R):
            pts = raster.simplify(part, 0.8)
            g.add(pts, cls=cls, atlas_id=r["id"], section=r["section"], name=None, district=None)
            if cls in ("R1", "A"):
                art_lines.append(pts)
    # ---- prodloužení tepny RD-12 od pobřežní silnice R1 k nábřeží (plán)
    g.add(L["rd12_ext"], cls="A", atlas_id="RD-12", section="surface", name=None, district=None, plan_new=True)
    art_lines.append(L["rd12_ext"])
    # ---- okružní komunikace
    g.add(L["ring"], cls="S", atlas_id=None, name="Okružní třída Náměstí čtyř", district=None, section="surface", no_snap=True)
    # ---- diagonální bulváry (hranice čtvrtí)
    diag_names = {45.0: "Jihovýchodní bulvár", 135.0: "Jihozápadní bulvár", 225.0: "Severozápadní bulvár", 315.0: "Severovýchodní bulvár"}
    blv = []
    for a_deg in (45.0, 135.0, 225.0, 315.0):
        a = math.radians(a_deg)
        d = (math.cos(a), math.sin(a))
        pts = [(O[0] + d[0] * LY.RING_R, O[1] + d[1] * LY.RING_R)]
        last_in = LY.RING_R
        r = LY.RING_R
        while r < 2400.0:
            r += 6.0
            p = (O[0] + d[0] * r, O[1] + d[1] * r)
            if in_mask(ctx.fp, [p[0]], [p[1]])[0]:
                last_in = r
            elif r - last_in > 60.0:
                break
        pts.append((O[0] + d[0] * last_in, O[1] + d[1] * last_in))
        g.add(pts, cls="B", atlas_id=None, name=diag_names[a_deg], district=None, section="surface")
        blv.append(pts)
    # ---- masky ke kontrole mřížek
    clear = G.draw_mask((NY, NX), to_px, lines=[(p, 22.0 / CELL) for p in art_lines] + [(p, 20.0 / CELL) for p in blv] + [(L["ring"], 22.0 / CELL)])
    ctx.clear = clear
    base_ok = ctx.fp & ~res & ~clear
    old = (ctx.did == DID_INDEX["C-06"]) & (ctx.dq > 14.0) & (ctx.dq < OLD_TOWN_DQ)
    ctx.old = old
    # ---- mřížky čtvrtí
    n_lat = 0
    for did, (theta, su, sv) in DISTRICT_LATTICE.items():
        ix = DID_INDEX[did]
        allowed = base_ok & (ctx.did == ix) & ~old
        jitter, skip, cross_every = DISTRICT_GRID_STYLE[did]
        runs = lattice_runs(ctx, ix, theta, su, sv, rng, allowed, jitter=jitter, skip=skip, cross_every=cross_every, origin=O)
        named_runs = sorted(range(len(runs)), key=lambda i: G.length(runs[i]), reverse=True)[:2]
        run_names = {ri: name for ri, name in zip(named_runs, DISTRICT_STREET_NAMES[did])}
        for ri, pts in enumerate(runs):
            mid = G.point_at(pts, G.length(pts) / 2)[0]
            # Klidné obytné ulice se střídají s užšími místními cestami.
            width = 7.0 + 2.1 * (1.0 + math.sin(mid[0] / 310.0 + mid[1] / 470.0)) + rng.uniform(-0.7, 0.7)
            g.add(pts, cls="C", atlas_id=None, name=run_names.get(ri), district=did, section="surface", row=max(6.0, min(11.0, width)))
        n_lat += len(runs)
    ctx.n_lattice = n_lat
    # ---- staré město: uličky podél pobřeží (vrstevnice vzdálenosti) a kolmé průchody
    old_ok = old & ~res & ~clear
    levels = [55.0, 125.0, 190.0, 300.0, 380.0, 465.0, 555.0, OLD_TOWN_DQ - 8.0]
    gdq = SimpleNamespace(x0=0.0, y0=0.0, dx=CELL)
    for lev in levels:
        for ln in raster.contour_lines(gdq, ctx.dq, lev):
            pts = raster.simplify(ln, 1.2)
            if G.length(pts) < 60.0:
                continue
            for run in runs_in_mask(pts, old_ok, step=4.0, min_len=30.0):
                g.add(run, cls="C", atlas_id=None, name=None, district="C-06", section="surface", row=8.0, level=lev)
    lane_clear = G.draw_mask((NY, NX), to_px, lines=[(p, 44.0 / CELL) for p in art_lines])
    lanes = old_lanes(ctx, old_ok & ~lane_clear, rng, levels)
    for pts in lanes:
        g.add(pts, cls="L", atlas_id=None, name=None, district="C-06", section="surface", ext=34.0)
    # ---- nábřeží (promenáda) o 12 m dál od vody než pobřeží
    g.add(ctx.quay_in, cls="P", atlas_id=None, name="Nábřeží 16. června", district="C-06", section="surface")
    # ---- spojka k nové čtvrti Východní nábřeží (zeleným koridorem severně od parku)
    g.add([(4560.0, 2140.0), (4900.0, 2270.0), (5250.0, 2390.0), (5580.0, 2475.0)], cls="B", atlas_id=None, name="Třída Východního nábřeží", district="C-05", section="surface", ext=60.0)
    # ---- přístupové ulice ke stanicím
    for s in city.stations:
        p = (s["u"], s["v"])
        best = (1e9, None)
        for lines in art_lines + blv:
            d, q, _ = G.nearest_on_polyline(p, lines)
            if d < best[0]:
                best = (d, q)
        if best[1] is not None and 6.0 < best[0] < 260.0:
            g.add([p, best[1]], cls="C", atlas_id=None, name=f"Přístup ke stanici {s['id']}", district=None, section="surface", station=s["id"])
    return g


def lattice_runs(ctx, ix, theta_deg, su, sv, rng, allowed, step=4.0, jitter=0.16, skip=0.10, cross_every=3, origin=None):
    th = math.radians(theta_deg)
    e1 = (math.cos(th), math.sin(th))
    e2 = (-math.sin(th), math.cos(th))
    ys, xs = np.nonzero(ctx.did == ix)
    uu, vv = (xs[::9] + 0.5) * CELL, (ys[::9] + 0.5) * CELL
    a = uu * e1[0] + vv * e1[1]
    b = uu * e2[0] + vv * e2[1]
    a0, a1, b0, b1 = a.min() - su, a.max() + su, b.min() - sv, b.max() + sv

    def seq(lo, hi, st):
        vals, x = [], lo + rng.uniform(0, st)
        while x < hi:
            vals.append(x)
            x += st * (1.0 + jitter * rng.uniform(-1, 1)) * (2.0 if rng.random() < skip else 1.0)
        return vals
    out = []
    lines = [("a", x) for x in seq(a0, a1, su)] + [("b", x) for x in seq(b0, b1, sv)]
    kind_idx = {"a": 0, "b": 0}
    for kind, val in lines:
        kind_idx[kind] += 1
        if kind == "a":
            t = np.arange(b0, b1, step)
            u, v = val * e1[0] + t * e2[0], val * e1[1] + t * e2[1]
        else:
            t = np.arange(a0, a1, step)
            u, v = t * e1[0] + val * e2[0], t * e1[1] + val * e2[1]
        mask = allowed if kind_idx[kind] % cross_every == 0 else allowed & ~ctx.rail_mask
        ok = in_mask(mask, u, v)
        d = np.diff(np.concatenate(([0], ok.astype(int), [0])))
        for s, e in zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]):
            if (e - s) * step < 30.0:
                continue
            # Společné hladké přemístění ulic zachová křižovatky, ale rozbije pravítkový vzhled.
            pts = [(float(u[k]), float(v[k])) for k in range(s, e)]
            if origin:
                ox, oy = origin
                bent = []
                for x, y in pts:
                    dx, dy = x - ox, y - oy
                    wx = 18.0 * math.sin(dy / 245.0 + dx / 810.0) + 8.0 * math.sin(dy / 108.0 - dx / 530.0)
                    wy = 20.0 * math.sin(dx / 275.0 - dy / 760.0) + 7.0 * math.sin(dx / 122.0 + dy / 610.0)
                    bent.append((x + wx, y + wy))
                pts = bent
            out.append(raster.simplify(pts, 6.0))
    return out


def old_lanes(ctx, old_ok, rng, levels):
    """Uličky starého města: proudnice gradientu vzdálenosti od pobřeží (kolmé na uličky podél břehu), a to jednak od nábřeží,
    jednak jako krátké průchody mezi sousedními uličkami podél břehu (dělí bloky na menší)."""
    dq = raster.gauss(np.where(ctx.land, ctx.dq, 0.0).astype(np.float32), 5.0)
    gy, gx = np.gradient(dq, CELL)
    gdq = SimpleNamespace(x0=0.0, y0=0.0, dx=CELL)

    def cell(q):
        return min(NY - 1, max(0, int(q[1] / CELL))), min(NX - 1, max(0, int(q[0] / CELL)))

    def trace(p, stop_d, max_steps=600):
        pts = [p]
        q = p
        for _ in range(max_steps):
            i, j = cell(q)
            vx, vy = gx[i, j], gy[i, j]
            n = math.hypot(vx, vy)
            if n < 1e-6:
                break
            q = (q[0] + 4.0 * vx / n, q[1] + 4.0 * vy / n)
            pts.append(q)
            if ctx.dq[cell(q)] > stop_d:
                break
        return raster.simplify(pts, 1.5)

    out = []
    occ = Image.new("L", (NX, NY), 0)
    occ_d = ImageDraw.Draw(occ)

    def accept(run):
        """Zamítne průchod, který by téměř celý ležel těsně vedle už přijaté uličky (úzké pruhy bloků)."""
        P = G.resample(run, 6.0)
        near = sum(1 for p in P if 0 <= int(p[0] / CELL) < NX and 0 <= int(p[1] / CELL) < NY and occ.getpixel((int(p[0] / CELL), int(p[1] / CELL))) > 0)
        if near > 0.35 * len(P):
            return False
        occ_d.line([(p[0] / CELL, p[1] / CELL) for p in run], fill=255, width=7)
        out.append(run)
        return True

    # a) od nábřeží do hloubky (část uliček končí dřív)
    total = G.length(ctx.quay_in)
    s_pos = 18.0
    while s_pos < total - 18.0:
        p, _ = G.point_at(ctx.quay_in, s_pos)
        s_pos += rng.uniform(36.0, 70.0)
        i, j = cell(p)
        if not ctx.land[i, j]:
            continue
        stop_d = OLD_TOWN_DQ if rng.random() < 0.5 else rng.uniform(240.0, 520.0)
        for run in runs_in_mask(trace(p, stop_d), old_ok, step=4.0, min_len=36.0):
            accept(run)
    # b) průchody mezi sousedními uličkami podél břehu
    lv = [14.0] + list(levels)
    for a_lev, b_lev in zip(lv[:-1], lv[1:]):
        for ln in raster.contour_lines(gdq, ctx.dq, a_lev):
            rs = G.resample(ln, 4.0)
            s = rng.uniform(10.0, 40.0)
            total = 4.0 * (len(rs) - 1)
            while s < total:
                p = rs[min(len(rs) - 1, int(s / 4.0))]
                s += rng.uniform(52.0, 105.0)
                if rng.random() < 0.28:
                    continue
                i, j = cell(p)
                if not old_ok[i, j]:
                    continue
                for run in runs_in_mask(trace(p, b_lev), old_ok, step=4.0, min_len=22.0):
                    accept(run)
    return out
