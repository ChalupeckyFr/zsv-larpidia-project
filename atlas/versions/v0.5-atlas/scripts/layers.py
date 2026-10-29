"""Opakovaně použitelné SVG vrstvy atlasu (F2 náhled fyzické mapy, později hlavní atlas v F5).

Všechny vrstvy kreslí do `svgkit.Sheet`; názvy vrstev jsou ve stylu Inkscape (inkscape:groupmode="layer").
"""
from __future__ import annotations

import base64
import io
import math

import numpy as np
from PIL import Image

import canon
import svgkit
from svgkit import PALETTE as P


def png_data_uri(rgba: np.ndarray) -> str:
    buf = io.BytesIO()
    Image.fromarray(rgba).save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def defs_clip(sh: svgkit.Sheet, main, para):
    sh.raw(f'<defs><clipPath id="clip-land"><path d="{sh.d(main)}"/><path d="{sh.d(para)}"/></clipPath></defs>')


def layer_sea(sh, main, para, shelf=True):
    W, H = round(sh.w * 1000), round(sh.h * 1000)
    with sh.layer("bg-sea", "Moře a šelf"):
        sh.rect_u(0, 0, W, H, fill=P["sea"])
        if shelf:
            for width_km, col in ((3.6, P["shelf3"]), (2.0, P["shelf2"]), (0.9, P["shelf1"])):
                for poly in (main, para):
                    sh.path(poly, fill="none", stroke=col, sw=round(width_km * 1000), extra='opacity="0.9"')


def layer_grid(sh, with_frame=True, step=2):
    import math as m
    with sh.layer("grid", "Km mřížka a referenční rámec"):
        x = m.ceil(sh.x0 / step) * step
        while x < sh.x0 + sh.w:
            sh.line((x, sh.y0), (x, sh.y0 + sh.h), P["grid"], 5)
            sh.text(x, sh.y0 + 0.28, f"{x:g}", size=100, anchor="middle", fill=P["ink_soft"], halo=False)
            x += step
        y = m.ceil(sh.y0 / step) * step
        while y < sh.y0 + sh.h:
            sh.line((sh.x0, y), (sh.x0 + sh.w, y), P["grid"], 5)
            sh.text(sh.x0 + 0.08, y - 0.07, f"{y:g}", size=100, fill=P["ink_soft"], halo=False)
            y += step
        if with_frame:
            sh.rect_km(0, 0, canon.FRAME_W_KM, canon.FRAME_H_KM, stroke=P["frame"], sw=14, dash="120 70")


def layer_land_base(sh, main, para, fill=None):
    with sh.layer("land", "Souš"):
        sh.path(main, fill=fill or P["land"], stroke="none", sw=0, extra='id="LARPIDIA_MAIN"')
        sh.path(para, fill=fill or P["land"], stroke="none", sw=0, extra='id="PARALAND"')


def layer_coast_line(sh, main, para):
    with sh.layer("coast", "Pobřežní čára"):
        sh.path(main, fill="none", stroke=P["land_edge"], sw=13)
        sh.path(para, fill="none", stroke=P["land_edge"], sw=13)


def layer_raster(sh, layer_id, label, href, opacity=1.0, clip=True):
    """Rastrová vrstva odkazem (relativní cesta k PNG); vloženou verzi vyrobí svgkit.embed_images()."""
    W, H = round(sh.w * 1000), round(sh.h * 1000)
    cp = ' clip-path="url(#clip-land)"' if clip else ""
    with sh.layer(layer_id, label):
        sh.raw(f'<image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="none" opacity="{opacity}"{cp} href="{href}"/>')


def layer_landcover(sh, polys_by_class, colors, names):
    with sh.layer("landcover", "Pokryv krajiny (návrh)", 'clip-path="url(#clip-land)"'):
        for cid, rings in polys_by_class.items():
            if not rings:
                continue
            d = " ".join(sh.d(r) for r in rings)
            hatch = ' stroke="#9b7d3c" stroke-width="5"' if names.get(cid) == "terraces" else ""
            sh.raw(f'<path id="lc-{names.get(cid, cid)}" d="{d}" fill="{colors[cid]}" fill-rule="evenodd"{hatch}/>')


