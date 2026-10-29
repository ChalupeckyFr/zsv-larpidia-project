# ATLAS — Mapy, satelitní styl a plán města

## Mapy vytvářej od geografie k estetice

**První výstup nikdy nesmí být jen nahodilá image-gen mapa s vymyšlenými názvy.** Nejprve vytvoř vektorové pobřeží obou ostrovů (SVG nebo GeoJSON), jejich relativní polohu, fixní reliéf a registry bodů v `GEOGRAPHY_AND_CANON.md`.

### Kanonická sekvence

1. MASTER OUTLINE: jeden společný neměnný obrys Larpidie a Paralandu, severka, 2–3 km průliv podle schválené hodnoty (zatím návrh 1,5 km), realistická plocha a měřítko.
2. RELIEF: vrstevnice nebo hypsometrie, západní pohoří do 500–600 m, nížinný východ, přehrada a tok horské řeky do moře.
3. HUMAN LAYER: hlavní město na jihu/jihovýchodě, severní městečka, východní průmysl, západní přírodní stezky; okružní silnice, tři železniční linky, přístavy a letiště.
4. STYLE: politická mapa, fyzická mapa, historická mapa, turistická mapa nebo satelitní styl. Všechny používají stejnou geografickou základnu.
5. LABELING: všechny názvy, legendy, měřítka a symboly vkládej jako editovatelné typografické vrstvy pro češtinu a japonštinu.

### Dva povinné snímky ostrovů v satelitním stylu

**S-01 / Larpidie:** šikmý či kolmý fotorealistický letecký/satelitně vypadající pohled na hlavní ostrov, západní zalesněné pohoří, východní průmysl, jižní město, zátoky a malé letiště. Bez vymyšleného pobřeží. Výslovně označeno *simulovaná satelitní vizualizace fiktivního ostrova*.

**S-02 / Paraland:** samostatný pohled na menší ostrov, historické městečko na severu, západní marina, střední hotely a aquapark, lesnatý východ. Tvar musí odpovídat master outline.

### M-01 / Plán hlavního města

Vhodný detail pro zakreslení správních budov, názvů čtyř čtvrtí, vlakových stanic (L2, L3), parlamentu, historického kostela, interaktivního muzea Košťálovy éry, tržiště, hlavního přístavu, parku, půjčoven, obchodů a kaváren.

Výrobní specifikace: primárně editovatelná vektorová mapa; nejprve dopravní graf a uliční síť, potom budovy a POI; severka, měřítko a legenda. Měřítko uváděj pouze tehdy, když georeferenční nebo aspoň lokální metrický model skutečně určuje délky ulic. U návrhu bez měřítkového podkladu napiš „schematický plán“.

### Historická mapa

1608–1800: perokresba na zažloutlém pergamenu, navigační růžice, přístav prvních osadníků, dobová toponyma a zemědělská půda. Nezakresluj moderní vysokorychlostní tunel, letiště ani továrny. Historická mapa používá stejné pobřeží, pouze dobovou znalost země a odpovídající sídla.

### Prompt pro vizuální styling (EN)

> A fictional, scientifically plausible satellite-style island atlas visualization, based strictly on the supplied fixed shoreline outline and topographic reference geometry, western forested mountains peaking around 560 m, eastern lowlands, southeastern historical capital and harbor, realistic coast and ocean coloration, credible human development scale. [STYLE]. Preserve the exact islands' silhouette, compass orientation and all canonical landmark placements. Do not create new islands, move ports, replace the eastern industrial region with mountain ridges, or generate made-up labels. Cartographic text will be composited separately.

**Pozor:** Samotné textové promptování generátoru není spolehlivá metoda vytváření přesné mapy. Je nutné předat mu referenční obrázek schváleného obrysu nebo výsledný snímek kompozitovat s GIS/SVG podkladem.
