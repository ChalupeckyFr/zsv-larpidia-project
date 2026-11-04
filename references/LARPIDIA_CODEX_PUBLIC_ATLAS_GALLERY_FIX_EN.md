# LARPIDIA — PUBLIC ATLAS, MAP UX, GALLERY & BRANDING REPAIR

**Implementation brief for Codex (English instructions; Czech visitor-facing copy).**

## 0. Mission and authority

You are working **inside the existing Larpidie school-project repository**. The author has visually inspected the result of the previous audit implementation and found important remaining errors. The encyclopedia is generally improved, but the live atlas, Larpington plan, image handling, gallery, and branding still expose development artifacts or behave incorrectly. **Fix the actual rendered public experience, not merely the text of a report.**

Read, if present, the existing `README.md`, `docs/LARPIDIA_PUBLIC_CONTENT_FIX_REPORT.md`, `docs/LARPIDIA_ATLAS_SEARCH_IMPLEMENTATION.md`, `docs/LARPIDIA_PUBLIC_CONTENT_AUDIT.md`, `docs/LARPIDIA_ATLAS_SEARCH_REVIEW.md`, and `references/LARPIDIA_CODEX_SCHVALENE_OPRAVY_PO_AUDITU_v1.md`. Use `references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md` as the immutable world/constitutional canon. The last approved A1–A8 decisions still apply: retain all 159 atlas places and all 662 Larpington objects as an illustrative map; L1/L2 operate; city L3 operates but the undersea connection is under construction; the highest mountain is approximately 560 m; five-day school week; Larpington museum open, Paraland exhibition unfinished; pensions for Larpidian citizens 65+; richer atlas search. No parliament. Do not add another round of constitutional decisions.

**Trust precedence:** current explicit author instructions in this brief > A1–A8 author decisions > v2.6 canonical facts > current verified public project data > legacy World Bible or unapproved draft fields. Preserve original archival files unchanged. Never turn a rough GIS draft, AI prompt, or real-world reference photo into an unverified canonical claim.

**Scope:** targeted repairs of public atlas, Larpington 2D plan, public map details, existing gallery, illustration linking, media inventory, shared logo components, relevant build/export wiring. **DO NOT redesign or re-model the actual 3D Larpington scene or 3D terrain in this job.** Preserve the present visual identity (warm cream, dark green/navy, editorial type), functional routes and maps. Work with the currently implemented architecture; avoid a broad framework migration. No git commit or push.

**Practical order:** (1) reproduce/locate runtime and export problems; (2) public details/metadata + click handling; (3) gallery/media + logo; (4) modest 2D cartography polish; (5) responsive/quality/security regression tests. If context or time becomes limited, complete and verify a cohesive phase and clearly record unfinished work; never report "all fixed" with the known symptoms still visible. Prefer reading targeted files to rereading the enormous canon repeatedly.

## 1. Absolute rule: public content is not a development dashboard

In the **public** interface (including iframes, deeply linked HTML pages, popovers, search result rows, map legend, all details, 3D page headers, gallery cards, mobile views), do NOT expose:

- `T-01`, `C-01`, `CP-B01`, etc. as **visible map labels**, card titles, search result subheadings or descriptions. Internal IDs MUST remain in registries, indexing, click targets, selection logic and deep-linking, and **searching `T-01` must still find `Praha`**. The user should never need to know these codes.
- `návrh jména`, `jméno: schváleno`, `existence: schváleno`, `poloha: návrh`, `needs-decision`, `approved/proposed` badges, `prac. Larpington`, `NÁVRH · v1.0-draft`, `PRACOVNÍ MODEL`, `schváleno × návrh`, `obrysy podle stavu` as authoring statuses. Leave underlying data/status flags intact for maintainers and non-public processing.
- `pseudo (hypotetické)`, `model` next to height, `Bible`, `bible_ref`, `urbanism.must_include_towns`, `photo_guide`, `PROPOSED CAMERA POINT`, `avoid`, tool prompts, prompt-ready markers, internal notes and photo/video production metadata.
- "The canon has not confirmed ...", "our team has not generated the photos yet", work-in-progress disclaimers, missing-file notes, or author instructions presented as visitor information.

