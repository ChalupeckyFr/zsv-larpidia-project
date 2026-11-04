# LARPIDIA — COMPLETE THE PUBLIC ATLAS, PLACE STORIES, 2D CARTOGRAPHY, GALLERY & BRANDING

**Author-approved implementation brief for Codex. Written in English for engineering clarity; ALL visitor-facing UI and descriptions must be natural Czech.**

**Priority: real result in the existing VS Code Live Server workflow, not just a passing export check.**

## 0. Read this first: this supersedes the narrow debugging prompt

The author has confirmed that a small earlier debugging prompt DID remove `NÁVRH · v1.0-draft` and some status badges from the atlas. That was only a successful proof that the active viewer can be edited. **Do not revert that success.** However, the debug patch also reduced formerly rich place details to a bleak card such as:

> **Železniční trať · centrální nížině**  
> Železniční trať v centrální nížině.  
> Zobrazit na mapě

This is **unacceptable as the finished product**: the heading is ungrammatical, the description tautological and almost all interesting real map/place context disappeared. Another screenshot shows giant oval settlement blobs around Larpington and generic POIs. The author wants the opposite: a **beautiful, credible visitor atlas with rich locally grounded information**, no visible production metadata, every selectable feature understandable, a more realistic 2D map, and a functioning gallery with a discreet author-only media status control.

**This is a complete PRODUCT/CONTENT pass, not another single-string deletion.** Follow the phased plan, but do not declare it complete if only text labels changed. Treat screenshots and new user instructions as higher-priority evidence than the previous completion reports.

### 0.1 Canon and approved decisions

Inspect the EXISTING repository, `README.md`, current root `index.html` and its real routes/iframes, and if present:

- `references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md` (immutable archive; all 102 decisions remain in force)
- `references/LARPIDIA_CODEX_SCHVALENE_OPRAVY_PO_AUDITU_v1.md`
- `references/LARPIDIA_CODEX_PUBLIC_ATLAS_GALLERY_FIX_EN.md` (prior complete UX brief; this new specification refines and supersedes it where different)
- `docs/LARPIDIA_PUBLIC_CONTENT_AUDIT.md`, `docs/LARPIDIA_ATLAS_SEARCH_REVIEW.md`
- `docs/LARPIDIA_PUBLIC_ATLAS_GALLERY_REPAIR_REPORT.md`
- `docs/LARPIDIA_REMAINING_CONTENT_DECISIONS.md`
- Existing atlas, capital, media and encyclopedia registries. Read **only relevant canon excerpts** rather than repeatedly consuming the entire 334 KB file.

Author decisions already approved: **all 159 atlas records and 662 city-plan records stay in data and on the map**; a single discreet orientation disclaimer is acceptable; L1 and L2 railway lines operate; L3 urban segment operates but the undersea Paraland connection is still under construction; school week 5 days, ≤2 early starts before 09:00; Larpington's main history museum is open while the Paraland exhibition is unfinished; basic pension for all Larpidian citizens aged ≥65 independent of work history; highest mountain **approximately 560 m**; rich mobile-friendly atlas search. **There is NO parliament.** Capital is **Larpington**, with traditional quarters Chalupecká, Kynčlova, Klimečkova, Žemličkova and a fifth creative/university-oriented urban zone; the separate campus town near Larpington is NOT one of its boroughs.

**NEW AUTHOR OVERRIDE (exact spelling required):** the place currently labelled approximately `Cimpřichovo Hradiště` is **`Cimprlichovo Hradiště`** (C-i-m-p-r-l-i-c-h-o-v-o; `Hradiště` retains diacritics). Find the original place by its stable internal ID / current registry value; update its **Czech public display name** consistently in every active atlas registry, embedded data generation, map label, search, gallery/article crosslink if relevant. Preserve the old spelling as an *internal searchable alias* for compatibility (not displayed). English/Japanese transliterations should be checked; do not treat guessed translations as authoritative. This rename is explicitly approved by the author. Do not alter other canonical names without grounds.

### 0.2 Source / runtime / output

The author's ordinary preview is: **VS Code → right-click ROOT `index.html` → Open with Live Server → navigate via the regular website**. Make THAT experience the source of truth and fix it as well as the public export; do not implement only in an exported HTML copy. Trace real iframe/source routes, investigate duplicated inline JSON versus JSON registries, and avoid divergent manually maintained sources. Preserve public URLs and existing functioning features. No framework migration, Git commit or push. Preserve existing 3D geometry and associated source files byte-for-byte; 3D rework is a later, separate project.

