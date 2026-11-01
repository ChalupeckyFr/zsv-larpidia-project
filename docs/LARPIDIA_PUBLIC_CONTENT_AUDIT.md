# Audit veřejného obsahu Larpidie

**Datum auditu:** 1. listopadu 2026  
**Rozsah:** aktivní web, aktivní atlas a plán Larpingtonu, oba 3D modely, galerie, zdrojové články encyklopedie a podklady určující jejich aktuální kánon.  
**Pravidlo:** tento report mapuje problémy. Neznámá fakta ani návrhy níže nejsou schváleným kánonem.

## 1. Shrnutí

- V aktivním webu jsem prošel zdroj a routování **55 samostatných zobrazení**: hlavní stránku; rozcestník, 9 kategorií a 39 článků encyklopedie; atlas; plán města; oba 3D modely a galerii. Ověřil jsem také 10 starších `#wiki-*` aliasů v kódu, které vedou na současné stránky.
- V inventáři je **70 záznamů o výskytech** a **64 unikátních problémů** po sloučení duplicit. Počítání výskytů bere jednu položku za jednotlivé veřejné místo; u opakovaného detailu registry každou kartu/záznam a u galerie každou scénu. Takto vychází **951 evidovaných umístění**. Nálezy zahrnují veřejná pracovní označení, editorské poznámky, nepodložené detaily, UX a rozpory s aktuálním kánonem.
- Závažnost skupin: **kritická 6**, **střední 27**, **drobná 37**. Kritické jsou tvrzení či názvy naznačující parlament a riziko přímého zpřístupnění interních podkladů, pokud se nasadí statický server s celým pracovním stromem.
- Výskytové počty, které jsou vyšší než jedna: `CS-002` 2, `CS-003` 2, `CS-008` 2, `CS-009` 159, `CS-016` 662, `CS-017` 3, `CS-018` 2, `CS-019` 2, `CS-022` 2, `CS-023` 24, `CS-024` 24, `CS-031` 4, `CS-042` 2, `CS-047` 2, `CS-063` 3 a `CS-065` 2. Každý další záznam `CS-*` počítá jedno umístění. Devět přímo ověřených interních URL v `CS-025` je vedeno zvlášť jako riziko přístupu k souborům, ne jako další textová umístění.
- Při sloučení duplicit se šest parlamentních zmínek `CS-014`, `CS-017`–`CS-019`, `CS-021` a `CS-022` počítá jako jeden problém; opakovaný výpočet oprávněných důchodců `CS-043`/`CS-046` jako druhý. Ostatní tematické opakování je již sdruženo do jednoho `CS-*` záznamu.
- Prošel jsem všech **39 článků Markdown**, katalog 9 kategorií, centrální `facts.json`, aktivní mapové datové registry a textové části veřejných HTML/JS. Dynamické detaily atlasu a městského plánu jsem kontroloval ze zdrojových registrů a jejich vykreslovací logiky.
- **Omezení vizuální kontroly:** automatický snímek stránky se v dostupném prostředí nepodařilo pořídit. Proto netvrdím, že jsem každou dynamickou stránku ručně otevřel a vizuálně prošel v prohlížeči. Mobilní pořadí prvků jsem zkontroloval ve zdrojových CSS; fyzické ovládání na zařízení ne.
- Na lokálním náhledu `scripts/serve_static.mjs` vrátilo HTTP 200 pro přímé URL k interním Markdownům, starším zdrojům, kánonu a mapovým interním seznamům. Jde o **lokální náhled, ne důkaz konfigurace veřejného hostingu**. Pokud se nasadí stejným způsobem z kořene projektu, tyto soubory budou dostupné i mimo hlavní navigaci.
- Výraz **„Hranice rozumu“** ani jeho varianta bez diakritiky se v kontrolovaných aktivních veřejných souborech nenašla. Výraz byl jen v zadání auditu.

### Provedené bezpečné úpravy části A

- Veřejný úvod encyklopedie používá slogan „Objevte Larpidii. / Ostrovní svět plný příběhů.“; text zve k poznávání země a odkaz na editorův návod byl odstraněn.
- Čtyři karty přehledu čerpají obyvatelstvo a délku pracovního týdne z centrálních faktů; politická karta říká „Ústavní spoluvláda“ a odkazuje na článek. Turistické útraty se počítají z modelovaných návštěv a výdajů, nejsou označené jako státní příjem.
- Odstranil jsem technickou větu o načítání dat z článku „Přehled“ a změnil nadpis „Krátké představení pro prezentaci“ na „Stručné představení“. Článek nadále nabízí užitečný souhrn.
- Karta mapy už návštěvníka nezve do „otevřených rozhodnutí“; nyní popisuje potvrzená a orientační místa. Odkaz „Přejít do galerie“ vede na existující `#galerie`.
- Barvy textu na tlačítkách mají změřený kontrast nejméně **4,5:1** ve výchozím, hover, active a disabled stavu. Přidán je viditelný `focus-visible`.

## 2. Úplný inventář nálezů

Výňatky jsou krátké části skutečného veřejného textu nebo textu zobrazovaného po výběru záznamu. „Bez duplicity“ znamená samostatný obsahový problém; „duplicitní“ odkazuje na další výskyt téže věci uvedený v záznamu. Návrhy níže jsou redakční doporučení, nikoli automaticky provedené změny. U nepotvrzených údajů je bezpečným dočasným textem jejich vynechání, ne doplnění odhadem.

### Hlavní stránka, atlas, město, 3D a galerie

**CS-001 — TECHNICKÝ ÚNIK · drobná · bez duplicity.**  
**Routa/sekce:** `#atlas`, zápatí mapové sekce. **Zdroj:** [`index.html:130`](../index.html).  
**Výňatek:** „Atlas v1.0-draft · prostorová data jsou pracovní návrh.“  
**Kánon:** nejde o tvrzení o světě, ale o interní verzi a stav GIS. **Doporučený text:** „Atlas Larpidie · orientační mapa“; upozornění, že jde o fiktivní mapu, ponechat jednou v popisu. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-002 — NEPOTVRZENÉ FAKTUM / UX-PROBLÉM · střední · duplicitní.**  
**Routa/sekce:** `#domu`, železniční karta a související článek. **Zdroj:** [`index.html:120`](../index.html), [`content/larpidia/mesta-a-doprava/zeleznice.md:1`](../content/larpidia/mesta-a-doprava/zeleznice.md).  
**Výňatek:** „Stav celé linky není v potvrzeném kánonu upřesněn“ (L1/L2).  
**Kánon:** v2.6 výslovně rozlišuje existenci/trasu a provozní stav jednotlivých úseků; pro L3 potvrzuje městský úsek v provozu a podmořský ve výstavbě, na Paraland jezdí lodě/trajekty (§39, zejména 88A). Stav L1/L2 jako celku není v článku doložen. **Doporučený text:** pro veřejný web vynechat interní poznámku a uvádět jen stav konkrétních úseků, jakmile jej autor potvrdí; L3 ve výstavbě ponechat jako skutečnost fikčního světa. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-003 — EDITORSKÁ POZNÁMKA · drobná · opakováno 2×.**  
**Routa/sekce:** `#galerie`, přehled galerie. **Zdroj:** [`index.html:136`](../index.html), [`index.html:142`](../index.html).  
**Výňatek:** „fotografie a videa zatím nebyly vygenerovány“ / „se v balíčku zatím nevygenerovaly“.  
**Kánon:** netýká se fikčního světa; popisuje výrobu webového obsahu. **Doporučený text:** „Galerie představuje připravené obrazové scény a mapové podklady“; u ilustrací případně jasně označit, že jde o vizualizace. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-004 — EDITORSKÁ POZNÁMKA · drobná · bez duplicity.**  
**Routa/sekce:** `#atlas`, popisek leteckého pohledu na Larpington. **Zdroj:** [`index.html:126`](../index.html).  
**Výňatek:** „Letecký pohled na pracovní návrh Larpingtonu“.  
**Kánon:** plán města je vizualizace, ale výraz „pracovní návrh“ je interní stav projektu. **Doporučený text:** „Orientační vizualizace Larpingtonu z výšky.“ **Postup:** JASNÉ — LZE OPRAVIT.

