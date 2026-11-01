# LARPIDIE — SCHVÁLENÉ OPRAVY WEBU A ATLASU PO AUDITU

**Zadání pro Codex, připravené k přímé implementaci.** 1. listopadu 2026. Tento soubor je **pokyn k opravě existujícího projektu**, nikoli další návrh nových ústavních otázek. Ústavní a světový kánon má **102/102 rozhodnutí** a **nesmí se měnit ani přepisovat**.

## 0. Co máš udělat

1. V kořeni projektu najdi aktivní web, encyklopedii, hlavní atlas, městský plán, 3D modely, galerii a nasazovací skripty. Nejprve si ověř skutečné cesty a stav pracovního stromu, nemazej uživatelské změny.
2. Přečti `references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md`, `docs/LARPIDIA_PUBLIC_CONTENT_AUDIT.md` a `docs/LARPIDIA_ATLAS_SEARCH_REVIEW.md`. Pokud jsou reporty jinde, najdi je; pokud chybí, tento dokument obsahuje úplné mapování CS-001 až CS-070, ale nevyvozuj z něj neznámý zdrojový kód. Archivní `v2.6` nikdy nepřepisuj. Pokud neexistuje, upozorni, **nevyráběj jej z paměti**.
3. Implementuj redakční opravy, odstranění zastaralých parlamentních pozůstatků, bezpečné oddělení veřejných a interních dat, **bohatší atlasové vyhledávání B** a nenápadné verzování v patičkách.
4. Neměň celkovou estetiku webu, typografii ani příjemnou barevnou paletu. Neměň skutečnou geometrii ostrovů, umístění stávajících bodů, 3D domů, reliéf ani existující schválená jména bez důvodu uvedeného v auditu. Nezasahuj do budoucí školní hry GeoGuessr; ta je samostatná funkce.
5. Pokud skutečné soubory nebo chování již byly opraveny, zachovej správný stav a neopakuj změny. Implementuj idempotentně, nikoli slepým hledáním a nahrazováním.

### Autorita zdrojů

Nejnovější potvrzené autorské rozhodnutí **v tomto dokumentu** má přednost v rozsahu nových upřesnění A1–A8. Zbytek světa určuje **aktuálně platný kánon v2.6**, nikoliv starší archivní odpovědi A/B/C, World Bible, atlasové `proposed` statusy či popisky promptů. Při konfliktu se starým zdrojem zachovej původní archiv a oprav **aktivní veřejné zobrazení nebo jeho odvozená data**. Nelze automaticky přenést interní návrhy do veřejného kánonu.

## 1. Autorova definitivní upřesnění A1–A8 (mimo ústavní číslování)

| ID | Schváleno | Závazné provedení |
|---|---|---|
| **A1B** | Veřejný atlas ukazuje **všechna místa**. | Orientační mapový registr zůstane úplný, nevyhazuj 108 návrhových prvků. Nezobrazuj individuální redakční štítky `proposed`, `needs-decision`, `Bible` ani workflow. Jedna věcná informace v legendě uvede, že poloha a některé názvy jsou na schematické mapě orientační. **Neříkej**, že každé místo je přesně geodeticky potvrzené. |
| **A2A** | Plán Larpingtonu má ukázat všech **662 objektů**. | Běžná městská zástavba může být ilustrativní; konkrétní jméno, instituce či historický příběh pouze tam, kde ho podporuje kánon nebo aktivní schválený obsah. Nevyhazuj domy jen kvůli původnímu statusu `proposed`. |
| **A3A** | Linky **L1 i L2 fungují**. | L1 = horská zážitková železnice, L2 = elektrická dráha v historickém stylu; citlivé podzemní úseky neprezentovat jako neomezeně otevřené bez podkladu. **Městská L3 je v provozu, podmořská L3 na Paraland se dokončuje a spojení nyní obstarávají lodě.** |
| **A4B** | Nejvyšší vrchol **přibližně 560 m n. m.** | Jde o výšku používanou ve fikčním atlasu; údaj `přibližně` neznamená, že vrchol sám není součástí světa, nýbrž že není doložena přesná shoda kóty s ilustrativním 3D/GIS modelem. Autor by klidně přijal přesných 560 m, až to bude harmonizováno s terénními daty; **zatím se drž volby B**. |
| **A5A** | Školy mají běžně **pět vyučovacích dnů**. | Pondělí–pátek; vyučování smí začít před 9:00 **nanejvýš dvakrát týdně**. Nepřepisovat na dospělý 24hodinový pracovní týden. |
| **A6B** | Hlavní muzeum v **Larpingtonu je otevřené**. | Menší expozice na **Paralandu se ještě dokončuje**. Jde o skutečnou fiktivní výstavbu, kterou **nesmíš skrýt** jako redakční poznámku; nedoplňuj adresy nebo termín otevření. |
| **A7A** | Všichni larpidští občané **od 65 let** mají nárok na základní státní důchod. | Bez požadavku na odpracované roky; modelová měsíční částka **12 000 Kč**. Nekládej další rezidenční nebo pracovní podmínky; státní občanství je podmínka. |
| **A8B** | Bohatší **vyhledávání v atlasu**. | Typy míst, ostrov, přehledné karty výsledků, klávesnice, diakritika, vycentrování SVG a **mobilní vysouvací panel**. Zachovej styl a podkladovou SVG mapu. |

