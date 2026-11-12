# 20 finálních anglických promptů (samostatné soubory jsou v téže složce)

Každý prompt je samostatný blok k vložení do generátoru obrázků. Stav: prompt-ready.

## Interní vazba na mediální manifest

Soubor `content/larpidia/media/assets.json` je společný registr článkových médií, fotografií i plánovaných scén. Následující stabilní ID odpovídají položkám `scenes[].manifest_id`; pouze scény s dostupným ověřeným souborem jsou zařazeny do veřejné galerie.

| Scéna | Stabilní ID | Lokalita v atlasu | Fotografie | Pohled kamery | Prompt | Stav |
|---|---|---|---|---|---|---|
| PHOTO_01 · Zimní hory nad Tichým oceánem | `story-photo-01` | `M-01` · Larpova hora | [PHOTO_01.png](../01_PHOTOS/PHOTO_01.png) | [mapový bod](../02_MAP_PINS/PHOTO_01_SNOW_ABOVE_THE_PACIFIC_map.jpg) | [prompt](PHOTO_01_SNOW_ABOVE_THE_PACIFIC_prompt.txt) | ověřená fotografie |
| PHOTO_02 · Vodopád u horské železnice | `story-photo-02` | `N-03` · Vodopád na horském toku | chybí: `PHOTO_02.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_02_WATERFALL_EXPRESS_map.jpg) | [prompt](PHOTO_02_WATERFALL_EXPRESS_prompt.txt) | fotografie chybí |
| PHOTO_03 · Staré centrum Larpingtonu | `story-photo-03` | `CP-SQ04` · Kostelní náměstí | chybí: `PHOTO_03.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_03_OLD_LARPINGTON_map.jpg) | [prompt](PHOTO_03_OLD_LARPINGTON_prompt.txt) | fotografie chybí |
| PHOTO_04 · Starý přístav Larpingtonu | `story-photo-04` | `C-02` · Historický přístav Larpingtonu | chybí: `PHOTO_04.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_04_LARPINGTON_OLD_HARBOUR_map.jpg) | [prompt](PHOTO_04_LARPINGTON_OLD_HARBOUR_prompt.txt) | fotografie chybí |
| PHOTO_05 · Ōru Maito po dešti | `story-photo-05` | `T-04` · Ōru Maito | chybí: `PHOTO_05.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_05_ORU_MAITO_AFTER_RAIN_map.jpg) | [prompt](PHOTO_05_ORU_MAITO_AFTER_RAIN_prompt.txt) | fotografie chybí |
| PHOTO_06 · Marina na Paralandu | `story-photo-06` | `H-02` · Marina Paraland | [PHOTO_06.png](../01_PHOTOS/PHOTO_06.png) | [mapový bod](../02_MAP_PINS/PHOTO_06_PARALAND_MARINA_map.jpg) | [prompt](PHOTO_06_PARALAND_MARINA_prompt.txt) | ověřená fotografie |
| PHOTO_07 · Zřícenina hradu na Paralandu | `story-photo-07` | `PL-06` · Zřícenina na Paralandu | chybí: `PHOTO_07.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_07_PARALAND_CASTLE_RUINS_map.jpg) | [prompt](PHOTO_07_PARALAND_CASTLE_RUINS_prompt.txt) | fotografie chybí |
| PHOTO_08 · Noční cesta Jeskem | `story-photo-08` | `V-07` · Vyhlídka na hrázi přehrady | chybí: `PHOTO_08.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_08_MIDNIGHT_JESKO_map.jpg) | [prompt](PHOTO_08_MIDNIGHT_JESKO_prompt.txt) | fotografie chybí |
| PHOTO_09 · Odpočinek na vrcholu při zlaté hodince | `story-photo-09` | `SP-05` · Studánka na hřebenovce | chybí: `PHOTO_09.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_09_GOLDEN_HOUR_SUMMIT_REST_map.jpg) | [prompt](PHOTO_09_GOLDEN_HOUR_SUMMIT_REST_prompt.txt) | fotografie chybí |
| PHOTO_10 · Horská louka | `story-photo-10` | `M-03` · Kulatý vrch | chybí: `PHOTO_10.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_10_SWISS_INSPIRED_MOUNTAIN_MEADOW_map.jpg) | [prompt](PHOTO_10_SWISS_INSPIRED_MOUNTAIN_MEADOW_prompt.txt) | fotografie chybí |
| PHOTO_11 · Horské jezero | `story-photo-11` | `N-04` · Přehradní jezero | chybí: `PHOTO_11.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_11_ALPINE_INSPIRED_LAKE_POSE_map.jpg) | [prompt](PHOTO_11_ALPINE_INSPIRED_LAKE_POSE_prompt.txt) | fotografie chybí |
| PHOTO_12 · Západ slunce nad Larpidií | `story-photo-12` | `M-03` · Kulatý vrch | chybí: `PHOTO_12.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_12_SUNSET_ABOVE_LARPIDIA_map.jpg) | [prompt](PHOTO_12_SUNSET_ABOVE_LARPIDIA_prompt.txt) | fotografie chybí |
| PHOTO_13 · Skrytý horský hřeben | `story-photo-13` | `N-04` · Přehradní jezero | chybí: `PHOTO_13.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_13_THE_HIDDEN_RIDGE_map.jpg) | [prompt](PHOTO_13_THE_HIDDEN_RIDGE_prompt.txt) | fotografie chybí |
| PHOTO_14 · Řeka ústící do moře | `story-photo-14` | `W-01` · Řeka Larp | chybí: `PHOTO_14.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_14_RIVER_TO_THE_SEA_map.jpg) | [prompt](PHOTO_14_RIVER_TO_THE_SEA_prompt.txt) | fotografie chybí |
| PHOTO_15 · Noční panorama Larpingtonu | `story-photo-15` | `HV-01` · Prémiový hotel – přístavní promenáda | chybí: `PHOTO_15.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_15_LARPINGTON_ROOFTOP_NIGHT_map.jpg) | [prompt](PHOTO_15_LARPINGTON_ROOFTOP_NIGHT_prompt.txt) | fotografie chybí |
| PHOTO_16 · Pobřeží za úvitu | `story-photo-16` | `V-04` · Vyhlídka na hrotu poloostrova | chybí: `PHOTO_16.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_16_COASTAL_DAWN_HAND_VIEW_map.jpg) | [prompt](PHOTO_16_COASTAL_DAWN_HAND_VIEW_prompt.txt) | fotografie chybí |
| PHOTO_17 · Hrad za ranního světla | `story-photo-17` | `PL-02` · Hrad Paralandu | chybí: `PHOTO_17.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_17_OLD_MONEY_CASTLE_MORNING_map.jpg) | [prompt](PHOTO_17_OLD_MONEY_CASTLE_MORNING_prompt.txt) | fotografie chybí |
| PHOTO_18 · Nádvoří starého kostela | `story-photo-18` | `CP-B07` · Historický kostel na Kostelním náměstí | chybí: `PHOTO_18.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_18_OLD_MONEY_CHURCH_COURTYARD_map.jpg) | [prompt](PHOTO_18_OLD_MONEY_CHURCH_COURTYARD_prompt.txt) | fotografie chybí |
| PHOTO_19 · Terasa s výhledem na moře | `story-photo-19` | `PL-03` · Jižní letovisko Paralandu | chybí: `PHOTO_19.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_19_MANOR_TERRACE_SEA_VIEW_map.jpg) | [prompt](PHOTO_19_MANOR_TERRACE_SEA_VIEW_prompt.txt) | fotografie chybí |
| PHOTO_20 · Historická ulice za zlaté hodinky | `story-photo-20` | `CP-B08` · Tržní hala | chybí: `PHOTO_20.jpg` | [mapový bod](../02_MAP_PINS/PHOTO_20_HERITAGE_STREET_ELEGANCE_map.jpg) | [prompt](PHOTO_20_HERITAGE_STREET_ELEGANCE_prompt.txt) | fotografie chybí |

Mapový náhled každé scény vede na evidovaný bod kamery; prompt zachovává směr záběru, viditelné orientační body, roční dobu a prostorové měřítko podle podkladů. Soubory mapových bodů a pracovní souřadnice jsou neveřejné produkční podklady. Fotografie se považuje za hotovou jen tehdy, když existuje soubor na ověřené cestě v manifestu.

Mapové náhledy scén jsou rovněž evidované v `viewpoint_path`. Jejich zdrojové obrázky obsahují pracovní ID, navržené body kamery a interní souřadnice, proto se do veřejné galerie nekopírují. Revize realismu: prompty PHOTO 03, 04, 06–11, 13 a 16–20 jsou přepsané tak, aby výsledek vypadal co nejvíce jako skutečná neupravená fotka z iPhonu; PHOTO 07 a 11 jsou nově bez lidí. Prompty PHOTO 01, 02, 05, 12, 14 a 15 zůstávají beze změny.

- [PHOTO 01 · SNOW ABOVE THE PACIFIC](#photo_01) (9:16; M-01)
- [PHOTO 02 · WATERFALL EXPRESS](#photo_02) (16:9; N-03, ST-L1-03)
- [PHOTO 03 · OLD LARPINGTON](#photo_03) (16:9; CP-SQ04)
- [PHOTO 04 · LARPINGTON OLD HARBOUR](#photo_04) (16:9; C-02)
- [PHOTO 05 · ŌRU MAITO AFTER RAIN](#photo_05) (9:16; T-04)
- [PHOTO 06 · PARALAND MARINA](#photo_06) (16:9; H-02, PL-05)
- [PHOTO 07 · PARALAND CASTLE RUINS](#photo_07) (9:16; PL-06)
- [PHOTO 08 · MIDNIGHT JESKO](#photo_08) (9:16; V-07, C-01)
- [PHOTO 09 · GOLDEN HOUR SUMMIT REST](#photo_09) (9:16; SP-05, M-01)
- [PHOTO 10 · SWISS-INSPIRED MOUNTAIN MEADOW](#photo_10) (9:16; M-03, SP-04)
- [PHOTO 11 · ALPINE-INSPIRED LAKE POSE](#photo_11) (9:16; N-04, ST-L1-02)
- [PHOTO 12 · SUNSET ABOVE LARPIDIA](#photo_12) (16:9; M-03, PG-01)
- [PHOTO 13 · THE HIDDEN RIDGE](#photo_13) (9:16; N-04)
- [PHOTO 14 · RIVER TO THE SEA](#photo_14) (16:9; W-01)
- [PHOTO 15 · LARPINGTON ROOFTOP NIGHT](#photo_15) (9:16; HV-01, CP-B07)
- [PHOTO 16 · COASTAL DAWN HAND VIEW](#photo_16) (9:16; V-04)
- [PHOTO 17 · OLD MONEY CASTLE MORNING](#photo_17) (16:9; PL-02)
- [PHOTO 18 · OLD MONEY CHURCH COURTYARD](#photo_18) (9:16; CP-B07)
- [PHOTO 19 · MANOR TERRACE SEA VIEW](#photo_19) (9:16; PL-03)
- [PHOTO 20 · HERITAGE STREET ELEGANCE](#photo_20) (16:9; CP-B08, CP-SQ03)

<a id="photo_01"></a>
## PHOTO 01 · SNOW ABOVE THE PACIFIC (9:16)

**Lokalita:** M-01 · **Kamera:** PROPOSED CAMERA POINT x 6.850, y 5.450 km

```
Scene name (for reference only, never to be written in the image): SNOW ABOVE THE PACIFIC. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must look like a genuine photo taken by a person on an Apple iPhone 15 (main camera, 1x, realistic smartphone HDR, natural human eye-level perspective, slightly imperfect everyday framing), not CGI, not a 3D render, not an illustration, not an advertising visualisation and not a drone shot.

