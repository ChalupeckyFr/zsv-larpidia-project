"""F4 – doplňky registru: matice dohledatelnosti kanonu, patch bible, dokument ke schválení."""
from __future__ import annotations

import csv
import json
from pathlib import Path

TRACE = {
    "K-001": ["LARPIDIA_MAIN", "PARALAND"], "K-002": ["places.json:lonlat_pseudo"], "K-003": ["LARPIDIA_MAIN"], "K-004": ["LARPIDIA_MAIN"], "K-005": ["PARALAND"],
    "K-006": ["LARPIDIA_MAIN", "PARALAND"], "K-007": ["PARALAND"], "K-008": ["L3", "ST-L3-06", "ST-L3-07", "rail_lines:undersea", "rail_lines:glass_gallery"],
    "K-009": ["PARALAND", "STRAIT"], "K-010": ["STRAIT"], "K-011": ["M-01", "M-02", "M-03"], "K-012": ["M-01"], "K-013": ["M-01", "M-02", "M-03", "SK-01", "PG-01"],
    "K-014": ["SK-01", "M-02"], "K-015": ["landcover:forest", "landcover:meadow", "SP-01", "N-03", "N-04", "N-02", "N-01", "B-01", "coast_classes"],
    "K-016": ["RD-R1"], "K-017": ["CY-01", "TR-01", "SP-01"], "K-018": ["places.json:region"], "K-019": ["C-02 (vlnolam)", "places.json:photo_guide.season"],
    "K-020": ["C-01"], "K-021": ["C-03", "C-04", "C-05", "C-06"], "K-022": ["T-01", "T-02", "T-03", "T-04"], "K-023": ["T-05", "T-06"], "K-024": ["places.json:photo_guide.styles"],
    "K-025": ["C-01", "C-02", "ST-W", "L3"], "K-026": ["I-01"], "K-027": ["PL-01", "PL-02", "PL-03", "PL-04", "PL-06", "H-02"], "K-028": ["H-02", "ST-L3-07", "HV-01"],
    "K-029": ["HV-01", "HV-02", "HV-03"], "K-030": ["n/a nespaciální (vizuální vodítko: elektrické klasické vozy)"], "K-031": ["n/a pro F7 (půjčovny v plánu hlavního města)"],
    "K-032": ["L1", "L2", "L3"], "K-033": ["L1", "L2", "L3"], "K-034": ["L3"], "K-035": ["C-02", "I-03", "H-01", "H-02"], "K-036": ["A-01", "A-02"], "K-037": ["I-02"],
    "K-038": ["n/a bez polohy (O15: nezakreslovat)"], "K-039": ["I-01", "I-02", "I-03"], "K-040": ["C-02 (O16, návrh)"], "K-041": ["landcover:terraces"],
    "K-042": ["n/a pro F7 (muzeum v plánu hlavního města)"], "K-043": ["V-02", "V-03", "V-06", "N-01", "TR-01"],
    "K-044": ["svg/physical_preview.svg", "svg/landcover_preview.svg", "svg/transport_preview.svg", "pending F5–F8 (politická, historická, satelit, plán města)"],
    "K-045": ["docs/CONFLICTS_AND_DECISIONS.md"], "K-050": ["north-up v SVG"], "K-051": ["LARPIDIA_MAIN"], "K-052": ["BAY-N1", "BAY-N2", "BAY-S", "CAPE-W", "PEN-SE"],
    "K-053": ["PARALAND", "H-02", "PL-01"], "K-054": ["W-01", "N-02", "N-03", "N-04"], "K-055": ["I-01", "A-01"], "K-056": ["B-01", "C-01", "C-02"],
    "K-057": ["places.json:X_pct,Y_pct"], "K-058": ["PL-01", "PL-02", "PL-03", "PL-04", "H-02", "TR-PL1"], "K-059": ["A-02"], "K-060": ["L1"], "K-061": ["L2"], "K-062": ["L3"],
    "K-063": ["RD-R1", "L1"], "K-064": ["places.json:photo_guide", "photo_guide.csv"], "K-065": ["pending F7"], "K-070": ["STRAIT"], "K-071": ["pending F6"],
    "K-072": ["navrženo CP-01 (pending F7)"], "K-073": ["pending F8"], "K-074": ["svg layers"], "K-075": ["places.json:photo_guide.avoid"], "K-076": ["A-01", "A-02"],
    "K-077": ["rail_lines:glass_gallery"], "K-078": ["L1", "N-02"], "K-079": ["C-02 (vlnolam)"], "K-080": ["n/a pravidlo priority"],
}


def update_trace(objs, docs: Path):
    path = docs / "canon_extract.csv"
    rows = list(csv.reader(path.open(encoding="utf-8-sig"), delimiter=";"))
    head = rows[0]
    ci = head.index("atlas_objects")
    ids = {o["id"] for o in objs}
    out = []
    for r in rows[1:]:
        cid = r[0]
        if cid in TRACE:
            r[ci] = " | ".join(TRACE[cid])
        elif cid.startswith("K-1"):
            first = r[2].split(" ")[0]
            r[ci] = first if first in ids else ""
        out.append(r)
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(head)
        w.writerows(out)
    return out


