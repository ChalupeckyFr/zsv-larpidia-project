"""Plán hlavního města (F7): dopravní graf uliční sítě z polyline (metry).

Postup: přidej polyline s atributy → `snap_ends` (prodlouží konce ke křižujícím ulicím) → `build` (průsečíky, dělení, uzly, hrany)
→ `prune` (odstraní krátké slepé výběžky a drobné izolované komponenty). Výsledek: uzly (id, u, v, stupeň) a hrany (uzly, délka, třída, geometrie).
"""
from __future__ import annotations

import math
from collections import defaultdict

import numpy as np

import cp_geom as G


class StreetGraph:
    def __init__(self, cell=96.0):
        self.polys: list[dict] = []
        self.cell = cell
        self.nodes: list[tuple[float, float]] = []
        self.edges: list[dict] = []

    def add(self, pts, **attrs):
        pts = [(float(p[0]), float(p[1])) for p in pts]
        if len(pts) >= 2 and G.length(pts) > 1.0:
            self.polys.append({"pts": pts, **attrs})

    # ---------------------------------------------------------------- prostorový hash segmentů
    def _segments(self):
        segs = []
        for pi, pl in enumerate(self.polys):
            pts = pl["pts"]
            for k in range(len(pts) - 1):
                segs.append((pi, k, pts[k], pts[k + 1]))
        return segs

    def _hash(self, segs):
        h = defaultdict(list)
        c = self.cell
        for si, (_, _, a, b) in enumerate(segs):
            x0, x1 = sorted((a[0], b[0]))
            y0, y1 = sorted((a[1], b[1]))
            for i in range(int(y0 // c), int(y1 // c) + 1):
                for j in range(int(x0 // c), int(x1 // c) + 1):
                    h[(i, j)].append(si)
        return h

    # ---------------------------------------------------------------- dosednutí a prodloužení koncových bodů
    def touch_ends(self, tol=1.0):
        """Konec polyline, který leží do `tol` m od jiné ulice, se posune přesně na ni (aby vznikla křižovatka)."""
        segs = self._segments()
        h = self._hash(segs)
        c = self.cell
        n = 0
        for pi, pl in enumerate(self.polys):
            for end in (0, -1):
                p = pl["pts"][end]
                best = None
                for i in range(int((p[1] - tol) // c), int((p[1] + tol) // c) + 1):
                    for j in range(int((p[0] - tol) // c), int((p[0] + tol) // c) + 1):
                        for si in h.get((i, j), []):
                            pj, _, a, b = segs[si]
                            if pj == pi:
                                continue
                            d, q, _ = G.nearest_on_polyline(p, [a, b])
                            if d < tol and (best is None or d < best[0]):
                                best = (d, q)
                if best and best[0] > 1e-9:
                    pl["pts"][end] = best[1]
                    n += 1
        return n

    def snap_ends(self, max_ext=16.0, min_gap=0.6):
        """Konec polyline, který nedosedá na jinou ulici, se prodlouží až k nejbližší ulici ve směru čáry (max_ext m)."""
        self.touch_ends()
        segs = self._segments()
        h = self._hash(segs)
        c = self.cell
        n_ext = 0
        for pi, pl in enumerate(self.polys):
            if pl.get("no_snap"):
                continue
            for end in (0, -1):
                pts = pl["pts"]
                p = pts[end]
                q = pts[1] if end == 0 else pts[-2]
                L = math.dist(p, q)
                if L < 1e-6:
                    continue
                d = ((p[0] - q[0]) / L, (p[1] - q[1]) / L)
                ext = float(pl.get("ext", max_ext))
                tip = (p[0] + d[0] * ext, p[1] + d[1] * ext)
                cand = set()
                x0, x1 = sorted((p[0], tip[0]))
                y0, y1 = sorted((p[1], tip[1]))
                for i in range(int(y0 // c), int(y1 // c) + 1):
                    for j in range(int(x0 // c), int(x1 // c) + 1):
                        cand.update(h.get((i, j), []))
                best = None
                for si in cand:
                    pj, _, a, b = segs[si]
                    if pj == pi:
                        continue
                    r = G.seg_intersect(p, tip, a, b)
                    if r and r[0] * max_ext >= min_gap * 0 and (best is None or r[0] < best[0]):
                        best = (r[0], r[2])
                    # už leží na ulici → nic neprodlužuj
                    if G.nearest_on_polyline(p, [a, b])[0] < min_gap:
                        best = (0.0, p)
                        break
                if best and best[0] > 0.0:
                    if end == 0:
                        pl["pts"].insert(0, best[1])
                    else:
                        pl["pts"].append(best[1])
                    n_ext += 1
        return n_ext

    # ---------------------------------------------------------------- průsečíky a dělení
    def build(self, snap=1.2):
        segs = self._segments()
        h = self._hash(segs)
        splits = defaultdict(list)           # (poly, seg) -> [t]
        seen = set()
        for si, (pi, k, a, b) in enumerate(segs):
            x0, x1 = sorted((a[0], b[0]))
            y0, y1 = sorted((a[1], b[1]))
            cand = set()
            for i in range(int(y0 // self.cell), int(y1 // self.cell) + 1):
                for j in range(int(x0 // self.cell), int(x1 // self.cell) + 1):
                    cand.update(h.get((i, j), []))
            for sj in cand:
                if sj <= si:
                    continue
                pj, kj, c2, d2 = segs[sj]
                if pj == pi and abs(kj - k) <= 1:
                    continue
                if (si, sj) in seen:
                    continue
                seen.add((si, sj))
                r = G.seg_intersect(a, b, c2, d2)
                if r:
                    splits[(pi, k)].append(r[0])
                    splits[(pj, kj)].append(r[1])
        # polyline → dělené úseky
        node_key = {}
        self.nodes = []

        def node(p):
            key = (round(p[0] / snap), round(p[1] / snap))
            for dk in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                kk = (key[0] + dk[0], key[1] + dk[1])
                if kk in node_key:
                    idx = node_key[kk]
                    if math.dist(self.nodes[idx], p) <= snap * 1.6:
                        return idx
            node_key[key] = len(self.nodes)
            self.nodes.append((float(p[0]), float(p[1])))
            return node_key[key]

        self.edges = []
        for pi, pl in enumerate(self.polys):
            pts = pl["pts"]
            events = []                              # (vzdálenost podél čáry, bod, je_řez)
            acc = 0.0
            for k in range(len(pts) - 1):
                a, b = pts[k], pts[k + 1]
                Lk = math.dist(a, b)
                events.append((acc, a, False))
                for t in splits.get((pi, k), []):
                    events.append((acc + t * Lk, (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), True))
                acc += Lk
            events.append((acc, pts[-1], False))
            events.sort(key=lambda e: e[0])
            cur = []
            for _, p, cut in events:
                if cur and math.dist(cur[-1], p) < 1e-6:
                    if cut and len(cur) >= 2:
                        self._emit(cur, pl, node)
                        cur = [p]
                    continue
                cur.append(p)
                if cut and len(cur) >= 2:
                    self._emit(cur, pl, node)
                    cur = [p]
            if len(cur) >= 2:
                self._emit(cur, pl, node)
        return self

    def _emit(self, pts, pl, node):
        a, b = node(pts[0]), node(pts[-1])
        L = G.length(pts)
        if a == b or L < 0.5:
            return
        self.edges.append({"a": a, "b": b, "pts": pts, "length": L, **{k: v for k, v in pl.items() if k != "pts"}})

    # ---------------------------------------------------------------- úklid
    def degrees(self):
        deg = defaultdict(int)
        for e in self.edges:
            deg[e["a"]] += 1
            deg[e["b"]] += 1
        return deg

    def dedupe(self):
        seen = {}
        out = []
        for e in self.edges:
            key = (min(e["a"], e["b"]), max(e["a"], e["b"]), round(e["length"] / 3.0))
            if key in seen:
                if _rank(e) > _rank(seen[key]):
                    out[out.index(seen[key])] = e
                    seen[key] = e
                continue
            seen[key] = e
            out.append(e)
        self.edges = out

    def prune(self, stub=14.0, min_comp_len=200.0, protect_classes=("A", "R1")):
        """Odstraní krátké slepé výběžky (stub m) a malé izolované komponenty."""
        for _ in range(6):
            deg = self.degrees()
            keep = []
            removed = 0
            for e in self.edges:
                dead = deg[e["a"]] == 1 or deg[e["b"]] == 1
                if dead and e["length"] < stub and e.get("cls") not in protect_classes:
                    removed += 1
                    continue
                keep.append(e)
            self.edges = keep
            if not removed:
                break
        # komponenty
        parent = list(range(len(self.nodes)))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for e in self.edges:
            ra, rb = find(e["a"]), find(e["b"])
            if ra != rb:
                parent[ra] = rb
        length = defaultdict(float)
        atlas = set()
        for e in self.edges:
            length[find(e["a"])] += e["length"]
            if e.get("atlas_id"):
                atlas.add(find(e["a"]))                       # úseky silnic atlasu se nemažou (geometrie atlasu zůstává celá)
        big = max(length, key=length.get) if length else None
        self.edges = [e for e in self.edges if length[find(e["a"])] >= min_comp_len or find(e["a"]) == big or find(e["a"]) in atlas]
        self.components = len({find(e["a"]) for e in self.edges})
        return self


def _rank(e):
    return {"A": 5, "R1": 5, "B": 4, "S": 4, "P": 3, "C": 2, "L": 1}.get(e.get("cls"), 0)
