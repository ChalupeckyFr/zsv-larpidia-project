"""Načtení prostředí pro lidskou vrstvu (F3) z uložených výstupů F2: DEM, jezero, toky, pokryv, pobřeží."""
from __future__ import annotations

import json
import math

import numpy as np
from PIL import Image, ImageDraw

import canon
import geom
import pathfind
import raster
import relief_model as rm
from canon import ATLAS

RELIEF = ATLAS / "current" / "relief"


class World:
    def __init__(self):
        self.g = raster.Grid(0.02)
        self.o = canon.load_outline()
        self.rows = {r["id"]: r for r in canon.table_rows()}
        im = Image.open(RELIEF / "dem_20m_u16.png")
        self.z = np.asarray(im).astype(np.float32) / 100.0
        self.cls = np.asarray(Image.open(RELIEF / "landcover_20m.png"))
        self.land_main = raster.rasterize(self.g, [self.o["main"]])
        self.land_para = raster.rasterize(self.g, [self.o["para"]])
        self.land = self.land_main | self.land_para
        hy = json.loads((RELIEF / "hydrography.geojson").read_text(encoding="utf-8"))
        self.hydro = hy
        self.rivers = []
        self.lake_poly = None
        self.waterfall = None
        for f in hy["features"]:
            p = f["properties"]
            if f["geometry"]["type"] == "LineString":
                self.rivers.append({"id": p["id"], "part": p["part"], "kind": p["kind"], "pts": [tuple(c) for c in f["geometry"]["coordinates"]]})
            elif f["geometry"]["type"] == "Polygon":
                self.lake_poly = [tuple(c) for c in f["geometry"]["coordinates"][0][:-1]]
                self.lake_level = p["level_m_model"]
            elif f["geometry"]["type"] == "Point":
                self.waterfall = tuple(f["geometry"]["coordinates"])
        self.lake = raster.rasterize(self.g, [self.lake_poly])
        rim = Image.new("L", (self.g.nx, self.g.ny), 0)
        d = ImageDraw.Draw(rim)
        for r in self.rivers:
            d.line([self.g.to_px(x, y) for x, y in r["pts"]], fill=255, width=2)
        self.river = np.asarray(rim) > 127
        pts = []
        for poly in (self.o["main"], self.o["para"]):
            pts.extend(poly[::2])
        self.coast_pts = np.array(pts, dtype=np.float32)
        self.D = raster.coarse_nearest(self.g, self.coast_pts, factor=3)
        self.env = pathfind.Env(self.g, self.z, self.land, self.lake, self.river, self.D)
        self.S = raster.slope_deg(self.z, self.g.dx * 1000.0)
        self.para_c = geom.centroid(self.o["para"])

    # ---- pomocné
    def zat(self, x, y):
        i, j = self.g.cell_of(x, y)
        return float(self.z[i, j])

    def slope_at(self, x, y):
        i, j = self.g.cell_of(x, y)
        return float(self.S[i, j])

    def cls_at(self, x, y):
        i, j = self.g.cell_of(x, y)
        return int(self.cls[i, j])

    def on_land(self, x, y):
        i, j = self.g.cell_of(x, y)
        return bool(self.land[i, j])

    def in_lake(self, x, y):
        i, j = self.g.cell_of(x, y)
        return bool(self.lake[i, j])

    def d_coast(self, x, y):
        i, j = self.g.cell_of(x, y)
        return float(self.D[i, j])

    def pos(self, rid):
        r = self.rows[rid]
        return (r["x_km"], r["y_km"])

    def para(self, u, v):
        return rm.para_to_world(u, v, self.para_c)

    def probe(self, label, x, y):
        return (f"{label:<22s} ({x:6.2f},{y:6.2f}) land={self.on_land(x, y)!s:5} lake={self.in_lake(x, y)!s:5} "
                f"z={self.zat(x, y):6.1f} slope={self.slope_at(x, y):5.1f} Dcoast={self.d_coast(x, y):4.2f} lc={self.cls_at(x, y)}")
