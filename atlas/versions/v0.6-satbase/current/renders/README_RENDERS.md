# Satelitní podklady S-01 a S-02 (atlas 0.5-atlas)

Obrázky jsou **simulované** a tvarově přesné: vznikly z výškového modelu, pokryvu krajiny, sídel a tras atlasu (`scripts/render_sat.py`).
Slouží jako reference pro fotorealistický generátor a jako podklad pro popisky. **Nejsou skutečná družicová data.**

| Soubor | Obsah |
|---|---|
| `S-01_base.png` / `.jpg` | Larpidie, kolmý pohled, 2240 × 1620 px, 10 m/px |
| `S-02_base.png` / `.jpg` | Paraland, 1400 × 1120 px, 5 m/px |
| `S-0x_mask_land.png` | binární maska souše (stejné pixely jako obraz) |
| `S-0x_mask_classes.png` | indexová maska tříd (les, louka, pole, terasy, křoviny, skála, pláž, jezero, zástavba, průmysl) |
| `S-0x_georef.json` | převod pixel → km, měřítko, SHA obrysu |
| `S-0x_labels_overlay.svg` | průhledná textová vrstva (cs/ja/en), měřítko, upozornění |
| `S-0x_with_labels.svg` | totéž nad vloženým podkladem |
| `S-0x_prompt.md` | prompt (EN), nastavení a povinná kontrola tvaru |

Kontrola vygenerovaného obrazu: `python atlas/scripts/verify_sat.py S-01 obraz.png` (IoU souše ≥ 0,95).
Převod pixelu na km: `x = x0 + (px + 0.5) · mpp / 1000`, `y = y0 + (py + 0.5) · mpp / 1000` (údaje v `S-0x_georef.json`).
