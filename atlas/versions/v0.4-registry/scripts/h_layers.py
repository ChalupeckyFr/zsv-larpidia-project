"""SVG vrstvy lidské vrstvy (F3): sídla, silnice, stezky, železnice, přístavy, letiště, POI, popisky bez kolizí.

Použije se i v hlavním atlasu (F5). Souřadnice km, jednotky SVG = m.
"""
from __future__ import annotations

import math

import h_rail as hr
import svgkit
from svgkit import PALETTE as P

INK = "#25313a"
ROAD = {"R1": {"fill": "#f0b84f", "casing": "#8a6a2a", "w": 30, "cw": 44},
        "R2": {"fill": "#ffffff", "casing": "#6f6f6f", "w": 22, "cw": 33},
        "R3": {"fill": "#f7f5ee", "casing": "#9a978e", "w": 13, "cw": 20}}
SETTLE_FILL = {"capital": "#d9b79c", "town": "#dec3a6", "village": "#e2cdb2", "hamlet": "#e4d3bb", "industry": "#bdbdbd", "port_area": "#b4b4b4",
               "old_town": "#d8b497", "resort": "#d4b9d8", "airport": "#cfcfcf"}
POI_STYLE = {
    "viewpoint": ("diamond", "#2c7a52", "vyhlídka"), "lighthouse": ("star", "#2c7a52", "maják"), "spring": ("circle", "#2a8fd0", "pramen / studánka"),
    "hotel_vip": ("square", "#7b4aa8", "prémiový hotel"), "castle": ("triangle", "#7a4a22", "hrad / zámeček"), "ruin": ("diamond", "#9a7a52", "zřícenina"),
    "aquapark": ("circle", "#1fa3c9", "aquapark"), "paragliding_launch": ("triangle", "#ffffff", "paragliding (start)"),
    "paragliding_landing": ("circle", "#ffffff", "paragliding (přistání)"), "beach": ("circle", "#e8d28a", "pláž"),
}


class LabelPlacer:
    def __init__(self, sheet):
        self.sh = sheet
        self.boxes = []

    def _box(self, x, y, text, size, anchor):
        w = 0.54 * size * len(text)
        h = size * 1.05
        if anchor == "start":
            return (x, y - h * 0.8, x + w, y + h * 0.25)
        if anchor == "end":
            return (x - w, y - h * 0.8, x, y + h * 0.25)
        return (x - w / 2, y - h * 0.8, x + w / 2, y + h * 0.25)

    def _hit(self, b, margin=12):
        for o in self.boxes:
            if not (b[2] + margin < o[0] or b[0] - margin > o[2] or b[3] + margin < o[1] or b[1] - margin > o[3]):
                return True
        return False

    def reserve(self, x_km, y_km, r_m=70):
        X, Y = self.sh.X(x_km), self.sh.Y(y_km)
        self.boxes.append((X - r_m, Y - r_m, X + r_m, Y + r_m))

    def place(self, x_km, y_km, text, size=100, weight="400", fill=None, options=None, halo=True, style=""):
        X, Y = self.sh.X(x_km), self.sh.Y(y_km)
        gap = 78 + size * 0.15
        opts = options or [("start", gap, 0), ("end", -gap, 0), ("middle", 0, -gap - size * 0.55), ("middle", 0, gap + size * 0.95),
                           ("start", gap, -size * 0.8), ("start", gap, size * 0.9), ("end", -gap, -size * 0.8), ("end", -gap, size * 0.9)]
        for anchor, dx, dy in opts:
            b = self._box(X + dx, Y + dy, text, size, anchor)
            if not self._hit(b):
                self.boxes.append(b)
                self.sh.text(X + dx, Y + dy, text, size=size, anchor=anchor, weight=weight, fill=fill, halo=halo, units=True, style=style)
                return True
        # nouzově: první varianta
        anchor, dx, dy = opts[0]
        self.sh.text(X + dx, Y + dy, text, size=size, anchor=anchor, weight=weight, fill=fill, halo=halo, units=True, style=style)
        return False


def layer_settlements(sh, settle, pl):
    with sh.layer("settlements", "Sídla a průmysl (půdorysy, návrh)"):
        for s in settle:
            col = SETTLE_FILL.get(s["kind"], "#dcc2a3")
            for r in s["rings"]:
                sh.path(r, fill=col, stroke="#8b6f55", sw=7, extra=f'data-id="{s["id"]}" data-status="proposed"')