**CS-005 — TECHNICKÝ ÚNIK · střední · bez duplicity.**  
**Routa/sekce:** samostatný interaktivní atlas, záhlaví. **Zdroj:** [`atlas/current/viewer/atlas.html:22`](../atlas/current/viewer/atlas.html).  
**Výňatek:** „NÁVRH · v1.0-draft“.  
**Kánon:** verze a pracovní stav nejsou vlastnosti Larpidie. **Doporučený text:** „Orientační atlas fiktivní Larpidie“; mapové nejistoty popsat čtenářsky srozumitelně v legendě. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-006 — NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** atlas, příklad v poli hledání. **Zdroj:** [`atlas/current/viewer/atlas.html:23`](../atlas/current/viewer/atlas.html).  
**Výňatek:** „např. N-03, přístav, Aokawa“.  
**Kánon:** Aokawa má v registru jméno `proposed`; příklad jej nabízí bez tohoto rozlišení. **Doporučený text:** změnit příklad na neutrální potvrzené ID, nebo na „zkuste název či ID místa“ bez názvu. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-007 — TECHNICKÝ ÚNIK · střední · bez duplicity.**  
**Routa/sekce:** atlas, text vytištěný přímo na mapě. **Zdroj:** [`atlas/current/viewer/atlas.html:739`](../atlas/current/viewer/atlas.html).  
**Výňatek:** „Polohy, výšky a trasy jsou pracovní návrh; schválená je jen existence prvků podle World Bible.“  
**Kánon:** část vystihuje rozdílnou jistotu mapových údajů, ale odkazuje návštěvníka na pracovní soubor a vnitřní schvalovací stav. V2.6 navíc říká, že starší World Bible je podřízený zdroj. **Doporučený text:** „Mapa je orientační; názvy a poloha některých míst se mohou lišit od jejich obecného popisu.“ Přesný rozsah schválených poloh ověřit před zkrácením. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-008 — EDITORSKÁ POZNÁMKA · drobná · bez duplicity.**  
**Routa/sekce:** atlas, legenda vrstvy stavu. **Zdroj:** [`atlas/current/viewer/atlas.html:805`](../atlas/current/viewer/atlas.html).  
**Výňatek:** „Pracovní návrh“ a „Čeká na rozhodnutí“.  
**Kánon:** jde o stav registrace údajů, nikoli o druh místa ve světě. **Doporučený text:** zachovat rozlišení jistoty, ale přejmenovat na návštěvnické „Orientačně umístěno“ a „Poloha či název nejsou upřesněny“ po potvrzení významu jednotlivých barev. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-009 — EDITORSKÁ POZNÁMKA · střední · opakováno v interaktivních detailech 159 záznamů.**  
**Routa/sekce:** atlas, kliknutelné záznamy míst. **Zdroj:** [`atlas/current/viewer/atlas.html:807`](../atlas/current/viewer/atlas.html), vykreslení detailu v téže stránce kolem řádků 823–837; datový zdroj [`atlas/current/registry/places.json`](../atlas/current/registry/places.json).  
**Výňatek:** „existence / název / poloha“, „pseudo (hypothetical)“, „Bible“, `photo_guide`, „Pohled kam“, „Roční doba“, „Vyhnout se“.  
**Kánon:** registr má 159 míst: 51 existencí označeno jako approved, 108 proposed; 149 názvů proposed, 6 needs-decision; všech 159 poloh proposed. Pop-up ale návštěvníkovi ukazuje i zdrojové odkazy, pracovní poznámky a instrukce pro tvorbu snímků. **Doporučený text:** veřejná karta místa má obsahovat název, druh, obecnou polohu a ověřené vysvětlení; produkční pokyny a interní reference oddělit od veřejného detailu. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-010 — NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** atlas, vrchol M-01 a navazující detaily. **Zdroj:** [`atlas/current/viewer/atlas.html:807`](../atlas/current/viewer/atlas.html), [`atlas/current/registry/places.json:21`](../atlas/current/registry/places.json).  
**Výňatek:** „Nejvyšší vrchol, pracovní 560 m“; zdrojová poznámka „560 m = proposed“.  
**Kánon:** v2.6 nepotvrzuje přesnou maximální nadmořskou výšku. Starší geografická poznámka označuje 560 m jako návrh. **Doporučený text:** „nejvyšší vrchol hlavního ostrova“ bez výšky, dokud se výška a měření nepotvrdí. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-011 — TECHNICKÝ ÚNIK · drobná · bez duplicity.**  
**Routa/sekce:** samostatný 3D reliéf. **Zdroj:** [`atlas/current/viewer/terrain-3d.html:35`](../atlas/current/viewer/terrain-3d.html).  
**Výňatek:** „NÁVRH · modelové výšky“.  
**Kánon:** správně říká, že nejde o geodetické měření, ale první slovo popisuje fázi tvůrčí práce. **Doporučený text:** „Ilustrativní 3D reliéf“ a krátké upozornění, že výšky jsou orientační. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-012 — TECHNICKÝ ÚNIK / NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** 3D Larpington. **Zdroj:** [`atlas/current/capital/capital-3d.html:23`](../atlas/current/capital/capital-3d.html), [`atlas/current/capital/capital-3d.html:29`](../atlas/current/capital/capital-3d.html).  
**Výňatek:** „PRACOVNÍ MODEL · CP-01“, „budoucí návrh v rezervě“ a modelové město s populací 12 000.  
**Kánon:** plán a výstavba mají být odlišeny od existujících prvků; údaj 12 000 obyvatel města se v aktuálním v2.6 nepodařilo dohledat. **Doporučený text:** nazvat výstup „Ilustrativní 3D model Larpingtonu“; hodnotu 12 000 nezobrazovat jako fakt, dokud se neurčí její zdroj a význam. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-013 — TECHNICKÝ ÚNIK · drobná · bez duplicity.**  
**Routa/sekce:** samostatný plán Larpingtonu, záhlaví. **Zdroj:** [`atlas/current/capital/capital_plan_viewer.html:18`](../atlas/current/capital/capital_plan_viewer.html).  
**Výňatek:** „NÁVRH · v1.0-draft“.  
**Kánon:** verze a draft nejsou veřejný popis města. **Doporučený text:** „Orientační plán Larpingtonu“. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-014 — ROZPOR S KÁNONEM / UX-PROBLÉM · kritická · duplicita tematické skupiny CS-017.**  
**Routa/sekce:** hledání v plánu Larpingtonu. **Zdroj:** [`atlas/current/capital/capital_plan_viewer.html:19`](../atlas/current/capital/capital_plan_viewer.html).  
**Výňatek:** „CP-B01, parlament, tržnice“.  
**Kánon:** Larpidie nemá parlament ani poslance (v2.6, rozhodnutí 2; závazný přehled §41). Příklad hledání tak nabízí instituci, která neexistuje. **Doporučený text:** „CP-B01, radnice, tržnice“ až po opravě záznamu CP-B01. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-015 — EDITORSKÁ POZNÁMKA · drobná · bez duplicity.**  
**Routa/sekce:** plán města, ovládací prvky a názvy mapových vrstev. **Zdroj:** [`atlas/current/capital/capital_plan_viewer.html:21`](../atlas/current/capital/capital_plan_viewer.html) a dynamické popisky vrstev.  
**Výňatek:** „Obrysy podle stavu (schváleno × návrh)“; názvy vrstev opakují „návrh“ a kandidátní POI.  
**Kánon:** mapový podklad je schematický, ale vrstvy popisují stav redakčního rozhodování. **Doporučený text:** ponechat přepínače věcných vrstev; nejistou přesnost vysvětlit jedním čtenářským upozorněním, interní kandidáty nezobrazovat jako atrakce. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-016 — EDITORSKÁ POZNÁMKA · střední · opakováno v interaktivních detailech 662 záznamů.**  
**Routa/sekce:** plán Larpingtonu, kliknutelné objekty. **Zdroj:** [`atlas/current/capital/capital_plan_viewer.html`](../atlas/current/capital/capital_plan_viewer.html), registry [`atlas/current/capital/cp_objects.json`](../atlas/current/capital/cp_objects.json).  
**Výňatek:** v kartách se zobrazují „Bible / zadání“, existence, návrhové názvy a polohy a interní `notes`.  
**Kánon:** 662 záznamů; pouze 6 má `exist_status=approved`, 656 `proposed`; všech 662 názvů a poloh je označeno jako proposed. **Doporučený text:** veřejné karty rozdělit na ověřené místo a orientační plánovací prvek; nezobrazovat zdrojové klíče a autorské poznámky. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-017 — ROZPOR S KÁNONEM · kritická · stejný rozpor ve 3 zdrojích.**  
**Routa/sekce:** plán a 3D Larpingtonu; objekt CP-B01. **Zdroj:** [`atlas/current/capital/cp_objects.json:162`](../atlas/current/capital/cp_objects.json), jeho kopie v HTML registru; [`atlas/current/capital/capital-3d-data.js`](../atlas/current/capital/capital-3d-data.js).  
**Výňatek:** „Radnice a parlament Larpingtonu“, poznámka „sídlo parlamentu“; 3D název „Larpington Town Hall and Parliament House“.  
**Kánon:** žádný parlament neexistuje. Budova radnice je samostatné potvrzené téma; parlamentní část názvu a popisu je zastaralý návrh. **Doporučený text:** veřejně uvést pouze radnici, pokud její totožnost odpovídá aktuálnímu rozhodnutí; odstranit parlament z názvu, poznámek i 3D labelu až v rámci schválené opravy. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-018 — ROZPOR S KÁNONEM · střední · duplicita CS-017.**  
**Routa/sekce:** atlas, detail `ST-S`. **Zdroj:** [`atlas/current/registry/places.json:5457`](../atlas/current/registry/places.json); obdobný záznam v plánu města kolem řádku 2166.  
**Výňatek:** poznámka u místa uvádí „parlament“.  
**Kánon:** jde o pozůstatek staršího úkolu; v2.6 výslovně přikazuje nepovažovat jej za existující budovu parlamentu. **Doporučený text:** odkazovat jen na potvrzenou funkci místa, nebo záznam skrýt do vyřešení polohy. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-019 — ROZPOR S KÁNONEM · kritická · duplicita CS-017.**  
**Routa/sekce:** přímá URL k datům, pokud je nasazen celý pracovní kořen. **Zdroj:** [`data/larpidia_world_bible.json:34`](../data/larpidia_world_bible.json), [`data/larpidia_world_bible.json:449`](../data/larpidia_world_bible.json).  
**Výňatek:** „demokraticky volený parlament“; `"elected_parliament": true`.  
**Kánon:** tento soubor je starší a podřízený aktuálnímu v2.6; parlament byl zrušen. **Doporučené řešení:** nepublikovat starší World Bible jako současný veřejný zdroj; zachovat ji jako archiv a aktualizovat pouze schválenou veřejnou prezentaci. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-020 — NEPOTVRZENÉ FAKTUM / ZASTARALÝ STAV · střední · bez duplicity.**  
**Routa/sekce:** přímá URL k World Bible. **Zdroj:** [`data/larpidia_world_bible.json:64`](../data/larpidia_world_bible.json), `population_working_model.status` (soubor uvádí verzi/datum draftu v metadatech).  
**Výňatek:** počet obyvatel 32 000 je ve starém souboru veden jako „proposed“.  
**Kánon:** 32 000 je v aktuálním v2.6 součástí schváleného modelu populace. Rozpor se týká stavu a autority zdroje, ne samotné hodnoty. **Doporučené řešení:** skrýt starou bibli z veřejného statického kořene a používat aktuální centrální fakta. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-021 — ROZPOR S KÁNONEM · kritická · duplicita CS-017.**  
**Routa/sekce:** přímá URL ke geografickému pracovnímu podkladu, pokud je kořen veřejný. **Zdroj:** [`references/GEOGRAPHY_AND_CANON.md:80`](../references/GEOGRAPHY_AND_CANON.md).  
**Výňatek:** pokyn zakreslit „jednu budovu parlamentu“.  
**Kánon:** v2.6 potvrzuje bezparlamentní ústavní systém a označuje starý parlament v mapových zadáních za zastaralý návrh. **Doporučené řešení:** zachovat původní soubor jako archiv; nepředkládat jej jako platnou referenci. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-022 — ROZPOR S KÁNONEM · kritická · duplicita CS-017.**  
**Routa/sekce:** přímá URL k realism/research poznámce, pokud je kořen veřejný. **Zdroj:** [`references/REALISM_AND_ZSV.md:5`](../references/REALISM_AND_ZSV.md), [`references/REALISM_AND_ZSV.md:7`](../references/REALISM_AND_ZSV.md).  
**Výňatek:** návrh „15 poslanců“ a jednokomorový parlament.  
**Kánon:** jde o překonaný návrh; aktuální systém parlament nemá. **Doporučené řešení:** archivovat mimo veřejný web, nevydávat za dnešní právní model. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-023 — EDITORSKÁ POZNÁMKA · drobná · opakováno 24×.**  
**Routa/sekce:** galerie, všech 20 fotografií a 4 videa. **Zdroj:** [`v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/06_GALLERY/index.html:105–916`](../v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/06_GALLERY/index.html).  
**Výňatek:** u každé scény je `status: "prompt-ready"`, stav „připraveno k vygenerování“ a `generated_image: null`.  
**Kánon:** jde o správný produkční stav obrazových souborů, ale není to popis Larpidie a opakuje se ve veřejných kartách. **Doporučený text:** návštěvnické označení „návrhová scéna“ / „ilustrativní vizualizace“, případně galerii zobrazovat až s hotovými vizuály. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-024 — TECHNICKÝ ÚNIK · střední · opakováno v 24 scénách a jejich metadatech.**  
**Routa/sekce:** galerie, rozbalení scény a přímé soubory promptů/JSON. **Zdroj:** tentýž `06_GALLERY/index.html` (scény `PHOTO_01`–`PHOTO_20`, `VIDEO_01`–`VIDEO_04`) a soubory pod `03_PHOTO_PROMPTS/`, `04_PHOTO_METADATA/`.  
**Výňatek:** „open prompt“, „PROPOSED CAMERA POINT“, cesty `expected_photo`, „ChatGPT/Gemini“ a výrobní metadata `canon_notes_cs`.  
**Kánon:** části jako kamera, výška, mapa a „avoid“ jsou produkční instrukce, ne veřejný popis místa. **Doporučené řešení:** veřejnou galerii oddělit od promptů a interního JSON registru; ponechat jen popisek, zdroj vizualizace a vazbu na místo. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-025 — TECHNICKÝ ÚNIK / BEZPEČNOST PUBLIKACE · kritická · bez duplicity.**  
**Routa/sekce:** všechny přímé cesty pod kořenem projektu, ne pouze UI. **Zdroj:** [`scripts/serve_static.mjs`](../scripts/serve_static.mjs).  
**Výňatek:** server mapuje URL přímo na libovolný soubor pod kořenem a filtruje jen únik mimo kořen; nemá seznam zakázaných interních cest. Lokální `HEAD` vrátil 200 pro kánon, World Bible, oba pracovní geografické dokumenty, tento úkol, editorův návod a mapové interní reporty.  
**Kánon:** pracovní archiv má zůstat interním podkladem. **Doporučené řešení:** před veřejným nasazením zveřejnit pouze build/whitelist adresář, nebo v hostingové konfiguraci vyloučit `references/`, pracovní reporty a staré verze; lokální preview samo o sobě neprokazuje, že hosting takto nastavený je. **Postup:** POTŘEBUJE DALŠÍ DATA (nasazovací konfigurace).

