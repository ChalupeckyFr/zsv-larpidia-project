# Atlas Larpidie a Paralandu – shrnutí pro tým (verze 1.0-draft)

Kanonický geografický podklad pro satelitní vizualizace (S-01, S-02), plán hlavního města a budoucí fotografie a videa. **Všechno je fikce a pracovní návrh**, dokud tým neschválí tři body v sekci 4. Originály projektu (bible, reference, šablony) se nezměnily (SHA-256 v `ORIGINALS_SHA256.txt`).

## 1. Co tým dostává

| Co | Kde | Poznámka |
|---|---|---|
| Zmrazený obrys obou ostrovů (varianta B) | `current/geometry/` | 175,0 km² a 13,98 km², průliv 1,50 km, rámec 24 × 16 km, SHA-256 obrysu v každém výstupu |
| Reliéf, vody, krajina | `current/relief/` | DEM 20 m, max. 560,0 m (modelové), řeka → jeskyně → vodopád → přehrada |
| Doprava, sídla, přístavy, letiště | `current/human/` | R1 53,9 km, L1 8,72 km, L2 29,0 km, L3 15,9 km (podmoří 1482 m) |
| Registr míst | `current/registry/` | 159 objektů, foto/video vodítko u bodových objektů |
| Atlas jako mapa a prohlížeč | `current/svg/`, `current/viewer/atlas.html` | A2 1 : 50 000, vrstvy, popisky cs/ja/en, režim kánon × návrh |
| Satelitní podklady a šikmé pohledy | `current/renders/` | S-00 (přehled), S-01 Larpidie, S-02 Paraland, **S-03 Larpington (2 m/px, domy z plánu města, výškový model budov)**, 6 šikmých pohledů (z toho 2 na Larpington s hmotami budov), masky, prompty, `verify_sat.py` |
| Plán hlavního města Larpingtonu (CP-01) | `current/capital/` | A2 1 : 10 000, 2005 úseků ulic (158,1 km), 874 bloků, 3242 ilustrativních domů (kapacita 12000 obyv.), 968 objektů |
| Rozhodnutí, rozpory, otázky | `docs/CONFLICTS_AND_DECISIONS.md` | R-01…R-07, C-01…C-22, O1…O25 |
| Návrh změn bible | `docs/bible_patch_v1.1.json` | neaplikováno; slučuje se až po schválení |
| Historie verzí | `versions/`, `CHANGELOG.md` | 11 neměnných snapshotů |

## 2. Jak to používat

1. **Mapa:** otevřete `current/viewer/atlas.html` (hledání, vrstvy, jazyky). Pro úpravy `current/svg/larpidia_atlas_master.svg` (Inkscape).
2. **Satelit a fotky:** do externího generátoru vždy vložte referenci (`current/renders/S-01_base.png` apod.) a prompt z `S-0x_prompt.md`; výsledek ověřte `python atlas/scripts/verify_sat.py S-01 obraz.png`. Šikmé pohledy: `OBLIQUE_PROMPTS.md`.
3. **Plán města:** `current/capital/capital_plan_viewer.html` a `capital_plan_base.svg`; zadání další etapy je v `docs/CAPITAL_PLAN_BRIEF.md`.
4. **Foto/video:** před každým záběrem vezměte řádek z `registry/photo_guide.csv` nebo `capital/cp_photo_guide.csv` (*pohled kam, blízké a vzdálené body, styl, roční doba, čemu se vyhnout*).

## 3. Co je schváleno a co je návrh

