# Satelitní podklady S-01 a S-02 a šikmé pohledy (atlas 1.0-draft)

Obrázky jsou **simulované** a tvarově přesné: vznikly z výškového modelu, pokryvu krajiny, sídel a tras atlasu (`scripts/render_sat.py`).
Slouží jako reference pro fotorealistický generátor a jako podklad pro popisky. **Nejsou skutečná družicová ani letecká data.**

| Soubor | Obsah |
|---|---|
| `S-01_base.png` / `.jpg` | Larpidie, kolmý pohled, 2240 × 1620 px, 10 m/px |
| `S-01_base_clouds.jpg` | totéž s mraky jen nad otevřeným mořem (kosmetická varianta, ne strukturní reference) |
| `S-02_base.png` / `.jpg` | Paraland, 1400 × 1120 px, 5 m/px |
| `S-03_base.png` / `.jpg` | Larpington (hlavní město), kolmý pohled, 2970 × 2100 px, 2 m/px; okno plánu CP-01, zástavba z plánu města |
| `S-00_overview.png` / `.jpg` / `_clouds.jpg` | oba ostrovy a průliv společně, 2970 × 2100 px, 10 m/px (celé plátno A2) |
| `S-0x_mask_land.png` | binární maska souše (stejné pixely jako obraz) |
| `S-0x_mask_classes.png` | indexová maska tříd (les, louka, pole, terasy, křoviny, skála, pláž, jezero, zástavba, průmysl) |
| `S-0x_georef.json` | převod pixel → km, měřítko, SHA obrysu |
| `S-0x_labels_overlay.svg` | průhledná textová vrstva (cs/ja/en), měřítko, upozornění |
| `S-0x_with_labels.svg` | totéž nad vloženým podkladem |
| `S-0x_prompt.md` | prompt (EN), nastavení a povinná kontrola tvaru |
| `S-01_oblique_S.jpg`, `S-01_oblique_NW.jpg` | šikmé pohledy na Larpidii (z moře jih / severozápad), 1800 × 1000 px |
| `S-02_oblique_SW.jpg`, `S-02_oblique_strait.jpg` | šikmé pohledy na Paraland (z jihozápadu / z poloostrova přes průliv) |
| `S-03_oblique_S.jpg`, `S-03_oblique_W.jpg` | šikmé pohledy na Larpington s hmotami budov (z moře jižně od přístavu / od západní stanice podél Hlavní třídy) |
| `S-03_buildings_height.png` | výškový model budov okna plánu: 16bit PNG, 1 jednotka = 0,1 m nad terénem, stejné pixely jako `S-03_base.png` (zdroj hmot pro 3D nástroje) |
| `*_oblique_*_camera.json` | kamera (poloha v km, výška, směr, zorné pole, obzor), zdroje a převýšení |
| `OBLIQUE_PROMPTS.md` | prompty pro šikmé pohledy |

Kontrola vygenerovaného obrazu: `python atlas/scripts/verify_sat.py S-01 obraz.png` (IoU souše ≥ 0,95); u šikmých pohledů
`python atlas/scripts/verify_sat.py S-01_oblique_S obraz.jpg` (silueta pevniny a obzor).
Převod pixelu na km: `x = x0 + (px + 0.5) · mpp / 1000`, `y = y0 + (py + 0.5) · mpp / 1000` (údaje v `S-0x_georef.json`).
Šikmé pohledy používají svislé převýšení 1,35× (jinak by 560 m hory vypadaly jako pahorky); souřadnice kamery jsou v lokálních km atlasu.