### Verze v zápatí — dodatečné explicitní přání autora

- **Nezobrazuj** `v1.0-draft`, `PRACOVNÍ MODEL`, `NÁVRH · verze…`, interní projektové identifikátory a jiné stavové/verzovací štítky **v hlavních nadpisech, kartách, bannerech, tlačítkách ani v mapovém těle**.
- **Verze samotná není zakázaná.** Je vítaná v **diskrétní společné patičce** (např. „Web · v…  |  Atlas · v…  |  Plán Larpingtonu · v…  |  3D model · v…“). Používej **skutečné verze z projektového metadatového zdroje**, ne smyšlené hodnoty. Pokud komponenta nemá vlastní stabilní verzi, vynech její číslo nebo je použita celková verze projektu; nepřidávej umělou `v1.0`.
- Ve všech částech to sjednoť, aniž by patička překážela při práci s mapou na mobilu. Zdroj verzí udržuj na jednom místě. Archivní názvy souborů a changelogy zůstávají v interním projektu.

## 2. Princip „žádná viditelná construction site“

Veřejné stránky mají návštěvníkovi ukazovat **zemi**, ne redakční poradu. Nesmí být viditelné `kánon nepotvrzuje`, `tento údaj zatím nebyl schválen`, `pracovní`, `prompt-ready`, `needs-decision`, `photo_guide`, `Bible`, `v1.0-draft`, `status` nebo zprávy o tom, co nezvládl Codex. **To ale neznamená tvrdit nepravdu.**

- Skutečná fikční stavba ve výstavbě (podmořská L3, menší muzeum na Paralandu) = zveřejnit její skutečný stav.
- Když není určen přesný počet, datum, cena, právní titul nebo souřadnice = použít přirozený obecný popis a neznámou informaci neuvádět. **Nevymýšlet ji a neoznačovat ji za potvrzenou.**
- Atlas = **orientační fikční mapa**. Veřejné datum i přesnost musí být prezentovány adekvátně. Statusy z původních registrů zůstanou v interním editoru; návštěvník neuvidí seznam schvalovacích stavů.
- Ekonomická čísla = rozlišovat **schválený model** a **skutečně doloženou finanční bilanci**. Turistické útraty 600 mil. Kč nejsou příjmem státu; 2,4 mld. Kč rozdělitelného zisku firem je pracovní ekonomický scénář, nikoli důkaz průmyslové kapacity.
- Historie = respektovat zveřejněná fakta o Košťálovi; nevyhlásit budoucí spekulaci za hotovou událost a nevydávat skutečné Japonsko a Jižní Koreu za signatáře skutečné smlouvy s Larpidií.

## 3. Přesné mapování všech 70 nálezů auditu

Jednotlivé záznamy odpovídají **přesně** `CS-001` až `CS-070` z `LARPIDIA_PUBLIC_CONTENT_AUDIT.md`. U každého je konkrétní pokyn k nápravě. ID nejsou nová otázka ani nové ústavní rozhodnutí. Různé řádky se mohou překrývat (např. parlament nebo počet seniorů): oprav **jediný sdílený zdroj** a zkontroluj všechna veřejná místa.

Legenda: `TEXT`=redakce článku; `KÁNON`=potvrzené pravidlo; `UI`=vizuální rozhraní; `DATA`=registry; `BEZPEČNOST`=deployment; `GALERIE`=média; ostatní jsou názvy příslušných sekcí.

### CS-001 až CS-025