---

## 1. Editorial and creative strategy: rich, place-specific content, NOT generic placeholders

**Division of responsibilities:** This brief provides the creative direction, naming grammar, example candidate names, tone, sample finished cards and acceptance tests. **You, Codex, must inspect the actual spatial registries and assign or generate appropriate names and text to the correct existing features.** You know their `type`, coordinates, region, island, neighbors and spatial relations in the repo. Do NOT randomly attach one of the example names below to an arbitrary feature. New literary names are *fictional atlas editorial labels*, not an alteration of constitutional history. Log all newly introduced proper names in a single editable internal name registry and distinguish author-approved names from editorial additions.

### 1.1 Every meaningful selectable feature needs human-readable identity

For all **159 atlas places**, and for all **662 selectable Larpington plan objects**, prepare a public representation. Preserve IDs internally, but never show them in the visitor-facing title, detail, result row, map label, tooltip or visible URL slug when avoidable. Every selectable feature needs:

- a sensible readable **Czech display name**, respecting existing canon/approved names;
- a distinct, natural one-sentence description conveying *what the place is and where it belongs*; never repeat the title in different words;
- meaningful public detail appropriate to the object's actual type (landscape, location, attractions, transport connections, viewpoints, neighborhood context); do not fabricate numerical capacities, exact travel times, ancient dates, businesses, biographies or completed constructions;
- where possible, linked neighboring places **resolved by actual names**, and actual directions/distances computed only from verified atlas coordinates;
- gracefully compact presentation for mundane buildings/utility pieces. **Do not fabricate a grand historical monument for every one of 662 houses.** A normal house may be called `Dům u [existing street name]`, `Nárožní dům v [existing district]`, `Dvorní dům u [existing established landmark]`; make labels distinguishable using real nearby geometry/streets rather than exposing `CP-...` codes. If such contextual anchor doesn't exist, assign a modest locally grounded descriptive name and document the naming inference privately.

For generic map objects currently named `Bod zájmu`, `POI`, `zajímavost`, `stanoviště`, `místo`, `objekt`, etc., **do not merely remove the marker**. Reclassify from registry geometry/environment/evidence into plausible landscape and visitor features such as **vyhlídka, rozcestí, studánka, stezka, lávka, odpočívadlo, menší náměstí, městská průchodová ulička, pobřežní výhled, zastávka, přírodní zákoutí**. Use sensible placement: a spring near a physically appropriate watercourse/terrain, a viewpoint on a hill/coast or meaningful vista, a crossroads at actual intersecting paths, a waterfront promenade on the coast, not on a ridge. Preserve the location and geometry; the *classification must fit*, or retain a neutral name and flag it privately. Don't invent 100 identical viewpoints.

### 1.2 In-world Czech toponymy: curated candidate bank, not a blind rename list

These are **creative suggestions** for existing correctly located anonymous features ONLY; they are not approved canonical names, not guaranteed to exist, and must not overwrite meaningful established names. Adapt/decline based on actual terrain, neighboring places, historical style and duplicates. The user wants memorable, culturally coherent atlas names rather than `Bod zájmu 37`.