def write_patch(objs, meta, docs: Path, atlas: Path, human: Path):
    rel = json.loads((atlas / "current" / "relief" / "relief_report.json").read_text(encoding="utf-8"))
    hum = json.loads((human / "human_report.json").read_text(encoding="utf-8"))
    out = json.loads((atlas / "current" / "geometry" / "outline_report.json").read_text(encoding="utf-8"))
    frozen = json.loads((atlas / "current" / "geometry" / "outline_FROZEN.json").read_text(encoding="utf-8"))

    def node(v, note=""):
        return {"value": v, "status": "proposed", "note": note}

    table = {o["id"]: {"X_pct": o["X_pct"], "Y_pct": o["Y_pct"], "x_km": o["x_km"], "y_km": o["y_km"]} for o in objs if o["origin"] == "geo_ref" and o["type"] != "coast_feature"}
    st = hum["stats"]
    patch = [
        {"op": "add", "path": "/geography/atlas_frame", "value": node({"frame_km": [24, 16], "canvas_a2_scale": "1:50000 (594×420 mm)", "variant": "B", "coast_sha256": frozen["coast_sha256"]},
                                                                      "R-01, R-06: rámec 24×16 km, varianta B obrysu; geometrie v atlas/current/geometry/outline_coast.json")},
        {"op": "add", "path": "/geography/main_island_area_model_km2", "value": node(out["main"]["area_km2"], "modelová plocha z vektorového obrysu (cíl 175)")},
        {"op": "add", "path": "/geography/paraland_area_model_km2", "value": node(out["para"]["area_km2"], "cíl 14")},
        {"op": "add", "path": "/geography/strait_model_km", "value": node(out["strait_km"], "nejmenší vzdálenost hlavní ostrov – Paraland")},
        {"op": "add", "path": "/geography/coordinates_table_v1_1", "value": node(table, "polohy z tabulky GEOGRAPHY po přijetí 3 odchylek ≤ 3 % (T-04, T-05, A-01)")},
        {"op": "add", "path": "/geography/peaks_model_m", "value": node({k: rel["elevations_m_model"][k] for k in ("M-01", "M-02", "M-03")}, "M-01 = working_peak_m 560; M-02, M-03 modelové")},
        {"op": "add", "path": "/geography/hydrology_model", "value": node({"lake_level_m": rel["lake"]["level_m_model"], "lake_area_km2": rel["lake"]["area_km2"], "dam_height_m": rel["lake"]["dam_height_m_model"],
                                                                           "waterfall_drop_m": round(rel["waterfall"]["top_m"] - rel["waterfall"]["bottom_m"], 1), "cave_elev_m": rel["elevations_m_model"]["N-02"]},
                                                                          "modelové hodnoty pro vodárenské dílo, vodopád a jeskyni")},
        {"op": "add", "path": "/urbanism/town_ids", "value": node({"Hoshimachi": "T-06", "Aokawa": "T-05"}, "ID pro města z other_towns")},
        {"op": "add", "path": "/urbanism/population_distribution_model", "value": node({"Larpington": 12000, "Praha": 4500, "Aokawa": 2600, "Ōru Maito": 2300, "Čimprlichovo Hradiště": 2000,
                                                                                       "Hoshimachi": 1600, "Havlišovo Doupě": 700, "Zelená průmyslová zóna": 600, "Paraland": 1400,
                                                                                       "osady (6×200)": 1200, "roztroušeně": 3100}, "součet 32 000; modelové, ne sčítání")},
        {"op": "add", "path": "/mobility/rail_network_model", "value": node({"L1": {"km": st["rail_km"]["L1"], "max_grade_pct": st["L1_max_grade_pct"], "stations": ["Larpington Západ", "Přehrada", "Vodopád", "Krystalová jeskyně", "Horská stanice"]},
                                                                            "L2": {"km": st["rail_km"]["L2"], "stations": 13},
                                                                            "L3": {"km": st["rail_km"]["L3"], "undersea_m": st["L3_undersea_m"], "glass_m": st["L3_glass_m"], "transfers_to_L2": 3}},
                                                                           "vedení a stanice návrh; role linek schváleny")},
        {"op": "add", "path": "/mobility/seaports_ids", "value": node({"C-02": "historický", "I-03": "nákladní", "H-01": "severní rybářský", "H-02": "marina Paraland"}, "≥ 3 přístavy (approved), ID návrh")},
        {"op": "add", "path": "/mobility/airports_detail", "value": node({"A-01": {"runway": "09/27", "length_m": 1900}, "A-02": {"runway": "04/22 travnatá", "length_m": 700}}, "dvě letiště (návrh), Paraland jen malá plocha")},
        {"op": "add", "path": "/mobility/road_network_model", "value": node({"R1_km": st["R1_km"], "R1_tunnels_km": st["R1_tunnel_km"], "R2_km": st["roads_km"]["R2"], "R3_km": st["roads_km"]["R3"],
                                                                           "trails_km": st["trails_km"], "cycleways_km": st["cycleways_km"]}, "R1 v SZ po útesech do 293 m a v 3 tunelech")},
        {"op": "add", "path": "/open_decisions/-", "value": {"id": "D7", "question": "Potvrdit obrys (varianta B) a tři odchylky ≤ 3 % (T-04, T-05, A-01).", "suggestion": "Viz atlas/current/registry/deviations.csv"}},
        {"op": "add", "path": "/open_decisions/-", "value": {"id": "D8", "question": "Potvrdit vedení L1/L2/L3, stanice a okružní silnici R1 (útesy + 3 tunely).", "suggestion": "Viz atlas/docs/F3_HUMAN_NOTES.md"}},
        {"op": "add", "path": "/open_decisions/-", "value": {"id": "D9", "question": "Potvrdit pracovní jména vrcholů, řek, zátok a míst na Paralandu.", "suggestion": "Viz atlas/docs/NAMES_AND_DEVIATIONS_TO_APPROVE.md"}},
    ]
    doc = {"patch_meta": {"target_file": "data/larpidia_world_bible.json", "base_version": meta["bible_version"], "base_sha256": meta["bible_sha256"], "proposed_version": "1.1-draft",
                          "format": "JSON Patch (RFC 6902) – NEAPLIKOVAT automaticky; sloučit až po schválení týmem", "atlas_version": meta["atlas_version"],
                          "rule": "originál bible se nemění (R-03); všechny položky mají status proposed"}, "patch": patch}
    (docs / "bible_patch_v1.1.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")


