"""F5: vrstvy hlavního atlasu čtené z uložených výstupů F1–F4 a z registru (bez přepočtů).

Každý prvek má `data-id` (ID z registru) a `data-st` (approved/proposed/needs_decision), takže prohlížeč umí zobrazit záznam a stavy.
Popisky jsou skutečné textové prvky ve vrstvách `labels-cs`, `labels-ja`, `labels-en`.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import canon
import geom
import h_layers as hl
import h_rail as hr
import landcover as lc
import svgkit
from canon import ATLAS
from svgkit import PALETTE as P

CUR = ATLAS / "current"
ST_COL = {"approved": "#2a8a4a", "proposed": "#d9741a", "needs_decision": "#c0392b"}

STATUS_CSS = """
.status-mode .pt[data-st="approved"]{fill:#2a8a4a!important}.status-mode .pt[data-st="proposed"]{fill:#d9741a!important}.status-mode .pt[data-st="needs_decision"]{fill:#c0392b!important}
.status-mode .ln[data-st="approved"]{stroke:#2a8a4a!important}.status-mode .ln[data-st="proposed"]{stroke:#d9741a!important}.status-mode .ln[data-st="needs_decision"]{stroke:#c0392b!important}
.status-mode .pg[data-st="approved"]{fill:#2a8a4a!important;fill-opacity:.55}.status-mode .pg[data-st="proposed"]{fill:#d9741a!important;fill-opacity:.55}
.status-mode #hypsometry,.status-mode #hillshade,.status-mode #landcover{opacity:.25}
"""


def fc(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))["features"]


class Data:
    def __init__(self):
        self.o = canon.load_outline()
        reg = json.loads((CUR / "registry" / "places.json").read_text(encoding="utf-8"))
        self.meta = reg["atlas_meta"]
        self.reg = {o["id"]: o for o in reg["objects"]}
        R, H = CUR / "relief", CUR / "human"
        self.contours = fc(R / "contours.geojson")
        self.hydro = fc(R / "hydrography.geojson")
        self.landcover = fc(R / "landcover.geojson")
        self.coast = fc(R / "coast_classes.geojson")
        self.settle = fc(H / "settlements.geojson")
        self.roads = fc(H / "roads.geojson")
        self.trails = fc(H / "trails_cycleways.geojson")
        self.rail = fc(H / "rail_lines.geojson")
        self.stations = fc(H / "rail_stations.geojson")
        self.pa = fc(H / "ports_airports.geojson")
        self.poi = fc(H / "poi.geojson")
        self.rr = json.loads((R / "relief_report.json").read_text(encoding="utf-8"))
        self.hr = json.loads((H / "human_report.json").read_text(encoding="utf-8"))
        self.fro = json.loads((CUR / "geometry" / "outline_FROZEN.json").read_text(encoding="utf-8"))

    def st(self, oid, key="exist_status"):
        o = self.reg.get(oid)
        v = o.get(key) if o else "proposed"
        return v if v in ST_COL else "proposed"

    def name(self, oid, lang="cs"):
        o = self.reg.get(oid)
        if not o:
            return oid
        np_ = o.get("name_proposed")
        if lang == "en":
            return o.get("name_en") or (np_["en"] if np_ else o["name_cs"])
        if lang == "ja":
            return o.get("name_ja") or (np_["ja"] if np_ else "")
        return (np_["cs"] if np_ else o["name_cs"]).replace(" (pracovní)", "")


def ring(coords):
    return [tuple(c) for c in coords[:-1]] if coords[0] == coords[-1] else [tuple(c) for c in coords]


# ------------------------------------------------------------------ vrstvy
def L_base(sh, D, variant):
    import layers
    main, para = D.o["main"], D.o["para"]
    layers.defs_clip(sh, main, para)
    sh.raw(f"<defs><style>{STATUS_CSS}</style></defs>")
    layers.layer_sea(sh, main, para)
    layers.layer_grid(sh, with_frame=True)
    fill = "#efeadb" if variant == "political" else P["land"]
    layers.layer_land_base(sh, main, para, fill=fill)


def L_rasters(sh, variant):
    import layers
    if variant == "political":
        return
    op_h = {"master": 0.7, "physical": 1.0, "status": 0.4}.get(variant, 0.7)
    layers.layer_raster(sh, "hypsometry", "Hypsometrické tónování (modelové výšky)", "../relief/hypsometry_rgba.png", opacity=op_h)
    layers.layer_raster(sh, "hillshade", "Stínovaný reliéf", "../relief/hillshade_rgba.png", opacity={"physical": 1.0, "master": 0.75, "status": 0.5}.get(variant, 0.75))


def L_landcover(sh, D, opacity=0.38):
    by = {}
    for f in D.landcover:
        by[f["properties"]["class"]] = f["geometry"]["coordinates"]
    names = {v: k for k, v in lc.CLASSES.items()}
    with sh.layer("landcover", "Pokryv krajiny (návrh)", f'clip-path="url(#clip-land)" opacity="{opacity}"'):
        for cname, polys in by.items():
            cid = names[cname]
            d = " ".join(sh.d([tuple(c) for c in poly[0][:-1]]) for poly in polys)
            hatch = ' stroke="#9b7d3c" stroke-width="5"' if cname == "terraces" else ""
            sh.raw(f'<path id="lc-{cname}" d="{d}" fill="{lc.LC_COLORS[cid]}" fill-rule="evenodd"{hatch}/>')


def L_coast_classes(sh, D):
    with sh.layer("coast-classes", "Typy pobřeží: pláže, útesy, skalnaté (návrh)"):
        with sh.group("beaches", 'fill="#f4e8bd" stroke="#d8c58a" stroke-width="5"'):
            for f in D.coast:
                if f["properties"]["class"] == "beach":
                    sh.raw(f'<path class="pg" data-st="proposed" d="{sh.d(ring(f["geometry"]["coordinates"][0]))}"/>')
        with sh.group("rocky-shore", 'fill="none" stroke="#7d7466" stroke-width="12" stroke-linecap="round" opacity="0.8"'):
            for f in D.coast:
                if f["properties"]["class"] == "rocky":
                    sh.raw(f'<path d="{sh.d([tuple(c) for c in f["geometry"]["coordinates"]], close=False)}"/>')
        with sh.group("cliffs", 'fill="none" stroke="#3b3a36" stroke-width="16" stroke-linecap="round"'):
            for f in D.coast:
                if f["properties"]["class"] == "cliff":
                    sh.raw(f'<path d="{sh.d([tuple(c) for c in f["geometry"]["coordinates"]], close=False)}"/>')


def L_contours(sh, D, labels=True):
    with sh.layer("contours", "Vrstevnice po 20 m (index 100 m, návrh)", 'clip-path="url(#clip-land)"'):
        with sh.group("contours-minor", 'fill="none" stroke="#a98458" stroke-width="5.5" stroke-linejoin="round" opacity="0.85"'):
            for f in D.contours:
                if not f["properties"]["index"]:
                    sh.raw(f'<path d="{sh.d([tuple(c) for c in f["geometry"]["coordinates"]], close=False)}"/>')
        with sh.group("contours-index", 'fill="none" stroke="#7b5326" stroke-width="10" stroke-linejoin="round"'):
            for f in D.contours:
                if f["properties"]["index"]:
                    sh.raw(f'<path d="{sh.d([tuple(c) for c in f["geometry"]["coordinates"]], close=False)}"/>')
    if labels:
        with sh.layer("contour-labels", "Výšky indexových vrstevnic"):
            for f in D.contours:
                c = f["geometry"]["coordinates"]
                if f["properties"]["index"] and len(c) > 40:
                    x, y = c[len(c) // 2]
                    sh.text(x, y + 0.03, f"{int(f['properties']['level_m'])}", size=80, anchor="middle", fill="#6b4520")


def L_hydro(sh, D):
    with sh.layer("hydro", "Vodní toky, jezero, vodopád (návrh)"):
        for f in D.hydro:
            p, g = f["properties"], f["geometry"]
            if g["type"] == "LineString":
                w = {"main": 24, "river": 20, "stream": 13}[p["kind"]]
                sh.raw(f'<path class="ln" data-id="{p["id"]}" data-st="{D.st(p["id"])}" id="river-{p["id"]}-{p["part"]}" d="{sh.d([tuple(c) for c in g["coordinates"]], close=False)}" '
                       f'fill="none" stroke="#3b8fc4" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
            elif g["type"] == "Polygon":
                sh.raw(f'<path class="pg" data-id="N-04" data-st="{D.st("N-04")}" d="{sh.d(ring(g["coordinates"][0]))}" fill="#8fc3e0" stroke="#3b8fc4" stroke-width="14"/>')
            else:
                x, y = g["coordinates"]
                sh.marker("diamond", (x, y), size=48, fill="#2c7fb8", stroke="#ffffff", sw=14, extra=f'class="pt" data-id="N-03" data-st="{D.st("N-03")}"')
        dam = D.reg["DAM-N04"]
        sh.marker("square", (dam["x_km"], dam["y_km"]), size=40, fill="#34495e", stroke="#ffffff", sw=12, extra=f'class="pt" data-id="DAM-N04" data-st="{D.st("DAM-N04")}"')


def L_settlements(sh, D, variant):
    with sh.layer("settlements", "Sídla a průmysl (půdorysy, návrh)"):
        for f in D.settle:
            p = f["properties"]
            col = hl.SETTLE_FILL.get(p["kind"], "#dcc2a3")
            if variant == "political":
                col = {"capital": "#e2a98a", "town": "#e8bf9f", "industry": "#c9c9c9", "village": "#ecd2b8"}.get(p["kind"], col)
            sh.path(ring(f["geometry"]["coordinates"][0]), fill=col, stroke="#8b6f55", sw=7, extra=f'class="pg" data-id="{p["id"]}" data-st="{D.st(p["id"])}"')


def L_trails(sh, D):
    with sh.layer("cycleways", "Cyklotrasy (návrh)"):
        for f in D.trails:
            p = f["properties"]
            if p["id"].startswith("CY"):
                sh.raw(f'<path class="ln" data-id="{p["id"]}" data-st="proposed" d="{sh.d([tuple(c) for c in f["geometry"]["coordinates"]], close=False)}" fill="none" stroke="#3a9a5a" stroke-width="9" stroke-dasharray="30 20" stroke-linecap="round"/>')
    with sh.layer("trails", "Pěší stezky, lyžování, trajekt (návrh)"):
        for f in D.trails:
            p, c = f["properties"], [tuple(q) for q in f["geometry"]["coordinates"]]
            if p["id"].startswith("TR"):
                sh.raw(f'<path class="ln" data-id="{p["id"]}" data-st="proposed" d="{sh.d(c, close=False)}" fill="none" stroke="#8b5a2b" stroke-width="8" stroke-dasharray="10 14" stroke-linecap="round"/>')
            elif p["id"] == "SK-01":
                sh.raw(f'<path id="SK-01" d="{sh.d(c, close=False)}" fill="none" stroke="#ffffff" stroke-width="34" stroke-linecap="round" opacity="0.9"/>')
                sh.raw(f'<path class="ln" data-id="SK-01" data-st="proposed" d="{sh.d(c, close=False)}" fill="none" stroke="#3c78c8" stroke-width="10" stroke-linecap="round"/>')
            elif p["id"] == "SK-02":
                sh.raw(f'<path class="ln" data-id="SK-02" data-st="proposed" d="{sh.d(c, close=False)}" fill="none" stroke="#25313a" stroke-width="9" stroke-dasharray="4 26" stroke-linecap="round"/>')
            elif p["id"] == "FERRY-1":
                sh.raw(f'<path class="ln" data-id="FERRY-1" data-st="proposed" d="{sh.d(c, close=False)}" fill="none" stroke="#1b6aa3" stroke-width="12" stroke-dasharray="50 34" stroke-linecap="round"/>')


def L_roads(sh, D, classes=("R1", "R2", "R3")):
    by = {}
    for f in D.roads:
        by.setdefault(f["properties"]["id"], []).append(f)
    order = {"R3": 0, "R2": 1, "R1": 2}
    with sh.layer("roads", "Silnice (návrh)"):
        for rid, feats in sorted(by.items(), key=lambda kv: order[kv[1][0]["properties"]["class"]]):
            cls = feats[0]["properties"]["class"]
            if cls not in classes:
                continue
            st = hl.ROAD[cls]
            for f in feats:
                tun = f["properties"]["section"] == "tunnel"
                sh.raw(f'<path d="{sh.d([tuple(c) for c in f["geometry"]["coordinates"]], close=False)}" fill="none" stroke="{st["casing"]}" stroke-width="{st["cw"]}" stroke-linecap="round" stroke-linejoin="round"{" opacity=\"0.75\"" if tun else ""}/>')
            for f in feats:
                tun = f["properties"]["section"] == "tunnel"
                dash = ' stroke-dasharray="46 34"' if tun else ""
                sh.raw(f'<path class="ln" data-id="{rid}" data-st="{D.st(rid)}" d="{sh.d([tuple(c) for c in f["geometry"]["coordinates"]], close=False)}" fill="none" stroke="{st["fill"]}" stroke-width="{st["w"]}" stroke-linecap="round" stroke-linejoin="round"{dash}/>')


def L_rail(sh, D):
    cols = {k: v["color"] for k, v in hr.LINE_STYLE.items()}
    for ln in ("L3", "L2", "L1"):
        feats = [f for f in D.rail if f["properties"]["line"] == ln]
        with sh.layer(f"rail-{ln}", f"{ln} {hr.LINE_STYLE[ln]['name']} (návrh)"):
            for f in feats:
                p = f["properties"]
                pts = [tuple(c) for c in f["geometry"]["coordinates"]]
                sec = p["section"]
                if sec == "glass_gallery":
                    sh.raw(f'<path d="{sh.d(pts, close=False)}" fill="none" stroke="#8fd3ff" stroke-width="40" stroke-linecap="round"/>')
                    sh.raw(f'<path class="ln" data-id="L3" data-st="{D.st("L3")}" d="{sh.d(pts, close=False)}" fill="none" stroke="{cols["L3"]}" stroke-width="10" stroke-linecap="round"/>')
                    continue
                case = "#222" if sec == "viaduct" else "#ffffff"
                cw = 50 if sec == "viaduct" else 40
                sh.raw(f'<path d="{sh.d(pts, close=False)}" fill="none" stroke="{case}" stroke-width="{cw}" opacity="0.88"/>')
                dash = {"tunnel": ' stroke-dasharray="70 40"', "undersea": ' stroke-dasharray="36 30"', "cave": ' stroke-dasharray="14 16"'}.get(sec, "")
                if ln == "L1" and sec == "tunnel":
                    dash = ' stroke-dasharray="60 36"'
                w = 30 if sec == "cave" else 24
                sh.raw(f'<path class="ln" data-id="{ln}" data-st="{D.st(ln)}" d="{sh.d(pts, close=False)}" fill="none" stroke="{cols[ln]}" stroke-width="{w}"{dash} stroke-linecap="round" stroke-linejoin="round"/>')
                if ln == "L2":
                    sh.raw(f'<path d="{sh.d(pts, close=False)}" fill="none" stroke="#ffffff" stroke-width="6" stroke-dasharray="26 26"/>')
    with sh.layer("stations", "Stanice (návrh)"):
        for f in D.stations:
            p = f["properties"]
            x, y = f["geometry"]["coordinates"]
            hub = len(p["lines"]) > 1
            sh.circle((x, y), 68 if hub else 46, "#ffffff", stroke="#1d2730", sw=18 if hub else 14, extra=f'class="pt" data-id="{p["id"]}" data-st="{D.st(p["id"])}" data-lines="{",".join(p["lines"])}"')
            if len(p["lines"]) == 3:
                sh.circle((x, y), 28, "#1d2730", stroke="none", sw=0)


def L_ports_airports(sh, D):
    with sh.layer("ports", "Přístavy a hráze (návrh)"):
        for f in D.pa:
            p, g = f["properties"], f["geometry"]
            part = p.get("part") or p.get("kind")
            if p.get("kind") in ("fishing_port", "marina", "historic_harbor", "cargo_port"):
                continue
            if part == "basin":
                sh.path(ring(g["coordinates"][0]), fill="#a8cde0", stroke="none", sw=0, extra='opacity="0.9"')
        for f in D.pa:
            p, g = f["properties"], f["geometry"]
            if p.get("kind") == "breakwater":
                sh.raw(f'<path d="{sh.d([tuple(c) for c in g["coordinates"]], close=False)}" fill="none" stroke="#4a4f55" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>')
            elif p.get("kind") == "pier":
                sh.path(ring(g["coordinates"][0]), fill="#6b6f75", stroke="#3f4349", sw=6)
    with sh.layer("airports", "Letiště (návrh)"):
        for f in D.pa:
            p, g = f["properties"], f["geometry"]
            if g["type"] != "Polygon" or p["id"] not in ("A-01", "A-02"):
                continue
            part = p.get("part")
            if part == "runway":
                sh.path(ring(g["coordinates"][0]), fill="#6a6a6a", stroke="#2f2f2f", sw=6, extra=f'class="pg" data-id="{p["id"]}" data-st="{D.st(p["id"])}"')
            elif part == "apron":
                sh.path(ring(g["coordinates"][0]), fill="#c4c4c4", stroke="#6d6d6d", sw=6)
            elif part == "terminal":
                sh.path(ring(g["coordinates"][0]), fill="#8d8d8d", stroke="#555", sw=6)


def L_poi(sh, D):
    with sh.layer("poi", "Body zájmu (návrh)"):
        for f in D.poi:
            p, (x, y) = f["properties"], f["geometry"]["coordinates"]
            shape, color, _ = hl.POI_STYLE[p["kind"]]
            stroke = "#1d2730" if color == "#ffffff" else "#ffffff"
            size = 34 if p["kind"] == "spring" else 44
            sh.marker(shape, (x, y), size=size, fill=color, stroke=stroke, sw=12, extra=f'class="pt" data-id="{p["id"]}" data-st="{D.st(p["id"])}"')


def L_peaks(sh, D):
    with sh.layer("peaks", "Vrcholy a přírodní body (návrh)"):
        for k in ("M-01", "M-02", "M-03"):
            o = D.reg[k]
            sh.marker("triangle", (o["x_km"], o["y_km"]), size=64, fill=P["peak"], stroke="#ffffff", sw=14, extra=f'class="pt" data-id="{k}" data-st="{D.st(k)}"')
        for k in ("N-01", "N-02"):
            o = D.reg[k]
            sh.marker("circle", (o["x_km"], o["y_km"]), size=52, fill=P["nature"], stroke="#ffffff", sw=14, extra=f'class="pt" data-id="{k}" data-st="{D.st(k)}"')
        for k in ("C-01",):
            o = D.reg[k]
            sh.marker("star", (o["x_km"], o["y_km"]), size=70, fill=P["capital"], stroke="#ffffff", sw=14, extra=f'class="pt" data-id="{k}" data-st="{D.st(k)}"')
        o = D.reg["I-02"]
        sh.marker("square", (o["x_km"], o["y_km"]), size=52, fill=P["industry"], stroke="#ffffff", sw=14, extra=f'class="pt" data-id="I-02" data-st="{D.st("I-02")}"')
        o = D.reg["P-01"]
        sh.marker("diamond", (o["x_km"], o["y_km"]), size=48, fill=P["rail_link"], stroke="#ffffff", sw=14, extra=f'class="pt" data-id="P-01" data-st="{D.st("P-01")}"')


# ------------------------------------------------------------------ popisky
def label_specs(D):
    """Seznam popisků: dict(id, x, y, cs, en, ja, size, weight, fill, opts, kind)."""
    L = []

    def add(**k):
        k.setdefault("weight", "400")
        k.setdefault("fill", "#1d2730")
        k.setdefault("opts", None)
        k.setdefault("style", "")
        L.append(k)

    # sídla
    seen = {}
    for f in D.settle:
        p = f["properties"]
        if p["kind"] in ("hamlet", "port_area"):
            continue
        r = ring(f["geometry"]["coordinates"][0])
        if p["id"] not in seen or geom.area(r) > seen[p["id"]][0]:
            seen[p["id"]] = (geom.area(r), r, p)
    size = {"capital": 205, "town": 150, "industry": 128, "village": 112, "old_town": 104, "resort": 96}
    for sid, (a, r, p) in seen.items():
        cx, cy = geom.centroid(r)
        o = D.reg.get(sid, {})
        add(id=sid, x=cx, y=cy, cs=D.name(sid, "cs"), en=D.name(sid, "en"), ja=D.name(sid, "ja") if sid in D.reg and D.reg[sid].get("name_ja") else "", size=size.get(p["kind"], 100),
            weight="700", fill="#2a1d12", prio=1 if p["kind"] in ("capital", "town") else 3, center=True)
    # letiště, přístavy
    for aid, nm in (("A-01", None), ("A-02", None)):
        o = D.reg[aid]
        add(id=aid, x=o["x_km"], y=o["y_km"], cs=f"{aid} {D.name(aid, 'cs')}", en=f"{aid} {D.name(aid, 'en')}", ja=D.name(aid, "ja"), size=100, weight="600", prio=4,
            opts=[("middle", 0, -270), ("middle", 0, 340), ("start", 140, 0)])
    for pid in ("C-02", "I-03", "H-01", "H-02"):
        o = D.reg[pid]
        add(id=pid, x=o["x_km"], y=o["y_km"], cs=f"{pid} {D.name(pid, 'cs')}", en=f"{pid} {D.name(pid, 'en')}", ja=D.name(pid, "ja"), size=96, weight="600", fill="#1b5f8c", prio=4,
            opts=[("middle", 0, 540), ("end", -180, 540), ("start", 180, 540), ("middle", 0, -420)])
    # vrcholy a příroda
    for k in ("M-01", "M-02", "M-03"):
        o = D.reg[k]
        z = o["elev_m_model"]
        add(id=k, x=o["x_km"], y=o["y_km"], cs=f"{D.name(k, 'cs')} {z:.0f} m", en=f"{D.name(k, 'en')} {z:.0f} m", ja=f"{D.name(k, 'ja')} {z:.0f} m", size=92, weight="700", fill="#5a3412", prio=2)
    for k in ("N-01", "N-02", "N-03", "N-04"):
        o = D.reg[k]
        add(id=k, x=o["x_km"], y=o["y_km"], cs=D.name(k, "cs"), en=D.name(k, "en"), ja=D.name(k, "ja"), size=92, weight="600", fill="#1f5f3f" if k in ("N-01", "N-02") else "#1b5f8c", prio=3)
    o = D.reg["I-02"]
    add(id="I-02", x=o["x_km"], y=o["y_km"], cs="I-02 Závod na řasy", en="I-02 Seaweed Plant", ja=D.name("I-02", "ja"), size=92, weight="600", fill="#3d3d3d", prio=4,
        opts=[("middle", 0, 330), ("start", 140, 0), ("end", -140, 0)])
    # čtvrti
    for k in ("C-03", "C-04", "C-05", "C-06"):
        o = D.reg[k]
        nm = o["name_cs"].replace(" čtvrť", "")
        add(id=k, x=o["x_km"], y=o["y_km"], cs=nm, en=nm, ja="", size=84, weight="600", fill="#6b2a1e", prio=6, opts=[("middle", 0, -90), ("middle", 0, 140)])
    # stanice (uzly a konečné)
    for f in D.stations:
        p = f["properties"]
        if len(p["lines"]) > 1 or p["id"] in ("ST-L1-05", "ST-L1-03", "ST-L3-07", "ST-L3-06"):
            nm = p["name_cs"].split("(")[0].strip()
            add(id=p["id"], x=f["geometry"]["coordinates"][0], y=f["geometry"]["coordinates"][1], cs=nm, en=nm, ja="", size=78, weight="600", prio=5)
    # POI
    for f in D.poi:
        p = f["properties"]
        if p["kind"] in ("viewpoint", "lighthouse", "hotel_vip", "castle", "ruin", "aquapark", "paragliding_launch"):
            add(id=p["id"], x=f["geometry"]["coordinates"][0], y=f["geometry"]["coordinates"][1], cs=p["id"], en=p["id"], ja="", size=70, prio=7)
    # zátoky, mysy
    for bid in ("BAY-N1", "BAY-N2", "BAY-S", "BAY-E", "CAPE-W", "CAPE-N", "PEN-SE"):
        o = D.reg[bid]
        add(id=bid, x=o["x_km"], y=o["y_km"], cs=D.name(bid, "cs"), en=D.name(bid, "en"), ja=D.name(bid, "ja"), size=92, weight="400", fill="#2f6f93", style='font-style="italic"', prio=8,
            opts=[("middle", 0, -330), ("middle", 0, 420), ("start", 180, 0), ("end", -180, 0)] if bid.startswith("BAY-N") else [("middle", 0, 440), ("start", 180, 0), ("end", -180, 0), ("middle", 0, -330)])
    return L


def draw_labels(sh, D, specs, langs=("cs", "ja", "en"), variant="master"):
    """Rozmístí popisky bez kolizí podle prvního jazyka (cs) a vykreslí je do tří vrstev."""
    lp = hl.LabelPlacer(sh)
    for f in D.stations:
        lp.reserve(*f["geometry"]["coordinates"], r_m=70)
    for f in D.poi:
        lp.reserve(*f["geometry"]["coordinates"], r_m=48)
    for k in ("M-01", "M-02", "M-03", "N-01", "N-02", "N-03", "N-04", "C-01"):
        lp.reserve(D.reg[k]["x_km"], D.reg[k]["y_km"], r_m=70)
    chosen = []
    for sp in sorted(specs, key=lambda s: s.get("prio", 9)):
        X, Y = sh.X(sp["x"]), sh.Y(sp["y"])
        size = sp["size"]
        gap = 78 + size * 0.15
        opts = sp["opts"]
        if sp.get("center"):
            opts = [("middle", 0, -size * 0.2), ("middle", 0, -(size + 60)), ("middle", 0, size * 1.1 + 60), ("start", 120, 0), ("end", -120, 0)]
        if opts is None:
            opts = [("start", gap, 0), ("end", -gap, 0), ("middle", 0, -gap - size * 0.55), ("middle", 0, gap + size * 0.95), ("start", gap, -size * 0.8), ("start", gap, size * 0.9), ("end", -gap, -size * 0.8), ("end", -gap, size * 0.9)]
        placed = None
        for anchor, dx, dy in opts:
            b = lp._box(X + dx, Y + dy, sp["cs"], size, anchor)
            if not lp._hit(b):
                lp.boxes.append(b)
                placed = (anchor, dx, dy)
                break
        if placed is None:
            continue                     # nevešlo se → vynechat (v prohlížeči jde dohledat v registru)
        chosen.append((sp, placed))
    for lang in langs:
        with sh.layer(f"labels-{lang}", f"Popisky ({lang})", 'display="inline"' if lang == "cs" else 'display="none"'):
            for sp, (anchor, dx, dy) in chosen:
                txt = sp[lang]
                if not txt:
                    continue
                sh.text(sh.X(sp["x"]) + dx, sh.Y(sp["y"]) + dy, txt, size=sp["size"], anchor=anchor, weight=sp["weight"], fill=sp["fill"], units=True, style=sp.get("style", ""),
                        extra=f'data-id="{sp["id"]}"')
    return len(chosen), len(specs)
