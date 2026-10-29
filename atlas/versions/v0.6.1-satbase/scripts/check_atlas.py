"""Souhrnná kontrola atlasu (F1–F4): geometrie, reliéf, lidská vrstva, registr, kanon, integrita snapshotů.

Spuštění:  python atlas/scripts/check_atlas.py
Výstup:    atlas/current/registry/atlas_check_report.json a přehled v konzoli (exit 1 při chybě).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import canon
import geom
import outline_checks as oc
from canon import ATLAS, ROOT

CUR = ATLAS / "current"
STAT = set(canon.STATUSES)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ck: dict[str, bool] = {}
    info: dict = {}

    # ---- 1) geometrie (zmrazená varianta)
    fro = json.loads((CUR / "geometry" / "outline_FROZEN.json").read_text(encoding="utf-8"))
    ck["geometrie: SHA-256 obrysu odpovídá zmrazené variantě"] = sha(CUR / "geometry" / "outline_coast.json") == fro["coast_sha256"]
    o = canon.load_outline()
    A, Ap = geom.area(o["main"]), geom.area(o["para"])
    strait = geom.min_dist_polys(o["main"], o["para"], step=0.03)[0]
    rows = canon.table_rows()
    pts = oc.check_points(o["main"], rows)
    ck[f"plocha hlavního ostrova {A:.2f} km² = 175 ± 3"] = abs(A - canon.MAIN_AREA_KM2) <= canon.MAIN_AREA_TOL
    ck[f"plocha Paralandu {Ap:.2f} km² = 14 ± 0,5"] = abs(Ap - canon.PARA_AREA_KM2) <= canon.PARA_AREA_TOL
    ck[f"průliv {strait:.3f} km = 1,5 ± 0,05"] = abs(strait - canon.STRAIT_KM) <= canon.STRAIT_TOL
    ck["ostrovy jsou jednoduché polygony (bez samoprotnutí)"] = not geom.self_intersections(o["main"]) and not geom.self_intersections(o["para"])
    ck["všech 23 bodů tabulky leží správně vůči pobřeží"] = all(p["ok"] for p in pts)
    dev = [r for r in rows if r["deviated"]]
    ck["odchylky od tabulky ≤ 3 % a jen přijaté (T-04, T-05, A-01)"] = {r["id"] for r in dev} == set(canon.ACCEPTED_DEVIATIONS) and all(max(abs(r["dev_pct"][0]), abs(r["dev_pct"][1])) <= 3.0 for r in dev)
    info["area_main_km2"], info["area_para_km2"], info["strait_km"] = round(A, 2), round(Ap, 2), round(strait, 3)

    # ---- 2) reliéf a lidská vrstva
    rr = json.loads((CUR / "relief" / "relief_report.json").read_text(encoding="utf-8"))
    hr = json.loads((CUR / "human" / "human_report.json").read_text(encoding="utf-8"))
    ck[f"reliéf: všech {len(rr['checks'])} kontrol v pořádku (max {rr['max_elev_m']} m)"] = rr["all_ok"]
    ck[f"lidská vrstva: všech {len(hr['checks'])} kontrol v pořádku"] = hr["all_ok"]
    info["relief_checks"], info["human_checks"] = len(rr["checks"]), len(hr["checks"])

    # ---- 3) registr
    reg = json.loads((CUR / "registry" / "places.json").read_text(encoding="utf-8"))["objects"]
    ids = [x["id"] for x in reg]
    ck["registr: ID jsou jedinečná"] = len(ids) == len(set(ids))
    ck["registr: každý objekt má exist/name/pos status a origin"] = all(x.get("exist_status") in STAT and x.get("name_status") in STAT and x.get("pos_status") in STAT and x.get("origin") for x in reg)
    ck["registr: všechny polohy jsou návrh (pos_status = proposed)"] = all(x["pos_status"] == "proposed" for x in reg)
    ck["registr: obsahuje všech 23 bodů tabulky"] = {r["id"] for r in rows} <= set(ids)
    tbl = {x["id"]: x for x in reg if x["origin"] == "geo_ref" and x["type"] != "coast_feature"}
    ck["registr: 20 bodů přesně podle tabulky, 3 s odchylkou"] = sum(1 for x in tbl.values() if not x.get("deviation")) == 20 and sum(1 for x in tbl.values() if x.get("deviation")) == 3

    def on_land_or_coast(x):
        pl = o["para"] if x.get("island") == "para" else o["main"]
        p = (x["x_km"], x["y_km"])
        if geom.point_in_poly(p, pl):
            return True
        return geom.nearest_on_poly(p, pl)[0] <= 0.2
    point_types = {"peak", "nature", "settlement", "port", "district", "industry", "airport", "rail_station", "poi"}
    bad = [x["id"] for x in reg if x["type"] in point_types and not on_land_or_coast(x)]
    ck["registr: bodové objekty leží na souši nebo na pobřeží"] = not bad
    info["registry_count"] = len(reg)
    info["registry_off_land"] = bad
    ck["registr: foto vodítko u všech bodových objektů"] = all(x.get("photo_guide") for x in reg if x["type"] in point_types)

    # ---- 4) kanon
    tr = list(csv.reader((ATLAS / "docs" / "canon_extract.csv").open(encoding="utf-8-sig"), delimiter=";"))
    h = tr[0]
    ci, si = h.index("atlas_objects"), h.index("status")
    appr = [r for r in tr[1:] if r[si] == "approved"]
    ck[f"kanon: všech {len(appr)} schválených tvrzení má odkaz na objekt atlasu nebo vysvětlení"] = all(r[ci].strip() for r in appr)
    ck["kanon: stavy `approved` v extrakci shodné s bible (validate_bible.py)"] = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_bible.py")], capture_output=True).returncode == 0
    orig_bad = []
    for line in (ATLAS / "docs" / "ORIGINALS_SHA256.txt").read_text(encoding="utf-8-sig").splitlines():
        hh, rel = line.split("  ", 1)
        if sha(ROOT / rel) != hh:
            orig_bad.append(rel)
    ck["originály projektu beze změny (14 souborů, SHA-256)"] = not orig_bad
    info["originals_changed"] = orig_bad

    # ---- 5) soubory
    xml_bad, gj_bad = [], []
    for f in (CUR / "svg").glob("*.svg"):
        try:
            ET.parse(f)
        except Exception:
            xml_bad.append(f.name)
    for f in CUR.rglob("*.geojson"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            if d.get("type") != "FeatureCollection" or not d["features"]:
                gj_bad.append(f.name)
        except Exception:
            gj_bad.append(f.name)
    ck["všechna SVG jsou validní XML"] = not xml_bad
    ck["všechna GeoJSON jsou validní a neprázdná"] = not gj_bad
    info["bad_svg"], info["bad_geojson"] = xml_bad, gj_bad

    # ---- 5b) atlas SVG a prohlížeč (F5)
    import re
    master = (CUR / "svg" / "larpidia_atlas_master.svg")
    if master.exists():
        svg = master.read_text(encoding="utf-8")
        need_layers = ["bg-sea", "land", "hypsometry", "hillshade", "landcover", "contours", "hydro", "settlements", "roads", "rail-L1", "rail-L2", "rail-L3",
                       "stations", "ports", "airports", "poi", "peaks", "labels-cs", "labels-ja", "labels-en", "marginalia"]
        have = set(re.findall(r'<g id="([^"]+)" inkscape:groupmode="layer"', svg))
        ck["atlas: hlavní SVG má všech 21 povinných vrstev (editovatelné, Inkscape)"] = all(l in have for l in need_layers)
        ids_in = set(re.findall(r'data-id="([^"]+)"', svg)) | set(re.findall(r'id="([^"]+)"', svg))
        line_pt = {"peak", "nature", "settlement", "port", "district", "industry", "airport", "rail_station", "poi", "road", "trail", "cycleway", "river", "rail_line", "infrastructure", "coast_feature", "other_line"}
        miss = [x["id"] for x in reg if x["type"] in line_pt and x["id"] not in ids_in]
        ck["atlas: každý objekt z registru je v hlavní mapě (data-id)"] = not miss
        info["atlas_missing_ids"] = miss
        ck["atlas: popisky text jsou skutečné <text> prvky ve 3 jazykových vrstvách"] = all(f'id="labels-{l}"' in svg for l in ("cs", "ja", "en")) and svg.count("<text") > 150
        ck["atlas: všechny varianty (master, physical, political, status) a schéma železnic existují"] = all((CUR / "svg" / f).exists() for f in (
            "larpidia_atlas_master.svg", "larpidia_atlas_physical.svg", "larpidia_atlas_political.svg", "larpidia_atlas_status.svg", "rail_scheme.svg"))
        vw = CUR / "viewer" / "atlas.html"
        ck["atlas: prohlížeč obsahuje celý registr a SVG"] = vw.exists() and f'"objects"' in vw.read_text(encoding="utf-8") and vw.stat().st_size > 400_000

    # ---- 5c) satelitní podklady (F6)
    rend = CUR / "renders"
    if (rend / "S-01_base.png").exists():
        import verify_sat as vs
        ok_iou = True
        ious = {}
        for nm in ("S-01", "S-02"):
            ref_land, ref_water = vs.reference_water(nm)
            from PIL import Image as _I, ImageFilter as _F
            import numpy as _np
            im = _I.open(rend / f"{nm}_base.png").convert("RGB")
            water = _np.asarray(_I.fromarray((vs.segment_water(_np.asarray(im)).astype(_np.uint8) * 255), "L").filter(_F.MedianFilter(7))) > 127
            m = vs.metrics(~ref_water, ~water)
            ious[nm] = round(m["iou"], 4)
            ok_iou &= m["iou"] >= 0.99
        ck["satelit: vlastní rendery S-01/S-02 drží tvar ostrova (IoU souše ≥ 0,99)"] = ok_iou
        info["sat_iou"] = ious
        g1 = json.loads((rend / "S-01_georef.json").read_text(encoding="utf-8"))
        ck["satelit: georeference nese SHA zmrazeného obrysu a plochu souše ≈ 175 km²"] = g1["coast_sha256"] == fro["coast_sha256"] and abs(g1["land_area_km2"] - 175.0) < 2.0
        ck["satelit: popisky (cs/ja/en) a prompty (EN, negativní omezení, označení simulace) existují"] = all((rend / f).exists() for f in (
            "S-01_labels_overlay.svg", "S-02_labels_overlay.svg", "S-01_with_labels.svg", "S-01_prompt.md", "S-02_prompt.md")) and "Negative" in (rend / "S-01_prompt.md").read_text(encoding="utf-8") and "Simulovaná satelitní" in (rend / "S-01_prompt.md").read_text(encoding="utf-8")
        for f in ("S-01_labels_overlay.svg", "S-02_labels_overlay.svg"):
            try:
                ET.parse(rend / f)
            except Exception:
                ck[f"satelit: {f} je validní XML"] = False
        cams = sorted(rend.glob("*_oblique_*_camera.json"))
        cam_ok = len(cams) >= 4
        for cf in cams:
            meta = json.loads(cf.read_text(encoding="utf-8"))
            cam_ok &= meta.get("status") == "proposed" and "vertical_exaggeration" in meta and (rend / f"{meta['id']}.jpg").exists()
        ck["satelit: přehled S-00 (+ georeference) a 4 šikmé pohledy s kamerou, statusem proposed a převýšením existují"] = cam_ok and all(
            (rend / f).exists() for f in ("S-00_overview.png", "S-00_overview.jpg", "S-00_georef.json", "OBLIQUE_PROMPTS.md", "README_RENDERS.md"))
        ck["satelit: kosmetické varianty s mraky existují a drží tvar (IoU ≥ 0,95 bez bílých ploch)"] = (rend / "S-01_base_clouds.jpg").exists() and (rend / "S-00_overview_clouds.jpg").exists() and vs.main(["S-01", str(rend / "S-01_base_clouds.jpg"), "--threshold", "0.95"]) == 0

    # ---- 6) snapshoty (neměnnost)
    snap_bad = []
    snaps = sorted((ATLAS / "versions").iterdir()) if (ATLAS / "versions").exists() else []
    for s in snaps:
        man = s / "MANIFEST.sha256"
        if not man.exists():
            snap_bad.append(s.name + ": chybí manifest")
            continue
        for line in man.read_text(encoding="utf-8").splitlines():
            hh, rel = line.split("  ", 1)
            p = s / rel
            if not p.exists() or sha(p) != hh:
                snap_bad.append(f"{s.name}/{rel}")
    ck[f"snapshoty ({len(snaps)}): manifesty sedí, nic se nezměnilo"] = not snap_bad
    info["snapshots"] = [s.name for s in snaps]
    info["snapshot_problems"] = snap_bad[:10]

    rep = {"atlas_version": canon.ATLAS_VERSION, "checks": ck, "all_ok": all(ck.values()), "info": info}
    (CUR / "registry" / "atlas_check_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in ck.items():
        print(("  OK    " if v else "  CHYBA ") + k)
    print("VÝSLEDEK:", "vše v pořádku" if rep["all_ok"] else "jsou chyby")
    return 0 if rep["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
