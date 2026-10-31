import assert from "node:assert/strict";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const catalog = JSON.parse(fs.readFileSync(path.join(root, "content/larpidia/index.json"), "utf8"));
const media = JSON.parse(fs.readFileSync(path.join(root, "content/larpidia/media/assets.json"), "utf8"));
const mime = { ".html": "text/html; charset=utf-8", ".json": "application/json; charset=utf-8", ".md": "text/markdown; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg" };

const server = http.createServer((request, response) => {
  const urlPath = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
  const file = path.resolve(root, `.${urlPath}`);
  if (!file.startsWith(`${root}${path.sep}`) && file !== root) { response.writeHead(403).end(); return; }
  fs.readFile(file, (error, content) => {
    if (error) { response.writeHead(404).end(); return; }
    response.writeHead(200, { "Content-Type": mime[path.extname(file).toLowerCase()] || "application/octet-stream" });
    response.end(content);
  });
});

await new Promise((resolve, reject) => server.listen(0, "127.0.0.1", (error) => error ? reject(error) : resolve()));
const address = server.address();
const base = `http://127.0.0.1:${address.port}`;
try {
  const checks = ["index.html", "encyclopedia.js", "site.js", "site.css", "content/larpidia/index.json", "content/larpidia/facts.json", "content/larpidia/media/assets.json"];
  for (const category of catalog.categories) for (const article of category.articles) checks.push(`content/larpidia/${category.id}/${article.id}.md`);
  for (const item of media.assets) checks.push(item.src);
  const responses = await Promise.all(checks.map((file) => fetch(`${base}/${file}`)));
  const failures = responses.map((response, index) => response.ok ? null : `${checks[index]} → HTTP ${response.status}`).filter(Boolean);
  assert.deepEqual(failures, [], "Every page, content file, script, style, and registered media file must be served.");
  const html = await (await fetch(`${base}/index.html`)).text();
  assert.match(html, /href="\#encyklopedie" data-nav="encyklopedie"/, "The existing encyclopedia menu remains present.");
  console.log(`Static HTTP smoke check passed: ${checks.length} content and asset paths returned successfully.`);
} finally {
  await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}