**Important truthfulness guardrail:** This is a *fictional* country. A single unobtrusive explanation such as `Orientační atlas fiktivní Larpidie` is appropriate. Do **not** pretend the fictional coordinate reference is real surveyed GPS. A label `Souřadnice v atlasu` using the existing local x/y coordinates is good; an optional approximate geographic position MUST be clearly framed as a fictional/model location, not accurate real-world GPS. If that wording undermines a polished visitor-facing atlas, omit the pseudo-GPS rather than misrepresenting it. Do not change geographic coordinates/geometry to make the wording appear more exact. For altitude, use `Nadmořská výška` and format e.g. `41,1 m n. m.` when an actual numeric field exists, with an overall legend note that the terrain is illustrative. Never invent missing measurements.

**Versioning:** remove draft/version badges from all headings, controls, tabs and content cards. Real software version identifiers are allowed **only in a small unobtrusive shared footer** (as previously approved), sourced from actual metadata. Do not fabricate version numbers or append `draft` to visitor-visible versions. Keep existing internal filenames and version history.

**No accidental data loss:** The author explicitly said "hide, don't delete." The 159 places and 662 city objects must remain; an unapproved field can be omitted from public UI without destroying it in source data. If a truly material place name/institution conflicts with canon, record the question in a small author-only decision register; do not mass-hide the map.

## 2. Main atlas and Larpington: redesign public place details

Investigate the *actual* entry points and data flow, likely `atlas/current/viewer/atlas.html` with `atlas/current/registry/places.json` and `atlas/current/capital/capital_plan_viewer.html` with `atlas/current/capital/cp_objects.json`, potentially embedded JSON copies and derived 3D data. Verify current paths instead of assuming they are identical to the previous audit. Inspect what **public export** really serves; changes to source files that don't propagate into output are not a fix.

### 2.1 Titles, languages and search behavior

Public card for object `T-01` should look like:

**Praha**
`English: Prague · 日本語: プラハ` (provided this translation is supported or straightforward from established transliterations)
`Město ve vnitrozemské nížině hlavního ostrova.`

Never `T-01 · Praha`; never `návrh jména: Praha / Praha / プラハ`. In search results show `Praha` plus a readable descriptor and area/region, not the code or workflow badge. **Keep matching on hidden ID** (exact and prefix, e.g. `T-01`, `C-01`, `CP-B01`), canonical/proposed names, localized names and supported aliases. Preserve diacritic-insensitive search, filters, enter/arrow navigation and mobile search drawer introduced previously. If no reliable translated name exists, omit that translation rather than copying a Czech name into English or fabricating Japanese; record only names that warrant editorial resolution. Provide Czech, English and Japanese text variants only when credible and appropriate. The user's `Praha` is a Larpidian fictional settlement; don't silently replace it with the real Czech capital or import real Prague's geography.

Public place titles should consistently remove prefixes such as `Hlavní město (prac. Larpington)` or `C-01 · ...`. The actual capital is **Larpington**, not `Praha`; preserve these as distinct locations in registry if both exist. Correct the capital name globally in the atlas/plan/3D **labels** without modifying 3D geometry.

### 2.2 Present raw registry fields as inviting editorial content

Public panel sections should be simple and visually consistent:

1. **Place name** + optional accurate alternative-language names.
2. **Short human description** based on available fields: `Město ve vnitrozemské nížině`, `Pobřežní osada na Paralandu`, `Horská vyhlídka` etc. Only the location/type supported by data; do not extrapolate a named business, monument or legal status.
3. **Poloha a výška**: visitor-readable regional phrase, `Souřadnice v atlasu` (formatted local x/y if useful), optional `Nadmořská výška` (m n. m.). Hide debug percentage coordinates (`X 70 %`, etc.) unless there is an explicit visitor use; they remain in source.
4. **Scenerie** (if real scenic data are available): `Výhledy`, `V okolí`, `V dálce`, `Atmosféra`. Convert references like `M-01 Z`, `M-02 Z`, `C-01` to **actual display names** with appropriate direction and verified/map-computable distance (keep the direction/distance if meaningful). Build an ID→displayName resolver from existing canonical registry. If a related ID cannot be resolved, omit or flag internally, NEVER show raw ID as fallback in public copy. Avoid manufacturing proximity from string labels.
5. **Zobrazit na mapě** action (when appropriate), reliably working.

