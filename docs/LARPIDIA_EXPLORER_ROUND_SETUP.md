# Nastavení kol Larpidia Explorer

Hra zatím používá režim `demo` a čtyři **skutečné body z veřejného atlasu**. Fotografie nejsou součástí hry; při výuce je promítejte samostatně.

Podrobné prompty pro generátor obrázků ke všem čtyřem ukázkovým kolům jsou ve složce [`explorer/prompts/`](../explorer/prompts/README.md). Jsou tam i ověřené indicie, které musí být na fotkách vidět. Složka se do veřejného webu nekopíruje. Při výměně cíle kola napište k novému místu i nový prompt.

## Vstupní heslo pro výuku

Explorer má vstupní obrazovku se společným heslem, které přednášející ukážou na tabuli. Před odemknutím je hra skrytá a nenačítá konfiguraci kol ani mapu. Běžný atlas zůstává veřejný.

Ověření probíhá lokálně pomocí SHA-256 přes Web Crypto, proto web vyžaduje HTTPS nebo lokální náhled na `localhost` / `127.0.0.1`. Heslo se na tabuli píše **velkými písmeny**. Před ověřením se zadaný text ořízne o mezery na krajích a převede na velká písmena, takže projde i heslo napsané malými. Heslo se neodesílá ani neukládá v otevřeném tvaru; ověřovací otisk je v `explorer/access.js`. Při změně hesla nahraďte `PASSWORD_DIGEST` SHA-256 otiskem nového hesla zapsaného velkými písmeny, například `node -e "console.log(require('crypto').createHash('sha256').update('NOVEHESLO').digest('hex'))"`, a znovu sestavte web.

Odemknutí je v `sessionStorage` stejné karty a přežije obnovení stránky. Nová samostatně otevřená karta vyžaduje heslo znovu; obnova nebo duplikování karty se může řídit chováním prohlížeče. Postup hry zůstává odděleně v `localStorage`. Pokud prohlížeč ukládání zakáže, zobrazí se upozornění a odemknutí platí jen do obnovení stránky.

Jde o **klientskou bránu pro třídní fair play, nikoli zabezpečení hostingu**. Návštěvník může bránu technicky obejít; statické soubory a cíle nejsou serverově chráněné. Kontrolu vstupu i celé hry spouští `node scripts/capture_explorer_screenshots.mjs`; aktuální heslo předejte prostředím `LARPIDIA_EXPLORER_PASSWORD`, nikdy je nevkládejte do testovacího kódu. Volitelné `LARPIDIA_SCREENSHOT_DIR` určuje složku snímků místo výchozí `docs/debug-screenshots/`.

## Až budou připravené fotografie

1. Vyberte fotografované místo v kanonickém atlasu Larpidie.
2. Zvolte jeho ID z veřejného registru `atlas/current/registry/places.public.json`. Pokud je potřeba přesná poloha stanoviště fotoaparátu, použijte ověřené atlasové souřadnice v metrech a upravte validační schéma i cíl kola společně.
3. V `explorer/rounds.json` změňte `targetPlaceId` u příslušného kola. Cíl musí existovat ve veřejném registru a mít platné souřadnice. Kód uživatelského rozhraní se kvůli výměně cílů neupravuje.
4. Plné fotografie ponechte ve snímcích přednášejících. Hra zobrazuje pouze mapu a po potvrzení název správného místa.
5. Spusťte `node explorer/validate-rounds.mjs` a `node explorer/scoring.test.cjs`; poté projděte všechna čtyři kola v prohlížeči.
6. Přepněte `mode` na `production` až po potvrzení všech čtyř fotografovaných míst a jejich odpovídajících bodů.

Souřadnice z registru jsou v kilometrech vzhledem k atlasovému rámci. Počátek rámce je `(-0,2 km, -1 km)`, proto se poloha v SVG v metrech počítá jako `((x_km + 0,2) × 1000, (y_km + 1) × 1000)`. Hra používá stejný převod pro cíle i validační kontrolu; skóre se tak počítá ve stejné soustavě jako atlas. Cílová místa v kódu prohlížeče nelze před motivovaným uživatelem utajit; hra je určena pro běžnou třídní fair play.
