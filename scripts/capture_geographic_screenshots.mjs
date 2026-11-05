import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { once } from "node:events";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = path.join(root, "docs/debug-screenshots");
fs.mkdirSync(outDir, { recursive: true });
const phase = process.argv[2] || "after";
const browserPath = [
  path.join(process.env["ProgramFiles(x86)"] || "C:/Program Files (x86)", "Microsoft/Edge/Application/msedge.exe"),
  path.join(process.env.ProgramFiles || "C:/Program Files", "Microsoft/Edge/Application/msedge.exe"),
].find((candidate) => fs.existsSync(candidate));
if (!browserPath) throw new Error("Microsoft Edge was not found.");

const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "larpidia-geography-"));
const profile = path.join(tempRoot, "edge-profile");
const server = spawn(process.execPath, [path.join(root, "scripts/serve_static.mjs"), "0"], { cwd: root, stdio: ["ignore", "pipe", "pipe"] });
let serverError = "";
server.stderr.setEncoding("utf8").on("data", (chunk) => { serverError += chunk; });
const base = await new Promise((resolve, reject) => {
  let stdout = "";
  const timer = setTimeout(() => reject(new Error(`Static server did not start: ${serverError}`)), 10_000);
  server.stdout.setEncoding("utf8").on("data", (chunk) => {
    stdout += chunk;
    const match = stdout.match(/http:\/\/127\.0\.0\.1:(\d+)\//);
    if (match) { clearTimeout(timer); resolve(`http://127.0.0.1:${match[1]}`); }
  });
  server.once("error", (error) => { clearTimeout(timer); reject(error); });
});
const browser = spawn(browserPath, [
  "--headless=new", "--no-sandbox", "--disable-renderer-code-integrity", "--disable-features=RendererCodeIntegrity",
  "--disable-gpu", "--disable-extensions", "--disable-background-networking", "--no-first-run", "--no-default-browser-check",
  "--remote-debugging-port=0", `--user-data-dir=${profile}`, "about:blank",
], { stdio: ["ignore", "ignore", "pipe"] });
let browserError = "";
browser.stderr.setEncoding("utf8").on("data", (chunk) => { browserError += chunk; });
let cdp;
let sessionId;
let messageId = 0;
const pending = new Map();
const runtimeErrors = [];
const call = async (method, params = {}) => {
  const id = ++messageId;
  const response = new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP ${method} timed out`)); }, 12_000);
    pending.set(id, { resolve: (value) => { clearTimeout(timer); resolve(value); }, reject: (error) => { clearTimeout(timer); reject(error); } });
  });
  cdp.send(JSON.stringify({ id, method, params, ...(sessionId && method !== "Target.attachToTarget" ? { sessionId } : {}) }));
  return response;
};
const evaluate = async (expression) => {
  const result = await call("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true, userGesture: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  return result.result?.value;
};
const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const connect = async () => {
  const activePortFile = path.join(profile, "DevToolsActivePort");
  for (let i = 0; i < 600 && !fs.existsSync(activePortFile); i++) await pause(50);
  if (!fs.existsSync(activePortFile)) throw new Error(`Edge did not open DevTools: ${browserError}`);
  const [port, endpoint] = fs.readFileSync(activePortFile, "utf8").trim().split(/\r?\n/);
  cdp = new WebSocket(`ws://127.0.0.1:${port}${endpoint}`);
  await new Promise((resolve, reject) => { cdp.addEventListener("open", resolve, { once: true }); cdp.addEventListener("error", reject, { once: true }); });
  cdp.addEventListener("message", (event) => {
    Promise.resolve(typeof event.data === "string" ? event.data : event.data.text()).then((raw) => {
      const message = JSON.parse(raw);
      if (message.id) {
        const request = pending.get(message.id);
        if (!request) return;
        pending.delete(message.id);
        if (message.error) request.reject(new Error(message.error.message)); else request.resolve(message.result || {});
      } else if (message.method === "Runtime.exceptionThrown") {
        runtimeErrors.push(message.params.exceptionDetails?.exception?.description || message.params.exceptionDetails?.text || "Runtime exception");
      }
    });
  });
  const target = await call("Target.createTarget", { url: "about:blank" });
  sessionId = (await call("Target.attachToTarget", { targetId: target.targetId, flatten: true })).sessionId;
  await call("Page.enable"); await call("Runtime.enable");
  await call("Emulation.setDeviceMetricsOverride", { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
};
const navigate = async (url) => {
  await call("Page.navigate", { url });
  const target = new URL(url).href;
  for (let i = 0; i < 200; i++) {
    const state = await evaluate("({href:location.href,ready:document.readyState})").catch(() => null);
    if (state?.href === target && state.ready === "complete") break;
    await pause(100);
  }
  await pause(1800);
};
const screenshot = async (name) => {
  const image = await call("Page.captureScreenshot", { format: "png", captureBeyondViewport: false, fromSurface: true });
  fs.writeFileSync(path.join(outDir, `${name}.png`), Buffer.from(image.data, "base64"));
};

try {
  await connect();
  const terrainUrl=`${base}/atlas/current/viewer/terrain-3d.html`;
  await navigate(terrainUrl);
  const terrainCheck=await evaluate(`(()=>{const w=window.LARPIDIA_ATLAS_WORLD,d=window.LARPIDIA_TERRAIN_DATA;return {axes:w?.axes,anchor:w?.toAtlas(...w.toWorld(6.96,5.44)),sample_m:d?.sample_m,heightEncoding:d?.height_encoding,highest:d?.max_elevation_m,roads:d?.roads?.length,visibleRoads:d?.roads?.filter(x=>!['tunnel','cave','undersea'].includes(x.section)).length,railways:d?.railways?.length,visibleRailways:d?.railways?.filter(x=>!['tunnel','cave','undersea'].includes(x.section)).length,hasExaggeration:!!document.querySelector('#exaggeration,#exag-value')}})()`);
  if(!terrainCheck.axes?.includes('+X east')||terrainCheck.anchor[0]!==6.96||terrainCheck.anchor[1]!==5.44||terrainCheck.sample_m!==40||terrainCheck.highest!==560||terrainCheck.roads!==62||terrainCheck.visibleRoads!==59||terrainCheck.railways!==26||terrainCheck.visibleRailways!==17||terrainCheck.hasExaggeration)throw new Error(`Terrain sanity check failed: ${JSON.stringify(terrainCheck)}`);
  await evaluate(`document.getElementById('view-north-up').click()`);await pause(350);await screenshot(`geography-${phase}-3d-island-north-up`);
  await evaluate(`document.getElementById('view-reservoir').click()`);await pause(350);await screenshot(`geography-${phase}-3d-reservoir`);
  await evaluate(`document.getElementById('view-west-coast').click()`);await pause(350);await screenshot(`geography-${phase}-3d-west-coast`);
  await evaluate(`document.getElementById('view-overview').click()`);await pause(350);await screenshot(`geography-${phase}-3d-roads-overview`);
  console.log(`Saved four verified terrain views for ${phase}.`);

  await navigate(`${base}/atlas/current/capital/capital-3d.html`);
  await evaluate(`document.querySelector('[data-city-style="nature"]').click()`);await pause(350);await screenshot(`geography-${phase}-3d-larpington`);
  await navigate(`${base}/atlas/current/capital/capital_plan_viewer.html`);
  await screenshot(`geography-${phase}-city-2d`);
  await navigate(`${base}/atlas/current/viewer/atlas.html`);
  const marker=await evaluate(`(()=>{const e=[...document.querySelectorAll('#map svg [data-id="C-01"]')].find(x=>x.localName==='circle');return {tag:e?.localName,role:e?.getAttribute('role'),tabindex:e?.getAttribute('tabindex'),points:e?.getAttribute('points'),count:document.querySelectorAll('#map svg [data-id="C-01"]').length}})()`);
  if(marker.tag!=='circle'||marker.points!==null||marker.tabindex==='-1')throw new Error(`Capital marker is not the expected restrained circle: ${JSON.stringify(marker)}`);
  await screenshot(`geography-${phase}-atlas-2d`);
  console.log(`Saved all six geography screenshots for ${phase}.`);
  console.log(`Runtime exceptions: ${runtimeErrors.length ? runtimeErrors.join(" | ") : "none"}`);
  if (runtimeErrors.length) process.exitCode = 1;
} finally {
  cdp?.close();
  if (browser.exitCode === null) { const exited = once(browser, "exit"); browser.kill(); await exited; }
  if (server.exitCode === null) { const exited = once(server, "exit"); server.kill(); await exited; }
  fs.rmSync(tempRoot, { recursive: true, force: true });
}
