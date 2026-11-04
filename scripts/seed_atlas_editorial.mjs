import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputPath = path.join(root, "content/larpidia/atlas_places_editorial.json");
if (fs.existsSync(outputPath)) throw new Error(`${path.relative(root, outputPath)} already exists; refusing to overwrite editorial work.`);

const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));
const atlasSource = readJson("atlas/current/registry/places.json").objects;
const capitalSource = readJson("atlas/current/capital/cp_objects.json").objects;
const streets = readJson("atlas/current/capital/cp_streets_atlas_km.geojson").features;
const districtsGeo = readJson("atlas/current/capital/cp_districts_atlas_km.geojson").features;
const byAtlasId = new Map(atlasSource.map((record) => [record.id, record]));
const byCapitalId = new Map(capitalSource.map((record) => [record.id, record]));

const atlasNames = {
  "M-01": { name: "Larpova hora", en: "Mount Larp", ja: "ラープ山", reason: "Pojmenování vychází z označení Larp/Mount Larp v geografických datech; výška zůstává přibližná." },
  "M-02": { name: "Zimní hora", en: "Winter Peak", ja: "冬山", reason: "České jméno odpovídá existujícímu anglickému a japonskému názvu a zimnímu zaměření místa." },
  "M-03": { name: "Kulatý vrch", en: "Round Hill", ja: "丸山", reason: "Zachovává popsaný zaoblený tvar a turistické využití." },
  "V-02": { name: "Vyhlídka pod Larpovou horou", reason: "Poloha leží pod M-01; stabilní ID zůstává v datech." },
  "C-01": { name: "Larpington", en: "Larpington", ja: "ラープトン", reason: "Hlavní město podle platného kánonu." },
  "T-01": { name: "Praha", en: "Prague", ja: "プラハ", reason: "Název a překlady podle existujícího schváleného pojmenování." },
  "T-02": { name: "Cimprlichovo Hradiště", ja: "チンプルリフ砦", aliases: ["Cimpřichovo Hradiště"], reason: "Přesné jméno podle nového výslovného rozhodnutí autora; starší chybný zápis zůstává aliasem pro hledání." },
  "T-03": { name: "Havlišovo Doupě", en: "Havliš's Den", ja: "ハヴリシュの巣", reason: "Zachování čitelného místního názvu z registru." },
  "T-04": { name: "Ōru Maito", ja: "オールマイト", reason: "Zachování místního romanizovaného jména; japonský zápis je v registru." },
  "T-05": { name: "Aokawa", ja: "青川", reason: "Zachování místního jména a japonského zápisu z registru." },
  "T-06": { name: "Hoshimachi", ja: "星町", reason: "Zachování místního jména a japonského zápisu z registru." },
  "HM-01": { name: "Úvalí u Prahy", reason: "Nové střídmé jméno osady v nížině; její poloha je u Prahy ověřena souřadnicemi." },
  "HM-02": { name: "Vodní Dvory", reason: "Nové místní jméno osady u vodopádu a přehradní oblasti; vazba vychází ze souřadnic." },
  "HM-03": { name: "Letištní Dvory", reason: "Nové orientační jméno osady v blízkosti regionálního letiště; bez tvrzení o jeho funkční závislosti." },
  "HM-04": { name: "Sadová Lhota", reason: "Nové střídmé místní jméno osady v severní nížinné části ostrova." },
  "HM-05": { name: "Západní Předměstí", reason: "Nové orientační jméno osady na západním okraji larpingtonské oblasti." },
  "HM-06": { name: "Hájov", reason: "Nové krátké místní jméno osady na přechodu nížiny a západní krajiny." },
  "PL-01": { name: "Staré město Paralandu", reason: "Z registru očištěné označení historického sídla." },
  "PL-03": { name: "Jižní letovisko Paralandu", reason: "Očištěno a gramaticky sjednoceno podle polohy a typu v registru." },
  "PL-05": { name: "Přístavní vesnice Paralandu", reason: "Očištěno a sjednoceno podle typu místa a polohy." },
  "B-01": { name: "Západní pláž Larpingtonského zálivu", reason: "Odlišeno podle souřadnic a blízké zátoky." },
  "B-02": { name: "Východní pláž Larpingtonského zálivu", reason: "Odlišeno podle souřadnic a blízké zátoky." },
  "B-03": { name: "Pláž Hoshimachi", reason: "Poloha při severním sídle Hoshimachi." },
  "B-04": { name: "Pláž na jihovýchodním poloostrově", reason: "Poloha na pobřežním poloostrově podle mapových souřadnic." },
  "B-05": { name: "Pláž u mariny Paralandu", reason: "Poloha v pobřežním okolí mariny podle mapových souřadnic." },
  "B-06": { name: "Jižní pláž Paralandu", reason: "Odlišeno podle polohy na jižním pobřeží ostrova." },
  "W-01": { name: "Řeka Larp", en: "Larp River", ja: "ラープ川", reason: "Český název podle explicitního návrhu v registru a navazujících geografických dat." },
  "W-02": { name: "Aokawa", en: "Aokawa River", ja: "青川", reason: "Zachovává místní jméno toku; odlišuje se od sídla Aokawa typem v kartě." },
  "W-03": { name: "Severní potok", en: "North Brook", ja: "北の小川", reason: "Zachovává popisný název z registru." },
  "W-04": { name: "Havlišův potok", en: "Havliš Brook", ja: "ハヴリシュ川", reason: "Očištěný český název z návrhu v registru." },
  "W-05": { name: "Pražský potok", en: "Praha Brook", ja: "プラハ川", reason: "Očištěný český název z návrhu v registru." },
  "W-06": { name: "Severní potok Paralandu", en: "Paraland North Brook", ja: "パラランド北川", reason: "Očištěný název toku na Paralandu." },
  "W-07": { name: "Jižní potok Paralandu", en: "Paraland South Brook", ja: "パラランド南川", reason: "Očištěný název toku na Paralandu." },
  L1: { name: "Horská železniční linka", reason: "Veřejný český název podle schválené horské funkce L1." },
  L2: { name: "Historická elektrická linka", reason: "Veřejný český název podle schválené elektrické dráhy L2 v historickém stylu." },
  L3: { name: "Městská rychlá linka", reason: "Popisuje provozní městský úsek bez tvrzení, že podmořská část na Paraland je otevřená." },
  "FERRY-1": { name: "Lodní spojení Larpington–Paraland", reason: "Zpřístupňuje současný lodní/traťový záměr jménem ostrovů; neimplikuje přepravu automobilů." },
  "SK-02": { name: "Vlek na Zimní horu", reason: "Očištěný název podle polohy u M-02; forma zůstává obecná." },
};

