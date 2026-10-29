# F8 – Závěrečná revize (atlas 1.0-draft)

Tento dokument říká, co se při závěrečné kontrole ověřilo, a co z toho plyne pro tým. Stav: **1.0-draft** – čeká na schválení tří bodů ze `FINAL_SUMMARY.md` (sekce 4); teprve potom se atlas zmrazí jako v1.0 a patch se sloučí do bible.

## 1. Co se ověřilo

| Kontrola | Výsledek |
|---|---|
| `check_atlas.py` (souhrnná kontrola, **41 kontrol**) | **vše v pořádku**: geometrie (SHA-256 obrysu, plochy, průliv, body), reliéf (13), lidská vrstva (32), registr, kanon (28 schválených tvrzení má odkaz), originály projektu beze změny (14 souborů), SVG a GeoJSON validní, vrstvy atlasu a prohlížeč, satelitní podklady (IoU souše, georeference, prompty, šikmé pohledy, mraky), plán hlavního města (13 vlastních kontrol + návaznost na atlas), shrnutí, manifesty všech snapshotů |
| Opakovatelnost | celý řetězec skriptů (reliéf → lidská vrstva → registr → atlas → satelit → plán města) byl spuštěn znovu v čisté kopii projektu: **81 ze 101 výstupních souborů je shodných byte po bytu** (včetně všech PNG/JPG renderů, GeoJSON, DEM a registrů); zbylých 20 se liší jen označením verze v popisku nebo ve zprávě o kontrole. Skripty jsou deterministické (pevná semínka) |
| Originály | `data/larpidia_world_bible.json`, reference, šablony a skripty projektu mají stejné SHA-256 jako na začátku (`ORIGINALS_SHA256.txt`); bible se nezměnila (patch není aplikován) |
| Snapshoty | všechny `versions/*` mají platný `MANIFEST.sha256`; nic se zpětně nezměnilo |
| Tvar ostrovů v obrazech | vlastní rendery S-01 / S-02 IoU souše 0,999 / 0,998; kontrola pozná posunutý obraz i obraz jiného pohledu |

## 2. Konzistence mezi vrstvami (ruční prohlídka)

- Stanice L1/L2/L3 v atlasu a v plánu města mají shodnou polohu (±0,3 m); tepny RD-11, RD-12, RD-07 a R1 mají v plánu stejnou délku jako v atlasu (kromě okružní komunikace u středu).
- Pobřeží v satelitních podkladech, šikmých pohledech i plánu je tentýž zmrazený obrys (SHA-256 `ffca09ac…`).
- Čtvrti C-03…C-06, přístav C-02 a stanice ST-W/N/E/S existují v registru atlasu i plánu.
- ID plánu `CP-*` nekolidují s ID atlasu (CP-01 místo M-01, rozpor C-03).
- Popisky: čeština je základ, japonština u japonských jmen, angličtina jako vypínatelná vrstva ve všech mapách.

## 3. Co se našlo a jak je to ošetřeno

| Nález | Řešení |
|---|---|
| C-17 – sídla a přístavy nesousedí (hlavní město × C-02, PL-05 × H-02) | plán CP-01 řeší staré město u přístavu (návrh); PL-05 čeká na potvrzení; render doplňuje pás zástavby jen vizuálně |
| C-18 – zastavěné území 6,3 km² místo 4,8 km² | návrh, rozhodnutí D11 |
| C-19 – hotel HV-01 daleko od promenády | v plánu CP-B09 u promenády (posun ≈ 270 m), atlas beze změny |
| C-20 – RD-12 končí 240 m před nábřežím | v plánu prodlouženo (Přístavní třída) |
| C-21 – pánev C-02 z F3 není čistý polygon | plán kreslí odvozenou vodní plochu; oprava geometrie je volitelný úkol po schválení |

## 4. Omezení (poctivě)

- Žádný obraz není skutečná družicová ani letecká fotografie; jde o simulované reference. Fotorealismus dodá externí generátor s referenčním obrázkem a následnou kontrolou tvaru.
- Ulice, bloky a půdorysy sídel jsou procedurální návrh; půdorysy domů hlavního města teprve vzniknou.
- Výšky, sklony, populace a délky jsou modelové hodnoty (viz `FINAL_SUMMARY.md`, sekce 3).
- Historická mapa 1608–1800 (K-073) a satelitní reference hlavního města (S-03) nevznikly.

## 5. Co dál

1. Tým projde `TEAM_APPROVAL_CHECKLIST.md` (3 skupiny rozhodnutí).
2. Po schválení: snapshot **v1.0**, sloučení `bible_patch_v1.1.json` do bible jako verze 1.1 (jen s výslovným souhlasem), nové SHA-256 originálů.
3. Detailní plán města (`CAPITAL_PLAN_BRIEF.md`), S-03, historická mapa, foto a videa.