SCENE: A vertical smartphone photo taken from a hiking trail just below the summit of a low forested coastal mountain on a Pacific island. In the foreground: a narrow dirt-and-gravel path bending to the left, grey weathered rocks and small boulders, flattened dry winter grass, and thin leftover patches of old dirty-white snow melting between the stones (only a few square metres, not a snow field). Below the ridge: steep green forested slopes (evergreen with some bare winter branches), low clouds drifting through the valleys, and far away to the west a calm grey-blue ocean under a hazy horizon.

COMPOSITION: Eye-level and handheld; the trail leads the eye diagonally from the bottom-right toward the distant sea; foreground rocks sharp, mid-slopes slightly soft, far horizon hazy.

LIGHT AND ATMOSPHERE: Cold, slightly dark late-afternoon light under a thin high overcast; soft diffuse shadows, a faint pale glow low in the west, damp air.

PHOTO LOOK: cool, slightly underexposed, lifted contrast, muted desaturated greens, cold blue-grey shadows, no warm tint, fine grain. Subtle authentic imperfections (only a few, not all at once): slightly tilted horizon (about 1°), soft atmospheric haze, a hint of noise in the shadows.

PEOPLE: No people anywhere in the frame: no figures, faces or silhouettes, not even tiny distant ones, and no animals.

PLACE AND SCALE: Fictional island nation Larpidie, south of Japan: a low forested coastal mountain (summit only about 560 m) with occasional short winter snow. It is not an alpine peak: no glaciers, no jagged snow-capped giants.

AVOID: no people, no buildings, no signposts, no deep alpine snowpack, no dramatic sunset colours. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs or lettering, interface overlays, borders or frames. Avoid a CGI or video-game look, oversaturated HDR halos, fake glowing skies, heavy vignette, plastic textures, warped architecture, impossible scale and AI text artefacts.

Aspect ratio 9:16.
```

<a id="photo_02"></a>
## PHOTO 02 · WATERFALL EXPRESS (16:9)

**Lokalita:** N-03, ST-L1-03 · **Kamera:** PROPOSED CAMERA POINT x 10.540, y 8.575 km

```
Scene name (for reference only, never to be written in the image): WATERFALL EXPRESS. Format 16:9.

Create a horizontal 16:9 widescreen smartphone photo. It must look like a genuine photo taken by a person on an Apple iPhone 15 (main camera, 1x, realistic smartphone HDR, natural human eye-level perspective, slightly imperfect everyday framing), not CGI, not a 3D render, not an illustration, not an advertising visualisation and not a drone shot.

SCENE: A tall, slender waterfall (about 40 to 45 m) pours over dark wet rock in a narrow mossy gorge in a temperate mountain forest and drops into a rocky pool; wet boulders covered in bright green moss, ferns, fine mist hanging in the air. At the right edge of the frame, partly hidden by tree trunks, the nose of a small modern electric panoramic tourist train (two short cars, dark green with a cream stripe) glides slowly into a mountain photo-stop, soft, slightly motion-blurred and cropped by the frame edge. The waterfall and forest are the main subject; the train is only a small secondary detail.

COMPOSITION: Wide landscape from a viewing platform at eye level, waterfall slightly left of centre, wet rocks and ferns in the foreground, depth from the foreground ferns into the misty gorge; no platform railing visible.

LIGHT AND ATMOSPHERE: Soft overcast mountain light in the late morning, no direct sun, deep green shadows, mist softly glowing.

PHOTO LOOK: natural saturation, soft contrast, gently lifted shadows, cool-green tint, slow-shutter silky water like an iPhone Live Photo long exposure while the rocks stay sharp. Subtle authentic imperfections (only a few, not all at once): a few droplets on the lens in one corner, slight softness at the frame edges.

PEOPLE: No people anywhere in the frame: no figures, faces or silhouettes, not even tiny distant ones, and no animals.

PLACE AND SCALE: Fictional island Larpidie: low forested mountains (about 130 m above sea level at the falls), temperate-subtropical moss and ferns; an electric heritage mountain tourist railway runs past the falls.

AVOID: no people, no signs with text, no dam, no tropical jungle, no rainbow, no giant waterfall scale. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs or lettering, interface overlays, borders or frames. Avoid a CGI or video-game look, oversaturated HDR halos, fake glowing skies, heavy vignette, plastic textures, warped architecture, impossible scale and AI text artefacts.