const regionNames = {
  west_northwest: "západní horská oblast hlavního ostrova",
  central_west: "západní vnitrozemí hlavního ostrova",
  central_lowland: "centrální nížina hlavního ostrova",
  south_southeast: "jižní část hlavního ostrova",
  southeast_offshore: "ostrov Paraland a jeho okolí",
  north: "severní část hlavního ostrova",
  east_northeast: "východní část hlavního ostrova",
  east: "východní část hlavního ostrova",
  west: "západní část hlavního ostrova",
  south: "jižní část hlavního ostrova",
  center: "střed hlavního ostrova",
};

const typeLabels = {
  settlement: "Sídlo", peak: "Hora", mountain: "Hora", nature: "Přírodní místo", poi: "Místo v krajině",
  district: "Městská čtvrť", port: "Přístav", rail_station: "Železniční stanice", rail_line: "Železniční linka",
  road: "Silnice", trail: "Pěší stezka", cycleway: "Cyklotrasa", river: "Vodní tok", coast_feature: "Pobřežní útvar",
  infrastructure: "Vodní stavba", industry: "Průmyslová oblast", airport: "Letiště", other_line: "Dopravní trasa",
};

const typeLabel = (record) => {
  const subtype = String(record.subtype || "").toLowerCase();
  if (subtype.includes("spring")) return "Pramen";
  if (subtype.includes("viewpoint")) return "Vyhlídka";
  if (subtype.includes("beach")) return "Pláž";
  if (subtype.includes("waterfall")) return "Vodopád";
  if (subtype.includes("castle")) return "Hradní areál";
  if (subtype.includes("ruin")) return "Zřícenina";
  if (subtype.includes("lighthouse")) return "Maják";
  if (subtype.includes("ski")) return subtype.includes("run") ? "Sjezdovka" : "Lyžařský vlek";
  if (subtype.includes("ferry")) return "Lodní spojení";
  if (record.type === "settlement") return ({ capital: "Hlavní město", town: "Město", old_town: "Historické sídlo", resort: "Letovisko", village: "Vesnice", hamlet: "Osada" })[subtype] || "Sídlo";
  return typeLabels[record.type] || "Místo v krajině";
};

const cleanSourceName = (value) => String(value || "")
  .replace(/\s*\([^)]*(?:pracovní|prac\.|návrh|proposed)[^)]*\)/gi, "")
  .replace(/\s*[,–—-]?\s*(?:pracovní|prac\.|návrh|proposed)\b.*$/i, "")
  .replace(/\s+/g, " ").trim();

