import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const current = path.join(root, "atlas/current");
const readJson = (file) => JSON.parse(fs.readFileSync(file, "utf8"));
const terrainSource = fs.readFileSync(path.join(current, "viewer/terrain-3d-data.js"), "utf8");
const terrain = JSON.parse(terrainSource.slice(terrainSource.indexOf("=") + 1, terrainSource.lastIndexOf(";")));
const helperContext = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(current, "viewer/atlas-to-world.js"), "utf8"), helperContext);
const world = helperContext.window.LARPIDIA_ATLAS_WORLD;
const mainRegistry = readJson(path.join(current, "registry/places.json"));
const cityRegistry = readJson(path.join(current, "capital/cp_objects.json"));
const packed = Buffer.from(terrain.packed, "base64");
const gridHeight = (row, col) => {
  const index = row * terrain.width + col;
  return ((packed[index * 3] << 8) | packed[index * 3 + 1]) * terrain.max_elevation_m / 65535;
};
const gridCover = (row, col) => packed[(row * terrain.width + col) * 3 + 2];
const gridPoint = (x, y) => ({
  col: Math.round((x - terrain.origin_xy_km[0]) / (terrain.sample_m / 1000)),
  row: Math.round((y - terrain.origin_xy_km[1]) / (terrain.sample_m / 1000)),
});
const nearestHeight = (x, y) => {
  const { row, col } = gridPoint(x, y);
  return gridHeight(row, col);
};
const round3 = (point) => point.map((value) => Number(Number(value).toFixed(3)));

function sourcePaths(file, rail = false) {
  const collection = readJson(file), paths = [];
  for (const feature of collection.features || []) {
    const props = feature.properties || {}, geometry = feature.geometry || {};
    const lines = geometry.type === "LineString" ? [geometry.coordinates]
      : geometry.type === "MultiLineString" ? geometry.coordinates : [];
    for (const [part, points] of lines.entries()) {
      if (points.length < 2) continue;
      paths.push(rail ? {
        id: String(props.id || `${props.line || "rail"}-${part + 1}`),
        line: String(props.line || ""), name: String(props.name_cs || props.line || "Railway"),
        section: String(props.section || "surface"), length_m: Number(props.length_m || 0), points: points.map(round3),
      } : {
        id: String(props.id || `road-${part + 1}`), class: String(props.class || "R3"),
        section: String(props.section || "surface"), name: String(props.name_cs || props.id || "Road"),
        length_m: Number(props.length_m || 0), points: points.map(round3),
      });
    }
  }
  return paths;
}

function coastSegments() {
  const features = readJson(path.join(current, "relief/coast_classes.geojson")).features;
  const segments = [];
  for (const feature of features) {
    const geometry = feature.geometry || {};
    const lines = geometry.type === "LineString" ? [geometry.coordinates]
      : geometry.type === "MultiLineString" ? geometry.coordinates
        : geometry.type === "Polygon" ? geometry.coordinates : [];
    for (const line of lines) for (let i = 0; i < line.length - 1; i++) {
      segments.push({ kind: feature.properties?.class || "unknown", a: line[i], b: line[i + 1] });
    }
  }
  return segments;
}

function distanceToSegment(point, a, b) {
  const dx = b[0] - a[0], dy = b[1] - a[1], length2 = dx * dx + dy * dy;
  const t = length2 ? Math.max(0, Math.min(1, ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / length2)) : 0;
  return Math.hypot(point[0] - a[0] - dx * t, point[1] - a[1] - dy * t);
}

assert.equal(terrain.sample_m, 40, "DEM mesh spacing must remain 40 m.");
assert.equal(terrain.height_encoding, "u16be-normalized-to-max-elevation");
assert.equal(packed.length, terrain.width * terrain.height * 3);
assert.equal(terrain.max_elevation_m, 560);
assert.deepEqual(Array.from(terrain.origin_xy_km), [-0.2, -1]);
assert.equal(world.toWorld(14.65, 9.5)[0], 0);
assert.equal(world.toWorld(14.65, 9.5)[1], 0);
assert.deepEqual(Array.from(world.toAtlas(...world.toWorld(6.96, 5.44))), [6.96, 5.44]);
assert.ok(world.toWorld(15.65, 9.5)[0] > world.toWorld(14.65, 9.5)[0], "East must increase +X.");
assert.ok(world.toWorld(14.65, 8.5)[1] < world.toWorld(14.65, 9.5)[1], "North must point toward -Z.");
const gridOrigin = world.gridToWorld(0, 0, terrain);
const nextCell = world.gridToWorld(1, 0, terrain);
assert.ok(Math.abs(nextCell[0] - gridOrigin[0] - 0.04) < 1e-12, "One DEM cell must equal 40 m in world space.");