Production guidance in `photo_guide` may help a writer prepare **short natural Czech scenic descriptions**, provided that it does not falsely assert unverified facts. E.g. an existing atmosphere describing a warm summer, historic masonry and sea wind can become a tasteful short `Atmosféra` paragraph *if geographically relevant*. `Vyhnout se` is a generative-image negative prompt, **not travel guidance**. Do NOT publish it as `Nehledejte zde` unless the content truly describes a factual visitor restriction. Otherwise keep it only in internal data. Do not show `Bible`, background model prompts or technical photo creation instructions, even collapsed.

Make the right-hand panel visually elegant, matching the encyclopedia and the left search panel: prominent title, readable spacing, subtle dividers, no huge raw JSON-like tables, responsive cards, coherent accessible typographic scale and focus rings. The inspector must not feel like an editor. Clicking another feature updates selected content without stacked event listeners or unwanted page scroll.

### 2.3 Sidebars and controls

- Harmonize left and right panes and replace inconsistent default blue browser checkboxes with accessible, coherent custom-styled controls or tasteful native accent colors. Preserve large touch targets.
- Group rarely used **public** map controls under a clearly named collapsible section `Vrstvy a nastavení mapy`. Initially accessible on first entry, but when the user selects/opens a place, collapse the settings area to prioritize its detail. Allow easy reopening; do not destroy selected filters. Do not collapse the entire map or main search unexpectedly.
- Remove the public checkbox/layer `Barvy podle stavu údajů`, `Obrysy podle stavu (schváleno × návrh)`, and status-derived colors/legend. If these are essential internal developer tools, keep them in a deliberately non-public admin/debug build, never in visitor UI or public exported payload.
- Keep visitor-useful filters (type, island, transport, water, landmarks, roads, buildings, etc.) and controls; do not accidentally remove new atlas search features. Prefer simple readable grouping rather than dozens of switches.
- A map feature hover should show a small **preview/highlight**; clicking/tapping should **select, update/open its detail and optionally focus the map**. In particular, fix Larpington objects that currently highlight on hover but do nothing on click. Debug actual SVG/pointer-events ordering, invisible overlays, event bubbling/delegation, iframe integration and dynamically rendered items. Add keyboard selection on focusable features or a reachable equivalent search/list, and preserve drag-to-pan so it doesn't trigger accidental selections.

### 2.4 2D urban cartography, not a full GIS rewrite

The current schematic atlas uses broad oval/tinted city blobs. The author wants an **elegant conventional 2D cartographic look**, inspired by typical city maps: readable street hierarchy, railway lines, water, green zones, urbanized areas and simplified building-block footprints in muted tan/brown. The real-life map of Prague the author showed is a **visual style reference only**, NOT a map to copy or project onto the fictional Larpidie. Preserve actual fictional positions, shorelines, road/rail routing and existing object IDs.

