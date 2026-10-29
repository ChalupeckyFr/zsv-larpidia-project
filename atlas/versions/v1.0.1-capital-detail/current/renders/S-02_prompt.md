# S-02 · Paraland – prompt pro externí generátor obrázků (image-to-image)

**Stav:** pracovní návrh (proposed). **Simulovaná satelitní vizualizace fiktivního ostrova**, ne družicová data.
**Referenční obrázek:** `S-02_base.png` (1400 × 1120 px, 5 m/px, sever nahoře). V levém horním rohu je kousek jihovýchodního poloostrova hlavního ostrova (průliv 1,5 km).

## Prompt (EN)

> Photorealistic top-down satellite photograph (nadir view, north up) of a small fictional resort island, subtropical summer, midday sun from the south, crisp Sentinel-2 / Maxar-style imagery.
> **Use the attached reference image as an exact structural guide: keep the island silhouette, the marina at the north-west coast, the old town on the north coast, the castle hill, the ring road, the airstrip, the resort cluster and aquapark in the south, the forested eastern hills and the sandy beaches in the sheltered eastern bays exactly as in the reference.**
> The island is about 5.5 km long: a small historic town with tiled roofs and a harbour bay in the north, a castle on a green headland, a ruin on a wooded slope, low-rise resort hotels with pools and a turquoise aquapark in the south, a small grass airstrip in the west, a marina with floating piers and breakwaters in the north-west, dense forest and low hills in the east with a hiking loop, pale sandy beaches in protected eastern bays, turquoise lagoon-like shallows fading to deep blue sea, open meadows in the west dotted with single trees and small groves, a part of the neighbouring main island's peninsula visible in the top-left corner.
> **Negative:** no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; no real-world landmarks or real place names.

## Nastavení a kontrola

- poměr stran 1,25 : 1; image-to-image strength **0,30–0,45**;
- kontrola tvaru: `python atlas/scripts/verify_sat.py S-02 cesta/k/vysledku.png --threshold 0.95`;
- popisky: `S-02_labels_overlay.svg` / `S-02_with_labels.svg`;
- šikmé pohledy na Paraland (z jihozápadu a z poloostrova přes průliv): `S-02_oblique_SW.jpg`, `S-02_oblique_strait.jpg`, prompty v `OBLIQUE_PROMPTS.md`;
- pod obrázek vždy: **„Simulovaná satelitní vizualizace fiktivního ostrova (návrh) – ne skutečná družicová data.“**

<details><summary>Georeference</summary>

```json
{
  "id": "S-02",
  "title": "Paraland – simulovaná satelitní vizualizace (návrh)",
  "status": "proposed",
  "px": [
    1400,
    1120
  ],
  "meters_per_pixel": 5.0,
  "window_km": {
    "x0": 22.1,
    "y0": 14.4,
    "w": 7.0,
    "h": 5.6
  },
  "pixel_to_km": "x_km = x0 + (px + 0.5) * mpp/1000 ; y_km = y0 + (py + 0.5) * mpp/1000 (sever nahoře, východ vpravo)",
  "orientation": "kolmý pohled shora (nadir), sever nahoře",
  "land_area_km2": 14.1,
  "disclaimer": "SIMULOVANÁ satelitní vizualizace fiktivního ostrova, ne skutečná družicová data",
  "atlas_version": "1.0-draft",
  "coast_sha256": "ffca09acdec9dac899c0699fd9abe6918338e5acbea6d180e42eb85ce34b3801"
}
```
</details>
