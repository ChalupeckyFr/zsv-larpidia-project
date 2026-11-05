import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { atlasInfoClickRenderer, atlasShowRenderer, cityShowRenderer } from "./public_viewer_renderers.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "public");
const read = (relative) => fs.readFileSync(path.join(root, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));
const writeSource = (relative, data) => {
  const target = path.join(root, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, data);
};
const write = (relative, data) => {
  const target = path.join(output, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, data);
};
const copy = (relative, destination = relative) => write(destination, fs.readFileSync(path.join(root, relative)));

const typeLabels = {
  peak: "Horský vrchol", mountain: "Hora", lake: "Jezero", reservoir: "Vodní nádrž",
  river: "Řeka", waterfall: "Vodopád", stream: "Potok", spring: "Pramen",
  beach: "Pláž", coast: "Pobřeží", cape: "Mys", peninsula: "Poloostrov",
  settlement: "Sídlo", town: "Město", village: "Obec", industrial: "Průmyslová oblast",
  rail_line: "Železniční trať", railway: "Železniční trať", rail_station: "Železniční stanice",
  station: "Stanice", road: "Silnice", highway: "Silnice", cycleway: "Cyklotrasa",
  trail: "Stezka", port: "Přístav", airport: "Letiště", viewpoint: "Vyhlídka",
  other_line: "Dopravní trasa", poi: "Místo zájmu", building: "Budova", house: "Dům",
  block: "Městský blok", street: "Ulice", square: "Veřejné prostranství", park: "Park",
  pier: "Molo", district: "Městská čtvrť", ferry: "Lodní spojení", default: "Místo",
};
const editorial = readJson("content/larpidia/atlas_places_editorial.json");
const regionLabels = {
  west_northwest: "západní horská oblast", central_west: "západní část ostrova",
  central_lowland: "centrální nížina", south_southeast: "jižní část ostrova",
  southeast_offshore: "Paraland a okolní moře", north: "severní část ostrova",
  east_northeast: "východní část ostrova", east: "východní část ostrova",
  west: "západní část ostrova", south: "jižní část ostrova", center: "střed ostrova",
};
const islandLabels = { main: "hlavní ostrov", para: "Paraland", "main+para": "oba ostrovy" };
const kindOf = (record) => {
  const raw = String(record.type || record.subtype || "").toLowerCase();
  if (raw.includes("rail") || raw === "l1" || raw === "l2" || raw === "l3") return "rail_line";
  if (raw.includes("station")) return "station";
  if (raw.includes("cycle")) return "cycleway";
  if (raw.includes("trail")) return "trail";
  if (raw.includes("river")) return "river";
  if (raw.includes("stream")) return "stream";
  if (raw.includes("peak")) return "peak";
  if (raw.includes("waterfall")) return "waterfall";
  if (raw.includes("reservoir")) return "reservoir";
  if (raw.includes("lake")) return "lake";
  if (raw.includes("port") || raw.includes("harbour")) return "port";
  if (raw.includes("airport")) return "airport";
  if (raw.includes("square")) return "square";
  if (raw.includes("park")) return "park";
  if (raw.includes("pier")) return "pier";
  if (raw.includes("street")) return "street";
  if (raw.includes("block")) return "block";
  if (raw.includes("house")) return "house";
  if (raw.includes("building") || raw.includes("town_hall")) return "building";
  return typeLabels[raw] ? raw : "default";
};
const regionLabel = (value) => regionLabels[String(value || "").toLowerCase()] || "ostrovní krajina";
const editorialFor = (record, capital = false) => (capital ? editorial.capital : editorial.atlas)?.[record.id];
const publicPlaceName = (record, kind, capital = false) => {
  const entry = editorialFor(record, capital);
  if (!entry?.public_name_cs) throw new Error(`Missing editorial public name for ${capital ? "city" : "atlas"} record ${record.id}.`);
  return entry.public_name_cs;
};
const cleanSearchTerm = (value) => String(value || "")
  .replace(/\s*\([^)]*(?:prac(?:ovní|ovně)?\.?|draft|návrh|proposed)[^)]*\)/gi, "")
  .replace(/\s*[,–—-]?\s*(?:prac(?:ovní|ovně)?|draft|návrh|proposed)\b.*$/i, "")
  .replace(/\s*[,–—-]?\s*prac\..*$/i, "")
  .replace(/\s+/g, " ")
  .trim();
const publicTranslations = (record, capital = false) => {
  const entry = editorialFor(record, capital);
  return {
    ...(entry?.public_name_en ? { name_en: entry.public_name_en } : {}),
    ...(entry?.public_name_ja ? { name_ja: entry.public_name_ja } : {}),
  };
};
const makePublicRecords = (source, capital = false) => source.objects.map((record) => {
  const kind = kindOf(record);
  const entry = editorialFor(record, capital);
  if (!entry) throw new Error(`Missing editorial enrichment for ${capital ? "city" : "atlas"} record ${record.id}.`);
  const translations = publicTranslations(record, capital);
  const displayName = publicPlaceName(record, kind, capital);
  const approvedSourceTranslations = record.name_status === "approved" ? [record.name_en, record.name_ja] : [];
  const searchTerms = new Set([
    record.id,
    displayName,
    translations.name_en,
    translations.name_ja,
    ...(entry.aliases || []),
    record.name_cs,
    ...approvedSourceTranslations,
  ].map(cleanSearchTerm).filter(Boolean));
  searchTerms.add(record.id);
  const publicRecord = {
    id: String(record.id),
    name_cs: displayName,
    ...translations,
    description: entry.short_description_cs,
    categoryLabel: entry.category_cs,
    region: entry.region_label_cs,
    subheading: entry.subheading_cs || [entry.category_cs, entry.region_label_cs].filter(Boolean).join(" · "),
    highlights: entry.highlights_cs || [],
    scenery: entry.scenery_cs || "",
    atmosphere: entry.atmosphere_cs || "",
    nearby: (entry.viewpoints || []).map((place) => ({
      id: place.place_id,
      name_cs: place.name_cs,
      direction_cs: place.direction_cs,
      distance_km: place.distance_km,
    })),
    searchTerms: [...searchTerms],
    typeKey: kind,
    typeLabel: entry.category_cs || typeLabels[kind] || typeLabels.default,
    islandKey: String(record.island || (capital ? "main" : "main")),
    islandLabel: islandLabels[String(record.island || "main")] || "ostrovní oblast",
  };
  for (const key of capital ? ["u", "v", "x_km", "y_km"] : ["x_km", "y_km"]) {
    if (Number.isFinite(record[key])) publicRecord[key] = record[key];
  }
  if (!capital && Number.isFinite(record.elev_m_model)) {
    publicRecord.elevationLabel = record.id === "M-01"
      ? "Přibližně 560 m n. m."
      : `přibližně ${Math.round(record.elev_m_model).toLocaleString("cs-CZ")} m n. m.`;
  }
  if (capital && Number.isFinite(record.u) && Number.isFinite(record.v)) {
    publicRecord.planCoordinates = `u ${Math.round(record.u).toLocaleString("cs-CZ")} m · v ${Math.round(record.v).toLocaleString("cs-CZ")} m`;
  }
  return publicRecord;
});

function publicSvg(svg) {
  let result = svg
    .replace(/<metadata\b[^>]*>[\s\S]*?<\/metadata>/gi, "")
    .replace(/\sdata-st="[^"]*"/g, "")
    .replace(/\sdata-proposed="[^"]*"/g, "")
    .replace(/\sinkscape:label="[^"]*"/g, "")
    .replace(/\.status-mode[^}]*\}/g, "")
    .replace(/<title[^>]*>[\s\S]*?<\/title>/i, "<title>Orientační mapa Larpidie</title>")
    .replace(/<desc[^>]*>[\s\S]*?<\/desc>/i, "<desc>Schematické zobrazení fikčních ostrovů Larpidie a Paralandu.</desc>");
  result = result.replace(/(<text\b[^>]*>)([\s\S]*?)(<\/text>)/gi, (match, open, inner, close) => {
    const id = open.match(/\bdata-id="([^"]+)"/)?.[1];
    if (id) return `${open}${close}`;
    const plain = inner.replace(/<[^>]*>/g, " ").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();
    if (/draft|proposed|needs[-_ ]decision|photo_guide|world bible|\bbible\b|prompt|schválen|čeká na rozhodnutí|pracovn|návrh|pseudo|AI-asistovan|Aokawa|parliament|parlament/i.test(plain)) {
      if (/fiktivní stát|atlas|mapa/i.test(plain)) return `${open}Orientační mapa fikčního souostroví.${close}`;
      return `${open}${close}`;
    }
    return match;
  });
  const settlementFabric = '<defs><pattern id="settlement-fabric" width="520" height="440" patternUnits="userSpaceOnUse"><g fill="#ad876f" opacity=".8"><rect x="23" y="25" width="56" height="25" rx="2"/><rect x="91" y="20" width="46" height="22" rx="2"/><rect x="33" y="61" width="48" height="21" rx="2"/><rect x="221" y="37" width="58" height="25" rx="2"/><rect x="290" y="31" width="48" height="22" rx="2"/><rect x="232" y="72" width="51" height="22" rx="2"/><rect x="383" y="25" width="55" height="24" rx="2"/><rect x="400" y="60" width="48" height="21" rx="2"/><rect x="42" y="171" width="57" height="24" rx="2"/><rect x="112" y="166" width="46" height="21" rx="2"/><rect x="52" y="205" width="50" height="22" rx="2"/><rect x="254" y="183" width="58" height="25" rx="2"/><rect x="324" y="177" width="47" height="22" rx="2"/><rect x="264" y="218" width="51" height="22" rx="2"/><rect x="389" y="178" width="57" height="24" rx="2"/><rect x="400" y="212" width="48" height="21" rx="2"/><rect x="114" y="334" width="56" height="24" rx="2"/><rect x="182" y="329" width="47" height="21" rx="2"/><rect x="124" y="368" width="50" height="22" rx="2"/><rect x="319" y="327" width="56" height="24" rx="2"/><rect x="387" y="322" width="47" height="21" rx="2"/><rect x="329" y="361" width="50" height="22" rx="2"/></g></pattern></defs>';
  if (result.includes('id="settlements"') && !result.includes('id="settlement-fabric"')) {
    result = result.replace("</clipPath></defs>", `</clipPath></defs>${settlementFabric}`);
    result = result.replace(/<path\b[^>]*>/g, (tag) => {
      const id = tag.match(/\bdata-id="([^"]+)"/)?.[1] || "";
      return /^(?:C-01|T-0[1-6]|PL-0[135]|HM-0[1-6])$/.test(id)
        ? tag.replace(/\bfill="[^"]*"/, 'fill="url(#settlement-fabric)"').replace(/\bstroke="[^"]*"/, 'stroke="none"')
        : tag;
    });
  }
  return result;
}

