# Zpráva o obrazových médiích a veřejné galerii

Zdrojový manifest: [content/larpidia/media/assets.json](../content/larpidia/media/assets.json). Kontrola ověřila skutečnou existenci souborů, veřejný allowlist, relativní cesty z kořene webu a vykreslení obrázků v Edge. Z 20 plánovaných fotografických scén existují přesně **2** soubory a **18** scén zůstává bez fotografie. Videozáznamy evidovány: **0**.

## Dostupné fotografie ve veřejné galerii

| Manifest ID | Popisek | Zdrojový soubor | Kopírovaná veřejná cesta |
| --- | --- | --- | --- |
| story-photo-01 | Zimní stezka mezi lesnatými svahy a pobřežím. | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_01.png | gallery/assets/mountain.png |
| story-photo-06 | Marina a pobřežní zástavba na Paralandu. | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_06.png | gallery/assets/paraland.png |

Oba soubory jsou PNG; cesty scény PHOTO_01 a PHOTO_06 byly sjednoceny s reálnými příponami. Kořenový test potvrdil, že se oba snímky dekódují a mají nenulové obrazové rozměry. Veřejný render potvrdil jejich zobrazení bez prázdných či rozbitých karet. Fotografie PHOTO_01 je použita také v příslušném článku; galerie ji deduplikuje podle centrálního manifestu.

## Scény bez fotografie

| Scéna | Název | Interní místo | Očekávaný soubor | Interní bod kamery |
| --- | --- | --- | --- | --- |
| PHOTO_02 | Vodopád u horské železnice | N-03 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_02.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_02_WATERFALL_EXPRESS_map.jpg |
| PHOTO_03 | Staré centrum Larpingtonu | CP-SQ04 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_03.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_03_OLD_LARPINGTON_map.jpg |
| PHOTO_04 | Starý přístav Larpingtonu | C-02 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_04.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_04_LARPINGTON_OLD_HARBOUR_map.jpg |
| PHOTO_05 | Ōru Maito po dešti | T-04 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_05.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_05_ORU_MAITO_AFTER_RAIN_map.jpg |
| PHOTO_07 | Zřícenina hradu na Paralandu | PL-06 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_07.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_07_PARALAND_CASTLE_RUINS_map.jpg |
| PHOTO_08 | Noční cesta Jeskem | V-07 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_08.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_08_MIDNIGHT_JESKO_map.jpg |
| PHOTO_09 | Odpočinek na vrcholu při zlaté hodince | SP-05 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_09.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_09_GOLDEN_HOUR_SUMMIT_REST_map.jpg |
| PHOTO_10 | Horská louka | M-03 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_10.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_10_SWISS_INSPIRED_MOUNTAIN_MEADOW_map.jpg |
| PHOTO_11 | Horské jezero | N-04 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_11.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_11_ALPINE_INSPIRED_LAKE_POSE_map.jpg |
| PHOTO_12 | Západ slunce nad Larpidií | M-03 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_12.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_12_SUNSET_ABOVE_LARPIDIA_map.jpg |
| PHOTO_13 | Skrytý horský hřeben | N-04 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_13.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_13_THE_HIDDEN_RIDGE_map.jpg |
| PHOTO_14 | Řeka ústící do moře | W-01 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_14.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_14_RIVER_TO_THE_SEA_map.jpg |
| PHOTO_15 | Noční panorama Larpingtonu | HV-01 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_15.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_15_LARPINGTON_ROOFTOP_NIGHT_map.jpg |
| PHOTO_16 | Pobřeží za úvitu | V-04 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_16.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_16_COASTAL_DAWN_HAND_VIEW_map.jpg |
| PHOTO_17 | Hrad za ranního světla | PL-02 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_17.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_17_OLD_MONEY_CASTLE_MORNING_map.jpg |
| PHOTO_18 | Nádvoří starého kostela | CP-B07 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_18.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_18_OLD_MONEY_CHURCH_COURTYARD_map.jpg |
| PHOTO_19 | Terasa s výhledem na moře | PL-03 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_19.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_19_MANOR_TERRACE_SEA_VIEW_map.jpg |
| PHOTO_20 | Historická ulice za zlaté hodinky | CP-B08 | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_20.jpg | v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/02_MAP_PINS/PHOTO_20_HERITAGE_STREET_ELEGANCE_map.jpg |

Chybějící snímky nejsou nahrazené ilustračními kartami. Autorův „Obrazový archiv“ v kořenovém náhledu počítá soubory dynamicky a zobrazuje stav **2 hotových / 18 chybějících**; [snímek archivu](debug-screenshots/author-media-modal.png). Veřejný export tlačítko ani plán scén neobsahuje a interní cesty k promptům vracejí 404.

Obecná ilustrace 'photo-001' a noční silniční ilustrace nejsou vydávány za místní fotografie a jsou vyřazeny z veřejné galerie. Veřejná příroda odkazuje na ověřenou fotografii PHOTO_01, nikoli na nesouvisející snímek.

## Kmenový soubor promptů

Úplný interní registr promptů zůstává v [ALL_PHOTO_PROMPTS.md](../v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/03_PHOTO_PROMPTS/ALL_PHOTO_PROMPTS.md). Obsahuje 20 stabilních ID, polohu v atlasu, samostatný bod kamery, prompt a stav dostupnosti. Původní dlouhé prompty zachovány; veřejný export je nepublikuje.
