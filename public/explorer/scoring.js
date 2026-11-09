(function (root) {
  "use strict";
  function scoreRound(guess, target, skipped = false) {
    if (skipped) return { distanceMeters: null, points: 0, perfect: false };
    if (![guess?.x, guess?.y, target?.x, target?.y].every(Number.isFinite)) {
      throw new TypeError("Souřadnice tipu a cíle musí být konečná čísla.");
    }
    const dx = guess.x - target.x;
    const dy = guess.y - target.y;
    const distanceMeters = Math.hypot(dx, dy);
    const perfect = Math.abs(dx) <= 1.5 && Math.abs(dy) <= 1.5;
    const points = perfect ? 5000 : distanceMeters >= 15000 ? 0 : Math.max(0, Math.min(5000, Math.round(5000 * (1 - distanceMeters / 15000) ** 2)));
    return { distanceMeters, points, perfect };
  }
  function totalScore(rounds) {
    return Math.max(0, Math.min(20000, rounds.reduce((sum, round) => sum + (Number.isInteger(round?.points) ? round.points : 0), 0)));
  }
  const api = Object.freeze({ scoreRound, totalScore });
  root.LarpidiaScoring = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof globalThis !== "undefined" ? globalThis : window);
