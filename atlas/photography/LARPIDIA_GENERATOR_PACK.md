# INSTRUCTIONS FOR THE IMAGE / VIDEO GENERATOR

You are the visual generator for Larpidia, a fictional Pacific island setting. This Markdown file contains an ordered library of 30 independent photo prompts and 10 independent short-video prompts. Treat each scene prompt as a complete generation brief.

Do not rewrite, analyze, summarize, or output the whole library unless the user asks. Generate only one finished image or video per turn. Never make a collage, contact sheet, multi-panel composition, or several alternatives unless the user explicitly requests one.

Remember the next photo and next video positions independently within the conversation:
- “START FOTKY” starts or resets the photo sequence at P01 and generates only P01.
- “DALŠÍ FOTKA” or “DALŠÍ” generates the next photo in the current photo sequence.
- “OPAKUJ” regenerates the current scene, using the user’s feedback, without advancing either sequence.
- “FOTKA P14” generates that specific photo. A direct scene request does not change the sequential pointer unless the user says to continue from it.
- “START VIDEA” switches to the video collection and generates V01 only if actual video-generation capability is available.
- “DALŠÍ VIDEO” generates the next video in the video sequence.
- “VIDEO V02” generates that specific video only if video generation is supported.

If generation fails, do not advance the relevant sequence. Use the scene’s stated aspect ratio. Do not add text, subtitles, labels, logos, or explanatory overlays. If video generation is unavailable, say so clearly and preserve the video prompt for use in a compatible tool. If image generation is unavailable, do not pretend an image was created.

This document cannot give you access to local atlas files. When a scene lists a reference image and it has not been attached in the conversation, tell the user the exact relative file path to upload. Never claim to have seen a local reference that was not actually attached. The written prompts remain usable on their own; explain that text alone cannot guarantee exact coastlines, building placement, or sightlines.

# LARPIDIA PHOTO & VIDEO GENERATOR PACK

Český návod: nahraj tento soubor do konverzace s generátorem, který umí vytvářet obrázky nebo videa. Potom použij například příkaz „START FOTKY“. Pro přesnější návaznost na konkrétní mapu nahraj také doporučenou referenci ze sekce Reference File Manifest. Cesty v manifestu jsou místní cesty projektu; ChatGPT ani Gemini je neuvidí, dokud soubor nepřipojíš.

## GLOBAL PHOTOGRAPHY RULES

All generated prompts below are written in English and are designed to be pasted independently. Unless a scene specifies otherwise, use an Apple iPhone 15 main 1x camera, approximately 26 mm equivalent, eye-level human perspective, realistic smartphone HDR, natural texture and a believable travel-photography finish. Keep framing slightly human and imperfect rather than polished like a luxury campaign. No CGI, illustration, fantasy styling, text, watermarks, or graphic overlays.

At least 80% of the 30 photos should contain no visible people. In this library, P21 is the one intentionally human-centered photo; the other photos should remain empty of visible people. Do not add decorative tourists, distant silhouettes, drivers, shop customers, or crowds. When a person is requested, keep them anatomically natural, appropriately lit, and important to the composition without overpowering the place.

A car may be the subject without showing a driver. Keep parked cars stationary unless a scene explicitly describes movement. Do not put vehicles on unsafe cliff edges, trail paths, railway tracks, or pedestrian spaces.

Make subtle photographic imperfections occasional and scene-appropriate: a small highlight bloom, gentle haze, mild motion softness, slight grain in low light, imperfect handheld framing, or soft reflections in glass. Keep the main subject in focus. Imperfections should never obscure the location or look like image damage.

Use distinct, restrained editing treatments across the collection. Exposure, contrast, highlights, shadows, temperature, saturation, and grain suggestions are visual guidance, not exact software-slider requirements. Do not apply one identical filter to every scene. Keep skin, stone, foliage, vehicles, and water plausible.

## GLOBAL GEOGRAPHY RULES

Larpidia and Paraland are fictional. Larpidia is the larger main island; Paraland is a separate, smaller island southeast of it. The main island’s western and northwestern side has forested low mountains, rocky coast, springs and trails. The highest summit is about 560 m in the atlas model; do not depict alpine-scale ranges, glaciers, or permanent snowfields. The central-west contains the reservoir, waterfall and crystal cave. The capital Larpington is in the south/southeast. Smaller historically mixed English/Welsh and Japanese-influenced towns are in the north. The eastern/northeastern side is lower and contains sustainable industry and settlements.

The atlas is a proposed fictional model. Feature existence or role may be approved while exact names, coordinates, alignments, and design details remain proposed. Do not turn proposed details into claims about a real place. Where the exact camera point, interior, street frontage, hotel, turnout, or sightline is not fixed in the atlas, treat it as a plausible composition choice, not established canon.

The main island and Paraland have compact, defined coastlines. Do not add giant islands, invented towns, unrelated skylines, extra ports, large resorts, or mountain chains. Keep every image local to its named scene. A distant landmark should appear only if the relevant location guide supports it and the view remains plausible.

The L1, L2, and L3 railway concepts are part of the project. Their detailed routes and station positions are proposals. L1 is a scenic western nature railway associated with the waterfall and crystal cave; L2 is a surface electric railway serving towns and industry; L3 is a mostly underground urban/regional connection with an undersea link to Paraland. Do not add steam, smoke, futuristic technology, or an unapproved glass tunnel.

Map and render files in the atlas are simulated/procedural references, not real satellite or photographic evidence. Attach them only as visual guides for relative location, terrain, or coastline. Text and a reference image improve consistency but cannot guarantee pixel-accurate geography or a verified line of sight.

## COLOR, CONTRAST, EXPOSURE & IMPERFECTION GUIDE

Use the scene-specific edit note under each photo. Approximate exposure and contrast values communicate the intended look only.

- Mountain hiking: slightly lowered exposure, controlled highlights, modest contrast, gently cool white balance, restrained saturation; retain natural greens and snow detail.
- Forest springs and waterfalls: protect bright water highlights, deepen greens carefully, retain shadow texture; mild softness or water motion is acceptable.
- Historic streets: slightly warm stone and lamp light, muted greens, moderate contrast, controlled highlights; avoid a sepia or fake vintage filter.
- Night city and cars: lower exposure, stronger but realistic contrast, warm practical lights, cool shadows, subtle low-light grain; preserve detail in black paint and dark streets.
- Paraland summer: warm highlights, rich but believable sea blues, slightly softened shadows; avoid tropical neon colors or an oversaturated resort-ad look.
- Industry and interiors: neutral or mildly cool color, clean but realistic contrast, readable material texture, restrained highlights; no artificial glowing machinery.
- Video: keep exposure and color stable during movement. Allow only natural auto-exposure adjustments; do not introduce flicker, abrupt grading changes, jump cuts, warped geometry, or changing weather within one continuous shot.

## PHOTO COLLECTION INDEX