| Terrain / feature type | Candidate public names in Czech | Suitable short factual/evocative description (adapt to verified place) |
|---|---|---|
| Ridge viewpoint | `Vyhlídka Nad přehradou` | `Z okraje horského svahu se otevírá pohled na vodní nádrž a navazující údolí.` |
| Ridge viewpoint | `Větrná vyhlídka` | `Otevřené místo na hřebeni, odkud lze sledovat proměny horské krajiny.` |
| Ridge viewpoint | `Skalní okno` | `Úzké vyhlídkové místo mezi skalními stěnami.` **Only if geology suggests it.** |
| Water/woods | `Studánka U kapradin` | `Prameniště při lesní stezce, přirozená zastávka cestou údolím.` **Only where water source is plausible.** |
| Water/woods | `Mechová studánka` | `Tiché místo na okraji stinného lesa, navazující na pěší trasu.` |
| Forest junction | `Rozcestí Pod borovicemi` | `Setkávají se zde lesní pěšiny směřující k [actual mapped places].` |
| Forest junction | `Rozcestí Tří stezek` | `Orientační bod na křižovatce turistických tras.` **Only where 3 paths meet.** |
| Forest path | `Javorová stezka` | `Krátký lesní úsek spojující [mapped places].` **Use only if vegetation supports a name.** |
| Forest/rest stop | `Odpočívadlo U kamenné zídky` | `Klidná zastávka na pěší trase za okrajem zástavby.` |
| Waterfall surroundings | `Vyhlídka Pod vodopádem` | `Místo na značené trase s výhledem k vodopádové stěně.` **Do not relocate real protected paths.** |
| Dam shore | `Přehradní vyhlídka` | `Pohled na hladinu nádrže a protilehlý horský svah.` |
| Coastal point | `Vyhlídka Na průliv` | `Výhled přes vodu k druhému ostrovu.` **Only if visible by actual orientation.** |
| Coastal point | `Sluneční mys` | `Nízký pobřežní výběžek s otevřeným výhledem na moře.` |
| Coastal path | `Stezka Nad zátokou` | `Pobřežní chodník sledující okraj [real mapped bay].` |
| Beach access | `Schody k zátoce` | `Pěší přístup k menšímu pobřežnímu úseku.` **Only if path/steps exist in geometry.** |
| Paraland | `Vyhlídka Na hlavní ostrov` | `Pohled přes krátký průliv na pobřeží hlavního ostrova.` |
| Paraland | `Zahradní promenáda` | `Klidnější pěší spojení mezi pobřežními částmi ostrova.` **Only where plausible.** |
| Urban passage | `Kamenná pasáž` | `Pěší průchod mezi bloky starší městské zástavby.` |
| Urban passage | `Ulička Pod schody` | `Úzká spojka mezi dvěma úrovněmi městských ulic.` **Only with grade difference.** |
| Urban square | `Náměstí U kašny` | `Menší veřejný prostor mezi městskými domy.` **Only if existing fountain or plausible from data; otherwise another name.** |
| Urban courtyard | `Tichý dvůr` | `Chráněné vnitroblokové zákoutí s navazujícími průchody.` |
| Old-town lookout | `Vyhlídka Nad střechami` | `Z vyvýšeného okraje čtvrti je vidět hustá zástavba Larpingtonu.` |
| Market or civic area | `Tržní průchod` | `Pěší spojení mezi obchodní ulicí a malým veřejným prostorem.` **Only if land use supports it.** |
| Transport node | `Zastávka U nábřeží` | `Místo nástupu na [actually operating line] při pobřežní komunikaci.` |
| Rail bridge | `Viadukt Nad údolím` | `Železniční úsek překonávající [actual mapped valley/watercourse].` **Only if bridge geometry present.** |
| Rail viewpoint | `Železniční vyhlídka` | `Místo s výhledem na trať a okolní krajinu.` **Not a track itself.** |
| Riverside footpath | `Nábřežní stezka` | `Pěší cesta sledující skutečný břeh vodního toku.` |

**Style guardrails:** Local names should sound like Czech-language geographic names or established bilingual local usage. Avoid randomly Japanese-sounding names for everything, theme-park marketing, absurdly poetic constructions, invented famous people, fake ancestral dynasties, and real-world landmark copies. Avoid repeating `Sluneční`, `Zelený` or `U starého...` across dozens of entries. An existing approved name ALWAYS outranks a candidate. Don't overname ordinary infrastructure or create hundreds of unnecessary canonical landmarks.

### 1.3 Editable name and content layer (important for future photo game)

Create or extend a **single structured editor-owned enrichment file** (use existing data schema when possible; e.g. `content/larpidia/atlas_places_editorial.json`, or another documented path) keyed by stable original feature IDs. Keep:

- `public_name_cs`, optional verified `public_name_en`/`public_name_ja`;
- `short_description_cs` (real substance, not tautology), `category_cs`, `region_label_cs`;
- `highlights_cs`, `scenery_cs`, `atmosphere_cs`, and `viewpoints` referencing other stable IDs privately;
- `editorial_status` in PRIVATE source (`author_approved` / `derived_from_source` / `new_editorial_name` / `requires_review`), `source_reason` and optional author note;
- `aliases` with former spellings and existing IDs for search, without showing them as labels;
- optional `media_id` / `photo_scene_id` link to the shared media registry.

A thin **public projection** retains only visitor-relevant fields and stable IDs required internally for matching/search. Do not expose source notes, prompts, status workflow, `Bible`, photo-production directives or old unpublished registries in public HTTP assets. Save a private report summarizing **how many names were preserved, clarified, newly generated and blocked**; flag only significant lore conflicts requiring author choice (not hundreds of repetitive naming questions). If time/limits constrain mass-content work, prioritize 159 atlas places and principal city landmarks, then complete remaining city object labels by reusable context-aware logic with visible quality checks; accurately report any remaining generic IDs.

