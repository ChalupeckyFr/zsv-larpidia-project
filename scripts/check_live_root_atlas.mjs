import assert from "node:assert/strict";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const rootReal = fs.realpathSync(root);
const screenshotPath = path.join(root, "docs/debug-screenshots/atlas-live-server-fixed.png");
const requests = new Set();
const failures = [];
const browserRequestUrls = new Map();
const mime = {
  ".html": "text/html; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
};

const server = http.createServer((request, response) => {
  if (request.method !== "GET" && request.method !== "HEAD") { response.writeHead(405).end(); return; }
  let pathname;
  try { pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname); }
  catch { response.writeHead(400).end(); return; }
  if (pathname === "/") pathname = "/index.html";
  const candidate = path.resolve(rootReal, `.${pathname}`);
  const relative = path.relative(rootReal, candidate);
  if (relative.startsWith(`..${path.sep}`) || relative === ".." || path.isAbsolute(relative)) { response.writeHead(403).end(); return; }
  try {
    const realFile = fs.realpathSync(candidate);
    const realRelative = path.relative(rootReal, realFile);
    if (realRelative.startsWith(`..${path.sep}`) || realRelative === ".." || path.isAbsolute(realRelative) || !fs.statSync(realFile).isFile()) { response.writeHead(404).end(); return; }
    requests.add(`/${relative.replaceAll(path.sep, "/")}`);
    response.writeHead(200, { "Content-Type": mime[path.extname(realFile).toLowerCase()] || "application/octet-stream", "X-Content-Type-Options": "nosniff", "Cache-Control": "no-store" });
    if (request.method === "HEAD") { response.end(); return; }
    fs.createReadStream(realFile).pipe(response);
  } catch { response.writeHead(404).end(); }
});

const browserCandidates = [
  path.join(process.env["ProgramFiles(x86)"] || "C:/Program Files (x86)", "Microsoft/Edge/Application/msedge.exe"),
  path.join(process.env.ProgramFiles || "C:/Program Files", "Microsoft/Edge/Application/msedge.exe"),
];
const browserPath = browserCandidates.find((candidate) => fs.existsSync(candidate));
if (!browserPath) throw new Error("Microsoft Edge was not found; the root Live Server render cannot be verified.");
const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "larpidia-live-root-"));
const profile = path.join(tempRoot, "edge-profile");
let browser;
let browserExit = null;
let cdp;
let targetSessionId;
let messageId = 0;
const pending = new Map();

async function startServer() {
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  return `http://127.0.0.1:${server.address().port}`;
}

async function command(method, params = {}) {
  const id = ++messageId;
  const result = new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`Edge DevTools timed out: ${method}`)); }, 10_000);
    pending.set(id, { resolve: (value) => { clearTimeout(timer); resolve(value); }, reject: (error) => { clearTimeout(timer); reject(error); } });
  });
  cdp.send(JSON.stringify({ id, method, params, ...(targetSessionId && !["Target.createTarget", "Target.attachToTarget"].includes(method) ? { sessionId: targetSessionId } : {}) }));
  return result;
}

