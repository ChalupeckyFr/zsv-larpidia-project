# Plán hlavního města Larpingtonu – podklad CP-01 (atlas 1.0-draft)

**Pracovní návrh (`proposed`).** Schematický podklad v lokálním metrickém modelu: délky ulic a vzdálenosti plynou z geometrie, názvy a polohy jsou návrh. Pobřeží, silnice, koleje, stanice a přístav C-02 jsou z atlasu beze změny.

## Souřadnice

- List A2 (594 × 420 mm) v měřítku **1 : 10 000**, okno 5 940 × 4 200 m; 1 jednotka SVG = 1 m.
- Lokální metry: `u` = východ, `v` = jih, počátek v SZ rohu okna. Převod na km atlasu: `x_km = 13,10 + u/1000`, `y_km = 10,30 + v/1000`.
- GeoJSON `cp_*.geojson` je v lokálních metrech, `cp_*_atlas_km.geojson` v km atlasu (bez zeměpisného CRS – fiktivní svět; pseudo-lon/lat jsou hypotetické).

## Soubory

| Soubor | Obsah |
|---|---|
| `capital_plan_base.svg` | vrstvené editovatelné SVG (Inkscape): moře, pevnina, vrstevnice, pláže, zelené klíny, čtvrtě, bloky, prostory, přístav, ulice, koleje, stanice, budovy, POI, trasy, mřížka, popisky cs/en/ja, okraje |
| `capital_plan_viewer.html` | prohlížeč s hledáním, vrstvami, jazyky a záznamem objektu |
| `cp_graph.json` | dopravní graf: uzly (stupeň) a hrany (třída, šířka, délka, název, odkaz na silnici atlasu) |
| `cp_streets/blocks/districts/buildings/spaces/points/routes/houses.geojson` | vrstvy plánu (`houses` = ilustrativní půdorysy domů, F9) |
| `cp_objects.json`, `cp_objects.csv`, `cp_photo_guide.csv` | registr 968 objektů plánu a foto/video vodítko |
| `cp_frame.json`, `cp_report.json` | rámec a výsledky kontrol |

## Třídy ulic (`cls`) a šířky

`R1` pobřežní silnice (22 m) · `A` tepny z atlasu (22 m) · `B` diagonální bulváry a spojka k Východnímu nábřeží (20 m) · `S` okružní komunikace Náměstí čtyř (14 m) · `P` nábřeží (18 m) · `C` místní ulice (10 m, ve starém městě 8 m) · `L` uličky starého města (5 m).

## Využití bloků (`land_use`)

| Kód | Význam | Počet bloků |
|---|---|---|
| `old_town_mixed` | Staré město – smíšená zástavba | 143 |
| `promenade_retail` | Přístavní promenáda – obchody s limitovanými kolekcemi, kavárny, půjčovny | 57 |
| `civic_mixed` | Státní čtvrť – instituce a služby | 37 |
| `transit_mixed` | Okolí stanice – služby a bydlení | 54 |
| `retail_main` | Hlavní třída – obchody a kavárny | 47 |
| `residential_mid` | Bydlení – středně husté | 374 |
| `residential_low` | Bydlení – zahrádkové | 118 |
| `school` | Škola a školní areál | 4 |
| `new_waterfront` | Východní nábřeží – nová smíšená čtvrť | 39 |
| `hotel_premium` | Prémiový hotel | 1 |

## Stav zástavby a domy (F9)

`cp_houses.geojson` (lokální metry) a `cp_houses_atlas_km.geojson` obsahují **3242 ilustrativních půdorysů domů** (`CP-H-xxxxx`: využití, podlaží, výška okapu a hřebene, barva střechy, modelová kapacita bydlení). Domy nejsou skutečné budovy a nejsou v registru objektů.
Bloky mají `build_state`: `built` (zastavěno), `partial` (zastavěno z části – hranice růstu města), `reserve` (**rezerva rozvoje**, jen řídké chaty) a `civic` (instituce a školy); ulice mají `state` `built` / `planned` (plánovaná ulice v rezervě).

Zastavěno je jádro, jehož kapacita bydlení odpovídá modelové populaci Larpingtonu (**12000**, `population_model` v atlasu): 217 bloků zastavěno, 29 z části, 586 v rezervě. Plné zastavění všech bloků podle jejich využití by dalo ≈ 48348 obyvatel (čtyřnásobek), tedy víc než schválený strop 40 000 obyvatel pro celou zemi; proto plán rozlišuje *vymezené území* (6,3 km²) a *stav zástavby* (rozhodnutí C-22). Předpoklady modelu: 38 m² podlahové plochy na obyvatele, užitná plocha 82%.

## Prefixy ID

`CP-01` plán · `CP-B` budovy · `CP-SQ` náměstí a předprostory · `CP-PK` parky · `CP-GW` zelené klíny · `CP-PR` promenáda · `CP-PI` molo · `CP-BL` bloky · `CP-H` domy (ilustrativní, F9) · `CP-UL` pojmenované ulice · `CP-AR` bezbariérové trasy · `CP-CF` kavárny · `CP-RN` půjčovny · `CP-SH` obchody · `CP-ZR` maloobchodní zóny. Stanice `ST-*`, čtvrtě `C-03…C-06` a přístav `C-02` mají ID atlasu.

Postup, rozhodnutí a omezení: `../../docs/F7_CAPITAL_NOTES.md`; zadání další etapy: `../../docs/CAPITAL_PLAN_BRIEF.md`.
