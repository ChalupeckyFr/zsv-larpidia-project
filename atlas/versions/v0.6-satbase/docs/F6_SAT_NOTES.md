# F6 – Satelitní podklady S-01 a S-02 (atlas v0.6-satbase)

Vše je **pracovní návrh (`proposed`)**. Obrázky jsou **simulovaná satelitní vizualizace fiktivního ostrova**, ne družicová data.

## Co vzniklo a jak

| Výstup | Popis |
|---|---|
| `renders/S-01_base.png` / `.jpg` | Larpidie, kolmý pohled, 2240 × 1620 px, 10 m/px |
| `renders/S-02_base.png` / `.jpg` | Paraland, 1400 × 1120 px, 5 m/px |
| `S-0x_mask_land.png`, `S-0x_mask_classes.png`, `S-0x_georef.json` | maska souše, třídy krajiny, převod pixel → km |
| `S-0x_labels_overlay.svg`, `S-0x_with_labels.svg` | popisky jako textové vrstvy (cs/ja/en), měřítko a označení simulace |
| `S-0x_prompt.md` | anglický prompt pro externí generátor, nastavení a povinná kontrola tvaru |
| `scripts/verify_sat.py` | porovná vygenerovaný obraz s maskou (IoU souše ≥ 0,95), hlásí posun a poměr ploch |

Rendery vznikají z DEM (bikubicky z 20 m), měkce smíchaných tříd pokryvu, půdorysů sídel, vektorových silnic, tratí, vod, přístavů a letišť. Moře má barvu podle vzdálenosti od pobřeží, příboj a světlý písek u pláží. Tvar ostrova je shodný s mapou: IoU souše vlastního renderu **0,999 (S-01) a 0,997 (S-02)**; kontrola dokáže poznat i posunutý obraz (test: IoU 0,77).

## Poctivě k výsledku

- Nebyl vytvořen žádný fotorealistický obraz. Vlastní rendery jsou **stylizované reference** (procedurální textury, pravidelná mřížka budov, půdorysy sídel z hladkých bloků); mají sloužit jako geometrie pro externí nástroj s referenčním obrázkem (Gemini, ChatGPT, Firefly, Stable Diffusion s ControlNet).
- Textový prompt bez reference tvar ostrova neudrží; proto je v každém promptu povinná příloha a kontrola `verify_sat.py`.
- Nepoužil jsem placené AI (Figma, Weave), jak tým rozhodl (R-05).
- Šikmé pohledy a sezónní varianty se mají generovat **z** nadir reference a znovu ověřit; hlavní město a okolí dostane vlastní podklad ve F7.

## Kontroly

`check_atlas.py`: vlastní rendery drží tvar (IoU ≥ 0,99), georeference nese SHA zmrazeného obrysu a plochu 175,4 km², prompty obsahují negativní omezení a označení simulace, popisky jsou validní SVG.
