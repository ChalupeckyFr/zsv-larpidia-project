# PHOTO — Fotorealistické obrázky Larpidie

## Úloha generátoru

Vytvoř fotorealistický záběr fiktivní Larpidie, který působí jako poctivá cestovatelská fotografie, nikoliv model 3D architektury či generické AI fantasy. Řiď se `larpidia_world_bible.json` a `GEOGRAPHY_AND_CANON.md`.

### Závazné údaje každého snímku

- `ID`: jednoznačný název obrázku
- `lokace`: ID z geografického registru (např. N-03, C-01, T-04)
- `sousedství`: co leží blízko / v dálce
- `roční doba`, `část dne`, `počasí`
- `úhel pohledu` + `ohnisko` + `kompozice`
- `vizuální styl`: upřímná cestovatelská fotografie, realistické barvy, drobné nedokonalosti
- `účel`: prezentace / atlas / plakát / Story
- `poměr stran`: 16:9, 4:5, 3:2 nebo 9:16
- `text v obrázku`: přidej až následně jako typografickou vrstvu, pokud je důležitá přesnost

### Obecný master vizuální prompt (EN – vhodný pro obrazové generátory)

> A believable editorial travel photograph taken on the fictional Pacific island nation of Larpidia. [EXACT CANON LOCATION AND SURROUNDINGS]. Authentic environmental storytelling, lived-in human scale, British and Welsh red-brick and stone heritage architecture mixed with carefully integrated modern Japanese urban infrastructure where appropriate, lush greenery, credible island topography, natural materials, believable vehicles and rail infrastructure, realistic weather and lighting for [SEASON / TIME], physically coherent geography, subtle human activity, excellent but unforced composition, natural photographic dynamic range, cinematic mood without CGI. [CAMERA AND LENS]. [ASPECT RATIO]. No fake satellite labels, no scrambled text, no implausible mega-cities, no fantasy mountain heights, no physically impossible floating structures, no repeating identical people, no generic tropical palm resort everywhere. The place must match Larpidia's canonical world bible.

### Fotky, které se musí vyskytovat v celé sérii

1. Zelený západní horský les s kamennou vyhlídkou; skryté studánky.
2. Průjezd vyhlídkového vlaku podél vodopádu a do osvětlené jeskyně.
3. Za deště romantické anglické uličky, kamenné chodníky, zahrady, cihla a mech.
4. Na severu kompaktní japonsky ovlivněné městečko: elektrické rozvody, úzká zástavba, útulné obchody, ulice (bez karikatur).
5. V létě cesta podél moře, lesnaté výběžky, autem přístupná bezpečná vyhlídka.
6. Ekologická průmyslová zóna: stín, otevřené haly, škola, jídelna, laboratoře, zeleň.
7. Larpington (název návrhový): přístav, historické náměstí, kostel, městský park, butiky.
8. Paraland: přirozený resort, malý historický hrad, hotely, aquapark a les na jediném ostrově.
9. Krátká zimní sezona na horské sjezdovce — bez obřích alpských masivů.
10. Reálný život obyvatel: ranní pekárna, školní ulice, noční tramvaj či vlak, cyklisté.

### Samostatné Stories – estetika současných sítí

`9:16 vertical`, přirozené světlo z telefonu, nenápadně nedokonalý záběr, drobný ruch, skutečně uvěřitelný moment, vhodný prostor na titulek. Série musí zachytit různorodost: *sunrise hike → coffee in old town → station/train POV → waterfall → night town*. Neopakuj šest variací na pláž a drink.

### Vzor 1 – ranní hike

> Vertical 9:16 authentic smartphone travel photograph from a marked forest overlook in western Larpidia, looking across a compact lush island mountain ridge toward a pale Pacific sunrise. The island's highest peak is approximately 560 meters, not alpine; faint low sea haze, mossy tree trunks, hikers wearing ordinary weather-appropriate walking clothes seen only as natural background figures, natural lens flare and small smartphone-camera imperfections, peaceful real-life outdoors moment. No commercial studio posing, no invented skyscrapers, no dangerous cliff jumping, no labels or text.

### Vzor 2 – město po dešti

> Photorealistic travel street photography at dusk in Larpington, capital of fictional Larpidia, historical southern harbor quarter. Welsh and English brick shopfronts, rain-darkened paving stones, climbing moss on old stone walls, small church tower glimpsed beyond cozy gardens, a few discreet modern Japanese street design cues, realistic electric classic cars, soft warm windows, young travelers walking toward an evening market, documentary 35mm photography, intimate atmosphere, no cyberpunk neon saturation, no textual signs unless added separately.

### Vzor 3 – severní japonské městečko

> Realistic vertical street photograph in Ōru Maito (オールマイト), a compact northern town of fictional Larpidia. Narrow lived-in Japanese-influenced residential streets mixed with occasional British-inherited brick houses, modest shops, compact cars, overhead utility detail and carefully maintained sidewalks, humid evening after rain, warm convenience-store lighting, authentic pedestrians, subtle anime-adjacent atmosphere without recreating any actual anime artwork or branded character, editorial travel photo.

### Vzor 4 – průmysl, na který jsou obyvatelé hrdí

> Natural architectural photograph from a public elevated pedestrian viewpoint above the sustainable industrial district in eastern Larpidia. Beautifully landscaped low-rise manufacturing campuses, modular production buildings with open courtyards, shade trees and sheltered bike parking, community school and café next to industrial research facilities, a small modern port in the distance, realistic low-emissions infrastructure, mild sunlight, coherent actual scale, professionally shot but not a generic science fiction factory, 16:9.

## Kontrola kvality

Na každou sérii vygeneruj kontrolní tabulku: `soubor | ID lokace | období | poměr stran | kontinuita | problém k opravě`. Pokud je v obrázku chyba, oprav jej cíleně, nepřepisuj kvůli tomu celou geografii.