---

## 2. Atlas details must be RICH, elegant and grammatical

### 2.1 Finished public place card: information architecture

A typical detail card should look like a carefully edited travel/geographic atlas entry, NOT a database inspector or one-sentence placeholder. Use actual relevant data and only show sections that have useful content:

**Title**: `Praha` / `Cimprlichovo Hradiště` / `Larpington` / the actual feature name. **No** `T-01`, `T-02`, `CP-…`, `prac.`, status prefix, internal version, code label or `(model)`.

**Subhead**: e.g. `Město v centrální nížině hlavního ostrova`, `Pobřežní vyhlídka na Paralandu`, `Železniční úsek v centrální nížině`, `Městské nábřeží v Larpingtonu`. Avoid broken declensions: **`Železniční trať v centrální nížině`**, NOT `Železniční trať · centrální nížině` and NOT the tautological sentence `Železniční trať v centrální nížině.` immediately under an identical heading.

**Short narrative**: ideally 2–4 informative, distinctive Czech sentences for an actual town or attraction; 1–2 concrete sentences for a mundane map object. Include *geographic context + relationship to visible landmarks/roads/coast + verified purpose or characteristic*; not empty marketing fluff. Town entries (especially Larpington) deserve a longer overview with neighborhood history/culture and connectivity already confirmed in canon; never reduce Larpington to one sentence.

**Relevant sections**, shown when enough verified/grounded information exists:

- `Kde místo leží` — island, district or region, proximity to named visible places; optional local atlas coordinates (x/y km), as **atlas coordinates**, not real-world measured GPS.
- `Nadmořská výška` — e.g. `přibližně 41 m n. m.` derived from DEM/model; avoid invented surveying precision. If original model says 41.1 and user wants it, may show `přibližně 41,1 m n. m.` with one global note that altitudes on map are orientational, not `výška (model)` on every card.
- `Výhledy a okolí` — real neighbor labels, views, direction and distances where computed from the **real existing** coordinate system (do not display raw IDs). Optional short named nearby clickable links.
- `Scenerie` / `Atmosféra` — **turn** structured camera/style/season metadata into compelling *public geography/travel prose*: e.g. `Úzké kamenné uličky a menší dvory se střídají s výhledy na přístav; v letních měsících má čtvrť rušnější pobřežní atmosféru.` Only if supported by existing assets/canon, not a new historical assertion.
- `Doprava a přístup` — only if relevant and based on actual roads, rail/ferry/canon; Paraland undersea train is NOT yet open.
- `Zajímavosti` — founded/heritage/protection facts if actually documented; do not fill with invented events.
- `Zobrazit na mapě` — working action to focus selected feature.

**Other languages:** under Czech title subtly show English name (`Praha` → **Prague**) and Japanese name (`プラハ`) if they exist or are safely verified, with no `návrh jména` label and no duplicated identical Czech/English name unless it really is the correct proper noun. Correct Czech primary naming always wins. Do not auto-translate proper names awkwardly.

### 2.2 Public visual mockups (illustrative; adapt to true data)

```text
DETAIL MÍSTA
Praha
Prague · プラハ
Město v centrální nížině hlavního ostrova
[2–3 specific sentences from real mapped roads, water and surroundings]

Kde místo leží
Hlavní ostrov · centrální nížina
Atlasové souřadnice: x 16,80 km · y 7,84 km   [if supported]
Nadmořská výška: přibližně 41 m n. m.         [if supported]

Výhledy a okolí
[Real nearby places as clickable NAMES; compass orientation and computed distances]

Scenerie
[Readable description grounded in known architecture, vegetation and season]

[ Zobrazit na mapě ]
```

```text
DETAIL MÍSTA
Larpington
Hlavní město Larpidie
[Meaningful overview, not one generic sentence. Cite four actual traditional quarters
and carefully distinguish the fifth urban creative area from the separate campus town.]

Městský charakter
Kompaktní historické bloky, nepravidelné ulice, dvory a zahrady;
některé části centra omezují automobilovou dopravu.

Čtvrti a okolí
Chalupecká · Kynčlova · Klimečkova · Žemličkova · ...
[Clickable context where registry supports it]

Doprava a spojení
[Canon-grounded access, without inventing exact routes/stations]

[ Zobrazit na mapě ]
```

