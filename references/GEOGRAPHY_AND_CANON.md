# Referenční geografická bible Larpidie (v1.0 — návrhová mapa)

> Všechno v souboru je **prostorový pracovní návrh** pro vizuální kontinuitu, dokud autoři neschválí finální mapu. Závazná fakta jsou ve `data/larpidia_world_bible.json`. Názvy a hodnoty s poznámkou `PROPOSED` jsou volitelné návrhy.

## Závazná orientace

- Hlavní ostrov Larpidie: přibližně 150–200 km²; pracovní varianta 175 km². Orientovaný zhruba západ–východ, mírně členité pobřeží, západní zalesněná vysočina a nižší východ.
- Paraland: menší samostatný ostrov **jihovýchodně** od hlavního. Pracovní rozloha 14 km², úzký průliv přibližně 1,5 km. Nenahrazovat další čtvrtí hlavního ostrova.
- Sever = nahoře, východ = vpravo. Všechny obrázky, plány a mapy tím musí být slučitelné.
- Západ / severozápad: lesy, skalnaté vyhlídky a útesy, nejvyšší horský masiv.
- Vnitrozemský západ: horské řeky, vodopád, krasově nebo vulkanicky podmíněná návštěvnická krystalová jeskyně, přehradní jezero.
- Východ / severovýchod: relativně rovnější průmyslová nížina, upravené výrobní areály a regionální letiště.
- Jih / jihovýchod: pláže a hlavní město s historickým přístavem, luxusním obchodem a univerzálně přístupnými prostranstvími.
- Sever: kompaktní smíšená anglicko-japonská městečka; tradiční trhy a staré kostely zůstávají součástí kulturního dědictví.

## Tvarová referenční pravidla ostrovů

Pro první **master mapu** zvol konkrétní siluetu a ulož souřadnice pobřeží jako SVG path, GeoJSON nebo tabulku bodů. Až poté generuj satelitně stylizované obrázky. Žádný obrázek nesmí libovolně měnit tvar ostrovů.

Doporučená silueta (PROPOSED): hlavní ostrov má protáhlé tělo, dvě severní zátoky, západní skalnatý mys, jižní záliv kolem historického přístavu a užší jihovýchodní poloostrov. Paraland má přibližně oválný tvar se západní marinou, severním historickým městečkem a východními lesy.

## Souřadnice pro návrhovou schematickou mapu

Souřadnice X/Y níže jsou **normalizované procentní pozice uvnitř referenčního obdélníku hlavního ostrova**, NE skutečné GPS. X roste k východu, Y k jihu. Pokud je nějaký bod blízko pobřeží, přesná poloha se definitivně stanoví až podle schválené křivky břehu.

| ID | Místo / bod | X | Y | Co musí být zachováno |
|---|---|---:|---:|---|
| M-01 | Nejvyšší vrchol, pracovní 560 m | 29 | 34 | lesnatý horský masiv na západě |
| M-02 | Lyžařská a paraglidingová hora | 38 | 33 | menší přirozený spád, krátká zimní sezona |
| M-03 | Zaoblený turistický vrch | 22 | 50 | výhledy, louky a značené trasy |
| N-01 | Skalní vyhlídka nad mořem | 12 | 40 | bezpečný výhled, žádné pobídky ke skokům |
| N-02 | Krystalová jeskyně | 38 | 47 | průjezd zážitkové L1 po obvodu jeskyně |
| N-03 | Vodopád a horská řeka | 43 | 54 | nedaleko jeskyně a přehrady |
| N-04 | Přehradní jezero | 48 | 61 | vodárenské dílo a rekreační pobřeží s ochranou zdroje |
| C-01 | Hlavní město (prac. Larpington) | 67 | 76 | historické jižní centrum |
| C-02 | Historický přístav hlavního města | 68 | 87 | nábřeží, butiky a promenády |
| C-03 | Chalupecká čtvrť | 61 | 76 | část centra |
| C-04 | Kynčlova čtvrť | 66 | 71 | část centra |
| C-05 | Klimečkova čtvrť | 72 | 76 | část centra |
| C-06 | Žemličkova čtvrť | 67 | 81 | část centra |
| T-01 | Praha | 70 | 49 | český toponym v obytné nížině |
| T-02 | Čimprlichovo Hradiště | 48 | 72 | historické městečko |
| T-03 | Havlišovo Doupě | 17 | 60 | horská venkovská obec |
| T-04 | Ōru Maito (オールマイト) | 56 | 20 | japonizované severní městečko |
| T-05 | Aokawa (青川) | 73 | 24 | další návrhové severní město |
| I-01 | Zelená průmyslová zóna | 82 | 53 | továrny, zahrady, školy, restaurace |
| I-02 | Závod na zpracování mořských řas | 88 | 60 | exportní závod blízko nákladního přístavu |
| I-03 | Nákladní přístav | 94 | 64 | infrastruktura pro export |
| A-01 | Hlavní regionální letiště | 83 | 37 | východní nížina, realistická vzletová dráha |
| P-01 | Spojení na Paraland | 82 | 83 | třetí železniční linka pod vodou |