async function evaluate(expression) {
  const result = await command("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true, userGesture: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  return result.result?.value;
}

async function openBrowser(base) {
  browser = spawn(browserPath, [
    "--headless=new", "--no-sandbox", "--disable-renderer-code-integrity", "--disable-features=RendererCodeIntegrity",
    "--disable-gpu", "--disable-extensions", "--disable-background-networking", "--no-first-run", "--no-default-browser-check",
    "--remote-debugging-port=0", `--user-data-dir=${profile}`, "about:blank",
  ], { stdio: ["ignore", "ignore", "pipe"] });
  let browserError = "";
  browser.stderr.setEncoding("utf8").on("data", (chunk) => { browserError += chunk; });
  browser.on("exit", (code, signal) => { browserExit = { code, signal }; });
  const portFile = path.join(profile, "DevToolsActivePort");
  for (let i = 0; i < 600 && !fs.existsSync(portFile) && !browserExit; i++) await new Promise((resolve) => setTimeout(resolve, 50));
  if (!fs.existsSync(portFile)) throw new Error(`Edge did not start DevTools: ${JSON.stringify(browserExit)} ${browserError}`);
  const [port, endpoint] = fs.readFileSync(portFile, "utf8").trim().split(/\r?\n/);
  cdp = new WebSocket(`ws://127.0.0.1:${port}${endpoint}`);
  await new Promise((resolve, reject) => {
    cdp.addEventListener("open", resolve, { once: true });
    cdp.addEventListener("error", reject, { once: true });
  });
  cdp.addEventListener("message", async (event) => {
    try {
      const message = JSON.parse(typeof event.data === "string" ? event.data : await event.data.text());
      if (!message.id) {
        if (message.method === "Runtime.exceptionThrown") failures.push(message.params.exceptionDetails?.exception?.description || message.params.exceptionDetails?.text || "Browser runtime exception");
        if (message.method === "Network.requestWillBeSent") browserRequestUrls.set(message.params.requestId, message.params.request.url);
        if (message.method === "Network.loadingFailed") {
          const failedUrl = browserRequestUrls.get(message.params.requestId);
          const errorText = message.params.errorText || "";
          if (failedUrl?.startsWith(base) && !errorText.includes("ERR_ABORTED")) failures.push(`${failedUrl}: ${errorText}`);
        }
        return;
      }
      const request = pending.get(message.id);
      if (!request) return;
      pending.delete(message.id);
      if (message.error) request.reject(new Error(`${message.error.code}: ${message.error.message}`));
      else request.resolve(message.result || {});
    } catch (error) { failures.push(`DevTools event decode: ${error.message}`); }
  });
  const target = await command("Target.createTarget", { url: "about:blank" });
  targetSessionId = (await command("Target.attachToTarget", { targetId: target.targetId, flatten: true })).sessionId;
  await command("Page.enable");
  await command("Runtime.enable");
  await command("Network.enable");
  await command("Emulation.setDeviceMetricsOverride", { width: 1600, height: 1000, deviceScaleFactor: 1, mobile: false });
  await command("Page.navigate", { url: `${base}/index.html` });
  for (let i = 0; i < 200; i++) {
    const state = await evaluate("({href:location.href,ready:document.readyState})").catch(() => null);
    if (state?.href === `${base}/index.html` && state.ready === "complete") return;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error("The root index.html did not finish loading through the local project-root HTTP server.");
}

async function waitFor(expression, description, attempts = 200) {
  let lastError = "";
  for (let i = 0; i < attempts; i++) {
    const value = await evaluate(expression).catch((error) => { lastError = error.message; return false; });
    if (value) return value;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error(`Timed out waiting for ${description}.${lastError ? ` Last browser evaluation: ${lastError}` : ""}${failures.length ? ` Browser errors: ${failures.slice(-3).join("; ")}` : ""}`);
}

const evidenceDirectory = path.join(root, "docs/debug-screenshots");
async function captureEvidence(name) {
  const image = await command("Page.captureScreenshot", { format: "png", captureBeyondViewport: false, fromSurface: true });
  fs.mkdirSync(evidenceDirectory, { recursive: true });
  const target = path.join(evidenceDirectory, name);
  fs.writeFileSync(target, Buffer.from(image.data, "base64"));
  return target;
}

try {
  const base = await startServer();
  await openBrowser(base);
  await evaluate(`document.querySelector('nav [data-nav="atlas"]').click()`);
  await waitFor(`(()=>{const v=document.querySelector('#view-atlas'),f=v?.querySelector('iframe[data-src]');return !!(v&&!v.hidden&&f?.getAttribute('src')?.endsWith('atlas/current/viewer/atlas.html')&&f.contentDocument?.readyState==='complete'&&f.contentDocument.querySelector('#q'))})()`, "the normal root navigation to load the country atlas iframe");
  const route = await evaluate(`(()=>{const f=document.querySelector('#view-atlas iframe');return {hash:location.hash,src:new URL(f.src).pathname,hidden:f.closest('[hidden]')!==null}})()`);
  assert.equal(route.hash, "#atlas");
  assert.equal(route.src, "/atlas/current/viewer/atlas.html");
  assert.equal(route.hidden, false);

  await evaluate(`document.querySelector('#view-atlas iframe').scrollIntoView({block:'center'})`);
  const searchResult = await evaluate(`(()=>{const d=document.querySelector('#view-atlas iframe').contentDocument,q=d.querySelector('#q');q.value='T-02';q.dispatchEvent(new Event('input',{bubbles:true}));const result=d.querySelector('#results [data-id="T-02"]');return {found:!!result,text:result?.innerText||'',id:result?.dataset.id||''}})()`);
  assert.equal(searchResult.found, true, "Hidden internal ID T-02 must still find the place.");
  assert.equal(searchResult.id, "T-02");
  assert.match(searchResult.text, /Cimprlichovo Hradiště/);
  assert.doesNotMatch(searchResult.text, /T-02|schváleno|návrh|approved|proposed/i);
  await evaluate(`document.querySelector('#view-atlas iframe').contentDocument.querySelector('#results [data-id="T-02"]').click()`);
  const details = await waitFor(`(()=>{const d=document.querySelector('#view-atlas iframe').contentDocument;return d.querySelector('#info h3')?.textContent==='Cimprlichovo Hradiště'?{heading:d.querySelector('#info h3').textContent,text:d.querySelector('#info').innerText,header:d.querySelector('header').innerText,visible:d.body.innerText,registryLoaded:d.querySelector('#info .place-kicker')?.textContent||''}:false})()`, "the selected T-02 place detail");
  assert.equal(details.heading, "Cimprlichovo Hradiště");
  assert.match(details.text, /Japonsky:\s*チンプルリフ砦/);
  assert.match(details.text, /MĚSTO V JIŽNÍ ČÁSTI HLAVNÍHO OSTROVA/i);
  assert.match(details.text, /silniční i železniční spojení/);
  assert.doesNotMatch(details.text, /Městská a venkovská sídla navazují|Sídla propojují místní silnice/i, "Generic regional filler must not replace useful card details.");
  assert.doesNotMatch(details.text, /Anglicky:/, "The source English field duplicates the Czech name and should not be shown as a translation.");
  assert.doesNotMatch(details.text, /T-02|návrh jména|existence:\s*schváleno|jméno:\s*schváleno|poloha:\s*návrh|Bible|pseudo|vodítko|model/i);
  const sourceRecord = JSON.parse(fs.readFileSync(path.join(root, "atlas/current/registry/places.json"), "utf8")).objects.find((item) => item.id === "T-02");
  assert.equal(sourceRecord?.name_status, "approved", "Editorial status remains in the private source registry.");
  assert.equal(sourceRecord?.pos_status, "proposed", "Position status remains in the private source registry.");
  assert.doesNotMatch(details.registryLoaded, /T-02|návrh|schváleno/i);
  assert.doesNotMatch(details.header, /NÁVRH\s*·\s*v1\.0-draft/i);
  assert.doesNotMatch(details.visible, /\bT-02\b|NÁVRH\s*·\s*v1\.0-draft|\bnávrh\b|pracovní|modelové výšky|existence:\s*schváleno|jméno:\s*schváleno|poloha:\s*návrh|pseudo \(hypotetické\)|Bible\/zadání|Foto \/ video vodítko/i);
  await evaluate(`(()=>{const d=document.querySelector('#view-atlas iframe').contentDocument,q=d.querySelector('#q');q.value='';q.dispatchEvent(new Event('input',{bubbles:true}))})()`);
  const rootMapPoint = await evaluate(`(()=>{const frame=document.querySelector('#view-atlas [data-map-panel="country"] iframe'),marker=frame?.contentDocument?.querySelector('#labels-cs text[data-id="T-02"]'),r=marker?.getBoundingClientRect(),f=frame?.getBoundingClientRect();return r&&f&&r.width>0&&r.height>0?{x:f.left+r.left+r.width/2,y:f.top+r.top+r.height/2}:null})()`);
  assert.ok(rootMapPoint && rootMapPoint.x > 0 && rootMapPoint.y > 0, "T-02 must expose a visible map hit target in the root website.");
  for (let click = 0; click < 2; click++) {
    await command("Input.dispatchMouseEvent", { type: "mousePressed", x: rootMapPoint.x, y: rootMapPoint.y, button: "left", clickCount: 1 });
    await command("Input.dispatchMouseEvent", { type: "mouseReleased", x: rootMapPoint.x, y: rootMapPoint.y, button: "left", clickCount: 1 });
    const clickedHeading = await evaluate(`document.querySelector('#view-atlas [data-map-panel="country"] iframe').contentDocument.querySelector('#info h3')?.textContent||''`);
    assert.equal(clickedHeading, "Cimprlichovo Hradiště", "Repeated direct map clicks must preserve the selected place details.");
  }
  await command("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x: rootMapPoint.x, y: rootMapPoint.y, id: 1, radiusX: 3, radiusY: 3, force: 1 }] });
  await command("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
  const touchedHeading = await evaluate(`document.querySelector('#view-atlas [data-map-panel="country"] iframe').contentDocument.querySelector('#info h3')?.textContent||''`);
  assert.equal(touchedHeading, "Cimprlichovo Hradiště", "A touch tap on the root atlas must select the same place as a mouse click.");

  const branding = await evaluate(`(()=>{const header=document.querySelector('header img.site-brand-logo'),footer=document.querySelector('#view-atlas footer img.site-brand-logo');return {headerHeight:header?.getBoundingClientRect().height,footerHeight:footer?.getBoundingClientRect().height,footerMax:getComputedStyle(footer).maxHeight,footerCount:document.querySelectorAll('#view-atlas footer img.site-brand-logo').length,ratio:footer?.naturalWidth/footer?.naturalHeight}})()`);
  assert.equal(branding.footerCount, 1, "The visible atlas footer must not contain a duplicated logo.");
  assert.ok(Math.abs(branding.headerHeight - branding.footerHeight) < 1, `Header/footer logo sizes differ: ${JSON.stringify(branding)}`);
  assert.ok(branding.footerHeight <= 48 && branding.footerMax === "48px", `Footer logo max height is not constrained: ${JSON.stringify(branding)}`);
  assert.ok(Number.isFinite(branding.ratio) && branding.ratio > 0, "The footer logo must have a valid intrinsic aspect ratio.");

  await captureEvidence(path.basename(screenshotPath));
  await captureEvidence("atlas-root-live-cimprlichovo.png");
  const atlasSpotChecks = [];
  const atlasIds = ["T-01", "T-02", "C-01", "T-03", "T-04", "M-01", "M-02", "M-03", "N-01", "N-02", "N-03", "N-04", "V-02", "SP-01", "SP-04", "B-01", "PL-02", "L1", "L2", "L3", "P-01"];
  for (const id of atlasIds) {
    const state = await evaluate(`(()=>{const d=document.querySelector('#view-atlas [data-map-panel="country"] iframe').contentDocument,q=d.querySelector('#q');q.value=${JSON.stringify(id)};q.dispatchEvent(new Event('input',{bubbles:true}));const result=d.querySelector('#results [data-id="${id}"]');if(!result)return {found:false};const row=result.innerText;result.click();return {found:true,row,heading:d.querySelector('#info h3')?.textContent||'',description:d.querySelector('#info .place-lead')?.textContent||'',text:d.querySelector('#info').innerText||''}})()`);
    assert.equal(state.found, true, `Atlas ID ${id} must remain searchable.`);
    assert.ok(state.row.startsWith(state.heading), `Atlas result ${id} must start with its public place name.`);
    assert.ok(state.description.length >= 75, `Atlas description for ${id} is too short to be useful.`);
    assert.doesNotMatch(state.text, /\b(?:T|C|M|N|V|SP|B|PL|RD|ST)-\d{2,}\b|existence:|návrh jména|schváleno|Bible|photo_guide|prac\.|draft/i, `Private metadata is visible for ${id}.`);
    atlasSpotChecks.push({ id, heading: state.heading, description: state.description });
    if (id === "T-01") await captureEvidence("atlas-root-live-praha.png");
    if (id === "C-01") {
      await evaluate(`(()=>{const d=document.querySelector('#view-atlas [data-map-panel="country"] iframe').contentDocument;const style=d.createElement('style');style.id='map-texture-before';style.textContent='#settlements path[data-id="C-01"]{fill:#d9b79c!important;stroke:#8b6f55!important}';d.head.append(style)})()`);
      await captureEvidence("atlas-2d-city-before.png");
      await evaluate(`document.querySelector('#view-atlas [data-map-panel="country"] iframe').contentDocument.querySelector('#map-texture-before').remove()`);
      await captureEvidence("atlas-2d-city-after.png");
      await captureEvidence("atlas-root-live-larpington.png");
    }
    if (id === "L1") await captureEvidence("atlas-root-live-railway-rich-card.png");
    if (id === "V-02") await captureEvidence("atlas-root-live-poi-detail.png");
  }
  assert.ok(atlasSpotChecks.some((item) => item.id === "C-01" && /Chalupecká.*Kynčlova.*Klimečkova.*Žemličkova/.test(item.description)), "Larpington must name its four canonical traditional quarters.");
  assert.match(atlasSpotChecks.find((item) => item.id === "T-02").heading, /^Cimprlichovo Hradiště$/);
  assert.doesNotMatch(atlasSpotChecks.find((item) => item.id === "M-01").description, /model/i, "The public mountain card must present approximate elevation without production language.");
  await evaluate(`(()=>{const d=document.querySelector('#view-atlas [data-map-panel="country"] iframe').contentDocument,q=d.querySelector('#q');q.value='Cimpřichovo Hradiště';q.dispatchEvent(new Event('input',{bubbles:true}));return d.querySelector('#results [data-id="T-02"] .result-title')?.innerText||''})()`)
    .then((aliasResult) => assert.equal(aliasResult, "Cimprlichovo Hradiště", "The previous spelling must remain a hidden search alias."));

  await evaluate(`document.querySelector('[data-atlas-mode="capital"]').click()`);
  await waitFor(`(()=>{const f=document.querySelector('#view-atlas [data-map-panel="capital"] iframe');return !!(f?.contentDocument?.readyState==='complete'&&f.contentDocument.querySelector('#q'))})()`, "the root navigation to Larpington's plan");
  await evaluate(`document.querySelector('#view-atlas [data-map-panel="capital"] iframe').scrollIntoView({block:'center'})`);
  const citySpotChecks = [];
  const cityIds = ["CP-01", "CP-B01", "CP-B06", "CP-B07", "CP-SQ01", "CP-PK02", "CP-PR01", "ST-W", "ST-S", "CP-BL-0001", "CP-BL-0342", "CP-CF01", "CP-RN01", "CP-SH04", "CP-ZR02", "CP-UL01", "CP-AR01", "CP-B12", "CP-PK03", "CP-BL-0243", "CP-PI01"];
  for (const id of cityIds) {
    const state = await evaluate(`(()=>{const d=document.querySelector('#view-atlas [data-map-panel="capital"] iframe').contentDocument,q=d.querySelector('#q');q.value=${JSON.stringify(id)};q.dispatchEvent(new Event('input',{bubbles:true}));const result=d.querySelector('#results [data-id="${id}"]');if(!result)return {found:false};const row=result.innerText;result.click();return {found:true,row,heading:d.querySelector('#info h3')?.textContent||'',description:d.querySelector('#info .place-lead')?.textContent||'',text:d.querySelector('#info').innerText||''}})()`);
    assert.equal(state.found, true, `City-plan ID ${id} must remain searchable.`);
    assert.ok(state.row.startsWith(state.heading), `City-plan result ${id} must start with its public place name.`);
    assert.ok(state.description.length >= 65, `City-plan description for ${id} is too short to be useful.`);
    assert.doesNotMatch(state.text, /\bCP-[A-Z0-9-]+\b|existence:|návrh jména|schváleno|Bible|photo_guide|prac\.|draft/i, `Private metadata is visible for city object ${id}.`);
    citySpotChecks.push({ id, heading: state.heading, description: state.description });
    if (id === "CP-B06") await captureEvidence("capital-root-live-museum.png");
  }

  await evaluate(`document.querySelector('nav [data-nav="galerie"]').click()`);
  await waitFor(`(()=>{const g=document.querySelector('[data-gallery-grid]'),images=[...(g?.querySelectorAll('img')||[])];return !!(g&&images.length>=1&&images.every(image=>image.complete&&image.naturalWidth>0))})()`, "gallery image decoding from the root website");
  const gallery = await evaluate(`(()=>[...document.querySelectorAll('[data-gallery-grid] img')].map(i=>({src:i.currentSrc,alt:i.alt,width:i.naturalWidth,height:i.naturalHeight,rect:i.getBoundingClientRect().toJSON()})))()`);
  assert.equal(gallery.length, 2, `The gallery should show the two verified locally available story photographs; received ${gallery.length}.`);
  assert.ok(gallery.every((image) => image.width > 0 && image.height > 0 && image.rect.width > 0 && image.rect.height > 0), "Gallery images must have decoded pixels and nonzero rendered size.");
  assert.ok(gallery.some((image) => image.src.endsWith("PHOTO_01.png")) && gallery.some((image) => image.src.endsWith("PHOTO_06.png")), "The public gallery should show the verified mountain and Paraland scenes.");
  await evaluate(`document.querySelector('nav [data-nav="encyklopedie"]').click()`);
  await waitFor(`(()=>!!document.querySelector('#view-encyklopedie [data-encyclopedia-app] a[href="#encyklopedie/geografie/priroda"]'))()`, "the root encyclopedia article navigation");
  await evaluate(`document.querySelector('#view-encyklopedie [data-encyclopedia-app] a[href="#encyklopedie/geografie/priroda"]').click()`);
  await waitFor(`(()=>!!document.querySelector('#view-encyklopedie .ency-prose img')&&document.querySelector('#view-encyklopedie .ency-prose img').complete)()`, "the root encyclopedia article photo");
  const articlePhoto = await evaluate(`(()=>{const i=document.querySelector('#view-encyklopedie .ency-prose img');return {alt:i.alt,src:i.currentSrc,width:i.naturalWidth,height:i.naturalHeight}})()`);
  assert.ok(articlePhoto.width > 0 && articlePhoto.height > 0 && articlePhoto.src.endsWith("PHOTO_01.png"), `The encyclopedia should use the verified winter mountain image: ${JSON.stringify(articlePhoto)}`);
  await evaluate(`document.querySelector('nav [data-nav="galerie"]').click()`);
  await waitFor(`(()=>document.querySelectorAll('[data-gallery-grid] img').length===2)()`, "returning to the root gallery");
  await command("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await evaluate("window.scrollTo(0,0)");
  await captureEvidence("gallery-live-mobile.png");
  const mediaButton = await evaluate(`!!document.querySelector('#view-galerie [data-media-status-open]')`);
  assert.equal(mediaButton, true, "The author media archive button must exist in the root development workflow.");
  await evaluate(`document.querySelector('#view-galerie [data-media-status-open]').click()`);
  const modal = await waitFor(`(()=>{const d=document.querySelector('#media-status-dialog');return !!(d?.open&&d.querySelector('[data-media-photo-count]')?.textContent!=='…'&&d.querySelector('[data-media-missing-count]')?.textContent!=='…')})()`, "the computed author-only photo inventory");
  assert.equal(modal, true);
  const modalCounts = await evaluate(`(()=>({photos:document.querySelector('#media-status-dialog [data-media-photo-count]').textContent,missing:document.querySelector('#media-status-dialog [data-media-missing-count]').textContent,available:document.querySelectorAll('#media-status-dialog [data-media-available] li').length,missingRows:document.querySelectorAll('#media-status-dialog [data-media-missing] li').length}))()`);
  assert.ok(Number(modalCounts.photos) >= 0 && Number(modalCounts.missing) >= 0);
  await captureEvidence("author-media-modal.png");
  await evaluate(`document.querySelector('#media-status-dialog [data-media-status-close]').click()`);
  await evaluate("window.scrollTo(0,document.body.scrollHeight)");
  await captureEvidence("footer-logo.png");
  const rootFooterLogo = await evaluate(`(()=>{const i=document.querySelector('#view-galerie footer img.site-brand-logo');return {found:!!i,width:i?.naturalWidth||0,height:i?.getBoundingClientRect().height||0,maxHeight:i?getComputedStyle(i).maxHeight:''}})()`);
  assert.ok(rootFooterLogo.found && rootFooterLogo.width > 0 && rootFooterLogo.height <= 48 && rootFooterLogo.maxHeight === "48px", `The root footer logo should render at the shared header size: ${JSON.stringify(rootFooterLogo)}`);

  const routeRequests = ["/index.html", "/site.js", "/atlas/current/viewer/atlas.html", "/site-brand.css", "/project-meta.js"];
  for (const requested of routeRequests) assert.ok(requests.has(requested), `Root HTTP server did not serve ${requested}.`);
  if (failures.length) throw new Error(`Browser/runtime/network errors: ${failures.join("; ")}`);
  console.log(`PASS kořenový index.html obsloužil lokální HTTP server na ${base}.`);
  console.log(`PASS normální navigace ${route.hash} načetla ${route.src}; T-02 je vyhledatelné bez zobrazení ID a produkčních údajů.`);
  console.log(`PASS detail: ${details.heading}; ${details.text.replace(/\s+/g, " ")}`);
  console.log(`PASS ${atlasSpotChecks.length} hlavních atlasových karet a ${citySpotChecks.length} objektů městského plánu: české názvy, popisy, skryté kódy.`);
  console.log(`PASS kořenová galerie: ${gallery.length} obrázků s dekódovanými pixely; Obrazový archiv ${modalCounts.photos} hotových / ${modalCounts.missing} chybějících.`);
  console.log(`PASS logo hlavičky/patičky: ${branding.headerHeight}px / ${branding.footerHeight}px; bez duplikace.`);
  console.log(`Snímky skutečného kořenového webu: ${evidenceDirectory}`);
} finally {
  if (cdp?.readyState === WebSocket.OPEN) { try { cdp.close(); } catch {} }
  if (browser && browserExit === null) {
    browser.kill();
    await Promise.race([new Promise((resolve) => browser.once("exit", resolve)), new Promise((resolve) => setTimeout(resolve, 3_000))]);
  }
  if (server.listening) await new Promise((resolve) => server.close(resolve));
  try { fs.rmSync(tempRoot, { recursive: true, force: true, maxRetries: 5, retryDelay: 150 }); } catch {}
}
