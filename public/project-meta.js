(() => {
  const scriptUrl = document.currentScript?.src;
  if (!scriptUrl) return;
  fetch(new URL("project-metadata.json", scriptUrl))
    .then((response) => {
      if (!response.ok) throw new Error("Project metadata unavailable");
      return response.json();
    })
    .then((meta) => {
      const pieces = [
        meta.webVersion && `Web v${meta.webVersion}`,
        meta.atlasVersion && `Atlas v${meta.atlasVersion}`,
        meta.capitalPlanVersion && `Plán Larpingtonu v${meta.capitalPlanVersion}`,
        "3D model",
      ].filter(Boolean);
      document.querySelectorAll("[data-project-footer]").forEach((element) => {
        element.textContent = `© Larpidie · ${pieces.join(" · ")}`;
      });
    })
    .catch(() => {
      document.querySelectorAll("[data-project-footer]").forEach((element) => {
        element.textContent = "© Larpidie · Fiktivní studentský projekt";
      });
    });
})();
