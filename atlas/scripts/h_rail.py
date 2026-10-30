"""Železnice L1, L2, L3 (F3). NÁVRH (proposed): kanon určuje role linek, jeskyni/vodopád na L1, podmořské napojení Paralandu a ~3 přestupy L2↔L3.

L1 Skyline Experience – vyvýšená zážitková trať z města k přehradě, vodopádu a jeskyní (koncová smyčka ~¾ obvodu) k horské stanici.
L2 Heritage Connect   – povrchová elektrická dráha městečka ↔ průmysl ↔ letiště ↔ severní města.
L3 Metro Blue         – převážně podzemní okruh hlavního města + větev pod průlivem na Paraland (krátká prosklená galerie).
"""
from __future__ import annotations

import math

import numpy as np

import geom
import pathfind
import raster
from raster import smoothstep

LINE_STYLE = {"L1": {"name": "Skyline Experience", "color": "#d9531e"}, "L2": {"name": "Heritage Connect", "color": "#2f7d4f"},
              "L3": {"name": "Metro Blue", "color": "#1f5fbf"}}

# společné uzly (přestupy) v hlavním městě
HUB_W = (14.15, 11.95)
HUB_N = (15.90, 10.95)
HUB_E = (17.65, 12.05)
HUB_S = (16.10, 13.05)


def best_spot(world, x, y, radius=0.4, slope_max=5.0, min_river=0.07, need_land=True):
    """Nejbližší vhodné místo k bodu (rovné, na souši, mimo jezero a mimo koryto)."""
    g = world.g
    best, bd = (x, y), 1e9
    n = int(radius / g.dx)
    i0, j0 = g.cell_of(x, y)
    for di in range(-n, n + 1, 2):
        for dj in range(-n, n + 1, 2):
            i, j = i0 + di, j0 + dj
            if not (0 <= i < g.ny and 0 <= j < g.nx):
                continue
            if need_land and not world.land[i, j]:
                continue
            if world.lake[i, j] or world.S[i, j] > slope_max:
                continue
            px, py = g.x0 + (j + 0.5) * g.dx, g.y0 + (i + 0.5) * g.dx
            if min(math.dist((px, py), q) for r in world.rivers for q in r["pts"][::3]) < min_river:
                continue
            d = math.dist((px, py), (x, y))
            if d < bd:
                best, bd = (px, py), d
    return best


def inward_normal_at(poly, p):
    d, q, i = geom.nearest_on_poly(p, poly)
    a, b = poly[i], poly[(i + 1) % len(poly)]
    tx, ty = b[0] - a[0], b[1] - a[1]
    L = math.hypot(tx, ty) or 1.0
    return (-(ty / L), tx / L)          # vnitřní normála pro polygon po směru hod. (y dolů)


def chord_mid(poly, p, direction, span=2.0, step=0.02):
    """Střed úsečky souše kolmé na `direction` procházející p (nebo None)."""
    px, py = -direction[1], direction[0]
    lo = hi = None
    k = 0.0
    inside = geom.point_in_poly(p, poly)
    if not inside:
        # hledej nejbližší vnitřní bod
        for kk in np.arange(0.0, span, step):
            for s in (1, -1):
                q = (p[0] + px * kk * s, p[1] + py * kk * s)
                if geom.point_in_poly(q, poly):
                    p = q
                    inside = True
                    break
            if inside:
                break
        if not inside:
            return None
    lo = hi = 0.0
    while hi < span and geom.point_in_poly((p[0] + px * (hi + step), p[1] + py * (hi + step)), poly):
        hi += step
    while -lo < span and geom.point_in_poly((p[0] + px * (lo - step), p[1] + py * (lo - step)), poly):
        lo -= step
    m = (lo + hi) / 2
    return (p[0] + px * m, p[1] + py * m)


def peninsula_centerline(poly, start, tip, step=0.15):
    pts = [start]
    p = start
    d = np.array([tip[0] - start[0], tip[1] - start[1]])
    d = d / np.linalg.norm(d)
    for _ in range(40):
        q = (p[0] + d[0] * step, p[1] + d[1] * step)
        m = chord_mid(poly, q, (d[0], d[1]))
        if m is None:
            break
        pts.append(m)
        nd = np.array([tip[0] - m[0], tip[1] - m[1]])
        if np.linalg.norm(nd) < step * 1.2:
            break
        nd = nd / np.linalg.norm(nd)
        d = 0.6 * d + 0.4 * nd
        d = d / np.linalg.norm(d)
        p = m
    return pts


