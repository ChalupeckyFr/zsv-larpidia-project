# Rozbor vyhledávání v atlasu Larpidie

**Datum:** 1. listopadu 2026  
**Rozsah:** vyhledávání v hlavním atlasu ostrova a Paralandu. Jde o analýzu aktuální implementace; atlas ani jeho vyhledávání jsem v této fázi nepřestavoval.

## 1. Kde se hledání nachází

- Veřejná stránka s atlasem je [`atlas/current/viewer/atlas.html`](../atlas/current/viewer/atlas.html), vložená do hlavní stránky v panelu `#atlas` přes `<iframe>` (`index.html:91–102`). Tlačítka v `index.html` přepínají hlavní atlas, detailní plán Larpingtonu a oba 3D modely (`site.js:47–67`). Samostatný plán Larpingtonu má vlastní vyhledávání; není to stejné vyhledávací pole jako atlas ostrovů.
- Pole je v levém postranním panelu atlasu, nad výsledky: `atlas.html:23`. Jeho nadpis je „Hledat místo“, ovšem není napojený přes `<label>` ani `aria-labelledby` na samotné pole.
- HTML, SVG mapové vrstvy, styly, JavaScript i hlavní datový registr jsou v jednom souboru `atlas.html`. Styl a responzivní pravidla jsou přibližně na řádcích 1–20; funkce hledání je na řádcích 856–862.
- Vložený registr `REG` je v `<script id="reg" type="application/json">` kolem řádku 807. Samostatný zdroj je [`atlas/current/registry/places.json`](../atlas/current/registry/places.json). Atlasový skript registr načítá z vloženého JSONu; samostatný `places.json` za běhu nenačítá. Při změně pouze jednoho z těchto souborů se zobrazení může rozejít.
- `places.json` a vložený registr v současném atlasu mají podle porovnání stejných 159 záznamů shodný obsah. Veřejné karty čtou také názvy a stavy z téhož vloženého registru.
- Samostatné vyhledávání městského plánu je v `atlas/current/capital/capital_plan_viewer.html:19` a používá vlastní vložený registr. Ten má 662 záznamů; vložená kopie a samostatné `cp_objects.json` se ve čtyřech položkách liší (`CP-B01`, `CP-PI01`, `CP-SQ02`, `CP-SQ10`). Jde o riziko správy dat, pokud by se stejným způsobem přidávala nová lokalita.

## 2. Jak hledání funguje nyní

### Shoda a filtrování

Při každém `input` hledání:

1. odstraní bílé znaky na začátku a konci a převede dotaz na malá písmena;
2. prohledá objekty, které mají souřadnici `x_km`;
3. hledá prostou podřetězcovou shodu v ID, českém názvu, anglickém názvu, japonském názvu a českém navrženém názvu;
4. ponechá nejvýše prvních 40 shod v původním pořadí registru.

Hledání neodstraňuje diakritiku, nedělí dotaz na slova a nevyhledává v typu, podtypu, ostrově/regionu, poznámkách, aliasu ani zdrojových odkazech. Navržené anglické a japonské názvy hledané nejsou, pokud současně nejsou uvedeny v polích schváleného názvu. Výsledek zobrazuje ID, přednostně český navržený název, a stav existence. Název se může ukázat jako hlavní popis, i když ještě není potvrzený.

### Kliknutí a mapa

- Výsledky jsou prvky `<div data-id="…">`, nikoli tlačítka nebo odkazy. Po kliknutí se zavolá `zoomTo(o)` a `show(o.id)` (`atlas.html:861`).
- `zoomTo` přiblíží a vycentruje SVG na souřadnice z registru; pravý panel otevře kartu vybraného místa. Detail má ještě samostatné tlačítko „Přiblížit na mapě“ (`atlas.html:837`). Tedy ano: klik na výsledek bod přiblíží i vycentruje.
- Výsledkový seznam zůstane pod polem zobrazený. Aktivní výsledek se v seznamu zvlášť neoznačí; vybrané místo zvýrazní sama mapa. Kliknutí na záznam přidává další obslužnou funkci na pravý panel `#info` znovu při každém otevření detailu (`atlas.html:838`), takže opakovaný výběr vytváří redundantní click handlery.
- Kliknutí přímo na mapový bod otevírá detail, ale hledání neprovede a samo o sobě mapu nepřibližuje. Kolečko ovládá zoom a tažení posun podle instrukce v záhlaví.

### Klávesnice, prázdný stav a přístupnost

