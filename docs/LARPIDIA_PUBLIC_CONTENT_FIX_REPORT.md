# Larpidie — zpráva o opravách veřejného obsahu

**Datum:** 1. listopadu 2026  
**Podklady:** schválené zadání po auditu, aktuální pracovní kánon v2.6 a oba předchozí audity v `docs/`.  
**Rozsah:** hlavní stránka, encyklopedie, mapy, plán Larpingtonu, 3D modely, galerie a statický export.

## Výsledek

Kánon v2.6 zůstal beze změn. Schválená upřesnění A1–A8 byla zanesena do veřejných textů, centrálních faktů a návštěvnických rozhraní. Zachována je dosavadní estetika, mapová geometrie, 3D data i ostatní stránky. Sjednotil se název radnice v CP-B01 a poznámka stanice ST-S; vložený registr městského plánu je nyní synchronizován s `cp_objects.json`.

Veřejný build vytvořil `public/` s **72 výslovně povolenými soubory**: všech 39 článků, 159 míst atlasu, 662 objektů plánu, původní modelové soubory a dvě dostupné galerie fotografií. Interní podklady ani výrobní balíček se nekopírují. Lokální server obsluhuje pouze `public/`.

## Stav nálezů CS-001 až CS-070

| ID | Stav | Provedená oprava |
|---|---|---|
| CS-001 | Hotovo | Název mapové sekce je neutrální; verze se načítají ze společných metadat do patičky. |
| CS-002 | Hotovo | L1 a L2 jsou popsané jako provozované linky; L3 rozlišuje městský a dokončovaný podmořský úsek. |
| CS-003 | Hotovo | Galerie ukazuje pouze dvě existující fotografie; chybějící scény nejsou vydávány za hotová média. |
| CS-004 | Hotovo | Popisek Larpingtonu zní „Orientační vizualizace Larpingtonu z výšky“. |
| CS-005 | Hotovo | Veřejné záhlaví atlasu nese název „Atlas Larpidie“; draft a verze jsou odstraněny z mapového těla. |
| CS-006 | Hotovo | Vyhledávání používá neutrální příklad místa nebo ID, bez Aokawy. |
| CS-007 | Hotovo | Interní odkazy na World Bible a workflow byly odstraněny; mapa uvádí orientační přesnost. |
| CS-008 | Hotovo | Veřejné vrstvy popisují geografii a funkce, ne stav schvalování. |
| CS-009 | Hotovo | Veřejný registr 159 míst obsahuje jen návštěvnická pole; poznámky, statusy, reference a foto vodítka zůstávají interní. |
| CS-010 | Hotovo | Nejvyšší vrchol je označen „přibližně 560 m n. m.“ |
| CS-011 | Hotovo | 3D terén má veřejný název „3D reliéf Larpidie“ a orientační popis výšek. |
| CS-012 | Hotovo | Z 3D Larpingtonu zmizel pracovní štítek i populace 12 000; rozlišení stávající a plánované zástavby zůstalo. |
| CS-013 | Hotovo | Městský plán se jmenuje „Plán Larpingtonu“; verze je pouze v patičce. |
| CS-014 | Hotovo | Příklad hledání používá radnici a tržnici, ne parlament. |
| CS-015 | Hotovo | Městské vrstvy mají návštěvnické názvy pro zástavbu, dopravu, objekty, zeleň a popisky. |
| CS-016 | Hotovo | Všech 662 objektů zůstává v plánu; veřejné detaily neobsahují poznámky, Bible/ref, statusy ani neověřené adresy. |
| CS-017 | Hotovo | CP-B01 je „Radnice Larpingtonu“ / „Larpington Town Hall“ ve zdrojovém i vloženém registru. |
| CS-018 | Hotovo | Ze záznamu ST-S byla odstraněna parlamentní funkce. |
| CS-019 | Hotovo | Starší World Bible zůstává archivní a není součástí veřejného exportu. |
| CS-020 | Hotovo | Populace 32 000 se bere z `facts.json`. |
| CS-021 | Hotovo | Starší geografické reference se v exportu nezveřejňují. |
| CS-022 | Hotovo | Starší realistické a ústavní návrhy se v exportu nezveřejňují. |
| CS-023 | Hotovo | Galerie uvádí existující obrazové soubory bez `generated_image:null` či pracovních karet. |
| CS-024 | Hotovo | Prompty, názvy `PHOTO_*` a metadata AI zůstávají mimo veřejný seznam médií. |
| CS-025 | Hotovo | Build používá allowlist a náhledový server vrací 404 pro interní cesty. |
| CS-026 | Hotovo | Ostrovy jsou popsány v severozápadním Pacifiku se schematickými zeměpisnými vztahy, bez GPS souřadnic. |
| CS-027 | Hotovo | Přírodní popisy se drží doložené nádrže, řek a vodopádu bez odhadů průtoků a jmen. |
| CS-028 | Hotovo | U mapy je jedno obecné upozornění na orientační charakter; provoz dopravy je vysvětlen zvlášť. |
| CS-029 | Hotovo | L1 je v provozu a citlivé podzemní prostory podléhají ochrannému režimu. |
| CS-030 | Hotovo | Horské půjčovny uvádějí zapůjčení s vratnou zálohou, bez ceníku či vymyšlených pravidel. |
| CS-031 | Hotovo | Rezervace, povolenky a limity jsou popsány návštěvnicky; bez hranic, cen, kapacit a nedoložených útesů. |
| CS-032 | Hotovo | U nezávislosti zůstal rok 1921 bez smyšleného dne. |
| CS-033 | Hotovo | Košťálova role je popsána jako hospodářský a společenský vliv, bez domyšleného titulu. |
| CS-034 | Hotovo | Obnova zachycuje hospodářský tlak a společenské dopady bez vymyšlených obětí či zásahů. |
| CS-035 | Hotovo | Současný děj uvádí Košťálovo věznění; hypotetické úplatky, návrat ani rozsudek nejsou vydávány za události. |
| CS-036 | Hotovo | Hlavní muzeum v Larpingtonu je otevřené; expozice na Paralandu se dokončuje. |
| CS-037 | Hotovo | DPH 12 % a 5 % je uvedeno v centrálních datech bez vymyšlených kategorií. |
| CS-038 | Hotovo | Progresivní daňová pásma se načítají z centrálních faktů. |
| CS-039 | Hotovo | Pracovní týden je 24 hodin, pondělí až čtvrtek po šesti hodinách; služby fungují ve směnách. |
| CS-040 | Hotovo | 14 000 pracujících je modelový údaj bez vymyšleného sektorového rozpisu. |
| CS-041 | Hotovo | Články uvádějí výrobu a vývoz řasových paliv a dalších produktů do Japonska a Jižní Koreje. |
| CS-042 | Hotovo | Zdravotnictví a školství mají jeden společný modelový rámec 1,6 mld. Kč; není rozdělen na dva resortní rozpočty. |
| CS-043 | Hotovo | Penzijní propočet je označen jako maximální ilustrativní scénář, ne jako skutečný výdaj. |
| CS-044 | Hotovo | Zahraniční specializovaná péče je vázaná na posouzenou potřebu a smluvní spolupráci. |
| CS-045 | Hotovo | Důchod 12 000 Kč od 65 let náleží larpidským občanům bez podmínky odpracovaných let. |
| CS-046 | Hotovo | Model 65+ se nepovažuje automaticky za počet oprávněných občanů; doplňkové srovnání je podmíněné. |
| CS-047 | Hotovo | Samostatné kampusové město a univerzitní zóna Larpingtonu jsou popsány jako navazující místa bez smyšleného názvu či adres. |
| CS-048 | Hotovo | Školní týden je pondělí až pátek; před 9. hodinou se začíná nejvýše dvakrát týdně. |
| CS-049 | Hotovo | Kuchyně popisuje ryby, řasy, rýži a britské a české vlivy bez vnuceného národního pokrmu. |
| CS-050 | Hotovo | Kulturní článek uvádí výroční festival a dobrovolné komunitní akce bez smyšleného názvu či data. |
| CS-051 | Hotovo | Popsány jsou čtyři resortní bloky a jejich společné rozdělení bez přiřazení konkrétním spoluvládcům. |
| CS-052 | Hotovo | Ústavní přehled vychází z potvrzených pravidel a vynechává editorské poznámky o nedokončených lhůtách. |
| CS-053 | Hotovo | Návrhy zákonů mohou podávat oprávnění občané od 15 let; kontrola a hlasování jsou popsány bez vymyšlených lhůt. |
| CS-054 | Hotovo | Elektronické hlasování je popsáno jako ústavní princip, ne jako hotová aplikace. |
| CS-055 | Hotovo | Veto je popsáno jako odkladné, se smírem a případným rozhodnutím občanů. |
| CS-056 | Hotovo | Odvolání uvádí prahy, dvanáctiměsíční odstup a soudně posuzovanou výjimku. |
| CS-057 | Hotovo | Ústavní soud a demokratické jádro jsou popsány bez vymyšleného seznamu ustanovení či jmenování soudců. |
| CS-058 | Hotovo | Veřejné úřady mají přímou volbu a druhé kolo; zvláštní odborná pravidla volebního úřadu jsou oddělena. |
| CS-059 | Hotovo | Volební úřad je nezávislý; text neslibuje neexistující dokončený hlasovací software. |
| CS-060 | Hotovo | Finanční dohled uvádí odbornou nominaci, potvrzení občany a sedmiletý mandát bez smyšlených komisí. |
| CS-061 | Hotovo | Běžný rozpočet vyžaduje tři hlasy, mimořádné závazky jednomyslnost; jejich povaha se posuzuje vůči příjmům a délce. |
| CS-062 | Hotovo | Provizorium je omezené na jednu dvanáctinu předchozího rozpočtu měsíčně; výjimky nejsou domýšleny. |
| CS-063 | Hotovo | Bezpečnostní spolupráce s Japonskem a Jižní Koreou je výslovně součástí fikčního světa, nikoli skutečná mezistátní smlouva. |
| CS-064 | Hotovo | Krizové plánování pokrývá oba ostrovy a civilní záchranné složky bez smyšlených evidencí návštěvníků. |
| CS-065 | Hotovo | Garda je popsána vedle policie, pobřežní stráže a záchranných složek bez neznámých počtů či výzbroje. |
| CS-066 | Hotovo | Paraland uvádí přibližně poloviční soukromé a státní vlastnictví historických objektů, možné kulturní využití i konzervované ruiny. |
| CS-067 | Hotovo | Městské půjčovny kol, elektrokol, koloběžek, elektrokoloběžek a skateboardů jsou bezplatné; horské půjčovny vracejí zálohu. |
| CS-068 | Hotovo | Pátá univerzitní a kreativní zóna navazuje na samostatné kampusové město; nové hranice nebyly zakresleny jako přesné. |
| CS-069 | Hotovo | Sociální podpora je popsána pozitivně jako cílená pomoc podle potřebnosti. |
| CS-070 | Hotovo | Veřejný export neobsahuje starou World Bible ani její alternativní motto; centrální motto zní „Life is meant to be lived.“ |

## Kontroly a omezení

- `node scripts/validate_encyclopedia.mjs` — prošlo: 9 kategorií, 39 článků a 7 médií.
- `node scripts/check_encyclopedia_runtime.mjs` — prošlo: centrální fakta, závislé výpočty a vnořené routy.
- `node scripts/check_public_export.mjs` — prošlo: 72 povolených souborů, 159 atlasových míst, 662 objektů plánu a syntaktická kontrola skriptů.
- `node scripts/check_encyclopedia_http.mjs` — prošlo: 79 veřejných cest HTTP 200 a 9 interních cest HTTP 404.
- `python atlas/scripts/check_atlas.py` se spustil, ale skončil na chybějícím modulu `numpy`; žádná nová závislost nebyla instalována.

Hostingová konfigurace v projektu nalezena nebyla. Lokální HTTP kontrola proto potvrzuje chování upraveného náhledového serveru, nikoli stav externí produkční služby. Automatický vizuální snímek atlasu nebyl dostupný; ověřena je syntaxe, obsah registrů a zdrojové responzivní CSS.
