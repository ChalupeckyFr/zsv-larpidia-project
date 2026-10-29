"""F6 – doplňky: textová vrstva popisků k satelitním podkladům a prompty pro externí generátor obrázků.

Spuštění:  python atlas/scripts/sat_extras.py
Výstup:    renders/S-0x_labels_overlay.svg, S-0x_with_labels.svg, S-0x_prompt.md, README_RENDERS.md
"""
from __future__ import annotations

import base64
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import atlas_svg as A
import canon
import render_sat as rs
import svgkit
from canon import ATLAS

OUT = ATLAS / "current" / "renders"

DISCLAIMER = "Simulovaná satelitní vizualizace fiktivního ostrova (návrh) – ne skutečná družicová data"


def labels_svg(name, spec, D, with_image: bool):
    c = spec["canvas"]
    sh = svgkit.Sheet(canvas=c)
    Wm, Hm = round(c["w"] * 1000), round(c["h"] * 1000)
    wpx, hpx = round(Wm / spec["mpp"]), round(Hm / spec["mpp"])
    if with_image:
        b64 = base64.b64encode((OUT / f"{name}_base.jpg").read_bytes()).decode("ascii")
        sh.raw(f'<g id="satellite-base" inkscape:groupmode="layer" inkscape:label="Simulovaný satelitní podklad"><image x="0" y="0" width="{Wm}" height="{Hm}" preserveAspectRatio="none" href="data:image/jpeg;base64,{b64}"/></g>')
    k = 1.25 * spec["mpp"] / 10.0 * 10.0 / 10.0          # velikost písma: ~12 px pro "100" z map 1:50 000
    specs = []
    for s in A.label_specs(D):
        if c["x0"] + 0.15 <= s["x"] <= c["x0"] + c["w"] - 0.15 and c["y0"] + 0.15 <= s["y"] <= c["y0"] + c["h"] - 0.15:
            s2 = dict(s)
            s2["size"] = s["size"] / 10.0 * 1.25 * spec["mpp"] * (1.0 if name == "S-01" else 1.0)
            specs.append(s2)
    A.draw_labels(sh, D, specs)
    with sh.layer("marginalia", "Měřítko a upozornění"):
        km = 5.0 if name == "S-01" else 1.0
        svgkit.nice_scale_bar(sh, 400, Hm - 520, km=km, label_size=int(16 * spec["mpp"] * 1.0))
        sh.text(400, Hm - 160, DISCLAIMER, size=int(15 * spec["mpp"]), units=True, fill="#ffffff", halo=False, style='opacity="0.9"')
        sh.text(400, 560, spec["title"], size=int(26 * spec["mpp"]), units=True, fill="#ffffff", weight="700", halo=False, style='opacity="0.95"')
    svg = sh.render(spec["title"], f"{DISCLAIMER}. Popisky jsou textové vrstvy cs/ja/en; pixel = {spec['mpp']} m.")
    svg = svg.replace('width="594mm" height="420mm"', f'width="{wpx}" height="{hpx}"')
    svg = re.sub(r'viewBox="0 0 \d+ \d+"', f'viewBox="0 0 {Wm} {Hm}"', svg, count=1)
    return svg


PROMPT_COMMON_NEG = ("no text, no labels, no captions, no logos, no watermarks, no grid lines, no borders; do not move, smooth or reshape the coastline; "
                     "do not add, remove or merge islands, bays, peninsulas, harbours or towns; do not add a second large airport or skyscrapers; "
                     "no snow caps or alpine glaciers (the highest peak is only 560 m); no clouds covering the coast; no cartoon or illustration style; "
                     "no real-world landmarks or real place names.")