- Vyhledávání má pouze posluchač události `input` (`atlas.html:861`). Není zde vlastní obsluha Enteru, Escape, šipek nahoru/dolů ani správa vybrané položky. Nativní prohlížeč může nabídnout vlastní ovládání typu `search`, ale stránka jej nerozšiřuje o práci s výsledky.
- Protože výsledky jsou neinteraktivní `<div>` bez `tabindex`, tlačítka nebo `role=option`, nedají se projít klávesnicí ani otevřít Enterem. Focus zůstává v poli.
- Když pole zůstane prázdné, výsledkový kontejner se vyčistí. Když dotaz nic nenajde, v kontejneru se vykreslí prázdný řetězec. Chybí text „Nic jsme nenašli“, počet výsledků i oznámení pro asistivní technologie.
- Výsledky nemají `listbox`/`option` s `aria-activedescendant`, oblast není `aria-live`; input nemá viditelný popisek při odstranění placeholderu. Jeho dostupný název tak závisí na implementaci prohlížeče a okolním kontextu.
- Výsledek nese stav existence jako barevný štítek, ale neukazuje stav jména ani polohy, přestože je karta detailu zobrazuje. Návštěvník může vybrat název „návrh jména“ dřív, než si všimne podrobnějšího stavu.

## 3. Desktop a mobil

- Desktopové rozvržení má levý panel přibližně 290 px, mapu uprostřed a pravý panel asi 335 px. Výsledky hledání jsou tedy vlevo a karta místa vpravo; při užším okně se výrazně zmenší prostor samotné mapy.
- Pod `1000px` přechází stránka do jednoho sloupce. Mapa se vykreslí jako první s výškou přibližně `58–66vh`, vlevo umístěný panel hledání následuje až pod ní a pravý panel s detailem ještě níže (`atlas.html` CSS, pravidla `@media max-width:1000px` a `620px`). Na telefonu je mapa přibližně 62vh vysoká. Uživatel tak musí sjet pod mapu, aby vůbec zadal hledání; po kliknutí může znovu rolovat k mapě i detailu.
- V mobilním režimu se nemění chování výsledků: nejde je ovládat klávesnicí, chybí prázdný stav a stav vybrané položky. Nebyl pořízen spolehlivý screenshot, takže toto hodnocení vychází ze zdrojového CSS a DOM, ne z ručního testu telefonu.

## 4. Vizuální a UX slabiny

1. **Výsledek je příliš chudý:** jen ID, jeden název a stav existence. Při podobných názvech chybí typ, oblast, ostrov a druhý řádek, který by místo odlišil.
2. **Nejistota názvu se může ztratit:** výsledek upřednostní `name_proposed.cs`, ale štítek zobrazuje pouze `exist_status`; návrhový stav názvu ani polohy není v seznamu vidět.
3. **Žádná odezva na neúspěšný dotaz:** prázdný výsledek vypadá jako rozbitá funkce. Chybí také počet nalezených míst a informace, že se zobrazuje jen prvních 40.
4. **Není normalizovaná diakritika:** například dotaz bez diakritiky nemusí najít český název s diakritikou.
5. **Myš je jediná cesta k výsledku:** seznam nelze ovládat klávesnicí a každý výsledek není samostatný ovládací prvek.
6. **Chybí vazba na kontext:** nelze hledat obecné výrazy v popisu, typu či regionu a nelze filtrovat podle ostrova nebo druhu.
7. **Mobil vyžaduje scroll:** hledání je po mapě místo toho, aby bylo dostupné u její horní hrany nebo v rozbalovacím panelu.
8. **Datová údržba se může rozejít:** atlas bere záznamy z kopie vložené do HTML; městský plán má čtyři položky odlišné od samostatného JSONu.
9. **Opakované otevírání detailu přidává handlery:** detail s každým výběrem zaregistruje nový click listener pro tlačítko zoomu.

## 5. Dva návrhy v souladu se současným atlasem

Oba návrhy zachovají SVG, paletu a současné rozvržení mapy. Nepřidávají mapovou knihovnu ani externí závislost. Názvy se mají nadále brát z jednoho registru, ne ručně přepisovat v komponentě.

### Návrh A — malé zlepšení stávajícího pole

- Doplnit skutečný `<label>` a přístupné výsledky jako tlačítka/listbox; přidat Enter, šipky, Escape a viditelný focus.
- Normalizovat diakritiku při vyhledávání, ale zachovat původní české názvy ve výsledcích.
- Přidat počet shod a jasné stavy „Začněte psát“, „Nic jsme nenašli“ a „Zobrazeno prvních 40 výsledků“.
- Zobrazovat ID, název, krátký typ a ostrov/oblast; u neověřeného jména nebo polohy použít srozumitelný malý štítek. Kliknutí nadále přiblíží/centruje mapu a otevře detail.
- Zaregistrovat obsluhu tlačítka detailu jednou, ne při každém zobrazení.
- **Rozsah:** malá změna HTML/CSS/JS atlasu a pár pomocných funkcí. **Riziko:** nízké; hlavní je správně přemapovat původní statusy na návštěvnické texty.

