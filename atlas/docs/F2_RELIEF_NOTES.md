# F2 – Reliéf a voda (atlas v0.2-relief)

Vše je **pracovní návrh (`proposed`)**. Kanon (approved) určuje jen existenci prvků: třívrcholové pohoří 500–600 m, horské řeky a vodopády, přehradní jezero, krystalová jeskyně, 10m pobřežní sráz s vyhlídkou, lesy, louky, písčité pláže, skalnaté pobřeží. Výšky, spády, tvar toků a rozložení pokryvu jsou modelové.

## Soubory (`current/`)

| Soubor | Obsah |
|---|---|
| `relief/dem_20m_u16.png` + `dem_meta.json` | výškový model, buňka 20 m, 16bitové PNG (výška v m × 100), počátek = levý horní roh plátna |
| `relief/hillshade_20m.png`, `hillshade_rgba.png`, `hypsometry_rgba.png` | stínování a hypsometrické tónování (podklad pro SVG a pozdější satelitní rendery) |
| `relief/contours.geojson` | vrstevnice po 20 m (index po 100 m), lokální km |
| `relief/hydrography.geojson` | toky W-01…W-07, přehradní jezero, vodopád N-03 |
| `relief/landcover.geojson`, `landcover_20m.png` | pokryv krajiny (les, louka, pole, rýžové terasy, křoviny, skála) |
| `relief/coast_classes.geojson` | pláže (polygony), útesy a skalnaté pobřeží (linie) |
| `relief/relief_report.json` | kontroly a výšky všech bodů tabulky |
| `svg/physical_preview.svg` (+ `_embedded`) | fyzická mapa A2 / 1 : 50 000 (vrstvy: moře, mřížka, hypsometrie, stínování, vrstevnice, vody, pobřeží, vrcholy) |
| `svg/landcover_preview.svg` | pokryv krajiny |

`physical_preview.svg` odkazuje na PNG v `../relief/` (běžné v Inkscape). `physical_preview_embedded.svg` má obrázky vložené a lze ho poslat samostatně.

## Modelové hodnoty ke schválení

| Prvek | Hodnota v modelu | Kanon |
|---|---|---|
| M-01 nejvyšší vrchol | **560 m** | bible: rozsah 500–600 m approved, 560 m proposed |
| M-02 prudší (sjezdovka) | 510 m | bible: prudší sjezdovková hora approved, výška návrh |
| M-03 zaoblený (turistika, paragliding) | 440 m | bible: approved, výška návrh |
| Pobřežní sráz N-01 | vyhlídka ve výšce ≈ 15 m, sráz ≈ 10 m | bible: ≈ 10 m approved |
| Jeskyně N-02 | ≈ 195 m n. m. | existence approved |
| Vodopád N-03 | horní hrana ≈ 128 m, dolní ≈ 84 m (**≈ 44 m**) | existence approved |
| Přehrada N-04 | hladina **≈ 68 m**, plocha **0,6 km²**, hráz ≈ 29 m, objem ≈ 4 mil. m³ (odhad: plocha × 7 m) | existence approved |
| Hlavní město (centrum) / přístav | ≈ 18 m / ≈ 1 m | – |
| Letiště A-01 | plocha ≈ 15 m, dráha se sklonem < 1,5° | – |

Hlavní řeka W-01 pramení na jihovýchodním svahu M-02, teče kolem jeskyně k vodopádu N-03, do přehrady N-04 a pod hrází přes Cimprlichovo Hradiště k jižnímu pobřeží. Ostatní toky: W-02 (Aokawa, do východní severní zátoky), W-03 a W-04 (potoky útesovým pobřežím), W-05 (nížinný potok do východní zátoky u nákladního přístavu), W-06 a W-07 (Paraland). Názvy toků jsou pracovní a doplní se ve F4.

## Rozhodnutí a pravidla modelu

- Koryta se odvozují z terénu: nikdy neteče do kopce (kontrola monotónního klesání).
- Maximum terénu je přesně M-01 (kontrola); šum se v nejvyšších polohách utlumuje.
- Pláže jen na jihu, jihovýchodě a východě Paralandu; žádné na útesovém severozápadě (SKILL.md).
- Rýžové terasy (historické, O17) jsou v jihozápadním podhůří; tým může polohu změnit.
- Zástavba, průmysl, silnice a železnice přijdou ve F3; pokryv pro ně bude přepočten.

## Kontroly (relief_report.json)

13/13 v pořádku: maximum = M-01 = 560 m, výšky vrcholů 560/510/440 ± 3 m, žádná záporná výška, všechny toky klesají, plochá hladina přehrady pod vodopádem, vodopád ≥ 30 m, jeskyně nad vodopádem, N-01 8–18 m, centrum 5–30 m a přístav ≤ 2 m, sklon dráhy letiště < 1,5°, žádná pláž na SZ, plocha přehrady 0,3–1,0 km².
