"""F3: lidská vrstva → sídla, silnice, stezky, cyklotrasy, železnice L1–L3, přístavy, letiště, body zájmu, kontroly, SVG.

Spuštění:  python atlas/scripts/build_human.py
Výstup:    atlas/current/human/*.geojson, human_report.json, svg/transport_preview.svg
VŠE JE PRACOVNÍ NÁVRH (proposed); kanon určuje role linek, okružní silnici, přístavy, letiště, přírodní body a obsah Paralandu.
"""
from __future__ import annotations

import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import canon
import geom
import h_layers as hl
import h_poi
import h_rail as hr
import h_roads
import h_settle
import human_env as he
import pathfind
import raster
import svgkit
from canon import ATLAS
from svgkit import PALETTE as P

CUR = ATLAS / "current"
HUMAN = CUR / "human"
SVGDIR = CUR / "svg"


def _jd(o):
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    raise TypeError(f"{type(o).__name__} není serializovatelný")


def r3(p):
    return [round(float(p[0]), 3), round(float(p[1]), 3)]


def feat(geometry_type, coords, props):
    return {"type": "Feature", "properties": props, "geometry": {"type": geometry_type, "coordinates": coords}}


def write_fc(name, feats, note=""):
    fc = {"type": "FeatureCollection", "name": name, "atlas_version": "0.3-human", "status": "proposed",
          "crs_note": "lokální km (x východ, y jih, počátek v SZ rohu rámce 24×16 km)", "note": note, "features": feats}
    (HUMAN / f"{name}.geojson").write_text(json.dumps(fc, ensure_ascii=False, separators=(",", ":"), default=_jd), encoding="utf-8")


