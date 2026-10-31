import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dataRoot = path.join(root, "content", "larpidia");
const errors = [];
const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const exists = (relative) => fs.existsSync(path.join(root, relative));
const getPath = (object, dotted) => dotted.split(".").reduce((value, key) => value == null ? undefined : value[key], object);

let catalog;
let facts;
let media;
try {
  catalog = readJson(path.join(dataRoot, "index.json"));
  facts = readJson(path.join(dataRoot, "facts.json"));
  media = readJson(path.join(dataRoot, "media", "assets.json"));
} catch (error) {
  console.error(`JSON could not be read: ${error.message}`);
  process.exit(1);
}

const articles = [];
const ids = new Set();
for (const category of catalog.categories || []) {
  if (!category.id || !category.title || !Array.isArray(category.articles)) errors.push(`Invalid category entry: ${JSON.stringify(category)}`);
  for (const article of category.articles || []) {
    const route = `${category.id}/${article.id}`;
    if (ids.has(route)) errors.push(`Duplicate article route: ${route}`);
    ids.add(route);
    const relative = `content/larpidia/${route}.md`;
    if (!exists(relative)) { errors.push(`Missing article file: ${relative}`); continue; }
    const source = fs.readFileSync(path.join(root, relative), "utf8");
    if (!article.title || !article.summary || !source.trim()) errors.push(`Missing metadata or empty article: ${route}`);
    articles.push({ ...article, category });
    for (const [, sourceType, factPath] of source.matchAll(/\{\{(fact|calc)\.([\w.]+)(?:\|[\w]+)?\}\}/g)) {
      const resolved = sourceType === "fact" ? getPath(facts, factPath) : facts.derived?.[factPath.split(".").at(-1)];
      if (resolved === undefined) errors.push(`Unknown ${sourceType} token ${factPath} in ${route}`);
    }
    for (const [, assetId] of source.matchAll(/!\[[^\]]*\]\(asset:([\w-]+)\)/g)) {
      if (!(media.assets || []).some((item) => item.id === assetId)) errors.push(`Unknown image id ${assetId} in ${route}`);
    }
    for (const [, hash] of source.matchAll(/\]\((#encyklopedie[^)]*)\)/g)) {
      const parts = hash.replace(/^#encyklopedie\/?/, "").split("/").filter(Boolean);
      if (parts.length === 2 && !ids.has(`${parts[0]}/${parts[1]}`) && !catalog.categories.some((item) => item.id === parts[0] && item.articles.some((entry) => entry.id === parts[1]))) {
        errors.push(`Broken encyclopedia link ${hash} in ${route}`);
      }
      if (parts.length === 1 && !catalog.categories.some((item) => item.id === parts[0])) errors.push(`Broken category link ${hash} in ${route}`);
    }
    const lower = source.toLocaleLowerCase("cs-CZ");
    if (/demokraticky voleným parlamentem|parlament a mimořádná pojistka|celý podmořský úsek l3 je v provozu/.test(lower)) errors.push(`Stale canon wording detected in ${route}`);
  }
}

const assetIds = new Set();
for (const item of media.assets || []) {
  if (assetIds.has(item.id)) errors.push(`Duplicate media id: ${item.id}`);
  assetIds.add(item.id);
  if (!item.src || !item.alt || !exists(item.src)) errors.push(`Missing media file, path, or alt text: ${item.id} (${item.src})`);
  if (item.article && !ids.has(item.article)) errors.push(`Media ${item.id} references unknown article ${item.article}`);
}

const requiredFacts = [
  ["country.population", 32000], ["country.mainIslandAreaKm2", 175], ["country.paralandAreaKm2", 14], ["country.currencyCode", "CZK"],
  ["constitution.coRulers", 4], ["constitution.votingAge", 15], ["economy.corporateTaxPercent", 5],
  ["economy.vat.standardPercent", 12], ["economy.vat.reducedPercent", 5],
  ["pensions.basicMonthlyCzk", 12000], ["pensions.ageYears", 65],
];
for (const [key, expected] of requiredFacts) if (getPath(facts, key) !== expected) errors.push(`Canon value mismatch for ${key}: expected ${expected}`);
if (facts.economy.workingDaysPerWeek * facts.economy.workingHoursPerDay !== 24) errors.push("The central working schedule no longer calculates to the canon 24-hour week.");

const corporateTaxReferences = articles.reduce((count, article) => {
  const source = fs.readFileSync(path.join(dataRoot, article.category.id, `${article.id}.md`), "utf8");
  return count + [...source.matchAll(/\{\{fact\.economy\.corporateTaxPercent\|percent\}\}/g)].length;
}, 0);
if (corporateTaxReferences < 1) errors.push("Company tax has no shared fact reference in any article.");

const indexHtml = fs.readFileSync(path.join(root, "index.html"), "utf8");
const css = fs.readFileSync(path.join(root, "site.css"), "utf8");
const appJs = fs.readFileSync(path.join(root, "encyclopedia.js"), "utf8");
const appView = (indexHtml.match(/<section class="view page-view" id="view-encyklopedie"[\s\S]*?<\/section>/) || [""])[0];
if (!appView.includes("data-encyclopedia-app")) errors.push("The original encyclopedia view is not mounted to the new content app.");
if (!indexHtml.includes("href=\"#encyklopedie\" data-nav=\"encyklopedie\"")) errors.push("The original encyclopedia menu route is missing.");
if (!appJs.includes("#encyklopedie/")) errors.push("Nested encyclopedia routes are not handled.");
if (!/@media\s*\(max-width:\s*720px\)/.test(css) || !css.includes(".ency-layout")) errors.push("Responsive encyclopedia styles are missing.");
if (/demokraticky volený parlament|20–40\s*<small>tis\.|150–200\s*<small>km²/.test(indexHtml)) errors.push("Stale homepage facts remain in the original view.");
if (/demokraticky voleným parlamentem|20 až 40 tisíc obyvatel/.test(fs.readFileSync(path.join(root, "larpidia-encyklopedie.md"), "utf8"))) errors.push("The legacy Markdown export still contains public encyclopedia text.");

if (errors.length) {
  console.error(`Encyclopedia validation failed (${errors.length} issue${errors.length === 1 ? "" : "s"}):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`Encyclopedia validation passed: ${catalog.categories.length} categories, ${articles.length} articles, ${media.assets.length} registered media files.`);
