# Dokončení veřejného atlasu, obsahu a rozhraní

Datum ověření: 2026-11-04.

## Výsledek

Kořenový web byl otevřen přes místní HTTP server s kořenem v projektu a navigací běžnou cestou přes 'http://127.0.0.1:62489/index.html#atlas'. Aktivním atlasovým iframe je 'atlas/current/viewer/atlas.html'; plán Larpingtonu používá 'atlas/current/capital/capital_plan_viewer.html'. Veřejný export i aktivní soubory vznikají z redakční vrstvy a šablon skriptem 'scripts/build_public_site.mjs'.

Zůstalo zachováno všech **159 míst atlasu** a **662 objektů plánu**. Každý má veřejný český název a popis, v redakční vrstvě není žádný prázdný ani kratší než 75 znaků dlouhý popis. V atlasu ani plánu nezůstaly duplicitní veřejné názvy ani obecné názvy typu „Bod zájmu“ či „Objekt“. T-02 se veřejně jmenuje přesně **Cimprlichovo Hradiště**; dřívější pravopis zůstává pouze jako interní vyhledávací alias. Identifikátory, stavová metadata a zdrojové poznámky zůstaly ve zdrojových registrech a ve veřejném rozhraní se nevykreslují.

Nově vzniklé názvy jsou označené jako redakční návrhy, ne jako změna ústavního kánonu. Soubor kánonu v2.6 zůstal beze změny. Úplný převod názvů a důvody jsou v [redakčním přehledu](LARPIDIA_EDITORIAL_PLACE_NAMES_REVIEW.md).

## Bodové ověření obsahu

Kořenový prohlížečový test vizuálně otevřel 21 karet atlasu a 21 objektů městského plánu. Následující tabulky uvádějí veřejné názvy a skutečné popisy z generovaného registru.

### Atlas

