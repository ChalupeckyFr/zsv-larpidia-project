"""Plán hlavního města (F7), krok 1: rastrový kontext – půdorys zástavby, čtvrtě (výseče kolem centra), koleje, nábřeží.

Půdorys vychází z modelových půdorysů sídla C-01 z F3 (tři laloky), doplněných o pás kolem historického přístavu C-02 a koridor podél
tepny RD-12 k přístavu (rozpor C-17), a uzavřených morfologicky, aby byl souvislý. Čtyři čtvrtě C-03…C-06 jsou výseče kolem
centrálního náměstí (průsečík tepen RD-11 a RD-12): západ Chalupecká, sever Kynčlova, východ Klimečkova, jih Žemličkova.
Vše je pracovní návrh.
"""
from __future__ import annotations

import math
from types import SimpleNamespace

import numpy as np

import cp_data as C
import cp_geom as G
import raster
from cp_data import CELL, NX, NY, to_px

DISTRICT_IDS = {"E": "C-05", "S": "C-06", "W": "C-03", "N": "C-04"}
DISTRICT_NAMES = {"C-03": "Chalupecká čtvrť", "C-04": "Kynčlova čtvrť", "C-05": "Klimečkova čtvrť", "C-06": "Žemličkova čtvrť"}
DID_INDEX = {"C-03": 1, "C-04": 2, "C-05": 3, "C-06": 4}        # hodnoty v rastru čtvrtí (0 = mimo město)


OLD_C = (3250.0, 0.0)              # střed starého města na pobřeží (u, dq)
OLD_A = (820.0, 700.0)             # poloosy půlelipsy (podél pobřeží, do vnitrozemí)


