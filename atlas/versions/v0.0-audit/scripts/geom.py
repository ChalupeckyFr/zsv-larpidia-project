"""Pomocná geometrie atlasu Larpidie (čistý Python, bez závislostí).

Souřadnice jsou v km. Osa x roste na východ, osa y na JIH (stejně jako obrazovka),
takže polygon orientovaný „po směru hodinových ručiček na mapě“ má kladnou plochu.
Vnější normála hrany s tečnou t = (tx, ty) je n = (ty, -tx).
"""
from __future__ import annotations

import math
import random

Point = tuple[float, float]


# ---------------------------------------------------------------- základní míry
def signed_area(poly: list[Point]) -> float:
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def area(poly: list[Point]) -> float:
    return abs(signed_area(poly))


def perimeter(poly: list[Point]) -> float:
    n = len(poly)
    return sum(math.dist(poly[i], poly[(i + 1) % n]) for i in range(n))


def centroid(poly: list[Point]) -> Point:
    a = signed_area(poly)
    cx = cy = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        f = x1 * y2 - x2 * y1
        cx += (x1 + x2) * f
        cy += (y1 + y2) * f
    return cx / (6 * a), cy / (6 * a)


def bbox(poly: list[Point]) -> tuple[float, float, float, float]:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def ensure_clockwise_on_map(poly: list[Point]) -> list[Point]:
    """Zajistí kladnou plochu (po směru hodinových ručiček při y dolů)."""
    return poly if signed_area(poly) > 0 else list(reversed(poly))


# ---------------------------------------------------------------- bod × polygon
def point_in_poly(pt: Point, poly: list[Point]) -> bool:
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


def dist_point_seg(p: Point, a: Point, b: Point) -> tuple[float, Point]:
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    l2 = dx * dx + dy * dy
    if l2 == 0:
        return math.dist(p, a), a
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / l2))
    q = (ax + t * dx, ay + t * dy)
    return math.dist(p, q), q


def nearest_on_poly(p: Point, poly: list[Point]) -> tuple[float, Point, int]:
    """Nejbližší bod na hranici polygonu: (vzdálenost, bod, index hrany)."""
    best = (1e18, poly[0], 0)
    n = len(poly)
    for i in range(n):
        d, q = dist_point_seg(p, poly[i], poly[(i + 1) % n])
        if d < best[0]:
            best = (d, q, i)
    return best


def signed_distance_to_coast(p: Point, poly: list[Point]) -> float:
    """Kladné uvnitř (na souši), záporné na moři."""
    d = nearest_on_poly(p, poly)[0]
    return d if point_in_poly(p, poly) else -d


# ---------------------------------------------------------------- polygon × polygon
def densify(poly: list[Point], step: float) -> list[Point]:
    out: list[Point] = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        L = math.dist(a, b)
        k = max(1, int(L / step))
        for j in range(k):
            t = j / k
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def min_dist_polys(P: list[Point], Q: list[Point], step: float = 0.03):
    """Nejmenší vzdálenost hranic dvou polygonů (pro disjunktní ostrovy = šířka průlivu).

    Vrací (vzdálenost, bod na P, bod na Q).
    """
    qx0, qy0, qx1, qy1 = bbox(Q)
    pad = 6.0
    P_d = [p for p in densify(P, step) if qx0 - pad <= p[0] <= qx1 + pad and qy0 - pad <= p[1] <= qy1 + pad]
    Q_d = densify(Q, step)
    best = (1e18, None, None)
    for p in P_d:
        px, py = p
        for q in Q_d:
            dx = px - q[0]
            dy = py - q[1]
            d2 = dx * dx + dy * dy
            if d2 < best[0]:
                best = (d2, p, q)
    _, p0, q0 = best
    # zpřesnění přesnými vzdálenostmi na okolních hranách
    dP, pbest, _ = nearest_on_poly(q0, P)
    dQ, qbest, _ = nearest_on_poly(p0, Q)
    if dP <= dQ:
        d, q_exact, _ = nearest_on_poly(pbest, Q)
        return d, pbest, q_exact
    d, p_exact, _ = nearest_on_poly(qbest, P)
    return d, p_exact, qbest


# ---------------------------------------------------------------- křivky
def catmull_rom_closed(ctrl: list[Point], spacing: float = 0.04, alpha: float = 0.5):
    """Centripetální Catmull–Rom spline uzavřené křivky.

    Vrací seznam (x, y, seg, u): seg = index řídicího bodu, u ∈ [0,1) poloha na segmentu.
    Vzorkování ~`spacing` km.
    """
    n = len(ctrl)
    out = []
    for i in range(n):
        p0, p1, p2, p3 = ctrl[(i - 1) % n], ctrl[i], ctrl[(i + 1) % n], ctrl[(i + 2) % n]
        t0 = 0.0
        t1 = t0 + max(math.dist(p0, p1), 1e-9) ** alpha
        t2 = t1 + max(math.dist(p1, p2), 1e-9) ** alpha
        t3 = t2 + max(math.dist(p2, p3), 1e-9) ** alpha
        k = max(6, int(math.dist(p1, p2) / spacing))
        for s in range(k):
            u = s / k
            t = t1 + (t2 - t1) * u

            def mix(a, b, ta, tb):
                w = (t - ta) / (tb - ta)
                return (a[0] * (1 - w) + b[0] * w, a[1] * (1 - w) + b[1] * w)

            a1 = mix(p0, p1, t0, t1)
            a2 = mix(p1, p2, t1, t2)
            a3 = mix(p2, p3, t2, t3)
            b1 = mix(a1, a2, t0, t2)
            b2 = mix(a2, a3, t1, t3)
            c = mix(b1, b2, t1, t2)
            out.append((c[0], c[1], i, u))
    return out