| Interní ID (jen v této zprávě) | Veřejný název | Typ | Veřejný popis |
| --- | --- | --- | --- |
| T-01 | Praha | Město | Praha leží v centrální nížině hlavního ostrova. Silniční a železniční vazby ji spojují s Larpingtonem, severními sídly i východním dopravním koridorem. |
| T-02 | Cimprlichovo Hradiště | Město | Cimprlichovo Hradiště leží v jižní části hlavního ostrova na cestě mezi Larpingtonem, západní vysočinou a přehradní oblastí. Městem prochází silniční i železniční spojení do vnitrozemí. |
| C-01 | Larpington | Hlavní město | Larpington je hlavním městem na jižním pobřeží hlavního ostrova. Jeho historické jádro tvoří čtyři tradiční čtvrti — Chalupecká, Kynčlova, Klimečkova a Žemličkova — vedle nichž se rozvíjí univerzitně-kreativní městská zóna. Samostatné kampusové město leží poblíž, ale do Larpingtonu nepatří. |
| T-03 | Havlišovo Doupě | Město | Havlišovo Doupě je horská obec na západě ostrova, v krajině lesnatých svahů a drobných vodních toků. Silniční trasa ji spojuje s Cimprlichovým Hradištěm. |
| T-04 | Ōru Maito | Město | Ōru Maito leží při severní zátoce a pobřežních trasách hlavního ostrova. Místní stanice a silnice navazují na síť severních sídel. |
| M-01 | Larpova hora | Horský vrchol | Larpova hora je lesnatý horský masiv v západní části ostrova. Vrchol dosahuje přibližně 560 m n. m.; hodnota je orientační, nejde o geodetickou kótu. Od hřebene vedou pěší trasy k nižším vrcholům. |
| M-02 | Zimní hora | Horský vrchol | Zimní hora má strmější svah se sjezdovkou a startem pro paragliding. Krátká zimní sezona omezuje lyžařské využití; značené trasy pokračují do okolních hor. |
| M-03 | Kulatý vrch | Horský vrchol | Kulatý vrch se zvedá nad horskými loukami a značenými pěšími trasami. Na svahu jsou vyznačeny také start a přistávací louka pro paragliding. |
| N-01 | Skalní vyhlídka nad mořem | Skalní vyhlídka | Skalní vyhlídka leží na západním pobřeží nad mořem a je přístupná po značené útesové stezce. Oplocené vyhlídkové místo umožňuje zastavit u okraje pobřežní krajiny. |
| N-02 | Krystalová jeskyně | Jeskyně | Krystalová jeskyně leží v západním horském pásmu. Horská železnice L1 projíždí tunelem po jejím obvodu; návštěvnický pohyb v citlivém místě je regulován. |
| N-03 | Vodopád na horském toku | Vodopád | Vodopád leží na horském toku v západním vnitrozemí, mezi Krystalovou jeskyní a přehradní oblastí. Podél vody vede pěší trasa a poblíž zastavuje horská linka L1. |
| N-04 | Přehradní jezero | Přehradní jezero | Přehradní jezero je součástí vodárenské soustavy západního vnitrozemí. Hráz, vyhlídka a železniční zastávka jsou v mapě vedeny odděleně; pobřeží podléhá ochraně zdroje vody. |
| V-02 | Útesová vyhlídka pod Larpovou horou | Vyhlídka | Oplocená útesová vyhlídka leží pod Larpovou horou na západním pobřeží. K místu vede značená stezka; vyhlídková plošina otevírá pohled přes moře. |
| SP-01 | Pramen řeky Larp | Pramen a studánka | Pramen řeky Larp leží v západním vnitrozemí u pěších tras horského povodí. Mapa jej uvádí jako prameniště; nehodnotí pitnost vody. |
| SP-04 | Studánka na stezce ke Kulatému vrchu | Pramen a studánka | Studánka leží pod Kulatým vrchem u pěší trasy na hřeben. Je vedena jako orientační vodní bod; pitnost není v atlasu specifikována. |
| B-01 | Západní pláž Larpingtonského zálivu | Pláž | Písečná pláž leží na západním okraji Larpingtonského zálivu, jižně od městského centra. Přístup k ní vede z pobřežní silnice. |
| PL-02 | Hrad Paralandu | Hrad | Hradní areál stojí ve vnitrozemí Paralandu v dosahu pěší památkové trasy. Mapa jej zasazuje do chráněné přírodní krajiny ostrova. |
| L1 | Horská železniční linka | Železniční linka | Horská linka L1 vede západním vnitrozemím kolem horské stanice, Krystalové jeskyně, vodopádu a přehrady. Linka je v provozu; její mapové vedení má orientační charakter. |
| L2 | Historická elektrická linka | Železniční linka | Linka L2 propojuje města hlavního ostrova s Prahou, Aokawou, Hoshimachi, letištěm a východním přístavem. Elektrická železnice je v provozu. |
| L3 | Městská rychlá linka | Železniční linka | Městský úsek linky L3 je v provozu a obsluhuje Larpington. Podmořské pokračování na Paraland se dokončuje; mez ostrovy nyní jezdí lodě a trajekty. |
| P-01 | Železniční spojení na Paraland | Železniční spojení | Podmořské železniční spojení na Paraland je připravovaným pokračováním linky L3, nikoli otevřeným tunelem. Do dokončení stavby zajišťují spojení mezi ostrovy lodě a trajekty. |

### Plán Larpingtonu

