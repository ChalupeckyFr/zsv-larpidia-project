# Larpidia Explorer — zpráva o implementaci

## Hotovo

- Samostatná stránka hry je dostupná na `explorer/index.html`; domovská stránka ji odkazuje v navigaci i na úvodní obrazovce. Běžný atlas a návrat na web zůstávají dostupné.
- Herní mapa načítá skutečné SVG přímo z běžného atlasu a veřejný registr 159 míst. Klepnutí se přes SVG transformační matici převádí na atlasové metry; zoom, posun, přetažení i gesto dvěma prsty zachovávají geografické ukotvení tipu.
- Čtyři demo cíle jsou existující místa `SP-01`, `DAM-N04`, `T-01` a `PL-01`. Hra je kontroluje proti veřejnému registru. Finální fotografie ani jejich stanoviště zatím nebyly zvoleny.
- Čtyři kola bodují v prohlížeči vzorcem ze specifikace, zobrazují tip, cíl, popis, vzdálenost a body až po potvrzení. Přeskočení vyžaduje potvrzení a dává nula bodů. Neexistuje odpočet ani časová penalizace.
- Rozpracovaná expedice, jméno týmu a výsledky se ukládají pouze do místního `localStorage`. Stránka neposílá herní údaje na server a nemá sdílené skóre ani žebříček.
- `scripts/build_public_site.mjs` zahrnuje soubory Exploreru do exportu. Veřejný export zachovává kontrolované počty 159 míst atlasu a 662 objektů Larpingtonu.
- Postup výměny demo cílů za skutečná fotografovaná místa je v [LARPIDIA_EXPLORER_ROUND_SETUP.md](LARPIDIA_EXPLORER_ROUND_SETUP.md).

## Ověření

- `node explorer/scoring.test.cjs` — přesná shoda, všechny rohy čtverce 3 × 3 m, bod těsně za hranicí, vzdálenosti 100 m / 1 km / 5 km / 15 km / nad 15 km, přeskočené kolo a strop 20 000 bodů.
- `node explorer/validate-rounds.mjs` — čtyři různé cíle existují ve veřejném registru a leží v atlasovém viewBoxu; ověřena hlavní ostrovní místa i Paraland. Souřadnice registru v kilometrech se násobí tisícem a odpovídají jednotkám SVG v metrech.
- `node scripts/build_public_site.mjs` — sestavení exportu proběhlo úspěšně a ohlásilo `159 atlas places, 662 Larpington objects`.
- `node scripts/capture_explorer_screenshots.mjs` — skutečný průchod v headless Microsoft Edge: vstupní obrazovka, umístění tipu, obnovení stránky, nezobrazení cíle před potvrzením, odhalení, všechna čtyři kola, konečný součet a samostatné načtení `public/`.
- Prošel také test přetažení mapy bez vložení tipu a opakované umístění stejného atlasového bodu před a po zoomu; rozdíl byl pod 0,01 m.
- Prohlížeč zachytil 39 statických požadavků, všechny metodou GET. Herní kód neodesílá POST, WebSocket ani analytické události.
- Ověřeno ve zdrojovém webu přes `scripts/serve_root.mjs` a zvlášť ve veřejném exportu přes `scripts/serve_static.mjs`. Jde o stejný root a `public/` obsah, které zpřístupňuje Live Server; nebyl spuštěn přímo příkaz z rozšíření VS Code.
- Mobilní rozvržení bylo ověřeno emulací Edge 390 × 844 a desktopové 1440 × 1000. Fyzický telefon k dispozici nebyl.

Snímky skutečně běžící aplikace jsou v `docs/debug-screenshots/`: `explorer-mobile-intro.png`, `explorer-desktop-round.png`, `explorer-mobile-guess.png`, `explorer-mobile-result.png` a `explorer-mobile-summary.png`.

## Omezení

Režim zůstává `demo`, protože čtyři finální fotografie a přesná fotografovaná stanoviště ještě neexistují. Souřadnice cíle jsou součástí statické konfigurace doručené prohlížeči, takže je motivovaný hráč může technicky prohlédnout. Hra je určena pro běžnou třídní fair play; serverovou ochranu ani synchronizaci záměrně nepoužívá.

## Dokončovací úpravy UI, atlasu a mobilního zobrazení

- Herní tip je vrstvený oranžový terč s kontrastním okrajem a zůstává přibližně 28 px široký i při změně zoomu. Správné místo má zelený kosočtverec se symbolem zaškrtnutí. Při velmi malé vzdálenosti se terče v obrazovce mírně odsunou, aby se nepřekryly.
- Výsledek kola i souhrn odkazují na skutečný atlas s parametrem `place`; atlas vybere místo, přiblíží mapu a otevře jeho detail.
- Ve veřejném atlasu mají existující plochy sídel sjednocenou tlumenou barvu a jemnější obrys. Geometrie a interakce zůstávají ze zdrojových sídelních dat.
- Ověření Edge zachytilo atlas, vybranou Prahu a mobilní atlas při 390 × 844 bez horizontálního přetékání. Snímky jsou v `docs/debug-screenshots/`.
