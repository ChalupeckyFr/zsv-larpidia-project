# S-01 · Larpidie – prompt pro externí generátor obrázků (image-to-image)

**Stav:** pracovní návrh (proposed). Výsledek je **simulovaná satelitní vizualizace fiktivního ostrova**, ne družicová data.
**Referenční obrázek:** `S-01_base.png` (2240 × 1620 px, 10 m/px, sever nahoře). Tvar ostrova **nesmí** změnit generátor, proto vždy přikládejte referenci
(Gemini, ChatGPT/gpt-image, Firefly, Stable Diffusion s ControlNet apod.). Samotný text bez reference tvar neudrží.

## Prompt (EN)

> Photorealistic top-down satellite photograph (nadir view, north up) of a fictional Pacific island nation, subtropical summer, midday sun from the south, crisp Sentinel-2 / Maxar-style imagery with natural colour grading.
> **Use the attached reference image as an exact structural guide: keep the coastline silhouette, the position of every harbour, town, road, rail line, reservoir, airport and forest/meadow boundary, and the framing, exactly as in the reference.**
> The main island is about 20 km across and elongated west–east: low forested mountains in the west and north-west (highest peak only 560 m, soft rounded ridges, dark mixed forest, one bright rounded meadow hill), steep rocky cliffs along the north-west coast, a small reservoir with a dam in the western interior, patchwork farmland and rice terraces in the south-west foothills, a compact historic capital on the southern coast with a harbour protected by breakwaters and red-brick/slate rooftops, compact smaller towns on the north coast and in the central lowland, a green low-rise industrial zone with light-roofed halls and a cargo port with piers in the east, a regional airport with a 1.9 km east–west runway, a narrow south-eastern peninsula, sandy beaches on the south and south-east coast, a coastal ring road, turquoise shallow water fading to deep blue open sea, subtle surf foam along the shore.
> Realistic textures: individual tree canopies, field parcels, building rooftops, thin asphalt roads, small rivers, natural shadows from relief.
> **Negative:** no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; no real-world landmarks or real place names.

## Nastavení

- poměr stran 1,38 : 1 (2240 × 1620 px); u image-to-image síla změny (strength / denoise) **0,30–0,45**; pokud nástroj umí, použijte referenci i jako strukturní/hranovou kontrolu (edge/depth);
- varianty: *late-afternoon golden light* (stíny na východ), *after the rain, saturated greens*, *winter morning, thin haze* (bez sněhu v nížinách);
- šikmý pohled (low-oblique, 35°) vždy generujte **z** této nadir reference a zachovejte rozložení; označte ho v názvu souboru `S-01_oblique_…`.

## Kontrola tvaru po generování (povinná)

```
python atlas/scripts/verify_sat.py S-01 cesta/k/vysledku.png --threshold 0.95 --overlay kontrola.png
```
IoU souše musí být ≥ 0,95 a „nejlepší posun“ blízko (0, 0). Pokud ne, zvyšte vazbu na referenci (nižší strength) nebo obraz upravte. Hotový obraz pak doplňte textovou vrstvou: `S-01_labels_overlay.svg` (popisky cs/ja/en, měřítko, upozornění) nebo použijte `S-01_with_labels.svg`.

## Povinné označení

Pod obrázek: **„Simulovaná satelitní vizualizace fiktivního ostrova (návrh) – ne skutečná družicová data.“** Skutečné značky a osobnosti se v obrázku neobjevují.

<details><summary>Georeference</summary>

```json
{
  "id": "S-01",
  "title": "Larpidie – simulovaná satelitní vizualizace (návrh)",
  "status": "proposed",
  "px": [
    2240,
    1620
  ],
  "meters_per_pixel": 10.0,
  "window_km": {
    "x0": 1.4,
    "y0": 0.0,
    "w": 22.4,
    "h": 16.2
  },
  "pixel_to_km": "x_km = x0 + (px + 0.5) * mpp/1000 ; y_km = y0 + (py + 0.5) * mpp/1000 (sever nahoře, východ vpravo)",
  "orientation": "kolmý pohled shora (nadir), sever nahoře",
  "land_area_km2": 175.4,
  "disclaimer": "SIMULOVANÁ satelitní vizualizace fiktivního ostrova, ne skutečná družicová data",
  "atlas_version": "0.5-atlas",
  "coast_sha256": "ffca09acdec9dac899c0699fd9abe6918338e5acbea6d180e42eb85ce34b3801"
}
```
</details>