| Audit | Typ | Konkrétní oprava |
|---|---|---|
| **CS-001** | TEXT | V zápatí mapové sekce nahradit `Atlas v1.0-draft` neutrálním názvem; verzování přesunout výhradně do nenápadné patičky s hodnotou z jedné společné konfigurace. |
| **CS-002** | KÁNON | L1 a L2 popsat jako provozované linky podle A3A; L1 horská zážitková, L2 historická elektrická. Zmínit omezení konkrétních chráněných podzemních úseků jen jsou-li doložena. L3 městský úsek funguje, podmořská část ne. |
| **CS-003** | TEXT | V galerii vynechat sdělení, že fotografie nebo videa nebyly vygenerovány. Zobrazit pouze skutečně dostupná média; chybějící scény nezveřejňovat jako hotové fotky. |
| **CS-004** | TEXT | Letecký snímek/3D popsat jako `Orientační vizualizace Larpingtonu z výšky`, bez slov `pracovní návrh`. |
| **CS-005** | UI | V záhlaví atlasu odstranit `NÁVRH · v1.0-draft`; zobrazit `Atlas Larpidie`, orientačnost vysvětlit v legendě. Verzi nanejvýš dole v patičce. |
| **CS-006** | UI | Placeholder vyhledávání změnit na `Hledat místo, oblast nebo ID…`; neuvádět nedoložené jméno Aokawa jako oficiální. |
| **CS-007** | TEXT | Z mapy odstranit vysvětlování pracovního schvalování a World Bible; použít jedno krátké věcné upozornění o orientačnosti schematické mapy, ne o aktuálnosti kánonu. |
| **CS-008** | UI | Přepracovat legendu: nezobrazovat `Pracovní návrh` a `Čeká na rozhodnutí`. U veřejné orientační mapy legendarizovat druh a funkci místa, ne interní workflow; pravdivé omezení přesnosti uvést jednou. |
| **CS-009** | DATA+UI | Pro 159 mapových míst vytvořit veřejné bezpečné detailové karty bez `photo_guide`, `notes`, Bible/ref, pseudo-statusů a výrobních pokynů. Použít potvrzené názvy, u nedoložených orientační názvy/jedno souhrnné upozornění; nezměnit původní souřadnice. |
| **CS-010** | KÁNON | Nejvyšší vrchol označit `přibližně 560 m n. m.` dle A4B. `560 m` nepovažovat za oficiálně zaměřenou přesnou výšku; pokud se ztotožní s metrickým terénním modelem, lze ji později zpřesnit na autorův pokyn. |
| **CS-011** | UI | U 3D reliéfu změnit titul `NÁVRH · modelové výšky` na `3D reliéf Larpidie` a do popisu dát `orientační zobrazení terénu`; interní verze jen v patičce. |
| **CS-012** | UI+DATA | Z 3D Larpingtonu odstranit `PRACOVNÍ MODEL · CP-01` a `budoucí návrh v rezervě`. Neověřených 12 000 obyvatel Larpingtonu neprezentovat jako fakt; zachovat geometrii a rozdíl existující/plánovaná infrastruktura. |
| **CS-013** | UI | Plán města pojmenovat `Plán Larpingtonu`, s orientační vysvětlivkou, bez `v1.0-draft` v záhlaví. Verzi jen patička. |
| **CS-014** | KÁNON | V hledání města odstranit příklad `parlament`; použít existující neutrální `radnice` nebo `tržnice` bez vytváření nové instituce. |
| **CS-015** | UI | V mapových vrstvách města odstranit interní rozdíl `schváleno × návrh`; nabídnout smysluplné návštěvnické vrstvy (ulice, domy, instituce, zelené plochy). Případný režim výstavby označovat věcně. |
| **CS-016** | DATA+UI | Pro 662 městských objektů zachovat kompletní zástavbu dle A2A. Běžné objekty zobrazovat jako budovy/ulice, jen konkrétním potvrzeným památkám či úřadům dát vlastní oficiální názvy. Nezobrazovat `Bible / zadání`, interní notes, statusy nebo domnělé adresy. |
| **CS-017** | KÁNON+DATA | Ve `CP-B01`, všech odvozených kopiích a `capital-3d-data.js` změnit `Radnice a parlament Larpingtonu`/`Town Hall and Parliament House` na `Radnice Larpingtonu`/`Larpington Town Hall`, odstranit falešnou funkci parlamentu. Zachovat ID, geometrii, jiné atributy. |
| **CS-018** | KÁNON+DATA | Ve `ST-S` a odpovídajících městských záznamech odstranit zmínku o parlamentu; uchovat jen ověřené užití objektu, jinak veřejně neutrální popis. |
| **CS-019** | BEZPEČNOST | Starší `data/larpidia_world_bible.json` nepoužívat jako živý veřejný zdroj ani přímo neservírovat; jeho historické parlamentní údaje nemají přebít 102 rozhodnutí. Archiv nemazat. |
| **CS-020** | BEZPEČNOST | Populaci 32 000 brát z aktuálního centrálního `facts.json`, ne ze starého `population_working_model.status=proposed` v archivní bibli; starou bibli nezveřejňovat. |
| **CS-021** | BEZPEČNOST | Starší `references/GEOGRAPHY_AND_CANON.md` uchovat interně, nepublikovat starou instrukci na parlamentní budovu ani přístup k souboru. |
| **CS-022** | BEZPEČNOST | Starší `references/REALISM_AND_ZSV.md` uchovat interně, nezveřejňovat už překonané parlamentní návrhy jako platný ústavní model. |
| **CS-023** | GALERIE | U 20 fotografických a čtyř video scén odstranit veřejné `prompt-ready` a `generated_image:null`; zobrazit jen existující snímek/video s čitelným popiskem nebo nezobrazit nehotovou kartu. |
| **CS-024** | GALERIE+BEZPEČNOST | Návštěvníkovi nezobrazovat `open prompt`, `PHOTO_`, výrobní metadata, modely AI ani cesty k interním promptům. Oddělit veřejný seznam médií od interního generator packu. |
| **CS-025** | BEZPEČNOST | Upravit publikování: nasazovat jen explicitní veřejný výstup/allowlist; blokovat přímé URL k `references/`, pracovním docs, staré World Bible, promptům a interním JSON poznámkám. Ověřit lokální i skutečný hosting, netvrdit automaticky produkční únik. |

### CS-026 až CS-050

