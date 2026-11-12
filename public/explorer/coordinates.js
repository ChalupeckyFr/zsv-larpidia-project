(() => {
  "use strict";
  const ORIGIN_X_KM = -0.2;
  const ORIGIN_Y_KM = -1.0;
  const KM_TO_METERS = 1000;

  function toSvg(xKm, yKm) {
    if (!Number.isFinite(xKm) || !Number.isFinite(yKm)) {
      throw new TypeError("Atlasové souřadnice musí být konečná čísla.");
    }
    return {
      x: (xKm - ORIGIN_X_KM) * KM_TO_METERS,
      y: (yKm - ORIGIN_Y_KM) * KM_TO_METERS,
    };
  }

  const api = Object.freeze({ toSvg });
  globalThis.LarpidiaExplorerCoordinates = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})();
