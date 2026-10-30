"""Plán hlavního města (F7), krok 5: objekty plánu (budovy, prostory, stanice, body zájmu, pojmenované ulice) a foto/video vodítko.

Každý objekt má stavy exist/name/pos (jako registr atlasu), původ (`bible` = schválené v bibli, `atlas` = objekt atlasu, `plan_new` = nové v plánu)
a odkaz na bibli či atlas. Všechny polohy a jména jsou pracovní návrh; „approved“ má jen to, co říká bible (parlament, muzeum, historický přístav C-02).
"""
from __future__ import annotations

import math

import cp_data as C
import cp_geom as G
import cp_layout as LY
import h_vis
from cp_context import DISTRICT_NAMES

OLD_STREETS = {
    55.0: ("Přístavní ulice", "Harbour Street"), 125.0: ("Rybářská ulice", "Fishermen's Street"), 190.0: ("Tržní ulice", "Market Street"),
    300.0: ("Kostelní ulice", "Church Street"), 380.0: ("Zahradní ulice", "Garden Street"), 465.0: ("Vinná ulice", "Vine Street"),
    555.0: ("Lipová ulice", "Linden Street"), 642.0: ("Okružní ulice Starého Města", "Old Town Ring Street"),
}
EN_NAMES = {
    "Okružní třída Náměstí čtyř": "Square of the Four Ring", "Jihovýchodní bulvár": "South-East Boulevard", "Jihozápadní bulvár": "South-West Boulevard",
    "Severozápadní bulvár": "North-West Boulevard", "Severovýchodní bulvár": "North-East Boulevard", "Nábřeží 16. června": "Quay of 16 June",
    "Třída Východního nábřeží": "East Waterfront Avenue", "Javorová ulice": "Maple Street", "Západní alej": "West Avenue",
    "Školní třída": "School Avenue", "Severní sadová": "North Garden Road", "Klimečkova třída": "Klimeček Avenue",
    "Skleněná ulice": "Glass Street", "Muzejní třída": "Museum Avenue", "Parková ulice": "Park Street",
}
KEY_DISTRICT = {"W": "C-03", "N": "C-04", "E": "C-05", "S": "C-06"}
STYLE_CAPITAL = "staré cihlové řadové domy, úzké křivé uličky, několikapatrové prosklené obchody na Hlavní třídě, kostely, státní budovy, parky a historický přístav; bez mrakodrapů"
AVOID_CAPITAL = "přístav není vedle nejvyšší hory; hory jen v dálce na západě; žádné mrakodrapy"
SEASON = "horké léto, 4 výrazná roční období; tajfunové období srpen–říjen"


def G_polys_green(ctx):
    """Polygony zelených klínů z masky `ctx.green` (jen větší plochy)."""
    return G.mask_to_polygons(ctx.green, 0.0, 0.0, C.CELL, min_area=60000.0, simplify_tol=3.0)


def church_polygon(c, a=20.0, b=7.5, x0=6.0, cc=14.0, d=7.0, ang_deg=0.0):
    """Křížový půdorys kostela (loď podél úhlu ang, příčná loď poblíž východního konce)."""
    pts = [(-a, -b), (x0 - d, -b), (x0 - d, -cc), (x0 + d, -cc), (x0 + d, -b), (a, -b), (a, b), (x0 + d, b), (x0 + d, cc), (x0 - d, cc), (x0 - d, b), (-a, b)]
    ca, sa = math.cos(math.radians(ang_deg)), math.sin(math.radians(ang_deg))
    return [(c[0] + x * ca - y * sa, c[1] + x * sa + y * ca) for x, y in pts]


