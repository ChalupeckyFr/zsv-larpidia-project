"""Plán hlavního města (F7): vrstvené, editovatelné SVG (A2, 1 : 10 000, 1 jednotka SVG = 1 m) – Inkscape/Illustrator vrstvy, popisky jako textové vrstvy."""
from __future__ import annotations

import math
from types import SimpleNamespace

import numpy as np

import cp_data as C
import cp_geom as G
import raster
from cp_blocks import LANDUSE
from svgkit import FONT, esc

W_M, H_M = C.W_M, C.H_M

USE_FILL = {
    "residential_low": "#ece6d4", "residential_mid": "#e8dcc2", "old_town_mixed": "#ebcdb1", "promenade_retail": "#f2b9a1", "retail_main": "#f1c99c",
    "civic_mixed": "#d9c9de", "transit_mixed": "#e6d3b0", "school": "#cfe0f0", "new_waterfront": "#dcd2ec", "hotel_premium": "#f0a8a0",
}
BUILDING_FILL = {"parliament": "#6b4f7a", "admin": "#7a5c5c", "museum": "#5c6b7a", "church": "#8b6f5a", "market_hall": "#a0793a", "hotel_premium": "#9a5b4a",
                 "school": "#3f78b5", "harbour_office": "#6a6a6a", "ferry_terminal": "#6a6a6a"}
LINE_COL = {"L1": "#2a8a4a", "L2": "#b0307a", "L3": "#1f5fae"}
ROW_STYLE = {"L": (5.0, "#fbf9f3", "#cdc6b4"), "C": (10.0, "#ffffff", "#bdb7a8"), "P": (18.0, "#fbf3e0", "#c8b98f"), "S": (14.0, "#ffffff", "#a9a395"),
             "B": (20.0, "#ffffff", "#a9a395"), "A": (22.0, "#ffffff", "#9d978a"), "R1": (22.0, "#fff6e6", "#9d978a")}


class Plan:
    def __init__(self):
        self.parts: list[str] = []

    def raw(self, s):
        self.parts.append(s)

    def layer(self, id_, label, extra=""):
        self.parts.append(f'<g id="{esc(id_)}" inkscape:groupmode="layer" inkscape:label="{esc(label)}" {extra}>')

    def end(self):
        self.parts.append("</g>")

    @staticmethod
    def d(pts, close=False):
        s = "M" + " L".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
        return s + (" Z" if close else "")

    def poly(self, pts, fill="none", stroke="none", sw=0, extra=""):
        self.parts.append(f'<path d="{self.d(pts, True)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')

    def text(self, u, v, s, size=24, anchor="middle", fill="#25313a", weight="400", halo=True, extra="", rotate=None, italic=False, spacing=0):
        h = f' stroke="#ffffff" stroke-width="{max(2.0, size / 5):.1f}" stroke-linejoin="round" paint-order="stroke"' if halo else ""
        rot = f' transform="rotate({rotate:.1f} {u:.1f} {v:.1f})"' if rotate is not None else ""
        it = ' font-style="italic"' if italic else ""
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        self.parts.append(f'<text x="{u:.1f}" y="{v:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{h}{it}{ls}{rot} {extra}>{esc(s)}</text>')

    def render(self, title, desc):
        head = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="594mm" height="420mm" viewBox="0 0 {int(W_M)} {int(H_M)}">\n<title>{esc(title)}</title>\n<desc>{esc(desc)}</desc>\n'
                '<style>.status-mode [data-st="approved"]{stroke:#2a8a4a!important;stroke-width:3!important}.status-mode [data-st="proposed"]{stroke:#d9741a!important;stroke-width:2!important}'
                '.hl{filter:drop-shadow(0 0 8px #ff2d55)}</style>\n')
        return head + "\n".join(self.parts) + "\n</svg>\n"