- Replace or visually reduce giant oval settlement blobs where possible in favor of **data-grounded generalized urban footprints** (multiple irregular polygons or city blocks along the existing road network), not millions of individual houses. Use existing street/block data if present; where insufficient, apply unobtrusive cartographic tinting rather than inventing dense road geometry or reshaping towns arbitrarily.
- Buildings/urban areas: softened brown/tan fill; roads: clear hierarchy with contrasting casing; rails: distinctive linear symbology; coastline/rivers/reservoir: consistent blue; parks/forest: subdued greens. Labels must remain readable at different zooms.
- Avoid fake precision, aggressive effects, excessive complex SVG DOM nodes and zoom-dependent jitter. Use CSS/SVG layers, simple geometries, existing viewBox coordinate system; add zoom level generalization if useful. **Do not copy OpenStreetMap/Google map tile images, copyrighted map styling assets, or literal real Prague road layouts.**
- Do not move town centers, anchors, roads, station positions, project railway alignments, shorelines, island geometry, or 3D object positions unless resolving an actual documented bug.
- Keep feature hit targets clickable and hoverable when new visual layers are added. Consider layering and `pointer-events` deliberately.

## 3. Gallery and all local media: fix functionality before restyling

The author reports a regression: gallery displays **giant blank white rectangles with only captions**, e.g. `Zimní horská krajina Larpidie` and `Marina na Paralandu`. This is not acceptable. Reproduce it from the same entry point the site uses, then fix the real root cause: broken relative URL inside hash routes or iframe, wrong public export asset paths, missing file, CSS invisible media, layout height/aspect, lazy-load/init issue, inconsistent encoding, etc. **Do not claim a fix based only on source code inspection.** If screenshot tooling is unavailable, inspect DOM/assets/HTTP requests and give a practical manual click-test checklist; say browser visual confirmation is pending.

### 3.1 Media inventory and safe sourcing

- Inspect only the project's actual local image/video assets and the existing scene registry. Resolve duplicates by filename/hash/intent. Distinguish meaningful photo/scene art from icons, logos, background decorations, UI screenshots, temp files, and old unused versions.
- Build **one canonical structured media manifest** with stable IDs, Czech short titles, type, verified resolved asset path, actual existence, linked place/scene where known, public visibility, optional view/camera/map image path, source/provenance if available. The manifest must be easy to update; do not hardcode media paths differently in every article.
- Display **all real, appropriate, usable existing Larpidie photos and scene visualizations** in the gallery, with short Czech captions. A linked article should have its best existing valid image only if it actually depicts that subject. Don't attach random beautiful but unrelated stock photos; don't use unverifiable external hotlinks; don't invent images or claim a prompt is an image.
- Missing media are not rendered as huge empty photo cards. If a scene has no image yet, hide its media card from the public gallery; optionally show a small tasteful generic category explanation in a place that needs context, not a broken image. Preserve the missing-scene entry in author-only inventory.
- Every gallery card: media occupies primary prominence, with a small caption below. If a corresponding orientation/viewpoint/map screenshot already exists, it should be **second**, after the actual photo. Do not swap primary photo with a plan/mockup. Provide consistent crop/aspect and responsive grid.
- If a local image is used anywhere in an article and is appropriate for the Larpidie gallery, include it in the shared manifest/gallery; do not duplicate large file blobs.
- Fix public media paths in both direct page navigation and `#encyklopedie/...`, `#atlas`, `#galerie` routes, plus safe exported build. Test filenames with Czech accents and whitespace if present.

### 3.2 Discreet footer media-status window: internal only

The author wants a small footer control opening a floating window with **image counts and a short Czech list of what exists versus what is missing**, with simple descriptions (not huge prompts). Implement this as an **author/development-only** footer utility so the public encyclopedia still looks complete. Label e.g. `Obrazový archiv` or `Stav fotografií` in development preview. Clicking opens an accessible compact modal/popover with:

- `Hotové fotografie: N`; `Chybějící scény: M` (computed, not fabricated)
- short Czech display titles of available and missing planned scenes; optional scene ID *inside this author-only utility*, not public.
- convenient close button, Esc, focus handling, scrolling on mobile.
- a path to the prompt registry for maintainers (as plain reference if hosted files cannot be opened safely).

In the **public production export**, hide the status control and do not expose the private planned-scene manifest or unpublished media plan through HTTP. The user previously rejected all visitor-visible "construction site" notes. If the author later explicitly requests a public gallery-status feature, that is a separate choice.

### 3.3 Central prompt file

Use the user-specified target (normalize separators for repository environment):

