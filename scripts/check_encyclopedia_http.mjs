import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = path.join(root, "public");
if (!fs.existsSync(publicRoot)) throw new Error("Public export is missing. Run `node scripts/build_public_site.mjs` first.");
const catalog = JSON.parse(fs.readFileSync(path.join(publicRoot, "content/larpidia/index.json"), "utf8"));
const media = JSON.parse(fs.readFileSync(path.join(publicRoot, "content/larpidia/media/assets.json"), "utf8"));

const child = spawn(process.execPath, [path.join(root, "scripts/serve_static.mjs"), "0"], { cwd: root, stdio: ["ignore", "pipe", "pipe"] });
let stderr = "";
child.stderr.setEncoding("utf8").on("data", (chunk) => { stderr += chunk; });
const base = await new Promise((resolve, reject) => {
  let stdout = "";
  const timeout = setTimeout(() => reject(new Error(`Static server did not start: ${stderr}`)), 8000);
  child.stdout.setEncoding("utf8").on("data", (chunk) => {
    stdout += chunk;
    const match = stdout.match(/http:\/\/127\.0\.0\.1:(\d+)\//);
    if (match) { clearTimeout(timeout); resolve(`http://127.0.0.1:${match[1]}`); }
  });
  child.once("error", (error) => { clearTimeout(timeout); reject(error); });
  child.once("exit", (code) => { clearTimeout(timeout); reject(new Error(`Static server exited (${code}): ${stderr}`)); });
});

try {
  const paths = [
    "", "index.html", "site.js", "site.css", "encyclopedia.js", "project-meta.js", "project-metadata.json",
    "atlas/current/viewer/atlas.html", "atlas/current/viewer/terrain-3d.html", "atlas/current/capital/capital_plan_viewer.html",
    "atlas/current/capital/capital-3d.html", "atlas/current/viewer/terrain-3d-data.js", "atlas/current/viewer/island-r1-3d-data.js",
    "atlas/current/capital/capital-3d-data.js", "atlas/current/capital/capital-3d-nature.js",
    "atlas/current/registry/places.public.json", "atlas/current/capital/cp_objects.public.json",
    "atlas/current/capital/capital_plan_base.png", "atlas/current/svg/transport_preview_embedded.svg",
    "atlas/current/svg/rail_scheme.svg", "atlas/current/svg/landcover_preview.svg",
    "atlas/current/renders/S-00_overview.jpg", "atlas/current/renders/S-00_overview_clouds.jpg",
    "atlas/current/renders/S-01_base.jpg", "atlas/current/renders/S-01_base_clouds.jpg",
    "atlas/current/renders/S-02_base.jpg", "atlas/current/renders/S-03_base.jpg", "atlas/photography/photos/LAR_PH_001.jpg",
    "gallery/assets/mountain.png", "gallery/assets/paraland.png",
    "content/larpidia/index.json", "content/larpidia/facts.json", "content/larpidia/media/assets.json",
  ];
  for (const category of catalog.categories) for (const article of category.articles) paths.push(`content/larpidia/${category.id}/${article.id}.md`);
  for (const item of media.assets) paths.push(item.src);
  const responses = await Promise.all(paths.map((file) => fetch(`${base}/${file}`)));
  const failures = responses.map((response, index) => response.ok ? null : `${paths[index]} → HTTP ${response.status}`).filter(Boolean);
  assert.deepEqual(failures, [], "Every public page, content file, script, style, model, and registered media asset must be served.");
  assert.equal(responses[0].headers.get("x-content-type-options"), "nosniff");

  const blocked = [
    "references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md", "references/LARPIDIA_CODEX_SCHVALENE_OPRAVY_PO_AUDITU_v1.md",
    "docs/LARPIDIA_PUBLIC_CONTENT_AUDIT.md", "docs/LARPIDIA_ATLAS_SEARCH_REVIEW.md", "data/larpidia_world_bible.json",
    "atlas/current/registry/places.json", "atlas/current/capital/cp_objects.json", "scripts/build_public_site.mjs",
    "v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/README_START_HERE.md",
  ];
  for (const file of blocked) {
    const response = await fetch(`${base}/${file}`);
    assert.equal(response.status, 404, `Internal file must not be served: ${file}`);
  }
  assert.equal((await fetch(`${base}/`, { method: "HEAD" })).status, 200, "HEAD requests should work for the public home page.");
  assert.equal((await fetch(`${base}/`, { method: "POST" })).status, 405, "Unsupported methods should be rejected.");

  const html = await (await fetch(`${base}/index.html`)).text();
  assert.match(html, /href="#encyklopedie" data-nav="encyklopedie"/, "The existing encyclopedia menu remains present.");
  assert.match(html, /gallery\/assets\/mountain\.png/, "The public gallery uses its available mountain image.");
  console.log(`Static HTTP smoke check passed: ${paths.length} public paths served; ${blocked.length} internal paths returned 404.`);
} finally {
  if (child.exitCode === null) {
    child.kill();
    await new Promise((resolve) => child.once("exit", resolve));
  }
}
