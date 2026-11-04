import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (name) => JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));
const outputPath = path.join(root, "content/larpidia/atlas_places_editorial.json");
const editorial = readJson("content/larpidia/atlas_places_editorial.json");
const atlas = readJson("atlas/current/registry/places.json").objects;
const city = readJson("atlas/current/capital/cp_objects.json").objects;
const streets = readJson("atlas/current/capital/cp_streets_atlas_km.geojson").features;
const districtsGeo = readJson("atlas/current/capital/cp_districts_atlas_km.geojson").features;
const byAtlas = new Map(atlas.map((item) => [item.id, item]));
const byCity = new Map(city.map((item) => [item.id, item]));

const curatedAtlasNames = {
  "C-01": "Larpington", "C-02": "Historický přístav Larpingtonu",
  "N-03": "Vodopád na horském toku", "N-04": "Přehradní jezero",
  "PL-01": "Staré městečko Paralandu", "PL-02": "Hrad Paralandu",
  "PL-03": "Jižní letovisko Paralandu", "PL-05": "Přístavní vesnice Paralandu",
  "PL-06": "Zřícenina na Paralandu", "PL-04": "Aquapark Paralandu",
  "HM-01": "Pražské Dvory", "HM-02": "Vodní Dvory", "HM-03": "Letištní Dvory",
  "HM-04": "Severní Dvorec", "HM-05": "Západní Dvory", "HM-06": "Hájová Stráň",
  "ST-L1-03": "Zastávka u vodopádu", "ST-L2-09": "Letištní výhybna",
  "ST-L1-04": "Nástupiště před Krystalovou jeskyní", "DAM-N04": "Hráz přehrady",
  "V-03": "Vyhlídka u Severního mysu", "V-04": "Vyhlídka na hrotu poloostrova",
  "V-05": "Vyhlídka na severovýchodním pobřeží", "V-06": "Vyhlídka na jihozápadním útesu",
  "V-07": "Vyhlídka na hrázi přehrady", "V-02": "Útesová vyhlídka pod Larpovou horou",
  "SP-01": "Pramen řeky Larp", "SP-04": "Studánka na stezce ke Kulatému vrchu",
  "SP-06": "Studánka u Horské stanice", "SP-08": "Studánka pod hradem na Paralandu",
  "ST-L3-06": "Stanice u spojení na Paraland", "ST-L3-07": "Stanice Paraland – Marina",
  "P-01": "Železniční spojení na Paraland",
  "RD-S01": "Přístup k Útesové vyhlídce pod Larpovou horou",
  "RD-S02": "Přístup k vyhlídce Severního mysu", "RD-S03": "Přístup k Majáku Severního mysu",
  "RD-S04": "Přístup k vyhlídce na hrotu poloostrova", "RD-S05": "Přístup k vyhlídce na severovýchodním pobřeží",
  "RD-S06": "Přístup k vyhlídce na jihozápadním útesu", "RD-S07": "Přístup k vyhlídce na hrázi přehrady",
  "RD-S08": "Přístup k pláži u Hoshimachi", "RD-S09": "Přístup k horské chatě u sjezdovky",
  "RD-S10": "Přístup k západní pláži Larpingtonského zálivu", "RD-S11": "Přístup k východní pláži Larpingtonského zálivu",
  "RD-S12": "Přístup k pláži u Hoshimachi", "RD-S13": "Přístup k pláži na jihovýchodním poloostrově",
  "RD-S14": "Místní silnice do Pražských Dvorů", "RD-S15": "Místní silnice do Vodních Dvorů",
  "RD-S16": "Místní silnice k Letištním Dvorům", "RD-S17": "Místní silnice k Severnímu Dvorci",
  "RD-S18": "Místní silnice do Západních Dvorů", "RD-S19": "Místní silnice k Hájové Stráni",
  "B-01": "Západní pláž Larpingtonského zálivu", "B-02": "Východní pláž Larpingtonského zálivu",
  "B-03": "Pláž u Hoshimachi", "B-04": "Pláž na jihovýchodním poloostrově",
  "B-05": "Pláž na východním pobřeží Paralandu", "B-06": "Jižní pláž Paralandu",
  "V-08": "Vyhlídka na východním kopci Paralandu",
  "ST-S": "Larpington Střed – Přístav (Žemličkova čtvrť)",
  "ST-W": "Larpington Západ (Chalupecká čtvrť)", "ST-N": "Larpington Sever (Kynčlova čtvrť)",
  "ST-E": "Larpington Východ (Klimečkova čtvrť)",
  "ST-L1-02": "Stanice u přehrady", "ST-L1-04": "Stanice u Krystalové jeskyně",
  "ST-L1-05": "Horská stanice", "ST-L2-01": "Cimprlichovo Hradiště",
  "ST-L2-05": "Stanice Zelená průmyslová zóna", "ST-L2-06": "Stanice závodu na zpracování řas",
  "ST-L2-07": "Stanice Nákladní přístav", "ST-L2-08": "Stanice Praha",
  "ST-L2-10": "Stanice u letiště", "ST-L2-11": "Stanice Aokawa", "ST-L2-12": "Stanice Ōru Maito",
  "ST-L2-13": "Stanice Hoshimachi", "ST-L3-05": "Stanice Východní nábřeží",
};
const curatedRoadNames = {
  "RD-PL2": "Přístupová silnice k hradu Paralandu", "RD-PL3": "Přístupová silnice k aquaparku Paralandu",
  "RD-PL4": "Přístupová silnice k přistávací ploše Paralandu",
  "RD-R1": "Okružní pobřežní silnice R1", "RD-PL1": "Okružní servisní silnice Paralandu",
};
Object.assign(curatedAtlasNames, {
  "ST-L2-01": "Stanice Cimprlichovo Hradiště",
  "W-02": "Řeka Aokawa",
});
Object.assign(curatedRoadNames, {
  "RD-S08": "Odbočka k hotelové pláži Hoshimachi",
  "RD-S12": "Příjezdová silnice k pláži Hoshimachi",
});
curatedAtlasNames["RD-S08"] = curatedRoadNames["RD-S08"];
curatedAtlasNames["RD-S12"] = curatedRoadNames["RD-S12"];
const region = {
  west_northwest: { phrase: "v západním horském pásmu hlavního ostrova", label: "západní horské pásmo · hlavní ostrov" },
  central_west: { phrase: "v západním vnitrozemí hlavního ostrova", label: "západní vnitrozemí · hlavní ostrov" },
  central_lowland: { phrase: "v centrální nížině hlavního ostrova", label: "centrální nížina · hlavní ostrov" },
  south_southeast: { phrase: "v jižní části hlavního ostrova", label: "jih hlavního ostrova" },
  southeast_offshore: { phrase: "na Paralandu, jihovýchodním ostrově", label: "Paraland · jihovýchodní ostrov" },
  north: { phrase: "v severní části hlavního ostrova", label: "sever hlavního ostrova" },
  east_northeast: { phrase: "ve východní části hlavního ostrova", label: "východ hlavního ostrova" },
  east: { phrase: "ve východní části hlavního ostrova", label: "východ hlavního ostrova" },
  west: { phrase: "v západní části hlavního ostrova", label: "západ hlavního ostrova" },
  south: { phrase: "v jižní části hlavního ostrova", label: "jih hlavního ostrova" },
  center: { phrase: "ve střední části hlavního ostrova", label: "střed hlavního ostrova" },
};
const typeLabel = (o) => {
  const sub = String(o.subtype || "").toLowerCase();
  if (o.id === "C-01") return "Hlavní město";
  if (o.type === "settlement") return ({ town: "Město", village: "Vesnice", hamlet: "Osada", old_town: "Historické sídlo", resort: "Letovisko", capital: "Hlavní město" })[sub] || "Sídlo";
  if (o.type === "peak") return "Horský vrchol";
  if (o.type === "nature") return ({ nature: o.id === "N-02" ? "Jeskyně" : o.id === "N-03" ? "Vodopád" : o.id === "N-04" ? "Přehradní jezero" : "Skalní vyhlídka" })[sub];
  if (o.type === "poi") return ({ viewpoint: "Vyhlídka", lighthouse: "Maják", paragliding_launch: "Start pro paragliding", paragliding_landing: "Přistávací louka", spring: "Pramen a studánka", hotel_vip: "Hotel", castle: "Hrad", ruin: "Zřícenina", aquapark: "Aquapark", beach: "Pláž" })[sub] || "Místo v krajině";
  return ({ district: "Městská čtvrť", port: "Přístav", industry: "Průmyslový areál", airport: "Letiště", rail_station: o.id === "P-01" ? "Železniční spojení" : "Železniční stanice", rail_line: "Železniční linka", road: "Silniční spojení", trail: "Pěší trasa", cycleway: "Cyklotrasa", river: "Vodní tok", coast_feature: ({ bay: "Zátoka", cape: "Mys", peninsula: "Poloostrov" })[sub], infrastructure: "Vodní stavba", other_line: ({ ski_run: "Sjezdovka", ski_lift: "Lyžařský vlek", ferry: "Lodní spojení" })[sub] })[o.type] || "Místo v krajině";
};
const subtitleRegionPhrase = (o) => {
  if (["N-01", "V-02", "V-06"].includes(o.id)) return "na západním pobřeží hlavního ostrova";
  if (["V-03", "LH-01"].includes(o.id)) return "u Severního mysu na hlavním ostrově";
  if (["V-04", "B-04", "PEN-SE"].includes(o.id)) return "na jihovýchodním poloostrově hlavního ostrova";
  if (o.id === "V-05") return "na severovýchodním pobřeží hlavního ostrova";
  if (["V-07", "ST-L1-02", "ST-L1-03", "DAM-N04"].includes(o.id)) return "u přehrady v západním vnitrozemí hlavního ostrova";
  if (["V-08", "B-05"].includes(o.id)) return "na východním pobřeží Paralandu";
  if (["B-06", "PL-03"].includes(o.id)) return "na jižním pobřeží Paralandu";
  if (o.id === "B-03") return "u Hoshimachi na severním pobřeží";
  if (["B-01", "B-02"].includes(o.id)) return "v Larpingtonském zálivu na jižním pobřeží";
  return (region[o.region] || { phrase: "v ostrovní krajině" }).phrase;
};
const publicType = new Set(["settlement", "peak", "nature", "district", "port", "rail_station", "rail_line", "road", "trail", "cycleway", "river", "coast_feature", "infrastructure", "industry", "airport", "poi", "other_line"]);
const highValue = (o) => publicType.has(o.type) && !["road", "rail_line", "trail", "cycleway", "other_line"].includes(o.type) && o.id !== "P-01";
const distance = (a, b) => Math.hypot(a.x_km - b.x_km, a.y_km - b.y_km);
const bearing = (a, b) => {
  const dirs = ["severně", "severovýchodně", "východně", "jihovýchodně", "jižně", "jihozápadně", "západně", "severozápadně"];
  const deg = (Math.atan2(b.x_km - a.x_km, -(b.y_km - a.y_km)) * 180 / Math.PI + 360) % 360;
  return dirs[Math.round(deg / 45) % 8];
};
const replaceRefs = (value) => String(value || "")
  .replace(/\bM-01\b/g, "Larpova hora").replace(/\bM-02\b/g, "Zimní hora").replace(/\bM-03\b/g, "Kulatý vrch")
  .replace(/\bC-01\b/g, "Larpington").replace(/\bC-02\b/g, "Historický přístav Larpingtonu")
  .replace(/\bT-01\b/g, "Praha").replace(/\bT-02\b/g, "Cimprlichovo Hradiště").replace(/\bT-03\b/g, "Havlišovo Doupě")
  .replace(/\bT-04\b/g, "Ōru Maito").replace(/\bT-05\b/g, "Aokawa").replace(/\bT-06\b/g, "Hoshimachi")
  .replace(/\bHM-01\b/g, "Pražské Dvory").replace(/\bHM-02\b/g, "Vodní Dvory").replace(/\bHM-03\b/g, "Letištní Dvory")
  .replace(/\bHM-04\b/g, "Severní Dvorec").replace(/\bHM-05\b/g, "Západní Dvory").replace(/\bHM-06\b/g, "Hájová Stráň")
  .replace(/\bST-W\b/g, "stanice Larpington Západ").replace(/\bST-N\b/g, "stanice Larpington Sever").replace(/\bST-E\b/g, "stanice Larpington Východ").replace(/\bST-S\b/g, "stanice Larpington Střed–Přístav")
  .replace(/\bST-L3-05\b/g, "stanice Východní nábřeží")
  .replace(/\s*\((?:pracovně|prac\.|pracovní|fotozastávka|model|proposed)[^)]*\)/gi, "")
  .replace(/Přístup ke stanici stanice /g, "Přístup ke stanici ")
  .replace(/\s*[-–—]\s*pracovní\b.*$/i, "").replace(/\s+/g, " ").trim();