| Audit | Typ | Konkrétní oprava |
|---|---|---|
| **CS-026** | TEXT | Poloha ostrovů: `fikční severozápadní Pacifik; mapa zachycuje zeměpisné vztahy schematicky`. Nevytvářet GPS souřadnice ani odstavec o interním potvrzování. |
| **CS-027** | TEXT | Přírodu popsat pomocí potvrzené nádrže, řeky a vodopádu; vynechat redakční vyjmenování neznámých průtoků, objemů a jmen. Žádné nové hodnoty neodhadovat. |
| **CS-028** | TEXT | Pod vizualizací nepsat `návrhové / nepotvrzuje`. Jeden obecný návštěvnický popisek o orientační mapě; provoz jednotlivých dopravních staveb popisovat zvlášť a pravdivě. |
| **CS-029** | KÁNON | L1 je v provozu dle A3A; podzemní nebo citlivé úseky nepovažovat automaticky za přístupné. Do článku uvést provoz celé linky a potřebné omezení bez vymyšlení konkrétního tunelu. |
| **CS-030** | TEXT | Horské půjčovny: věcně uvést `zapůjčení s vratnou zálohou`; neuvádět fiktivní ceník, splatnost ani proklamaci `není stanoveno`. |
| **CS-031** | TEXT | Chráněná mořská rezervace, rezervační systém a limity zůstávají; neuvádět přesné hranice, ceny, kapacity ani nedoložené korálové útesy. Přepsat do uživatelského popisu dostupných druhů aktivit a ochrany přírody. |
| **CS-032** | TEXT | U nezávislosti ponechat rok 1921; vynechat vysvětlivku, že den zatím nebyl určen. |
| **CS-033** | HISTORIE | Košťálovu úlohu popsat jako hospodářskou a společensky vlivnou moc bez vymyšleného úředního titulu; odstranit formulaci `kánon nepotvrzuje krále/premiéra`. |
| **CS-034** | HISTORIE | Věcně popsat hospodářský tlak, nejistotu rodin a pozdější obnovu; vypustit větu o tom, co encyklopedie neví o jednotlivých osobách. Nevymýšlet konkrétní oběti nebo zásahy. |
| **CS-035** | HISTORIE | Košťál je v současném fikčním ději ve vězení; budoucí úplatky/návrat nejsou potvrzené události. Nedoplňovat nedoložený rozsudek nebo konkrétní právní titul zadržení. |
| **CS-036** | KÁNON | Dle A6B: hlavní interaktivní muzeum v Larpingtonu JE OTEVŘENÉ; menší expozice na Paralandu SE PŘIPRAVUJE/DOKONČUJE. Realistický popis institucionálního stavu bez smyšlených adres a otevírací doby. |
| **CS-037** | EKONOMIKA | U DPH uvést sazby 12 % a 5 % na vybrané potřeby; vynechat editorské upozornění, že seznam sazeb není rozepsaný. Nevymýšlet konkrétní nové sazební výjimky. |
| **CS-038** | EKONOMIKA | `Kánon uvádí modelová pásma` nahradit veřejným `Daň z příjmů využívá progresivní pásma...`; číselné hranice/0-3-5-7 % načítat z centrálních faktů. |
| **CS-039** | EKONOMIKA | Uvést 24 hodin, Po–Čt 6 hodin denně, výjimky směnného provozu; odstranit seznam dosud nenapsaných pracovněprávních ustanovení. |
| **CS-040** | EKONOMIKA | Počet pracujících 14 000 uvést jako model, bez nedoloženého odvětvového rozpisu či pracovního statusu a bez omluvné věty `nejsou potvrzené`. |
| **CS-041** | EKONOMIKA | Popsat export státních firem vyrábějících řasová paliva a průmyslové produkty do Japonska/Jižní Koreje; nevymýšlet názvy firem/objem tržeb. Opravit překlep `výrobních kapacity`. |
| **CS-042** | EKONOMIKA | U zdravotnictví a školství zachovat společný **modelový limit 1,6 mld. Kč**; neprohlašovat služby za prokazatelně plně financované ani stávající model za skutečný audit. Interní věty o `neprokázané dostatečnosti` přesunout do poznámek; pravdivé označení `modelový` ponechat. |
| **CS-043** | EKONOMIKA | Pensionový výpočet 5 120 × 12 000 × 12 = 737,28 mil. Kč označit jako MAXIMÁLNÍ ilustrativní scénář, pouze pokud by všichni senioři splňovali nárok; neprezentovat jako skutečnou výdajovou položku. |
| **CS-044** | ZDRAVOTNICTVÍ | Popsat zahraniční smluvní specializovanou péči a nezbytný transport po posouzení potřeby; nezavádět automatické právo na libovolnou léčbu. Nevypisovat chybějící objem/konkrétní nemocnice. |
| **CS-045** | KÁNON | Dle A7A základní státní důchod pro **všechny larpidské občany od 65 let bez podmínky odpracovaných let**. Uvést 12 000 Kč/měsíc jako modelovou schválenou částku; nevyžadovat pětiletý pobyt ani občanství jiné země. |
| **CS-046** | EKONOMIKA | Sladit s CS-043 a CS-045: 16 % seniorů (5 120) není automaticky počet **larpidských občanů** od 65 let. Výdaje podle počtu občanů; výše uvedený scénář jasně podmínit. |
| **CS-047** | SPOLEČNOST | Samostatné kampusové město poblíž Larpingtonu; navazující kreativní/univerzitní zóna v hlavním městě. Reálné studijní obory ponechat, ale nevymýšlet jméno města, počet fakult a adresy. Interní poznámku smazat. |
| **CS-048** | KÁNON | Dle A5A školní týden PONDĚLÍ–PÁTEK (5 dnů); začátek vyučování před 9:00 nejvýše dvakrát týdně. Dospělý pracovní týden 24 hodin nadále platí odděleně. |
| **CS-049** | KULTURA | Popisovat místní kuchyni ryb, řas, rýže a britsko-českých vlivů; neuvádět `zatím neexistuje oficiální národní jídlo`. Nepřidávat oficiální pokrm. |
| **CS-050** | KULTURA | Popsat velkou výroční slavnost plus menší akce a dobrovolný Den larpu/Mog Day, ale nevymýšlet oficiální název a datum velkého festivalu. |

