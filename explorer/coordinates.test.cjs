const assert = require("node:assert/strict");
const { toSvg } = require("./coordinates.js");

for (const [xKm, yKm, expectedX, expectedY] of [
  [9.61, 5.79, 9810, 6790],
  [12.18, 10.65, 12380, 11650],
  [16.8, 7.84, 17000, 8840],
  [26.108, 16.307, 26308, 17307],
]) {
  const actual = toSvg(xKm, yKm);
  assert.ok(Math.abs(actual.x - expectedX) < 1e-8);
  assert.ok(Math.abs(actual.y - expectedY) < 1e-8);
}
assert.throws(() => toSvg(Number.NaN, 0), TypeError);
assert.throws(() => toSvg(0, Number.POSITIVE_INFINITY), TypeError);
console.log("Atlasové cíle se správně převádějí do SVG souřadnic.");
