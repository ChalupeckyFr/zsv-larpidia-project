(() => {
  const views = [...document.querySelectorAll("[data-view]")];
  const navLinks = [...document.querySelectorAll("[data-nav]")];
  const menuButton = document.querySelector(".menu-toggle");
  const mainNav = document.querySelector(".main-nav");
  const toast = document.querySelector(".toast");
  const homeSlogans = [
    "Místo, kde se<br /><em>potkávají světy.</em>",
    "Life is meant<br /><em>to be lived.</em>",
    "Ostrov, kde život<br /><em>znamená víc než každodenní rutinu.</em>",
  ];
  let inMemorySlogan = -1;

  function rotateHomeSlogan() {
    const heading = document.getElementById("home-slogan");
    if (!heading) return;
    let previous = inMemorySlogan;
    try {
      const saved = window.localStorage.getItem("larpidia-home-slogan");
      const stored = saved === null ? Number.NaN : Number(saved);
      if (Number.isInteger(stored) && stored >= 0 && stored < homeSlogans.length) previous = stored;
      const next = (previous + 1) % homeSlogans.length;
      window.localStorage.setItem("larpidia-home-slogan", String(next));
      inMemorySlogan = next;
      heading.innerHTML = homeSlogans[next];
    } catch {
      inMemorySlogan = (inMemorySlogan + 1) % homeSlogans.length;
      heading.innerHTML = homeSlogans[inMemorySlogan];
    }
  }

  function routeForHash(hash) {
    if (hash.startsWith("#wiki-")) return "encyklopedie";
    const route = hash.replace(/^#/, "").split("-")[0];
    return views.some((view) => view.dataset.view === route) ? route : "domu";
  }

  function loadFrames(scope) {
    scope.querySelectorAll("iframe[data-src]").forEach((frame) => {
      if (frame.closest("[hidden]")) return;
      if (!frame.getAttribute("src")) frame.src = frame.dataset.src;
    });
  }

  function setAtlasMode(mode) {
    document.querySelectorAll("[data-atlas-mode]").forEach((button) => {
      const selected = button.dataset.atlasMode === mode;
      button.classList.toggle("selected", selected);
      button.setAttribute("aria-selected", String(selected));
    });
    document.querySelectorAll("[data-map-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.mapPanel !== mode;
      if (!panel.hidden) loadFrames(panel);
    });
    const link = document.getElementById("open-map-link");
    if (link) {
      const isTerrain = mode === "terrain3d";
      link.href = isTerrain
        ? "atlas/current/viewer/terrain-3d.html"
        : mode === "capital"
          ? "atlas/current/capital/capital_plan_viewer.html"
          : "atlas/current/viewer/atlas.html";
      link.textContent = isTerrain ? "Otevřít 3D model zvlášť ↗" : "Otevřít atlas v novém okně ↗";
    }
  }

  function activateView(viewName, { scroll = true } = {}) {
    if (viewName === "domu") rotateHomeSlogan();
    views.forEach((view) => {
      const active = view.dataset.view === viewName;
      view.hidden = !active;
      view.classList.toggle("active", active);
    });
    navLinks.forEach((link) => {
      const active = link.dataset.nav === viewName;
      link.classList.toggle("active", active);
      if (active) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
    const activeView = views.find((view) => view.dataset.view === viewName);
    if (activeView) loadFrames(activeView);
    mainNav.classList.remove("open");
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Otevřít navigaci");
    if (scroll) window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function showFromHash() {
    const hash = window.location.hash;
    const route = routeForHash(hash);
    activateView(route, { scroll: !hash.startsWith("#wiki-") });
    if (hash.startsWith("#wiki-")) {
      window.setTimeout(() => document.getElementById(hash.slice(1))?.scrollIntoView({ block: "start" }), 40);
    }
  }

  window.addEventListener("hashchange", showFromHash);
  showFromHash();

  document.querySelectorAll("[data-atlas-mode]").forEach((button) => {
    button.addEventListener("click", () => setAtlasMode(button.dataset.atlasMode));
  });

  menuButton.addEventListener("click", () => {
    const open = !mainNav.classList.contains("open");
    mainNav.classList.toggle("open", open);
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute("aria-label", open ? "Zavřít navigaci" : "Otevřít navigaci");
  });

  let toastTimeout;
  function notify(message) {
    toast.textContent = message;
    toast.classList.add("show");
    window.clearTimeout(toastTimeout);
    toastTimeout = window.setTimeout(() => toast.classList.remove("show"), 2300);
  }

  async function copyText(text) {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const field = document.createElement("textarea");
        field.value = text;
        field.style.position = "fixed";
        field.style.opacity = "0";
        document.body.append(field);
        field.select();
        const ok = document.execCommand("copy");
        field.remove();
        if (!ok) throw new Error("copy failed");
      }
      notify("Text byl zkopírován do schránky.");
    } catch {
      notify("Kopírování není v tomto prohlížeči dostupné.");
    }
  }

  document.querySelectorAll(".copy-text").forEach((button) => {
    button.addEventListener("click", () => {
      const source = document.getElementById(button.dataset.copy);
      if (source) copyText(source.innerText.trim());
    });
  });

  const dialog = document.querySelector(".map-dialog");
  const dialogImage = dialog.querySelector("img");
  const dialogTitle = document.getElementById("dialog-map-title");
  const originalLink = dialog.querySelector(".dialog-original");
  document.querySelectorAll("[data-map-image]").forEach((button) => {
    button.addEventListener("click", () => {
      const imagePath = button.dataset.mapImage;
      dialogTitle.textContent = button.dataset.mapTitle || "Mapa Larpidie";
      dialogImage.src = imagePath;
      dialogImage.alt = button.dataset.mapTitle || "Mapa Larpidie";
      originalLink.href = imagePath;
      if (typeof dialog.showModal === "function") dialog.showModal();
      else window.open(imagePath, "_blank", "noopener");
    });
  });
  dialog.querySelector(".dialog-close").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
})();