Aspect ratio 16:9.
```

<a id="photo_03"></a>
## PHOTO 03 · OLD LARPINGTON (16:9)

**Lokalita:** CP-SQ04 · **Kamera:** PROPOSED CAMERA POINT x 15.956, y 13.671 km

```
Scene name (for reference only, never to be written in the image): OLD LARPINGTON. Format 16:9.

Create a horizontal 16:9 widescreen smartphone photo. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: An early-morning view straight down a quiet old-town street, about 8 m wide, in the historic harbour quarter of a small island capital founded by English and Welsh settlers around 1600. Both sides are lined with terraced two- and three-storey houses of weathered red-brown brick and honey-coloured sandstone: uneven slate and faded terracotta roofs with lichen and moss on the ridges, white-painted timber sash windows with slightly peeling paint, stone sills and lintels, black cast-iron gutters and downpipes with rust streaks, a few front doors painted muted green and navy. Narrow pavements of worn sandstone flags; the carriageway is uneven grey granite setts with darker damp joints and small shallow puddles from a drizzle that has just stopped. Window boxes and hanging baskets with geraniums, hydrangeas and agapanthus; a young lime tree in a cast-iron tree grille. On the right, a tiny corner café, still closed: two folding wooden chairs leaning against a small round table and a rolled-up cream canvas awning with no lettering. About 70 m ahead the street opens onto a square, and on the right above the rooftops rises the short square tower of the old parish church: brick with sandstone corner stones, a weathered stone parapet and a pitched slate roof, softened by morning haze.

CAMERA AND COMPOSITION: Handheld at standing eye level in the middle of the street, looking west along its axis. One-point perspective, slightly off-centre to the left; the houses converge naturally toward the square; the church tower sits in the upper right part of the frame, small but clearly readable at about 70 m. No cars.

LIGHT AND WEATHER: Early summer, about 30 minutes after sunrise, right after a light drizzle. The low sun is behind the camera, over the photographer's right shoulder, filtered by thin haze: it lights the east face of the church tower and catches a few chimneys and upper windows, while the street itself is still in cool blue shade. The wet setts reflect the pale sky; damp air with slight haze in the distance.

REALISM DETAILS: Lived-in details: slightly uneven roof and window lines, repaired brickwork with mismatched bricks, a cast-iron drain grate, a few fallen lime leaves stuck to the wet setts, a closed wheelie bin tucked into a side passage, a bicycle leaning against a railing, cracks and small weeds in the pavement joints, condensation on a ground-floor window.

PHOTO PROCESSING: Standard iPhone Smart HDR processing: restrained natural contrast, slightly cool shadows and warm sunlit stone, believable dynamic range (the bright sky above the roofs may clip slightly), fine luminance noise on the shaded side, no filter, no added grain or vignette; a tiny natural lean in the vertical lines from the wide lens.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Old Larpington, the historic core of the fictional island capital of Larpidie in the north-west Pacific, south of Japan: a British-built harbour town that looks comparable to the old towns of Cornwall or the Channel Islands, with mossy brick and stone, gardens, churches and market squares; houses of two to three storeys, narrow streets, nothing taller than the church tower.

AVOID: no people, no cars, no modern shop signs or neon, no satellite dishes, no skyscrapers, no Mediterranean, Japanese or theme-park architecture, no spotless surfaces. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 16:9.
```

<a id="photo_04"></a>
## PHOTO 04 · LARPINGTON OLD HARBOUR (16:9)

**Lokalita:** C-02 · **Kamera:** PROPOSED CAMERA POINT x 16.235, y 13.900 km

```
Scene name (for reference only, never to be written in the image): LARPINGTON OLD HARBOUR. Format 16:9.

Create a horizontal 16:9 widescreen smartphone photo. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: The historic inner harbour of a small island capital on a late-summer afternoon. A wide promenade of worn cream sandstone slabs runs along a granite quay wall. On the left, a continuous row of old brick-and-stone harbour warehouses and a dignified two-storey customs house of pale stone, now cafés and small shops: tall round-arched ground-floor openings with dark green timber frames, black-painted iron canopies, hanging lanterns, folded parasols and stacked bistro chairs, no readable signage. On the right, the calm green-grey harbour basin with about a dozen small boats: wooden and fibreglass fishing boats with blue and white hulls and two small white sailing dinghies, old tyres used as fenders, mooring ropes running to cast-iron bollards. Ahead, the promenade leads to a short stone pier and a low ferry terminal building; beyond the basin lies the long dark line of a granite breakwater with a small white harbour light at its end, and the open bay hazy behind it. Behind the warehouses, terracotta and slate roofs of the old town climb gently, with one slender church spire.

CAMERA AND COMPOSITION: Handheld at eye level near the quay edge, looking east-north-east along the promenade. The quay edge forms a strong leading line from the lower right corner; the warehouses fill the left third, the water the right third; the pier, ferry terminal and breakwater are small in the distance near the centre.

LIGHT AND WEATHER: Late summer, about 3:30 in the afternoon, clear sky with light haze over the bay. The sun is behind the photographer, so the facades are evenly front-lit in warm light and the short shadows of bollards and lamp posts point away from the camera; the water has small ripples with soft reflections of the boats.

REALISM DETAILS: Salt stains and a band of green algae along the waterline of the quay wall, rusty iron mooring rings set into the stone, coiled ropes, a few lobster pots and a stack of weathered plastic fish crates, bird droppings on a bollard, slightly uneven paving, an orange life ring on a post (no lettering), patched render on one warehouse, a little floating seaweed.

PHOTO PROCESSING: Standard iPhone Smart HDR: natural and slightly warm, true-to-life teal-green water, moderate contrast, a believable pale-blue hazy sky (not artificially deep blue), no filter; slight chromatic fringing on high-contrast edges near the frame corners.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Larpington Old Harbour, fictional: the historic harbour of the capital of Larpidie (north-west Pacific, south of Japan), protected by two stone breakwaters against southern typhoon swell; a basin for small boats and a promenade with cafés and small shops in English-style brick and stone. The large cargo port is elsewhere and not in view.

AVOID: no people, no large ships, no cranes, containers or industrial port, no superyachts, no readable boat names or signs, no tropical palm-beach look. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 16:9.
```

<a id="photo_05"></a>
## PHOTO 05 · ŌRU MAITO AFTER RAIN (9:16)

**Lokalita:** T-04 · **Kamera:** PROPOSED CAMERA POINT x 13.552, y 3.970 km

```
Scene name (for reference only, never to be written in the image): ŌRU MAITO AFTER RAIN. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must look like a genuine photo taken by a person on an Apple iPhone 15 (main camera, 1x, realistic smartphone HDR, natural human eye-level perspective, slightly imperfect everyday framing), not CGI, not a 3D render, not an illustration, not an advertising visualisation and not a drone shot.

SCENE: A narrow evening street in a small Japanese-influenced town on a Pacific island, just after rain: wet asphalt reflecting warm shop lights and paper lanterns, small family restaurants with fabric noren curtains (blank, no lettering) and wooden sliding doors, a narrow pavement, overhead utility wires, a vending machine glowing softly (no logos), a compact Japanese hatchback parked at the kerb (generic design, no badge, no readable plate), puddles with reflections. The buildings mix compact Japanese shopfronts with a few older brick-and-stone houses with moss, a sign of the island's mixed English-Japanese heritage. A blue-hour sky fades above the rooftops.

COMPOSITION: Vertical, handheld at eye level, a slightly off-centre perspective down the street with the wet road filling the lower third and reflecting the lights; the parked car in the right foreground.

LIGHT AND ATMOSPHERE: Blue hour: last cool daylight overhead, warm amber shop and lantern light below, reflections on every wet surface.

PHOTO LOOK: cinematic but phone-realistic: deeper contrast, teal-and-amber balance, lifted blacks, visible fine noise, slight underexposure. Subtle authentic imperfections (only a few, not all at once): slight motion blur on distant lights, a small lens flare from a lantern.

PEOPLE: No people anywhere in the frame: no figures, faces or silhouettes, not even tiny distant ones, and no animals.

PLACE AND SCALE: Ōru Maito, fictional northern town of Larpidie with a Japanese minority and Japanese-style narrow streets, next to older English-style brick houses; small harbour town atmosphere.

