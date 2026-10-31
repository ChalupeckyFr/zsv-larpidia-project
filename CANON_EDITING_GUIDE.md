# Úpravy encyklopedie Larpidie

Veřejná encyklopedie je součástí hlavního webu v `index.html#encyklopedie`. Nevytvářejte vedle ní další kopii článků. Obsah se čte přímo ze souborů JSON a Markdown; web je statický a nepotřebuje databázi ani externí CMS.

## Kde upravit text článku

Každá kategorie má vlastní složku v `content/larpidia/`:

| Kategorie | Složka |
|---|---|
| O Larpidii | `content/larpidia/zakladni-informace/` |
| Geografie a příroda | `content/larpidia/geografie/` |
| Historie | `content/larpidia/historie/` |
| Politický systém a ústava | `content/larpidia/politika/` |
| Ekonomika | `content/larpidia/ekonomika/` |
| Obyvatelé a život | `content/larpidia/spolecnost/` |
| Města a doprava | `content/larpidia/mesta-a-doprava/` |
| Paraland a památky | `content/larpidia/paraland/` |
| Zahraniční vztahy a bezpečnost | `content/larpidia/zahranici-a-bezpecnost/` |

Články jsou soubory `.md`; například text daní najdete v `content/larpidia/ekonomika/dane.md`. Otevřete soubor, upravte běžný Markdown a uložte ho. Podporují se nadpisy, odstavce, seznamy, tabulky, odkazy a zvýraznění.

V každém detailu je tlačítko **Kopírovat článek**. Zkopíruje aktuálně zobrazený text včetně hodnot načtených z centrálního JSONu. V článku přehledu je navíc samostatný krátký odstavec připravený pro úvod prezentace.

## Jak upravit opakovaný údaj

Centrální fakta jsou v `content/larpidia/facts.json`. Články a hlavní přehled používají zástupné značky jako `{{fact.economy.corporateTaxPercent|percent}}` a `{{fact.country.population|number}}`.

**Příklad změny daně ze zisku firem:**

1. Otevřete `content/larpidia/facts.json`.
2. Najděte `"corporateTaxPercent": 5` a změňte hodnotu například na `6`.
3. Uložte JSON a obnovte místní stránku. Článek Daně zobrazí 6 % všude, kde používá tuto značku; obsahové karty ani komponenty se neopravují zvlášť.
4. Před zveřejněním ověřte, že změna odpovídá aktuálně schválenému kánonu.

Modelové a souhrnné hodnoty jsou odvozené ze vstupů ve stejném JSONu. Například délka pracovního týdne = počet pracovních dnů × hodin za den; turistický obrat = počet modelových návštěv × průměrná modelová útrata; částka na penzijní scénář se počítá z populace, podílu obyvatel 65+ a měsíčního důchodu. Tyto výsledky proto nejsou samostatně ručně udržovaná čísla. Pokud upravíte vstup, stránka výsledek přepočítá při dalším načtení. U modelových scénářů zůstává v textu upozornění, že nejde o konečný schodek ani naměřenou statistiku.

Značka může být například:

```md
Daň ze zisku: **{{fact.economy.corporateTaxPercent|percent}}**.
```

Formáty jsou `number`, `percent`, `czk`, `area` a `join` pro seznam. Odvozené částky používají předponu `calc`, například `{{calc.economy.tourismTurnoverCzk|czk}}`. Vypočítávané položky a jejich vztahy jsou v oddílu `derived` v `facts.json`.

## Jak přidat novou podstránku

1. Vytvořte Markdown soubor ve složce kategorie, např. `content/larpidia/geografie/klima.md`.
2. V `content/larpidia/index.json` přidejte objekt do pole `articles` příslušné kategorie. Musí mít jedinečné `id`, `title`, `summary`; volitelně také `keywords` a `media`.
3. Odkaz na článek bude mít tvar `#encyklopedie/geografie/klima`. Není potřeba upravovat navigaci v `index.html` ani JavaScriptovou komponentu.
4. Spusťte kontrolu `node scripts/validate_encyclopedia.mjs`.
5. Ověřte také chování sdílených hodnot příkazem `node scripts/check_encyclopedia_runtime.mjs`; kontrola zkouší dočasnou kopii dat s upravenou daní a turistickou útratou a zdrojové soubory nemění. Statické cesty lze ověřit příkazem `node scripts/check_encyclopedia_http.mjs`.

