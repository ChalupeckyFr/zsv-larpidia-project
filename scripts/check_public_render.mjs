import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = path.join(root, "public");
if (!fs.existsSync(publicRoot)) throw new Error("Run `node scripts/build_public_site.mjs` before the browser check.");
const sourceIndex = fs.readFileSync(path.join(root, "index.html"), "utf8");
const devStatusButton = sourceIndex.match(/<button\b[^>]*data-media-status-open[^>]*>[\s\S]*?<\/button>/i)?.[0];
const devStatusDialog = sourceIndex.match(/<dialog\b[^>]*id="media-status-dialog"[\s\S]*?<\/dialog>/i)?.[0];
if (!devStatusButton || !devStatusDialog) throw new Error("The author-only media status controls are missing from index.html.");
const devStatusMarkup = `${devStatusButton}${devStatusDialog}`;
const devStatusScript = fs.readFileSync(path.join(root, "scripts/dev_media_status.js"), "utf8")
  .replace("document.currentScript?.src", JSON.stringify("http://127.0.0.1/scripts/dev_media_status.js"));
const devMediaManifest = JSON.parse(fs.readFileSync(path.join(root, "content/larpidia/media/assets.json"), "utf8"));
const devMediaAvailablePaths = [...new Set([
  ...devMediaManifest.assets.filter((asset) => asset.public && asset.gallery).map((asset) => asset.src),
  ...devMediaManifest.scenes.map((scene) => scene.photo_path).filter(Boolean),
])].filter((relative) => fs.existsSync(path.join(root, ...relative.split(/[\\/]/))));
const chromeCandidates = [
  path.join(process.env["ProgramFiles(x86)"] || "C:/Program Files (x86)", "Microsoft/Edge/Application/msedge.exe"),
  path.join(process.env.ProgramFiles || "C:/Program Files", "Microsoft/Edge/Application/msedge.exe"),
];
const browserPath = chromeCandidates.find((candidate) => fs.existsSync(candidate));
if (!browserPath) throw new Error("Microsoft Edge was not found. Install Edge or update chromeCandidates in this script.");

const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "larpidia-public-render-"));
const profile = path.join(tempRoot, "edge-profile");
const screenshots = path.join(tempRoot, "screenshots");
fs.mkdirSync(screenshots, { recursive: true });
const server = spawn(process.execPath, [path.join(root, "scripts/serve_static.mjs"), "0"], { cwd: root, stdio: ["ignore", "pipe", "pipe"] });
let serverError = "";
server.stderr.setEncoding("utf8").on("data", (chunk) => { serverError += chunk; });
const base = await new Promise((resolve, reject) => {
  let stdout = "";
  const timeout = setTimeout(() => reject(new Error(`Static server did not start: ${serverError}`)), 10_000);
  server.stdout.setEncoding("utf8").on("data", (chunk) => {
    stdout += chunk;
    const match = stdout.match(/http:\/\/127\.0\.0\.1:(\d+)\//);
    if (match) { clearTimeout(timeout); resolve(`http://127.0.0.1:${match[1]}`); }
  });
  server.once("error", (error) => { clearTimeout(timeout); reject(error); });
  server.once("exit", (code) => { clearTimeout(timeout); reject(new Error(`Static server exited (${code}): ${serverError}`)); });
});

const browser = spawn(browserPath, [
  "--headless=new", "--no-sandbox", "--disable-renderer-code-integrity", "--disable-features=RendererCodeIntegrity",
  "--disable-gpu", "--disable-extensions", "--disable-background-networking", "--no-first-run", "--no-default-browser-check",
  "--remote-debugging-port=0", `--user-data-dir=${profile}`, "about:blank",
], { stdio: ["ignore", "ignore", "pipe"] });
let browserError = "";
browser.stderr.setEncoding("utf8").on("data", (chunk) => { browserError += chunk; });
let browserExit = null;
browser.on("exit", (code, signal) => { browserExit = { code, signal }; });
let cdp;
let targetSessionId;
let messageId = 0;
const pending = new Map();
const events = new Map();
const runtimeErrors = [];
const networkFailures = [];
const requestUrls = new Map();

function onEvent(name, callback) {
  if (!events.has(name)) events.set(name, new Set());
  events.get(name).add(callback);
  return () => events.get(name)?.delete(callback);
}

function waitEvent(name, timeoutMs = 15_000) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { off(); reject(new Error(`Timed out waiting for ${name}`)); }, timeoutMs);
    const off = onEvent(name, (params) => { clearTimeout(timer); off(); resolve(params); });
  });
}