const distance = (a, b) => Math.hypot(Number(a.x_km) - Number(b.x_km), Number(a.y_km) - Number(b.y_km));
const bearing = (a, b) => {
  const dx = Number(b.x_km) - Number(a.x_km), dy = Number(b.y_km) - Number(a.y_km);
  const labels = ["severně", "severovýchodně", "východně", "jihovýchodně", "jižně", "jihozápadně", "západně", "severozápadně"];
  return labels[Math.round((Math.atan2(dx, -dy) * 180 / Math.PI + 360) % 360 / 45) % 8];
};
const nearest = (record, items, limit = 3) => items.filter((other) => other.id !== record.id && Number.isFinite(other.x_km) && Number.isFinite(other.y_km))
  .map((other) => ({ record: other, distance_km: distance(record, other) }))
  .sort((a, b) => a.distance_km - b.distance_km || String(a.record.id).localeCompare(String(b.record.id)))
  .slice(0, limit);

const rawAtlasName = (record) => {
  const override = atlasNames[record.id];
  if (override) return override.name;
  let name = cleanSourceName(record.name_cs);
  if ((!name || /^osada\s*\(bez názvu\)$/i.test(name)) && record.name_proposed?.cs) name = cleanSourceName(record.name_proposed.cs);
  if (/^osada\s*\(bez názvu\)$/i.test(name)) return `Osada v ${regionNames[record.region] || "ostrovní krajině"}`;
  name = name.replace(/\bM-01\b/g, "Larpova hora").replace(/\bM-02\b/g, "Zimní hora").replace(/\bC-01\b/g, "Larpington");
  return name || `${typeLabel(record)} v ${regionNames[record.region] || "ostrovní krajině"}`;
};

const atlasPublicNames = Object.fromEntries(atlasSource.map((record) => [record.id, rawAtlasName(record)]));
const islandLabel = (record) => record.island === "para" ? "Paralandu" : "hlavního ostrova";
const compassDistance = (entry) => `${entry.direction} · ${entry.distance_km < 1 ? `${Math.round(entry.distance_km * 1000)} m` : `${entry.distance_km.toFixed(1).replace(".", ",")} km`}`;

