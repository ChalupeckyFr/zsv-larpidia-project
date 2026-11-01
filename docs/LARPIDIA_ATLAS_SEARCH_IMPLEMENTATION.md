# Larpidie — implementace veřejného atlasu a vyhledávání

**Datum:** 1. listopadu 2026  
**Zadání:** schválená varianta A8B z `references/LARPIDIA_CODEX_SCHVALENE_OPRAVY_PO_AUDITU_v1.md`, nálezy CS-005 až CS-025 a rozbor `docs/LARPIDIA_ATLAS_SEARCH_REVIEW.md`.

## Hlavní atlas

Aktivní SVG podklad, jeho vrstvy, tvar ostrovů a souřadnice zůstaly zachované. Veřejný atlas zobrazuje všech **159 míst**. Návštěvnické záznamy se při buildu vytvářejí z aktivního `places.json` do samostatného `places.public.json`; obsahují pouze ID, bezpečný název, typ, ostrov, oblast a souřadnice. Neobsahují redakční poznámky, foto vodítka, Bible/ref ani stavová pole.

Vyhledávání nabízí:

- volný dotaz a filtry podle ostrova a typu místa;
- hledání bez rozlišení diakritiky, rozdělení dotazu na slova a řazení přesných shod před obecnými;
- karty s názvem, druhem, ostrovem/oblastí a ID, spolu s živým počtem výsledků a prázdným stavem;
- ovládání šipkami nahoru/dolů, Enterem a Escape; výsledky jsou tlačítka v přístupném seznamu;
- kliknutí, které vycentruje a přiblíží SVG, zvýrazní záznam a otevře jeho bezpečný detail;
- na úzkých displejích vysouvací panel hledání s tlačítkem otevření a zavření; respektuje `prefers-reduced-motion`.

Ovládání mapy a tematické vrstvy zůstaly funkční. Workflow legenda a přepínač stavů byly nahrazeny věcnými názvy vrstev. Schematická přesnost se vysvětluje jednou v legendě.

## Plán Larpingtonu a 3D zobrazení

Plán ponechává všech **662 objektů**, původní geometrii i měřítko. Vložená kopie registru je synchronizována s `cp_objects.json` skriptem `scripts/sync_capital_registry.mjs`; build současně odmítne rozdílné kopie. U čtyř dříve rozcházejících se záznamů se souřadnice `u/v` shodovaly a zůstaly zachované.

Veřejné městské záznamy používají obecný typový název nebo schválený název. Značky `photo_guide`, `Bible`, statusy, interní poznámky a návrhová jména nejsou součástí `cp_objects.public.json`. CP-B01 a ST-S odpovídají aktuálnímu kánonu. Městské vrstvy a vyhledávání podle typu mají návštěvnické popisky.

3D stránky zachovávají data terénu a městské geometrie. Odstranily se jen nesprávné veřejné štítky, nepodložená populace Larpingtonu a redakční popisy. Rozlišení stávající a plánované zástavby zůstává zřetelné.

## Veřejný build a verze

`scripts/build_public_site.mjs` vytváří přesný allowlist ve složce `public/`. Kopíruje aktivní stránku, 39 článků, centrální fakta, potřebná SVG/3D data a registrovaná média. Nepřenáší `references/`, `docs/`, `data/`, `scripts/`, `templates/`, starší verze atlasu ani `v1.1/` s interními prompty.

`scripts/serve_static.mjs` servíruje pouze výstup `public/`, bezpečně omezuje cesty na tento adresář a přijímá pouze GET/HEAD. Lokální smoke test ověřuje veřejné cesty i 404 pro interní dokumenty, Bible, pracovní registry a prompt pack.

Jeden zdroj `project-metadata.json` poskytuje verze do diskrétních společných patiček. Hlavní web uvádí verzi podle README; atlas a plán používají verzi vydání `1.0.1-capital-detail`. 3D modelům bez samostatné stabilní verze se číslo nepřidává.

## Ověření

Prošly `node scripts/validate_encyclopedia.mjs`, `node scripts/check_encyclopedia_runtime.mjs`, `node scripts/check_public_export.mjs` a `node scripts/check_encyclopedia_http.mjs`. Exportní kontrola potvrzuje 72 povolených souborů, 159 míst, 662 městských objektů a syntaxi všech veřejných skriptů; HTTP kontrola vrátila 200 pro 79 veřejných cest a 404 pro 9 interních cest.

`python atlas/scripts/check_atlas.py` se nepodařilo dokončit, protože prostředí nemá modul `numpy`. Závislost nebyla instalována. Vizuální screenshot v dostupném prostředí nebyl pořízen; responzivní chování je ověřené ve zdrojovém CSS a skripty/registrům prošly automatické kontroly. V projektu nebylo nalezeno nastavení produkčního hostingu, takže stav externího nasazení nebylo možné ověřit.
