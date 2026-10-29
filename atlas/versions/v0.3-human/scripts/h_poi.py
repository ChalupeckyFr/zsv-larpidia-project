"""Přístavy, letiště a body zájmu (F3). NÁVRH (proposed).

Kanon: ≥ 3 přístavy (historický, nákladní, severní rybářský, marina Paralandu), ~2 letiště (regionální + malá plocha na Paralandu),
vyhlídky na útesech s bezpečným přístupem (žádné pobídky ke skokům), prameny a studánky, vodopád, jeskyně, lyžařská hora s krátkou sezonou,
zaoblený vrch pro turistiku a paragliding, menší počet prémiových hotelů na hlavním ostrově, Paraland: hrad/zámeček, zřícenina, aquapark, resorty.
"""
from __future__ import annotations

import math

import numpy as np

import geom
import h_rail as hr
import raster


def unit(v):
    L = math.hypot(*v) or 1.0
    return (v[0] / L, v[1] / L)


def coast_frame(poly, p):
    d, q, i = geom.nearest_on_poly(p, poly)
    a, b = poly[i], poly[(i + 1) % len(poly)]
    t = unit((b[0] - a[0], b[1] - a[1]))
    n_out = (t[1], -t[0])          # vnější normála (do moře)
    return q, t, n_out, i


def pt(o, a, b, s=1.0):
    """o + a*(první) + b*(druhý) pomocí 2D bázových vektorů."""
    return (o[0] + a[0] * s + b[0] * s, o[1] + a[1] * s + b[1] * s)


def _lin(o, ux, kx, uy, ky):
    return (o[0] + ux[0] * kx + uy[0] * ky, o[1] + ux[1] * kx + uy[1] * ky)


def chain_between(poly, ia, ib):
    n = len(poly)
    fw = []
    i = ia
    while i != ib:
        fw.append(poly[i])
        i = (i + 1) % n
    fw.append(poly[ib])
    bw = []
    i = ia
    while i != ib:
        bw.append(poly[i])
        i = (i - 1) % n
    bw.append(poly[ib])
    return fw if len(fw) <= len(bw) else bw


def sea_ok(world, p):
    return not world.land[world.g.cell_of(*p)]


def breakwater_harbor(world, poly, anchor, width=0.9, mouth=0.18, depth=0.42, name=""):
    """Hradby a přístavní pánev u pobřeží v bodě `anchor`. Vrací dict s polylines a polygonem pánve."""
    q, t, n, i = coast_frame(poly, anchor)
    # t = směr podél pobřeží; hradba A zleva (−t), hradba B zprava (+t)
    a0 = _lin(q, t, -width / 2, n, 0.0)
    b0 = _lin(q, t, +width / 2, n, 0.0)
    a_line = [a0, _lin(q, t, -width / 2, n, depth * 0.55), _lin(q, t, -width / 2 + 0.06, n, depth * 0.95), _lin(q, t, -mouth / 2 - 0.02, n, depth)]
    b_line = [b0, _lin(q, t, +width / 2, n, depth * 0.40), _lin(q, t, +width / 2 - 0.08, n, depth * 0.70), _lin(q, t, +mouth / 2 + 0.02, n, depth * 0.78)]
    ia = min(range(len(poly)), key=lambda k: math.dist(poly[k], a0))
    ib = min(range(len(poly)), key=lambda k: math.dist(poly[k], b0))
    quay = chain_between(poly, ia, ib)
    basin = list(quay) + list(reversed(b_line)) + list(reversed(a_line))
    ok = all(sea_ok(world, p) for p in a_line[1:] + b_line[1:])
    return {"anchor": q, "tangent": t, "normal": n, "mole_a": a_line, "mole_b": b_line, "quay": quay, "basin": basin, "ok_sea": ok, "name": name}


def piers(world, poly, anchor, count=3, length=0.45, spacing=0.30, width=0.06, along=0.0):
    q, t, n, i = coast_frame(poly, anchor)
    out = []
    for k in range(count):
        off = (k - (count - 1) / 2) * spacing + along
        s = _lin(q, t, off, n, 0.0)
        e = _lin(q, t, off, n, length)
        a = _lin(s, t, -width / 2, n, 0)
        b = _lin(s, t, +width / 2, n, 0)
        c = _lin(e, t, +width / 2, n, 0)
        d = _lin(e, t, -width / 2, n, 0)
        out.append({"pts": [a, b, c, d], "center_line": [s, e], "ok_sea": sea_ok(world, e)})
    return out


