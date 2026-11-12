# Prompty pro fotografie Larpidia Explorer

Složka obsahuje podrobné prompty pro generátor obrázků ke čtyřem kolům ukázkového režimu ([`explorer/rounds.json`](../rounds.json)). Každý prompt popisuje realistickou fotku z iPhonu pořízenou přímo u cílového bodu. Obsahuje také indicie, podle kterých hráči poznají, kde v atlasu místo leží.

Složka není součástí veřejného webu. [`scripts/build_public_site.mjs`](../../scripts/build_public_site.mjs) ji do `public/` nekopíruje, takže prompty ani seznam indicií se k hráčům nedostanou.

## Jak prompty použít

1. Otevřete soubor `.txt` daného kola a vložte do generátoru **celý text**. Prompty jsou v angličtině, protože s ní generátory pracují spolehlivěji.
2. Generujte ve formátu **16:9**, který se hodí pro projekci na tabuli.
3. Zkontrolujte výsledek podle sloupce „Musí být vidět“. Pokud klíčová indicie chybí nebo je na obrázku jakýkoli text či název, vygenerujte obrázek znovu.
4. Hotové fotky vložte do prezentace přednášejících. Hra fotky nezobrazuje (viz [`docs/LARPIDIA_EXPLORER_ROUND_SETUP.md`](../../docs/LARPIDIA_EXPLORER_ROUND_SETUP.md)).

## Přehled kol

| Kolo | Cílové místo | Prompt | Stanoviště a směr záběru | Musí být vidět (indicie) |
|---|---|---|---|---|
| 1 | Pramen řeky Larp (`SP-01`) | [01_SP-01_pramen_reky_Larp_prompt.txt](01_SP-01_pramen_reky_Larp_prompt.txt) | u pramene ve 279 m n. m., pohled na JJV (≈160°), 1×, začátek června, pozdní odpoledne | voda vyvěrající mezi balvany, horské chaty a stanice horské dráhy pod pramenem vpravo, daleko vlevo Larpington se starým přístavem, celý obzor tvoří moře |
| 2 | Hráz přehrady (`DAM-N04`) | [02_DAM-N04_hraz_prehrady_prompt.txt](02_DAM-N04_hraz_prehrady_prompt.txt) | koruna hráze asi 200 m severně od bodu, pohled na SZ (≈310°) přes nádrž, 1×, polovina listopadu, dopoledne | betonová hráz, odběrná věž a bóje, úzká nádrž v lesích, na obzoru Kulatý vrch (vlevo), Larpova hora (uprostřed) a Zimní hora se sjezdovkou (vpravo) |
| 3 | Praha (`T-01`) | [03_T-01_praha_prompt.txt](03_T-01_praha_prompt.txt) | západní okraj města u železničního přejezdu trati L2, pohled na Z (≈280°), 2×, konec února, ráno | cihlové a kamenné městečko na rovině, přejezd, pole, hory 8–11 km daleko s bílou zasněženou sjezdovkou na Zimní hoře, žádné moře |
| 4 | Staré městečko Paralandu (`PL-01`) | [04_PL-01_stare_mestecko_Paralandu_prompt.txt](04_PL-01_stare_mestecko_Paralandu_prompt.txt) | ulička ve starém městečku, pohled na JV (≈145°) do kopce, 2×, začátek října, pozdní odpoledne | kamenné domky, zřícenina hradu na zalesněném kopci asi 0,5 km nad městečkem, přímořské detaily (skleněné plováky, palmy), moře není vidět, protože je za zády |

Názvy míst do promptů záměrně nepíšeme. Generátor by je mohl vypsat do obrázku a třeba u Prahy by kreslil skutečnou Prahu.

## Jak byly indicie ověřeny

Každý prvek v promptu je skutečně viditelný ze stanoviště fotoaparátu. Ověření proběhlo výpočtem přímé viditelnosti nad výškovým modelem atlasu ([`atlas/current/relief/dem_20m_u16.png`](../../atlas/current/relief/dem_20m_u16.png), mřížka 20 m):

- výška očí 1,6 m nad terénem;
- započítané zakřivení Země;
- souřadnice z [`atlas/current/registry/places.json`](../../atlas/current/registry/places.json).

Poloha slunce odpovídá zvolenému datu a času na zhruba 34° s. š. Slunce je vždy za fotoaparátem nebo z boku, takže v záběru nesvítí proti objektivu.

| Kolo | Viditelné (azimut, vzdálenost) | Záměrně vynecháno, protože to ze stanoviště vidět není |
|---|---|---|
| 1 | Larpington 135°, 9,1 km; starý přístav 140°, 10,5 km; chaty HV-03 181°, 0,8 km; Horská stanice 195°, 0,7 km; tok řeky Larp 148–166° do 1,4 km; moře na celém obzoru 134–197° | vrchol Zimní hory, sjezdovka a vleky, Larpova hora, přehradní jezero (schované za hřbetem ve 2 km) |
| 2 | Kulatý vrch 290°, 7,3 km; Larpova hora 314°, 7,2 km; Zimní hora 329°, 6,0 km; horní část sjezdovky; nádrž SZ od hráze | Larpington a moře (z koruny je zakrývá okraj údolí) |
| 3 | Kulatý vrch 269°, 11,5 km; Larpova hora 284°, 10,1 km; Zimní hora 288°, 8,1 km; střední a horní část sjezdovky 282°, 7,9 km | moře, přehrada, Larpington (ten je 4,4 km na J, mimo záběr) |
| 4 | zřícenina PL-06 144°, 0,52 km (vrchol věže těsně dosahuje k obzoru); moře 0,3 km na S (za fotoaparátem) | vrchol Vyhlídky V-08, hlavní ostrov a hory, Larpington, marina; hrad PL-02 (295°, 1,5 km) je sice vidět, ale leží mimo záběr |
