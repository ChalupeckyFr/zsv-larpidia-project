# F7 – Podklad plánu hlavního města (atlas v0.7-capital-base)

Vše je **pracovní návrh (`proposed`)**. Plán CP-01 je *podklad* (metrický model, ulice, bloky, prostory, klíčové budovy, stanice, registr), ne hotový grafický plán. ID plánu je **CP-01**, protože „M-01“ z MAP_PROMPT je v tabulce nejvyšší vrchol (C-03). Pobřeží, silnice, koleje, stanice a přístav C-02 z atlasu se **nemění**; plán je kreslí 1 : 1 a jen na ně navazuje.

## Metrický model

- Okno plánu: **5 940 × 4 200 m** (x 13,10–19,04 km, y 10,30–14,50 km atlasu) = list **A2 (594 × 420 mm) v měřítku 1 : 10 000**; 1 jednotka SVG = 1 m.
- Lokální souřadnice: `u` = východ (m), `v` = jih (m), počátek v SZ rohu okna; `x_km = 13,10 + u/1000`, `y_km = 10,30 + v/1000`.
- Měřítko a měřítková čára platí, protože délky ulic a vzdálenosti plynou přímo z této geometrie (podle MAP_PROMPT). Čtvercová síť 500 m má popisky v km atlasu.

## Co vzniklo (`current/capital/`)

| Soubor | Obsah |
|---|---|
| `capital_plan_base.svg` | editovatelné vrstvené SVG: moře, pevnina, vrstevnice 5 m, pláže, zelené klíny, čtvrtě, bloky podle využití, prostory, přístav, ulice (obrys + výplň po třídách), koleje, stanice, klíčové budovy, kavárny/půjčovny/obchody, bezbariérové trasy, mřížka, popisky cs / en / ja (textové vrstvy), měřítko, severka, legenda |
| `capital_plan_viewer.html` | prohlížeč: hledání, vrstvy, jazyky, režim stavů, záznam s foto/video vodítkem |
| `cp_graph.json` | dopravní graf (1 355 uzlů, 2 005 hran, délky z geometrie) |
| `cp_streets.geojson`, `cp_blocks…`, `cp_districts…`, `cp_buildings…`, `cp_spaces…`, `cp_points…`, `cp_routes…` | vrstvy v lokálních metrech; každá i jako `*_atlas_km.geojson` (km atlasu) |
| `cp_objects.json` / `.csv`, `cp_photo_guide.csv` | registr 968 objektů plánu (stavy exist/name/pos, původ, odkaz na bibli a atlas) a vodítko pro foto/video |
| `cp_frame.json`, `cp_report.json` | rámec a výsledky vlastních kontrol |

## Koncepce města (návrh)

- **Náměstí čtyř** ve středu (průsečík tepen RD-11 a RD-12): okružní komunikace kolem **Parlamentní zahrady** s budovou parlamentu (CP-B01); **čtyři správní budovy** (CP-B02…B05) stojí ve větrníkovém uspořádání, každá poblíž tepny své čtvrti. Z náměstí vychází 8 paprsků: 4 tepny z atlasu a 4 diagonální bulváry, které tvoří hranice čtvrtí.
- **Čtvrtě C-03…C-06** jsou výseče kolem centra: západ Chalupecká (u uzlu ST-W), sever Kynčlova (ST-N), východ Klimečkova (ST-E), jih Žemličkova (staré město a přístav). Každá má vlastní natočení uliční mřížky, školu a park do 900 m od středu.
- **Staré město** (půlelipsa 820 × 700 m, 0,92 km²) u historického přístavu C-02: uličky rovnoběžné s pobřežím, kolmé průchody, **Přístavní náměstí** na konci prodloužené tepny RD-12, **Tržní náměstí** s tržní halou, **Kostelní náměstí** s historickým kostelem, **Přístavní promenáda** a nábřeží (Nábřeží 16. června, podle data prvního osídlení 1608-06-16), přístavní úřad, přístaviště lodní linky na Paraland, prémiový hotel nad promenádou.
- **Státní čtvrť a kultura:** muzeum Košťálovy éry (CP-B06) u Centrálního parku; historický kostel (CP-B07); tržnice (CP-B08).
- **Zelené klíny** (2,3 km², 6 ploch) mezi čtvrtěmi uvnitř okruhu L3: nezastavěná rezerva (louky, sady, sport) a parky u čtvrtí.
- **Východní nábřeží** (0,4 km²): nová čtvrť u stanice ST-L3-05, napojená Třídou Východního nábřeží a zeleným koridorem.
- **Železnice:** L1/L2 povrchové, L3 podzemní (z atlasu); povrchové stanice (W, N, E) mají budovu, nástupiště a předprostor; podzemní (S, L3-05) dva vstupní pavilony.