def sample_z(world, pts):
    return np.array([world.zat(x, y) for x, y in pts], dtype=np.float64)


def dense(pts, step=0.02):
    out = []
    for a, b in zip(pts, pts[1:]):
        L = math.dist(a, b)
        k = max(1, int(L / step))
        for i in range(k):
            out.append((a[0] + (b[0] - a[0]) * i / k, a[1] + (b[1] - a[1]) * i / k))
    out.append(pts[-1])
    return out


def chainage(pts):
    s = [0.0]
    for a, b in zip(pts, pts[1:]):
        s.append(s[-1] + math.dist(a, b))
    return np.array(s)


def track_profile(s, zt, gmax=0.06, smooth_km=0.5):
    ds = float(np.mean(np.diff(s))) if len(s) > 1 else 0.02
    sig = max(0.5, smooth_km / ds)
    r = int(3 * sig)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sig) ** 2)
    k /= k.sum()
    z = np.convolve(np.pad(zt, r, mode="edge"), k, mode="valid")
    g = gmax * ds * 1000.0
    for i in range(1, len(z)):
        z[i] = min(max(z[i], z[i - 1] - g), z[i - 1] + g)
    for i in range(len(z) - 2, -1, -1):
        z[i] = min(max(z[i], z[i + 1] - g), z[i + 1] + g)
    return z


def classify(pts, zt, ztrack, up=6.0, down=9.0, min_viaduct_m=80, min_tunnel_m=120):
    """Úseky: surface / viaduct / tunnel podle rozdílu mezi niveletou a terénem."""
    ds = np.hypot(np.diff([p[0] for p in pts]), np.diff([p[1] for p in pts]))
    h = ztrack - zt
    lab = np.where(h > up, "viaduct", np.where(h < -down, "tunnel", "surface"))
    runs = []
    start = 0
    for i in range(1, len(lab) + 1):
        if i == len(lab) or lab[i] != lab[start]:
            L = float(ds[start:i].sum()) * 1000.0 if i > start else 0.0
            runs.append([start, i - 1, str(lab[start]), L])
            start = i
    # krátké viadukty/tunely → povrch
    for r in runs:
        if r[2] == "viaduct" and r[3] < min_viaduct_m:
            r[2] = "surface"
        if r[2] == "tunnel" and r[3] < min_tunnel_m:
            r[2] = "surface"
    merged = []
    for r in runs:
        if merged and merged[-1][2] == r[2]:
            merged[-1][1] = r[1]
            merged[-1][3] += r[3]
        else:
            merged.append(list(r))
    return merged


def max_grade(s, z, window_km=0.5):
    best = 0.0
    j = 0
    for i in range(len(s)):
        while s[i] - s[j] > window_km:
            j += 1
        if s[i] - s[j] >= window_km * 0.8:
            best = max(best, abs(z[i] - z[j]) / ((s[i] - s[j]) * 1000.0))
    return best


def segments_from_runs(pts, runs):
    out = []
    for a, b, lab, L in runs:
        seg = pts[a:b + 1]
        if len(seg) >= 2:
            out.append({"section": lab, "pts": seg, "length_m": round(L)})
    return out


