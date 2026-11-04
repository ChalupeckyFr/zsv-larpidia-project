# Oprava veřejného atlasu, plánu města a galerie

Opravy jsou sestavené do lokálního exportu `public/`. Ověření proběhlo na tomto exportu, nikoli na nasazeném hostingu.

## Provedené změny

- `scripts/build_public_site.mjs` vytváří veřejné whitelist projekce registrů. Zachovává všech **159 míst atlasu** a **662 objektů Larpingtonu**, souřadnice i interní ID pro hledání, ale do veřejných dat nepřenáší pracovní stavy, pseudo-GPS, poznámky, biblické odkazy ani fotografická vodítka. Synchronizaci vloženého registru plánu města generátor kontroluje před sestavením.
- Karty a popisky používají návštěvnické české názvy. Hledání `T-01` otevře **Prahu**, její podporované varianty `English: Prague · 日本語: プラハ`, stručný český popis, místní souřadnice a orientační výšku `41,1 m n. m.`. Legenda vysvětluje, že reliéf a výšky jsou orientační. ID zůstává v registrech a cílech prvků, ale nezobrazuje se v kartách, mapových štítcích ani detailu.
- Detail se po výběru aktualizuje a nastavení vrstev se sbalí. Oprava v `atlas/current/capital/capital_plan_viewer.html` ukládá cíl kliknutí před zachycením pointeru; tím se klik na městský objekt neztratí po jeho zvýraznění. V testu opakovaně otevřely detail radnice i další objekt.
- Upravené veřejné 2D popisky a lišty používají souřadnice v atlasu/plánu namísto procentních diagnostických souřadnic. Mobilní hlavička plánu Larpingtonu skládá název, orientační popis a odkaz na 3D bez překrytí.
- `content/larpidia/media/assets.json` je rozšířený zdrojový inventář s existencí, veřejností, popisky, vazbou na článek/místo a neveřejným soupisem scén. Veřejná galerie používá čtyři existující lokální obrazy: dvě fotografie a dvě ilustrace. Chybějící obrazové karty se negenerují. Veřejné cesty pro příběhové fotografie jsou namapované do `gallery/assets/`, takže export nemusí odkrývat interní složku promptů.
- Pomocný přehled `Obrazový archiv` je pouze ve zdrojovém náhledu; skutečný skript, markup a inventář v Edge ukázaly **2 hotové fotografie** a **18 chybějících scén**. Veřejná stránka přehled ani neveřejný seznam scén neobsahuje.
- `site-brand.js` a `site-brand.css` používají stejný skutečný soubor `Larpidie logo.png` v hlavičkách a patičkách včetně samostatných mapových stránek. Vnořené stránky se značkou neduplikují logo iframe rodiče. Rozdílné původní značky byly tvořené samostatnými `span.brand-mark` v různých šablonách; společný skript je převádí na ověřený obrazový soubor a doplňuje jej také do samostatně otevřených prohlížečů.
- Stávající soubor promptů byl rozšířen, ne nahrazen: `v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/03_PHOTO_PROMPTS/ALL_PHOTO_PROMPTS.md`.

## Příklady před a po

- Detail `T-01`: z pracovních polí a diagnostických souřadnic na **Praha** → `English: Prague · 日本語: プラハ` → český popis → `Souřadnice v atlasu` → `Nadmořská výška: 41,1 m n. m.`.
- Plán města: kliknutí už nezůstává jen u zvýraznění; výběr otevře detail objektu. ID zůstává použitelné přes hledání, ale není titulkem ani součástí veřejného popisu.
- Galerie: čtyři obrazové karty mají skutečně načtené obrázky; v prohlížeči nebyly prázdné ani rozbité karty.

## Ověření

Z kořene projektu:

```powershell
node scripts/build_public_site.mjs
node scripts/check_public_export.mjs
node scripts/check_encyclopedia_http.mjs
node scripts/check_public_render.mjs
```

- Sestavení: `public/` obsahuje všech 159 míst a 662 městských objektů.
- Export: **76 povolených souborů**, 39 článků, všechna ID a souřadnice zachovány; všechny veřejné skripty prošly syntaktickou kontrolou. Test zároveň ověřuje přesnou shodu čtyř 3D datových souborů se zdrojem SHA-256 a shodu SVG `path d` v obou 2D mapách.
- HTTP: obslouženo 85 veřejných cest; 14 interních cest včetně dokumentace, zdrojových registrů a promptů vrátilo 404.
- Edge headless: skutečné vykreslení veřejného exportu na desktopu a při šířce 390 px. Ověřeno vyhledávání ID, anglického názvu a názvu bez diakritiky, nulový výsledek, český detail Prahy a její výška, výběry mapových prvků v atlasu i plánu, opakované kliknutí, posun a přiblížení, jazykové popisky, mobilní dotykové klepnutí, sbalení vrstev, čitelnost detailu při posouvání mobilního panelu, nekolizní hlavička města, 4 vykreslené galerijní obrázky a načtené logo. Nenašly se chyby načítání lokálních souborů ani neodchycené chyby JavaScriptu.
- Stejný prohlížeč spustil zdrojový skript a skutečné HTML dialogu archivu nad soupisem ověřeným vůči souborům na disku. Kontrola potvrdila hodnoty 2/18, čtyři dostupné položky, osmnáct chybějících scén a návrat fokusu po zavření.
- Snímky skutečně vykreslených desktopových i mobilních stránek z posledního běhu jsou dočasně uložené mimo repozitář v `%TEMP%\larpidia-public-render-5hmPy5\screenshots\`.
- `git diff --check` prošel pro zdrojové změny i nově sestavené mapové HTML. Zůstávají pouze upozornění Git o převodu konců řádků LF/CRLF v pracovním stromu.

## Hranice ověření a zbývající obsah

- Automatický Edge běh používá `--disable-gpu`, proto **samotný obraz WebGL 3D scén nebyl vizuálně ověřen**. Veřejné 3D HTML a odkazy jsou přítomné a všechny čtyři geometrické datové JS soubory jsou bajt po bajtu totožné se zdrojem; kontrola tedy potvrzuje zachování dat, nikoli vizuální shodu vykresleného snímku.
- Galerie záměrně obsahuje čtyři dostupné obrazy; dalších 18 plánovaných fotografií není vytvořeno a zůstává pouze v interním inventáři.
- U scén `PHOTO_01` a `PHOTO_06` inventář uvádí skutečnou cestu k souboru `.png` a současně plánovanou cestu `.jpg`. Použité PNG existují a fungují; sjednocení očekávané přípony je ponecháno v rozhodovacím přehledu.
- Nebyl ověřen žádný veřejný hosting ani nasazení. Ověřený náhled spusťte přes `node scripts/serve_static.mjs`; server zpřístupňuje výhradně `public/` na `http://localhost:4173/`.
