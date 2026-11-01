# Zadání pro Codex: doladění encyklopedie, audit „construction site“ a průzkum vyhledávání v atlasu

Nová encyklopedie Larpidie vizuálně dopadla velmi dobře. **Zachovej současnou typografii, barevnou paletu, karty, rozložení článků, vyhledávání v encyklopedii a základní navigaci.** Nedělej nový design ani kompletní refaktor. Potřebuju opravit několik jasných nedostatků, potom systematicky dohledat všechny veřejně viditelné interní poznámky a připravit podklady pro další redakční rozhodnutí.

**Rozděl práci do tří částí A/B/C.** Část A skutečně implementuj. V části B problematické formulace a nejasná fakta především **zmapuj, nevymýšlej jejich řešení**. V části C analyzuj vyhledávání atlasu, ale jeho větší přestavbu zatím neprováděj.

## A — Okamžité opravy veřejného rozhraní

### A1. Úvodní slogan

Na hlavní stránce encyklopedie je nadpis „Průvodce pro každou prezentaci.“ To je matoucí: web není jen pomůcka k prezentaci, ale veřejný průvodce fiktivní zemí pro každého návštěvníka.

Nahraď ho například tímto textem, se zachováním současného působivého dvouřádkového typografického stylu (včetně kurzivy, pokud sedí):

**„Objevte Larpidii. / Ostrovní svět plný příběhů.“**

Uprav i okolní popisek tak, aby přirozeně zval k objevování historie, přírody, měst, kultury a fungování státu. Vymaž z veřejného textu technické věty typu „Opakované údaje se načítají ze společných projektových dat“ a výrazy, které návštěvníkům neříkají nic o Larpidii. Zachovej přirozené a nenápadné sdělení, že jde o **fiktivní** svět/školní projekt, ale neopakuj tuto nálepku v každém odstavci.

Z veřejného úvodu také odstraň prominentní vývojářský odkaz „Jak upravit obsah“, pokud míří na interní návod pro editory. Návod `CANON_EDITING_GUIDE.md` zůstane v projektu, ale není hlavním obsahem pro běžného návštěvníka. Pokud je třeba nějaká uživatelsky přístupná informační stránka, odděl ji od editorových instrukcí.

### A2. Čtyři úvodní statistické karty

Nynější řada „Obyvatel / Hlavní ostrov / Druhý ostrov / Spoluvládci“ není dobrým prvním seznámením s výjimečností země. Rozlohy 175 a 14 bez jednotky jsou navíc nejasné. Nahraď **jen tuto úvodní řadu** čtyřmi vizuálně vyváženými údaji:

1. **Obyvatelstvo — 32 000**.
2. **Politický systém — Ústavní spoluvláda** (čtyři rovnocenní spoluvládci a přímá demokracie; nepoužívej chybně „republika“ ani „parlament“). Je-li místo, doplň krátké vysvětlení, jinak proklik na odpovídající článek.
3. **Pracovní týden — 24 h** (běžný režim; nepřetržité služby mají směny).
4. **Roční turistické útraty — 600 mil. Kč** (model: 40 000 návštěv × 15 000 Kč). Pozor: jde o tržby v turistické ekonomice, **nikoli příjem státního rozpočtu**. Pokud potřebuješ stručný popisek, napiš „Útraty návštěvníků / rok“.

Hodnoty načítej z již zavedeného centralizovaného zdroje faktů, nebo je z něj odvozuj; nevytvářej druhé ručně udržované kopie. Pokud datový model neumí odvozené údaje, přidej jednoduché odvození. Udrž čistou typografii a responsivní chování i s delším textem „Ústavní spoluvláda“. Samotnou rozlohu ostrovů samozřejmě ponech v příslušných článcích.

### A3. Nečitelná světlá tlačítka

Na světlém pozadí se například tlačítko „Přejít do galerie“ zobrazuje téměř bílým textem bez dostatečného kontrastu. Oprav kontrast **primárního i sekundárního** tlačítka a všech stavů: default, hover, focus, active, disabled. U aktivních tlačítek dodrž alespoň WCAG AA kontrast pro běžný text (4,5 : 1), viditelný focus pro klávesnici; u skutečně deaktivovaných prvků musí být stav srozumitelný a nelze je zaměnit za neviditelné funkční odkazy.

