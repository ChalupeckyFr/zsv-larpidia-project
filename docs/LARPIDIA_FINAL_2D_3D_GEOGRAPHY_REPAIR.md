# Larpidie: final 2D/3D geography and terrain repair

## Result

The 3D island, Larpington terrain and transport layers now use one documented atlas coordinate transform. The 3D island is north-up, its elevations use real kilometre units, the reservoir sits at its source coordinates, and transport geometry is projected from the existing route files. The public atlas still contains 159 places and the Larpington registry still contains 662 objects.

The external screenshots mentioned in the original request were not available in this repository. The implementation and evidence below use the written requirements, project source data and new browser captures.

## Orientation and coordinate transform

Atlas SVG and DEM coordinates increase east in `x` and south in `y`, with DEM rows stored north to south. The prior 3D pages used separate hand-written transforms and treated positive world `Z` as north. That left the displayed north direction dependent on the camera basis and did not provide a shared conversion for the terrain, water and transport features; a small camera yaw could not resolve that axis mismatch.

The reusable transform is in `atlas/current/viewer/atlas-to-world.js`:

```text
world X = atlas x − 14.65 km       east is +X
world Z = atlas y − 9.50 km       south is +Z, north is −Z
world Y = elevation in metres / 1000
```

The 3D DEM grid uses its recorded origin `[-0.2, -1.0] km` and 40 m sample interval. Its row order therefore increases in the same direction as world `+Z`. The atlas-to-world helper is also used for the reservoir, streams, roads, railways and Larpington scene. Terrain triangles are wound for upward normals, and the north-up camera uses `-Z` as screen-up.

Control-point checks read the generated height field at registry coordinates: M-01 is 560 m, M-02 is 509.9 m, M-03 is 440 m, and Larpington’s C-01 location is 18.2 m. The lake surface uses the source model level of 67.6 m. Ocean samples remain at 0 m. At 40 m horizontal samples, the 560 m peak is 1.9% of the approximately 29.7 km DEM width, with no vertical exaggeration.

## Elevation, coast and Larpington terrain

Both 3D viewers now convert metres to kilometres once and no longer expose an elevation exaggeration slider. Building and infrastructure heights remain independent physical heights and are positioned over sampled terrain. The DEM is sampled at 40 m rather than 100 m and stores height in 16-bit values alongside the 8-bit land-cover channel. This reduces height quantization from about 2.2 m per step to about 0.009 m per step; no relief anchors or coastlines were moved.

The steep northwest shoreline was compared with `atlas/current/relief/coast_classes.geojson`. The largest adjacent 40 m height step is 207.4 m on a source segment classified `cliff`; the next largest is 176.1 m on a segment classified `rocky`. These explicit features remain in the model. Outside those mapped steep classes, the maximum adjacent shore step is 44.6 m. The finer grid, correct triangle winding and removal of the previous coarse height bands eliminate mesh spikes and stair-step artifacts visible in the repaired west-coast view. I did not flatten the mapped cliff or alter the canonical coastline.

Larpington now sits on its unexaggerated source DEM. Its center sample is 18.2 m, and the surrounding source terrain spans roughly 0–61.5 m. Existing gentle terrain in green and wooded zones remains visible without moving the harbor, streets, stations or buildings. I did not synthesize new hills or change building footprints. The existing 662-object city plan already has compact block coverage; its green wedges and open areas are retained as parks and public spaces rather than filled with invented buildings.

## City marker and selection

The large red capital star is replaced by a small restrained circle at the existing C-01 coordinates. C-01 remains searchable, keyboard-focusable and clickable.

Map symbols, labels, search results and nearby-place buttons call the same selection/detail pipeline in both viewers. The four Larpington district labels now carry their canonical city IDs, so they resolve to the same detail card and highlight as their district shapes. The same pipeline also handles keyboard Enter/Space and mobile taps. Internal IDs remain hidden from public details.

The browser regression compares text, map focus and highlight after clicking a city shape and its label. It covers C-01 Larpington, Praha, Hoshimachi, Cimprlichovo Hradiště, the Útesová vyhlídka point, and the Larpington Chalupecká district label. Search selection and touch selection are also exercised.

## Roads and railways

The terrain generator now copies each supported line from `atlas/current/human/roads.geojson` and `rail_lines.geojson`; it does not draw an ellipse or another substitute route. The regression compares every generated point to its source coordinates and checks round trips through the shared transform.