const places = new Map(mainRegistry.objects.map((place) => [place.id, place]));
const heightChecks = [["M-01", 560, 0.05], ["M-02", 510, 1], ["M-03", 440, 1], ["C-01", 18.2, 1]];
for (const [id, expected, tolerance] of heightChecks) {
  const point = places.get(id);
  assert.ok(point && Number.isFinite(point.x_km) && Number.isFinite(point.y_km), `${id} must exist in the canonical registry.`);
  assert.ok(Math.abs(nearestHeight(point.x_km, point.y_km) - expected) <= tolerance, `${id} terrain elevation must match its canonical control.`);
  const [x, z] = world.toWorld(point.x_km, point.y_km);
  const roundTrip = world.toAtlas(x, z);
  assert.ok(Math.abs(roundTrip[0] - point.x_km) < 1e-9 && Math.abs(roundTrip[1] - point.y_km) < 1e-9,
    `${id} must map back to its atlas location.`);
}
const lake = terrain.water_features.find((feature) => feature.id === "W-lake-N04");
assert.equal(lake?.level_m, 67.6, "The reservoir surface must use its canonical model level.");
assert.equal(gridHeight(0, 0), 0, "The outer sea grid must remain at sea level.");
assert.equal(cityRegistry.objects.length, 662, "All city objects must be retained.");
assert.deepEqual(cityRegistry.objects.filter((item) => /^C-0[3-6]$/.test(item.id)).map((item) => item.name_cs), [
  "Chalupecká čtvrť", "Kynčlova čtvrť", "Klimečkova čtvrť", "Žemličkova čtvrť",
]);

const sourceRoads = sourcePaths(path.join(current, "human/roads.geojson"));
const sourceRailways = sourcePaths(path.join(current, "human/rail_lines.geojson"), true);
assert.deepEqual(terrain.roads, sourceRoads, "Every 3D road point must come from the existing road GeoJSON.");
assert.deepEqual(terrain.railways, sourceRailways, "Every 3D rail point must come from the existing rail GeoJSON.");
for (const feature of [...terrain.roads, ...terrain.railways]) for (const [x, y] of feature.points) {
  const [worldX, worldZ] = world.toWorld(x, y);
  const roundTrip = world.toAtlas(worldX, worldZ);
  assert.ok(Math.abs(roundTrip[0] - x) < 1e-9 && Math.abs(roundTrip[1] - y) < 1e-9,
    `${feature.id} route coordinates must round-trip unchanged.`);
}
assert.equal(terrain.roads.length, 62);
assert.equal(terrain.railways.length, 26);
assert.equal(terrain.roads.filter((feature) => !["tunnel", "cave", "undersea"].includes(feature.section)).length, 59);
assert.equal(terrain.railways.filter((feature) => !["tunnel", "cave", "undersea"].includes(feature.section)).length, 17);

const coast = coastSegments();
let maxUnsupportedShoreJump = 0, maxExplicitCliffJump = 0, maxExplicitRockyJump = 0;
for (let row = 0; row < terrain.height; row++) for (let col = 0; col < terrain.width; col++) {
  for (const [dr, dc] of [[1, 0], [0, 1]]) {
    const nextRow = row + dr, nextCol = col + dc;
    if (nextRow >= terrain.height || nextCol >= terrain.width || (gridCover(row, col) === 0) === (gridCover(nextRow, nextCol) === 0)) continue;
    const jump = Math.abs(gridHeight(row, col) - gridHeight(nextRow, nextCol));
    const point = [terrain.origin_xy_km[0] + (col + dc / 2) * terrain.sample_m / 1000,
      terrain.origin_xy_km[1] + (row + dr / 2) * terrain.sample_m / 1000];
    let nearest = { kind: "unknown", distance: Infinity };
    for (const segment of coast) {
      const distance = distanceToSegment(point, segment.a, segment.b);
      if (distance < nearest.distance) nearest = { kind: segment.kind, distance };
    }
    if (nearest.distance <= 0.12 && nearest.kind === "cliff") maxExplicitCliffJump = Math.max(maxExplicitCliffJump, jump);
    else if (nearest.distance <= 0.12 && nearest.kind === "rocky") maxExplicitRockyJump = Math.max(maxExplicitRockyJump, jump);
    else maxUnsupportedShoreJump = Math.max(maxUnsupportedShoreJump, jump);
  }
}
assert.ok(maxExplicitCliffJump > 200, "The known northwest cliff relief must remain intact.");
assert.ok(maxExplicitRockyJump > 150, "The mapped rocky cape relief must remain intact.");
assert.ok(maxUnsupportedShoreJump < 50, `Unclassified shore steps must remain gentle; saw ${maxUnsupportedShoreJump.toFixed(1)} m.`);

for (const file of ["viewer/terrain-3d.html", "capital/capital-3d.html"]) {
  const html = fs.readFileSync(path.join(current, file), "utf8");
  assert.doesNotMatch(html, /id=["'](?:exaggeration|exag-value)["']/i, `${file} must not expose terrain exaggeration.`);
}
assert.match(fs.readFileSync(path.join(current, "viewer/terrain-3d.html"), "utf8"), /vertical=1\/1000/,
  "Terrain elevations must convert metres to kilometre world units once.");

console.log(`PASS shared transform: +X east, north=-Z; 40 m = 0.04 km.`);
console.log(`PASS controls: M-01 560 m, M-02 ${nearestHeight(places.get("M-02").x_km, places.get("M-02").y_km).toFixed(1)} m, M-03 440 m, Larpington ${nearestHeight(places.get("C-01").x_km, places.get("C-01").y_km).toFixed(1)} m; lake ${lake.level_m} m.`);
console.log(`PASS source-aligned routes: ${terrain.roads.length} road fragments (${terrain.roads.length - 59} tunnels hidden), ${terrain.railways.length} rail fragments (${terrain.railways.length - 17} underground/undersea hidden).`);
console.log(`PASS coast: explicit cliff ${maxExplicitCliffJump.toFixed(1)} m and rocky ${maxExplicitRockyJump.toFixed(1)} m retained; unclassified maximum ${maxUnsupportedShoreJump.toFixed(1)} m.`);
