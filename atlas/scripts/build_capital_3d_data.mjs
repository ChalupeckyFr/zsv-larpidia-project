import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const capital = path.join(root, 'atlas/current/capital');
const output = path.join(capital, 'capital-3d-data.js');
const read = (name) => JSON.parse(fs.readFileSync(path.join(capital, name), 'utf8'));
const ring = (feature) => {
  const geometry = feature.geometry;
  if (!geometry || geometry.type !== 'Polygon') return null;
  const coordinates = geometry.coordinates[0];
  const open = coordinates.length > 3 && coordinates[0][0] === coordinates.at(-1)[0] && coordinates[0][1] === coordinates.at(-1)[1]
    ? coordinates.slice(0, -1) : coordinates;
  return open.map(([x, y]) => [Math.round(x * 10) / 10, Math.round(y * 10) / 10]);
};
const line = (feature) => {
  const geometry = feature.geometry;
  if (!geometry) return [];
  if (geometry.type === 'LineString') return [geometry.coordinates];
  if (geometry.type === 'MultiLineString') return geometry.coordinates;
  return [];
};
const pointInPolygon = (x, y, polygon) => {
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const [xi, yi] = polygon[i];
    const [xj, yj] = polygon[j];
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
};
const boxOf = (polygon) => polygon.reduce((box, [x, y]) => ({
  minX: Math.min(box.minX, x), minY: Math.min(box.minY, y),
  maxX: Math.max(box.maxX, x), maxY: Math.max(box.maxY, y),
}), { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity });

const blockFeatures = read('cp_blocks.geojson').features;
const houseFeatures = read('cp_houses.geojson').features;
const usedCells = new Map();
const cellSize = 100;
const cellKey = (x, y) => `${x},${y}`;
const addUsedBox = (box) => {
  for (let y = Math.floor(box.minY / cellSize); y <= Math.floor(box.maxY / cellSize); y++) {
    for (let x = Math.floor(box.minX / cellSize); x <= Math.floor(box.maxX / cellSize); x++) {
      const key = cellKey(x, y);
      if (!usedCells.has(key)) usedCells.set(key, []);
      usedCells.get(key).push(box);
    }
  }
};
for (const feature of houseFeatures) {
  const polygon = ring(feature);
  if (!polygon) continue;
  const box = boxOf(polygon);
  addUsedBox(box);
}

const futureColors = Object.fromEntries(['residential_low', 'residential_mid', 'old_town_mixed', 'promenade_retail', 'retail_main', 'transit_mixed', 'new_waterfront'].map((use) => [use, '#b87558']));
const futureTargets = {
  residential_low: 2, residential_mid: 6, old_town_mixed: 7, promenade_retail: 5,
  retail_main: 5, transit_mixed: 6, new_waterfront: 4,
};
const future = [];
for (const feature of blockFeatures) {
  const props = feature.properties;
  if (!['reserve', 'partial'].includes(props.build_state)) continue;
  const polygon = ring(feature);
  if (!polygon) continue;
  const box = boxOf(polygon), use = props.land_use || 'residential_mid';
  const target = props.build_state === 'partial' ? 2 : (futureTargets[use] || 3);
  const count = Math.max(0, target - Number(props.houses || 0));
  if (!count || box.maxX - box.minX < 16 || box.maxY - box.minY < 14) continue;
  const cols = Math.max(1, Math.ceil(Math.sqrt(target * (box.maxX - box.minX) / (box.maxY - box.minY))));
  const rows = Math.max(1, Math.ceil(target / cols));
  const width = Math.min(13, (box.maxX - box.minX) / (cols + 1) * 0.46);
  const depth = Math.min(9, (box.maxY - box.minY) / (rows + 1) * 0.46);
  const seed = [...props.id].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 11);
  let placed = 0;
  for (let n = 0; n < cols * rows && placed < count; n++) {
    const slot = (n + seed) % (cols * rows), col = slot % cols, row = Math.floor(slot / cols);
    const cx = box.minX + (col + 1) * (box.maxX - box.minX) / (cols + 1);
    const cy = box.minY + (row + 1) * (box.maxY - box.minY) / (rows + 1);
    const points = [[cx - width / 2, cy - depth / 2], [cx + width / 2, cy - depth / 2],
      [cx + width / 2, cy + depth / 2], [cx - width / 2, cy + depth / 2]];
    if (!points.every(([x, y]) => pointInPolygon(x, y, polygon))) continue;
    const candidate = boxOf(points);
    let overlaps = false;
    for (let y = Math.floor(candidate.minY / cellSize); y <= Math.floor(candidate.maxY / cellSize) && !overlaps; y++) {
      for (let x = Math.floor(candidate.minX / cellSize); x <= Math.floor(candidate.maxX / cellSize) && !overlaps; x++) {
        for (const old of usedCells.get(cellKey(x, y)) || []) {
          if (!(candidate.maxX < old.minX || candidate.minX > old.maxX || candidate.maxY < old.minY || candidate.minY > old.maxY)) {
            overlaps = true; break;
          }
        }
      }
    }
    if (overlaps) continue;
    const height = use === 'new_waterfront' ? 14 : ['old_town_mixed', 'promenade_retail', 'retail_main'].includes(use) ? 9 : 6;
    future.push({ id: `${props.id}-F${placed + 1}`, block: props.id, use, points, height, color: futureColors[use] || '#b88368' });
    addUsedBox(candidate);
    placed++;
  }
}

const data = {
  blocks: blockFeatures.flatMap((f) => { const p = ring(f); return p ? [{ id: f.properties.id, use: f.properties.land_use, state: f.properties.build_state, points: p }] : []; }),
  houses: houseFeatures.flatMap((f) => { const p = ring(f); return p ? [{ id: f.properties.id, use: f.properties.subtype || 'residential_mid', kind: f.properties.kind || 'core', points: p, height: Number(f.properties.height_m || 4), floors: Number(f.properties.floors || 1), style: f.properties.architectural_style || 'residential', color: f.properties.roof_color || '#b87558' }] : []; }),
  future,
  buildings: read('cp_buildings.geojson').features.flatMap((f) => {
    const p = ring(f); return p ? [{ id: f.properties.id, subtype: f.properties.subtype, name: f.properties.name_en || f.properties.name_cs, points: p }] : [];
  }),
  streets: read('cp_streets.geojson').features.flatMap((f) => line(f).map((points) => ({
    width: Number(f.properties.row_m || 10), state: f.properties.state || 'built', cls: f.properties.cls || 'C',
    points: points.map(([x, y]) => [Math.round(x * 10) / 10, Math.round(y * 10) / 10]),
  }))),
  parks: read('cp_spaces.geojson').features.flatMap((f) => {
    const p = ring(f); return p ? [{ id: f.properties.id, points: p, type: f.properties.subtype || f.properties.type }] : [];
  }),
};
fs.writeFileSync(output, `/* Generated from cp_*.geojson by build_capital_3d_data.mjs. */\nwindow.LARPIDIA_CAPITAL_3D = ${JSON.stringify(data)};\n`, 'utf8');
console.log(`Wrote ${path.relative(root, output)} · ${data.houses.length} homes, ${data.future.length} future buildings.`);