### Články encyklopedie — geografie, historie a Paraland

**CS-026 — NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/geografie/ostrovy`, poloha. **Zdroj:** [`content/larpidia/geografie/ostrovy.md:1`](../content/larpidia/geografie/ostrovy.md).  
**Výňatek:** „Přesné zeměpisné souřadnice … jsou pracovní, nikoli potvrzená poloha na skutečné mapě.“  
**Kánon:** potvrzen je fikční severozápadní Pacifik a vzájemná poloha ostrovů, ne skutečné GPS souřadnice. **Doporučený text:** „Larpidie leží ve fikční části severozápadního Pacifiku; atlas ukazuje schematické umístění.“ **Postup:** JASNÉ — LZE OPRAVIT.

**CS-027 — NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/geografie/priroda`, řeky a nádrž. **Zdroj:** [`content/larpidia/geografie/priroda.md:5`](../content/larpidia/geografie/priroda.md).  
**Výňatek:** „průtoky, kapacity nádrží ani přesné názvy řek nejsou … stanovené“.  
**Kánon:** přírodní prvky jsou součástí krajiny, ale tyto hydrologické parametry nejsou doloženy. **Doporučený text:** popsat řeku, nádrž a vodopád bez názvů či čísel, případně úsek skrýt do schválení parametrů. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-028 — EDITORSKÁ POZNÁMKA · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/geografie/priroda`, poznámka pod mapovou vizualizací. **Zdroj:** [`content/larpidia/geografie/priroda.md:11`](../content/larpidia/geografie/priroda.md).  
**Výňatek:** „některé detaily … jsou … návrhové; zobrazená trasa … nepotvrzuje dokončenou stavbu“.  
**Kánon:** nutné oddělit vizualizovanou geometrii od skutečně fungující stavby; to není samo o sobě fikční „construction site“. **Doporučený text:** ponechat upozornění jednou, v krátké podobě: „Atlas je orientační ilustrace; dopravní stavby jsou popsány podle skutečného stavu.“ **Postup:** JASNÉ — LZE OPRAVIT.

**CS-029 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/geografie/ochrana-prirody`, podzemní horská trasa. **Zdroj:** [`content/larpidia/geografie/ochrana-prirody.md:5`](../content/larpidia/geografie/ochrana-prirody.md).  
**Výňatek:** „Samotný atlasový zákres podzemního úseku nepotvrzuje jeho současný provoz.“  
**Kánon:** správné rozlišení mapy od provozu; v2.6 konkrétně zakazuje odvozovat provoz podzemních částí L1 pouze ze zákresu. **Doporučený text:** uvést potvrzený stav této konkrétní části, až bude dohledán; zatím nevydávat mapu za důkaz provozu. **Postup:** POTŘEBUJE DALŠÍ DATA. Nezaměňovat s rozestavěným podmořským L3, který je potvrzené fikční dění.