function atlasDescription(record, near) {
  const name = atlasPublicNames[record.id];
  const area = regionNames[record.region] || "ostrovní krajině";
  const first = near[0]?.record;
  const second = near[1]?.record;
  const around = first && second ? `V okolí leží ${atlasPublicNames[first.id]} a ${atlasPublicNames[second.id]}.`
    : first ? `V okolní krajině se nachází také ${atlasPublicNames[first.id]}.` : "Je součástí orientační mapy souostroví.";
  const kind = String(record.type || "").toLowerCase();
  const sub = String(record.subtype || "").toLowerCase();
  if (record.id === "C-01") return "Larpington je hlavním městem a největším městským uzlem jižního pobřeží. Čtyři tradiční čtvrti Chalupecká, Kynčlova, Klimečkova a Žemličkova doplňuje univerzitně-kreativní zóna; samostatné kampusové město leží poblíž, ale není larpingtonskou čtvrtí. Městské železniční spojení, silniční tahy a historický přístav propojují centrum s dalšími částmi ostrova.";
  if (record.id === "T-01") return "Praha leží ve vnitrozemské nížině mezi Larpingtonem a severními sídly. Silniční síť odtud pokračuje k Aokawě a letištnímu koridoru; železniční stanice ji napojuje na linku L2.";
  if (record.id === "T-02") return "Město leží v jižní části hlavního ostrova na silničním a železničním směru mezi Larpingtonem, západní vysočinou a přehradní oblastí. Jeho poloha tvoří přirozený orientační bod při cestě od městského pobřeží do vnitrozemí.";
  if (record.id === "T-03") return "Horské sídlo leží na západě ostrova v krajině lesů, svahů a drobných vodních toků. Místní silniční spojení navazuje na trasu od Cimprlichova Hradiště.";
  if (record.id === "T-04") return "Severní městečko leží při pobřežní zátoce, v krajině severních silničních a cyklistických tras. Jeho japonsky znějící místní název se zachovává v zavedené podobě.";
  if (record.id === "T-05") return "Aokawa leží na severním pobřeží u stejnojmenné zátoky. Silniční a cyklistické trasy odtud pokračují k Ōru Maitu, Hoshimachi i směrem na Prahu.";
  if (record.id === "T-06") return "Hoshimachi je severní pobřežní sídlo při stejnojmenné zátoce. Okolní silniční síť je napojena na Aokawu a severovýchodní pobřeží.";
  if (record.id === "M-01") return "Lesnatý horský masiv na západě ostrova dosahuje v orientačním modelu přibližně 560 m n. m. Hřeben navazují další horské vrcholy a vyhlídky; udaná výška není přesnou geodetickou kótou.";
  if (record.id === "M-02") return "Strmější horský svah v západní vysočině soustřeďuje lyžařskou sjezdovku a start pro paragliding. Zimní sezona je podle klimatického podkladu krátká.";
  if (record.id === "M-03") return "Zaoblený vrch leží v krajině horských luk a značených pěších tras. Mapa u něj zachycuje vyhlídková a odpočinková místa i start pro paragliding.";
  if (record.id === "N-02") return "Krystalová jeskyně se nachází v západním horském pásmu. Jde o citlivou přírodní lokalitu s regulovaným návštěvnickým přístupem.";
  if (record.id === "N-03") return "Vodopád na horském toku leží v západním vnitrozemí mezi horskou železnicí a přehradní oblastí. Navazuje na něj vodní pěší trasa podél řeky.";
  if (record.id === "N-04") return "Přehradní jezero zadržuje vodu v západní části ostrova pod horským povodím. Hráz, železniční zastávka a vyhlídka jsou v mapě vedeny jako samostatné body.";
  if (record.id === "L1") return "Horská zážitková železnice vede západním vnitrozemím kolem horské stanice, krystalové jeskyně, vodopádu a přehrady. Linka je v provozu; její poloha v mapě je orientační.";
  if (record.id === "L2") return "Historická elektrická dráha propojuje sídla hlavního ostrova včetně Prahy, Aokawy, Hoshimachi a Larpingtonu. Linka je v provozu; na mapě ji doplňuje spojení k regionálnímu letišti a východnímu přístavu.";
  if (record.id === "L3") return "Městská část rychlé linky L3 je v provozu. Podmořské pokračování na Paraland se dokončuje; mezi ostrovy nyní zajišťují pravidelné spojení lodě a trajekty.";
  if (kind === "settlement") {
    if (sub === "hamlet") return `Malé sídlo leží v ${area}. ${around}`;
    if (sub === "old_town") return `Historické sídlo leží v ${area} na ostrově ${islandLabel(record)}. ${around}`;
    if (sub === "resort") return `Letovisko leží v ${area} na ostrově ${islandLabel(record)}. ${around}`;
    return `Sídlo leží v ${area}. ${around}`;
  }
  if (kind === "peak") return `Vrchol náleží k lesnaté horské krajině ${area}. ${around}`;
  if (kind === "nature") return `${name} leží v ${area}. ${around}`;
  if (kind === "poi" && sub.includes("spring")) return `Pramen leží v ${area} v pěším dosahu okolních tras a vodních toků. ${around}`;
  if (kind === "poi" && sub.includes("viewpoint")) return `Vyhlídkové místo leží v ${area} na okraji pobřeží nebo horského terénu. ${around}`;
  if (kind === "poi" && sub.includes("beach")) return `Pobřežní místo leží v ${area} na jednom z písečných úseků ostrova. ${around}`;
  if (kind === "poi" && sub.includes("paragliding")) return `Místo leží v ${area} v návaznosti na horské svahy a okolní pěší síť. ${around}`;
  if (kind === "poi" && sub.includes("castle")) return `Historický areál se nachází na ostrově Paraland v jeho starší vnitrozemské části. ${around}`;
  if (kind === "poi" && sub.includes("ruin")) return `Pozůstatek historické stavby leží v členité krajině Paralandu. ${around}`;
  if (kind === "poi" && sub.includes("hotel")) return `Ubytovací objekt leží v ${area} u pobřežní nebo horské návštěvnické oblasti. ${around}`;
  if (kind === "rail_station") return `Stanice leží v ${area} a navazuje na železniční síť ostrova. ${around}`;
  if (kind === "rail_line") return `${name} je součástí železniční sítě souostroví. ${around}`;
  if (kind === "road") return `Silniční úsek leží v ${area} a propojuje části ostrova vyznačené v názvu trasy. ${around}`;
  if (kind === "trail") return `Pěší trasa vede krajinou ${area}; její pojmenované cíle odpovídají místům v mapovém registru. ${around}`;
  if (kind === "cycleway") return `Cyklotrasa je součástí ostrovní sítě a vede přes ${area}. ${around}`;
  if (kind === "river") return `Vodní tok odvádí vodu krajinou ${area}. ${around}`;
  if (kind === "coast_feature") return `Pobřežní útvar leží na ${islandLabel(record)} a vymezuje část zdejšího členitého břehu. ${around}`;
  if (kind === "port") return `Přístavní místo leží v ${area} a váže se na pobřežní dopravu nebo místní lodní provoz. ${around}`;
  if (kind === "airport") return `Letištní plocha leží ve východní části hlavního ostrova, stranou od historického centra. ${around}`;
  if (kind === "industry") return `Průmyslové území leží ve východní části hlavního ostrova v návaznosti na silniční, železniční a přístavní koridory. ${around}`;
  if (kind === "infrastructure") return `Vodní stavba leží v přehradní oblasti západního vnitrozemí. ${around}`;
  if (kind === "other_line" && sub === "ferry") return "Lodní trasa propojuje historický přístav Larpingtonu s marinou na Paralandu. Přepravu mezi ostrovy zajišťují lodě; podmořská část L3 se dokončuje.";
  return `${typeLabel(record)} leží v ${area}. ${around}`;
}