function sanitizeViewerMarkup(html, { title, kind }) {
  let result = html.replace(/<script\b(?=[^>]*\bid="reg")(?=[^>]*\btype="application\/json")[^>]*>[\s\S]*?<\/script>/, "");
  result = result
    .replace(/<title>[^<]*<\/title>/, `<title>${title}</title>`)
    .replace(/<svg\b[\s\S]*?<\/svg>/, (svg) => publicSvg(svg))
    .replace(/\.st\.(?:approved|proposed|needs_decision)\s*\{[^}]*\}/gi, "")
    .replace(/\.legend-swatch\.(?:approved|proposed|needs_decision)\s*\{[^}]*\}/gi, "")
    .replace(/<script src="([^"]+)"><\/script>/g, '<script src="$1"></script>');
  return result;
}

function replaceSection(source, start, end, replacement) {
  const a = source.indexOf(start);
  const b = source.indexOf(end, a);
  if (a < 0 || b < 0) {
    if (start === "const q=document.getElementById('q'),res=document.getElementById('results');" && (source.includes('const q = document.getElementById("q")') || source.includes("const q=document.getElementById(\"q\"),res=document.getElementById(\"results\"),count=document.getElementById(\"search-count\")"))) return source;
    throw new Error(`Public viewer template marker missing: ${start}`);
  }
  return `${source.slice(0, a)}${replacement}${source.slice(b)}`;
}

function replaceRegexSection(source, startPattern, endPattern, replacement, label) {
  const start = startPattern.exec(source);
  if (!start) throw new Error(`Public viewer template marker missing: ${label}`);
  endPattern.lastIndex = start.index + start[0].length;
  const end = endPattern.exec(source);
  if (!end) throw new Error(`Public viewer template end marker missing: ${label}`);
  return `${source.slice(0, start.index)}${replacement}${source.slice(end.index)}`;
}

function replaceWholeLine(source, marker, replacement) {
  const start = source.indexOf(marker);
  if (start < 0) throw new Error(`Public viewer function missing: ${marker}`);
  const end = source.indexOf("\n", start);
  if (end < 0) throw new Error(`Public viewer function line is incomplete: ${marker}`);
  return `${source.slice(0, start)}${replacement}${source.slice(end)}`;
}

