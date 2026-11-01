import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const registryPath = path.join(root, "atlas/current/capital/cp_objects.json");
const viewerPath = path.join(root, "atlas/current/capital/capital_plan_viewer.html");
const registry = JSON.parse(fs.readFileSync(registryPath, "utf8"));
if (!Array.isArray(registry.objects) || registry.objects.length !== 662) throw new Error("Expected all 662 Larpington plan objects.");

const townHall = registry.objects.find((item) => item.id === "CP-B01");
const southStation = registry.objects.find((item) => item.id === "ST-S");
if (!townHall || !southStation) throw new Error("The town hall or ST-S registry entry is missing.");
townHall.name_cs = "Radnice Larpingtonu";
townHall.name_en = "Larpington Town Hall";
townHall.notes = String(townHall.notes || "").replace(/Radnice a sídlo parlamentu/i, "Radnice");
townHall.bible_ref = String(townHall.bible_ref || "").replace(/politics\.elected_parliament\s*\(approved\);?\s*/i, "");
if (!townHall.bible_ref) townHall.bible_ref = "capital_roles: státní instituce";
southStation.notes = String(southStation.notes || "").replace(/\bparlament,?\s*/i, "").replace(/\s{2,}/g, " ").trim();
registry.meta.status_note = "exist_status approved jen pro schválená místa a prvky hlavní infrastruktury";

const viewer = fs.readFileSync(viewerPath, "utf8");
const marker = /(<script type="application\/json" id="reg">)[\s\S]*?(<\/script>)/;
if (!marker.test(viewer)) throw new Error("Embedded city registry marker is missing from the capital plan viewer.");
let updatedViewer = viewer.replace(marker, (_match, open, close) => `${open}${JSON.stringify(registry)}${close}`);
updatedViewer = updatedViewer
  .replace('placeholder="ID nebo název (např. CP-B01, parlament, tržnice)"', 'placeholder="ID nebo název (např. CP-B01, radnice, tržnice)"')
  .replace(">Parliament</text>", ">Town Hall</text>")
  .replace("Stavy: schváleno = parlament, muzeum, historický přístav C-02; vše ostatní (jména, polohy, využití bloků) je návrh. Sever nahoře, východ vpravo.", "Orientační plán města; názvy a některé polohy jsou schematické. Sever nahoře, východ vpravo.");

fs.writeFileSync(registryPath, `${JSON.stringify(registry, null, 1)}\n`, "utf8");
fs.writeFileSync(viewerPath, updatedViewer, "utf8");
console.log("Synchronized the 662-object city plan registry and removed obsolete parliamentary labels.");
