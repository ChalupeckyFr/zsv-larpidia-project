"""F4: jednotný registr míst a objektů + seznam odchylek, návrh jmen, patch bible a matice dohledatelnosti kanonu.

Spuštění:  python atlas/scripts/build_registry.py
Výstup:    atlas/current/registry/places.json, places.csv, deviations.csv, names_proposed.csv, atlas_check_report.json
           atlas/docs/bible_patch_v1.1.json, atlas/docs/NAMES_AND_DEVIATIONS_TO_APPROVE.md, docs/canon_extract.csv (sloupec atlas_objects)
Originály projektu se nemění. VŠE NOVÉ JE PRACOVNÍ NÁVRH (proposed).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import canon
import geom
import h_vis
import human_env as he
from canon import ATLAS

CUR = ATLAS / "current"
HUMAN = CUR / "human"
REG = CUR / "registry"
DOCS = ATLAS / "docs"

# ------------------------------------------------------------------ návrh jmen (PROPOSED)
# id: (cs, en, ja)
NAMES = {
    "M-01": ("Larpova hora", "Mount Larp", "ラープ山"), "M-02": ("Zimní hora", "Winter Peak", "冬山"), "M-03": ("Kulatý vrch", "Round Hill", "丸山"),
    "N-01": ("Mys Skalní vyhlídky", "Cliff Lookout Cape", "断崖展望岬"), "N-02": ("Krystalová jeskyně", "Crystal Cave", "水晶洞"),
    "N-03": ("Larpský vodopád", "Larp Falls", "ラープの滝"), "N-04": ("Přehradní jezero Larp", "Larp Reservoir", "ラープ湖"),
    "C-01": ("Larpington", "Larpington", "ラープトン"), "C-02": ("Historický přístav Larpington", "Larpington Old Harbour", "ラープトン旧港"),
    "T-01": ("Praha", "Praha", "プラハ"), "T-02": ("Čimprlichovo Hradiště", "Čimprlichovo Hradiště", "チンプルリフ砦"), "T-03": ("Havlišovo Doupě", "Havliš's Den", "ハヴリシュの巣"),
    "T-04": ("Ōru Maito", "Ōru Maito", "オールマイト"), "T-05": ("Aokawa", "Aokawa", "青川"), "T-06": ("Hoshimachi", "Hoshimachi", "星町"),
    "I-01": ("Zelená průmyslová zóna", "Green Industrial Zone", "グリーン工業地帯"), "I-02": ("Závod na zpracování mořských řas", "Seaweed Processing Plant", "海藻処理工場"),
    "I-03": ("Nákladní přístav", "Cargo Port", "貨物港"), "A-01": ("Regionální letiště Larpidie", "Larpidia Regional Airport", "ラーピディア地方空港"),
    "A-02": ("Přistávací plocha Paraland", "Paraland Airstrip", "パラランド飛行場"), "P-01": ("Paraland Link", "Paraland Link", "パラランド連絡"),
    "H-01": ("Severní rybářský přístav", "North Fishing Port", "北の漁港"), "H-02": ("Marina Paraland", "Paraland Marina", "パラランド・マリーナ"),
    "W-01": ("Řeka Larp", "Larp River", "ラープ川"), "W-02": ("Aokawa (Modrá řeka)", "Aokawa (Blue River)", "青川"), "W-03": ("Severní potok", "North Brook", "北の小川"),
    "W-04": ("Havlišův potok", "Havliš Brook", "ハヴリシュ川"), "W-05": ("Pražský potok", "Praha Brook", "プラハ川"),
    "W-06": ("Severní potok Paralandu", "Paraland North Brook", "パラランド北川"), "W-07": ("Jižní potok Paralandu", "Paraland South Brook", "パラランド南川"),
    "PL-01": ("Staré městečko Paralandu", "Paraland Old Town", "パラランド旧市街"), "PL-02": ("Zámek Paraland", "Paraland Castle", "パラランド城"),
    "PL-03": ("Resorty jih", "South Resorts", "南リゾート"), "PL-04": ("Aquapark Paraland", "Paraland Aquapark", "パラランド・アクアパーク"),
    "PL-05": ("Marina – přístavní vesnice", "Marina Village", "マリーナ村"), "PL-06": ("Zřícenina nad městečkem", "Ruin above the Old Town", "旧市街の廃墟"),
    "LH-01": ("Maják severního mysu", "North Cape Lighthouse", "北岬灯台"),
}
BAYS = [
    ("BAY-N1", "Zátoka Ōru Maito", "Ōru Maito Bay", "オールマイト湾", (13.9, 2.5)), ("BAY-N2", "Zátoka Hoshimachi", "Hoshimachi Bay", "星町湾", (19.2, 3.4)),
    ("BAY-S", "Záliv Larpington", "Larpington Bay", "ラープトン湾", (17.5, 14.2)), ("BAY-E", "Zátoka nákladního přístavu", "Cargo Bay", "貨物湾", (21.2, 12.0)),
    ("CAPE-W", "Skalní mys", "Rock Cape", "岩岬", (2.7, 6.4)), ("CAPE-N", "Severní mys", "North Cape", "北岬", (16.6, 1.5)),
    ("PEN-SE", "Poloostrov Paraland Link", "Paraland Link Peninsula", "パラランド連絡半島", (21.8, 14.2)),
]

STYLE = {
    "capital": "cihlové anglicko-velšské domy, kamenné zdi s mechem, kostel, uličky; diskrétní japonské prvky infrastruktury; historický přístav a butiky",
    "north": "kompaktní smíšená anglicko-japonská městečka, úzké ulice, trhy a staré kostely; vlhké večery, teplá světla obchodů",
    "industry": "vzdušné zelené průmyslové areály se stromy, školami, školkami a restauracemi; ne sci-fi továrna",
    "mountain": "zalesněné nízké pohoří do 560 m (ne alpské), louky, mechové kmeny, žádné město ani přístav",
    "coast_cliff": "útesy a skalnaté pobřeží, bezpečné vyhlídky s oplocením; bez pláží a bez pobídek ke skokům",
    "beach": "písčité pláže jen na jihu/jihovýchodě hlavního ostrova a na východě Paralandu",
    "paraland": "resorty, aquapark, malé historické městečko, hrad/zámeček, lesy; klidná rekreace s rezervacemi",
    "rail_l1": "tematizovaný vyhlídkový vlak (hypotetické licencované motivy), osvětlená krystalová jeskyně, vodopád za oknem",
    "rail_l2": "historicky stylizované elektrické soupravy (parní vzhled bez spalování)",
    "rail_l3": "moderní podzemní metro, krátká prosklená galerie pod průlivem",
}
AVOID = {
    "west_northwest": "žádné pláže na útesovém SZ; žádná velkoměstská zástavba; vrcholy max 560 m",
    "central_west": "jeskyně, vodopád a přehrada jsou blízko sebe; žádné mrakodrapy",
    "north": "žádné vysokohorské štíty; japonský vliv bez karikatur",
    "east_northeast": "rovná nížina, bez horských hřbetů uvnitř průmyslu a letiště",
    "south_southeast": "přístav není vedle nejvyšší hory; hory jen v dálce na západě",
    "central_lowland": "obytná nížina, bez moře za zástavbou",
    "southeast_offshore": "Paraland je samostatný menší ostrov; žádné druhé velké letiště",
}
SEASON = "horké léto, 4 výrazná roční období, krátká zimní sezona na M-02 (zasněžování); tajfunové období srpen–říjen"

KIND_TYPE = {"viewpoint": "poi", "lighthouse": "poi", "spring": "poi", "hotel_vip": "poi", "castle": "poi", "ruin": "poi", "aquapark": "poi",
             "paragliding_launch": "poi", "paragliding_landing": "poi", "beach": "poi"}


def region_of(x, y, island):
    if island == "para" or x > 22.4 and y > 14.6:
        return "southeast_offshore"
    if x < 9.5:
        return "west_northwest"
    if 9.5 <= x < 13.2 and 5.2 <= y < 10.6:
        return "central_west"
    if y < 5.4:
        return "north"
    if x >= 17.0 and y < 12.4:
        return "east_northeast"
    if y >= 10.6:
        return "south_southeast"
    return "central_lowland"


def style_for(kind, region, x):
    if kind in ("capital", "district", "port") and region == "south_southeast":
        return STYLE["capital"]
    if region == "north":
        return STYLE["north"]
    if kind in ("industry", "airport", "port_area") or (region == "east_northeast" and kind not in ("beach",)):
        return STYLE["industry"]
    if region in ("west_northwest", "central_west"):
        return STYLE["mountain"] if kind not in ("village", "town") else STYLE["north"]
    if region == "southeast_offshore":
        return STYLE["paraland"]
    return STYLE["capital"]


def load_fc(name):
    return json.loads((HUMAN / f"{name}.geojson").read_text(encoding="utf-8"))["features"]


def lonlat(x, y):
    lon, lat = canon.km_to_lonlat(x, y)
    return [lon, lat]


def build():
    REG.mkdir(parents=True, exist_ok=True)
    W = he.World()
    trows = canon.table_rows()
    objs = []

    def pct(x, y):
        X, Y = canon.km_to_pct(x, y)
        return round(X, 2), round(Y, 2)

    def add(o):
        o.setdefault("name_ja", "")
        o.setdefault("name_en", "")
        if o["id"] in NAMES:
            cs, en, ja = NAMES[o["id"]]
            o["name_proposed"] = {"cs": cs, "en": en, "ja": ja}
            o["name_en"] = en
            o["name_ja"] = o["name_ja"] or ja
        if o.get("x_km") is not None:
            o["X_pct"], o["Y_pct"] = pct(o["x_km"], o["y_km"])
            o["lonlat_pseudo"] = lonlat(o["x_km"], o["y_km"])
            o["elev_m_model"] = round(W.zat(o["x_km"], o["y_km"]), 1)
            o["region"] = region_of(o["x_km"], o["y_km"], o.get("island", "main"))
        o.setdefault("origin", "atlas_new")
        o.setdefault("pos_status", "proposed")
        o.setdefault("notes", "")
        objs.append(o)

    # --- A) tabulka GEOGRAPHY (23 bodů, efektivní polohy zvolené varianty)
    TYPE = {"peak": "peak", "nature": "nature", "capital": "settlement", "port": "port", "district": "district", "town": "settlement", "industry": "industry",
            "airport": "airport", "rail_link": "rail_station"}
    for r in trows:
        add({"id": r["id"], "type": TYPE[r["category"]], "subtype": r["category"], "name_cs": r["name_doc"], "island": "main", "x_km": r["x_km"], "y_km": r["y_km"],
             "exist_status": r["exist_status"], "name_status": r["name_status"], "pos_status": "proposed", "origin": "geo_ref",
             "bible_ref": r["bible_ref"], "geo_ref_pct_orig": [r["X_pct_orig"], r["Y_pct_orig"]], "deviation": ({"dx_pct": r["dev_pct"][0], "dy_pct": r["dev_pct"][1], "dev_km": r["dev_km"]} if r["deviated"] else None),
             "notes": r["must_keep"]})
    # --- B) sídla mimo tabulku
    sett = {}
    for f in load_fc("settlements"):
        p = f["properties"]
        sett.setdefault(p["id"], p)
    table_ids = {r["id"] for r in trows}
    for sid, p in sett.items():
        if sid in table_ids:
            continue
        ring = next(f for f in load_fc("settlements") if f["properties"]["id"] == sid)["geometry"]["coordinates"][0]
        cx, cy = geom.centroid([tuple(c) for c in ring[:-1]])
        isl = "para" if sid.startswith("PL-") else "main"
        add({"id": sid, "type": "settlement", "subtype": p["kind"], "name_cs": p["name_cs"], "name_ja": p.get("name_ja", ""), "island": isl, "x_km": round(cx, 3), "y_km": round(cy, 3),
             "exist_status": p["exist_status"], "name_status": p["name_status"], "pos_status": "proposed", "origin": p["origin"], "population_model": p["population_model"],
             "footprint_km2": p["area_km2"], "notes": "modelová populace, ne sčítání"})
    # --- C) přístavy a letiště mimo tabulku
    pa = {}
    for f in load_fc("ports_airports"):
        pr = f["properties"]
        if f["geometry"]["type"] == "Point" and pr.get("kind") in ("fishing_port", "marina"):
            add({"id": pr["id"], "type": "port", "subtype": pr["kind"], "name_cs": pr["name_cs"], "island": "para" if pr["id"] == "H-02" else "main",
                 "x_km": f["geometry"]["coordinates"][0], "y_km": f["geometry"]["coordinates"][1], "exist_status": pr["exist_status"], "name_status": pr["name_status"],
                 "pos_status": "proposed", "notes": pr["note"]})
        if f["geometry"]["type"] == "Polygon" and pr.get("part") == "runway" and pr["id"] == "A-02":
            ring = f["geometry"]["coordinates"][0][:-1]
            cx, cy = geom.centroid([tuple(c) for c in ring])
            add({"id": "A-02", "type": "airport", "subtype": "light_airstrip", "name_cs": pr["name_cs"], "island": "para", "x_km": round(cx, 3), "y_km": round(cy, 3),
                 "exist_status": pr["exist_status"], "name_status": "proposed", "pos_status": "proposed", "runway": pr["runway"], "length_m": pr["length_m"], "notes": pr["note"]})
    # --- D) body zájmu
    for f in load_fc("poi"):
        p = f["properties"]
        add({"id": p["id"], "type": "poi", "subtype": p["kind"], "name_cs": p["name_cs"], "island": p["island"], "x_km": f["geometry"]["coordinates"][0], "y_km": f["geometry"]["coordinates"][1],
             "exist_status": p["exist_status"], "name_status": p["name_status"], "pos_status": "proposed", "notes": p.get("note", "")})
    # --- E) stanice
    for f in load_fc("rail_stations"):
        p = f["properties"]
        if p["id"] == "ST-L3-06":
            pass
        add({"id": p["id"], "type": "rail_station", "subtype": "hub" if len(p["lines"]) > 1 else "station", "name_cs": p["name_cs"], "island": "para" if p["id"] == "ST-L3-07" else "main",
             "x_km": f["geometry"]["coordinates"][0], "y_km": f["geometry"]["coordinates"][1], "lines": p["lines"], "exist_status": "proposed", "name_status": "proposed",
             "pos_status": "proposed", "notes": p.get("note", "")})
    # --- F) pojmenované tvary pobřeží (zátoky, mysy)
    for bid, cs, en, ja, (x, y) in BAYS:
        add({"id": bid, "type": "coast_feature", "subtype": "bay" if bid.startswith("BAY") else ("cape" if bid.startswith("CAPE") else "peninsula"), "name_cs": cs, "name_en": en, "name_ja": ja,
             "island": "main", "x_km": x, "y_km": y, "exist_status": "approved" if bid in ("CAPE-W", "BAY-S", "BAY-N1", "BAY-N2", "PEN-SE") else "proposed", "name_status": "proposed", "pos_status": "proposed",
             "origin": "geo_ref", "notes": "silueta z GEOGRAPHY_AND_CANON.md (PROPOSED): dvě severní zátoky, západní skalnatý mys, jižní záliv, JV poloostrov", "name_proposed": {"cs": cs, "en": en, "ja": ja}})
    # přehrada, vodopád jsou v tabulce (N-03, N-04); hráz navíc
    hf = json.loads((ATLAS / "current" / "relief" / "hydrography.geojson").read_text(encoding="utf-8"))["features"]
    rel = json.loads((ATLAS / "current" / "relief" / "relief_report.json").read_text(encoding="utf-8"))
    dam = next(r for r in W.rivers if r["id"] == "W-01" and r["part"] == "down")["pts"][0]
    add({"id": "DAM-N04", "type": "infrastructure", "subtype": "dam", "name_cs": "Hráz přehrady N-04", "island": "main", "x_km": dam[0], "y_km": dam[1], "exist_status": "approved", "name_status": "proposed",
         "pos_status": "proposed", "origin": "bible", "notes": f"vodárenské dílo; hráz ≈ {rel['lake']['dam_height_m_model']} m (model)", "name_en": "Larp Dam", "name_ja": "ラープダム"})
    # --- G) liniové objekty (reprezentativní bod = střed; geometrie je v GeoJSON)
    def line_mid(coords):
        return coords[len(coords) // 2]

    lines_reg = []
    rl = load_fc("rail_lines")
    for ln, nm in (("L1", "Skyline Experience"), ("L2", "Heritage Connect"), ("L3", "Metro Blue")):
        fs = [f for f in rl if f["properties"]["line"] == ln]
        pts = [tuple(c) for f in fs for c in f["geometry"]["coordinates"]]
        L = sum(math.dist(a, b) for f in fs for a, b in zip(f["geometry"]["coordinates"], f["geometry"]["coordinates"][1:]))
        add({"id": ln, "type": "rail_line", "subtype": ln, "name_cs": nm, "island": "main+para" if ln == "L3" else "main", "x_km": line_mid(pts)[0], "y_km": line_mid(pts)[1],
             "exist_status": "approved", "name_status": "proposed", "pos_status": "proposed", "origin": "bible", "length_km": round(L, 1), "bible_ref": "mobility.rail_lines; rail_line_roles_approved",
             "notes": "role linky schválena, jméno a vedení návrh"})
    for f in load_fc("roads"):
        p = f["properties"]
        if p["part"] != 0:
            continue
        c = f["geometry"]["coordinates"]
        full = [g for g in load_fc("roads") if g["properties"]["id"] == p["id"]]
        L = sum(math.dist(a, b) for g in full for a, b in zip(g["geometry"]["coordinates"], g["geometry"]["coordinates"][1:]))
        mid = full[len(full) // 2]["geometry"]["coordinates"]
        m = mid[len(mid) // 2]
        add({"id": p["id"], "type": "road", "subtype": p["class"], "name_cs": p["name_cs"], "island": p["island"], "x_km": m[0], "y_km": m[1], "exist_status": p["exist_status"], "name_status": "proposed",
             "pos_status": "proposed", "origin": p["origin"], "length_km": round(L, 2), "notes": p.get("note", "")})
    for f in load_fc("trails_cycleways"):
        p = f["properties"]
        c = f["geometry"]["coordinates"]
        m = line_mid(c)
        add({"id": p["id"], "type": "trail" if p["id"].startswith("TR") else ("cycleway" if p["id"].startswith("CY") else "other_line"), "subtype": p.get("kind", ""), "name_cs": p["name_cs"],
             "island": p.get("island", "main"), "x_km": m[0], "y_km": m[1], "exist_status": p.get("exist_status", "proposed"), "name_status": "proposed", "pos_status": "proposed",
             "origin": p.get("origin", "atlas_new"), "length_km": p.get("length_km"), "notes": p.get("note", "")})
    for f in hf:
        p = f["properties"]
        if f["geometry"]["type"] == "LineString" and p["part"] in ("all", "up"):
            c = f["geometry"]["coordinates"]
            m = line_mid(c)
            add({"id": p["id"], "type": "river", "subtype": p["kind"], "name_cs": p["name_working"], "island": "para" if p["id"] in ("W-06", "W-07") else "main", "x_km": m[0], "y_km": m[1],
                 "exist_status": "approved" if p["id"] == "W-01" else "proposed", "name_status": "proposed", "pos_status": "proposed", "origin": "atlas_new", "length_km": p["length_km"],
                 "bible_ref": "geography.natural_features (horské řeky)" if p["id"] == "W-01" else "", "notes": f"koryto {p['bed_start_m']}→{p['bed_end_m']} m (model)"})

    # --- foto/video vodítko pro bodové objekty
    vh = next(o for o in objs if o["id"] == "V-08")
    landmarks = {"M-01": W.pos("M-01"), "M-02": W.pos("M-02"), "M-03": W.pos("M-03"), "V-08": (vh["x_km"], vh["y_km"]),
                 "CAPE-N": (16.6, 1.5), "C-01": W.pos("C-01")}
    lm_h = {"M-01": 560, "M-02": 510, "M-03": 440, "V-08": 150, "CAPE-N": 20, "C-01": 20}
    lm_range = {"M-01": 26.0, "M-02": 26.0, "M-03": 26.0, "V-08": 14.0, "CAPE-N": 14.0, "C-01": 14.0}
    for o in objs:
        if o["type"] in ("road", "trail", "cycleway", "river", "rail_line", "other_line") or o.get("x_km") is None:
            continue
        p = (o["x_km"], o["y_km"])
        near = sorted(((math.dist(p, (q["x_km"], q["y_km"])), q["id"]) for q in objs if q is not o and q.get("x_km") is not None
                       and q["type"] not in ("road", "trail", "cycleway", "river", "rail_line", "other_line", "rail_station") and math.dist(p, (q["x_km"], q["y_km"])) < 1.0))
        vis = []
        h_obs = 12.0 if o["subtype"] in ("viewpoint", "lighthouse") else 2.0
        for lid, lp in landmarks.items():
            if lid == o["id"]:
                continue
            d = math.dist(p, lp)
            if 0.4 < d < lm_range[lid] and h_vis.visible(W, p, lp, h_obs, lm_h[lid] * 0.6):
                vis.append({"id": lid, "bearing_deg": round(h_vis.bearing_deg(p, lp)), "dir": h_vis.compass_cs(h_vis.bearing_deg(p, lp)), "dist_km": round(d, 1)})
        order = {k: i for i, k in enumerate(landmarks)}
        vis.sort(key=lambda v: (order[v["id"]] if v["dist_km"] > 1.5 else order[v["id"]] - 10))
        dc = W.d_coast(*p)
        sea_dir = None
        if dc < 0.8 and o.get("island") != "x":
            from h_poi import coast_frame
            poly = W.o["para"] if o.get("island") == "para" else W.o["main"]
            q, t, n, i = coast_frame(poly, p)
            sea_dir = h_vis.compass_cs((math.degrees(math.atan2(n[0], -n[1])) + 360) % 360)
        reg = o["region"]
        o["photo_guide"] = {
            "location_id": o["id"], "view_toward": ", ".join(f"{v['id']} {v['dir']}" for v in vis[:3]) or "bez dalekých dominant", "sea_direction": sea_dir,
            "near_ids": [n[1] for n in near[:6]], "far_visible": vis[:5], "styles": style_for(o["subtype"], reg, o["x_km"]), "season": SEASON, "avoid": AVOID[reg],
            "check_line": f"{o['id']} | pohled {', '.join(v['dir'] + ' ' + v['id'] for v in vis[:2]) or 'dle záměru'} | z jaké strany: dle kompozice | roční doba | {STYLE.get('capital') if reg == 'south_southeast' else '…'} | blízké: {', '.join(n[1] for n in near[:4]) or '–'} | vzdálené: {', '.join(v['id'] for v in vis[:3]) or '–'}"}
    # --- zápisy
    seen = set()
    for o in objs:
        if o["id"] in seen:
            raise SystemExit(f"Duplicitní ID v registru: {o['id']}")
        seen.add(o["id"])
    meta = {"atlas_version": "0.4-registry", "created": "2026-10-23", "bible_version": canon.load_bible()["meta"]["version"], "bible_sha256": canon.bible_sha256(),
            "frame_km": [canon.FRAME_W_KM, canon.FRAME_H_KM], "variant": canon.CHOSEN_VARIANT, "status_note": "pos_status = proposed pro všechny polohy; exist_status/name_status dle bible",
            "pseudo_geo_note": "lonlat_pseudo je HYPOTETICKÉ (kolem 33,9 N / 137,6 E)", "count": len(objs)}
    (REG / "places.json").write_text(json.dumps({"atlas_meta": meta, "objects": objs}, ensure_ascii=False, indent=1), encoding="utf-8")
    cols = ["id", "type", "subtype", "name_cs", "name_en", "name_ja", "island", "region", "X_pct", "Y_pct", "x_km", "y_km", "elev_m_model", "exist_status", "name_status", "pos_status", "origin", "length_km", "notes"]
    with (REG / "places.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(cols)
        for o in objs:
            w.writerow([o.get(c, "") if o.get(c) is not None else "" for c in cols])
    with (REG / "photo_guide.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["location_id", "pohled_kam", "směr_moře", "blízké_body", "vzdálené_viditelné", "architektura", "roční_doba", "vyhnout_se"])
        for o in objs:
            g = o.get("photo_guide")
            if g:
                w.writerow([g["location_id"], g["view_toward"], g["sea_direction"] or "", ", ".join(g["near_ids"]), ", ".join(f"{v['id']} ({v['dir']}, {v['dist_km']} km)" for v in g["far_visible"]), g["styles"], g["season"], g["avoid"]])
    # odchylky
    with (REG / "deviations.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["id", "název", "původní X %", "původní Y %", "nové X %", "nové Y %", "odchylka X %", "odchylka Y %", "vzdálenost km", "důvod", "stav"])
        for r in trows:
            if r["deviated"]:
                w.writerow([r["id"], r["name_doc"], r["X_pct_orig"], r["Y_pct_orig"], r["X_pct"], r["Y_pct"], r["dev_pct"][0], r["dev_pct"][1], r["dev_km"],
                            "uvolnit severní obal pro hlubší zátoky (varianta B, R-06)", "přijato volbou varianty B; potvrdí tým při schvalování D1"])
    return W, objs, meta


if __name__ == "__main__":
    import registry_extra as rx

    W, objs, meta = build()
    c = Counter(o["type"] for o in objs)
    print("registr:", meta["count"], "objektů;", dict(c))
    rx.update_trace(objs, DOCS)
    rx.write_patch(objs, meta, DOCS, ATLAS, HUMAN)
    rx.write_names_doc(objs, DOCS, REG, NAMES, BAYS)
    print("matice dohledatelnosti, bible_patch_v1.1.json a NAMES_AND_DEVIATIONS_TO_APPROVE.md zapsány")