def layer_roads(sh, roads, sections):
    with sh.layer("roads", "Silnice (návrh)"):
        order = {"R3": 0, "R2": 1, "R1": 2}
        for r in sorted(roads, key=lambda r: order[r["class"]]):
            st = ROAD[r["class"]]
            segs = sections.get(r["id"]) or [{"section": "surface", "pts": r["pts"]}]
            for sg in segs:
                dash = ' stroke-dasharray="46 34"' if sg["section"] == "tunnel" else ""
                op = ' opacity="0.75"' if sg["section"] == "tunnel" else ""
                sh.raw(f'<path d="{sh.d(sg["pts"], close=False)}" fill="none" stroke="{st["casing"]}" stroke-width="{st["cw"]}" stroke-linecap="round" stroke-linejoin="round"{op}/>')
            for sg in segs:
                dash = ' stroke-dasharray="46 34"' if sg["section"] == "tunnel" else ""
                sh.raw(f'<path id="{r["id"]}" d="{sh.d(sg["pts"], close=False)}" fill="none" stroke="{st["fill"]}" stroke-width="{st["w"]}" stroke-linecap="round" stroke-linejoin="round"{dash}/>')


def layer_trails(sh, trails, cycleways, ski, ferry):
    with sh.layer("trails", "Pěší stezky, cyklotrasy, lyže, trajekt (návrh)"):
        for c in cycleways:
            sh.raw(f'<path id="{c["id"]}" d="{sh.d(c["pts"], close=False)}" fill="none" stroke="#3a9a5a" stroke-width="9" stroke-dasharray="30 20" stroke-linecap="round"/>')
        for t in trails:
            sh.raw(f'<path id="{t["id"]}" d="{sh.d(t["pts"], close=False)}" fill="none" stroke="#8b5a2b" stroke-width="8" stroke-dasharray="10 14" stroke-linecap="round"/>')
        if ski:
            sh.raw(f'<path id="SK-run" d="{sh.d(ski["run"], close=False)}" fill="none" stroke="#ffffff" stroke-width="34" stroke-linecap="round" opacity="0.9"/>')
            sh.raw(f'<path d="{sh.d(ski["run"], close=False)}" fill="none" stroke="#3c78c8" stroke-width="10" stroke-linecap="round"/>')
            sh.raw(f'<path id="SK-lift" d="{sh.d(ski["lift"], close=False)}" fill="none" stroke="#25313a" stroke-width="9" stroke-dasharray="4 26" stroke-linecap="round"/>')
        if ferry:
            sh.raw(f'<path id="FERRY-1" d="{sh.d(ferry, close=False)}" fill="none" stroke="#1b6aa3" stroke-width="12" stroke-dasharray="50 34" stroke-linecap="round"/>')


def layer_ports_airports(sh, ports, airports):
    with sh.layer("ports", "Přístavy a hráze (návrh)"):
        for p in ports:
            g = p["geom"]
            sh.path(g["basin"], fill="#a8cde0", stroke="none", sw=0, extra="opacity=\"0.9\"")
            for line in (g["mole_a"], g["mole_b"]):
                sh.raw(f'<path d="{sh.d(line, close=False)}" fill="none" stroke="#4a4f55" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>')
            if g.get("quay"):
                sh.raw(f'<path d="{sh.d(g["quay"], close=False)}" fill="none" stroke="#6b6f75" stroke-width="16" stroke-linecap="round"/>')
            for pi in p.get("piers", []):
                sh.path(pi["pts"], fill="#6b6f75", stroke="#3f4349", sw=6, extra="")
    with sh.layer("airports", "Letiště (návrh)"):
        for a in airports:
            if a.get("apron"):
                sh.path(a["apron"], fill="#c4c4c4", stroke="#6d6d6d", sw=6)
                sh.path(a["terminal"], fill="#8d8d8d", stroke="#555", sw=6)
                sh.raw(f'<path d="{sh.d(a["taxiway"], close=False)}" fill="none" stroke="#8d8d8d" stroke-width="14"/>')
            sh.path(a["runway"], fill="#6a6a6a", stroke="#2f2f2f", sw=6, extra=f'id="rwy-{a["id"]}"')