**CS-030 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/geografie/ochrana-prirody`, horská půjčovna. **Zdroj:** [`content/larpidia/geografie/ochrana-prirody.md:7`](../content/larpidia/geografie/ochrana-prirody.md).  
**Výňatek:** „konkrétní výše, vracení a provozní pravidla nejsou určeny“.  
**Kánon:** potvrzuje vratnou zálohu, ne její výši a pravidla. **Doporučený text:** do veřejného textu ponechat pouze skutečně potvrzenou vratnou zálohu, vynechat podrobná pravidla. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-031 — NEPOTVRZENÉ FAKTUM · střední · opakováno v `ochrana-prirody.md:11`, `turistika-a-rezervace.md:5` a `morska-rezervace.md:3–5`.**  
**Routa/sekce:** `#encyklopedie/geografie/ochrana-prirody`, `#encyklopedie/paraland/turistika-a-rezervace`, `#encyklopedie/paraland/morska-rezervace`. **Zdroj:** uvedené soubory pod `content/larpidia/geografie/` a `content/larpidia/paraland/`.  
**Výňatek:** „Přesný ceník, zóny a limity … nejsou“; „podrobnosti o přesných chráněných zónách lze doplnit“; korálový útes „není potvrzený“.  
**Kánon:** potvrzena je rozsáhlá mořská rezervace a luxusnější turistika; konkrétní zóny, poplatky, kapacity a přesný ekosystém nikoli. V2.6 varuje před vymýšlením korálů. **Doporučený text:** popsat účel rezervace a zásadu ochrany bez čísel a bez konkrétních ekosystémů; interní poznámky o nepotvrzení vynechat. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-032 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/historie/casova-osa`, rok 1921. **Zdroj:** [`content/larpidia/historie/casova-osa.md:8`](../content/larpidia/historie/casova-osa.md).  
**Výňatek:** „Přesný den vyhlášení není určen.“  
**Kánon:** potvrzený je rok 1921, nikoli datum dne. **Doporučený text:** ponechat rok a vynechat redakční poznámku o dni. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-033 — EDITORSKÁ POZNÁMKA · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/historie/kostalova-era`, moc a titul Košťála. **Zdroj:** [`content/larpidia/historie/kostalova-era.md:1`](../content/larpidia/historie/kostalova-era.md).  
**Výňatek:** „Kánon jej nepotvrzuje jako krále ani jako předsedu vlády“.  
**Kánon:** jeho vliv vycházel z hospodářských koncesí; kánon nepotvrzuje titul krále ani premiéra. Samotné upozornění je věcně ochranné, ale odkazuje na redakční autoritu. **Doporučený text:** pozitivně popsat doložený ekonomický vliv a nepřidávat žádný státní titul. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-034 — EDITORSKÁ POZNÁMKA · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/historie/kostalova-era`, tlak a poškozené osoby. **Zdroj:** [`content/larpidia/historie/kostalova-era.md:5`](../content/larpidia/historie/kostalova-era.md).  
**Výňatek:** „Encyklopedie nepřidává nedoložené podrobnosti o jednotlivých obětech, soudech nebo konkrétních metodách nátlaku.“  
**Kánon:** ekonomická nadvláda a společenské dopady jsou potvrzené, seznam obětí a konkrétní metody ne. **Doporučený text:** stručně popsat doložené strukturální dopady; tuto redakční omluvu vynechat. **Postup:** POTŘEBUJE DALŠÍ DATA pro případný další detail.

**CS-035 — NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/historie/kostalova-era`, soudní stav. **Zdroj:** [`content/larpidia/historie/kostalova-era.md:11`](../content/larpidia/historie/kostalova-era.md).  
**Výňatek:** „Přesný rozsudek ani právní titul … nejsou doložené“; budoucí podplácení či návrat jsou „obavy či hypotézy“.  
**Kánon:** Košťál je v aktuálním ději ve vězení; přesný rozsudek ani budoucí výsledek potvrzen není. **Doporučený text:** ponechat pouze aktuální potvrzený stav a hypotézy z veřejného životopisného článku vynechat. **Postup:** POTŘEBUJE DALŠÍ DATA pro právní titul; JASNÉ — LZE OPRAVIT pro odstranění spekulace.

**CS-036 — NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/historie/obnova-a-muzea`, muzea. **Zdroj:** [`content/larpidia/historie/obnova-a-muzea.md:11`](../content/larpidia/historie/obnova-a-muzea.md).  
**Výňatek:** „Larpington má mít hlavní moderní interaktivní historické muzeum.“  
**Kánon:** potvrzuje hlavní muzeum v Larpingtonu a druhou menší expozici na Paralandu, ale konkrétní objekt či provozní připravenost se nesmí odvodit z návrhového plánu. **Doporučený text:** určit, zda jde o otevřené muzeum, schválenou instituci bez lokace, nebo budoucí projekt; do té doby nepoužívat „má mít“ jako veřejný popis dokončeného města. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-037 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/ekonomika/dane`, DPH. **Zdroj:** [`content/larpidia/ekonomika/dane.md:9`](../content/larpidia/ekonomika/dane.md).  
**Výňatek:** „Seznam výrobků a služeb pro sníženou sazbu zatím není přesně určen.“  
**Kánon:** sazby 12 % a 5 % jsou potvrzeny; konkrétní kategorie pro nižší sazbu nejsou úplně rozepsány. **Doporučený text:** uvést sazby a neuvádět příklady výrobků, dokud nebudou rozhodnuty. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-038 — TECHNICKÝ ÚNIK · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/ekonomika/dane`, daň z příjmů. **Zdroj:** [`content/larpidia/ekonomika/dane.md:13`](../content/larpidia/ekonomika/dane.md).  
**Výňatek:** „Kánon uvádí modelová pásma s mezními sazbami“.  
**Kánon:** sazby patří do veřejného modelu, ale slovo „kánon“ je redakční odkaz. **Doporučený text:** „Model daně z příjmů počítá s těmito mezními pásmy:“ (ověřit návaznost na centrální `facts.json`). **Postup:** JASNÉ — LZE OPRAVIT.

**CS-039 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/ekonomika/prace-a-mzdy`. **Zdroj:** [`content/larpidia/ekonomika/prace-a-mzdy.md:3`](../content/larpidia/ekonomika/prace-a-mzdy.md).  
**Výňatek:** „pravidla smluv, přesčasů, minimální mzdy a dovolené nejsou … určené“.  
**Kánon:** potvrzuje standard 24 hodin týdně a směnný režim nepřetržitých služeb, ne úplný pracovní zákoník. **Doporučený text:** zaměřit článek na potvrzený pracovní týden a směny; přesné podmínky uvést až po doplnění pravidel. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-040 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/ekonomika/prace-a-mzdy`, pracovní struktura. **Zdroj:** [`content/larpidia/ekonomika/prace-a-mzdy.md:7`](../content/larpidia/ekonomika/prace-a-mzdy.md).  
**Výňatek:** „Přesné rozdělení podle odvětví ani zaměstnanecký status jednotlivců nejsou potvrzené.“  
**Kánon:** modelový počet pracujících je znám, přesné sektory a statusy nikoli. **Doporučený text:** zobrazovat jen agregované schválené hodnoty; tuto poznámku odstranit, pokud stránka žádné sektorové údaje netvrdí. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA, zda budou odvětvová čísla potřeba.

**CS-041 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/ekonomika/statni-podniky`. **Zdroj:** [`content/larpidia/ekonomika/statni-podniky.md:1`](../content/larpidia/ekonomika/statni-podniky.md).  
**Výňatek:** „Přesné názvy … výrobních kapacity a položkové tržby nejsou … určené.“  
**Kánon:** export řasových paliv a výrobků do Japonska a Jižní Koreje je potvrzen; názvy firem a položková produkce nejsou. **Doporučený text:** ponechat obecný popis státních podniků, nedoplňovat názvy ani tržby bez dat; opravit i gramatickou chybu „výrobních kapacity“. **Postup:** JASNÉ — LZE OPRAVIT pro překlep; jinak VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-042 — NEPOTVRZENÉ FAKTUM · střední · opakováno ve 2 článcích.**  
**Routa/sekce:** ekonomický model a zdravotnictví. **Zdroj:** [`content/larpidia/ekonomika/ekonomicky-model.md:15`](../content/larpidia/ekonomika/ekonomicky-model.md), [`content/larpidia/spolecnost/zdravotnictvi.md:3`](../content/larpidia/spolecnost/zdravotnictvi.md).  
**Výňatek:** „nebylo prokázáno, že částka pokryje … služby“ / „rámec je napjatý a jeho dostatečnost nebyla prokázána“.  
**Kánon:** 1,6 mld. Kč je společný modelový roční rámec zdravotnictví a školství, jeho dostatečnost není doložena. **Doporučený text:** nepředstírat rozpočtové krytí; na veřejné stránce říct, co rámec obsahuje, a nechat vynechání poznámky o nedoložení do doby, než bude uzavřena rozpočtová bilance. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-043 — NEPOTVRZENÉ FAKTUM · drobná · duplicitní s CS-046.**  
**Routa/sekce:** `#encyklopedie/ekonomika/ekonomicky-model`, důchodový výdaj. **Zdroj:** [`content/larpidia/ekonomika/ekonomicky-model.md:19`](../content/larpidia/ekonomika/ekonomicky-model.md).  
**Výňatek:** „skutečný počet oprávněných příjemců není určen“.  
**Kánon:** 16 % populace ve věku 65+ je modelová demografie; automaticky to neznamená stejný počet oprávněných příjemců. **Doporučený text:** označit částku jako horní ilustrativní scénář a nesměšovat ji s rozpočtovým výdajem. **Postup:** JASNÉ — LZE OPRAVIT (popis modelu lze zkrátit bez vymyšlení počtu).

