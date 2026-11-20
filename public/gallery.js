(() => {
  const grid = document.querySelector("[data-gallery-grid]");
  if (!grid) return;

  const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[char]);

  const removeUnavailable = (figure) => figure.remove();
  const addCard = (asset) => {
    if (!asset?.src || !asset.title || !asset.alt || !asset.caption) return;
    const imageUrl = new URL(asset.src, document.baseURI);
    if (imageUrl.origin !== window.location.origin) return;

    const figure = document.createElement("figure");
    figure.dataset.assetId = asset.id;
    figure.innerHTML = `<button class="gallery-image-button" type="button" aria-label="Zvětšit fotografii: ${escapeHtml(asset.title)}"><img src="${escapeHtml(imageUrl.href)}" alt="${escapeHtml(asset.alt)}" width="1200" height="900" decoding="async"></button><figcaption><strong>${escapeHtml(asset.title)}</strong><span>${escapeHtml(asset.caption)}</span></figcaption>`;
    const image = figure.querySelector("img");
    image.addEventListener("error", () => removeUnavailable(figure), { once: true });
    image.addEventListener("load", () => {
      if (!image.naturalWidth) removeUnavailable(figure);
    }, { once: true });
    figure.querySelector(".gallery-image-button").addEventListener("click", () => {
      const dialog = document.querySelector(".map-dialog");
      if (!dialog || typeof dialog.showModal !== "function") {
        window.open(imageUrl.href, "_blank", "noopener");
        return;
      }
      const dialogImage = dialog.querySelector("img");
      const title = document.getElementById("dialog-map-title");
      const original = dialog.querySelector(".dialog-original");
      title.textContent = asset.title;
      dialogImage.src = imageUrl.href;
      dialogImage.alt = asset.alt;
      dialog.setAttribute("aria-label", "Zvětšená fotografie");
      original.href = imageUrl.href;
      original.textContent = "Otevřít fotografii v plné velikosti ↗";
      dialog.querySelector(".dialog-close").setAttribute("aria-label", "Zavřít fotografii");
      dialog.showModal();
    });
    grid.appendChild(figure);
  };

  const loadGallery = async () => {
    const manifestUrl = new URL(grid.dataset.galleryManifestSrc || "content/larpidia/media/assets.json", document.baseURI);
    manifestUrl.searchParams.set("v", "20261120-2");
    const response = await fetch(manifestUrl, { cache: "no-store" });
    if (!response.ok) throw new Error(`Galerie HTTP ${response.status}`);
    const manifest = await response.json();
    const assets = grid.dataset.galleryMode === "public"
      ? manifest.assets
      : (manifest.assets || []).filter((asset) => asset.public === true && asset.gallery === true && asset.exists === true)
        .map((asset) => ({ ...asset, title: asset.galleryTitle || asset.title || asset.id }));
    grid.replaceChildren();
    assets.forEach(addCard);
    if (!grid.querySelector("figure")) {
      const message = document.createElement("p");
      message.className = "gallery-loading";
      message.textContent = "Galerie nyní neobsahuje žádné dostupné obrazy.";
      grid.appendChild(message);
    }
  };

  loadGallery().catch(() => {
    grid.replaceChildren();
    const message = document.createElement("p");
    message.className = "gallery-loading";
    message.textContent = "Obrazovou galerii se nepodařilo načíst.";
    grid.appendChild(message);
  });
})();
