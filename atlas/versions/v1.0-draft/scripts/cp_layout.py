"""Plán hlavního města (F7), krok 2: kompozice veřejných prostor a klíčových budov (pracovní návrh).

Střed města tvoří Náměstí čtyř: okružní komunikace kolem Parlamentní zahrady s budovou parlamentu; čtyři správní budovy stojí
v „větrníkovém“ uspořádání (každá patří jedné čtvrti, poblíž její tepny). Staré město s tržištěm, kostelem a promenádou leží u přístavu
(polohy se odvozují od nábřeží a od prodloužené tepny RD-12). Souřadnice jsou lokální metry plánu (u východ, v jih).
Poloha parlamentu a správních budov je otevřené rozhodnutí týmu (O19).
"""
from __future__ import annotations

import math

import cp_context as CX
import cp_geom as G

# ---- parametry
RING_R = 72.0           # poloměr osy okružní komunikace kolem parlamentní zahrady (m)
GARDEN_R = 58.0         # poloměr zahrady (m)
CIVIC_R = 170.0         # poloměr státní čtvrti (bez uliční mřížky)
ADMIN_R = 138.0         # vzdálenost správních budov od středu
ADMIN_OFFSET_DEG = 26.0


def circle(c, r, n=48):
    return [(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def rect(c, w, h, ang):
    return G.oriented_rect(c[0], c[1], w, h, ang)


def rect_poly(spec):
    return rect(spec["c"], spec["w"], spec["h"], spec["ang"])


def station_layout(ctx):
    """Půdorysy stanic: povrchové (W, N, E – na L2/L1) mají budovu, nástupiště a předprostor na straně města; podzemní (S, L3-05) mají vstupní pavilony."""
    O = ctx.O
    out = {}
    surf = [r["pts"] for r in ctx.rail_lines]
    for s in ctx.city.stations:
        p = (s["u"], s["v"])
        sid = s["id"]
        if sid in ("ST-W", "ST-N", "ST-E"):
            best = min(((G.nearest_on_polyline(p, pts), pts) for pts in surf), key=lambda x: x[0][0])
            (dist, q, sl), pts = best
            _, t = G.point_at(pts, sl)
            n = (-t[1], t[0])
            if (O[0] - p[0]) * n[0] + (O[1] - p[1]) * n[1] < 0:      # normála směřuje k městu
                n = (-n[0], -n[1])
            ang = math.degrees(math.atan2(t[1], t[0]))
            big = sid == "ST-W"
            bw, bh = (96.0, 20.0) if big else (66.0, 16.0)
            out[sid] = {
                "kind": "surface",
                "building": G.oriented_rect(p[0] + n[0] * 28.0, p[1] + n[1] * 28.0, bw, bh, ang),
                "platform": G.oriented_rect(p[0], p[1], bw + 24.0, 9.0, ang),
                "plaza": G.oriented_rect(p[0] + n[0] * 70.0, p[1] + n[1] * 70.0, bw + 24.0, 54.0, ang),
                "axis": (t, n),
            }
        else:
            near = None
            out[sid] = {
                "kind": "underground",
                "building": None,
                "entrances": [G.oriented_rect(p[0] - 17.0, p[1], 13.0, 8.0, 0.0), G.oriented_rect(p[0] + 17.0, p[1], 13.0, 8.0, 0.0)],
                "plaza": G.oriented_rect(p[0], p[1], 66.0, 38.0, 0.0),
            }
    return out


def build_layout(ctx):
    O = ctx.O
    L = {"O": O}
    # ---- Náměstí čtyř
    ring = circle(O, RING_R, 64)
    L["ring"] = ring + [ring[0]]
    L["garden"] = circle(O, GARDEN_R, 48)
    L["civic_zone"] = circle(O, CIVIC_R, 64)
    L["parliament"] = {"c": O, "w": 56.0, "h": 34.0, "ang": 0.0}
    admin = []
    for key, a_k in (("W", 180.0), ("N", 270.0), ("E", 0.0), ("S", 90.0)):
        a = math.radians(a_k + ADMIN_OFFSET_DEG)
        c = (O[0] + ADMIN_R * math.cos(a), O[1] + ADMIN_R * math.sin(a))
        admin.append({"district_key": key, "c": c, "w": 52.0, "h": 30.0, "ang": math.degrees(a) + 90.0})
    L["admin"] = admin
    # ---- Muzeum a Centrální park (jihozápadně od státní čtvrti, západně od tepny RD-12)
    L["museum"] = {"c": (O[0] - 290.0, O[1] + 215.0), "w": 74.0, "h": 46.0, "ang": 0.0}
    L["park_central"] = {"c": (O[0] - 205.0, O[1] + 345.0), "w": 330.0, "h": 190.0, "ang": 0.0}
    # ---- stanice
    L["stations"] = {s["id"]: (s["u"], s["v"]) for s in ctx.city.stations}
    # ---- staré město a přístav (jih)
    q = ctx.rd12_quay_pt                                           # konec prodloužené tepny RD-12 na nábřeží
    L["rd12_ext"] = [ctx.rd12_south_end, q]
    L["harbor_sq"] = {"c": (q[0], q[1] - 52.0), "w": 124.0, "h": 70.0, "ang": 0.0}              # Přístavní náměstí na konci tepny
    u_m = q[0] + 290.0
    L["market_sq"] = {"c": (u_m, CX.v_at_dq(ctx, u_m, 190.0)), "w": 100.0, "h": 66.0, "ang": 0.0}   # Tržní náměstí
    L["market_hall"] = {"c": (u_m, CX.v_at_dq(ctx, u_m, 190.0) - 14.0), "w": 54.0, "h": 22.0, "ang": 0.0}
    u_c = q[0] - 400.0
    vc = CX.v_at_dq(ctx, u_c, 205.0)
    L["church_sq"] = {"c": (u_c, vc), "w": 74.0, "h": 60.0, "ang": 0.0}                         # Kostelní náměstí
    L["church"] = {"c": (u_c, vc - 8.0), "w": 40.0, "h": 15.0, "ang": 0.0, "transept": (14.0, 28.0)}
    u_h = q[0] + 360.0
    L["hotel"] = {"c": (u_h, CX.v_at_dq(ctx, u_h, 92.0)), "w": 64.0, "h": 36.0, "ang": 0.0}      # HV-01 – prémiový hotel nad promenádou
    u_f = q[0] + 105.0
    L["ferry_pier"] = {"c": (u_f, CX.v_at_dq(ctx, u_f, -34.0)), "w": 22.0, "h": 68.0, "ang": 0.0}   # přístaviště lodní linky FERRY-1 (do vody)
    L["ferry_terminal"] = {"c": (u_f, L["ferry_pier"]["c"][1] - 58.0), "w": 38.0, "h": 16.0, "ang": 0.0}
    L["harbor_office"] = {"c": (q[0] - 118.0, q[1] - 46.0), "w": 46.0, "h": 22.0, "ang": 0.0}
    # ---- parky u stanic a mezi východním lalokem a novou čtvrtí
    st = ctx.city.station
    L["park_north"] = {"c": (st("ST-N")["u"] + 110.0, st("ST-N")["v"] + 330.0), "w": 260.0, "h": 150.0, "ang": 0.0}
    L["park_east"] = {"c": (4880.0, 2380.0), "w": 300.0, "h": 120.0, "ang": 16.0}
    L["park_c05"] = {"c": (4200.0, 2000.0), "w": 240.0, "h": 130.0, "ang": 12.0}
    L["park_west"] = {"c": (st("ST-W")["u"] + 520.0, st("ST-W")["v"] + 330.0), "w": 240.0, "h": 150.0, "ang": -8.0}
    return L
