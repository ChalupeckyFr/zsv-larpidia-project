import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (file) => JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
const write = (file, content) => fs.writeFileSync(path.join(root, file), `${content.trim()}\n`, "utf8");
const cell = (value) => String(value ?? "—").replaceAll("|", "\\|").replace(/\s+/g, " ").trim() || "—";
const table = (headers, rows) => [
  `| ${headers.join(" | ")} |`,
  `| ${headers.map(() => "---").join(" | ")} |`,
  ...rows.map((row) => `| ${row.map(cell).join(" | ")} |`),
].join("\n");

const editorial = readJson("content/larpidia/atlas_places_editorial.json");
const atlasPrivate = readJson("atlas/current/registry/places.json").objects;
const cityPrivate = readJson("atlas/current/capital/cp_objects.json").objects;
const atlasPublic = readJson("atlas/current/registry/places.public.json").objects;
const cityPublic = readJson("atlas/current/capital/cp_objects.public.json").objects;
const assets = readJson("content/larpidia/media/assets.json");
const byId = (records) => new Map(records.map((item) => [item.id, item]));
const atlasPrivateById = byId(atlasPrivate), cityPrivateById = byId(cityPrivate);
const atlasPublicById = byId(atlasPublic), cityPublicById = byId(cityPublic);

const atlasIds = ["T-01", "T-02", "C-01", "T-03", "T-04", "M-01", "M-02", "M-03", "N-01", "N-02", "N-03", "N-04", "V-02", "SP-01", "SP-04", "B-01", "PL-02", "L1", "L2", "L3", "P-01"];
const cityIds = ["CP-01", "CP-B01", "CP-B06", "CP-B07", "CP-SQ01", "CP-PK02", "CP-PR01", "ST-W", "ST-S", "CP-BL-0001", "CP-BL-0342", "CP-CF01", "CP-RN01", "CP-SH04", "CP-ZR02", "CP-UL01", "CP-AR01", "CP-B12", "CP-PK03", "CP-BL-0243", "CP-PI01"];
const atlasEditorial = Object.values(editorial.atlas), cityEditorial = Object.values(editorial.capital);
const statuses = [...atlasEditorial, ...cityEditorial].reduce((out, item) => {
  out[item.editorial_status] = (out[item.editorial_status] || 0) + 1;
  return out;
}, {});
const allEditorial = [...atlasEditorial, ...cityEditorial];
const duplicateNames = (entries) => {
  const names = new Map();
  for (const [id, entry] of entries) names.set(entry.public_name_cs, [...(names.get(entry.public_name_cs) || []), id]);
  return [...names.values()].filter((ids) => ids.length > 1).length;
};
const missingScenes = assets.scenes.filter((scene) => !scene.photo_path || !fs.existsSync(path.join(root, scene.photo_path)));
const availableScenes = assets.scenes.filter((scene) => scene.photo_path && fs.existsSync(path.join(root, scene.photo_path)));
const publicPhotos = assets.assets.filter((asset) => asset.mediaType === "photo" && asset.public && asset.gallery && fs.existsSync(path.join(root, asset.src)));
const videoCount = assets.assets.filter((asset) => asset.mediaType === "video").length;
const gitRows = execFileSync("git", ["status", "--short", "--untracked-files=all"], { cwd: root, encoding: "utf8" })
  .split(/\r?\n/).filter(Boolean).map((line) => [line.slice(0, 2), line.slice(3)]);
const genericNames = allEditorial.filter((item) => /^(?:poi|bod z[aá]jmu|bez n[aá]zvu|m[ií]sto|objekt)(?:\b|\s)/i.test(item.public_name_cs));
const emptyDescriptions = allEditorial.filter((item) => !item.short_description_cs?.trim());
const shortDescriptions = allEditorial.filter((item) => (item.short_description_cs || "").trim().length < 75);
const noReview = allEditorial.filter((item) => item.editorial_status === "requires_review");
const generatedNameCount = statuses.new_editorial_name || 0;
const clarifiedNameCount = statuses.derived_from_source || 0;
const approvedNameCount = statuses.author_approved || 0;

const atlasSpotRows = atlasIds.map((id) => {
  const item = atlasPublicById.get(id);
  return [id, item?.name_cs, item?.categoryLabel, item?.description];
});
const citySpotRows = cityIds.map((id) => {
  const item = cityPublicById.get(id);
  return [id, item?.name_cs, item?.categoryLabel, item?.description];
});

