import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const config = JSON.parse(fs.readFileSync(path.join(root, "explorer/rounds.json"), "utf8"));
const places = JSON.parse(fs.readFileSync(path.join(root, "atlas/current/registry/places.public.json"), "utf8"));
const atlas = fs.readFileSync(path.join(root, "atlas/current/viewer/atlas.html"), "utf8");
assert.equal(config.schemaVersion, 1, "Nepodporované schemaVersion konfigurace.");
assert.ok(["demo", "production"].includes(config.mode), "Neplatný režim konfigurace.");
assert.equal(config.rounds.length, 4, "Hra musí mít přesně čtyři kola.");
assert.equal(places.objects.length, 159, "Veřejný atlas musí mít 159 míst.");
const byId = new Map(places.objects.map((place) => [place.id, place]));
const targets = new Set();
for (const [index, round] of config.rounds.entries()) {
  assert.equal(round.publicNumber, index + 1, `Neplatné veřejné číslo kola ${index + 1}.`);
  assert.ok(round.id && !targets.has(round.targetPlaceId), `Chybné nebo duplicitní ID cíle v kole ${index + 1}.`);
  targets.add(round.targetPlaceId);
  const place = byId.get(round.targetPlaceId);
  assert.ok(place, `Cíl ${round.targetPlaceId} v kole ${index + 1} chybí ve veřejném registru.`);
  assert.ok(Number.isFinite(place.x_km) && Number.isFinite(place.y_km), `Místo ${place.id} nemá platné atlasové souřadnice.`);
  const svgX = place.x_km * 1000;
  const svgY = place.y_km * 1000;
  assert.ok(svgX >= 0 && svgX <= 29700 && svgY >= 0 && svgY <= 21000, `Místo ${place.id} je mimo mapové viewBox.`);
  assert.ok(atlas.includes(`data-id="${place.id}"`), `Geometrie místa ${place.id} není součástí kanonického atlasu.`);
  console.log(`Kolo ${index + 1}: ${place.id} · ${place.name_cs} · SVG (${svgX}, ${svgY}) = atlasové metry.`);
}
for (const id of ["T-01", "SP-01", "PL-01"]) assert.ok(byId.has(id) && atlas.includes(`data-id="${id}"`), `Chybí kontrolní místo ${id}.`);
console.log("Konfigurace, všechny cíle a mapové souřadnice jsou platné.");
