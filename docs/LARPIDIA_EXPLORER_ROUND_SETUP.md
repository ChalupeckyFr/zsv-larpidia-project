# Nastavení kol Larpidia Explorer

Hra zatím používá režim `demo` a čtyři **skutečné body z veřejného atlasu**. Fotografie nejsou součástí hry; při výuce je promítejte samostatně.

## Až budou připravené fotografie

1. Vyberte fotografované místo v kanonickém atlasu Larpidie.
2. Zvolte jeho ID z veřejného registru `atlas/current/registry/places.public.json`. Pokud je potřeba přesná poloha stanoviště fotoaparátu, použijte ověřené atlasové souřadnice v metrech a upravte validační schéma i cíl kola společně.
3. V `explorer/rounds.json` změňte `targetPlaceId` u příslušného kola. Cíl musí existovat ve veřejném registru a mít platné souřadnice. Kód uživatelského rozhraní se kvůli výměně cílů neupravuje.
4. Plné fotografie ponechte ve snímcích přednášejících. Hra zobrazuje pouze mapu a po potvrzení název správného místa.
5. Spusťte `node explorer/validate-rounds.mjs` a `node explorer/scoring.test.cjs`; poté projděte všechna čtyři kola v prohlížeči.
6. Přepněte `mode` na `production` až po potvrzení všech čtyř fotografovaných míst a jejich odpovídajících bodů.

Souřadnice z registru jsou v kilometrech; hra je násobí tisícem. Čísla v atlasovém SVG odpovídají metrům, takže se skóre počítá přímo v této soustavě. Cílová místa v kódu prohlížeče nelze před motivovaným uživatelem utajit; hra je určena pro běžnou třídní fair play.