function atlasScenery(record) {
  const type = String(record.type || "").toLowerCase(), sub = String(record.subtype || "").toLowerCase();
  if (["peak", "mountain"].includes(type)) return "Lesnaté svahy a otevřenější horské partie se střídají s navazujícími pěšími trasami; jde o nízké ostrovní pohoří, nikoli vysokohorskou krajinu.";
  if (record.id === "N-04") return "Hladina přehrady leží pod horským povodím; v okolní mapě se potkává vodní plocha, hráz a železniční přístup.";
  if (type === "river") return "Koryto propojuje vnitrozemský terén s nižšími částmi ostrova; tok a jeho délka vycházejí z orientačního modelu.";
  if (type === "coast_feature" || type === "port" || (type === "poi" && sub.includes("beach"))) return record.island === "para" ? "Pobřežní poloha na Paralandu je součástí ostrova ležícího jihovýchodně od hlavního ostrova." : "Pobřeží přechází od zátok a přístavních úseků k otevřeným výhledům na moře.";
  if (type === "poi" && sub.includes("spring")) return "Prameniště doplňuje síť horských vodních toků a pěších cest.";
  if (record.island === "para") return "Paraland spojuje pobřežní sídla a letoviska s rozsáhlými přírodními plochami; turistický pohyb je regulován.";
  if (record.region === "south_southeast") return "Jižní oblast přechází od městského zázemí k pobřeží a ostrovním dopravním spojením.";
  return "Místní charakter dotvářejí reliéf, vodstvo a síť pojmenovaných tras zakreslených v atlasu.";
}

const districtLabels = Object.fromEntries(capitalSource.filter((record) => record.type === "district").map((record) => [record.id, record.name_cs]));
const pointInRing = (point, ring) => {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i], [xj, yj] = ring[j];
    const cross = ((yi > point[1]) !== (yj > point[1])) && point[0] < ((xj - xi) * (point[1] - yi)) / ((yj - yi) || 1e-12) + xi;
    if (cross) inside = !inside;
  }
  return inside;
};
const districtAt = (record) => {
  if (record.district && districtLabels[record.district]) return record.district;
  for (const feature of districtsGeo) {
    const polygons = feature.geometry.type === "Polygon" ? [feature.geometry.coordinates] : feature.geometry.coordinates;
    if (polygons.some((polygon) => pointInRing([record.x_km, record.y_km], polygon[0]))) return feature.properties.id;
  }
  return null;
};
const pointSegmentDistance = (p, a, b) => {
  const dx = b[0] - a[0], dy = b[1] - a[1], d2 = dx * dx + dy * dy;
  const t = d2 ? Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / d2)) : 0;
  return Math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy));
};
const streetIndex = streets.filter((feature) => feature.properties.name_cs).map((feature) => feature);
function nearestStreets(record, limit = 2) {
  const point = [record.x_km, record.y_km], best = new Map();
  for (const feature of streetIndex) {
    const coordinates = feature.geometry.coordinates;
    let d = Infinity;
    for (let i = 1; i < coordinates.length; i++) d = Math.min(d, pointSegmentDistance(point, coordinates[i - 1], coordinates[i]));
    const name = feature.properties.name_cs;
    if (d < (best.get(name)?.distance_km ?? Infinity)) best.set(name, { name, distance_km: d, district: feature.properties.district });
  }
  return [...best.values()].sort((a, b) => a.distance_km - b.distance_km || a.name.localeCompare(b.name, "cs")).slice(0, limit);
}