# ---------------------------------------------------------------- L1
def build_l1(world, rcost):
    env = world.env
    n02 = world.pos("N-02")
    stations = []
    s1 = HUB_W
    s2 = best_spot(world, 12.40, 10.10, 0.5, 6.0, 0.08)
    s3 = best_spot(world, 10.55, 8.62, 0.6, 7.0, 0.07)
    s5 = best_spot(world, 9.45, 6.45, 0.5, 4.0, 0.07)
    phi_in = math.atan2(s3[1] - n02[1], s3[0] - n02[0])
    R_port, R_track = 0.075, 0.062
    out_pt = lambda phi, r: (n02[0] + r * math.cos(phi), n02[1] + r * math.sin(phi))
    approach = out_pt(phi_in, R_port + 0.28)       # povrchový bod před portálem
    portal_in = out_pt(phi_in, R_port)
    phi_out = phi_in + math.radians(262.0)         # ~¾ obvodu
    portal_out = out_pt(phi_out, R_port)
    exit_pt = out_pt(phi_out, R_port + 0.28)
    # trasa A* (město → přehrada → vodopád → před portál); dolní část od portálu k horské stanici
    p1 = pathfind.route(env, rcost, [s1, s2, s3, approach], smooth_iters=3)
    p2 = pathfind.route(env, rcost, [exit_pt, s5], smooth_iters=3)
    # oblouk v jeskyni (¾ obvodu)
    arc = []
    n = 40
    for k in range(n + 1):
        phi = phi_in + math.radians(262.0) * k / n
        arc.append(out_pt(phi, R_track))
    tunnel_in = [approach, portal_in, arc[0]]
    tunnel_out = [arc[-1], portal_out, exit_pt]
    # klasifikace povrchových částí
    parts = []
    for name, pts in (("approach", p1), ("departure", p2)):
        d = dense(pts, 0.02)
        s = chainage(d)
        zt = sample_z(world, d)
        zt_s = track_profile(s, zt, 0.06)
        runs = classify(d, zt, zt_s)
        parts.append({"name": name, "pts": d, "s": s, "zt": zt, "ztrack": zt_s, "runs": runs})
    seg = []
    seg += segments_from_runs(parts[0]["pts"], parts[0]["runs"])
    seg.append({"section": "tunnel", "pts": tunnel_in, "length_m": 280, "note": "vstupní tunel do jeskyně"})
    seg.append({"section": "cave", "pts": arc, "length_m": round(2 * math.pi * R_track * 1000 * 262 / 360), "note": "průjezd osvětlenou krystalovou jeskyní (~¾ obvodu)"})
    seg.append({"section": "tunnel", "pts": tunnel_out, "length_m": 280, "note": "výjezd z jeskyně"})
    seg += segments_from_runs(parts[1]["pts"], parts[1]["runs"])
    full = parts[0]["pts"] + tunnel_in[1:] + arc[1:] + tunnel_out[1:] + parts[1]["pts"][1:]
    zt_full = sample_z(world, full)
    sfull = chainage(full)
    # niveleta (pro přehled sklonu): terén, v jeskyni a tunelech plynule
    ztrack = track_profile(sfull, zt_full, 0.06)
    stn = [
        {"id": "ST-L1-01", "name": "Larpington Západ", "pt": s1, "lines": ["L1", "L2", "L3"], "hub": "W", "note": "uzel L1/L2/L3, přestup"},
        {"id": "ST-L1-02", "name": "Přehrada", "pt": s2, "lines": ["L1"], "note": "rekreační pobřeží přehrady, ochrana zdroje vody"},
        {"id": "ST-L1-03", "name": "Vodopád (fotozastávka)", "pt": s3, "lines": ["L1"], "note": "N-03 – fotozastávka; bezpečná vyhlídková plošina"},
        {"id": "ST-L1-04", "name": "Krystalová jeskyně", "pt": approach, "lines": ["L1"], "note": "N-02 – nástupiště před vstupním tunelem; vlak pokračuje jeskyní"},
        {"id": "ST-L1-05", "name": "Horská stanice", "pt": s5, "lines": ["L1"], "note": "konečná u pohoří M-02/M-03; návaznost na turistiku, lyžování a paragliding"},
    ]
    return {"segments": seg, "full": full, "s": sfull, "zt": zt_full, "ztrack": ztrack, "stations": stn,
            "cave": {"center": n02, "R_track": R_track, "R_portal": R_port, "phi_in_deg": math.degrees(phi_in) % 360, "arc_deg": 262.0,
                     "portal_in": portal_in, "portal_out": portal_out}}


