import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const password = process.env.LARPIDIA_EXPLORER_PASSWORD;
if (!password) throw new Error("Pro kontrolu vstupu nastavte LARPIDIA_EXPLORER_PASSWORD na aktuální heslo.");
const outDir = process.env.LARPIDIA_SCREENSHOT_DIR
  ? path.resolve(process.env.LARPIDIA_SCREENSHOT_DIR) : path.join(root, "docs/debug-screenshots");
fs.mkdirSync(outDir, { recursive: true });
const browserPath = [
  path.join(process.env["ProgramFiles(x86)"] || "C:/Program Files (x86)", "Microsoft/Edge/Application/msedge.exe"),
  path.join(process.env.ProgramFiles || "C:/Program Files", "Microsoft/Edge/Application/msedge.exe"),
].find((candidate) => fs.existsSync(candidate));
if (!browserPath) throw new Error("Microsoft Edge nebyl nalezen; skutečné snímky prohlížeče nelze pořídit.");
const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "larpidia-explorer-"));
const servers = ["serve_root.mjs", "serve_static.mjs"].map((script) => {
  const child = spawn(process.execPath, [path.join(root, "scripts", script), "0"], { cwd: root, stdio: ["ignore", "pipe", "pipe"] });
  child.stderr.setEncoding("utf8"); child.errorText = ""; child.stderr.on("data", (chunk) => { child.errorText += chunk; });
  return child;
});
const startServer = (child) => new Promise((resolve, reject) => {
  let output = "";
  const timer = setTimeout(() => reject(new Error(`HTTP server did not start: ${child.errorText}`)), 10000);
  child.stdout.setEncoding("utf8").on("data", (chunk) => {
    output += chunk;
    const match = output.match(/http:\/\/127\.0\.0\.1:(\d+)\//);
    if (match) { clearTimeout(timer); resolve(`http://127.0.0.1:${match[1]}`); }
  });
  child.once("error", (error) => { clearTimeout(timer); reject(error); });
});
const [rootUrl, publicUrl] = await Promise.all(servers.map(startServer));
const profile = path.join(tempRoot, "edge-profile");
const browser = spawn(browserPath, [
  "--headless=new", "--no-sandbox", "--disable-renderer-code-integrity", "--disable-features=RendererCodeIntegrity",
  "--disable-gpu", "--disable-extensions", "--disable-background-networking", "--no-first-run", "--no-default-browser-check",
  "--remote-debugging-port=0", `--user-data-dir=${profile}`, "about:blank",
], { stdio: ["ignore", "ignore", "pipe"] });
let browserError = "";
browser.stderr.setEncoding("utf8").on("data", (chunk) => { browserError += chunk; });
let cdp, sessionId, id = 0;
const pending = new Map();
const requestMethods = [];
const requestUrls = [];
const call = (method, params = {}) => new Promise((resolve, reject) => {
  const requestId = ++id;
  const timer = setTimeout(() => { pending.delete(requestId); reject(new Error(`CDP ${method} timed out`)); }, 15000);
  pending.set(requestId, { resolve: (value) => { clearTimeout(timer); resolve(value); }, reject: (error) => { clearTimeout(timer); reject(error); } });
  cdp.send(JSON.stringify({ id: requestId, method, params, ...(sessionId ? { sessionId } : {}) }));
});
const evaluate = async (expression) => {
  const result = await call("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true, userGesture: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  return result.result?.value;
};
const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const screenshot = async (name) => {
  const image = await call("Page.captureScreenshot", { format: "png", captureBeyondViewport: false, fromSurface: true });
  fs.writeFileSync(path.join(outDir, `${name}.png`), Buffer.from(image.data, "base64"));
};
const waitFor = async (expression, description) => {
  for (let attempt = 0; attempt < 120; attempt++) {
    if (await evaluate(expression).catch(() => false)) return;
    await pause(100);
  }
  throw new Error(`Časový limit při čekání na ${description}.`);
};
const navigate = async (url) => {
  await call("Page.navigate", { url });
  await waitFor("document.readyState === 'complete'", "načtení stránky");
};
const setViewport = (width, height, mobile) => call("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile });
const clickPoint = async (x, y) => {
  await call("Input.dispatchMouseEvent", { type: "mouseMoved", x, y });
  await call("Input.dispatchMouseEvent", { type: "mousePressed", x, y, button: "left", clickCount: 1 });
  await call("Input.dispatchMouseEvent", { type: "mouseReleased", x, y, button: "left", clickCount: 1 });
};
const dragMap = async (x, y, dx, dy) => {
  await call("Input.dispatchMouseEvent", { type: "mouseMoved", x, y });
  await call("Input.dispatchMouseEvent", { type: "mousePressed", x, y, button: "left", buttons: 1, clickCount: 1 });
  await call("Input.dispatchMouseEvent", { type: "mouseMoved", x: x + dx, y: y + dy, button: "left", buttons: 1 });
  await call("Input.dispatchMouseEvent", { type: "mouseReleased", x: x + dx, y: y + dy, button: "left", buttons: 0, clickCount: 1 });
};

const checkLocked = async (label, requestStart = requestUrls.length) => {
  await waitFor("!document.querySelector('#access-submit').disabled", `vstupní brány (${label})`);
  const state = await evaluate("({locked:!document.querySelector('#access-panel').hidden,contentHidden:document.querySelector('#explorer-content').hidden,resetHidden:document.querySelector('#reset-game').hidden,map:!!document.querySelector('#map-viewport svg')})");
  if (!state.locked || !state.contentHidden || !state.resetHidden || state.map) throw new Error(`Hra není před zadáním hesla uzamčená (${label}).`);
  if (requestUrls.slice(requestStart).some((url) => /\/(?:rounds\.json|registry\/places\.public\.json|viewer\/atlas\.html)(?:[?#]|$)/.test(url))) {
    throw new Error(`Herní konfigurace nebo mapa se načetla před odemknutím (${label}).`);
  }
};
const enterPassword = async (value) => {
  await evaluate(`(()=>{const p=document.querySelector('#access-password');p.value=${JSON.stringify(value)};p.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#access-form').requestSubmit()})()`);
};
const unlockExplorer = async (label, storageBlocked = false, typed = password) => {
  await enterPassword("incorrect-classroom-password");
  await waitFor("!document.querySelector('#access-status').hidden", "odmítnutí špatného hesla");
  if (!await evaluate("document.querySelector('#explorer-content').hidden && document.querySelector('#access-password').getAttribute('aria-invalid') === 'true'")) throw new Error(`Špatné heslo odemklo hru (${label}).`);
  await evaluate("document.querySelector('#access-toggle').click()");
  if (!await evaluate("document.querySelector('#access-password').type === 'text' && document.querySelector('#access-toggle').getAttribute('aria-pressed') === 'true' && getComputedStyle(document.querySelector('#access-password')).textTransform === 'uppercase'")) throw new Error("Zobrazení hesla nefunguje nebo heslo není zobrazené velkými písmeny.");
  await evaluate("document.querySelector('#access-toggle').click()");
  await enterPassword(typed);
  await waitFor("document.querySelector('#access-panel').hidden && !document.querySelector('#start-button').disabled", `odemknutí hry (${label})`);
  if (!await evaluate("document.querySelector('#access-password').value === '' && !document.querySelector('#explorer-content').hidden && !!document.querySelector('#map-viewport svg')")) throw new Error(`Odemknutí nedokončilo načtení hry (${label}).`);
  if (await evaluate(`Object.values(sessionStorage).some(value=>${JSON.stringify([password.toUpperCase(), password.toLowerCase()])}.some(secret=>value.toUpperCase().includes(secret.toUpperCase())))`)) throw new Error("Heslo se uložilo v otevřeném tvaru.");
  if (storageBlocked && !await evaluate("!document.querySelector('#access-storage-warning').hidden")) throw new Error("Chybí upozornění na zablokované uložení přístupu.");
  console.log(`Vstup (${label}): chybné heslo odmítnuto, ${typed === password ? "správné" : "správné v jiné velikosti písmen s mezerami"} odemklo hru; heslo se neukládá v otevřeném tvaru.`);
};

try {
  const activePortFile = path.join(profile, "DevToolsActivePort");
  for (let i = 0; i < 300 && !fs.existsSync(activePortFile); i++) await pause(50);
  if (!fs.existsSync(activePortFile)) throw new Error(`Edge neotevřel DevTools: ${browserError}`);
  const [port, endpoint] = fs.readFileSync(activePortFile, "utf8").trim().split(/\r?\n/);
  cdp = new WebSocket(`ws://127.0.0.1:${port}${endpoint}`);
  await new Promise((resolve, reject) => { cdp.addEventListener("open", resolve, { once: true }); cdp.addEventListener("error", reject, { once: true }); });
  cdp.addEventListener("message", async (event) => {
    const message = JSON.parse(typeof event.data === "string" ? event.data : await event.data.text());
    if (message.method === "Network.requestWillBeSent") {
      requestMethods.push(message.params.request.method);
      requestUrls.push(message.params.request.url);
    }
    if (!message.id) return;
    const request = pending.get(message.id);
    if (!request) return;
    pending.delete(message.id);
    if (message.error) request.reject(new Error(message.error.message)); else request.resolve(message.result || {});
  });
  const browserTarget = await call("Target.createTarget", { url: "about:blank" });
  sessionId = (await call("Target.attachToTarget", { targetId: browserTarget.targetId, flatten: true })).sessionId;
  await call("Page.enable"); await call("Runtime.enable"); await call("Network.enable");
  await setViewport(1440, 1000, false);
  const rootRequestStart = requestUrls.length;
  await navigate(`${rootUrl}/explorer/index.html`);
  await checkLocked("root", rootRequestStart);
  await screenshot("explorer-access-desktop");
  await setViewport(390, 844, true); await pause(200);
  if (await evaluate("document.documentElement.scrollWidth > innerWidth")) throw new Error("Vstupní brána na mobilu vodorovně přetéká.");
  await screenshot("explorer-access-mobile");
  await unlockExplorer("root");
  await waitFor("document.querySelector('#map-viewport svg')", "kanonické mapy root webu");
  const intro = await evaluate("({title:document.querySelector('#intro-title').textContent,places:document.querySelectorAll('#map-viewport svg [data-id]').length,mode:document.querySelector('#mode-label').textContent})");
  if (!intro.title.includes("Larpidia Explorer") || intro.places < 159 || !intro.mode.includes("Zkušební")) throw new Error(`Úvodní obrazovka/mapa se nenačetla správně: ${JSON.stringify(intro)}`);
  await setViewport(390, 844, true); await pause(250);
  const introState = await evaluate("({visible:!document.querySelector('#intro-panel').hidden,gameHidden:document.querySelector('#game-panel').hidden})");
  if (!introState.visible || !introState.gameHidden) throw new Error(`Vstupní obrazovka nemá správné stavy: ${JSON.stringify(introState)}`);
  await screenshot("explorer-mobile-intro");
  await evaluate("document.querySelector('#team-name').value='Kontrolní tým';document.querySelector('#start-button').click()");
  await waitFor("!document.querySelector('#game-panel').hidden", "prvního kola");
  await setViewport(1440, 1000, false); await pause(250);
  await screenshot("explorer-desktop-round");

  await setViewport(390, 844, true); await pause(300);
  const mapRect = await evaluate("(()=>{const r=document.querySelector('#map-viewport').getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2}})()");
  await dragMap(mapRect.x, mapRect.y, 34, 18);
  if (await evaluate("!document.querySelector('#confirm-button').disabled")) throw new Error("Tažení mapy omylem umístilo tip.");
  const target = await evaluate("fetch('../atlas/current/registry/places.public.json').then(r=>r.json()).then(r=>{const p=r.objects.find(o=>o.id==='SP-01'),t=LarpidiaExplorerCoordinates.toSvg(p.x_km,p.y_km);const q=new DOMPoint(t.x+100,t.y).matrixTransform(document.querySelector('#map-viewport svg').getScreenCTM());return{x:q.x,y:q.y}})");
  await clickPoint(target.x, target.y);
  await waitFor("!document.querySelector('#confirm-button').disabled", "umístění tipu");
  const before = await evaluate("({answer:document.querySelector('#result-place').textContent,hidden:document.querySelector('#round-result').hidden,guess:document.querySelector('#map-viewport .guess-marker').style.display,cursor:document.querySelector('#map-viewport .keyboard-marker').style.display})");
  const unrevealedControls = await evaluate("({actionsHidden:document.querySelector('#result-actions').hidden,legendHidden:document.querySelector('#map-legend').hidden})");
  if (!before.hidden || before.guess === "none" || before.answer !== "—" || before.cursor !== "none" || !unrevealedControls.actionsHidden || !unrevealedControls.legendHidden) throw new Error(`Před potvrzením se zobrazil výsledek, zůstal kurzor po klepnutí, nebo chybí tip: ${JSON.stringify({before,unrevealedControls})}`);
  const markerSizeAtOverview = await evaluate("document.querySelector('#map-viewport .guess-marker circle').getBoundingClientRect().width");
  if (markerSizeAtOverview < 26 || markerSizeAtOverview > 34) throw new Error(`Tip je při celém souostroví příliš malý: ${markerSizeAtOverview}px.`);
  await screenshot("explorer-mobile-guess");
  const originalGuess = await evaluate("JSON.parse(localStorage.getItem('larpidia-explorer:v1')).guess");
  await evaluate("document.querySelector('#zoom-in').click()");
  const markerSizeZoomed = await evaluate("document.querySelector('#map-viewport .guess-marker circle').getBoundingClientRect().width");
  if (Math.abs(markerSizeAtOverview - markerSizeZoomed) > 0.75) throw new Error(`Velikost tipu se změnila se zoomem: ${markerSizeAtOverview}px → ${markerSizeZoomed}px.`);
  const samePoint = await evaluate(`(()=>{const p=${JSON.stringify(originalGuess)},q=new DOMPoint(p.x,p.y).matrixTransform(document.querySelector('#map-viewport svg').getScreenCTM());return{x:q.x,y:q.y}})()`);
  await clickPoint(samePoint.x, samePoint.y);
  const repositionedGuess = await evaluate("JSON.parse(localStorage.getItem('larpidia-explorer:v1')).guess");
  if (Math.abs(originalGuess.x - repositionedGuess.x) > .01 || Math.abs(originalGuess.y - repositionedGuess.y) > .01) throw new Error(`Zoom změnil uloženou polohu tipu: ${JSON.stringify({originalGuess,repositionedGuess})}`);
  await screenshot("explorer-mobile-zoom-guess");
  await call("Page.reload"); await waitFor("!document.querySelector('#confirm-button').disabled", "obnovy uloženého tipu");
  if (!await evaluate("document.querySelector('#access-panel').hidden")) throw new Error("Obnovení karty zapomnělo odemknutí.");
  await evaluate("document.querySelector('#confirm-button').click()");
  await waitFor("!document.querySelector('#round-result').hidden", "odhalení výsledku");
  const result = await evaluate("({place:document.querySelector('#result-place').textContent,href:document.querySelector('#result-place').getAttribute('href'),points:document.querySelector('#result-points').textContent,targetVisible:document.querySelector('#map-viewport .target-marker').style.display,guessVisible:document.querySelector('#map-viewport .guess-marker').style.display,guessColor:getComputedStyle(document.querySelectorAll('#map-viewport .guess-marker circle')[1]).fill,targetColor:getComputedStyle(document.querySelector('#map-viewport .target-marker path')).fill})");
  if (result.place !== "Pramen řeky Larp" || !result.href.includes("place=SP-01") || !result.points.includes("bodů") || result.targetVisible === "none" || result.guessVisible === "none" || result.guessColor === result.targetColor) throw new Error(`Výsledek, atlasový odkaz nebo rozlišení značek není správné: ${JSON.stringify(result)}`);
  await screenshot("explorer-mobile-result");

  for (let round = 1; round < 4; round++) {
    await evaluate("document.querySelector('#next-button').click()");
    await waitFor("!document.querySelector('#game-panel').hidden && document.querySelector('#round-result').hidden", `kola ${round + 1}`);
    const point = await evaluate(`fetch('../atlas/current/registry/places.public.json').then(r=>r.json()).then(r=>fetch('rounds.json').then(c=>c.json()).then(c=>{const p=r.objects.find(o=>o.id===c.rounds[${round}].targetPlaceId),t=LarpidiaExplorerCoordinates.toSvg(p.x_km,p.y_km);const q=new DOMPoint(t.x+100,t.y).matrixTransform(document.querySelector('#map-viewport svg').getScreenCTM());return{x:q.x,y:q.y}}))`);
    await clickPoint(point.x, point.y);
    await pause(120);
    const interaction = await evaluate(`(()=>{const e=document.querySelector('#map-viewport'),s=document.querySelector('#map-viewport svg'),r=e.getBoundingClientRect(),p=new DOMPoint(${point.x},${point.y}).matrixTransform(s.getScreenCTM().inverse());return{point:${JSON.stringify(point)},rect:{x:r.x,y:r.y,w:r.width,h:r.height},mapped:{x:p.x,y:p.y},status:document.querySelector('#pin-status').textContent,disabled:document.querySelector('#confirm-button').disabled}})()`);
    if (interaction.disabled) throw new Error(`Tip kola ${round+1} nešel umístit: ${JSON.stringify(interaction)}`);
    await waitFor("!document.querySelector('#confirm-button').disabled", "tipu dalšího kola");
    await evaluate("document.querySelector('#confirm-button').click()");
    await waitFor("!document.querySelector('#round-result').hidden", "výsledku dalšího kola");
  }
  await evaluate("document.querySelector('#next-button').click()");
  await waitFor("!document.querySelector('#summary-panel').hidden", "souhrnu čtyř kol");
  const summary = await evaluate("({total:document.querySelector('#final-score').textContent,rows:document.querySelectorAll('.break-row').length,sceneHidden:document.querySelector('#score-scene').hidden})");
  if (summary.rows !== 4 || Number(summary.total.replace(/\\s/g,'')) <= 0 || !summary.sceneHidden) throw new Error(`Závěrečný souhrn nebo práh nízkého skóre je neplatný: ${JSON.stringify(summary)}`);
  await screenshot("explorer-mobile-summary");
  if (!await evaluate("JSON.parse(localStorage.getItem('larpidia-explorer:v1')).rounds.every(round=>Math.abs(round.errorMeters-100)<.01)")) throw new Error("Odhady 100 metrů od cíle nemají očekávanou vzdálenost.");
  console.log(`Root web: mapa ${intro.places} prvků, tip se po obnovení zachoval, odpověď před potvrzením skrytá; ${result.place} → ${result.points}; souhrn ${summary.total}/20 000.`);

  const forceZeroScore = "(()=>{const key='larpidia-explorer:v1',s=JSON.parse(localStorage.getItem(key));s.currentRound=4;s.rounds=[0,1,2,3].map(i=>({points:0,skipped:true,targetConfigId:'test-'+i,target:null,targetPlaceId:null,errorMeters:null}));localStorage.setItem(key,JSON.stringify(s))})()";
  await evaluate(forceZeroScore); await call("Page.reload");
  await waitFor("!document.querySelector('#summary-panel').hidden && !document.querySelector('#score-scene').hidden", "nízkobodové scény");
  await waitFor("document.querySelector('#score-scene').classList.contains('revealed')", "pixelové lišky po černé obrazovce");
  const scareState = await evaluate("({title:document.querySelector('#score-scene-title').textContent,fox:!document.querySelector('#score-fox').hidden,flower:!document.querySelector('#score-flower').hidden,black:getComputedStyle(document.querySelector('#score-scene')).backgroundColor,score:document.querySelector('#final-score').textContent})");
  if (!scareState.title.includes("You didn't even try") || !scareState.fox || scareState.flower || scareState.black !== "rgb(0, 0, 0)" || Number(scareState.score.replace(/\\s/g,'')) !== 0) throw new Error(`Nízkobodová scéna se nezobrazila správně: ${JSON.stringify(scareState)}`);
  await screenshot("explorer-low-score-fox");
  await evaluate("document.querySelector('#score-did').click()");
  const flowerState = await evaluate("({title:document.querySelector('#score-scene-title').textContent,flower:!document.querySelector('#score-flower').hidden,fox:!document.querySelector('#score-fox').hidden,returnHidden:document.querySelector('#score-return').hidden})");
  if (!flowerState.title.includes("maybe it wasn't your lucky day") || !flowerState.flower || flowerState.fox || flowerState.returnHidden) throw new Error(`Volba „I did“ nezobrazila slunečnici: ${JSON.stringify(flowerState)}`);
  await screenshot("explorer-low-score-flower");
  await evaluate("document.querySelector('#score-return').click()");
  if (await evaluate("document.querySelector('#score-scene').hidden && document.querySelector('#final-score').textContent.includes('0')") !== true) throw new Error("Návrat ze slunečnice nezachoval souhrn a skóre.");
  await evaluate(forceZeroScore); await call("Page.reload");
  await waitFor("!document.querySelector('#score-scene').hidden && document.querySelector('#score-scene').classList.contains('revealed')", "druhé nízkobodové scény");
  await evaluate("document.querySelector('#score-no').click()");
  await waitFor("!document.querySelector('#score-return').hidden", "bezpečného návratu z černé obrazovky");
  const noState = await evaluate("({black:getComputedStyle(document.querySelector('#score-scene')).backgroundColor,returnVisible:!document.querySelector('#score-return').hidden,score:document.querySelector('#final-score').textContent})");
  if (noState.black !== "rgb(0, 0, 0)" || !noState.returnVisible || Number(noState.score.replace(/\\s/g,'')) !== 0) throw new Error(`Černá obrazovka nebo bezpečný návrat nefunguje: ${JSON.stringify(noState)}`);
  await screenshot("explorer-low-score-no");
  await evaluate("document.querySelector('#score-return').click()");
  console.log("Nízké skóre: černá obrazovka → liška → obě volby; slunečnice a bezpečný návrat zachovaly skóre 0.");

  const gameSessionId = sessionId;
  const freshTab = await call("Target.createTarget", { url: "about:blank" });
  sessionId = (await call("Target.attachToTarget", { targetId: freshTab.targetId, flatten: true })).sessionId;
  try {
    await call("Page.enable"); await call("Runtime.enable"); await call("Network.enable");
    const freshRequestStart = requestUrls.length;
    await navigate(`${rootUrl}/explorer/index.html`);
    await checkLocked("nová karta s uloženým postupem", freshRequestStart);
    const blockedStorage = await call("Page.addScriptToEvaluateOnNewDocument", { source: `
      for (const method of ['getItem','setItem']) {
        const original=Storage.prototype[method];
        Storage.prototype[method]=function(...args){
          if(this===sessionStorage) throw new DOMException('Test: session storage blocked','SecurityError');
          return original.apply(this,args);
        };
      }
    ` });
    await navigate(`${publicUrl}/explorer/index.html`);
    await checkLocked("zablokované sessionStorage");
    await unlockExplorer("zablokované sessionStorage", true);
    await call("Page.reload");
    await checkLocked("obnovení bez sessionStorage");
    await call("Page.removeScriptToEvaluateOnNewDocument", { identifier: blockedStorage.identifier });
    const noCrypto = await call("Page.addScriptToEvaluateOnNewDocument", { source: "Object.defineProperty(globalThis,'crypto',{value:{}})" });
    await call("Page.reload");
    await checkLocked("nedostupné Web Crypto");
    await enterPassword(password);
    await waitFor("!document.querySelector('#access-status').hidden", "chyby nedostupného ověření");
    if (!await evaluate("document.querySelector('#explorer-content').hidden && document.querySelector('#access-status').textContent.includes('HTTPS')")) throw new Error("Nedostupné Web Crypto neudrželo hru zamčenou.");
    await call("Page.removeScriptToEvaluateOnNewDocument", { identifier: noCrypto.identifier });
    console.log("Nová karta vyžaduje heslo i s uloženou hrou; zablokované sessionStorage i nedostupné Web Crypto mají výslovnou hlášku.");
  } finally {
    sessionId = gameSessionId;
    await call("Target.closeTarget", { targetId: freshTab.targetId });
  }

  await setViewport(1280, 900, false);
  const publicRequestStart = requestUrls.length;
  await navigate(`${publicUrl}/explorer/index.html`);
  await checkLocked("public", publicRequestStart);
  await unlockExplorer("public", false, `  ${password.toLowerCase()} `);
  await waitFor("document.querySelector('#map-viewport svg')", "mapy veřejného exportu");
  const exported = await evaluate("({link:document.querySelector('.brand').getAttribute('href'),map:!!document.querySelector('#map-viewport svg'),count:document.querySelectorAll('#map-viewport svg [data-id]').length})");
  if (!exported.map || exported.count < 159 || exported.link !== '../index.html') throw new Error(`Veřejný export nefunguje: ${JSON.stringify(exported)}`);
  console.log(`Public export: funkční Explorer a stejná mapa (${exported.count} míst).`);
  await navigate(`${rootUrl}/atlas/current/viewer/atlas.html?place=T-01`);
  await waitFor("document.querySelector('#info h3')?.textContent.includes('Praha') && document.querySelector('#map svg [data-id=\\\"T-01\\\"].hl')", "přímého výběru místa v atlasu");
  const selectedDesktop = await evaluate("({name:document.querySelector('#info h3').textContent,highlighted:document.querySelectorAll('#map svg [data-id=\"T-01\"].hl').length,map:document.querySelector('#map').getBoundingClientRect().width})");
  if (!selectedDesktop.name.includes("Praha") || !selectedDesktop.highlighted || selectedDesktop.map < 500) throw new Error(`Odkaz na vybrané místo v atlasu selhal: ${JSON.stringify(selectedDesktop)}`);
  await screenshot("explorer-atlas-desktop-selected");
  await setViewport(390, 844, true); await pause(250);
  const selectedMobile = await evaluate("(()=>{const map=document.querySelector('#map').getBoundingClientRect(),info=document.querySelector('#info').getBoundingClientRect();return{width:innerWidth,scrollWidth:document.documentElement.scrollWidth,map:{width:map.width,height:map.height},info:{width:info.width,height:info.height},name:document.querySelector('#info h3')?.textContent,controls:[...document.querySelectorAll('#map button,.mobile-search-trigger')].filter(b=>getComputedStyle(b).display!=='none').length}})()");
  if (selectedMobile.scrollWidth > selectedMobile.width + 2 || selectedMobile.map.width < 320 || selectedMobile.map.height < 250 || !selectedMobile.name?.includes("Praha") || !selectedMobile.controls) throw new Error(`Mobilní atlas má neplatné rozložení: ${JSON.stringify(selectedMobile)}`);
  await screenshot("explorer-atlas-mobile-selected");
  console.log(`Atlas: odkaz place=T-01 otevřel Prahu a zvýraznil ji. Mobilní atlas 390×844: šířka stránky ${selectedMobile.scrollWidth}px, mapa ${Math.round(selectedMobile.map.width)}×${Math.round(selectedMobile.map.height)}px.`);
  if (requestMethods.some((method) => method !== "GET")) throw new Error(`Herní stránka odeslala požadavek jiný než GET: ${requestMethods.join(", ")}`);
  console.log(`Síť: ${requestMethods.length} statických požadavků, všechny metodou GET.`);
} finally {
  cdp?.close();
  for (const child of [browser, ...servers]) {
    if (child.exitCode === null) { child.kill(); await new Promise((resolve) => child.once("exit", resolve)); }
  }
  fs.rmSync(tempRoot, { recursive: true, force: true });
}
