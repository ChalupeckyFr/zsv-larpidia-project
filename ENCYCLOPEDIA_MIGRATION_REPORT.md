# Migrační přehled encyklopedie Larpidie

## Změněné soubory původní encyklopedie

- `index.html` — obsah původního dlouhého článku s neaktuálními tvrzeními byl nahrazen rozcestníkem aplikace. Zachováno menu **Encyklopedie**, ID `view-encyklopedie` a výchozí adresa `#encyklopedie`.
- `site.js` — doplněno směrování pro `#encyklopedie/kategorie/článek`; původní obecná adresa i ostatní části webu zůstávají zachované.
- `site.css` — přidány styly pro kategorie, články, vyhledávání, obsah článku a mobilní zobrazení.
- `larpidia-encyklopedie.md` — starý samostatný text byl nahrazen krátkým odkazem na živou encyklopedii, aby vedle webu nezůstala druhá, rozporná kopie.
- V hlavním přehledu webu byly opraveny zastaralé rychlé údaje o populaci, rozloze a parlamentu. Přehled železnic nyní rozlišuje provozní městskou L3 od jejího nedokončeného podmořského pokračování.

## Nové soubory

- `encyclopedia.js` — vykreslování z obsahového katalogu, čtení Markdownu, centrální fakta, výpočty a vyhledávání.
- `content/larpidia/index.json` — devět kategorií a jejich články.
- `content/larpidia/facts.json` — centrální opakované parametry a definice odvozených modelových částek.
- `content/larpidia/media/assets.json` — registr existujících map a fotografických podkladů.
- 39 tematických Markdown článků v `content/larpidia/`.
- `CANON_EDITING_GUIDE.md` — postup pro úpravy textů, faktů, stránek a médií.
- `scripts/validate_encyclopedia.mjs` — obsahový validátor.
- `scripts/check_encyclopedia_runtime.mjs` — běhová kontrola změny centrální daně, navázaných výpočtů a vnořených URL. Test mění jen kopii načtených JSON dat.
- `scripts/check_encyclopedia_http.mjs` — smoke kontrola statického HTTP servírování všech článků a mediálních cest.
- `scripts/serve_static.mjs` — jednoduchý místní webový server bez balíčkovacího systému.

## Opakovaná čísla a závislé výpočty

Populace, rozlohy, sazby, hlasovací hranice, pracovní režim, důchod, mzda, ekonomické scénáře a stav železničních úseků jsou uloženy v `content/larpidia/facts.json`. Články je zobrazují zástupnými značkami, ne vlastními nezávislými kopiemi. Změna vstupu ovlivní všechny jeho odkazy při načtení. Turistický obrat, převod zisku podniků, stabilizační fond, maximální penzijní scénář a částečná potřeba financování se přepočítávají z centrálních vstupů. Články výslovně označují propočty jako modelové a částečné.

## Nalezené zastaralé rozpory

- Původní `index.html` i `larpidia-encyklopedie.md` tvrdily, že země má parlament, poslance nebo parlamentní volby. Aktuální kánon stanoví čtyři rovnocenné spoluvládce a žádný parlament.
- Starý veřejný text zaměňoval plánované či zakreslené spojení L3 za hotový podmořský tunel. Aktuální stav je: městská L3 funguje, podmořský úsek se dokončuje, mezi ostrovy jezdí lodě a trajekty.
- Hlavní stránka uváděla dřívější rozsah populace a rozlohy místo hodnot **32 000**, **175 km²** a **14 km²**.
- `data/larpidia_world_bible.json` obsahuje starší stav návrhů a příznak parlamentu. Kánon v2.6 jej výslovně přebíjí; nebyl přepisován.
- Geografické a starší pracovní podklady obsahují neaktuální názvy či zvažované varianty a v některých místech označují budovu parlamentu. Tyto prvky nebyly převedeny na veřejná fakta.
- Starší historie světové bible kladla znalost královského původu čtveřice příliš brzy. Veřejný text nyní zachovává pořadí: odhalující video → policejní zásah → až poté zjištění královského původu.
- Archiv v2.6 obsahuje historické varianty A/B/C a starší úryvky označené jako nerozhodnuté. Do veřejné encyklopedie byly přeneseny pouze aktuálně potvrzené údaje a následná autorova upřesnění; rozhodovací kódy a pracovní poznámky nebyly publikovány.
- U `LAR_PH_001.jpg` záznam metadat stále uvádí `not_generated`, přestože JPG existuje. Proto je použit pouze jako výslovně ilustrační vizuál bez potvrzení přesného místa či výhledu. `LAR_PH_002.jpg` ukazuje konkrétní automobil a nebyl přiřazen článku bez doložené potřeby.

## Detaily, které zůstávají neurčené

Veřejný text nevymýšlí přesný školní týden, název a hranice kampusového města, městské hranice páté funkční zóny, datum otevření podmořské L3, provozní stav celé L1 a L2, bezpečnostní návrh živého elektronického hlasování, přesné lhůty legislativní kanceláře, úplný seznam nezměnitelných práv, detaily mezinárodních dohod, přesné sazební výjimky nebo ceník návštěvnických povolenek. Vlajka, znak i hymna nemají definitivní autorskou podobu a encyklopedie je nevytváří.

Modelové ekonomické údaje nejsou prezentovány jako měřené statistiky. Turistický obrat není příjem státu; zisk státní firmy není jejími tržbami; předběžný rozdíl výdajového scénáře není konečný rozpočtový schodek. Články nepřidávají přesný rozsudek nad Košťálem ani neprokázané tvrzení o podplácení.

## Kontroly

Projekt je statický HTML/CSS/JavaScript a nemá balíčkovací nebo build systém, proto nebyl vytvořen nový build krok. Kontrola dat, existujících cest, Markdown článků, odkazů a placeholderů se provádí příkazem `node scripts/validate_encyclopedia.mjs`; běhová kontrola centrálních změn a výpočtů příkazem `node scripts/check_encyclopedia_runtime.mjs`; statické HTTP cesty ověřuje `node scripts/check_encyclopedia_http.mjs`. Mobilní pravidla jsou definována pro šířky do 720 px. Zkouška screenshotu v headless Edge selhala při inicializaci grafického procesu, takže nebyl uložen vizuální snímek.