AVOID: no people, no readable text or kanji signs, no neon cyberpunk look, no brand logos. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs or lettering, interface overlays, borders or frames. Avoid a CGI or video-game look, oversaturated HDR halos, fake glowing skies, heavy vignette, plastic textures, warped architecture, impossible scale and AI text artefacts.

Aspect ratio 9:16.
```

<a id="photo_06"></a>
## PHOTO 06 · PARALAND MARINA (16:9)

**Lokalita:** H-02, PL-05 · **Kamera:** PROPOSED CAMERA POINT x 23.255, y 15.742 km

```
Scene name (for reference only, never to be written in the image): PARALAND MARINA. Format 16:9.

Create a horizontal 16:9 widescreen smartphone photo. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: A small leisure marina on a quiet resort island in midsummer, seen from the outer end of the middle of three wooden pontoons. About fifteen modest boats are moored on both sides: small white sailing yachts of 7 to 10 m with furled sails and blue sail covers, a few open motor boats and wooden day boats, fenders squeezed against the pontoon, mooring lines slack on the cleats. The water is clear and calm: turquoise over a pale sandy bottom with patches of dark seagrass. Toward the shore, a low promenade of stone and timber with a row of whitewashed and soft pastel two-storey houses with terracotta roofs, a small single-storey ferry terminal with a canopy at one end, restaurant terraces with empty tables and closed cream parasols, potted oleanders. A short breakwater of rough grey boulders closes the marina on the left. Behind the village rise low, rounded green hills with scrub and pines, and on a hill slightly right of centre, about 1.4 km away, stands a small pale stone castle, softened by haze.

CAMERA AND COMPOSITION: Handheld at standing height on the pontoon, looking east-north-east back toward the shore. The converging pontoon boards and cleats lead from the bottom edge to the promenade; boats frame both sides; the village and hills are layered behind, the castle small and slightly right of centre.

LIGHT AND WEATHER: Bright midsummer midday: high sun from the right, short hard shadows, sparkling highlights on the water, a few small cumulus clouds over the hills, light haze softening the hills.

REALISM DETAILS: Weathered silver-grey pontoon boards with nail heads and salt stains, a water-and-power pedestal on the pontoon with a coiled hose, frayed rope ends, algae on the pontoon floats, small scuffs and waterline stains on the hulls, uneven pastel paint with damp patches at the base of the houses, a few floating leaves.

PHOTO PROCESSING: Bright natural iPhone HDR: clean whites without halos, realistic turquoise water (not neon), slightly lifted shadows, no filter; a little specular glare on the water and a mild flare from the brightest reflections.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Paraland, a small fictional resort island of Larpidie in the north-west Pacific: a leisure marina with three pontoons and two breakwaters, a harbour village of low houses and a small terminal for the passenger boat to the capital; a small castle stands on a hill about 1.4 km to the east. Everything is small-scale and quiet.

AVOID: no people, no superyachts or cruise ships, no high-rise hotels, no readable boat names or signs, no Caribbean palm-lined resort look, no neon-turquoise water. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 16:9.
```

<a id="photo_07"></a>
## PHOTO 07 · PARALAND CASTLE RUINS (9:16)

**Lokalita:** PL-06 · **Kamera:** PROPOSED CAMERA POINT x 26.250, y 16.720 km

```
Scene name (for reference only, never to be written in the image): PARALAND CASTLE RUINS. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: An empty heritage footpath through low pine and scrub woodland opens onto a grassy hilltop, with an old ruined stone castle about 160 m ahead. The ruin: the lower two thirds of a round keep built of rough grey-brown local stone and lime mortar, its top broken off unevenly; fragments of curtain walls 3 to 6 m high with empty arched window openings and a collapsed gateway; ivy and moss on the shaded faces, small ferns and wallflowers growing from the joints, a few fallen blocks lying in the grass. In the foreground: a narrow path of compacted gravel and exposed bedrock edged with loose stones, worn in the middle, crossed by pine roots; long fresh spring grass with small white and yellow wildflowers (daisies, buttercups); a few wind-bent pines on both sides. To the right of the ruin, a thin strip of grey-blue sea is visible on the horizon between the trees.

CAMERA AND COMPOSITION: Handheld at standing eye level on the path, looking east. Portrait; the path enters from the bottom edge and leads up toward the ruin; the keep stands in the upper middle right of the frame, the pines frame both sides, a patch of bright grey sky above.

LIGHT AND WEATHER: Spring midday under a bright, high overcast with a thinner, brighter patch in the clouds: soft, even light with faint shadows, the stone matte and slightly damp; a quiet, slightly melancholic mood.

REALISM DETAILS: Stones of irregular size and colour, mortar washed out of the joints, patches of grey and yellow lichen, dry pine needles and a few cones on the path, a small puddle in a rut, grass trampled short near the walls, reddish-brown soil showing at the path edges.

PHOTO PROCESSING: Natural iPhone processing: soft contrast, muted slightly cool colours, real fresh spring green (not neon), a plain bright grey sky without invented detail, fine noise in the shaded pines, no filter, no added vignette; slightly soft corners.

PEOPLE: No people anywhere in the frame: the path is empty; no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Paraland, a small fictional island of Larpidie: the ruin of an old stone castle on a low hill (only about 55 m above the sea) above the island's historic old town, on the heritage trail from the old town past the ruin to the newer castle. Modest scale: a small medieval-style ruin, not a huge fortress.

AVOID: no people, no tourists, no signs or information boards, no fences, no fantasy or fairy-tale castle, no dramatic cliffs, no flags, no dragons. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 9:16.
```

<a id="photo_08"></a>
## PHOTO 08 · MIDNIGHT JESKO (9:16)

**Lokalita:** V-07, C-01 · **Kamera:** PROPOSED CAMERA POINT x 12.370, y 10.360 km

```
Scene name (for reference only, never to be written in the image): MIDNIGHT JESKO. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: A black Koenigsegg Jesko hypercar with subtle gold-coloured wheels and a thin gold pinstripe, parked, stationary and switched off with no lights on, on an empty asphalt lay-by beside a quiet hill road near a reservoir dam at night. Authentic Jesko proportions seen from a low front three-quarter angle: a very low, wide mid-engine body, teardrop glass canopy, closed doors, a large front splitter with small canards, deep side air intakes and a long tail with the huge swan-neck rear wing on two pylons. The glossy black paint carries soft, slightly distorted reflections of the city lights and the dark sky; a thin film of dew on the windscreen. Behind the car, beyond a galvanised steel crash barrier and a strip of dark farmland, the land falls gently to a wide coastal plain: about 4 km away the warm sodium-orange and white lights of a low-rise harbour city spread across the plain in a glittering band, with brighter clusters at the harbour on the right, a dark bay beyond it, and a few tiny red and green navigation lights at sea. Clear deep-navy sky with a faint orange-grey city glow at the horizon and a few stars.

CAMERA AND COMPOSITION: Handheld in Night mode with the camera low, about 80 cm above the ground, looking east-south-east. Portrait; the car fills the lower half slightly left of centre; the city lights form a band across the upper third; the number-plate area is blank or out of view.

LIGHT AND WEATHER: Late summer, about two hours after sunset, clear and dry with light haze near the horizon. The car is lit only by the ambient glow of the city, the sky and one distant warm street lamp from the left; deep shadows are allowed; no flash, no studio light.

REALISM DETAILS: Real night-photo behaviour: fine colour noise in the shadows, slight smearing from Night-mode processing in the darkest areas, a small flare ghost from the street lamp, slightly blown highlights in the brightest city lights, coarse asphalt texture with a worn white edge line, dry grass tufts at the foot of the crash barrier, a little road dust and a few water spots on the lower bodywork.

PHOTO PROCESSING: Dark and moody but true-to-life iPhone Night-mode photo: slightly underexposed, neutral-to-cool shadows, warm sodium-orange city lights, the gold accents catching only small highlights, no teal-and-orange grade, no light trails.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Larpidie, fictional island nation in the north-west Pacific: a safe lay-by next to the viewpoint at a reservoir dam in the western hills, about 80 m above the coastal plain, looking at the small capital Larpington and its bay 4 to 6 km away; the city is low-rise with no skyscrapers.

