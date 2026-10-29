"""Rastrové pomůcky atlasu (numpy + Pillow). Mřížka pokrývá celé plátno atlasu (A2 / 1 : 50 000).

Řádky rostou na jih (y), sloupce na východ (x) – stejně jako souřadnice v km.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

import canon


class Grid:
    def __init__(self, cell_km: float = 0.02, canvas: dict | None = None):
        c = canvas or canon.CANVAS
        self.dx = cell_km
        self.x0, self.y0 = c["x0"], c["y0"]
        self.nx = int(round(c["w"] / cell_km))
        self.ny = int(round(c["h"] / cell_km))

    @property
    def shape(self):
        return (self.ny, self.nx)

    def xs(self):
        return (self.x0 + (np.arange(self.nx) + 0.5) * self.dx).astype(np.float32)

    def ys(self):
        return (self.y0 + (np.arange(self.ny) + 0.5) * self.dx).astype(np.float32)

    def mesh(self):
        X, Y = np.meshgrid(self.xs(), self.ys())
        return X, Y

    def to_px(self, x, y):
        return (x - self.x0) / self.dx, (y - self.y0) / self.dx

    def cell_of(self, x, y):
        return int((y - self.y0) / self.dx), int((x - self.x0) / self.dx)


# ---------------------------------------------------------------- rasterizace
def rasterize(grid: Grid, polys) -> np.ndarray:
    im = Image.new("L", (grid.nx, grid.ny), 0)
    d = ImageDraw.Draw(im)
    for poly in polys:
        d.polygon([grid.to_px(*p) for p in poly], fill=255)
    return np.asarray(im) > 127


# ---------------------------------------------------------------- vzdálenosti
def _resize_f(arr: np.ndarray, size_wh, resample=Image.BILINEAR) -> np.ndarray:
    im = Image.fromarray(arr.astype(np.float32), mode="F").resize(size_wh, resample)
    return np.asarray(im)


def coarse_nearest(grid: Grid, pts: np.ndarray, factor: int = 3, want_index: bool = False):
    """Vzdálenost (km) k nejbližšímu z bodů `pts` (N×2) – počítáno na hrubší mřížce a zvětšeno.

    Vrací dist (km) a volitelně index nejbližšího bodu.
    """
    cx = grid.x0 + (np.arange(0, grid.nx, factor) + factor / 2) * grid.dx
    cy = grid.y0 + (np.arange(0, grid.ny, factor) + factor / 2) * grid.dx
    CX, CY = np.meshgrid(cx.astype(np.float32), cy.astype(np.float32))
    flat_x, flat_y = CX.ravel(), CY.ravel()
    best = np.full(flat_x.shape, np.inf, dtype=np.float32)
    arg = np.zeros(flat_x.shape, dtype=np.int32)
    P = pts.astype(np.float32)
    chunk = 150
    for s in range(0, len(P), chunk):
        p = P[s:s + chunk]
        d2 = (flat_x[:, None] - p[None, :, 0]) ** 2 + (flat_y[:, None] - p[None, :, 1]) ** 2
        j = np.argmin(d2, axis=1)
        m = d2[np.arange(len(flat_x)), j]
        better = m < best
        best = np.where(better, m, best)
        arg = np.where(better, j + s, arg)
    dist = np.sqrt(best).reshape(CX.shape)
    big = _resize_f(dist, (grid.nx, grid.ny))
    if not want_index:
        return big
    idx = Image.fromarray(arg.reshape(CX.shape).astype(np.int32), mode="I").resize((grid.nx, grid.ny), Image.NEAREST)
    return big, np.asarray(idx)


def resample_polyline(poly, step_km: float, closed=True) -> np.ndarray:
    pts = list(poly) + ([poly[0]] if closed else [])
    out = [pts[0]]
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        L = math.dist(a, b)
        if L == 0:
            continue
        t = step_km - acc
        while t <= L:
            out.append((a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L))
            t += step_km
        acc = L - (t - step_km)
    return np.array(out, dtype=np.float32)


# ---------------------------------------------------------------- šum a rozostření
def value_noise(grid: Grid, cell_km: float, rng: np.random.Generator) -> np.ndarray:
    lx = int(grid.nx * grid.dx / cell_km) + 5
    ly = int(grid.ny * grid.dx / cell_km) + 5
    base = rng.standard_normal((ly, lx)).astype(np.float32)
    w = int(round(lx * cell_km / grid.dx))
    h = int(round(ly * cell_km / grid.dx))
    big = _resize_f(base, (w, h), Image.BICUBIC)
    return big[: grid.ny, : grid.nx]


def fbm(grid: Grid, seed: int, octaves) -> np.ndarray:
    """octaves = [(cell_km, amplitude), …] → součet vyhlazených šumů; normalizováno na ≈ N(0, Σamp²)."""
    rng = np.random.default_rng(seed)
    out = np.zeros(grid.shape, dtype=np.float32)
    for cell, amp in octaves:
        n = value_noise(grid, cell, rng)
        n = n / (n.std() + 1e-9)
        out += amp * n
    return out


def ridged_mf(grid: Grid, seed: int, cell0: float = 1.9, octaves: int = 5, lac: float = 2.05, gain: float = 0.55) -> np.ndarray:
    """Hřebenový multifraktál 0..1 (1 = hřbet, 0 = údolí) s vazbou oktáv, tvoří větvené hřbety a údolí."""
    rng = np.random.default_rng(seed)
    total = np.zeros(grid.shape, dtype=np.float32)
    weight = np.ones(grid.shape, dtype=np.float32)
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        n = value_noise(grid, cell0 / (lac ** o), rng)
        n = n / (n.std() + 1e-9)
        sgn = np.clip(1.0 - np.abs(n) * 0.85, 0.0, 1.0) ** 2
        sgn = sgn * weight
        total += amp * sgn
        norm += amp
        weight = np.clip(sgn * 2.2, 0.15, 1.0)
        amp *= gain
    return total / norm


def box_blur(a: np.ndarray, r: int) -> np.ndarray:
    if r <= 0:
        return a
    k = 2 * r + 1
    out = a.astype(np.float64)
    for axis in (1, 0):
        pad = [(0, 0), (0, 0)]
        pad[axis] = (r + 1, r)
        cs = np.cumsum(np.pad(out, pad, mode="edge"), axis=axis)
        if axis == 1:
            out = (cs[:, k:] - cs[:, :-k]) / k
        else:
            out = (cs[k:, :] - cs[:-k, :]) / k
    return out.astype(np.float32)


def gauss(a: np.ndarray, sigma_cells: float) -> np.ndarray:
    if sigma_cells <= 0.3:
        return a
    w = math.sqrt(4 * sigma_cells ** 2 + 1)
    r = max(1, int(round((w - 1) / 2)))
    for _ in range(3):
        a = box_blur(a, r)
    return a


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0 + 1e-12), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- reliéf: sklon, stínování
def slope_deg(z: np.ndarray, dx_m: float) -> np.ndarray:
    gy, gx = np.gradient(z, dx_m)
    return np.degrees(np.arctan(np.hypot(gx, gy)))


def hillshade(z: np.ndarray, dx_m: float, az_deg=315.0, alt_deg=42.0, exag=1.6) -> np.ndarray:
    gy, gx = np.gradient(z * exag, dx_m)           # gy = d/d(řádek) = k jihu
    dzdx, dzdy_north = gx, -gy
    nx, ny, nz = -dzdx, -dzdy_north, np.ones_like(z)
    norm = np.sqrt(nx * nx + ny * ny + nz * nz)
    az, alt = math.radians(az_deg), math.radians(alt_deg)
    lx, ly, lz = math.sin(az) * math.cos(alt), math.cos(az) * math.cos(alt), math.sin(alt)
    return np.clip((nx * lx + ny * ly + nz * lz) / norm, 0.0, 1.0)


# ---------------------------------------------------------------- vrstevnice (marching squares)
_CASE_EDGES = {
    1: [("L", "B")], 2: [("B", "R")], 3: [("L", "R")], 4: [("T", "R")], 6: [("T", "B")], 7: [("T", "L")],
    8: [("T", "L")], 9: [("T", "B")], 11: [("T", "R")], 12: [("L", "R")], 13: [("B", "R")], 14: [("L", "B")],
}


def contour_lines(grid: Grid, z: np.ndarray, level: float):
    """Vrstevnice výšky `level` jako seznam polyline [(x_km, y_km), …] (uzavřené mají shodný první a poslední bod)."""
    a = z[:-1, :-1] >= level
    b = z[:-1, 1:] >= level
    c = z[1:, 1:] >= level
    d = z[1:, :-1] >= level
    case = a * 8 + b * 4 + c * 2 + d * 1
    ii, jj = np.nonzero((case > 0) & (case < 15))
    segs = []     # dvojice hran; hrana = ('h'|'v', řádek, sloupec)
    cs = case[ii, jj]
    for i, j, k in zip(ii.tolist(), jj.tolist(), cs.tolist()):
        edge = {"T": ("h", i, j), "B": ("h", i + 1, j), "L": ("v", i, j), "R": ("v", i, j + 1)}
        if k in (5, 10):
            center = (z[i, j] + z[i, j + 1] + z[i + 1, j + 1] + z[i + 1, j]) / 4 >= level
            if k == 5:      # TR + BL uvnitř
                pairs = [("T", "L"), ("B", "R")] if center else [("T", "R"), ("L", "B")]
            else:           # TL + BR uvnitř
                pairs = [("T", "R"), ("L", "B")] if center else [("T", "L"), ("B", "R")]
        else:
            pairs = _CASE_EDGES[k]
        for p, q in pairs:
            segs.append((edge[p], edge[q]))

    def point(e):
        t, i, j = e
        if t == "h":                           # hrana mezi (i,j) a (i,j+1)
            z1, z2 = z[i, j], z[i, j + 1]
            f = (level - z1) / (z2 - z1) if z2 != z1 else 0.5
            col, row = j + f, i
        else:                                  # hrana mezi (i,j) a (i+1,j)
            z1, z2 = z[i, j], z[i + 1, j]
            f = (level - z1) / (z2 - z1) if z2 != z1 else 0.5
            col, row = j, i + f
        return (grid.x0 + (col + 0.5) * grid.dx, grid.y0 + (row + 0.5) * grid.dx)

    adj: dict = {}
    for s, (p, q) in enumerate(segs):
        adj.setdefault(p, []).append(s)
        adj.setdefault(q, []).append(s)
    used = [False] * len(segs)
    lines = []
    for s0 in range(len(segs)):
        if used[s0]:
            continue
        used[s0] = True
        p, q = segs[s0]
        chain = [p, q]
        for end in (1, 0):                      # prodlužuj za oba konce
            while True:
                tail = chain[-1] if end == 1 else chain[0]
                nxt = None
                for s in adj.get(tail, []):
                    if not used[s]:
                        nxt = s
                        break
                if nxt is None:
                    break
                used[nxt] = True
                a2, b2 = segs[nxt]
                new = b2 if a2 == tail else a2
                if end == 1:
                    chain.append(new)
                else:
                    chain.insert(0, new)
        lines.append([point(e) for e in chain])
    return lines


def simplify(pts, tol: float):
    """Douglas–Peucker (iterativně) pro otevřenou polyline."""
    n = len(pts)
    if n < 3:
        return list(pts)
    keep = [False] * n
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    P = np.asarray(pts, dtype=np.float64)
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        pa, pb = P[a], P[b]
        seg = pb - pa
        L2 = float(seg @ seg)
        mid = P[a + 1:b]
        if L2 == 0:
            d = np.hypot(*(mid - pa).T)
        else:
            t = np.clip(((mid - pa) @ seg) / L2, 0, 1)
            proj = pa + t[:, None] * seg
            d = np.hypot(*(mid - proj).T)
        k = int(np.argmax(d))
        if d[k] > tol:
            m = a + 1 + k
            keep[m] = True
            stack.append((a, m))
            stack.append((m, b))
    return [tuple(p) for p, kp in zip(pts, keep) if kp]


def chaikin(pts, closed=False, iters=1):
    for _ in range(iters):
        out = []
        n = len(pts)
        rng = range(n if closed else n - 1)
        if not closed:
            out.append(pts[0])
        for i in rng:
            p, q = pts[i], pts[(i + 1) % n]
            out.append((0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]))
            out.append((0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1]))
        if not closed:
            out.append(pts[-1])
        pts = out
    return pts


def save_png8(arr: np.ndarray, path):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="L").save(path, optimize=True)


def save_png16(arr: np.ndarray, path):
    Image.fromarray(np.clip(arr, 0, 65535).astype(np.uint16)).save(path)