def build_ports(world):
    main, para = world.o["main"], world.o["para"]
    P = world.pos
    ports = []
    h = breakwater_harbor(world, main, P("C-02"), width=0.95, mouth=0.20, depth=0.48, name="Historický přístav")
    ports.append({"id": "C-02", "name": "Historický přístav hlavního města", "kind": "historic_harbor", "island": "main", "geom": h,
                  "note": "nábřeží, butiky, promenády; vlnolam proti tajfunům z jihu (bible disaster_planning)", "exist": "approved", "name_status": "proposed"})
    h = breakwater_harbor(world, main, P("I-03"), width=1.1, mouth=0.30, depth=0.38, name="Nákladní přístav")
    pi = piers(world, main, P("I-03"), count=3, length=0.42, spacing=0.34, width=0.07, along=0.0)
    ports.append({"id": "I-03", "name": "Nákladní přístav", "kind": "cargo_port", "island": "main", "geom": h, "piers": pi,
                  "note": "export řasové suroviny a luxusního zboží; v zátoce chráněné poloostrovem", "exist": "proposed", "name_status": "proposed"})
    # severní rybářský přístav u Ōru Maito: dno zátoky
    cand = min((p for p, ty in zip(main, world.o["main_types"]) if ty == "harbor" and p[1] < 5.0), key=lambda p: math.dist(p, (13.7, 3.0)))
    h = breakwater_harbor(world, main, cand, width=0.6, mouth=0.14, depth=0.30, name="Rybářský přístav")
    ports.append({"id": "H-01", "name": "Severní rybářský přístav", "kind": "fishing_port", "island": "main", "geom": h,
                  "note": "malý přístav v zátoce u Ōru Maito; rybí trh", "exist": "proposed", "name_status": "proposed", "at": cand})
    # marina Paralandu: nejzápadnější vrchol typu harbor
    harb = [p for p, ty in zip(para, world.o["para_types"]) if ty == "harbor"]
    ux, uy = math.cos(math.radians(38.0)), math.sin(math.radians(38.0))
    tip = max(main, key=lambda p: p[0] * ux + p[1] * uy)
    mar = min(harb, key=lambda p: math.dist(p, tip))          # shodné s přistáním L3 (h_rail.build_l3)
    h = breakwater_harbor(world, para, mar, width=0.55, mouth=0.16, depth=0.26, name="Marina Paraland")
    pi = piers(world, para, mar, count=3, length=0.14, spacing=0.14, width=0.03, along=0.0)
    ports.append({"id": "H-02", "name": "Marina Paraland", "kind": "marina", "island": "para", "geom": h, "piers": pi,
                  "note": "rekreační marina a terminál L3 na západním pobřeží Paralandu", "exist": "proposed", "name_status": "proposed", "at": mar})
    return ports


def ferry_route(world, c02_geom, marina_geom):
    a = c02_geom["mole_a"][-1]
    b = marina_geom["mole_a"][-1]
    pts = [a, b]
    # vyhni se souši: přidej pomocný bod jižně od poloostrova, pokud přímka kříží souš
    def crosses(p, q):
        for k in range(41):
            x = (p[0] + (q[0] - p[0]) * k / 40, p[1] + (q[1] - p[1]) * k / 40)
            if world.land[world.g.cell_of(*x)]:
                return True
        return False
    if crosses(a, b):
        mid = ((a[0] + b[0]) / 2, max(a[1], b[1]) + 0.9)
        pts = [a, mid, b]
    return geom.catmull_rom_open(pts, 0.05)


# ---------------------------------------------------------------- letiště
def runway_rect(c, length_km, width_km, angle_deg):
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    hl, hw = length_km / 2, width_km / 2
    pts = [(c[0] - ux * hl - vx * hw, c[1] - uy * hl - vy * hw), (c[0] + ux * hl - vx * hw, c[1] + uy * hl - vy * hw),
           (c[0] + ux * hl + vx * hw, c[1] + uy * hl + vy * hw), (c[0] - ux * hl + vx * hw, c[1] - uy * hl + vy * hw)]
    return pts, (ux, uy), (vx, vy)


