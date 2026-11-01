import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "public");
if (!fs.existsSync(output)) throw new Error("Public export is missing. Run `node scripts/build_public_site.mjs` first.");
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));
const publicJson = (relative) => JSON.parse(fs.readFileSync(path.join(output, relative), "utf8"));
const slash = (value) => value.split(path.sep).join("/");
const catalog = readJson("content/larpidia/index.json");
const media = readJson("content/larpidia/media/assets.json");
const publicCatalog = publicJson("content/larpidia/index.json");
const publicMedia = publicJson("content/larpidia/media/assets.json");
const placeSource = readJson("atlas/current/registry/places.json");
const citySource = readJson("atlas/current/capital/cp_objects.json");
const places = publicJson("atlas/current/registry/places.public.json");
const city = publicJson("atlas/current/capital/cp_objects.public.json");

assert.equal(catalog.categories.reduce((n, category) => n + category.articles.length, 0), 39, "Expected the existing set of 39 public articles.");
assert.deepEqual(publicCatalog, catalog, "The public encyclopedia catalog must be preserved.");
assert.equal(publicMedia.assets.length, media.assets.length, "The public media list must preserve each available asset.");
assert.ok(publicMedia.assets.every((item) => Object.keys(item).every((key) => ["id", "src", "alt", "caption", "article", "kind"].includes(key))), "Production metadata must not enter the public media list.");

const byId = (items) => items.map((item) => item.id).sort();
assert.equal(places.objects.length, 159, "All 159 island atlas places must be retained.");
assert.equal(city.objects.length, 662, "All 662 Larpington plan objects must be retained.");
assert.deepEqual(byId(places.objects), byId(placeSource.objects), "Every island atlas ID must be present in the public projection.");
assert.deepEqual(byId(city.objects), byId(citySource.objects), "Every city plan ID must be present in the public projection.");
const positions = (items, keys) => items.map((item) => [item.id, ...keys.map((key) => item[key])]).sort(([a], [b]) => a.localeCompare(b));
assert.deepEqual(positions(places.objects, ["x_km", "y_km"]), positions(placeSource.objects, ["x_km", "y_km"]), "Public atlas coordinates must match the source registry exactly.");
assert.deepEqual(positions(city.objects, ["u", "v"]), positions(citySource.objects, ["u", "v"]), "Public city plan coordinates must match the source registry exactly.");
const safePlaceKeys = new Set(["id", "name_cs", "typeKey", "typeLabel", "islandKey", "islandLabel", "region", "x_km", "y_km", "elevationLabel"]);
const safeCityKeys = new Set([...safePlaceKeys, "u", "v"]);
assert.ok(places.objects.every((item) => Object.keys(item).every((key) => safePlaceKeys.has(key))), "The island registry contains only visitor-facing fields.");
assert.ok(city.objects.every((item) => Object.keys(item).every((key) => safeCityKeys.has(key))), "The city registry contains only visitor-facing fields.");
assert.ok(places.objects.every((item) => Number.isFinite(item.x_km) && Number.isFinite(item.y_km)), "All island atlas entries must be searchable and mappable.");
assert.ok(city.objects.every((item) => Number.isFinite(item.u) && Number.isFinite(item.v)), "All city plan entries must be searchable and mappable.");
assert.equal(city.objects.find((item) => item.id === "CP-B01")?.name_cs, "Radnice Larpingtonu");

const forbiddenViewerText = [/v1\.0-draft/i, /PRACOVNÍ MODEL/i, /photo_guide/i, /needs[_-]decision/i, /\bproposed\b/i, /\bBible\b/i, /parliament|parlament/i, /Aokawa/i, /name_proposed/i, /exist_status|name_status|pos_status/i];
for (const relative of ["atlas/current/viewer/atlas.html", "atlas/current/capital/capital_plan_viewer.html"]) {
  const html = fs.readFileSync(path.join(output, relative), "utf8");
  for (const pattern of forbiddenViewerText) assert.doesNotMatch(html, pattern, `Internal atlas wording remains in ${relative}: ${pattern}`);
}
const capital3d = fs.readFileSync(path.join(output, "atlas/current/capital/capital-3d.html"), "utf8");
assert.doesNotMatch(capital3d, /12\s*000|PRACOVNÍ MODEL|budoucí návrh v rezervě/i);
assert.match(capital3d, /Model neuvádí počet obyvatel/);
const terrain3d = fs.readFileSync(path.join(output, "atlas/current/viewer/terrain-3d.html"), "utf8");
assert.match(terrain3d, /3D reliéf Larpidie/);
assert.match(terrain3d, /přibližně 560 m n\. m\./);

const expected = new Set([
  "index.html", "site.js", "site.css", "encyclopedia.js", "project-meta.js", "project-metadata.json", "Larpidie logo.png",
  "content/larpidia/index.json", "content/larpidia/facts.json", "content/larpidia/media/assets.json",
  "atlas/current/renders/S-00_overview.jpg", "atlas/current/renders/S-00_overview_clouds.jpg",
  "atlas/current/renders/S-01_base.jpg", "atlas/current/renders/S-01_base_clouds.jpg",
  "atlas/current/renders/S-02_base.jpg", "atlas/current/renders/S-03_base.jpg",
  "atlas/photography/photos/LAR_PH_001.jpg", "atlas/current/capital/capital_plan_base.png",
  "atlas/current/viewer/terrain-3d-data.js", "atlas/current/viewer/island-r1-3d-data.js", "atlas/current/viewer/terrain-3d.html",
  "atlas/current/capital/capital-3d-data.js", "atlas/current/capital/capital-3d-nature.js", "atlas/current/capital/capital-3d.html",
  "atlas/current/registry/places.public.json", "atlas/current/viewer/atlas.html",
  "atlas/current/capital/cp_objects.public.json", "atlas/current/capital/capital_plan_viewer.html",
  "atlas/current/svg/transport_preview_embedded.svg", "atlas/current/svg/rail_scheme.svg", "atlas/current/svg/landcover_preview.svg",
  "gallery/assets/mountain.png", "gallery/assets/paraland.png",
]);
for (const category of catalog.categories) for (const article of category.articles) expected.add(`content/larpidia/${category.id}/${article.id}.md`);
for (const item of media.assets) expected.add(item.src);
const actual = [];
function walk(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) walk(absolute);
    else actual.push(slash(path.relative(output, absolute)));
  }
}
walk(output);
assert.deepEqual(actual.sort(), [...expected].sort(), "The deployment folder must match the explicit public allowlist.");

for (const relative of actual.filter((file) => file.endsWith(".js"))) {
  new vm.Script(fs.readFileSync(path.join(output, relative), "utf8"), { filename: relative });
}
for (const relative of actual.filter((file) => file.endsWith(".html"))) {
  const html = fs.readFileSync(path.join(output, relative), "utf8");
  for (const match of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const attrs = match[1];
    const body = match[2].trim();
    if (!body || /\btype\s*=\s*["']application\/(?:json|ld\+json)["']/i.test(attrs)) continue;
    new vm.Script(body, { filename: `${relative} inline script` });
  }
}

for (const blocked of ["references", "docs", "data", "scripts", "templates", "v1.1", "atlas/versions"]) {
  assert.ok(!fs.existsSync(path.join(output, blocked)), `Internal project directory was copied into public/: ${blocked}`);
}
console.log(`Public export check passed: ${actual.length} allowlisted files, 39 articles, 159 atlas places, 662 city objects; all public scripts parse.`);