| ID | Scene | Format | Atlas location |
|---|---|---:|---|
| P01 | Snow Above the Pacific | 9:16 | M-01 |
| P02 | Hidden Forest Spring | 9:16 | SP-03 |
| P03 | Mountain Waterfall | 9:16 | N-03 |
| P04 | Waterfall Express | 16:9 | N-03, ST-L1-03, L1 |
| P05 | Skiing Above the Coast | 16:9 | M-02, SK-01 |
| P06 | Cliffside Sunset | 16:9 | N-01, CAPE-W |
| P07 | Mountain Reservoir | 16:9 | N-04, DAM-N04, V-07 |
| P08 | Old Larpington Street | 9:16 | C-01, CP-B07, CP-UL04 |
| P09 | Larpington After Rain | 9:16 | C-01, CP-UL19 |
| P10 | Ōru Maito Nights | 9:16 | T-04 |
| P11 | Empty Sunday Market | 16:9 | C-01, CP-SQ03, CP-B08 |
| P12 | Larpington Old Harbor | 16:9 | C-02 |
| P13 | Luxury Shopping Afternoon | 9:16 | C-01, CP-ZR02, CP-SH01 |
| P14 | Midnight Jesko | 9:16 | V-04, C-01 |
| P15 | Coastal GT-R | 9:16 | RD-R1, V-06 |
| P16 | Heritage Train L2 | 16:9 | L2, ST-L2-01 |
| P17 | Inside Crystal Cave | 9:16 | N-02, ST-L1-04, L1 |
| P18 | Metro L3 Station | 16:9 | L3, ST-L3-05 |
| P19 | Empty Coastal Road at Night | 9:16 | RD-R1, V-02 |
| P20 | Paraland Marina | 16:9 | H-02, PL-05 |
| P21 | Castle Ruins | 9:16 | PL-06, PL-01 |
| P22 | Hotel Balcony Morning | 9:16 | PL-03 |
| P23 | Beach Restaurant After Sunset | 9:16 | PL-03, B-05 |
| P24 | Hidden Beach Trail | 9:16 | TR-PL1, B-06 |
| P25 | Summer Water Park | 16:9 | PL-04 |
| P26 | Green Technology District | 16:9 | I-01 |
| P27 | Algae Production Facility | 16:9 | I-02 |
| P28 | Rainy Japanese Café | 9:16 | T-04 |
| P29 | Historic Square at Blue Hour | 16:9 | C-01, CP-SQ01 |
| P30 | Coast From a Train Window | 16:9 | L2, ST-L2-13 |

## PHOTO PROMPTS P01–P10

### P01 — Snow Above the Pacific
**Format:** 9:16 vertical  
**Location:** M-01, Mount Larp, western highlands. Summit elevation 560 m is a model value; trail point and sea sightline are not verified.  
**Reference:** S-01_base.png for island scale and relative terrain.  
**Edit:** Exposure about -0.3 EV, contrast +15, highlights -25, shadows -10, saturation -5, slightly cool temperature; keep snow white and forest green, with only subtle highlight bloom.

**Prompt (English):**  
Create one photorealistic vertical 9:16 hiking photograph as if casually taken on an Apple iPhone 15 main 1x camera, approximately 26 mm equivalent. The photographer is standing on a narrow trail near M-01, the forested western highland summit of fictional Larpidia, at about 560 m above sea level in the atlas model. Show a few irregular remnants of melting snow beside damp stones, coarse grass, moss and natural low-mountain vegetation in the foreground. Green wooded slopes descend through the middle distance, with low cloud caught in one or two valleys. Beyond them, allow a modest, hazy glimpse of the Pacific coast only where the terrain makes it plausible; do not turn this into a panorama of the whole island. The landscape must feel compact and low, never alpine. Early spring after a brief cold spell, natural daylight breaking through cloud, realistic smartphone HDR and slightly imperfect handheld framing. Keep snow patchy, not a continuous winter blanket. No people, buildings, ski resort, extra islands, text, or watermark. This is a beautiful incidental hiking moment, not an advertisement or CGI render.

### P02 — Hidden Forest Spring
**Format:** 9:16 vertical  
**Location:** SP-03, a registered spring in the western highlands, near the M-03 hiking area; exact camera position is approximate.  
**Reference:** S-01_base.png for the island’s western forest belt.  
**Edit:** Exposure -0.1 EV, contrast +8, highlights -20, shadows +8, slightly warm sunlight against cool green shade; mild lens softness around the frame.

**Prompt (English):**  
Photograph a small, quiet forest spring on the marked hiking landscape around SP-03 in western Larpidia. Use a vertical 9:16 composition from a person’s standing eye level, as if captured on an iPhone 15 main 1x camera. In the foreground, clear water wells gently from a low stone lip into a shallow natural basin, with wet pebbles, leaf litter, moss and a few grasses. The middle ground is layered with tree trunks and damp undergrowth; a narrow footpath passes beside the spring without looking constructed like a park attraction. A few shafts of soft sunlight filter through the canopy and catch the water, while the surrounding forest remains cool and shaded. Keep the spring modest and believable, not a luminous fantasy grotto. No people, buildings, signs, pipes, statues, or readable text. Preserve realistic water reflections, natural greens and slight smartphone exposure imperfections.

### P03 — Mountain Waterfall
**Format:** 9:16 vertical  
**Location:** N-03, Larp Falls, in the central-western nature area.  
**Reference:** S-01_base.png or S-01_oblique_NW.jpg for the central-west terrain relationship; these are simulations.  
**Edit:** Exposure -0.2 EV, contrast +18, highlights -30, shadows -8, slightly cool shade, modest texture on rocks; allow natural water motion softness.

**Prompt (English):**  
Create a realistic vertical 9:16 travel photograph of N-03, Larp Falls, a mountain river waterfall in the central-western forest of fictional Larpidia. Frame the falls from a safe natural viewing spot on the established trail. A narrow stream drops over weathered dark rock into a small clear pool; the waterfall is striking but not enormous. Ferns, moss, wet stones and forest growth fill the lower edges. Above and beyond the falls, show only a modest wooded slope and a soft opening of daylight through the trees. Make the water bright but retain detail in its highlights, and keep the shaded rock texture visible. iPhone 15 main 1x camera, eye-level travel framing, realistic HDR, a touch of water-motion softness and a slightly underexposed forest mood. No people, buildings, rail infrastructure in the foreground, giant cliffs, or fantasy glow.

### P04 — Waterfall Express
**Format:** 16:9 landscape  
**Location:** L1 photo stop at ST-L1-03 beside N-03, Larp Falls. Route alignment is an atlas proposal; the railway’s scenic nature role is established.  
**Reference:** S-01_oblique_NW.jpg and S-01_base.png for broad terrain only.  
**Edit:** Exposure -0.2 EV, contrast +12, highlights -20, natural greens, slightly cool shade; mild motion softness confined to train wheels and water.

**Prompt (English):**  
Create a wide 16:9 photorealistic travel photograph of the L1 scenic electric railway passing the waterfall viewing area at ST-L1-03 beside N-03, Larp Falls, in western Larpidia. From a safe trail-side platform, show one compact modern excursion train moving slowly along a realistic track through forest, near the waterfall but not crossing its face or blocking the river. Keep the train and falls both clearly recognizable: the waterfall occupies one side of the frame, the train curves through the middle distance, and wooded low hills form the background. The track can use a modest elevated section where needed, but avoid a huge viaduct or theme-park engineering. iPhone 15 main 1x travel-photo look, late afternoon daylight, slightly imperfect framing, believable movement softness on the train only, controlled highlights on water. No passengers visible, no steam, smoke, fantasy crystals, text, logos, or extra mountains.

### P05 — Skiing Above the Coast
**Format:** 16:9 landscape  
**Location:** SK-01 on M-02, the proposed short-season ski slope in the western highlands; summit height about 510 m in the model.  
**Reference:** S-01_base.png; the atlas does not verify a sea view from the slope.  
**Edit:** Exposure -0.3 EV, contrast +15, highlights -25, cool white balance, saturation -8; keep snow patches and tree detail, with slight haze in the distance.

**Prompt (English):**  
Photograph the modest ski slope SK-01 on M-02 in western Larpidia during a short winter-sport season. Compose a wide 16:9 view from the side of the safe run: a narrow groomed strip of snow descends among green-brown forest and exposed winter grass, with low wooded ridges behind it. Show only enough snowmaking coverage to make the slope plausible at this low elevation; the rest of the landscape remains naturally season-colored. If a distant opening permits, a faint blue Pacific horizon may appear, but do not force a coastline into view. Keep all mountains rounded and below the atlas model maximum of about 560 m. No people or lifts are necessary. iPhone 15 main 1x travel photography, cold clear winter light, realistic smartphone HDR and slightly imperfect composition. No alpine peaks, glaciers, huge ski resort, dense snow blanket, logos, text, or CGI.