def outward_normals(poly: list[Point]) -> list[Point]:
    """Jednotkové vnější normály pro polygon s kladnou plochou (po směru hodin na mapě)."""
    n = len(poly)
    res = []
    for i in range(n):
        x0, y0 = poly[(i - 1) % n]
        x1, y1 = poly[(i + 1) % n]
        tx, ty = x1 - x0, y1 - y0
        L = math.hypot(tx, ty) or 1.0
        res.append((ty / L, -tx / L))
    return res


def arc_positions(poly: list[Point]) -> tuple[list[float], float]:
    s = [0.0]
    n = len(poly)
    for i in range(1, n):
        s.append(s[-1] + math.dist(poly[i - 1], poly[i]))
    total = s[-1] + math.dist(poly[-1], poly[0])
    return s, total


def periodic_noise(cells: int, rng: random.Random):
    vals = [rng.uniform(-1, 1) for _ in range(cells)]

    def f(t: float) -> float:
        i0 = math.floor(t)
        u = t - i0
        u = u * u * (3 - 2 * u)
        a = vals[i0 % cells]
        b = vals[(i0 + 1) % cells]
        return a * (1 - u) + b * u

    return f


def displace(poly: list[Point], offsets: list[float]) -> list[Point]:
    normals = outward_normals(poly)
    return [(p[0] + nx * d, p[1] + ny * d) for p, (nx, ny), d in zip(poly, normals, offsets)]


def coast_noise(poly: list[Point], weights: list[float], octaves, seed: int) -> list[float]:
    """Součet oktáv periodického šumu podél oblouku × lokální váha (0 = bez šumu)."""
    s, total = arc_positions(poly)
    rng = random.Random(seed)
    layers = []
    for wavelength, amp in octaves:
        cells = max(3, round(total / wavelength))
        layers.append((cells / total, amp, periodic_noise(cells, rng)))
    out = []
    for si, w in zip(s, weights):
        v = 0.0
        for k, amp, f in layers:
            v += amp * f(si * k)
        out.append(v * w)
    return out


# ---------------------------------------------------------------- samoprotnutí
def _seg_intersect(a, b, c, d) -> bool:
    def orient(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    o1, o2 = orient(a, b, c), orient(a, b, d)
    o3, o4 = orient(c, d, a), orient(c, d, b)
    return (o1 * o2 < 0) and (o3 * o4 < 0)


def self_intersections(poly: list[Point], cell: float = 0.5, limit: int = 20):
    """Vrací seznam dvojic indexů protínajících se hran (prázdný = jednoduchý polygon)."""
    n = len(poly)
    grid: dict[tuple[int, int], list[int]] = {}
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        for cx in range(int(x0 // cell), int(x1 // cell) + 1):
            for cy in range(int(y0 // cell), int(y1 // cell) + 1):
                grid.setdefault((cx, cy), []).append(i)
    seen = set()
    found = []
    for idxs in grid.values():
        for ii in range(len(idxs)):
            for jj in range(ii + 1, len(idxs)):
                i, j = idxs[ii], idxs[jj]
                if (i, j) in seen:
                    continue
                seen.add((i, j))
                if abs(i - j) <= 1 or (i == 0 and j == n - 1):
                    continue
                if _seg_intersect(poly[i], poly[(i + 1) % n], poly[j], poly[(j + 1) % n]):
                    found.append((i, j))
                    if len(found) >= limit:
                        return found
    return found


# ---------------------------------------------------------------- konvexní obal, zátoky
def convex_hull(points: list[Point]) -> list[Point]:
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def pockets(poly: list[Point], min_depth: float = 0.5):
    """Zátoky (kapsy konvexního obalu): [{depth, mouth, centroid, area, bbox}] seřazeno sestupně."""
    hull = convex_hull(poly)
    hull_set = {p: True for p in hull}
    n = len(poly)
    idx = [i for i, p in enumerate(poly) if p in hull_set]
    res = []
    for a, b in zip(idx, idx[1:] + [idx[0] + n]):
        chain = [poly[k % n] for k in range(a, b + 1)]
        if len(chain) < 3:
            continue
        p, q = chain[0], chain[-1]
        mouth = math.dist(p, q)
        if mouth < 1e-9:
            continue
        depth = 0.0
        for c in chain[1:-1]:
            depth = max(depth, abs((q[0] - p[0]) * (p[1] - c[1]) - (p[0] - c[0]) * (q[1] - p[1])) / mouth)
        if depth >= min_depth:
            cx = sum(c[0] for c in chain) / len(chain)
            cy = sum(c[1] for c in chain) / len(chain)
            res.append({
                "depth_km": depth, "mouth_km": mouth, "centroid": (cx, cy),
                "area_km2": abs(signed_area(chain)),
                "from": p, "to": q,
            })
    return sorted(res, key=lambda r: -r["depth_km"])


# ---------------------------------------------------------------- transformace
def rotate_pts(pts, angle_deg: float, origin: Point = (0.0, 0.0)):
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    ox, oy = origin
    return [(ox + (x - ox) * ca - (y - oy) * sa, oy + (x - ox) * sa + (y - oy) * ca) for x, y in pts]


def translate_pts(pts, dx: float, dy: float):
    return [(x + dx, y + dy) for x, y in pts]


def smoothstep(e0: float, e1: float, x: float) -> float:
    if e1 == e0:
        return 1.0 if x >= e1 else 0.0
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)
