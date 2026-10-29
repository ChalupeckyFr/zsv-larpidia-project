---
name: larpidia-creative-studio
description: Tvoří konzistentní texty, mapy, fotorealistické obrázky, videoprompty a školní podklady fiktivního státu Larpidie. Použij při každém požadavku na Larpidii.
---

# Larpidia Creative Studio

Tento skill řídí produkci světa fiktivního státu Larpidie pro středoškolský projekt ZSV.

## Vstupy – načítání podle potřeby

1. **Vždy načti** `data/larpidia_world_bible.json`. Je to jediný zdroj kanonických dat.
2. Pro mapy, konkrétní lokality a venkovní scény načti `references/GEOGRAPHY_AND_CANON.md`.
3. Pro politiku, daně, průmysl, zákony a klimatologii načti `references/REALISM_AND_ZSV.md`.
4. Pro jednotlivé úlohy načti právě odpovídající šablonu z `templates/`.
5. Při neurčité žádosti použij `LARPIDIA_MASTER_PROMPT.md` jako výchozí provozní postup.

## Závazné priority

- Rozlišuj `approved` × `proposed` × `needs_decision`. Návrhy označ jasně, nikdy je nevydávej za rozhodnutí týmu.
- Vše je fikce. Skutečné značky nejsou skuteční partneři, Košťál není skutečný veřejně obviňovaný člověk. Instagram Stories nesmí nepravdivě dokládat návštěvu konkrétní reálné osobnosti.
- Všechny lokality, orientace, reliéf, železnice a tvary ostrovů musí být konzistentní napříč mapami a záběry.
- Nedodávej fiktivní data jako reálné statistiky. Modelové hodnoty a rozpočty označ.
- Neuváděj, že jsi vytvořil obrázek, video, graf, GIS soubor nebo prezentaci, pokud skutečně nevznikl. Při absenci nástroje dej exportovatelný prompt nebo zdrojová data.
- Zážitkové extrémy prezentuj jako bezpečná vyhlídková místa, nikoli jako návody na nebezpečné kaskadérské aktivity.
- Zachovávej stručné, dobře strukturované a vizuálně použitelné texty v češtině se správnou diakritikou.

## Workflow

**Fáze 1: Pochop zadání.** Identifikuj typ úlohy, platformu, požadovaný počet výstupů a jejich orientaci; doplň vhodné výchozí volby, pokud uživatel neurčí.

**Fáze 2: Ověř kontinuitu.** Pro každou lokality zkontroluj ID a sousedství. Neukazuj pláže na útesovém severozápadě a horské vrcholy uvnitř nížinného města. Paraland je samostatný menší ostrov.

**Fáze 3: Dodej výrobní specifikaci.** U obrazů jedno zadání na jeden snímek; u videí storyboard a motion; u map měřítko, severku, topologii, legendu; u ekonomiky vzorce; u historie chronologii.

**Fáze 4: Vykonej nebo předej.** Pokud je dostupný nástroj, vytvoř reálný výstup. Není-li, dodej přesný prompt a soupis zdrojových referencí.

**Fáze 5: Kontrola.** Zkontroluj 1) soulad s kanonem; 2) vizuální styl; 3) dějepisné a ekonomické vysvětlení; 4) místa a roční období; 5) označení fikce.

## Obvyklé pokyny uživatele

- „Vytvoř 4 fotky ze západních hor“ → `templates/IMAGE_PROMPT.md` + geografie.
- „Dej mi satelitní mapu ostrovů“ → `templates/MAP_PROMPT.md` + geografie. Označ jako fikční satelitně stylizovanou mapu.
- „Vygeneruj 12s story z vlaku“ → `templates/VIDEO_PROMPT.md` + geografie.
- „Připrav ZSV prezentaci“ → `templates/PRESENTATION_PROMPT.md` + realismus a data.
- „Doplň dějiny muzea Košťála“ → `templates/WORLD_BUILDING_PROMPT.md` + právní uvěřitelnost.

## Poznámka k dlouhým úlohám

Nedělej vše v jedné generaci. Nejprve bible / mapa, poté obrázky, po nich prezentace. Předpoklady explicitně zapisuj do výstupu a připrav nové hodnoty k odsouhlasení.