AVOID: no people, no driving, no motion blur or light trails, no other cars, no headlights or tail lights on, no badges or logos other than the car's own shape, no readable number plate, no skyscrapers, no distorted car proportions. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 9:16.
```

<a id="photo_09"></a>
## PHOTO 09 · GOLDEN HOUR SUMMIT REST (9:16)

**Lokalita:** SP-05, M-01 · **Kamera:** PROPOSED CAMERA POINT x 6.000, y 6.800 km

```
Scene name (for reference only, never to be written in the image): GOLDEN HOUR SUMMIT REST. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: Two young hikers in dark outdoor clothing (dark shell jackets, black trousers, dark beanies) sit close together on a flat grey rock outcrop on a grassy mountain shoulder, seen from behind and slightly from the side, looking out over a wide valley toward the main mountain range. Two small backpacks and a metal water bottle lie on the rock beside them. In the foreground: tussocky autumn grass turned straw-gold and rust, low bracken gone copper-brown, lichen-covered rocks, a narrow worn footpath. Below, the valley is already in cool blue shadow with thin mist lying along the stream; the forested slopes are a warm-temperate mix of dark cedar and cypress, pines and deciduous trees in autumn colour (orange, yellow, wine red). About 3.3 km away rises a broad, rounded forested mountain of only about 510 m, the second-highest summit of the range; a narrow cleared grassy strip runs down its upper slope like a small ski run (no snow, no lifts visible), and its top is lit warm orange by the last sun.

CAMERA AND COMPOSITION: Handheld, standing a few metres behind the hikers, slightly above them, looking east-north-east. Portrait; the hikers sit in the lower third slightly right of centre, the valley and the lit summit fill the middle, sky in the upper quarter; the foreground rocks are sharp, the distant mountain slightly soft from haze.

LIGHT AND WEATHER: Autumn golden hour, about 25 minutes before sunset, clear sky with a few thin high clouds. The low sun is directly behind the camera: the hikers' backs and the rocks are warmly lit, their long shadows stretch forward down the slope toward the valley, and the sunlit tops of the far ridges glow orange while the valley floor lies in shadow; the eastern sky ahead is soft blue fading to pale pink near the horizon. No backlight, no rim light, no sun in the frame.

REALISM DETAILS: Natural, slightly slumped sitting posture, creased jackets, a little mud on the boots, wisps of hair under a beanie, fine dust and lichen on the rock, individual grass blades lit from behind the camera, uneven mist, a power line or small farm track barely visible in the valley.

PHOTO PROCESSING: Natural iPhone golden-hour photo: warm but not orange-soaked, believable contrast, slightly cool shadows, clean blue sky, a little noise in the shadowed valley, no filter, no added grain, no vignette.

PEOPLE: Exactly two people in the frame: two young hikers sitting close together, seen from behind and slightly from the side, faces not visible. Natural anatomy and proportions, real clothing folds, shadows consistent with the sun behind the camera. No other people anywhere, not even tiny distant figures.

PLACE AND SCALE: The western mountains of Larpidie, a fictional island nation in the north-west Pacific, south of Japan, with warm summers, distinct seasons and occasional winter snow: low, forested, rounded mountains of 300 to 560 m with grassy shoulders and rock outcrops; modest scale.

AVOID: no extra people, no visible faces, no logos on clothing, no tent or camp, no Alpine or Himalayan scale, no snow-covered peaks, no glaciers, no rim light or backlit silhouettes, no sun in the frame. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 9:16.
```

<a id="photo_10"></a>
## PHOTO 10 · SWISS-INSPIRED MOUNTAIN MEADOW (9:16)

**Lokalita:** M-03, SP-04 · **Kamera:** PROPOSED CAMERA POINT x 4.520, y 8.700 km

```
Scene name (for reference only, never to be written in the image): SWISS-INSPIRED MOUNTAIN MEADOW. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: A sloping early-summer hay meadow in low green mountains. A narrow footpath of trampled grass and bare earth winds from the bottom of the frame up across the meadow, full of wildflowers: white ox-eye daisies, yellow buttercups, purple clover and knapweed, tall grasses with seed heads. Along the path runs a weathered post-and-rail fence of grey timber, partly leaning. About 120 m away at the upper edge of the meadow stands a mountain chalet of dark weathered timber on a rough stone base, with a wide low-pitched roof of grey slate, a wooden balcony with simple carved rails, small windows with white frames and a stack of firewood under the eaves; next to it one or two small timber barns. A small clear brook runs through the meadow in the middle distance in a shallow channel of stones and ferns. Around the meadow grow tall dark Japanese cedars and cypresses mixed with a few broadleaf trees. About 1 km behind rises a rounded grassy summit of about 440 m with a few rocky outcrops, partly covered by a soft cloud shadow.

CAMERA AND COMPOSITION: Handheld at standing eye level on the path, looking north-east. Portrait; the path leads diagonally from the bottom left corner toward the chalet, which sits slightly right of centre in the middle third; the rounded summit and sky fill the top third.

LIGHT AND WEATHER: Early summer, mid-morning, mixed sun and fluffy cumulus clouds. The sun is high from the right, lighting the meadow and the chalet's right side, with soft-edged cloud shadows moving across the slope; humid, slightly hazy air in the distance.

REALISM DETAILS: Grass moving slightly in the breeze (a little motion softness in the tallest stems), dew still on the shaded grass, moss on the fence posts, a rusty wire on one post, uneven timber on the chalet with darker weathering under the eaves, small mud patches on the path.

PHOTO PROCESSING: Natural iPhone daylight processing: true-to-life greens (not neon), soft highlights on the clouds, moderate contrast, light atmospheric haze on the summit, no filter, no added grain or vignette.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: The western meadows of Larpidie, a fictional island nation in the north-west Pacific with warm, humid summers and distinct seasons: hill pastures and small chalets on a low-mountain scale (300 to 500 m), with Japanese cedar and cypress forest; mood reminiscent of Swiss pastures, but warm-temperate vegetation and modest scale.

AVOID: no people, no cars, no animals, no readable text, no ski lifts, no snow, no glaciers, no giant Alpine peaks, no spruce-only Alpine forest, no perfectly manicured lawn. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 9:16.
```

<a id="photo_11"></a>
## PHOTO 11 · ALPINE-INSPIRED LAKE POSE (9:16)

**Lokalita:** N-04, ST-L1-02 · **Kamera:** PROPOSED CAMERA POINT x 12.205, y 10.170 km

```
Scene name (for reference only, never to be written in the image): ALPINE-INSPIRED LAKE POSE. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: An empty pebbly shore of a calm mountain reservoir in summer. In the foreground: rounded grey and ochre pebbles of mixed size, some still wet at the water's edge, a bleached silver-grey piece of driftwood lying diagonally, dry grass tufts and a few small reeds. The water is clear and blue-green, transparent near the shore so that the pebbles on the bottom are visible, then darker further out, with gentle ripples. Along the opposite shore runs a pale band of bare stony bank a few metres high where the water level has dropped, then steep slopes of dense green forest: dark Japanese cedar and cypress, pines and broadleaf trees. At the far left on the shore, the small roofs of a hamlet among trees. In the background, 6 to 8 km away and softened by blue haze, rise the highest mountains of the island, only about 500 to 560 m high, rounded and forested, the higher one on the right.

CAMERA AND COMPOSITION: Handheld at standing eye level just above the water's edge, looking west-north-west across the lake. Portrait; the pebbles and driftwood fill the lower third, the water the middle, the forested slopes and the hazy mountains the upper part; the horizon slightly above the middle.

LIGHT AND WEATHER: Summer, early afternoon, clear sky with a few fair-weather clouds above the mountains. The sun is high from the left, giving bright sparkles on the ripples and crisp short shadows behind the pebbles; the distant mountains are paler in the summer haze.

REALISM DETAILS: Small algae film on the stones at the waterline, a thin line of dried foam and twigs along the edge, a faint mark of the previous water level on the rocks, uneven tree heights on the slopes, a single dead tree among the green ones.