Zkontroluj skutečný cíl „Přejít do galerie“: pokud existuje a má být aktivní, oprav barvy a funkčnost. Pokud cíl neexistuje, nedělej falešně klikatelné tlačítko; napiš to do auditu.

### A4. Drobné copywritingové úniky

Automaticky můžeš opravit **zcela jasné technické texty** v navigaci a úvodu, například meta-věty o tom, jak jsou načítaná data, pracovní štítky určené editorům, redundantní „VEŘEJNÝ PRŮVODCE“ apod. Nevypouštěj ale skutečná fakta o rozestavěné dopravě nebo probíhajících historických procesech. Nezkracuj rozsáhlé články, neměň jejich fakta a neodstraňuj jejich podstatu.

## B — ÚPLNÝ AUDIT „CONSTRUCTION SITE“ VEŘEJNÉHO WEBU

Pod „construction site“ myslím případy, kdy návštěvník vidí **interní proces tvorby projektu**: „není potvrzeno“, „o tom ještě nevíme“, „autor musí rozhodnout“, „hranice rozumu“, „pracovní kánon“, „technická implementace“, „zatím jsme to nevymysleli“, „TODO“, „placeholder“ a podobně. To ničí dojem hotové a přirozeně napsané encyklopedie.

**Nezaměňuj to s reálným stavem fikční země:** například „podmořská L3 je ve výstavbě“, „probíhá soudní řízení“, „obnova pobřeží pokračuje“ mohou být platnými příběhovými fakty. Ty do auditu nezařazuj jako chybu jen proto, že obsahují slovo „výstavba“ nebo „zatím“.

### Kde a jak hledat

1. Projdi **všechny veřejné routy**, zejména úvod, všechny kategorie a všechny články encyklopedie, klikatelné podstránky, atlas, 3D město, galerie, Paraland a další veřejné stránky. Zahrň i mobilní varianty a obsah zobrazovaný po interakci (rozbalení, vyhledávání, prázdné výsledky apod.), pokud je to v tvém prostředí možné.
2. Projdi zdrojové obsahové soubory (Markdown/JSON) i textové řetězce v komponentách, protože část textů může být natvrdo zapsaná v UI. Hledej i varianty bez diakritiky.
3. Zachyť konkrétní nadpis **„Hranice rozumu“**, pokud existuje, a všechny podobné nadpisy, které vysvětlují *limity tvůrců* místo Larpidie.
4. Zkontroluj i věcné rozpory a neúplné údaje proti `references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md`, včetně starších verzí World Bible, které mohou obsahovat překonaná pravidla.
5. Neoznamuj „prošel jsem celý web“, pokud jsi nemohl skutečně otevřít všechny dynamické cesty. V takovém případě v reportu přiznej nepokrytá místa.

### Vytvoř přesně tento hlavní soubor

`docs/LARPIDIA_PUBLIC_CONTENT_AUDIT.md`

Musí obsahovat:

**1. Shrnutí:** počet nalezených výskytů, počet unikátních problémů, počet prověřených URL/rout, co bylo a nebylo možné prohlédnout, rozdělení podle závažnosti.

**2. Úplný inventář všech výskytů** (ne jen 10 vybraných příkladů). Každý záznam musí mít:
- unikátní ID např. `CS-001`;
- veřejnou URL či routu a konkrétní nadpis/sekci;
- cestu ke zdrojovému souboru a pokud lze i řádky;
- přesný krátký výňatek skutečně viditelného textu;
- zařazení `TECHNICKÝ ÚNIK / EDITORSKÁ POZNÁMKA / NEPOTVRZENÉ FAKTUM / ROZPOR S KÁNONEM / CHYBĚJÍCÍ OBSAH / UX-PROBLÉM / DALŠÍ`;
- závažnost `kritická / střední / drobná`;
- zda jde o duplicitu už evidovaného problému;
- odkaz na relevantní část kánonu, je-li doložitelná;
- navržený veřejně přirozený text nebo vhodné řešení;
- označení doporučeného postupu `JASNÉ — LZE OPRAVIT / VYŽADUJE ROZHODNUTÍ AUTORA / POTŘEBUJE DALŠÍ DATA`.