### P06 — Cliffside Sunset
**Format:** 16:9 landscape  
**Location:** N-01 at CAPE-W, the safe rocky western-coast lookout.  
**Reference:** S-01_base.png and S-01_oblique_NW.jpg for the west-coast character.  
**Edit:** Exposure -0.2 EV, contrast +12, warm highlights, slightly cool shadows, highlights -25, gentle atmospheric haze; allow a small sun flare.

**Prompt (English):**  
Create a wide 16:9 sunset travel photograph from the safe lookout at N-01 near CAPE-W on Larpidia’s rocky western coast. Show a sturdy path and discreet safety rail in the near foreground, with weathered grass and dark coastal stone leading toward a low, uneven cliff edge set well back from the visitor area. The Pacific fills the open west-facing distance, catching muted amber light and blue-gray reflections. Across the middle distance, include only the island’s low forested coastal slopes; no beach is visible beneath this rocky northwestern coast. Let the setting sun soften the horizon without turning the sky into a dramatic fantasy spectacle. Eye-level iPhone 15 main 1x photograph, natural HDR, slightly warm highlights, restrained saturation and one subtle lens flare. No people, cliff-jumping, buildings, city skyline, or extra islands.

### P07 — Mountain Reservoir
**Format:** 16:9 landscape  
**Location:** N-04 Larp Reservoir, viewed from V-07 near DAM-N04 in the central-west.  
**Reference:** S-01_base.png and the atlas relief reference; protect the small inland reservoir setting.  
**Edit:** Exposure -0.2 EV, contrast +10, highlights -20, slightly cool shadows, restrained saturation; keep water reflective but not turquoise-glowing.

**Prompt (English):**  
Photograph the inland reservoir N-04 from its safe viewpoint V-07 near the modelled dam DAM-N04 in central-western Larpidia. Use a wide 16:9 landscape frame with calm reservoir water in the foreground, a wooded shoreline and rounded green hills around it. A small, realistic section of the dam embankment may appear at one edge to establish the water-management setting; do not make the structure monumental. The lake must read as a compact reservoir enclosed by land, not an ocean bay. Include natural reflections, a few reeds or stones along the shore, and soft cloud over the western forest. No people, boats, resort development, skyscrapers, or mountain peaks above the established low range. iPhone 15 main 1x, believable daylight, subtle atmospheric haze and moderate edited contrast.

### P08 — Old Larpington Street
**Format:** 9:16 vertical  
**Location:** C-01 Larpington, near CP-UL04 Church Street and CP-B07, the working-name historic church.  
**Reference:** S-03_oblique_S.jpg for broad city context; the capital plan is illustrative, not a real building photo.  
**Edit:** Exposure -0.2 EV, contrast +12, highlights -15, slightly warm stone, muted greens; retain natural brick and gentle edge softness.

**Prompt (English):**  
Create a vertical 9:16 iPhone 15 travel photograph in the old center of fictional Larpington, on the proposed Church Street area near CP-B07. Show a narrow brick-and-stone street leading toward a modest historic church on Church Square. The church and street should feel rooted in an English/Welsh-influenced island tradition: weathered brick, local stone, slate or tiled roofs, modest Gothic details, moss in shaded joints and small gardens. Add restrained contemporary Japanese street infrastructure only where natural, not as a themed set. Frame from eye level, with the church visible beyond the lane and enough foreground paving to create depth. Late afternoon after light cloud, warm but realistic color, no people, no oversized cathedral, no high-rise buildings, readable signs, text, or watermarks.

### P09 — Larpington After Rain
**Format:** 9:16 vertical  
**Location:** C-01, in the proposed historic street area near CP-UL19 Market Street.  
**Reference:** S-03_oblique_S.jpg for compact capital placement and coastline relation.  
**Edit:** Exposure -0.4 EV, contrast +20, highlights -20, deep but readable shadows, warm lamps against cool wet stone, subtle sensor grain.

**Prompt (English):**  
Photograph an empty evening street in old Larpington after rain, near the proposed Market Street area in C-01. Use a vertical 9:16 handheld iPhone 15 main 1x composition. Wet cobbles and dark paving reflect a few warm street lamps; brick shopfronts and modest stone façades narrow toward a quiet bend. Show closed café windows and subdued town lighting, with no pedestrians, parked cars, or crowd reflections. The atmosphere is intimate and damp rather than noir or theatrical. Preserve believable shadow detail, restrained warm highlights and realistic smartphone low-light grain. Architecture should remain compact and English/Welsh-influenced, with no glass towers, neon billboard walls, invented landmarks, legible text, or decorative overlays.

### P10 — Ōru Maito Nights
**Format:** 9:16 vertical  
**Location:** T-04 Ōru Maito, a northern mixed English/Japanese-influenced town; exact lane is not assigned in the atlas.  
**Reference:** S-01_base.png for the town’s northern location and island scale.  
**Edit:** Exposure -0.5 EV, contrast +22, warm shop lights and cool blue shadows, highlights -20, subtle night grain.

**Prompt (English):**  
Create a realistic vertical 9:16 night travel photograph in T-04 Ōru Maito, a small northern town on fictional Larpidia. The exact street is a plausible composition within the registered town, not a fixed atlas address. Show a narrow, lived-in lane with compact brick-and-stone buildings, a few understated Japanese-influenced storefront details, warm lantern-like practical lighting and one small right-hand-drive compact car parked legally at the curb. Keep the street quiet and free of visible people. The cultural mix should feel ordinary and local, not an anime set or caricature; avoid dense neon, giant Japanese signs, pagodas, or a metropolitan skyline. iPhone 15 main 1x, natural handheld framing, realistic reflections and slight low-light grain. Any shop lettering must be too small to read, with no text overlay.


## PHOTO PROMPTS P11–P20

### P11 — Empty Sunday Market
**Format:** 16:9 landscape  
**Location:** C-01, CP-SQ03 Market Square, beside CP-B08 Market Hall.  
**Reference:** S-03_base.png and capital_plan_base.png for approximate square/block layout only.  
**Edit:** Exposure -0.2 EV, contrast +10, highlights -15, slightly warm stone and brick, muted greens; preserve morning softness.

**Prompt (English):**  
Create a wide 16:9 early-morning travel photograph of CP-SQ03, the proposed Market Square in Larpington, just before the Sunday market opens. The square is empty of people. A few closed market awnings and neatly arranged empty stalls sit near CP-B08 Market Hall; leave the paving and surrounding buildings visually clear. Show modest brick-and-stone façades, a covered market structure and a few damp patches from overnight dew. The market should feel like a working small-city place, not a tourist festival. Keep the street scale compact and the architecture consistent with Larpington’s English/Welsh-influenced core and discreet local details. Soft morning light, iPhone 15 main 1x perspective from across the square, restrained warm edit and gentle natural shadows. No vendors, customers, crowds, banners, legible text, skyscrapers, or invented monuments.

### P12 — Larpington Old Harbor
**Format:** 16:9 landscape  
**Location:** C-02, Larpington Old Harbour, in the south/southeast capital area.  
**Reference:** S-03_oblique_S.jpg and S-03_base.png for harbour and city position; both are simulations.  
**Edit:** Exposure -0.1 EV, contrast +12, highlights -20, warm stone and sunlit water, natural blue sea, slight haze.