**CS-044 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/spolecnost/zdravotnictvi`, specializovaná péče. **Zdroj:** [`content/larpidia/spolecnost/zdravotnictvi.md:5`](../content/larpidia/spolecnost/zdravotnictvi.md).  
**Výňatek:** „Konkrétní nároky, objem péče a organizace smluv zatím nejsou podrobně popsané.“  
**Kánon:** zahraniční smluvní péče a doprava jsou možným/potvrzeným prvkem modelu, nikoli automatický nárok každého pacienta. **Doporučený text:** ponechat obecný princip a vynechat nevyřešené provozní detaily. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-045 — NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/spolecnost/socialni-podpora-a-duchody`. **Zdroj:** [`content/larpidia/spolecnost/socialni-podpora-a-duchody.md:5`](../content/larpidia/spolecnost/socialni-podpora-a-duchody.md).  
**Výňatek:** „Přesné podmínky pobytu či občanství potřebují dopracování.“  
**Kánon:** základní důchod 12 000 Kč od 65 let je modelově potvrzen, ale okruh oprávněných osob je nutné vyjasnit. **Doporučený text:** výši a věk uvést jako model; nárokové podmínky popsat až po rozhodnutí. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-046 — NEPOTVRZENÉ FAKTUM · drobná · duplicita CS-043.**  
**Routa/sekce:** ekonomický model, výpočet počtu seniorů. **Zdroj:** [`content/larpidia/ekonomika/ekonomicky-model.md:19`](../content/larpidia/ekonomika/ekonomicky-model.md).  
**Výňatek:** „skutečný počet oprávněných příjemců není určen.“  
**Kánon:** stejné rozlišení 65+ a oprávněný důchodce. **Doporučený text:** držet vysvětlení na jedné stránce a na druhé odkazovat na stejný model. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-047 — NEPOTVRZENÉ FAKTUM · střední · opakováno v 2 článcích.**  
**Routa/sekce:** školství a kampusové město. **Zdroj:** [`content/larpidia/spolecnost/skolstvi-a-univerzity.md:5`](../content/larpidia/spolecnost/skolstvi-a-univerzity.md), [`content/larpidia/mesta-a-doprava/kampusove-mesto.md:9`](../content/larpidia/mesta-a-doprava/kampusove-mesto.md).  
**Výňatek:** „Přesný název, obvod a umístění nejsou veřejně určeny“; druhý článek doplňuje počet institucí a adresu.  
**Kánon:** samostatné sídlo, koleje a odborná zaměření jsou potvrzené; jméno, hranice, přesné umístění a počet institucí nikoli. **Doporučený text:** ponechat „kampusové město poblíž Larpingtonu“ a vynechat nevyřešené administrativní detaily. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-048 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/spolecnost/skolstvi-a-univerzity`, školní týden. **Zdroj:** [`content/larpidia/spolecnost/skolstvi-a-univerzity.md:11`](../content/larpidia/spolecnost/skolstvi-a-univerzity.md).  
**Výňatek:** „Délka školního týdne — čtyři, nebo pět dní — rozhodnutá není.“  
**Kánon:** pracovní týden dospělých je 24 hodin, školní rozvrh se z něj nesmí odvozovat (§39, 83A). **Doporučený text:** uvést jen potvrzený nejčasnější začátek výuky; počet dnů vynechat. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-049 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/spolecnost/kultura-a-svatky`, kuchyně. **Zdroj:** [`content/larpidia/spolecnost/kultura-a-svatky.md:1`](../content/larpidia/spolecnost/kultura-a-svatky.md).  
**Výňatek:** „Konkrétní oficiální národní jídlo stanoveno není.“  
**Kánon:** kulinářské vlivy jsou popsány, oficiální pokrm ne. **Doporučený text:** vynechat slovo „národní“ nebo představit běžné suroviny a kuchyňské vlivy bez vymyšleného symbolického pokrmu. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-050 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** stejný článek, hlavní festival. **Zdroj:** [`content/larpidia/spolecnost/kultura-a-svatky.md:7`](../content/larpidia/spolecnost/kultura-a-svatky.md).  
**Výňatek:** „Název a přesný termín hlavního festivalu určené nejsou.“  
**Kánon:** Den larpu a Mog Day jsou dobrovolné komunitní akce; velký festival je samostatná událost, jejíž jméno/datum není uvedeno. **Doporučený text:** dokud se nerozhodne, popsat obecně kulturní a sousedské akce, bez označení konkrétního hlavního festivalu. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

### Politický systém, doprava a bezpečnost

**CS-051 — EDITORSKÁ POZNÁMKA · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/spoluvladci`, tematické resorty. **Zdroj:** [`content/larpidia/politika/spoluvladci.md:10`](../content/larpidia/politika/spoluvladci.md).  
**Výňatek:** osobní „přiřazení portfolií“ spoluvládcům není stanoveno.  
**Kánon:** jsou potvrzené čtyři tematické bloky, ale jejich osobní rozdělení může být neznámé nebo záměrně nevymezené. **Doporučený text:** popsat pouze čtyři oblasti jako kolektivní kompetence a neuvádět interní přiřazovací poznámku. **Postup:** POTŘEBUJE DALŠÍ DATA, pokud se mají uvádět konkrétní osoby a resorty.

**CS-052 — EDITORSKÁ POZNÁMKA · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/ustavni-system`. **Zdroj:** [`content/larpidia/politika/ustavni-system.md:22`](../content/larpidia/politika/ustavni-system.md).  
**Výňatek:** souhrnná věta, že „podrobnosti postupu / časové lhůty / náprava“ potřebují další dopracování.  
**Kánon:** základní ústavní model je podrobně potvrzen, ale některé prováděcí detaily otevřené. **Doporučený text:** stránku rozdělit na schválený proces a případné budoucí prováděcí předpisy; veřejně nevypisovat redakční stav. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA. (Ověřit přesnou formulaci a rozsah této poznámky při následné redakci.)

**CS-053 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/navrhovani-zakonu`. **Zdroj:** [`content/larpidia/politika/navrhovani-zakonu.md:7`](../content/larpidia/politika/navrhovani-zakonu.md).  
**Výňatek:** „Přesné lhůty, zveřejňování odůvodnění a opravné prostředky nejsou zatím úplně stanovené.“  
**Kánon:** občan může návrh podat bez sběru podpisů; před hlasováním proběhne formální a právní kontrola. Prováděcí lhůty nejsou potvrzeny. **Doporučený text:** popsat potvrzenou posloupnost bez závorky o interním stavu. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-054 — NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/schvalovani-zakonu`, elektronický hlasovací systém. **Zdroj:** [`content/larpidia/politika/schvalovani-zakonu.md:13`](../content/larpidia/politika/schvalovani-zakonu.md).  
**Výňatek:** „bezpečnostní návrh … tajnost a audit hlasu … nejsou technicky doložené“.  
**Kánon:** právo hlasovat a veřejné agregované výsledky jsou součástí pravidel, hotová aplikace ale není potvrzena. **Doporučený text:** uvést občanské hlasování a dohled úřadu; nepopisovat neexistující aplikaci ani průběžný digitální režim jako již funkční službu. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-055 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/veto-a-spory`. **Zdroj:** [`content/larpidia/politika/veto-a-spory.md:5`](../content/larpidia/politika/veto-a-spory.md).  
**Výňatek:** „Přesný termín veta a délka smíru nejsou stanovené.“  
**Kánon:** odkladné veto, následné smírčí jednání a možnost předat spor občanům jsou potvrzené; přesné lhůty ne. **Doporučený text:** ponechat popis pravomoci a vynechat časové údaje, které nejsou stanovené. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-056 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/odvolani-spoluvladce`. **Zdroj:** [`content/larpidia/politika/odvolani-spoluvladce.md:15`](../content/larpidia/politika/odvolani-spoluvladce.md).  
**Výňatek:** pravidla opakovaných petic, délka kampaně a kroky po neúspěšném referendu nejsou stanoveny.  
**Kánon:** odvolání má odlišná přísnější pravidla než běžný zákon; text nesmí zaměnit hranice referenda za běžné hlasování. **Doporučený text:** ponechat jen potvrzený odvolací postup a nevyplňovat nezadané lhůty odhadem. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-057 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/prava-a-soudy`. **Zdroj:** [`content/larpidia/politika/prava-a-soudy.md:3`](../content/larpidia/politika/prava-a-soudy.md).  
**Výňatek:** úplný seznam nezměnitelných ustanovení a detaily jmenování soudců nejsou doloženy.  
**Kánon:** existuje ústavní soud a ochrana základních demokratických principů; konkrétní úplný výčet a proces jmenování vyžadují opatrnost. **Doporučený text:** uvádět pouze potvrzené soudní záruky, dokud není schválen seznam a jmenovací postup. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-058 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/volby-uradu`. **Zdroj:** [`content/larpidia/politika/volby-uradu.md:7`](../content/larpidia/politika/volby-uradu.md).  
**Výňatek:** kvalifikace kandidátů, přesné nominační termíny a nestrannostní detaily nejsou úplně určené.  
**Kánon:** občané od 15 let volí vedoucí veřejných úřadů podle potvrzených pravidel; podrobnosti kandidatury je třeba porovnat s rozhodnutími o volbách. **Doporučený text:** oddělit již potvrzené volební kolo/mandát od nepopsaných kvalifikačních požadavků. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-059 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/volebni-urad`. **Zdroj:** [`content/larpidia/politika/volebni-urad.md:5`](../content/larpidia/politika/volebni-urad.md).  
**Výňatek:** přesná organizace, rozpočet a technické bezpečnostní postupy nejsou hotově popsané.  
**Kánon:** nezávislý volební úřad existuje a jeho volby kontroluje; implementační podrobnosti nejsou hotovým popisem. **Doporučený text:** veřejně uvést jeho ústavní roli, ne pracovní schéma a technická řešení. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-060 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/financni-kontrola`. **Zdroj:** [`content/larpidia/politika/financni-kontrola.md:5`](../content/larpidia/politika/financni-kontrola.md).  
**Výňatek:** složení odborné komise a zákonné důvody předčasného odvolání jsou „k dopracování“.  
**Kánon:** odborná nominace, občanské potvrzení a sedmileté období vedení jsou potvrzeny; konkrétní komise a zákonné důvody ne. **Doporučený text:** ponechat známý postup a vynechat poznámku o nedokončené komisi. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-061 — NEPOTVRZENÉ FAKTUM · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/politika/statni-rozpocet`, velké závazky. **Zdroj:** [`content/larpidia/politika/statni-rozpocet.md:5`](../content/larpidia/politika/statni-rozpocet.md).  
**Výňatek:** přesná hranice, od níž je závazek mimořádný, není stanovena.  
**Kánon:** běžný rozpočet vyžaduje tři hlasy spoluvládců; mimořádný dluh jednomyslnost, hranice však není doložena. **Doporučený text:** uvádět rozlišení a požadavek jednomyslnosti bez procentního prahu. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-062 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** stejný článek, provizorní rozpočet. **Zdroj:** [`content/larpidia/politika/statni-rozpocet.md:15`](../content/larpidia/politika/statni-rozpocet.md).  
**Výňatek:** nouzové výjimky „má stanovit zákon“.  
**Kánon:** průběžné financování nezbytných služeb a limit výdajů jsou popsány; přesná nouzová výjimka ne. **Doporučený text:** jasně označit jen potvrzený limit a nevypisovat neexistující výjimku. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-063 — NEPOTVRZENÉ FAKTUM · střední · opakováno ve 3 textech.**  
**Routa/sekce:** `#encyklopedie/ekonomika/obchod-a-export`, `#encyklopedie/zahranici-a-bezpecnost/zahranicni-vztahy`, `#encyklopedie/zahranici-a-bezpecnost/krizove-rizeni`. **Zdroj:** [`content/larpidia/ekonomika/obchod-a-export.md:3`](../content/larpidia/ekonomika/obchod-a-export.md), [`content/larpidia/zahranici-a-bezpecnost/zahranicni-vztahy.md:3`](../content/larpidia/zahranici-a-bezpecnost/zahranicni-vztahy.md), [`content/larpidia/zahranici-a-bezpecnost/krizove-rizeni.md:7`](../content/larpidia/zahranici-a-bezpecnost/krizove-rizeni.md).  
**Výňatek:** „přesný právní text, signatáři, mechanismus aktivace a datum … nejsou stanoveny“; „přesná smluvní pravidla jsou otevřená“.  
**Kánon:** fiktivní bezpečnostní spolupráce s Japonskem a Jižní Koreou je potvrzena, nesmí se vydávat za skutečnou smlouvu těchto vlád. **Doporučený text:** jednou veřejně vysvětlit fikční spolupráci obecně, ostatní články odkázat na stejný popis; konkrétní právní povinnosti neuvádět. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA. (Jde o tři výskyty jednoho tématu.)

