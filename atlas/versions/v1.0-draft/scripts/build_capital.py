"""F7: podklad plánu hlavního města Larpingtonu (CP-01) – ulice, graf, bloky, prostory, klíčové budovy, registr, SVG a prohlížeč.

Spuštění:  python atlas/scripts/build_capital.py
Výstup:    atlas/current/capital/  (cp_frame.json, cp_graph.json, cp_*.geojson [lokální metry] a *_atlas_km.geojson, cp_objects.json/csv,
           cp_photo_guide.csv, cp_report.json, capital_plan_base.svg, capital_plan_viewer.html)
Vše je pracovní návrh (proposed); geometrie atlasu (pobřeží, silnice, koleje, stanice, přístav C-02) se nemění.
"""
from __future__ import annotations

import csv
import heapq
import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import canon
import cp_blocks as BL
import cp_context as CX
import cp_data as C
import cp_geom as G
import cp_layout as LY
import cp_poi as PO
import cp_streets as ST
import cp_svg as SV
import cp_viewer as VW
from canon import ATLAS

OUT = ATLAS / "current" / "capital"


def build_graph(ctx, L):
    g = ST.generate(ctx, L)
    g.snap_ends(16.0)
    g.build()
    g.dedupe()
    g.prune(min_comp_len=600.0)
    did_name = {v: k for k, v in CX.DID_INDEX.items()}
    for i, e in enumerate(g.edges, 1):
        e["id"] = f"E{i:04d}"
        mid = G.point_at(e["pts"], e["length"] / 2)[0]
        ij = (min(C.NY - 1, max(0, int(mid[1] / C.CELL))), min(C.NX - 1, max(0, int(mid[0] / C.CELL))))
        e["district"] = e.get("district") or did_name.get(int(ctx.did[ij]))
        e["row_m"] = e.get("row") or ST.ROW[e["cls"]]
    return g


def add_street_objects(ctx, graph, objs, names):
    """Pojmenované ulice jako objekty plánu (CP-UL##)."""
    order = sorted(names)
    for n, nm in enumerate(order, 1):
        es = names[nm]
        longest = max(es, key=lambda e: e["length"])
        mid = G.point_at(longest["pts"], longest["length"] / 2)[0]
        aid = next((e["atlas_id"] for e in es if e.get("atlas_id")), None)
        coast = nm == "Pobřežní třída"
        u, v = mid
        x, y = C.to_km((u, v))
        objs.append({
            "id": f"CP-UL{n:02d}", "type": "street", "subtype": longest["cls"], "name_cs": nm, "name_en": es[0].get("name_en", nm), "region": "south_southeast",
            "district": None, "u": round(u, 1), "v": round(v, 1), "x_km": round(x, 4), "y_km": round(y, 4), "length_m": round(sum(e["length"] for e in es)),
            "exist_status": "approved" if coast else "proposed", "name_status": "proposed", "pos_status": "proposed", "origin": "bible" if coast else ("atlas" if aid else "plan_new"),
            "atlas_ref": aid, "bible_ref": "mobility.coastal_ring_road (approved)" if coast else "", "notes": "pojmenovaný celek ulic (název je návrh)", "edges": len(es)})


def node_xy(graph, i):
    return graph.nodes[i]


