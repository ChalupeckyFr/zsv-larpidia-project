"""Plán hlavního města (F7), krok 4: bloková území (mezi ulicemi), veřejné prostory a využití bloků (pracovní návrh).

Bloky vznikají z rastru 1 m: zástavba (půdorys města) minus ulice (šířka podle třídy) minus veřejné prostory a železniční koridor;
souvislé plochy se označí a převedou na polygony. Využití bloku určují pravidla podle polohy (staré město, státní čtvrť, stanice, hlavní třídy…).
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

import cp_data as C
import cp_geom as G
import cp_layout as LY
import raster
from cp_context import DID_INDEX
from cp_streets import ROW

CB = 1.0                                     # m, jemný rastr bloků
NXB, NYB = int(C.W_M / CB), int(C.H_M / CB)

LANDUSE = {
    "old_town_mixed": "Staré město – smíšená zástavba",
    "promenade_retail": "Přístavní promenáda – obchody s limitovanými kolekcemi, kavárny, půjčovny",
    "civic_mixed": "Státní čtvrť – instituce a služby",
    "transit_mixed": "Okolí stanice – služby a bydlení",
    "retail_main": "Hlavní třída – obchody a kavárny",
    "residential_mid": "Bydlení – středně husté",
    "residential_low": "Bydlení – zahrádkové",
    "school": "Škola a školní areál",
    "new_waterfront": "Východní nábřeží – nová smíšená čtvrť",
    "hotel_premium": "Prémiový hotel",
}


def upscale(mask2):
    """Rastr plánu (CELL m) → jemný rastr bloků (CB m)."""
    k = int(round(C.CELL / CB))
    return np.repeat(np.repeat(mask2, k, axis=0), k, axis=1)


def px_b(u, v):
    return (u / CB, v / CB)


def space_polys(ctx, L):
    """Veřejné prostory jako polygony (id, typ, název, polygon)."""
    sp = [
        ("CP-SQ01", "plaza", "Náměstí čtyř", L["civic_zone"]),
        ("CP-PK01", "park", "Parlamentní zahrada", L["garden"]),
        ("CP-PK02", "park", "Centrální park", LY.rect_poly(L["park_central"])),
        ("CP-PK03", "park", "Severní park", LY.rect_poly(L["park_north"])),
        ("CP-PK04", "park", "Západní park", LY.rect_poly(L["park_west"])),
        ("CP-PK05", "park", "Východní park (zelený koridor k Východnímu nábřeží)", LY.rect_poly(L["park_east"])),
        ("CP-PK06", "park", "Park Klimečkovy čtvrti", LY.rect_poly(L["park_c05"])),
        ("CP-SQ02", "square", "Přístavní náměstí", LY.rect_poly(L["harbor_sq"])),
        ("CP-SQ03", "square", "Tržní náměstí", LY.rect_poly(L["market_sq"])),
        ("CP-SQ04", "square", "Kostelní náměstí", LY.rect_poly(L["church_sq"])),
        ("CP-PR01", "promenade", "Přístavní promenáda", G.buffer_polyline_poly([p for p in ctx.quay_in if 2450 <= p[0] <= 4150], 9.5)),
    ]
    return sp


def build_blocks(ctx, L, graph, spaces, stations):
    """Bloková území: polygony s plochou a využitím."""
    st = Image.new("L", (NXB, NYB), 0)
    d = ImageDraw.Draw(st)
    for e in graph.edges:
        w = e.get("row") or ROW.get(e["cls"], 10.0)
        d.line([px_b(*p) for p in e["pts"]], fill=255, width=max(1, int(round(w / CB))), joint="curve")
    street = np.asarray(st) > 127
    sp = Image.new("L", (NXB, NYB), 0)
    d = ImageDraw.Draw(sp)
    for _, _, _, poly in spaces:
        d.polygon([px_b(*p) for p in poly], fill=255)
    for sid, s in stations.items():
        d.polygon([px_b(*p) for p in s["plaza"]], fill=255)
    d.polygon([px_b(*p) for p in ctx.city.basin], fill=255)                  # přístavní pánev není blok
    space = np.asarray(sp) > 127
    block = upscale(ctx.fp) & ~street & ~space & ~upscale(ctx.rail_mask)
    ctx.street_mask_b = street
    labels, n, bbox, area_px = G.label_mask(block)
    blocks = []
    min_area = 450.0
    for k in range(1, n + 1):
        a = float(area_px[k]) * CB * CB
        if a < min_area:
            continue
        r0, r1, c0, c1 = bbox[k]
        sub = labels[r0:r1 + 1, c0:c1 + 1] == k
        polys = G.mask_to_polygons(sub, c0 * CB, r0 * CB, CB, min_area=min_area, simplify_tol=1.1)
        if not polys:
            continue
        poly = max(polys, key=G.area)
        cen = G.centroid(poly)
        if not G.point_in_poly(cen, ctx.city.coast):                          # úzký pruh u vody mimo pevninu
            continue
        blocks.append({"poly": poly, "area": G.area(poly), "c": cen})
    return blocks


def classify_blocks(ctx, L, blocks, stations, spaces):
    O = ctx.O
    city = ctx.city
    main = [ctx.r11, ctx.r12]
    st_pts = [(s["u"], s["v"]) for s in city.stations]
    cell = C.CELL
    school_cand = {}
    for i, b in enumerate(blocks):
        u, v = b["c"]
        ij = (min(C.NY - 1, max(0, int(v / cell))), min(C.NX - 1, max(0, int(u / cell))))
        did = int(ctx.did[ij])
        b["district"] = next((k for k, x in DID_INDEX.items() if x == did), None)
        b["dq"] = float(ctx.dq[ij])
        b["r"] = math.dist((u, v), O)
        b["d_station"] = min(math.dist((u, v), p) for p in st_pts)
        b["d_main"] = min(G.nearest_on_polyline((u, v), ln)[0] for ln in main)
        if bool(ctx.east_new[ij]):
            use = "new_waterfront"
        elif bool(ctx.old_zone[ij]) and b["district"] == "C-06":
            use = "promenade_retail" if b["dq"] < 110.0 else "old_town_mixed"
        elif b["r"] < 330.0:
            use = "civic_mixed"
        elif b["d_station"] < 170.0:
            use = "transit_mixed"
        elif b["d_main"] < 48.0 and b["r"] < 1150.0:
            use = "retail_main"
        else:
            use = "residential_mid" if b["r"] < 1450.0 else "residential_low"
        b["use"] = use
        if use in ("residential_mid", "residential_low") and 4800.0 <= b["area"] <= 16000.0 and 480.0 <= b["r"] <= 1100.0:
            school_cand.setdefault(b["district"], []).append(i)
    # škola: jeden blok na čtvrt, nejbližší k parku
    park_c = {"C-03": L["park_west"]["c"], "C-04": L["park_north"]["c"], "C-05": L["park_east"]["c"], "C-06": L["park_central"]["c"]}
    for did, idxs in school_cand.items():
        if did not in park_c:
            continue
        k = min(idxs, key=lambda i: math.dist(blocks[i]["c"], park_c[did]))
        blocks[k]["use"] = "school"
    # hotel
    hx, hy = L["hotel"]["c"]
    for b in blocks:
        if G.point_in_poly((hx, hy), b["poly"]):
            b["use"] = "hotel_premium"
    return blocks