`v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/03_PHOTO_PROMPTS/ALL_PHOTO_PROMPTS.md`

- Inspect first: if it already exists, **preserve it and extend/organize** without overwriting high-quality custom prompts or removing previous scenes. If absent, create it by consolidating **real existing** prompt text available elsewhere in the repo, with source references. Do not invent complete 20-scene prompts from scratch merely to fill a number.
- Each scene should be associated with its image-manifest ID and a clear stable link to its intended subject/viewpoint; report missing prompts or conflicting scene definitions in the author-only decisions/issues file.
- This file is INTERNAL and must not be served by the production static export. Do not put full AI prompts in visitor HTML or public JSON.

## 4. Shared logo / header / footer

A collaborator has created an **actual image logo** that appears in their presentation. The author managed to replace the logo in one header and one gallery footer but not in encyclopedia and atlas footer/header. Investigate the real logo asset in the repository first. It might be in an unsaved or untracked local path; do NOT guess its name. If found and appropriate, use that same verified image for the site branding everywhere: homepage, encyclopedia, gallery, atlas host page, and subviewers as appropriate. Keep accessible alt text `Larpidie`, proper dimensions/retina rendering and legible contrast. Centralize shared markup/style so one change applies to all modes. Do not mistakenly duplicate logo across iframes. If actual file is absent, leave existing logo in place and report exact expected asset/location; don't fabricate a replacement.

Explain briefly in a developer note why the previous `span`/CSS mark rendered differently across page templates (likely duplicated header/footer or iframe/partial styles) once verified from source. Preserve existing routes and navigation.

## 5. Data synchronization, export and safety

Previous audit reported an HTML-embedded atlas registry plus a separate JSON registry and four mismatched city objects. Verify the current actual data-flow **after the previous Codex update**, then establish a single authoritative source for each viewer or an automated one-way generation step. Do not silently mutate canonical names or change object counts. If a static JSON fetch requires a server, keep offline/local preview behavior working using the project's supported build process. Repair public rendering AND the exported public version, not just one.

**Public/private separation must be REAL, not a CSS disguise:** If a visitor can request the same registry or serialized JavaScript payload over HTTP and read `Bible`, `photo_guide`, draft notes or protected author files, hiding the fields from DOM is insufficient. Prefer public derived data projections/whitelists for the output and private source registries outside the web root. Keep functional hidden IDs as required for search, but strip unnecessary metadata. Test direct URLs for internal archives/`references`/`docs`/photo prompts/legacy drafts return 404 in the *built public export*. Don't make the build expose newly created author-only report files. Preserve prior safe-export behavior and the URL tests the previous implementation introduced.

When reconstructing rich public scenic descriptions, it is acceptable to generate visitor-oriented copy from existing structured content, but validate named places and directions against registry/canon; don't auto-promote `proposed` fields to confirmed institutional reality. For an uncertain exact proper name, prefer a neutral geographic display label and a grouped internal unresolved-item report, not 150 individual questions.

## 6. Required verification and tests

At minimum:

