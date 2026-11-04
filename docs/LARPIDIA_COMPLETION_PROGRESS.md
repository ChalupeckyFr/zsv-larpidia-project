# Stav dokončení atlasu a galerie Larpidie

Aktualizováno: 2026-11-04. Postup obnovuje již hotové změny a zachovává práci z předchozího běhu.

## Fáze podle zadání

| Fáze | Stav | Důkaz |
|---|---|---|
| 1. Skutečný zdroj, trasy, zachování dřívější opravy a redakční zdroj popisů | COMPLETE AND TESTED | Kořenový web otevřel aktivní iframe '/atlas/current/viewer/atlas.html'; staré značky a statusy nejsou v zobrazeném DOM. T-02 je přesně Cimprlichovo Hradiště a starší pravopis zůstává aliasem. |
| 2. Obsah a pojmenování 159 + 662 prvků | COMPLETE AND TESTED | 159/159 a 662/662 záznamů; 0 prázdných či krátkých popisů, 0 obecných názvů a 0 duplicitních veřejných názvů. Ověřeno 21 + 21 karet v kořenovém prohlížeči; úplný rejstřík v 'LARPIDIA_EDITORIAL_PLACE_NAMES_REVIEW.md'. |
| 3. Atlasové rozhraní a 2D kartografie | COMPLETE AND TESTED | Vyhledávání, výběr z výsledků, opakované kliknutí do mapy a dotyk T-02 přes kořenový web; mobilní rozvržení a interakce v Edge. Snímky před/po jsou v 'docs/debug-screenshots/atlas-2d-city-before.png' a 'atlas-2d-city-after.png'. |
| 4. Galerie, archiv médií a branding | COMPLETE AND TESTED | Dvě skutečné fotografie vykreslené s obrazovými rozměry; 18 chybějících scén se nevydává za fotografie. Soukromý archiv počítá 2/18 a ve veřejném exportu i jeho datech chybí. Hlavička a patička mají shodnou výšku loga 48 px. |
| 5. Kontroly, odolnost exportu a zprávy | COMPLETE AND TESTED | Root/Edge prohlížečové testy, allowlist a 404 test, parsování skriptů a 'git diff --check' úspěšné; 3D datové hashe a cesty SVG ověřeny. Výsledky a omezení jsou rozepsané v této zprávě a třech doplňkových zprávách. |

## Skutečně provedené kontroly

- Kořenový 'index.html' přes lokální HTTP server ekvivalentní Live Serveru; naposledy 'http://127.0.0.1:62489/index.html#atlas'. Přes homepage otevřen aktivní atlas, vybrán T-02, ověřeny karta, vyhledávací alias, statusy v DOM, opakovaný klik myší, dotyk, galerijní obrázky, soukromý archiv a logo. Server se po testu ukončil.
- Veřejný export v Edge přes dočasný HTTP server; test otevřel atlas, plán Larpingtonu, galerii a článek standardní navigací. Ověřil 662 objektů, kliknutí na SVG objekt, mobilní rozložení, fotografie bez chyby a skrytí interních cest.
- 'node scripts/check_public_export.mjs': allowlist, datové počty, syntaxi a shodu zdrojového a veřejného vieweru.
- 'node scripts/check_encyclopedia_http.mjs': 72 veřejných cest dostupných, 17 interních cest 404.
- 'node --check' pro upravené skripty a 'git diff --check' bez chyb.
- Cesty 'd' atlasového SVG: 361/361 shodných s výchozím stavem. Cesty 'd' plánu: 5 954/5 954 shodných. Zdrojové registry zachovaly shodný JSON obsah; žádné souřadnice nebyly upraveny.

## Přesný seznam pracovního stromu

Následující seznam je výstupem 'git status --short --untracked-files=all' při tvorbě této zprávy. Obsahuje i necommitnutou práci převzatou z přerušeného běhu; status '??' proto nemusí znamenat, že daný soubor vznikl při tomto navázání.