async function call(method, params = {}) {
  const id = ++messageId;
  const result = new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP ${method} timed out`)); }, 10_000);
    pending.set(id, { resolve: (value) => { clearTimeout(timer); resolve(value); }, reject: (error) => { clearTimeout(timer); reject(error); } });
  });
  cdp.send(JSON.stringify({ id, method, params, ...(targetSessionId && method !== "Target.createTarget" && method !== "Target.attachToTarget" ? { sessionId: targetSessionId } : {}) }));
  return result;
}

async function evaluate(expression) {
  const result = await call("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true, userGesture: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  return result.result?.value;
}

async function connectToBrowser() {
  const activePortFile = path.join(profile, "DevToolsActivePort");
  for (let i = 0; i < 600 && !fs.existsSync(activePortFile) && !browserExit; i++) await new Promise((resolve) => setTimeout(resolve, 50));
  if (!fs.existsSync(activePortFile)) throw new Error(`Edge did not open a DevTools endpoint (${JSON.stringify(browserExit)}): ${browserError}`);
  const [port, browserPathname] = fs.readFileSync(activePortFile, "utf8").trim().split(/\r?\n/);
  cdp = new WebSocket(`ws://127.0.0.1:${port}${browserPathname}`);
  await new Promise((resolve, reject) => {
    cdp.addEventListener("open", resolve, { once: true });
    cdp.addEventListener("error", reject, { once: true });
  });
  cdp.addEventListener("message", (event) => {
    const raw = event.data;
    const decode = typeof raw === "string" ? Promise.resolve(raw) : raw.text();
    decode.then((serialized) => {
    const message = JSON.parse(serialized);
    if (message.id) {
      const request = pending.get(message.id);
      if (!request) return;
      pending.delete(message.id);
      if (message.error) request.reject(new Error(`${message.error.code}: ${message.error.message}`));
      else request.resolve(message.result || {});
      return;
    }
    if (message.method === "Runtime.exceptionThrown") runtimeErrors.push(message.params.exceptionDetails?.exception?.description || message.params.exceptionDetails?.text || "Runtime exception");
    if (message.method === "Network.requestWillBeSent") requestUrls.set(message.params.requestId, message.params.request.url);
    if (message.method === "Network.loadingFailed" && requestUrls.get(message.params.requestId)?.startsWith(base)) networkFailures.push(`${requestUrls.get(message.params.requestId)} (${message.params.errorText})`);
    for (const callback of events.get(message.method) || []) callback(message.params);
    }).catch((error) => console.error(`CDP message decode failed: ${error.message}`));
  });
  const target = await call("Target.createTarget", { url: "about:blank" });
  const attached = await call("Target.attachToTarget", { targetId: target.targetId, flatten: true });
  targetSessionId = attached.sessionId;
  await call("Page.enable");
  await call("Runtime.enable");
  await call("Network.enable");
  await call("Log.enable");
  await call("Emulation.setDeviceMetricsOverride", { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });
  return `http://127.0.0.1:${port}`;
}