### Návrh B — bohatší, stále střídmý panel

- Přidat nad výsledky kompaktní panel s poli **Hledat**, **Ostrov**, **Typ** a volitelným přepínačem „zobrazit i orientační položky“.
- Výsledky zobrazit jako přehledné karty se jménem, ID, typem, ostrovem a stavem mapové polohy. Přidat tlačítko „vycentrovat“ a ponechat kliknutí na kartu pro výběr a detail.
- Zachovat klávesnici, živý počet výsledků, bezvýsledkový stav a možnost vymazat filtry. Vybraná karta by zůstala zvýrazněná i při otevřeném pravém detailu.
- Na mobilu nabídnout panel hledání jako kompaktní vysouvací spodní/vrchní zásuvku s výsledky; po výběru bodu panel zůstane zavřený a mapa zůstane viditelná, detail bude v přístupném panelu pod mapou.
- **Rozsah:** střední změna layoutu jednoho atlasového vieweru a jeho CSS/JS. **Riziko:** střední; více stavů filtrů, mobilní interakce a synchronizace výběru. SVG mapa se nemění.

## 6. Datové zdroje pro názvy a budoucí úpravy

- Pro lokality hlavního atlasu použít `atlas/current/registry/places.json` jako jediný udržovaný zdroj. Dnes se jeho obsah kopíruje do `atlas.html`; vhodný budoucí krok je při buildu vygenerovat vložený JSON z tohoto souboru nebo načítat JSON přímo přes `fetch`, pokud bude web servírován přes HTTP.
- Pole vhodná pro hledání: `id`, `name_cs`, `name_en`, `name_ja`, `name_proposed`, `type`, `subtype`, `island`, `region` a případně schválené veřejné aliasy. Interní `notes`, `bible_ref`, pseudokoordináty a `photo_guide` nejsou vhodným veřejným indexem.
- Zobrazované jméno musí respektovat `name_status`; navržený název nezobrazovat jako potvrzený. `exist_status`, `name_status` a `pos_status` jsou tři různé věci a nemají se slévat do jednoho barevného štítku.
- Pro městský plán je odpovídající zdroj `atlas/current/capital/cp_objects.json`; je třeba odstranit synchronizační odchylku čtyř záznamů vůči vloženému registru dřív, než by se stejný princip použil na městském vyhledávání.
- Zpráva v auditu veřejného obsahu uvádí, že některé současné registry obsahují pracovní názvy a produkční data. Před jejich použitím ve veřejných kartách je nejprve potřeba redakčně schválit veřejný obsah; technické propojení samo nezmění jeho kanonický status.

## 7. Rozsah a technická rizika

| Oblast | Malé úpravy | Bohatší panel |
|---|---:|---:|
| Soubory | `atlas.html` + případně generátor registru | `atlas.html`, CSS a vyhledávací JS |
| Změna mapové geometrie | žádná | žádná |
| Nové knihovny | žádné | žádné |
| Riziko duplicity dat | přetrvá, pokud zůstane ruční vložená kopie | stejné, pokud se nevyřeší zdroj registru |
| Přístupnost | výrazně lepší s malou změnou | výrazně lepší, ale víc stavů k otestování |
| Mobil | hledání zůstane pod mapou, pokud se nerozmístí panel | lze zpřístupnit jako zásuvku |

Hlavní technická rizika jsou rozcházející se kopie registrů, veřejné zobrazování návrhových názvů a stavů, dostupnost výsledků z klávesnice a zachování správného vycentrování SVG při zúženém mobilním panelu. Vzhledem k jednosouborové implementaci není důvod přidávat velkou knihovnu mapy.

## 8. Co šlo a nešlo ověřit

- Zkontroloval jsem zdrojové HTML, JS, CSS, datové registry, klíčové obsluhy událostí a mapové režimy. Přes `site.js` jsem ověřil, že hlavní atlas skutečně odpovídá routě `atlas/current/viewer/atlas.html` a samostatný plán města používá jiný soubor.
- Z kódu je doloženo, že vyhledávací výsledek volá centrování/zoom a otevírá detail.
- Snímek atlasu v prohlížeči se v dostupném prostředí nepodařilo vytvořit; report proto neobsahuje screenshot a vizuální hodnocení mobilu vychází z responzivních pravidel CSS.
- Žádná navržená změna hledání zatím nebyla implementována.
