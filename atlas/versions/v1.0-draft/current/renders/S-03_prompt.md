# S-03 · Larpington (hlavní město) – prompt pro externí generátor obrázků (image-to-image)

**Stav:** pracovní návrh (proposed). **Simulovaná satelitní vizualizace fiktivního města**, ne družicová data.
**Referenční obrázek:** `S-03_base.png` (2970 × 2100 px, 2 m/px, sever nahoře) = okno plánu hlavního města CP-01 (A2, 1 : 10 000). Zástavba, ulice a prostory pocházejí z plánu (`current/capital/`), pobřeží je zmrazený obrys atlasu.

## Prompt (EN)

> Photorealistic top-down satellite photograph (nadir view, north up) of a fictional compact harbour capital of about 12,000 people on a subtropical Pacific island, midday sun from the south, crisp Maxar-style imagery.
> **Use the attached reference image as an exact structural guide: keep the coastline, the harbour with its two breakwaters and the ferry pier, every street, block, square, park and the position of each key building exactly as in the reference.**
> A circular civic square with an eight-armed star of avenues in the centre (a parliament building in a round garden, four administrative buildings arranged like a pinwheel around it), four neighbourhoods with differently rotated street grids around it, an old harbour town on the south coast with curving streets parallel to the shoreline, a market square, a church with a cruciform roof, a harbour promenade with boutiques and cafés, a premium hotel, parks, green wedges of meadows and orchards between the neighbourhoods, surface railway lines with small stations, terracotta, slate and light-grey roofs, brick and stone houses with gardens, tree-lined avenues.
> Realistic textures: individual building roofs with soft shadows falling to the north, thin asphalt streets with pavements, tree canopies, boats in the harbour, turquoise shallows fading to deep blue.
> **Negative:** no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; no real-world landmarks or real place names.

## Nastavení a kontrola

- image-to-image strength **0,25–0,40** (město je detailní; vyšší hodnoty přepíšou uliční síť);
- kontrola tvaru: `python atlas/scripts/verify_sat.py S-03 cesta/k/vysledku.png --threshold 0.95` (hlídá pobřeží a přístav, ne jednotlivé ulice; ulice zkontrolujte překryvem s `capital_plan_base.png`);
- šikmé pohledy na město generujte z této reference a plánu; pod obrázek vždy: **„Simulovaná satelitní vizualizace fiktivního ostrova (návrh) – ne skutečná družicová data.“**

<details><summary>Georeference</summary>

```json
{
  "id": "S-03",
  "title": "Larpington – simulovaná satelitní vizualizace hlavního města (návrh)",
  "status": "proposed",
  "px": [
    2970,
    2100
  ],
  "meters_per_pixel": 2.0,
  "window_km": {
    "x0": 13.1,
    "y0": 10.3,
    "w": 5.94,
    "h": 4.2
  },
  "pixel_to_km": "x_km = x0 + (px + 0.5) * mpp/1000 ; y_km = y0 + (py + 0.5) * mpp/1000 (sever nahoře, východ vpravo)",
  "orientation": "kolmý pohled shora (nadir), sever nahoře",
  "land_area_km2": 21.65,
  "disclaimer": "SIMULOVANÁ satelitní vizualizace fiktivního ostrova, ne skutečná družicová data",
  "atlas_version": "1.0-draft",
  "coast_sha256": "ffca09acdec9dac899c0699fd9abe6918338e5acbea6d180e42eb85ce34b3801"
}
```
</details>