### CS-051 až CS-070

| Audit | Typ | Konkrétní oprava |
|---|---|---|
| **CS-051** | POLITIKA | U spoluvládců vyjmenovat čtyři resortní oblasti dle 22A a společné rozhodnutí o rozdělení dle 25A. Neukládat žádnému konkrétnímu spoluvládci domyšlený resort. |
| **CS-052** | POLITIKA | Ústavní systém prezentovat pozitivně a kompletně z potvrzených 102 rozhodnutí. Odstranit editorské pasáže o `nutnosti dopracování lhůt`. Bez smyšlených nových ústavních předpisů. |
| **CS-053** | POLITIKA | Navrhování zákona: každý oprávněný občan od 15 let bez podpisů, právní/technická kontrola a veřejné hlasování; bez vymyšlených procesních lhůt či odvolání. |
| **CS-054** | POLITIKA | O elektronickém hlasování uvést zvolený ústavní **princip** a odpovědnost nezávislého volebního úřadu; neprohlašovat nedoloženou aplikaci za dokončenou, otestovanou či nezranitelnou. Průběžné souhrnné výsledky dle 42C ukazované dvakrát denně jsou koncepce systému. |
| **CS-055** | POLITIKA | Veto je odkladné; smír a případné rozhodnutí občanů potvrzené. Bez nedoloženého 14denního limitu nebo jiných čísel. Nepřepisovat interní větu `lhůty nejsou stanoveny` na veřejnou stránku. |
| **CS-056** | POLITIKA | Odvolání: petice 10 % VŠECH oprávněných, referendum nad 50 % platných hlasů s účastí min. 30 % oprávněných; po neúspěchu dalších 12 měsíců, soudně posuzovaná výjimka pro nové závažné okolnosti (41B). Nevymýšlet délku kampaně. |
| **CS-057** | POLITIKA | Věcně popsat nezávislý ústavní soud a nezměnitelné demokratické jádro; nepsat neexistující uzavřený seznam ustanovení ani personální pravidla soudců. |
| **CS-058** | POLITIKA | Vedoucí úřadů: občanská volba, druhé kolo ze dvou finalistů dle 20A, u technických rolí kvalifikace dle 19C. U volebního úřadu zvláštní přímá volba z odborně způsobilých kandidátů (40B), nepředjímat zvláštní volební proceduru, pokud kánon neříká. |
| **CS-059** | POLITIKA | Volební úřad je nezávislý; odpovědnost za hlasování a ochranu tajnosti. Odstranit otázky o nerozhodnutém rozpočtu a softwaru; nevyhlašovat dokončenou e-volební službu. |
| **CS-060** | POLITIKA | NKÚL: odborná komise navrhne vedení, občané potvrdí; 7 let bez bezprostředního opakování, nezávislá kontrola všech státem ovládaných podniků. Nevymýšlet jména členů výběrové komise ani důvody odvolání. |
| **CS-061** | POLITIKA | Rozpočet: běžný souhlas 3/4, mimořádný dluh/velké závazky 4/4; výjimečnost kombinací relativních příjmů a dlouhých závazků. Nevkládat konkrétní číselné prahy, které nebyly stanoveny. |
| **CS-062** | POLITIKA | Rozpočtové provizorium nejvýše 1/12 předchozího schváleného ročního rozpočtu měsíčně s úzce vymezenými mimořádnými výjimkami; nevymýšlet jejich přesnou definici nebo správní postup. |
| **CS-063** | ZAHRANIČÍ | Fikční bezpečnostní spolupráce s Japonskem/Jižní Koreou a obchodní vazby, bez zveřejnění neexistujícího přesného textu smlouvy nebo tvrzení, že reálné státy skutečně uzavřely dohodu. Neautomatizovat vojenský zásah. |
| **CS-064** | BEZPEČNOST | Krizové plány obou ostrovů, národní garda, policie, pobřežní stráž a záchranné složky. Nepopisovat nedoloženou registraci návštěvníků nebo kapacity zařízení. |
| **CS-065** | BEZPEČNOST | Zachovat civilní a obranné instituce, ale nepřidávat neznámé počty členů, výzbroj, základny, rozpočet nebo operační detaily gardy. |
| **CS-066** | PARALAND | Historické domy a zámky zhruba z poloviny soukromé (např. TJR/Togi) a z poloviny státní; vybrané budovy pro kulturní/ubytovací využití, některé zachované zříceniny. Nevymýšlet seznam konkrétních hotelů ani práva vstupu na soukromý pozemek. |
| **CS-067** | DOPRAVA | Bezplatná výpůjčka městských kol, elektrokol, koloběžek, elektrokoloběžek a skateboardů; v horách půjčování s vratnou zálohou. Bez nepodložených limitů nebo smluvních podmínek. |
| **CS-068** | ATLAS | Pátou kreativní zónu Larpingtonu a samostatné blízké kampusové město popsat jako navazující, nikoli totožné. Nezakreslovat nové administrativní hranice jako přesné bez geodetického/mapového podkladu. |
| **CS-069** | SPOLEČNOST | Ze článku o sociální podpoře odstranit editorské `Kánon nepotvrzuje univerzální základní příjem`; pozitivně popsat cílené dávky podle schváleného modelu 54A. |
| **CS-070** | BEZPEČNOST | Nevystavovat starou World Bible ani její kandidátní české motto. Jediné potvrzené veřejné motto je doslova `Life is meant to be lived.`. |