| Interní ID (jen v této zprávě) | Veřejný název | Typ | Veřejný popis |
| --- | --- | --- | --- |
| CP-01 | Plán Larpingtonu | Městský plán | Orientační plán zachycuje kompaktní Larpington s nepravidelnými ulicemi, městskými bloky, parky a historickým přístavem. Rozlišuje čtyři tradiční čtvrti; univerzitně-kreativní zóna je potvrzena v kánonu, její přesný obvod však tento plán nevymezuje. Samostatné kampusové město neleží uvnitř městských čtvrtí. |
| CP-B01 | Radnice Larpingtonu | Budova | Radnice leží v občanském centru Larpingtonu, v dosahu Náměstí čtyř a hlavních městských ulic. Její poloha propojuje správní funkce s veřejným prostorem centra. |
| CP-B06 | Interaktivní muzeum Košťálovy éry | Budova | Muzeum dějin Larpidie v Larpingtonu je otevřené. Interaktivní expozice využívá archivní materiály, filmovou rekonstrukci a komentované prohlídky; leží u Centrálního parku. |
| CP-B07 | Historický kostel na Kostelním náměstí | Budova | Historický kostel stojí na Kostelním náměstí v Žemličkově čtvrti. Cihla a kámen jej propojují s měřítkem starší městské zástavby. |
| CP-SQ01 | Náměstí čtyř | Veřejné prostranství | Náměstí čtyř je veřejným prostranstvím v Larpingtonu. Navazuje na okolní ulice a městské budovy. |
| CP-PK02 | Centrální park | Park | Centrální park tvoří zelenou plochu v Žemličkově čtvrti a přerušuje souvislou městskou zástavbu. |
| CP-PR01 | Přístavní promenáda | Promenáda | Přístavní promenáda sleduje pobřeží Larpingtonu a propojuje pěší veřejné prostory v přístavní části města. |
| ST-W | Larpington Západ (Chalupecká) | Železniční stanice | Larpington Západ (Chalupecká) obsluhuje městskou železniční síť a leží v Chalupecké čtvrti. Její poloha navazuje na místní ulice a veřejná prostranství. |
| ST-S | Larpington Střed – Přístav (Žemličkova) | Železniční stanice | Larpington Střed – Přístav (Žemličkova) obsluhuje městskou železniční síť a leží v Žemličkově čtvrti. Její poloha navazuje na místní ulice a veřejná prostranství. |
| CP-BL-0001 | Nízký obytný blok u Školní třídy (Kynčlově čtvrti) | Nízký obytný blok | Plán vymezuje tuto plochu mezi ulicemi Školní třída a Severní třída v Kynčlově čtvrti pro nízkou obytnou zástavbu. Jde o jednu z ploch určených pro čtení v podrobném měřítku plánu. |
| CP-BL-0342 | Blok starší městské zástavby u Okružní ulice Starého Města (Žemličkově čtvrti) | Blok starší městské zástavby | Plán vymezuje tuto plochu mezi ulicemi Okružní ulice Starého Města a Lipová ulice v Žemličkově čtvrti pro smíšené využití starší městské zástavby. Jde o jednu z ploch určených pro čtení v podrobném měřítku plánu. |
| CP-CF01 | Kavárna u Tržnice | Kavárna | Kavárna u Tržnice je zakreslena v městském parteru Žemličkově čtvrti, v návaznosti na okolní veřejné prostory. |
| CP-RN01 | Půjčovna kol a e-skútrů – přístav | Půjčovna | Půjčovna kol a e-skútrů – přístav doplňuje nabídku městské mobility v Larpingtonu a leží v dosahu veřejné dopravy nebo pobřeží. |
| CP-SH04 | Obchodní pasáž Hlavní třídy | Obchod | Obchodní pasáž Hlavní třídy navazuje na obchodní osu a pěší prostory Klimečkově čtvrti. Poloha v plánu jej řadí do městského parteru. |
| CP-ZR02 | Zóna Hlavní třídy | Obchodní oblast | Zóna Hlavní třídy navazuje na obchodní osu a pěší prostory Žemličkově čtvrti. Poloha v plánu jej řadí do městského parteru. |
| CP-UL01 | Hlavní třída | Městská ulice | Hlavní třída je součástí uliční sítě v Klimečkově čtvrti; v okolí leží Obchodní dům Northlight a Obchodní pasáž Hlavní třídy. |
| CP-AR01 | Bezbariérová trasa stanice Larpington Střed–Přístav → Přístavní náměstí | Pěší trasa | Bezbariérová trasa stanice Larpington Střed–Přístav → Přístavní náměstí propojuje bezbariérově přístupné veřejné prostory v městské síti Larpingtonu. |
| CP-B12 | Škola – Kynčlova čtvrť | Budova | Škola – Kynčlova čtvrť doplňuje školní a vzdělávací zázemí Kynčlově čtvrti. Je součástí městské vybavenosti v dosahu okolních ulic. |
| CP-PK03 | Severní park | Park | Severní park tvoří zelenou plochu v Kynčlově čtvrti a přerušuje souvislou městskou zástavbu. |
| CP-BL-0243 | Blok nového nábřeží u Skleněné ulice (Klimečkově čtvrti) | Blok nového nábřeží | Plán vymezuje tuto plochu mezi ulicemi Skleněná ulice a Třída Východního nábřeží v Klimečkově čtvrti pro novější městskou zástavbu u nábřeží. Jde o jednu z ploch určených pro čtení v podrobném měřítku plánu. |
| CP-PI01 | Molo lodní linky | Přístavní molo | Molo lodní linky zpřístupňuje lodní dopravu v historickém přístavu Larpingtonu. |