**3. Sloučený seznam REDAKČNÍCH ROZHODNUTÍ PRO AUTORA.** Seskup duplicitní výskyty do tematických celků, např. historie, geografie, fungování státu, školy, Paraland, doprava, ekonomika, nevysvětlené názvy. Každý unikátní dotaz dostane ID `R-01`, `R-02` atd. U každého:
- co už skutečně víme z kánonu;
- co přesně chybí a proč to potřebujeme;
- tvůj rozumný **konkrétní návrh doplnění ve stylu Larpidie**;
- jednu až tři alternativy, pokud má volba reálné důsledky;
- seznam souvisejících `CS-...` výskytů;
- prioritu a doporučený dopad na web/atlas/fotky.

**4. Jisté automaticky opravitelné věci vs. skutečné otázky.** U maličkostí doporuč rovnou redakční úpravu místo zbytečné otázky. Nezvyšuj uměle počet dotazů. U velkých rozhodnutí nic nepotvrzuj za autory.

**5. Návrh pořadí nápravy** ve třech skupinách: rychlé opravy / nutné společné rozhodnutí / budoucí rozšíření.

Důležité: Nedomýšlej **nová tvrzení jako schválený kánon**. Můžeš navrhovat uvěřitelná doplnění a přirozené formulace, ale jasně je označ jako pracovní návrhy v interním souboru. Neveřejné otázky a poznámky se nesmějí objevit na veřejných stránkách. Pokud článek zatím neobsahuje dost ověřených fikčních informací, můžeš doporučit stručný, věcně správný text nebo skrytí prázdné sekce — ne vymyšlené datum či výsledek.

**V této fázi neopravuj automaticky všechny problematické články** a neschvaluj nové události. Nejprve potřebuji audit projít s ChatGPT, rozhodnout chybějící věci a potom ti dodat soubor schválených oprav. Bezpečné kosmetické úpravy z části A proveď hned.

## C — ANALÝZA VYHLEDÁVÁNÍ V ATLASU, ZATÍM BEZ PŘESTAVBY

Chci později vylepšit vyhledávání v interaktivním atlasu, ale momentálně ti nedávám dostatečně přesný vizuální návrh. Proto zatím vyhledej skutečnou implementaci a vytvoř:

`docs/LARPIDIA_ATLAS_SEARCH_REVIEW.md`

Uveď:
1. kde přesně se vyhledávání nachází (routy, komponenty, styly, datové zdroje);
2. jak funguje nyní: co hledá, jak filtruje, jak vypadají výsledky, co se stane po kliknutí, zda umí přiblížit a vycentrovat bod na mapě;
3. nynější chování na desktopu a mobilu; klávesnice, Escape, Enter, šipky, focus, bezvýsledkový stav;
4. konkrétní vizuální a UX slabiny včetně screenshotů, pokud nástroj umožňuje screenshoty pořídit;
5. **dva konkrétní návrhy** modernějšího, elegantního hledání, které vizuálně zapadnou do stávajícího atlasu; jeden jen s drobnými úpravami, druhý s bohatším panelem výsledků;
6. které existující datové soubory lze využít, aby názvy lokalit zůstaly shodné s atlasem;
7. odhad rozsahu změn a případná technická rizika.

Nevyměňuj knihovnu mapy, nepřidávej těžké závislosti a atlasové vyhledávání zatím zásadně nepřestavuj. Chci s ChatGPT nejdřív vybrat správné řešení.

## D — Omezení, ověření a výstup

- Zachovej existující vzhled, strukturu a fungování encyklopedie, atlasu, 3D Larpingtonu i galerií mimo výslovně požadované malé opravy.
- Nenahrávej automaticky obrázky, nepřepisuj kánon v2.6 ani centrální fakta podle nepotvrzených dohadů.
- Oprav UI z části A přímo v kódu; audit z části B a rozbor atlasu z části C ulož jako **soubory**. Nechci jen shrnutí do chatu.
- Spusť dostupné testy/build. Ověř funkční odkazy, čitelnost tlačítek a responzivitu; uveď, co šlo a nešlo otestovat.
- Nevytvářej Git commit ani push, pokud to výslovně nepožádám.
- Na konci napiš stručně: změněné soubory, provedené vizuální opravy, počet auditních nálezů a přesné cesty k oběma reportům.

**Důležité pořadí:** nejprve malá vizuální náprava; pak úplný audit veřejných textů; pak technický rozbor atlasového vyhledávání. Při auditu raději najdi více skutečných výskytů a sluč je do méně dobrých otázek pro autora než několik problémů zamlč.