function makeAtlasViewer() {
  let html = sanitizeViewerMarkup(read("templates/atlas_viewer_template.html"), { title: "Atlas Larpidie", kind: "atlas" });
  html = html
    .replace('<header><h1>Atlas Larpidie a Paralandu</h1><span class="badge">NÁVRH · v1.0-draft</span>', '<header><h1>Atlas Larpidie</h1>')
    .replace('<aside class="l"><h2>Hledat místo</h2><input id="q" type="search" placeholder="ID nebo název (např. N-03, přístav, Aokawa)"><div id="results"></div>', `<aside class="l" id="search-panel"><h2>Najít místo</h2><label for="q">Hledat</label><input id="q" type="search" placeholder="Hledat místo, oblast nebo ID…" autocomplete="off"><label for="island-filter">Ostrov</label><select id="island-filter"><option value="">Všechny ostrovy</option><option value="main">Hlavní ostrov</option><option value="para">Paraland</option></select><label for="type-filter">Typ</label><select id="type-filter"><option value="">Všechny typy</option></select><div class="search-actions"><button class="small" id="clear-filters" type="button">Vymazat filtry</button><button class="small mobile-close" id="close-search" type="button">Zavřít</button></div><p id="search-count" role="status" aria-live="polite">Zadejte název nebo zvolte filtr.</p><div id="results" role="listbox" aria-label="Výsledky hledání"></div>`)
    .replace('<div id="map"><svg', '<div id="map"><button id="open-search" class="mobile-search-trigger" type="button" aria-expanded="false" aria-controls="search-panel">Hledat místa</button><svg')
    .replace('<h2>Ovládání mapy</h2><label class="row"><input type="checkbox" id="status"> Barvy podle stavu údajů</label><button class="small" id="reset">Zobrazit celou mapu</button>', '<h2>Ovládání mapy</h2><button class="small" id="reset">Zobrazit celou mapu</button>')
    .replace('Zobrazí se stav, poloha, modelová výška a případné foto či video vodítko.', 'Zobrazí se stručný popis místa a jeho orientační poloha.')
    .replace(/<span class="legend-item"><i class="legend-swatch approved"><\/i>Schválený základ<\/span><span class="legend-item"><i class="legend-swatch proposed"><\/i>Pracovní návrh<\/span><span class="legend-item"><i class="legend-swatch needs_decision"><\/i>Čeká na rozhodnutí<\/span>/, "")
    .replace('<section class="side-section"><h2>Legenda</h2><div class="legend">', '<section class="side-section"><h2>Legenda</h2><p>Mapa je orientační; poloha a některé názvy jsou zobrazeny schematicky.</p><div class="legend">')
    .replace('<footer><span id="coord">–</span><span id="count"></span></footer>', '<footer><span id="coord">Orientační fikční mapa</span><span id="count"></span><span data-project-footer></span></footer>');
  html = html.replace(/<header>[\s\S]*?<\/header>/, '<header><h1>Atlas Larpidie</h1><span class="head-note">Orientační atlas fiktivní Larpidie</span><a class="head-link" href="terrain-3d.html" target="_blank" rel="noopener">Otevřít 3D terén ↗</a></header>');
  html = html.replace(/<aside class="l"[^>]*>[\s\S]*?<\/aside>/, `<aside class="l" id="search-panel">
<h2>Najít místo</h2><label for="q">Hledat místo, oblast nebo ID</label><input id="q" type="search" placeholder="Např. Praha, Prague nebo T-01" autocomplete="off">
<label for="island-filter">Ostrov</label><select id="island-filter"><option value="">Všechny ostrovy</option><option value="main">Hlavní ostrov</option><option value="para">Paraland</option></select>
<label for="type-filter">Typ místa</label><select id="type-filter"><option value="">Všechny typy</option></select>
<div class="search-actions"><button class="small" id="clear-filters" type="button">Vymazat filtry</button><button class="small mobile-close" id="close-search" type="button">Zavřít</button></div>
<p id="search-count" role="status" aria-live="polite">Zadejte název nebo zvolte filtr.</p><div id="results" role="listbox" aria-label="Výsledky hledání"></div>
<details class="language-settings" open><summary>Jazyk popisků</summary><div class="seg"><button data-lang="cs" aria-pressed="true">Čeština</button><button data-lang="ja" aria-pressed="false">Japonština</button><button data-lang="en" aria-pressed="false">Angličtina</button></div></details>
</aside>`);
  html = html.replace(/<aside class="r">[\s\S]*?<\/aside>/, `<aside class="r">
<section class="side-section detail-section"><h2>Podrobnosti místa</h2><div id="info" aria-live="polite"><p class="record-hint">Vyberte místo v mapě nebo ve výsledcích hledání.</p></div></section>
<details class="side-section map-settings" id="layer-settings" open><summary>Vrstvy a nastavení mapy</summary><button class="small" id="reset" type="button">Zobrazit celou mapu</button><div id="layers"></div>
<section class="side-section"><h2>Legenda</h2><p>Orientační zobrazení reliéfu a krajiny fiktivního souostroví. Výškové údaje jsou orientační.</p><div class="legend"><span class="legend-item"><i class="legend-swatch sea"></i>Moře a pobřeží</span><span class="legend-item"><i class="legend-swatch nature"></i>Reliéf a krajina</span><span class="legend-item"><i class="legend-line"></i>Řeky a vodstvo</span><span class="legend-item"><i class="legend-line rail"></i>Železnice</span><span class="legend-item"><i class="legend-symbol"></i>Místa a body zájmu</span></div></section></details>
</aside>`);
  html = html.replace('<div id="map">', '<div id="map"><button id="open-search" class="mobile-search-trigger" type="button" aria-expanded="false" aria-controls="search-panel">Hledat místa</button>');
  html = html.replace('<button data-lang="ja" aria-pressed="false">日本語</button>', '<button data-lang="ja" aria-pressed="false">Japonština</button>')
    .replace('<button data-lang="en" aria-pressed="false">English</button>', '<button data-lang="en" aria-pressed="false">Angličtina</button>');
  html = html.replace("</style>", `
 .mobile-search-trigger{display:none}.mobile-close{display:none}#search-panel label{display:block;margin:.55rem 0 .2rem;color:var(--soft);font-size:.86rem;font-weight:650}#search-panel select,#search-panel input[type=search]{width:100%;min-height:2.5rem;padding:.45rem .6rem;border:1px solid var(--line);border-radius:7px;background:var(--card);color:var(--ink);font:inherit}.search-actions{display:flex;gap:.45rem;margin:.55rem 0}.result-card{display:block;width:100%;margin:.35rem 0;padding:.65rem .7rem;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);text-align:left;cursor:pointer}.result-card:hover,.result-card[aria-selected=true]{border-color:var(--acc);background:color-mix(in srgb,var(--acc) 9%,var(--card))}.result-title,.result-meta{display:block}.result-title{font-weight:700}.result-meta{margin-top:.2rem;color:var(--soft);font-size:.85rem}#search-count{margin:.55rem 0;color:var(--soft);font-size:.85rem}.place-kicker{margin:0!important;color:var(--soft);font-size:.75rem;font-weight:750;letter-spacing:.06em;text-transform:uppercase}.detail-section #info h3{margin:.2rem 0 .25rem;font:600 1.7rem/1.12 Georgia,serif;letter-spacing:-.02em}.place-translations{margin:.2rem 0 .75rem!important;color:var(--soft);font-size:.85rem}.place-lead{font-size:.96rem;line-height:1.6}.place-detail-group{margin:.85rem 0;padding-top:.65rem;border-top:1px solid var(--line)}.place-detail-group h4{margin:0 0 .35rem;color:var(--ink);font-size:.83rem}.place-detail-group p{margin:.2rem 0!important;font-size:.88rem}.place-detail-group ul{margin:.25rem 0;padding-left:1.1rem;font-size:.86rem}.place-detail-group li{margin:.25rem 0}.nearby-list{list-style:none;padding:0!important}.nearby-list li{display:flex;justify-content:space-between;align-items:center;gap:.45rem}.nearby-list li>span{white-space:nowrap;color:var(--soft);font-size:.76rem}.nearby-place{padding:0;border:0;background:none;color:var(--acc);font:inherit;font-weight:700;text-align:left;cursor:pointer}.nearby-place:hover{text-decoration:underline}.place-coordinate{color:var(--soft);font-size:.79rem;font-variant-numeric:tabular-nums}
@media(max-width:1000px){body{grid-template-columns:minmax(0,1fr);grid-template-rows:auto minmax(48vh,1fr) auto auto}header{grid-row:1}#map{grid-column:1;grid-row:2;min-height:48vh}aside.r{grid-column:1;grid-row:3;max-height:30vh;overflow:auto}body>footer{grid-column:1;grid-row:4}#search-panel{position:fixed;z-index:60;inset:0 auto 0 0;width:min(88vw,360px);height:100dvh;max-height:100dvh;overflow:auto;transform:translateX(-105%);transition:transform .22s ease;box-shadow:0 0 28px #0005}body.search-open #search-panel{transform:translateX(0)}.mobile-search-trigger{display:inline-flex;position:absolute;z-index:20;top:12px;left:12px;align-items:center;padding:.6rem .8rem;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font:inherit;font-weight:700;box-shadow:0 2px 8px #0002}.mobile-close{display:inline-flex}}
@media(prefers-reduced-motion:reduce){#search-panel{transition:none}}
</style>`);
  html = html.replace("</style>", `
body{grid-template-columns:minmax(232px,252px) minmax(0,1fr) minmax(264px,296px);grid-template-rows:auto minmax(0,1fr) auto}
header{padding:11px clamp(16px,1.6vw,26px);box-shadow:0 2px 10px rgba(31,42,51,.035)}
aside{min-width:0;padding:clamp(14px,1.3vw,21px);background:color-mix(in srgb,var(--bg) 76%,var(--card))}
aside.l{border-right:1px solid var(--line)}aside.r{border-left:1px solid var(--line)}
#map{min-height:0;box-shadow:inset 0 0 0 1px rgba(31,42,51,.08)}
#layer-settings>summary{padding:2px 0 9px;color:var(--ink);font-size:.88rem;font-weight:750;cursor:pointer;list-style-position:inside}
#layer-settings>#reset{margin:0 0 8px}
#layers .layer-group{margin:7px 0 0;padding:0 0 8px;border-color:color-mix(in srgb,var(--line) 76%,transparent)}
#layers .layer-group h2{margin:8px 0 5px;color:var(--soft);font-size:.68rem;letter-spacing:.075em;text-transform:uppercase}
label.row{min-height:33px;margin:1px 0;padding:5px 8px;gap:10px;border:1px solid transparent;border-radius:8px;font-size:.84rem;line-height:1.32;transition:background-color .14s ease,border-color .14s ease}
label.row:hover{border-color:color-mix(in srgb,var(--acc) 16%,transparent);background:color-mix(in srgb,var(--acc) 7%,var(--card))}
label.row input[type=checkbox]{appearance:none;accent-color:var(--acc);display:grid;flex:0 0 18px;place-content:center;width:18px;height:18px;margin:0;border:1px solid #a9a99e;border-radius:5px;background:var(--card);cursor:pointer;transition:background-color .14s ease,border-color .14s ease,box-shadow .14s ease}
label.row input[type=checkbox]::before{content:"";width:8px;height:4px;border:2px solid #fff;border-top:0;border-right:0;transform:translateY(-1px) rotate(-45deg) scale(0);transform-origin:center;transition:transform .12s ease}
label.row input[type=checkbox]:checked{border-color:var(--acc);background:var(--acc)}
label.row input[type=checkbox]:checked::before{transform:translateY(-1px) rotate(-45deg) scale(1)}
label.row input[type=checkbox]:focus-visible{outline:3px solid color-mix(in srgb,var(--acc) 34%,transparent);outline-offset:2px}
.small{transition:background-color .14s ease,border-color .14s ease,box-shadow .14s ease}.small:hover{background:color-mix(in srgb,var(--acc) 7%,var(--card));box-shadow:0 2px 8px rgba(31,42,51,.06)}
@media(max-width:1080px){body{grid-template-columns:minmax(0,1fr);grid-template-rows:auto minmax(48vh,1fr) auto auto}header{grid-row:1}#map{grid-column:1;grid-row:2;min-height:48vh}aside.r{grid-column:1;grid-row:3;max-height:30vh;overflow:auto}body>footer{grid-column:1;grid-row:4}#search-panel{position:fixed;z-index:60;inset:0 auto 0 0;width:min(88vw,360px);height:100dvh;max-height:100dvh;overflow:auto;transform:translateX(-105%);transition:transform .22s ease;box-shadow:0 0 28px #0005}body.search-open #search-panel{transform:translateX(0)}.mobile-search-trigger{display:inline-flex;position:absolute;z-index:20;top:12px;left:12px;align-items:center;padding:.6rem .8rem;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font:inherit;font-weight:700;box-shadow:0 2px 8px #0002}.mobile-close{display:inline-flex}aside.r{border:0;border-top:1px solid var(--line)}}
@media(prefers-reduced-motion:reduce){label.row,.small,label.row input[type=checkbox],label.row input[type=checkbox]::before{transition:none}}
</style>`);
  html = html.replace(/<script>\s*const svg=document\.querySelector\('#map svg'\);const REG=JSON\.parse\(document\.getElementById\('reg'\)\.textContent\);const BYID=Object\.fromEntries\(REG\.objects\.map\(o=>\[o\.id,o\]\)\);/, "<script>\n(async()=>{\nconst svg=document.querySelector('#map svg');const REG=await (await fetch('../registry/places.public.json')).json();const BYID=Object.fromEntries(REG.objects.map(o=>[o.id,o]));");
  html = html.replace(/let vb=\[\.\.\.FULL\];const X0=/, "let vb=[...FULL];const X0=");
  html = html.replace(/const STATUS_CS=[\s\S]*?document\.getElementById\('info'\)\.addEventListener/, `function show(id){const o=BYID[id];const box=document.getElementById('info');if(!o){box.textContent='Místo se nepodařilo najít.';return}highlight(id);box.classList.add('active');const labelEls=svg.querySelectorAll('text[data-id="'+CSS.escape(o.id)+'"]');labelEls.forEach(el=>el.textContent=o.name_cs);let h='<h3>'+esc(o.name_cs)+'</h3><p>'+esc(o.typeLabel)+' · '+esc(o.islandLabel)+'</p><p>'+esc(o.region)+' · orientační poloha</p>';if(o.elevationLabel)h+='<p>'+esc(o.elevationLabel)+'</p>';h+='<p><button class="small" data-zoom-id="'+esc(o.id)+'">Zobrazit na mapě</button></p>';box.innerHTML=h}\ndocument.getElementById('info').addEventListener`);
  html = replaceSection(html, "const q=document.getElementById('q'),res=document.getElementById('results');", "document.getElementById('count').textContent=", `const q=document.getElementById('q'),res=document.getElementById('results'),count=document.getElementById('search-count'),islandFilter=document.getElementById('island-filter'),typeFilter=document.getElementById('type-filter');
const searchable=REG.objects.filter(o=>Number.isFinite(o.x_km)&&Number.isFinite(o.y_km));let activeResult=-1,selectedId=null;
const normalize=value=>String(value??'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLocaleLowerCase('cs-CZ').trim();
const typeKeys=[...new Set(searchable.map(o=>o.typeKey))].sort((a,b)=>REG.typeLabels[a].localeCompare(REG.typeLabels[b],'cs'));
typeKeys.forEach(key=>{const option=document.createElement('option');option.value=key;option.textContent=REG.typeLabels[key];typeFilter.appendChild(option)});
function search(){const terms=normalize(q.value).split(/\\s+/).filter(Boolean),island=islandFilter.value,type=typeFilter.value;let hits=searchable.filter(o=>(!island||o.islandKey.includes(island))&&(!type||o.typeKey===type));if(terms.length)hits=hits.filter(o=>{const hay=normalize([o.id,o.name_cs,o.typeLabel,o.islandLabel,o.region].join(' '));return terms.every(term=>hay.includes(term))});hits.sort((a,b)=>{const aa=normalize(a.name_cs),bb=normalize(b.name_cs),query=normalize(q.value);const score=o=>o.id.toLowerCase()===query?0:normalize(o.name_cs)===query?1:normalize(o.name_cs).startsWith(query)?2:3;return score(a)-score(b)||aa.localeCompare(bb,'cs')||a.id.localeCompare(b.id)});activeResult=-1;res.replaceChildren();const shown=hits.slice(0,60);count.textContent=hits.length?hits.length+\" míst\"+(hits.length>shown.length?\", zobrazeno prvních \"+shown.length:\"\"):\"Žádné odpovídající místo jsme nenašli.\";for(const o of shown){const button=document.createElement('button');button.type='button';button.className='result-card';button.setAttribute('role','option');button.setAttribute('aria-selected',String(o.id===selectedId));button.dataset.id=o.id;button.innerHTML='<span class="result-title">'+esc(o.name_cs)+'</span><span class="result-meta">'+esc(o.typeLabel)+' · '+esc(o.islandLabel)+' · '+esc(o.region)+'</span><span class="result-id">'+esc(o.id)+'</span>';res.appendChild(button)}}
function selectResult(id){const o=BYID[id];if(!o)return;selectedId=id;search();selectPlace(id);closeSearch()}
function closeSearch(){document.body.classList.remove('search-open');document.getElementById('open-search').setAttribute('aria-expanded','false')}
document.getElementById('open-search').addEventListener('click',()=>{document.body.classList.add('search-open');document.getElementById('open-search').setAttribute('aria-expanded','true');q.focus()});document.getElementById('close-search').addEventListener('click',closeSearch);
document.getElementById('clear-filters').addEventListener('click',()=>{q.value='';islandFilter.value='';typeFilter.value='';search();q.focus()});q.addEventListener('input',search);islandFilter.addEventListener('change',search);typeFilter.addEventListener('change',search);
res.addEventListener('click',e=>{const button=e.target.closest('button[data-id]');if(button)selectResult(button.dataset.id)});q.addEventListener('keydown',e=>{const cards=[...res.querySelectorAll('button[data-id]')];if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(!cards.length)return;activeResult=(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;cards[activeResult].focus()}else if(e.key==='Enter'){const target=e.target.closest('button[data-id]');const id=target?.dataset.id||cards[Math.max(0,activeResult)]?.dataset.id;if(id){e.preventDefault();selectResult(id)}}else if(e.key==='Escape'){closeSearch();q.blur()}});res.addEventListener('keydown',e=>{if(e.key==='Escape'){closeSearch();q.focus()}});search();
`);
  html = html.replace("document.getElementById('status').onchange=e=>svg.classList.toggle('status-mode',e.target.checked);", "");
  html = html.replace("['pracovní','proposed']", "");
  html = html.replace("res.addEventListener('keydown',e=>{if(e.key==='Escape'){closeSearch();q.focus()}});search();", "res.addEventListener('keydown',e=>{const cards=[...res.querySelectorAll('button[data-id]')];if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const index=cards.indexOf(e.target.closest('button[data-id]'));const next=(index+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;cards[next]?.focus()}else if(e.key==='Escape'){closeSearch();q.focus()}});search();");
  html = html.replace("activeResult=(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;", "activeResult=activeResult<0?(e.key==='ArrowDown'?0:cards.length-1):(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;");
  html = replaceWholeLine(html, "function translateMapLabel(", "function translateMapLabel(text,lang,id){return text}");
  html = html.replace(/document\.getElementById\('coord'\)\.textContent=`x \$\{kx\.toFixed\(2\)\} km · y \$\{ky\.toFixed\(2\)\} km · X \$\{\(kx\/FW\*100\)\.toFixed\(1\)\} % · Y \$\{\(ky\/FH\*100\)\.toFixed\(1\)\} %`;/, "document.getElementById('coord').textContent=`Souřadnice v atlasu: x ${kx.toFixed(2)} km · y ${ky.toFixed(2)} km`;");
  const visitorShow = [
    "function show(id){const o=BYID[id],box=document.getElementById('info');if(!o){box.textContent='Místo se nepodařilo najít.';return}highlight(id);box.classList.add('active');document.getElementById('layer-settings').open=false;svg.querySelectorAll('text[data-id=\"'+CSS.escape(o.id)+'\"]').forEach(el=>el.textContent=o.name_cs);let h='<p class=\"place-kicker\">'+esc(o.categoryLabel)+' · '+esc(o.region)+'</p><h3>'+esc(o.name_cs)+'</h3>';const translations=[o.name_en?'Anglicky: '+o.name_en:'',o.name_ja?'Japonsky: '+o.name_ja:''].filter(Boolean);if(translations.length)h+='<p class=\"place-translations\">'+esc(translations.join(' · '))+'</p>';h+='<p class=\"place-lead\">'+esc(o.description)+'</p>';if(o.highlights?.length)h+='<section class=\"place-detail-group\"><h4>Zajímavosti</h4><ul>'+o.highlights.map(item=>'<li>'+esc(item)+'</li>').join('')+'</ul></section>';if(o.scenery)h+='<section class=\"place-detail-group\"><h4>Scenerie</h4><p>'+esc(o.scenery)+'</p></section>';if(o.atmosphere)h+='<section class=\"place-detail-group\"><h4>Místní charakter</h4><p>'+esc(o.atmosphere)+'</p></section>';if(o.x_km!=null&&o.y_km!=null)h+='<p class=\"place-coordinate\">Souřadnice v atlasu: x '+Number(o.x_km).toLocaleString(\'cs-CZ\',{minimumFractionDigits:2,maximumFractionDigits:2})+' km · y '+Number(o.y_km).toLocaleString(\'cs-CZ\',{minimumFractionDigits:2,maximumFractionDigits:2})+' km</p>';if(o.elevationLabel)h+='<p class=\"place-coordinate\">Nadmořská výška: '+esc(o.elevationLabel)+'</p>';if(o.nearby?.length)h+='<section class=\"place-detail-group\"><h4>Nejbližší místa</h4><ul class=\"nearby-list\">'+o.nearby.map(n=>'<li><button type=\"button\" class=\"nearby-place\" data-zoom-id=\"'+esc(n.id)+'\">'+esc(n.name_cs)+'</button><span>'+esc(n.direction_cs)+' · '+(n.distance_km<1?Math.round(n.distance_km*100)*10+' m':Number(n.distance_km).toLocaleString(\'cs-CZ\',{maximumFractionDigits:1})+' km')+'</span></li>').join('')+'</ul></section>';if(o.planCoordinates)h+='<p class=\"place-coordinate\">Souřadnice v plánu: '+esc(o.planCoordinates)+'</p>';h+='<p><button class=\"small\" data-zoom-id=\"'+esc(o.id)+'\">Zobrazit na mapě</button></p>';box.innerHTML=h}",
  ].join("");
  html = replaceRegexSection(html, /function show\(id\)\{/, /document\.getElementById\('info'\)\.addEventListener/, atlasShowRenderer + "\n");
  const oldAtlasInfoClick = "document.getElementById('info').addEventListener('click',e=>{const b=e.target.closest('[data-zoom-id]');if(b&&BYID[b.dataset.zoomId])selectPlace(b.dataset.zoomId)});";
  if (!html.includes(oldAtlasInfoClick)) throw new Error("Could not locate the atlas detail-card click handler.");
  html = html.replace(oldAtlasInfoClick, atlasInfoClickRenderer);
  const sourcePresenter = html.indexOf("const publicTypeLabels=");
  const publicHelpers = html.indexOf("const publicUsefulAtlasText=", sourcePresenter);
  const publicShow = html.indexOf("function show(id){", sourcePresenter);
  if (sourcePresenter < 0 || publicHelpers < 0 || publicShow < 0) throw new Error("Atlas visitor presentation helpers could not be separated from the public export.");
  html = html.slice(0, sourcePresenter) + "const publicName=o=>o.name_cs;\n" + html.slice(publicHelpers);
  const visitorSearch = [
    "function search(){const terms=normalize(q.value).split(/\\s+/).filter(Boolean),island=islandFilter.value,type=typeFilter.value;let hits=searchable.filter(o=>(!island||o.islandKey.includes(island))&&(!type||o.typeKey===type));if(terms.length)hits=hits.filter(o=>{const hay=normalize([o.id,o.name_cs,o.name_en,o.name_ja,o.typeLabel,o.islandLabel,o.region,...(o.searchTerms||[])].join(' '));return terms.every(term=>hay.includes(term))});hits.sort((a,b)=>{const aa=normalize(a.name_cs),bb=normalize(b.name_cs),query=normalize(q.value),score=o=>normalize(o.id)===query?0:(o.searchTerms||[]).some(term=>normalize(term)===query)?1:normalize(o.name_cs)===query?2:normalize(o.name_cs).startsWith(query)?3:4;return score(a)-score(b)||aa.localeCompare(bb,'cs')||a.id.localeCompare(b.id)});activeResult=-1;res.replaceChildren();const shown=hits.slice(0,60);count.textContent=hits.length?hits.length+\" míst\"+(hits.length>shown.length?\", zobrazeno prvních \"+shown.length:\"\"): \"Žádné odpovídající místo jsme nenašli.\";for(const o of shown){const button=document.createElement('button');button.type='button';button.className='result-card';button.setAttribute('role','option');button.setAttribute('aria-selected',String(o.id===selectedId));button.dataset.id=o.id;button.innerHTML='<span class=\"result-title\">'+esc(o.name_cs)+'</span><span class=\"result-meta\">'+esc(o.description)+' · '+esc(o.region)+'</span>';res.appendChild(button)}}",
  ].join("");
  html = replaceRegexSection(html, /function search\(\)\{/, /function selectResult/, visitorSearch + "\n");
  html = html.replace(/<\/script>\s*<\/body>/, "})();\n</script>\n</body>");
  if (!html.includes('src="../../../project-meta.js"')) html = html.replace("</body>", '<script src="../../../project-meta.js" defer></script>\n</body>');
  if (!html.includes('src="../../../site-brand.js"')) html = html.replace("</body>", '<script src="../../../site-brand.js" defer></script>\n</body>');
  if (!html.includes('href="../../../site-brand.css"')) html = html.replace("</head>", '<link rel="stylesheet" href="../../../site-brand.css">\n</head>');
  return html.replace(/[ \t]+(?=\r?$)/gm, "");
}

function makeCapitalViewer() {
  let html = sanitizeViewerMarkup(read("templates/capital_plan_viewer_template.html"), { title: "Plán Larpingtonu", kind: "capital" });
  html = html
    .replace('<header><h1>Larpington – podklad plánu hlavního města (CP-01)</h1><span class="badge">NÁVRH · v1.0-draft</span>', '<header><h1>Plán Larpingtonu</h1>')
    .replace('placeholder="ID nebo název (např. CP-B01, parlament, tržnice)"', 'placeholder="Hledat místo, oblast nebo ID…"')
    .replace('<h2>Hledání</h2><input id="q" type="search" placeholder="Hledat místo, oblast nebo ID…"><div id="results"></div>', '<h2>Hledat místo</h2><label for="q">Hledat</label><input id="q" type="search" placeholder="Hledat místo, oblast nebo ID…"><label for="type-filter">Typ</label><select id="type-filter"><option value="">Všechny typy</option></select><button class="small" id="clear-filters" type="button">Vymazat hledání</button><div id="search-count" role="status" aria-live="polite">Zadejte název nebo zvolte filtr.</div><div id="results" role="listbox" aria-label="Výsledky hledání"></div>')
    .replace('<h2>Režim</h2><label class="row"><input type="checkbox" id="status"> Obrysy podle stavu (schváleno × návrh)</label>', '<h2>Mapové vrstvy</h2>')
    .replace('Zobrazí se stav, poloha v metrech plánu i v km atlasu a foto/video vodítko.', 'Zobrazí se stručný popis objektu a jeho poloha v plánu.')
    .replace(/<footer><span id="coord">–<\/span><span id="count"><\/span><\/footer>/, '<footer><span id="coord">Orientační plán města</span><span id="count"></span><span data-project-footer></span></footer>');
  html = html.replace(/<header>[\s\S]*?<\/header>/, '<header><h1>Plán Larpingtonu</h1><span style="color:var(--soft)">Orientační plán hlavního města</span><a class="city3d-link" href="capital-3d.html" target="_blank" rel="noopener">Otevřít 3D Larpington ↗</a></header>');
  html = html.replace(/<aside>[\s\S]*?<\/aside>/, `<aside class="city-search-panel" id="search-panel">
<h2>Najít místo</h2><label for="q">Hledat místo, oblast nebo ID</label><input id="q" type="search" placeholder="Např. Radnice Larpingtonu nebo CP-B01" autocomplete="off">
<label for="type-filter">Typ místa</label><select id="type-filter"><option value="">Všechny typy</option></select><div class="search-actions"><button class="small" id="clear-filters" type="button">Vymazat filtry</button><button class="small mobile-close" id="close-search" type="button">Zavřít</button></div>
<div id="search-count" role="status" aria-live="polite">Zadejte název nebo zvolte filtr.</div><div id="results" role="listbox" aria-label="Výsledky hledání"></div>
<details class="language-settings" open><summary>Jazyk popisků</summary><div class="seg"><button data-lang="cs" aria-pressed="true">Čeština</button><button data-lang="ja" aria-pressed="false">Japonština</button><button data-lang="en" aria-pressed="false">Angličtina</button></div></details>
<details class="map-settings" id="layer-settings" open><summary>Vrstvy a nastavení mapy</summary><label class="row"><input type="checkbox" id="house-numbers-toggle"> Čísla domů při přiblížení</label><button class="small" id="reset" type="button">Zobrazit celý plán</button><div id="layers"></div></details>
</aside>`);
  html = html.replace('<div id="map">', '<div id="map"><button id="open-search" class="mobile-search-trigger" type="button" aria-expanded="false" aria-controls="search-panel">Hledat místa</button>');
  html = html.replace(/<aside class="r">[\s\S]*?<\/aside>/, '<aside class="r"><section class="detail-section"><h2>Podrobnosti místa</h2><div id="info" aria-live="polite"><p style="color:var(--soft)">Vyberte objekt v plánu nebo ve výsledcích hledání.</p></div></section></aside>');
  html = html.replace(/\.status-mode\s*\[data-st="(?:approved|proposed)"\]\s*\{[^}]*\}/gi, "");
  html = html.replace("</style>", `
 .city-search-panel{box-sizing:border-box;overflow:auto}.city-search-panel label{display:block;margin:.55rem 0 .2rem;color:var(--soft);font-size:.86rem;font-weight:650}.city-search-panel select,.city-search-panel input[type=search]{box-sizing:border-box;width:100%;min-height:2.5rem;padding:.45rem .6rem;border:1px solid var(--line,#d4d1c7);border-radius:7px;background:var(--card,#fff);color:var(--ink,#242a27);font:inherit}.city-search-panel input[type=checkbox]{accent-color:#326653}.search-actions{display:flex;gap:.45rem;margin:.55rem 0}.result-card{display:block;width:100%;margin:.35rem 0;padding:.65rem .7rem;border:1px solid var(--line,#d4d1c7);border-radius:8px;background:var(--card,#fff);color:var(--ink,#242a27);text-align:left;cursor:pointer}.result-card:hover,.result-card[aria-selected=true]{border-color:#326653;background:#edf3ef}.result-title,.result-meta{display:block}.result-title{font-weight:700}.result-meta{margin-top:.2rem;color:var(--soft,#65716a);font-size:.85rem}.language-settings,.map-settings{border-top:1px solid var(--line,#d4d1c7);padding-top:.7rem;margin-top:.8rem}.language-settings summary,.map-settings summary{cursor:pointer;font-weight:700;padding:.3rem 0}.detail-section #info{line-height:1.55}.detail-section #info h3{font:600 1.65rem/1.13 Georgia,serif;margin:.2rem 0 .25rem}.detail-section #info p{margin:.45rem 0}.place-kicker{margin:0!important;color:var(--soft,#65716a);font-size:.74rem;font-weight:750;letter-spacing:.06em;text-transform:uppercase}.place-translations{margin:.2rem 0 .7rem!important;color:var(--soft,#65716a);font-size:.85rem}.place-lead{font-size:.94rem;line-height:1.6}.place-detail-group{margin:.8rem 0;padding-top:.6rem;border-top:1px solid var(--line,#d4d1c7)}.place-detail-group h4{margin:0 0 .35rem;font-size:.83rem}.place-detail-group p,.place-detail-group ul{margin:.25rem 0!important;font-size:.86rem}.place-detail-group ul{padding-left:1.1rem}.nearby-list{list-style:none;padding:0!important}.nearby-list li{display:flex;justify-content:space-between;align-items:center;gap:.4rem;margin:.25rem 0}.nearby-list li>span{color:var(--soft,#65716a);font-size:.76rem;white-space:nowrap}.nearby-place{padding:0;border:0;background:none;color:#326653;font:inherit;font-weight:700;text-align:left;cursor:pointer}.place-coordinate{color:var(--soft,#65716a);font-size:.79rem;font-variant-numeric:tabular-nums}.mobile-search-trigger{display:none}.mobile-close{display:none}
@media(max-width:1000px){body{grid-template-columns:minmax(0,1fr);grid-template-rows:auto minmax(48vh,1fr) auto auto}header{grid-row:1}#map{grid-column:1;grid-row:2;min-height:48vh}aside.r{grid-column:1;grid-row:3;max-height:30vh;overflow:auto}body>footer{grid-column:1;grid-row:4}.city-search-panel{position:fixed;z-index:60;inset:0 auto 0 0;width:min(88vw,360px);height:100dvh;max-height:100dvh;transform:translateX(-105%);transition:transform .22s ease;box-shadow:0 0 28px #0005}body.search-open .city-search-panel{transform:translateX(0)}.mobile-search-trigger{display:inline-flex;position:absolute;z-index:20;top:12px;left:12px;padding:.6rem .8rem;border:1px solid var(--line,#d4d1c7);border-radius:8px;background:var(--card,#fff);color:var(--ink,#242a27);font:inherit;font-weight:700}.mobile-close{display:inline-flex}}
</style>`);
  html = html.replace("</style>", "@media(max-width:620px){header{display:grid;grid-template-columns:36px minmax(0,1fr);gap:3px 8px;padding:8px 12px}header>.site-brand-home{grid-column:1;grid-row:1/3;margin:0}header>h1{grid-column:2;grid-row:1;margin:0;font-size:1.05rem}header>span{grid-column:2;grid-row:2;font-size:.78rem}header>.city3d-link{grid-column:2;grid-row:3;justify-self:start;white-space:nowrap;font-size:.82rem}}</style>");
  html = html.replace(/const lab\s*=\s*el\.getAttribute\("inkscape:label"\)\s*\|\|\s*i;/, "const lab=({'bg-sea':'Moře','land':'Pevnina','contours':'Výškové linie','beaches':'Pláže','grid':'Souřadnicová síť','green-wedges':'Zelené plochy','districts':'Čtvrti','blocks':'Městské bloky','spaces':'Veřejná prostranství','harbor':'Přístav','streets':'Ulice','rail-surface':'Železniční tratě','rail-L3':'Železniční linka L3','stations':'Stanice','access-route':'Přístupové trasy','houses':'Domy','buildings-key':'Budovy','poi':'Místa zájmu','future-development':'Plánované doplnění zástavby','labels-cs':'České popisky','labels-en':'Anglické popisky','labels-ja':'Japonské popisky','marginalia':'Okraje mapy'})[i]||'Mapová vrstva';");
  html = html.replace(/<script>\s*(?=const svg\s*=\s*document\.querySelector\("#map svg"\);)/, "<script>\n(async()=>{\n");
  html = html.replace(/const REG\s*=\s*JSON\.parse\(document\.getElementById\("reg"\)\.textContent\);/, "const REG = await (await fetch('cp_objects.public.json')).json();");
  html = html.replace(/function stBadge\(k, v\)\s*\{[\s\S]*?function addFutureDevelopment\(\)/, `function show(id){const o=BYID[id],box=document.getElementById('info');if(!o){box.textContent='Objekt se nepodařilo najít.';return}highlight(id);document.getElementById('layer-settings').open=false;svg.querySelectorAll('text[data-id="'+CSS.escape(o.id)+'"]').forEach(el=>el.textContent=o.name_cs);let h='<h3>'+esc(o.name_cs)+'</h3>';const translations=[o.name_en?'English: '+o.name_en:'',o.name_ja?'日本語: '+o.name_ja:''].filter(Boolean);if(translations.length)h+='<p class="place-translations">'+esc(translations.join(' · '))+'</p>';h+='<p>'+esc(o.description)+'</p><p>'+esc(o.region)+'</p>';if(Number.isFinite(o.u)&&Number.isFinite(o.v))h+='<p><strong>Poloha v plánu:</strong> u '+o.u.toLocaleString('cs-CZ')+' m · v '+o.v.toLocaleString('cs-CZ')+' m</p>';h+='<p><button class="small" data-zoom-id="'+esc(o.id)+'">Zobrazit na mapě</button></p>';box.innerHTML=h}
document.getElementById('info').addEventListener('click',e=>{const b=e.target.closest('[data-zoom-id]');if(b&&BYID[b.dataset.zoomId])zoomTo(BYID[b.dataset.zoomId])});
function addFutureDevelopment()`);
  const cityShowStart = html.indexOf("function show(id){");
  const cityFutureStart = html.indexOf("function addFutureDevelopment()", cityShowStart);
  if (cityShowStart < 0 || cityFutureStart < 0) throw new Error("Could not locate the active Larpington detail renderer.");
  html = html.slice(0, cityShowStart) + cityShowRenderer + "\n" + html.slice(cityFutureStart);
  html = html.replace(/document\.getElementById\("status"\)\.onchange\s*=\s*\(e\)\s*=>\s*svg\.classList\.toggle\("status-mode", e\.target\.checked\);\s*/, "");
  html = replaceRegexSection(html, /const q\s*=\s*document\.getElementById\("q"\),[\s\S]*?res\s*=\s*document\.getElementById\("results"\);/, /document\.getElementById\("count"\)\.textContent\s*=/, [
    `const q=document.getElementById("q"),res=document.getElementById("results"),count=document.getElementById("search-count"),typeFilter=document.getElementById("type-filter");`,
    `const searchable=REG.objects.filter(o=>Number.isFinite(o.u)&&Number.isFinite(o.v)),normalize=value=>String(value??"").normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLocaleLowerCase("cs-CZ").trim();let activeResult=-1,selectedId=null;`,
    `const typeKeys=[...new Set(searchable.map(o=>o.typeKey))].sort((a,b)=>REG.typeLabels[a].localeCompare(REG.typeLabels[b],"cs"));typeKeys.forEach(key=>{const option=document.createElement("option");option.value=key;option.textContent=REG.typeLabels[key];typeFilter.appendChild(option)});`,
    `function search(){const terms=normalize(q.value).split(/\\s+/).filter(Boolean);let hits=searchable.filter(o=>!typeFilter.value||o.typeKey===typeFilter.value);if(terms.length)hits=hits.filter(o=>{const hay=normalize([o.id,o.name_cs,o.name_en,o.name_ja,o.description,o.typeLabel,o.islandLabel,o.region,...(o.searchTerms||[])].join(" "));return terms.every(term=>hay.includes(term))});hits.sort((a,b)=>{const query=normalize(q.value),score=o=>normalize(o.id)===query?0:(o.searchTerms||[]).some(term=>normalize(term)===query)?1:normalize(o.name_cs)===query?2:normalize(o.name_cs).startsWith(query)?3:4;return score(a)-score(b)||a.name_cs.localeCompare(b.name_cs,"cs")||a.id.localeCompare(b.id)});activeResult=-1;res.replaceChildren();const shown=hits.slice(0,60);count.textContent=hits.length?hits.length+" objektů"+(hits.length>shown.length?", zobrazeno prvních "+shown.length:""):"Žádný odpovídající objekt jsme nenašli.";for(const o of shown){const button=document.createElement("button");button.type="button";button.className="result-card";button.setAttribute("role","option");button.setAttribute("aria-selected",String(o.id===selectedId));button.dataset.id=o.id;button.innerHTML='<span class="result-title">'+esc(o.name_cs)+'</span><span class="result-meta">'+esc(o.description)+' · '+esc(o.region)+'</span>';res.appendChild(button)}}`,
    `function selectResult(id){const o=BYID[id];if(!o)return;selectedId=id;search();selectObject(id);closeSearch()}`,
    `function closeSearch(){document.body.classList.remove("search-open");document.getElementById("open-search").setAttribute("aria-expanded","false")}`,
    `document.getElementById("open-search").addEventListener("click",()=>{document.body.classList.add("search-open");document.getElementById("open-search").setAttribute("aria-expanded","true");q.focus()});document.getElementById("close-search").addEventListener("click",closeSearch);`,
    `document.getElementById("clear-filters").addEventListener("click",()=>{q.value="";typeFilter.value="";search();q.focus()});q.addEventListener("input",search);typeFilter.addEventListener("change",search);`,
    `res.addEventListener("click",e=>{const button=e.target.closest("button[data-id]");if(button)selectResult(button.dataset.id)});q.addEventListener("keydown",e=>{const cards=[...res.querySelectorAll("button[data-id]")];if(e.key==="ArrowDown"||e.key==="ArrowUp"){e.preventDefault();if(!cards.length)return;activeResult=(activeResult+(e.key==="ArrowDown"?1:-1)+cards.length)%cards.length;cards[activeResult].focus()}else if(e.key==="Enter"){const id=cards[Math.max(0,activeResult)]?.dataset.id;if(id){e.preventDefault();selectResult(id)}}else if(e.key==="Escape"){closeSearch();q.blur()}});res.addEventListener("keydown",e=>{if(e.key==="Escape"){closeSearch();q.focus()}});search();`
  ].join("\n"), "city search");
  html = html.replace(/<span class="result-id">'\+esc\(o\.id\)\+'<\/span>/g, "");
  html = html.replace(/document\.getElementById\("count"\)\.textContent\s*=\s*REG\.objects\.length\s*\+\s*"[^"]*";/, 'document.getElementById("count").textContent=REG.objects.length+" objektů";');
  html = html.replace(/document\.getElementById\("coord"\)\.textContent\s*=\s*`u \$\{sx\.toFixed\(0\)\} m · v \$\{sy\.toFixed\(0\)\} m · atlas x \$\{\(X0 \+ sx \/ 1000\)\.toFixed\(3\)\} km, y \$\{\(Y0 \+ sy \/ 1000\)\.toFixed\(3\)\} km`;/, 'document.getElementById("coord").textContent=`Souřadnice v plánu: u ${sx.toFixed(0)} m · v ${sy.toFixed(0)} m`;');
  html = html.replace(/<desc>[\s\S]*?<\/desc>/, '<desc>Schematický orientační plán hlavního města Larpingtonu.</desc>');
  html = html.replace(/node\.setAttribute\("data-proposed",\s*"true"\);/g, "");
  html = html.replace(/<script>\s*const svg=document\.querySelector\('#map svg'\);const REG=JSON\.parse\(document\.getElementById\('reg'\)\.textContent\);const BYID=Object\.fromEntries\(REG\.objects\.map\(o=>\[o\.id,o\]\)\);/, "<script>\n(async()=>{\nconst svg=document.querySelector('#map svg');const REG=await (await fetch('cp_objects.public.json')).json();const BYID=Object.fromEntries(REG.objects.map(o=>[o.id,o]));");
  html = html.replace(/function stBadge\(k,v\)\{[\s\S]*?function addFutureDevelopment/, `function show(id){const o=BYID[id];const box=document.getElementById('info');if(!o){box.textContent='Objekt se nepodařilo najít.';return}highlight(id);const labels=svg.querySelectorAll('text[data-id="'+CSS.escape(o.id)+'"]');labels.forEach(el=>el.textContent=o.name_cs);let h='<p class="place-kicker">'+esc(o.categoryLabel)+' · '+esc(o.region)+'</p><h3>'+esc(o.name_cs)+'</h3>';const translations=[o.name_en?'Anglicky: '+o.name_en:'',o.name_ja?'Japonsky: '+o.name_ja:''].filter(Boolean);if(translations.length)h+='<p class="place-translations">'+esc(translations.join(' · '))+'</p>';h+='<p class="place-lead">'+esc(o.description)+'</p>';if(o.highlights?.length)h+='<section class="place-detail-group"><h4>Zajímavosti</h4><ul>'+o.highlights.map(item=>'<li>'+esc(item)+'</li>').join('')+'</ul></section>';if(o.scenery)h+='<section class="place-detail-group"><h4>Scenerie</h4><p>'+esc(o.scenery)+'</p></section>';if(o.atmosphere)h+='<section class="place-detail-group"><h4>Místní charakter</h4><p>'+esc(o.atmosphere)+'</p></section>';if(o.nearby?.length)h+='<section class="place-detail-group"><h4>Nejbližší místa</h4><ul class="nearby-list">'+o.nearby.map(n=>'<li><button type="button" class="nearby-place" data-zoom-id="'+esc(n.id)+'">'+esc(n.name_cs)+'</button><span>'+esc(n.direction_cs)+' · '+(n.distance_km<1?Math.round(n.distance_km*100)*10+' m':Number(n.distance_km).toLocaleString('cs-CZ',{maximumFractionDigits:1})+' km')+'</span></li>').join('')+'</ul></section>';if(o.planCoordinates)h+='<p class="place-coordinate">Souřadnice v plánu: '+esc(o.planCoordinates)+'</p>';h+='<p><button class="small" data-zoom-id="'+esc(o.id)+'">Zobrazit na mapě</button></p>';box.innerHTML=h}\ndocument.getElementById('info').addEventListener('click',e=>{const b=e.target.closest('[data-zoom-id]');if(b&&BYID[b.dataset.zoomId]){zoomTo(BYID[b.dataset.zoomId]);if(b.dataset.zoomId!==document.querySelector('#info h3')?.dataset.id)show(b.dataset.zoomId)}});\nfunction addFutureDevelopment`);
  html = html
    .replace("layer.setAttribute('inkscape:label','Návrh budoucí zástavby v rezervě')", "layer.setAttribute('inkscape:label','Plánované doplnění zástavby')")
    .replace("layer.setAttribute('aria-label','Schematické budoucí domy v dosud nezastavěných blocích')", "layer.setAttribute('aria-label','Ilustrativní budovy plánované k doplnění')")
    .replace("node.setAttribute('data-proposed','true');", "");
  html = replaceSection(html, "const q=document.getElementById('q'),res=document.getElementById('results');", "document.getElementById('count').textContent=", `const q=document.getElementById('q'),res=document.getElementById('results'),count=document.getElementById('search-count'),typeFilter=document.getElementById('type-filter');const searchable=REG.objects.filter(o=>Number.isFinite(o.u)&&Number.isFinite(o.v));let activeResult=-1,selectedId=null;const normalize=value=>String(value??'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLocaleLowerCase('cs-CZ').trim();const typeKeys=[...new Set(searchable.map(o=>o.typeKey))].sort((a,b)=>REG.typeLabels[a].localeCompare(REG.typeLabels[b],'cs'));typeKeys.forEach(key=>{const option=document.createElement('option');option.value=key;option.textContent=REG.typeLabels[key];typeFilter.appendChild(option)});function search(){const terms=normalize(q.value).split(/\\s+/).filter(Boolean);let hits=searchable.filter(o=>!typeFilter.value||o.typeKey===typeFilter.value);if(terms.length)hits=hits.filter(o=>{const hay=normalize([o.id,o.name_cs,o.typeLabel,o.islandLabel,o.region].join(' '));return terms.every(term=>hay.includes(term))});hits.sort((a,b)=>{const score=o=>normalize(o.id)===normalize(q.value)?0:normalize(o.name_cs)===normalize(q.value)?1:normalize(o.name_cs).startsWith(normalize(q.value))?2:3;return score(a)-score(b)||a.name_cs.localeCompare(b.name_cs,'cs')||a.id.localeCompare(b.id)});activeResult=-1;res.replaceChildren();const shown=hits.slice(0,60);count.textContent=hits.length?hits.length+\" objektů\"+(hits.length>shown.length?\", zobrazeno prvních \"+shown.length:\"\"):\"Žádný odpovídající objekt jsme nenašli.\";for(const o of shown){const button=document.createElement('button');button.type='button';button.className='result-card';button.setAttribute('role','option');button.setAttribute('aria-selected',String(o.id===selectedId));button.dataset.id=o.id;button.innerHTML='<span class="result-title">'+esc(o.name_cs)+'</span><span class="result-meta">'+esc(o.typeLabel)+' · '+esc(o.islandLabel)+' · '+esc(o.region)+'</span><span class="result-id">'+esc(o.id)+'</span>';res.appendChild(button)}}function selectResult(id){const o=BYID[id];if(!o)return;selectedId=id;search();selectObject(id)}q.addEventListener('input',search);typeFilter.addEventListener('change',search);document.getElementById('clear-filters').addEventListener('click',()=>{q.value='';typeFilter.value='';search();q.focus()});res.addEventListener('click',e=>{const button=e.target.closest('button[data-id]');if(button)selectResult(button.dataset.id)});q.addEventListener('keydown',e=>{const cards=[...res.querySelectorAll('button[data-id]')];if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(!cards.length)return;activeResult=(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;cards[activeResult].focus()}else if(e.key==='Enter'){const target=e.target.closest('button[data-id]');const id=target?.dataset.id||cards[Math.max(0,activeResult)]?.dataset.id;if(id){e.preventDefault();selectResult(id)}}else if(e.key==='Escape'){q.value='';search()}});res.addEventListener('keydown',e=>{if(e.key==='Escape'){q.focus()}});search();
`);
  html = html.replace("document.getElementById('status').onchange=e=>svg.classList.toggle('status-mode',e.target.checked);", "");
  html = html.replace("res.addEventListener('keydown',e=>{if(e.key==='Escape'){q.focus()}});search();", "res.addEventListener('keydown',e=>{const cards=[...res.querySelectorAll('button[data-id]')];if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const index=cards.indexOf(e.target.closest('button[data-id]'));const next=(index+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;cards[next]?.focus()}else if(e.key==='Escape'){q.focus()}});search();");
  html = html.replace("activeResult=(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;", "activeResult=activeResult<0?(e.key==='ArrowDown'?0:cards.length-1):(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;");
  html = html.replace("document.getElementById('count').textContent=REG.objects.length+' objektů v registru plánu';", "document.getElementById('count').textContent=REG.objects.length+' objektů';\nsvg.querySelectorAll('text[data-id]').forEach(el=>{const record=BYID[el.dataset.id];if(record)el.textContent=record.name_cs});\n");
  html = html.replace(/addFutureDevelopment\(\);/, "addFutureDevelopment();svg.querySelectorAll('text[data-id]').forEach(el=>{const record=BYID[el.dataset.id];if(record)el.textContent=record.name_cs});");
  html = html.replace(/<\/script>\s*<\/body>/, "})();\n</script><script src=\"../../../project-meta.js\" defer></script><script src=\"../../../site-brand.js\" defer></script>\n</body>");
  html = html.replace("</head>", '<link rel="stylesheet" href="../../../site-brand.css">\n</head>');
  return html.replace(/[ \t]+(?=\r?$)/gm, "");
}

if (process.argv.includes("--geography-only")) {
  if (path.resolve(output) !== path.join(root, "public")) throw new Error("Refusing to update a path outside the generated public directory.");
  if (!fs.existsSync(output)) throw new Error("The existing public output is required for a targeted geography update.");
  const existingOutput = fs.lstatSync(output);
  if (!existingOutput.isDirectory() || existingOutput.isSymbolicLink()) throw new Error("Refusing to update a non-directory or linked public output path.");
  const placeSource = readJson("atlas/current/registry/places.json");
  const citySource = readJson("atlas/current/capital/cp_objects.json");
  const cityViewerSource = read("templates/capital_plan_viewer_template.html");
  const embeddedCityRegistry = cityViewerSource.match(/<script\b(?=[^>]*\bid="reg")(?=[^>]*\btype="application\/json")[^>]*>([\s\S]*?)<\/script>/);
  if (!embeddedCityRegistry || JSON.stringify(JSON.parse(embeddedCityRegistry[1])) !== JSON.stringify(citySource)) {
    throw new Error("The embedded city plan registry is out of sync with cp_objects.json. Run scripts/sync_capital_registry.mjs.");
  }
  const placeRecords = makePublicRecords(placeSource);
  const cityRecords = makePublicRecords(citySource, true);
  if (placeRecords.length !== 159 || cityRecords.length !== 662) throw new Error(`Registry count mismatch: ${placeRecords.length}/159 places, ${cityRecords.length}/662 city objects.`);
  const ids = (items) => items.map((item) => item.id).sort();
  if (new Set(ids(placeRecords)).size !== 159 || new Set(ids(cityRecords)).size !== 662) throw new Error("Public registry contains duplicate IDs.");
  if (ids(placeRecords).join("\n") !== ids(placeSource.objects).join("\n") || ids(cityRecords).join("\n") !== ids(citySource.objects).join("\n")) throw new Error("A source registry object is missing from the public projection.");
  if (placeRecords.some((item) => "notes" in item || "photo_guide" in item || "bible_ref" in item || "exist_status" in item || "name_status" in item || "pos_status" in item)) throw new Error("Private atlas fields leaked into a public place record.");
  if (cityRecords.some((item) => "notes" in item || "photo_guide" in item || "bible_ref" in item || "exist_status" in item || "name_status" in item || "pos_status" in item)) throw new Error("Private city fields leaked into a public city record.");
  const publicPlacesJson = JSON.stringify({ count: placeRecords.length, typeLabels, objects: placeRecords });
  const publicCityJson = JSON.stringify({ count: cityRecords.length, typeLabels, meta: { origin_atlas_km: citySource.meta.origin_atlas_km }, objects: cityRecords });
  write("atlas/current/registry/places.public.json", publicPlacesJson);
  write("atlas/current/capital/cp_objects.public.json", publicCityJson);
  write("atlas/current/viewer/atlas.html", makeAtlasViewer());
  write("atlas/current/capital/capital_plan_viewer.html", makeCapitalViewer());
  for (const relative of [
    "atlas/current/viewer/atlas-to-world.js",
    "atlas/current/viewer/terrain-3d-data.js",
    "atlas/current/viewer/terrain-3d.html",
    "atlas/current/capital/capital-3d-data.js",
    "atlas/current/capital/capital-3d-nature.js",
    "atlas/current/capital/capital-3d.html",
  ]) {
    let data = fs.readFileSync(path.join(root, relative));
    if (relative.endsWith("terrain-3d.html") || relative.endsWith("capital-3d.html")) {
      let html = data.toString("utf8");
      if (!html.includes("site-brand.css")) html = html.replace("</head>", '<link rel="stylesheet" href="../../../site-brand.css">\n</head>');
      if (!html.includes("site-brand.js")) html = html.replace("</body>", '<script src="../../../site-brand.js" defer></script>\n</body>');
      data = Buffer.from(html, "utf8");
    }
    write(relative, data);
  }
  console.log(`Public geography updated in place: ${placeRecords.length} atlas places, ${cityRecords.length} Larpington objects.`);
  process.exit(0);
}

if (path.resolve(output) !== path.join(root, "public")) throw new Error("Refusing to clear a path outside the generated public directory.");
if (fs.existsSync(output)) {
  const existingOutput = fs.lstatSync(output);
  if (!existingOutput.isDirectory() || existingOutput.isSymbolicLink()) throw new Error("Refusing to clear a non-directory or linked public output path.");
  fs.rmSync(output, { recursive: true, force: true });
}
fs.mkdirSync(output, { recursive: true });
for (const relative of ["index.html", "site.js", "site.css", "site-brand.css", "site-brand.js", "gallery.js", "encyclopedia.js", "project-meta.js", "project-metadata.json", "Larpidie logo.png"]) copy(relative);
let publicHome = read("index.html")
  .replace(/\s*<script src="scripts\/dev_media_status\.js" defer><\/script>/, "")
  .replace(/<button\b(?=[^>]*\bclass=["'][^"']*\bmedia-status-trigger\b)[^>]*>[\s\S]*?<\/button\s*>/i, "")
  .replace(/<dialog\b(?=[^>]*\bclass=["'][^"']*\bmedia-status-dialog\b)[^>]*>[\s\S]*?<\/dialog\s*>/i, "")
  .replace('data-gallery-mode="source"', 'data-gallery-mode="public"');
write("index.html", publicHome.replace(/[ \t]+(?=\r?$)/gm, ""));
const contentRoot = path.join(root, "content/larpidia");
function copyArticles(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, entry.name);
    const relative = path.relative(root, absolute);
    if (entry.isDirectory()) copyArticles(absolute);
    else if (entry.name.endsWith(".md")) copy(relative);
  }
}
for (const relative of ["content/larpidia/index.json", "content/larpidia/facts.json"]) copy(relative);
copyArticles(contentRoot);
const media = readJson("content/larpidia/media/assets.json");
write("content/larpidia/media/assets.json", JSON.stringify({ assets: media.assets.filter((asset) => asset.public && asset.exists).map((asset) => ({
  id: asset.id,
  src: asset.publicSrc || asset.src,
  alt: asset.alt,
  caption: asset.caption,
  article: asset.article,
  kind: asset.kind,
  gallery: asset.gallery === true,
  ...(asset.gallery === true ? { title: asset.galleryTitle || asset.title || asset.id } : {}),
})) }));
for (const asset of media.assets.filter((item) => item.public && item.exists)) {
  const destination = asset.publicSrc || asset.src;
  if (!destination || path.isAbsolute(destination) || destination.split(/[\\/]/).includes("..")) throw new Error(`Unsafe public media path for ${asset.id}.`);
  copy(asset.src, destination);
}
copy("atlas/current/renders/S-00_overview.jpg");
copy("atlas/current/renders/S-00_overview_clouds.jpg");
copy("atlas/current/renders/S-01_base.jpg");
copy("atlas/current/renders/S-01_base_clouds.jpg");
copy("atlas/current/renders/S-02_base.jpg");
copy("atlas/current/renders/S-03_base.jpg");
copy("atlas/current/capital/capital_plan_base.png");
copy("atlas/current/viewer/terrain-3d-data.js");
copy("atlas/current/viewer/island-r1-3d-data.js");
copy("atlas/current/viewer/terrain-3d.html");
copy("atlas/current/capital/capital-3d-data.js");
copy("atlas/current/capital/capital-3d-nature.js");
copy("atlas/current/capital/capital-3d.html");
const placeSource = readJson("atlas/current/registry/places.json");
const citySource = readJson("atlas/current/capital/cp_objects.json");
const cityViewerSource = read("templates/capital_plan_viewer_template.html");
const embeddedCityRegistry = cityViewerSource.match(/<script\b(?=[^>]*\bid="reg")(?=[^>]*\btype="application\/json")[^>]*>([\s\S]*?)<\/script>/);
if (!embeddedCityRegistry || JSON.stringify(JSON.parse(embeddedCityRegistry[1])) !== JSON.stringify(citySource)) {
  throw new Error("The embedded city plan registry is out of sync with cp_objects.json. Run scripts/sync_capital_registry.mjs.");
}
const placeRecords = makePublicRecords(placeSource);
const cityRecords = makePublicRecords(citySource, true);
const typeMap = { ...typeLabels };
const publicPlacesJson = JSON.stringify({ count: placeRecords.length, typeLabels: typeMap, objects: placeRecords });
const publicCityJson = JSON.stringify({ count: cityRecords.length, typeLabels: typeMap, meta: { origin_atlas_km: citySource.meta.origin_atlas_km }, objects: cityRecords });
const publicAtlasHtml = makeAtlasViewer();
const publicCapitalHtml = makeCapitalViewer();
write("atlas/current/registry/places.public.json", publicPlacesJson);
write("atlas/current/capital/cp_objects.public.json", publicCityJson);
write("atlas/current/viewer/atlas.html", publicAtlasHtml);
write("atlas/current/capital/capital_plan_viewer.html", publicCapitalHtml);
writeSource("atlas/current/registry/places.public.json", publicPlacesJson);
writeSource("atlas/current/capital/cp_objects.public.json", publicCityJson);
writeSource("atlas/current/viewer/atlas.html", publicAtlasHtml);
writeSource("atlas/current/capital/capital_plan_viewer.html", publicCapitalHtml);
for (const relative of ["atlas/current/viewer/terrain-3d.html", "atlas/current/capital/capital-3d.html"]) {
  let html = read(relative);
  const prefix = "../../../";
  if (!html.includes("site-brand.css")) html = html.replace("</head>", `<link rel="stylesheet" href="${prefix}site-brand.css">\n</head>`);
  if (!html.includes("site-brand.js")) html = html.replace("</body>", `<script src="${prefix}site-brand.js" defer></script>\n</body>`);
  write(relative, html);
}
for (const relative of ["atlas/current/svg/transport_preview_embedded.svg", "atlas/current/svg/rail_scheme.svg", "atlas/current/svg/landcover_preview.svg"]) {
  write(relative, publicSvg(read(relative)));
}
const ids = (list) => list.map((item) => item.id).sort();
if (placeRecords.length !== 159 || cityRecords.length !== 662) throw new Error(`Registry count mismatch: ${placeRecords.length}/159 places, ${cityRecords.length}/662 city objects.`);
if (new Set(ids(placeRecords)).size !== 159 || new Set(ids(cityRecords)).size !== 662) throw new Error("Public registry contains duplicate IDs.");
if (ids(placeRecords).join("\n") !== ids(placeSource.objects).join("\n") || ids(cityRecords).join("\n") !== ids(citySource.objects).join("\n")) throw new Error("A source registry object is missing from the public projection.");
if (placeRecords.some((item) => "notes" in item || "photo_guide" in item || "bible_ref" in item || "exist_status" in item || "name_status" in item || "pos_status" in item)) throw new Error("Private atlas fields leaked into a public place record.");
if (cityRecords.some((item) => "notes" in item || "photo_guide" in item || "bible_ref" in item || "exist_status" in item || "name_status" in item || "pos_status" in item)) throw new Error("Private city fields leaked into a public city record.");
if (cityRecords.find((item) => item.id === "CP-B01")?.name_cs !== "Radnice Larpingtonu") throw new Error("The public city registry does not use the approved town hall name.");
console.log(`Public site built in public/: ${placeRecords.length} atlas places, ${cityRecords.length} Larpington objects.`);