**Prompt (English):**  
Photograph C-02, Larpington Old Harbour, as a realistic wide 16:9 travel image from the public quay. Include weathered brick warehouses, a modest historic harbour office, a few small working and leisure boats, and a stone waterfront promenade with restrained boutique frontage. Keep the harbour compact and integrated into the southern capital rather than resembling a major international port. Water should show small natural ripples and believable reflections; distant low hills may be faintly visible toward the northwest, never immediately behind the port as a giant range. No people, cruise ships, container terminal, large yachts, or fantasy architecture. Use iPhone 15 main 1x travel-photography perspective, late-afternoon daylight, realistic HDR, warm highlights, controlled reflections and a subtle atmospheric softness.

### P13 — Luxury Shopping Afternoon
**Format:** 9:16 vertical  
**Location:** C-01, proposed Main Avenue retail zone CP-ZR02 and limited-edition boutiques CP-SH01.  
**Reference:** S-03_oblique_W.jpg and capital_plan_base.png for the compact capital layout only.  
**Edit:** Exposure -0.1 EV, contrast +10, highlights -15, slightly warm façades, moderate saturation; subtle glass reflections.

**Prompt (English):**  
Create a vertical 9:16 afternoon travel photograph on the proposed Main Avenue retail area in Larpington, around CP-ZR02 and CP-SH01. Frame an elegant but human-scale shopping street with a few refined boutique windows set into English/Welsh-influenced brick and stone buildings. Include slate or tile roofs, iron details, restrained planting and realistic window reflections. The shops should suggest limited-edition design retail without readable brand names or luxury excess. Keep the street empty of visible people so the architecture and storefronts carry the image. Photograph at eye level on an iPhone 15 main 1x camera, with soft afternoon sun, slightly warm tones, natural smartphone HDR and a casual handheld crop. No giant department store, glass skyscrapers, heavy gold decoration, legible signage, text, or watermark.

### P14 — Midnight Jesko
**Format:** 9:16 vertical  
**Location:** V-04, a safe proposed viewpoint near the southeastern peninsula; Larpington C-01 is about 6.4 km to the west in the atlas model. Exact parking position is not registered.  
**Reference:** S-01_base.png for island/peninsula position; S-03_oblique_S.jpg for the capital’s broad placement.  
**Edit:** Exposure -0.5 EV, contrast +25, highlights -20, warm distant lights, cool shadows, subtle low-light grain; retain detail in black paint.

**Prompt (English):**  
Create a vertical 9:16 nighttime iPhone travel photograph of a black-and-gold Koenigsegg Jesko parked legally at a safe paved scenic turnout near V-04 on Larpidia’s southeastern peninsula. The exact turnout is a visual proposal; keep the car well back from any edge, behind a sensible barrier if the viewpoint has one, and away from the driving lane. Make the Jesko recognizable through its low sculpted body and distinctive aerodynamic proportions, with tasteful gold accents and realistic paint reflections; do not rely on readable logos or license text. Compose the car large in the lower half while a restrained cluster of distant Larpington lights glows across the dark landscape to the northwest. The vehicle is stationary, engine off, no driver or people visible. iPhone 15 main 1x, natural handheld framing, darker edited exposure, warm practical lights, cool shadows and mild sensor grain. No racing, burnout, cliff-edge parking, extra cars, or neon sci-fi city.

### P15 — Coastal GT-R
**Format:** 9:16 vertical  
**Location:** RD-R1 coastal ring road near V-06 on the southwest coast; the exact safe lay-by is a composition proposal, not a registered parking point.  
**Reference:** S-01_base.png and S-01_oblique_NW.jpg for the main island’s west-coast shape and road context.  
**Edit:** Exposure -0.2 EV, contrast +16, highlights -15, slightly cool sea and warm late-day reflections; mild lens flare.

**Prompt (English):**  
Photograph a dark-blue Nissan Skyline GT-R parked at a small, safe roadside lay-by beside RD-R1 near the proposed V-06 southwest-coast viewpoint. Keep the car entirely on a paved pull-off, not on the road, trail, cliff edge or beach. Use a vertical 9:16 composition with the GT-R as the clear foreground subject and a modest view of rugged coast, low vegetation and Pacific water behind it. The coastal ring road in this rough northwestern region may run inland behind rocky terrain, so do not force a dangerous cliffside road into the frame. Late-afternoon light glints naturally across the blue paint; maintain realistic vehicle proportions and subtle reflections. No person visible, no motion, racing, extra islands, huge waves, readable plate, text, or watermark. iPhone 15 main 1x travel photo, natural HDR, slightly imperfect handheld framing.

### P16 — Heritage Train L2
**Format:** 16:9 landscape  
**Location:** L2 near ST-L2-01, by the historic town T-02 and the central-west reservoir region.  
**Reference:** S-01_base.png plus atlas/current/human/rail_lines.geojson as a route guide; the route is proposed.  
**Edit:** Exposure -0.1 EV, contrast +12, highlights -15, warm sun with natural green tones; slight motion softness on the moving train.

**Prompt (English):**  
Create a wide 16:9 landscape travel photograph of one L2 heritage-styled electric train passing through the green countryside near ST-L2-01 and historic town T-02. Show the train from a safe public viewpoint beside the track, crossing a modest rural rail section bordered by trees, grass and low stone walls. Its body may recall a classic British railcar, but it must clearly be an electrically powered modern railway vehicle: no smoke, steam plume, open firebox, or active steam locomotive. Keep the landscape gentle and island-scaled, with wooded low hills rather than alpine peaks. Late-spring sun, iPhone 15 main 1x look, natural color and realistic track detail; a touch of motion softness on wheels is acceptable. No visible passengers, crowds, giant viaduct, overhead fantasy machinery, text, or logos.

### P17 — Inside Crystal Cave
**Format:** 9:16 vertical  
**Location:** N-02 Crystal Cave, viewed from the L1 tourist train near ST-L1-04.  
**Reference:** S-01_base.png for the cave’s western-highland setting. No detailed cave photograph exists in the atlas.  
**Edit:** Exposure -0.3 EV, contrast +14, highlights -25, cool shadows with a few warm practical cave lights, subtle glass reflections and mild grain.

**Prompt (English):**  
Create a vertical 9:16 photograph from inside a slowly moving L1 tourist train as it passes through N-02, the crystal cave in western Larpidia. Shoot through a clean carriage window: include a faint realistic reflection of the interior along one edge, while the cave remains the subject. Show a broad but believable natural cavern with dark limestone or volcanic-looking rock, modest mineral crystals embedded in the walls and carefully placed warm-white visitor lighting. The train follows a track around part of the cavern rather than flying through open space. Crystal surfaces should catch small highlights, not glow or form enormous jewel clusters. Use the iPhone 15 main 1x smartphone look, controlled low-light exposure, realistic texture and gentle motion softness outside the glass. No people, fantasy colors, giant geodes, text, or sci-fi tunnel.

### P18 — Metro L3 Station
**Format:** 16:9 landscape  
**Location:** ST-L3-05, East Waterfront station area in Larpington; L3 station design is not fully specified.  
**Reference:** S-03_base.png and capital_plan_base.png for the capital’s approximate urban position and block scale.  
**Edit:** Exposure -0.2 EV, contrast +16, highlights -20, neutral-cool lighting with a few warm accents; clean reflections, no excessive sharpening.

**Prompt (English):**  
Photograph a quiet, modern L3 regional metro platform at the proposed ST-L3-05 East Waterfront station in Larpington. Use a wide 16:9 composition looking down the platform toward a stopped, realistically proportioned electric metro train. Architecture is contemporary and functional, with durable tile, concrete, glass and discreet wayfinding forms, but no readable signs. Keep the station human-scaled and consistent with a compact island capital; no massive underground palace or futuristic holograms. The train doors are closed or just opening, with no visible passengers or staff. iPhone 15 main 1x documentary travel style, realistic station lighting, moderate contrast and subtle reflections. The shot is a proposed design interpretation because the atlas fixes the station location concept, not its final interior architecture. No text overlays, logos, crowd, or underwater glass walls.