const atlasNames = {};
for (const o of atlas) {
  const entry = editorial.atlas[o.id];
  const sourceName = o.name_cs || o.name || "";
  const chosen = curatedAtlasNames[o.id] || curatedRoadNames[o.id] || (entry.public_name_cs === "Cimpřichovo Hradiště" ? "Cimprlichovo Hradiště" : replaceRefs(entry.public_name_cs || sourceName));
  atlasNames[o.id] = chosen;
  const oldAliases = new Set(entry.aliases || []);
  if (sourceName && sourceName !== chosen) oldAliases.add(sourceName);
  if (o.id === "T-02") oldAliases.add("Cimpřichovo Hradiště");
  entry.public_name_cs = chosen;
  if (oldAliases.size) entry.aliases = [...oldAliases].filter(Boolean);
  const loc = region[o.region] || { phrase: "v ostrovní krajině", label: "ostrovní krajina" };
  entry.category_cs = typeLabel(o);
  entry.region_label_cs = loc.label;
  entry.subheading_cs = `${entry.category_cs} ${subtitleRegionPhrase(o)}`;
  // Approved translations remain eligible; proposed translations are never promoted by this pass.
  if (o.name_status !== "approved" && !["T-02", "C-01"].includes(o.id)) {
    delete entry.public_name_en;
    delete entry.public_name_ja;
  }
}