PHOTO PROCESSING: Natural iPhone daylight processing: clear but not oversaturated water, realistic greens, a little haze on the distant mountains, believable contrast, no filter, no added grain or vignette; a slight specular glare on the water.

PEOPLE: No people anywhere in the frame: the shore is empty; no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Larp Reservoir in Larpidie, a fictional island nation in the north-west Pacific south of Japan: a drinking-water reservoir in low forested hills, with a recreational pebbly shore on its east side; lake and hills of modest, low-mountain scale.

AVOID: no people, no boats, no dam wall, no logos, no glaciers, no snow, no giant Alpine peaks, no turquoise glacier-lake colour, no jetty, no buildings in the foreground. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 9:16.
```

<a id="photo_12"></a>
## PHOTO 12 · SUNSET ABOVE LARPIDIA (16:9)

**Lokalita:** M-03, PG-01 · **Kamera:** PROPOSED CAMERA POINT x 5.300, y 8.010 km

```
Scene name (for reference only, never to be written in the image): SUNSET ABOVE LARPIDIA. Format 16:9.

Create a horizontal 16:9 widescreen smartphone photo. It must look like a genuine photo taken by a person on an Apple iPhone 15 (main camera, 1x, realistic smartphone HDR, natural human eye-level perspective, slightly imperfect everyday framing), not CGI, not a 3D render, not an illustration, not an advertising visualisation and not a drone shot.

SCENE: Exactly two young hikers sit side by side on a grassy mountain meadow with their backs to the camera, looking toward the sunset. The sky is huge and dramatic: layered dark blue-grey clouds with a narrow band of orange light at the horizon, the ocean glimmering far below; small yellow wildflowers in the grass in the foreground catch the last light. The hikers wear dark jackets and beanies, their backpacks lie beside them.

COMPOSITION: Wide landscape; the two hikers small in the lower centre (about one fifth of the frame height), the sky takes two thirds of the frame; wildflowers sharp in the foreground.

LIGHT AND ATMOSPHERE: Sunset after rain: the last orange light low on the horizon, cool dark clouds above; dramatic yet natural. The hikers are backlit, so they appear as dark shapes with only a faint rim light on their shoulders, hair and beanies.

PHOTO LOOK: dark, moody, higher contrast, pulled highlights, cool blue-grey sky with one narrow orange band, lowered exposure. Subtle authentic imperfections (only a few, not all at once): slightly overexposed horizon band, a soft lens flare.

PEOPLE: Exactly two people in the frame: two young hikers in dark jackets and beanies sitting side by side on the grass, backs to the camera, backpacks beside them. Natural anatomy, natural clothing, correct proportions and cast shadows. No other persons anywhere, not even tiny distant figures.

PLACE AND SCALE: Rounded grassy mountain (about 440 m) in western Larpidie, fictional, with the Pacific visible to the west; low-mountain scale, no giant peaks.

AVOID: no extra people, no faces, no logos on clothing, no tent, no fantasy colours, no Himalayan scale. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs or lettering, interface overlays, borders or frames. Avoid a CGI or video-game look, oversaturated HDR halos, fake glowing skies, heavy vignette, plastic textures, warped architecture, impossible scale and AI text artefacts.

Aspect ratio 16:9.
```

<a id="photo_13"></a>
## PHOTO 13 · THE HIDDEN RIDGE (9:16)

**Lokalita:** N-04 · **Kamera:** PROPOSED CAMERA POINT x 12.032, y 9.828 km

```
Scene name (for reference only, never to be written in the image): THE HIDDEN RIDGE. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: A view from a small natural terrace of rock and grass about 20 m above a dark, still reservoir, looking down and across the water. In the foreground: tussocky autumn grass in olive and straw tones, grey lichen-covered rocks, a faint footpath and, at the very right edge of the frame, a simple weathered timber safety rail with two posts. Below, the steep rocky banks drop at 30 to 45 degrees into the lake: grey stone slabs, scree and clinging shrubs. The water is dark slate-grey and almost mirror-still, with thin bands of mist lying on it. The opposite slopes are covered in dense forest: dark Japanese cedar and cypress, pines and patches of broadleaf trees in muted autumn rust and yellow. Along the far shore, the grey roofs of a tiny hamlet are half hidden in the mist. Higher up on the far slope, one pale break of light where the clouds thin a little.

CAMERA AND COMPOSITION: Handheld at standing eye level at the edge of the terrace, tilted slightly downward, looking west across the lake. Portrait; the foreground rocks and grass fill the lower quarter, the dark water and mist the middle, the far forested slope and the low cloud the upper part.

LIGHT AND WEATHER: Autumn, early morning, fully overcast with low cloud touching the higher ridges. Soft, flat, cool light without shadows; mist on the water and in the folds of the far slope; one faint brighter patch on the far slope where the light breaks through; quiet, moody atmosphere.

REALISM DETAILS: Dew drops on the grass blades, wet dark rock surfaces, a few fallen leaves caught between the rocks, cracked and grey timber on the rail with a rusty bolt, uneven mist that is thicker in some places than others, small ripples from a fish or a breath of wind in one spot.

PHOTO PROCESSING: Natural iPhone processing on an overcast morning: low contrast, muted cool greens and greys, true dark tones without crushed blacks, a plain grey sky without invented detail, fine noise in the dark water, no filter, no added grain or vignette.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Larp Reservoir in the hills of western-central Larpidie, a fictional island nation in the north-west Pacific with distinct seasons: a dark water-supply lake in a valley of low forested hills with steep rocky banks; terrace about 85 m above sea level; modest, low-mountain scale.

AVOID: no people, no boats, no dam wall, no buildings in the foreground, no dramatic fjord or Alpine scale, no sunshine or golden light, no fantasy fog effects. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 9:16.
```

<a id="photo_14"></a>
## PHOTO 14 · RIVER TO THE SEA (16:9)

**Lokalita:** W-01 · **Kamera:** PROPOSED CAMERA POINT x 11.600, y 12.955 km

```
Scene name (for reference only, never to be written in the image): RIVER TO THE SEA. Format 16:9.

Create a horizontal 16:9 widescreen smartphone photo. It must look like a genuine photo taken by a person on an Apple iPhone 15 (main camera, 1x, realistic smartphone HDR, natural human eye-level perspective, slightly imperfect everyday framing), not CGI, not a 3D render, not an illustration, not an advertising visualisation and not a drone shot.

SCENE: A strong rocky river enters the sea on a wild coast: dark wet boulders and cobbles in the foreground, fast braided channels of clear, slightly tea-coloured water spilling across a pebble and dark-sand shore into small breaking waves, low coastal rocks flanking the river mouth, scrub and wind-bent trees on the banks, a hazy grey horizon.

COMPOSITION: Wide landscape, camera low near the water; the river leads from the lower left toward the surf in the centre, rocks in the foreground, sea and sky in the upper third.

LIGHT AND ATMOSPHERE: Cold grey overcast late-autumn morning, wet sheen on the stones, fine spray in the air.

PHOTO LOOK: cool desaturated blue-grey, slightly dark, crisp wet textures, fine grain. Subtle authentic imperfections (only a few, not all at once): a few droplets on the lens, slight softness at the edges.

PEOPLE: No people anywhere in the frame: no figures, faces or silhouettes, not even tiny distant ones, and no animals.

PLACE AND SCALE: Mouth of the main river of Larpidie, fictional, on the south coast; the river is the main stream below a reservoir; rough pebble shore with boulders.

AVOID: no people, no buildings, no boats, no bridges, no sunny beach vibe, no tropical palms. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs or lettering, interface overlays, borders or frames. Avoid a CGI or video-game look, oversaturated HDR halos, fake glowing skies, heavy vignette, plastic textures, warped architecture, impossible scale and AI text artefacts.

Aspect ratio 16:9.
```

<a id="photo_15"></a>
## PHOTO 15 · LARPINGTON ROOFTOP NIGHT (9:16)

**Lokalita:** HV-01, CP-B07 · **Kamera:** PROPOSED CAMERA POINT x 16.628, y 13.707 km

```
Scene name (for reference only, never to be written in the image): LARPINGTON ROOFTOP NIGHT. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must look like a genuine photo taken by a person on an Apple iPhone 15 (main camera, 1x, realistic smartphone HDR, natural human eye-level perspective, slightly imperfect everyday framing), not CGI, not a 3D render, not an illustration, not an advertising visualisation and not a drone shot.