# ---------------------------------------------------------------- L2
def build_l2(world, rcost):
    env = world.env
    st = {}
    st["T02"] = best_spot(world, 11.70, 11.45, 0.4, 3.0)
    st["PRAHA"] = best_spot(world, 16.70, 8.15, 0.4, 3.0)
    st["J1"] = best_spot(world, 17.00, 6.60, 0.4, 3.0)
    st["AOKAWA"] = best_spot(world, 17.45, 4.55, 0.4, 3.0, 0.06)
    st["ORU"] = best_spot(world, 13.70, 4.00, 0.4, 3.0)
    st["HOSHI"] = best_spot(world, 19.25, 4.10, 0.4, 3.0)
    st["AIRPORT"] = best_spot(world, 19.50, 6.85, 0.4, 2.0)
    st["I01"] = best_spot(world, 19.50, 8.90, 0.4, 3.0)
    st["I02"] = best_spot(world, 21.00, 9.40, 0.4, 3.0)
    st["I03"] = best_spot(world, 22.10, 10.00, 0.3, 3.0)
    arc = geom.catmull_rom_open([HUB_W, (14.75, 11.35), HUB_N, (16.95, 11.25), HUB_E], 0.03)
    branches = []

    def rt(points, it=3):
        return pathfind.route(env, rcost, points, smooth_iters=it)

    branches.append(("L2-A1", "Cimprlichovo Hradiště – Larpington Západ", rt([st["T02"], HUB_W])))
    branches.append(("L2-A2", "městský oblouk Západ – Sever – Východ", arc))
    branches.append(("L2-A3", "Larpington Východ – Zelená průmyslová zóna", rt([HUB_E, st["I01"]])))
    branches.append(("L2-A4", "Zelená zóna – závod na řasy – nákladní přístav", rt([st["I01"], st["I02"], st["I03"]])))
    branches.append(("L2-B1", "Larpington Sever – Praha", rt([HUB_N, st["PRAHA"]])))
    branches.append(("L2-B2", "Praha – odbočka – Aokawa", rt([st["PRAHA"], st["J1"], st["AOKAWA"]])))
    branches.append(("L2-C1", "Aokawa – Ōru Maito", rt([st["AOKAWA"], st["ORU"]])))
    branches.append(("L2-C2", "Aokawa – Hoshimachi", rt([st["AOKAWA"], st["HOSHI"]])))
    branches.append(("L2-D1", "odbočka – letiště", rt([st["J1"], st["AIRPORT"]])))
    segs, total = [], 0.0
    for bid, name, pts in branches:
        d = dense(pts, 0.02)
        s = chainage(d)
        # mosty: úseky do 45 m od řeky/potoka
        seg = {"branch": bid, "name": name, "pts": d, "length_km": float(s[-1])}
        segs.append(seg)
        total += float(s[-1])
    stn = [
        {"id": "ST-L2-01", "name": "Cimprlichovo Hradiště", "pt": st["T02"], "lines": ["L2"], "note": "historické městečko T-02"},
        {"id": "ST-L2-02", "name": "Larpington Západ", "pt": HUB_W, "lines": ["L1", "L2", "L3"], "hub": "W", "note": "uzel L1/L2/L3"},
        {"id": "ST-L2-03", "name": "Larpington Sever (Kynčlova)", "pt": HUB_N, "lines": ["L2", "L3"], "hub": "N", "note": "přestup L2↔L3"},
        {"id": "ST-L2-04", "name": "Larpington Východ (Klimečkova)", "pt": HUB_E, "lines": ["L2", "L3"], "hub": "E", "note": "přestup L2↔L3"},
        {"id": "ST-L2-05", "name": "Zelená průmyslová zóna", "pt": st["I01"], "lines": ["L2"], "note": "I-01, školy a jídelny v areálu"},
        {"id": "ST-L2-06", "name": "Závod na zpracování řas", "pt": st["I02"], "lines": ["L2"], "note": "I-02"},
        {"id": "ST-L2-07", "name": "Nákladní přístav", "pt": st["I03"], "lines": ["L2"], "note": "I-03 – převážně nákladní, omezeně osobní"},
        {"id": "ST-L2-08", "name": "Praha", "pt": st["PRAHA"], "lines": ["L2"], "note": "T-01"},
        {"id": "ST-L2-09", "name": "Odbočka Letiště (výhybna)", "pt": st["J1"], "lines": ["L2"], "note": "výhybna, bez nástupiště"},
        {"id": "ST-L2-10", "name": "Letiště", "pt": st["AIRPORT"], "lines": ["L2"], "note": "A-01"},
        {"id": "ST-L2-11", "name": "Aokawa", "pt": st["AOKAWA"], "lines": ["L2"], "note": "T-05, rozvětvení na Ōru Maito a Hoshimachi"},
        {"id": "ST-L2-12", "name": "Ōru Maito", "pt": st["ORU"], "lines": ["L2"], "note": "T-04"},
        {"id": "ST-L2-13", "name": "Hoshimachi", "pt": st["HOSHI"], "lines": ["L2"], "note": "T-06"},
    ]
    return {"branches": segs, "stations": stn, "length_km": total}