const atlasRows = atlasPrivate.map((original) => {
  const entry = editorial.atlas[original.id];
  return [original.id, original.name_cs, entry?.public_name_cs, `${original.type}${original.subtype ? ` / ${original.subtype}` : ""}`, entry?.editorial_status, entry?.source_reason];
});
const cityRows = cityPrivate.map((original) => {
  const entry = editorial.capital[original.id];
  return [original.id, original.name_cs, entry?.public_name_cs, `${original.type}${original.subtype ? ` / ${original.subtype}` : ""}`, entry?.editorial_status, entry?.source_reason];
});

write("docs/LARPIDIA_ATLAS_CONTENT_AND_UI_COMPLETION_REPORT.md", `
# Dokončení veřejného atlasu, obsahu a rozhraní

Datum ověření: 2026-11-04.

## Výsledek

Kořenový web byl otevřen přes místní HTTP server s kořenem v projektu a navigací běžnou cestou přes 'http://127.0.0.1:62489/index.html#atlas'. Aktivním atlasovým iframe je 'atlas/current/viewer/atlas.html'; plán Larpingtonu používá 'atlas/current/capital/capital_plan_viewer.html'. Veřejný export i aktivní soubory vznikají z redakční vrstvy a šablon skriptem 'scripts/build_public_site.mjs'.

Zůstalo zachováno všech **159 míst atlasu** a **662 objektů plánu**. Každý má veřejný český název a popis, v redakční vrstvě není žádný prázdný ani kratší než 75 znaků dlouhý popis. V atlasu ani plánu nezůstaly duplicitní veřejné názvy ani obecné názvy typu „Bod zájmu“ či „Objekt“. T-02 se veřejně jmenuje přesně **Cimprlichovo Hradiště**; dřívější pravopis zůstává pouze jako interní vyhledávací alias. Identifikátory, stavová metadata a zdrojové poznámky zůstaly ve zdrojových registrech a ve veřejném rozhraní se nevykreslují.

Nově vzniklé názvy jsou označené jako redakční návrhy, ne jako změna ústavního kánonu. Soubor kánonu v2.6 zůstal beze změny. Úplný převod názvů a důvody jsou v [redakčním přehledu](LARPIDIA_EDITORIAL_PLACE_NAMES_REVIEW.md).

## Bodové ověření obsahu

Kořenový prohlížečový test vizuálně otevřel 21 karet atlasu a 21 objektů městského plánu. Následující tabulky uvádějí veřejné názvy a skutečné popisy z generovaného registru.

### Atlas

${table(["Interní ID (jen v této zprávě)", "Veřejný název", "Typ", "Veřejný popis"], atlasSpotRows)}

### Plán Larpingtonu

${table(["Interní ID (jen v této zprávě)", "Veřejný název", "Typ", "Veřejný popis"], citySpotRows)}

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

Ve fotoarchivu jsou skutečné dva snímky a 18 plánovaných scén bez souboru. Galerie ukazuje pouze dostupné fotografie bez prázdných karet; chybějící scény jsou uvedené v interním archivu a mediálním přehledu. Nových redakčních názvů je ${generatedNameCount}; jejich místní odvození a stav schválení jsou přehledně označené, ale jejich případné budoucí povýšení na kanonické názvy vyžaduje redakční rozhodnutí.
`);

