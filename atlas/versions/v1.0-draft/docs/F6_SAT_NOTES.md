# F6 – Satelitní podklady a šikmé pohledy (atlas v0.6.1-satbase)

Vše je **pracovní návrh (`proposed`)**. Obrázky jsou **simulovaná satelitní vizualizace fiktivního ostrova**, ne družicová ani letecká data.

## Co vzniklo a jak

| Výstup | Popis |
|---|---|
| `renders/S-01_base.png` / `.jpg` | Larpidie, kolmý pohled, 2240 × 1620 px, 10 m/px |
| `renders/S-02_base.png` / `.jpg` | Paraland, 1400 × 1120 px, 5 m/px |
| `renders/S-00_overview.png` / `.jpg` | oba ostrovy a průliv společně, 2970 × 2100 px, 10 m/px (celé plátno A2) |
| `renders/S-01_base_clouds.jpg`, `S-00_overview_clouds.jpg` | kosmetická varianta s mraky jen nad otevřeným mořem |
| `renders/S-01_oblique_S.jpg`, `S-01_oblique_NW.jpg`, `S-02_oblique_SW.jpg`, `S-02_oblique_strait.jpg` | čtyři šikmé pohledy (1800 × 1000 px) s kamerou v `*_camera.json` |
| `S-0x_mask_land.png`, `S-0x_mask_classes.png`, `S-0x_georef.json` | maska souše, třídy krajiny, převod pixel → km |
| `S-0x_labels_overlay.svg`, `S-0x_with_labels.svg` | popisky jako textové vrstvy (cs/ja/en), měřítko a označení simulace |
| `S-0x_prompt.md`, `OBLIQUE_PROMPTS.md` | anglické prompty pro externí generátor, nastavení a povinná kontrola tvaru |
| `scripts/verify_sat.py` | porovná vygenerovaný obraz s maskou (IoU souše ≥ 0,95); u šikmých pohledů porovná siluetu s referenčním šikmým pohledem; bílé plochy (mraky, příboj) vynechá |

Rendery vznikají z DEM (bikubicky z 20 m), měkce smíchaných tříd pokryvu, půdorysů sídel, vektorových silnic, tratí, vod, přístavů a letišť. Tvar ostrova je shodný s mapou: IoU souše vlastního renderu **0,999 (S-01) a 0,998 (S-02)**; kontrola pozná i posunutý obraz (IoU 0,77) i obraz jiného pohledu (IoU 0,11).

## 2. kolo: „Doladit vzhled“ (v0.6.1)

První sada podkladů (v0.6) vypadala jako schematická: kruhové zástavby, pestrá „patchworková“ pole, duhový kontejnerový areál, hladká zeleň. Změny:

- **Sídla:** zástavba po blocích (ulice, parcely, střechy, stíny; slunce z jihu, stín k severu), pět stylů (staré město, běžné sídlo, resort, zelená průmyslová zóna, přístav s kontejnerovým areálem), úhel uliček po okrscích, řidnutí hustoty k okrajům, nepravidelné půdorysy (uzavření laloků + šum), stuhová zástavba podél silnic.
- **Pole:** parcely na pootočené mřížce s živými ploty a půlenými parcelami, tlumená paleta, rozhodnutí „pole × pastvina“ po parcelách (okraje nepravidelné), skleníky jen vzácně.
- **Lesy a louky:** zubaté okraje lesa, remízky hustší u lesa, sušší a zelenější tóny pastvin, samoty (2–3 budovy s dvorem) podél silnic, rozptýlené stromy a háje v jemných oknech (≤ 6 m/px), pěšiny a sjezdovka.
- **Moře:** šelf podle typu pobřeží (široký u pláží, hluboká voda u útesů), kalné vody u ústí řek, jemnější přechod barev.
- **Přístavy a Paraland:** lodě v pánvích, nákladní loď u mola, hrad, zřícenina a aquapark ve správných rozměrech (v metrech).
- **Mraky:** jen kosmetická varianta, výhradně nad otevřeným mořem (pobřeží a ostrov zůstávají čisté), se stíny na hladině.
- **Šikmé pohledy:** kamera s posunutým objektivem (svislice zůstávají svislé; zdroje S-02 5 m a interní okno 3 m/px pro poloostrov, jinak S-00 10 m), obzor a atmosférická perspektiva, svislé převýšení 1,35×.

## S-03: Larpington (hlavní město) z plánu CP-01

`renders/S-03_base.png` / `.jpg` (2970 × 2100 px, **2 m/px**, sever nahoře) je okno plánu hlavního města (A2, 1 : 10 000): pixel = 2 m plánu, takže ho lze překrýt plánem bez převodu. Zástavba, ulice, bloky, parky a klíčové budovy se berou z `current/capital/` (`scripts/cp_sat.py`), pobřeží a krajina z atlasu. Domy vznikají v blocích podle využití (perimetrová zástavba starého města s dvory, řadové a rodinné domy, desky Východního nábřeží, státní budovy), stíny padají na sever, podél tepen a v parcích jsou stromy, v zelených klínech sady, zahrádky a hřiště. Platí totéž co u ostatních podkladů: **simulace a pracovní návrh**; domy jsou ilustrativní, ne půdorysy skutečných budov. Popisky (cs/en/ja) se přebírají z plánu (`S-03_labels_overlay.svg`), prompt je v `S-03_prompt.md`, tvar pobřeží hlídá `verify_sat.py S-03`.

## Poctivě k výsledku

- Nebyl vytvořen žádný fotorealistický obraz. Vlastní rendery jsou **stylizované reference** (procedurální textury, pravidelné bloky budov, půdorysy sídel z modelových laloků); mají sloužit jako geometrie pro externí nástroj s referenčním obrázkem (Gemini, ChatGPT, Firefly, Stable Diffusion s ControlNet).
- Textový prompt bez reference tvar ostrova neudrží; proto je v každém promptu povinná příloha a kontrola `verify_sat.py`.
- Šikmé pohledy jsou ilustrace z výškového modelu (voxelový render): bližší záběry jsou kvůli rozlišení zdroje (10 / 5 / 3 m) měkké a útesy mají svislé pruhování.
- **C-17 (nález):** čtvrti hlavního města nesahají k přístavu C-02 a přístavní vesnice PL-05 leží ~0,6 km od mariny. Render proto doplňuje pás zástavby kolem pánve a koridor k sídlu; půdorysy sídel v registru se **nezměnily** (rozhodnutí v F8).
- Hlavní město má na satelitu „křížový“ tvar z modelových laloků půdorysu (F3); je to návrh, ne kánon.
- Nepoužil jsem placené AI (Figma, Weave), jak tým rozhodl (R-05).
- Interní okno `X-pen` (3 m/px, poloostrov a průliv) se generuje do `atlas/work/sat/` (mimo snapshoty) příkazem `python atlas/scripts/render_sat.py X-pen`; `obliques` ho vytvoří sám, pokud chybí.

## Kontroly

`check_atlas.py`: vlastní rendery drží tvar (IoU ≥ 0,99), georeference nese SHA zmrazeného obrysu a plochu 175,4 km², prompty obsahují negativní omezení a označení simulace, popisky jsou validní SVG, přehled S-00 a čtyři šikmé pohledy mají kamery se stavem `proposed` a převýšením, varianty s mraky drží tvar.
