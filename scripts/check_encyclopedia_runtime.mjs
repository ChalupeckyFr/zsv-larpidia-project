import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));
const catalog = readJson("content/larpidia/index.json");
const facts = readJson("content/larpidia/facts.json");
facts.economy.corporateTaxPercent = 6;
facts.economy.tourism.modelAverageSpendCzkPerVisit = 16000;
facts.economy.workingHoursPerDay = 7;
const media = readJson("content/larpidia/media/assets.json");
let currentHash = "#encyklopedie/ekonomika/dane";
let hashChange;
const sharedPopulation = { dataset: { fact: "country.population", format: "number" }, textContent: "" };
const app = {
  innerHTML: "",
  querySelector: () => null,
  querySelectorAll: () => [],
};
const normalizedMarkup = () => app.innerHTML.replace(/[\s\u00a0\u202f]+/g, " ");

const documentStub = {
  querySelector: (selector) => selector === "[data-encyclopedia-app]" ? app : null,
  querySelectorAll: (selector) => selector === "[data-fact]" ? [sharedPopulation] : [],
  addEventListener: () => {},
};
const windowStub = {
  location: { get hash() { return currentHash; }, set hash(value) { currentHash = value; } },
  scrollTo: () => {},
  addEventListener: (name, callback) => { if (name === "hashchange") hashChange = callback; },
};
const fetchStub = async (url) => {
  const relative = String(url).replace(/^\//, "");
  const source = relative === "content/larpidia/facts.json"
    ? JSON.stringify(facts)
    : fs.readFileSync(path.join(root, relative), "utf8");
  return {
    ok: true,
    json: async () => JSON.parse(source),
    text: async () => source,
  };
};

vm.runInNewContext(fs.readFileSync(path.join(root, "encyclopedia.js"), "utf8"), {
  document: documentStub,
  window: windowStub,
  fetch: fetchStub,
  console,
});
await new Promise((resolve) => setTimeout(resolve, 0));

assert.match(normalizedMarkup(), /Daň ze zdanitelného zisku firem: <strong>6 %<\/strong>/, "Changing one central tax value updates the article text.");
assert.equal(sharedPopulation.textContent.replace(/[\s\u00a0\u202f]+/g, " "), "32 000", "The homepage fact component reads the shared population value.");

currentHash = "#encyklopedie/ekonomika/ekonomicky-model";
await hashChange();
assert.match(normalizedMarkup(), /640 000 000 Kč/, "Tourism turnover is recalculated after a central input changes.");
assert.match(normalizedMarkup(), /1 200 000 000 Kč/, "Enterprise transfer is calculated from profit and transfer share.");
assert.match(normalizedMarkup(), /240 000 000 Kč/, "Stabilization fund is calculated from the state transfer.");
assert.match(normalizedMarkup(), /1 377 280 000 Kč/, "The dependent partial funding scenario recalculates from its inputs.");

currentHash = "#encyklopedie/politika/schvalovani-zakonu";
await hashChange();
assert.match(normalizedMarkup(), /od <strong>15 let<\/strong>/, "Nested article URL renders its matching article.");

currentHash = "#encyklopedie/ekonomika/prace-a-mzdy";
await hashChange();
assert.match(normalizedMarkup(), /28 hodin týdně/, "The working-week summary recalculates from its central schedule inputs.");

console.log("Encyclopedia runtime checks passed: shared tax and population values, dependent formulas, schedule recalculation, and nested article routing.");
