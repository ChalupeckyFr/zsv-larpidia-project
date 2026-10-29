# CHANGELOG atlasu Larpidie

Nejnovější nahoře. Každý záznam = neměnný snapshot ve `versions/`.

## v1.0.1-capital-detail — 2026-10-24

F9: ilustrativní domy v plánu hlavního města ve stavu zástavby podle modelové populace, S-03 z těchto domů a dva šikmé pohledy na Larpington s hmotami budov.

- Domy: 3 242 ilustrativních půdorysů (cp_houses.geojson, CP-H), kapacita bydlení 12 000 = populace Larpingtonu; 586 bloků je rezerva rozvoje, plánované ulice čárkovaně; vrstva v SVG a prohlížeči
- S-03 znovu z domů plánu, výškový model budov S-03_buildings_height.png a šikmé pohledy S-03_oblique_S a S-03_oblique_W (celkem 6 pohledů)
- Nález C-22: plné zastavění bloků by dalo ≈ 48 000 obyvatel (víc než schválený strop 40 000 pro zemi); D11 rozšířeno; docs/F9_CAPITAL_DETAIL_NOTES.md, FINAL_SUMMARY a checklist aktualizovány
- export_png.py používá vlastní profil prohlížeče; check_atlas.py rozšířen (domy × populace, výškový model, 6 šikmých pohledů)

## v1.0-draft — 2026-10-24

F8: závěrečná revize – atlas 1.0-draft ke schválení týmem (3 otevřené body), plán hlavního města, satelitní reference S-03, shrnutí a kontrolní seznam.

- Nově S-03 (Larpington, 2970x2100 px @2 m, zástavba z plánu CP-01, IoU souše 0,998), prompt a popisky z plánu; S-00…S-03 a šikmé pohledy znovu vyrenderovány s verzí 1.0-draft
- docs/FINAL_SUMMARY.md, TEAM_APPROVAL_CHECKLIST.md, F8_REVIEW.md, README_ATLAS.md přepsáno; nejvýše tři otevřené body (D1/D7, D8/D10-D12, D2/D5/D9)
- PNG náhledy map (export_png.py), README_CAPITAL.md, matice kanonu K-021…K-074 aktualizována, rozpory C-17…C-21 a otázky O19…O25
- Opakovatelnost: celý řetězec skriptů v čisté kopii dal 81 ze 101 výstupů shodných byte po bytu (zbytek jen označení verze); check_atlas.py 41 kontrol v pořádku

## v0.7-capital-base — 2026-10-24

F7: podklad plánu hlavního města Larpingtonu (CP-01): metrický model A2 1 : 10 000, uliční síť a dopravní graf, bloky, veřejné prostory, klíčové budovy, stanice, registr a prohlížeč.

- Okno 5 940 × 4 200 m (1 j = 1 m), 4 čtvrtě jako výseče kolem Náměstí čtyř, staré město u přístavu C-02, zelené klíny, nová čtvrť Východní nábřeží; zastavěné území 6,31 km² (C-18)
- Ulice 158 km (graf: 1 355 uzlů, 2 005 hran, souvislý), 874 bloků s využitím, 15 klíčových budov, 12 parků a zelených klínů, 9 náměstí, 3 bezbariérové trasy (max. sklon 3,6 %)
- Registr plánu 968 objektů (CP-*), foto/video vodítko, GeoJSON v metrech i km atlasu, SVG vrstvy cs/en/ja, HTML prohlížeč, cp_report.json (13 kontrol)
- Rozpory C-17…C-21 a otázky O19…O25; patch bible: /urbanism/capital_plan_model a D10–D12; docs/F7_CAPITAL_NOTES.md a CAPITAL_PLAN_BRIEF.md; check_atlas.py rozšířen

## v0.6.1-satbase — 2026-10-24

F6, 2. kolo (Doladit vzhled): realističtější satelitní podklady S-01/S-02, přehled S-00, čtyři šikmé pohledy a kosmetické varianty s mraky.