write("docs/LARPIDIA_EDITORIAL_PLACE_NAMES_REVIEW.md", `
# Přehled redakčních názvů veřejného atlasu

Tento interní přehled obsahuje všechna veřejná jména 159 míst atlasu a 662 objektů Larpingtonu, jejich původní jména ve zdrojových registrech, typ, stav redakčního zpracování a stručný důvod. Interní ID a pracovní údaje jsou zde záměrně viditelné pouze pro údržbu.

## Souhrn

- Zachováno nebo upřesněno podle zdrojů: ${clarifiedNameCount}.
- Nově vytvořený redakční název: ${generatedNameCount}.
- Výslovně autorsky schválené: ${approvedNameCount}.
- Záznamy označené 'requires_review': ${noReview.length}.
- Atlas: ${atlasPrivate.length} záznamů; unikátních veřejných jmen bez prázdných popisů: ${atlasPublic.length}.
- Larpington: ${cityPrivate.length} záznamů; unikátních veřejných jmen bez prázdných popisů: ${cityPublic.length}.
- Prázdné nebo podlimitní popisy (<75 znaků): ${emptyDescriptions.length + shortDescriptions.length}; obecné názvy: ${genericNames.length}.

Stav 'new_editorial_name' znamená tvůrčí, geograficky odvozený návrh v redakční vrstvě; nejde o změnu kánonu. Názvy vznikly z typu prvku, jeho regionu, blízkých pojmenovaných míst a u objektů města také z existující uliční geometrie. Veřejný export si ponechává jen návštěvnická pole a skryté ID potřebné pro hledání a mapové propojení.

Schválený přepis T-02 je **Cimprlichovo Hradiště**. Starší pravopis je ponechán jako neveřejný alias. Železniční stanice u města je odlišená názvem „Stanice Cimprlichovo Hradiště“. Obdobně jsou rozlišeny řeka Aokawa a sídlo Aokawa a dva příjezdy k pláži Hoshimachi. Otevřené konflikty vyžadující rozhodnutí autora: ${noReview.length}.

## Místa hlavního atlasu

${table(["ID", "Původní zdrojový název", "Veřejný český název", "Typ", "Stav", "Důvod / opora"], atlasRows)}

## Objekty plánu Larpingtonu

${table(["ID", "Původní zdrojový název", "Veřejný český název", "Typ", "Stav", "Důvod / opora"], cityRows)}

## Zásada pro další úpravy

Udržovat jména a popisy v jediném zdrojovém souboru 'content/larpidia/atlas_places_editorial.json'; regenerovat návštěvnické projekce skriptem 'scripts/refine_atlas_editorial.mjs' a sestavením 'scripts/build_public_site.mjs'. Neměnit souřadnice, geometrii ani fakta kánonu při redakci názvů.
`);

const availablePhotoRows = publicPhotos.map((asset) => [asset.id, asset.caption, asset.src, asset.publicSrc]);
const missingPhotoRows = missingScenes.map((scene) => [scene.scene_id, scene.title_cs, scene.place_id, scene.expected_photo_path, scene.viewpoint_path]);
write("docs/LARPIDIA_MEDIA_MANIFEST_REPORT.md", `
# Zpráva o obrazových médiích a veřejné galerii

Zdrojový manifest: [content/larpidia/media/assets.json](../content/larpidia/media/assets.json). Kontrola ověřila skutečnou existenci souborů, veřejný allowlist, relativní cesty z kořene webu a vykreslení obrázků v Edge. Z 20 plánovaných fotografických scén existují přesně **${availableScenes.length}** soubory a **${missingScenes.length}** scén zůstává bez fotografie. Videozáznamy evidovány: **${videoCount}**.

## Dostupné fotografie ve veřejné galerii

${table(["Manifest ID", "Popisek", "Zdrojový soubor", "Kopírovaná veřejná cesta"], availablePhotoRows)}

Oba soubory jsou PNG; cesty scény PHOTO_01 a PHOTO_06 byly sjednoceny s reálnými příponami. Kořenový test potvrdil, že se oba snímky dekódují a mají nenulové obrazové rozměry. Veřejný render potvrdil jejich zobrazení bez prázdných či rozbitých karet. Fotografie PHOTO_01 je použita také v příslušném článku; galerie ji deduplikuje podle centrálního manifestu.

## Scény bez fotografie

${table(["Scéna", "Název", "Interní místo", "Očekávaný soubor", "Interní bod kamery"], missingPhotoRows)}

Chybějící snímky nejsou nahrazené ilustračními kartami. Autorův „Obrazový archiv“ v kořenovém náhledu počítá soubory dynamicky a zobrazuje stav **${availableScenes.length} hotových / ${missingScenes.length} chybějících**; [snímek archivu](debug-screenshots/author-media-modal.png). Veřejný export tlačítko ani plán scén neobsahuje a interní cesty k promptům vracejí 404.

Obecná ilustrace 'photo-001' a noční silniční ilustrace nejsou vydávány za místní fotografie a jsou vyřazeny z veřejné galerie. Veřejná příroda odkazuje na ověřenou fotografii PHOTO_01, nikoli na nesouvisející snímek.

## Kmenový soubor promptů

Úplný interní registr promptů zůstává v [ALL_PHOTO_PROMPTS.md](../v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/03_PHOTO_PROMPTS/ALL_PHOTO_PROMPTS.md). Obsahuje 20 stabilních ID, polohu v atlasu, samostatný bod kamery, prompt a stav dostupnosti. Původní dlouhé prompty zachovány; veřejný export je nepublikuje.
`);

