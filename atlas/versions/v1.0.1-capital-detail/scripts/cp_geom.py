"""Geometrické pomůcky plánu hlavního města (F7). Souřadnice v metrech (u východ, v jih). Bez GIS knihoven: numpy + Pillow.

Obsah: průsečíky úseček, délky a převzorkování polyline, posun polyline, ořez polygonu konvexním polygonem (Sutherland–Hodgman),
označování souvislých ploch masky (run-length), polygony z masky (marching squares z raster.contour_lines), pravoúhelník kolem osy.
"""
from __future__ import annotations

import math
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw

import raster

Pt = tuple[float, float]


# ------------------------------------------------------------------ polyline
def length(pts) -> float:
    return float(sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:])))


def resample(pts, step: float):
    """Body po `step` metrech podél lomené čáry (včetně prvního a posledního bodu)."""
    out = [tuple(pts[0])]
    acc = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.dist(a, b)
        if L < 1e-9:
            continue
        t = step - acc
        while t < L:
            out.append((a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L))
            t += step
        acc = L - (t - step)
    if math.dist(out[-1], pts[-1]) > 1e-6:
        out.append(tuple(pts[-1]))
    return out


def point_at(pts, s: float):
    """Bod a směr (tx, ty) ve vzdálenosti s od začátku polyline."""
    acc = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.dist(a, b)
        if acc + L >= s and L > 0:
            t = (s - acc) / L
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        acc += L
    a, b = pts[-2], pts[-1]
    L = math.dist(a, b) or 1.0
    return tuple(pts[-1]), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)


def nearest_on_polyline(p, pts):
    """(vzdálenost, nejbližší bod, vzdálenost podél čáry)."""
    best = (1e18, None, 0.0)
    acc = 0.0
    px, py = p
    for a, b in zip(pts[:-1], pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - a[0]) * dx + (py - a[1]) * dy) / L2))
        q = (a[0] + dx * t, a[1] + dy * t)
        d = math.dist(p, q)
        if d < best[0]:
            best = (d, q, acc + math.sqrt(L2) * t)
        acc += math.sqrt(L2)
    return best


def offset_polyline(pts, d: float):
    """Posun polyline o d metrů doleva (vzhledem ke směru; v souřadnicích s y dolů je „vlevo“ záporná y-normála). Přibližně, s mitrem."""
    n = len(pts)
    out = []
    for i in range(n):
        if i == 0:
            t = (pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
        elif i == n - 1:
            t = (pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
        else:
            t1 = (pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
            t2 = (pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
            l1 = math.hypot(*t1) or 1.0
            l2 = math.hypot(*t2) or 1.0
            t = (t1[0] / l1 + t2[0] / l2, t1[1] / l1 + t2[1] / l2)
        L = math.hypot(*t) or 1.0
        nx, ny = t[1] / L, -t[0] / L          # vlevo od směru (y dolů)
        out.append((pts[i][0] + nx * d, pts[i][1] + ny * d))
    return out


def seg_intersect(p, p2, q, q2):
    """Průsečík úseček (t, u, bod) nebo None; t, u ∈ [0, 1] podél p→p2 a q→q2. Rovnoběžky → None."""
    rx, ry = p2[0] - p[0], p2[1] - p[1]
    sx, sy = q2[0] - q[0], q2[1] - q[1]
    den = rx * sy - ry * sx
    if abs(den) < 1e-12:
        return None
    t = ((q[0] - p[0]) * sy - (q[1] - p[1]) * sx) / den
    u = ((q[0] - p[0]) * ry - (q[1] - p[1]) * rx) / den
    eps = 1e-9
    if -eps <= t <= 1.0 + eps and -eps <= u <= 1.0 + eps:
        t, u = min(1.0, max(0.0, t)), min(1.0, max(0.0, u))
        return t, u, (p[0] + rx * t, p[1] + ry * t)
    return None


def polyline_intersections(a, b):
    """Všechny průsečíky dvou polyline: seznam (bod, s_a, s_b) – s_* = vzdálenost podél příslušné čáry."""
    out = []
    sa = 0.0
    for a0, a1 in zip(a[:-1], a[1:]):
        La = math.dist(a0, a1)
        sb = 0.0
        for b0, b1 in zip(b[:-1], b[1:]):
            Lb = math.dist(b0, b1)
            r = seg_intersect(a0, a1, b0, b1)
            if r:
                out.append((r[2], sa + r[0] * La, sb + r[1] * Lb))
            sb += Lb
        sa += La
    return out


# ------------------------------------------------------------------ polygon
def area(poly) -> float:
    s = 0.0
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        s += float(x0) * float(y1) - float(x1) * float(y0)
    return abs(s) / 2.0


def centroid(poly):
    a2 = 0.0
    cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        c = x0 * y1 - x1 * y0
        a2 += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    if abs(a2) < 1e-9:
        return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))
    return (cx / (3 * a2), cy / (3 * a2))


def point_in_poly(pt, poly) -> bool:
    x, y = pt
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-18) + xi:
            inside = not inside
        j = i
    return inside


def clip_convex(subject, clip):
    """Sutherland–Hodgman: ořez polygonu `subject` konvexním polygonem `clip` (oba proti směru hodin nebo oba po směru)."""
    def inside(p, a, b, sign):
        return sign * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) >= 0

    def inter(p, q, a, b):
        r = seg_intersect_inf(p, q, a, b)
        return r if r else q

    sign = 1.0 if signed_area(clip) > 0 else -1.0
    out = list(subject)
    for a, b in zip(clip, clip[1:] + clip[:1]):
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside(e, a, b, sign):
                if not inside(s, a, b, sign):
                    out.append(inter(s, e, a, b))
                out.append(e)
            elif inside(s, a, b, sign):
                out.append(inter(s, e, a, b))
            s = e
    return out


