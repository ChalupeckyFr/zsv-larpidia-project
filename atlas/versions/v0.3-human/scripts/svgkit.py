"""Malý SVG nástroj pro atlas. Jednotka SVG = 1 m na zemi; plátno A2 (594 × 420 mm) = 1 : 50 000.

Vrstvy jsou Inkscape/Illustrator-kompatibilní skupiny (`inkscape:groupmode="layer"`).
Texty jsou skutečné <text> prvky (editovatelné), s kontur­ou přes `paint-order`.
"""
from __future__ import annotations

import html
from contextlib import contextmanager

from canon import CANVAS

FONT = "'Segoe UI','Noto Sans','Noto Sans JP','Yu Gothic','Meiryo','Arial',sans-serif"

PALETTE = {
    "sea": "#cfe2ec", "shelf1": "#c1d9e6", "shelf2": "#b4d0e0", "shelf3": "#a8c8da",
    "land": "#e6e3cc", "land_edge": "#4c5a63", "ink": "#25313a", "ink_soft": "#5b6770",
    "grid": "#9fb6c4", "frame": "#d1621b", "proposed": "#b4541b",
    "peak": "#7a4a22", "nature": "#2c7a52", "capital": "#a8231b", "district": "#cf5b4e",
    "port": "#1b6aa3", "town": "#2b2f33", "industry": "#5a5f63", "airport": "#5b49a8", "rail_link": "#1b6aa3",
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


class Sheet:
    def __init__(self, canvas: dict | None = None):
        c = canvas or CANVAS
        self.x0, self.y0, self.w, self.h = c["x0"], c["y0"], c["w"], c["h"]
        self.parts: list[str] = []

    # ---- souřadnice
    def X(self, x_km: float) -> int:
        return round((x_km - self.x0) * 1000)

    def Y(self, y_km: float) -> int:
        return round((y_km - self.y0) * 1000)

    def pt(self, p) -> str:
        return f"{self.X(p[0])},{self.Y(p[1])}"

    def d(self, poly, close=True) -> str:
        s = "M" + " L".join(self.pt(p) for p in poly)
        return s + (" Z" if close else "")

    # ---- skladba
    def raw(self, s: str) -> None:
        self.parts.append(s)

    @contextmanager
    def layer(self, id_: str, label: str, extra: str = ""):
        self.parts.append(f'<g id="{esc(id_)}" inkscape:groupmode="layer" inkscape:label="{esc(label)}" {extra}>')
        yield
        self.parts.append("</g>")

    @contextmanager
    def group(self, id_: str = "", extra: str = ""):
        self.parts.append(f'<g id="{esc(id_)}" {extra}>' if id_ else f"<g {extra}>")
        yield
        self.parts.append("</g>")

    def path(self, poly, fill="none", stroke="none", sw=0, close=True, extra=""):
        self.parts.append(
            f'<path d="{self.d(poly, close)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linejoin="round" stroke-linecap="round" {extra}/>'
        )

    def line(self, a, b, stroke, sw, dash="", extra=""):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{self.X(a[0])}" y1="{self.Y(a[1])}" x2="{self.X(b[0])}" y2="{self.Y(b[1])}" '
            f'stroke="{stroke}" stroke-width="{sw}"{da} stroke-linecap="round" {extra}/>'
        )

    def rect_km(self, x0, y0, x1, y1, fill="none", stroke="none", sw=0, dash="", extra=""):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<rect x="{self.X(x0)}" y="{self.Y(y0)}" width="{round((x1 - x0) * 1000)}" height="{round((y1 - y0) * 1000)}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da} {extra}/>'
        )

    def rect_u(self, x, y, w, h, fill="none", stroke="none", sw=0, rx=0, extra=""):
        """Obdélník v jednotkách SVG (m), souřadnice od levého horního rohu plátna."""
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" {extra}/>'
        )

    def circle(self, p, r_m, fill, stroke="#fff", sw=18, extra=""):
        self.parts.append(f'<circle cx="{self.X(p[0])}" cy="{self.Y(p[1])}" r="{r_m}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def marker(self, kind: str, p, size=70, fill="#000", stroke="#fff", sw=18, extra=""):
        cx, cy = self.X(p[0]), self.Y(p[1])
        s = size
        if kind == "triangle":
            pts = f"{cx},{cy - s} {cx + s * 0.95},{cy + s * 0.7} {cx - s * 0.95},{cy + s * 0.7}"
            self.parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
        elif kind == "square":
            self.parts.append(f'<rect x="{cx - s * 0.85}" y="{cy - s * 0.85}" width="{s * 1.7}" height="{s * 1.7}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
        elif kind == "diamond":
            pts = f"{cx},{cy - s * 1.1} {cx + s * 1.1},{cy} {cx},{cy + s * 1.1} {cx - s * 1.1},{cy}"
            self.parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
        elif kind == "star":
            import math
            pts = []
            for k in range(10):
                r = s * 1.35 if k % 2 == 0 else s * 0.6
                a = -math.pi / 2 + k * math.pi / 5
                pts.append(f"{cx + r * math.cos(a):.0f},{cy + r * math.sin(a):.0f}")
            self.parts.append(f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
        else:
            self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def text(self, x_km, y_km, s, size=130, anchor="start", fill=None, weight="400", halo=True,
             style="", extra="", rotate=None, units=False):
        fill = fill or PALETTE["ink"]
        x = x_km if units else self.X(x_km)
        y = y_km if units else self.Y(y_km)
        h = f' stroke="#ffffff" stroke-width="{max(16, size // 6)}" stroke-linejoin="round" paint-order="stroke"' if halo else ""
        rot = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}"{h}{rot} {style} {extra}>{esc(s)}</text>'
        )

    # ---- výstup
    def render(self, title: str, desc: str, width_mm=594, height_mm=420) -> str:
        W, H = round(self.w * 1000), round(self.h * 1000)
        head = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{width_mm}mm" height="{height_mm}mm" viewBox="0 0 {W} {H}">\n'
            f"<title>{esc(title)}</title>\n<desc>{esc(desc)}</desc>\n"
        )
        return head + "\n".join(self.parts) + "\n</svg>\n"