**Mandatory negative test:** No public entry may end up with only a generic heading + a sentence repeating that heading + a button if its source record contains meaningful nearby places, photo guide or landscape/transport context. For sparse objects add *true contextual data* (neighboring mapped landmarks, surroundings or route) rather than imaginary facts.

### 2.3 Preserve map intelligence, but remove production language

- Retain internal IDs for lookup, georeferencing and queries; support searching `T-01`, `T-02` etc.; **display only actual place names** in results and detail.
- Never render `návrh jména`, `existence: schváleno`, `jméno: návrh`, `poloha: návrh`, `pseudo (hypotetické)`, `Bible`, `bible_ref`, `photo_guide`, `FOTO / VIDEO VODÍTKO`, `Vyhnout se`, `prac.`, `draft`, raw `settlement / town · main · central_lowland`, developer notes or `POI 12` as public text.
- Don't show fake real-world coordinate precision as fact. If the source has modelled 33.x° N 137.x° E, either show once under clearly named **`Orientační geografické souřadnice fiktivního atlasu`** or prefer local km atlas coordinates. Put one short reader-facing disclosure in the legend/help, not on every card. The world is fictional.
- Resolve `M-01 Z`, `M-02 Z`, `C-01 J` etc. into real approved/display labels plus human compass directions, e.g. `Mount Larp (západně, 10,1 km)`, **only where source coordinate check agrees**. Do not silently make up what raw compass tokens mean.
- Keep atmosphere/season information, but transform it into 1–3 interesting sentences. `Nehledejte zde` is not needed by default: production negative prompts like `vyhnout se obytné nížině` are camera instructions, NOT evidence that the landscape doesn't exist. If visitors would truly benefit from a caveat, phrase it as natural visitor advice backed by canon (e.g. visitor access restricted in crystal caves).
- If a locality is marked `proposed` internally, it may still appear as an **illustrative named atlas location** per author decision A1B; this does not automatically make its fictional existence a high-level canon fact. Keep editing statuses private and internally review a short high-impact conflict list.
- Clean unused status-dependent display controls and legend; keep real map layer filters.

### 2.4 Map panel / left rail / search

Keep the warm cream/green editorial identity. Improve spacing, typography, readable contrast and accessible touch targets. Use consistent map-control styling (avoid inconsistent default blue checkboxes). Keep the existing richer search: diacritic-insensitive name search, bilingual names, internal-ID aliases, island/type filters, keyboard/Enter/Escape, clear result states and mobile sliding panel.

Organize display layers under **`Vrstvy a nastavení mapy`** in a tidy accordion: settings can be open when user first arrives, but **collapse the settings section** when a detail opens; do NOT hide the selected detail or erase filters. Users can reopen it easily. Right sidebar should scroll usefully on desktop, and be a readable bottom sheet/stacked region on narrow screens. When a map item is selected, do not scroll away from the map unpredictably.

**Input & selection:** Hover = preview/highlight; click/tap = select + show rich detail; repeated clicks work; search selection focuses map; drag pans instead of selecting. Address SVG overlays stealing pointer events. A feature clickable from list must also be selectable via appropriate accessible action if map-layer hit target is ambiguous. Ensure both main atlas and Larpington plan work with mouse, keyboard and touch. Preserve 159/662 objects.

---

## 3. 2D cartography: elegant real-map conventions, NOT giant town ovals

Screenshots show crude large colored elliptical settlements, including Larpington. Aim for a richer **traditional atlas/cartographic look**, using the real Czech city map shown by the author only as a *style inspiration*, NOT geographic source. Keep the Larpidie geometry, island shapes and actual coordinate anchors, roads, rail alignments, water and zoning intact.

- Replace/de-emphasize simplistic settlement ovals with readable, irregular built-up-area shapes / generalized city blocks and **small tan/brown building footprints** clustered along **existing** streets. Where street geometries are sparse, synthesize only modest cartographic generalized blocks from existing settlement extents and land-use/road data, avoiding the false impression that every invented street exists. Do not generate 662 detailed buildings twice in the island-scale atlas; city-scale detail can use existing city footprints.
- Standard map visual hierarchy: sea pale blue, water/reservoir blue, forest soft green, contour/elevation quiet, roads with casing and categories, railway distinctive dashes/ties/lines, built-up areas muted warm brown, public spaces subtle, labels legible.
- Use zoom-based generalization: big labels/settlement texture at island overview, more street/blocks detail only as map zoom increases. Keep good performance with SVG/Canvas layers; prefer simple shapes and CSS over hundreds of expensive DOM animations.
- Keep hit targets and semantics: decorative building textures cannot swallow clicks. Avoid hand-drawn geometry that misplaces towns or contradicts known paths. Do NOT copy literal Google/OSM tiles/real Prague map roads into Larpidie.
- New cartography should be visible both through ROOT Live Server and after build export. Provide clear before/after screenshots at identical zoom/center for map and Larpington.

