(() => {
  const scriptUrl = document.currentScript?.src;
  if (!scriptUrl) return;
  const logoUrl = new URL("Larpidie logo.png", scriptUrl).href;

  const applyLogo = (image) => {
    image.src = logoUrl;
    image.alt = "Larpidie";
    image.width = 48;
    image.height = 48;
    image.classList.add("site-brand-logo");
    image.removeAttribute("aria-hidden");
  };

  document.querySelectorAll("img.logo, img.logo--footer").forEach(applyLogo);
  document.querySelectorAll("span.brand-mark").forEach((mark) => {
    const image = document.createElement("img");
    applyLogo(image);
    image.classList.add("logo--footer");
    mark.replaceWith(image);
  });

  if (window.self !== window.top) return;
  const homeUrl = new URL("index.html#domu", scriptUrl).href;
  const makeBrandLink = (className) => {
    const link = document.createElement("a");
    link.className = className;
    link.href = homeUrl;
    link.setAttribute("aria-label", "Larpidie — úvodní stránka");
    const image = document.createElement("img");
    applyLogo(image);
    link.appendChild(image);
    return link;
  };

  const header = document.querySelector("header");
  if (header && !header.querySelector(".site-brand-logo")) {
    header.prepend(makeBrandLink("site-brand-home"));
  }

  document.querySelectorAll("footer").forEach((footer) => {
    if (!footer.querySelector(".site-brand-logo")) {
      footer.prepend(makeBrandLink("site-brand-footer"));
    }
  });
})();
