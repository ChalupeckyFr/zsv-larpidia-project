# F9 – Domy v plánu hlavního města a šikmé pohledy na Larpington (snapshot v1.0.1-capital-detail)

Etapa nad rámec původního plánu F0–F8 (plán ji vedl jako „mimo rozsah“; zadání je v `CAPITAL_PLAN_BRIEF.md`). Atlas zůstává ve verzi 1.0-draft ke schválení týmem; F9 ji doplňuje (snapshot `v1.0.1-capital-detail`, předchozí `v1.0-draft` se nemění). Vše je **pracovní návrh (`proposed`)**, domy jsou **ilustrativní půdorysy**, ne skutečné budovy.

## Co přibylo

| Výstup | Kde | Popis |
|---|---|---|
| Domy | `current/capital/cp_houses.geojson` (+ `_atlas_km`) | ilustrativní půdorysy (`CP-H-xxxxx`): využití, podlaží, výška okapu a hřebene, barva střechy, modelová kapacita bydlení; vrstva `houses` v SVG a prohlížeči |
| Stav bloků a ulic | `cp_blocks.geojson` (`build_state`, `houses`, `capacity_model`), `cp_streets.geojson` (`state`) | bloky `built` / `partial` / `reserve` / `civic`, ulice `built` / `planned` |
| Plán města | `capital_plan_base.svg` / `.png`, `capital_plan_viewer.html` | rezerva rozvoje světle, plánované ulice čárkovaně, legenda a poznámka o stavu zástavby |
| Satelit S-03 | `renders/S-03_base.png` / `.jpg` | tytéž domy jako v plánu; rezerva zůstává krajinou (louky, sady), plánované ulice jsou polní cesty, chaty mají zahrádky |
| Výškový model budov | `renders/S-03_buildings_height.png` | 16bit PNG, 1 jednotka = 0,1 m nad terénem, stejné pixely jako S-03 (domy se sedlovými střechami, klíčové budovy ploché) |
| Šikmé pohledy | `renders/S-03_oblique_S.jpg`, `S-03_oblique_W.jpg` (+ `_camera.json`) | z moře jižně od přístavu k Náměstí čtyř; od západní stanice podél Hlavní třídy; stěny budov tmavším odstínem střechy; prompty v `OBLIQUE_PROMPTS.md` |

## Jak domy vznikají (`scripts/cp_houses.py`)

1. V každém z 874 bloků se podle využití vytvoří kandidáti bez překryvů a mimo klíčové budovy: perimetrová zástavba (staré město, promenáda, Hlavní třída, okolí stanic, bydlení), rodinné domy, desky Východního nábřeží, instituce státní čtvrti. Školy a hotel mají vlastní klíčové budovy.
2. Bloky se zastavují od **jader**: Náměstí čtyř, přístavní náměstí a stanice (stanice jsou slabší jádra). Hranice zastavění se bisekcí doladí tak, aby **kapacita bydlení odpovídala modelové populaci Larpingtonu** (`population_model` C-01 v `current/human/settlements.geojson`, 12 000). Blok na hranici se plní od strany jádra.
3. Ostatní bloky jsou **rezerva rozvoje**; stojí v nich jen řídké chaty (124), které se počítají do kapacity.
4. Kapacita = půdorys × podlaží × podíl bydlení × 0,82 / 38 m² na obyvatele (modelové předpoklady v `cp_report.json`).

## Výsledek

| Ukazatel | Hodnota |
|---|---|
| Domy | 3 242 (3 118 v jádru, 124 chat) |
| Kapacita bydlení | 12 000 obyvatel (cíl 12 000) |
| Bloky | 217 zastavěných, 29 částečně, 586 rezerva, 42 institucí a škol |
| Zastavěnost zastavěných bloků | ≈ 29 % půdorysu |
| Plné zastavění všech bloků (pro srovnání) | ≈ 48 000 obyvatel (4,0×) |

## Nález C-22 (k rozhodnutí týmu, součást bodu 2 ve `FINAL_SUMMARY.md`)

Plán vymezuje 6,31 km² a 874 bloků. Kdyby se všechny zastavěly podle svého využití, měly by kapacitu ≈ 48 000 obyvatel, tedy víc než schválený strop 40 000 pro **celou zemi** (bible: `population_range`) a čtyřnásobek modelové populace Larpingtonu. Plán proto rozlišuje **vymezené území** a **stav zástavby**. Alternativy:

- **(b) výchozí:** ponechat vymezené území a rezervu rozvoje; město vypadá jako kompaktní jádro s plánovanou sítí kolem;
- (a) zmenšit vymezené území na ≈ 2 km² (kompaktní město; nový plán);
- (c) zvýšit populaci Larpingtonu a snížit ostatní sídla (součet ≤ 40 000).

Stav zástavby řídí jediné číslo (`population_model`); po změně stačí znovu spustit `build_capital.py` a `render_sat.py all`.

## Kontroly

`build_capital.py`: 17 kontrol plánu (z toho 4 nové: ID domů, kapacita × populace × strop 40 000, domy na souši mimo ulice a klíčové budovy, stavy bloků). `check_atlas.py`: výškový model budov (stejné pixely jako S-03, největší výška ≤ 40 m), šest šikmých pohledů, domy × populace v atlasu.

## Omezení

- Domy jsou procedurální (typologie podle využití bloku); neodpovídají skutečným parcelám ani budovám a nemají adresy.
- Šikmé pohledy mají svislé převýšení 1,35× (terén i budovy); zdroj S-03 má 2 m/px, takže blízké záběry jsou měkké a domy mají jednoduché sedlové střechy.
- Stylování (barvy plánu) čeká na schválení státních barev (D6); adresní vrstva POI a výřezy 1 : 2 500 zatím nevznikly.