def name_streets(ctx, graph):
    """Pojmenuje hrany podle atlasu, třídy a vrstevnice vzdálenosti; vrací slovník název → hrany."""
    O = ctx.O
    names = {}
    for e in graph.edges:
        nm = e.get("name")
        aid = e.get("atlas_id")
        mid = G.point_at(e["pts"], e["length"] / 2)[0]
        inside = bool(ctx.fp[min(C.NY - 1, max(0, int(mid[1] / C.CELL))), min(C.NX - 1, max(0, int(mid[0] / C.CELL)))])
        if nm is None and aid == "RD-11" and inside:
            nm = ("Hlavní třída", "Main Avenue")
        elif nm is None and aid == "RD-12" and inside:
            nm = ("Přístavní třída", "Harbour Avenue") if mid[1] > O[1] else ("Severní třída", "North Avenue")
        elif nm is None and e["cls"] == "R1" and inside:
            nm = ("Pobřežní třída", "Coast Road")
        elif nm is None and aid == "RD-07" and inside:
            nm = ("Východní třída", "East Avenue")
        elif nm is None and e.get("level") in OLD_STREETS:
            nm = OLD_STREETS[e["level"]]
        elif isinstance(nm, str):
            nm = (nm, EN_NAMES.get(nm, nm.replace("Přístup ke stanici", "Access to station")))
        if nm:
            e["name_cs"], e["name_en"] = nm
            names.setdefault(nm[0], []).append(e)
    return names


def photo_guide(city, obj, others):
    u, v = obj["u"], obj["v"]
    x, y = C.to_km((u, v))
    p = (x, y)
    landmarks = {"M-01": city.W.pos("M-01"), "M-02": city.W.pos("M-02"), "M-03": city.W.pos("M-03")}
    lm_h = {"M-01": 560, "M-02": 510, "M-03": 440}
    vis = []
    for lid, lp in landmarks.items():
        d = math.dist(p, lp)
        if 0.4 < d < 26.0 and h_vis.visible(city.W, p, lp, 2.0, lm_h[lid] * 0.6):
            vis.append({"id": lid, "bearing_deg": round(h_vis.bearing_deg(p, lp)), "dir": h_vis.compass_cs(h_vis.bearing_deg(p, lp)), "dist_km": round(d, 1)})
    near = sorted(((math.hypot(u - o["u"], v - o["v"]), o["id"]) for o in others if o is not obj and o["type"] in ("building", "square", "park", "station", "promenade", "harbor", "pier", "retail_zone", "rental", "cafe", "shop") and math.hypot(u - o["u"], v - o["v"]) < 320.0))
    dc = float(city_dq(city, u, v))
    sea = "jih (přístav)" if 0.0 <= dc < 900.0 else None
    return {
        "location_id": obj["id"], "view_toward": ", ".join(f"{q['id']} {q['dir']}" for q in vis[:2]) or "bez dalekých dominant",
        "sea_direction": sea, "near_ids": [n[1] for n in near[:6]], "far_visible": vis, "styles": STYLE_CAPITAL, "season": SEASON, "avoid": AVOID_CAPITAL,
        "check_line": f"{obj['id']} | pohled dle záměru (moře na jihu, hory na západě v dálce) | z jaké strany: dle kompozice | roční doba | {STYLE_CAPITAL.split(';')[0]} | blízké: {', '.join(n[1] for n in near[:4]) or '–'} | vzdálené: {', '.join(q['id'] for q in vis[:2]) or '–'}"}


def city_dq(city, u, v):
    p = (u, v)
    best = min(math.dist(p, q) for q in city.coast[::3])
    return best if G.point_in_poly(p, city.coast) else -best


