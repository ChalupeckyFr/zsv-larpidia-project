# Rozpory, rozhodnutí a otevřené otázky — Atlas Larpidie

Stav k 2026-10-23, verze atlasu viz `../CHANGELOG.md`. Originály projektu (bible, reference, šablony) se nemění; jejich SHA-256 jsou v `ORIGINALS_SHA256.txt` (14 souborů).

Priorita při sporu (README): výslovné nové schválení týmem > schválené údaje v bibli > návrhy v souborech > preference generátoru.

## A. Rozhodnutí týmu

| ID | Rozhodnutí | Důsledek |
|---|---|---|
| R-01 | Referenční rámec hlavního ostrova **24 × 16 km**, průliv **1,5 km**, plochy **175 km² + 14 km²** (modelové) | Převod X % → x = X·0,24 km, Y % → y = Y·0,16 km |
| R-02 | Souřadnice z GEOGRAPHY jsou základ, **odchylky do ~3 %** (≈ 0,72 km ve směru x, 0,48 km ve směru y) | Každá odchylka je zapsána v sekci D |
| R-03 | Výstupy do `atlas/`, **originály beze změny**; změny kanonu jen jako `docs/bible_patch_v1.1.json` | Do bible se sloučí až po schválení |
| R-04 | **Verzovaný styl**: po každé významné úpravě neměnný snapshot v `versions/` | `snapshot.py`, `CHANGELOG.md`, `MANIFEST.sha256` |
| R-05 | S-01/S-02 = vlastní render + prompty pro externí nástroj s referenčním obrázkem; bez placené AI | Žádné volání Figma/Weave bez nového souhlasu |

## B. Rozpory a mezery v podkladech

| ID | Nález | Řešení | Stav |
|---|---|---|---|
| C-01 | Šířka průlivu: MAP_PROMPT „2–3 km“ × GEOGRAPHY a JSON „1,5 km“ | 1,5 km (R-01) | vyřešeno |
| C-02 | Rozměry referenčního obdélníku nejsou nikde uvedeny | 24 × 16 km (R-01) | vyřešeno |
| C-03 | **Kolize ID**: v MAP_PROMPT se plán hlavního města jmenuje „M-01“, ale M-01 je v tabulce nejvyšší vrchol | Vrchol zůstává M-01. Plán města dostane ID **CP-01** (O14) | navrženo |
| C-04 | Paragliding: JSON (approved) = zaoblený vrchol pro turistiku a paragliding; tabulka: M-02 = lyžování **i** paragliding, M-03 = jen turistika | Platí bible: M-02 sjezdovka, M-03 turistika + paragliding (O2) | navrženo |
| C-05 | L1 je „okruh“, ale vede „z města do západní přírody“ | Linka + koncová smyčka v jeskyni (O1) | navrženo |
| C-06 | L3 má 3 přestupy na L2, ale jádro hlavního města je jen ≈ 2,6 × 1,6 km | L2 obchází město obloukem (O4) | navrženo |
| C-07 | Paraland leží mimo referenční obdélník (P-01 je na jihovýchodním poloostrově, Paraland až za průlivem) | Společný rámec atlasu (plátno A2 / 1 : 50 000) | vyřešeno |
| C-08 | Okružní **pobřežní** silnice (approved) × útesy a skalní mys na SZ | Silnice vede po většině obvodu u moře, na SZ krátce vnitrozemím za útesy | navrženo |
| C-09 | Souřadnice bez umístění v tabulce: severní rybářský přístav, Hoshimachi, marina a vše na Paralandu, stanice linek, letiště na Paralandu, pláže, hráz, vyhlídky, prameny | Navrhne se jako `atlas_new` + `proposed` | otevřeno do F3 |
| C-10 | Jižní přístav C-02 je vystavený tajfunům (bible `disaster_planning`) | Vlnolam a poznámka v registru | navrženo |
| C-11 | Pláže ne na útesovém SZ (SKILL.md) | Pláže jen J/JV hlavního ostrova a V Paralandu | navrženo |
| C-12 | Hodnocení „stavu“ celé tabulky: poloha všech bodů je `proposed`, schválená je jen existence a role | Atlas zůstává *draft* do schválení D1 | trvá |

## C. Otevřené otázky (výchozí volba platí, pokud tým nenamítne)