def signed_area(poly) -> float:
    s = 0.0
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        s += x0 * y1 - x1 * y0
    return s / 2.0


def seg_intersect_inf(p, q, a, b):
    """Průsečík přímky p–q s přímkou a–b."""
    rx, ry = q[0] - p[0], q[1] - p[1]
    sx, sy = b[0] - a[0], b[1] - a[1]
    den = rx * sy - ry * sx
    if abs(den) < 1e-12:
        return None
    t = ((a[0] - p[0]) * sy - (a[1] - p[1]) * sx) / den
    return (p[0] + rx * t, p[1] + ry * t)


def oriented_rect(cx, cy, w, h, angle_deg):
    """Pravoúhelník se středem (cx, cy), šířkou w (podél směru angle) a hloubkou h; angle ve stupních (0 = východ, 90 = jih)."""
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        pts.append((cx + dx * ca - dy * sa, cy + dx * sa + dy * ca))
    return pts


def buffer_polyline_poly(pts, half_w):
    """Polygon (pásek) kolem polyline s poloviční šířkou half_w – z levého a pravého posunu."""
    left = offset_polyline(pts, half_w)
    right = offset_polyline(pts, -half_w)
    return left + right[::-1]


# ------------------------------------------------------------------ rastr: kreslení a značení
def draw_mask(shape_hw, to_px, polys=(), lines=()):
    """Binární maska z polygonů a čar; `lines` = [(polyline, šířka_px), …]; `to_px(x, y)` → (sloupec, řádek) v pixelech."""
    H, W = shape_hw
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    for poly in polys:
        d.polygon([to_px(*p) for p in poly], fill=255)
    for ln, w in lines:
        d.line([to_px(*p) for p in ln], fill=255, width=max(1, int(round(w))), joint="curve")
    return np.asarray(im) > 127


def label_mask(mask: np.ndarray):
    """Souvislé plochy (4-okolí) po řádkových úsecích s union-find. Vrací (labels int32, počet, bbox[n+1, 4] = r0, r1, c0, c1 (včetně), plocha[n+1] v pixelech)."""
    H, W = mask.shape
    parent = [0]

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            if ra < rb:
                parent[rb] = ra
            else:
                parent[ra] = rb

    runs_all = []
    prev = []
    padded = np.zeros((H, W + 2), dtype=np.int8)
    padded[:, 1:-1] = mask
    diff = np.diff(padded, axis=1)
    for i in range(H):
        starts = np.nonzero(diff[i] == 1)[0]
        ends = np.nonzero(diff[i] == -1)[0]
        cur = []
        pj = 0
        for s, e in zip(starts.tolist(), ends.tolist()):
            lab = 0
            while pj < len(prev) and prev[pj][1] <= s:
                pj += 1
            k = pj
            while k < len(prev) and prev[k][0] < e:
                if lab == 0:
                    lab = prev[k][2]
                else:
                    union(lab, prev[k][2])
                k += 1
            if lab == 0:
                parent.append(len(parent))
                lab = len(parent) - 1
            cur.append((s, e, lab))
            runs_all.append((i, s, e, lab))
        prev = cur
    labels = np.zeros((H, W), dtype=np.int32)
    remap = {}
    boxes = {}
    for i, s, e, lab in runs_all:
        r = find(lab)
        k = remap.get(r)
        if k is None:
            k = remap[r] = len(remap) + 1
            boxes[k] = [i, i, s, e - 1, 0]
        labels[i, s:e] = k
        b = boxes[k]
        b[1] = i
        b[2] = min(b[2], s)
        b[3] = max(b[3], e - 1)
        b[4] += e - s
    n = len(remap)
    bbox = np.zeros((n + 1, 4), dtype=np.int64)
    area_px = np.zeros(n + 1, dtype=np.int64)
    for k, b in boxes.items():
        bbox[k] = b[:4]
        area_px[k] = b[4]
    return labels, n, bbox, area_px


def mask_to_polygons(mask: np.ndarray, x0: float, y0: float, cell: float, min_area: float = 0.0, simplify_tol: float = 0.0):
    """Obrysy souvislých ploch masky jako polygony (metry). Vnější okraje; díry se ignorují (blok bez dvorů)."""
    pad = np.pad(mask.astype(np.float64), 1)
    g = SimpleNamespace(x0=x0 - cell, y0=y0 - cell, dx=cell)
    polys = []
    for ln in raster.contour_lines(g, pad, 0.5):
        if len(ln) < 4 or math.dist(ln[0], ln[-1]) > 1e-6:
            continue
        pts = [(float(p[0]), float(p[1])) for p in ln[:-1]]
        if simplify_tol > 0:
            pts = [(float(p[0]), float(p[1])) for p in raster.simplify(pts + [pts[0]], simplify_tol)[:-1]]
        if len(pts) >= 3 and area(pts) >= min_area:
            polys.append(pts)
    # díry mají opačné vinutí – vynecháme je podle znaménka vůči největšímu polygonu
    if not polys:
        return []
    polys.sort(key=area, reverse=True)
    sgn = signed_area(polys[0]) > 0
    return [p for p in polys if (signed_area(p) > 0) == sgn]
