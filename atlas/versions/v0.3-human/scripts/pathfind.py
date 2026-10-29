"""Hledání tras (A*) nad nákladovou mapou terénu: silnice, železnice, stezky sledují reliéf.

Nákladová mapa je na hrubší mřížce (60 m = 3 × 20 m). Trasy se pak vyhlazují a zjednodušují.
"""
from __future__ import annotations

import heapq
import math

import numpy as np

import raster
from raster import smoothstep

INF = np.inf
_N8 = [(-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
       (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)), (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))]


class Env:
    """Prostředí: DEM, masky a odvozená pole na hrubé mřížce."""

    def __init__(self, grid: raster.Grid, z: np.ndarray, land: np.ndarray, lake: np.ndarray, river: np.ndarray, D: np.ndarray, factor: int = 3):
        self.g = grid
        self.f = factor
        self.cell = grid.dx * factor
        ny, nx = (grid.ny // factor) * factor, (grid.nx // factor) * factor

        def blk(a, op="mean"):
            a = a[:ny, :nx].astype(np.float32)
            r = a.reshape(ny // factor, factor, nx // factor, factor)
            return r.mean(axis=(1, 3)) if op == "mean" else (r.max(axis=(1, 3)) if op == "max" else r.min(axis=(1, 3)))

        self.z = blk(z)
        self.land = blk(land.astype(np.float32), "min") > 0.5
        self.lake = blk(lake.astype(np.float32), "max") > 0.5
        self.river = blk(river.astype(np.float32), "max") > 0.5
        self.D = blk(D)
        gy, gx = np.gradient(self.z, self.cell * 1000.0)
        self.slope = np.degrees(np.arctan(np.hypot(gx, gy)))
        self.ny, self.nx = self.z.shape

    def cell_of(self, x, y):
        i = int((y - self.g.y0) / self.cell)
        j = int((x - self.g.x0) / self.cell)
        return min(max(i, 0), self.ny - 1), min(max(j, 0), self.nx - 1)

    def xy(self, i, j):
        return (self.g.x0 + (j + 0.5) * self.cell, self.g.y0 + (i + 0.5) * self.cell)

    def snap(self, x, y, cost, radius=8):
        """Nejbližší průchozí buňka k bodu."""
        i0, j0 = self.cell_of(x, y)
        if np.isfinite(cost[i0, j0]):
            return i0, j0
        best, bd = None, 1e9
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                i, j = i0 + di, j0 + dj
                if 0 <= i < self.ny and 0 <= j < self.nx and np.isfinite(cost[i, j]):
                    d = di * di + dj * dj
                    if d < bd:
                        best, bd = (i, j), d
        return best


def astar(cost: np.ndarray, start, goal):
    """A* po 8 sousedech. cost >= 1 (inf = neprůchozí). Vrací seznam buněk (i, j) nebo None."""
    ny, nx = cost.shape
    gs = np.full(cost.shape, np.inf, dtype=np.float64)
    par = np.full(cost.shape + (2,), -1, dtype=np.int32)
    gs[start] = 0.0
    gi, gj = goal
    h = lambda i, j: math.hypot(i - gi, j - gj)
    heap = [(h(*start), 0.0, start[0], start[1])]
    while heap:
        f, g, i, j = heapq.heappop(heap)
        if (i, j) == (gi, gj):
            break
        if g > gs[i, j] + 1e-9:
            continue
        ci = cost[i, j]
        for di, dj, w in _N8:
            a, b = i + di, j + dj
            if a < 0 or b < 0 or a >= ny or b >= nx:
                continue
            cb = cost[a, b]
            if not np.isfinite(cb):
                continue
            ng = g + w * 0.5 * (ci + cb)
            if ng < gs[a, b]:
                gs[a, b] = ng
                par[a, b] = (i, j)
                heapq.heappush(heap, (ng + h(a, b), ng, a, b))
    if not np.isfinite(gs[gi, gj]):
        return None
    path = [(gi, gj)]
    while path[-1] != tuple(start):
        pi, pj = par[path[-1]]
        path.append((int(pi), int(pj)))
    return path[::-1]


def route(env: Env, cost: np.ndarray, points, smooth_iters=2, simplify_m=12.0, start_exact=True):
    """Trasa přes po sobě jdoucí body (x, y) v km. Vrací vyhlazenou polyline [(x, y)]."""
    cells = [env.snap(x, y, cost) for x, y in points]
    out = []
    for (a, b), (p, q) in zip(zip(cells, cells[1:]), zip(points, points[1:])):
        path = astar(cost, a, b)
        if path is None:
            raise RuntimeError(f"Trasu {p} → {q} se nepodařilo najít")
        pts = [env.xy(i, j) for i, j in path]
        if out:
            pts = pts[1:]
        out.extend(pts)
    if start_exact and out:
        out[0] = tuple(points[0])
        out[-1] = tuple(points[-1])
    if len(out) > 3:
        out = raster.simplify(out, 0.03)
        out = raster.chaikin(out, closed=False, iters=smooth_iters)
        out = raster.simplify(out, simplify_m / 1000.0)
    return out


# ---------------------------------------------------------------- nákladové mapy
def road_cost(env: Env, bonus_mask=None, coast_target=None, coast_w=4.0, forest_mask=None, max_slope=22.0,
              zmax=None, tunnel_slope=None, tunnel_cost=7.0):
    """Cena silnice. Strmé buňky (max_slope < sklon ≤ tunnel_slope) lze projet jen jako tunel (vyšší cena)."""
    c = 1.0 + (env.slope / 6.0) ** 2
    if tunnel_slope:
        c = np.where((env.slope > max_slope) & (env.slope <= tunnel_slope), tunnel_cost + (env.slope / 12.0) ** 2, c)
        c = np.where(env.slope > tunnel_slope, np.inf, c)
    else:
        c = np.where(env.slope > max_slope, np.inf, c)
    if zmax is not None:
        c = np.where(env.z > zmax, np.inf, c)
    c = np.where(~env.land | env.lake, np.inf, c)
    c = np.where(env.river & np.isfinite(c), c + 7.0, c)
    if forest_mask is not None:
        c = np.where(forest_mask & np.isfinite(c), c + 0.25, c)
    if coast_target is not None:
        c = np.where(np.isfinite(c), c + coast_w * np.abs(env.D - coast_target), c)
    if bonus_mask is not None:
        c = np.where(bonus_mask & np.isfinite(c), np.maximum(1.0, c * 0.40), c)
    return c


def rail_cost(env: Env, bonus_mask=None, max_slope=9.0):
    c = 1.0 + (env.slope / 2.4) ** 2
    c = np.where(env.slope > max_slope, np.inf, c)
    c = np.where(~env.land | env.lake, np.inf, c)
    c = np.where(env.river & np.isfinite(c), c + 12.0, c)
    if bonus_mask is not None:
        c = np.where(bonus_mask & np.isfinite(c), np.maximum(1.0, c * 0.5), c)
    return c


def trail_cost(env: Env, max_slope=30.0):
    c = 1.0 + (env.slope / 10.0) ** 2
    c = np.where(env.slope > max_slope, np.inf, c)
    c = np.where(~env.land | env.lake, np.inf, c)
    c = np.where(env.river & np.isfinite(c), c + 1.5, c)
    return c


def mark_path(env: Env, mask: np.ndarray, pts, width_cells=1):
    """Označí buňky podél polyline v hrubé masce (pro bonus slučování sítí)."""
    for a, b in zip(pts, pts[1:]):
        n = max(2, int(math.dist(a, b) / env.cell * 1.5))
        for k in range(n + 1):
            x = a[0] + (b[0] - a[0]) * k / n
            y = a[1] + (b[1] - a[1]) * k / n
            i, j = env.cell_of(x, y)
            mask[max(0, i - width_cells + 1):i + width_cells, max(0, j - width_cells + 1):j + width_cells] = True
    return mask
