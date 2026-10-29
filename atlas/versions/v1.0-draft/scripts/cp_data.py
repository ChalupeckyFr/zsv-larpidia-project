"""Plán hlavního města (F7): rámec, lokální metrický model a načtení dat atlasu do metrů.

Lokální soustava plánu: u = východ (m), v = jih (m), počátek v severozápadním rohu okna (x = 13,10 km, y = 10,30 km atlasu).
Okno 5 940 × 4 200 m = list A2 (594 × 420 mm) v měřítku 1 : 10 000; 1 jednotka SVG = 1 m.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

import atlas_svg as A
import human_env as he
import cp_geom as G
from canon import ATLAS

CUR = ATLAS / "current"
PLAN_ID = "CP-01"
X0_KM, Y0_KM = 13.10, 10.30
W_M, H_M = 5940.0, 4200.0
CELL = 2.0                                  # m, pracovní rastr
NX, NY = int(W_M / CELL), int(H_M / CELL)


def to_m(p):
    return ((p[0] - X0_KM) * 1000.0, (p[1] - Y0_KM) * 1000.0)


def to_km(p):
    return (X0_KM + p[0] / 1000.0, Y0_KM + p[1] / 1000.0)


def to_px(u, v):
    return (u / CELL, v / CELL)


def in_win(p, pad=0.0):
    return -pad <= p[0] <= W_M + pad and -pad <= p[1] <= H_M + pad


def window_runs(pts, pad=60.0):
    """Rozdělí polyline na souvislé úseky uvnitř okna (s přesahem `pad` m)."""
    runs, cur = [], []
    for p in pts:
        if in_win(p, pad):
            cur.append(p)
        else:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


class City:
    """Data atlasu přepočtená do lokálních metrů plánu."""

    def __init__(self):
        self.D = A.Data()
        self.W = he.World()
        D = self.D
        self.coast = [to_m(p) for p in D.o["main"]]
        self.beaches = [[to_m(p) for p in A.ring(f["geometry"]["coordinates"][0])] for f in D.coast if f["properties"]["class"] == "beach"]
        self.settle_rings = [[to_m(p) for p in A.ring(f["geometry"]["coordinates"][0])] for f in D.settle if f["properties"]["id"] == "C-01"]
        self.roads = []
        for f in D.roads:
            pr = f["properties"]
            for run in window_runs([to_m(q) for q in f["geometry"]["coordinates"]]):
                self.roads.append({"id": pr["id"], "class": pr["class"], "section": pr["section"], "pts": run})
        self.rails = []
        for f in D.rail:
            pr = f["properties"]
            for run in window_runs([to_m(q) for q in f["geometry"]["coordinates"]]):
                self.rails.append({"line": pr["line"], "section": pr["section"], "name": pr.get("name_cs"), "pts": run})
        st = json.loads((CUR / "human" / "rail_stations.geojson").read_text(encoding="utf-8"))
        self.stations = []
        for f in st["features"]:
            u, v = to_m(f["geometry"]["coordinates"])
            if in_win((u, v), 10.0):
                self.stations.append({**f["properties"], "u": u, "v": v})
        self.basin = None
        self.moles = []
        self.harbor_pt = None
        for f in D.pa:
            pr, gm = f["properties"], f["geometry"]
            if pr["id"] != "C-02":
                continue
            if gm["type"] == "Point":
                self.harbor_pt = to_m(gm["coordinates"])
            elif pr.get("kind") == "harbor_basin":
                self.basin = [to_m(p) for p in A.ring(gm["coordinates"][0])]
            elif pr.get("kind") == "breakwater":
                self.moles.append({"part": pr.get("part"), "pts": [to_m(p) for p in gm["coordinates"]]})
        self.harbor_water = self._harbor_water()
        self.ferry = None
        for f in D.trails:
            if f["properties"]["id"] == "FERRY-1":
                self.ferry = [to_m(q) for q in f["geometry"]["coordinates"]]
        reg = json.loads((CUR / "registry" / "places.json").read_text(encoding="utf-8"))
        self.reg = {o["id"]: o for o in reg["objects"]}
        self.z = self._dem()

    def _harbor_water(self):
        """Vodní plocha přístavu pro kresbu plánu: pobřeží mezi kořeny vlnolamů, východní vlnolam, vjezd a západní vlnolam (pánev z atlasu zůstává beze změny v registru)."""
        ma = next(m["pts"] for m in self.moles if m["part"] == "mole_a")
        mb = next(m["pts"] for m in self.moles if m["part"] == "mole_b")
        u0, u1 = mb[0][0], ma[0][0]
        coast = sorted((q for q in self.coast if u0 <= q[0] <= u1 and q[1] > 3300.0), key=lambda q: q[0])
        return coast + list(ma) + list(reversed(mb))

    def _dem(self):
        """Výška terénu (m n. m.) v okně na rastru CELL m (bikubicky z 20m DEM atlasu)."""
        g = self.W.g
        x0 = (X0_KM - g.x0) / g.dx
        y0 = (Y0_KM - g.y0) / g.dx
        x1 = x0 + (W_M / 1000.0) / g.dx
        y1 = y0 + (H_M / 1000.0) / g.dx
        im = Image.fromarray(self.W.z.astype(np.float32), mode="F")
        return np.asarray(im.resize((NX, NY), Image.BICUBIC, box=(x0, y0, x1, y1))).astype(np.float32)

    # ---- pomocné rastry
    def land_mask(self):
        return G.draw_mask((NY, NX), to_px, polys=[self.coast])

    def station(self, sid):
        return next(s for s in self.stations if s["id"] == sid)

    def road(self, rid):
        return [r for r in self.roads if r["id"] == rid]

    def z_at(self, u, v):
        i = min(NY - 1, max(0, int(v / CELL)))
        j = min(NX - 1, max(0, int(u / CELL)))
        return float(self.z[i, j])


def frame_json():
    return {
        "id": PLAN_ID,
        "title": "Larpington – podklad plánu hlavního města (návrh)",
        "status": "proposed",
        "local_system": "u = východ (m), v = jih (m); počátek v SZ rohu okna",
        "origin_atlas_km": {"x": X0_KM, "y": Y0_KM},
        "size_m": {"w": W_M, "h": H_M},
        "sheet": "A2 594 × 420 mm, měřítko 1 : 10 000 (1 jednotka SVG = 1 m)",
        "convert": "x_km = 13.10 + u/1000 ; y_km = 10.30 + v/1000",
        "work_raster_cell_m": CELL,
    }