class Placer:
    """Jednoduché rozmísťování popisků bez překryvů (metry)."""

    def __init__(self):
        self.boxes = []

    @staticmethod
    def box(u, v, text, size, anchor):
        w, h = 0.52 * size * len(text), size * 1.05
        if anchor == "start":
            return (u, v - h * 0.8, u + w, v + h * 0.25)
        if anchor == "end":
            return (u - w, v - h * 0.8, u, v + h * 0.25)
        return (u - w / 2, v - h * 0.8, u + w / 2, v + h * 0.25)

    def hit(self, b, margin=5.0):
        return any(not (b[2] + margin < o[0] or b[0] - margin > o[2] or b[3] + margin < o[1] or b[1] - margin > o[3]) for o in self.boxes)

    def reserve(self, u, v, r):
        self.boxes.append((u - r, v - r, u + r, v + r))

    def place(self, pl, u, v, text, size=22, gap=14.0, **kw):
        opts = [("start", gap, 0), ("end", -gap, 0), ("middle", 0, -gap - size * 0.4), ("middle", 0, gap + size * 0.9), ("start", gap, -size * 0.9), ("start", gap, size * 1.0),
                ("end", -gap, -size * 0.9), ("end", -gap, size * 1.0)]
        for anchor, du, dv in opts:
            b = self.box(u + du, v + dv, text, size, anchor)
            if not self.hit(b):
                self.boxes.append(b)
                pl.text(u + du, v + dv, text, size=size, anchor=anchor, **kw)
                return True
        return False


def contours(city, interval=5.0, major=25.0):
    z = raster.gauss(city.z.astype(np.float32), 1.5)
    g = SimpleNamespace(x0=0.0, y0=0.0, dx=C.CELL)
    minor, maj = [], []
    for lev in np.arange(interval, float(z.max()) + 0.1, interval):
        for ln in raster.contour_lines(g, z, float(lev)):
            if len(ln) < 4:
                continue
            ln = raster.simplify(ln, 1.6)
            (maj if abs(lev / major - round(lev / major)) < 1e-6 else minor).append((float(lev), ln))
    return minor, maj


