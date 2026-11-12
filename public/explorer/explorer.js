(() => {
  "use strict";
  const $ = (selector) => document.querySelector(selector);
  const STORAGE_KEY = "larpidia-explorer:v1";
  const SAVE_VERSION = 1;
  const FULL_VIEW = { x: 0, y: 0, width: 29700, height: 21000 };
  const ui = {
    intro: $("#intro-panel"), game: $("#game-panel"), summary: $("#summary-panel"), team: $("#team-name"),
    start: $("#start-button"), storageWarning: $("#storage-warning"), summaryWarning: $("#summary-storage-warning"),
    heading: $("#round-heading"), kicker: $("#round-kicker"), score: $("#live-score"), viewport: $("#map-viewport"),
    loading: $("#map-loading"), hint: $("#map-hint"), pinStatus: $("#pin-status"), confirm: $("#confirm-button"),
    skip: $("#skip-button"), actions: $("#action-bar"), resultActions: $("#result-actions"), result: $("#round-result"),
    legend: $("#map-legend"), next: $("#next-button"),
  };
  let config, places, placeById, mapSvg, overlay, guessGroup, targetGroup, connector, cursorGroup, view = { ...FULL_VIEW };
  let state = { schemaVersion: SAVE_VERSION, configVersion: null, teamName: "", started: false, currentRound: 0, guess: null, rounds: [null, null, null, null] };
  let storageAvailable = true;
  let saveWarning = "";
  let mapReady = false;
  let lastTapAt = 0;
  let scoreSceneTimer = 0;
  let returnSceneTimer = 0;
  let cursor = { x: 14850, y: 10500 };
  const pointers = new Map();
  let gesture = null;

  const fmt = (n, digits = 0) => new Intl.NumberFormat("cs-CZ", { maximumFractionDigits: digits, minimumFractionDigits: digits }).format(n);
  function warnStorage(message) {
    saveWarning = message;
    ui.storageWarning.hidden = false;
    ui.storageWarning.textContent = message;
    ui.summaryWarning.hidden = false;
    ui.summaryWarning.textContent = message;
  }
  function save() {
    if (!storageAvailable) return;
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
    catch { storageAvailable = false; warnStorage("Prohlížeč nedovolil uložit postup. Hrát můžete dál, ale po obnovení stránky se nemusí zachovat."); }
  }
  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const saved = JSON.parse(raw);
      if (!saved || saved.schemaVersion !== SAVE_VERSION || saved.configVersion !== config.mode + ":" + config.schemaVersion) {
        warnStorage("Uložený postup patří ke starší verzi hry a byl obnoven jako nová expedice.");
        return;
      }
      if (!Array.isArray(saved.rounds) || saved.rounds.length !== 4 || !Number.isInteger(saved.currentRound) || saved.currentRound < 0 || saved.currentRound > 4) throw new Error("Neplatný uložený průběh.");
      state = { ...state, ...saved, teamName: typeof saved.teamName === "string" ? saved.teamName.slice(0, 32) : "", rounds: saved.rounds };
    } catch {
      warnStorage("Uložený postup se nepodařilo přečíst. Můžete začít novou expedici.");
    }
  }
  const results = () => state.rounds.filter(Boolean);
  const total = () => window.LarpidiaScoring.totalScore(state.rounds);
  const currentResult = () => state.rounds[state.currentRound] || null;
  const atlasPlaceUrl = (placeId) => `../atlas/current/viewer/atlas.html?place=${encodeURIComponent(placeId)}`;

  function parseViewBox() { return view; }
  function setViewBox(next) {
    const width = Math.max(85, Math.min(45000, next.width));
    const height = width * (next.height / next.width);
    view = { x: next.x, y: next.y, width, height };
    view.x = Math.max(-12000, Math.min(41700 - width, view.x));
    view.y = Math.max(-9000, Math.min(30000 - height, view.y));
    if (mapSvg) mapSvg.setAttribute("viewBox", `${view.x} ${view.y} ${view.width} ${view.height}`);
    renderMarkers();
  }
  function pointFromClient(clientX, clientY) {
    if (!mapSvg) return { x: 0, y: 0 };
    const point = mapSvg.createSVGPoint();
    point.x = clientX; point.y = clientY;
    const mapped = point.matrixTransform(mapSvg.getScreenCTM().inverse());
    return { x: mapped.x, y: mapped.y };
  }
  function panPixels(dx, dy) {
    const rect = ui.viewport.getBoundingClientRect();
    const scale = mapSvg?.getScreenCTM();
    if (!scale || !rect.width || !rect.height) return;
    const a = pointFromClient(rect.left + rect.width / 2, rect.top + rect.height / 2);
    const b = pointFromClient(rect.left + rect.width / 2 + dx, rect.top + rect.height / 2 + dy);
    setViewBox({ ...view, x: view.x - (b.x - a.x), y: view.y - (b.y - a.y) });
  }
  function zoomAt(clientX, clientY, factor) {
    const anchor = pointFromClient(clientX, clientY);
    const width = Math.max(85, Math.min(45000, view.width * factor));
    const ratio = width / view.width;
    setViewBox({ x: anchor.x - (anchor.x - view.x) * ratio, y: anchor.y - (anchor.y - view.y) * ratio, width, height: view.height * ratio });
  }
  function zoomCenter(factor) {
    const rect = ui.viewport.getBoundingClientRect();
    zoomAt(rect.left + rect.width / 2, rect.top + rect.height / 2, factor);
  }
  function renderMarkers() {
    if (!overlay) return;
    const result = currentResult();
    const activeGuess = result?.guess || (!result ? state.guess : null);
    guessGroup.style.display = activeGuess ? "" : "none";
    const separateCloseMarkers = result && !result.skipped && markerDistancePx(result.guess, result.target) < 30;
    if (activeGuess) guessGroup.setAttribute("transform", markerTransform(activeGuess, separateCloseMarkers ? -9 : 0));
    targetGroup.style.display = result && !result.skipped ? "" : "none";
    if (result && !result.skipped) targetGroup.setAttribute("transform", markerTransform(result.target, separateCloseMarkers ? 9 : 0));
    connector.style.display = result && !result.skipped ? "" : "none";
    if (result && !result.skipped) {
      connector.setAttribute("x1", result.guess.x); connector.setAttribute("y1", result.guess.y);
      connector.setAttribute("x2", result.target.x); connector.setAttribute("y2", result.target.y);
    }
    cursorGroup.setAttribute("transform", markerTransform(cursor));
  }
  function markerDistancePx(first, second) {
    const matrix = mapSvg?.getScreenCTM();
    if (!matrix) return Infinity;
    const dx = (first.x - second.x) * matrix.a + (first.y - second.y) * matrix.c;
    const dy = (first.x - second.x) * matrix.b + (first.y - second.y) * matrix.d;
    return Math.hypot(dx, dy);
  }
  function markerTransform(point, offsetPx = 0) {
    const matrix = mapSvg?.getScreenCTM();
    const pixelScale = matrix ? Math.sqrt(Math.abs(matrix.a * matrix.d - matrix.b * matrix.c)) : 1;
    const counterScale = 1 / Math.max(pixelScale, 0.000001);
    return `translate(${point.x} ${point.y}) translate(${offsetPx * counterScale} 0) scale(${counterScale})`;
  }
  function makeMarker(className, label, symbol) {
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    group.setAttribute("class", className); group.setAttribute("aria-label", label);
    group.style.filter = "drop-shadow(0 1px 2px #173b3180)";
    const rim = document.createElementNS(group.namespaceURI, "circle");
    rim.setAttribute("r", "14"); rim.style.fill = "#fffdf4"; rim.style.stroke = "#173b31"; rim.style.strokeWidth = "2px";
    group.append(rim);
    const symbolShape = document.createElementNS(group.namespaceURI, symbol === "guess" ? "circle" : "path");
    if (symbol === "guess") {
      symbolShape.setAttribute("r", "9.5"); symbolShape.style.fill = "#c3462d";
      symbolShape.style.stroke = "#fff"; symbolShape.style.strokeWidth = "1.7px";
    } else {
      symbolShape.setAttribute("d", "M0 -9 L9 0 L0 9 L-9 0 Z");
      symbolShape.style.fill = "#236745"; symbolShape.style.stroke = "#fff"; symbolShape.style.strokeWidth = "1.5px";
    }
    group.append(symbolShape);
    const glyph = document.createElementNS(group.namespaceURI, "path");
    glyph.setAttribute("d", symbol === "guess" ? "M-4.5 0 L4.5 0 M0 -4.5 L0 4.5" : "M-4 0 L-1 3 L4.5 -4");
    glyph.style.fill = "none"; glyph.style.stroke = "white"; glyph.style.strokeWidth = "2px";
    glyph.style.strokeLinecap = "round"; glyph.style.strokeLinejoin = "round";
    group.append(glyph); return group;
  }
  function scopeAtlasStyles(cssText) {
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(cssText);
    function readRules(rules) {
      return [...rules].map((rule) => {
        if (rule.type === CSSRule.STYLE_RULE) {
          const selectors = rule.selectorText.split(",").map((selector) => {
            const trimmed = selector.trim();
            if (trimmed.startsWith("#map > svg")) return "#map-viewport > svg" + trimmed.slice("#map > svg".length);
            if (trimmed.startsWith("#map svg")) return "#map-viewport > svg" + trimmed.slice("#map svg".length);
            if (trimmed === "#map" || trimmed.startsWith("#map.")) return "#map-viewport > svg" + trimmed.slice("#map".length);
            return "#map-viewport > svg " + trimmed;
          });
          return `${selectors.join(",")}{${rule.style.cssText}}`;
        }
        if (rule.cssRules) return `${rule.cssText.slice(0, rule.cssText.indexOf("{"))}{${readRules(rule.cssRules)}}`;
        return rule.cssText;
      }).join("\n");
    }
    return readRules(sheet.cssRules);
  }
  async function loadMap() {
    try {
      const response = await fetch("../atlas/current/viewer/atlas.html", { credentials: "same-origin" });
      if (!response.ok) throw new Error(`Atlas odpověděl stavem ${response.status}.`);
      const html = await response.text();
      const parsed = new DOMParser().parseFromString(html, "text/html");
      const source = parsed.querySelector("#map > svg");
      if (!source) throw new Error("V atlasu nebyla nalezena zdrojová mapa.");
      mapSvg = document.importNode(source, true);
      mapSvg.removeAttribute("width"); mapSvg.removeAttribute("height");
      mapSvg.setAttribute("preserveAspectRatio", "xMidYMid meet");
      mapSvg.setAttribute("focusable", "false");
      const style = document.createElementNS("http://www.w3.org/2000/svg", "style");
      style.textContent = scopeAtlasStyles([...parsed.querySelectorAll("head style")].map((item) => item.textContent).join("\n"));
      mapSvg.insertBefore(style, mapSvg.firstChild);
      overlay = document.createElementNS(mapSvg.namespaceURI, "g"); overlay.setAttribute("class", "explorer-overlay"); overlay.setAttribute("aria-hidden", "true");
      connector = document.createElementNS(mapSvg.namespaceURI, "line"); connector.setAttribute("class", "connector"); overlay.append(connector);
      guessGroup = makeMarker("guess-marker", "Váš odhad", "guess"); targetGroup = makeMarker("target-marker", "Správné místo", "target"); cursorGroup = makeMarker("keyboard-marker", "Kurzor mapy", "guess");
      cursorGroup.style.opacity = ".58"; cursorGroup.style.display = "none";
      overlay.append(guessGroup, targetGroup, cursorGroup); mapSvg.append(overlay);
      ui.viewport.replaceChildren(mapSvg); mapReady = true; setViewBox(FULL_VIEW); render();
      new ResizeObserver(() => renderMarkers()).observe(ui.viewport);
    } catch (error) {
      ui.loading.textContent = "Atlas se nepodařilo načíst. Obnovte stránku nebo zkontrolujte, že ji otevíráte přes místní webový server.";
      ui.loading.className = "map-error";
      console.error("Larpidia Explorer map loading failed:", error);
    }
  }
  function placeGuess(point) {
    if (!mapReady || !state.started || currentResult() || state.currentRound >= 4) return;
    if (point.x < 0 || point.x > 29700 || point.y < 0 || point.y > 21000) return;
    state.guess = { x: point.x, y: point.y };
    ui.confirm.disabled = false; ui.pinStatus.textContent = "Tip označen · můžete jej přesunout";
    save(); renderMarkers();
  }
  function confirmGuess() {
    if (!state.guess || currentResult() || state.currentRound >= 4) return;
    const round = config.rounds[state.currentRound];
    const targetPlace = placeById.get(round.targetPlaceId);
    const target = window.LarpidiaExplorerCoordinates.toSvg(targetPlace.x_km, targetPlace.y_km);
    const score = window.LarpidiaScoring.scoreRound(state.guess, target);
    state.rounds[state.currentRound] = { guess: { ...state.guess }, targetConfigId: round.id, target, targetPlaceId: targetPlace.id, errorMeters: score.distanceMeters, points: score.points, skipped: false };
    state.guess = null; save(); revealResult();
  }
  function skipRound() {
    if (currentResult() || state.currentRound >= 4 || !window.confirm("Přeskočit toto kolo? Získáte 0 bodů a odpověď už nepůjde změnit.")) return;
    state.rounds[state.currentRound] = { guess: null, targetConfigId: config.rounds[state.currentRound].id, target: null, targetPlaceId: null, errorMeters: null, points: 0, skipped: true };
    state.guess = null; save(); revealResult();
  }
  function formatDistance(meters) {
    if (meters < 1000) return `${fmt(Math.round(meters))} m`;
    return `${fmt(meters / 1000, meters >= 10000 ? 1 : 2)} km`;
  }
  function revealResult() {
    const result = currentResult();
    if (!result) return;
    ui.result.hidden = false; ui.actions.hidden = true; ui.resultActions.hidden = false; ui.legend.hidden = !mapReady;
    if (result.skipped) {
      $("#result-guess").textContent = "Kolo přeskočeno";
      $("#result-place").textContent = "Cíl zůstává skrytý";
      $("#result-place").removeAttribute("href");
      $("#result-description").textContent = "Za toto kolo se body nepřičítají.";
      $("#result-distance").textContent = "—";
      $("#result-points").textContent = "+0 bodů";
    } else {
      const place = placeById.get(result.targetPlaceId);
      $("#result-guess").textContent = "Označené místo na mapě";
      $("#result-place").textContent = place.name_cs;
      $("#result-place").href = atlasPlaceUrl(place.id);
      $("#result-place").setAttribute("aria-label", `Otevřít místo ${place.name_cs} ve veřejném atlasu`);
      $("#result-description").textContent = place.description;
      $("#result-distance").textContent = formatDistance(result.errorMeters);
      $("#result-points").textContent = `+${fmt(result.points)} bodů`;
      if (mapReady) fitPoints([result.guess, result.target]);
    }
    ui.score.textContent = `${fmt(total())} / 20 000`;
    ui.next.textContent = state.currentRound === 3 ? "Zobrazit výsledky" : "Další kolo";
    ui.heading.textContent = `Kolo ${state.currentRound + 1}/4`;
    $("#round-total-label").textContent = `Po kole: ${fmt(total())} bodů`;
    renderMarkers();
  }
  function fitPoints(points) {
    if (!points.length) return;
    const minX = Math.min(...points.map((p) => p.x)), maxX = Math.max(...points.map((p) => p.x));
    const minY = Math.min(...points.map((p) => p.y)), maxY = Math.max(...points.map((p) => p.y));
    const padding = Math.max(800, Math.max(maxX - minX, maxY - minY) * .45);
    const rect = ui.viewport.getBoundingClientRect();
    const ar = rect.width / Math.max(1, rect.height);
    let width = Math.max(1000, maxX - minX + padding * 2), height = Math.max(1000, maxY - minY + padding * 2);
    if (width / height < ar) width = height * ar; else height = width / ar;
    setViewBox({ x: (minX + maxX - width) / 2, y: (minY + maxY - height) / 2, width, height });
  }
  function showLowScoreScene() {
    const scene = $("#score-scene");
    scene.hidden = false;
    scene.classList.remove("revealed", "flower-mode", "no-answer");
    $("#score-fox").hidden = false;
    $("#score-flower").hidden = true;
    $("#score-scene-title").textContent = "You didn't even try, did you?";
    $("#score-scene-copy").textContent = "Tahle expedice skončila s méně než 3 000 body.";
    $("#score-scene-actions").hidden = false;
    $("#score-return").hidden = true;
    clearTimeout(scoreSceneTimer); clearTimeout(returnSceneTimer);
    scoreSceneTimer = setTimeout(() => {
      scene.classList.add("revealed");
      $("#score-did").focus();
    }, 1250);
  }
  function closeLowScoreScene() {
    const scene = $("#score-scene");
    clearTimeout(scoreSceneTimer); clearTimeout(returnSceneTimer);
    scene.hidden = true;
    $("#new-game-button").focus();
  }
  function answerI_did() {
    $("#score-fox").hidden = true;
    $("#score-flower").hidden = false;
    $("#score-scene").classList.add("flower-mode");
    $("#score-scene-title").textContent = "maybe it wasn't your lucky day...";
    $("#score-scene-copy").textContent = `Vaše skóre ${fmt(total())} bodů zůstává zachováno.`;
    $("#score-scene-actions").hidden = true;
    $("#score-return").hidden = false;
    $("#score-return").focus();
  }
  function answerNo() {
    const scene = $("#score-scene");
    scene.classList.add("no-answer");
    $("#score-return").hidden = true;
    clearTimeout(returnSceneTimer);
    returnSceneTimer = setTimeout(() => {
      $("#score-return").hidden = false;
      $("#score-return").focus();
    }, 1600);
  }
  function showSummary() {
    ui.intro.hidden = true; ui.game.hidden = true; ui.summary.hidden = false;
    $("#team-result").textContent = state.teamName ? `Tým: ${state.teamName}` : "Vaše expedice";
    $("#final-score").textContent = fmt(total());
    const breakdown = $("#breakdown"); breakdown.replaceChildren();
    state.rounds.forEach((round, index) => {
      const row = document.createElement("div"); row.className = "break-row";
      const title = document.createElement("strong"); title.textContent = `Kolo ${index + 1}`;
      const points = document.createElement("span"); points.textContent = `+${fmt(round?.points || 0)} bodů`;
      const distance = document.createElement("span"); distance.textContent = round?.skipped ? "Přeskočeno" : formatDistance(round?.errorMeters || 0);
      row.append(title, points, distance); breakdown.append(row);
      if (round?.targetPlaceId) {
        const placeLink = document.createElement("a"); placeLink.className = "summary-place-link";
        placeLink.href = atlasPlaceUrl(round.targetPlaceId); placeLink.target = "_blank"; placeLink.rel = "noopener";
        placeLink.textContent = `${placeById.get(round.targetPlaceId).name_cs} · Zobrazit v atlasu ↗`;
        row.append(placeLink);
      }
    });
    save();
    if (total() < 3000 && !$("#score-scene").dataset.played) {
      $("#score-scene").dataset.played = "true";
      showLowScoreScene();
    }
  }
  function startSummaryIfComplete() {
    if (state.currentRound >= 4 && state.rounds.every(Boolean)) showSummary();
  }
  function advance() {
    if (!currentResult()) return;
    if (state.currentRound === 3) { state.currentRound = 4; save(); showSummary(); return; }
    state.currentRound += 1; state.guess = null; setViewBox(FULL_VIEW); save(); render();
    ui.viewport.focus({ preventScroll: true });
  }
  function render() {
    ui.intro.hidden = state.started;
    ui.game.hidden = !state.started || state.currentRound >= 4;
    ui.summary.hidden = !state.started || state.currentRound < 4;
    if (!state.started) { ui.team.value = state.teamName; return; }
    if (state.currentRound >= 4) { startSummaryIfComplete(); return; }
    const result = currentResult();
    ui.heading.textContent = `Kolo ${state.currentRound + 1}/4`;
    ui.kicker.textContent = `Expedice · ${state.teamName || "váš tým"}`;
    ui.score.textContent = `${fmt(total())} / 20 000`;
    ui.confirm.disabled = !state.guess || Boolean(result);
    ui.pinStatus.textContent = state.guess ? "Tip označen · můžete jej přesunout" : "Tip zatím není označen";
    ui.result.hidden = !result;
    ui.actions.hidden = Boolean(result);
    ui.resultActions.hidden = !result;
    if (mapReady) renderMarkers();
    if (result) revealResult();
  }

  function setNewGame() {
    if (!window.confirm("Začít novou expedici? Dosavadní postup v tomto zařízení se smaže.")) return;
    try { localStorage.removeItem(STORAGE_KEY); } catch { warnStorage("Prohlížeč nedovolil odstranit uložený postup."); }
    state = { schemaVersion: SAVE_VERSION, configVersion: config.mode + ":" + config.schemaVersion, teamName: "", started: false, currentRound: 0, guess: null, rounds: [null, null, null, null] };
    ui.summaryWarning.hidden = true; ui.storageWarning.hidden = !saveWarning; setViewBox(FULL_VIEW); render();
  }
  function clientPoint(event) { return { x: event.clientX, y: event.clientY }; }
  ui.viewport.addEventListener("pointerdown", (event) => {
    if (cursorGroup) cursorGroup.style.display = "none";
    if (!mapReady) return;
    ui.viewport.setPointerCapture(event.pointerId);
    const pt = clientPoint(event); pointers.set(event.pointerId, pt);
    if (pointers.size === 1) gesture = { start: pt, last: pt, moved: false, type: "pan" };
    else if (pointers.size === 2) {
      const [a, b] = [...pointers.values()];
      gesture = { type: "pinch", midpoint: { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }, distance: Math.hypot(a.x - b.x, a.y - b.y), moved: true };
    }
  });
  ui.viewport.addEventListener("pointermove", (event) => {
    if (!pointers.has(event.pointerId) || !gesture) return;
    const next = clientPoint(event), previous = pointers.get(event.pointerId);
    pointers.set(event.pointerId, next);
    if (pointers.size === 1 && gesture.type === "pan") {
      const dx = next.x - gesture.last.x, dy = next.y - gesture.last.y;
      if (Math.hypot(next.x - gesture.start.x, next.y - gesture.start.y) > 5) gesture.moved = true;
      if (gesture.moved) panPixels(dx, dy);
      gesture.last = next;
    } else if (pointers.size === 2) {
      const [a, b] = [...pointers.values()], midpoint = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
      const distance = Math.hypot(a.x - b.x, a.y - b.y);
      if (gesture.distance > 1 && distance > 1) zoomAt(gesture.midpoint.x, gesture.midpoint.y, gesture.distance / distance);
      panPixels(midpoint.x - gesture.midpoint.x, midpoint.y - gesture.midpoint.y);
      gesture = { type: "pinch", midpoint, distance, moved: true };
    }
  });
  function endPointer(event) {
    const wasTap = pointers.size === 1 && gesture?.type === "pan" && !gesture.moved;
    const point = clientPoint(event);
    pointers.delete(event.pointerId);
    if (wasTap) {
      const now = Date.now();
      placeGuess(pointFromClient(point.x, point.y));
      if (now - lastTapAt < 280) zoomAt(point.x, point.y, .68);
      lastTapAt = now;
    }
    if (!pointers.size) gesture = null;
    else if (pointers.size === 1) { const remaining = [...pointers.values()][0]; gesture = { type: "pan", start: remaining, last: remaining, moved: true }; }
  }
  ui.viewport.addEventListener("pointerup", endPointer);
  ui.viewport.addEventListener("pointercancel", endPointer);
  ui.viewport.addEventListener("wheel", (event) => { if (!mapReady) return; event.preventDefault(); zoomAt(event.clientX, event.clientY, event.deltaY < 0 ? .82 : 1.22); }, { passive: false });
  ui.viewport.addEventListener("dblclick", (event) => { event.preventDefault(); zoomAt(event.clientX, event.clientY, .6); });
  ui.viewport.addEventListener("blur", () => { if (cursorGroup) cursorGroup.style.display = "none"; });
  ui.viewport.addEventListener("keydown", (event) => {
    const step = Math.max(40, view.width * .035); let changed = true;
    if (event.key === "ArrowLeft") cursor.x -= step;
    else if (event.key === "ArrowRight") cursor.x += step;
    else if (event.key === "ArrowUp") cursor.y -= step;
    else if (event.key === "ArrowDown") cursor.y += step;
    else if (event.key === "Enter" || event.key === " ") placeGuess(cursor);
    else changed = false;
    if (changed) {
      event.preventDefault();
      if (cursorGroup) cursorGroup.style.display = event.key.startsWith("Arrow") ? "" : "none";
      renderMarkers();
    }
  });

  ui.start.addEventListener("click", () => {
    state.teamName = ui.team.value.trim().slice(0, 32); state.started = true;
    state.configVersion = config.mode + ":" + config.schemaVersion; save(); render();
  });
  ui.confirm.addEventListener("click", confirmGuess);
  ui.skip.addEventListener("click", skipRound);
  ui.next.addEventListener("click", advance);
  $("#zoom-in").addEventListener("click", () => zoomCenter(.72));
  $("#zoom-out").addEventListener("click", () => zoomCenter(1.4));
  $("#reset-view").addEventListener("click", () => setViewBox(FULL_VIEW));
  $("#new-game-button").addEventListener("click", setNewGame);
  $("#reset-game").addEventListener("click", setNewGame);
  $("#score-did").addEventListener("click", answerI_did);
  $("#score-no").addEventListener("click", answerNo);
  $("#score-return").addEventListener("click", closeLowScoreScene);
  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !$("#score-scene").hidden) closeLowScoreScene();
  });

  async function init() {
    try {
      const [configResponse, placesResponse] = await Promise.all([
        fetch("rounds.json", { credentials: "same-origin" }),
        fetch("../atlas/current/registry/places.public.json", { credentials: "same-origin" }),
      ]);
      if (!configResponse.ok || !placesResponse.ok) throw new Error("Nepodařilo se načíst veřejnou konfiguraci hry a atlasu.");
      [config, places] = await Promise.all([configResponse.json(), placesResponse.json()]);
      if (config.schemaVersion !== 1 || !["demo", "production"].includes(config.mode) || !Array.isArray(config.rounds) || config.rounds.length !== 4) throw new Error("Konfigurace musí obsahovat čtyři kola a podporované schemaVersion.");
      if (!Array.isArray(places.objects) || places.objects.length !== 159) throw new Error("Veřejný registr atlasu nemá očekávaných 159 míst.");
      placeById = new Map(places.objects.map((place) => [place.id, place]));
      for (const round of config.rounds) {
        const target = placeById.get(round.targetPlaceId);
        if (!target || !Number.isFinite(target.x_km) || !Number.isFinite(target.y_km) || target.x_km < 0 || target.x_km > 29.7 || target.y_km < 0 || target.y_km > 21) throw new Error(`Kolo ${round.publicNumber}: cíl neodpovídá skutečnému veřejnému místu atlasu.`);
      }
      $("#mode-label").textContent = config.mode === "demo" ? "Zkušební expedice · ukázkové cíle z veřejného atlasu" : "Expedice Larpidií";
      state.configVersion = config.mode + ":" + config.schemaVersion;
      load();
      if (state.started && state.currentRound < 4) ui.viewport.focus({ preventScroll: true });
      await loadMap();
      ui.start.disabled = !mapReady;
      $("#reset-game").disabled = !mapReady;
      render();
    } catch (error) {
      $("#mode-label").textContent = "Hru se nepodařilo připravit";
      ui.storageWarning.hidden = false;
      ui.storageWarning.textContent = error.message;
      ui.start.disabled = true;
      console.error("Larpidia Explorer configuration error:", error);
    }
  }
  window.LarpidiaExplorerAccess.ready.then(init);
})();