## Rozhraní a ověření

- T-02 lze najít interním ID i starším pravopisem; výsledek a karta zobrazí pouze **Cimprlichovo Hradiště**. Karta obsahuje geografický kontext, dopravní vazby, atlasové souřadnice, přibližnou výšku a sousední místa s vypočteným směrem a vzdáleností.
- Praha, Larpington, horská linka L1, pobřežní vyhlídka V-02 a hlavní muzeum mají obsahově specifické karty. Detail Larpingtonu uvádí čtyři kanonické čtvrti a výslovně odlišuje samostatné kampusové město.
- Kořenový test otevřel atlas běžnou navigací; ověřil hledání T-02, kliknutí do výsledků, dva opakované přímé kliky na mapu a dotyk na mapový prvek. Ověřil skrytí ID a produkčních stavů v DOM, uzavření nastavení vrstev po výběru, správnou velikost loga a jednu kopii loga.
- Veřejný export byl otevřen v Edge přes 'http://127.0.0.1:61279/index.html#atlas' a 'http://127.0.0.1:61279/index.html#galerie'. Test ověřil atlas, plán, opakovaný klik na mapový prvek, ovládání vrstev, mobilní rozložení, galerii, článek s fotografií a dostupnost neveřejných cest; dočasný server se po testu ukončil.
- Exportní kontrola: 74 souborů v allowlistu, 39 článků, 159 míst a 662 objektů; 72 veřejných HTTP cest obslouženo a 17 neveřejných cest vrací 404.
- Zdroje veřejného registru a šablony jsou [atlas_places_editorial.json](../content/larpidia/atlas_places_editorial.json), [atlas_viewer_template.html](../templates/atlas_viewer_template.html), [capital_plan_viewer_template.html](../templates/capital_plan_viewer_template.html), [public_viewer_renderers.mjs](../scripts/public_viewer_renderers.mjs) a [build_public_site.mjs](../scripts/build_public_site.mjs).

## Mapová grafika a snímky

Sídelní texturu tvoří řídké malé bloky v existujících sídelních obrysech. Obrysy mají vypnutou výraznou linku; cesty, dopravní vedení a všechny SVG atributy 'd' zůstaly nezměněné. Ověřená srovnávací snímky jsou pořízené ve stejném zobrazení:

- [Před úpravou 2D textury](debug-screenshots/atlas-2d-city-before.png)
- [Po úpravě 2D textury](debug-screenshots/atlas-2d-city-after.png)

Další snímky skutečného kořenového webu v [docs/debug-screenshots](debug-screenshots/): [T-02 – atlas-live-server-fixed.png](debug-screenshots/atlas-live-server-fixed.png), [Praha](debug-screenshots/atlas-root-live-praha.png), [Cimprlichovo Hradiště](debug-screenshots/atlas-root-live-cimprlichovo.png), [Larpington](debug-screenshots/atlas-root-live-larpington.png), [L1](debug-screenshots/atlas-root-live-railway-rich-card.png), [vyhlídka V-02](debug-screenshots/atlas-root-live-poi-detail.png), [muzeum v plánu](debug-screenshots/capital-root-live-museum.png), [mobilní galerie](debug-screenshots/gallery-live-mobile.png), [soukromý obrazový archiv](debug-screenshots/author-media-modal.png) a [velikost loga](debug-screenshots/footer-logo.png).

## Zachování dat a omezení

Strukturní porovnání zdrojových registrů s výchozím stavem potvrdilo shodná ID a data; 361 cest v atlasovém SVG a 5 954 cest v plánu Larpingtonu mají shodné atributy geometrie. Výšková data, geometrická data 3D scén a oba zdrojové 3D prohlížeče zůstaly beze změny; porovnání SHA-256 exportu také prošlo.

Ve fotoarchivu jsou skutečné dva snímky a 18 plánovaných scén bez souboru. Galerie ukazuje pouze dostupné fotografie bez prázdných karet; chybějící scény jsou uvedené v interním archivu a mediálním přehledu. Nových redakčních názvů je 591; jejich místní odvození a stav schválení jsou přehledně označené, ale jejich případné budoucí povýšení na kanonické názvy vyžaduje redakční rozhodnutí.
