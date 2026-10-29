"""Viditelnost z DEM (přímá viditelnost) a pomocné funkce pro foto/video vodítko v registru (F4)."""
from __future__ import annotations

import math

import numpy as np

import hydro

COMPASS = ["S", "SV", "V", "JV", "J", "JZ", "Z", "SZ"]     # sever nahoře; y roste na jih


def bearing_deg(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    return (math.degrees(math.atan2(dx, -dy)) + 360.0) % 360.0       # 0° = sever, 90° = východ


def compass_cs(deg):
    return COMPASS[int(((deg + 22.5) % 360) // 45)]


def visible(world, a, b, h_obs=2.0, h_tgt=0.0, samples=90):
    """Je cíl b vidět z bodu a (terén jako jediná překážka)?"""
    za = world.zat(*a) + h_obs
    zb = world.zat(*b) + h_tgt
    n = max(8, min(samples, int(math.dist(a, b) / 0.06)))
    xs = np.linspace(a[0], b[0], n + 1)[1:-1]
    ys = np.linspace(a[1], b[1], n + 1)[1:-1]
    if len(xs) == 0:
        return True
    zt = hydro.bilinear(world.z, world.g, xs, ys)
    zl = za + (zb - za) * (np.arange(1, n) / n)
    return bool(np.all(zt < zl - 0.5))