def build_objects(ctx, L, graph, blocks, spaces, stations):
    city = ctx.city
    objs = []

    def add(**o):
        o.setdefault("region", "south_southeast")
        o.setdefault("name_status", "proposed")
        o.setdefault("pos_status", "proposed")
        o.setdefault("exist_status", "proposed")
        o.setdefault("origin", "plan_new")
        poly = o.get("poly")
        if poly and "u" not in o:
            o["u"], o["v"] = G.centroid(poly)
        if poly:
            o.setdefault("area_m2", round(G.area(poly), 1))
        x, y = C.to_km((o["u"], o["v"]))
        o["x_km"], o["y_km"] = round(x, 4), round(y, 4)
        o["u"], o["v"] = round(o["u"], 1), round(o["v"], 1)
        objs.append(o)
        return o

    O = ctx.O
    add(id="CP-01", type="plan", subtype="city_plan", name_cs="Plán hlavního města Larpingtonu – podklad", name_en="Larpington city plan – base", u=O[0], v=O[1],
        origin="bible", bible_ref="MAP_PROMPT M-01 (v atlasu CP-01, protože M-01 je vrchol)", exist_status="approved",
        notes="schematický podklad v lokálním metrickém modelu (1 j = 1 m); ID CP-01 místo M-01 kvůli kolizi s vrcholem M-01")
    # ---- čtvrtě
    for did, polys in ctx.districts.items():
        big = max(polys, key=G.area)
        add(id=did, type="district", subtype="district", name_cs=DISTRICT_NAMES[did], name_en=DISTRICT_NAMES[did].replace("čtvrť", "District"), poly=big,
            origin="geo_ref", atlas_ref=did, bible_ref="urbanism.capital_four_districts", notes="v plánu výseč kolem Náměstí čtyř; jména z příjmení autorů (návrh)", area_m2=round(sum(G.area(p) for p in polys), 1))
    # ---- budovy
    add(id="CP-B01", type="building", subtype="parliament", name_cs="Budova parlamentu", name_en="Parliament House", name_ja="議事堂", poly=LY.rect_poly(L["parliament"]),
        exist_status="approved", origin="bible", bible_ref="politics.elected_parliament (approved); capital_roles: státní instituce", notes="uprostřed Parlamentní zahrady; poloha je otevřené rozhodnutí O19")
    for k, a in enumerate(L["admin"]):
        did = KEY_DISTRICT[a["district_key"]]
        add(id=f"CP-B0{2 + k}", type="building", subtype="admin", name_cs=f"Správní budova – {DISTRICT_NAMES[did]}", name_en=f"Administrative building – {DISTRICT_NAMES[did].replace('čtvrť', 'District')}",
            poly=LY.rect_poly(a), district=did, bible_ref="MAP_PROMPT M-01: čtyři správní budovy", notes="jedna budova pro každou čtvrť, větrníkové uspořádání kolem Náměstí čtyř; poloha je otevřené rozhodnutí O19")
    add(id="CP-B06", type="building", subtype="museum", name_cs="Interaktivní muzeum Košťálovy éry", name_en="Interactive Museum of the Košťál Era", name_ja="コシュチャール時代インタラクティブ博物館",
        poly=LY.rect_poly(L["museum"]), exist_status="approved", origin="bible", bible_ref="history.museum (approved); MAP_PROMPT M-01",
        notes="interaktivní expozice, archiv, filmová rekonstrukce, komentované prohlídky čtyř spoluvládců; u Centrálního parku")
    ch = L["church"]
    add(id="CP-B07", type="building", subtype="church", name_cs="Historický kostel (Kostel sv. Jiří – pracovně)", name_en="Historic church (St George's – working name)", name_ja="歴史的教会",
        poly=church_polygon(ch["c"], ang_deg=0.0), bible_ref="history.founding_story: první osadníci stavěli kostely; MAP_PROMPT M-01", notes="na Kostelním náměstí ve starém městě; cihla a kámen, mechem porostlé zdi")
    mh = L["market_hall"]
    add(id="CP-B08", type="building", subtype="market_hall", name_cs="Tržní hala", name_en="Market hall", name_ja="市場ホール", poly=LY.rect_poly(mh),
        bible_ref="history.founding_story: tržiště; MAP_PROMPT M-01", notes="krytá část tržiště na Tržním náměstí")
    hv = city.reg["HV-01"]
    moved = math.dist(C.to_m((hv["x_km"], hv["y_km"])), L["hotel"]["c"])
    add(id="CP-B09", type="building", subtype="hotel_premium", name_cs="Prémiový hotel nad promenádou", name_en="Premium harbour hotel", poly=LY.rect_poly(L["hotel"]), atlas_ref="HV-01",
        origin="atlas", bible_ref="urbanism.main_island_vip_lodging (approved)", notes=f"HV-01 z atlasu posunut o {moved:.0f} m k přístavní promenádě (poloha k potvrzení; atlas se tím nemění)")
    add(id="CP-B10", type="building", subtype="harbour_office", name_cs="Přístavní úřad a celnice (historická budova)", name_en="Harbour office and customs house", poly=LY.rect_poly(L["harbor_office"]),
        notes="u Přístavního náměstí; sídlo správy přístavu C-02")
    pf = L["ferry_pier"]
    add(id="CP-B11", type="building", subtype="ferry_terminal", name_cs="Terminál lodní linky na Paraland", name_en="Paraland ferry terminal", poly=LY.rect_poly(L["ferry_terminal"]),
        atlas_ref="FERRY-1", origin="atlas", notes="volitelný lodní okruh C-02 ↔ H-02 (bez autopřevozu)")
    add(id="CP-PI01", type="pier", subtype="ferry_pier", name_cs="Molo lodní linky", name_en="Ferry pier", poly=LY.rect_poly(pf), atlas_ref="FERRY-1", origin="atlas")
    # ---- přístav C-02 (z atlasu)
    add(id="C-02", type="harbor", subtype="historic_harbor", name_cs="Historický přístav Larpington", name_en="Larpington Old Harbour", name_ja="ラープトン旧港", poly=city.basin, origin="geo_ref", atlas_ref="C-02",
        exist_status="approved", bible_ref="GEOGRAPHY C-02: nábřeží, butiky, promenády", notes="pánev a dva vlnolamy z atlasu beze změny; plán přidává nábřeží, molo a Přístavní náměstí")
    # ---- prostory
    for sid, typ, nm, poly in spaces:
        sub = {"plaza": "civic_plaza", "park": "park", "square": "square", "promenade": "promenade"}[typ]
        ex = "approved" if sid == "CP-PR01" else "proposed"
        en = {"CP-SQ01": "Square of the Four", "CP-PK01": "Parliament Garden", "CP-PK02": "Central Park", "CP-PK03": "North Park", "CP-PK04": "West Park",
              "CP-PK05": "East Park", "CP-PK06": "Klimeček District Park", "CP-SQ02": "Harbour Square", "CP-SQ03": "Market Square", "CP-SQ04": "Church Square",
              "CP-PR01": "Harbour Promenade"}[sid]
        add(id=sid, type="park" if typ == "park" else ("promenade" if typ == "promenade" else "square"), subtype=sub, name_cs=nm, name_en=en, poly=poly, exist_status=ex,
            bible_ref="GEOGRAPHY C-02: nábřeží, butiky a promenády" if sid == "CP-PR01" else ("MAP_PROMPT M-01: park" if typ == "park" else ""))
    # ---- zelené klíny mezi čtvrtěmi (uvnitř okruhu L3)
    sector = {(-1, -1): "severozápadní", (1, -1): "severovýchodní", (1, 1): "jihovýchodní", (-1, 1): "jihozápadní"}
    en_sector = {"severozápadní": "North-west", "severovýchodní": "North-east", "jihovýchodní": "South-east", "jihozápadní": "South-west"}
    used_names = {}
    for k, poly in enumerate(sorted(G_polys_green(ctx), key=lambda p: -G.area(p)), 1):
        c = G.centroid(poly)
        nm = sector[(1 if c[0] >= ctx.O[0] else -1, 1 if c[1] >= ctx.O[1] else -1)]
        used_names[nm] = used_names.get(nm, 0) + 1
        suffix = "" if used_names[nm] == 1 else f" {used_names[nm]}"
        add(id=f"CP-GW{k:02d}", type="park", subtype="green_wedge", name_cs=f"Zelený klín {nm}{suffix}", name_en=f"{en_sector[nm]} green wedge{suffix}", poly=poly,
            notes="nezastavěné území mezi čtvrtěmi uvnitř okruhu L3: louky, sady, sport a rezerva pro budoucí zástavbu (návrh)")
    for k, (sid, s) in enumerate(stations.items()):
        add(id=f"CP-SQ{5 + k:02d}", type="square", subtype="station_plaza", name_cs=f"Předprostor stanice {sid}", name_en=f"Station forecourt {sid}", poly=s["plaza"], atlas_ref=sid, origin="atlas")
    # ---- stanice (atlas) s půdorysem z plánu
    for s in city.stations:
        pl = stations[s["id"]]
        add(id=s["id"], type="station", subtype=pl["kind"], name_cs=s["name_cs"], name_en=s["name_cs"], u=s["u"], v=s["v"], origin="atlas", atlas_ref=s["id"], lines=s["lines"],
            transfer=s.get("transfer", False), notes=s.get("note", ""), plan_geometry="surface station with platforms" if pl["kind"] == "surface" else "underground, two entrance pavilions")
    # ---- bloky
    for i, b in enumerate(blocks, 1):
        add(id=f"CP-BL-{i:04d}", type="block", subtype=b["use"], name_cs=f"Blok {i:04d}", name_en=f"Block {i:04d}", poly=b["poly"], district=b["district"], u=b["c"][0], v=b["c"][1],
            land_use=b["use"], notes="bloková plocha mezi ulicemi (využití je návrh)")
    return objs


