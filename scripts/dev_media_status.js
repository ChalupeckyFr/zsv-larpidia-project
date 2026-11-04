(() => {
  const openButton = document.querySelector("[data-media-status-open]");
  const dialog = document.getElementById("media-status-dialog");
  if (!openButton || !dialog) return;

  const closeButton = dialog.querySelector("[data-media-status-close]");
  const photoCount = dialog.querySelector("[data-media-photo-count]");
  const missingCount = dialog.querySelector("[data-media-missing-count]");
  const availableList = dialog.querySelector("[data-media-available]");
  const missingList = dialog.querySelector("[data-media-missing]");
  const scriptUrl = document.currentScript?.src;
  const manifestUrl = scriptUrl && new URL("../content/larpidia/media/assets.json", scriptUrl);
  let previousFocus = null;
  let loaded = false;

  const exists = async (relativePath) => {
    if (!relativePath) return false;
    try {
      const response = await fetch(new URL(relativePath, document.baseURI), { method: "HEAD" });
      return response.ok;
    } catch {
      return false;
    }
  };

  const fillList = (list, items, labelOf) => {
    list.replaceChildren();
    items.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = labelOf(item);
      list.appendChild(li);
    });
  };

  const loadStatus = async () => {
    if (loaded) return;
    if (!manifestUrl) throw new Error("Manifest médií není dostupný.");
    const response = await fetch(manifestUrl);
    if (!response.ok) throw new Error("Manifest médií není dostupný.");
    const manifest = await response.json();
    const galleryAssets = (manifest.assets || []).filter((asset) => asset.public && asset.gallery);
    const availableAssets = [];
    for (const asset of galleryAssets) {
      if (await exists(asset.src)) availableAssets.push(asset);
    }

    const scenes = manifest.scenes || [];
    const resolvedScenes = await Promise.all(scenes.map(async (scene) => ({
      scene,
      available: scene.photo_path ? await exists(scene.photo_path) : false,
    })));
    const availablePhotos = resolvedScenes.filter(({ scene, available }) => {
      const asset = galleryAssets.find((item) => item.id === scene.asset_id);
      return available && asset?.mediaType === "photo";
    });
    const missingScenes = resolvedScenes.filter(({ available }) => !available);

    photoCount.textContent = String(availablePhotos.length);
    missingCount.textContent = String(missingScenes.length);
    fillList(availableList, availableAssets, (asset) => `${asset.galleryTitle || asset.id}${asset.sceneId ? ` · ${asset.sceneId}` : ""}`);
    fillList(missingList, missingScenes, ({ scene }) => `${scene.title_cs} · ${scene.scene_id}`);
    loaded = true;
  };

  openButton.addEventListener("click", async () => {
    previousFocus = openButton;
    try {
      await loadStatus();
    } catch {
      photoCount.textContent = "—";
      missingCount.textContent = "—";
      fillList(availableList, [{ label: "Údaje se nepodařilo načíst." }], (item) => item.label);
      fillList(missingList, [], () => "");
    }
    dialog.showModal();
    closeButton.focus();
  });
  closeButton.addEventListener("click", () => dialog.close());
  dialog.addEventListener("close", () => previousFocus?.focus());
})();