### P19 — Empty Coastal Road at Night
**Format:** 9:16 vertical  
**Location:** RD-R1 in the rugged west/northwest, near the V-02 access area. The atlas says this road sometimes turns inland and uses short tunnels.  
**Reference:** S-01_base.png and S-01_oblique_NW.jpg for road/coast relation.  
**Edit:** Exposure -0.5 EV, contrast +22, highlights -20, cool blue-gray night shadows, small warm road lights, subtle natural sensor grain.

**Prompt (English):**  
Create a vertical 9:16 night photograph of an empty section of Larpidia’s coastal ring road RD-R1 in the rugged west/northwest. Choose a safe roadside viewpoint near the V-02 access area. The road curves through low forest and dark rock, with a faint glimpse of the Pacific through a natural opening if the angle permits. Respect the atlas concept that the road runs inland through short tunnels in the roughest northwest rather than clinging directly to a sheer cliff. No vehicle, cyclist or pedestrian is visible. A few practical road lights and reflective lane markings give depth without turning the road into a brightly lit highway. iPhone 15 main 1x low-light photo, slightly underexposed, realistic grain and controlled highlights; keep the road surface and trees readable. No dangerous edge, giant bridge, extra islands, city skyline, text, or dramatic light streaks.

### P20 — Paraland Marina
**Format:** 16:9 landscape  
**Location:** H-02 Paraland Marina and PL-05 Marina Village on Paraland’s west coast.  
**Reference:** S-02_base.png and S-02_oblique_strait.jpg for Paraland’s separate-island position and marina side.  
**Edit:** Exposure -0.1 EV, contrast +10, warm highlights, rich but believable sea blue, softened shadows; a few natural water glints.

**Prompt (English):**  
Photograph H-02, the proposed Paraland Marina, beside PL-05 Marina Village on the small separate island of Paraland. Make a wide 16:9 summer travel image from the public promenade: a handful of small leisure boats sit in a compact sheltered marina, with low stone quays, modest waterfront cafés and green island slopes behind them. Keep the marina small and local rather than a superyacht harbor; the island must feel limited in scale. Show open sea toward the northwest, consistent with the atlas guide, but do not add another large island on the horizon. Warm afternoon sun, natural reflections, iPhone 15 main 1x framing, realistic HDR and slightly softened shadows. No crowds, huge cruise liners, resort towers, unreadable signage in focus, or text overlay.


## PHOTO PROMPTS P21–P30

### P21 — Castle Ruins
**Format:** 9:16 vertical  
**Location:** PL-06, Ruin above the Old Town, near PL-01 on Paraland. Ruin existence is in the atlas; its exact position, name and design remain proposed.  
**Reference:** S-02_base.png for Paraland’s compact scale and the old-town/ruin relationship.  
**Edit:** Exposure -0.2 EV, contrast +14, highlights -18, slightly warm stone, muted greens; gentle atmospheric softness.

**Prompt (English):**  
Create a realistic vertical 9:16 travel photograph at PL-06, the proposed ruin above Paraland Old Town on the small island of Paraland. One visitor stands naturally on the grass-and-stone approach path in front of the ruin, full-length and small enough that the place remains the main subject. Show weathered local masonry, a partial old wall and one modest broken tower section, with softened stone edges, lichen and restrained vegetation. The structure should read clearly as a historic castle ruin without becoming a fantasy fortress. Include low island greenery and, if the view opens naturally, a subdued glimpse of the southern sea; do not invent dramatic cliffs or a second island. The exact architecture and camera point are not fixed in the atlas, so use a plausible, modest design. Late-afternoon coastal light, iPhone 15 main 1x, believable human proportions and focus, slight handheld imperfection. No costume, weapon, medieval scene, extra people, text, or CGI.

### P22 — Hotel Balcony Morning
**Format:** 9:16 vertical  
**Location:** PL-03 South Resorts, Paraland. A specific hotel and balcony are not individually identified in the registry.  
**Reference:** S-02_base.png and S-02_oblique_SW.jpg for the southern resort area and island scale.  
**Edit:** Exposure -0.1 EV, contrast +8, warm morning highlights, rich but natural sea blue, soft shadows; mild glass reflection.

**Prompt (English):**  
Photograph a quiet breakfast on a hotel balcony in the PL-03 southern resort area of Paraland. The hotel itself and balcony are a plausible visual interpretation, not a named atlas building. In a vertical 9:16 frame, place a small breakfast tray with coffee, fruit and bread in the foreground, a simple balcony rail at mid-frame, and a calm view toward the southwest sea beyond low green island terrain. Let early sunlight warm the table and nearby wall while the sea remains a believable blue. Keep the architecture low-rise and restrained, consistent with a small resort island; no hotel tower or giant resort complex. No people are visible. iPhone 15 main 1x travel snapshot, natural reflections in the balcony glass, slightly imperfect framing and subtle HDR. No readable menus, logos, extra islands, or text overlays.

### P23 — Beach Restaurant After Sunset
**Format:** 9:16 vertical  
**Location:** PL-03 South Resorts near B-05 on Paraland’s southern shore; exact restaurant is not registered.  
**Reference:** S-02_base.png and S-02_oblique_SW.jpg for the south/coastal resort zone.  
**Edit:** Exposure -0.3 EV, contrast +14, warm practical lights against cool blue dusk, highlights -20, slight low-light grain.

**Prompt (English):**  
Create a vertical 9:16 evening travel photograph of a small open-air restaurant terrace in the PL-03 southern resort area near B-05 on Paraland. The specific restaurant is an illustrative local venue, not a registered business. Frame an empty table, simple timber or stone details and a few warm practical lamps in the foreground; beyond the terrace, show a narrow darkening strip of southern sea and a quiet beach edge. Keep the terrace modest, with low island landscaping and no resort towers. The mood is calm just after sunset, with natural blue-hour color and warm light reflected on glassware. iPhone 15 main 1x smartphone HDR, lowered exposure, controlled highlights and subtle grain. No visible people, readable signs, bright neon, party scene, fantasy coastline, or text overlay.

### P24 — Hidden Beach Trail
**Format:** 9:16 vertical  
**Location:** TR-PL1, the proposed walking loop through eastern Paraland’s forests, leading toward B-06 on the east coast.  
**Reference:** S-02_base.png and S-02_oblique_SW.jpg for Paraland’s east forest and beach side.  
**Edit:** Exposure -0.1 EV, contrast +10, highlights -20, slightly warm sun flecks, natural greens and sea color; small lens flare is acceptable.

**Prompt (English):**  
Photograph a narrow footpath on TR-PL1, the eastern forest walking loop on Paraland, as it descends through trees toward the small sandy cove at B-06. Use a vertical 9:16 eye-level iPhone 15 main 1x composition. In the foreground, show leaf litter, roots, grasses and a worn but safe trail; the middle distance opens through coastal trees to a modest crescent of pale sand and calm water. Keep the cove small and local, on Paraland’s eastern side, with low greenery and no built resort frontage. Let warm sunlight break through leaves without over-saturating the scene. No people, signs, extra islands, dramatic cliffs, or tropical jungle exaggeration. Natural HDR, believable foliage detail, slightly casual framing and a soft sea haze.