The source contains 62 road fragments and 26 rail fragments. The scene displays 59 roads; its three tunnel fragments stay hidden. It displays 17 rail fragments; seven tunnel sections, one cave section and one undersea section stay hidden. Rails have their own color and checkbox. Visible routes are sampled at 40 m, placed on the DEM with a 1 m rendering offset, and bridge/viaduct decks use small model lifts where the source identifies those sections. Source files do not provide surveyed bridge deck heights, so those lifts are model assumptions.

## Source files and generation

- `atlas/current/viewer/atlas-to-world.js` — shared coordinate transform.
- `atlas/current/viewer/terrain-3d.html` and `atlas/current/capital/capital-3d.html` — true-scale terrain, axes, normals, water and transport projection.
- `atlas/scripts/build_terrain_3d.py` and `scripts/build_terrain_3d_payload.mjs` — reproducible 40 m, 16-bit payload generation; fixed Python payload dimensions to use the new 16-bit array.
- `atlas/current/viewer/terrain-3d-data.js` — regenerated from relief PNGs, hydrography and transport GeoJSON.
- `templates/atlas_viewer_template.html`, `templates/capital_plan_viewer_template.html` and their current generated viewers — marker, canonical district label IDs, keyboard support and shared selection pipeline.
- `scripts/public_viewer_renderers.mjs` and `scripts/build_public_site.mjs` — shared public selection behavior and a non-destructive `--geography-only` export path.
- `scripts/check_geographic_consistency.mjs`, `scripts/check_public_render.mjs` and `scripts/capture_geographic_screenshots.mjs` — geography, browser and screenshot regressions.

The payload generator was rerun and reproduced the same SHA-256 in source and public output: `392D3E66B85B3421F2782A400AE65920E7F31518CE3F76774746C643CDE58062`. The targeted public export reported 159 atlas places and 662 Larpington objects. The full destructive public rebuild was not run.

## Verification

- `node scripts/check_geographic_consistency.mjs` — passed transform, scale, registry anchor, lake level, route-source equality and coast-class checks.
- `node scripts/check_public_render.mjs` — passed in Edge, including 159/662 registry counts, search, shape-versus-label selection, keyboard selection, gallery, privacy paths and narrow-screen atlas/city layout. No browser runtime or network failures were reported.
- `node scripts/check_live_root_atlas.mjs` — passed through the root `index.html` and local HTTP server; root atlas navigation, place cards, city objects, gallery and branding rendered.
- `node scripts/capture_geographic_screenshots.mjs final` — saved the six requested geography views plus an extra main-atlas comparison image; no runtime exceptions.
- Terrain payload regeneration produced a byte-identical result. JavaScript syntax checks passed for the new checker and capture script.

The Python generator could not be executed in this Windows environment because the available Python launchers resolve to inaccessible Windows Store stubs. Its output-size reference was corrected during review, but runtime parity remains unverified here; the Node generator is the verified reproducible path.

## Screenshot evidence

All final images are actual Edge captures of the public export:

1. North-up 3D island: [geography-final-3d-island-north-up.png](debug-screenshots/geography-final-3d-island-north-up.png)
2. Reservoir and mountain orientation: [geography-final-3d-reservoir.png](debug-screenshots/geography-final-3d-reservoir.png)
3. Northwest cliff/rocky coast: [geography-final-3d-west-coast.png](debug-screenshots/geography-final-3d-west-coast.png)
4. Larpington and surrounding terrain: [geography-final-3d-larpington.png](debug-screenshots/geography-final-3d-larpington.png)
5. Connected island transport overview: [geography-final-3d-roads-overview.png](debug-screenshots/geography-final-3d-roads-overview.png)
6. Larpington 2D plan without the red star: [geography-final-city-2d.png](debug-screenshots/geography-final-city-2d.png)
7. 2D atlas comparison: [geography-final-atlas-2d.png](debug-screenshots/geography-final-atlas-2d.png)

Baseline captures are retained at [geography-before-3d-island.png](debug-screenshots/geography-before-3d-island.png) and [geography-before-city-2d.png](debug-screenshots/geography-before-city-2d.png).

## Remaining limits

Relief and route inputs are explicitly model/proposed project data, not survey-grade terrain or engineering alignments. The mapped northwest cliff and rocky cape remain steep by design; their true sub-40 m profiles are unknown. Bridge deck lifts are approximations because the transport sources do not specify deck elevations. The source city plan was preserved rather than adding speculative buildings or hills.
