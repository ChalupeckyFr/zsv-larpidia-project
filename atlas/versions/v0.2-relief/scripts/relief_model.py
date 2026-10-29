"""Výškový model Larpidie a Paralandu (analytický, deterministický). VŠE JE PRACOVNÍ NÁVRH (proposed).

Pevné kotvy z bible: nejvyšší vrchol 500–600 m (pracovně 560 m), třívrcholové pohoří (jedna prudší sjezdovková hora,
jeden zaoblený vrchol), 10m pobřežní sráz s vyhlídkou (N-01), jeskyně, vodopád a přehrada v západním vnitrozemí.
Ostatní výšky jsou modelové (atlas_new).
"""
from __future__ import annotations

import math

import numpy as np

import canon
import geom
import raster
from raster import smoothstep

PEAK_TARGETS = {"M-01": 560.0, "M-02": 510.0, "M-03": 440.0}   # M-01 pracovní z bible; ostatní návrh
TYPE_CODE = {"cliff": 0, "rocky": 1, "mixed": 2, "beach": 3, "harbor": 4, "industrial": 5}
# (c0 = podíl výšky přímo na pobřeží, w = šířka náběhu v km)
EDGE = {0: (0.45, 0.10), 1: (0.30, 0.25), 2: (0.10, 0.50), 3: (0.0, 1.00), 4: (0.0, 0.60), 5: (0.0, 0.70)}

NOISE_SEED = 20261023
PARA_LOCAL_ROT = 24.0
# Paraland: místní soustava (u podél delší osy, v kolmo na jih), vůči těžišti
PARA_FEATURES = {
    "hill_east": (1.45, -0.15, 128.0, 0.95, 0.80),    # u, v, výška, σu, σv
    "hill_east2": (0.70, 0.55, 82.0, 0.60, 0.55),
    "castle_hill": (-1.45, -1.30, 58.0, 0.40, 0.35),
}


def egauss(X, Y, cx, cy, sx, sy, rot_deg=0.0):
    a = math.radians(rot_deg)
    c, s = math.cos(a), math.sin(a)
    u = (X - cx) * c + (Y - cy) * s
    v = -(X - cx) * s + (Y - cy) * c
    return np.exp(-0.5 * ((u / sx) ** 2 + (v / sy) ** 2))


def ridge(X, Y, p, q, hp, hq, sigma):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L2 = dx * dx + dy * dy
    t = np.clip(((X - p[0]) * dx + (Y - p[1]) * dy) / L2, 0.0, 1.0)
    d2 = (X - (p[0] + t * dx)) ** 2 + (Y - (p[1] + t * dy)) ** 2
    return (hp + (hq - hp) * t) * np.exp(-d2 / (2 * sigma ** 2))


def para_to_world(u, v, centroid):
    a = math.radians(PARA_LOCAL_ROT)
    return (centroid[0] + u * math.cos(a) - v * math.sin(a), centroid[1] + u * math.sin(a) + v * math.cos(a))