async function navigate(url) {
  await call("Page.navigate", { url });
  console.log(`Navigating ${url}`);
  const targetUrl = new URL(url).href;
  let state;
  for (let i = 0; i < 200; i++) {
    state = await evaluate("({href:location.href,ready:document.readyState})").catch(() => null);
    if (state?.href === targetUrl && state.ready === "complete") break;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  if (state?.href !== targetUrl || state.ready !== "complete") throw new Error(`Page did not finish loading ${targetUrl}: ${JSON.stringify(state)}`);
  await new Promise((resolve) => setTimeout(resolve, 250));
}

async function screenshot(name) {
  const image = await call("Page.captureScreenshot", { format: "png", captureBeyondViewport: false, fromSurface: true });
  fs.writeFileSync(path.join(screenshots, `${name}.png`), Buffer.from(image.data, "base64"));
}

async function setSearch(value) {
  await evaluate(`(()=>{const q=document.querySelector('#q');q.value=${JSON.stringify(value)};q.dispatchEvent(new Event('input',{bubbles:true}));return q.value})()`);
  await new Promise((resolve) => setTimeout(resolve, 80));
}

async function selectFirstResult() {
  await evaluate(`document.querySelector('#results button[data-id]')?.click()`);
  await new Promise((resolve) => setTimeout(resolve, 100));
}

async function pointFor(selector) {
  return evaluate(`(()=>{const els=[...document.querySelectorAll(${JSON.stringify(selector)})];for(const el of els){const r=el.getBoundingClientRect();if(r.width>=4&&r.height>=4&&r.right>0&&r.bottom>0&&r.left<innerWidth&&r.top<innerHeight)return {x:r.left+r.width/2,y:r.top+r.height/2,tag:el.tagName,id:el.getAttribute('data-id'),w:r.width,h:r.height}}return null})()`);
}

async function mouseClick(point) {
  if (!point) throw new Error("No visible SVG feature was found for the click test.");
  await call("Input.dispatchMouseEvent", { type: "mouseMoved", x: point.x, y: point.y });
  await call("Input.dispatchMouseEvent", { type: "mousePressed", x: point.x, y: point.y, button: "left", clickCount: 1 });
  await call("Input.dispatchMouseEvent", { type: "mouseReleased", x: point.x, y: point.y, button: "left", clickCount: 1 });
  await new Promise((resolve) => setTimeout(resolve, 100));
}

async function touchTap(point) {
  if (!point) throw new Error("No visible SVG feature was found for the touch test.");
  await call("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x: point.x, y: point.y, id: 1, radiusX: 3, radiusY: 3, force: 1 }] });
  await call("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
  await new Promise((resolve) => setTimeout(resolve, 100));
}

async function bodyText() {
  return evaluate("document.body.innerText");
}

try {
  const devtoolsBase = await connectToBrowser();
  const failures = [];
  const screenshotsForReport = [];
  const check = async (label, action) => {
    try { await action(); console.log(`PASS ${label}`); }
    catch (error) { failures.push(`${label}: ${error.message}`); console.error(`FAIL ${label}: ${error.message}`); }
  };

  await check("atlas loads records, layers and search without runtime errors", async () => {
    await navigate(`${base}/atlas/current/viewer/atlas.html`);
    const state = await evaluate(`(async()=>{const records=await fetch('../registry/places.public.json').then(r=>r.json());return {count:document.querySelector('#count').textContent,recordCount:records.objects.length,layerCount:document.querySelectorAll('#layers input[data-l]').length,searchCount:!!document.querySelector('#search-count'),map:!!document.querySelector('#map svg')}})()`);
    assert.equal(state.recordCount, 159); assert.match(state.count, /159/); assert.ok(state.layerCount >= 15); assert.ok(state.searchCount && state.map);
  });

  await check("atlas hidden ID, English and diacritic-insensitive search render clean Czech results", async () => {
    await setSearch("T-01");
    let result = await evaluate(`({text:document.querySelector('#results').innerText,count:document.querySelector('#results button')?.dataset.id,ids:[...document.querySelectorAll('#results button')].map(x=>x.innerText)})`);
    assert.equal(result.count, "T-01"); assert.match(result.text, /Praha/); assert.doesNotMatch(result.text, /T-01|schváleno|návrh/i);
    await selectFirstResult();
    let details = await evaluate(`document.querySelector('#info').innerText`);
    assert.match(details, /Praha/); assert.match(details, /Anglicky: Prague/); assert.match(details, /Japonsky: プラハ/); assert.match(details, /Město v centrální nížině hlavního ostrova/i); assert.match(details, /Atlasové souřadnice:/); assert.match(details, /Nadmořská výška:/); assert.doesNotMatch(details, /T-01|status|Bible|pseudo|pracovní|draft|modelové/i);
    assert.doesNotMatch(await bodyText(), /T-01|C-01|CP-[A-Z0-9-]+|v1\.0-draft|PRACOVNÍ MODEL|návrh jména|pseudo \(hypotetické\)|Bible\/zadání|Foto \/ video vodítko|schváleno × návrh/i);
    await setSearch("prague"); assert.match(await evaluate(`document.querySelector('#results').innerText`), /Praha/);
    await setSearch("pristav"); assert.match(await evaluate(`document.querySelector('#results').innerText`), /přístav/i);
    await setSearch("T-02");
    const t02 = await evaluate(`(()=>({id:document.querySelector('#results button')?.dataset.id,text:document.querySelector('#results').innerText}))()`);
    assert.equal(t02.id, "T-02"); assert.match(t02.text, /Cimprlichovo Hradiště/); assert.doesNotMatch(t02.text, /T-02|schváleno|návrh/i);
    await selectFirstResult();
    const t02Details = await evaluate(`document.querySelector('#info').innerText`);
    assert.match(t02Details, /Cimprlichovo Hradiště/); assert.match(t02Details, /Japonsky: チンプルリフ砦/); assert.match(t02Details, /MĚSTO V JIŽNÍ ČÁSTI HLAVNÍHO OSTROVA/);
    assert.doesNotMatch(t02Details, /T-02|schváleno|návrh|Bible|pseudo|výška \(model\)|modelová kóta/i);
    await setSearch("qzxwvv-no-place"); assert.match(await evaluate(`document.querySelector('#search-count').innerText`), /nenašli/);
  });

  await check("atlas rendered map click updates the place detail repeatedly", async () => {
    await setSearch("T-01"); await selectFirstResult();
    const target = await pointFor('#map svg [data-id="T-01"].interactive');
    assert.ok(target, "Praha map feature was not visible after zooming to its result.");
    await mouseClick(target);
    let detail = await evaluate(`document.querySelector('#info').innerText`);
    assert.match(detail, /Praha/); assert.doesNotMatch(detail, /T-01/);
    await setSearch("C-01"); await selectFirstResult();
    const second = await pointFor('#map svg [data-id="C-01"].interactive');
    assert.ok(second, "Larpington map feature was not visible after zooming to its result.");
    await mouseClick(second);
    detail = await evaluate(`document.querySelector('#info').innerText`);
    assert.match(detail, /Larpington/); assert.doesNotMatch(detail, /C-01|prac\./i);
    assert.equal(await evaluate(`document.querySelector('#layer-settings').open`), false);
    await screenshot("atlas-desktop-selected"); screenshotsForReport.push(path.join(screenshots, "atlas-desktop-selected.png"));
  });

  await check("atlas pan, zoom, language layers and navigation remain available", async () => {
    const before = await evaluate(`document.querySelector('#map svg').getAttribute('viewBox')`);
    const mapCenter = await evaluate(`(()=>{const r=document.querySelector('#map').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`);
    await call("Input.dispatchMouseEvent", { type: "mouseMoved", x: mapCenter.x, y: mapCenter.y });
    await call("Input.dispatchMouseEvent", { type: "mousePressed", x: mapCenter.x, y: mapCenter.y, button: "left", clickCount: 1 });
    await call("Input.dispatchMouseEvent", { type: "mouseMoved", x: mapCenter.x + 20, y: mapCenter.y + 10, button: "left" });
    await call("Input.dispatchMouseEvent", { type: "mouseReleased", x: mapCenter.x + 20, y: mapCenter.y + 10, button: "left", clickCount: 1 });
    await call("Input.dispatchMouseEvent", { type: "mouseWheel", x: mapCenter.x, y: mapCenter.y, deltaY: -120, deltaX: 0 });
    await new Promise((resolve) => setTimeout(resolve, 100));
    const after = await evaluate(`document.querySelector('#map svg').getAttribute('viewBox')`);
    assert.notEqual(after, before);
    await evaluate(`document.querySelector('button[data-lang="ja"]').click()`);
    assert.equal(await evaluate(`document.querySelector('#labels-ja').style.display`), "");
    assert.equal(await evaluate(`document.querySelector('button[data-lang="ja"]').innerText`), "Japonština");
    assert.match(await evaluate(`document.querySelector('a.head-link').getAttribute('href')`), /terrain-3d\.html/);
  });

  await check("Larpington loads 662 records and CP-B01 search stays hidden in results and details", async () => {
    await navigate(`${base}/atlas/current/capital/capital_plan_viewer.html`);
    const state = await evaluate(`(async()=>{const records=await fetch('cp_objects.public.json').then(r=>r.json());return {count:document.querySelector('#count').textContent,recordCount:records.objects.length,layerCount:document.querySelectorAll('#layers input[data-l]').length,searchCount:!!document.querySelector('#search-count'),map:!!document.querySelector('#map svg')}})()`);
    assert.equal(state.recordCount, 662); assert.match(state.count, /662/); assert.ok(state.layerCount >= 10); assert.ok(state.searchCount && state.map);
    await setSearch("CP-B01");
    let result = await evaluate(`({text:document.querySelector('#results').innerText,id:document.querySelector('#results button')?.dataset.id})`);
    assert.equal(result.id, "CP-B01"); assert.match(result.text, /Radnice Larpingtonu/); assert.doesNotMatch(result.text, /CP-B01|approved|proposed/i);
    await selectFirstResult();
    let details = await evaluate(`document.querySelector('#info').innerText`);
    assert.match(details, /Radnice Larpingtonu/); assert.doesNotMatch(details, /CP-B01|existence|Bible|foto|video|proposed/i);
    assert.doesNotMatch(await bodyText(), /T-\d+|C-\d+|CP-[A-Z0-9-]+|v1\.0-draft|PRACOVNÍ MODEL|návrh jména|pseudo \(hypotetické\)|Bible\/zadání|Foto \/ video vodítko|schváleno × návrh/i);
  });

  await check("a real Larpington SVG object responds to repeated map clicks", async () => {
    const point = await pointFor('#map svg [data-id="CP-B01"]');
    assert.ok(point, "Town Hall feature was not visible after selecting its result.");
    await mouseClick(point);
    let details = await evaluate(`document.querySelector('#info').innerText`);
    assert.match(details, /Radnice Larpingtonu/); assert.doesNotMatch(details, /CP-B01/);
    await setSearch("CP-B02"); await selectFirstResult();
    const next = await pointFor('#map svg [data-id="CP-B02"]');
    assert.ok(next, "Second city feature was not visible after selection.");
    await mouseClick(next);
    details = await evaluate(`document.querySelector('#info').innerText`);
    assert.doesNotMatch(details, /CP-B02/);
    await screenshot("capital-desktop-selected"); screenshotsForReport.push(path.join(screenshots, "capital-desktop-selected.png"));
  });

  await check("gallery visibly loads all local media, with no broken image cards", async () => {
    await navigate(`${base}/index.html#galerie`);
    const state = await evaluate(`new Promise(resolve=>{const check=()=>{const imgs=[...document.querySelectorAll('[data-gallery-grid] img')];if(imgs.length>=2&&imgs.every(i=>i.complete))resolve({count:imgs.length,loaded:imgs.filter(i=>i.naturalWidth>0).length,images:imgs.map(i=>({src:i.getAttribute('src'),w:i.naturalWidth,alt:i.alt})),brand:[...document.querySelectorAll('.site-brand-logo')].map(i=>({src:i.currentSrc,alt:i.alt,w:i.naturalWidth}))});else setTimeout(check,100)};check()})`);
    assert.equal(state.count, 2); assert.equal(state.loaded, 2); assert.ok(state.brand.length >= 1 && state.brand.every((item) => item.w > 0 && item.alt === "Larpidie"));
    assert.equal(await evaluate(`!!document.querySelector('[data-media-status-open],#media-status-dialog')`), false);
    await screenshot("gallery-desktop"); screenshotsForReport.push(path.join(screenshots, "gallery-desktop.png"));
    await navigate(`${base}/index.html#encyklopedie/zakladni-informace/prehled`);
    await new Promise((resolve) => setTimeout(resolve, 150));
    const articleImages = await evaluate(`({broken:[...document.querySelectorAll('img')].filter(i=>i.getAttribute('src')&&i.complete&&!i.naturalWidth).map(i=>i.getAttribute('src')),logo:[...document.querySelectorAll('.site-brand-logo')].map(i=>({alt:i.alt,w:i.naturalWidth}))})`);
    assert.deepEqual(articleImages.broken, []); assert.ok(articleImages.logo.length && articleImages.logo.every((item) => item.alt === "Larpidie" && item.w > 0));
  });

  await check("author-only image status dialog computes available photos and missing scenes", async () => {
    await navigate(`${base}/index.html#galerie`);
    const status = await evaluate(`(async()=>{document.querySelector('#view-galerie footer')?.insertAdjacentHTML('beforeend',${JSON.stringify(devStatusMarkup)});const manifest=${JSON.stringify(devMediaManifest)},paths=new Set(${JSON.stringify(devMediaAvailablePaths)}),originalFetch=window.fetch.bind(window);window.fetch=(input,options={})=>{const href=input instanceof URL?input.href:typeof input==='string'?input:input.url;const url=new URL(href,location.href);if(url.pathname.endsWith('/content/larpidia/media/assets.json'))return Promise.resolve({ok:true,json:()=>Promise.resolve(manifest)});if(String(options.method||'GET').toUpperCase()==='HEAD')return Promise.resolve({ok:paths.has(decodeURIComponent(url.pathname.replace(/^\\/+/,'')))});return originalFetch(input,options)};(0,eval)(${JSON.stringify(devStatusScript)});const button=document.querySelector('[data-media-status-open]'),dialog=document.querySelector('#media-status-dialog');button.focus();button.click();for(let i=0;i<150&&!dialog.open;i++)await new Promise(resolve=>setTimeout(resolve,20));return {opened:dialog.open,photos:dialog.querySelector('[data-media-photo-count]').textContent,missing:dialog.querySelector('[data-media-missing-count]').textContent,availableCount:dialog.querySelector('[data-media-available]').children.length,availableTitles:[...dialog.querySelector('[data-media-available]').children].map(item=>item.textContent),missingItems:dialog.querySelector('[data-media-missing]').children.length,focusOnClose:document.activeElement===dialog.querySelector('[data-media-status-close]')}})()`);
    assert.equal(status.opened, true, `Modal did not open: ${JSON.stringify(status)}`); assert.equal(status.photos, "2"); assert.equal(status.missing, "18"); assert.equal(status.availableCount, 2); assert.equal(status.availableTitles.length, 2); assert.equal(status.missingItems, 18); assert.equal(status.focusOnClose, true, `Close button did not receive focus: ${JSON.stringify(status)}`);
    await screenshot("dev-media-status-desktop"); screenshotsForReport.push(path.join(screenshots, "dev-media-status-desktop.png"));
    await evaluate(`document.querySelector('[data-media-status-close]').click()`);
    await new Promise((resolve) => setTimeout(resolve, 50));
    const restored = await evaluate(`(()=>({closed:!document.querySelector('#media-status-dialog').open,focusReturned:document.activeElement===document.querySelector('[data-media-status-open]'),active:document.activeElement?.outerHTML?.slice(0,120)}))()`);
    assert.ok(restored.closed && restored.focusReturned, `Dialog did not close and restore focus: ${JSON.stringify(restored)}`);
    await evaluate(`document.querySelector('[data-media-status-open]').click()`);
    await evaluate(`new Promise(resolve=>{const check=()=>document.querySelector('#media-status-dialog').open?resolve(true):setTimeout(check,10);check()})`);
    await call("Input.dispatchKeyEvent", { type: "keyDown", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
    await call("Input.dispatchKeyEvent", { type: "keyUp", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
    await new Promise((resolve) => setTimeout(resolve, 50));
    const escaped = await evaluate(`(()=>({closed:!document.querySelector('#media-status-dialog').open,focusReturned:document.activeElement===document.querySelector('[data-media-status-open]')}))()`);
    assert.ok(escaped.closed && escaped.focusReturned, `Escape did not close the dialog and restore focus: ${JSON.stringify(escaped)}`);
  });

  await check("responsive atlas and gallery fit a narrow screen and keep the search drawer reachable", async () => {
    await call("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
    await navigate(`${base}/atlas/current/viewer/atlas.html`);
    let mobile = await evaluate(`({width:innerWidth,scroll:document.documentElement.scrollWidth,trigger:getComputedStyle(document.querySelector('#open-search')).display,button:!!document.querySelector('#open-search')})`);
    assert.equal(mobile.width, 390); assert.ok(mobile.scroll <= mobile.width + 2); assert.notEqual(mobile.trigger, "none"); assert.ok(mobile.button);
    await evaluate(`document.querySelector('#open-search').click()`);
    assert.equal(await evaluate(`document.body.classList.contains('search-open')`), true);
    await setSearch("T-01"); await selectFirstResult();
    assert.equal(await evaluate(`document.body.classList.contains('search-open')`), false);
    await touchTap(await pointFor('#map svg [data-id="T-01"].interactive'));
    assert.match(await evaluate(`document.querySelector('#info').innerText`), /Praha/);
    await screenshot("atlas-mobile-selected"); screenshotsForReport.push(path.join(screenshots, "atlas-mobile-selected.png"));
    const mobileDetail = await evaluate(`(()=>{const panel=document.querySelector('aside.r'),footer=document.querySelector('body>footer'),heading=panel.querySelector('#info h3');const scrollable=panel.scrollHeight>panel.clientHeight;heading?.scrollIntoView({block:'end'});return {scrollable,scrollTop:panel.scrollTop,panelTop:panel.getBoundingClientRect().top,panelBottom:panel.getBoundingClientRect().bottom,footerTop:footer.getBoundingClientRect().top,headingTop:heading?.getBoundingClientRect().top,headingBottom:heading?.getBoundingClientRect().bottom}})()`);
    assert.ok(mobileDetail.headingTop >= mobileDetail.panelTop - 1 && mobileDetail.headingBottom <= mobileDetail.panelBottom + 1, "The place heading should be reachable inside the mobile detail panel.");
    assert.ok(mobileDetail.panelBottom <= mobileDetail.footerTop + 1, "The mobile footer must not overlap the place detail panel.");
    await navigate(`${base}/atlas/current/capital/capital_plan_viewer.html`);
    mobile = await evaluate(`(()=>{const link=document.querySelector('header .city3d-link').getBoundingClientRect(),title=document.querySelector('header h1').getBoundingClientRect(),note=document.querySelector('header>span').getBoundingClientRect();return {width:innerWidth,scroll:document.documentElement.scrollWidth,trigger:getComputedStyle(document.querySelector('#open-search')).display,linkRight:link.right,linkTop:link.top,titleBottom:title.bottom,noteBottom:note.bottom}})()`);
    assert.ok(mobile.scroll <= mobile.width + 2); assert.notEqual(mobile.trigger, "none");
    assert.ok(mobile.linkRight <= mobile.width && mobile.linkTop >= mobile.titleBottom && mobile.linkTop >= mobile.noteBottom, "The Larpington mobile header and 3D link must not overlap or clip.");
    await evaluate(`document.querySelector('#open-search').click()`);
    await setSearch("CP-B01"); await selectFirstResult();
    await touchTap(await pointFor('#map svg [data-id="CP-B01"]'));
    assert.match(await evaluate(`document.querySelector('#info').innerText`), /Radnice Larpingtonu/);
    await screenshot("capital-mobile-selected"); screenshotsForReport.push(path.join(screenshots, "capital-mobile-selected.png"));
    await navigate(`${base}/index.html#galerie`);
    const gallery = await evaluate(`new Promise(resolve=>{const check=()=>{const imgs=[...document.querySelectorAll('[data-gallery-grid] img')];if(imgs.length>=2&&imgs.every(i=>i.complete))resolve({width:innerWidth,scroll:document.documentElement.scrollWidth,loaded:imgs.filter(i=>i.naturalWidth).length,columns:getComputedStyle(document.querySelector('[data-gallery-grid]')).gridTemplateColumns});else setTimeout(check,100)};check()})`);
    assert.ok(gallery.scroll <= gallery.width + 2); assert.equal(gallery.loaded, 2);
    await screenshot("gallery-mobile"); screenshotsForReport.push(path.join(screenshots, "gallery-mobile.png"));
  });

  await check("public and author-only paths are separated in the served export", async () => {
    const paths = ["references/LARPIDIA_USTAVNI_KANON_PRACOVNI_v2.6.md", "docs/LARPIDIA_PUBLIC_ATLAS_GALLERY_REPAIR_REPORT.md", "v1.1/LARPIDIA_VISUAL_ATLAS_STORY_PACK_v1_2/03_PHOTO_PROMPTS/ALL_PHOTO_PROMPTS.md", "scripts/dev_media_status.js", "atlas/current/registry/places.json", "atlas/current/capital/cp_objects.json"];
    for (const file of paths) assert.equal((await fetch(`${base}/${file}`)).status, 404, `${file} must stay private.`);
    const publicManifest = await fetch(`${base}/content/larpidia/media/assets.json`).then((response) => response.json());
    assert.equal(publicManifest.scenes, undefined); assert.equal(publicManifest.excluded, undefined);
    assert.ok(publicManifest.assets.every((asset) => !("provenance" in asset) && !("status" in asset) && !("relatedPlaceId" in asset)));
  });

  const fullText = await bodyText().catch(() => "");
  assert.doesNotMatch(fullText, /v1\.0-draft|PRACOVNÍ MODEL|návrh jména|pseudo \(hypotetické\)|Bible\/zadání|Foto \/ video vodítko/i);
  if (runtimeErrors.length) failures.push(`Uncaught browser runtime errors: ${runtimeErrors.join("; ")}`);
  if (networkFailures.length) failures.push(`Browser network failures: ${networkFailures.join("; ")}`);
  if (failures.length) throw new Error(failures.join("\n"));
  console.log(`Rendered public export passed in Edge. Screenshots: ${screenshotsForReport.join(", ")}`);
} finally {
  if (cdp?.readyState === WebSocket.OPEN) { try { cdp.close(); } catch {} }
  if (browser.exitCode === null) {
    browser.kill();
    await Promise.race([new Promise((resolve) => browser.once("exit", resolve)), new Promise((resolve) => setTimeout(resolve, 3_000))]);
  }
  if (server.exitCode === null) {
    server.kill();
    await new Promise((resolve) => server.once("exit", resolve));
  }
  if (process.env.LARPIDIA_KEEP_RENDER_SCREENSHOTS === "1") console.log(`Render evidence retained in ${tempRoot}`);
  else try { fs.rmSync(tempRoot, { recursive: true, force: true, maxRetries: 5, retryDelay: 150 }); } catch {}
}