- **Kanon z bible/šablon:** 95 tvrzení v `canon_extract.csv`: 28 schválených, 66 navržených, 1 k rozhodnutí. Každé schválené tvrzení má v atlasu odkaz na objekt nebo vysvětlení.
- **Objekty atlasu (159):** existence `approved` 51 · `proposed` 108 · `needs_decision` 0; jména `approved` 4, `proposed` 149; **polohy `proposed` u všech 159**.
- **Objekty plánu města (968):** existence `approved` 6 (parlament, muzeum, historický přístav, pobřežní silnice, promenáda, plán), ostatní `proposed`; všechny polohy a jména `proposed`.
- Schválená existence u objektů atlasu: B-01, B-02, B-03, B-04, B-05, B-06, BAY-N1, BAY-N2, BAY-S, C-01, C-02, CAPE-W, CY-01, CY-02, CY-03, CY-04, CY-05, CY-06, DAM-N04, I-01, L1, L2, L3, M-01, M-02, M-03, N-01, N-02, N-03, N-04, P-01, PEN-SE, PL-01, PL-02, PL-03, PL-04, PL-05, PL-06, RD-R1, SP-01 ….
- **Modelové hodnoty** (ne měření, ne kánon): výšky vrcholů, hladina a hráz přehrady, výška vodopádu, populace sídel (součet 32 000), délky tras, zastavěné území, sklony.
- Pseudo-souřadnice (kolem 33,9 N / 137,6 E) jsou **hypotetické**; satelitní obrázky jsou **simulace**, ne družicová data.

## 4. Nejvýše tři otevřené body k rozhodnutí týmu

Pro zmrazení **v1.0** stačí rozhodnout tyto tři skupiny; zbytek platí jako výchozí volba, pokud tým nenamítne.

1. **Geometrie a polohy (D1, D7).** Potvrdit obrys varianty B, rámec 24 × 16 km a 3 odchylky ≤ 3 % od tabulky (T-04, T-05, A-01); polohy všech bodů jsou zatím `proposed`.
2. **Doprava a hlavní město (D8, D10, D11, D12).** Potvrdit vedení R1/L1/L2/L3 (R1 po útesech a ve 3 tunelech, právě 3 přestupy L2↔L3), kompozici města (Náměstí čtyř × parlament u přístavu), zastavěné území 6,31 km² (zastavěno je jen jádro pro 12000 obyvatel, zbytek je rezerva rozvoje, C-22) a napojení na přístav, polohu hotelu HV-01 a muzea.
3. **Jména a modelová čísla (D2, D5, D9).** Potvrdit 44 navržených jmen (`registry/names_proposed.csv`), jména čtvrtí a ulic plánu, rozlohy (175 + 14 km²), populaci 32 000 a výšky vrcholů. D6 (barvy vlajky) ovlivní jen paletu map.

Podrobný seznam k zaškrtnutí: `docs/TEAM_APPROVAL_CHECKLIST.md`.

## 5. Poctivě: omezení

- Nebyl vytvořen žádný fotorealistický obraz ani družicová data; S-00…S-02 a šikmé pohledy jsou procedurální reference, ze kterých externí generátor (s referenčním obrázkem) vytvoří realistickou verzi. Tvar se ověřuje IoU maskou.
- Procedurální jsou i ulice a bloky plánu města; **domy v plánu, v S-03 a v šikmých pohledech jsou ilustrativní půdorysy** (3242 domů vzniká v blocích podle využití a je kalibrováno na modelovou populaci Larpingtonu), nejsou to skutečné budovy. Plné zastavění všech bloků by dalo ≈ 48348 obyvatel, víc než schválený strop 40 000 pro celou zemi (C-22).
- Geometrie přístavní pánve C-02 z F3 není čistý polygon (C-21); plán kreslí odvozenou vodní plochu.
- Historická mapa 1608–1800 zatím nevznikla.

## 6. Co dál

1. Tým zaškrtne `TEAM_APPROVAL_CHECKLIST.md` → atlas **v1.0 (freeze)**, patch se sloučí do bible jako 1.1.
2. Dopracování detailního plánu města podle připomínek týmu (`CAPITAL_PLAN_BRIEF.md`: výřezy 1 : 2 500, adresní vrstva) a historická mapa 1608–1800.
3. Fotografie a videa z vodítek v registrech, vždy s referenčním obrázkem a kontrolou tvaru.
