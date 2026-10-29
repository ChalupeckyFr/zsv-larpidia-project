# Šikmé pohledy – prompty pro externí generátor (image-to-image)

**Stav:** pracovní návrh (proposed). Reference jsou **simulované šikmé pohledy** vytvořené z výškového modelu a nadir podkladů atlasu, ne družicová ani letecká data.
Kamera má posunutý objektiv (svislice zůstávají svislé; obzor leží ve zlomku výšky obrazu `horizon`). Generátoru vždy předejte referenci a nastavte
image-to-image strength **0,30–0,45** (nižší = věrnější tvar). Samotný text bez reference siluetu ostrova neudrží.

Kontrola siluety (`verify_sat.py`) porovnává pevninu a obzor s referenčním šikmým pohledem; bílé plochy (mraky, příboj) jsou z porovnání vynechány.

Pod obrázek vždy: **„Simulovaná satelitní vizualizace fiktivního ostrova (návrh) – ne skutečná družicová data.“**

## S-01_oblique_NW

**Referenční obrázek:** `S-01_oblique_NW.jpg` (1800 × 1000 px) · **kamera:** `S-01_oblique_NW_camera.json` (x -6.0 km, y 3.2 km, výška 2600 m, směr 99° od severu, vodorovné zorné pole 64°)
**Záběr:** z moře severozápadně od ostrova k východu: útesy severozápadu, hory, přehrada, jihovýchodní poloostrov.

> Photorealistic low-oblique aerial photograph of Larpidie, a fictional Pacific island nation, subtropical summer, clear day, natural colour grading, soft atmospheric haze toward the horizon.
> **Use the attached reference image as an exact structural guide: keep the camera position and field of view, the horizon height, the coastline silhouette, and the position of every harbour, town, road, reservoir, forest and meadow boundary exactly as in the reference.** Relief is shown 1.35× vertically exaggerated in the reference; keep the same proportions.
> Realistic textures: tree canopies, field parcels with hedgerows, tiled and slate roofs, thin asphalt roads, turquoise shallows fading to deep blue, subtle surf along the shore, natural shadows (sun from the south-west).
> **Negative:** no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; no real-world landmarks or real place names.

Kontrola siluety: `python atlas/scripts/verify_sat.py S-01_oblique_NW cesta/k/vysledku.jpg --threshold 0.95`

## S-01_oblique_S

**Referenční obrázek:** `S-01_oblique_S.jpg` (1800 × 1000 px) · **kamera:** `S-01_oblique_S_camera.json` (x 16.4 km, y 21.6 km, výška 3000 m, směr 1° od severu, vodorovné zorné pole 62°)
**Záběr:** z moře jižně od hlavního města k severu: historický přístav, město, pláže, pole a hory na severozápadě.

> Photorealistic low-oblique aerial photograph of Larpidie, a fictional Pacific island nation, subtropical summer, clear day, natural colour grading, soft atmospheric haze toward the horizon.
> **Use the attached reference image as an exact structural guide: keep the camera position and field of view, the horizon height, the coastline silhouette, and the position of every harbour, town, road, reservoir, forest and meadow boundary exactly as in the reference.** Relief is shown 1.35× vertically exaggerated in the reference; keep the same proportions.
> Realistic textures: tree canopies, field parcels with hedgerows, tiled and slate roofs, thin asphalt roads, turquoise shallows fading to deep blue, subtle surf along the shore, natural shadows (sun from the south-west).
> **Negative:** no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; no real-world landmarks or real place names.

Kontrola siluety: `python atlas/scripts/verify_sat.py S-01_oblique_S cesta/k/vysledku.jpg --threshold 0.95`

## S-02_oblique_strait

**Referenční obrázek:** `S-02_oblique_strait.jpg` (1800 × 1000 px) · **kamera:** `S-02_oblique_strait_camera.json` (x 19.7 km, y 12.0 km, výška 900 m, směr 131° od severu, vodorovné zorné pole 62°)
**Záběr:** z jihovýchodního poloostrova hlavního ostrova přes průliv 1,5 km na Paraland.

> Photorealistic low-oblique aerial photograph of Paraland, a small fictional resort island, subtropical summer, clear day, natural colour grading, soft atmospheric haze toward the horizon.
> **Use the attached reference image as an exact structural guide: keep the camera position and field of view, the horizon height, the coastline silhouette, and the position of every harbour, town, road, reservoir, forest and meadow boundary exactly as in the reference.** Relief is shown 1.35× vertically exaggerated in the reference; keep the same proportions.
> Realistic textures: tree canopies, field parcels with hedgerows, tiled and slate roofs, thin asphalt roads, turquoise shallows fading to deep blue, subtle surf along the shore, natural shadows (sun from the south-west).
> **Negative:** no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; no real-world landmarks or real place names.

