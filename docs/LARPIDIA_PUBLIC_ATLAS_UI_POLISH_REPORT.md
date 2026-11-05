# Public Atlas UI Polish Report

Date: 2026-11-04

## Files changed

- `site.css`, `scripts/build_public_site.mjs`, and `templates/capital_plan_viewer_template.html`
- Generated root and export viewers: `atlas/current/viewer/atlas.html`, `atlas/current/capital/capital_plan_viewer.html`, and their `public/` copies; `public/site.css`
- Browser verification: `scripts/check_live_root_atlas.mjs` and `scripts/check_public_render.mjs`
- Two fresh screenshots in `docs/debug-screenshots/`

## Changes

- Widened the root atlas surface beyond the article column and increased its desktop viewport height.
- Rebalanced the viewer columns to give the map more space, refined panel spacing, and kept the search drawer and stacked mobile layout.
- Styled layer checkboxes with the site’s rust accent, visible keyboard focus, and full-row hover and click targets. Applied the same controls to the Larpington plan.
- Kept the existing public content, names, privacy filtering, and interactions intact.

## Verification

- Rebuilt the public site: **159 atlas places** and **662 Larpington objects** retained.
- `node scripts/check_public_export.mjs` passed.
- `node scripts/check_live_root_atlas.mjs` passed against `index.html#atlas` over local HTTP, including search, repeated clicks, mobile taps, and public/private checks.
- `node scripts/check_public_render.mjs` passed in Edge for the public export, including search, map interaction, custom layer toggles, responsive behavior, and private-path checks.
- Visually verified the root page in Edge over local HTTP.

## Screenshots

- [Root atlas, desktop](debug-screenshots/atlas-ui-polish-root-desktop.png)
- [Layer controls, close view](debug-screenshots/atlas-ui-polish-layer-controls.png)

## Intentionally unchanged

Editorial text and names, all 159 places and 662 objects, coordinates, map geometry and paths, terrain and 3D data, site palette, footer branding, and public/private data separation.

## Remaining limitations

The narrow-screen layout uses the existing search drawer and vertically scrollable detail/layer panels; no interaction or rendering regressions were observed.