1. Find the actual active code path AND generated public export before editing. Verify the correct build/serve commands from repo scripts or README.
2. **159 atlas places and 662 Larpington objects** retained; spot-check search for exact hidden ID (`T-01` finds `Praha`), diacritic-insensitive name, English name (`Prague`), and no-result state. Results and public detail show names, never raw ID/status.
3. Select/hover an atlas feature; click then updates detail. Select/hover a Larpington building/POI; click opens detail. Repeat multiple times, then pan/zoom, switch views and test tap behavior. Ensure no duplicate listener accumulation.
4. Confirm for both viewers that `návrh jména`, `Bible`, `pseudo (hypotetické)`, `photo_guide`, `FOTO / VIDEO VODÍTKO`, `v1.0-draft`, `PRACOVNÍ`, `schváleno × návrh` and raw `CP-...` are absent in public visible UI. Use a scan of visitor-visible templates and dynamic renderers, not only source grep; exclude innocuous internal source commentary.
5. Confirm public card example `Praha`, translated English `Prague`, and a human-readable Czech description; `Larpington` not shown as `prac. Larpington`. No parliament remains as a public active institution.
6. Verify genuine photos appear **visibly** in both direct and hashed gallery routes; no giant whitespace placeholders, no broken `src`; valid primary photo before map/viewpoint image. Check on a narrow mobile viewport. If screenshots cannot be captured programmatically, report exact browser steps to verify and do not falsely claim visual validation.
7. Footer utility counts match the manifest, prompts stored at requested path, and author-only data are missing from the production export. Confirm the author's logo file used consistently **if it exists**.
8. Check internal report/prompt/canon paths are blocked (404) by the public-export server; run prior HTTP/export tests and validate any new public data bundles are scrubbed.
9. Test successful syntax/runtime/validation/build and link checks with available project dependencies. **Do not install `numpy` or other new dependency just to silence a non-essential Python check**; clearly record any missing optional test.
10. Keep 3D geometry unchanged; keep map coordinate anchors/road routing unchanged; verify existing atlas/3D navigation remains intact.

**Important:** a plain grep for words like `draft` is not a sufficient pass criterion; the earlier update reported success despite visible draft badges and raw inspector data. Verify real rendered output path in the browser or simulated DOM plus the exported pages, and document what was actually tested versus not tested.

## 7. Deliverables

Make actual project code/data/config changes and create:

**`docs/LARPIDIA_PUBLIC_ATLAS_GALLERY_REPAIR_REPORT.md`** — Czech, concise but concrete. Include what changed, paths, before/after examples, tests actually executed and their observed results, public export path/build command, inventory counts, failure cases, and explicitly note any visual/browser verification not completed. Don't report completed work you haven't checked.

**`docs/LARPIDIA_REMAINING_CONTENT_DECISIONS.md`** — Czech, only real author-level unresolved decisions (group related registry records); include source reference and your recommended choice. If there are no unresolved decisions, say so. Do not turn 159+662 map rows into questionnaires, do not add decisions 103+.

**`docs/LARPIDIA_PUBLIC_UX_SMOKE_TEST.md`** — Czech, a compact manual click-through checklist for desktop/mobile with checkboxes and clear URLs/commands; include atlas ID search, city-object click, gallery media, logo, developer footer, public-file exclusion, and 3D regression.

Do not overwrite old reports; write these new ones. Keep changes easy for the user to edit without digging through huge HTML. At the end of the Codex conversation, report actual completion **per subsection**, precise modified paths, tests, and honest blockers. Don't overstate whether the full public deployment is fixed unless tested on that same deployment.

## 8. Acceptance examples (non-negotiable)

- BAD: `T-01 · Praha / návrh jména: Praha / Praha / プラハ / existence: schváleno / poloha: návrh / pseudo (hypotetické)`.
- GOOD: `Praha` → `English: Prague · 日本語: プラハ` → `Město ve vnitrozemské nížině hlavního ostrova.` → `Souřadnice v atlasu: …` → `Nadmořská výška: 41,1 m n. m.` (if field present). Internal ID and status remain usable in data/search but are visually absent.
- BAD: `C-01 · Hlavní město (prac. Larpington)`.
- GOOD: `Larpington` → `Hlavní město Larpidie.`
- BAD: huge blank gallery card labeled `Zimní horská krajina Larpidie` or `Marina na Paralandu` when the file is missing/not loaded.
- GOOD: actual verified photo shown prominently with a short caption; optional viewpoint screenshot follows; absent media excluded from public gallery and counted in author-only inventory.
- BAD: checkbox `Obrysy podle stavu (schváleno × návrh)`; banner `NÁVRH · v1.0-draft`; public `Bible` field; a map object that highlights on hover but does nothing when tapped.
- GOOD: layers by visitor-friendly type, accurate small version text only in footer, click/tap opens detail, private metadata stays private.

**Concentrate on shipping and testing these concrete corrections, not writing another reassuring but unverified summary.**