def _circle(c, r, n=48):
    return [(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def uv_grid():
    jj, ii = np.meshgrid(np.arange(NX), np.arange(NY))
    return (jj + 0.5) * CELL, (ii + 0.5) * CELL


def dist_to_points(pts_m, factor=4):
    """Vzdálenost (m) k nejbližšímu z bodů; počítáno na hrubší mřížce a zvětšeno na rastr plánu."""
    cw, ch = NX // factor, NY // factor
    cu = (np.arange(cw) + 0.5) * CELL * factor
    cv = (np.arange(ch) + 0.5) * CELL * factor
    U, V = np.meshgrid(cu.astype(np.float32), cv.astype(np.float32))
    fu, fv = U.ravel(), V.ravel()
    best = np.full(fu.shape, np.inf, dtype=np.float32)
    P = np.asarray(pts_m, dtype=np.float32)
    for s in range(0, len(P), 120):
        p = P[s:s + 120]
        d2 = (fu[:, None] - p[None, :, 0]) ** 2 + (fv[:, None] - p[None, :, 1]) ** 2
        best = np.minimum(best, d2.min(axis=1))
    d = np.sqrt(best).reshape(U.shape)
    from PIL import Image
    return np.asarray(Image.fromarray(d.astype(np.float32), mode="F").resize((NX, NY), Image.BILINEAR))


class Ctx:
    pass


def build_ctx(city: C.City) -> Ctx:
    ctx = Ctx()
    ctx.city = city
    land = city.land_mask()
    ctx.land = land
    r11 = next(r for r in city.roads if r["id"] == "RD-11")["pts"]
    r12 = next(r for r in city.roads if r["id"] == "RD-12")["pts"]
    p, s11, s12 = G.polyline_intersections(r11, r12)[0]
    ctx.O = (float(p[0]), float(p[1]))                  # střed města = střed centrálního náměstí
    ctx.r11, ctx.r12 = r11, r12
    # jižní konec tepny RD-12 (končí na pobřežní silnici R1, 240 m před nábřežím; plán ji prodlužuje k nábřeží)
    ctx.rd12_south_end = r12[0] if r12[0][1] > r12[-1][1] else r12[-1]
    U, V = uv_grid()
    # podepsaná vzdálenost k pobřeží (m; záporná ve vodě) – pro uspořádání starého města
    coast_pts = G.resample([q for q in city.coast if -200 <= q[0] <= C.W_M + 200 and -200 <= q[1] <= C.H_M + 200], 12.0)
    dq = dist_to_points(coast_pts)
    ctx.dq = np.where(land, dq, -dq)
    rings = G.draw_mask((NY, NX), to_px, polys=city.settle_rings)
    beach = G.draw_mask((NY, NX), to_px, polys=city.beaches)
    # staré město: půlelipsa kolem přístavu (u středu 3250 m; 820 m do stran, 700 m do vnitrozemí)
    old_zone = land & (((U - OLD_C[0]) / OLD_A[0]) ** 2 + (ctx.dq / OLD_A[1]) ** 2 < 1.0) & (ctx.dq > 0)
    # nová čtvrť Východní nábřeží u stanice ST-L3-05 a zelený koridor k východnímu laloku
    st5 = city.station("ST-L3-05")
    east_new = G.draw_mask((NY, NX), to_px, polys=[_circle((st5["u"], st5["v"] - 90.0), 340.0)], lines=[([(4850.0, 2330.0), (st5["u"], st5["v"] - 90.0)], 160.0 / CELL)])
    fp = (rings | old_zone | east_new) & land
    fp = (raster.gauss(fp.astype(np.float32), 90.0 / CELL) > 0.42) & land
    ctx.beach_near = raster.gauss(beach.astype(np.float32), 20.0 / CELL) > 0.2
    fp &= ~ctx.beach_near
    ctx.fp = fp
    # zelené klíny: pevnina uvnitř okruhu metra L3 (elipsa kolem stanic W, N, E, S), která není zastavěná
    inloop = ((U - 2800.0) / 1850.0) ** 2 + ((V - 1700.0) / 1150.0) ** 2 < 1.0
    rail_all = G.draw_mask((NY, NX), to_px, lines=[(r["pts"], 30.0 / CELL) for r in city.rails if r["line"] in ("L1", "L2") and r["section"] == "surface"])
    ctx.green = land & inloop & ~fp & ~rail_all & (ctx.dq > 30.0)
    ctx.old_zone = old_zone & fp
    # čtvrtě
    ang = np.degrees(np.arctan2(V - ctx.O[1], U - ctx.O[0]))
    did = np.zeros((NY, NX), dtype=np.int8)
    wedge_sel = {"E": (ang >= -45) & (ang < 45), "S": (ang >= 45) & (ang < 135),
                 "W": (ang >= 135) | (ang < -135), "N": (ang >= -135) & (ang < -45)}
    for key, sel in wedge_sel.items():
        did[fp & sel] = DID_INDEX[DISTRICT_IDS[key]]
    ctx.did = did
    ctx.U, ctx.V = U, V
    ctx.ang = ang
    ctx.east_new = east_new & fp
    ctx.districts = {}
    for did_id, ix in DID_INDEX.items():
        polys = G.mask_to_polygons(did == ix, 0.0, 0.0, CELL, min_area=2e4, simplify_tol=2.5)
        ctx.districts[did_id] = polys
    # koleje: koridor 26 m kolem povrchových úseků L1 a L2
    rails = [(r["pts"], 26.0 / CELL) for r in city.rails if r["line"] in ("L1", "L2") and r["section"] == "surface"]
    ctx.rail_mask = G.draw_mask((NY, NX), to_px, lines=rails)
    ctx.rail_lines = [r for r in city.rails if r["line"] in ("L1", "L2") and r["section"] == "surface"]
    # nábřeží: úsek pobřeží u přístavu, vyhlazený
    coast = [q for q in city.coast if 2350.0 <= q[0] <= 4150.0 and q[1] > 3300.0]
    coast.sort(key=lambda q: q[0])
    ctx.quay = raster.chaikin(coast, closed=False, iters=2)
    ctx.quay_in = G.offset_polyline(ctx.quay, 12.0)          # osa nábřežní ulice (12 m od vody)
    u0, v0 = ctx.rd12_south_end
    ints = G.polyline_intersections([(u0, v0), (u0, v0 + 700.0)], ctx.quay_in)
    ctx.rd12_quay_pt = ints[0][0] if ints else G.nearest_on_polyline((u0, v0), ctx.quay_in)[1]   # prodloužená tepna RD-12 jde rovně na jih k nábřeží
    return ctx


def v_at_dq(ctx, u, d):
    """Souřadnice v (jižněji = větší) bodu na sloupci u, kde vzdálenost od pobřeží do vnitrozemí je právě d metrů."""
    j = min(NX - 1, max(0, int(u / CELL)))
    col = ctx.dq[:, j]
    idx = np.nonzero(col >= d)[0]
    if len(idx) == 0:
        return float(np.nonzero(col > 0)[0].max() * CELL)
    i = int(idx.max())
    return (i + 0.5) * CELL