def add_points(ctx, L, blocks, objs):
    """Body zájmu: kavárny, půjčovny, obchody; školy v blocích; maloobchodní zóny."""
    city = ctx.city
    q = ctx.rd12_quay_pt
    from cp_context import v_at_dq

    def add(**o):
        o.setdefault("region", "south_southeast")
        o.setdefault("name_status", "proposed")
        o.setdefault("pos_status", "proposed")
        o.setdefault("exist_status", "proposed")
        o.setdefault("origin", "plan_new")
        x, y = C.to_km((o["u"], o["v"]))
        o["x_km"], o["y_km"] = round(x, 4), round(y, 4)
        o["u"], o["v"] = round(o["u"], 1), round(o["v"], 1)
        objs.append(o)

    ms = L["market_sq"]["c"]
    cs_ = L["church_sq"]["c"]
    hs = L["harbor_sq"]["c"]
    cafes = [("Kavárna u Tržnice", "Market Café", (ms[0] - 36.0, ms[1] + 20.0)), ("Kavárna na Tržním náměstí", "Market Square Café", (ms[0] + 38.0, ms[1] + 22.0)),
             ("Kavárna u kostela", "Church Café", (cs_[0] + 40.0, cs_[1] + 18.0)), ("Přístavní kavárna", "Harbour Café", (hs[0] - 40.0, hs[1] + 16.0)),
             ("Kavárna na promenádě", "Promenade Café", (q[0] + 150.0, v_at_dq(ctx, q[0] + 150.0, 40.0))),
             ("Kavárna Náměstí čtyř – západ", "Square of the Four Café – West", (ctx.O[0] - 110.0, ctx.O[1] + 112.0)),
             ("Kavárna Náměstí čtyř – východ", "Square of the Four Café – East", (ctx.O[0] + 112.0, ctx.O[1] + 108.0)),
             ("Kavárna u Centrálního parku", "Central Park Café", (L["park_central"]["c"][0] + 130.0, L["park_central"]["c"][1] - 70.0))]
    for k, (cz, en, (u, v)) in enumerate(cafes, 1):
        add(id=f"CP-CF{k:02d}", type="cafe", subtype="cafe", name_cs=cz, name_en=en, u=u, v=v, bible_ref="MAP_PROMPT M-01: kavárny")
    rentals = [("Půjčovna kol a e-skútrů – přístav", "Bike and e-scooter rental – harbour", (q[0] - 70.0, q[1] - 14.0)),
               ("Půjčovna kajaků a loděk", "Kayak and boat rental", (q[0] + 235.0, v_at_dq(ctx, q[0] + 235.0, 22.0))),
               ("Půjčovna kol – Střed–Přístav", "Bike rental – ST-S", (city.station("ST-S")["u"] + 44.0, city.station("ST-S")["v"] + 8.0)),
               ("Půjčovna kol – Západ (uzel L1/L2/L3)", "Bike rental – West hub", (city.station("ST-W")["u"] + 70.0, city.station("ST-W")["v"] + 62.0))]
    for k, (cz, en, (u, v)) in enumerate(rentals, 1):
        add(id=f"CP-RN{k:02d}", type="rental", subtype="rental", name_cs=cz, name_en=en, u=u, v=v, bible_ref="MAP_PROMPT M-01: půjčovny")
    shops = [("Butiky s limitovanými kolekcemi – západ", "Limited-edition boutiques – west", (q[0] - 190.0, v_at_dq(ctx, q[0] - 190.0, 70.0))),
             ("Butiky s limitovanými kolekcemi – střed", "Limited-edition boutiques – centre", (q[0] + 40.0, v_at_dq(ctx, q[0] + 40.0, 95.0))),
             ("Butiky s limitovanými kolekcemi – východ", "Limited-edition boutiques – east", (q[0] + 250.0, v_at_dq(ctx, q[0] + 250.0, 80.0))),
             ("Obchodní pasáž Hlavní třídy", "Main Avenue arcade", (ctx.O[0] + 330.0, ctx.O[1] - 14.0)),
             ("Obchody u Tržního náměstí", "Market Square shops", (ms[0] + 10.0, ms[1] - 62.0)),
             ("Vlajkový obchod Aster & Tide", "Aster & Tide flagship", (ctx.O[0] + 120.0, ctx.O[1] - 48.0)),
             ("Obchodní dům Northlight", "Northlight department store", (ctx.O[0] + 300.0, ctx.O[1] - 48.0)),
             ("Mizu Design House", "Mizu Design House", (ctx.O[0] + 520.0, ctx.O[1] - 48.0)),
             ("Galerie Juniper", "Juniper Gallery", (ctx.O[0] + 730.0, ctx.O[1] - 48.0))]
    for k, (cz, en, (u, v)) in enumerate(shops, 1):
        add(id=f"CP-SH{k:02d}", type="shop", subtype="retail", name_cs=cz, name_en=en, u=u, v=v, bible_ref="GEOGRAPHY C-02 / capital_roles: obchody s limitovanými kolekcemi")
    # ---- školy: budova uvnitř bloku, který určila klasifikace
    n = 0
    for b in blocks:
        if b["use"] != "school":
            continue
        n += 1
        cx, cy = b["c"]
        ang = 0.0
        street = ctx.street_mask_b
        xs = [p[0] for p in b["poly"]]
        ys = [p[1] for p in b["poly"]]
        poly, found = None, False
        for w, h in ((56.0, 20.0), (44.0, 16.0), (32.0, 12.0)):
            cands = sorted(((math.hypot(x - cx, y - cy), x, y) for x in range(int(min(xs)), int(max(xs)) + 1, 4) for y in range(int(min(ys)), int(max(ys)) + 1, 4)))
            for _, x, y in cands:
                r = G.oriented_rect(x, y, w, h, ang)
                if all(G.point_in_poly(p, b["poly"]) for p in r) and not street[int(y - h / 2) - 1:int(y + h / 2) + 2, int(x - w / 2) - 1:int(x + w / 2) + 2].any():
                    poly, found, cx, cy = r, True, x, y
                    break
            if found:
                break
        if not found:
            poly = G.oriented_rect(cx, cy, 32.0, 12.0, ang)
        add(id=f"CP-B{11 + n:02d}", type="building", subtype="school", name_cs=f"Škola – {DISTRICT_NAMES[b['district']]}", name_en=f"School – {DISTRICT_NAMES[b['district']].replace('čtvrť', 'District')}",
            u=cx, v=cy, poly=poly, district=b["district"], bible_ref="MAP_PROMPT M-01: školy; social_services: kvalitní dostupné školství", notes="školní blok (areál se hřištěm)")
        objs[-1]["area_m2"] = round(G.area(poly), 1)
    # ---- maloobchodní zóny (výčet bloků)
    for zid, use, nm, en in (("CP-ZR01", "promenade_retail", "Zóna přístavní promenády", "Harbour promenade zone"), ("CP-ZR02", "retail_main", "Zóna Hlavní třídy", "Main Avenue zone"),
                             ("CP-ZR03", "old_town_mixed", "Zóna starého města", "Old town zone")):
        sel = [b for b in blocks if b["use"] == use]
        if not sel:
            continue
        cu = sum(b["c"][0] * b["area"] for b in sel) / sum(b["area"] for b in sel)
        cv = sum(b["c"][1] * b["area"] for b in sel) / sum(b["area"] for b in sel)
        add(id=zid, type="retail_zone", subtype=use, name_cs=nm, name_en=en, u=cu, v=cv, land_use=use, block_count=len(sel), area_m2=round(sum(b["area"] for b in sel), 0),
            notes="souhrn bloků s daným využitím")
    return objs