`id` pište malými písmeny bez diakritiky a mezer. Musí přesně odpovídat názvu souboru bez přípony.

## Jak přidat nebo vyměnit fotografii

Přidejte existující obrázek do projektu a zaregistrujte jej v `content/larpidia/media/assets.json`: jeho `id`, relativní `src`, přístupný `alt` text, popisek, vazbu na článek a typ. V Markdownu jej vložte značkou `![Popis](asset:id)`. Cesty jsou relativní ke kořeni webu. Neodkazujte na obrázek, který v projektu není.

Příklad položky registru:

```json
{"id":"nova-mapa","src":"atlas/current/renders/nova-mapa.jpg","alt":"Přehledová mapa západního pobřeží","caption":"Modelová mapa pobřeží.","article":"geografie/priroda","kind":"map"}
```

## Lokální zobrazení a nasazení

Protože se články načítají pomocí `fetch`, otevřete web přes místní HTTP server, ne přímo jako `file://`. Projekt obsahuje jednoduchý server bez dalších balíčků; v kořenové složce spusťte:

```powershell
node scripts/serve_static.mjs
```

Potom navštivte `http://127.0.0.1:4173/#encyklopedie`. Volitelně lze port změnit argumentem, např. `node scripts/serve_static.mjs 8000`. Po úpravě souboru obnovte stránku; automatický reload není nutný. Veřejný web načte nové soubory po nasazení aktualizované verze projektu; nový build krok se nepoužívá.

## Důležitá pravidla proti rozporům

- Opakovaná čísla neopisujte natvrdo do článků. Použijte faktickou značku z `facts.json`.
- Když nové číslo mění základ modelového výpočtu, upravte jeho vstup v `facts.json`; nepřepisujte ručně výsledek výpočtu v článku.
- Nejnovější potvrzený kánon má přednost před starou World Bible a staršími webovými texty. Pracovní archiv v `references/` není veřejný článek a obsahuje překonané varianty.
- Nevydávejte modelové ekonomické výpočty za naměřená data. Nerozměňujte tržby za zisk nebo příjem státního rozpočtu.
- Larpidie je fiktivní školní projekt. Skutečné státy v textech nejsou důkazem skutečných smluv.
- Neuvádějte detaily, které autoři nepotvrdili. Zvlášť respektujte stav podmořské L3, pravidla hlasování a podobu státních symbolů.
- Neměňte původní soubor kánonu v2.6 jako součást běžné úpravy webového obsahu.

## Důležité soubory

- `index.html` — existující web, navigace a původní místo encyklopedie.
- `encyclopedia.js` — vykreslení kategorií, článků, vyhledávání a sdílených faktů.
- `scripts/serve_static.mjs` — místní webový server bez dalších závislostí.
- `site.css` — vizuální podoba a mobilní rozvržení.
- `content/larpidia/index.json` — kategorie, názvy článků, popisy a vyhledávací metadata.
- `content/larpidia/facts.json` — centrální opakované hodnoty a modelové výpočty.
- `content/larpidia/<kategorie>/*.md` — samostatné texty článků.
- `content/larpidia/media/assets.json` — registr obrázků, popisků a vazeb na články.
- `scripts/validate_encyclopedia.mjs` — kontrola souborů, odkazů a zástupných značek.
- `scripts/check_encyclopedia_runtime.mjs` — ověřuje aktualizaci centrálních čísel a přepočet odvozených hodnot.
- `scripts/check_encyclopedia_http.mjs` — ověřuje načítání všech článků, médií, skriptů a stylů přes HTTP.
- `ENCYCLOPEDIA_MIGRATION_REPORT.md` — přehled migrace, nalezených rozporů a omezení.
