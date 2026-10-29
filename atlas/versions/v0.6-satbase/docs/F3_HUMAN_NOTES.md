# F3 – Lidská vrstva (atlas v0.3-human)

Vše je **pracovní návrh (`proposed`)**. Kanon (approved) určuje: role linek L1/L2/L3, podmořské napojení Paralandu, okružní pobřežní silnici s odbočkami, hustou síť cyklotras a stezek, ≥ 3 přístavy, ~2 letiště (návrh), zelený průmysl, Paraland (historické městečko, hrad/zámeček, zříceniny, resorty, aquapark, promenáda), menší počet prémiových hotelů na hlavním ostrově, vyhlídky s bezpečným přístupem. Vedení tras, stanice, jména a velikosti sídel jsou návrh.

## Soubory (`current/human/`, `current/svg/transport_preview.svg`)

`settlements`, `roads`, `trails_cycleways`, `rail_lines`, `rail_stations`, `ports_airports`, `poi` (`*.geojson`, lokální km) + `human_report.json` (kontroly a statistiky). Vedení tras hledá A* nad skutečným DEM (sklon, voda, pobřeží), takže silnice a tratě sledují reliéf.

## Železnice

| Linka | Návrh vedení | Délka | Poznámky |
|---|---|---|---|
| **L1 Skyline Experience** (O1) | Larpington Západ → Přehrada → Vodopád N-03 (fotozastávka) → Krystalová jeskyně N-02 → Horská stanice | 8,7 km | Stoupá z 33 na 242 m, největší sklon 4,9 % (500 m). V jeskyni smyčka ≈ 262° (~¾ obvodu), dva portály, ≈ 284 m. Úseky: povrch, viadukt, krátké tunely |
| **L2 Heritage Connect** (O3, O4) | Čimprlichovo Hradiště – Larpington (oblouk Západ–Sever–Východ) – Zelená zóna – závod na řasy – nákladní přístav; Sever – Praha – odbočka – Aokawa – Ōru Maito / Hoshimachi; odbočka na letiště | 29 km, 13 stanic | Povrchová, souvislá síť. Havlišovo Doupě bez železnice |
| **L3 Metro Blue** (O4) | Městský okruh (Západ, Sever, Východ, Střed–Přístav) + větev Východní nábřeží – Paraland Link (P-01) – podmoří – Paraland Marina | 15,9 km, 7 stanic | Podmořský úsek 1 482 m (průliv 1,5 km), prosklená galerie 226 m. Okruh a větev v tunelu |

**Přestupy L2↔L3 jsou právě 3** (Západ, Sever, Východ, jako v bibli). Uzel Larpington Západ spojuje L1, L2 i L3. Rozpor C-06 (3 přestupy v malém jádru) je vyřešen tím, že přestupní uzly leží na okraji čtvrtí (≈ 0,3–0,6 km od středu čtvrtí).

## Silnice, stezky a cyklotrasy

- **R1 okružní pobřežní silnice (approved)**: 53,9 km, uzavřená. V útesovém severozápadě pod M-01 pobřeží neexistuje, proto R1 vede po útesech až do výšky 293 m a v **3 tunelech (2,2 km)**. Tuto úpravu (rozpor C-08) je třeba potvrdit.
- Spojnice třídy R2 (≈ 49 km): město–Praha–Aokawa–Ōru Maito/Hoshimachi, letiště–průmysl–přístav, Čimprlichovo–přehrada–Horská stanice, Čimprlichovo–Havlišovo Doupě, dvě tepny hlavního města.
- Odbočky třídy R3 na vyhlídky, pláže, hotely a osady (30 km). Paraland: vlastní okružní servisní silnice (11,9 km), **bez autopřevozu** (O5).
- Pěší stezky 24,8 km (TR-01…07 na hlavním ostrově, TR-PL1–2 na Paralandu), cyklotrasy 93,7 km (CY-01 pobřežní okruh, CY-02…06).
- Lyžařská sjezdovka na M-02: převýšení 277 m, délka 1,7 km (krátká sezona, zasněžování, viz klima v bibli).

## Přístavy a letiště

Přístavy (O6): **C-02** historický (vlnolam proti tajfunům z jihu), **I-03** nákladní (3 mola v zátoce chráněné poloostrovem), **H-01** severní rybářský, **H-02** marina Paraland (u přistání L3). Volitelný lodní okruh C-02 ↔ H-02 (6,6 km, bez autopřevozu). Letiště (O7): **A-01** dráha 09/27, 1 900 m, 0,92 km od moře, sklon < 1,5°, 2,4 km od průmyslu; **A-02** travnatá dráha 700 m na Paralandu.

## Sídla a obyvatelé (modelové rozdělení 32 000)

Larpington 12 000 · Praha 4 500 · Aokawa 2 600 · Ōru Maito 2 300 · Čimprlichovo Hradiště 2 000 · Hoshimachi 1 600 · Havlišovo Doupě 700 · Zelená průmyslová zóna 600 · Paraland 1 400 (staré městečko 900, marina 200, resorty 300) · 6 osad po 200 · roztroušeně 3 100. **Není to sčítání.** Hoshimachi dostalo ID T-06 (v bibli je jen jméno, `proposed`).

## Nová ID

H-01, H-02 (přístavy), A-02, V-02…V-08 (vyhlídky), LH-01 (maják), SP-01…SP-08 (prameny), HV-01…HV-03 (hotely), PG-01/02 (paragliding), SK-01/02 (sjezdovka, lanovka), B-01…B-06 (pláže), T-06 (Hoshimachi), HM-01…06 (osady), PL-01…PL-06 (Paraland), ST-* (stanice), RD-* (silnice), TR-*, CY-*, FERRY-1.

## Kontroly

31/31 v pořádku (`human_report.json`): souvislost L2, přestupy, podmořský úsek a galerie, L1 prochází jeskyní a vodopádem, sklon L1 ≤ 6 %, žádná trať ani silnice nevede jezerem, R1 uzavřená 45–75 km a ≤ 300 m, přístavy na pobřeží a hráze v moři, letiště celá na souši, populace sídel + roztroušení = 32 000, Paraland má hrad, zříceninu, aquapark, resorty, marinu a pěší okruh, pláže ne na SZ.