const blockType = {
  residential_low: "Nízký obytný blok", residential_mid: "Obytný blok", old_town_mixed: "Smíšený blok starého města",
  promenade_retail: "Blok pobřežní promenády", transit_mixed: "Blok u dopravního uzlu", retail_main: "Obchodní blok",
  civic_mixed: "Blok městské vybavenosti", new_waterfront: "Blok nového nábřeží", school: "Školní blok",
};
const landUse = {
  residential_low: "nízkou obytnou zástavbu", residential_mid: "kompaktní obytnou zástavbu nižšího až středního měřítka",
  old_town_mixed: "smíšené využití bloků starší městské zástavby", promenade_retail: "obchody a služby podél nábřežní promenády",
  transit_mixed: "smíšené městské využití u dopravního uzlu", retail_main: "obchody a služby podél hlavní obchodní osy",
  civic_mixed: "městskou vybavenost", new_waterfront: "novější městskou zástavbu u nábřeží", school: "školní a vzdělávací zázemí",
};
const capitalCategory = {
  plan: "Městský plán", district: "Městská čtvrť", building: "Budova", station: "Stanice", square: "Náměstí a předprostor",
  park: "Park a zeleň", promenade: "Promenáda", harbor: "Přístav", pier: "Přístavní molo", street: "Městská ulice",
  block: "Městský blok", shop: "Obchod", cafe: "Kavárna", rental: "Půjčovna", route: "Pěší trasa", retail_zone: "Obchodní oblast",
};
const capitalCleanName = (record) => String(record.name_cs || "").replace(/\s*\([^)]*(?:pracovní|prac\.|návrh|proposed)[^)]*\)/gi, "")
  .replace(/\s*[,–—-]?\s*(?:pracovní|prac\.|návrh|proposed)\b.*$/i, "").replace(/\s+/g, " ").trim();

const blockStreetCounter = new Map();
const capitalNames = {};
for (const record of capitalSource) {
  if (record.type !== "block") {
    let name = capitalCleanName(record);
    if (record.id === "CP-01") name = "Plán Larpingtonu";
    if (record.id === "CP-B07") name = "Historický kostel v Žemličkově čtvrti";
    if (record.id === "CP-B01") name = "Radnice Larpingtonu";
    name = name.replace(/\bST-W\b/g, "Larpington-západ").replace(/\bST-N\b/g, "Larpington-sever").replace(/\bST-E\b/g, "Larpington-východ").replace(/\bST-S\b/g, "Larpington-jih").replace(/\bST-L3-05\b/g, "Východní nábřeží");
    name = name.replace(/\bM-01\b/g, "Larpova hora").replace(/\bM-02\b/g, "Zimní hora").replace(/\bC-01\b/g, "Larpington");
    capitalNames[record.id] = name || `${capitalCategory[record.type] || "Místo"} v Larpingtonu`;
    continue;
  }
  const nearbyStreets = nearestStreets(record, 1);
  const streetName = nearbyStreets[0]?.name || "uliční síť Larpingtonu";
  const dId = districtAt(record), district = districtLabels[dId] || "Larpington";
  const groupKey = `${dId || "city"}|${streetName}|${record.subtype}`;
  const localNumber = (blockStreetCounter.get(groupKey) || 0) + 1;
  blockStreetCounter.set(groupKey, localNumber);
  const label = blockType[record.subtype] || "Městský blok";
  capitalNames[record.id] = `${label} · ${streetName} ${String(localNumber).padStart(2, "0")}`;
}

const atlas = {};
for (const record of atlasSource) {
  const override = atlasNames[record.id] || {};
  const name = atlasPublicNames[record.id];
  const close = nearest(record, atlasSource, 3).map(({ record: other, distance_km }) => ({
    place_id: other.id,
    name_cs: atlasPublicNames[other.id],
    direction_cs: bearing(record, other),
    distance_km: Number(distance_km.toFixed(2)),
  }));
  const aliases = new Set([...(override.aliases || []), cleanSourceName(record.name_cs)].filter((item) => item && item !== name));
  const isOverride = Object.hasOwn(atlasNames, record.id);
  atlas[record.id] = {
    public_name_cs: name,
    ...(override.en ? { public_name_en: override.en } : record.name_status === "approved" && record.name_en && record.name_en !== name ? { public_name_en: cleanSourceName(record.name_en) } : {}),
    ...(override.ja ? { public_name_ja: override.ja } : record.name_status === "approved" && record.name_ja ? { public_name_ja: cleanSourceName(record.name_ja) } : {}),
    short_description_cs: atlasDescription(record, close.map((nearby) => ({ record: byAtlasId.get(nearby.place_id) }))),
    category_cs: typeLabel(record),
    region_label_cs: regionNames[record.region] || "ostrovní krajina",
    highlights_cs: [atlasScenery(record)],
    scenery_cs: atlasScenery(record),
    atmosphere_cs: record.island === "para" ? "Pobytová a přírodní krajina ostrova Paralandu se střídá podél pobřeží a v jeho zalesněném vnitrozemí." : record.region === "west_northwest" || record.region === "central_west" ? "Západ ostrova působí horským a lesnatým dojmem; stezky propojují vyhlídky, vodstvo a menší sídla." : record.region === "south_southeast" ? "Jižní část ostrova propojuje městské prostředí s pobřežím a lodní dopravou." : "Ostrovní krajina se zde otevírá od sídel a dopravních koridorů směrem k pobřeží.",
    viewpoints: close,
    editorial_status: isOverride ? (record.id === "T-02" || record.id === "T-01" || record.id === "C-01" ? "author_approved" : "new_editorial_name") : "derived_from_source",
    source_reason: override.reason || "Zachován existující geografický název po odstranění interního pracovního dovětku; popis a okolí jsou odvozeny z typu, regionu a sousedních souřadnic atlasu.",
    ...(aliases.size ? { aliases: [...aliases] } : {}),
  };
}