def prompt_s01(D):
    ref = (OUT / "S-01_georef.json").read_text(encoding="utf-8")
    return f"""# S-01 · Larpidie – prompt pro externí generátor obrázků (image-to-image)

**Stav:** pracovní návrh (proposed). Výsledek je **simulovaná satelitní vizualizace fiktivního ostrova**, ne družicová data.
**Referenční obrázek:** `S-01_base.png` (2240 × 1620 px, 10 m/px, sever nahoře). Tvar ostrova **nesmí** změnit generátor, proto vždy přikládejte referenci
(Gemini, ChatGPT/gpt-image, Firefly, Stable Diffusion s ControlNet apod.). Samotný text bez reference tvar neudrží.

## Prompt (EN)

> Photorealistic top-down satellite photograph (nadir view, north up) of a fictional Pacific island nation, subtropical summer, midday sun from the south, crisp Sentinel-2 / Maxar-style imagery with natural colour grading.
> **Use the attached reference image as an exact structural guide: keep the coastline silhouette, the position of every harbour, town, road, rail line, reservoir, airport and forest/meadow boundary, and the framing, exactly as in the reference.**
> The main island is about 20 km across and elongated west–east: low forested mountains in the west and north-west (highest peak only 560 m, soft rounded ridges, dark mixed forest, one bright rounded meadow hill), steep rocky cliffs along the north-west coast, a small reservoir with a dam in the western interior, patchwork farmland and rice terraces in the south-west foothills, a compact historic capital on the southern coast with a harbour protected by breakwaters and red-brick/slate rooftops, compact smaller towns on the north coast and in the central lowland, a green low-rise industrial zone with light-roofed halls and a cargo port with piers in the east, a regional airport with a 1.9 km east–west runway, a narrow south-eastern peninsula, sandy beaches on the south and south-east coast, a coastal ring road, turquoise shallow water fading to deep blue open sea, subtle surf foam along the shore.
> Realistic textures: individual tree canopies, field parcels, building rooftops, thin asphalt roads, small rivers, natural shadows from relief.
> **Negative:** {PROMPT_COMMON_NEG}

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

Pod obrázek: **„{DISCLAIMER}.“** Skutečné značky a osobnosti se v obrázku neobjevují.

<details><summary>Georeference</summary>

```json
{ref}
```
</details>
"""


def prompt_s02(D):
    ref = (OUT / "S-02_georef.json").read_text(encoding="utf-8")
    return f"""# S-02 · Paraland – prompt pro externí generátor obrázků (image-to-image)

**Stav:** pracovní návrh (proposed). **Simulovaná satelitní vizualizace fiktivního ostrova**, ne družicová data.
**Referenční obrázek:** `S-02_base.png` (1400 × 1120 px, 5 m/px, sever nahoře). V levém horním rohu je kousek jihovýchodního poloostrova hlavního ostrova (průliv 1,5 km).

## Prompt (EN)

> Photorealistic top-down satellite photograph (nadir view, north up) of a small fictional resort island, subtropical summer, midday sun from the south, crisp Sentinel-2 / Maxar-style imagery.
> **Use the attached reference image as an exact structural guide: keep the island silhouette, the marina at the north-west coast, the old town on the north coast, the castle hill, the ring road, the airstrip, the resort cluster and aquapark in the south, the forested eastern hills and the sandy beaches in the sheltered eastern bays exactly as in the reference.**
> The island is about 5.5 km long: a small historic town with tiled roofs and a harbour bay in the north, a castle on a green headland, a ruin on a wooded slope, low-rise resort hotels with pools and a turquoise aquapark in the south, a small grass airstrip in the west, a marina with floating piers and breakwaters in the north-west, dense forest and low hills in the east with a hiking loop, pale sandy beaches in protected eastern bays, turquoise lagoon-like shallows fading to deep blue sea, a part of the neighbouring main island's peninsula visible in the top-left corner.
> **Negative:** {PROMPT_COMMON_NEG}

## Nastavení a kontrola

- poměr stran 1,25 : 1; image-to-image strength **0,30–0,45**;
- kontrola tvaru: `python atlas/scripts/verify_sat.py S-02 cesta/k/vysledku.png --threshold 0.95`;
- popisky: `S-02_labels_overlay.svg` / `S-02_with_labels.svg`;
- pod obrázek vždy: **„{DISCLAIMER}.“**

<details><summary>Georeference</summary>

```json
{ref}
```
</details>
"""


def readme():
    return f"""# Satelitní podklady S-01 a S-02 (atlas {canon.ATLAS_VERSION})

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
"""


def main():
    D = A.Data()
    for name, spec in rs.WINDOWS.items():
        (OUT / f"{name}_labels_overlay.svg").write_text(labels_svg(name, spec, D, with_image=False), encoding="utf-8")
        (OUT / f"{name}_with_labels.svg").write_text(labels_svg(name, spec, D, with_image=True), encoding="utf-8")
    (OUT / "S-01_prompt.md").write_text(prompt_s01(D), encoding="utf-8")
    (OUT / "S-02_prompt.md").write_text(prompt_s02(D), encoding="utf-8")
    (OUT / "README_RENDERS.md").write_text(readme(), encoding="utf-8")
    print("renders: popisky, prompty a README zapsány")


if __name__ == "__main__":
    main()
