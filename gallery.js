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
    figure.innerHTML = `<img src="${escapeHtml(imageUrl.href)}" alt="${escapeHtml(asset.alt)}" width="1200" height="900" decoding="async"><figcaption><strong>${escapeHtml(asset.title)}</strong><span>${escapeHtml(asset.caption)}</span></figcaption>`;
    const image = figure.querySelector("img");
    image.addEventListener("error", () => removeUnavailable(figure), { once: true });
    image.addEventListener("load", () => {
      if (!image.naturalWidth) removeUnavailable(figure);
    }, { once: true });
    grid.appendChild(figure);
  };

  const loadGallery = async () => {
    const manifestUrl = new URL(grid.dataset.galleryManifestSrc || "content/larpidia/media/assets.json", document.baseURI);
    const response = await fetch(manifestUrl);
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
