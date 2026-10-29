# LARPIDIA AI STUDIO — verze 1.0

**Školní projekt ZSV (fiktivní stát).** Autoři: František Chalupecký, Ondřej Kynčl, Matěj Klimeček, Štěpán Žemlička.

> Všechna místa, instituce, smlouvy, události, ekonomické ukazatele a návštěvy influencerů Larpidie jsou součástí fikce. Uvedené skutečné značky nemají s projektem žádnou dohodu ani jej neschválily. Košťál je fiktivní postava.

## Proč tento balíček vznikl

Jeden masivní prompt má tendenci vymýšlet při každé generaci jinou podobu země. Toto je sada propojených souborů s jedním zdrojem pravdy, konzistentní mapovou topologií a oddělenými úlohami pro text, obrázky, mapy, video a školní prezentaci.

## Obsah

- `LARPIDIA_MASTER_PROMPT.md` – zkopírovatelný hlavní prompt pro běžný chat s LLM.
- `SKILL.md` – návod pro agenta se schopností načítat skilly a soubory (formát Agent Skills).
- `data/larpidia_world_bible.json` – strojově čitelný kanonický model světa, se stavem jednotlivých tvrzení.
- `references/GEOGRAPHY_AND_CANON.md` – přesné prostorové vztahy a pravidla kontinuity.
- `references/REALISM_AND_ZSV.md` – věrohodnost, ekonomika, právo, klimatické kompromisy a návrhy alternativ.
- `templates/IMAGE_PROMPT.md` – tvorba realistických fotografií včetně sociálních sítí.
- `templates/MAP_PROMPT.md` – mapy, satelitní styl, plán města a udržování stejných tvarů ostrovů.
- `templates/VIDEO_PROMPT.md` – krátká videa, reels a vertikální Stories.
- `templates/PRESENTATION_PROMPT.md` – prezentace, plakát, grafy a ZSV.
- `templates/WORLD_BUILDING_PROMPT.md` – rozšiřování historie, politiky, měst a muzea.
- `START_HERE_PROMPTS.md` – hotové zadávací věty k vložení do chatu.
- `templates/UNIVERSAL_COUNTRY_TEMPLATE.md` – univerzální prázdná šablona pro spolužáky.
- `scripts/validate_bible.py` – lokální kontrola základních invariantů databáze.

## Nejrychlejší způsob použití

**ChatGPT / Gemini / běžný chat Claude:** Přilož `data/larpidia_world_bible.json` a vlož text z `LARPIDIA_MASTER_PROMPT.md`. Když jde o jednu konkrétní práci, přilož i příslušný soubor ze složky `templates`. Pokud lze připojit celou složku projektu, nahraj ji celou a požádej o načtení `SKILL.md`.

**Claude s podporou vlastních Skills:** Použij samostatný soubor `Larpidia_Claude_Skill_v1.zip` (v jeho kořeni je `SKILL.md`). Archiv `Larpidia_AI_Studio_v1.zip` obsahuje navíc nadřazenou složku a slouží hlavně pro sdílení nebo rozbalení. Balíček je navržen ve formátu Agent Skills. Pokud služba konkrétní podobu archivu odmítne, nahraj soubory ručně jako přílohy (způsob instalace se může lišit). Oficiální dokumentace: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

**Důležité:** Samotný prompt nevytváří soubory či videa bez dostupných nástrojů. Agent má pouze provést úlohy, k nimž má skutečně nástroje, a zbytek předat jako konkrétní zadání pro jiný nástroj.

## Pracovní postup

1. Načti World Bible a přečti, co je `approved` a co `proposed`/`needs_decision`.
2. Nejprve vytvoř definitivní vrstevnicovou/topologickou mapu a hlavní registry míst. Nejdříve zafixuj orientaci sever–jih a tvar obou ostrovů.
3. Schval názvy / návrhové parametry; pouze poté změň stav na `approved`.
4. Generuj jednu skupinu výstupů na zadání (např. 5 fotografií stejné oblasti).
5. Před každou vizualizací ověř vazbu na registry; změny synchronizuj zpět do databáze.
6. Prezentace a plakát vytvářej až nad verzovanými definitivními texty a mapami.

## Úpravy a verzování

Každá změna pravidel se zapíše do JSON a zvýší se `meta.version`. Při sporu platí pořadí: výslovné nové schválení skupiny > schválené údaje ve World Bible > návrhy v souborech > stylistické preference generátoru.

`approved` = sděleno autory, `proposed` = pracovní návrh AI, `needs_decision` = doplnit či potvrdit. Číselné hodnoty od AI musejí být jasně označené jako modelové.
