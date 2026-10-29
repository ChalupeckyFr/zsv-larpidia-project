"""Kanonická data atlasu Larpidie.

Zdroj: data/larpidia_world_bible.json (jediný zdroj pravdy) a tabulka v
references/GEOGRAPHY_AND_CANON.md (pracovní návrh). Tento soubor NIC nevymýšlí
nad rámec těchto podkladů; vše nové je označeno `origin = "atlas_new"` jinde.

Stavy (jako v bibli): approved / proposed / needs_decision.
Poloha všech bodů je dosud `proposed` (návrhová mapa), proto se u řádků tabulky
rozlišuje stav existence/jména (`exist_status`, `name_status`) a stav polohy (`pos_status`).
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # …/zsv-projects
ATLAS = ROOT / "atlas"
BIBLE_PATH = ROOT / "data" / "larpidia_world_bible.json"

# ---------------------------------------------------------------- rozhodnutí týmu
FRAME_W_KM = 24.0           # referenční obdélník hlavního ostrova (rozhodnuto týmem)
FRAME_H_KM = 16.0
MAIN_AREA_KM2 = 175.0       # bible: 150–200 approved, 175 proposed
PARA_AREA_KM2 = 14.0        # bible: proposed
STRAIT_KM = 1.5             # bible/GEOGRAPHY (rozhodnuto týmem; MAP_PROMPT 2–3 km se nepoužije)
MAIN_AREA_TOL = 3.0
PARA_AREA_TOL = 0.5
STRAIT_TOL = 0.05
DEVIATION_LIMIT_PCT = 3.0   # povolená odchylka bodů tabulky od původní polohy

LAT0, LON0 = 33.9, 137.6    # bible: working_coordinates (proposed, hypotetické)
CENTER_KM = (FRAME_W_KM / 2, FRAME_H_KM / 2)

# Plátno = A2 na výšku/šířku v měřítku 1 : 50 000 (594 × 420 mm = 29,7 × 21,0 km)
SCALE_DENOM = 50_000
CANVAS = {"x0": -0.2, "y0": -1.0, "w": 29.7, "h": 21.0}   # km, poloha vůči SZ rohu rámce

STATUSES = ("approved", "proposed", "needs_decision")
ATLAS_VERSION = "0.6.1-satbase"          # verze aktuálně generovaných výstupů (zvyšuje se při snapshotu)


def pct_to_km(X: float, Y: float) -> tuple[float, float]:
    return X / 100.0 * FRAME_W_KM, Y / 100.0 * FRAME_H_KM


def km_to_pct(x: float, y: float) -> tuple[float, float]:
    return x / FRAME_W_KM * 100.0, y / FRAME_H_KM * 100.0


def km_to_lonlat(x: float, y: float) -> tuple[float, float]:
    """Pseudo-WGS84 (HYPOTETICKÉ): rámec je vystředěn na working_coordinates z bible."""
    km_per_deg_lat = 110.95
    km_per_deg_lon = 111.32 * math.cos(math.radians(LAT0))
    lon = LON0 + (x - CENTER_KM[0]) / km_per_deg_lon
    lat = LAT0 - (y - CENTER_KM[1]) / km_per_deg_lat
    return round(lon, 6), round(lat, 6)


def load_bible() -> dict:
    return json.loads(BIBLE_PATH.read_text(encoding="utf-8"))


def bible_sha256() -> str:
    return hashlib.sha256(BIBLE_PATH.read_bytes()).hexdigest()


# ---------------------------------------------------------------- tabulka GEOGRAPHY_AND_CANON.md
# (id, název dle dokumentu, X %, Y %, „co musí být zachováno“ dle dokumentu,
#  kategorie, stav existence, stav jména, odkaz do bible)
_TABLE = [
    ("M-01", "Nejvyšší vrchol, pracovní 560 m", 29, 34, "lesnatý horský masiv na západě",
     "peak", "approved", "proposed", "geography.mountains; geography.highest_peak_m; geography.working_peak_m (560 m = proposed)"),
    ("M-02", "Lyžařská a paraglidingová hora", 38, 33, "menší přirozený spád, krátká zimní sezona",
     "peak", "approved", "proposed", "geography.mountains (prudší sjezdovková hora); geography.climate"),
    ("M-03", "Zaoblený turistický vrch", 22, 50, "výhledy, louky a značené trasy",
     "peak", "approved", "proposed", "geography.mountains (zaoblený vrchol pro turistiku a paragliding)"),
    ("N-01", "Skalní vyhlídka nad mořem", 12, 40, "bezpečný výhled, žádné pobídky ke skokům",
     "nature", "approved", "proposed", "geography.natural_features (10m pobřežní sráz s vyhlídkou); visitor_experience.activities_safety"),
    ("N-02", "Krystalová jeskyně", 38, 47, "průjezd zážitkové L1 po obvodu jeskyně",
     "nature", "approved", "proposed", "geography.natural_features (krystalová jeskyně s turistickou železnicí); mobility.rail_lines L1"),
    ("N-03", "Vodopád a horská řeka", 43, 54, "nedaleko jeskyně a přehrady",
     "nature", "approved", "proposed", "geography.natural_features (vodopády na horských řekách)"),
    ("N-04", "Přehradní jezero", 48, 61, "vodárenské dílo a rekreační pobřeží s ochranou zdroje",
     "nature", "approved", "proposed", "geography.natural_features (přehradní jezero)"),
    ("C-01", "Hlavní město (prac. Larpington)", 67, 76, "historické jižní centrum",
     "capital", "approved", "proposed", "urbanism.capital_roles; urbanism.capital_name (proposed)"),
    ("C-02", "Historický přístav hlavního města", 68, 87, "nábřeží, butiky a promenády",
     "port", "approved", "proposed", "urbanism.capital_roles (přístav); mobility.seaports (proposed)"),
    ("C-03", "Chalupecká čtvrť", 61, 76, "část centra",
     "district", "proposed", "proposed", "urbanism.capital_four_districts (proposed, D2)"),
    ("C-04", "Kynčlova čtvrť", 66, 71, "část centra",
     "district", "proposed", "proposed", "urbanism.capital_four_districts (proposed, D2)"),
    ("C-05", "Klimečkova čtvrť", 72, 76, "část centra",
     "district", "proposed", "proposed", "urbanism.capital_four_districts (proposed, D2)"),
    ("C-06", "Žemličkova čtvrť", 67, 81, "část centra",
     "district", "proposed", "proposed", "urbanism.capital_four_districts (proposed, D2)"),
    ("T-01", "Praha", 70, 49, "český toponym v obytné nížině",
     "town", "approved", "approved", "urbanism.must_include_towns"),
    ("T-02", "Čimprlichovo Hradiště", 48, 72, "historické městečko",
     "town", "approved", "approved", "urbanism.must_include_towns"),
    ("T-03", "Havlišovo Doupě", 17, 60, "horská venkovská obec",
     "town", "approved", "approved", "urbanism.must_include_towns"),
    ("T-04", "Ōru Maito (オールマイト)", 56, 20, "japonizované severní městečko",
     "town", "approved", "approved", "urbanism.must_include_towns"),
    ("T-05", "Aokawa (青川)", 73, 24, "další návrhové severní město",
     "town", "proposed", "proposed", "urbanism.other_towns (proposed)"),
    ("I-01", "Zelená průmyslová zóna", 82, 53, "továrny, zahrady, školy, restaurace",
     "industry", "approved", "proposed", "urbanism.industry_style"),
    ("I-02", "Závod na zpracování mořských řas", 88, 60, "exportní závod blízko nákladního přístavu",
     "industry", "proposed", "proposed", "economy.renewable_feedstock (proposed)"),
    ("I-03", "Nákladní přístav", 94, 64, "infrastruktura pro export",
     "port", "proposed", "proposed", "mobility.seaports (proposed)"),
    ("A-01", "Hlavní regionální letiště", 83, 37, "východní nížina, realistická vzletová dráha",
     "airport", "proposed", "proposed", "mobility.airports (proposed)"),
    ("P-01", "Spojení na Paraland", 82, 83, "třetí železniční linka pod vodou",
     "rail_link", "approved", "proposed", "geography.paraland_connection; mobility.rail_lines L3"),
]


def geo_ref_table(deviations: dict | None = None) -> list[dict]:
    """Tabulka GEOGRAPHY_AND_CANON.md. `deviations` = {id: (X %, Y %)} povolené odchylky (≤ 3 %).

    x_km/y_km jsou efektivní (případně odchýlené) polohy, *_orig původní z tabulky.
    """
    deviations = deviations or {}
    rows = []
    for (rid, name, X, Y, keep, cat, st_e, st_n, bref) in _TABLE:
        x0, y0 = pct_to_km(X, Y)
        Xn, Yn = deviations.get(rid, (X, Y))
        if abs(Xn - X) > DEVIATION_LIMIT_PCT + 1e-9 or abs(Yn - Y) > DEVIATION_LIMIT_PCT + 1e-9:
            raise ValueError(f"Odchylka {rid} překračuje {DEVIATION_LIMIT_PCT} %: ({Xn - X:+.1f}, {Yn - Y:+.1f})")
        x, y = pct_to_km(Xn, Yn)
        rows.append({
            "id": rid, "name_doc": name, "X_pct": Xn, "Y_pct": Yn, "x_km": round(x, 3), "y_km": round(y, 3),
            "X_pct_orig": X, "Y_pct_orig": Y, "x_km_orig": round(x0, 3), "y_km_orig": round(y0, 3),
            "deviated": (Xn, Yn) != (X, Y), "dev_pct": (round(Xn - X, 2), round(Yn - Y, 2)),
            "dev_km": round(math.dist((x, y), (x0, y0)), 3),
            "must_keep": keep, "category": cat,
            "exist_status": st_e, "name_status": st_n, "pos_status": "proposed",
            "origin": "geo_ref", "bible_ref": bref,
        })
    return rows


def table_by_id(deviations: dict | None = None) -> dict[str, dict]:
    return {r["id"]: r for r in geo_ref_table(deviations)}

# ---------------------------------------------------------------- zvolená (zmrazená) varianta obrysu
CHOSEN_VARIANT = "B"        # rozhodnutí R-06 (2026-10-23)
ACCEPTED_DEVIATIONS = {     # odchylky ≤ 3 % schválené volbou varianty B: id -> (X %, Y %)
    "T-04": (56, 23.0), "T-05": (73, 26.5), "A-01": (82, 40.0),
}


def load_outline() -> dict:
    """Zmrazená geometrie z current/geometry/outline_coast.json: hlavní ostrov, Paraland, typy pobřeží po vrcholech."""
    d = json.loads((ATLAS / "current" / "geometry" / "outline_coast.json").read_text(encoding="utf-8"))

    def types(runs, n):
        out = [None] * n
        for a, b, t in runs:
            for i in range(a, b + 1):
                out[i] = t
        return out

    main = [tuple(p) for p in d["main"]["vertices"]]
    para = [tuple(p) for p in d["paraland"]["vertices"]]
    return {"main": main, "para": para,
            "main_types": types(d["main"]["coast_type_runs"], len(main)),
            "para_types": types(d["paraland"]["coast_type_runs"], len(para))}


def table_rows() -> list[dict]:
    """Tabulka GEOGRAPHY s přijatými odchylkami (efektivní polohy zvolené varianty)."""
    return geo_ref_table(ACCEPTED_DEVIATIONS)