## 4. Implementace hledání atlasu podle A8B (povinné UX)

### 4.1 Nejdřív prověř existující architekturu

Audit uvádí hlavní viewer `atlas/current/viewer/atlas.html`, registry `atlas/current/registry/places.json` (159 objektů) a městský plán `atlas/current/capital/capital_plan_viewer.html` + `atlas/current/capital/cp_objects.json` (662 objektů). Hlavní atlas se zobrazuje v `iframe` na hlavní stránce. Nevnucuj moderní mapový framework, **zachovej původní SVG geometrii**, kolečko/gesta pro zoom a tažení mapy; drobný refactor stávajícího HTML/CSS/JS je v pořádku. Hledání v hlavním atlasu je primární cíl; pokud lze jednotné komponenty snadno využít i v městském plánu, doplň je, ale nikdy tím nerozbij jeho vlastní režimy.

### 4.2 Desktop

- Panel nahoře/po straně mapy v dosavadním vizuálním stylu, s políčky **Hledat**, **Ostrov**, **Typ**. Filtrování kategorií musí být čitelné a responzivní. Nezobrazuj návštěvníkovi přepínač `proposed`/`approved`, protože volba A1B chce všechna místa v orientačním atlasu.
- Ve výsledkové kartě **název, typ a ostrov / oblast**, pokud doložené; případně interní ID jako nenápadný identifikátor pouze je-li pro orientaci užitečný (ne jako hlavní text). Žádné `Bible`, statusy názvů/poloh, informace o AI prompech nebo fotografických výrobních pokynech.
- Kliknutí/Enter výsledku → vybrat, přiblížit a vycentrovat mapový objekt, zvýraznit vybranou kartu a otevřít veřejný detail. Přidat jasnou volbu „Zobrazit na mapě“, když je panel výsledků oddělený od detailu.
- **Vyhledávání bez diakritiky**: `.normalize('NFD')` + odstranění kombinujících znaků, casefold/lowercase, trim, slova hledat v rozumných kombinacích názvů/aliasů/typu/ostrova; neindexovat neveřejné `notes`, `photo_guide`, interní zdroje. Zachovat diakritiku ve zobrazeném textu.
- Výsledek se nesmí záviset na pořadí registru a prvních 40 shodách bez upozornění. Řazení: exact název/ID → začátek názvu → ostatní textové shody; stránkování nebo omezení s informací o počtu. Bez výsledků zobrazit „Žádné odpovídající místo jsme nenašli“ a možnost vymazat filtry.

### 4.3 Ovládání a přístupnost

- `label` a viditelný focus; sémantické tlačítko pro každou položku nebo správně implementovaný `listbox`/`option`; **šipky**, **Enter**, **Escape**, **Tab** a čitelné `aria-live` pro počty/shody. Klávesnicí musí být možné vybrat výsledek i otevřít detail.
- Ošetřit jednotný event handler pro zoom v detailu, nikoliv registrovat nového posluchače pokaždé při `show()`. Omezit výpočet při psaní podle potřeby, ale u 159 záznamů není třeba složitý engine.
- Stav výběru a mapový fokus zachovat při přepnutí filtrů, pokud to dává smysl; nechat bezpečný reset.

### 4.4 Telefon a dotyk

- Dnes je vyhledávání **pod mapou** (mapa cca 62vh), což nutí skrolovat. Na mobilu vlož **kompaktní viditelné tlačítko Hledat místa** nad mapu či na její okraj. Po stisku se otevře **vysouvací horní nebo spodní panel** s poli Hledat/Ostrov/Typ, výsledky a možností zavřít.
- Po výběru místa panel zavřít a ukázat vycentrovaný mapový bod. Detail zobraz jako mobilní panel, který nezakrývá celou mapu. Zpět/zavřít musí fungovat. Nepokládat ovládání na místo, kde překrývá horní navigaci webu nebo systémovou lištu telefonu.
- Dotykové zoomování dvěma prsty, posun mapy, kliknutí na bod, zobrazení výsledků a ovládání návratu otestovat. Zajistit dostatečné touch targety a přiměřenou kontrastnost. Pokud prohlížeč blokuje některá gesta, zdokumentovat omezení místo předstírání funkčnosti.