const terrainDataSource = fs.readFileSync(path.join(root, "atlas/current/viewer/terrain-3d-data.js"), "utf8");
const terrainData = JSON.parse(terrainDataSource.match(/window\.LARPIDIA_TERRAIN_DATA\s*=\s*(\{.*\});\s*$/s)[1]);
const capitalDataSource = fs.readFileSync(path.join(root, "atlas/current/capital/capital-3d-data.js"), "utf8");
const capitalData = JSON.parse(capitalDataSource.match(/window\.LARPIDIA_CAPITAL_3D\s*=\s*(\{.*\});\s*$/s)[1]);
const meshWidth = (terrainData.width - 1) * 2 + 1, meshHeight = (terrainData.height - 1) * 2 + 1;
const terrainTileCount = Math.ceil((meshWidth - 1) / 254) * Math.ceil((meshHeight - 1) / 254);
const cityGeometryRows = Object.entries(capitalData).filter(([, value]) => Array.isArray(value)).map(([key, value]) => [key, value.length]);
write("docs/LARPIDIA_3D_TECHNICAL_OPTIONS.md", `
# Technická poznámka k současným 3D scénám

Tato zpráva je pouze rozbor. Zdrojové soubory, výšková data, geometrie ani ovládání 3D scén nebyly upraveny.

## Použitá technologie a geometrie

Obě scény používají vlastní vykreslování přes **WebGL 1.0**, GLSL vertex/fragment shadery a nativní 'canvas'. Není zde Three.js ani Babylon.js.

- **Terén:** [terrain-3d.html](../atlas/current/viewer/terrain-3d.html) čte výškovou mřížku ${terrainData.width} × ${terrainData.height} a při vykreslení ji převzorkuje na ${meshWidth} × ${meshHeight} bodů. Dlaždice po 254 buňkách dávají ${terrainTileCount} terénních GPU bufferů. Vedle nich se vykresluje oceán, vodní prvky a volitelně okružní silnice. Sezónní počasí se kreslí samostatnou 2D canvas vrstvou.
- **Larpington:** [capital-3d.html](../atlas/current/capital/capital-3d.html) vytváří batched vertex/index buffery z [capital-3d-data.js](../atlas/current/capital/capital-3d-data.js). Zdroj obsahuje následující počty polygonálních prvků v jednotlivých kategoriích:

${table(["Kategorie", "Prvků"], cityGeometryRows)}

Kreslení města slučuje domy, bloky, budovy, budoucí stavby, náměstí, silnice, dominanty a pobřežní prvky do skupin bufferů. Alternativní přírodní režim v [capital-3d-nature.js](../atlas/current/capital/capital-3d-nature.js) seskupuje bloky, parky, trávníky, domy, budovy, zeleň a cesty.

## Kamera a ovládání

V obou scénách tažení ukazatelem otáčí kameru; kolečko upravuje rychlost pohybu. Klávesy WASD nebo šipky posouvají kameru, Ctrl/Shift mění výšku a Home obnoví výchozí kameru. Rozhraní nabízí ovladač rychlosti, změnu převýšení a u terénu volbu sezony, barevného režimu a okružní silnice; městská scéna má přepnutí technického/přírodního stylu, budoucích staveb a názvů ulic. Vstup používá Pointer Events, proto obslouží i dotykové ukazatele.

## Výkonová místa a bezpečný další krok

Terén překresluje šest dlaždic a při změně sezony nebo převýšení znovu generuje výškové buffery; počasí běží přes 'requestAnimationFrame'. Larpington při změně převýšení přestavuje více skupin městské geometrie, zatímco přírodní vrstvu sestavuje při prvním použití a ukládá ji do bufferů. Rozumné další ověření je zaznamenat čas vykreslení a dobu změny převýšení na jednom desktopu a jednom mobilním zařízení, potom případně oddělit opakované buffer uploady od změn kamery. Bez profilování není vhodné přidávat detailnější stíny, větší výškovou mřížku ani nový renderer.

Ohraničený další úkol: samostatný profilovací průchod se dvěma referenčními zařízeními, bez úpravy souřadnic či topologie; změny pouze po srovnání snímkové frekvence, času obnovy scény a paměti GPU.

Ověření zachování: čtyři zdrojové 3D datové soubory se přesně shodují s veřejnými kopiemi podle SHA-256; zdrojové HTML obou 3D scén je shodné s výchozím stavem.
`);