Kontrola siluety: `python atlas/scripts/verify_sat.py S-02_oblique_strait cesta/k/vysledku.jpg --threshold 0.95`

## S-02_oblique_SW

**Referenční obrázek:** `S-02_oblique_SW.jpg` (1800 × 1000 px) · **kamera:** `S-02_oblique_SW_camera.json` (x 21.8 km, y 20.3 km, výška 1000 m, směr 47° od severu, vodorovné zorné pole 60°)
**Záběr:** z moře jihozápadně od Paralandu: resorty a aquapark na jihu, východní les a pláže.

> Photorealistic low-oblique aerial photograph of Paraland, a small fictional resort island, subtropical summer, clear day, natural colour grading, soft atmospheric haze toward the horizon.
> **Use the attached reference image as an exact structural guide: keep the camera position and field of view, the horizon height, the coastline silhouette, and the position of every harbour, town, road, reservoir, forest and meadow boundary exactly as in the reference.** Relief is shown 1.35× vertically exaggerated in the reference; keep the same proportions.
> Realistic textures: tree canopies, field parcels with hedgerows, tiled and slate roofs, thin asphalt roads, turquoise shallows fading to deep blue, subtle surf along the shore, natural shadows (sun from the south-west).
> **Negative:** no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; no real-world landmarks or real place names.

Kontrola siluety: `python atlas/scripts/verify_sat.py S-02_oblique_SW cesta/k/vysledku.jpg --threshold 0.95`

## S-03_oblique_S

**Referenční obrázek:** `S-03_oblique_S.jpg` (1800 × 1000 px) · **kamera:** `S-03_oblique_S_camera.json` (x 16.3 km, y 15.0 km, výška 300 m, směr 0° od severu, vodorovné zorné pole 54°)
**Záběr:** z moře jižně od přístavu k severu: historický přístav, staré město, Přístavní třída a Náměstí čtyř s hmotami budov.

> Photorealistic low-oblique aerial photograph of Larpington, the compact fictional harbour capital of a Pacific island nation, subtropical summer, clear day, natural colour grading, soft atmospheric haze toward the horizon.
> **Use the attached reference image as an exact structural guide: keep the camera position and field of view, the horizon height, the coastline silhouette, and the position of every harbour, town, road, reservoir, forest and meadow boundary exactly as in the reference.** Relief is shown 1.35× vertically exaggerated in the reference; keep the same proportions.
> Realistic textures: tree canopies, field parcels with hedgerows, tiled and slate roofs, thin asphalt roads, turquoise shallows fading to deep blue, subtle surf along the shore, natural shadows (sun from the south-west).
> **Negative:** no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; no real-world landmarks or real place names.

Kontrola siluety: `python atlas/scripts/verify_sat.py S-03_oblique_S cesta/k/vysledku.jpg --threshold 0.95`

## S-03_oblique_W

**Referenční obrázek:** `S-03_oblique_W.jpg` (1800 × 1000 px) · **kamera:** `S-03_oblique_W_camera.json` (x 13.0 km, y 12.6 km, výška 330 m, směr 82° od severu, vodorovné zorné pole 52°)
**Záběr:** z polí západně od města k východu podél Hlavní třídy: západní stanice, Náměstí čtyř se správními budovami a parlamentem, v pozadí Klimečkova čtvrť.

> Photorealistic low-oblique aerial photograph of Larpington, the compact fictional harbour capital of a Pacific island nation, subtropical summer, clear day, natural colour grading, soft atmospheric haze toward the horizon.
> **Use the attached reference image as an exact structural guide: keep the camera position and field of view, the horizon height, the coastline silhouette, and the position of every harbour, town, road, reservoir, forest and meadow boundary exactly as in the reference.** Relief is shown 1.35× vertically exaggerated in the reference; keep the same proportions.
> Realistic textures: tree canopies, field parcels with hedgerows, tiled and slate roofs, thin asphalt roads, turquoise shallows fading to deep blue, subtle surf along the shore, natural shadows (sun from the south-west).
> **Negative:** no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; no real-world landmarks or real place names.

Kontrola siluety: `python atlas/scripts/verify_sat.py S-03_oblique_W cesta/k/vysledku.jpg --threshold 0.95`
