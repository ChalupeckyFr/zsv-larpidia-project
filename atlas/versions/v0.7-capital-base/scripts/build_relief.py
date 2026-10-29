"""F2: reliéf a voda → DEM, hillshade, vrstevnice, hydrografie, pokryv krajiny, třídy pobřeží, SVG náhledy, kontroly.

Spuštění:  python atlas/scripts/build_relief.py
Výstup:    atlas/current/relief/*  a  atlas/current/svg/physical_preview.svg, landcover_preview.svg
VŠE JE PRACOVNÍ NÁVRH (proposed); výšky jsou modelové.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

import canon
import geom
import hydro
import landcover as lc
import layers
import raster
import relief_model as rm
import svgkit
from canon import ATLAS
from raster import smoothstep
from svgkit import PALETTE as P

CUR = ATLAS / "current"
RELIEF = CUR / "relief"
SVGDIR = CUR / "svg"
SHORT = {"M-01": "Nejvyšší vrchol", "M-02": "Lyžařská hora", "M-03": "Zaoblený vrch"}


# ------------------------------------------------------------------ rastry pro SVG
def hypsometric_rgba(z, land, scale=2):
    stops = [(0, (228, 230, 202)), (20, (222, 227, 192)), (80, (214, 218, 178)), (200, (208, 200, 160)),
             (350, (198, 180, 136)), (560, (184, 160, 120))]
    xs = [s[0] for s in stops]
    rgb = np.zeros(z.shape + (3,), dtype=np.float32)
    for c in range(3):
        rgb[..., c] = np.interp(z, xs, [s[1][c] for s in stops])
    a = np.where(land, 255, 0).astype(np.uint8)
    out = np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), a])
    im = Image.fromarray(out, mode="RGBA")
    im = im.resize((z.shape[1] // scale, z.shape[0] // scale), Image.BILINEAR)
    return np.asarray(im)


def hillshade_rgba(z, land, dx_m=20.0):
    hs = raster.hillshade(z, dx_m, az_deg=315.0, alt_deg=42.0, exag=2.4)
    sh_a = np.clip((0.70 - hs) * 1.5, 0.0, 0.55)
    hi_a = np.clip((hs - 0.80) * 1.2, 0.0, 0.30)
    rgba = np.zeros(z.shape + (4,), dtype=np.uint8)
    dark = sh_a > 0
    rgba[..., 0] = np.where(dark, 50, 255)
    rgba[..., 1] = np.where(dark, 38, 252)
    rgba[..., 2] = np.where(dark, 25, 235)
    rgba[..., 3] = (np.where(dark, sh_a, hi_a) * 255).astype(np.uint8)
    rgba[..., 3] = np.where(land, rgba[..., 3], 0)
    return hs, rgba


# ------------------------------------------------------------------ vrstevnice
def build_contours(g, z, lake_mask, levels):
    out = []
    for lev in levels:
        for line in raster.contour_lines(g, z, lev):
            if len(line) < 6:
                continue
            ij = [g.cell_of(x, y) for x, y in line[:: max(1, len(line) // 12)]]
            inside = np.mean([lake_mask[i, j] for i, j in ij])
            if inside > 0.6:
                continue
            closed = line[0] == line[-1]
            pts = raster.simplify(line, 0.006)
            if len(pts) < 4:
                continue
            pts = raster.chaikin(pts[:-1] if closed else pts, closed=closed, iters=1)
            if closed:
                pts = pts + [pts[0]]
            out.append({"level": float(lev), "index": lev % 100 == 0, "line": pts, "closed": closed})
    return out


# ------------------------------------------------------------------ export
def write_geojson(path, features, name):
    fc = {"type": "FeatureCollection", "name": name,
          "crs_note": "lokální km (x východ, y jih, počátek v SZ rohu rámce 24×16 km); pracovní návrh (proposed)",
          "features": features}
    Path(path).write_text(json.dumps(fc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def r3(p):
    return [round(float(p[0]), 3), round(float(p[1]), 3)]


def main():
    t_all = time.time()
    RELIEF.mkdir(parents=True, exist_ok=True)
    SVGDIR.mkdir(parents=True, exist_ok=True)
    o = canon.load_outline()
    rows = {r["id"]: r for r in canon.table_rows()}
    g = raster.Grid(0.02)
    T = rm.Terrain(g, o, rows)
    H, z0 = T.calibrate()
    z, hy = hydro.build_hydro(T, z0)
    print(f"terén+hydro {time.time() - t_all:.0f}s; max {z.max():.1f} m; hladina jezera {hy['lake_level']:.1f} m")

    # --- rastry
    hs, hs_rgba = hillshade_rgba(z, T.land)
    hyp_rgba = hypsometric_rgba(z, T.land)
    raster.save_png16(np.round(z * 100.0), RELIEF / "dem_20m_u16.png")
    raster.save_png8(hs * 255.0, RELIEF / "hillshade_20m.png")
    meta = {"atlas_version": "0.2-relief", "status": "proposed", "origin_xy_km": [g.x0, g.y0], "cell_km": g.dx, "ncols": g.nx, "nrows": g.ny,
            "value": "výška v m × 100 (uint16), řádky na jih, sloupce na východ; počátek = levý horní roh plátna A2 (km od SZ rohu rámce)",
            "max_m": round(float(z.max()), 1)}
    (RELIEF / "dem_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- vrstevnice
    contours = build_contours(g, z, hy["lake_mask"], range(20, 561, 20))
    print(f"vrstevnice: {len(contours)} polyline, {sum(len(c['line']) for c in contours)} bodů")

    # --- pokryv krajiny + pobřeží
    cls, aux = lc.compute_landcover(T, z, hy)
    img = Image.fromarray(cls, mode="L")
    pal = [0] * 768
    for k, hexcol in {0: "#cfe2ec", 1: "#b9d19e", 2: "#dfe8b4", 3: "#f1e4b0", 4: "#e6d49a", 5: "#e3e1c2", 6: "#c9c1b0", 7: "#f4e8bd", 8: "#8fc3e0", 9: "#3b8fc4"}.items():
        pal[k * 3:k * 3 + 3] = [int(hexcol[i:i + 2], 16) for i in (1, 3, 5)]
    img.putpalette(pal)
    img.save(RELIEF / "landcover_20m.png")
    polys = {cid: lc.class_polygons(g, cls, cid) for cid in (1, 2, 3, 4, 5, 6)}
    ccl = lc.coast_classes(o)
    print("pokryv:", {lc.CLASSES[k]: len(v) for k, v in polys.items()}, "| pláže", len(ccl["beaches"]), "útesy", len(ccl["cliffs"]), "skalnaté", len(ccl["rocky"]))

    # --- GeoJSON
    cf = []
    for c in contours:
        cf.append({"type": "Feature", "properties": {"id": f"CT-{int(c['level'])}", "level_m": c["level"], "index": c["index"], "status": "proposed", "origin": "atlas_new"},
                   "geometry": {"type": "LineString", "coordinates": [r3(p) for p in c["line"]]}})
    write_geojson(RELIEF / "contours.geojson", cf, "contours_20m")

    hf = []
    for r in hy["rivers"]:
        d = r["def"]
        pts = r["P"][::3]
        hf.append({"type": "Feature", "properties": {"id": d["id"], "part": r["part"], "name_working": d["name"], "kind": d["kind"], "status": "proposed",
                                                     "origin": "atlas_new", "bed_start_m": round(float(r["bed"][0]), 1), "bed_end_m": round(float(r["bed"][-1]), 1),
                                                     "length_km": round(float(r["s"][-1]), 2)},
                   "geometry": {"type": "LineString", "coordinates": [r3(p) for p in pts]}})
    lake = hy["lake_poly"]
    hf.append({"type": "Feature", "properties": {"id": "W-lake-N04", "ref": "N-04", "name_working": "Přehradní jezero", "level_m_model": round(hy["lake_level"], 1),
                                                 "area_km2": round(geom.area(lake), 3), "status": "approved(existence)/proposed(tvar)", "origin": "bible+atlas_new"},
               "geometry": {"type": "Polygon", "coordinates": [[r3(p) for p in lake] + [r3(lake[0])]]}})
    wf = hy["waterfall"]
    hf.append({"type": "Feature", "properties": {"id": "N-03", "name_working": "Vodopád", "top_m_model": round(wf["top_m"], 1), "bottom_m_model": round(wf["bottom_m"], 1),
                                                 "drop_m_model": round(wf["top_m"] - wf["bottom_m"], 1), "status": "approved(existence)/proposed(výška)"},
               "geometry": {"type": "Point", "coordinates": r3((wf["x"], wf["y"]))}})
    write_geojson(RELIEF / "hydrography.geojson", hf, "hydrography")

    lf = []
    for cid, rings in polys.items():
        if not rings:
            continue
        lf.append({"type": "Feature", "properties": {"class": lc.CLASSES[cid], "class_cs": lc.CLASS_NAMES_CS[cid], "status": "proposed", "origin": "atlas_new",
                                                     "note": "polygony s dírami: pravidlo even-odd"},
                   "geometry": {"type": "MultiPolygon", "coordinates": [[[r3(p) for p in ring] + [r3(ring[0])]] for ring in rings]}})
    write_geojson(RELIEF / "landcover.geojson", lf, "landcover")

    cc = []
    for b in ccl["beaches"]:
        cc.append({"type": "Feature", "properties": {"class": "beach", "island": b["island"], "status": "proposed"},
                   "geometry": {"type": "Polygon", "coordinates": [[r3(p) for p in b["ring"]] + [r3(b["ring"][0])]]}})
    for k in ("cliffs", "rocky"):
        for c in ccl[k]:
            cc.append({"type": "Feature", "properties": {"class": k[:-1] if k == "cliffs" else "rocky", "island": c["island"], "status": "proposed"},
                       "geometry": {"type": "LineString", "coordinates": [r3(p) for p in c["line"]]}})
    write_geojson(RELIEF / "coast_classes.geojson", cc, "coast_classes")

    # --- kontroly a vzorky výšek
    report = checks(T, z, hy, polys, ccl, rows)
    (RELIEF / "relief_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- SVG náhledy
    Image.fromarray(hyp_rgba, mode="RGBA").save(RELIEF / "hypsometry_rgba.png", optimize=True)
    Image.fromarray(hs_rgba, mode="RGBA").save(RELIEF / "hillshade_rgba.png", optimize=True)
    svg_physical(o, rows, z, hs_rgba, hyp_rgba, contours, hy, ccl, report)
    svg_landcover(o, rows, polys, ccl, hy, report)
    print(f"hotovo za {time.time() - t_all:.0f}s")
    for k, v in report["checks"].items():
        print(("  OK  " if v else "  CHYBA"), k)
    return report


def checks(T, z, hy, polys, ccl, rows):
    g = T.g
    land = T.land
    elev = {rid: round(T.at(z, *T.pos(rid)), 1) for rid in rows}
    m1 = T.pos("M-01")
    imax = np.unravel_index(np.argmax(z), z.shape)
    xmax, ymax = g.x0 + (imax[1] + 0.5) * g.dx, g.y0 + (imax[0] + 0.5) * g.dx
    S = raster.slope_deg(z, g.dx * 1000.0)
    a01 = T.pos("A-01")
    box = (np.abs(T.X - a01[0]) < 0.95) & (np.abs(T.Y - a01[1]) < 0.20)
    wf = hy["waterfall"]
    rivers_ok = all(bool(np.all(np.diff(r["bed"]) <= 1e-6)) for r in hy["rivers"])
    dam_foot = None
    for r in hy["rivers"]:
        if r["def"]["id"] == "W-01" and r["part"] == "down":
            dam_foot = float(r["bed"][0])
    beach_nw = [b for b in ccl["beaches"] if (np.mean([p[0] for p in b["ring"]]) < 9.0 and np.mean([p[1] for p in b["ring"]]) < 9.0)]
    chk = {
        "nejvyšší bod = M-01 (±0,5 km)": math.dist((xmax, ymax), m1) < 0.5,
        "maximum 555–565 m (nejvyšší vrchol 560 m)": 555.0 <= float(z.max()) <= 565.0,
        "výšky vrcholů M-01/M-02/M-03 = 560/510/440 ± 3 m": all(abs(elev[k] - v) <= 3 for k, v in rm.PEAK_TARGETS.items()),
        "žádná záporná výška na souši": float(z[land].min()) >= 0.0,
        "všechny toky klesají (monotónní koryto)": rivers_ok,
        "hladina přehrady je plochá a pod vodopádem": hy["lake_level"] is not None and hy["lake_level"] < wf["bottom_m"] + 1.0,
        "výška vodopádu N-03 ≥ 30 m": wf["top_m"] - wf["bottom_m"] >= 30.0,
        "jeskyně N-02 je výš než vodopád N-03": elev["N-02"] > elev["N-03"],
        "vyhlídka N-01 ve výšce 8–18 m (cca 10m sráz)": 8.0 <= elev["N-01"] <= 18.0,
        "centrum hlavního města 5–30 m, přístav ≤ 2 m": 5.0 <= elev["C-01"] <= 30.0 and elev["C-02"] <= 2.0,
        "dráha letiště A-01 má sklon < 1,5°": float(S[box].max()) < 1.5,
        "žádná pláž na útesovém severozápadě": len(beach_nw) == 0,
        "přehrada má plochu 0,3–1,0 km²": 0.3 <= geom.area(hy["lake_poly"]) <= 1.0,
    }
    return {
        "atlas_version": "0.2-relief", "status": "proposed", "max_elev_m": round(float(z.max()), 1), "max_at_km": (round(xmax, 2), round(ymax, 2)),
        "lake": {"level_m_model": round(hy["lake_level"], 1), "area_km2": round(geom.area(hy["lake_poly"]), 3),
                 "dam_foot_m_model": None if dam_foot is None else round(dam_foot, 1),
                 "dam_height_m_model": None if dam_foot is None else round(hy["lake_level"] + hydro.DAM["crest_above_lake_m"] - dam_foot, 1),
                 "volume_Mm3_model": round(geom.area(hy["lake_poly"]) * 1e6 * 7.0 / 1e6, 2), "note": "objem = plocha × průměrná hloubka 7 m (modelový odhad)"},
        "waterfall": {k: round(v, 3) if isinstance(v, float) else v for k, v in wf.items()},
        "land_slope_over_35deg_pct": round(float((S[land] > 35).mean() * 100), 2),
        "elevations_m_model": elev, "checks": {k: bool(v) for k, v in chk.items()}, "all_ok": bool(all(chk.values())),
    }


# ------------------------------------------------------------------ SVG
def _peaks(rows, z, T):
    out = []
    for k in ("M-01", "M-02", "M-03"):
        x, y = T_pos = rows[k]["x_km"], rows[k]["y_km"]
        out.append({"id": k, "name": SHORT[k], "x": x, "y": y, "z": T.at(z, x, y)})
    return out


def marginalia(sh, title, subtitle, lines, legend_items):
    W, H = round(sh.w * 1000), round(sh.h * 1000)
    sh_title_y = 560
    with sh.layer("marginalia", "Titul, legenda, měřítko"):
        sh.text(500, sh_title_y, title, size=330, weight="700", units=True, halo=False)
        sh.text(500, sh_title_y + 340, subtitle, size=185, units=True, halo=False, fill=P["proposed"], weight="600")
        sh.text(500, sh_title_y + 620, "Fiktivní stát. Všechny polohy a výšky jsou pracovní návrh (proposed); schválena je jen existence prvků.", size=125,
                units=True, halo=False, fill=P["ink_soft"])
        for i, s in enumerate(lines):
            sh.text(500, 17550 + i * 235, s, size=132, units=True, halo=False)
        svgkit.nice_scale_bar(sh, 11500, 19200, km=5.0)
        sh.text(11500, 19800, "Měřítko 1 : 50 000 při tisku na A2 (594 × 420 mm); 1 jednotka SVG = 1 m", size=105, units=True, halo=False, fill=P["ink_soft"])
        svgkit.north_arrow(sh, 28500, 1800)
        lx, ly = 24650, 2600
        sh.rect_u(lx - 200, ly - 330, 4850, 330 + 300 * (len(legend_items) + 1) + 240, fill="#ffffffd9", stroke=P["ink_soft"], sw=8, rx=40)
        sh.text(lx, ly, "Legenda", size=165, weight="700", units=True, halo=False)
        for i, item in enumerate(legend_items):
            yy = ly + 340 + i * 300
            kind = item[0]
            if kind == "swatch":
                sh.rect_u(lx, yy - 150, 260, 190, fill=item[1], stroke=P["ink_soft"], sw=6)
            elif kind == "line":
                sh.raw(f'<line x1="{lx}" y1="{yy - 50}" x2="{lx + 260}" y2="{yy - 50}" stroke="{item[1]}" stroke-width="{item[3] if len(item) > 3 else 14}"/>')
            elif kind == "marker":
                sh.marker(item[3], (sh.x0 + (lx + 130) / 1000, sh.y0 + (yy - 50) / 1000), size=58, fill=item[1])
            sh.text(lx + 340, yy, item[2], size=118, units=True, halo=False)


def svg_physical(o, rows, z, hs_rgba, hyp_rgba, contours, hy, ccl, report):
    sh = svgkit.Sheet()
    main, para = o["main"], o["para"]
    layers.defs_clip(sh, main, para)
    layers.layer_sea(sh, main, para)
    layers.layer_grid(sh)
    layers.layer_land_base(sh, main, para)
    layers.layer_raster(sh, "hypsometry", "Hypsometrické tónování (modelové výšky)", "../relief/hypsometry_rgba.png")
    layers.layer_raster(sh, "hillshade", "Stínovaný reliéf", "../relief/hillshade_rgba.png")
    layers.layer_coast_classes(sh, ccl)
    layers.layer_contours(sh, contours)
    layers.layer_contour_labels(sh, contours)
    rivers = [{"id": r["def"]["id"], "part": r["part"], "kind": r["def"]["kind"], "pts": [tuple(p) for p in r["P"][::2]]} for r in hy["rivers"]]
    wf = hy["waterfall"]
    dam = None
    for r in hy["rivers"]:
        if r["def"]["id"] == "W-01" and r["part"] == "down":
            dam = tuple(r["P"][0])
    layers.layer_hydro(sh, rivers, hy["lake_poly"], (wf["x"], wf["y"]), dam)
    layers.layer_coast_line(sh, main, para)
    T_at = lambda arr, x, y: arr[sh_cell(x, y)]
    g = raster.Grid(0.02)

    def zat(x, y):
        i, j = g.cell_of(x, y)
        return float(z[i, j])

    pk = [{"id": k, "name": SHORT[k], "x": rows[k]["x_km"], "y": rows[k]["y_km"], "z": zat(rows[k]["x_km"], rows[k]["y_km"])} for k in ("M-01", "M-02", "M-03")]
    layers.layer_peaks(sh, pk)
    with sh.layer("poi-nature", "Přírodní body N-01…N-04"):
        info = {"N-01": f"N-01 Skalní vyhlídka · cca {report['elevations_m_model']['N-01']:.0f} m", "N-02": f"N-02 Krystalová jeskyně · cca {report['elevations_m_model']['N-02']:.0f} m",
                "N-03": f"N-03 Vodopád · {report['waterfall']['top_m'] - report['waterfall']['bottom_m']:.0f} m", "N-04": f"N-04 Přehrada · hladina {report['lake']['level_m_model']:.0f} m"}
        off = {"N-01": (-0.2, -0.2, "end"), "N-02": (-0.2, 0.0, "end"), "N-03": (0.22, 0.04, "start"), "N-04": (0.4, 0.34, "start")}
        for k in ("N-01", "N-02", "N-03", "N-04"):
            r = rows[k]
            p = (r["x_km"], r["y_km"])
            if k != "N-03" and k != "N-04":
                sh.marker("circle", p, size=55, fill=P["nature"], extra=f'id="pt-{k}" data-status="proposed"')
            dx, dy, an = off[k]
            sh.text(p[0] + dx, p[1] + dy, info[k], size=112, anchor=an, weight="600")
    legend = [("swatch", "#e4e6ca", "nížina 0–20 m"), ("swatch", "#d6dab4", "20–80 m"), ("swatch", "#d0c8a0", "80–200 m"),
              ("swatch", "#c6b488", "200–350 m"), ("swatch", "#b8a078", "350–560 m"),
              ("line", "#a98458", "vrstevnice 20 m", 6), ("line", "#7b5326", "indexová vrstevnice 100 m", 10),
              ("line", "#3b8fc4", "tok, jezero", 20), ("marker", P["peak"], "vrchol (výška modelová)", "triangle"),
              ("line", "#3b3a36", "útesové pobřeží", 16), ("swatch", "#f4e8bd", "písčitá pláž")]
    lines = [f"Nejvyšší bod {report['max_elev_m']:.0f} m (cíl 560 m) · modelový terén 20 m/pixel", f"Přehrada N-04: hladina {report['lake']['level_m_model']:.0f} m, {report['lake']['area_km2']:.2f} km² · vodopád N-03 {report['waterfall']['top_m'] - report['waterfall']['bottom_m']:.0f} m",
             "Výšky a toky jsou modelové; schválena je existence pohoří, vodopádu, přehrady, jeskyně a pobřežního srázu."]
    marginalia(sh, "LARPIDIE a PARALAND — fyzická mapa", "reliéf, vody a pobřeží · atlas v0.2-relief · NÁVRH (proposed)", lines, legend)
    svg = sh.render("Larpidie a Paraland – fyzická mapa (návrh)", "Reliéf, vrstevnice, vody. Pracovní návrh. 1 jednotka = 1 m, A2 = 1:50 000.")
    (SVGDIR / "physical_preview.svg").write_text(svg, encoding="utf-8")
    (SVGDIR / "physical_preview_embedded.svg").write_text(svgkit.embed_images(svg, SVGDIR), encoding="utf-8")


def sh_cell(x, y):
    g = raster.Grid(0.02)
    return g.cell_of(x, y)


def svg_landcover(o, rows, polys, ccl, hy, report):
    sh = svgkit.Sheet()
    main, para = o["main"], o["para"]
    layers.defs_clip(sh, main, para)
    layers.layer_sea(sh, main, para)
    layers.layer_grid(sh)
    layers.layer_land_base(sh, main, para, fill="#e9e6cf")
    layers.layer_landcover(sh, polys, lc.LC_COLORS, {k: v for k, v in lc.CLASSES.items()})
    layers.layer_coast_classes(sh, ccl)
    rivers = [{"id": r["def"]["id"], "part": r["part"], "kind": r["def"]["kind"], "pts": [tuple(p) for p in r["P"][::2]]} for r in hy["rivers"]]
    layers.layer_hydro(sh, rivers, hy["lake_poly"], None, None)
    layers.layer_coast_line(sh, main, para)
    legend = [("swatch", lc.LC_COLORS[1], "les"), ("swatch", lc.LC_COLORS[2], "louka"), ("swatch", lc.LC_COLORS[3], "pole"),
              ("swatch", lc.LC_COLORS[4], "rýžové terasy (historické)"), ("swatch", lc.LC_COLORS[5], "křoviny, travnaté plochy"),
              ("swatch", lc.LC_COLORS[6], "skála"), ("swatch", "#f4e8bd", "písčitá pláž"), ("line", "#3b8fc4", "tok, jezero", 20),
              ("line", "#3b3a36", "útesové pobřeží", 16)]
    lines = ["Zástavba, průmysl a silnice přibudou ve fázi F3 (lidská vrstva).", "Pokryv je modelový návrh podle výšky, sklonu a polohy; kanon určuje jen typy prvků."]
    marginalia(sh, "LARPIDIE a PARALAND — pokryv krajiny", "model pokryvu · atlas v0.2-relief · NÁVRH (proposed)", lines, legend)
    (SVGDIR / "landcover_preview.svg").write_text(sh.render("Larpidie a Paraland – pokryv krajiny (návrh)", "Pracovní návrh pokryvu krajiny. 1 jednotka = 1 m, A2 = 1:50 000."), encoding="utf-8")


if __name__ == "__main__":
    main()
