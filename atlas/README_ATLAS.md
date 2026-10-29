# Atlas Larpidie a Paralandu (Larpidia Creative Studio) – verze 1.0-draft

Kanonický geografický podklad pro satelitní vizualizace (S-01, S-02), plán hlavního města Larpingtonu a všechny budoucí fotky a videa.
**Vše je fikce.** Polohy, výšky, trasy a jména jsou *pracovní návrh* (`proposed`); schválená je jen existence prvků podle World Bible, dokud tým neschválí tři body ze `docs/FINAL_SUMMARY.md` (sekce 4). Originály projektu (bible, reference, šablony) se nemění, jejich SHA-256 jsou v `docs/ORIGINALS_SHA256.txt`.

## Rychlý start

1. **Mapa:** otevřete `current/viewer/atlas.html` (jeden soubor, funguje offline): hledání, vrstvy, jazyky popisků (CS/JA/EN), režim *kánon × návrh*, kliknutím na objekt se zobrazí záznam z registru a foto/video vodítko.
2. **Mapy pro tisk a úpravy:** `current/svg/larpidia_atlas_master.svg` (vrstvené, Inkscape), `…_physical.svg`, `…_political.svg`, `…_status.svg`, `rail_scheme.svg`. Tisk A2 (594 × 420 mm) je přesně **1 : 50 000**; 1 jednotka SVG = 1 m. Soubory `*_embedded.svg` mají obrázky vložené.
3. **Satelitní podklady a šikmé pohledy:** `current/renders/` – `S-01_base` (Larpidie), `S-02_base` (Paraland), `S-03_base` (Larpington, 2 m/px) s výškovým modelem budov `S-03_buildings_height.png`, `S-00_overview`, šest šikmých pohledů (z toho `S-03_oblique_S` a `S-03_oblique_W` na Larpington s hmotami budov), masky, georeference, popisky a prompty (`S-0x_prompt.md`, `OBLIQUE_PROMPTS.md`). Jsou to **simulace**; do externího generátoru vždy vložte referenční obrázek a výsledek ověřte `python atlas/scripts/verify_sat.py S-01 obraz.png`.
4. **Plán hlavního města:** `current/capital/capital_plan_viewer.html` (prohlížeč) a `capital_plan_base.svg` (A2, 1 : 10 000, vrstvy cs/en/ja, včetně ilustrativních domů a rezervy rozvoje). Domy a stav zástavby: `cp_houses.geojson`, `docs/F9_CAPITAL_DETAIL_NOTES.md`. Zadání dalších úprav: `docs/CAPITAL_PLAN_BRIEF.md`.
5. **Registry:** `current/registry/places.csv` a `places.json` (159 objektů atlasu, foto/video vodítko), `current/capital/cp_objects.csv` (968 objektů plánu), `photo_guide.csv`, `deviations.csv`, `names_proposed.csv`.
6. **Rozhodnutí týmu:** `docs/FINAL_SUMMARY.md` a `docs/TEAM_APPROVAL_CHECKLIST.md`.

## Obsah

| Složka | Obsah |
|---|---|
| `current/geometry/` | zmrazený obrys (varianta B): `outline_coast.json`, GeoJSON v km a pseudo-WGS84, report |
| `current/relief/` | DEM 20 m (16bit PNG), stínování, vrstevnice, hydrografie, pokryv krajiny, typy pobřeží |
| `current/human/` | sídla, silnice, stezky a cyklotrasy, železnice L1–L3 + stanice, přístavy a letiště, body zájmu |
| `current/registry/` | registr 159 objektů, foto/video vodítko, odchylky, návrh jmen, `atlas_check_report.json` |
| `current/svg/`, `current/viewer/` | mapy a prohlížeč atlasu |
| `current/renders/` | satelitní podklady S-00…S-03, šikmé pohledy, masky, georeference, popisky, prompty |
| `current/capital/` | plán hlavního města: SVG, prohlížeč, graf, GeoJSON (m i km atlasu; vrstvy včetně domů), registr, vodítko, report |
| `docs/` | `FINAL_SUMMARY.md`, `TEAM_APPROVAL_CHECKLIST.md`, `CONFLICTS_AND_DECISIONS.md`, `canon_extract.csv`, `bible_patch_v1.1.json`, poznámky k fázím F2, F3, F6, F7, F8, F9 (domy a šikmé pohledy na Larpington), zadání plánu města |
| `versions/vX.Y-název/` | neměnné snapshoty (kopie `current/`, `docs/`, `scripts/` + `MANIFEST.sha256`); historie v `CHANGELOG.md` |
| `scripts/` | generátory a kontroly (Python; potřebují `numpy`, `pillow`) |
| `work/` | pracovní soubory mimo snapshoty (varianty obrysu, interní okno 3 m/px) |