const byIdName = (id) => atlasNames[id] || id;
const landmarks = atlas.filter(highValue).filter((o) => Number.isFinite(o.x_km) && Number.isFinite(o.y_km));
const nearbyFor = (o) => landmarks.filter((item) => item.id !== o.id && atlasNames[item.id] !== atlasNames[o.id])
  .map((item) => ({ item, d: distance(o, item) }))
  .filter(({ d }) => d > 0.04 && d <= 8)
  .sort((a, b) => a.d - b.d || a.item.id.localeCompare(b.item.id))
  .slice(0, 3)
  .map(({ item, d }) => ({ place_id: item.id, name_cs: byIdName(item.id), direction_cs: bearing(o, item), distance_km: Number(d.toFixed(2)) }));

const specialDescriptions = {
  "C-01": "Larpington je hlavním městem na jižním pobřeží hlavního ostrova. Jeho historické jádro tvoří čtyři tradiční čtvrti — Chalupecká, Kynčlova, Klimečkova a Žemličkova — vedle nichž se rozvíjí univerzitně-kreativní městská zóna. Samostatné kampusové město leží poblíž, ale do Larpingtonu nepatří.",
  "C-02": "Historický přístav navazuje na jižní městské centrum a přístavní promenádu. Lodní a trajektová doprava dnes zajišťuje spojení s Paralandem; podmořské pokračování železniční linky L3 se stále dokončuje.",
  "T-01": "Praha leží v centrální nížině hlavního ostrova. Silniční a železniční vazby ji spojují s Larpingtonem, severními sídly i východním dopravním koridorem.",
  "T-02": "Cimprlichovo Hradiště leží v jižní části hlavního ostrova na cestě mezi Larpingtonem, západní vysočinou a přehradní oblastí. Městem prochází silniční i železniční spojení do vnitrozemí.",
  "T-03": "Havlišovo Doupě je horská obec na západě ostrova, v krajině lesnatých svahů a drobných vodních toků. Silniční trasa ji spojuje s Cimprlichovým Hradištěm.",
  "T-04": "Ōru Maito leží při severní zátoce a pobřežních trasách hlavního ostrova. Místní stanice a silnice navazují na síť severních sídel.",
  "T-05": "Aokawa leží u severní zátoky na křižovatce pobřežních a vnitrozemských tras. Odtud vedou spojení k Ōru Maitu, Hoshimachi a do centrální nížiny.",
  "T-06": "Hoshimachi je severní pobřežní sídlo při stejnojmenné zátoce. Silniční a cyklistické trasy je propojují s Aokawou a severovýchodním pobřežím.",
  "M-01": "Larpova hora je lesnatý horský masiv v západní části ostrova. Model uvádí přibližně 560 m n. m.; nejde o přesnou geodetickou kótu. Hřeben navazují pěší trasy a nižší vrcholy.",
  "M-02": "Zimní hora má strmější svah se sjezdovkou a startem pro paragliding. Krátká zimní sezona omezuje lyžařské využití; značené trasy pokračují do okolních hor.",
  "M-03": "Kulatý vrch se zvedá nad horskými loukami a značenými pěšími trasami. Na svahu jsou vyznačeny také start a přistávací louka pro paragliding.",
  "N-01": "Skalní vyhlídka leží na západním pobřeží nad mořem a je přístupná po značené útesové stezce. Oplocené vyhlídkové místo umožňuje zastavit u okraje pobřežní krajiny.",
  "N-02": "Krystalová jeskyně leží v západním horském pásmu. Horská železnice L1 projíždí tunelem po jejím obvodu; návštěvnický pohyb v citlivém místě je regulován.",
  "N-03": "Vodopád leží na horském toku v západním vnitrozemí, mezi Krystalovou jeskyní a přehradní oblastí. Podél vody vede pěší trasa a poblíž zastavuje horská linka L1.",
  "N-04": "Přehradní jezero je součástí vodárenské soustavy západního vnitrozemí. Hráz, vyhlídka a železniční zastávka jsou v mapě vedeny odděleně; pobřeží podléhá ochraně zdroje vody.",
  "V-02": "Oplocená útesová vyhlídka leží pod Larpovou horou na západním pobřeží. K místu vede značená stezka; vyhlídková plošina otevírá pohled přes moře.",
  "V-03": "Vyhlídka stojí u Severního mysu v blízkosti navigačního majáku. Pobřežní poloha poskytuje rozhled na severní zátoky a přilehlé moře.",
  "V-04": "Vyhlídkové místo leží na hrotu jihovýchodního poloostrova. Z pobřežního výběžku je otevřený výhled směrem k Paralandu.",
  "V-05": "Vyhlídka leží na severovýchodním pobřeží hlavního ostrova. Její poloha navazuje na pobřežní cestu a výhled přes moře.",
  "V-06": "Vyhlídka na jihozápadním útesu obrací pohled k otevřenému moři. K místu vede místní přístupová cesta a značená pěší trasa.",
  "V-07": "Vyhlídka na hrázi směřuje přes vodní hladinu přehradního jezera. Pobřežní prostor je součástí chráněné vodárenské oblasti.",
  "V-08": "Vyhlídka leží na východním kopci Paralandu. Vyvýšená poloha otevírá pohled přes okolní lesnaté svahy k pobřeží ostrova.",
  "SP-01": "Pramen řeky Larp leží v západním vnitrozemí u pěších tras horského povodí. Mapa jej uvádí jako prameniště; nehodnotí pitnost vody.",
  "SP-02": "Studánka leží v severní části ostrova u Severního potoka. Je zakreslena v návaznosti na místní pěší trasu; atlas neuvádí rozbor pitnosti vody.",
  "SP-03": "Pramen Havlišova potoka leží v horském zázemí Havlišova Doupěte. Je jedním z vodních bodů podél značených tras západní krajiny.",
  "SP-04": "Studánka leží pod Kulatým vrchem u pěší trasy na hřeben. Je vedena jako orientační vodní bod; pitnost není v atlasu specifikována.",
  "SP-05": "Studánka se nachází u hřebenové trasy mezi vrcholy západní vysočiny. Mapa ji propojuje s pěší sítí, nikoli s ověřeným zdrojem pitné vody.",
  "SP-06": "Studánka leží poblíž Horské stanice a turistických tras k okolním vrcholům. Je zakreslena jako prameniště bez údaje o pitnosti.",
  "SP-07": "Studánka nad vodopádem leží u pěší trasy v údolí horského toku. Její poloha doplňuje vodní zastavení mezi vodopádem a přehradou.",
  "SP-08": "Studánka leží na pěší trase pod hradem na Paralandu. Mapa ji uvádí jako místní vodní bod; pitnost vody nehodnotí.",
  "B-01": "Písečná pláž leží na západním okraji Larpingtonského zálivu, jižně od městského centra. Přístup k ní vede z pobřežní silnice.",
  "B-02": "Písečná pláž leží na východním okraji Larpingtonského zálivu. Je součástí jižního pobřeží hlavního ostrova.",
  "B-03": "Pláž leží u severního pobřežního sídla Hoshimachi. Je jedním z písečných úseků vyznačených na hlavním ostrově.",
  "B-04": "Pláž leží na jihovýchodním poloostrově hlavního ostrova. Pobřežní poloha je přístupná místní silnicí.",
  "B-05": "Písečná pláž leží na východním pobřeží Paralandu. Její pobřežní poloha je součástí návštěvnické oblasti ostrova.",
  "B-06": "Jižní pláž leží na pobřeží Paralandu v dosahu letoviska. Pohyb v přírodním zázemí ostrova podléhá místní regulaci.",
  "I-01": "Zelená průmyslová zóna leží ve východní části hlavního ostrova. Vedle výrobních provozů jsou v areálu zakresleny také zahrady, školy a stravovací zázemí.",
  "I-02": "Závod na zpracování mořských řas leží nedaleko nákladního přístavu a železniční trati L2. Jeho umístění navazuje na východní průmyslový a exportní koridor.",
  "I-03": "Nákladní přístav obsluhuje východní exportní oblast. Osobní provoz je omezený; hlavní vazbu tvoří železnice a silniční spojení s průmyslovým areálem.",
  "A-01": "Hlavní regionální letiště leží ve východní nížině, stranou historického centra. Silnice i železniční spojení je propojují s Prahou a průmyslovým koridorem.",
  "P-01": "Podmořské železniční spojení na Paraland je připravovaným pokračováním linky L3, nikoli otevřeným tunelem. Do dokončení stavby zajišťují spojení mezi ostrovy lodě a trajekty.",
  "PL-01": "Staré městečko leží ve vnitrozemí Paralandu a tvoří historické sídlo ostrova. Pěší památková trasa odtud pokračuje ke zřícenině a hradu.",
  "PL-02": "Hradní areál stojí ve vnitrozemí Paralandu v dosahu pěší památkové trasy. Mapa jej zasazuje do chráněné přírodní krajiny ostrova.",
  "PL-03": "Jižní letovisko leží při pobřeží Paralandu. Pobytová zástavba zde navazuje na plážové úseky a místní silniční síť.",
  "PL-04": "Aquapark je samostatná návštěvnická atrakce na Paralandu. Přístup k areálu je regulován rezervací.",
  "PL-05": "Přístavní vesnice se rozkládá u mariny na Paralandu. Lodní terminál propojuje západní pobřeží ostrova s Larpingtonem.",
  "PL-06": "Zřícenina leží nedaleko Starého městečka na Paralandu a je jedním ze zastavení místní památkové trasy. Její poloha zůstává v mapě zachována podle původního registru.",
  "L1": "Horská linka L1 vede západním vnitrozemím kolem horské stanice, Krystalové jeskyně, vodopádu a přehrady. Linka je v provozu; její mapové vedení má orientační charakter.",
  "L2": "Linka L2 propojuje města hlavního ostrova s Prahou, Aokawou, Hoshimachi, letištěm a východním přístavem. Elektrická železnice je v provozu.",
  "L3": "Městský úsek linky L3 je v provozu a obsluhuje Larpington. Podmořské pokračování na Paraland se dokončuje; mez ostrovy nyní jezdí lodě a trajekty.",
  "FERRY-1": "Lodní okruh spojuje historický přístav Larpingtonu s marinou na Paralandu. Přeprava mezi ostrovy probíhá po vodě; lodě nepřevážejí automobily.",
};
Object.assign(specialDescriptions, {
  "M-01": "Larpova hora je lesnatý horský masiv v západní části ostrova. Vrchol dosahuje přibližně 560 m n. m.; hodnota je orientační, nejde o geodetickou kótu. Od hřebene vedou pěší trasy k nižším vrcholům.",
  "ST-L2-01": "Stanice Cimprlichovo Hradiště obsluhuje město na provozované lince L2. Leží u jeho zástavby a navazuje na železniční spojení jižní části hlavního ostrova.",
  "W-02": "Řeka Aokawa protéká severní částí hlavního ostrova a odvádí vodu k nižším polohám. V její blízkosti leží sídlo Aokawa i stanice stejného jména.",
  "RD-S08": "Krátká odbočka R3 zpřístupňuje hotelové zázemí u pláže Hoshimachi. Navazuje na pobřežní silnici a leží mezi hotelem a písečným pobřežím.",
  "RD-S12": "Příjezdová silnice R3 vede k pláži u Hoshimachi. Její poloha navazuje na plážový úsek a stejnojmennou zátoku.",
});
const kindDescription = (o, nearest) => {
  if (specialDescriptions[o.id]) return specialDescriptions[o.id];
  const sub = String(o.subtype || "").toLowerCase();
  const loc = (region[o.region] || { phrase: "v ostrovní krajině" }).phrase;
  const names = nearest.slice(0, 2).map((x) => x.name_cs);
  const around = names.length ? ` V okolí leží ${names.join(" a ")}.` : "";
  if (o.type === "settlement") return o.subtype === "hamlet" ? `Menší sídlo leží ${loc} a navazuje na místní dopravní síť.${around}` : `${typeLabel(o)} leží ${loc}.${around}`;
  if (o.type === "district") return `${atlasNames[o.id]} je jednou ze čtyř tradičních čtvrtí Larpingtonu. Její poloha navazuje na kompaktní uliční síť jižního městského centra.${around}`;
  if (o.type === "peak") return `${atlasNames[o.id]} vystupuje nad okolní lesnatou krajinou ${loc}. Pěší trasy v mapě propojují hřeben s blízkými vyhlídkami a sídly.${around}`;
  if (o.type === "nature") return `${typeLabel(o)} se nachází ${loc} a doplňuje soustavu místního reliéfu a vodstva.${around}`;
  if (o.type === "poi" && sub === "spring") return `Prameniště je zakreslené ${loc} v návaznosti na místní pěší síť a vodní toky.${around}`;
  if (o.type === "poi" && sub === "viewpoint") return `Vyhlídkové místo leží ${loc} u pobřeží nebo na vyvýšeném terénu. Přístup k němu vede po vyznačené trase či místní cestě.${around}`;
  if (o.type === "poi" && sub === "beach") return `Písečný úsek pobřeží leží ${loc}. Jeho poloha odpovídá jižnímu pobřeží hlavního ostrova nebo východnímu pobřeží Paralandu.${around}`;
  if (o.type === "poi" && sub === "paragliding_launch") return `Startovní místo leží ${loc} na horském svahu. V mapě navazuje na pěší trasu k okolním vrcholům.${around}`;
  if (o.type === "poi" && sub === "paragliding_landing") return `Přistávací louka leží pod horskými svahy ${loc} a navazuje na místní pěší síť.${around}`;
  if (o.type === "poi" && sub === "hotel_vip") return `Hotel leží ${loc} v pobřežním či horském návštěvnickém zázemí.${around}`;
  if (o.type === "poi" && sub === "lighthouse") return `Maják označuje severní pobřežní mys. Podle mapového podkladu slouží také jako vyhlídkové místo.${around}`;
  if (o.type === "poi" && sub === "castle") return `Hradní areál leží ${loc} a je součástí historických míst vyznačených na ostrově.${around}`;
  if (o.type === "poi" && sub === "ruin") return `Zřícenina leží ${loc} v návaznosti na pěší trasu mezi historickými místy.${around}`;
  if (o.type === "poi" && sub === "aquapark") return `Samostatný aquapark leží ${loc}; přístup k areálu je regulován rezervací.${around}`;
  if (o.type === "port") return `Přístav leží ${loc} u pobřežních dopravních tras. Jeho význam určuje místní rybářská, rekreační nebo nákladní funkce.${around}`;
  if (o.type === "rail_station") {
    const line = /^ST-L1/.test(o.id) ? "horskou linku L1" : /^ST-L2/.test(o.id) ? "linku L2" : /^ST-L3/.test(o.id) ? "městskou linku L3" : "městskou železniční síť";
    if (o.id === "ST-L2-09") return "Letištní výhybna slouží k odbočení z linky L2; nemá nástupiště a není určena k nástupu cestujících.";
    const linePhrase = line.replace("horskou linku", "horské lince").replace("linku L2", "lince L2").replace("městskou linku", "městské lince").replace("městskou železniční síť", "městské železniční síti");
    return `Stanice na ${linePhrase} leží ${loc} a zpřístupňuje okolní sídla, krajinu nebo dopravní uzly.${around}`;
  }
  if (o.type === "rail_line") return `${atlasNames[o.id]} je součástí železniční sítě souostroví. Její trasa propojuje uzly vyznačené v mapě.${around}`;
  if (o.type === "road" && (/^RD-S/.test(o.id) || /^RD-PL[234]/.test(o.id))) return `Přístupová silnice vede ${loc} k cíli uvedenému v názvu trasy.${around}`;
  if (o.type === "road") return `Silniční spojení ${atlasNames[o.id]} vede ${loc} a propojuje místa uvedená v názvu trasy.${around}`;
  if (o.type === "trail") return `Pěší trasa ${atlasNames[o.id]} vede ${loc} a propojuje pojmenované cíle v mapě.${around}`;
  if (o.type === "cycleway") return `Cyklotrasa ${atlasNames[o.id]} je součástí ostrovní sítě a propojuje sídla a dopravní uzly ${loc}.${around}`;
  if (o.type === "river") return `Vodní tok ${atlasNames[o.id]} odvádí vodu ${loc} směrem k nižším částem ostrova.${around}`;
  if (o.type === "coast_feature") return `${typeLabel(o)} vymezuje část členitého pobřeží ${loc}.${around}`;
  if (o.type === "infrastructure") return `Hráz zadržuje vodu přehradního jezera ${loc}. Okolní rekreační pobřeží je podřízeno ochraně vodního zdroje.${around}`;
  if (o.type === "industry") return `${typeLabel(o)} leží ${loc} u dopravních koridorů východního pobřeží.${around}`;
  if (o.type === "airport") return `Letištní plocha leží ${loc} a je napojena na silniční a železniční síť ostrova.${around}`;
  if (o.type === "other_line" && sub === "ski_run") return `Sjezdovka vede po strmějším svahu Zimní hory. Krátká zimní sezona omezuje její využití.`;
  if (o.type === "other_line" && sub === "ski_lift") return `Vlek zpřístupňuje svah Zimní hory a navazuje na místní sjezdovku; jeho využití omezuje krátká zimní sezona.`;
  return `${typeLabel(o)} leží ${loc} a navazuje na pojmenovaná místa v okolí.${around}`;
};
const scenicFor = (o) => {
  if (["M-01", "M-02", "M-03"].includes(o.id) || o.type === "peak") return "Lesnaté svahy přecházejí v horské louky a otevřené partie hřebenů; nejde o vysokohorskou krajinu.";
  if (o.type === "river" || ["N-03", "N-04", "DAM-N04"].includes(o.id)) return "Voda propojuje horské povodí, říční údolí a nižší části ostrova.";
  if (o.type === "coast_feature" || o.type === "port" || (o.type === "poi" && o.subtype === "beach")) return o.island === "para" ? "Pobřeží Paralandu střídá zátoky, pláže a zalesněné vnitrozemí." : "Členité pobřeží přechází od chráněných zátok k otevřeným výhledům na moře.";
  if (o.type === "poi" && o.subtype === "spring") return "Prameniště jsou zasazena do sítě horských toků a pěších cest; mapa neuvádí posouzení pitnosti.";
  if (o.island === "para") return "Zalesněné vnitrozemí Paralandu navazuje na pobřežní sídla; pohyb v chráněných částech ostrova je regulován.";
  if (o.type === "settlement") return o.region === "central_lowland" ? "Mírnější reliéf nížiny umožňuje přirozené propojení sídel silnicemi a železnicí." : "Městská a venkovská sídla navazují na okolní reliéf, vodstvo a dopravní trasy.";
  if (o.region === "west_northwest" || o.region === "central_west") return "Západní část ostrova tvoří lesnaté svahy, horské vodstvo a pěší trasy mezi vyhlídkami.";
  if (o.region === "south_southeast") return "Jižní pobřeží přechází od městské zástavby k plážím a lodním spojením.";
  if (o.region === "central_lowland") return "Centrální nížina propojuje sídla, zemědělskou krajinu a východo-západní dopravní osy.";
  if (o.region === "east_northeast" || o.region === "east") return "Východ ostrova spojuje pobřežní průmyslovou oblast s letištěm a městskými trasami.";
  return "Poloha a okolní vazby vycházejí z orientačního geografického modelu atlasu.";
};
const atmosphereFor = (o) => {
  if (o.type === "settlement" && o.id === "C-01") return "Kompaktní město s nepravidelnými ulicemi, dvory a historickým přístavem.";
  if (o.type === "settlement") return o.island === "para" ? "Menší pobřežní sídla a přírodní zázemí se střídají v krajině s regulovaným pohybem návštěvníků." : "Sídla propojují místní silnice a železniční zastávky; charakter okolí se mění od nížiny po horské svahy.";
  if (o.type === "rail_line" || o.type === "rail_station") return "Železnice tvoří jednu z hlavních vazeb mezi sídly, pobřežím a vnitrozemím.";
  if (o.type === "poi" && o.subtype === "viewpoint") return "Místo ke krátkému zastavení nad pobřežím nebo horskou krajinou.";
  if (o.type === "poi" && o.subtype === "spring") return "Klidný orientační bod na pěší trase v blízkosti vody.";
  if (o.island === "para") return "Ostrovní prostředí propojuje místní sídla s pobřežím a chráněnými přírodními plochami.";
  if (o.region === "west_northwest" || o.region === "central_west") return "Západní krajina spojuje horské trasy, vodní místa a menší sídla.";
  if (o.region === "south_southeast") return "Městský jih navazuje na přístavní a pobřežní prostředí.";
  return "Krajinný charakter určuje poloha mezi sídly a hlavními dopravními vazbami.";
};
for (const o of atlas) {
  const entry = editorial.atlas[o.id];
  entry.viewpoints = nearbyFor(o);
  entry.short_description_cs = kindDescription(o, entry.viewpoints);
  entry.highlights_cs = [];
  if (o.type === "rail_station" && (/^ST-L1/.test(o.id) || /^ST-L2/.test(o.id) || o.id === "ST-L3-05")) entry.highlights_cs = ["Stanice na provozovaném úseku železnice."];
  if (o.id === "P-01") entry.highlights_cs = ["Podmořský úsek se dokončuje; současné mezioostrovní spojení zajišťují lodě a trajekty."];
  entry.scenery_cs = scenicFor(o);
  entry.atmosphere_cs = atmosphereFor(o);
  if (o.type === "road" && !curatedRoadNames[o.id] && !curatedAtlasNames[o.id]) entry.public_name_cs = replaceRefs(entry.public_name_cs);
}