## Paraland — referenční rozložení

- **Západní pobřeží**: marina a železniční terminál L3 přicházející z Larpidie.
- **Sever**: malé staré město, zřícenina a zachovaný hrad/zámeček.
- **Jih / střed**: resorty a hotelové komplexy přístupné hlavně s rezervací, aquapark jako samostatná atrakce.
- **Východ**: lesy, menší kopce, pěší okruh a pláže v chráněných zátokách.
- **Letectví**: jen malá plocha pro omezený provoz lehkých letadel (PROPOSED), ne druhé velké mezinárodní letiště.

## Železniční síť — pevný koncept

- **L1 / Skyline Experience**: vyvýšený zážitkový okruh z města do západní přírody; fotografická zastávka u vodopádu a krátký tunel do nádherné osvětlené jeskyně, v níž trať objíždí asi tři čtvrtiny obvodu. Tematické soupravy v různých stylizacích jako zážitek, ne pouhý billboard. Název PROPOSED.
- **L2 / Heritage Connect**: povrchové elektrické vlaky se stylizací historických parních či starších souprav. Obsluhuje městečka a ekologickou průmyslovou zónu. Název PROPOSED.
- **L3 / Metro Blue**: rychlá převážně podzemní doprava po hlavním městě a pod průlivem na Paraland, přibližně tři přestupy na L2. Technicky extrémně náročná krátká podmořská výhledová galerie, nikoli nekonečný celoskleněný tunel. Název PROPOSED.
- Okružní pobřežní silnice se nesmí zaměnit za železniční okruh. Lesní odbočky, cyklotrasy a pěší stezky se napojují na vybrané vyhlídky a studánky.

## Povinná kontrola fotografie / videa

Před generací uveď:

`location_id | pohled kam | z jaké strany | roční doba | architektonické styly | blízké body | vzdálené body`.

Příklad: `N-03 | pohled severozápad | z lesní pěšiny | říjen | žádné městské mrakodrapy | N-02 poblíž | M-01 v dálce`.

Pokud se ve výsledku objeví přístav vedle nejvyšší hory či vysokohorské ledovce v nadmořské výšce 560 m, je to nekonzistentní výstup a je třeba jej upravit.

## Postup pro plán hlavního města

1. Ze souřadnic městských čtvrtí navrhni samostatnou městskou mapu, nikoliv jen přiblížený celostátní obrázek.
2. Definuj skutečná bloková území, náměstí, přístav, muzeum, čtyři správní budovy, jednu budovu parlamentu, zastávky L2/L3, školy, parky, kostel, maloobchodní zóny, půjčovny a promenádu.
3. Udělej legendu, severku, měřítko ve **skutečných jednotkách podle finální mapy** a kontrolu délky tras. Měřítko `1:10 000` lze uvést jen pokud odpovídá nakresleným vzdálenostem.
4. Vizuální mapu vytvoř přes přesný vektorový podklad, popisky přidej následně jako textové vrstvy.