def nice_scale_bar(sheet: Sheet, x_u: float, y_u: float, km: float = 5.0, label_size: int = 120):
    """Měřítkový pruh (v jednotkách SVG, horní levý roh pruhu)."""
    seg = km / 5 * 1000
    for i in range(5):
        fill = "#25313a" if i % 2 == 0 else "#ffffff"
        sheet.rect_u(x_u + i * seg, y_u, seg, 70, fill=fill, stroke="#25313a", sw=10)
    for i in range(0, 6):
        sheet.text(x_u + i * seg, y_u + 210, f"{i * km / 5:g}", size=label_size, anchor="middle", units=True, halo=False)
    sheet.text(x_u + 5 * seg + 140, y_u + 62, "km", size=label_size, units=True, halo=False)


def north_arrow(sheet: Sheet, x_u: float, y_u: float, size: int = 520):
    s = size
    sheet.raw(f'<g id="north-arrow" transform="translate({x_u},{y_u})">'
              f'<polygon points="0,{-s} {s * 0.28},{s * 0.35} 0,{s * 0.15} {-s * 0.28},{s * 0.35}" fill="#25313a" stroke="#fff" stroke-width="14"/>'
              f'<polygon points="0,{-s} {s * 0.28},{s * 0.35} 0,{s * 0.15}" fill="#ffffff" stroke="#25313a" stroke-width="14"/>'
              f'<text x="0" y="{-s - 70}" font-family="{FONT}" font-size="190" font-weight="700" text-anchor="middle" fill="#25313a">S</text></g>')


def embed_images(svg_text: str, base_dir) -> str:
    """Nahradí relativní href obrázků vloženými data URI (samostatný SVG pro odeslání)."""
    import base64
    import re
    from pathlib import Path as _P

    def repl(m):
        href = m.group(1)
        if href.startswith("data:"):
            return m.group(0)
        data = (_P(base_dir) / href).resolve().read_bytes()
        return 'href="data:image/png;base64,' + base64.b64encode(data).decode("ascii") + '"'

    return re.sub(r'href="([^"]+\.png)"', repl, svg_text)