- Sídla po blocích (ulice, parcely, střechy, stíny; 5 stylů), nepravidelné půdorysy, stuhová zástavba, hlavní město dosahuje k přístavu (C-17 – jen vzhled, půdorysy sídel beze změny)
- Pole po parcelách s živými ploty (tlumená paleta), zubaté okraje lesů, remízky, samoty podél silnic, rozptýlené stromy v jemných oknech, šelf moře podle typu pobřeží
- S-00_overview (oba ostrovy, 2970x2100 px @10 m) a čtyři šikmé pohledy (voxelový render z DEM, kamera s posunutým objektivem, převýšení 1,35x, *_camera.json)
- Varianty s mraky jen nad otevřeným mořem; verify_sat.py umí šikmé pohledy a vynechává bílé plochy; OBLIQUE_PROMPTS.md; check_atlas.py rozšířen (33 kontrol)
- IoU souše vlastních renderů 0,999 (S-01) / 0,998 (S-02); canon.ATLAS_VERSION = 0.6.1-satbase; docs/F6_SAT_NOTES.md přepsáno; rozpor C-17

## v0.6-satbase — 2026-10-23

F6: simulované satelitní podklady S-01 (Larpidie) a S-02 (Paraland), masky, georeference, popisky, prompty a kontrola tvaru.

- S-01_base 2240x1620 px @10 m, S-02_base 1400x1120 px @5 m (kolmý pohled, sever nahoře); IoU souše vlastních renderů 0,999 / 0,997
- Masky souše a tříd, georeference (S-0x_georef.json se SHA obrysu), popisky cs/ja/en jako SVG textové vrstvy, upozornění na simulaci
- Prompty (EN) + negativní omezení pro externí generátor s referenčním obrázkem; verify_sat.py (IoU >= 0,95)
- Bez placené AI (R-05); fotorealismus se řeší externě z této reference
- check_atlas.py rozšířen o kontroly satelitních podkladů; docs/F6_SAT_NOTES.md

## v0.5-atlas — 2026-10-23

F5: hlavní atlas – vrstvené SVG (master, fyzická, politická, kánon×návrh), schéma železnic a interaktivní prohlížeč.

- larpidia_atlas_master/physical/political/status.svg (A2, 1:50 000, 21 vrstev, popisky cs/ja/en jako textové vrstvy, data-id + stav u každého prvku) a *_embedded.svg
- rail_scheme.svg: netopografické schéma L1/L2/L3 (okruh L3, přestupy, podmoří 1,48 km, galerie 226 m)
- viewer/atlas.html: hledání, vrstvy, jazyky CS/JA/EN, režim kánon×návrh, záznam z registru a foto/video vodítko, souřadnice kurzoru
- check_atlas.py rozšířen na 27 kontrol (vrstvy SVG, pokrytí registru v mapě, prohlížeč)
- R-07: pokračovat s návrhy jmen/odchylek; dopravní koncepce potvrzena jako návrh
- README_ATLAS.md přepsáno; canon.ATLAS_VERSION

## v0.4-registry — 2026-10-23

F4: jednotný registr míst a objektů (159 objektů) s foto/video vodítkem z DEM, odchylky, návrh jmen, patch bible a matice dohledatelnosti kanonu.

- places.json/csv: ID, jména cs/en/ja (návrh), region, X/Y %, km, pseudo-lon/lat, výška, stavy exist/name/pos, origin; photo_guide.csv: viditelné dominanty z DEM, směr moře, blízké body, styl, vyhnout se
- deviations.csv (3 odchylky ≤ 3 %: T-04, T-05, A-01), names_proposed.csv, docs/NAMES_AND_DEVIATIONS_TO_APPROVE.md
- docs/bible_patch_v1.1.json: návrh změn bible (neaplikováno; originál beze změny)
- canon_extract.csv: sloupec atlas_objects vyplněn (95/95; 28 approved tvrzení má odkaz nebo vysvětlení)
- check_atlas.py: 22/22 kontrol (geometrie, reliéf, lidská vrstva, registr, kanon, originály, snapshoty)
- Oprava: BOM v ORIGINALS_SHA256.txt (čtení utf-8-sig); stav cyklotras normalizován na approved

## v0.3-human — 2026-10-23

F3: lidská vrstva – sídla, silnice (R1 okruh 54 km), stezky a cyklotrasy, železnice L1/L2/L3, přístavy, letiště, body zájmu, Paraland.