def layer_contours(sh, contours):
    """contours = [{level, index, line:[(x,y)…]}]"""
    with sh.layer("contours", "Vrstevnice po 20 m (index 100 m, návrh)", 'clip-path="url(#clip-land)"'):
        minor = [c for c in contours if not c["index"]]
        major = [c for c in contours if c["index"]]
        with sh.group("contours-minor", 'fill="none" stroke="#a98458" stroke-width="5.5" stroke-linejoin="round" opacity="0.9"'):
            for c in minor:
                sh.raw(f'<path d="{sh.d(c["line"], close=False)}"/>')
        with sh.group("contours-index", 'fill="none" stroke="#7b5326" stroke-width="10" stroke-linejoin="round"'):
            for c in major:
                sh.raw(f'<path d="{sh.d(c["line"], close=False)}"/>')


def layer_contour_labels(sh, contours, every=1):
    with sh.layer("contour-labels", "Výšky indexových vrstevnic"):
        for c in contours:
            if not c["index"] or len(c["line"]) < 40:
                continue
            k = len(c["line"]) // 2
            x, y = c["line"][k]
            sh.text(x, y + 0.03, f"{int(c['level'])}", size=82, anchor="middle", fill="#6b4520", halo=True)


def layer_hydro(sh, rivers, lake_poly, waterfall, dam_pt=None):
    with sh.layer("hydro", "Vodní toky, jezero, vodopád (návrh)"):
        for r in rivers:
            kind = r["kind"]
            w = {"main": 24, "river": 20, "stream": 13}[kind]
            sh.raw(f'<path id="river-{r["id"]}-{r["part"]}" d="{sh.d(r["pts"], close=False)}" fill="none" stroke="#3b8fc4" stroke-width="{w}" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
        sh.path(lake_poly, fill="#8fc3e0", stroke="#3b8fc4", sw=14, extra='id="W-lake-N04"')
        if waterfall:
            wx, wy = waterfall
            sh.marker("diamond", (wx, wy), size=48, fill="#2c7fb8", stroke="#ffffff", sw=14, extra='id="pt-N-03"')
        if dam_pt:
            sh.marker("square", dam_pt, size=40, fill="#34495e", stroke="#ffffff", sw=12, extra='id="dam-N04"')


def layer_coast_classes(sh, cc):
    with sh.layer("coast-classes", "Typy pobřeží: pláže, útesy, skalnaté (návrh)"):
        with sh.group("beaches", f'fill="{PALETTE_BEACH}" stroke="#d8c58a" stroke-width="5"'):
            for b in cc["beaches"]:
                sh.raw(f'<path d="{sh.d(b["ring"])}"/>')
        with sh.group("rocky-shore", 'fill="none" stroke="#7d7466" stroke-width="12" stroke-linecap="round" opacity="0.8"'):
            for r in cc["rocky"]:
                sh.raw(f'<path d="{sh.d(r["line"], close=False)}"/>')
        with sh.group("cliffs", 'fill="none" stroke="#3b3a36" stroke-width="16" stroke-linecap="round"'):
            for c in cc["cliffs"]:
                sh.raw(f'<path d="{sh.d(c["line"], close=False)}"/>')


PALETTE_BEACH = "#f4e8bd"


def layer_peaks(sh, peaks):
    """peaks = [{id, name, x, y, z}]"""
    with sh.layer("peaks", "Vrcholy a výšky (modelové)"):
        for p in peaks:
            sh.marker("triangle", (p["x"], p["y"]), size=70, fill=P["peak"], extra=f'id="pk-{p["id"]}" data-status="proposed"')
            sh.text(p["x"] + 0.16, p["y"] - 0.12, f'{p["id"]} {p["name"]}', size=118, weight="700")
            sh.text(p["x"] + 0.16, p["y"] + 0.05, f'{p["z"]:.0f} m (model)', size=108, fill=P["ink_soft"])