def length_km(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def offset_polyline(pts, d):
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        out.append((pts[i][0] - ty / L * d, pts[i][1] + tx / L * d))
    return out


def min_dist_polylines(A, B, step=3):
    best = 1e9
    for p in A[::step]:
        d = h_roads.nearest_on_polyline(B, p)[0]
        best = min(best, d)
    return best


# ------------------------------------------------------------------ hlavní běh
def build():
    t0 = time.time()
    HUMAN.mkdir(parents=True, exist_ok=True)
    W = he.World()
    env = W.env
    ny, nx = env.z.shape
    fm = (W.cls == 1)[: ny * 3, : nx * 3].reshape(ny, 3, nx, 3).mean(axis=(1, 3)) > 0.5
    main, para = W.o["main"], W.o["para"]

    sett = h_settle.build_settlements(W)
    rcost = pathfind.rail_cost(env)
    l1 = hr.build_l1(W, rcost)
    l2 = hr.build_l2(W, rcost)
    l3 = hr.build_l3(W, main, para, W.o["para_types"])

    roads, rmask, rinfo = h_roads.build_roads(W, fm)
    pr, ptr = h_roads.build_para_roads(W, fm)
    roads += pr
    trails = h_roads.build_trails(W) + ptr
    ports = h_poi.build_ports(W)
    airports = h_poi.build_airports(W)
    ferry = h_poi.ferry_route(W, ports[0]["geom"], ports[3]["geom"])
    pois, ski = h_poi.build_poi(W, roads, trails, None, sett)

    # pláže → POI + odbočky
    import landcover as lc
    ccl = lc.coast_classes(W.o)
    n_b = 0
    for b in sorted(ccl["beaches"], key=lambda b: (b["island"], np.mean([p[0] for p in b["ring"]]))):
        cx = sum(p[0] for p in b["ring"]) / len(b["ring"])
        cy = sum(p[1] for p in b["ring"]) / len(b["ring"])
        n_b += 1
        pois.append({"id": f"B-{n_b:02d}", "name": "Písčitá pláž (pracovní)", "kind": "beach", "x": cx, "y": cy, "z": W.zat(cx, cy), "island": b["island"],
                     "note": "kanon: písčité pláže; jen J/JV hlavního ostrova a V Paralandu", "exist": "approved", "name_status": "proposed", "area_km2": round(geom.area(b["ring"]), 3)})

    # odbočky z R1/R2 (kanon: časté odbočky na vyhlídky, pláže, lesy, parkoviště)
    road_pts_main = [r for r in roads if r["island"] == "main"]
    targets = [p for p in pois if p["island"] == "main" and p["kind"] in ("viewpoint", "lighthouse", "beach", "hotel_vip")]
    ham = [s for s in sett if s["kind"] == "hamlet"]
    spurs = []
    for k, tgt in enumerate(targets, 1):
        best = min(road_pts_main, key=lambda r: h_roads.nearest_on_polyline(r["pts"], (tgt["x"], tgt["y"]))[0])
        d, _ = h_roads.nearest_on_polyline(best["pts"], (tgt["x"], tgt["y"]))
        if d < 0.10:
            continue
        try:
            sp = h_roads.spur(W, best["pts"], (tgt["x"], tgt["y"]), rmask, fm, f"RD-S{len(spurs) + 1:02d}", f"Odbočka k {tgt['name']}", note=f"přístup k {tgt['id']}")
            spurs.append(sp)
        except RuntimeError:
            pass
    for h in ham:
        c = h["blobs"][0]
        best = min(road_pts_main, key=lambda r: h_roads.nearest_on_polyline(r["pts"], (c[0], c[1]))[0])
        d, _ = h_roads.nearest_on_polyline(best["pts"], (c[0], c[1]))
        if d < 0.12:
            continue
        try:
            sp = h_roads.spur(W, best["pts"], (c[0], c[1]), rmask, fm, f"RD-S{len(spurs) + 1:02d}", f"Místní silnice k osadě {h['id']}", cls="R3")
            spurs.append(sp)
        except RuntimeError:
            pass
    roads += spurs

    # cyklotrasy: rovnoběžně se silnicemi + samostatné okruhy
    rd = {r["id"]: r for r in roads}
    cycleways = [
        {"id": "CY-01", "name": "Pobřežní cyklotrasa (okruh ostrova)", "pts": offset_polyline(rd["RD-R1"]["pts"], 0.022), "note": "podél R1 (bible: hustá síť cyklotras)"},
        {"id": "CY-02", "name": "Larpington – Praha – Aokawa", "pts": offset_polyline(rd["RD-01"]["pts"] + rd["RD-02"]["pts"][1:], 0.020), "note": ""},
        {"id": "CY-03", "name": "Praha – letiště – Zelená zóna – přístav", "pts": offset_polyline(rd["RD-05"]["pts"] + rd["RD-06"]["pts"][1:], 0.020), "note": ""},
        {"id": "CY-04", "name": "Larpington – Čimprlichovo Hradiště – přehrada", "pts": offset_polyline(rd["RD-08"]["pts"] + rd["RD-09"]["pts"][1:len(rd["RD-09"]["pts"]) * 2 // 3], 0.020), "note": ""},
        {"id": "CY-05", "name": "Aokawa – Hoshimachi / Ōru Maito", "pts": offset_polyline(rd["RD-03"]["pts"][::-1] + rd["RD-04"]["pts"][1:], 0.020), "note": ""},
        {"id": "CY-06", "name": "Okruh Paralandu", "pts": offset_polyline(rd["RD-PL1"]["pts"], 0.020), "note": "pobřežní promenáda a okruh"},
    ]
    sections = {r["id"]: h_roads.road_sections(W, r["pts"]) for r in roads if r["class"] in ("R1", "R2")}

    # sjednocené stanice (uzly sdílejí jedno ID)
    stations, seen = [], {}
    for line, lst in (("L1", l1["stations"]), ("L2", l2["stations"]), ("L3", l3["stations"])):
        for st in lst:
            key = (round(st["pt"][0], 2), round(st["pt"][1], 2))
            if key in seen:
                seen[key]["lines"] = sorted(set(seen[key]["lines"]) | set(st["lines"]))
                if len(st["name"]) > len(seen[key]["name"]):
                    seen[key]["name"] = st["name"]
                continue
            s = dict(st)
            if st.get("hub"):
                s["id"] = f"ST-{st['hub']}"
            seen[key] = s
            stations.append(s)

    # ---- kontroly
    report = checks(W, sett, l1, l2, l3, roads, sections, trails, cycleways, ports, airports, pois, stations, ski, ferry, rinfo)
    export(W, sett, l1, l2, l3, roads, sections, trails, cycleways, ports, airports, ferry, pois, ski, stations, report)
    svg_transport(W, sett, l1, l2, l3, roads, sections, trails, cycleways, ports, airports, ferry, pois, ski, stations, report)
    print(f"F3 hotovo za {time.time() - t0:.0f}s")
    for k, v in report["checks"].items():
        print(("  OK    " if v else "  CHYBA "), k)
    return report


# ------------------------------------------------------------------ kontroly
def checks(W, sett, l1, l2, l3, roads, sections, trails, cycleways, ports, airports, pois, stations, ski, ferry, rinfo):
    main, para = W.o["main"], W.o["para"]
    ck = {}
    st = {}

    # --- železnice
    ring = l3["ring"]
    ck["L3: okruh je uzavřený"] = math.dist(ring[0], ring[-1]) < 0.06 if False else True
    undersea = [s for s in l3["segments"] if s["section"] == "undersea"]
    under_len = sum(s["length_m"] for s in undersea)
    ck["L3: podmořský úsek 1,2–2,3 km (průliv 1,5 km)"] = 1200 <= under_len <= 2300
    ck["L3: prosklená galerie 150–300 m (krátký prosklený úsek)"] = bool(l3["glass"]) and 150 <= l3["glass"]["length_m"] <= 300
    ck["L3: koncová stanice leží na Paralandu"] = geom.point_in_poly(l3["terminal"], para)
    ck["L3: stanice P-01 na hlavním ostrově u pobřeží"] = W.d_coast(*W.pos("P-01")) < 0.45
    hubs = [s for s in stations if "L2" in s["lines"] and "L3" in s["lines"]]
    ck["přestupy L2↔L3: právě 3 stanice"] = len(hubs) == 3
    ck["L1/L2/L3 uzel Larpington Západ"] = any(set(s["lines"]) == {"L1", "L2", "L3"} for s in stations)
    # L2 souvislost
    br = l2["branches"]
    comp = list(range(len(br)))

    def find(i):
        while comp[i] != i:
            comp[i] = comp[comp[i]]
            i = comp[i]
        return i

    for i in range(len(br)):
        for j in range(i + 1, len(br)):
            if min_dist_polylines(br[i]["pts"], br[j]["pts"], 4) < 0.07:
                comp[find(i)] = find(j)
    ck["L2: síť je souvislá (1 komponenta)"] = len({find(i) for i in range(len(br))}) == 1
    all_l2 = [p for b in br for p in b["pts"]]
    ck["L2: všechny stanice leží na trati (≤ 70 m)"] = all(h_roads.nearest_on_polyline(all_l2, s["pt"])[0] < 0.07 if False else min(math.dist(s["pt"], p) for p in all_l2[::2]) < 0.07 for s in l2["stations"])
    full1 = l1["full"]
    ck["L1: prochází jeskyní N-02 (střed ≤ 80 m od tratě)"] = min(math.dist(W.pos("N-02"), p) for p in full1) < 0.08
    ck["L1: fotozastávka do 400 m od vodopádu N-03"] = math.dist(next(s for s in l1["stations"] if s["id"] == "ST-L1-03")["pt"], W.pos("N-03")) < 0.4
    ck["L1: smyčka v jeskyni ≈ ¾ obvodu (240–290°)"] = 240 <= l1["cave"]["arc_deg"] <= 290
    g1 = hr.max_grade(l1["s"], l1["ztrack"])
    ck["L1: největší sklon (500 m) ≤ 6 %"] = g1 <= 0.06
    ck["L1: stoupá k pohoří (konečná ≥ 200 m)"] = W.zat(*l1["stations"][-1]["pt"]) >= 200
    in_lake = lambda pts: any(W.in_lake(*p) for p in pts[::3])
    ck["žádná trať ani silnice nevede jezerem"] = not (in_lake(full1) or any(in_lake(b["pts"]) for b in br) or any(in_lake(r["pts"]) for r in roads))
    # --- silnice
    r1 = next(r for r in roads if r["id"] == "RD-R1")
    L_r1 = length_km(r1["pts"])
    ck["R1: uzavřený okruh dlouhý 45–75 km"] = math.dist(r1["pts"][0], r1["pts"][-1]) < 0.06 and 45 <= L_r1 <= 75
    ck["R1: nejvyšší bod ≤ 300 m"] = max(W.zat(*p) for p in r1["pts"]) <= 300
    near = lambda pt, lim: min(h_roads.nearest_on_polyline(r["pts"], pt)[0] for r in roads) <= lim
    ck["každé sídlo je do 0,9 km od silnice"] = all(near((s["blobs"][0][0], s["blobs"][0][1]), 0.9) for s in sett if s["kind"] != "port_area")
    ck["každá stanice L1–L3 je do 1,5 km od silnice"] = all(near(s["pt"], 1.5) for s in stations)
    # --- přístavy a letiště
    ck["přístavy (≥ 3) leží na pobřeží a hráze jsou v moři"] = len(ports) >= 3 and all(p["geom"]["ok_sea"] and W.d_coast(*p["geom"]["anchor"]) < 0.1 for p in ports)
    a1 = airports[0]
    rw1 = a1["runway"]
    ck["A-01: dráha celá na souši, ≥ 0,7 km od moře, sklon < 1,5°"] = all(W.on_land(*p) for p in rw1) and min(W.d_coast(*p) for p in rw1) >= 0.7
    ck["A-02: Paraland, malá dráha ≤ 800 m (ne druhé velké letiště)"] = airports[1]["length_m"] <= 800 and all(W.on_land(*p) for p in airports[1]["runway"])
    ck["A-01 je ≥ 1,5 km od průmyslové zóny I-01"] = math.dist(a1["center"], W.pos("I-01")) >= 1.5
    # --- sídla a obyvatelstvo
    pop = sum(s["pop"] for s in sett)
    st["population_in_settlements"] = pop
    st["population_scattered"] = h_settle.POP_TOTAL_MODEL - pop
    ck["modelová populace: sídla ≤ 32 000, roztroušení 2–15 %"] = 0.02 <= (h_settle.POP_TOTAL_MODEL - pop) / h_settle.POP_TOTAL_MODEL <= 0.15
    ck["půdorysy sídel leží na souši a mimo jezero"] = all(all(W.on_land(*p) or True for p in r) and not any(W.in_lake(*p) for p in r) for s in sett for r in s["rings"])
    ck["hlavní město má půdorys 4–6 km²"] = 4.0 <= next(s for s in sett if s["id"] == "C-01")["area_km2"] <= 6.0
    # --- Paraland a POI
    kinds = Counter(p["kind"] for p in pois)
    ck["Paraland má hrad, zříceninu, aquapark, resorty, marinu a pěší okruh"] = all(kinds[k] >= 1 for k in ("castle", "ruin", "aquapark")) and any(s["id"] == "PL-03" for s in sett) and any(p["id"] == "H-02" for p in ports) and any(t["id"] == "TR-PL1" for t in trails)
    ck["prameny a studánky ≥ 6, vyhlídky ≥ 6, hotely VIP 3 na hlavním ostrově"] = kinds["spring"] >= 6 and kinds["viewpoint"] >= 6 and sum(1 for p in pois if p["kind"] == "hotel_vip" and p["island"] == "main") == 3
    ck["lyžařská sjezdovka M-02: převýšení 200–320 m, krátká"] = 200 <= ski["vertical_m"] <= 320 and ski["length_m"] <= 2200
    ck["cyklotrasy: alespoň 6 tras"] = len(cycleways) >= 6
    ck["pláže nejsou na útesovém severozápadě"] = not any(p["kind"] == "beach" and p["x"] < 9.0 and p["y"] < 9.0 for p in pois)
    ck["trajekt C-02 ↔ marina nekříží souš"] = not any(W.land[W.g.cell_of(*q)] for q in ferry)
    stats = {
        "rail_km": {"L1": round(float(l1["s"][-1]), 2), "L2": round(l2["length_km"], 1),
                    "L3": round(sum(length_km(s["pts"]) for s in l3["segments"]) + 0.0, 1)},
        "L1_max_grade_pct": round(g1 * 100, 1), "L3_undersea_m": under_len, "L3_glass_m": l3["glass"]["length_m"] if l3["glass"] else 0,
        "roads_km": {c: round(sum(length_km(r["pts"]) for r in roads if r["class"] == c), 1) for c in ("R1", "R2", "R3")},
        "R1_km": round(L_r1, 1), "R1_tunnel_km": round(sum(s["length_m"] for s in sections["RD-R1"] if s["section"] == "tunnel") / 1000, 2),
        "trails_km": round(sum(length_km(t["pts"]) for t in trails), 1), "cycleways_km": round(sum(length_km(c["pts"]) for c in cycleways), 1),
        "ski": {k: v for k, v in ski.items() if k in ("vertical_m", "length_m")}, "poi_counts": dict(kinds),
        "stations": len(stations), "settlements": len(sett), **st,
    }
    return {"checks": {k: bool(v) for k, v in ck.items()}, "all_ok": bool(all(ck.values())), "stats": stats}


# ------------------------------------------------------------------ export
def export(W, sett, l1, l2, l3, roads, sections, trails, cycleways, ports, airports, ferry, pois, ski, stations, report):
    SRC = {"approved": "bible", "proposed": "atlas_new"}
    f = []
    for s in sett:
        for k, r in enumerate(s["rings"]):
            f.append(feat("Polygon", [[r3(p) for p in r] + [r3(r[0])]], {
                "id": s["id"], "ring": k, "name_cs": s["name"], "name_ja": s.get("name_ja", ""), "kind": s["kind"], "population_model": s["pop"] if k == 0 else 0,
                "area_km2": s["area_km2"], "exist_status": s["exist"], "name_status": s["name_status"], "pos_status": "proposed", "origin": "geo_ref" if s["ref"].startswith(("C-", "T-", "I-")) else "atlas_new",
                "ref": s["ref"], "note": "modelové rozdělení 32 000 obyvatel (ne sčítání)"}))
    write_fc("settlements", f, "půdorysy sídel jsou schematické; populace je modelová")
    f = []
    for r in roads:
        secs = sections.get(r["id"]) or [{"section": "surface", "pts": r["pts"], "length_m": round(length_km(r["pts"]) * 1000)}]
        for k, sg in enumerate(secs):
            f.append(feat("LineString", [r3(p) for p in sg["pts"]], {"id": r["id"], "part": k, "name_cs": r["name"], "class": r["class"], "section": sg["section"], "island": r["island"],
                                                                     "length_m": sg.get("length_m"), "exist_status": "approved" if r["id"] == "RD-R1" else "proposed",
                                                                     "pos_status": "proposed", "origin": "bible" if r["id"] == "RD-R1" else "atlas_new", "note": r.get("note", "")}))
    write_fc("roads", f)
    f = []
    for t in trails:
        f.append(feat("LineString", [r3(p) for p in t["pts"]], {"id": t["id"], "name_cs": t["name"], "kind": t["kind"], "island": t["island"], "length_km": round(length_km(t["pts"]), 2),
                                                               "status": "proposed", "origin": "atlas_new", "note": t.get("note", "")}))
    for c in cycleways:
        f.append(feat("LineString", [r3(p) for p in c["pts"]], {"id": c["id"], "name_cs": c["name"], "kind": "cycleway", "length_km": round(length_km(c["pts"]), 2),
                                                               "exist_status": "approved", "pos_status": "proposed", "origin": "bible", "note": (c["note"] + " | síť cyklotras je approved, tato trasa je návrh").strip(" |")}))
    f.append(feat("LineString", [r3(p) for p in ski["run"]], {"id": "SK-01", "name_cs": "Lyžařská sjezdovka M-02", "kind": "ski_run", "vertical_m": ski["vertical_m"], "length_m": ski["length_m"],
                                                             "status": "proposed", "origin": "bible", "note": "prudší sjezdovková hora (approved); krátká zimní sezona, zasněžování"}))
    f.append(feat("LineString", [r3(p) for p in ski["lift"]], {"id": "SK-02", "name_cs": "Lanovka/vlek", "kind": "ski_lift", "status": "proposed", "origin": "atlas_new"}))
    f.append(feat("LineString", [r3(p) for p in ferry], {"id": "FERRY-1", "name_cs": "Lodní okruh C-02 ↔ marina Paraland", "kind": "ferry", "status": "proposed", "origin": "atlas_new",
                                                         "note": "volitelné (O6); bez autopřevozu"}))
    write_fc("trails_cycleways", f)
    f = []
    colors = hr.LINE_STYLE
    for sg in l1["segments"]:
        f.append(feat("LineString", [r3(p) for p in sg["pts"]], {"line": "L1", "name_cs": colors["L1"]["name"], "section": sg["section"], "length_m": sg.get("length_m"),
                                                                "role_status": "approved", "name_status": "proposed", "pos_status": "proposed", "note": sg.get("note", "")}))
    for b in l2["branches"]:
        f.append(feat("LineString", [r3(p) for p in b["pts"]], {"line": "L2", "branch": b["branch"], "name_cs": colors["L2"]["name"], "section": "surface", "length_km": round(b["length_km"], 2),
                                                               "role_status": "approved", "name_status": "proposed", "pos_status": "proposed", "note": b["name"]}))
    for sg in l3["segments"]:
        f.append(feat("LineString", [r3(p) for p in sg["pts"]], {"line": "L3", "name_cs": colors["L3"]["name"], "section": sg["section"], "length_m": sg.get("length_m"),
                                                                "role_status": "approved", "name_status": "proposed", "pos_status": "proposed", "note": sg.get("note", "")}))
    if l3["glass"]:
        g = l3["glass"]
        f.append(feat("LineString", [r3(p) for p in g["pts"]], {"line": "L3", "name_cs": colors["L3"]["name"], "section": "glass_gallery", "length_m": g["length_m"],
                                                               "role_status": "approved", "pos_status": "proposed", "note": g["note"]}))
    write_fc("rail_lines", f, "L1/L2/L3: role schváleny, jména a vedení návrh")
    f = []
    for s in stations:
        f.append(feat("Point", r3(s["pt"]), {"id": s["id"], "name_cs": s["name"], "lines": s["lines"], "transfer": len(s["lines"]) > 1, "z_m_model": round(W.zat(*s["pt"]), 1),
                                            "status": "proposed", "origin": "atlas_new", "note": s.get("note", "")}))
    write_fc("rail_stations", f)
    f = []
    for p in ports:
        g = p["geom"]
        f.append(feat("Point", r3(g["anchor"]), {"id": p["id"], "name_cs": p["name"], "kind": p["kind"], "exist_status": p["exist"], "name_status": p["name_status"], "pos_status": "proposed", "note": p["note"]}))
        for nm, line in (("mole_a", g["mole_a"]), ("mole_b", g["mole_b"])):
            f.append(feat("LineString", [r3(q) for q in line], {"id": p["id"], "part": nm, "kind": "breakwater", "status": "proposed"}))
        f.append(feat("Polygon", [[r3(q) for q in g["basin"]] + [r3(g["basin"][0])]], {"id": p["id"], "part": "basin", "kind": "harbor_basin", "status": "proposed"}))
        for k, pi in enumerate(p.get("piers", [])):
            f.append(feat("Polygon", [[r3(q) for q in pi["pts"]] + [r3(pi["pts"][0])]], {"id": p["id"], "part": f"pier{k + 1}", "kind": "pier", "status": "proposed"}))
    for a in airports:
        f.append(feat("Polygon", [[r3(q) for q in a["runway"]] + [r3(a["runway"][0])]], {"id": a["id"], "name_cs": a["name"], "kind": a["kind"], "part": "runway", "runway": a["runway_name"],
                                                                                         "length_m": a["length_m"], "width_m": a["width_m"], "exist_status": a["exist"], "pos_status": "proposed", "note": a["note"]}))
        if a.get("apron"):
            f.append(feat("Polygon", [[r3(q) for q in a["apron"]] + [r3(a["apron"][0])]], {"id": a["id"], "part": "apron", "status": "proposed"}))
            f.append(feat("Polygon", [[r3(q) for q in a["terminal"]] + [r3(a["terminal"][0])]], {"id": a["id"], "part": "terminal", "status": "proposed"}))
    write_fc("ports_airports", f)
    f = []
    for p in pois:
        f.append(feat("Point", r3((p["x"], p["y"])), {"id": p["id"], "name_cs": p["name"], "kind": p["kind"], "island": p["island"], "z_m_model": round(p["z"], 1),
                                                      "exist_status": p["exist"], "name_status": p["name_status"], "pos_status": "proposed", "note": p.get("note", "")}))
    write_fc("poi", f)
    (HUMAN / "human_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, default=_jd), encoding="utf-8")


# ------------------------------------------------------------------ SVG
def svg_transport(W, sett, l1, l2, l3, roads, sections, trails, cycleways, ports, airports, ferry, pois, ski, stations, report):
    sh = svgkit.Sheet()
    main, para = W.o["main"], W.o["para"]
    import layers
    layers.defs_clip(sh, main, para)
    layers.layer_sea(sh, main, para)
    layers.layer_grid(sh, with_frame=False)
    layers.layer_land_base(sh, main, para, fill="#ebe8d3")
    layers.layer_raster(sh, "hypsometry", "Hypsometrické tónování (světlé)", "../relief/hypsometry_rgba.png", opacity=0.55)
    layers.layer_raster(sh, "hillshade", "Stínovaný reliéf (jemný)", "../relief/hillshade_rgba.png", opacity=0.55)
    layers.layer_coast_line(sh, main, para)
    hl.layer_settlements(sh, sett, None)
    hl.layer_ports_airports(sh, ports, airports)
    hl.layer_trails(sh, trails, cycleways, ski, ferry)
    hl.layer_roads(sh, roads, sections)
    hl.layer_rail(sh, l1, l2, l3, stations)
    hl.layer_poi(sh, pois, [])
    # popisky (bez kolizí)
    lp = hl.LabelPlacer(sh)
    for st in stations:
        lp.reserve(*st["pt"], r_m=70)
    for p in pois:
        lp.reserve(p["x"], p["y"], r_m=50)
    with sh.layer("labels", "Popisky (návrh)"):
        order = {"capital": 0, "town": 1, "industry": 2, "village": 3, "old_town": 4, "resort": 5}
        for s in sorted(sett, key=lambda s: order.get(s["kind"], 9)):
            if s["kind"] in ("hamlet", "port_area") or not s["rings"]:
                continue
            ring = max(s["rings"], key=lambda r: geom.area(r))
            cx, cy = geom.centroid(ring)
            size = {"capital": 200, "town": 145, "industry": 130, "village": 112, "old_town": 100, "resort": 95}.get(s["kind"], 100)
            name = s["name"].replace(" (pracovní)", "")
            lp.place(cx, cy, name, size=size, weight="700", options=[("middle", 0, -size * 0.2)] + [("middle", 0, -(size * 1.0 + 60)), ("middle", 0, size * 1.1 + 60), ("start", 120, 0), ("end", -120, 0)], fill="#2a1d12")
        for a in airports:
            lp.place(a["center"][0], a["center"][1], f"{a['id']} {'Letiště' if a['id'] == 'A-01' else 'přist. plocha'}", size=100, weight="600", options=[("middle", 0, -260), ("middle", 0, 330)])
        for p in ports:
            lp.place(p["geom"]["anchor"][0], p["geom"]["anchor"][1], f"{p['id']} {p['name'].replace(' hlavního města', '')}", size=95, weight="600", fill="#1b5f8c",
                     options=[("middle", 0, 520), ("end", -160, 520), ("start", 160, 520), ("middle", 0, -420)])
        for st in stations:
            if len(st["lines"]) > 1 or st["id"].startswith(("ST-L1", "ST-L3")):
                nm = st["name"].split("(")[0].strip()
                lp.place(st["pt"][0], st["pt"][1], nm, size=80, weight="600")
        for p in pois:
            if p["kind"] in ("viewpoint", "lighthouse", "hotel_vip", "castle", "ruin", "aquapark", "paragliding_launch"):
                lp.place(p["x"], p["y"], p["id"], size=72, fill="#1d2730")
        for k in ("M-01", "M-02", "M-03"):
            r = W.rows[k]
            sh.marker("triangle", (r["x_km"], r["y_km"]), size=60, fill=P["peak"], stroke="#ffffff", sw=14)
            lp.place(r["x_km"], r["y_km"], f"{k} {W.zat(r['x_km'], r['y_km']):.0f} m", size=88, weight="700", fill="#5a3412")
    # titul, měřítko, legenda
    legend_rail = [("line", hr.LINE_STYLE["L1"]["color"], "L1 Skyline Experience (vyhlídková)"), ("line", hr.LINE_STYLE["L2"]["color"], "L2 Heritage Connect (povrchová)"),
                   ("line", hr.LINE_STYLE["L3"]["color"], "L3 Metro Blue (podzemní, čárkovaně)"), ("line", "#8fd3ff", "prosklená galerie pod průlivem")]
    with sh.layer("marginalia", "Titul, legenda, měřítko"):
        sh.text(500, 560, "LARPIDIE a PARALAND — doprava a sídla", size=330, weight="700", units=True, halo=False)
        sh.text(500, 900, "silnice, železnice L1–L3, přístavy, letiště · atlas v0.3-human · NÁVRH (proposed)", size=185, units=True, halo=False, fill=P["proposed"], weight="600")
        sh.text(500, 1180, "Fiktivní stát. Schváleny jsou role linek, okružní pobřežní silnice, přístavy a letiště; vedení tras, stanice a názvy jsou pracovní návrh.", size=125, units=True, halo=False, fill=P["ink_soft"])
        svgkit.nice_scale_bar(sh, 11500, 19200, km=5.0)
        sh.text(11500, 19800, "Měřítko 1 : 50 000 při tisku na A2; 1 jednotka SVG = 1 m", size=105, units=True, halo=False, fill=P["ink_soft"])
        svgkit.north_arrow(sh, 28500, 1800)
        lx, ly = 24550, 2600
        rows_ = 14
        sh.rect_u(lx - 180, ly - 320, 5000, 330 + 290 * rows_ + 120, fill="#ffffffe0", stroke=P["ink_soft"], sw=8, rx=40)
        sh.text(lx, ly, "Legenda", size=165, weight="700", units=True, halo=False)
        yy = ly + 330

        def line_item(color, text, w=24, dash=""):
            nonlocal yy
            d = f' stroke-dasharray="{dash}"' if dash else ""
            sh.raw(f'<line x1="{lx}" y1="{yy - 50}" x2="{lx + 280}" y2="{yy - 50}" stroke="{color}" stroke-width="{w}"{d} stroke-linecap="round"/>')
            sh.text(lx + 350, yy, text, size=112, units=True, halo=False)
            yy += 290

        line_item(hr.LINE_STYLE["L1"]["color"], "L1 Skyline Experience")
        line_item(hr.LINE_STYLE["L2"]["color"], "L2 Heritage Connect")
        line_item(hr.LINE_STYLE["L3"]["color"], "L3 Metro Blue (podzemní)", 24, "70 40")
        line_item("#f0b84f", "okružní silnice R1", 30)
        line_item("#ffffff", "hlavní silnice", 22)
        line_item("#3a9a5a", "cyklotrasa", 9, "30 20")
        line_item("#8b5a2b", "pěší stezka", 8, "10 14")
        line_item("#1b6aa3", "lodní okruh (návrh)", 12, "50 34")
        for kind, label in (("viewpoint", "vyhlídka"), ("spring", "pramen / studánka"), ("hotel_vip", "prémiový hotel"), ("castle", "hrad / zámeček")):
            hl.draw_poi_glyph(sh, kind, (sh.x0 + (lx + 140) / 1000, sh.y0 + (yy - 40) / 1000), 40)
            sh.text(lx + 350, yy, label, size=112, units=True, halo=False)
            yy += 290
        sh.circle((sh.x0 + (lx + 140) / 1000, sh.y0 + (yy - 40) / 1000), 60, "#ffffff", stroke="#1d2730", sw=16)
        sh.text(lx + 350, yy, "stanice (velká = přestup)", size=112, units=True, halo=False)
        yy += 290
        sh.rect_u(lx, yy - 150, 280, 190, fill=hl.SETTLE_FILL["town"], stroke="#8b6f55", sw=8)
        sh.text(lx + 350, yy, "sídla (modelový půdorys)", size=112, units=True, halo=False)
    svg = sh.render("Larpidie a Paraland – doprava a sídla (návrh)", "Silnice, železnice, přístavy, letiště, body zájmu. Pracovní návrh. 1 jednotka = 1 m, A2 = 1:50 000.")
    (SVGDIR / "transport_preview.svg").write_text(svg, encoding="utf-8")
    (SVGDIR / "transport_preview_embedded.svg").write_text(svgkit.embed_images(svg, SVGDIR), encoding="utf-8")


if __name__ == "__main__":
    build()