## Čísla

| Veličina | Hodnota |
|---|---|
| Zastavěné území (půdorys) | 6,31 km² (F3: 4,77 km² ze tří laloků) – C-18 |
| Čtvrtě | C-03 1,49 km², C-04 1,08, C-05 1,85, C-06 1,88 |
| Ulice celkem | 158,1 km (tepny 10,4, R1 6,5, bulváry 3,8, ring 0,5, místní 120,1, uličky 15,0, nábřeží 1,8) |
| Graf | 1 355 uzlů, 2 005 hran, 968 křižovatek, 357 slepých konců (hlavně na okraji), jedna souvislá síť (99,9 %) |
| Bloky | 874, celkem 4,53 km², medián 4 800 m² |
| Využití bloků | bydlení středně husté 374, zahrádkové 118, staré město 143, promenáda 57, hlavní třída 47, státní čtvrť 37, okolí stanic 54, Východní nábřeží 39, školy 4, hotel 1 |
| Bezbariérové trasy | ST-S → Přístavní náměstí 1 021 m (max. 3,6 %), náměstí → hotel 716 m (1,6 %), ST-S → Náměstí čtyř → muzeum 1 424 m (0,8 %) – kandidáti, měřeno z DEM |

## Schváleno × návrh

`approved` je jen to, co říká bible: parlament (CP-B01), muzeum (CP-B06), historický přístav C-02, pobřežní silnice (Pobřežní třída) a promenáda u přístavu (CP-PR01) a samotný plán CP-01 (zadání v MAP_PROMPT). **Všechny polohy** jsou `proposed`; názvy ulic, čtvrtí a míst jsou pracovní.

## Rozpory a otevřené otázky

Rozpory C-17 až C-21 a otázky O19 až O25 jsou v `CONFLICTS_AND_DECISIONS.md`. Nejdůležitější k rozhodnutí týmu:

1. **O19** – kde stojí parlament a správní budovy (Náměstí čtyř × historická budova u přístavu);
2. **C-18 / D11** – zastavěné území města 6,3 km² místo 4,8 km² (staré město u přístavu, Východní nábřeží, zelené klíny);
3. **C-19 / D12** – poloha hotelu HV-01 na promenádě a muzea u Centrálního parku.

## Poctivě k výsledku

- Ulice, bloky a budovy jsou **procedurální návrh** (mřížky natočené podle čtvrtí, uličky starého města z vzdálenosti od pobřeží); nejde o skutečný územní plán. Délky ale plynou z metrického modelu.
- Bloky jsou **mezi ulicemi**, ne zástavba: půdorysy běžných domů jsou úkol další etapy. Klíčové budovy mají jednoduché obdélníkové půdorysy (kostel křížový).
- Okraje města mají **357 slepých konců** (mřížka končí na hranici půdorysu) – jsou to rezervy pro budoucí rozšíření.
- Zelené klíny a polohy parků jsou návrh kompozice; vrstevnice 5 m pocházejí z DEM atlasu (model).
- Žádné skutečné mapové podklady, žádná placená AI.

## Kontroly (`cp_report.json`)

13 vlastních kontrol: rámec A2 1 : 10 000; ID a stavy; polohy `proposed`; schváleno jen podle bible; stanice = atlas; délky tepen atlasu zachovány (±1,2 %, kromě okružní komunikace u středu); souvislý graf; bloky a budovy na pevnině mimo pánev; čtvrť má správní budovu, školu a park; povinné objekty; budovy mimo ulice; bezbariérové trasy; vrstvy a popisky SVG. V `check_atlas.py` k tomu přibyly kontroly existence souborů, validity SVG a GeoJSON a shody se stanicemi v registru atlasu.