def build_airports(world):
    P = world.pos
    out = []
    c = P("A-01")
    rw, u, v = runway_rect(c, 1.9, 0.045, 0.0)
    apron_c = (c[0] + 0.05, c[1] + 0.27)
    apron, _, _ = runway_rect(apron_c, 0.55, 0.12, 0.0)
    taxi = [(c[0] + 0.10, c[1] + 0.02), (c[0] + 0.10, c[1] + 0.22)]
    term_c = (c[0] + 0.05, c[1] + 0.38)
    term, _, _ = runway_rect(term_c, 0.28, 0.07, 0.0)
    out.append({"id": "A-01", "name": "Regionální letiště Larpidie", "kind": "regional_airport", "island": "main", "runway": rw, "runway_name": "09/27",
                "length_m": 1900, "width_m": 45, "apron": apron, "taxiway": taxi, "terminal": term, "center": c,
                "note": "východní nížina; dráha 09/27, přibližně 1 900 m; malé až střední regionální letiště", "exist": "proposed", "name_status": "proposed"})
    # Paraland: travnatá dráha 700 m, sklon podle osy ostrova
    spot = hr.best_spot(world, *world.para(-1.15, 0.62), 0.35, 2.0, 0.04)
    rw2, _, _ = runway_rect(spot, 0.70, 0.03, 24.0)
    out.append({"id": "A-02", "name": "Přistávací plocha Paraland", "kind": "light_airstrip", "island": "para", "runway": rw2, "runway_name": "04/22 (travnatá)",
                "length_m": 700, "width_m": 30, "center": spot, "note": "jen lehká letadla, omezený provoz; žádné druhé velké letiště (kanon)",
                "exist": "proposed", "name_status": "proposed"})
    return out


# ---------------------------------------------------------------- body zájmu
def descend(world, start, max_len=1.6, stop_z=None, step=0.04):
    zs = raster.gauss(world.z, 4)
    g = world.g
    p = start
    pts = [p]
    L = 0.0
    for _ in range(int(max_len / step)):
        best, bz = None, 1e9
        for k in range(16):
            a = k * math.pi / 8
            q = (p[0] + step * math.cos(a), p[1] + step * math.sin(a))
            i, j = g.cell_of(*q)
            z = zs[i, j]
            if z < bz and not world.lake[i, j]:
                best, bz = q, z
        if best is None:
            break
        p = best
        pts.append(p)
        L += step
        if stop_z is not None and bz <= stop_z:
            break
    return pts