const capital = {};
const capitalNeighborhood = capitalSource.filter((record) => record.type !== "block" && Number.isFinite(record.x_km) && Number.isFinite(record.y_km));
for (const record of capitalSource) {
  const name = capitalNames[record.id], districtId = districtAt(record), districtName = districtLabels[districtId] || "Larpington";
  const close = nearest(record, capitalNeighborhood, 3).map(({ record: other, distance_km }) => ({
    place_id: other.id, name_cs: capitalNames[other.id] || other.name_cs,
    direction_cs: bearing(record, other), distance_km: Number(distance_km.toFixed(2)),
  }));
  const localStreets = record.type === "block" ? nearestStreets(record, 2) : [];
  const subtype = String(record.subtype || "").toLowerCase();
  const highlights = [];
  let description;
  let scenery;
  if (record.id === "CP-01") {
    description = "Orientační plán ukazuje kompaktní Larpington s nepravidelnými ulicemi, městskými bloky, veřejnými prostranstvími a historickým přístavem. Zobrazuje čtyři tradiční čtvrti i městské dopravní vazby; univerzitně-kreativní zóna je potvrzena v kánonu, její přesný obvod však v tomto plánu zakreslen není.";
    scenery = "Nízká a středně vysoká kompaktní zástavba se střídá s dvory, zahradami, parky a pobřežními prostory.";
  } else if (record.type === "block") {
    const streetsText = localStreets.map((street) => street.name).filter(Boolean);
    const roadPhrase = streetsText.length >= 2 ? `mezi ulicemi ${streetsText[0]} a ${streetsText[1]}` : streetsText[0] ? `u ulice ${streetsText[0]}` : "v uliční síti města";
    const use = landUse[subtype] || "městské využití";
    description = `V plánu Larpingtonu je plocha ${roadPhrase} v ${districtName} vymezena pro ${use}. Jde o jednu z městských ploch čitelných v podrobném měřítku plánu.`;
    scenery = subtype.includes("old_town") ? "Okolí starší čtvrti tvoří hustší městské bloky a nepravidelná uliční síť." : subtype.includes("waterfront") || subtype.includes("promenade") ? "Městský blok navazuje na pobřežní promenádu a veřejné prostory u vody." : subtype.includes("transit") ? "Blok leží v městském prostředí utvářeném návazností na veřejnou dopravu." : "Půdorys bloku doplňuje kompaktní uliční strukturu dané čtvrti.";
    if (streetsText[0]) highlights.push(`Nejbližší pojmenovaná ulice: ${streetsText[0]}.`);
  } else {
    const nearName = close[0]?.name_cs;
    const loc = nearName ? ` V bezprostředním okolí leží ${nearName}.` : "";
    if (record.type === "district") description = `${name} je jednou ze čtyř tradičních čtvrtí hlavního města.${loc}`;
    else if (record.type === "building" && subtype === "museum") description = "Hlavní interaktivní muzeum dějin v Larpingtonu je otevřené a přibližuje vývoj země pomocí historických pramenů a audiovizuálních rekonstrukcí.";
    else if (record.type === "building" && subtype === "town_hall") description = "Radniční budova je součástí občanského centra Larpingtonu; v jejím okolí se sbíhají veřejná prostranství a hlavní městské ulice.";
    else if (record.type === "station") description = `${name} obsluhuje městskou železniční síť a leží v ${districtName}.${loc}`;
    else if (record.type === "street") description = `${name} tvoří část nepravidelné městské uliční sítě a propojuje veřejná prostranství v různých částech Larpingtonu.${loc}`;
    else if (record.type === "square") description = `${name} je veřejným prostranstvím v ${districtName}; jeho poloha navazuje na okolní ulice, stanice nebo městské budovy.${loc}`;
    else if (record.type === "park") description = `${name} tvoří zelenou plochu v ${districtName} a doplňuje kompaktní městskou zástavbu.${loc}`;
    else if (record.type === "promenade") description = `${name} sleduje městské pobřeží a propojuje pěší prostory v přístavní části Larpingtonu.${loc}`;
    else if (record.type === "harbor") description = "Historický přístav tvoří městské nábřeží s lodním molem a návazností na starší zástavbu. Přes ostrovy nyní vedou lodní a trajektová spojení.";
    else if (record.type === "building" && subtype === "church") description = `Historický kostel leží na Kostelním náměstí v ${districtName}; cihlové a kamenné zdi doplňují měřítko starší městské zástavby.${loc}`;
    else if (record.type === "building" && subtype === "school") description = `Školní budova je součástí městské vybavenosti ${districtName}.${loc}`;
    else if (record.type === "building") description = `${name} je součástí občanské nebo městské vybavenosti ${districtName}.${loc}`;
    else if (record.type === "shop" || record.type === "retail_zone") description = `${name} navazuje na obchodní osu a pěší prostory ${districtName}.${loc}`;
    else if (record.type === "cafe") description = `${name} je součástí městského parteru Larpingtonu a pěšího prostředí ${districtName}.${loc}`;
    else if (record.type === "route") description = `${name} propojuje přístupné veřejné prostory v městské síti Larpingtonu.${loc}`;
    else if (record.type === "pier") description = `${name} slouží jako přístupové místo k lodní dopravě v historickém přístavu.${loc}`;
    else if (record.type === "rental") description = `${name} doplňuje nabídku sdílené městské mobility v Larpingtonu.${loc}`;
    else description = `${capitalCategory[record.type] || "Městské místo"} v ${districtName}, zakreslené v podrobném plánu Larpingtonu.${loc}`;
    scenery = record.type === "park" ? "Zelené plochy a koridory přerušují souvislou zástavbu a zpřístupňují pěší průchody." : record.type === "harbor" || record.type === "pier" || record.type === "promenade" ? "Pobřežní prostředí propojuje nábřežní prostory, starší zástavbu a lodní přístupy." : `Městský prostor navazuje na charakter ${districtName.toLocaleLowerCase("cs-CZ")} a okolní nepravidelnou uliční síť.`;
  }
  capital[record.id] = {
    public_name_cs: name,
    ...(record.name_status === "approved" && record.name_en && record.name_en !== name ? { public_name_en: record.name_en.replace(/\s*\([^)]*(?:working|proposed)[^)]*\)/gi, "").trim() } : {}),
    ...(record.name_status === "approved" && record.name_ja ? { public_name_ja: record.name_ja } : {}),
    short_description_cs: description,
    category_cs: capitalCategory[record.type] || "Městské místo",
    region_label_cs: districtName,
    highlights_cs: highlights,
    scenery_cs: scenery,
    atmosphere_cs: record.type === "harbor" || record.type === "promenade" ? "Pobřežní městská část propojuje každodenní pěší pohyb s historickým přístavem." : "Ulice, dvory a veřejné prostory vytvářejí kompaktní městský celek s místním charakterem jednotlivých čtvrtí.",
    viewpoints: close,
    editorial_status: record.type === "block" ? "new_editorial_name" : "derived_from_source",
    source_reason: record.type === "block"
      ? `Původní pořadové označení bylo nahrazeno čitelným názvem podle kategorie, nejbližší skutečné uliční geometrie (${localStreets[0]?.name || "uliční síť"}) a místní čtvrti. Číselné pořadí je pouze lokální rozlišení bloků stejného typu u téže ulice.`
      : "Zachován význam existujícího objektu; veřejný popis vychází z jeho typu, polohy, nejbližší pojmenované geometrie a platného kánonu.",
    ...(record.name_cs && record.name_cs !== name ? { aliases: [record.name_cs] } : {}),
  };
}

const data = {
  meta: {
    title: "Redakční vrstva veřejného atlasu Larpidie",
    schema_version: 1,
    generated_at: "2026-11-03",
    note_cs: "Pracovní soubor pro redakci. Stav schválení, odůvodnění a aliasy jsou neveřejné; veřejný export vybírá pouze návštěvnická pole.",
  },
  atlas,
  capital,
};
if (Object.keys(atlas).length !== 159 || Object.keys(capital).length !== 662) throw new Error(`Expected 159 atlas/662 city entries, received ${Object.keys(atlas).length}/${Object.keys(capital).length}.`);
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
console.log(`Seeded ${Object.keys(atlas).length} atlas and ${Object.keys(capital).length} Larpington editorial records.`);