| Git | Soubor |
| --- | --- |
| M | atlas/current/capital/capital_plan_viewer.html |
| M | atlas/current/viewer/atlas.html |
| M | content/larpidia/geografie/priroda.md |
| M | content/larpidia/media/assets.json |
| M | index.html |
| M | public/atlas/current/capital/capital-3d.html |
| M | public/atlas/current/capital/capital_plan_viewer.html |
| M | public/atlas/current/capital/cp_objects.public.json |
| M | public/atlas/current/registry/places.public.json |
| M | public/atlas/current/svg/transport_preview_embedded.svg |
| M | public/atlas/current/viewer/atlas.html |
| M | public/atlas/current/viewer/terrain-3d.html |
| D | public/atlas/photography/photos/LAR_PH_001.jpg |
| M | public/content/larpidia/geografie/priroda.md |
| M | public/content/larpidia/media/assets.json |
| M | public/index.html |
| M | public/site.css |
| M | scripts/build_public_site.mjs |
| M | scripts/check_encyclopedia_http.mjs |
| M | scripts/check_public_export.mjs |
| M | site.css |
| M | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/03_PHOTO_PROMPTS/ALL_PHOTO_PROMPTS.md |
| ?? | atlas/current/capital/cp_objects.public.json |
| ?? | atlas/current/registry/places.public.json |
| ?? | content/larpidia/atlas_places_editorial.json |
| ?? | docs/LARPIDIA_3D_TECHNICAL_OPTIONS.md |
| ?? | docs/LARPIDIA_ATLAS_CONTENT_AND_UI_COMPLETION_REPORT.md |
| ?? | docs/LARPIDIA_COMPLETION_PROGRESS.md |
| ?? | docs/LARPIDIA_EDITORIAL_PLACE_NAMES_REVIEW.md |
| ?? | docs/LARPIDIA_MEDIA_MANIFEST_REPORT.md |
| ?? | docs/LARPIDIA_PUBLIC_ATLAS_GALLERY_REPAIR_REPORT.md |
| ?? | docs/LARPIDIA_PUBLIC_UX_SMOKE_TEST.md |
| ?? | docs/LARPIDIA_REMAINING_CONTENT_DECISIONS.md |
| ?? | docs/debug-screenshots/atlas-2d-city-after.png |
| ?? | docs/debug-screenshots/atlas-2d-city-before.png |
| ?? | docs/debug-screenshots/atlas-live-server-fixed.png |
| ?? | docs/debug-screenshots/atlas-root-live-cimprlichovo.png |
| ?? | docs/debug-screenshots/atlas-root-live-larpington.png |
| ?? | docs/debug-screenshots/atlas-root-live-poi-detail.png |
| ?? | docs/debug-screenshots/atlas-root-live-praha.png |
| ?? | docs/debug-screenshots/atlas-root-live-railway-rich-card.png |
| ?? | docs/debug-screenshots/author-media-modal.png |
| ?? | docs/debug-screenshots/capital-root-live-museum.png |
| ?? | docs/debug-screenshots/footer-logo.png |
| ?? | docs/debug-screenshots/gallery-live-mobile.png |
| ?? | gallery.js |
| ?? | public/gallery.js |
| ?? | public/site-brand.css |
| ?? | public/site-brand.js |
| ?? | references/LARPIDIA_CODEX_COMPLETION_ATLAS_GALLERY_NAMING_EN_v2.md |
| ?? | references/LARPIDIA_CODEX_PUBLIC_ATLAS_GALLERY_FIX_EN.md |
| ?? | scripts/check_live_root_atlas.mjs |
| ?? | scripts/check_public_render.mjs |
| ?? | scripts/dev_media_status.js |
| ?? | scripts/generate_completion_reports.mjs |
| ?? | scripts/public_viewer_renderers.mjs |
| ?? | scripts/refine_atlas_editorial.mjs |
| ?? | scripts/seed_atlas_editorial.mjs |
| ?? | site-brand.css |
| ?? | site-brand.js |
| ?? | templates/atlas_viewer_template.html |
| ?? | templates/capital_plan_viewer_template.html |

Soubor 'references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md' nebyl upraven. Nebyl proveden Git commit ani push.

## Zbývající omezení

- 18 plánovaných fotografií zatím nemá soubor; jejich přesný seznam je v 'LARPIDIA_MEDIA_MANIFEST_REPORT.md'. Galerie zobrazuje všechny aktuálně dostupné skutečné fotografie a nevkládá prázdné náhražky.
- 591 názvů je redakční návrh podle typu prvku, regionu, sousedů a uliční geometrie. Jsou dohledatelné v interním přehledu a zůstávají oddělené od kanonických rozhodnutí.
- Testy používají skutečný kořen projektu přes lokální server a Edge, nikoli živou instanci rozšíření VS Code Live Server. Kořen, relativní cesty a navigační tok jsou stejné.
