(() => {
  const app = document.querySelector("[data-encyclopedia-app]");
  if (!app) return;

  const formatters = {
    number: new Intl.NumberFormat("cs-CZ"),
    currency: new Intl.NumberFormat("cs-CZ", { style: "currency", currency: "CZK", maximumFractionDigits: 0 }),
  };
  let catalog;
  let facts;
  let media;
  let articles = [];
  let articleLoadPromise;
  let computed = {};

  const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
  const get = (root, path) => path.split(".").reduce((value, key) => value == null ? undefined : value[key], root);
  const titleCase = (value) => value.charAt(0).toLocaleUpperCase("cs-CZ") + value.slice(1);
  const slugify = (value) => value.toLocaleLowerCase("cs-CZ").normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const routeFor = (categoryId, articleId) => `#encyklopedie/${categoryId}/${articleId}`;
  const allArticles = () => catalog.categories.flatMap((category) => category.articles.map((article) => ({ ...article, category })));
  const legacyRoutes = {
    "#wiki-prehled": "#encyklopedie/zakladni-informace/prehled",
    "#wiki-jmeno": "#encyklopedie/zakladni-informace/obyvatelstvo-a-jazyky",
    "#wiki-geografie": "#encyklopedie/geografie/ostrovy",
    "#wiki-spolecnost": "#encyklopedie/spolecnost/kultura-a-svatky",
    "#wiki-politika": "#encyklopedie/politika/ustavni-system",
    "#wiki-ekonomika": "#encyklopedie/ekonomika/ekonomicky-model",
    "#wiki-historie": "#encyklopedie/historie/casova-osa",
    "#wiki-turismus": "#encyklopedie/paraland/turistika-a-rezervace",
    "#wiki-prezentace": "#encyklopedie/zakladni-informace/prehled",
    "#wiki-stavy": "#encyklopedie",
  };

  function calculateFacts() {
    const result = { economy: {} };
    const definitions = facts.derived || {};
    const pending = new Set(Object.keys(definitions));
    const resolve = (path) => {
      if (path.startsWith("calc.")) return get(result, path.slice(5));
      if (path === "12") return 12;
      return get(facts, path);
    };
    let guard = pending.size + 2;
    while (pending.size && guard-- > 0) {
      for (const name of [...pending]) {
        const definition = definitions[name];
        const args = definition.inputs.map(resolve);
        if (args.some((value) => value === undefined)) continue;
        let value;
        if (definition.operation === "multiply") value = args.reduce((total, item) => total * Number(item), 1);
        else if (definition.operation === "percentOf") value = Number(args[0]) * Number(args[1]) / 100;
        else if (definition.operation === "subtract") value = Number(args[0]) - Number(args[1]);
        else if (definition.operation === "sumThenSubtract") value = Number(args[0]) + Number(args[1]) - Number(args[2]);
        if (!Number.isFinite(value)) continue;
        result.economy[name] = value;
        pending.delete(name);
      }
    }
    return result;
  }

  function displayFact(value, format) {
    if (Array.isArray(value)) return value.join(", ");
    if (format === "percent") return `${formatters.number.format(Number(value))} %`;
    if (format === "czk") return formatters.currency.format(Number(value));
    if (format === "area") return `${formatters.number.format(Number(value))} km²`;
    if (format === "number" || typeof value === "number") return formatters.number.format(Number(value));
    return String(value ?? "");
  }

  function fillSharedFacts() {
    document.querySelectorAll("[data-fact]").forEach((node) => {
      const value = get(facts, node.dataset.fact);
      if (value !== undefined) node.textContent = displayFact(value, node.dataset.format);
    });
  }

  function resolveTokens(source) {
    return source.replace(/\{\{(fact|calc)\.([\w.]+)(?:\|([\w]+))?\}\}/g, (_token, sourceType, path, format) => {
      const value = get(sourceType === "fact" ? facts : computed, path);
      return value === undefined ? "[údaj není v centrálních datech]" : displayFact(value, format);
    });
  }

  function safeHref(href) {
    const candidate = href.trim();
    if (/^(#|https:\/\/|mailto:)/i.test(candidate)) return candidate;
    if (/^[\w./-]+\.(?:html|pdf|png|jpe?g|svg|md)$/i.test(candidate)) return candidate;
    return "#encyklopedie";
  }

  function inlineMarkdown(text, assetNodes) {
    let value = esc(text);
    value = value.replace(/`([^`]+)`/g, "<code>$1</code>");
    value = value.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    value = value.replace(/\*([^*]+)\*/g, "<em>$1</em>");
    value = value.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, label, href) => `<a href="${esc(safeHref(href))}">${label}</a>`);
    value = value.replace(/@@ASSET_(\d+)@@/g, (_match, index) => assetNodes[Number(index)] || "");
    return value;
  }

  function renderMarkdown(source, article) {
    const assets = [];
    let markdown = resolveTokens(source).replace(/!\[([^\]]*)\]\(asset:([\w-]+)\)/g, (_match, alt, id) => {
      const item = media.assets.find((asset) => asset.id === id);
      if (!item) return "";
      const index = assets.length;
      assets.push(`<figure class="ency-media"><img src="${esc(item.src)}" alt="${esc(alt || item.alt)}" loading="lazy"><figcaption>${esc(item.caption)}</figcaption></figure>`);
      return `\n@@ASSET_${index}@@\n`;
    });
    const lines = markdown.replace(/\r/g, "").split("\n");
    const blocks = [];
    const toc = [];
    let i = 0;
    while (i < lines.length) {
      const line = lines[i].trim();
      if (!line) { i++; continue; }
      const heading = line.match(/^(#{1,3})\s+(.+)$/);
      if (heading) {
        const level = heading[1].length;
        const label = heading[2].replace(/\*|`/g, "");
        const id = `${article.category.id}-${article.id}-${slugify(label)}`;
        blocks.push(`<h${level} id="${esc(id)}">${inlineMarkdown(label, assets)}</h${level}>`);
        if (level === 2 || level === 3) toc.push({ id, label, level });
        i++; continue;
      }
      if (/^@@ASSET_\d+@@$/.test(line)) { blocks.push(`<div class="ency-asset-slot">${inlineMarkdown(line, assets)}</div>`); i++; continue; }
      if (line.startsWith("|")) {
        const rows = [];
        while (i < lines.length && lines[i].trim().startsWith("|")) rows.push(lines[i++].trim());
        const cells = rows.map((row) => row.split("|").slice(1, -1).map((cell) => cell.trim()));
        const bodyRows = cells.filter((row) => !row.every((cell) => /^:?-{3,}:?$/.test(cell)));
        if (bodyRows.length) {
          const [header, ...body] = bodyRows;
          blocks.push(`<div class="ency-table-scroll"><table><thead><tr>${header.map((cell) => `<th>${inlineMarkdown(cell, assets)}</th>`).join("")}</tr></thead><tbody>${body.map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell, assets)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);
        }
        continue;
      }
      if (/^[-*]\s+/.test(line) || /^\d+\.\s+/.test(line)) {
        const ordered = /^\d+\.\s+/.test(line);
        const tag = ordered ? "ol" : "ul";
        const items = [];
        while (i < lines.length && (ordered ? /^\s*\d+\.\s+/.test(lines[i]) : /^\s*[-*]\s+/.test(lines[i]))) {
          items.push(`<li>${inlineMarkdown(lines[i].replace(/^\s*(?:[-*]|\d+\.)\s+/, ""), assets)}</li>`);
          i++;
        }
        blocks.push(`<${tag}>${items.join("")}</${tag}>`);
        continue;
      }
      if (line.startsWith("> ")) {
        const quote = [];
        while (i < lines.length && lines[i].trim().startsWith(">")) quote.push(inlineMarkdown(lines[i].trim().replace(/^>\s?/, ""), assets)), i++;
        blocks.push(`<blockquote>${quote.map((item) => `<p>${item}</p>`).join("")}</blockquote>`);
        continue;
      }
      const paragraph = [line];
      i++;
      while (i < lines.length && lines[i].trim() && !/^(#{1,3})\s+|\|[- :|]+\|$|[-*]\s+|\d+\.\s+|>\s?|@@ASSET_\d+@@$/.test(lines[i].trim())) paragraph.push(lines[i++].trim());
      blocks.push(`<p>${inlineMarkdown(paragraph.join(" "), assets)}</p>`);
    }
    return { html: blocks.join("\n"), toc };
  }

  function articleHref(article) { return routeFor(article.category.id, article.id); }

  function searchBox() {
    return `<div class="ency-search-wrap"><label class="ency-search"><span aria-hidden="true">⌕</span><input type="search" data-ency-search placeholder="Hledat v článcích…" aria-label="Hledat v encyklopedii"><kbd>/</kbd></label><div class="ency-search-results" data-search-results hidden></div></div>`;
  }

  function renderNav(activeId) {
    return `<aside class="ency-sidebar"><a class="ency-home-link" href="#encyklopedie">← Přehled encyklopedie</a><p class="ency-side-label">KATEGORIE</p><nav aria-label="Kategorie encyklopedie">${catalog.categories.map((category) => `<a class="ency-nav-category ${category.id === activeId ? "active" : ""}" href="#encyklopedie/${category.id}"><span>${category.icon}</span><b>${esc(category.title)}</b></a>`).join("")}</nav><div class="ency-side-links"><a href="#atlas">Otevřít atlas ↗</a><a href="#galerie">Prohlédnout galerii ↗</a></div></aside>`;
  }

  function renderSearchMatches(query, container) {
    const needle = query.trim().toLocaleLowerCase("cs-CZ");
    if (!needle) { container.hidden = true; container.innerHTML = ""; return; }
    const matches = articles.filter((article) => `${article.title} ${article.summary} ${(article.keywords || []).join(" ")} ${resolveTokens(article.text)}`.toLocaleLowerCase("cs-CZ").includes(needle)).slice(0, 8);
    container.innerHTML = matches.length
      ? matches.map((article) => `<a class="ency-search-result" href="${articleHref(article)}"><span>${esc(article.category.title)}</span><b>${esc(article.title)}</b><small>${esc(article.summary)}</small></a>`).join("")
      : `<p class="ency-no-results">Pro „${esc(query)}“ jsme nic nenašli.</p>`;
    container.hidden = false;
  }

  function hookSearch() {
    const input = app.querySelector("[data-ency-search]");
    const results = app.querySelector("[data-search-results]");
    if (!input || !results) return;
    input.addEventListener("input", () => renderSearchMatches(input.value, results));
    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter") results.querySelector("a")?.click();
      if (event.key === "Escape") { input.value = ""; renderSearchMatches("", results); input.blur(); }
    });
  }

  function renderHub() {
    const stats = [
      ["Obyvatel", displayFact(facts.country.population, "number"), "country.population"],
      ["Hlavní ostrov", displayFact(facts.country.mainIslandAreaKm2, "area"), "country.mainIslandAreaKm2"],
      ["Druhý ostrov", displayFact(facts.country.paralandAreaKm2, "area"), "country.paralandAreaKm2"],
      ["Spoluvládci", displayFact(facts.constitution.coRulers, "number"), "constitution.coRulers"],
    ];
    app.innerHTML = `<div class="ency-layout">${renderNav("")}<div class="ency-main"><div class="ency-topline"><span>VEŘEJNÝ PRŮVODCE · ŠKOLNÍ PROJEKT</span><span>FIKTIVNÍ STÁT</span></div><div class="ency-hub-intro"><p class="eyebrow">ENCYKLOPEDIE LARPIDIE</p><h2>Malý ostrovní stát,<br><em>promyšlený do detailu.</em></h2><p>${esc(catalog.description)} Začněte rychlým přehledem nebo otevřete téma, které vás zajímá.</p></div>${searchBox()}<div class="ency-stats">${stats.map(([label, value, path]) => `<div><span>${esc(label)}</span><b data-fact="${path}">${esc(value)}</b></div>`).join("")}</div><div class="ency-category-grid">${catalog.categories.map((category) => `<section class="ency-category-card"><div class="ency-category-card-top"><span>${category.icon} / ${esc(category.eyebrow)}</span><span>↗</span></div><h3><a href="#encyklopedie/${category.id}">${esc(category.title)}</a></h3><p>${esc(category.description)}</p><ul>${category.articles.map((article) => `<li><a href="${routeFor(category.id, article.id)}">${esc(article.title)}<span>→</span></a></li>`).join("")}</ul></section>`).join("")}</div><div class="ency-tools"><div><span class="ency-tool-kicker">MAPY A MÍSTA</span><h3>Čtěte a prohlížejte současně.</h3><p>Články odkazují na interaktivní atlas, plán Larpingtonu i existující galerii.</p></div><a class="button button-dark" href="#atlas">Otevřít atlas <span>↗</span></a><a class="button button-light" href="#galerie">Přejít do galerie <span>↗</span></a></div><div class="ency-fiction-note"><b>Fiktivní školní projekt</b><span>Larpidie, její lidé, instituce, historie, smlouvy a ekonomické údaje jsou smyšlené. Ekonomické propočty jsou u každého tématu označené jako modelové.</span></div><div class="ency-edit-links"><a href="CANON_EDITING_GUIDE.md" target="_blank">Jak upravovat obsah ↗</a><a href="ENCYCLOPEDIA_MIGRATION_REPORT.md" target="_blank">Migrační přehled ↗</a></div></div></div>`;
    hookSearch();
    fillSharedFacts();
  }

  function renderCategory(category) {
    app.innerHTML = `<div class="ency-layout">${renderNav(category.id)}<div class="ency-main"><div class="ency-topline"><span><a href="#encyklopedie">ENCYKLOPEDIE</a> / KATEGORIE</span><span>${category.icon} · ${esc(category.eyebrow)}</span></div><div class="ency-category-heading"><a href="#encyklopedie">← Všechny kategorie</a><h2>${esc(category.title)}</h2><p>${esc(category.description)}</p></div>${searchBox()}<div class="ency-article-list">${category.articles.map((article, index) => `<a class="ency-list-item" href="${routeFor(category.id, article.id)}"><span class="ency-list-index">${String(index + 1).padStart(2, "0")}</span><span><b>${esc(article.title)}</b><small>${esc(article.summary)}</small></span><span class="ency-list-arrow">↗</span></a>`).join("")}</div><div class="ency-related-links"><a href="#atlas">Otevřít atlas ↗</a><a href="#galerie">Prohlédnout galerii ↗</a></div></div></div>`;
    hookSearch();
  }

  function renderArticle(article) {
    const rendered = renderMarkdown(article.text, article);
    const toc = rendered.toc.length ? `<aside class="ency-toc"><b>V TOMTO ČLÁNKU</b>${rendered.toc.map((item) => `<a class="level-${item.level}" href="#${esc(item.id)}">${esc(item.label)}</a>`).join("")}</aside>` : "";
    const siblings = article.category.articles.map((item) => ({ ...item, category: article.category }));
    const index = siblings.findIndex((item) => item.id === article.id);
    const prev = siblings[index - 1];
    const next = siblings[index + 1];
    app.innerHTML = `<div class="ency-layout">${renderNav(article.category.id)}<div class="ency-main"><div class="ency-topline"><span><a href="#encyklopedie">ENCYKLOPEDIE</a> / <a href="#encyklopedie/${article.category.id}">${esc(article.category.title)}</a></span><span>ČLÁNEK · ${esc(article.category.eyebrow)}</span></div>${searchBox()}<div class="ency-article-layout"><article class="ency-article"><nav class="ency-breadcrumb" aria-label="Drobečková navigace"><a href="#encyklopedie">Encyklopedie</a><span>›</span><a href="#encyklopedie/${article.category.id}">${esc(article.category.title)}</a><span>›</span><span>${esc(article.title)}</span></nav><div class="ency-article-heading"><div class="ency-article-heading-line"><span class="ency-article-kicker">${esc(article.category.eyebrow)}</span><button class="ency-copy-button" type="button" data-copy-article>Kopírovat článek <span aria-hidden="true">▣</span></button></div><h2>${esc(article.title)}</h2><p>${esc(article.summary)}</p><span class="ency-copy-status" data-copy-status aria-live="polite"></span></div><div class="ency-prose">${rendered.html}</div><div class="ency-article-bottom"><span>Obsah je součástí fikčního školního projektu.</span><a href="#encyklopedie">Zpět na rozcestník ↑</a></div><nav class="ency-prevnext" aria-label="Další články">${prev ? `<a href="${articleHref(prev)}"><small>← PŘEDCHOZÍ</small><b>${esc(prev.title)}</b></a>` : `<span></span>`}${next ? `<a href="${articleHref(next)}"><small>DALŠÍ →</small><b>${esc(next.title)}</b></a>` : `<span></span>`}</nav></article>${toc}</div></div></div>`;
    hookSearch();
    hookArticleCopy();
    fillSharedFacts();
    app.querySelectorAll(".ency-toc a").forEach((link) => link.addEventListener("click", (event) => {
      const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      if (target) { event.preventDefault(); target.scrollIntoView({ behavior: "smooth", block: "start" }); }
    }));
  }

  function hookArticleCopy() {
    const button = app.querySelector("[data-copy-article]");
    const source = app.querySelector(".ency-prose");
    const status = app.querySelector("[data-copy-status]");
    if (!button || !source || !status) return;
    button.addEventListener("click", async () => {
      const text = source.innerText.trim();
      try {
        if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(text);
        else {
          const field = document.createElement("textarea");
          field.value = text;
          field.style.position = "fixed";
          field.style.opacity = "0";
          document.body.append(field);
          field.select();
          const copied = document.execCommand("copy");
          field.remove();
          if (!copied) throw new Error("copy unavailable");
        }
        status.textContent = "Článek je zkopírovaný do schránky.";
      } catch {
        status.textContent = "Kopírování není v tomto prohlížeči dostupné.";
      }
    });
  }

  async function loadArticles() {
    if (articles.length) return articles;
    if (!articleLoadPromise) {
      articleLoadPromise = Promise.all(allArticles().map(async (article) => {
        const response = await fetch(`content/larpidia/${article.category.id}/${article.id}.md`);
        if (!response.ok) throw new Error(`Chybí článek: ${article.category.id}/${article.id}.md`);
        return { ...article, text: await response.text() };
      })).then((loaded) => { articles = loaded; return articles; });
    }
    return articleLoadPromise;
  }

  async function renderRoute() {
    await loadArticles();
    window.scrollTo?.({ top: 0, behavior: "auto" });
    const parts = window.location.hash.replace(/^#encyklopedie\/?/, "").split("/").filter(Boolean);
    if (!parts.length) { renderHub(); return; }
    const category = catalog.categories.find((item) => item.id === parts[0]);
    if (!category) { renderHub(); return; }
    if (parts.length === 1) { renderCategory(category); return; }
    const article = articles.find((item) => item.category.id === category.id && item.id === parts[1]);
    if (article) renderArticle(article);
    else renderCategory(category);
  }

  function renderError(error) {
    app.innerHTML = `<div class="ency-error"><h2>Encyklopedii se nepodařilo načíst</h2><p>${esc(error.message)}</p><p>Obsah se načítá z editovatelných JSON a Markdown souborů, proto web spusťte přes místní webový server (ne přímo jako soubor <code>file://</code>).</p><button class="button button-dark" type="button" onclick="location.reload()">Zkusit znovu</button></div>`;
  }

  function handleLocationHash() {
    const hash = window.location.hash;
    const legacyTarget = legacyRoutes[hash];
    if (legacyTarget) window.history?.replaceState(null, "", legacyTarget);
    if (!window.location.hash.startsWith("#encyklopedie")) return Promise.resolve();
    return renderRoute().catch(renderError);
  }

  async function init() {
    try {
      const legacyTarget = legacyRoutes[window.location.hash];
      if (legacyTarget) window.history?.replaceState(null, "", legacyTarget);
      const [catalogResponse, factsResponse, mediaResponse] = await Promise.all([
        fetch("content/larpidia/index.json"), fetch("content/larpidia/facts.json"), fetch("content/larpidia/media/assets.json"),
      ]);
      if (![catalogResponse, factsResponse, mediaResponse].every((response) => response.ok)) throw new Error("Obsahové soubory se nepodařilo načíst.");
      [catalog, facts, media] = await Promise.all([catalogResponse.json(), factsResponse.json(), mediaResponse.json()]);
      computed = calculateFacts();
      fillSharedFacts();
      window.addEventListener("hashchange", handleLocationHash);
      document.addEventListener("keydown", (event) => {
        if (event.key === "/" && !["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName)) {
          event.preventDefault();
          app.querySelector("[data-ency-search]")?.focus();
        }
      });
      if (window.location.hash.startsWith("#encyklopedie") || legacyRoutes[window.location.hash]) await renderRoute();
    } catch (error) {
      renderError(error);
    }
  }

  init();
})();