const districtLabels = Object.fromEntries(city.filter((o) => o.type === "district").map((o) => [o.id, o.name_cs]));
const districtPhrase = { "C-03": "Chalupecké čtvrti", "C-04": "Kynčlově čtvrti", "C-05": "Klimečkově čtvrti", "C-06": "Žemličkově čtvrti" };
const pointInRing = (point, ring) => {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i], [xj, yj] = ring[j];
    if (((yi > point[1]) !== (yj > point[1])) && point[0] < ((xj - xi) * (point[1] - yi)) / ((yj - yi) || 1e-12) + xi) inside = !inside;
  }
  return inside;
};
const districtAt = (o) => {
  if (o.district && districtLabels[o.district]) return o.district;
  for (const feature of districtsGeo) {
    const polygons = feature.geometry.type === "Polygon" ? [feature.geometry.coordinates] : feature.geometry.coordinates;
    if (polygons.some((polygon) => pointInRing([o.x_km, o.y_km], polygon[0]))) return feature.properties.id;
  }
  return null;
};
const pointSegmentDistance = (p, a, b) => {
  const dx = b[0] - a[0], dy = b[1] - a[1], d2 = dx * dx + dy * dy;
  const t = d2 ? Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / d2)) : 0;
  return Math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy));
};
const namedStreets = streets.filter((f) => f.properties.name_cs);
const nearestStreets = (o, limit = 2) => {
  const best = new Map();
  for (const feature of namedStreets) {
    const c = feature.geometry.coordinates; let d = Infinity;
    for (let i = 1; i < c.length; i++) d = Math.min(d, pointSegmentDistance([o.x_km, o.y_km], c[i - 1], c[i]));
    const name = feature.properties.name_cs;
    if (d < (best.get(name)?.d ?? Infinity)) best.set(name, { name, d });
  }
  return [...best.values()].sort((a, b) => a.d - b.d || a.name.localeCompare(b.name, "cs")).slice(0, limit);
};
const cityTypes = {
  residential_low: "Nízký obytný blok", residential_mid: "Obytný blok", old_town_mixed: "Blok starší městské zástavby",
  promenade_retail: "Obchodní blok u promenády", transit_mixed: "Blok u dopravního uzlu", retail_main: "Obchodní blok",
  civic_mixed: "Blok městské vybavenosti", new_waterfront: "Blok nového nábřeží", school: "Školní blok", hotel_premium: "Hotelový blok",
};
const streetGenitive = {
  "Hlavní třída": "Hlavní třídy", "Javorová ulice": "Javorové ulice", "Jihovýchodní bulvár": "Jihovýchodního bulváru",
  "Jihozápadní bulvár": "Jihozápadního bulváru", "Klimečkova třída": "Klimečkovy třídy", "Kostelní ulice": "Kostelní ulice",
  "Lipová ulice": "Lipové ulice", "Muzejní třída": "Muzejní třídy", "Nábřeží 16. června": "Nábřeží 16. června",
  "Okružní třída Náměstí čtyř": "Okružní třídy Náměstí čtyř", "Okružní ulice Starého Města": "Okružní ulice Starého Města",
  "Parková ulice": "Parkové ulice", "Pobřežní třída": "Pobřežní třídy", "Přístavní třída": "Přístavní třídy",
  "Přístavní ulice": "Přístavní ulice", "Přístup ke stanici Larpington Sever": "přístupu ke stanici Larpington Sever",
  "Přístup ke stanici Larpington Střed–Přístav": "přístupu ke stanici Larpington Střed–Přístav",
  "Přístup ke stanici Larpington Západ": "přístupu ke stanici Larpington Západ", "Rybářská ulice": "Rybářské ulice",
  "Severní sadová": "Severní sadové ulice", "Severní třída": "Severní třídy", "Severovýchodní bulvár": "Severovýchodního bulváru",
  "Severozápadní bulvár": "Severozápadního bulváru", "Skleněná ulice": "Skleněné ulice", "Tržní ulice": "Tržní ulice",
  "Třída Východního nábřeží": "Třídy Východního nábřeží", "Vinná ulice": "Vinné ulice", "Zahradní ulice": "Zahradní ulice",
  "Západní alej": "Západní aleje", "Školní třída": "Školní třídy",
};
const landUse = {
  residential_low: "nízkou obytnou zástavbu", residential_mid: "kompaktní obytnou zástavbu", old_town_mixed: "smíšené využití starší městské zástavby",
  promenade_retail: "obchody a služby podél nábřežní promenády", transit_mixed: "smíšené městské využití u dopravního uzlu",
  retail_main: "obchody a služby podél hlavní obchodní osy", civic_mixed: "městskou vybavenost", new_waterfront: "novější městskou zástavbu u nábřeží",
  school: "školní a vzdělávací zázemí", hotel_premium: "hotelové zázemí",
};
const cleanName = (o) => replaceRefs(String(o.name_cs || "").replace(/\s*\([^)]*(?:pracovní|prac\.|návrh|proposed)[^)]*\)/gi, ""));
const cityNames = {};
const blockCounts = new Map();
for (const o of city) {
  if (o.type !== "block") {
    cityNames[o.id] = o.id === "CP-01" ? "Plán Larpingtonu" : o.id === "CP-B07" ? "Historický kostel na Kostelním náměstí" : cleanName(o);
  } else {
    const districtId = districtAt(o), dname = districtPhrase[districtId] || "Larpingtonu";
    const street = replaceRefs(nearestStreets(o, 1)[0]?.name || "městské uliční síti").replace(/Přístup ke stanici stanice /g, "Přístup ke stanici ");
    const label = cityTypes[o.subtype] || "Městský blok";
    const key = `${districtId}|${street}|${o.subtype}`;
    const n = (blockCounts.get(key) || 0) + 1; blockCounts.set(key, n);
    const streetForm = streetGenitive[street] || street;
    cityNames[o.id] = `${label} u ${streetForm} (${dname})`;
    // Retain an ordinal only where the exact same contextual label would otherwise collide.
    if (n > 1) cityNames[o.id] += ` · část ${n}`;
  }
}
const cityNeighbors = city.filter((o) => o.type !== "block" && Number.isFinite(o.x_km) && Number.isFinite(o.y_km));
const cityById = new Map(city.map((o) => [o.id, o]));
for (const o of city) {
  const entry = editorial.capital[o.id];
  const districtId = districtAt(o), district = districtPhrase[districtId] || "Larpingtonu";
  const streetNames = o.type === "block" ? nearestStreets(o, 2).map((s) => s.name) : [];
  const close = cityNeighbors.filter((item) => item.id !== o.id).map((item) => ({ item, d: Math.hypot(o.x_km - item.x_km, o.y_km - item.y_km) }))
    .filter(({ d }) => d > 0.03).sort((a, b) => a.d - b.d || a.item.id.localeCompare(b.item.id)).slice(0, 3)
    .map(({ item, d }) => ({ place_id: item.id, name_cs: cityNames[item.id] || item.name_cs, direction_cs: bearing(o, item), distance_km: Number(d.toFixed(2)) }));
  const name = cityNames[o.id];
  const subtype = String(o.subtype || "").toLowerCase();
  let description, scenery;
  if (o.id === "CP-01") {
    description = "Orientační plán zachycuje kompaktní Larpington s nepravidelnými ulicemi, městskými bloky, parky a historickým přístavem. Rozlišuje čtyři tradiční čtvrti; univerzitně-kreativní zóna je potvrzena v kánonu, její přesný obvod však tento plán nevymezuje. Samostatné kampusové město neleží uvnitř městských čtvrtí.";
    scenery = "Nízká a středně vysoká zástavba se střídá s dvory, zahradami, parky a pobřežními veřejnými prostory.";
  } else if (o.type === "block") {
    const loc = streetNames.length > 1 ? `mezi ulicemi ${streetNames[0]} a ${streetNames[1]}` : streetNames[0] ? `u ulice ${streetNames[0]}` : "v městské uliční síti";
    description = `Plán vymezuje tuto plochu ${loc} v ${district} pro ${landUse[subtype] || "městské využití"}. Jde o jednu z ploch určených pro čtení v podrobném měřítku plánu.`;
    scenery = subtype.includes("old_town") ? "Okolí tvoří hustší bloky starší městské zástavby a nepravidelná uliční síť." : subtype.includes("waterfront") || subtype.includes("promenade") ? "Blok navazuje na pobřežní promenádu a veřejné prostory u vody." : subtype.includes("transit") ? "Městský prostor se váže na blízký uzel veřejné dopravy." : `Půdorys bloku doplňuje kompaktní uliční strukturu ${district}.`;
  } else if (o.type === "district") {
    description = `${name} je jednou ze čtyř tradičních čtvrtí Larpingtonu. Její ulice, veřejná prostranství a místní vybavenost tvoří část kompaktního jižního centra.`;
    scenery = `Městská struktura ${district} navazuje na nepravidelnou síť ulic, bloků a dvorů.`;
  } else if (o.type === "building" && subtype === "museum") {
    description = "Muzeum dějin Larpidie v Larpingtonu je otevřené. Interaktivní expozice využívá archivní materiály, filmovou rekonstrukci a komentované prohlídky; leží u Centrálního parku.";
    scenery = "Veřejný kulturní areál navazuje na park a okolní městské ulice.";
  } else if (o.type === "building" && subtype === "church") {
    description = `Historický kostel stojí na Kostelním náměstí v ${district}. Cihla a kámen jej propojují s měřítkem starší městské zástavby.`;
    scenery = "Kostelní náměstí a okolní bloky tvoří část historického městského prostředí.";
  } else if (o.type === "building" && subtype === "town_hall") {
    description = "Radnice leží v občanském centru Larpingtonu, v dosahu Náměstí čtyř a hlavních městských ulic. Její poloha propojuje správní funkce s veřejným prostorem centra.";
    scenery = "Veřejná budova navazuje na městské náměstí a nepravidelnou uliční síť.";
  } else if (o.type === "station") {
    description = `${name} obsluhuje městskou železniční síť a leží v ${district}. Její poloha navazuje na místní ulice a veřejná prostranství.`;
    scenery = "Stanice je součástí kompaktní městské struktury a propojuje čtvrti s hlavními dopravními směry.";
  } else if (o.type === "street") {
    const nearbyNames = close.filter((item) => cityById.get(item.place_id)?.type !== "street").slice(0, 2).map((item) => item.name_cs);
    const context = nearbyNames.length ? `; v okolí leží ${nearbyNames.join(" a ")}` : "; navazuje na místní veřejná prostranství a okolní ulice";
    description = `${name} je součástí uliční sítě v ${district}${context}.`;
    scenery = "Městské ulice střídají obchodní, obytné a veřejné prostory.";
  } else if (o.type === "square") {
    description = `${name} je veřejným prostranstvím v ${district}. Navazuje na okolní ulice a městské budovy.`;
    scenery = "Prostor náměstí je součástí pěší a veřejné sítě města.";
  } else if (o.type === "park") {
    description = `${name} tvoří zelenou plochu v ${district} a přerušuje souvislou městskou zástavbu.`;
    scenery = "Zeleň a pěší průchody propojují park s okolními městskými bloky.";
  } else if (o.type === "promenade") {
    description = `${name} sleduje pobřeží Larpingtonu a propojuje pěší veřejné prostory v přístavní části města.`;
    scenery = "Nábřeží spojuje otevřený pobřežní prostor s bloky města a přístavními přístupy.";
  } else if (o.type === "harbor") {
    description = "Historický přístav tvoří městské nábřeží s molem, přístavními budovami a návazností na starší zástavbu. Lodní spoje propojují Larpington s Paralandem.";
    scenery = "Přístavní prostředí spojuje vodní plochu, mola, promenádu a historické městské bloky.";
  } else if (o.type === "building" && subtype === "school") {
    description = `${name} doplňuje školní a vzdělávací zázemí ${district}. Je součástí městské vybavenosti v dosahu okolních ulic.`;
    scenery = "Školní areál je zasazen do kompaktní městské čtvrti.";
  } else if (o.type === "building") {
    description = `${name} patří k městské vybavenosti ${district}. Jeho poloha navazuje na okolní veřejné prostory a uliční síť.`;
    scenery = "Městské budovy a veřejná prostranství vytvářejí kompaktní prostředí čtvrti.";
  } else if (o.type === "shop" || o.type === "retail_zone") {
    description = `${name} navazuje na obchodní osu a pěší prostory ${district}. Poloha v plánu jej řadí do městského parteru.`;
    scenery = "Obchodní prostory se vážou na hlavní ulice a pěší pohyb městem.";
  } else if (o.type === "cafe") {
    description = `${name} je zakreslena v městském parteru ${district}, v návaznosti na okolní veřejné prostory.`;
    scenery = "Kavárenský parter doplňuje pěší prostředí městských ulic a náměstí.";
  } else if (o.type === "route") {
    description = `${name} propojuje bezbariérově přístupné veřejné prostory v městské síti Larpingtonu.`;
    scenery = "Trasa navazuje na městské náměstí, stanice a veřejné budovy podle svého vyznačeného průběhu.";
  } else if (o.type === "pier") {
    description = `${name} zpřístupňuje lodní dopravu v historickém přístavu Larpingtonu.`;
    scenery = "Molo propojuje městské nábřeží s vodní dopravou.";
  } else if (o.type === "rental") {
    description = `${name} doplňuje nabídku městské mobility v Larpingtonu a leží v dosahu veřejné dopravy nebo pobřeží.`;
    scenery = "Půjčovna navazuje na pěší, městské a pobřežní trasy.";
  } else {
    description = `${name} je součástí ${district} a jeho poloha navazuje na městské ulice a veřejná prostranství.`;
    scenery = "Městský prostor tvoří kompaktní bloky, nepravidelné ulice a místní veřejná vybavenost.";
  }
  const old = entry.aliases || [];
  if (o.name_cs && o.name_cs !== name && !old.includes(o.name_cs)) entry.aliases = [...old, o.name_cs];
  entry.public_name_cs = name;
  entry.category_cs = ({ plan: "Městský plán", district: "Městská čtvrť", building: "Budova", station: "Železniční stanice", square: "Veřejné prostranství", park: "Park", promenade: "Promenáda", harbor: "Přístav", pier: "Přístavní molo", street: "Městská ulice", block: cityTypes[subtype] || "Městský blok", shop: "Obchod", cafe: "Kavárna", rental: "Půjčovna", route: "Pěší trasa", retail_zone: "Obchodní oblast" })[o.type] || "Městské místo";
  entry.region_label_cs = districtLabels[districtId] || "Larpington";
  entry.subheading_cs = o.type === "plan" ? "Orientační plán hlavního města Larpingtonu" : `${entry.category_cs} v ${district}`;
  entry.short_description_cs = description;
  entry.highlights_cs = [];
  if (o.id === "CP-B06") entry.highlights_cs = ["Otevřené hlavní muzeum dějin Larpidie.", "Expozice pracuje s archivem, filmovou rekonstrukcí a komentovanými prohlídkami."];
  if (o.id === "CP-B07") entry.highlights_cs = ["Historický kostel na Kostelním náměstí."];
  if (o.type === "block" && streetNames[0]) entry.highlights_cs = [`Nejbližší pojmenovaná ulice: ${streetNames[0]}.`];
  entry.scenery_cs = scenery;
  entry.atmosphere_cs = o.type === "park" ? "Zelené plochy a pěší koridory přerušují souvislou zástavbu." : o.type === "harbor" || o.type === "pier" || o.type === "promenade" ? "Pobřežní část propojuje každodenní městský pohyb s historickým přístavem." : `Ulice, dvory a veřejné prostory utvářejí kompaktní prostředí ${district}.`;
  entry.viewpoints = close;
  entry.editorial_status = o.type === "block" ? "new_editorial_name" : entry.editorial_status || "derived_from_source";
  entry.source_reason = o.type === "block" ? `Název a popis jsou odvozeny z nejbližší skutečné uliční geometrie (${streetNames[0] || "městská uliční síť"}), typu plochy a příslušné městské čtvrti. Pořadové přípony rozlišují shodné lokální popisy; nejsou to adresy.` : entry.source_reason || "Popis vychází z existujícího typu objektu, městské čtvrti a pojmenované uliční geometrie.";
}

if (Object.keys(editorial.atlas).length !== 159 || Object.keys(editorial.capital).length !== 662) throw new Error("Počet redakčních záznamů se změnil.");
if (editorial.atlas["T-02"].public_name_cs !== "Cimprlichovo Hradiště") throw new Error("T-02 musí používat schválený zápis Cimprlichovo Hradiště.");
editorial.meta.refined_at = "2026-11-03";
fs.writeFileSync(outputPath, `${JSON.stringify(editorial, null, 2)}\n`, "utf8");
console.log(`Refined ${Object.keys(editorial.atlas).length} atlas and ${Object.keys(editorial.capital).length} city-plan editorial records.`);
