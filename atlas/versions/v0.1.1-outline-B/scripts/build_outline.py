"""F1: obrys Larpidie a Paralandu (varianty A/B) → geometrie, kontroly, náhledový list SVG.

Spuštění:  python atlas/scripts/build_outline.py [A|B|all] [--debug]
Výstup:    atlas/current/geometry/variants/<A|B>/…   a   outline_compare.html
Vše je pracovní návrh (proposed); plochy a průliv jsou řízeny rozhodnutími R-01.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import canon
import geom
import outline_checks as oc
import shapes
import svgkit
from canon import ATLAS, CANVAS

OUT = ATLAS / "work" / "outline"          # pracovní varianty (zvolená se zmrazí do current/geometry)
W_TYPE = {"cliff": 1.0, "rocky": 0.8, "mixed": 0.5, "beach": 0.25, "harbor": 0.08, "industrial": 0.12}
OCTAVES = [(5.0, 0.30), (2.0, 0.17), (0.8, 0.085), (0.28, 0.03)]   # (vlnová délka km, amplituda km)
PIN_R = 0.40
SEEDS = {"A": 20261023, "B": 20261024}


# ------------------------------------------------------------------ stavba polygonu
def build_polygon(ctrl, seed, target_area, octave_scale=1.0):
    """Z řídicích bodů (x, y, ctype, pin) vyrobí hustý polygon: hladký základ → posun (plocha) → šum pobřeží.

    Plocha se ladí posunem hladkého základu po normále (utlumeno u pinů) a šum se přidává až po něm,
    takže jemné vlnky nikdy netvoří smyčky. Cílová plocha se dorovná sečnou metodou.
    """
    xy = [(c[0], c[1]) for c in ctrl]
    if geom.signed_area(xy) < 0:
        ctrl = list(reversed(ctrl))
        xy = [(c[0], c[1]) for c in ctrl]
    n = len(ctrl)
    cr = geom.catmull_rom_closed(xy, spacing=0.04)
    base = [(x, y) for x, y, _, _ in cr]
    pins = [(c[0], c[1]) for c in ctrl if c[3]]

    weights, pinfac, types = [], [], []
    for (x, y, seg, u) in cr:
        t0, t1 = ctrl[seg][2], ctrl[(seg + 1) % n][2]
        w = W_TYPE[t0] * (1 - u) + W_TYPE[t1] * u
        dmin = min((math.dist((x, y), pt) for pt in pins), default=9.0)
        f = geom.smoothstep(0.0, PIN_R, dmin)
        weights.append(w * f)
        pinfac.append(f)
        types.append(t0 if u < 0.5 else t1)

    nrm = geom.outward_normals(base)
    segl = [math.dist(base[i], base[(i + 1) % len(base)]) for i in range(len(base))]
    denom = sum(f * l for f, l in zip(pinfac, segl))

    def assemble(d, scale):
        shifted = [(b[0] + nx * d * f, b[1] + ny * d * f) for b, (nx, ny), f in zip(base, nrm, pinfac)]
        offs = geom.coast_noise(shifted, weights, [(l, a * scale) for l, a in OCTAVES], seed)
        return geom.displace(shifted, offs)

    scale = octave_scale
    for _ in range(8):
        d_prev, a_prev = 0.0, geom.area(assemble(0.0, scale))
        d = (target_area - a_prev) / denom
        poly, ok = None, True
        for _it in range(10):
            poly = assemble(d, scale)
            if geom.self_intersections(poly):
                ok = False
                break
            a = geom.area(poly)
            if abs(a - target_area) < 0.04:
                break
            if abs(a - a_prev) < 1e-9:
                break
            d_new = d + (target_area - a) * (d - d_prev) / (a - a_prev)
            d_prev, a_prev, d = d, a, d_new
        if ok:
            return poly, types, {"noise_scale": round(scale, 3), "pins": [c[3] for c in ctrl if c[3]],
                                 "area_calibrated": abs(geom.area(poly) - target_area) < 0.1, "base_offset_km": round(d, 3)}
        scale *= 0.8
    raise RuntimeError("Nepodařilo se sestavit polygon bez samoprotnutí – uprav řídicí body.")


def build_paraland_local(polar, axes, rot_deg, seed, target):
    a, b = axes
    ctrl = []
    for (t, f, ct, pin) in polar:
        r = math.radians(t)
        ctrl.append((a * f * math.cos(r), b * f * math.sin(r), ct, pin))
    rot = geom.rotate_pts([(c[0], c[1]) for c in ctrl], rot_deg)
    ctrl = [(p[0], p[1], c[2], c[3]) for p, c in zip(rot, ctrl)]
    return build_polygon(ctrl, seed, target, octave_scale=0.8)


def place_paraland(main, para_local, approach_deg, strait_km):
    """Posune Paraland po směru approach_deg od hrotu poloostrova tak, aby nejmenší vzdálenost = strait_km."""
    ux, uy = math.cos(math.radians(approach_deg)), math.sin(math.radians(approach_deg))
    tip = max(main, key=lambda p: p[0] * ux + p[1] * uy)
    lo, hi = 0.0, 14.0

    def at(s):
        return geom.translate_pts(para_local, tip[0] + ux * s, tip[1] + uy * s)

    for _ in range(36):
        mid = (lo + hi) / 2
        d = geom.min_dist_polys(main, at(mid), step=0.06)[0]
        if d < strait_km:
            lo = mid
        else:
            hi = mid
    para = at((lo + hi) / 2)
    return para, tip


# ------------------------------------------------------------------ list SVG
LABELS = {  # id: (text, dx_km, dy_km, anchor)
    "M-01": ("M-01 Nejvyšší vrchol", -0.18, -0.20, "end"), "M-02": ("M-02 Lyžařská hora", 0.18, -0.22, "start"),
    "M-03": ("M-03 Zaoblený vrch", -0.18, 0.28, "end"), "N-01": ("N-01 Skalní vyhlídka", -0.20, -0.18, "end"),
    "N-02": ("N-02 Krystalová jeskyně", -0.20, 0.0, "end"), "N-03": ("N-03 Vodopád", 0.20, 0.02, "start"),
    "N-04": ("N-04 Přehrada", 0.20, 0.10, "start"), "C-01": ("C-01 Larpington", 0.14, 0.02, "start"),
    "C-02": ("C-02 Hist. přístav", -0.22, 0.42, "end"), "C-03": ("C-03 Chalupecká", -0.18, 0.05, "end"),
    "C-04": ("C-04 Kynčlova", -0.12, -0.20, "end"), "C-05": ("C-05 Klimečkova", 0.18, 0.05, "start"),
    "C-06": ("C-06 Žemličkova", 0.14, 0.04, "start"), "T-01": ("T-01 Praha", 0.20, 0.06, "start"),
    "T-02": ("T-02 Čimprlichovo Hradiště", -0.22, 0.12, "end"), "T-03": ("T-03 Havlišovo Doupě", 0.22, 0.08, "start"),
    "T-04": ("T-04 Ōru Maito オールマイト", 0.0, 0.40, "middle"), "T-05": ("T-05 Aokawa 青川", 0.2, 0.34, "start"),
    "I-01": ("I-01 Zelená průmyslová zóna", -0.20, 0.0, "end"), "I-02": ("I-02 Závod na řasy", -0.20, 0.06, "end"),
    "I-03": ("I-03 Nákladní přístav", -0.24, 0.40, "end"), "A-01": ("A-01 Letiště", 0.22, -0.02, "start"),
    "P-01": ("P-01 Spojení na Paraland", 0.0, -0.32, "middle"),
}
MARK = {"peak": ("triangle", "peak"), "nature": ("circle", "nature"), "capital": ("star", "capital"),
        "district": ("circle", "district"), "port": ("diamond", "port"), "town": ("circle", "town"),
        "industry": ("square", "industry"), "airport": ("diamond", "airport"), "rail_link": ("diamond", "rail_link")}


def make_sheet(key, main, para, report, strait, rows, debug=False):
    P = svgkit.PALETTE
    sh = svgkit.Sheet()
    W, H = round(sh.w * 1000), round(sh.h * 1000)
    with sh.layer("bg-sea", "Moře"):
        sh.rect_u(0, 0, W, H, fill=P["sea"])
        for width_km, col in ((3.6, P["shelf3"]), (2.0, P["shelf2"]), (0.9, P["shelf1"])):
            for poly in (main, para):
                sh.path(poly, fill="none", stroke=col, sw=round(width_km * 1000), extra='opacity="0.9"')
    with sh.layer("grid", "Km mřížka a rámec"):
        gx = math.ceil(sh.x0 / 2) * 2
        x = gx
        while x < sh.x0 + sh.w:
            sh.line((x, sh.y0), (x, sh.y0 + sh.h), P["grid"], 6)
            sh.text(x, sh.y0 + 0.28, f"{x:g}", size=105, anchor="middle", fill=P["ink_soft"], halo=False)
            x += 2
        y = math.ceil(sh.y0 / 2) * 2
        while y < sh.y0 + sh.h:
            sh.line((sh.x0, y), (sh.x0 + sh.w, y), P["grid"], 6)
            sh.text(sh.x0 + 0.08, y - 0.07, f"{y:g}", size=105, fill=P["ink_soft"], halo=False)
            y += 2
        sh.rect_km(0, 0, canon.FRAME_W_KM, canon.FRAME_H_KM, stroke=P["frame"], sw=16, dash="120 70")
        for k in range(1, 10):
            fx, fy = canon.FRAME_W_KM * k / 10, canon.FRAME_H_KM * k / 10
            sh.line((fx, -0.12), (fx, 0.12), P["frame"], 14)
            sh.line((-0.12, fy), (0.12, fy), P["frame"], 14)
            sh.text(fx, -0.2, f"{k * 10} %", size=88, anchor="middle", fill=P["frame"], halo=False)
            sh.text(-0.16, fy + 0.04, f"{k * 10} %", size=88, anchor="end", fill=P["frame"], halo=False)
    with sh.layer("land", "Souš (pracovní návrh)"):
        sh.path(main, fill=P["land"], stroke=P["land_edge"], sw=14, extra='id="LARPIDIA_MAIN"')
        sh.path(para, fill=P["land"], stroke=P["land_edge"], sw=14, extra='id="PARALAND"')
    if debug:
        with sh.layer("debug", "Ladění (obal bodů)"):
            hull = geom.convex_hull([(r["x_km"], r["y_km"]) for r in rows])
            sh.path(hull, stroke="#c0392b", sw=10, extra='stroke-dasharray="60 40"')
    with sh.layer("dimension", "Průliv"):
        d, a, b = strait
        sh.line(a, b, P["proposed"], 20)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        sh.text(mx + 0.25, my + 0.28, f"průliv {d:.2f} km".replace(".", ","), size=125, fill=P["proposed"], weight="600")
    with sh.layer("deviations", "Odchylky od tabulky (≤ 3 %)"):
        for r in rows:
            if r["deviated"]:
                a, b = (r["x_km_orig"], r["y_km_orig"]), (r["x_km"], r["y_km"])
                sh.line(a, b, P["proposed"], 14, dash="60 40")
                sh.raw(f'<circle cx="{sh.X(a[0])}" cy="{sh.Y(a[1])}" r="62" fill="none" stroke="{P["proposed"]}" stroke-width="16" stroke-dasharray="40 30"/>')
                sh.text(a[0] - 0.12, a[1] + 0.34, f"orig. {r['id']}", size=88, anchor="end", fill=P["proposed"], halo=True)
    with sh.layer("points", "Body z tabulky (pracovní návrh)"):
        for r in rows:
            kind, col = MARK[r["category"]]
            p = (r["x_km"], r["y_km"])
            size = 62 if r["category"] != "capital" else 66
            sh.marker(kind, p, size=size, fill=P[col], extra=f'id="pt-{r["id"]}" data-status="{r["pos_status"]}"')
            txt, dx, dy, anc = LABELS[r["id"]]
            sh.text(p[0] + dx, p[1] + dy, txt, size=112, anchor=anc, weight="600")
    m, pm = report["main"], report["para"]
    with sh.layer("marginalia", "Titul, legenda, metriky"):
        sh.text(500, 560, "LARPIDIE a PARALAND — obrys ostrovů", size=330, weight="700", units=True, halo=False)
        sh.text(500, 900, f"{shapes.VARIANTS[key]['title']} · atlas v0.1-outline · NÁVRH (proposed)", size=190,
                units=True, halo=False, fill=P["proposed"], weight="600")
        sh.text(500, 1180, "Fiktivní stát. Poloha a tvar jsou pracovní návrh, schválena je jen existence prvků.", size=130,
                units=True, halo=False, fill=P["ink_soft"])
        # metriky
        lines = [
            f"Hlavní ostrov: {m['area_km2']:.1f} km² (cíl 175 ± 3) · obvod {m['perimeter_km']:.0f} km",
            f"Obálka: {m['bbox']['w_km']:.1f} × {m['bbox']['h_km']:.1f} km · zaplnění obálky {m['bbox']['fill_of_bbox'] * 100:.0f} %",
            f"Paraland: {pm['area_km2']:.1f} km² (cíl 14 ± 0,5) · průliv {strait[0]:.2f} km (cíl 1,5)".replace(".", ","),
            f"Rámec {canon.FRAME_W_KM:g} × {canon.FRAME_H_KM:g} km (oranžově) · mřížka 2 km · sever nahoře",
            f"Body tabulky v pořádku: {report['points_ok']}/{len(rows)} · zátoky na severu: {report['silhouette']['north_bays']}",
            ("Odchylky od tabulky (≤ 3 %): " + ", ".join(f"{r['id']} {r['dev_pct'][0]:+.1f}/{r['dev_pct'][1]:+.1f} %" for r in rows if r["deviated"]))
            if any(r["deviated"] for r in rows) else "Odchylky od tabulky: žádné (všechny body přesně podle GEOGRAPHY_AND_CANON.md)",
        ]
        for i, s in enumerate(lines):
            sh.text(500, 17250 + i * 230, s.replace(".", ",") if i != 2 else s, size=135, units=True, halo=False)
        svgkit.nice_scale_bar(sh, 11500, 19100, km=5.0)
        sh.text(11500, 19700, "Měřítko 1 : 50 000 při tisku na A2 (594 × 420 mm); 1 jednotka SVG = 1 m", size=105, units=True,
                halo=False, fill=P["ink_soft"])
        svgkit.north_arrow(sh, 28500, 1800)
        # legenda
        lx, ly = 24650, 2800
        sh.rect_u(lx - 200, ly - 330, 4850, 4700, fill="#ffffffcc", stroke=P["ink_soft"], sw=8, rx=40)
        sh.text(lx, ly, "Legenda", size=165, weight="700", units=True, halo=False)
        legend = [("triangle", "peak", "vrchol"), ("circle", "nature", "přírodní bod"), ("star", "capital", "hlavní město"),
                  ("circle", "district", "čtvrť"), ("circle", "town", "město / obec"), ("square", "industry", "průmysl"),
                  ("diamond", "port", "přístav"), ("diamond", "airport", "letiště"), ("diamond", "rail_link", "napojení na Paraland")]
        for i, (k, c, t) in enumerate(legend):
            yy = ly + 330 + i * 300
            sh.marker(k, (sh.x0 + (lx + 130) / 1000, sh.y0 + (yy - 40) / 1000), size=58, fill=P[c])
            sh.text(lx + 330, yy, t, size=125, units=True, halo=False)
        yy = ly + 330 + len(legend) * 300 + 80
        sh.raw(f'<line x1="{lx}" y1="{yy}" x2="{lx + 260}" y2="{yy}" stroke="{P["frame"]}" stroke-width="16" stroke-dasharray="120 70"/>')
        sh.text(lx + 330, yy + 40, "referenční rámec 24 × 16 km", size=115, units=True, halo=False)
        sh.text(lx, yy + 330, "Polohy všech bodů: P = pracovní", size=110, units=True, halo=False, fill=P["proposed"])
        sh.text(lx, yy + 480, "návrh (proposed), dosud neschváleno.", size=110, units=True, halo=False, fill=P["proposed"])
    return sh.render(f"Larpidie a Paraland – obrys, {shapes.VARIANTS[key]['title']}",
                     "Pracovní návrh obrysu (proposed). Jednotka SVG = 1 m; tisk A2 = 1:50 000.")


# ------------------------------------------------------------------ GeoJSON
def ring(poly, fn):
    pts = [list(fn(*p)) for p in poly]
    pts.append(pts[0])
    return pts


def geojson(main, para, strait, key, local: bool, rows):
    fn = (lambda x, y: (round(x, 4), round(y, 4))) if local else canon.km_to_lonlat
    meta = {"atlas_version": "0.1-outline", "variant": key, "status": "proposed", "origin": "atlas_new",
            "crs": "lokální km (x východ, y jih, počátek v SZ rohu rámce 24×16 km)" if local else
            "pseudo-WGS84 – HYPOTETICKÉ souřadnice kolem 33,9 N / 137,6 E (bible: working_coordinates, proposed)"}
    feats = [
        {"type": "Feature", "properties": {"id": "LARPIDIA_MAIN", "name": "Larpidie", "area_km2": round(geom.area(main), 2), **meta},
         "geometry": {"type": "Polygon", "coordinates": [ring(main, fn)]}},
        {"type": "Feature", "properties": {"id": "PARALAND", "name": "Paraland", "area_km2": round(geom.area(para), 2), **meta},
         "geometry": {"type": "Polygon", "coordinates": [ring(para, fn)]}},
        {"type": "Feature", "properties": {"id": "STRAIT", "name": "Průliv (nejmenší vzdálenost)", "length_km": round(strait[0], 3), **meta},
         "geometry": {"type": "LineString", "coordinates": [list(fn(*strait[1])), list(fn(*strait[2]))]}},
        {"type": "Feature", "properties": {"id": "FRAME", "name": "Referenční rámec 24×16 km", **meta},
         "geometry": {"type": "Polygon", "coordinates": [ring([(0, 0), (24, 0), (24, 16), (0, 16)], fn)]}},
    ]
    for r in rows:
        feats.append({"type": "Feature", "properties": {k: r[k] for k in ("id", "name_doc", "X_pct", "Y_pct", "X_pct_orig", "Y_pct_orig", "deviated", "dev_km", "category",
                                                                          "exist_status", "name_status", "pos_status", "origin")},
                      "geometry": {"type": "Point", "coordinates": list(fn(r["x_km"], r["y_km"]))}})
    return {"type": "FeatureCollection", "name": f"larpidie_outline_{key}", "features": feats}


# ------------------------------------------------------------------ hlavní běh
SEED_TRIES = 14


def best_main(ctrl, rows, key):
    """Z několika semínek šumu vybere polygon, který projde všemi kontrolami a má nejbohatší pobřeží."""
    best, fallback = None, None
    for s in range(SEED_TRIES):
        seed = SEEDS[key] + s * 101
        try:
            poly, types, info = build_polygon(ctrl, seed, canon.MAIN_AREA_KM2)
        except RuntimeError:
            continue
        pts = oc.check_points(poly, rows)
        sil = oc.silhouette(poly, shapes.PARA_APPROACH_DEG, rows)
        ok = all(p["ok"] for p in pts) and sil["north_bays_ok"] and sil["south_bay_ok"] and sil["west_cape"]["ok"]
        info = {**info, "seed": seed, "seed_try": s}
        cand = (geom.perimeter(poly), poly, types, info)
        if fallback is None:
            fallback = cand
        if ok and (best is None or cand[0] > best[0]):
            best = cand
    chosen = best or fallback
    if chosen is None:
        raise RuntimeError("Žádné semínko nedalo platný polygon.")
    chosen[3]["checks_passed"] = best is not None
    return chosen[1], chosen[2], chosen[3]


def build_variant(key, debug=False):
    v = shapes.VARIANTS[key]
    rows = canon.geo_ref_table(v["deviations"])
    main, types, minfo = best_main(v["main"], rows, key)
    para_local, ptypes, pinfo = build_paraland_local(v["para"], shapes.PARA_AXES, shapes.PARA_ROT_DEG, SEEDS[key] + 7, canon.PARA_AREA_KM2)
    # Paraland je zatím vycentrován kolem počátku → vycentrovat na těžiště a umístit
    cx, cy = geom.centroid(para_local)
    para_local = geom.translate_pts(para_local, -cx, -cy)
    para, tip = place_paraland(main, para_local, shapes.PARA_APPROACH_DEG, canon.STRAIT_KM)
    strait = geom.min_dist_polys(main, para, step=0.03)
    pts = oc.check_points(main, rows)
    sil = oc.silhouette(main, shapes.PARA_APPROACH_DEG, rows)
    report = {
        "variant": key, "title": v["title"], "note": v["note"],
        "deviations": [{"id": r["id"], "from_pct": (r["X_pct_orig"], r["Y_pct_orig"]), "to_pct": (r["X_pct"], r["Y_pct"]),
                        "dev_pct": r["dev_pct"], "dev_km": r["dev_km"]} for r in rows if r["deviated"]], "noise": minfo, "tip_se": (round(tip[0], 2), round(tip[1], 2)),
        "main": {"area_km2": round(geom.area(main), 2), "perimeter_km": round(geom.perimeter(main), 1),
                 "vertices": len(main), "bbox": oc.bbox_report(main), "centroid": tuple(round(c, 2) for c in geom.centroid(main))},
        "para": {"area_km2": round(geom.area(para), 2), "perimeter_km": round(geom.perimeter(para), 1), "vertices": len(para),
                 "bbox": oc.bbox_report(para), "centroid": tuple(round(c, 2) for c in geom.centroid(para))},
        "strait_km": round(strait[0], 3), "strait_pts": (tuple(round(c, 3) for c in strait[1]), tuple(round(c, 3) for c in strait[2])),
        "points": pts, "points_ok": sum(1 for p in pts if p["ok"]), "silhouette": sil,
        "checks": {
            "area_main_ok": abs(geom.area(main) - canon.MAIN_AREA_KM2) <= canon.MAIN_AREA_TOL,
            "area_para_ok": abs(geom.area(para) - canon.PARA_AREA_KM2) <= canon.PARA_AREA_TOL,
            "strait_ok": abs(strait[0] - canon.STRAIT_KM) <= canon.STRAIT_TOL,
            "simple_polygons": not geom.self_intersections(main) and not geom.self_intersections(para),
            "all_points_ok": all(p["ok"] for p in pts),
            "north_bays_ok": sil["north_bays_ok"], "south_bay_ok": sil["south_bay_ok"], "west_cape_ok": sil["west_cape"]["ok"],
        },
    }
    return main, para, types, ptypes, strait, report, rows


def runs(types):
    out, start = [], 0
    for i in range(1, len(types) + 1):
        if i == len(types) or types[i] != types[start]:
            out.append([start, i - 1, types[start]])
            start = i
    return out


def write_variant(key, debug=False):
    main, para, types, ptypes, strait, report, rows = build_variant(key, debug)
    d = OUT / "variants" / key
    d.mkdir(parents=True, exist_ok=True)
    (d / f"outline_{key}.svg").write_text(make_sheet(key, main, para, report, strait, rows, debug), encoding="utf-8")
    (d / f"outline_{key}_local_km.geojson").write_text(json.dumps(geojson(main, para, strait, key, True, rows), ensure_ascii=False), encoding="utf-8")
    (d / f"outline_{key}_pseudo_wgs84.geojson").write_text(json.dumps(geojson(main, para, strait, key, False, rows), ensure_ascii=False), encoding="utf-8")
    coast = {"atlas_version": "0.1-outline", "variant": key, "status": "proposed", "units": "km (x východ, y jih)",
             "main": {"vertices": [[round(x, 4), round(y, 4)] for x, y in main], "coast_type_runs": runs(types)},
             "paraland": {"vertices": [[round(x, 4), round(y, 4)] for x, y in para], "coast_type_runs": runs(ptypes)}}
    (d / f"outline_{key}_coast.json").write_text(json.dumps(coast, ensure_ascii=False), encoding="utf-8")
    (d / f"outline_{key}_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def summarize(rep):
    c = rep["checks"]
    print(f"== Varianta {rep['variant']}: hlavní {rep['main']['area_km2']} km², obvod {rep['main']['perimeter_km']} km, "
          f"obálka {rep['main']['bbox']['w_km']}×{rep['main']['bbox']['h_km']} (výplň {rep['main']['bbox']['fill_of_bbox']}), "
          f"Paraland {rep['para']['area_km2']} km², průliv {rep['strait_km']} km, šum×{rep['noise']['noise_scale']}")
    print("   kontroly:", {k: v for k, v in c.items()})
    bad = [p for p in rep["points"] if not p["ok"]]
    print(f"   body OK {rep['points_ok']}/{len(rep['points'])}; chyby:",
          [(p["id"], p["d_coast_km"], p["rule"], "uvnitř" if p["inside"] else "VENKU") for p in bad])
    s = rep["silhouette"]
    print("   zátoky:", s["pockets"][:6])
    print(f"   sever: {s['north_bays']} zátok; jih hloubka {s['south_bay_depth_km']}; mys {s['west_cape']}; "
          f"JV hrot {s['se_tip']}; šířka poloostrova {s['peninsula_width_km']} km")


# ------------------------------------------------------------------ srovnávací stránka A/B
COMPARE_CSS = """
:root{--bg:#f6f4ee;--ink:#1f2a33;--soft:#5a6670;--line:#d9d3c3;--acc:#b4541b;--card:#fffdf8}
@media (prefers-color-scheme:dark){:root{--bg:#161b20;--ink:#e8e6df;--soft:#9aa6ae;--line:#2c353c;--acc:#f0a070;--card:#1d242a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 'Segoe UI',system-ui,sans-serif}
main{max-width:1280px;margin:0 auto;padding:20px 16px 48px}h1{font-size:1.5rem;margin:.2em 0 .1em}h2{font-size:1.1rem;margin:1.6em 0 .5em}
.sub{color:var(--soft);margin:0 0 1em}.badge{display:inline-block;background:var(--acc);color:#fff;border-radius:999px;padding:1px 10px;font-size:.8rem;margin-right:6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:12px 0}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.tabs button{font:inherit;color:var(--ink);background:var(--card);border:1px solid var(--line);
border-radius:999px;padding:6px 16px;cursor:pointer}.tabs button[aria-pressed=true]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.stage{position:relative;background:#cfe2ec;border:1px solid var(--line);border-radius:12px;overflow:hidden}.stage svg{display:block;width:100%;height:auto}
.stage .b{position:absolute;inset:0}.stage.show-a .b{display:none}.stage.show-b .a{display:none}
.stage.overlay .b>g:not([id$="-land"]){display:none}.stage.overlay .b [id$="LARPIDIA_MAIN"],.stage.overlay .b [id$="PARALAND"]{fill:rgba(214,88,24,.38)!important;stroke:#d4581a!important;stroke-width:32!important}
table{width:100%;border-collapse:collapse;font-size:.92rem}th,td{padding:6px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{color:var(--soft);font-weight:600}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
ul{margin:.3em 0 .3em 1.2em;padding:0}li{margin:.25em 0}code{background:var(--line);padding:0 4px;border-radius:4px;font-size:.9em}
"""


def _inline_svg(path, prefix, cls):
    import re
    s = Path(path).read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>\s*", "", s)
    s = re.sub(r'(<svg[^>]*?)\swidth="[^"]*"\s+height="[^"]*"', r"\1", s, count=1)
    s = s.replace("<svg ", f'<svg class="{cls}" ', 1)
    s = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{prefix}-{m.group(1)}"', s)
    return s


def write_compare(reports):
    A, B = reports["A"], reports["B"]
    D = OUT / "variants"

    def row(label, a, b, note=""):
        return f"<tr><th>{label}</th><td class='n'>{a}</td><td class='n'>{b}</td><td>{note}</td></tr>"

    def f(x, nd=1):
        return f"{x:.{nd}f}".replace(".", ",")

    def pk(rep, cx, cy, r=3.5):
        c = [p for p in rep["silhouette"]["pockets"] if math.dist(p["centroid"], (cx, cy)) < r]
        return max((p["depth_km"] for p in c), default=0.0)

    def north(rep):
        ps = sorted([p for p in rep["silhouette"]["pockets"] if p["centroid"][1] < 7 and p["depth_km"] >= 0.45],
                    key=lambda p: p["centroid"][0])
        return " / ".join(f(p["depth_km"], 1) for p in ps) + " km"

    rows = "".join([
        row("Plocha hlavního ostrova (cíl 175 ± 3 km²)", f(A["main"]["area_km2"]) + " km²", f(B["main"]["area_km2"]) + " km²", "pracovní hodnota z bible, <code>proposed</code>"),
        row("Plocha Paralandu (cíl 14 ± 0,5 km²)", f(A["para"]["area_km2"]) + " km²", f(B["para"]["area_km2"]) + " km²", ""),
        row("Průliv (nejmenší vzdálenost, cíl 1,5 km)", f(A["strait_km"], 2) + " km", f(B["strait_km"], 2) + " km", "rozhodnuto týmem"),
        row("Obvod pobřeží hlavního ostrova", f(A["main"]["perimeter_km"], 0) + " km", f(B["main"]["perimeter_km"], 0) + " km", ""),
        row("Obálka ostrova", f"{f(A['main']['bbox']['w_km'])} × {f(A['main']['bbox']['h_km'])} km",
            f"{f(B['main']['bbox']['w_km'])} × {f(B['main']['bbox']['h_km'])} km",
            f"zaplnění obálky {f(A['main']['bbox']['fill_of_bbox'] * 100, 0)} % / {f(B['main']['bbox']['fill_of_bbox'] * 100, 0)} %"),
        row("Body tabulky přesně podle GEOGRAPHY", f"{23 - len(A['deviations'])} z 23", f"{23 - len(B['deviations'])} z 23",
            "B: T-04 a T-05 o 3,0 a 2,5 % na jih, A-01 o 1 % na západ a 3 % na jih (hranice 3 %)"),
        row("Severní zátoky (hloubka vůči obalu)", north(A), north(B), "kánon: dvě severní zátoky"),
        row("Jižní záliv u historického přístavu C-02", f(A["silhouette"]["south_bay_depth_km"]) + " km", f(B["silhouette"]["south_bay_depth_km"]) + " km", ""),
        row("Východní záliv u nákladního přístavu I-03 (nové)", f(pk(A, 21.2, 12.0)) + " km", f(pk(B, 21.3, 12.1)) + " km", "vytváří jihovýchodní poloostrov"),
        row("Šířka JV poloostrova 1,5 km před hrotem", f(A["silhouette"]["peninsula_width_km"], 1) + " km", f(B["silhouette"]["peninsula_width_km"], 1) + " km", "kánon: užší jihovýchodní poloostrov"),
        row("Západní skalnatý mys (N-01)", f(A["silhouette"]["west_cape"]["dist_to_N-01_km"], 2) + " km od hrotu",
            f(B["silhouette"]["west_cape"]["dist_to_N-01_km"], 2) + " km od hrotu", "vyhlídka přímo na mysu"),
    ])
    svg_a = _inline_svg(D / "A" / "outline_A.svg", "A", "a")
    svg_b = _inline_svg(D / "B" / "outline_B.svg", "B", "b")
    html = f"""<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Larpidie – obrys A/B</title><style>{COMPARE_CSS}</style></head><body><main>
<h1>Obrys Larpidie a Paralandu – výběr varianty</h1>
<p class="sub"><span class="badge">NÁVRH</span>atlas v0.1-outline · pracovní návrh (proposed) · fiktivní stát · plátno A2, měřítko 1 : 50 000</p>
<div class="card"><strong>Co jsem zjistil.</strong> 24 bodů z tabulky GEOGRAPHY tvoří konvexní obal o ploše <strong>135 km²</strong>.
Ostrov o 175 km² ho proto musí kopírovat s rezervou jen ~0,65 km, takže členitost je omezená (což odpovídá kánonu „mírně členité pobřeží“).
Zátoky a poloostrov jsem proto vykrojil dovnitř (východní zátoka u nákladního přístavu) a ven jen tam, kde to nic nestojí.
<ul><li><strong>A</strong> drží všech 23 bodů přesně podle tabulky, tělo je kompaktnější.</li>
<li><strong>B</strong> posouvá 3 body o ≤ 3 % (zdokumentováno), má hlubší zátoky, výraznější mys a delší poloostrov.</li>
<li>Třetí cesta: menší rámec (např. 21,6 × 14,4 km) by umožnil členitější tvar bez odchylek. Vyžaduje změnu rozhodnutí R-01.</li></ul></div>
<div class="tabs" role="group" aria-label="Zobrazení"><button data-m="a" aria-pressed="true">Varianta A</button><button data-m="b" aria-pressed="false">Varianta B</button><button data-m="overlay" aria-pressed="false">Překryv (B oranžově přes A)</button></div>
<div class="stage show-a" id="stage">{svg_a}{svg_b}</div>
<h2>Porovnání</h2><div class="card"><table><thead><tr><th></th><th class="n">A</th><th class="n">B</th><th>Poznámka</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="sub">Všechny polohy jsou <code>proposed</code>. Geometrii najdete v <code>atlas/current/geometry/variants/</code> (SVG, GeoJSON v km a pseudo-WGS84, report JSON).
Pseudo-zeměpisné souřadnice jsou hypotetické. Po výběru varianty se druhá uloží už jen do archivního snapshotu.</p>
</main><script>
const st=document.getElementById('stage');document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-pressed',x===b));
st.className='stage '+(b.dataset.m==='a'?'show-a':b.dataset.m==='b'?'show-b':'overlay');}});
</script></body></html>"""
    (OUT / "outline_compare.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    debug = "--debug" in sys.argv
    keys = list(shapes.VARIANTS) if not args or args[0] == "all" else [args[0]]
    reps = {}
    for k in keys:
        reps[k] = write_variant(k, debug)
        summarize(reps[k])
    if set(reps) == {"A", "B"}:
        write_compare(reps)
        print("outline_compare.html zapsán")