SCENE: A night, story-style photo from an elegant hotel rooftop terrace overlooking a small historic harbour town. Foreground: a wrought-iron and stone balustrade, softly lit stone steps and warm-toned paving, a corner of a teak lounge chair. In the distance the illuminated old town: warm yellow window lights, a floodlit brick-and-stone church tower, terracotta rooftops in shadow, harbour lights reflected in dark water; a deep navy sky with a few stars.

COMPOSITION: Portrait; the balustrade and steps in the lower third, the old town a glowing band across the middle, sky above; a slight handheld tilt.

LIGHT AND ATMOSPHERE: Night: warm artificial light from windows, street lamps and a floodlit church; the sky deep navy with the last faint glow in the west.

PHOTO LOOK: moody Instagram look: underexposed by about one stop, warm city lights against a deep navy sky, soft bokeh, fine grain. Subtle authentic imperfections (only a few, not all at once): slight bloom around the brightest lamps, soft detail in the dark rooftops.

PEOPLE: No people anywhere in the frame: no figures, faces or silhouettes, not even tiny distant ones, and no animals.

PLACE AND SCALE: Larpington, fictional harbour capital of Larpidie: a compact brick-and-stone old town of two to three floors with terracotta roofs and a church tower; elegant, quiet, European island mood.

AVOID: no people, no skyscrapers, no neon signs, no readable text, no Dubai-style opulence, no fireworks. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs or lettering, interface overlays, borders or frames. Avoid a CGI or video-game look, oversaturated HDR halos, fake glowing skies, heavy vignette, plastic textures, warped architecture, impossible scale and AI text artefacts.

Aspect ratio 9:16.
```

<a id="photo_16"></a>
## PHOTO 16 · COASTAL DAWN HAND VIEW (9:16)

**Lokalita:** V-04 · **Kamera:** PROPOSED CAMERA POINT x 22.050, y 14.450 km

```
Scene name (for reference only, never to be written in the image): COASTAL DAWN HAND VIEW. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: A first-person view from a low coastal lookout at the very tip of a peninsula, just above the sea, on a cold winter morning. Only the photographer's right hand and wrist are visible in the lower foreground, extended naturally toward the sea, holding a small plain white ceramic coffee cup; a thin wisp of steam rises from the coffee in the cold air. On the wrist a simple stainless-steel wristwatch with a plain dark dial and no brand or text, partly under the cuff of a navy wool coat sleeve. Just beyond the hand runs a simple galvanised steel railing with a little rust at the joints, and below it dark wet rocks with small waves breaking white. Across a calm strait about 2 to 3 km wide lies the low, dark coast of a small island: on its left part, on a gentle hill, the dark silhouette of a small castle; on its right part, a cluster of warm yellow lights of a small harbour village and marina reflected in the water. Above the island, the sky glows in the pre-sunrise gradient from deep indigo above to soft pink and a thin orange band exactly where the sun is about to rise behind the island.

CAMERA AND COMPOSITION: Handheld with the left hand, at standing eye level, looking east-south-east straight toward the sunrise point. Portrait; the hand and cup sharp in the lower third, the railing just above them, the horizon on the upper-third line; the island coast soft and small; the focus on the cup with the far shore slightly soft.

LIGHT AND WEATHER: Winter blue hour, about 15 minutes before sunrise, cold, clear and calm. The only light comes from the glowing horizon straight ahead and the soft blue sky: the back of the hand and the cup are lit softly from the front and above, with a faint warm reflection on the cup rim; the harbour lights on the island are still on.

REALISM DETAILS: Natural hand anatomy (five fingers, realistic knuckles and nails, slight redness from the cold), a few drops of coffee on the cup rim, fine scratches on the watch glass, condensation from the breath barely visible, a little sea spray on the railing, slight unevenness of the horizon from handheld framing.

PHOTO PROCESSING: Natural iPhone low-light processing: soft contrast, true indigo-to-pink sky without exaggerated saturation, slight noise in the dark sea and rocks, gentle highlights on the harbour lights, no filter, no added grain or vignette, no fake bokeh.

PEOPLE: No person is visible except the photographer's own right hand and wrist in first-person view (no face, no body, no other people anywhere, not even tiny distant figures).

PLACE AND SCALE: The tip of the south-eastern peninsula of Larpidie, a fictional island nation in the north-west Pacific with distinct seasons and occasional winter snow, looking across a 2-km strait toward the small island of Paraland with its hilltop castle on the left and its harbour village on the right.

AVOID: no face, no full body, no other people, no phone visible, no brand logos or text on the watch or cup, no boats in the foreground, no snow on the ground, no sun disc above the horizon, no castle on the right side. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 9:16.
```

<a id="photo_17"></a>
## PHOTO 17 · OLD MONEY CASTLE MORNING (16:9)

**Lokalita:** PL-02 · **Kamera:** PROPOSED CAMERA POINT x 24.790, y 15.715 km

```
Scene name (for reference only, never to be written in the image): OLD MONEY CASTLE MORNING. Format 16:9.

Create a horizontal 16:9 widescreen smartphone photo. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: A calm early-morning view across the forecourt of a small historic château-like castle on a hill. The castle: a two-storey main block of pale cream limestone with weathered, slightly stained ashlar, tall arched windows with small-paned white frames, a steep grey slate roof with small dormers and two tall stone chimneys, and one short round corner tower with a conical slate roof. A modest but dignified stone staircase with worn steps leads to an arched oak door with iron studs. In the foreground: a formal garden with clipped boxwood hedges, a raked pale gravel path leading toward the stairs, two large terracotta pots with lemon trees, a few climbing roses on the wall. On the left a low stone parapet, and beyond it the hazy sea and, far away, the low dark coast of the main island.

CAMERA AND COMPOSITION: Handheld at standing eye level on the gravel path, looking north-west toward the castle. Wide landscape framing; the gravel path leads from the bottom edge to the stairs; the castle fills the centre right; the parapet and sea view open on the left third; the verticals lean very slightly inward from the wide lens.

LIGHT AND WEATHER: Early summer, early morning, clear sky with light haze over the sea. The low sun is from the right and slightly behind the camera, lighting the facade warmly at a glancing angle, so that every stone and window frame has soft shadows on its left; long shadows of the hedges fall to the left; the sea on the left is pale and hazy.

REALISM DETAILS: Lichen and dark weather streaks on the limestone below the windowsills, a few missing slates, moss in the stair joints, footprints and rake marks in the gravel, a garden hose coiled at the base of a wall, dew on the boxwood, a slightly uneven hedge top, a simple iron lantern above the door.

PHOTO PROCESSING: Natural iPhone morning processing: warm but true limestone colours, pale-blue hazy sky, restrained contrast, the sea and far coast soft in the haze, no filter, no added grain or vignette.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Paraland Castle on its hill on the small island of Paraland, part of the fictional island nation Larpidie in the north-west Pacific: a small château-style castle of pale limestone with a formal garden, about 1.4 km from the island's harbour; quiet European old-money mood.

AVOID: no people, no cars, no flags with text, no theme-park or fairy-tale castle, no tourists, no scaffolding, no huge palace, no sun in the frame, no direct backlight. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 16:9.
```

<a id="photo_18"></a>
## PHOTO 18 · OLD MONEY CHURCH COURTYARD (9:16)

**Lokalita:** CP-B07 · **Kamera:** PROPOSED CAMERA POINT x 15.857, y 13.673 km

```
Scene name (for reference only, never to be written in the image): OLD MONEY CHURCH COURTYARD. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: A quiet corner of a small church square beside an old English-style parish church in late spring. The south wall of the nave runs diagonally through the frame: red-brown brick with honey sandstone quoins, buttresses and window surrounds, tall pointed-arch windows with leaded clear glass, moss and ivy climbing at the base. About 35 m away, a small pointed-arch side door of dark oak with black iron hinges sits at the top of three worn stone steps. In the foreground: the edge of the square with old granite setts and a narrow strip of gravel, a low moss-covered stone wall with a wrought-iron gate standing slightly ajar, and the trunk and lower branches of a large old linden tree in fresh pale-green leaf. A few weathered gravestones lean in the grass along the wall. A simple wooden bench with no plaque stands under the tree.