### P25 — Summer Water Park
**Format:** 16:9 landscape  
**Location:** PL-04 Paraland Aquapark, in the southern resort area near PL-03 and B-05.  
**Reference:** S-02_base.png and S-02_oblique_SW.jpg for its broad southern placement.  
**Edit:** Exposure -0.1 EV, contrast +10, warm highlights, lively but believable pool blues, slightly softened shadows; no heavy saturation.

**Prompt (English):**  
Create a wide 16:9 summer photograph of PL-04, the separate aquapark attraction on Paraland. Show a few realistic water slides, a modest pool complex, green planting and low service buildings in a compact island setting. The water park is completely empty of people, with clean but used surfaces, natural reflections and calm pool water. Keep the attraction substantial enough to read as an aquapark but not a vast theme-park metropolis; no towering rides, oversized resort skyline or second large island. Bright summer daylight, iPhone 15 main 1x travel-photo look, realistic smartphone HDR, warm highlights and rich but credible sea-and-pool colors. No text, branding, mascots, crowds, or fantasy structures.

### P26 — Green Technology District
**Format:** 16:9 landscape  
**Location:** I-01 Green Industrial Zone on Larpidia’s eastern/northeastern lowland.  
**Reference:** S-01_base.png for the industrial zone’s eastern placement and the flat lowland context.  
**Edit:** Exposure -0.1 EV, contrast +12, highlights -15, neutral daylight with slightly cool shadows, moderate saturation; clear material texture.

**Prompt (English):**  
Photograph the proposed industrial area I-01 in eastern Larpidia as a believable wide 16:9 documentary travel image. Show one low-rise modern production building with practical loading access, tree shade, planted strips and a small landscaped pedestrian edge. Let other low industrial roofs and green corridors recede across a flat lowland; do not place mountain ridges inside the district. The scene should suggest thoughtful environmental design through trees, daylight, clean operations and compact massing, not through glowing technology or a futuristic city. No people or moving vehicles. iPhone 15 main 1x, natural overcast-to-sunlit conditions, realistic HDR, moderate contrast and slightly muted colors. Do not show smokestacks, toxic discharge, huge warehouses, skyscrapers, readable company names, text, or watermarks.

### P27 — Algae Production Facility
**Format:** 16:9 landscape  
**Location:** I-02 Seaweed Processing Plant, proposed facility in the eastern lowland near the export harbor.  
**Reference:** S-01_base.png for the industrial area’s position; no detailed interior reference exists.  
**Edit:** Exposure -0.2 EV, contrast +12, highlights -20, neutral-cool white balance with restrained green tones; no artificial glow.

**Prompt (English):**  
Create a photorealistic wide 16:9 interior photograph inside the proposed I-02 seaweed-processing facility in eastern Larpidia. Show a clean, practical industrial room with stainless-steel tanks, orderly pipes, valves, a few covered processing vessels and a small section of translucent cultivation equipment containing naturally olive-green microalgae. The operation should look like real food- or bio-material processing, not a laboratory spaceship. Include non-slip flooring, washable wall surfaces and realistic utility lighting. No people are visible, and there are no readable labels, logos, or invented statistics. The interior design is a plausible proposal because the atlas identifies the facility location but does not define its building interior. iPhone 15 main 1x documentary photo, balanced exposure, subtle cool shadows and visible metal texture. No neon-green liquid, glowing tanks, smoke, or CGI.

### P28 — Rainy Japanese Café
**Format:** 9:16 vertical  
**Location:** T-04 Ōru Maito in northern Larpidia; exact café interior is not registered.  
**Reference:** S-01_base.png for the town’s northern position and small-town scale.  
**Edit:** Exposure -0.3 EV, contrast +12, warm table highlights against cool rainy window light, muted greens, gentle grain.

**Prompt (English):**  
Photograph a quiet table inside a small café in T-04 Ōru Maito on a rainy day. The café is a plausible venue within the registered northern town, not a fixed atlas interior. In a vertical 9:16 composition, place a ceramic matcha drink and a small traditional-style cake or pastry sharply in the foreground. Beyond them, a rain-streaked window shows a narrow town street with compact brick-and-stone buildings and restrained Japanese-influenced details. Keep the exterior small-town and believable, with no pagoda or oversized neon signage. No people are visible. Use an iPhone 15 main 1x close travel-photo perspective, warm interior light against cool window tones, realistic reflections, slightly lowered exposure and subtle low-light grain. No legible text, logos, or watermarks.

### P29 — Historic Square at Blue Hour
**Format:** 16:9 landscape  
**Location:** CP-SQ01, the proposed Square of the Four, in C-01 Larpington.  
**Reference:** S-03_oblique_S.jpg and capital_plan_base.png for square/civic-core placement only.  
**Edit:** Exposure -0.3 EV, contrast +16, highlights -20, deep blue sky, warm windows, subdued saturation; slight atmospheric softness.

**Prompt (English):**  
Create a wide 16:9 blue-hour photograph of CP-SQ01, the proposed Square of the Four in Larpington’s civic center. Frame the empty square from one corner so its paving leads toward compact brick-and-stone civic buildings with warm windows. Keep the architecture human-scaled and consistent with the English/Welsh-influenced capital, with discreet contemporary Japanese infrastructure details rather than a themed mixture. Distant low western hills may appear only faintly if the street opening allows; the square is not on the coast. No people, cars, oversized parliament, skyscrapers, flags, readable signs, or invented monuments. iPhone 15 main 1x travel photography, realistic blue-hour exposure, warm practical lights, controlled highlights, slightly imperfect handheld composition and natural low-light grain.

### P30 — Coast From a Train Window
**Format:** 16:9 landscape  
**Location:** L2 near ST-L2-13, with nearby T-06, HV-02, BAY-N2 and B-03; the photo guide indicates the sea to the south.  
**Reference:** S-01_base.png and atlas/current/human/rail_lines.geojson for broad route context; route details remain proposed.  
**Edit:** Exposure -0.2 EV, contrast +10, highlights -20, natural greens and blue sea, subtle window reflections and mild motion blur outside.

**Prompt (English):**  
Create a wide 16:9 travel photograph from a passenger seat inside an L2 electric train near ST-L2-13 on northern Larpidia’s coastal side. Shoot through the train window toward the south, where the atlas guide places the sea. Show a close strip of green lowland and coastal vegetation, then a modest blue bay beyond it; let nearby trees have slight natural motion blur while the horizon and distant coast remain legible. Include faint reflections of the carriage window along one edge, but keep the landscape dominant. The train is an ordinary electrically powered surface railway; no steam or smoke. iPhone 15 main 1x snapshot, realistic HDR, softly edited color and imperfect travel framing. No visible passengers, extra islands, high mountains, text, or graphic overlays.

## VIDEO COLLECTION INDEX

| ID | Scene | Duration | Format | Atlas location |
|---|---|---:|---:|---|
| V01 | Mountain 180° Turn | 8 seconds | 9:16 | M-01 |
| V02 | Entering the Old Church | 8 seconds | 9:16 | C-01, CP-B07, CP-UL04 |
| V03 | Waterfall Railway Pass | 8 seconds | 16:9 | N-03, ST-L1-03, L1 |
| V04 | Walking Through Old Larpington | 8 seconds | 9:16 | C-01, CP-UL04 |
| V05 | Midnight Jesko Walkaround | 8 seconds | 9:16 | V-04, C-01 |
| V06 | Paraland Marina Walk | 8 seconds | 16:9 | H-02, PL-05 |
| V07 | Ocean Cliffs | 8 seconds | 16:9 | N-01, CAPE-W |
| V08 | L3 Train Arriving | 8 seconds | 9:16 | L3, ST-L3-05 |
| V09 | Ōru Maito Rainy Night | 8 seconds | 9:16 | T-04 |
| V10 | Paraland Castle Ruins | 8 seconds | 16:9 | PL-06, PL-01 |