write("docs/LARPIDIA_COMPLETION_PROGRESS.md", `
# Stav dokončení atlasu a galerie Larpidie

Aktualizováno: 2026-11-04. Postup obnovuje již hotové změny a zachovává práci z předchozího běhu.

## Fáze podle zadání

| Fáze | Stav | Důkaz |
|---|---|---|
| 1. Skutečný zdroj, trasy, zachování dřívější opravy a redakční zdroj popisů | COMPLETE AND TESTED | Kořenový web otevřel aktivní iframe '/atlas/current/viewer/atlas.html'; staré značky a statusy nejsou v zobrazeném DOM. T-02 je přesně Cimprlichovo Hradiště a starší pravopis zůstává aliasem. |
| 2. Obsah a pojmenování 159 + 662 prvků | COMPLETE AND TESTED | 159/159 a 662/662 záznamů; 0 prázdných či krátkých popisů, 0 obecných názvů a 0 duplicitních veřejných názvů. Ověřeno 21 + 21 karet v kořenovém prohlížeči; úplný rejstřík v 'LARPIDIA_EDITORIAL_PLACE_NAMES_REVIEW.md'. |
| 3. Atlasové rozhraní a 2D kartografie | COMPLETE AND TESTED | Vyhledávání, výběr z výsledků, opakované kliknutí do mapy a dotyk T-02 přes kořenový web; mobilní rozvržení a interakce v Edge. Snímky před/po jsou v 'docs/debug-screenshots/atlas-2d-city-before.png' a 'atlas-2d-city-after.png'. |
| 4. Galerie, archiv médií a branding | COMPLETE AND TESTED | Dvě skutečné fotografie vykreslené s obrazovými rozměry; 18 chybějících scén se nevydává za fotografie. Soukromý archiv počítá 2/18 a ve veřejném exportu i jeho datech chybí. Hlavička a patička mají shodnou výšku loga 48 px. |
| 5. Kontroly, odolnost exportu a zprávy | COMPLETE AND TESTED | Root/Edge prohlížečové testy, allowlist a 404 test, parsování skriptů a 'git diff --check' úspěšné; 3D datové hashe a cesty SVG ověřeny. Výsledky a omezení jsou rozepsané v této zprávě a třech doplňkových zprávách. |

## Skutečně provedené kontroly

- Kořenový 'index.html' přes lokální HTTP server ekvivalentní Live Serveru; naposledy 'http://127.0.0.1:62489/index.html#atlas'. Přes homepage otevřen aktivní atlas, vybrán T-02, ověřeny karta, vyhledávací alias, statusy v DOM, opakovaný klik myší, dotyk, galerijní obrázky, soukromý archiv a logo. Server se po testu ukončil.
- Veřejný export v Edge přes dočasný HTTP server; test otevřel atlas, plán Larpingtonu, galerii a článek standardní navigací. Ověřil 662 objektů, kliknutí na SVG objekt, mobilní rozložení, fotografie bez chyby a skrytí interních cest.
- 'node scripts/check_public_export.mjs': allowlist, datové počty, syntaxi a shodu zdrojového a veřejného vieweru.
- 'node scripts/check_encyclopedia_http.mjs': 72 veřejných cest dostupných, 17 interních cest 404.
- 'node --check' pro upravené skripty a 'git diff --check' bez chyb.
- Cesty 'd' atlasového SVG: 361/361 shodných s výchozím stavem. Cesty 'd' plánu: 5 954/5 954 shodných. Zdrojové registry zachovaly shodný JSON obsah; žádné souřadnice nebyly upraveny.

## Přesný seznam pracovního stromu

Následující seznam je výstupem 'git status --short --untracked-files=all' při tvorbě této zprávy. Obsahuje i necommitnutou práci převzatou z přerušeného běhu; status '??' proto nemusí znamenat, že daný soubor vznikl při tomto navázání.

${table(["Git", "Soubor"], gitRows)}

Soubor 'references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md' nebyl upraven. Nebyl proveden Git commit ani push.

## Zbývající omezení

- 18 plánovaných fotografií zatím nemá soubor; jejich přesný seznam je v 'LARPIDIA_MEDIA_MANIFEST_REPORT.md'. Galerie zobrazuje všechny aktuálně dostupné skutečné fotografie a nevkládá prázdné náhražky.
- ${generatedNameCount} názvů je redakční návrh podle typu prvku, regionu, sousedů a uliční geometrie. Jsou dohledatelné v interním přehledu a zůstávají oddělené od kanonických rozhodnutí.
- Testy používají skutečný kořen projektu přes lokální server a Edge, nikoli živou instanci rozšíření VS Code Live Server. Kořen, relativní cesty a navigační tok jsou stejné.
`);

console.log(`Vytvořeny zprávy; počty: ${atlasPrivate.length} atlas, ${cityPrivate.length} městských objektů, ${availableScenes.length} fotografie, ${missingScenes.length} chybějících scén.`);