CAMERA AND COMPOSITION: Handheld at standing eye level from the south-west corner of the square, looking east-north-east along the church wall. Portrait; the iron gate and linden trunk frame the left foreground, the church wall leads diagonally to the side door slightly right of centre; the church roof and a patch of sky at the top; vertical lines converge slightly from the phone's wide lens.

LIGHT AND WEATHER: Late spring, mid-afternoon, mostly clear. The sun is behind the camera and filtered through the linden leaves, scattering dappled patches of warm light on the setts, the steps and the brick wall; the rest is in soft, cool shade; calm, quiet atmosphere.

REALISM DETAILS: Uneven, slightly sunken setts with moss in the joints, worn hollows in the middle of the stone steps, faded and patched mortar, ivy tendrils on the gate, linden seeds and a few fallen blossoms on the ground, lichen on the gravestones (no readable inscriptions), a slight rust bloom on the gate.

PHOTO PROCESSING: Natural iPhone daylight processing: soft but true contrast between dappled sun and shade, restrained warm brick tones, natural spring greens, no filter, no added grain or vignette; a few small bright highlights in the leaves may clip.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Old Larpington, the historic core of the fictional island capital of Larpidie in the north-west Pacific: an English-style parish church of brick and sandstone on the church square, built by the first British settlers around 1600; quiet, European, understated.

AVOID: no people, no cars, no readable text on plaques, gates or gravestones, no modern lighting, no flashy luxury, no Gothic cathedral scale, no flowers in unnatural colours. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 9:16.
```

<a id="photo_19"></a>
## PHOTO 19 · MANOR TERRACE SEA VIEW (9:16)

**Lokalita:** PL-03 · **Kamera:** PROPOSED CAMERA POINT x 24.600, y 18.060 km

```
Scene name (for reference only, never to be written in the image): MANOR TERRACE SEA VIEW. Format 9:16.

Create a vertical 9:16 portrait smartphone photo, like a full-screen phone story. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: The sea-view terrace of a small historic seaside manor hotel early in the morning. In the foreground: a weathered pale stone balustrade with turned balusters and a wide top rail; a large terracotta pot of lavender standing on the terrace; the corner of a small round table with a white linen cloth, a clear glass of water and a white cup of coffee on a saucer; the back of a rattan chair at the left edge. Beyond the balustrade, the land falls about 14 m to a low wooded shoreline of pines and shrubs, and about 600 m away curves a small sandy bay with clear, soft turquoise water, darker blue further out. On the right, a low green headland with pines and grey rocks runs into the sea, softened by morning haze. A few small whitewashed villas with terracotta roofs are scattered among the trees along the bay.

CAMERA AND COMPOSITION: Handheld at seated-to-standing height beside the table, looking south-south-west over the balustrade. Portrait; balustrade, lavender and table in the lower third, the bay and headland in the middle, sky above; natural depth of field from a phone, everything readable.

LIGHT AND WEATHER: Late summer, early morning, clear sky with a thin haze over the sea. The low sun comes from the left, lighting the lavender, the cup and the balustrade warmly from the side and casting long soft shadows of the balusters to the right across the terrace; the sea has a gentle shimmer on the left.

REALISM DETAILS: Lichen and small cracks in the stone balustrade, a few fallen lavender flowers on the tiles, slight creases in the linen, a faint ring of water under the glass, condensation on the glass, a slightly uneven horizon from handheld framing.

PHOTO PROCESSING: Natural iPhone morning processing: soft warm light, realistic turquoise water (not neon), restrained contrast, slight haze on the headland, no filter, no added grain or vignette; a small reflection glare on the glass.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: The south coast of Paraland, a small fictional resort island of Larpidie in the north-west Pacific: low historic hotels and villas above a sandy bay, warm-temperate pines and shrubs; understated European island elegance, not flashy.

AVOID: no people, no pool parties, no gold or marble excess, no yachts in the foreground, no readable text, no high-rise hotels, no tropical palm-beach look, no fake tilt-shift blur. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 9:16.
```

<a id="photo_20"></a>
## PHOTO 20 · HERITAGE STREET ELEGANCE (16:9)

**Lokalita:** CP-B08, CP-SQ03 · **Kamera:** PROPOSED CAMERA POINT x 16.458, y 13.665 km

```
Scene name (for reference only, never to be written in the image): HERITAGE STREET ELEGANCE. Format 16:9.

Create a horizontal 16:9 widescreen smartphone photo. It must be indistinguishable from a real, unedited photo that an ordinary person took on an Apple iPhone 15 with the main camera (1x, 26 mm-equivalent, f/1.6), standard Apple Photos processing, straight out of camera, with natural human perspective and slightly imperfect everyday framing. Not CGI, not a 3D render, not an illustration, not concept art, not a stock or advertising photo, not a drone shot and not filtered.

SCENE: A historic market street about 75 m before it opens onto a large market square, in autumn. Both sides are lined with well-kept two- and three-storey facades of red-brown brick and honey-coloured sandstone, white timber sash windows, a few dark green shutters, slate roofs and chimneys; at street level small shops with dark painted wooden shopfronts and quiet window displays, without readable lettering. The street is paved with grey granite setts and edged with sandstone pavements, with black cast-iron lamp posts and a few planters with late flowers. At the end of the street, on the far side of the square, stands the old stone market hall: a long two-storey building of pale sandstone, about 10 m high, with a row of tall round arches on the ground floor, a slate roof and a small lantern turret, but no clock. On the left side of the street, a 1960s cream British saloon car is parked at the kerb, clean and slightly faded, with no badges and no number plate visible. A few young lime trees along the square have turned yellow.

CAMERA AND COMPOSITION: Handheld at standing eye level slightly right of the centre of the street, looking east-north-east toward the square. Wide landscape framing; one-point perspective with the market hall small and centred at the end of the street; the parked car in the left foreground but not the main subject.

LIGHT AND WEATHER: Autumn golden hour, about 40 minutes before sunset, clear sky. The low sun is directly behind the camera: it lights the market hall and the facades at the end of the street in warm gold, while the near part of the street is partly in shade from the houses; long shadows stretch forward along the setts; the sky ahead is pale blue.

REALISM DETAILS: Fallen yellow lime leaves along the kerb, worn and slightly uneven setts with moss in the joints, a small repair patch of asphalt, chewing-gum spots on the pavement, slight dust on the car, a few dark rust streaks under the gutters, a closed café umbrella, slightly misaligned window frames.

PHOTO PROCESSING: Natural iPhone golden-hour processing: warm but true honey-stone colours, believable contrast between sunlit and shaded parts, clean pale-blue sky, no filter, no added grain or vignette; no lens flare, since the sun is behind the camera.

PEOPLE: No people anywhere in the frame: no figures, faces, silhouettes, shadows or reflections of people, not even tiny distant ones, and no animals.

PLACE AND SCALE: Old Larpington, the historic core of the fictional island capital of Larpidie in the north-west Pacific: a market street leading to the market square (about 100 by 66 m) with the stone market hall; English-style brick and stone of two to three storeys; a calm, elegant small-town atmosphere.

AVOID: no people, no modern signage, no neon, no readable text, no supercars, no busy traffic, no number plates, no car badges, no clock on the market hall, no lens flare or sun in the frame. No text of any kind anywhere in the image: no captions, titles, watermarks, logos, readable signs, number plates or lettering, interface overlays, borders or frames. Avoid typical AI-image tells: waxy or plastic textures, over-smoothed surfaces, warped or melting architecture, inconsistent perspective, impossible scale, duplicated objects, malformed hands, HDR halos, oversaturated colours, glowing skies, cinematic colour grading, fake bokeh or tilt-shift blur, heavy vignette and gibberish lettering.

Aspect ratio 16:9.
```
