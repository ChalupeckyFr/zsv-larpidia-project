import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "public");
const read = (relative) => fs.readFileSync(path.join(root, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));
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
const publicPlaceName = (record, kind, capital = false) => {
  if (capital && record.id === "CP-B01") return "Radnice Larpingtonu";
  if (record.id === "M-01") return "Nejvyšší vrchol (přibližně 560 m n. m.)";
  if (capital && record.name_status === "approved" && record.name_cs) {
    return String(record.name_cs).replace(/\s*\([^)]*(?:pracovní|návrh)[^)]*\)/gi, "").trim();
  }
  if (!capital && record.name_status === "approved" && record.name_cs) {
    return String(record.name_cs).replace(/\s*\([^)]*(?:pracovní|návrh)[^)]*\)/gi, "").trim();
  }
  const label = typeLabels[kind] || typeLabels.default;
  if (capital) return `${label} · Larpington`;
  return `${label} · ${regionLabel(record.region)}`;
};
const makePublicRecords = (source, capital = false) => source.objects.map((record) => {
  const kind = kindOf(record);
  const publicRecord = {
    id: String(record.id),
    name_cs: publicPlaceName(record, kind, capital),
    typeKey: kind,
    typeLabel: typeLabels[kind] || typeLabels.default,
    islandKey: String(record.island || (capital ? "main" : "main")),
    islandLabel: islandLabels[String(record.island || "main")] || "ostrovní oblast",
    region: regionLabel(record.region),
  };
  for (const key of capital ? ["u", "v", "x_km", "y_km"] : ["x_km", "y_km"]) {
    if (Number.isFinite(record[key])) publicRecord[key] = record[key];
  }
  if (!capital && record.id === "M-01") publicRecord.elevationLabel = "Přibližně 560 m n. m.";
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
  if (a < 0 || b < 0) throw new Error(`Public viewer template marker missing: ${start}`);
  return `${source.slice(0, a)}${replacement}${source.slice(b)}`;
}

function replaceWholeLine(source, marker, replacement) {
  const start = source.indexOf(marker);
  if (start < 0) throw new Error(`Public viewer function missing: ${marker}`);
  const end = source.indexOf("\n", start);
  if (end < 0) throw new Error(`Public viewer function line is incomplete: ${marker}`);
  return `${source.slice(0, start)}${replacement}${source.slice(end)}`;
}

function makeAtlasViewer() {
  let html = sanitizeViewerMarkup(read("atlas/current/viewer/atlas.html"), { title: "Atlas Larpidie", kind: "atlas" });
  html = html
    .replace('<header><h1>Atlas Larpidie a Paralandu</h1><span class="badge">NÁVRH · v1.0-draft</span>', '<header><h1>Atlas Larpidie</h1>')
    .replace('<aside class="l"><h2>Hledat místo</h2><input id="q" type="search" placeholder="ID nebo název (např. N-03, přístav, Aokawa)"><div id="results"></div>', `<aside class="l" id="search-panel"><h2>Najít místo</h2><label for="q">Hledat</label><input id="q" type="search" placeholder="Hledat místo, oblast nebo ID…" autocomplete="off"><label for="island-filter">Ostrov</label><select id="island-filter"><option value="">Všechny ostrovy</option><option value="main">Hlavní ostrov</option><option value="para">Paraland</option></select><label for="type-filter">Typ</label><select id="type-filter"><option value="">Všechny typy</option></select><div class="search-actions"><button class="small" id="clear-filters" type="button">Vymazat filtry</button><button class="small mobile-close" id="close-search" type="button">Zavřít</button></div><p id="search-count" role="status" aria-live="polite">Zadejte název nebo zvolte filtr.</p><div id="results" role="listbox" aria-label="Výsledky hledání"></div>`)
    .replace('<div id="map"><svg', '<div id="map"><button id="open-search" class="mobile-search-trigger" type="button" aria-expanded="false" aria-controls="search-panel">Hledat místa</button><svg')
    .replace('<h2>Ovládání mapy</h2><label class="row"><input type="checkbox" id="status"> Barvy podle stavu údajů</label><button class="small" id="reset">Zobrazit celou mapu</button>', '<h2>Ovládání mapy</h2><button class="small" id="reset">Zobrazit celou mapu</button>')
    .replace('Zobrazí se stav, poloha, modelová výška a případné foto či video vodítko.', 'Zobrazí se stručný popis místa a jeho orientační poloha.')
    .replace(/<span class="legend-item"><i class="legend-swatch approved"><\/i>Schválený základ<\/span><span class="legend-item"><i class="legend-swatch proposed"><\/i>Pracovní návrh<\/span><span class="legend-item"><i class="legend-swatch needs_decision"><\/i>Čeká na rozhodnutí<\/span>/, "")
    .replace('<section class="side-section"><h2>Legenda</h2><div class="legend">', '<section class="side-section"><h2>Legenda</h2><p>Mapa je orientační; poloha a některé názvy jsou zobrazeny schematicky.</p><div class="legend">')
    .replace('<footer><span id="coord">–</span><span id="count"></span></footer>', '<footer><span id="coord">Orientační fikční mapa</span><span id="count"></span><span data-project-footer></span></footer>');
  html = html.replace("</style>", `
.mobile-search-trigger{display:none}.mobile-close{display:none}#search-panel label{display:block;margin:.55rem 0 .2rem;color:var(--soft);font-size:.86rem;font-weight:650}#search-panel select,#search-panel input[type=search]{width:100%;min-height:2.5rem;padding:.45rem .6rem;border:1px solid var(--line);border-radius:7px;background:var(--card);color:var(--ink);font:inherit}.search-actions{display:flex;gap:.45rem;margin:.55rem 0}.result-card{display:block;width:100%;margin:.35rem 0;padding:.65rem .7rem;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);text-align:left;cursor:pointer}.result-card:hover,.result-card[aria-selected=true]{border-color:var(--acc);background:color-mix(in srgb,var(--acc) 9%,var(--card))}.result-title,.result-meta,.result-id{display:block}.result-title{font-weight:700}.result-meta{margin-top:.2rem;color:var(--soft);font-size:.85rem}.result-id{margin-top:.2rem;color:var(--acc);font-size:.76rem;font-variant-numeric:tabular-nums}#search-count{margin:.55rem 0;color:var(--soft);font-size:.85rem}
@media(max-width:1000px){body{grid-template-columns:minmax(0,1fr);grid-template-rows:auto minmax(48vh,1fr) auto auto}header{grid-row:1}#map{grid-column:1;grid-row:2;min-height:48vh}aside.r{grid-column:1;grid-row:3;max-height:30vh;overflow:auto}body>footer{grid-column:1;grid-row:4}#search-panel{position:fixed;z-index:60;inset:0 auto 0 0;width:min(88vw,360px);height:100dvh;max-height:100dvh;overflow:auto;transform:translateX(-105%);transition:transform .22s ease;box-shadow:0 0 28px #0005}body.search-open #search-panel{transform:translateX(0)}.mobile-search-trigger{display:inline-flex;position:absolute;z-index:20;top:12px;left:12px;align-items:center;padding:.6rem .8rem;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font:inherit;font-weight:700;box-shadow:0 2px 8px #0002}.mobile-close{display:inline-flex}}
@media(prefers-reduced-motion:reduce){#search-panel{transition:none}}
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
function selectResult(id){const o=BYID[id];if(!o)return;selectedId=id;search();zoomTo(o);show(id);closeSearch()}
function closeSearch(){document.body.classList.remove('search-open');document.getElementById('open-search').setAttribute('aria-expanded','false')}
document.getElementById('open-search').addEventListener('click',()=>{document.body.classList.add('search-open');document.getElementById('open-search').setAttribute('aria-expanded','true');q.focus()});document.getElementById('close-search').addEventListener('click',closeSearch);
document.getElementById('clear-filters').addEventListener('click',()=>{q.value='';islandFilter.value='';typeFilter.value='';search();q.focus()});q.addEventListener('input',search);islandFilter.addEventListener('change',search);typeFilter.addEventListener('change',search);
res.addEventListener('click',e=>{const button=e.target.closest('button[data-id]');if(button)selectResult(button.dataset.id)});q.addEventListener('keydown',e=>{const cards=[...res.querySelectorAll('button[data-id]')];if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(!cards.length)return;activeResult=(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;cards[activeResult].focus()}else if(e.key==='Enter'){const target=e.target.closest('button[data-id]');const id=target?.dataset.id||cards[Math.max(0,activeResult)]?.dataset.id;if(id){e.preventDefault();selectResult(id)}}else if(e.key==='Escape'){closeSearch();q.blur()}});res.addEventListener('keydown',e=>{if(e.key==='Escape'){closeSearch();q.focus()}});search();
`);
  html = html.replace("document.getElementById('status').onchange=e=>svg.classList.toggle('status-mode',e.target.checked);", "");
  html = html.replace("['pracovní','proposed']", "");
  html = html.replace("res.addEventListener('keydown',e=>{if(e.key==='Escape'){closeSearch();q.focus()}});search();", "res.addEventListener('keydown',e=>{const cards=[...res.querySelectorAll('button[data-id]')];if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const index=cards.indexOf(e.target.closest('button[data-id]'));const next=(index+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;cards[next]?.focus()}else if(e.key==='Escape'){closeSearch();q.focus()}});search();");
  html = html.replace("activeResult=(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;", "activeResult=activeResult<0?(e.key==='ArrowDown'?0:cards.length-1):(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;");
  html = html.replace("document.getElementById('count').textContent=REG.objects.length+' objektů v registru';", "document.getElementById('count').textContent=REG.objects.length+' míst';\nconst layerLabels={ 'bg-sea':'Moře','land':'Ostrovy','coast':'Pobřeží','grid':'Souřadnicová síť','hypsometry':'Výškové pásmo','hillshade':'Reliéf','landcover':'Využití krajiny','coast-classes':'Typy pobřeží','contours':'Výškové linie','contour-labels':'Výškové popisky','hydro':'Řeky a vodstvo','settlements':'Sídla','poi':'Místa zájmu','peaks':'Horské vrcholy','roads':'Silnice','cycleways':'Cyklotrasy','trails':'Stezky','rail-L3':'Železniční linka L3','rail-L2':'Železniční linka L2','rail-L1':'Železniční linka L1','stations':'Stanice','ports':'Přístavy','airports':'Letiště','labels-areas':'Popisky oblastí','labels-cs':'České popisky','labels-ja':'Japonské popisky','labels-en':'Anglické popisky','marginalia':'Okraje mapy'};\nlp.querySelectorAll('input[data-l]').forEach(input=>{const label=input.parentElement;if(label)label.lastChild.textContent=' '+(layerLabels[input.dataset.l]||'Mapová vrstva')});\nsvg.querySelectorAll('#marginalia').forEach(el=>el.style.display='none');\nsvg.querySelectorAll('text[data-id]').forEach(el=>{const record=BYID[el.dataset.id];if(record)el.textContent=record.name_cs});");
  html = replaceWholeLine(html, "function translateMapLabel(", "function translateMapLabel(text,lang,id){return text}");
  html = html.replace(/<\/script>\s*<\/body>/, "})();\n</script><script src=\"../../../project-meta.js\" defer></script>\n</body>");
  return html;
}

function makeCapitalViewer() {
  let html = sanitizeViewerMarkup(read("atlas/current/capital/capital_plan_viewer.html"), { title: "Plán Larpingtonu", kind: "capital" });
  html = html
    .replace('<header><h1>Larpington – podklad plánu hlavního města (CP-01)</h1><span class="badge">NÁVRH · v1.0-draft</span>', '<header><h1>Plán Larpingtonu</h1>')
    .replace('placeholder="ID nebo název (např. CP-B01, parlament, tržnice)"', 'placeholder="Hledat místo, oblast nebo ID…"')
    .replace('<h2>Hledání</h2><input id="q" type="search" placeholder="Hledat místo, oblast nebo ID…"><div id="results"></div>', '<h2>Hledat místo</h2><label for="q">Hledat</label><input id="q" type="search" placeholder="Hledat místo, oblast nebo ID…"><label for="type-filter">Typ</label><select id="type-filter"><option value="">Všechny typy</option></select><button class="small" id="clear-filters" type="button">Vymazat hledání</button><div id="search-count" role="status" aria-live="polite">Zadejte název nebo zvolte filtr.</div><div id="results" role="listbox" aria-label="Výsledky hledání"></div>')
    .replace('<h2>Režim</h2><label class="row"><input type="checkbox" id="status"> Obrysy podle stavu (schváleno × návrh)</label>', '<h2>Mapové vrstvy</h2>')
    .replace('Zobrazí se stav, poloha v metrech plánu i v km atlasu a foto/video vodítko.', 'Zobrazí se stručný popis objektu a jeho poloha v plánu.')
    .replace(/<footer><span id="coord">–<\/span><span id="count"><\/span><\/footer>/, '<footer><span id="coord">Orientační plán města</span><span id="count"></span><span data-project-footer></span></footer>');
  html = html.replace("const lab=el.getAttribute('inkscape:label')||i;", "const lab=({'bg-sea':'Moře','land':'Pevnina','contours':'Výškové linie','beaches':'Pláže','grid':'Souřadnicová síť','green-wedges':'Zelené plochy','districts':'Čtvrti','blocks':'Městské bloky','spaces':'Veřejná prostranství','harbor':'Přístav','streets':'Ulice','rail-surface':'Železniční tratě','rail-L3':'Železniční linka L3','stations':'Stanice','access-route':'Přístupové trasy','houses':'Domy','buildings-key':'Budovy','poi':'Místa zájmu','future-development':'Plánované doplnění zástavby','labels-cs':'České popisky','labels-en':'Anglické popisky','labels-ja':'Japonské popisky','marginalia':'Okraje mapy'})[i]||i;");
  html = html.replace(/<script>\s*const svg=document\.querySelector\('#map svg'\);const REG=JSON\.parse\(document\.getElementById\('reg'\)\.textContent\);const BYID=Object\.fromEntries\(REG\.objects\.map\(o=>\[o\.id,o\]\)\);/, "<script>\n(async()=>{\nconst svg=document.querySelector('#map svg');const REG=await (await fetch('cp_objects.public.json')).json();const BYID=Object.fromEntries(REG.objects.map(o=>[o.id,o]));");
  html = html.replace(/function stBadge\(k,v\)\{[\s\S]*?function addFutureDevelopment/, `function show(id){const o=BYID[id];const box=document.getElementById('info');if(!o){box.textContent='Objekt se nepodařilo najít.';return}highlight(id);const labels=svg.querySelectorAll('text[data-id="'+CSS.escape(o.id)+'"]');labels.forEach(el=>el.textContent=o.name_cs);let h='<h3>'+esc(o.name_cs)+'</h3><p>'+esc(o.typeLabel)+' · '+esc(o.islandLabel)+'</p><p>'+esc(o.region)+' · orientační poloha</p>';if(Number.isFinite(o.u)&&Number.isFinite(o.v))h+='<p>Plán: '+Math.round(o.u)+' × '+Math.round(o.v)+' m</p>';h+='<p><button class="small" data-zoom-id="'+esc(o.id)+'">Zobrazit na mapě</button></p>';box.innerHTML=h}\ndocument.getElementById('info').addEventListener('click',e=>{const b=e.target.closest('[data-zoom-id]');if(b&&BYID[b.dataset.zoomId])zoomTo(BYID[b.dataset.zoomId])});\nfunction addFutureDevelopment`);
  html = html
    .replace("layer.setAttribute('inkscape:label','Návrh budoucí zástavby v rezervě')", "layer.setAttribute('inkscape:label','Plánované doplnění zástavby')")
    .replace("layer.setAttribute('aria-label','Schematické budoucí domy v dosud nezastavěných blocích')", "layer.setAttribute('aria-label','Ilustrativní budovy plánované k doplnění')")
    .replace("node.setAttribute('data-proposed','true');", "");
  html = replaceSection(html, "const q=document.getElementById('q'),res=document.getElementById('results');", "document.getElementById('count').textContent=", `const q=document.getElementById('q'),res=document.getElementById('results'),count=document.getElementById('search-count'),typeFilter=document.getElementById('type-filter');const searchable=REG.objects.filter(o=>Number.isFinite(o.u)&&Number.isFinite(o.v));let activeResult=-1,selectedId=null;const normalize=value=>String(value??'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLocaleLowerCase('cs-CZ').trim();const typeKeys=[...new Set(searchable.map(o=>o.typeKey))].sort((a,b)=>REG.typeLabels[a].localeCompare(REG.typeLabels[b],'cs'));typeKeys.forEach(key=>{const option=document.createElement('option');option.value=key;option.textContent=REG.typeLabels[key];typeFilter.appendChild(option)});function search(){const terms=normalize(q.value).split(/\\s+/).filter(Boolean);let hits=searchable.filter(o=>!typeFilter.value||o.typeKey===typeFilter.value);if(terms.length)hits=hits.filter(o=>{const hay=normalize([o.id,o.name_cs,o.typeLabel,o.islandLabel,o.region].join(' '));return terms.every(term=>hay.includes(term))});hits.sort((a,b)=>{const score=o=>normalize(o.id)===normalize(q.value)?0:normalize(o.name_cs)===normalize(q.value)?1:normalize(o.name_cs).startsWith(normalize(q.value))?2:3;return score(a)-score(b)||a.name_cs.localeCompare(b.name_cs,'cs')||a.id.localeCompare(b.id)});activeResult=-1;res.replaceChildren();const shown=hits.slice(0,60);count.textContent=hits.length?hits.length+\" objektů\"+(hits.length>shown.length?\", zobrazeno prvních \"+shown.length:\"\"):\"Žádný odpovídající objekt jsme nenašli.\";for(const o of shown){const button=document.createElement('button');button.type='button';button.className='result-card';button.setAttribute('role','option');button.setAttribute('aria-selected',String(o.id===selectedId));button.dataset.id=o.id;button.innerHTML='<span class="result-title">'+esc(o.name_cs)+'</span><span class="result-meta">'+esc(o.typeLabel)+' · '+esc(o.islandLabel)+' · '+esc(o.region)+'</span><span class="result-id">'+esc(o.id)+'</span>';res.appendChild(button)}}function selectResult(id){const o=BYID[id];if(!o)return;selectedId=id;search();zoomTo(o);show(id)}q.addEventListener('input',search);typeFilter.addEventListener('change',search);document.getElementById('clear-filters').addEventListener('click',()=>{q.value='';typeFilter.value='';search();q.focus()});res.addEventListener('click',e=>{const button=e.target.closest('button[data-id]');if(button)selectResult(button.dataset.id)});q.addEventListener('keydown',e=>{const cards=[...res.querySelectorAll('button[data-id]')];if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(!cards.length)return;activeResult=(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;cards[activeResult].focus()}else if(e.key==='Enter'){const target=e.target.closest('button[data-id]');const id=target?.dataset.id||cards[Math.max(0,activeResult)]?.dataset.id;if(id){e.preventDefault();selectResult(id)}}else if(e.key==='Escape'){q.value='';search()}});res.addEventListener('keydown',e=>{if(e.key==='Escape'){q.focus()}});search();
`);
  html = html.replace("document.getElementById('status').onchange=e=>svg.classList.toggle('status-mode',e.target.checked);", "");
  html = html.replace("res.addEventListener('keydown',e=>{if(e.key==='Escape'){q.focus()}});search();", "res.addEventListener('keydown',e=>{const cards=[...res.querySelectorAll('button[data-id]')];if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const index=cards.indexOf(e.target.closest('button[data-id]'));const next=(index+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;cards[next]?.focus()}else if(e.key==='Escape'){q.focus()}});search();");
  html = html.replace("activeResult=(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;", "activeResult=activeResult<0?(e.key==='ArrowDown'?0:cards.length-1):(activeResult+(e.key==='ArrowDown'?1:-1)+cards.length)%cards.length;");
  html = html.replace("document.getElementById('count').textContent=REG.objects.length+' objektů v registru plánu';", "document.getElementById('count').textContent=REG.objects.length+' objektů';\nsvg.querySelectorAll('text[data-id]').forEach(el=>{const record=BYID[el.dataset.id];if(record)el.textContent=record.name_cs});\n");
  html = html.replace(/<\/script>\s*<\/body>/, "})();\n</script><script src=\"../../../project-meta.js\" defer></script>\n</body>");
  return html;
}

if (path.resolve(output) !== path.join(root, "public")) throw new Error("Refusing to clear a path outside the generated public directory.");
if (fs.existsSync(output)) {
  const existingOutput = fs.lstatSync(output);
  if (!existingOutput.isDirectory() || existingOutput.isSymbolicLink()) throw new Error("Refusing to clear a non-directory or linked public output path.");
  fs.rmSync(output, { recursive: true, force: true });
}
fs.mkdirSync(output, { recursive: true });
for (const relative of ["index.html", "site.js", "site.css", "encyclopedia.js", "project-meta.js", "project-metadata.json", "Larpidie logo.png"]) copy(relative);
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
write("content/larpidia/media/assets.json", JSON.stringify({ assets: media.assets.map(({ id, src, alt, caption, article, kind }) => ({ id, src, alt, caption, article, kind })) }));
copy("atlas/current/renders/S-00_overview.jpg");
copy("atlas/current/renders/S-00_overview_clouds.jpg");
copy("atlas/current/renders/S-01_base.jpg");
copy("atlas/current/renders/S-01_base_clouds.jpg");
copy("atlas/current/renders/S-02_base.jpg");
copy("atlas/current/renders/S-03_base.jpg");
copy("atlas/photography/photos/LAR_PH_001.jpg");
copy("atlas/current/capital/capital_plan_base.png");
copy("atlas/current/viewer/terrain-3d-data.js");
copy("atlas/current/viewer/island-r1-3d-data.js");
copy("atlas/current/viewer/terrain-3d.html");
copy("atlas/current/capital/capital-3d-data.js");
copy("atlas/current/capital/capital-3d-nature.js");
copy("atlas/current/capital/capital-3d.html");
const placeSource = readJson("atlas/current/registry/places.json");
const citySource = readJson("atlas/current/capital/cp_objects.json");
const cityViewerSource = read("atlas/current/capital/capital_plan_viewer.html");
const embeddedCityRegistry = cityViewerSource.match(/<script\b(?=[^>]*\bid="reg")(?=[^>]*\btype="application\/json")[^>]*>([\s\S]*?)<\/script>/);
if (!embeddedCityRegistry || JSON.stringify(JSON.parse(embeddedCityRegistry[1])) !== JSON.stringify(citySource)) {
  throw new Error("The embedded city plan registry is out of sync with cp_objects.json. Run scripts/sync_capital_registry.mjs.");
}
const placeRecords = makePublicRecords(placeSource);
const cityRecords = makePublicRecords(citySource, true);
const typeMap = Object.fromEntries(Object.entries(typeLabels).filter(([key]) => key !== "default"));
write("atlas/current/registry/places.public.json", JSON.stringify({ count: placeRecords.length, typeLabels: typeMap, objects: placeRecords }));
write("atlas/current/capital/cp_objects.public.json", JSON.stringify({ count: cityRecords.length, typeLabels: typeMap, meta: { origin_atlas_km: citySource.meta.origin_atlas_km }, objects: cityRecords }));
write("atlas/current/viewer/atlas.html", makeAtlasViewer());
write("atlas/current/capital/capital_plan_viewer.html", makeCapitalViewer());
for (const relative of ["atlas/current/svg/transport_preview_embedded.svg", "atlas/current/svg/rail_scheme.svg", "atlas/current/svg/landcover_preview.svg"]) {
  write(relative, publicSvg(read(relative)));
}
for (const [source, destination] of [
  ["v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_01.png", "gallery/assets/mountain.png"],
  ["v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/01_PHOTOS/PHOTO_06.png", "gallery/assets/paraland.png"],
]) copy(source, destination);

const ids = (list) => list.map((item) => item.id).sort();
if (placeRecords.length !== 159 || cityRecords.length !== 662) throw new Error(`Registry count mismatch: ${placeRecords.length}/159 places, ${cityRecords.length}/662 city objects.`);
if (new Set(ids(placeRecords)).size !== 159 || new Set(ids(cityRecords)).size !== 662) throw new Error("Public registry contains duplicate IDs.");
if (ids(placeRecords).join("\n") !== ids(placeSource.objects).join("\n") || ids(cityRecords).join("\n") !== ids(citySource.objects).join("\n")) throw new Error("A source registry object is missing from the public projection.");
if (placeRecords.some((item) => "notes" in item || "photo_guide" in item || "bible_ref" in item || "exist_status" in item || "name_status" in item || "pos_status" in item)) throw new Error("Private atlas fields leaked into a public place record.");
if (cityRecords.some((item) => "notes" in item || "photo_guide" in item || "bible_ref" in item || "exist_status" in item || "name_status" in item || "pos_status" in item)) throw new Error("Private city fields leaked into a public city record.");
if (cityRecords.find((item) => item.id === "CP-B01")?.name_cs !== "Radnice Larpingtonu") throw new Error("The public city registry does not use the approved town hall name.");
console.log(`Public site built in public/: ${placeRecords.length} atlas places, ${cityRecords.length} Larpington objects.`);