## Stavy a značení

`approved` = schváleno týmem (existence/role z bible) · `proposed` = pracovní návrh · `needs_decision` = otevřené. U objektů se rozlišuje `exist_status`, `name_status` a `pos_status` (poloha je zatím vždy `proposed`) a `origin` (`bible`, `geo_ref`, `atlas_new`, u plánu města i `atlas`, `plan_new`). Hodnoty výšek, populace, délek a zastavěné plochy jsou **modelové**, ne měření. Pseudo-souřadnice kolem 33,9 N / 137,6 E jsou **hypotetické**.

## Přegenerování (v tomto pořadí)

```
python atlas/scripts/build_relief.py     # F2: DEM, vody, pokryv, mapy reliéfu
python atlas/scripts/build_human.py      # F3: sídla, doprava, přístavy, letiště, POI
python atlas/scripts/build_registry.py   # F4: registr, foto vodítko, patch bible
python atlas/scripts/build_atlas.py      # F5: SVG mapy a prohlížeč
python atlas/scripts/build_capital.py    # F7: plán hlavního města (doplní i patch bible a matici kanonu)
python atlas/scripts/render_sat.py all   # F6: S-00…S-03, šikmé pohledy (S-03 potřebuje hotový plán města; jen Larpington: render_sat.py S-03, pak render_sat.py obliques S-03)
python atlas/scripts/sat_extras.py       # F6: popisky, prompty, README k renderům
python atlas/scripts/export_png.py       # volitelné PNG náhledy map (Edge/Chrome)
python atlas/scripts/build_summary.py    # F8: shrnutí a kontrolní seznam
python atlas/scripts/check_atlas.py      # souhrnná kontrola (musí skončit „vše v pořádku“)
python atlas/scripts/snapshot.py vX.Y-název --desc "…" --change "…"   # neměnný snapshot
```

Obrys ostrovů (F1) je zmrazený v `current/geometry/outline_coast.json`; varianty se generují do `work/` (`build_outline.py`, `freeze_outline.py`). Celý řetězec je deterministický (pevná semínka); výsledky se při opakování shodují.

## Pravidla

1. Originály projektu se nemění. Změny kanonu jdou jen do `docs/bible_patch_v1.1.json` a slučují se po schválení týmem.
2. Každá významná úprava = nový snapshot a záznam v `CHANGELOG.md`.
3. Satelitní a šikmé pohledy jsou *simulované* a nejsou skutečná družicová ani letecká data; bez placené AI (R-05).
4. Prefix ID: M- vrcholy · N- příroda · C- hlavní město · T- města · I- průmysl · A- letiště · P-01 spojení na Paraland · H- přístavy · W- vody · B- pláže · V- vyhlídky · SP- prameny · PL- Paraland · ST- stanice · RD- silnice · TR- stezky · CY- cyklotrasy · HV- hotely · SK- lyžování · PG- paragliding · **CP-** plán hlavního města (CP-H ilustrativní domy, CP-B budovy, CP-SQ náměstí, CP-PK parky, CP-GW zelené klíny, CP-BL bloky, CP-UL ulice, CP-AR bezbariérové trasy, CP-CF kavárny, CP-RN půjčovny, CP-SH obchody, CP-ZR maloobchodní zóny).