---

## 4. Gallery, photographs, visual stories and author-only media inventory

### 4.1 Repair the actual current gallery

The author previously saw giant blank off-white picture rectangles with only captions, e.g. `Zimní horská krajina Larpidie` and `Marina na Paralandu`. Prior Codex reported gallery assets loaded but there were still `.png` vs `.jpg` mismatches for `PHOTO_01` and `PHOTO_06`. Re-check the **current rendered result**, image `naturalWidth`, computed display styles, actual asset path, MIME type, public export, and relative URL resolution through hash/iframe routes; **do not assert success merely because HTTP returned 200**.

- All **real** locally available, appropriate Larpidie images should appear in the **same public gallery** (include ones used in articles), deduplicated by asset hash/scene or equivalent; no fake photo placeholders or giant empty cards for missing scenes.
- Photo first, explanatory caption immediately below, optional matching map/camera-location screenshot **second**. Avoid swapping them. If both photos and map visualizations exist, separate clearly.
- A random imported snowy-rock image must **not** be used as a real Larpidie photo if its identity/location cannot be demonstrated. Audit every article image. Link to known subject or replace with a genuinely matching available asset; if not available, show no image rather than unrelated stock material.
- Build/maintain one central photo manifest linking scene IDs, actual path, short Czech description, location IDs (internal), gallery item, photo/viewpoint ordering and current existence. Never infer a photo exists because a prompt expects a filename.
- Verify actual media count dynamically rather than freezing prior report's `2 available, 18 missing` (it may now have changed). Videos are a separate count if applicable; avoid double-counting thumbnails.

### 4.2 Compact author-only footer modal

In development/author preview only (including root Live Server, if this is the intended author mode), add a subtle footer item such as **`Obrazový archiv`**. It opens a small accessible floating panel/modal with:

- `Hotové fotografie: N` and `Chybějící scény: M` computed from actual existence;
- a scannable Czech list of available and missing image scenes (each with a short, human-readable Czech name and optional internal scene key only in this private control);
- optionally click a present scene to open its gallery image or relevant article;
- close control, Escape, proper focus restoration, mobile usability;
- no long image-generation prompts in the UI.

In the **public export**, hide the author-only button AND do not publish unpublished scene plans, private source registries or prompts. A mere CSS `display:none` while the data remain downloadable is not sufficient protection. A public site should not advertise its own incomplete photo checklist.

### 4.3 Exact requested master photo-prompt file

`v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/03_PHOTO_PROMPTS/ALL_PHOTO_PROMPTS.md`

Inspect before writing. Extend/organize existing original long prompts without overwriting work, deleting detailed camera instructions or duplicating scenes. Each scene gets a stable link to its image manifest and **specific accurate map viewpoint**: camera location, direction, nearby visible landmarks, season and geometry where documented. If a desired subject has no prompt, you MAY write a *new explicit draft prompt* consistent with actual map and canon, clearly marking it **INTERNAL DRAFT**; do not claim there is a generated image. For example, a future 4-round classroom geography game wants a ski slope overlooking the reservoir and a Paraland beach with a sightline across the strait to the main island; use existing verified placements before generating imagery. Other scenes only if compatible with map and legend. Do not generate the pictures here; just maintain prompt text and records.

---

## 5. Shared logo, footer versions and site chrome

- Find the collaborator's **real image logo** within the repository and use one central asset reference across header, footer, encyclopedia, atlas host, gallery; avoid multiple icons or fallback CSS `span` duplicates. **Footer logo was observed to be about twice the desired size**. Constrain it to the header's visual height and width, `object-fit:contain`, natural aspect ratio, alt text `Larpidie`; adjust responsive CSS across routes and iframes as needed. Don't invent a missing asset.
- No `NÁVRH · v1.0-draft` near page titles, no status badge in public card. **Version numbers MAY appear discreetly in footer** (`Atlas · verze …`, `Web · verze …`) only when sourced from real metadata; never render `draft` as the user's first impression. Current debug result reportedly removed the header badge: **keep it removed**.
- Ensure footer and header remain consistent after selecting `#atlas`, `#galerie`, `#encyklopedie/...`, as well as direct page loads. Avoid duplicating the footer/logo inside nested iframe UI.