| # | Otázka | Výchozí volba | Nutné před |
|---|---|---|---|
| O1 | L1: okruh, nebo linka? | Linka z Chalupecké čtvrti přes Čimprlichovo Hradiště a přehradu k vodopádu a jeskyni; jeskyně = koncová smyčka na ¾ obvodu s jedním portálem; horská stanice | F3 |
| O2 | Který vrchol je lyžařský a který paraglidingový? | M-01 nejvyšší (560 m), M-02 prudší sjezdovka (~510 m), M-03 zaoblený – turistika + paragliding (~440 m); výšky `proposed` | F2 |
| O3 | Trasa L2 | Hlavní město → Praha → (odbočka k A-01) → Aokawa → Ōru Maito; druhá větev k I-01/I-02/I-03; Havlišovo Doupě bez železnice; Hoshimachi na lince | F3 |
| O4 | L3 a tři přestupy na L2 | ~8 stanic; L2 obchází město obloukem (sever + východ) | F3 |
| O5 | Silnice | R1 okružní pobřežní silnice (~70–80 km); Paraland vlastní okružní servisní silnice bez autopřevozu | F3 |
| O6 | Přístavy | C-02 historický, I-03 nákladní, **H-01** severní rybářský, **H-02** marina Paraland; volitelně lodní okruh C-02 ↔ H-02 | F3 |
| O7 | Letiště | A-01 dráha 09/27 ≈ 1 900 m; **A-02** na Paralandu travnatá ≈ 700 m | F3 |
| O8 | Jména nových prvků | Navrhnu česky (+ EN/JA tam, kde se hodí), vše `proposed` | F4 |
| O9 | Umístění Hoshimachi a rybářského přístavu | Rybářský přístav v hlubší severní zátoce u Ōru Maito; Hoshimachi ve východní severní zátoce | F1 |
| O10 | Velikost sídel | Půdorysy z modelového rozdělení 32 000 obyvatel (označeno „modelové“) | F3 |
| O11 | Jazyky popisků | Čeština + japonština u japonských jmen; EN jako vypínatelná vrstva | F5 |
| O12 | Plán města v této etapě | Jen podklad | F7 |
| O13 | Barvy | Neutrální paleta, vlajka/barvy čekají na D6 | F5 |
| O14 | ID plánu hlavního města (kolize s M-01) | **CP-01** | F7 |
| O15 | Poloha naleziště larpiditu (bible: omezené naleziště, bez polohy) | Na mapě **nezakreslovat**; v registru záznam bez polohy (`needs_decision`) | F4 |
| O16 | Místo prvního přistání osadníků 1608 (bible jen „přístavy, kostely, tržiště“) | Historický přístav C-02 (`proposed`); potřebné pro historickou mapu a muzeum | F8 |
| O17 | Kde jsou historické rýžové terasy a pole | Jihozápadní úpatí kolem Čimprlichova Hradiště a Havlišova Doupěte (`proposed`) | F2 |

## D. Odchylky od polohy v tabulce GEOGRAPHY

Zatím žádné. Plní se ve fázích F1 a F4 (ID, původní X/Y, nová X/Y, odchylka v %, důvod). Mezní hodnota 3 %.

## E. Konvence

- **status** (`approved` / `proposed` / `needs_decision`) jako v bibli; navíc **origin**: `bible` (s JSON cestou), `geo_ref` (řádek tabulky), `atlas_new` (nové v tomto atlasu).
- U bodů z tabulky se rozlišuje `exist_status` / `name_status` / `pos_status`. Poloha je zatím vždy `proposed`.
- ID: stávající M- (vrcholy), N- (příroda), C- (hlavní město), T- (města), I- (průmysl), A- (letiště), P-01 (spojení na Paraland), S-01/S-02 (satelitní snímky), L1–L3 (linky). Nové: W- (voda), H- (přístavy), B- (pláže), V- (vyhlídky), SP- (prameny), PL- (Paraland), ST- (stanice), RD- (silnice), TR- (stezky), CP- (plány měst).
- Souřadnice: lokální km (x východ, y jih, počátek v SZ rohu rámce 24 × 16 km). Pseudo-lon/lat (kolem 33,9 N / 137,6 E) je **hypotetické**.
- SVG: 1 jednotka = 1 m, tisk A2 (594 × 420 mm) přesně 1 : 50 000.
