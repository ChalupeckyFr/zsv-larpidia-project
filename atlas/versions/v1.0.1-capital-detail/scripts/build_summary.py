"""F8: shrnutí pro tým a kontrolní seznam ke schválení (generováno z registrů, takže čísla nelžou).

Spuštění:  python atlas/scripts/build_summary.py
Výstup:    atlas/docs/FINAL_SUMMARY.md, atlas/docs/TEAM_APPROVAL_CHECKLIST.md
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import canon
from canon import ATLAS

CUR = ATLAS / "current"
DOCS = ATLAS / "docs"


def read_csv(path):
    with path.open(encoding="utf-8-sig") as fh:
        return list(csv.reader(fh, delimiter=";"))


def main():
    reg = json.loads((CUR / "registry" / "places.json").read_text(encoding="utf-8"))["objects"]
    cap = json.loads((CUR / "capital" / "cp_objects.json").read_text(encoding="utf-8"))["objects"]
    rep = json.loads((CUR / "capital" / "cp_report.json").read_text(encoding="utf-8"))
    human = json.loads((CUR / "human" / "human_report.json").read_text(encoding="utf-8"))
    relief = json.loads((CUR / "relief" / "relief_report.json").read_text(encoding="utf-8"))
    canon_rows = read_csv(DOCS / "canon_extract.csv")
    head = canon_rows[0]
    st_i = head.index("status")
    claims = Counter(r[st_i] for r in canon_rows[1:])
    ex = Counter(o["exist_status"] for o in reg)
    nm = Counter(o["name_status"] for o in reg)
    ps = Counter(o["pos_status"] for o in reg)
    cex = Counter(o["exist_status"] for o in cap)
    types = Counter(o["type"] for o in reg)
    approved_ids = sorted(o["id"] for o in reg if o["exist_status"] == "approved")
    dev = read_csv(CUR / "registry" / "deviations.csv")[1:]
    names = read_csv(CUR / "registry" / "names_proposed.csv")[1:]
    snaps = sorted(p.name for p in (ATLAS / "versions").iterdir()) if (ATLAS / "versions").exists() else []
    s = rep["stats"]
    v = canon.ATLAS_VERSION

    def cz(x):
        """Číslo s desetinnou čárkou."""
        return str(x).replace(".", ",")

    L = [f"# Atlas Larpidie a Paralandu – shrnutí pro tým (verze {v})", "",
         "Kanonický geografický podklad pro satelitní vizualizace (S-01, S-02), plán hlavního města a budoucí fotografie a videa. **Všechno je fikce a pracovní návrh**, dokud tým neschválí tři body v sekci 4. Originály projektu (bible, reference, šablony) se nezměnily (SHA-256 v `ORIGINALS_SHA256.txt`).", "",
         "## 1. Co tým dostává", "",
         "| Co | Kde | Poznámka |", "|---|---|---|",
         "| Zmrazený obrys obou ostrovů (varianta B) | `current/geometry/` | 175,0 km² a 13,98 km², průliv 1,50 km, rámec 24 × 16 km, SHA-256 obrysu v každém výstupu |",
         f"| Reliéf, vody, krajina | `current/relief/` | DEM 20 m, max. {cz(relief['elevations_m_model']['M-01'])} m (modelové), řeka → jeskyně → vodopád → přehrada |",
         f"| Doprava, sídla, přístavy, letiště | `current/human/` | R1 {cz(human['stats']['R1_km'])} km, L1 {cz(human['stats']['rail_km']['L1'])} km, L2 {cz(human['stats']['rail_km']['L2'])} km, L3 {cz(human['stats']['rail_km']['L3'])} km (podmoří {human['stats']['L3_undersea_m']} m) |",
         f"| Registr míst | `current/registry/` | {len(reg)} objektů, foto/video vodítko u bodových objektů |",
         "| Atlas jako mapa a prohlížeč | `current/svg/`, `current/viewer/atlas.html` | A2 1 : 50 000, vrstvy, popisky cs/ja/en, režim kánon × návrh |",
         "| Satelitní podklady a šikmé pohledy | `current/renders/` | S-00 (přehled), S-01 Larpidie, S-02 Paraland, **S-03 Larpington (2 m/px, domy z plánu města, výškový model budov)**, 6 šikmých pohledů (z toho 2 na Larpington s hmotami budov), masky, prompty, `verify_sat.py` |",
         f"| Plán hlavního města Larpingtonu (CP-01) | `current/capital/` | A2 1 : 10 000, {s['edges']} úseků ulic ({cz(s['streets_km_total'])} km), {s['blocks']} bloků, {s['houses']['houses']} ilustrativních domů (kapacita {s['houses']['capacity']} obyv.), {len(cap)} objektů |",
         "| Rozhodnutí, rozpory, otázky | `docs/CONFLICTS_AND_DECISIONS.md` | R-01…R-07, C-01…C-22, O1…O25 |",
         "| Návrh změn bible | `docs/bible_patch_v1.1.json` | neaplikováno; slučuje se až po schválení |",
         "| Historie verzí | `versions/`, `CHANGELOG.md` | " + f"{len(snaps)} neměnných snapshotů" + " |", "",
         "## 2. Jak to používat", "",
         "1. **Mapa:** otevřete `current/viewer/atlas.html` (hledání, vrstvy, jazyky). Pro úpravy `current/svg/larpidia_atlas_master.svg` (Inkscape).",
         "2. **Satelit a fotky:** do externího generátoru vždy vložte referenci (`current/renders/S-01_base.png` apod.) a prompt z `S-0x_prompt.md`; výsledek ověřte `python atlas/scripts/verify_sat.py S-01 obraz.png`. Šikmé pohledy: `OBLIQUE_PROMPTS.md`.",
         "3. **Plán města:** `current/capital/capital_plan_viewer.html` a `capital_plan_base.svg`; zadání další etapy je v `docs/CAPITAL_PLAN_BRIEF.md`.",
         "4. **Foto/video:** před každým záběrem vezměte řádek z `registry/photo_guide.csv` nebo `capital/cp_photo_guide.csv` (*pohled kam, blízké a vzdálené body, styl, roční doba, čemu se vyhnout*).", "",
         "## 3. Co je schváleno a co je návrh", "",
         f"- **Kanon z bible/šablon:** {sum(claims.values())} tvrzení v `canon_extract.csv`: {claims.get('approved', 0)} schválených, {claims.get('proposed', 0)} navržených, {claims.get('needs_decision', 0)} k rozhodnutí. Každé schválené tvrzení má v atlasu odkaz na objekt nebo vysvětlení.",
         f"- **Objekty atlasu ({len(reg)}):** existence `approved` {ex.get('approved', 0)} · `proposed` {ex.get('proposed', 0)} · `needs_decision` {ex.get('needs_decision', 0)}; jména `approved` {nm.get('approved', 0)}, `proposed` {nm.get('proposed', 0)}; **polohy `proposed` u všech {ps.get('proposed', 0)}**.",
         f"- **Objekty plánu města ({len(cap)}):** existence `approved` {cex.get('approved', 0)} (parlament, muzeum, historický přístav, pobřežní silnice, promenáda, plán), ostatní `proposed`; všechny polohy a jména `proposed`.",
         f"- Schválená existence u objektů atlasu: {', '.join(approved_ids[:40])}{' …' if len(approved_ids) > 40 else ''}.",
         "- **Modelové hodnoty** (ne měření, ne kánon): výšky vrcholů, hladina a hráz přehrady, výška vodopádu, populace sídel (součet 32 000), délky tras, zastavěné území, sklony.",
         "- Pseudo-souřadnice (kolem 33,9 N / 137,6 E) jsou **hypotetické**; satelitní obrázky jsou **simulace**, ne družicová data.", "",
         "## 4. Nejvýše tři otevřené body k rozhodnutí týmu", "",
         "Pro zmrazení **v1.0** stačí rozhodnout tyto tři skupiny; zbytek platí jako výchozí volba, pokud tým nenamítne.", "",
         f"1. **Geometrie a polohy (D1, D7).** Potvrdit obrys varianty B, rámec 24 × 16 km a {len(dev)} odchylky ≤ 3 % od tabulky ({', '.join(r[0] for r in dev)}); polohy všech bodů jsou zatím `proposed`.",
         f"2. **Doprava a hlavní město (D8, D10, D11, D12).** Potvrdit vedení R1/L1/L2/L3 (R1 po útesech a ve 3 tunelech, právě 3 přestupy L2↔L3), kompozici města (Náměstí čtyř × parlament u přístavu), zastavěné území {cz(s['footprint_km2'])} km² (zastavěno je jen jádro pro {s['houses']['target_population']:.0f} obyvatel, zbytek je rezerva rozvoje, C-22) a napojení na přístav, polohu hotelu HV-01 a muzea.",
         f"3. **Jména a modelová čísla (D2, D5, D9).** Potvrdit {len(names)} navržených jmen (`registry/names_proposed.csv`), jména čtvrtí a ulic plánu, rozlohy (175 + 14 km²), populaci 32 000 a výšky vrcholů. D6 (barvy vlajky) ovlivní jen paletu map.", "",
         "Podrobný seznam k zaškrtnutí: `docs/TEAM_APPROVAL_CHECKLIST.md`.", "",
         "## 5. Poctivě: omezení", "",
         "- Nebyl vytvořen žádný fotorealistický obraz ani družicová data; S-00…S-02 a šikmé pohledy jsou procedurální reference, ze kterých externí generátor (s referenčním obrázkem) vytvoří realistickou verzi. Tvar se ověřuje IoU maskou.",
         f"- Procedurální jsou i ulice a bloky plánu města; **domy v plánu, v S-03 a v šikmých pohledech jsou ilustrativní půdorysy** ({s['houses']['houses']} domů vzniká v blocích podle využití a je kalibrováno na modelovou populaci Larpingtonu), nejsou to skutečné budovy. Plné zastavění všech bloků by dalo ≈ {s['houses']['full_buildout_capacity']} obyvatel, víc než schválený strop 40 000 pro celou zemi (C-22).",
         "- Geometrie přístavní pánve C-02 z F3 není čistý polygon (C-21); plán kreslí odvozenou vodní plochu.",
         "- Historická mapa 1608–1800 zatím nevznikla.", "",
         "## 6. Co dál", "",
         "1. Tým zaškrtne `TEAM_APPROVAL_CHECKLIST.md` → atlas **v1.0 (freeze)**, patch se sloučí do bible jako 1.1.",
         "2. Dopracování detailního plánu města podle připomínek týmu (`CAPITAL_PLAN_BRIEF.md`: výřezy 1 : 2 500, adresní vrstva) a historická mapa 1608–1800.",
         "3. Fotografie a videa z vodítek v registrech, vždy s referenčním obrázkem a kontrolou tvaru.", ""]
    (DOCS / "FINAL_SUMMARY.md").write_text("\n".join(L), encoding="utf-8")

    C = [f"# Kontrolní seznam ke schválení (atlas {v})", "",
         "Zaškrtněte *schváleno*, nebo napište změnu. Cokoli nezaškrtnuté zůstává `proposed`. Po vyplnění se změny zapíšou do `bible_patch_v1.1.json` (nová minor verze atlasu) a atlas se zmrazí jako v1.0.", "",
         "## 1. Geometrie a polohy (D1, D7)", "",
         "| ☐ | Položka | Výchozí volba | Kde |", "|---|---|---|---|",
         "| ☐ | Obrys ostrovů – varianta B | zmrazeno (SHA-256 `ffca09ac…`) | `current/geometry/` |",
         "| ☐ | Rámec 24 × 16 km, průliv 1,5 km | ponechat | `docs/CONFLICTS_AND_DECISIONS.md` R-01 |"]
    for r in dev:
        C.append(f"| ☐ | Odchylka {r[0]} {r[1]}: {r[2]}/{r[3]} → {r[4]}/{r[5]} % ({r[8]} km) | přijmout | `registry/deviations.csv` |")
    C += ["| ☐ | Polohy ostatních 20 bodů z tabulky GEOGRAPHY | beze změny | `registry/places.csv` |", "",
          "## 2. Doprava a hlavní město (D8, D10, D11, D12)", "",
          "| ☐ | Položka | Výchozí volba | Kde |", "|---|---|---|---|",
          "| ☐ | R1: útesy ≤ 293 m a 3 tunely (2,2 km) v SZ | potvrzeno jako návrh (R-07) | `docs/F3_HUMAN_NOTES.md` |",
          "| ☐ | L1 jako linka s koncovou smyčkou v jeskyni (~262°) | potvrzeno jako návrh | tamtéž |",
          "| ☐ | L2 oblouk Západ–Sever–Východ, L3 okruh + větev na Paraland, 3 přestupy | potvrzeno jako návrh | tamtéž |",
          "| ☐ | Přístavy C-02, I-03, H-01, H-02; letiště A-01 (1 900 m) a A-02 (700 m) | návrh | `current/human/ports_airports.geojson` |",
          "| ☐ | O19: parlament uprostřed Náměstí čtyř a čtyři správní budovy ve větrníku | ano (alternativa: parlament u přístavu) | `docs/F7_CAPITAL_NOTES.md` |",
          f"| ☐ | Zastavěné území hlavního města {s['footprint_km2']} km² (staré město u přístavu, Východní nábřeží, zelené klíny) | ano | C-18 |",
          f"| ☐ | Stav zástavby: zastavěno jádro pro {s['houses']['target_population']:.0f} obyvatel, ostatní bloky rezerva rozvoje (alternativy: menší vymezené území, nebo vyšší populace Larpingtonu při součtu ≤ 40 000) | ano | C-22 |",
          "| ☐ | Hotel HV-01 na promenádě, muzeum u Centrálního parku | ano | C-19, O22 |",
          "| ☐ | Prodloužení tepny RD-12 k nábřeží (Přístavní třída) | ano | C-20 |",
          "| ☐ | Vzhled satelitních podkladů S-01/S-02 po doladění | schválit nebo napsat, co vadí | `current/renders/` |", "",
          "## 3. Jména a modelová čísla (D2, D5, D9)", "",
          "| ☐ | Položka | Výchozí volba | Kde |", "|---|---|---|---|",
          f"| ☐ | {len(names)} navržených jmen míst (cs/en/ja) | ponechat jako pracovní | `registry/names_proposed.csv` |",
          "| ☐ | Larpington a čtyři čtvrtě (Chalupecká, Kynčlova, Klimečkova, Žemličkova) | D2 | `docs/NAMES_AND_DEVIATIONS_TO_APPROVE.md` |",
          "| ☐ | Názvy ulic a míst plánu města (O25) | pracovní | `capital/cp_objects.csv` |",
          "| ☐ | Rozlohy 175 + 14 km², populace 32 000 (modelové rozdělení) | D5, C-16 | `docs/F3_HUMAN_NOTES.md` |",
          f"| ☐ | Výšky vrcholů M-01 {relief['elevations_m_model']['M-01']} m (kanon 560), M-02 {relief['elevations_m_model']['M-02']} m, M-03 {relief['elevations_m_model']['M-03']} m (modelové) | ponechat | `docs/F2_RELIEF_NOTES.md` |",
          "| ☐ | O15: poloha larpiditu se nezakresluje | beze změny | O15 |", "",
          "## Po schválení", "", "1. `atlas/scripts/snapshot.py v1.0 …` (zmrazení), 2. sloučení patche do `data/larpidia_world_bible.json` jako verze 1.1 (jen po výslovném souhlasu týmu), 3. nový SHA-256 originálů do `ORIGINALS_SHA256.txt`.", ""]
    (DOCS / "TEAM_APPROVAL_CHECKLIST.md").write_text("\n".join(C), encoding="utf-8")
    print("shrnutí a kontrolní seznam zapsány:", DOCS / "FINAL_SUMMARY.md")


if __name__ == "__main__":
    main()