# ---------------------------------------------------------------- L3
def build_l3(world, main_poly, para_poly, para_types):
    ring_ctrl = [HUB_N, (16.95, 11.25), HUB_E, (17.05, 12.80), HUB_S, (15.05, 12.75), HUB_W, (14.80, 11.35)]
    ring = [(x, y) for x, y, _, _ in geom.catmull_rom_closed(ring_ctrl, spacing=0.03)]
    pen = world.pos("P-01")
    # špička poloostrova = bod polygonu nejdál ve směru JV
    ux, uy = math.cos(math.radians(38.0)), math.sin(math.radians(38.0))
    tip = max(main_poly, key=lambda p: p[0] * ux + p[1] * uy)
    center = peninsula_centerline(main_poly, pen, tip, 0.15)
    # hrot: poslední bod střednice posuň těsně k hrotu
    center = center + [tip] if math.dist(center[-1], tip) > 0.25 else center
    # přistání na Paralandu: nejbližší vrchol typu 'harbor' k hrotu
    harb = [p for p, t in zip(para_poly, para_types) if t == "harbor"]
    landing = min(harb, key=lambda p: math.dist(p, tip))
    n_in = inward_normal_at(para_poly, landing)
    terminal = (landing[0] + n_in[0] * 0.14, landing[1] + n_in[1] * 0.14)
    tail_ctrl = [HUB_E, (18.20, 12.50), (18.80, 12.90), pen] + center[1:-1] + [tip]
    tail = geom.catmull_rom_open(tail_ctrl, 0.03)
    strait = geom.catmull_rom_open([tip, ((tip[0] + landing[0]) / 2, (tip[1] + landing[1]) / 2), landing, terminal], 0.03)
    # klasifikace podle polohy bodu: pod souší = tunel, pod mořem = podmoří
    def lab(p):
        if geom.point_in_poly(p, main_poly) or geom.point_in_poly(p, para_poly):
            return "tunnel"
        return "undersea"
    full_tail = tail + strait[1:]
    labs = [lab(p) for p in full_tail]
    runs, start = [], 0
    for i in range(1, len(labs) + 1):
        if i == len(labs) or labs[i] != labs[start]:
            runs.append([start, i - 1, labs[start]])
            start = i
    segments = [{"section": "tunnel", "pts": ring + [ring[0]], "note": "městský okruh (převážně ražený/hloubený tunel)"}]
    for a, b, l in runs:
        pts = full_tail[a:b + 1]
        if len(pts) < 2:
            continue
        length = chainage(pts)[-1] * 1000.0
        segments.append({"section": l, "pts": pts, "length_m": round(length)})
    under = [r for r in segments if r["section"] == "undersea"]
    under_len = sum(r["length_m"] for r in under)
    # prosklená galerie: ~220 m uprostřed podmořského úseku
    glass = None
    if under:
        u = max(under, key=lambda r: r["length_m"])
        pts = u["pts"]
        s = chainage(pts)
        mid = s[-1] / 2
        a = np.searchsorted(s, mid - 0.11)
        b = np.searchsorted(s, mid + 0.11)
        glass = {"section": "glass_gallery", "pts": pts[a:b + 1], "length_m": round(float((s[min(b, len(s) - 1)] - s[a]) * 1000)),
                 "note": "krátká kontrolovaná panoramatická galerie (bible: krátký prosklený úsek)"}
    stn = [
        {"id": "ST-L3-01", "name": "Larpington Západ (Chalupecká)", "pt": HUB_W, "lines": ["L1", "L2", "L3"], "hub": "W", "note": "přestup na L2 a L1"},
        {"id": "ST-L3-02", "name": "Larpington Sever (Kynčlova)", "pt": HUB_N, "lines": ["L2", "L3"], "hub": "N", "note": "přestup na L2"},
        {"id": "ST-L3-03", "name": "Larpington Východ (Klimečkova)", "pt": HUB_E, "lines": ["L2", "L3"], "hub": "E", "note": "přestup na L2; začátek větve na Paraland"},
        {"id": "ST-L3-04", "name": "Larpington Střed – Přístav (Žemličkova)", "pt": HUB_S, "lines": ["L3"], "hub": "S", "note": "stará zástavba, parlament, historický přístav C-02 (cca 0,9 km)"},
        {"id": "ST-L3-05", "name": "Východní nábřeží", "pt": (18.80, 12.90), "lines": ["L3"], "note": "nová čtvrť na východním pobřeží"},
        {"id": "ST-L3-06", "name": "Paraland Link (P-01)", "pt": pen, "lines": ["L3"], "note": "P-01 – poslední stanice na hlavním ostrově"},
        {"id": "ST-L3-07", "name": "Paraland – Marina", "pt": terminal, "lines": ["L3"], "note": "terminál L3 na západním pobřeží Paralandu u mariny"},
    ]
    return {"ring": ring, "segments": segments, "glass": glass, "stations": stn, "tip": tip, "landing": landing, "terminal": terminal,
            "undersea_m": under_len, "center_peninsula": center}