def layer_rail(sh, l1, l2, l3, stations):
    c1, c2, c3 = hr.LINE_STYLE["L1"]["color"], hr.LINE_STYLE["L2"]["color"], hr.LINE_STYLE["L3"]["color"]
    with sh.layer("rail-L3", "L3 Metro Blue (podzemní, návrh)"):
        for sg in l3["segments"]:
            dash = {"tunnel": "70 40", "undersea": "36 30"}.get(sg["section"], "")
            sh.raw(f'<path d="{sh.d(sg["pts"], close=False)}" fill="none" stroke="#ffffff" stroke-width="40" opacity="0.85"/>')
            d = f' stroke-dasharray="{dash}"' if dash else ""
            sh.raw(f'<path id="L3-{sg["section"]}" d="{sh.d(sg["pts"], close=False)}" fill="none" stroke="{c3}" stroke-width="24"{d} stroke-linecap="butt"/>')
        if l3["glass"]:
            sh.raw(f'<path id="L3-glass" d="{sh.d(l3["glass"]["pts"], close=False)}" fill="none" stroke="#8fd3ff" stroke-width="40" stroke-linecap="round"/>')
            sh.raw(f'<path d="{sh.d(l3["glass"]["pts"], close=False)}" fill="none" stroke="{c3}" stroke-width="10" stroke-linecap="round"/>')
    with sh.layer("rail-L2", "L2 Heritage Connect (povrchová, návrh)"):
        for b in l2["branches"]:
            sh.raw(f'<path d="{sh.d(b["pts"], close=False)}" fill="none" stroke="#ffffff" stroke-width="40"/>')
            sh.raw(f'<path id="{b["branch"]}" d="{sh.d(b["pts"], close=False)}" fill="none" stroke="{c2}" stroke-width="24" stroke-linecap="round"/>')
            sh.raw(f'<path d="{sh.d(b["pts"], close=False)}" fill="none" stroke="#ffffff" stroke-width="6" stroke-dasharray="26 26"/>')
    with sh.layer("rail-L1", "L1 Skyline Experience (vyhlídková, návrh)"):
        for sg in l1["segments"]:
            sec = sg["section"]
            case = "#222" if sec == "viaduct" else "#ffffff"
            cw = 50 if sec == "viaduct" else 40
            sh.raw(f'<path d="{sh.d(sg["pts"], close=False)}" fill="none" stroke="{case}" stroke-width="{cw}" opacity="{0.9 if sec != "cave" else 0.6}"/>')
            dash = ' stroke-dasharray="60 36"' if sec == "tunnel" else (' stroke-dasharray="14 16"' if sec == "cave" else "")
            w = 30 if sec == "cave" else 24
            sh.raw(f'<path id="L1-{sec}" d="{sh.d(sg["pts"], close=False)}" fill="none" stroke="{c1}" stroke-width="{w}"{dash} stroke-linecap="round"/>')
    with sh.layer("stations", "Stanice (návrh)"):
        for st in stations:
            hub = len(st["lines"]) > 1
            r = 68 if hub else 46
            sh.circle(st["pt"], r, "#ffffff", stroke="#1d2730", sw=18 if hub else 14, extra=f'id="{st["id"]}" data-lines="{",".join(st["lines"])}"')
            if len(st["lines"]) == 3:
                sh.circle(st["pt"], 28, "#1d2730", stroke="none", sw=0)


def draw_poi_glyph(sh, kind, p, size=48):
    shape, color, _ = POI_STYLE[kind]
    stroke = "#1d2730" if color == "#ffffff" else "#ffffff"
    sh.marker(shape, p, size=size, fill=color, stroke=stroke, sw=12)


def layer_poi(sh, pois, extra_points):
    with sh.layer("poi", "Body zájmu (návrh)"):
        for p in pois:
            draw_poi_glyph(sh, p["kind"], (p["x"], p["y"]), 44 if p["kind"] != "spring" else 34)
        for e in extra_points:
            sh.marker(e["shape"], (e["x"], e["y"]), size=e.get("size", 50), fill=e["fill"], stroke="#ffffff", sw=12)