### 4.5 Zdroje pravdy a bezpečnost veřejného registru

- **Primární interní registry** jsou `places.json` a `cp_objects.json`. Dnes atlas čte vložený `<script id="reg">`; **městský plán se v `CP-B01`, `CP-PI01`, `CP-SQ02`, `CP-SQ10` liší od samostatného JSONu**. Zajisti **jednu udržovanou datovou autoritu** a generovaný výstup do atlasového HTML, nebo veřejný `fetch` **sanitizovaného veřejného registru**. Vždy ověř, že hosting používá HTTP server (přímé `file://` může fetch blokovat).
- **Nevystavuj syrový interní `places.json` a `cp_objects.json` s `notes`, prompty, návrhovými jmény, `Bible` a dalšími redakčními informacemi**, pokud obsahují neveřejné položky. Vytvoř veřejnou projekci se schválenými nebo bezpečně orientačními popisy. V interní práci zachovej původní data, včetně poloh; nemaž 159/662 položek jen kvůli statusům.
- Zvlášť projdi všechny čtyři odchylky městského registru, nepřeplácej správné údaje starší vloženou kopií; `CP-B01` musí být bez parlamentu všude. Přidej automatický test konzistence počtu ID a veřejně sdílených názvů/geometrie.
- **Nedotýkej se fyzické kalibrace mapy pro budoucí soutěž GeoGuessr.** Přesnost na metry nelze odvodit ze samotných pixelů ilustrativního SVG; nynější úkol je pouze vyhledávání a čistota webu.

## 5. Oddělení veřejných a interních souborů — povinný bezpečnostní krok

**Důležité:** Audit potvrdil HTTP 200 pro několik interních dokumentů na **lokálním preview**; *nepotvrdil*, že totožné cesty jsou zveřejněné na produkčním webu. Prověř skutečný způsob deploye a podle něj oprav.

1. **Nevystavovat celý repozitář jako document root.** Upřednostni bezpečný build/export s veřejným adresářem, výslovně schválenými cestami nebo konfiguračním allowlistem. Jestli projekt nemá build, uprav `scripts/serve_static.mjs` a nasazovací workflow tak, aby z veřejné stránky nešlo načíst interní oblasti.
2. Zveřejnit jen nezbytné HTML/CSS/JS, bezpečné mapové/encyklopedické projekce a samotné skutečné obrázky/videa. `references/`, `docs/` s reporty, staré `data/larpidia_world_bible.json`, prompty, interní foto JSON, záložní historie verzí a pracovní instrukce **nepatří** mezi veřejné assety. Pokud si aplikace nyní načítá přímo `content/larpidia/facts.json` a články, publikuj **vyčištěnou veřejnou kopii** potřebných dat, nikoliv celou zdrojovou složku se soukromými komentáři.
3. **Rychlý smoke test:** přímé URL na interní dokumenty a citlivé JSON cesty musí vracet přiměřený 403/404; veřejná encyklopedie, atlas, mapa, 3D a galerie nadále musí vracet 200 a skutečně fungovat. Testuj lokální preview i přesné produkční hostingové nastavení, pokud je dostupné. Bez přístupu k produkci tuto mezeru výslovně uveď v reportu.
4. **Neřešit pouze skrytím odkazů v menu.** Pokud je soubor dostupný přímou URL, problém trvá. Nepřepisuj ani nemaž archivy v pracovním stromu. Ověř, že nepropadne přímá URL starých `atlas/versions/` nebo galerie s prompty.
5. Nezahrnuj hesla, tokeny, osobní údaje ani jiné neveřejné materiály do veřejných JS bundle, SVG metadat a JSON fetch odpovědí.

## 6. Příklady přirozeného veřejného textu

- **Atlas:** „Prozkoumejte ostrovy Larpidie na orientační mapě. Vyberte místo nebo ho najděte podle názvu.“
- **3D model:** „3D Larpington — prohlédněte si městské ulice, čtvrti a okolní pobřeží.“
- **Železnice:** „Horská L1 a historická elektrická L2 spojují významné oblasti ostrova. Městská část L3 je v provozu; podmořské spojení na Paraland se dokončuje a nyní je možné cestovat lodí.“
- **Školy:** „Veřejné školy vyučují od pondělí do pátku. Výuka začíná před devátou hodinou nejvýše dvakrát týdně.“
- **Historie:** „Hlavní interaktivní muzeum v Larpingtonu přibližuje vývoj země. Na Paralandu vzniká menší navazující expozice.“
- **Důchod:** „Larpidští občané mají od 65 let nárok na základní státní důchod. Jeho výchozí měsíční částka činí 12 000 Kč.“
- **Moře:** „Významná část okolního moře patří do chráněné rezervace. Přístup do citlivých lokalit podléhá návštěvnickým pravidlům a kapacitním omezením.“
- **Kultura:** „Dobrovolný Den larpu a Mog Day jsou součástí místních komunitních akcí; zapojit se lze i bez zveřejňování vlastní fotografie.“
- **Patička:** `© Larpidie · Fiktivní studentský projekt · Web vX · Atlas vY` — jen když X/Y odpovídají skutečným metadatům; jinak zobraz název bez čísla.