def build_poi(world, roads, trails, ccl, settle):
    P = world.pos
    main, para = world.o["main"], world.o["para"]
    spot = lambda x, y, r=0.4, s=6.0, rv=0.05: hr.best_spot(world, x, y, r, s, rv)
    pois = []

    def add(pid, name, kind, p, note="", island="main", exist="proposed", name_status="proposed"):
        pois.append({"id": pid, "name": name, "kind": kind, "x": p[0], "y": p[1], "z": world.zat(*p), "note": note, "island": island,
                     "exist": exist, "name_status": name_status})

    # vyhlídky s bezpečným přístupem (kanon: žádné pobídky ke skokům)
    safe = "bezpečná vyhlídka s oplocením a zábradlím; bez pobídky ke skokům do moře"
    add("V-02", "Útesová vyhlídka pod M-01", "viewpoint", spot(6.9, 4.55, 0.5, 20.0, 0.05), safe)
    add("V-03", "Vyhlídka severního mysu", "viewpoint", spot(16.5, 1.85, 0.4, 8.0), safe + "; maják LH-01")
    add("LH-01", "Maják severního mysu", "lighthouse", spot(16.6, 1.80, 0.4, 8.0), "navigační maják, rozhledna")
    add("V-04", "Vyhlídka na hrotu poloostrova", "viewpoint", spot(22.05, 14.45, 0.4, 6.0), safe + "; výhled na Paraland")
    add("V-05", "Vyhlídka na severovýchodním pobřeží", "viewpoint", spot(21.45, 4.5, 0.4, 8.0), safe)
    add("V-06", "Vyhlídka na jihozápadním útesu", "viewpoint", spot(4.7, 10.95, 0.5, 14.0, 0.05), safe)
    add("V-07", "Vyhlídka na hrázi přehrady", "viewpoint", spot(12.30, 10.32, 0.4, 10.0), "pohled na přehradní jezero N-04; ochrana zdroje vody")
    # horská turistika
    add("PG-01", "Paraglidingový start (zaoblený vrch M-03)", "paragliding_launch", spot(*P("M-03"), 0.3, 12.0), "start proti převládajícímu západnímu proudění; M-03 = zaoblený vrchol pro turistiku a paragliding (bible)")
    land = hr.best_spot(world, 4.55, 9.30, 0.9, 4.0, 0.06)
    add("PG-02", "Paraglidingové přistání (louka)", "paragliding_landing", land, "přistávací louka pod M-03")
    # prameny a studánky
    sp = [("SP-01", "Pramen hlavní řeky", (9.62, 5.78)), ("SP-02", "Studánka u severního potoka", (8.05, 5.05)), ("SP-03", "Pramen Havlišova potoka", (4.95, 8.30)),
          ("SP-04", "Studánka na stezce k M-03", (4.75, 8.75)), ("SP-05", "Studánka na hřebenovce", (6.3, 6.85)), ("SP-06", "Studánka u Horské stanice", (9.2, 6.3)),
          ("SP-07", "Studánka nad vodopádem", (10.2, 8.25))]
    for sid, nm, (x, y) in sp:
        add(sid, nm, "spring", spot(x, y, 0.45, 18.0, 0.03), "prameny a studánky přístupné pěšími trasami (bible approved)", exist="approved")
    pp = hr.best_spot(world, *world.para(-0.9, -1.15), 0.4, 14.0, 0.03)
    add("SP-08", "Studánka pod hradem (Paraland)", "spring", pp, "Paraland", island="para", exist="proposed")
    # prémiové hotely na hlavním ostrově (menší počet)
    add("HV-01", "Prémiový hotel – přístavní promenáda", "hotel_vip", spot(16.50, 13.55, 0.3, 4.0), "kanon: menší počet prémiových hotelů na hlavním ostrově; běžní turisté mají přístup na ostrov")
    add("HV-02", "Prémiový hotel – pláž Hoshimachi", "hotel_vip", spot(19.05, 3.65, 0.3, 4.0), "")
    add("HV-03", "Horská chata u lyžařské sjezdovky", "hotel_vip", spot(9.60, 6.60, 0.4, 6.0), "chalupy u sjezdovky")
    # Paraland
    add("PL-02", "Hrad/zámeček (pracovní)", "castle", spot(*world.para(-1.42, -1.25), 0.3, 12.0), "kanon: hrad/zámeček na Paralandu", island="para", exist="approved")
    add("PL-06", "Zřícenina (pracovní)", "ruin", spot(*world.para(0.55, -0.95), 0.4, 14.0), "kanon: zříceniny", island="para", exist="approved")
    add("PL-04", "Aquapark", "aquapark", spot(*world.para(0.05, 0.92), 0.5, 4.0), "kanon: aquapark jako samostatná atrakce, rezervace", island="para", exist="approved")
    add("V-08", "Vyhlídka na východním kopci Paralandu", "viewpoint", spot(*world.para(1.40, -0.12), 0.4, 20.0), "Paraland", island="para")
    # lyžařská hora M-02: sjezdovka po spádnici ze sedla pod vrcholem
    top = spot(*P("M-02"), 0.2, 25.0, 0.04)
    run = descend(world, (top[0] + 0.0, top[1] + 0.05), 1.7, stop_z=world.zat(*P("M-02")) - 300.0)
    base = run[-1]
    lift = [spot(base[0], base[1], 0.15, 20.0), top]
    ski = {"run": run, "lift": lift, "base": base, "top": top, "vertical_m": round(world.zat(*top) - world.zat(*base)),
           "length_m": round(sum(math.dist(a, b) for a, b in zip(run, run[1:])) * 1000)}
    return pois, ski
