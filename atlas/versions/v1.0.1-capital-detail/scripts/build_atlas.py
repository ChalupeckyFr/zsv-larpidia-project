"""F5: hlavní atlas – vrstvené SVG (master, fyzická, politická, stavy), schéma železnic a interaktivní prohlížeč.

Spuštění:  python atlas/scripts/build_atlas.py
Výstup:    atlas/current/svg/larpidia_atlas_*.svg (+ _embedded), rail_scheme.svg, atlas/current/viewer/atlas.html
Čte jen uložené výstupy F1–F4 a registr; nic nepřepočítává. VŠE JE PRACOVNÍ NÁVRH (proposed).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import atlas_svg as A
import canon
import geom
import h_layers as hl
import h_rail as hr
import svgkit
from canon import ATLAS
from svgkit import PALETTE as P

CUR = ATLAS / "current"
SVGDIR = CUR / "svg"
VIEW = CUR / "viewer"

TITLES = {
    "master": ("LARPIDIE a PARALAND — atlas", "hlavní mapa: reliéf, příroda, sídla, doprava, body zájmu"),
    "physical": ("LARPIDIE a PARALAND — fyzická mapa", "reliéf, vrstevnice, vody, pobřeží a vrcholy"),
    "political": ("LARPIDIE a PARALAND — politická mapa", "sídla, hlavní město, doprava, přístavy a letiště"),
    "status": ("LARPIDIE a PARALAND — kánon × návrh", "zeleně = schválená existence, oranžově = návrh, červeně = otevřené rozhodnutí"),
}


# ------------------------------------------------------------------ legenda a okraje
def legend_panel(sh, x, y, title, items, w=5000, row=290):
    h = 330 + row * len(items) + 90
    sh.rect_u(x - 180, y - 320, w, h, fill="#ffffffe3", stroke=P["ink_soft"], sw=8, rx=40)
    sh.text(x, y, title, size=165, weight="700", units=True, halo=False)
    yy = y + 330
    for it in items:
        kind = it[0]
        if kind == "swatch":
            sh.rect_u(x, yy - 150, 280, 190, fill=it[1], stroke=P["ink_soft"], sw=6)
            label = it[2]
        elif kind == "line":
            d = f' stroke-dasharray="{it[4]}"' if len(it) > 4 and it[4] else ""
            sh.raw(f'<line x1="{x}" y1="{yy - 50}" x2="{x + 280}" y2="{yy - 50}" stroke="{it[1]}" stroke-width="{it[3]}"{d} stroke-linecap="round"/>')
            label = it[2]
        elif kind == "marker":
            sh.marker(it[3], (sh.x0 + (x + 140) / 1000, sh.y0 + (yy - 45) / 1000), size=46, fill=it[1], stroke="#ffffff", sw=12)
            label = it[2]
        elif kind == "station":
            sh.circle((sh.x0 + (x + 140) / 1000, sh.y0 + (yy - 45) / 1000), it[1], "#ffffff", stroke="#1d2730", sw=16)
            label = it[2]
        else:
            label = it[1]
        sh.text(x + 350, yy, label, size=112, units=True, halo=False)
        yy += row


def marginalia(sh, D, variant):
    title, sub = TITLES[variant]
    with sh.layer("marginalia", "Titul, legenda, měřítko, stavy"):
        sh.text(500, 560, title, size=330, weight="700", units=True, halo=False)
        sh.text(500, 900, f"{sub} · atlas {canon.ATLAS_VERSION} · NÁVRH (proposed)", size=170, units=True, halo=False, fill=P["proposed"], weight="600")
        sh.text(500, 1170, "Fiktivní stát (školní projekt ZSV). Polohy, výšky a trasy jsou pracovní návrh; schválená je jen existence prvků podle World Bible.", size=122, units=True, halo=False, fill=P["ink_soft"])
        sh.text(500, 1360, "Autoři: F. Chalupecký, O. Kynčl, M. Klimeček, Š. Žemlička · Larpidia Creative Studio (AI-asistovaný návrh). Bez skutečných družicových dat.", size=108, units=True, halo=False, fill=P["ink_soft"])
        svgkit.nice_scale_bar(sh, 11500, 19250, km=5.0)
        sh.text(11500, 19820, "Měřítko 1 : 50 000 při tisku na A2 (594 × 420 mm); 1 jednotka SVG = 1 m; sever nahoře", size=104, units=True, halo=False, fill=P["ink_soft"])
        svgkit.north_arrow(sh, 28500, 1800)
        sh.text(500, 20280, f"Rámec 24 × 16 km (oranžově, X/Y v %) · pseudo-souřadnice 33,9 N / 137,6 E jsou HYPOTETICKÉ · obrys: varianta B (SHA {D.fro['coast_sha256'][:8]}…)", size=100, units=True, halo=False, fill=P["ink_soft"])
        # legenda dopravy a sídel (NE)
        lx = 24550
        items = []
        if variant in ("master", "political", "status"):
            items += [("line", hr.LINE_STYLE["L1"]["color"], "L1 Skyline Experience", 24), ("line", hr.LINE_STYLE["L2"]["color"], "L2 Heritage Connect", 24),
                      ("line", hr.LINE_STYLE["L3"]["color"], "L3 Metro Blue (podzemní)", 24, "70 40"), ("line", "#f0b84f", "okružní silnice R1", 30),
                      ("line", "#ffffff", "hlavní silnice", 22)]
            if variant != "political":
                items += [("line", "#3a9a5a", "cyklotrasa", 9, "30 20"), ("line", "#8b5a2b", "pěší stezka", 8, "10 14")]
            items += [("station", 60, "stanice (velká = přestup)"), ("swatch", hl.SETTLE_FILL["town"], "sídla (modelový půdorys)")]
        if variant in ("master", "physical"):
            items += [("marker", P["peak"], "vrchol (výška modelová)", "triangle"), ("line", "#3b8fc4", "tok, jezero", 20)]
        if variant == "status":
            items += [("swatch", A.ST_COL["approved"], "approved – schválená existence"), ("swatch", A.ST_COL["proposed"], "proposed – pracovní návrh"), ("swatch", A.ST_COL["needs_decision"], "needs_decision – otevřené")]
        legend_panel(sh, lx, 2600, "Legenda", items, w=5000)
        if variant in ("master", "physical"):
            rel = [("swatch", "#e4e6ca", "nížina 0–20 m"), ("swatch", "#d6dab4", "20–80 m"), ("swatch", "#d0c8a0", "80–200 m"), ("swatch", "#c6b488", "200–350 m"),
                   ("swatch", "#b8a078", "350–560 m"), ("line", "#a98458", "vrstevnice 20 m", 6), ("line", "#7b5326", "indexová 100 m", 10), ("line", "#3b3a36", "útesové pobřeží", 16),
                   ("swatch", "#f4e8bd", "písčitá pláž")]
            legend_panel(sh, 500, 15250 - 290 * len(rel) + 800, "Reliéf a příroda", rel, w=4600)


def big_labels(sh, D, variant):
    main, para = D.o["main"], D.o["para"]
    cx, cy = geom.centroid(main)
    with sh.layer("labels-areas", "Názvy ostrovů a moře"):
        sh.raw(f'<text x="{sh.X(cx - 1.0)}" y="{sh.Y(cy + 0.9)}" font-family="{svgkit.FONT}" font-size="560" font-weight="700" letter-spacing="180" text-anchor="middle" '
               f'fill="#25313a" fill-opacity="0.22" transform="rotate(-6 {sh.X(cx - 1.0)} {sh.Y(cy + 0.9)})">LARPIDIE</text>')
        pcx, pcy = geom.centroid(para)
        sh.raw(f'<text x="{sh.X(pcx - 3.2)}" y="{sh.Y(pcy + 1.2)}" font-family="{svgkit.FONT}" font-size="330" font-weight="700" letter-spacing="90" text-anchor="end" fill="#25313a" fill-opacity="0.35">PARALAND</text>')
        sh.raw(f'<text x="{sh.X(7.0)}" y="{sh.Y(17.9)}" font-family="{svgkit.FONT}" font-size="400" font-style="italic" letter-spacing="220" text-anchor="middle" fill="#3f6f8c" fill-opacity="0.55">TICHÝ OCEÁN</text>')
        d = D.reg["STRAIT"] if "STRAIT" in D.reg else None
        sh.text(21.2, 15.9, "průliv 1,5 km", size=95, anchor="middle", fill="#2f6f93", style='font-style="italic"')


# ------------------------------------------------------------------ složení variant
def compose(D, variant):
    sh = svgkit.Sheet()
    A.L_base(sh, D, variant)
    A.L_rasters(sh, variant)
    if variant == "master":
        A.L_landcover(sh, D, 0.34)
    if variant in ("master", "physical"):
        A.L_coast_classes(sh, D)
        A.L_contours(sh, D, labels=True)
    import layers
    layers.layer_coast_line(sh, D.o["main"], D.o["para"])
    A.L_hydro(sh, D)
    A.L_settlements(sh, D, variant)
    if variant in ("master", "status"):
        A.L_trails(sh, D)
    if variant == "political":
        A.L_roads(sh, D, classes=("R1", "R2"))
    elif variant in ("master", "status"):
        A.L_roads(sh, D)
    if variant in ("master", "political", "status"):
        A.L_rail(sh, D)
    A.L_ports_airports(sh, D)
    if variant in ("master", "status"):
        A.L_poi(sh, D)
    A.L_peaks(sh, D)
    specs = A.label_specs(D)
    if variant == "physical":
        keep = {"M-01", "M-02", "M-03", "N-01", "N-02", "N-03", "N-04", "BAY-N1", "BAY-N2", "BAY-S", "BAY-E", "CAPE-W", "CAPE-N", "PEN-SE", "C-01", "T-01", "T-02", "T-03", "T-04", "T-05", "T-06", "C-02", "I-03", "H-01", "H-02"}
        specs = [s for s in specs if s["id"] in keep]
    placed, total = A.draw_labels(sh, D, specs, variant=variant)
    big_labels(sh, D, variant)
    marginalia(sh, D, variant)
    title, sub = TITLES[variant]
    svg = sh.render(f"{title} (návrh)", f"{sub}. Pracovní návrh. 1 jednotka = 1 m; A2 = 1:50 000.", root_class="status-mode" if variant == "status" else "")
    return svg, (placed, total)


# ------------------------------------------------------------------ schéma železnic (netopografické)
def rail_scheme(D):
    # schematické souřadnice (mřížka 120 px); sever nahoře, topologie jako ve skutečnosti
    U = 104
    ox, oy = 150, 150
    S = lambda p: (ox + p[0] * U, oy + p[1] * U)
    hubW, hubN, hubE, hubS = (4, 6), (6, 4), (8, 6), (6, 8)
    ring = [(5, 4), (7, 4), (8, 5), (8, 7), (7, 8), (5, 8), (4, 7), (4, 5)]
    c = {k: v["color"] for k, v in hr.LINE_STYLE.items()}
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<svg xmlns="http://www.w3.org/2000/svg" width="1900" height="1330" viewBox="0 0 1900 1330" font-family="Segoe UI, Noto Sans, Arial, sans-serif">',
           '<title>Schéma železnic Larpidie a Paralandu (návrh)</title>',
           '<rect width="1900" height="1330" fill="#f7f5ee"/>',
           '<text x="60" y="64" font-size="40" font-weight="700" fill="#25313a">Schéma železnic: L1 · L2 · L3</text>',
           '<text x="60" y="100" font-size="21" fill="#b4541b" font-weight="600">NÁVRH (proposed) · atlas v0.5 · schéma není v měřítku; role linek jsou schváleny, vedení a stanice jsou návrh</text>']
    def poly(pts, col, w=14, dash="", cap="round"):
        d = " ".join(f"{S(p)[0]:.0f},{S(p)[1]:.0f}" for p in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="{cap}"{da}/>'
    # L3 okruh (osmiúhelník) + větev
    ring_pts = ring + [ring[0]]
    out.append(poly(ring_pts, c["L3"], 16, "30 12"))
    out.append(poly([hubE, (9.5, 6), (11, 6)], c["L3"], 16, "30 12"))
    out.append(poly([(11, 6), (14.4, 6)], "#8fd3ff", 22))
    out.append(poly([(11, 6), (14.4, 6)], c["L3"], 7, "14 10"))
    # L2: oblouk W–N–E (nad okruhem), větve
    out.append(poly([(4, 5.6), (5, 4.6), (6, 4.6), (7, 4.6), (8, 5.6)], c["L2"], 14))
    out.append(poly([hubW, (2.6, 7.4)], c["L2"], 14))                                  # T-02
    out.append(poly([hubN, (6, 2.8), (6, 1.4), (6, 0.2)], c["L2"], 14))               # Praha – J1 – Aokawa
    out.append(poly([(6, 0.2), (3.2, 0.2)], c["L2"], 14))                             # Ōru Maito
    out.append(poly([(6, 0.2), (9.2, 0.2)], c["L2"], 14))                             # Hoshimachi
    out.append(poly([(6, 1.4), (7.6, 1.4)], c["L2"], 14))                             # letiště
    out.append(poly([hubE, (9.2, 4.8), (10.2, 3.6), (12.2, 3.6)], c["L2"], 14))       # průmysl, přístav
    # L1: z uzlu Západ na SZ k jeskyni a horské stanici
    out.append(poly([hubW, (3.2, 5), (2.4, 4.2), (1.2, 4.2), (0.8, 3.2), (0.8, 2.0)], c["L1"], 14))
    out.append(f'<circle cx="{S((0.8, 1.6))[0]:.0f}" cy="{S((0.8, 1.6))[1]:.0f}" r="30" fill="none" stroke="{c["L1"]}" stroke-width="9" stroke-dasharray="8 7"/>')
    stations = [
        ("Larpington Západ (L1·L2·L3)", hubW, "end", -26, 6, 3), ("Larpington Sever (L2·L3)", hubN, "middle", 0, -34, 2), ("Larpington Východ (L2·L3)", hubE, "end", -24, 34, 2),
        ("Larpington Střed – Přístav (L3)", hubS, "middle", 0, 46, 1), ("Východní nábřeží", (9.5, 6), "middle", 0, -26, 1), ("Paraland Link (P-01)", (11, 6), "middle", 0, 40, 1),
        ("Paraland – Marina", (14.4, 6), "start", 26, 6, 1),
        ("Čimprlichovo Hradiště", (2.6, 7.4), "middle", 0, 38, 1), ("Praha", (6, 2.8), "start", 24, 6, 1), ("výhybna Letiště", (6, 1.4), "end", -22, -6, 0), ("Letiště", (7.6, 1.4), "start", 24, 6, 1),
        ("Aokawa", (6, 0.2), "middle", 0, -26, 1), ("Ōru Maito", (3.2, 0.2), "middle", 0, -26, 1), ("Hoshimachi", (9.2, 0.2), "middle", 0, -26, 1),
        ("Zelená průmyslová zóna", (10.2, 3.6), "middle", 0, -26, 1), ("Závod na řasy", (11.2, 3.6), "middle", 0, 38, 1), ("Nákladní přístav", (12.2, 3.6), "start", 26, 6, 1),
        ("Přehrada", (2.4, 4.2), "middle", 0, -28, 1), ("Vodopád", (1.2, 4.2), "middle", 0, 40, 1), ("Krystalová jeskyně", (0.8, 2.6), "start", 26, 6, 1), ("Horská stanice", (0.8, 1.6), "start", 44, 6, 1),
    ]
    for nm, p, anc, dx, dy, lv in stations:
        x, y = S(p)
        r = {0: 8, 1: 12, 2: 17, 3: 21}[lv]
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" stroke="#1d2730" stroke-width="{4 if lv > 1 else 3}"/>')
        out.append(f'<text x="{x + dx:.0f}" y="{y + dy:.0f}" font-size="19" font-weight="600" text-anchor="{anc}" fill="#1d2730" stroke="#f7f5ee" stroke-width="5" paint-order="stroke">{nm}</text>')
    # popisy podmoří a okruhu
    mx, my = S((12.9, 6))
    out.append(f'<text x="{mx:.0f}" y="{my + 52:.0f}" font-size="18" text-anchor="middle" fill="#1f5fbf" font-style="italic">podmoří 1,48 km · prosklená galerie 226 m</text>')
    out.append(f'<text x="{S((10.2, 6))[0]:.0f}" y="{S((10.2, 6))[1] + 100:.0f}" font-size="16" text-anchor="middle" fill="#5b6770">poloostrov Paraland Link</text>')
    rx, ry = S((6, 6))
    out.append(f'<text x="{rx:.0f}" y="{ry:.0f}" font-size="26" text-anchor="middle" fill="#6b2a1e" font-weight="700">LARPINGTON</text><text x="{rx:.0f}" y="{ry + 26:.0f}" font-size="17" text-anchor="middle" fill="#6b2a1e">městský okruh L3 · 4 uzly</text>')
    # legenda
    lx, ly = 1290, 960
    out.append(f'<rect x="{lx - 20}" y="{ly - 36}" width="560" height="330" rx="12" fill="#fff" stroke="#c9c3b3"/>')
    out.append(f'<text x="{lx}" y="{ly}" font-size="24" font-weight="700" fill="#25313a">Legenda</text>')
    for i, (col, txt, dash, w) in enumerate([(c["L1"], "L1 Skyline Experience – vyhlídková, smyčka v jeskyni", "", 14), (c["L2"], "L2 Heritage Connect – povrchová", "", 14),
                                             (c["L3"], "L3 Metro Blue – podzemní (čárkovaně)", "30 12", 16), ("#8fd3ff", "prosklená galerie pod průlivem", "", 18)]):
        yy = ly + 44 + i * 46
        da = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<line x1="{lx}" y1="{yy - 6}" x2="{lx + 90}" y2="{yy - 6}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{da}/>')
        out.append(f'<text x="{lx + 110}" y="{yy}" font-size="19" fill="#25313a">{txt}</text>')
    for i, (r, txt) in enumerate([(21, "přestupní uzel (L1·L2·L3)"), (17, "přestup L2 ↔ L3 (právě tři)"), (12, "stanice")]):
        yy = ly + 232 + i * 28 - 0
        out.append(f'<circle cx="{lx + 44}" cy="{yy - 6}" r="{r * 0.62:.0f}" fill="#fff" stroke="#1d2730" stroke-width="3"/><text x="{lx + 110}" y="{yy}" font-size="19" fill="#25313a">{txt}</text>')
    out.append('</svg>')
    return "\n".join(out)


# ------------------------------------------------------------------ prohlížeč
VIEWER_CSS = """
:root{--bg:#f6f4ee;--ink:#1f2a33;--soft:#5a6670;--line:#d9d3c3;--acc:#b4541b;--card:#fffdf8;--ok:#2a8a4a;--warn:#d9741a;--bad:#c0392b}
@media (prefers-color-scheme:dark){:root{--bg:#141a1f;--ink:#e8e6df;--soft:#9aa6ae;--line:#2c353c;--acc:#f0a070;--card:#1b2227}}
*{box-sizing:border-box}html,body{height:100%;margin:0}body{background:var(--bg);color:var(--ink);font:14px/1.45 'Segoe UI',system-ui,sans-serif;display:grid;grid-template-columns:320px 1fr 340px;grid-template-rows:auto 1fr auto}
header{grid-column:1/-1;display:flex;gap:14px;align-items:center;padding:8px 14px;border-bottom:1px solid var(--line);background:var(--card)}header h1{font-size:1.05rem;margin:0}.badge{background:var(--acc);color:#fff;border-radius:999px;padding:1px 10px;font-size:.75rem}
aside{overflow:auto;padding:10px 12px;border-right:1px solid var(--line)}aside.r{border-right:0;border-left:1px solid var(--line)}h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:var(--soft);margin:12px 0 6px}
#map{position:relative;overflow:hidden;background:#cfe2ec;cursor:grab;touch-action:none}#map.drag{cursor:grabbing}#map svg{width:100%;height:100%;display:block}
label.row{display:flex;gap:8px;align-items:center;padding:2px 0;cursor:pointer}input[type=search]{width:100%;padding:7px 9px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink)}
.seg{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}.seg button{flex:1;padding:5px;border:0;background:var(--card);color:var(--ink);cursor:pointer}.seg button[aria-pressed=true]{background:var(--ink);color:var(--bg)}
#results{max-height:210px;overflow:auto;margin-top:6px}#results div{padding:4px 6px;border-radius:6px;cursor:pointer;display:flex;justify-content:space-between;gap:8px}#results div:hover{background:var(--line)}
.st{display:inline-block;border-radius:999px;padding:0 8px;font-size:.72rem;color:#fff}.st.approved{background:var(--ok)}.st.proposed{background:var(--warn)}.st.needs_decision{background:var(--bad)}
dl{margin:6px 0}dt{color:var(--soft);font-size:.75rem;margin-top:6px}dd{margin:0}footer{grid-column:1/-1;padding:4px 14px;border-top:1px solid var(--line);color:var(--soft);font-size:.8rem;display:flex;justify-content:space-between;background:var(--card)}
.hl{outline:none;filter:drop-shadow(0 0 60px #ff2d55)}button.small{font:inherit;padding:3px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);cursor:pointer}
@media (max-width:980px){body{grid-template-columns:1fr;grid-template-rows:auto 62vh auto auto auto}#map{order:1}aside{border:0;order:2;max-height:none}aside.r{order:3}footer{order:4}}
"""

VIEWER_JS = r"""
const svg=document.querySelector('#map svg');const REG=JSON.parse(document.getElementById('reg').textContent);const BYID=Object.fromEntries(REG.objects.map(o=>[o.id,o]));
const vb0=svg.viewBox.baseVal;const FULL=[vb0.x,vb0.y,vb0.width,vb0.height];let vb=[...FULL];svg.removeAttribute('width');svg.removeAttribute('height');
const X0=-0.2,Y0=-1.0,FW=24,FH=16;function setVB(){svg.setAttribute('viewBox',vb.join(' '))}
const map=document.getElementById('map');
function clientToSvg(ev){const r=svg.getBoundingClientRect();const k=Math.max(vb[2]/r.width,vb[3]/r.height);const cx=r.left+r.width/2,cy=r.top+r.height/2;return [vb[0]+vb[2]/2+(ev.clientX-cx)*k,vb[1]+vb[3]/2+(ev.clientY-cy)*k]}
map.addEventListener('wheel',e=>{e.preventDefault();const [sx,sy]=clientToSvg(e);const f=e.deltaY<0?0.8:1.25;const nw=Math.min(FULL[2],vb[2]*f),nh=nw*vb[3]/vb[2];vb=[sx-(sx-vb[0])*nw/vb[2],sy-(sy-vb[1])*nh/vb[3],nw,nh];setVB()},{passive:false});
let drag=null;map.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,vb:[...vb],moved:false};map.setPointerCapture(e.pointerId)});
map.addEventListener('pointermove',e=>{const [sx,sy]=clientToSvg(e);const kx=sx/1000+X0,ky=sy/1000+Y0;document.getElementById('coord').textContent=`x ${kx.toFixed(2)} km · y ${ky.toFixed(2)} km · X ${(kx/FW*100).toFixed(1)} % · Y ${(ky/FH*100).toFixed(1)} %`;
 if(drag){const r=svg.getBoundingClientRect();const k=Math.max(vb[2]/r.width,vb[3]/r.height);if(Math.abs(e.clientX-drag.x)+Math.abs(e.clientY-drag.y)>4){drag.moved=true;map.classList.add('drag')}vb=[drag.vb[0]-(e.clientX-drag.x)*k,drag.vb[1]-(e.clientY-drag.y)*k,vb[2],vb[3]];setVB()}});
map.addEventListener('pointerup',e=>{const was=drag&&drag.moved;drag=null;map.classList.remove('drag');if(!was){const t=e.target.closest('[data-id]');if(t)show(t.getAttribute('data-id'))}});
function zoomTo(o,w=3200){const x=(o.x_km-X0)*1000,y=(o.y_km-Y0)*1000;const r=svg.getBoundingClientRect();const h=w*r.height/r.width;vb=[x-w/2,y-h/2,w,h];setVB()}
let hlEl=[];function highlight(id){hlEl.forEach(e=>e.classList.remove('hl'));hlEl=[...svg.querySelectorAll(`[data-id="${CSS.escape(id)}"]`)].filter(e=>!e.closest('#labels-cs,#labels-ja,#labels-en'));hlEl.forEach(e=>e.classList.add('hl'))}
function esc(s){return String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function stBadge(k,v){return `<span class="st ${esc(v)}" title="${esc(k)}">${esc(k)}: ${esc(v)}</span>`}
function show(id){const o=BYID[id];const box=document.getElementById('info');if(!o){box.innerHTML=`<p>Objekt <b>${esc(id)}</b> není v registru.</p>`;return}highlight(id);
 const np=o.name_proposed;const g=o.photo_guide;let h=`<h3 style="margin:.2em 0">${esc(o.id)} · ${esc(o.name_cs)}</h3>`;
 if(np)h+=`<div style="color:var(--soft)">návrh jména: ${esc(np.cs)} / ${esc(np.en)} / ${esc(np.ja)}</div>`;
 h+=`<p>${stBadge('existence',o.exist_status)} ${stBadge('jméno',o.name_status)} ${stBadge('poloha',o.pos_status)}</p><dl>`;
 h+=`<dt>Typ</dt><dd>${esc(o.type)} / ${esc(o.subtype)} · ${esc(o.island)} · ${esc(o.region||'')}</dd>`;
 if(o.x_km!=null){h+=`<dt>Poloha</dt><dd>x ${o.x_km.toFixed(2)} km, y ${o.y_km.toFixed(2)} km · X ${o.X_pct} %, Y ${o.Y_pct} %<br><span style="color:var(--soft)">pseudo (hypotetické): ${o.lonlat_pseudo?o.lonlat_pseudo[1].toFixed(4)+' N, '+o.lonlat_pseudo[0].toFixed(4)+' E':''}</span></dd>`;
  if(o.elev_m_model!=null)h+=`<dt>Výška (model)</dt><dd>${o.elev_m_model} m</dd>`}
 if(o.deviation)h+=`<dt>Odchylka od tabulky</dt><dd>X ${o.deviation.dx_pct>0?'+':''}${o.deviation.dx_pct} %, Y ${o.deviation.dy_pct>0?'+':''}${o.deviation.dy_pct} % (${o.deviation.dev_km} km)</dd>`;
 if(o.population_model)h+=`<dt>Obyvatelé (model)</dt><dd>${o.population_model}</dd>`;if(o.length_km)h+=`<dt>Délka</dt><dd>${o.length_km} km</dd>`;if(o.lines)h+=`<dt>Linky</dt><dd>${o.lines.join(', ')}</dd>`;
 if(o.notes)h+=`<dt>Poznámka</dt><dd>${esc(o.notes)}</dd>`;if(o.bible_ref)h+=`<dt>Bible</dt><dd>${esc(o.bible_ref)}</dd>`;
 if(g){h+=`<h2>Foto / video vodítko</h2><dl><dt>Pohled kam</dt><dd>${esc(g.view_toward)}${g.sea_direction?` · moře: ${esc(g.sea_direction)}`:''}</dd><dt>Blízké body</dt><dd>${esc((g.near_ids||[]).join(', ')||'–')}</dd>`+
  `<dt>Vzdálené viditelné</dt><dd>${esc((g.far_visible||[]).map(v=>`${v.id} (${v.dir}, ${v.dist_km} km)`).join('; ')||'–')}</dd><dt>Styl</dt><dd>${esc(g.styles)}</dd><dt>Roční doba</dt><dd>${esc(g.season)}</dd><dt>Vyhnout se</dt><dd>${esc(g.avoid)}</dd></dl>`}
 box.innerHTML=h+'</dl><p><button class="small" onclick="zoomTo(BYID[\''+o.id+'\'])">Přiblížit</button></p>'}
// vrstvy
const layers=[...svg.querySelectorAll(':scope > g[id]')].filter(g=>g.getAttribute('inkscape:groupmode')==='layer');const lp=document.getElementById('layers');
const groups={'Základ':['bg-sea','grid','land','coast'],'Reliéf':['hypsometry','hillshade','landcover','coast-classes','contours','contour-labels'],'Voda':['hydro'],'Sídla':['settlements'],
 'Doprava':['roads','cycleways','trails','rail-L3','rail-L2','rail-L1','stations','ports','airports'],'Body zájmu':['poi','peaks'],'Popisky':['labels-areas','labels-cs','labels-ja','labels-en'],'Okraje':['marginalia']};
for(const [gname,ids] of Object.entries(groups)){const present=ids.filter(i=>svg.getElementById(i));if(!present.length)continue;lp.insertAdjacentHTML('beforeend',`<h2>${gname}</h2>`);
 present.forEach(i=>{const el=svg.getElementById(i);const lab=el.getAttribute('inkscape:label')||i;const on=!(i.startsWith('labels-')&&i!=='labels-cs'&&i!=='labels-areas');el.style.display=on?'':'none';
 lp.insertAdjacentHTML('beforeend',`<label class="row"><input type="checkbox" data-l="${i}" ${on?'checked':''}> ${esc(lab)}</label>`)})}
lp.addEventListener('change',e=>{const i=e.target.dataset.l;if(i)svg.getElementById(i).style.display=e.target.checked?'':'none'});
document.querySelectorAll('[data-lang]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-lang]').forEach(x=>x.setAttribute('aria-pressed',x===b));['cs','ja','en'].forEach(l=>{const el=svg.getElementById('labels-'+l);if(el)el.style.display=(l===b.dataset.lang)?'':'none';const cb=lp.querySelector(`[data-l="labels-${l}"]`);if(cb)cb.checked=(l===b.dataset.lang)})});
document.getElementById('status').onchange=e=>svg.classList.toggle('status-mode',e.target.checked);
document.getElementById('reset').onclick=()=>{vb=[...FULL];setVB()};
// hledání
const q=document.getElementById('q'),res=document.getElementById('results');
function search(){const t=q.value.trim().toLowerCase();if(!t){res.innerHTML='';return}
 const hits=REG.objects.filter(o=>o.x_km!=null&&((o.id+' '+o.name_cs+' '+(o.name_en||'')+' '+(o.name_ja||'')+' '+((o.name_proposed||{}).cs||'')).toLowerCase().includes(t))).slice(0,40);
 res.innerHTML=hits.map(o=>`<div data-id="${esc(o.id)}"><span>${esc(o.id)} · ${esc(((o.name_proposed||{}).cs)||o.name_cs)}</span><span class="st ${esc(o.exist_status)}">${esc(o.exist_status)}</span></div>`).join('')}
q.addEventListener('input',search);res.addEventListener('click',e=>{const d=e.target.closest('[data-id]');if(d){const o=BYID[d.dataset.id];zoomTo(o);show(o.id)}});
document.getElementById('count').textContent=REG.objects.length+' objektů v registru';
"""


def viewer(D, svg_embedded: str):
    VIEW.mkdir(parents=True, exist_ok=True)
    reg = json.loads((CUR / "registry" / "places.json").read_text(encoding="utf-8"))
    svg_inline = svg_embedded.split("?>", 1)[1].strip()
    html = f"""<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Atlas Larpidie – prohlížeč</title><style>{VIEWER_CSS}</style></head><body>
<header><h1>Atlas Larpidie a Paralandu</h1><span class="badge">NÁVRH · v{canon.ATLAS_VERSION}</span><span style="color:var(--soft)">fiktivní stát · kolečko = přiblížení, tažení = posun, klik = záznam z registru</span></header>
<aside><h2>Hledání</h2><input id="q" type="search" placeholder="ID nebo název (např. N-03, přístav, Aokawa)"><div id="results"></div>
<h2>Jazyk popisků</h2><div class="seg"><button data-lang="cs" aria-pressed="true">CS</button><button data-lang="ja" aria-pressed="false">JA</button><button data-lang="en" aria-pressed="false">EN</button></div>
<h2>Režim</h2><label class="row"><input type="checkbox" id="status"> Barvy podle stavu (kánon × návrh)</label><button class="small" id="reset">Celá mapa</button>
<div id="layers"></div></aside>
<div id="map">{svg_inline}</div>
<aside class="r"><h2>Záznam</h2><div id="info"><p style="color:var(--soft)">Klikněte na objekt v mapě nebo vyhledejte. Zobrazí se stav (approved / proposed / needs_decision), poloha, výška a foto/video vodítko.</p></div></aside>
<footer><span id="coord">–</span><span id="count"></span></footer>
<script id="reg" type="application/json">{json.dumps({"objects": reg["objects"]}, ensure_ascii=False)}</script><script>{VIEWER_JS}</script></body></html>"""
    (VIEW / "atlas.html").write_text(html, encoding="utf-8")
    return len(html)


def main():
    D = A.Data()
    SVGDIR.mkdir(parents=True, exist_ok=True)
    results = {}
    for v in ("master", "physical", "political", "status"):
        svg, (pl, tot) = compose(D, v)
        (SVGDIR / f"larpidia_atlas_{v}.svg").write_text(svg, encoding="utf-8")
        emb = svgkit.embed_images(svg, SVGDIR)
        (SVGDIR / f"larpidia_atlas_{v}_embedded.svg").write_text(emb, encoding="utf-8")
        results[v] = (pl, tot, len(svg) // 1024, len(emb) // 1024)
        print(f"{v:9s}: popisky {pl}/{tot}, SVG {len(svg) // 1024} kB, vložené {len(emb) // 1024} kB")
    (SVGDIR / "rail_scheme.svg").write_text(rail_scheme(D), encoding="utf-8")
    n = viewer(D, (SVGDIR / "larpidia_atlas_master_embedded.svg").read_text(encoding="utf-8"))
    print(f"viewer/atlas.html {n // 1024} kB; rail_scheme.svg")


if __name__ == "__main__":
    main()