def write_names_doc(objs, docs: Path, reg: Path, names: dict, bays: list):
    dev = [o for o in objs if o.get("deviation")]
    rows = [(i, *names[i]) for i in names] + [(b[0], b[1], b[2], b[3]) for b in bays]
    with (reg / "names_proposed.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["id", "česky", "anglicky", "japonsky", "stav", "schválit"])
        for n in rows:
            w.writerow([n[0], n[1], n[2], n[3], "proposed", ""])
    L = ["# K schválení: odchylky od tabulky a návrh jmen (atlas v0.4-registry)", "",
         "Vše je **pracovní návrh**. Označte u každé řádky *schváleno / upravit* a pošlete zpět; schválené změny se zapíšou do `bible_patch_v1.1.json` a po schválení D1 do bible.", "",
         "## 1. Odchylky od polohy v tabulce GEOGRAPHY (mezní hodnota 3 %)", "",
         "| ID | Název | Původní X/Y | Nové X/Y | Odchylka | Schválit |", "|---|---|---|---|---|---|"]
    for o in dev:
        d = o["deviation"]
        L.append(f"| {o['id']} | {o['name_cs']} | {o['geo_ref_pct_orig'][0]} / {o['geo_ref_pct_orig'][1]} % | {o['X_pct']} / {o['Y_pct']} % | {d['dx_pct']:+.1f} / {d['dy_pct']:+.1f} % ({d['dev_km']} km) | ☐ |")
    L += ["", "Důvod: stáhnout severní obal bodů a uvolnit místo pro hlubší severní zátoky, výraznější mys a delší poloostrov (volba varianty B, R-06). Zbylých 20 bodů je přesně podle tabulky.", "",
          "## 2. Navržená jména (česky / anglicky / japonsky)", "", "| ID | Česky | Anglicky | Japonsky | Schválit |", "|---|---|---|---|---|"]
    for n in rows:
        L.append(f"| {n[0]} | {n[1]} | {n[2]} | {n[3]} | ☐ |")
    L += ["", "Jména povinných měst (Praha, Čimprlichovo Hradiště, Havlišovo Doupě, Ōru Maito) jsou **schválená**; ostatní jsou návrh. Japonské zápisy jsou orientační a před tiskem je má zkontrolovat rodilý mluvčí.", "",
          "## 3. Další body k potvrzení", "",
          "- **R1 na severozápadě** vede po útesech až do 293 m a ve 3 tunelech (2,2 km), protože pod M-01 není pobřežní pás.",
          "- **L3** je jedna linka: městský okruh (Západ, Sever, Východ, Střed–Přístav) + větev na Paraland; přestupy na L2 jsou právě 3.",
          "- **Hoshimachi** dostalo ID T-06 a polohu ve východní severní zátoce.",
          "- **Populace** je modelové rozdělení 32 000 (28 900 v sídlech, 3 100 roztroušeně).",
          "- Značky směrů v registru: S = sever, J = jih, V = východ, Z = západ (SV = severovýchod apod.).", ""]
    (docs / "NAMES_AND_DEVIATIONS_TO_APPROVE.md").write_text("\n".join(L), encoding="utf-8")