- Železnice: L1 8,7 km (smyčka v jeskyni ~262°, sklon max 4,9 %), L2 29 km / 13 stanic, L3 15,9 km (podmoří 1 482 m, galerie 226 m); právě 3 přestupy L2↔L3
- Silnice R1 53,9 km uzavřená (útesy až 293 m, 3 tunely), R2 49 km, R3 30 km; stezky 24,8 km; cyklotrasy 93,7 km; sjezdovka M-02 (277 m)
- Přístavy C-02, I-03, H-01, H-02; letiště A-01 (1 900 m) a A-02 (700 m); POI: vyhlídky, prameny, hotely, hrad, zřícenina, aquapark
- Sídla s modelovou populací 32 000; hlavní město 4,8 km2; 31/31 kontrol (human_report.json)
- Relief doladěn pro sídla (nižší severní pahorkatina, ploché zóny Ōru Maito a Hoshimachi)
- Dokumentace: docs/F3_HUMAN_NOTES.md; rozpory C-05, C-06, C-08 implementovány, nové C-14..C-16

## v0.2-relief — 2026-10-23

F2: reliéf (DEM 20 m, max 560 m), vrstevnice, hydrografie (toky, vodopád, přehrada), pokryv krajiny, typy pobřeží, fyzická mapa A2.

- Výškový model: M-01 560 m, M-02 510 m, M-03 440 m (modelové); 13/13 kontrol v pořádku (relief_report.json)
- Hydrografie W-01..W-07, vodopád N-03 (~44 m), přehrada N-04 (hladina ~68 m, 0,6 km2, hráz ~29 m)
- Pokryv krajiny (les, louka, pole, rýžové terasy O17, křoviny, skála) a pobřeží (pláže jen J/JV/V Paralandu, útesy na SZ)
- SVG: physical_preview.svg (+embedded), landcover_preview.svg; knihovny raster.py, relief_model.py, hydro.py, landcover.py, layers.py, build_relief.py
- Dokumentace: docs/F2_RELIEF_NOTES.md (modelové hodnoty ke schválení)

## v0.1.1-outline-B — 2026-10-23

Tým zvolil variantu B; geometrie obrysu zmrazena jako kanonický základ atlasu (R-06).

- current/geometry/outline_coast.json = zmrazená varianta B (SHA-256 ffca09ac...), shodná se snapshotem v0.1-outline
- canon.py: CHOSEN_VARIANT, ACCEPTED_DEVIATIONS (T-04, T-05, A-01), load_outline(), table_rows()
- Pracovní varianty se generují do atlas/work/ (mimo snapshoty); varianta A zůstává jen v archivu v0.1-outline
- Rozhodnuto: rámec zůstává 24x16 km (O18 uzavřeno)

## v0.1-outline — 2026-10-23

F1: obrys Larpidie a Paralandu ve dvou variantách (A věrná tabulce, B členitější) ke schválení týmem.

- Rámec 24×16 km, plocha 175,0 km² a 14,0 km², průliv 1,50 km; plátno A2 / 1:50 000 (1 jednotka SVG = 1 m)
- Varianta A: 0 odchylek od tabulky; varianta B: T-04, T-05, A-01 posunuty o <= 3 % (viz docs/CONFLICTS_AND_DECISIONS.md, sekce D)
- Nález C-13: konvexní obal bodů tabulky = 135 km2, proto jen mírně členité pobřeží; navržena i volba menšího rámce (O18)
- Výstupy: variants/A|B (SVG, GeoJSON v km i pseudo-WGS84, coast.json s typy pobřeží, report.json), outline_compare.html
- Nástroje: geom.py, svgkit.py, shapes.py, outline_checks.py, build_outline.py, snapshot.py

## v0.0-audit — 2026-10-23

F0: audit kanonu, hashe originálů, extrakce tvrzení, rozpory a otevřené otázky.

- SHA-256 14 originálů (ORIGINALS_SHA256.txt); validate_bible.py = OK
- canon_extract.csv: 95 tvrzení (28 approved, 66 proposed, 1 needs_decision)
- CONFLICTS_AND_DECISIONS.md: rozhodnutí R-01..R-05, rozpory C-01..C-12, otázky O1..O17
- Nález: kolize ID M-01 (vrchol × plán města v MAP_PROMPT) → navrženo CP-01