def build_svg(ctx, L, graph, blocks, spaces, stations, objs, routes, meta):
    city = ctx.city
    pl = Plan()
    byid = {o["id"]: o for o in objs}
    # ---------------- základ
    pl.layer("bg-sea", "Moře")
    pl.raw(f'<rect x="0" y="0" width="{W_M:.0f}" height="{H_M:.0f}" fill="#d3e6f0"/>')
    pl.end()
    pl.layer("land", "Pevnina")
    pl.poly(city.coast, fill="#f2efe4", stroke="#7d8c93", sw=1.6, extra='id="coast-main"')
    pl.end()
    minor, maj = contours(city)
    pl.layer("contours", "Vrstevnice 5 m (index 25 m)")
    pl.raw('<g fill="none" stroke="#cdb99a" stroke-width="0.7" stroke-linejoin="round">' + "".join(f'<path d="{pl.d(ln)}"/>' for _, ln in minor) + "</g>")
    pl.raw('<g fill="none" stroke="#b39a74" stroke-width="1.3" stroke-linejoin="round">' + "".join(f'<path d="{pl.d(ln)}"/>' for _, ln in maj) + "</g>")
    for lev, ln in maj[::4]:
        mid = ln[len(ln) // 2]
        pl.text(mid[0], mid[1], f"{lev:.0f}", size=13, fill="#8a7550", halo=True)
    pl.end()
    pl.layer("beaches", "Pláže (z atlasu)")
    for ring in city.beaches:
        pl.poly(ring, fill="#ecdcae", stroke="none", extra='opacity="0.9"')
    pl.end()
    pl.layer("green-wedges", "Zelené klíny uvnitř okruhu L3 (návrh)")
    for o in objs:
        if o.get("subtype") == "green_wedge":
            pl.poly(o["poly"], fill="#e3ecd2", stroke="none", extra=f'data-id="{o["id"]}" data-st="proposed"')
    pl.end()
    # ---------------- čtvrtě
    pl.layer("districts", "Čtvrtě C-03 … C-06 (návrh)")
    dfill = {"C-03": "#9bd09b", "C-04": "#e2d680", "C-05": "#e89a82", "C-06": "#9bbbe4"}
    for did, polys in ctx.districts.items():
        for p in polys:
            pl.poly(p, fill=dfill[did], stroke="#a05a4a", sw=1.2, extra=f'data-id="{did}" data-st="proposed" opacity="0.16" stroke-dasharray="14 8"')
    pl.end()
    # ---------------- bloky
    pl.layer("blocks", "Bloková území podle využití (návrh)")
    by_use = {}
    for i, b in enumerate(blocks, 1):
        by_use.setdefault(b["use"], []).append((i, b))
    for use, items in by_use.items():
        pl.raw(f'<g id="blocks-{use}" fill="{USE_FILL[use]}" stroke="#c4b79b" stroke-width="0.6" stroke-linejoin="round">')
        for i, b in items:
            pl.raw(f'<path d="{pl.d(b["poly"], True)}" data-id="CP-BL-{i:04d}" data-st="proposed"/>')
        pl.raw("</g>")
    pl.end()
    # ---------------- veřejné prostory
    pl.layer("spaces", "Parky, náměstí, promenáda (návrh)")
    sp_fill = {"park": "#cfe3bd", "square": "#efe7d5", "promenade": "#f6e6c8", "plaza": "#ebe2cf"}
    for sid, typ, nm, poly in spaces:
        pl.poly(poly, fill=sp_fill[typ], stroke="#aab59a" if typ == "park" else "#cdbf9d", sw=1.0, extra=f'data-id="{sid}" data-st="{byid[sid]["exist_status"]}"')
    for sid, s in stations.items():
        pl.poly(s["plaza"], fill="#efe7d5", stroke="#cdbf9d", sw=0.8, extra=f'data-id="CP-SQ{5 + list(stations).index(sid):02d}" data-st="proposed"')
    pl.end()
    # ---------------- přístav
    pl.layer("harbor", "Přístav C-02 (z atlasu) a molo")
    pl.poly(city.harbor_water, fill="#c3dcea", stroke="none", extra='data-id="C-02" data-st="approved"')
    for mo in city.moles:
        pl.raw(f'<path d="{pl.d(mo["pts"])}" fill="none" stroke="#6d6a62" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
        pl.raw(f'<path d="{pl.d(mo["pts"])}" fill="none" stroke="#b9b4a6" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    pf = byid["CP-PI01"]
    pl.poly(pf["poly"], fill="#9a8f7c", stroke="#5f584c", sw=1.0, extra='data-id="CP-PI01" data-st="proposed"')
    pl.end()
    # ---------------- ulice (obrys + výplň po třídách)
    pl.layer("streets", "Ulice podle tříd (obrys + výplň)")
    for cls in ("L", "C", "P", "S", "B", "A", "R1"):
        es = [e for e in graph.edges if e["cls"] == cls]
        if not es:
            continue
        w, fill, cas = ROW_STYLE[cls]
        by_row = {}
        for e in es:
            by_row.setdefault(e.get("row") or w, []).append(e)
        for row, ee in by_row.items():
            d = " ".join(pl.d(e["pts"]) for e in ee)
            pl.raw(f'<path id="streets-{cls}-cas-{int(row)}" d="{d}" fill="none" stroke="{cas}" stroke-width="{row + 3:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
        for row, ee in by_row.items():
            d = " ".join(pl.d(e["pts"]) for e in ee)
            pl.raw(f'<path id="streets-{cls}-fill-{int(row)}" d="{d}" fill="none" stroke="{fill}" stroke-width="{row:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    pl.end()
    # ---------------- koleje
    pl.layer("rail-surface", "Železnice L1 / L2 – povrch (z atlasu)")
    for r in ctx.rail_lines:
        pl.raw(f'<path d="{pl.d(r["pts"])}" fill="none" stroke="#3a3a3a" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
        pl.raw(f'<path d="{pl.d(r["pts"])}" fill="none" stroke="{LINE_COL[r["line"]]}" stroke-width="3" stroke-dasharray="14 10" stroke-linecap="butt" stroke-linejoin="round"/>')
    pl.end()
    pl.layer("rail-L3", "Metro L3 – podzemí (z atlasu)")
    for r in city.rails:
        if r["line"] == "L3":
            pl.raw(f'<path d="{pl.d(r["pts"])}" fill="none" stroke="{LINE_COL["L3"]}" stroke-width="4" stroke-dasharray="16 10" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>')
    pl.end()
    # ---------------- stanice
    pl.layer("stations", "Stanice (z atlasu) – budovy, nástupiště, vstupy")
    for sid, s in stations.items():
        if s["kind"] == "surface":
            pl.poly(s["platform"], fill="#a8a39a", stroke="#5f5b52", sw=0.8)
            pl.poly(s["building"], fill="#6c5f58", stroke="#3e3631", sw=1.0, extra=f'data-id="{sid}" data-st="proposed"')
        else:
            for en in s["entrances"]:
                pl.poly(en, fill="#6c5f58", stroke="#3e3631", sw=1.0, extra=f'data-id="{sid}" data-st="proposed"')
    for st in city.stations:
        cols = [LINE_COL[l] for l in st["lines"]]
        r0 = 24.0
        pl.raw(f'<g data-id="{st["id"]}" data-st="proposed"><circle cx="{st["u"]:.1f}" cy="{st["v"]:.1f}" r="{r0}" fill="#ffffff" stroke="{cols[0]}" stroke-width="7"/>')
        for k, c in enumerate(cols[1:], 1):
            pl.raw(f'<circle cx="{st["u"]:.1f}" cy="{st["v"]:.1f}" r="{r0 - 6.5 * k:.1f}" fill="none" stroke="{c}" stroke-width="4"/>')
        pl.raw("</g>")
    pl.end()
    # ---------------- klíčové budovy
    pl.layer("buildings-key", "Klíčové budovy (návrh)")
    for o in objs:
        if o["type"] == "building" and o.get("poly"):
            pl.poly(o["poly"], fill=BUILDING_FILL.get(o["subtype"], "#7a6a60"), stroke="#3e3631", sw=1.1, extra=f'data-id="{o["id"]}" data-st="{o["exist_status"]}"')
    pl.end()
    # ---------------- body zájmu
    pl.layer("poi", "Kavárny, půjčovny, obchody (návrh)")
    for o in objs:
        if o["type"] in ("cafe", "rental", "shop"):
            u, v = o["u"], o["v"]
            if o["type"] == "cafe":
                pl.raw(f'<circle cx="{u}" cy="{v}" r="8" fill="#c8782a" stroke="#fff" stroke-width="2.4" data-id="{o["id"]}" data-st="proposed"/>')
            elif o["type"] == "rental":
                pl.raw(f'<rect x="{u - 7}" y="{v - 7}" width="14" height="14" fill="#2b78c2" stroke="#fff" stroke-width="2.4" data-id="{o["id"]}" data-st="proposed"/>')
            else:
                pl.raw(f'<polygon points="{u},{v - 9} {u + 9},{v} {u},{v + 9} {u - 9},{v}" fill="#c2306e" stroke="#fff" stroke-width="2.4" data-id="{o["id"]}" data-st="proposed"/>')
    pl.end()
    # ---------------- bezbariérová trasa
    pl.layer("access-route", "Bezbariérové trasy – kandidáti (sklon ≤ 5 %, návrh)")
    for rt in routes:
        pl.raw(f'<path d="{pl.d(rt["pts"])}" fill="none" stroke="#2a8a4a" stroke-width="5" stroke-dasharray="3 9" stroke-linecap="round" data-id="{rt["id"]}" data-st="proposed"/>')
    pl.end()
    # ---------------- souřadnicová mřížka (po 500 m; popisky v km atlasu)
    pl.layer("grid", "Souřadnicová mřížka 500 m (popisky = km atlasu)")
    g_lines = []
    for u in range(0, int(W_M) + 1, 500):
        g_lines.append(f"M{u},0 L{u},{int(H_M)}")
    for v in range(0, int(H_M) + 1, 500):
        g_lines.append(f"M0,{v} L{int(W_M)},{v}")
    pl.raw(f'<path d="{" ".join(g_lines)}" fill="none" stroke="#6f7f88" stroke-width="0.8" stroke-dasharray="10 14" opacity="0.45"/>')
    for u in range(500, int(W_M), 500):
        pl.text(u + 6, 30, f"x {C.X0_KM + u / 1000:.1f}", size=17, anchor="start", fill="#4d5c64", halo=False)
    for v in range(500, int(H_M), 500):
        pl.text(8, v - 6, f"y {C.Y0_KM + v / 1000:.1f}", size=17, anchor="start", fill="#4d5c64", halo=False)
    pl.end()
    # ---------------- popisky
    def new_placer():
        pr = Placer()
        for o in objs:
            if o["type"] in ("building", "station", "cafe", "rental", "shop", "pier"):
                pr.reserve(o["u"], o["v"], 15)
        return pr

    street_labels = street_label_specs(graph, objs)
    for lang, key in (("cs", "name_cs"), ("en", "name_en"), ("ja", "name_ja")):
        pl.layer(f"labels-{lang}", {"cs": "Popisky – čeština", "en": "Popisky – English", "ja": "Popisky – 日本語"}[lang], extra='style="display:none"' if lang != "cs" else "")
        if lang == "ja":
            for o in objs:
                if o.get("name_ja") and o["type"] in ("building", "harbor"):
                    pl.text(o["u"], o["v"] + 34, o["name_ja"], size=20, fill="#1f2a33", weight="500")
            pl.end()
            continue
        pl_place = new_placer()
        for did, polys in ctx.districts.items():
            big = max(polys, key=G.area)
            c = G.centroid(big)
            pl.text(c[0], c[1] + 28, byid[did]["name_cs" if lang == "cs" else "name_en"], size=74, fill="#6a4f46", weight="700", halo=False, extra='opacity="0.30"', spacing=8)
        for o in objs:
            nm = o.get(key) or o["name_cs"]
            if o["type"] == "building" and o["subtype"] != "school":
                pl_place.place(pl, o["u"], o["v"], nm, size=19, weight="600", fill="#33222e")
            elif o["id"] == "CP-PK01":
                for k, part in enumerate(nm.split(" ", 1)):
                    pl.text(o["u"], o["v"] + 30 + 15 * k, part, size=13, fill="#3e5a3e", weight="600", italic=True)
            elif o["id"] == "CP-SQ01":
                pl.text(o["u"], o["v"] - 146, nm, size=17, fill="#5a4a32", weight="600")
            elif o.get("subtype") == "green_wedge":
                pl.text(o["u"], o["v"], nm, size=30, fill="#6b8a55", weight="600", italic=True, halo=False)
            elif o["type"] == "park" or o["id"] in ("CP-SQ02", "CP-SQ03", "CP-SQ04"):
                pl.text(o["u"], o["v"] + 6, nm, size=22 if o["type"] == "park" else 18, fill="#3e5a3e" if o["type"] == "park" else "#5a4a32", weight="600", italic=o["type"] == "park")
            elif o["type"] == "station":
                pl_place.place(pl, o["u"], o["v"], nm.split("(")[0].strip(), size=26, gap=32.0, weight="700", fill="#1f2a33")
            elif o["type"] == "cafe":
                pl_place.place(pl, o["u"], o["v"], nm, size=13, gap=10.0, fill="#7a4a12")
            elif o["type"] in ("rental", "shop"):
                pl_place.place(pl, o["u"], o["v"], nm, size=13, gap=10.0, fill="#1f4e80" if o["type"] == "rental" else "#7a1f48")
        pl.text(3260, 3880, "Historický přístav" if lang == "cs" else "Old Harbour", size=40, fill="#2f6280", italic=True, halo=False, spacing=4)
        for sp in street_labels:
            nm = sp["name_cs"] if lang == "cs" else sp["name_en"]
            pid = f'sl-{lang}-{sp["id"]}-{sp["tag"]}'
            pl.raw(f'<defs><path id="{pid}" d="{pl.d(sp["pts"])}"/></defs>')
            pl.raw(f'<text font-family="{FONT}" font-size="{sp["size"]}" font-weight="600" fill="#3a3a3a" stroke="#ffffff" stroke-width="{sp["size"] / 5:.1f}" paint-order="stroke" letter-spacing="2" '
                   f'data-id="{sp["id"]}"><textPath href="#{pid}" startOffset="{sp["offset"] * 100:.0f}%" text-anchor="middle">{esc(nm)}</textPath></text>')
        pl.end()
    # ---------------- okraje
    pl.layer("marginalia", "Měřítko, severka, legenda, titulek")
    marginalia(pl, meta)
    pl.end()
    return pl.render("Larpington – podklad plánu hlavního města (návrh)", "Schematický podklad v lokálním metrickém modelu (1 jednotka SVG = 1 m), A2 v měřítku 1 : 10 000. Pracovní návrh (proposed).")


def edge_chains(edges):
    """Souvislé řetězy hran stejného jména (jako polyline); na rozcestí se pokračuje hranou s nejmenším zalomením."""
    adj = {}
    for i, e in enumerate(edges):
        adj.setdefault(e["a"], []).append(i)
        adj.setdefault(e["b"], []).append(i)
    used = set()
    chains = []

    def seg_from(e, node):
        return list(e["pts"]) if e["a"] == node else list(e["pts"])[::-1]

    def direction(p, q):
        L = math.dist(p, q) or 1.0
        return ((q[0] - p[0]) / L, (q[1] - p[1]) / L)

    for i0 in sorted(range(len(edges)), key=lambda i: -edges[i]["length"]):
        if i0 in used:
            continue
        used.add(i0)
        e0 = edges[i0]
        pts, head, tail = list(e0["pts"]), e0["a"], e0["b"]
        for end in (1, -1):
            while True:
                node = tail if end == 1 else head
                cand = [j for j in adj[node] if j not in used]
                if not cand:
                    break
                cur_dir = direction(pts[-2], pts[-1]) if end == 1 else direction(pts[1], pts[0])
                best = max(cand, key=lambda j: sum(a * b for a, b in zip(cur_dir, direction(*seg_from(edges[j], node)[:2]))))
                used.add(best)
                ej = edges[best]
                seg = seg_from(ej, node)
                other = ej["b"] if ej["a"] == node else ej["a"]
                if end == 1:
                    pts = pts + seg[1:]
                    tail = other
                else:
                    pts = seg[::-1][:-1] + pts
                    head = other
        chains.append(pts)
    return chains


def street_label_specs(graph, objs):
    """Pro každé jméno ulice vybere nejdelší souvislé řetězy hran jako osu textu (zleva doprava); text se zmenší, aby se vešel."""
    by = {}
    for e in graph.edges:
        if e.get("name_cs"):
            by.setdefault((e["name_cs"], e.get("name_en", e["name_cs"])), []).append(e)
    specs = []
    sid = {o["name_cs"]: o["id"] for o in objs if o["type"] == "street"}
    for (cs, en), es in by.items():
        if cs.startswith("Přístup"):
            continue
        base = 22 if es[0]["cls"] in ("A", "R1", "B", "S", "P") else 17
        cl = sorted(((G.length(c), c) for c in edge_chains(es)), key=lambda x: -x[0])
        for k, (L, pts) in enumerate(cl[:2]):
            if L < 120.0 or (k == 1 and L < 260.0):
                continue
            if pts[0][0] > pts[-1][0]:
                pts = pts[::-1]
            n = max(len(cs), len(en))
            for off in ((0.5,) if L < 1600.0 else (0.2, 0.5, 0.8)):
                avail = 0.9 * L * 2 * min(off, 1 - off)
                for size in (base, base - 3, base - 6):
                    if 0.55 * size * n + 2 * n <= avail:
                        specs.append({"id": sid.get(cs, "CP-UL??"), "name_cs": cs, "name_en": en, "pts": pts, "size": size, "offset": off, "tag": f"{k}{int(off * 10)}"})
                        break
    return specs


def marginalia(pl, meta):
    # titulek (vlevo nahoře)
    pl.text(110, 150, "Larpington – podklad plánu hlavního města", size=72, anchor="start", weight="700", fill="#2a1f1c", halo=False)
    pl.text(110, 225, "Plán CP-01 · schematický podklad v lokálním metrickém modelu · pracovní návrh (proposed)", size=34, anchor="start", fill="#5a4a46", halo=False)
    pl.text(110, 275, f"List A2 (594 × 420 mm), měřítko 1 : 10 000, 1 jednotka SVG = 1 m · atlas {meta['atlas_version']} · severka nahoře", size=28, anchor="start", fill="#5a4a46", halo=False)
    pl.text(110, 320, "Fiktivní město (simulace). Délky ulic a vzdálenosti plynou z metrického modelu; názvy a polohy jsou návrh.", size=26, anchor="start", fill="#5a4a46", halo=False)
    # severka (vpravo nahoře)
    s = 150
    x, y = W_M - 230, 330
    pl.raw(f'<g id="north-arrow" transform="translate({x},{y})"><polygon points="0,{-s} {s * 0.28},{s * 0.35} 0,{s * 0.15} {-s * 0.28},{s * 0.35}" fill="#25313a" stroke="#fff" stroke-width="4"/>'
           f'<polygon points="0,{-s} {s * 0.28},{s * 0.35} 0,{s * 0.15}" fill="#ffffff" stroke="#25313a" stroke-width="4"/>'
           f'<text x="0" y="{-s - 22}" font-family="{FONT}" font-size="60" font-weight="700" text-anchor="middle" fill="#25313a">S</text></g>')
    # měřítko 0–500 m
    bx, by = 4150.0, 3680.0
    for i in range(5):
        pl.raw(f'<rect x="{bx + i * 100}" y="{by}" width="100" height="14" fill="{"#25313a" if i % 2 == 0 else "#ffffff"}" stroke="#25313a" stroke-width="2"/>')
    for i in range(6):
        pl.text(bx + i * 100, by + 52, f"{i * 100}", size=26, halo=False)
    pl.text(bx + 540, by + 14, "m", size=26, anchor="start", halo=False)
    pl.text(bx, by - 18, "Měřítko 1 : 10 000 (A2) – délky z lokálního metrického modelu", size=24, anchor="start", halo=False)
    # legenda
    lx, ly = 4150.0, 3790.0
    pl.raw(f'<rect x="{lx - 20}" y="{ly - 30}" width="1760" height="400" fill="#ffffff" fill-opacity="0.85" stroke="#9aa6ae" stroke-width="1.5"/>')
    pl.text(lx, ly + 6, "Legenda", size=30, anchor="start", weight="700", halo=False)
    col_w = 440.0
    short = {"old_town_mixed": "Staré město", "promenade_retail": "Přístavní promenáda", "retail_main": "Hlavní třída", "civic_mixed": "Státní čtvrť", "transit_mixed": "Okolí stanice",
             "residential_mid": "Bydlení – střední", "residential_low": "Bydlení – zahrádkové", "school": "Škola", "new_waterfront": "Východní nábřeží"}
    use_items = [(u, USE_FILL[u], short[u]) for u in ("old_town_mixed", "promenade_retail", "retail_main", "civic_mixed", "transit_mixed", "residential_mid", "residential_low", "school", "new_waterfront")]
    for k, (u, col, nm) in enumerate(use_items):
        cx, cy = lx + (k // 5) * col_w, ly + 40 + (k % 5) * 32
        pl.raw(f'<rect x="{cx}" y="{cy - 17}" width="30" height="20" fill="{col}" stroke="#a89c80" stroke-width="1"/>')
        pl.text(cx + 40, cy, nm, size=19, anchor="start", halo=False)
    sym = [("Park", "#cfe3bd", "rect"), ("Zelený klín", "#e3ecd2", "rect"), ("Náměstí / promenáda", "#efe7d5", "rect"), ("Klíčová budova", "#6b4f7a", "rect"), ("Kavárna / půjčovna / obchody", "#c8782a", "circle")]
    for k, (nm, col, shape) in enumerate(sym):
        cx, cy = lx + 2 * col_w + (k // 3) * 420, ly + 40 + (k % 3) * 32
        if shape == "circle":
            pl.raw(f'<circle cx="{cx + 15}" cy="{cy - 7}" r="9" fill="{col}" stroke="#fff" stroke-width="2"/>')
        elif shape == "diamond":
            pl.raw(f'<polygon points="{cx + 15},{cy - 18} {cx + 25},{cy - 8} {cx + 15},{cy + 2} {cx + 5},{cy - 8}" fill="{col}" stroke="#fff" stroke-width="2"/>')
        else:
            pl.raw(f'<rect x="{cx}" y="{cy - 17}" width="30" height="20" fill="{col}" stroke="#7d746a" stroke-width="1"/>')
        pl.text(cx + 40, cy, nm, size=19, anchor="start", halo=False)
    ry = ly + 230
    for k, (nm, col, dash) in enumerate((("L1 Skyline (povrch)", LINE_COL["L1"], "14 10"), ("L2 Heritage Connect (povrch)", LINE_COL["L2"], "14 10"), ("L3 Metro Blue (podzemí)", LINE_COL["L3"], "16 10"))):
        cx = lx + k * 540
        pl.raw(f'<line x1="{cx}" y1="{ry}" x2="{cx + 70}" y2="{ry}" stroke="{col}" stroke-width="4" stroke-dasharray="{dash}"/>')
        pl.text(cx + 82, ry + 6, nm, size=19, anchor="start", halo=False)
    ry += 40
    for k, (nm, col, w) in enumerate((("tepna / silnice", "#9d978a", 8), ("ulice", "#bdb7a8", 4), ("ulička", "#cdc6b4", 2))):
        cx = lx + k * 360
        pl.raw(f'<line x1="{cx}" y1="{ry}" x2="{cx + 70}" y2="{ry}" stroke="{col}" stroke-width="{w + 3}"/><line x1="{cx}" y1="{ry}" x2="{cx + 70}" y2="{ry}" stroke="#ffffff" stroke-width="{w}"/>')
        pl.text(cx + 82, ry + 6, nm, size=19, anchor="start", halo=False)
    pl.raw(f'<line x1="{lx + 1100}" y1="{ry}" x2="{lx + 1170}" y2="{ry}" stroke="#2a8a4a" stroke-width="5" stroke-dasharray="3 9" stroke-linecap="round"/>')
    pl.text(lx + 1182, ry + 6, "bezbariérová trasa (kandidát)", size=19, anchor="start", halo=False)
    pl.text(lx, ry + 52, "Stavy: schváleno = parlament, muzeum, historický přístav C-02; vše ostatní (jména, polohy, využití bloků) je návrh. Sever nahoře, východ vpravo.", size=19, anchor="start", fill="#5a4a46", halo=False)