def routes_over_graph(ctx, graph, L, objs):
    city = ctx.city
    adj = defaultdict(list)
    z = city.z_at
    for k, e in enumerate(graph.edges):
        a, b = e["a"], e["b"]
        pa, pb = graph.nodes[a], graph.nodes[b]
        grade = abs(z(*pb) - z(*pa)) / max(e["length"], 1.0)
        cost = e["length"] * (1.0 + 14.0 * max(0.0, grade - 0.05))
        if e["cls"] in ("L",):
            cost *= 1.6                                  # úzké uličky jen jako nouze
        adj[a].append((b, cost, k))
        adj[b].append((a, cost, k))

    used = [i for i in adj if adj[i]]

    def nearest_node(p):
        return min(used, key=lambda i: math.dist(graph.nodes[i], p))

    def dijkstra(s, t):
        dist = {s: 0.0}
        prev = {}
        pq = [(0.0, s)]
        while pq:
            d, x = heapq.heappop(pq)
            if x == t:
                break
            if d > dist.get(x, 1e18):
                continue
            for y, c, k in adj[x]:
                nd = d + c
                if nd < dist.get(y, 1e18):
                    dist[y] = nd
                    prev[y] = (x, k)
                    heapq.heappush(pq, (nd, y))
        path, x = [], t
        while x != s:
            px, k = prev[x]
            path.append((px, x, k))
            x = px
        return path[::-1]

    def polyline(path):
        pts = []
        for a, b, k in path:
            e = graph.edges[k]
            seg = e["pts"] if e["a"] == a else e["pts"][::-1]
            pts.extend(seg if not pts else seg[1:])
        return pts

    def stats(pts):
        rs = G.resample(pts, 10.0)
        zz = [z(*p) for p in rs]
        gr = [abs(zz[i + 3] - zz[i]) / 30.0 for i in range(len(zz) - 3)]
        return {"length_m": round(G.length(pts)), "max_grade_pct": round(100 * max(gr), 1) if gr else 0.0,
                "share_over_5pct": round(sum(1 for x in gr if x > 0.05) / max(1, len(gr)), 3), "dz_m": round(zz[-1] - zz[0], 1)}

    st_s = city.station("ST-S")
    q = ctx.rd12_quay_pt
    harbor = (L["harbor_sq"]["c"][0], L["harbor_sq"]["c"][1])
    spec = [
        ("CP-AR01", "Bezbariérová trasa ST-S → Přístavní náměstí", (st_s["u"], st_s["v"]), harbor),
        ("CP-AR02", "Bezbariérová trasa Přístavní náměstí → hotel na promenádě", harbor, L["hotel"]["c"]),
        ("CP-AR03", "Bezbariérová trasa ST-S → Náměstí čtyř → muzeum", (st_s["u"], st_s["v"]), L["museum"]["c"]),
    ]
    out = []
    for rid, nm, a, b in spec:
        path = dijkstra(nearest_node(a), nearest_node(b))
        pts = [a] + polyline(path) + [b]
        s = stats(pts)
        out.append({"id": rid, "name_cs": nm, "pts": pts, **s})
        c = pts[len(pts) // 2]
        x, y = C.to_km(c)
        objs.append({"id": rid, "type": "route", "subtype": "accessible_route", "name_cs": nm, "name_en": nm, "region": "south_southeast", "u": round(c[0], 1), "v": round(c[1], 1),
                     "x_km": round(x, 4), "y_km": round(y, 4), "length_m": s["length_m"], "exist_status": "proposed", "name_status": "proposed", "pos_status": "proposed", "origin": "plan_new",
                     "bible_ref": "GEOGRAPHY: univerzálně přístupná prostranství",
                     "notes": f"kandidát na bezbariérovou trasu: největší sklon {s['max_grade_pct']} % (na 30 m), podíl úseků nad 5 % = {s['share_over_5pct']}; převýšení {s['dz_m']} m"})
    return out


# ------------------------------------------------------------------ zápisy
def geom_poly(poly, km=False):
    pts = [C.to_km(p) if km else p for p in poly]
    pts = [[round(p[0], 4 if km else 2), round(p[1], 4 if km else 2)] for p in pts]
    return {"type": "Polygon", "coordinates": [pts + [pts[0]]]}


def geom_line(pts, km=False):
    return {"type": "LineString", "coordinates": [[round(q[0], 4 if km else 2), round(q[1], 4 if km else 2)] for q in ([C.to_km(p) for p in pts] if km else pts)]}


def write_geojson(path, feats, note):
    fc = {"type": "FeatureCollection", "name": path.stem, "properties": {"note": note, "plan_id": C.PLAN_ID, "status": "proposed", "atlas_version": canon.ATLAS_VERSION}, "features": feats}
    path.write_text(json.dumps(fc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def feature_sets(ctx, graph, blocks, objs, routes):
    """Vrstvy GeoJSON jako dvojice (lokální metry, km atlasu): districts, blocks, streets, buildings, spaces, points, routes."""
    out = {}
    byid = {o["id"]: o for o in objs}

    def build(kind):
        loc, km = [], []
        for item in kind:
            props, geom, g_ = item
            loc.append({"type": "Feature", "properties": props, "geometry": g_(geom, False)})
            km.append({"type": "Feature", "properties": props, "geometry": g_(geom, True)})
        return loc, km

    base = lambda o: {k: o.get(k) for k in ("id", "type", "subtype", "name_cs", "name_en", "district", "exist_status", "name_status", "pos_status", "origin", "atlas_ref", "area_m2", "length_m", "land_use")}
    out["districts"] = build([(base(o), o["poly"], geom_poly) for o in objs if o["type"] == "district"])
    out["blocks"] = build([(base(o), o["poly"], geom_poly) for o in objs if o["type"] == "block"])
    out["buildings"] = build([(base(o), o["poly"], geom_poly) for o in objs if o["type"] in ("building", "pier") and o.get("poly")])
    out["spaces"] = build([(base(o), o["poly"], geom_poly) for o in objs if o["type"] in ("square", "park", "promenade", "harbor") and o.get("poly")])
    sf = []
    for e in graph.edges:
        p = {"id": e["id"], "cls": e["cls"], "row_m": e["row_m"], "length_m": round(e["length"], 1), "name_cs": e.get("name_cs"), "name_en": e.get("name_en"), "atlas_id": e.get("atlas_id"),
             "section": e.get("section"), "district": e.get("district"), "node_a": e["a"], "node_b": e["b"]}
        sf.append((p, e["pts"], geom_line))
    out["streets"] = build(sf)
    pts_l, pts_k = [], []
    for o in objs:
        if o["type"] in ("cafe", "rental", "shop", "station", "retail_zone"):
            pr = base(o)
            pts_l.append({"type": "Feature", "properties": pr, "geometry": {"type": "Point", "coordinates": [o["u"], o["v"]]}})
            pts_k.append({"type": "Feature", "properties": pr, "geometry": {"type": "Point", "coordinates": [o["x_km"], o["y_km"]]}})
    out["points"] = (pts_l, pts_k)
    out["routes"] = build([({"id": r["id"], "name_cs": r["name_cs"], "length_m": r["length_m"], "max_grade_pct": r["max_grade_pct"], "share_over_5pct": r["share_over_5pct"], "dz_m": r["dz_m"]}, r["pts"], geom_line)
                           for r in routes])
    return out


def write_registry(objs):
    clean = []
    for o in objs:
        d = {k: v for k, v in o.items() if k != "poly"}
        if o.get("poly"):
            d["has_polygon"] = True
        if o["type"] == "block":
            d["land_use_text"] = BL.LANDUSE.get(o.get("land_use"), "")
        clean.append(d)
    meta = {"plan_id": C.PLAN_ID, "atlas_version": canon.ATLAS_VERSION, "bible_version": canon.load_bible()["meta"]["version"], "bible_sha256": canon.bible_sha256(),
            "origin_atlas_km": {"x": C.X0_KM, "y": C.Y0_KM}, "size_m": {"w": C.W_M, "h": C.H_M}, "count": len(clean),
            "status_note": "pos_status = proposed pro všechny polohy; exist_status approved jen pro to, co říká bible (parlament, muzeum, historický přístav C-02, pobřežní silnice)"}
    (OUT / "cp_objects.json").write_text(json.dumps({"meta": meta, "objects": clean}, ensure_ascii=False, indent=1), encoding="utf-8")
    cols = ["id", "type", "subtype", "name_cs", "name_en", "name_ja", "district", "u", "v", "x_km", "y_km", "area_m2", "length_m", "land_use", "exist_status", "name_status", "pos_status", "origin", "atlas_ref", "bible_ref", "notes"]
    with (OUT / "cp_objects.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(cols)
        for o in clean:
            w.writerow([("" if o.get(c) is None else o.get(c)) for c in cols])
    with (OUT / "cp_photo_guide.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["location_id", "pohled_kam", "směr_moře", "blízké_body", "vzdálené_viditelné", "architektura", "roční_doba", "vyhnout_se"])
        for o in clean:
            g = o.get("photo_guide")
            if g:
                w.writerow([g["location_id"], g["view_toward"], g["sea_direction"] or "", ", ".join(g["near_ids"]), ", ".join(f"{v['id']} ({v['dir']}, {v['dist_km']} km)" for v in g["far_visible"]), g["styles"], g["season"], g["avoid"]])
    return meta, clean


def graph_json(graph):
    deg = graph.degrees()
    nodes = [{"id": i, "u": round(p[0], 1), "v": round(p[1], 1), "x_km": round(C.to_km(p)[0], 4), "y_km": round(C.to_km(p)[1], 4), "degree": deg.get(i, 0)} for i, p in enumerate(graph.nodes) if i in deg]
    edges = [{"id": e["id"], "a": e["a"], "b": e["b"], "length_m": round(e["length"], 1), "cls": e["cls"], "row_m": e["row_m"], "name_cs": e.get("name_cs"), "atlas_id": e.get("atlas_id"),
              "section": e.get("section"), "district": e.get("district")} for e in graph.edges]
    return {"plan_id": C.PLAN_ID, "status": "proposed", "note": "dopravní graf uliční sítě v lokálním metrickém modelu; délky z geometrie (m)", "nodes": nodes, "edges": edges}


def stats_of(ctx, graph, blocks, routes, objs):
    deg = graph.degrees()
    by = defaultdict(float)
    for e in graph.edges:
        by[e["cls"]] += e["length"]
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in graph.edges:
        ra, rb = find(e["a"]), find(e["b"])
        if ra != rb:
            parent[ra] = rb
    comps = Counter(find(e["a"]) for e in graph.edges)
    largest = max(comps.values()) if comps else 0
    return {
        "footprint_km2": round(float(ctx.fp.sum()) * C.CELL ** 2 / 1e6, 2),
        "districts_km2": {k: round(sum(G.area(p) for p in v) / 1e6, 2) for k, v in ctx.districts.items()},
        "streets_km": {k: round(v / 1000, 1) for k, v in sorted(by.items())}, "streets_km_total": round(sum(by.values()) / 1000, 1),
        "nodes": len(deg), "edges": len(graph.edges), "intersections_deg3plus": sum(1 for v in deg.values() if v >= 3), "dead_ends": sum(1 for v in deg.values() if v == 1),
        "components": len(comps), "largest_component_share": round(largest / max(1, len(graph.edges)), 3),
        "blocks": len(blocks), "block_area_km2": round(sum(b["area"] for b in blocks) / 1e6, 2), "block_median_m2": round(sorted(b["area"] for b in blocks)[len(blocks) // 2]),
        "land_use_blocks": dict(Counter(b["use"] for b in blocks)),
        "objects": dict(Counter(o["type"] for o in objs)),
        "routes": [{k: r[k] for k in ("id", "length_m", "max_grade_pct", "share_over_5pct", "dz_m")} for r in routes],
    }


def run_checks(ctx, L, graph, blocks, objs, routes, stations, svg_text):
    city = ctx.city
    ck = {}
    ck["rámec: okno plánu leží uvnitř plátna atlasu a odpovídá listu A2 v měřítku 1 : 10 000"] = (
        abs(C.W_M - 5940.0) < 1e-6 and abs(C.H_M - 4200.0) < 1e-6 and canon.CANVAS["x0"] <= C.X0_KM and C.X0_KM + C.W_M / 1000 <= canon.CANVAS["x0"] + canon.CANVAS["w"]
        and canon.CANVAS["y0"] <= C.Y0_KM and C.Y0_KM + C.H_M / 1000 <= canon.CANVAS["y0"] + canon.CANVAS["h"] and 'width="594mm" height="420mm" viewBox="0 0 5940 4200"' in svg_text)
    ids = [o["id"] for o in objs]
    ck["registr plánu: ID jsou jedinečná a každý objekt má stavy a původ"] = len(ids) == len(set(ids)) and all(
        o.get("exist_status") and o.get("name_status") and o.get("pos_status") and o.get("origin") for o in objs)
    ck["registr plánu: všechny polohy jsou návrh (pos_status = proposed)"] = all(o["pos_status"] == "proposed" for o in objs)
    appr = sorted(o["id"] for o in objs if o["exist_status"] == "approved")
    ck["registr plánu: schváleno je jen to, co říká bible (CP-01, parlament, muzeum, C-02, pobřežní silnice)"] = set(appr) <= {"CP-01", "CP-B01", "CP-B06", "C-02", "CP-PR01"} | {o["id"] for o in objs if o["type"] == "street" and o["name_cs"] == "Pobřežní třída"}
    atlas_st = {s["id"]: (s["u"], s["v"]) for s in city.stations}
    ck["stanice plánu přesně odpovídají stanicím atlasu (poloha, linky)"] = all(
        math.dist((o["u"], o["v"]), atlas_st[o["id"]]) < 0.2 for o in objs if o["type"] == "station") and {o["id"] for o in objs if o["type"] == "station"} == set(atlas_st)
    # silnice atlasu zůstaly
    ok_roads = True
    detail = {}
    for rid in ("RD-11", "RD-12", "RD-07", "RD-R1"):
        atlas_len = sum(G.length(r["pts"]) for r in city.roads if r["id"] == rid)
        plan_len = sum(e["length"] for e in graph.edges if e.get("atlas_id") == rid and not e.get("plan_new"))
        clip = 2 * LY.RING_R if rid in ("RD-11", "RD-12") else 0.0
        detail[rid] = (round(atlas_len), round(plan_len), clip)
        ok_roads &= abs(atlas_len - clip - plan_len) <= max(10.0, 0.012 * atlas_len)
    ck["tepny atlasu (RD-11, RD-12, RD-07, R1) mají v plánu stejnou délku (kromě okružní komunikace u středu; ±1,2 %)"] = ok_roads
    st = stats_of(ctx, graph, blocks, routes, objs)
    ck["graf: jedna souvislá síť (≥ 99 % hran ve největší komponentě)"] = st["largest_component_share"] >= 0.99
    ck["bloky a budovy leží na pevnině a mimo přístavní pánev"] = all(
        G.point_in_poly(G.centroid(o["poly"]), city.coast) and not G.point_in_poly(G.centroid(o["poly"]), city.basin) for o in objs if o["type"] in ("block", "building") and o.get("poly"))
    ck["čtvrtě: každá z C-03…C-06 má správní budovu, školu a park do 900 m od středu"] = all(
        any(o["type"] == "building" and o["subtype"] == "admin" and o["district"] == d for o in objs) and any(o["type"] == "building" and o["subtype"] == "school" and o["district"] == d for o in objs)
        and any(o["type"] == "park" and math.hypot(o["u"] - G.centroid(max(ctx.districts[d], key=G.area))[0], o["v"] - G.centroid(max(ctx.districts[d], key=G.area))[1]) < 900.0 for o in objs) for d in ctx.districts)
    need = {"CP-B01", "CP-B06", "CP-B07", "CP-B08", "CP-SQ03", "CP-PR01", "CP-PK01", "C-02", "ST-W", "ST-N", "ST-E", "ST-S"}
    ck["plán obsahuje parlament, čtyři správní budovy, muzeum, kostel, tržiště, přístav, promenádu, park a stanice L2/L3"] = need <= set(ids) and sum(1 for o in objs if o.get("subtype") == "admin") == 4
    # budovy neleží na ulicích (klíčové budovy vs. rastr ulic)
    street = ctx.street_mask_b
    bad = []
    for o in objs:
        if o["type"] == "building" and o.get("poly") and o["subtype"] not in ("ferry_terminal",):
            poly = o["poly"]
            xs = [p[0] for p in poly]
            ys = [p[1] for p in poly]
            samples = 0
            hits = 0
            for uu in range(int(min(xs)), int(max(xs)) + 1, 3):
                for vv in range(int(min(ys)), int(max(ys)) + 1, 3):
                    if G.point_in_poly((uu, vv), poly):
                        samples += 1
                        hits += bool(street[min(BL.NYB - 1, vv), min(BL.NXB - 1, uu)])
            if samples and hits / samples > 0.12:
                bad.append((o["id"], round(hits / samples, 2)))
    ck["klíčové budovy neleží na uličním rastru (≤ 12 % plochy)"] = not bad
    ck["bezbariérové trasy: tři trasy, každá ≥ 400 m a největší sklon ≤ 8 %"] = len(routes) == 3 and all(r["length_m"] >= 400 and r["max_grade_pct"] <= 8.0 for r in routes)
    ck["SVG: povinné vrstvy a popisky cs/en/ja jsou skutečné <text> prvky"] = all(f'id="{l}"' in svg_text for l in ("bg-sea", "land", "blocks", "streets", "rail-L3", "stations", "buildings-key", "poi", "labels-cs", "labels-en", "labels-ja", "marginalia")) and svg_text.count("<text") > 120
    return ck, st, detail, bad


def write_readme(st):
    use_rows = "\n".join(f"| `{k}` | {v} | {st['land_use_blocks'].get(k, 0)} |" for k, v in BL.LANDUSE.items())
    txt = f"""# Plán hlavního města Larpingtonu – podklad CP-01 (atlas {canon.ATLAS_VERSION})

**Pracovní návrh (`proposed`).** Schematický podklad v lokálním metrickém modelu: délky ulic a vzdálenosti plynou z geometrie, názvy a polohy jsou návrh. Pobřeží, silnice, koleje, stanice a přístav C-02 jsou z atlasu beze změny.

## Souřadnice

- List A2 (594 × 420 mm) v měřítku **1 : 10 000**, okno 5 940 × 4 200 m; 1 jednotka SVG = 1 m.
- Lokální metry: `u` = východ, `v` = jih, počátek v SZ rohu okna. Převod na km atlasu: `x_km = 13,10 + u/1000`, `y_km = 10,30 + v/1000`.
- GeoJSON `cp_*.geojson` je v lokálních metrech, `cp_*_atlas_km.geojson` v km atlasu (bez zeměpisného CRS – fiktivní svět; pseudo-lon/lat jsou hypotetické).

## Soubory

| Soubor | Obsah |
|---|---|
| `capital_plan_base.svg` | vrstvené editovatelné SVG (Inkscape): moře, pevnina, vrstevnice, pláže, zelené klíny, čtvrtě, bloky, prostory, přístav, ulice, koleje, stanice, budovy, POI, trasy, mřížka, popisky cs/en/ja, okraje |
| `capital_plan_viewer.html` | prohlížeč s hledáním, vrstvami, jazyky a záznamem objektu |
| `cp_graph.json` | dopravní graf: uzly (stupeň) a hrany (třída, šířka, délka, název, odkaz na silnici atlasu) |
| `cp_streets/blocks/districts/buildings/spaces/points/routes.geojson` | vrstvy plánu |
| `cp_objects.json`, `cp_objects.csv`, `cp_photo_guide.csv` | registr {sum(st['objects'].values())} objektů plánu a foto/video vodítko |
| `cp_frame.json`, `cp_report.json` | rámec a výsledky kontrol |

## Třídy ulic (`cls`) a šířky

`R1` pobřežní silnice (22 m) · `A` tepny z atlasu (22 m) · `B` diagonální bulváry a spojka k Východnímu nábřeží (20 m) · `S` okružní komunikace Náměstí čtyř (14 m) · `P` nábřeží (18 m) · `C` místní ulice (10 m, ve starém městě 8 m) · `L` uličky starého města (5 m).

## Využití bloků (`land_use`)

| Kód | Význam | Počet bloků |
|---|---|---|
{use_rows}

## Prefixy ID

`CP-01` plán · `CP-B` budovy · `CP-SQ` náměstí a předprostory · `CP-PK` parky · `CP-GW` zelené klíny · `CP-PR` promenáda · `CP-PI` molo · `CP-BL` bloky · `CP-UL` pojmenované ulice · `CP-AR` bezbariérové trasy · `CP-CF` kavárny · `CP-RN` půjčovny · `CP-SH` obchody · `CP-ZR` maloobchodní zóny. Stanice `ST-*`, čtvrtě `C-03…C-06` a přístav `C-02` mají ID atlasu.

Postup, rozhodnutí a omezení: `../../docs/F7_CAPITAL_NOTES.md`; zadání další etapy: `../../docs/CAPITAL_PLAN_BRIEF.md`.
"""
    (OUT / "README_CAPITAL.md").write_text(txt, encoding="utf-8")


def update_atlas_docs(objs, st):
    """Zapíše plán do patche bible (návrh, bez aplikace) a do matice dohledatelnosti kanonu."""
    import registry_extra as rx
    docs = ATLAS / "docs"
    byid = {o["id"]: o for o in objs}
    pp = docs / "bible_patch_v1.1.json"
    doc = json.loads(pp.read_text(encoding="utf-8"))
    doc["patch"] = [p for p in doc["patch"] if not p["path"].startswith("/urbanism/capital_plan") and not (p["path"] == "/open_decisions/-" and p["value"].get("id") in ("D10", "D11", "D12"))]
    key = {k: {"id": byid[k]["id"], "x_km": byid[k]["x_km"], "y_km": byid[k]["y_km"]} for k in ("CP-B01", "CP-B06", "CP-B07", "CP-B08", "CP-B09", "CP-SQ01", "CP-SQ03", "CP-PR01")}
    model = {"plan_id": C.PLAN_ID, "sheet": "A2, 1 : 10 000, okno x 13,10–19,04 km, y 10,30–14,50 km",
             "built_up_km2": st["footprint_km2"], "districts_km2": st["districts_km2"], "streets_km": st["streets_km_total"], "blocks": st["blocks"],
             "composition": "Náměstí čtyř (parlament v Parlamentní zahradě, čtyři správní budovy ve větrníkovém uspořádání), čtyři čtvrtě jako výseče kolem centra, staré město u přístavu s tržištěm a kostelem, zelené klíny uvnitř okruhu L3",
             "key_objects": key, "files": "atlas/current/capital/"}
    doc["patch"].append({"op": "add", "path": "/urbanism/capital_plan_model", "value": {"value": model, "status": "proposed", "note": "podklad plánu hlavního města (F7); vše návrh"}})
    doc["patch"] += [
        {"op": "add", "path": "/open_decisions/-", "value": {"id": "D10", "question": "Potvrdit kompozici centra hlavního města: Náměstí čtyř (parlament uprostřed, čtyři správní budovy kolem) – nebo parlament v historické budově u přístavu.", "suggestion": "Viz atlas/docs/F7_CAPITAL_NOTES.md (O19)"}},
        {"op": "add", "path": "/open_decisions/-", "value": {"id": "D11", "question": f"Potvrdit zastavěné území hlavního města ({st['footprint_km2']} km² místo 4,8 km² z F3; zahrnuje staré město u přístavu, čtvrť Východní nábřeží a zelené klíny) a napojení na přístav (C-17).", "suggestion": "Viz atlas/docs/F7_CAPITAL_NOTES.md (C-17, O21)"}},
        {"op": "add", "path": "/open_decisions/-", "value": {"id": "D12", "question": "Potvrdit názvy čtvrtí a ulic plánu, polohu prémiového hotelu HV-01 na promenádě a muzea u Centrálního parku.", "suggestion": "Viz atlas/current/capital/cp_objects.csv"}},
    ]
    doc["patch_meta"]["atlas_version"] = canon.ATLAS_VERSION
    pp.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    # matice dohledatelnosti (TRACE je ve zdrojovém modulu registry_extra a odkazuje i na objekty plánu CP-*)
    reg = json.loads((ATLAS / "current" / "registry" / "places.json").read_text(encoding="utf-8"))
    rx.update_trace(reg["objects"] + [{"id": o["id"]} for o in objs], docs)


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    city = C.City()
    ctx = CX.build_ctx(city)
    L = LY.build_layout(ctx)
    stations = LY.station_layout(ctx)
    graph = build_graph(ctx, L)
    spaces = BL.space_polys(ctx, L)
    blocks = BL.build_blocks(ctx, L, graph, spaces, stations)
    BL.classify_blocks(ctx, L, blocks, stations, spaces)
    names = PO.name_streets(ctx, graph)
    objs = PO.build_objects(ctx, L, graph, blocks, spaces, stations)
    PO.add_points(ctx, L, blocks, objs)
    add_street_objects(ctx, graph, objs, names)
    routes = routes_over_graph(ctx, graph, L, objs)
    for o in objs:
        if o["type"] in ("building", "square", "park", "station", "promenade", "harbor", "pier", "retail_zone", "rental", "cafe", "shop", "plan"):
            o["photo_guide"] = PO.photo_guide(city, o, objs)
    meta = {"atlas_version": canon.ATLAS_VERSION}
    svg = SV.build_svg(ctx, L, graph, blocks, spaces, stations, objs, routes, meta)
    (OUT / "capital_plan_base.svg").write_text(svg, encoding="utf-8")
    rmeta, clean = write_registry(objs)
    (OUT / "capital_plan_viewer.html").write_text(VW.viewer_html(svg, clean, rmeta), encoding="utf-8")
    (OUT / "cp_frame.json").write_text(json.dumps(C.frame_json() | {"atlas_version": canon.ATLAS_VERSION}, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "cp_graph.json").write_text(json.dumps(graph_json(graph), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    sets = feature_sets(ctx, graph, blocks, objs, routes)
    for name, (loc, km) in sets.items():
        write_geojson(OUT / f"cp_{name}.geojson", loc, "lokální metry plánu (u východ, v jih; počátek v SZ rohu okna)")
        write_geojson(OUT / f"cp_{name}_atlas_km.geojson", km, "lokální km atlasu (x východ, y jih; shodné se souřadnicemi atlasu)")
    ck, st, detail, bad = run_checks(ctx, L, graph, blocks, objs, routes, stations, svg)
    rep = {"plan_id": C.PLAN_ID, "atlas_version": canon.ATLAS_VERSION, "checks": ck, "all_ok": all(ck.values()), "stats": st, "atlas_road_lengths_m (atlas, plan, ring_clip)": detail,
           "buildings_on_streets": bad, "build_seconds": round(time.time() - t0, 1)}
    (OUT / "cp_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    write_readme(st)
    update_atlas_docs(objs, st)
    for k, v in ck.items():
        print(("  OK    " if v else "  CHYBA ") + k)
    print("statistika:", json.dumps({k: st[k] for k in ("footprint_km2", "streets_km_total", "nodes", "edges", "dead_ends", "blocks", "block_area_km2")}, ensure_ascii=False))
    print("trasy:", st["routes"])
    print("VÝSLEDEK:", "vše v pořádku" if rep["all_ok"] else "jsou chyby", f"({time.time() - t0:.0f} s)")
    return 0 if rep["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
