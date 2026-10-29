# Zadání pro další etapu: detailní plán hlavního města (navazuje na atlas v0.7-capital-base)

**Cíl:** z podkladu CP-01 vytvořit grafický, tiskový a prezentační **plán hlavního města Larpingtonu** (list A2 1 : 10 000 a výřezy 1 : 2 500), na kterém půjde stavět fotografie, videa a historická mapa. Podklad je hotový (`current/capital/`); tento dokument říká, co ještě chybí a co musí schválit tým.

## 1. Nejdřív rozhodnout (tým)

| # | Otázka | Výchozí volba |
|---|---|---|
| O19 / D10 | Parlament a čtyři správní budovy | Náměstí čtyř (parlament v zahradě uprostřed, správní budovy ve větrníku) |
| C-18 / D11 | Zastavěné území 6,3 km², staré město u přístavu, Východní nábřeží | ponechat |
| C-19, O22 / D12 | Hotel HV-01 na promenádě, muzeum u Centrálního parku | ponechat |
| O25 | Názvy čtvrtí, ulic a míst | pracovní, `proposed` |
| C-21 | Oprava geometrie pánve C-02 v atlasu (nový tvar vodní plochy) | oprava v F8 |

## 2. Co udělat v plánu

1. **Zástavba bloků:** z bloků (`cp_blocks.geojson`) vytvořit půdorysy domů podle využití (`land_use`): staré město cihla a kámen, úzké uličky; promenáda – butiky a kavárny; Hlavní třída – obchody; státní čtvrť – instituce; bydlení – řady a domy se zahradami. Zachovat plochy a odstupy z metrického modelu.
2. **Adresní a POI vrstva:** rozmístit kavárny, půjčovny, obchody a služby (`cp_points.geojson` jsou jen první body) podle využití bloků; označit univerzálně přístupné trasy (`cp_routes.geojson`).
3. **Stylování:** barevná paleta až po schválení vlajky/barev (D6); tučné hlavní třídy, jemné uličky; vrstevnice jen u okrajů; lodě a mola v přístavu.
4. **Popisky:** čeština, japonština u japonských jmen, angličtina jako vypínatelná vrstva; názvy ulic po křivce (už jsou jako `textPath`), kolizní kontrola.
5. **Měřítko a kontrola délek:** měřítko 1 : 10 000 platí; u výřezů 1 : 2 500 přepočítat; zkontrolovat délky tras proti `cp_graph.json`.
6. **Satelitní reference hlavního města (S-03):** z bloků a budov vyrenderovat kolmý snímek 2 m/px (stejný postup jako S-01/S-02) a z něj šikmé pohledy; kontrola tvaru `verify_sat.py`.
7. **Foto/video seznam:** z `cp_photo_guide.csv` připravit seznam záběrů (*location_id | pohled kam | z jaké strany | roční doba | architektonické styly | blízké | vzdálené*); hlavní osy: Přístavní třída k moři, Náměstí čtyř, promenáda při západu slunce, Tržní náměstí, pohled z ST-S.
8. **Historická mapa 1608–1800** (K-073): z téhož pobřeží, jen staré město u přístavu (bez parlamentu, metra a letiště).

## 3. Pravidla (platí dál)

- Pobřeží, silnice, koleje a stanice z atlasu se nemění; změny kanonu jen přes `bible_patch_v1.1.json`.
- Nic neoznačovat jako `approved`, co schválil jen návrh (viz `F7_CAPITAL_NOTES.md`, sekce Schváleno × návrh).
- Každý obrázek označit jako *simulovaná vizualizace fiktivního města*; bez skutečných značek a osobností.
- Před generováním obrazu vždy předat referenční obrázek (SVG/PNG z plánu) a zkontrolovat siluetu.

## 4. Vstupy

`current/capital/capital_plan_base.svg`, `cp_*.geojson` (metry i km atlasu), `cp_objects.json`, `cp_photo_guide.csv`, `cp_graph.json`, `cp_report.json`; dále `current/renders/` (S-00…S-02, šikmé pohledy), `current/registry/places.json`, `docs/CONFLICTS_AND_DECISIONS.md`.