**CS-064 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/zahranici-a-bezpecnost/krizove-rizeni`, návštěvníci. **Zdroj:** [`content/larpidia/zahranici-a-bezpecnost/krizove-rizeni.md:3`](../content/larpidia/zahranici-a-bezpecnost/krizove-rizeni.md).  
**Výňatek:** registrační systém návštěvníků a kapacita turistických míst nejsou stanoveny.  
**Kánon:** krizové plánování má zahrnout ostrovy, přístavy, hory a mořské území; přesný evidenční systém nikoli. **Doporučený text:** popsat obecnou organizaci evakuace bez tvrzení, že systém registrace již funguje. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-065 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/zahranici-a-bezpecnost/narodni-garda` a krizové řízení. **Zdroj:** [`content/larpidia/zahranici-a-bezpecnost/narodni-garda.md:3`](../content/larpidia/zahranici-a-bezpecnost/narodni-garda.md), [`krizove-rizeni.md:5`](../content/larpidia/zahranici-a-bezpecnost/krizove-rizeni.md).  
**Výňatek:** velikost, složení, výzbroj, základny, rozpočet a podrobné pravomoci nejsou rozhodnuté.  
**Kánon:** národní garda a její obranná role jsou potvrzeny v §41; v2.6 ji výslovně odlišuje od policie a dalších služeb. **Doporučený text:** popsat pouze potvrzenou roli a vztah k policii, nezveřejňovat pracovní inventář chybějících parametrů. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-066 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/paraland/pamatky`. **Zdroj:** [`content/larpidia/paraland/pamatky.md:5`](../content/larpidia/paraland/pamatky.md).  
**Výňatek:** přesný seznam památek k obnově a konkrétní budoucí hotely nejsou stanovené.  
**Kánon:** existují památky, druhá menší expozice a kombinace státního/soukromého vlastnictví; přesný seznam budoucí obnovy či hotelů potvrzen není (§41). **Doporučený text:** popsat obecný charakter památek a vlastnický model; neuvádět nepodložené objekty nebo plánované hotely. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-067 — NEPOTVRZENÉ FAKTUM · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/mesta-a-doprava/dalsi-doprava`, městské půjčovny. **Zdroj:** [`content/larpidia/mesta-a-doprava/dalsi-doprava.md:3`](../content/larpidia/mesta-a-doprava/dalsi-doprava.md).  
**Výňatek:** přesné podmínky půjčení, časové limity, zálohy a financování servisu nebyly stanoveny.  
**Kánon:** bezplatné městské půjčovny a typy sdílených prostředků jsou potvrzené; provozní pravidla ne. **Doporučený text:** ponechat druhy prostředků a princip bezplatné půjčovny, vynechat vymyšlené limity a depozita. **Postup:** VYŽADUJE ROZHODNUTÍ AUTORA.

**CS-068 — EDITORSKÁ POZNÁMKA · střední · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/mesta-a-doprava/ctvrti-larpingtonu`, pátá zóna. **Zdroj:** [`content/larpidia/mesta-a-doprava/ctvrti-larpingtonu.md:7`](../content/larpidia/mesta-a-doprava/ctvrti-larpingtonu.md).  
**Výňatek:** „Přesný obvod zóny čeká na zanesení do mapových dat.“  
**Kánon:** propojení kampusu a městské zóny je potvrzené, přesná hranice nikoli. **Doporučený text:** popsat vztah Larpingtonu a kampusu slovně; hranici v atlasu neoznačovat jako definitivní. **Postup:** POTŘEBUJE DALŠÍ DATA.

**CS-069 — EDITORSKÁ POZNÁMKA · drobná · bez duplicity.**  
**Routa/sekce:** `#encyklopedie/spolecnost/socialni-podpora-a-duchody`, sociální pomoc. **Zdroj:** [`content/larpidia/spolecnost/socialni-podpora-a-duchody.md:1`](../content/larpidia/spolecnost/socialni-podpora-a-duchody.md).  
**Výňatek:** „Kánon nepotvrzuje univerzální základní příjem“.  
**Kánon:** veřejná pomoc je cílená na lidi v obtížné situaci; nepodmíněný příjem pro každého potvrzen není. **Doporučený text:** napsat přímo, že veřejná sociální pomoc je určena lidem v obtížné životní situaci; interní formulaci o tom, co kánon nepotvrzuje, vynechat. **Postup:** JASNÉ — LZE OPRAVIT.

**CS-070 — ROZPOR S KÁNONEM · střední · bez duplicity.**  
**Routa/sekce:** přímá URL ke starší World Bible, pokud je projektový kořen součástí veřejného webu. **Zdroj:** [`data/larpidia_world_bible.json:29`](../data/larpidia_world_bible.json), pole `identity.motto`.  
**Výňatek:** stará navržená věta „Žij naplno, s respektem.“ je ve zdroji z 23. 10. 2026 označena jako `proposed`.  
**Kánon:** novější potvrzené heslo v2.6 je „Life is meant to be lived.“; starší bibli nepoužívat jako autoritu pro současný veřejný web. **Doporučené řešení:** znepřístupnit archivní zdroj veřejnosti; na webu ponechat centrální potvrzené heslo. **Postup:** JASNÉ — LZE OPRAVIT.

## 3. Sloučená redakční rozhodnutí pro autora

Následující pracovní návrhy jsou pouze možnosti k společnému projití. Nejsou potvrzené a **nemají se samy propsat do veřejných dat**. Názvy `R-*` jsou identifikátory tohoto redakční auditu, nikoli nová číslovaná otázka ústavy. V2.6 uvádí, že série 102 rozhodnutí je uzavřená; proto zde není navrhováno přidat otázku 103.

### Geografie, města a návštěvnost

**R-01 — Geografická přesnost atlasu a nejvyšší vrchol**  
**Víme:** fikční poloha v severozápadním Pacifiku, Paraland jihovýchodně, vrcholový masiv a jeho turistická role. **Chybí:** zda 560 m někdy schválit a jak zacházet s pseudokoordináty. **Pracovní návrh:** atlas oddělit na obecnou fikční polohu ostrovů a lokální schematickou mapu bez GPS; výšky zveřejnit pouze po výslovném potvrzení. **Alternativy:** (a) ponechat zcela fiktivní souřadnicový systém; (b) zvolit přibližnou reálnou oblast; (c) nezveřejňovat přesné souřadnice. **CS:** 006–010, 026. **Priorita:** vysoká, ovlivní všechny mapy a galerie.

**R-02 — Vodní toky, nádrž a pobřežní ekosystém**  
**Víme:** vodopád, řeky, nádrž a mořská rezervace patří do světa; přesné řeky a korály se nemají vymýšlet. **Chybí:** názvy, průtoky, kapacita, hranice rezervace a typ ekosystému. **Pracovní návrh:** zveřejnit pouze obecný popis toků a rezervace, bez hydrologických čísel a názvů. **Alternativy:** (a) řeky ponechat bezejmenné; (b) po autorově volbě přidat několik názvů a říční povodí; (c) určit zóny rezervace až po kontrole mapy. **CS:** 027–031. **Priorita:** vysoká, dopad na atlas, 3D terén, mapové štítky a snímky.