## 7. Kontroly před předáním

**Funkčnost:**

- Spustit existující linter/testy/build; otestovat aktivní routy, všech 39 článků, 9 kategorií, atlas (159 objektů), plán (662 objektů), oba 3D modely, galerii i přechody z původního menu. Neodstraňovat aktivní obsah kvůli drobným nedostatkům.
- Ověřit, že první uživatelská oprava encyklopedie (nový nadpis, 4 úvodní karty, tmavší tlačítko) zůstala zachována a žádná regresní změna ji nevrátila. Kontrast sekundárních tlačítek a focus alespoň na úrovni běžné přístupnosti.
- Ověřit desktop a skutečný mobilní viewport ve vyhledávání, plynulost mapového posunu, zaměření bodu z výsledků a návrat z detailu. Když není možná interaktivní ruční zkouška, pravdivě zdokumentovat **co se otestovalo automaticky a co ne**.
- Automatizovat kontrolu `parlament`, `parliament`, `draft`, `proposed`, `needs-decision`, `prompt-ready`, `Bible`, `photo_guide` ve **veřejně zveřejněných řetězcích a assetech**, nikoliv slepě v celém pracovním repozitáři (archiv je legitimní). Rozlišit případnou historickou citaci od tvrzení o současné instituci.
- Hlídat **přesně 102 původních rozhodnutí**, žádné nové ústavní otázky. Autorovy A1–A8 jsou doplnění UI a každodenního fungování, nemění historii hlasování 1–102. Pokud je kánon dostupný, spočítat hash před/po; neupravovat jeho bajty.

**Obsah:**

- Potvrdit `32 000` obyvatel, `175 km²` hlavního ostrova, `14 km²` Paralandu, 4 spoluvládce a žádný parlament.
- DPH 12/5 %, daň firem 5 %, pracovní týden 24 hodin, školy 5 dnů, důchod 12 000 Kč od 65 let pro občany, 16 % populace 65+, modelových 14 000 pracujících.
- Vývoz řasových paliv, spolupráce Japonsko/Jižní Korea pouze **ve fikci**, L1/L2 provoz, podmořská L3 ve výstavbě, Paraland chráněné moře, muzeum Larpington otevřené / Paraland ve výstavbě.
- Ústavní detaily zejména rozhodnutí **37B**, **38B**, **40B**, **41B**, **42C**, **34A**, **35A**, **36A**. Ponechat nezměnitelné principy, právo zastavení s 95 % **všech** oprávněných, ne 95 % účasti, a bezparlamentní uspořádání.
- **Nedoplňovat** libovolné přesné hranice rezervací, neexistující turistické poplatky, městské adresy, počty vojáků a provozní dobu muzeí.

## 8. Požadované výstupy v projektu

Implementuj změny přímo. **Nevytvářej druhou encyklopedii**, uprav aktivní. Neměň původní kánon v2.6. Proveď testy a vytvoř dva **interní** reporty:

1. `docs/LARPIDIA_PUBLIC_CONTENT_FIX_REPORT.md` — seznam souborů, změny, ověření, tabulka `CS-001`–`CS-070` se stavem **HOTOVO / ČÁSTEČNĚ / BLOKOVÁNO / ZÁMĚRNĚ VYNECHÁNO**; u nehotových přesný technický či obsahový důvod, žádná nevysvětlená vynechání. Uveď které faktické doplňky A1–A8 byly uloženy do centrálních dat a kde.
2. `docs/LARPIDIA_ATLAS_SEARCH_IMPLEMENTATION.md` — popis nového vyhledávání, UX pro desktop/mobil, jak upravit registry a testy konzistence, seznam dostupných omezení a výsledky zkoušek.

V reportu také potvrď, kde a jak se vykreslují **verze v patičce**, odkud se berou jejich skutečné hodnoty a jak se mění v budoucnu. Pokud se verze nedala bezpečně zjistit, přiznej to a nedoplňuj fiktivní číslo.

**Zakázáno:** nové ústavní otázky 103+, nahrazení mapy jiným náhodným atlasem, smazání 159/662 objektů, záměna turistických tržeb za státní příjem, vymyšlení faktů, odeslání změn na Git/hosting bez uživatelova pokynu. Bez výslovného zadání žádný `git commit`, `git push`, ani přestavba 3D geometrie.

**Finální zpráva pro autora:** krátké shrnutí provedených oprav, cesty dvou reportů, potvrzení zachování kánonu, seznam případných přesných překážek. Nepotřebuješ se ptát na další obsah; kde chybí informace, použij bezpečné obecné znění nebo věc vynech a zaznamenej interně.