## VIDEO PROMPTS V01–V05

### V01 — Mountain 180° Turn
**Duration:** 8 seconds  
**Format:** 9:16 vertical  
**Location:** Trail viewpoint near M-01 in the western highlands; precise camera point and ocean line-of-sight are not verified.  
**Reference:** S-01_base.png for broad island geography; attach if available.

**Prompt (English):**  
Generate one continuous 8-second vertical 9:16 smartphone travel video at a safe trail viewpoint near M-01, the modelled 560 m summit in western Larpidia. Opening composition: one hiker stands naturally at the left edge of the frame beside a narrow path with a few melting snow patches, stones and green grass; forested low slopes fill the view. The camera makes one slow, smooth 180-degree turn from left to right around the operator’s standing position, with mild natural handheld sway but no cut, zoom, teleportation or sudden speed change. During the turn, reveal layered green slopes and a cautious distant glimpse of blue Pacific only where a plausible gap in terrain permits it. End on the path and open coastal horizon, keeping the mountains modest and the island local in scale. Early-spring daylight, slightly cool edited color, stable exposure and subtle smartphone HDR. Keep the hiker’s body, trail, terrain and horizon consistent throughout. Natural wind and faint birds only; no music, speech, titles, or extra people.

### V02 — Entering the Old Church
**Duration:** 8 seconds  
**Format:** 9:16 vertical  
**Location:** CP-B07, the working-name historic church near CP-UL04 and CP-SQ04 in C-01 Larpington.  
**Reference:** S-03_oblique_S.jpg for the city area; upload a church image only if one is available—none is defined by the atlas.

**Prompt (English):**  
Create a single unbroken 8-second vertical 9:16 handheld video in the old center of Larpington, approaching the modest historic church CP-B07 from the Church Street area CP-UL04. Opening composition: the church’s weathered brick-and-stone front is visible beyond a quiet paved lane. The camera walks forward slowly for several steps, rises slightly with natural footfall, reaches an already open wooden doorway, and passes through it without crossing solid walls. End just inside the entrance, looking toward a dim, believable church interior where soft daylight falls through a few restrained stained-glass panels. Keep the same door, masonry, window positions and interior architecture throughout the continuous move; no morphing, cuts or camera jumps. Warm late-afternoon exterior light transitions naturally to a darker interior with stable exposure. Slightly warm, edited travel-video color, mild hand sway. No people, oversized cathedral scale, fantasy ornament, readable text, music or narration. Natural footsteps and faint room ambience only.

### V03 — Waterfall Railway Pass
**Duration:** 8 seconds  
**Format:** 16:9 landscape  
**Location:** Safe viewing platform at ST-L1-03 beside N-03 Larp Falls. The exact L1 alignment is proposed.  
**Reference:** S-01_oblique_NW.jpg and S-01_base.png for local region; neither is a ground-level photo.

**Prompt (English):**  
Generate a continuous 8-second 16:9 travel video from a safe viewing platform beside N-03, Larp Falls, near ST-L1-03. Opening composition is a wide, steady view of the modest forest waterfall and its rocky stream, with a realistic L1 track visible at a safe distance. A compact scenic electric train enters slowly from the left, passes through the middle ground beside the falls, and exits to the right; the camera makes only a small smooth pan to follow it, then settles back on the waterfall. Keep the stream, rock formations, track, train design and surrounding low forest unchanged for the full clip. Use natural overcast daylight, slightly dark edited greens, controlled water highlights and realistic train motion with no jerking or wheel deformation. Include soft water noise and a restrained electric rail hum only. No steam, smoke, people, dramatic viaduct, cuts, text, music, or changing scenery.

### V04 — Walking Through Old Larpington
**Duration:** 8 seconds  
**Format:** 9:16 vertical  
**Location:** C-01 Larpington, along the proposed CP-UL04 Church Street area.  
**Reference:** S-03_base.png for broad capital layout. Exact street façades are not fixed.

**Prompt (English):**  
Create one continuous 8-second vertical 9:16 handheld video walking slowly along a quiet historic lane in C-01 Larpington near CP-UL04. Start with wet stone paving and a brick wall close in the foreground; move forward at an unhurried walking pace past compact English/Welsh-influenced brick and stone houses, modest garden details and one understated café frontage. Let warm window light and damp paving reflections appear naturally. End with the street opening toward a small square, without revealing a harbor or mountains in the immediate street. Keep buildings, doors and window positions stable during the whole shot; no cuts, speed ramps, warping or sudden exposure shifts. iPhone 15 main 1x feel, slight footstep sway, warm historic-street grade with cool wet shadows. No pedestrians or readable signage. Natural footsteps and faint rain drip only; no music or voiceover.

### V05 — Midnight Jesko Walkaround
**Duration:** 8 seconds  
**Format:** 9:16 vertical  
**Location:** A safe paved turnout near V-04 on the southeastern peninsula; distant Larpington lights are a plausible view, exact parking point is proposed.  
**Reference:** S-01_base.png and S-03_oblique_S.jpg for broad geography.

**Prompt (English):**  
Create an 8-second vertical 9:16 nighttime phone video of a stationary black-and-gold Koenigsegg Jesko at a safe paved scenic turnout near V-04. The car is fully parked behind a sensible roadside barrier and well away from any edge. Opening frame: low front three-quarter view of the car, with dark landscape and a modest cluster of Larpington lights far to the northwest. The camera operator walks a slow, smooth arc of about 120 degrees from the front toward the side, keeping the car in focus and the distant lights softly visible. End on a side-rear three-quarter view; the car never moves, changes shape, changes paint, or gains/loses parts. Use realistic phone exposure, warm practical lights, cool night shadows, restrained reflections and mild sensor grain. No driver, people, racing, engine revving, burnout, cuts, changing plates, text, music or narration. Ambient night air only.


### V06 — Paraland Marina Walk
**Duration:** 8 seconds  
**Format:** 16:9 landscape  
**Location:** H-02 Paraland Marina and PL-05 Marina Village on the west coast of Paraland.  
**Reference:** S-02_base.png and S-02_oblique_strait.jpg.

**Prompt (English):**  
Create one continuous 8-second 16:9 handheld travel video walking along the public edge of H-02 Paraland Marina beside PL-05 Marina Village. Start close to gently rippling water and the sterns of two small moored boats. Walk slowly forward along the low stone promenade, passing simple railings and a modest café frontage, then finish with a wider view across the compact marina and low green island interior. Keep the harbor small, consistent and calm; boat ropes and water move naturally, while every quay, building and boat remains the same throughout. Bright summer afternoon with warm highlights, believable sea-blue color and stable smartphone exposure. iPhone 15 main 1x, mild natural hand sway, no gimbal-perfect motion. No people, large yachts, cruise ships, extra islands, cuts, teleportation, changing architecture, readable signs, music or narration. Natural water, gulls and soft harbor ambience only.

### V07 — Ocean Cliffs
**Duration:** 8 seconds  
**Format:** 16:9 landscape  
**Location:** N-01 and CAPE-W, the safe rocky lookout on Larpidia’s west coast.  
**Reference:** S-01_base.png or S-01_oblique_NW.jpg for the west-coast geography.

**Prompt (English):**  
Generate an 8-second continuous 16:9 smartphone video from the safe fenced lookout at N-01 near CAPE-W on Larpidia’s rocky western coast. Opening frame shows the marked path, grass and safety rail in the foreground, with ocean beyond. The camera slides gently sideways along the public viewing area, then pans a little toward the west to reveal low dark cliffs and waves breaking against rocks well below. End on a steady view of the Pacific and the rugged shoreline. Keep the camera safely behind the rail; no one approaches the edge. Water movement should remain natural and consistent, without giant storm waves. Soft late-afternoon light, slightly cool shadows, restrained contrast, realistic phone stabilization with faint handheld movement. Include wind and surf only. No beach below the northwestern cliffs, extra island, cut, camera jump, text, music, or narration.