**R-03 — Kampusové město a hranice městských zón**  
**Víme:** kampus je samostatné sídlo poblíž Larpingtonu; existuje pátá městská zóna s vazbou na kampus; školy mají popsaná zaměření. **Chybí:** název sídla, hranice, přesná poloha, počet institucí a přesný obvod páté zóny. **Pracovní návrh:** do potvrzení používat „kampusové město poblíž Larpingtonu“ a v mapě nezobrazovat přesné hranice jako definitivní. **Alternativy:** (a) pojmenovat podle geografické oblasti; (b) vybrat samostatný český/anglický název; (c) ponechat popisný název bez vlastního jména. **CS:** 047, 068. **Priorita:** vysoká, dopad na městský plán, dopravu, školství a fotky.

**R-04 — Provozní stav L1 a L2**  
**Víme:** L1–L3 jsou zobrazeny na mapě; L3 má funkční městský úsek, podmořské pokračování se dokončuje a mezi ostrovy jezdí lodě/trajekty. **Chybí:** potvrzení stavu jednotlivých úseků L1/L2 a podzemní části. **Pracovní návrh:** ve veřejném atlasu oddělit trasu od provozu a u každého úseku zobrazovat jen potvrzený stav. **Alternativy:** (a) otevřeno; (b) rozestavěno; (c) plánováno/nezprovozněno — volit pouze po autorově potvrzení. **CS:** 002, 029. **Priorita:** vysoká; dopad na atlas, dopravní článek a galerii.

**R-05 — Larpington: potvrzené a ilustrační budovy**  
**Víme:** Larpington je hlavní město, má radnici, historický přístav, čtvrti, parky a kompaktní městské měřítko; parlament nemá. **Chybí:** u kterých z 662 objektů jde o schválený konkrétní objekt a u kterých jen ilustraci; zdroj údaje o populaci modelu 12 000; potvrzené hranice částí města. **Pracovní návrh:** ponechat radnici jako radnici, odstranit parlamentní označení a přesnou populaci 3D města nezveřejnit, dokud nebude doložena. **Alternativy:** (a) veřejný plán ukazuje pouze potvrzené objekty; (b) ukazuje i návrhové prvky s jemným „orientační“ označením; (c) oddělit plánovací vrstvu do samostatného režimu. **CS:** 012–018. **Priorita:** kritická kvůli parlamentu; dopad na mapu, 3D, fotky a galerii.

**R-06 — Turistické poplatky, kvóty a chráněné zóny**  
**Víme:** Paraland má luxusnější cestovní ruch, chráněné plochy a rozsáhlou mořskou rezervaci; některá vytížená místa mohou vyžadovat rezervaci/kvótu/poplatek. **Chybí:** konkrétní místa, ceny, limity a zóny. **Pracovní návrh:** ponechat pouze obecný popis regulovaného vstupu a ochrany, bez částek. **Alternativy:** (a) poplatek jen na několik turistických cílů; (b) bez poplatku, s rezervační kapacitou; (c) rozdělit pravidla podle konkrétních rezervací. **CS:** 031, 066. **Priorita:** střední; dopad na Paraland, návštěvnické info, mapu a rezervace.

**R-21 — Městské a horské půjčovny**  
**Víme:** ve městech fungují bezplatné půjčovny kol, koloběžek a skateboardů; horské půjčovny vyžadují vratnou zálohu. **Chybí:** doba půjčení, systém výdeje/vrácení, výše a podmínky vrácení zálohy a údržba. **Pracovní návrh:** veřejně popsat jen bezplatný městský princip a vratnou horskou zálohu. **Alternativy:** (a) samoobslužná stanoviště; (b) výdej přes dopravní uzly; (c) kombinace se servisem u provozovatelů. **CS:** 030, 067. **Priorita:** nízká až střední; dopad na městskou mobilitu, turistické informace a mapové body.

### Historie, kultura a sociální služby

**R-07 — Muzea a historické objekty**  
**Víme:** hlavní muzeum v Larpingtonu a menší expozice na Paralandu; konkrétní objekty mohou být památkově cenné či v různém stavu. **Chybí:** zda obě expozice již fungují a které konkrétní stavby se opravují či přestavují. **Pracovní návrh:** veřejně popsat existenci institučního konceptu a její vztah ke sbírkám; jednotlivé stavby a hotely uvádět až po potvrzení. **Alternativy:** (a) muzeum již otevřené; (b) instituce schválená, prostory ve výstavbě; (c) muzeum jako plánovaná instituce. **CS:** 036, 066. **Priorita:** střední; dopad na historii, Paraland, mapu a galerie.

**R-08 — Nevyjasněné detaily Košťálovy éry**  
**Víme:** ekonomické koncese, odhalující video, následný policejní zásah a poté zjištění královského původu; Košťál je v aktuálním ději ve vězení. **Chybí:** přesný právní titul, rozsudek, případné další údaje o poškozených. **Pracovní návrh:** držet veřejnou chronologii a zveřejňovat jen potvrzený právní stav; hypotetický návrat či úplatky neuvádět jako dějové události. **Alternativy:** (a) článek zůstane u současné fáze bez rozsudku; (b) doplní se potvrzený soudní výsledek; (c) doplní se anonymizovaný souhrn škod po schválení. **CS:** 033–035. **Priorita:** vysoká kvůli historii a právní přesnosti.

**R-09 — Kultura: národní jídlo a výroční festival**  
**Víme:** kuchyně spojuje mořské a regionální vlivy; Den larpu a Mog Day jsou dobrovolné komunitní akce; připomínkových dnů je více než státních volných dnů. **Chybí:** oficiální pokrm a název/datum hlavního festivalu. **Pracovní návrh:** nepojmenovávat pokrm za stát, dokud jej autor neurčí; festival zatím nechat jako obecný kulturní program. **Alternativy:** (a) zvolit jedno reprezentativní jídlo; (b) představit více regionálních jídel bez oficiálního statusu; (c) festival propojit s jedním již potvrzeným výročími, nebo jej ponechat samostatně. **CS:** 049–050. **Priorita:** nízká; dopad na kulturní článek a případné fotky.

**R-10 — Oprávnění k základnímu důchodu**  
**Víme:** modelových 12 000 Kč měsíčně od 65 let; model věkové struktury 16 % populace 65+; individuální nárok nelze automaticky odvozovat z věku celé skupiny. **Chybí:** zda se nárok váže na občanství, pobyt, nebo jinou podmínku. **Pracovní návrh:** do rozhodnutí uvádět částku jako modelovou a nevypisovat podmínku, kterou kánon nepotvrdil. **Alternativy:** (a) občanství; (b) dlouhodobý pobyt; (c) kombinované pravidlo. **CS:** 043, 045–046. **Priorita:** vysoká; dopad na sociální systém a rozpočtový model.

**R-11 — Zdravotnictví a školství v rozpočtovém rámci**  
**Víme:** 1,6 mld. Kč je společný modelový rámec obou oblastí a není prokázáno, že pokryje jejich rozsah. **Chybí:** úplné výdajové položky, potřeby služeb a financování případného schodku. **Pracovní návrh:** zachovat správné společné označení a nezveřejňovat závěr „služby plně financovány“, dokud není celý model sladěn. **Alternativy:** (a) doplnit rozpočtové zdroje; (b) změnit rozsah služeb; (c) ponechat rámec jako model bez tvrzení o soběstačnosti. **CS:** 042, 044. **Priorita:** vysoká; dopad na ekonomické souhrny, zdravotnictví a školství.

### Ústava, ekonomika, doprava a bezpečnost

**R-12 — Lhůty občanských návrhů a opravné prostředky**  
**Víme:** občan může předložit návrh bez sběru podpisů; nezávislá legislativní kancelář provede formální a právní kontrolu; rozhodují občané. **Chybí:** lhůty, doplnění návrhu, odůvodnění a opravný postup. **Pracovní návrh:** veřejně popsat pouze potvrzené kroky; procesní časy ponechat v prováděcím předpisu. **Alternativy:** (a) jednotná lhůta; (b) lhůty podle náročnosti; (c) bez pevné lhůty, se zveřejněným odůvodněním prodlení. **CS:** 052–053. **Priorita:** vysoká; dopad na ústavní vysvětlení.

**R-13 — Tajnost a audit digitálního hlasování**  
**Víme:** oprávněný volič má jeden započtený hlas, má existovat osobní i elektronická cesta a průběžné veřejné agregace; hotová aplikace není doložena. **Chybí:** technické řešení, které oddělí identitu hlasujícího od obsahu hlasu a zároveň umožní audit. **Pracovní návrh:** neprezentovat veřejnosti technologii, dokud není její model navržen; ústavní princip popsat bez tvrzení o aplikaci. **Alternativy:** (a) fyzický lístek + digitální agregace; (b) nezávisle auditovaný elektronický systém; (c) obě metody souběžně. **CS:** 054, 058–059. **Priorita:** vysoká; dopad na demokracii, volební úřad a UX budoucích systémů.

**R-14 — Veto, smír a odvolání spoluvládce**  
**Víme:** veto je odkladné, po něm smír a možný návrat věci k občanům; odvolání má odlišný, přísnější postup; politický nesouhlas sám o sobě není soudním důvodem. **Chybí:** délky lhůt, opakované petice a postup po neúspěšném odvolacím hlasování. **Pracovní návrh:** neuvádět konkrétní lhůty; zachovat oddělené schéma zákonného veta a odvolání. **Alternativy:** (a) jedna pevná lhůta; (b) čas podle druhu řízení; (c) lhůta stanovená nezávislým úřadem. **CS:** 055–057. **Priorita:** vysoká; dopad na ústavní články a volební grafiku.