---

## 6. Public/private build & data integrity

- The author views **ROOT `index.html` via VS Code Live Server**. Test all changed UI there (or an equivalent server rooted at project root), not just a generated export. Trace root/iframes and stop patching the wrong viewer copy.
- Preserve 159 main atlas places and 662 city plan objects; stable IDs, coordinates, polygon/path geometries and 3D data must not be silently changed. Name edits in the approved enrichment layer/registry are permitted; do not break old links or search aliases.
- Source registries can remain rich PRIVATE files with editorial notes and statuses. Public derived registry includes only visitor-safe fields + the opaque internal IDs required to implement search and linking. Tests should fail if `Bible`, `photo_guide`, unpublished prompts, raw draft-state fields or full working canon are accessible through the published public build. `references`, private `docs`, internal master prompt paths should return 404 when publicly hosted using the recommended export server (test deployment assumptions separately).
- Eliminate mismatched embedded-vs-standalone registers via one source or deterministic regeneration; avoid stale cached bundles. Maintain safe export allowlist and previously passing HTTP tests.
- Don't create a second atlas, new data universe, new 3D world, or expensive new front-end framework. This is a polish/curation job on an established project.

---

## 7. Work phases, concrete deliverables and **mandatory visual acceptance**

### PHASE 1 — Identify actual source, preserve functioning cleanup

1. Inventory current root Live Server routing, atlas iframe, Larpington plan, JS data renderers, gallery route, image manifest and export/build.
2. Verify old header badge and status badges really are gone in the ACTIVE viewer; do not reintroduce them.
3. Locate `Cimpřichovo Hradiště` and rename to **`Cimprlichovo Hradiště`** at the proper editable source, with generated/public copies synchronized and alias preserved for search.
4. Record which stage actually owns place descriptions and scenic metadata; fix that source, not only DOM text substitutions.

### PHASE 2 — Rich content and naming

1. Build editable enrichment source and public projection. Generate public display labels for all 159 atlas locations + all 662 city selectable objects based on type, valid names, actual neighborhoods, geometry and neighbors.
2. Replace generic POI entries where appropriate with context-grounded named viewpoints, junctions, springs etc.; preserve all original IDs and locations.
3. Restore meaningful public `Výhledy a okolí`, `Scenerie`, `Atmosféra`, relevant transport, accessible elevation and local coordinate information. Resolve internal IDs to visible names. Do not dump photo-generation prompts.
4. Ensure grammatical Czech for all generated labels; NO `Železniční trať · centrální nížině`, NO circular descriptions. Capital gets meaningful richer entry.
5. Create `docs/LARPIDIA_EDITORIAL_PLACE_NAMES_REVIEW.md` documenting new names mapped to stable IDs, evidence/reason and conflicts needing real editorial approval. Short grouped decisions only; do not ask 821 questions.

### PHASE 3 — Atlas UX & cartography

1. Elegant detail card and consistent rail styling; collapsible layers panel; accessible controls; hide developer states but keep useful layers.
2. Fix select/hover/click/mobile for atlas and city objects, avoid overlay interception.
3. Generalize oval settlement patches into realistic city blocks/land-use textures grounded in existing geometry. Ensure road/rail hierarchy legible. Capture same-zoom before/after visual comparison.

### PHASE 4 — Gallery, photo archive, logo

1. Audit actual images, fix gallery rendering, consolidate image manifest, use correct image first and map view second.
2. Add dev-only footer media modal and correct prompt registry path without exposing internals publicly.
3. Use verified shared logo asset consistently; shrink oversized footer logo.

### PHASE 5 — Tests, hardening, reporting