### V08 — L3 Train Arriving
**Duration:** 8 seconds  
**Format:** 9:16 vertical  
**Location:** ST-L3-05 East Waterfront station area in Larpington; detailed architecture remains proposed.  
**Reference:** S-03_base.png and capital_plan_base.png for the city location and scale.

**Prompt (English):**  
Create one continuous 8-second vertical 9:16 video of a modern electric L3 train arriving at the proposed ST-L3-05 East Waterfront station in Larpington. Opening composition: a quiet, human-scaled underground platform seen from behind the safety line, with a tunnel at the far end and clean, practical tile and concrete surfaces. The train’s headlights appear in the tunnel, then one realistic metro set enters at moderate speed, slows smoothly, stops with its doors aligned to the platform and opens them at the end. The camera remains nearly fixed with only slight handheld movement. Keep platform geometry, train shape, lighting and door positions consistent; no cuts, warping, extra train cars appearing, or sudden exposure change. Neutral-cool station light, moderate edited contrast, realistic reflections. Natural rail hum and brake sound only. No passengers, readable signs, futuristic screens, underwater glass walls, text overlays, music, or voiceover.

### V09 — Ōru Maito Rainy Night
**Duration:** 8 seconds  
**Format:** 9:16 vertical  
**Location:** T-04 Ōru Maito, a small northern town; exact street alignment is not fixed.  
**Reference:** S-01_base.png for the north-of-island town context.

**Prompt (English):**  
Create an 8-second vertical 9:16 handheld phone video walking slowly through a quiet lane in T-04 Ōru Maito on a rainy night. Start with close reflections of warm shop lights on wet pavement, then move forward three or four unhurried steps past compact brick-and-stone buildings with subtle Japanese-influenced details. End with the lane gently opening toward a small junction; keep the town low-rise and intimate. Show rain falling lightly and water dripping from eaves, with no visible people or moving cars. The camera has mild natural hand sway and realistic autofocus behavior, not a cinematic tracking rig. Use cool blue-gray shadows, warm practical lights, stable exposure and a little low-light grain. Keep buildings and storefronts unchanged across the shot. No neon canyon, pagoda, legible text, cuts, changing weather, music, or narration. Natural rain and distant town ambience only.

### V10 — Paraland Castle Ruins
**Duration:** 8 seconds  
**Format:** 16:9 landscape  
**Location:** PL-06 Ruin above the Old Town, near PL-01 on Paraland. Exact ruin design and camera point are proposed.  
**Reference:** S-02_base.png for island scale and the old-town/ruin relation.

**Prompt (English):**  
Generate one continuous 8-second 16:9 travel video at PL-06, the proposed ruin above Paraland Old Town. Opening composition: one visitor stands still in the grass at the left foreground as a scale reference, with a weathered stone wall and modest broken tower section behind them. The camera makes a slow, steady forward move of a few paces toward the ruin while keeping the person secondary and the masonry as the main subject. End with a closer view of the same wall and tower, allowing a restrained glimpse of southern sea through an opening only if the terrain permits it. Keep the exact stonework, wall outline, person, clothing and vegetation consistent throughout; no morphing, cuts, teleportation or change of weather. Soft late-afternoon light, slightly warm stone, muted greens, subtle handheld movement and realistic exposure. Natural breeze and distant seabirds only. No costumes, weapons, medieval army, fantasy fortress, extra people, text, music or narration.

## REFERENCE FILE MANIFEST

All paths below are relative to the project root. They refer to local files; attach the relevant image to the generator conversation when prompted. The generator must not assume it can open these paths itself. Every atlas render listed here is procedural/simulated, not real satellite or photographic evidence. Use it only as a relative geography guide.

| Reference file | Use for scenes | What it can and cannot guide |
|---|---|---|
| atlas/current/renders/S-01_base.png | P01–P19, P26–P28, P30; V01, V03–V05, V07, V09 | Main-island outline, broad placement of terrain, towns, roads and coast. Nadir map only; it cannot prove a ground-level view or building design. |
| atlas/current/renders/S-01_oblique_NW.jpg | P03–P06, P15, P19; V03, V07 | Simulated oblique view of northwestern cliffs, forests and western highlands. Do not treat it as an actual photograph or exact camera viewshed. |
| atlas/current/renders/S-01_oblique_S.jpg | P08–P09, P11–P14, P18, P29; V02, V04–V05, V08 | Simulated broad placement of Larpington, southern harbor and capital landform; individual buildings are illustrative. |
| atlas/current/renders/S-02_base.png | P20–P25; V06, V10 | Paraland outline, resort/forest regions and approximate location of old town, castle, ruin and beaches. Does not define the exact ruin appearance. |
| atlas/current/renders/S-02_oblique_SW.jpg | P22–P25 | Simulated southern resort side, east forest and beach relationships. Not ground-level photography. |
| atlas/current/renders/S-02_oblique_strait.jpg | P20; V06 | Simulated relation of Paraland marina to the strait and main island. |
| atlas/current/renders/S-03_base.png | P08–P09, P11–P14, P18, P29; V02, V04–V05, V08 | Simulated capital footprint and city blocks; not reliable facade detail. |
| atlas/current/renders/S-03_oblique_S.jpg | P08–P09, P11–P14, P29; V02, V04–V05 | Simulated southern view of capital and old harbor. Buildings are illustrative masses, not established architecture. |
| atlas/current/renders/S-03_oblique_W.jpg | P13, P29 | Simulated west-to-east view along the capital civic core. Use only for approximate layout. |
| atlas/current/capital/capital_plan_base.png | P08–P09, P11, P13, P18, P29; V02, V04, V08 | Schematic plan layout and proposed civic/street locations; it is not a real photograph and has illustrative urban details. |
| atlas/current/registry/photo_guide.csv | Any requested location-guide text | Upload only if the model can use supporting text documents. It carries the per-location view, nearby features and avoid notes. |
| atlas/current/human/rail_lines.geojson | P04, P16–P18, P30; V03, V08 | Optional route geometry context if the generator can interpret GeoJSON. L1/L2/L3 alignment remains proposed; this file is not a visual image. |
| atlas/current/relief/hillshade_20m.png | P01–P07; V01, V03, V07 | Optional simulated terrain shading for broad relief relationships. It cannot establish exact visibility from a camera point. |

For exact scene references, follow the Reference line on the selected prompt first. If a listed file is missing from the conversation, ask the user to upload that exact file before claiming to use it. A scene can still be generated from its full written prompt if the user prefers a text-only interpretation.

## NOTES FOR THE USER

- Nahraj tento Markdown soubor do jedné konverzace s generátorem. Pak napiš „START FOTKY“ a postupuj příkazem „DALŠÍ FOTKA“. Video začni příkazem „START VIDEA“.
- Každý příkaz vytvoří právě jeden výstup. Přímé příkazy „FOTKA P21“ nebo „VIDEO V10“ vyberou konkrétní scénu.
- Pro přesnější geografické vodítko připoj k dané scéně i referenční obrázek uvedený v jejím promptu nebo v manifestu. Samotný soubor Markdown lokální obrázky nepřenáší.
- Pořadí generování si AI pamatuje v rámci dané konverzace. V nové konverzaci znovu použij příkaz START.
- Všechny lokality jsou součástí fiktivního geografického modelu. Některé body, názvy, návrhy budov, interiéry a přesné polohy zůstávají návrhové; text ani atlasové reference nezaručují pixelově přesnou geografii.