**R-15 — Ústavní soud a neměnné principy**  
**Víme:** soud chrání ústavní pořádek a demokratické záruky. **Chybí:** přesný seznam chráněných ustanovení, způsob jmenování soudců a některé opravné prostředky. **Pracovní návrh:** veřejně vyjmenovat pouze již potvrzené principy; seznam a personální postup doplnit po ústavním rozhodnutí. **Alternativy:** (a) uzavřený výčet; (b) obecná klauzule doplněná soudním testem; (c) kombinace výčtu a obecné ochrany práv. **CS:** 057. **Priorita:** vysoká.

**R-16 — Nezávislost volebního a finančního dohledu**  
**Víme:** volební úřad a finanční kontrola mají být nezávislé; kandidatury vedoucích veřejných úřadů mají občanské potvrzení; NKÚL vede odborně nominovaný kontrolor se sedmiletým mandátem. **Chybí:** složení výběrových komisí, rozpočtová nezávislost, důvody odvolání a technické kontrolní postupy. **Pracovní návrh:** veřejně vysvětlit mandát a nezávislost, provozní detaily uvést až po potvrzení. **Alternativy:** (a) odborná komise s veřejným výběrem; (b) víceinstituční nominace; (c) jednotný, ale nezávisle kontrolovaný postup. **CS:** 058–060. **Priorita:** střední až vysoká; dopad na politické články.

**R-17 — Mimořádné závazky a provizorní rozpočet**  
**Víme:** běžný rozpočet schvalují nejméně tři spoluvládci; mimořádný dluh jednomyslně; při prodlení pokračují služby v omezeném režimu. **Chybí:** hranice mimořádného dluhu a přesně vymezené nouzové výjimky. **Pracovní návrh:** zveřejnit počet hlasů a provizorní limit, bez prahu nebo výjimky. **Alternativy:** (a) nominální peněžní hranice; (b) podíl rozpočtu; (c) seznam typů dlouhodobých závazků. **CS:** 061–062. **Priorita:** střední; dopad na rozpočet a ústavní přehled.

**R-18 — Obranná spolupráce s Japonskem a Jižní Koreou**  
**Víme:** jde o fiktivní bezpečnostní spolupráci; nesmí se tvrdit, že skutečné vlády uzavřely smlouvu s Larpidií. **Chybí:** přesný dokument, signatáři ve fikčním světě, datum a mechanismus pomoci. **Pracovní návrh:** ponechat obecný popis fikční spolupráce s viditelnou fikční atribucí; nepřepisovat jako reálnou smlouvu. **Alternativy:** (a) rámcová konzultační dohoda; (b) obranná pomoc jen po samostatném rozhodnutí; (c) neformální spolupráce bez automatického závazku. **CS:** 063. **Priorita:** vysoká kvůli přesnosti vůči skutečným státům.

**R-19 — Krizová evidence návštěvníků a role národní gardy**  
**Víme:** krizový plán zahrnuje ostrovy, přístavy a turistické oblasti; garda je menší obranná složka vedle policie, pobřežní stráže a záchranných služeb. **Chybí:** kapacita turistických míst, evidence lidí, velikost gardy, výzbroj, základny, rozpočet a detailní pravomoci. **Pracovní návrh:** popsat civilní a obranné složky jejich potvrzenými rolemi; nedoplňovat čísla ani operační systém odhadem. **Alternativy:** návštěvnická evidence může být lokální evidence u provozovatelů, dobrovolná registrace, nebo bez předběžné evidence s krizovým sčítáním. **CS:** 064–065. **Priorita:** střední; dopad na bezpečnostní články a Paraland.

**R-20 — Ostatní nepojmenované modelové údaje**  
**Víme:** daň ze zisku 5 %, DPH 12/5 %, 24hodinový pracovní týden, důchodový model 12 000 Kč od 65 let, návštěvnost 40 000 ročně a útrata 15 000 Kč na návštěvu jsou v aktuálním centrálním modelu. Částky musejí být odlišeny od rozpočtových příjmů a naměřených statistik. **Chybí:** některé produktové kategorie snížené DPH, konkrétní firmy, pracovní smluvní detaily a podmínky dávky. **Pracovní návrh:** centrální hodnoty ponechat a otázky oddělit od schválených sazeb; veřejně neuvádět dopočítané součty jako jisté příjmy státu. **Alternativy:** sazby bez seznamu výjimek; seznam kategorií až po explicitním potvrzení; nebo odložit popis výjimek. **CS:** 037–041, 045–046. **Priorita:** střední; dopad na fakta, ekonomické souhrny a prezentace.

## 4. Jasné opravy a skutečné otázky

### Lze opravit redakčně bez nového rozhodnutí

- Odstranit z veřejných stránek pracovní verze, drafty, `Bible / zadání`, produkční názvy polí a věty o centrálních souborech.
- Nahradit „Kánon uvádí…“ běžným veřejným vysvětlením; opravit překlep „výrobních kapacity“.
- Změnit příklady vyhledávání tak, aby nevyzdvihovaly proposed název.
- Neuvádět parlament v názvu radnice, příkladech hledání ani textových štítcích. V2.6 je v tomto bodě jednoznačný.
- Neuvádět přesný den nezávislosti, pokud je potvrzen jen rok 1921; neuvádět spekulace o Košťálově budoucnosti jako událost.
- Zachovat transparentní, ale návštěvnicky formulované upozornění, že mapy jsou ilustrativní a některé trasy neznamenají provoz.
- Odstranit z veřejných galerií výrobní prompty a instrukce pro ukládání souborů.

### Vyžaduje rozhodnutí autora nebo další podklady

- Přesné názvy a parametry řek, nádrže, vrcholových výšek, rezervací, lokalit, kampusu a čtvrtí.
- Provozní stav L1/L2 a částí podzemní infrastruktury; potvrzení konkrétních objektů ve městě.
- Přesný rozsudek a právní stav Košťála, status muzea, symbolické názvy festivalu a pokrmu.
- Prováděcí podrobnosti ústavy, hlasování, soudnictví, volebních a kontrolních orgánů, rozpočtu a sociálních nároků.
- Provozní systém cestovního ruchu, bezpečnosti, národní gardy, půjčoven, škol a zahraniční spolupráce.
- Nasazovací pravidla, která určí, zda jsou interní soubory dostupné skutečnému veřejnému webu.

## 5. Doporučené pořadí nápravy

### Rychlé opravy

1. Odstranit parlamentní text z atlasu, vyhledávacích příkladů a označení CP-B01; zachovat označení radnice podle potvrzené funkce.
2. Přestat veřejně servírovat pracovní zdroje, starší World Bible, interní foto-prompty, `photo_guide`, „Bible / zadání“ a interní poznámky.
3. Nahradit štítky `v1.0-draft`, `PRACOVNÍ MODEL`, `prompt-ready` a „čeká na rozhodnutí“ popisem orientační mapy/ilustrace; ponechat přesné vysvětlení nejistoty tam, kde chrání návštěvníka před chybným závěrem.
4. U Košťála, daňových modelů a přehledu odstranit redakční fráze, nikoli potvrzené dějové informace.
5. Zachovat správné rozlišení: městská L3 funguje; podmořská L3 se dokončuje; mezi ostrovy jezdí trajekty/lodě. To není redakční nedostatek.

### Nutné společné rozhodnutí

1. Projít `R-01` až `R-20` a schválit pouze ta doplnění, která jsou pro veřejný příběh žádoucí.
2. Před opravou atlasu sladit názvy, polohy, stav provozu a městské objekty s aktuálním v2.6; starší soubory nepoužívat jako rozhodující zdroj.
3. Rozhodnout, zda mají veřejné mapy ukazovat jen potvrzené objekty, nebo i orientační plánovací prvky v oddělené vrstvě.

### Budoucí rozšíření

1. Po potvrzení obsahu vytvořit návštěvnický registr médií a oddělit ho od promptů/produkčních metadat.
2. Sladit samostatný JSON registry s jejich vloženými kopiemi a přidat kontrolu driftu při aktualizaci.
3. Stanovit veřejný export/build, který nezahrne archivní reference, pracovní rozhodovací záznamy a historické verze atlasu.

## 6. Zdroje a omezení

- Autoritativní podklad: `references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md` (102 rozhodnutí; starší archivní návrhy podléhají novějším potvrzením a kapitole 41). Původní soubor nebyl změněn.
- Porovnané starší zdroje: `data/larpidia_world_bible.json`, `references/GEOGRAPHY_AND_CANON.md`, `references/REALISM_AND_ZSV.md`.
- Aktivní datové zdroje: `content/larpidia/index.json`, `content/larpidia/facts.json`, 39 Markdown článků, `atlas/current/registry/places.json`, `atlas/current/capital/cp_objects.json` a příslušné vložené registry.
- Archivy `atlas/versions/` existují jako historické soubory. Tento audit se soustředí na aktivní routy a největší veřejné konflikty; jednotlivé staré verze atlasu nebyly všechny ručně vykresleny ani obsahově inventarizovány. Jejich přímé vystavení závisí na nasazení.
- V tomto auditu nebyl upraven obsah nevyřešených faktů, centrální data ani atlasové registry.
