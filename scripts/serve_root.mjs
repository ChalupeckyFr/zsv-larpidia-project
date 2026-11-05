import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const root = fs.realpathSync(projectRoot);
const port = Number(process.argv[2] || 4174);
if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error("Port must be an integer from 0 to 65535.");
const mime = {
  ".html": "text/html; charset=utf-8", ".json": "application/json; charset=utf-8", ".md": "text/markdown; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml",
  ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".ico": "image/x-icon",
};

const server = http.createServer((request, response) => {
  if (request.method !== "GET" && request.method !== "HEAD") { response.writeHead(405).end(); return; }
  let urlPath;
  try { urlPath = decodeURIComponent(new URL(request.url, "http://localhost").pathname); }
  catch { response.writeHead(400).end(); return; }
  if (urlPath === "/") urlPath = "/index.html";
  const candidate = path.resolve(root, `.${urlPath}`);
  const relative = path.relative(root, candidate);
  if (!relative || relative.startsWith(`..${path.sep}`) || relative === ".." || path.isAbsolute(relative) || relative.split(path.sep).includes(".git")) {
    response.writeHead(403).end(); return;
  }
  let file;
  try {
    file = fs.realpathSync(candidate);
    const realRelative = path.relative(root, file);
    if (realRelative.startsWith(`..${path.sep}`) || realRelative === ".." || path.isAbsolute(realRelative) || !fs.statSync(file).isFile()) {
      response.writeHead(404).end(); return;
    }
  } catch { response.writeHead(404).end(); return; }
  const headers = { "Content-Type": mime[path.extname(file).toLowerCase()] || "application/octet-stream", "X-Content-Type-Options": "nosniff" };
  if (request.method === "HEAD") { response.writeHead(200, headers).end(); return; }
  response.writeHead(200, headers);
  fs.createReadStream(file).pipe(response);
});

server.listen(port, "127.0.0.1", () => console.log(`Larpidia source preview: http://127.0.0.1:${server.address().port}/`));