class Terrain:
    """Připraví pole (maska souše, vzdálenost k moři, typ pobřeží) a umí postavit DEM."""

    def __init__(self, grid: raster.Grid, outline: dict, rows: dict):
        self.g = grid
        self.o = outline
        self.rows = rows
        self.X, self.Y = grid.mesh()
        self.main_mask = raster.rasterize(grid, [outline["main"]])
        self.para_mask = raster.rasterize(grid, [outline["para"]])
        self.land = self.main_mask | self.para_mask
        # body pobřeží s typy (každý 2. vrchol ≈ 80 m)
        pts, types = [], []
        for poly, ty in ((outline["main"], outline["main_types"]), (outline["para"], outline["para_types"])):
            for i in range(0, len(poly), 2):
                pts.append(poly[i])
                types.append(TYPE_CODE[ty[i]])
        self.coast_pts = np.array(pts, dtype=np.float32)
        self.coast_types = np.array(types, dtype=np.int8)
        self.D, idx = raster.coarse_nearest(grid, self.coast_pts, factor=3, want_index=True)
        self.type_field = self.coast_types[idx]
        c0 = np.take(np.array([EDGE[k][0] for k in range(6)], dtype=np.float32), self.type_field)
        w = np.take(np.array([EDGE[k][1] for k in range(6)], dtype=np.float32), self.type_field)
        self.c0 = raster.gauss(c0, 8)
        self.w = raster.gauss(w, 8)
        self.para_centroid = geom.centroid(outline["para"])
        self.noise = raster.fbm(grid, NOISE_SEED, [(2.2, 1.0), (0.9, 0.55), (0.35, 0.28), (0.12, 0.12)])
        self.noise_low = raster.fbm(grid, NOISE_SEED + 1, [(1.8, 1.0), (0.8, 0.45)])
        rn = raster.fbm(grid, NOISE_SEED + 2, [(0.75, 1.0), (0.33, 0.55), (0.15, 0.25)])
        self.ridged = np.clip(1.0 - np.abs(rn) / 1.6, 0.0, 1.0).astype(np.float32)   # hřebenový šum 0..1
        self.rmf = raster.gauss(raster.ridged_mf(grid, NOISE_SEED + 3, cell0=2.4, octaves=4, gain=0.5), 4)

    # ------------------------------------------------------------ pomocné
    def at(self, arr, x, y):
        i, j = self.g.cell_of(x, y)
        return float(arr[i, j])

    def pos(self, rid):
        r = self.rows[rid]
        return (r["x_km"], r["y_km"])

    # ------------------------------------------------------------ DEM
    def build(self, H, params=None):
        p = {"dome": 150.0, "dome2": 80.0, "rough": 0.11, "rough0": 4.5, **(params or {})}
        X, Y, D = self.X, self.Y, self.D
        M1, M2, M3 = self.pos("M-01"), self.pos("M-02"), self.pos("M-03")
        # nížinná základna: pozvolný vzestup od moře
        L = 3.0 + 20.0 * (1 - np.exp(-D / 3.0))
        # široká západní klenba + severní pahorkatina
        U = p["dome"] * egauss(X, Y, 6.8, 7.2, 4.6, 4.2) + p["dome2"] * egauss(X, Y, 11.5, 4.2, 2.8, 1.5, -15)
        # pohoří (M-01 nejvyšší, M-02 prudší, M-03 zaoblený) + hřbety a výběžek k jeskyni
        P1 = H["M-01"] * egauss(X, Y, M1[0], M1[1], 1.35, 1.05, -20)
        P2 = H["M-02"] * egauss(X, Y, M2[0], M2[1], 0.80, 0.95, 0)
        P3 = H["M-03"] * egauss(X, Y, M3[0], M3[1], 1.45, 1.25, 30)
        R12 = ridge(X, Y, M1, M2, H["M-01"], H["M-02"], 0.62) * 0.78
        R13 = ridge(X, Y, M1, M3, H["M-01"], H["M-03"], 0.75) * 0.66
        SP = ridge(X, Y, M2, (9.85, 7.10), H["M-02"] * 0.72, 150.0, 0.70)
        m = raster.gauss(np.maximum.reduce([P1, P2, P3, R12, R13, SP]), 5)
        # Paraland: kopce
        para = np.zeros_like(X)
        for name, (u, v, h, su, sv) in PARA_FEATURES.items():
            cx, cy = para_to_world(u, v, self.para_centroid)
            para += h * egauss(X, Y, cx, cy, su, sv, PARA_LOCAL_ROT)
        z = L + U + m + para
        # drsnost: nulová na vrcholech
        peak_guard = np.ones_like(X)
        for pk in (M1, M2, M3):
            peak_guard *= 1 - np.exp(-(((X - pk[0]) ** 2 + (Y - pk[1]) ** 2) / (0.45 ** 2)))
        hi_guard = 1.0 - smoothstep(330.0, 500.0, U + m)         # nejvyšší polohy zůstávají hladké → maximum = M-01
        amp = (p["rough0"] + p["rough"] * (U + m + para)) * peak_guard * (0.25 + 0.75 * hi_guard)
        z = z + amp * self.noise * 0.35
        # hřebenový šum: ostré hřbety a strže jen v horách; mírné zvlnění v nížinách
        mw = smoothstep(110.0, 360.0, U + m) * peak_guard
        z = z + 16.0 * mw * (self.ridged - 0.42) * hi_guard
        # hřebenový multifraktál: ubírá z výšky v úžlabích, hřbety zůstávají (maximum zůstává na M-01)
        gully = 1.0 - self.rmf
        z = z * (1.0 - 0.34 * smoothstep(120.0, 380.0, U + m) * peak_guard * np.clip((gully - 0.15) / 0.85, 0, 1) ** 1.15)
        z = z + 7.0 * smoothstep(0.2, 3.0, D) * (1.0 - mw) * self.noise_low * 0.5 * peak_guard
        # útesový mys N-01 je nízký (~10–14 m)
        n01 = self.pos("N-01")
        dn = np.sqrt(((X - n01[0]) / 1.35) ** 2 + ((Y - n01[1]) / 0.85) ** 2) * (1.0 + 0.22 * self.noise_low)   # protáhlý nepravidelný mys
        z = z * (0.05 + 0.95 * smoothstep(0.30, 1.9, dn))
        z = z + 8.0 * np.exp(-(dn / 0.45) ** 2)
        # pobřežní profil (útes / skála / pláž), vyhlazený
        edge = self.c0 + (1 - self.c0) * smoothstep(0.0, 1.0, D / np.maximum(self.w, 0.05))
        edge = raster.gauss(edge.astype(np.float32), 3)
        z = z * edge
        z = np.where(self.land, np.maximum(z, 0.0), 0.0).astype(np.float32)
        # nížiny bez drobných jamek: vyhlazení jen pod ~80 m (normalizovaná konvoluce na souši)
        lf = self.land.astype(np.float32)
        zb = raster.gauss(z * lf, 6) / np.maximum(raster.gauss(lf, 6), 1e-3)
        w_low = 1.0 - smoothstep(30.0, 90.0, z)
        z = np.where(self.land, z * (1 - w_low) + zb * w_low, 0.0).astype(np.float32)
        return z

    def calibrate(self, params=None):
        H = dict(PEAK_TARGETS)
        base = {"M-01": 560.0, "M-02": 510.0, "M-03": 440.0}
        for _ in range(14):
            z = self.build(H, params)
            for k in H:
                got = self.at(z, *self.pos(k))
                H[k] += (base[k] - got) * 0.9
        return H, self.build(H, params)