1. Run the **normal ROOT Live Server equivalent**, click from homepage into atlas and gallery, select the following specific objects: `T-01` (shown publicly as **Praha**), `T-02` (if this is the matching renamed city, **Cimprlichovo Hradiště**), `C-01`/Larpington, one railway segment, one generic-looking former POI, one building in Larpington; preserve raw IDs for private testing/search but never render them publicly. Check names/translation and rich details, including existing mapped views; click on map, use search, repeat and test touch.
2. Confirm no short generic railway card (`Železniční trať … / Železniční trať … / Zobrazit na mapě`) when spatial/scenic data exist. Confirm all text is proper Czech and `v centrální nížině` grammatical.
3. Confirm gallery images visibly render at nonzero dimensions and are actually appropriate for their labels, no blank white placeholders. Test all gallery routes and new author control on narrow mobile screens.
4. Confirm exact object totals 159 and 662, stable coordinates/paths; check the original 3D file hashes remain unchanged; check search `T-01`, `T-02`, `Praha`, `Prague`, `Cimprlichovo`, and misspelled legacy alias (which should still find new correct display name).
5. Scan **rendered user-visible DOM**, iframe content, and generated public assets for development language/IDs/field keys: `NÁVRH · v1.0-draft`, `prac.`, `návrh jména`, `existence:`, `jméno:`, `poloha: návrh`, `pseudo`, `Bible`, `photo_guide`, `FOTO / VIDEO VODÍTKO`, `settlement / town`, and generic `Bod zájmu`. Distinguish false matches inside harmless text/source from actual DOM. No hidden auth-only registry exposed through the public export.
6. Public export smoke + 404 tests, current README launch/build instructions, syntax/data validation, `git diff --check`; avoid new heavyweight dependencies. Browser screenshots must be saved to **`docs/debug-screenshots/` inside repo** (NOT `%TEMP%` only). Ideally create at least:
   - `atlas-root-live-praha.png`
   - `atlas-root-live-cimprlichovo.png`
   - `atlas-root-live-railway-rich-card.png`
   - `atlas-root-live-larpington.png`
   - `atlas-2d-city-before-after.png` (or separate before/after)
   - `gallery-live-mobile.png`
   - `author-media-modal.png`
   - `footer-logo.png`
   If screenshot renderer unavailable, explicitly admit it and include URLs plus manual screenshot steps; do not invent success.
7. Check representative content quality across at least **20 main-atlas locations** (towns, peaks, springs/POIs, transport, Paraland/coast, historic buildings) and **20 city-plan objects** from distinct categories. Record names + 1 meaningful public detail each in report. Testing only one handpicked item is insufficient.

### Final report files (all internal, Czech)

- **`docs/LARPIDIA_ATLAS_CONTENT_AND_UI_COMPLETION_REPORT.md`** — actual changes and source paths; Live Server and export URLs; spot-check table of 20+20 locations; count of generic placeholders removed; remaining limitations; test and screenshot paths; old/new card examples; grammar checks and map before/after evidence.
- **`docs/LARPIDIA_EDITORIAL_PLACE_NAMES_REVIEW.md`** — every edited/new place name indexed by stable internal ID, formerly displayed label, new public label, type/justification, `author_approved` vs new editorial suggestion; grouped genuinely unresolved points.
- **`docs/LARPIDIA_MEDIA_MANIFEST_REPORT.md`** — real file-based photo counts, missing scene list, media mismatches fixed, gallery routes and status-dialog checks, exact master photo-prompts path.
- **`docs/LARPIDIA_3D_TECHNICAL_OPTIONS.md`** — **analysis only**, not redesign: identify 3D engine (e.g. SVG, Three.js, Babylon, custom WebGL from the ACTUAL source, don't guess), number/type of draw objects if measurable, camera and navigation controls, rendering hot spots, easy safe improvements vs costly/performance-risky upgrades, and a recommended bounded next 3D task. Don't edit 3D assets/geometry.

### Completion criteria and honesty

**NOT DONE** if any active public viewer still shows code/status labels, any eligible entry is a tautological one-liner, Cimpřichovo instead of the explicitly requested Cimprlichovo, the city still mainly appears as a giant oval where existing data allow a better representation, selected features are unclickable, gallery image slots remain blank, or Codex has only tested a separate export while root Live Server differs.

If a phase cannot be implemented with current repo data or run time, **do not substitute an invented fact or omit the content**; preserve the site, clearly report blockers, and finish the highest-priority coherent portion with verifiable results. No Git commit/push. Final response in **Czech** summarizing real tested changes with screenshot paths and how to view them using the author's normal workflow.

---

## 8. Quick launch instruction for the implementer

Proceed without requesting another questionnaire. The author prefers creative, consistent local details and coherent geographic names to repetitive `not confirmed` notices. Use cautious editorial creativity for *small-scale atmosphere, modest POI labels and descriptions* while preserving official facts, known city names, numbers, transport states and original geometric positions. **Do not make the atlas empty in the name of hiding internal metadata.** A complete public atlas should be **informative, attractive, credible and fun to explore**.
