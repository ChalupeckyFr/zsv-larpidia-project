import fs from "node:fs";
import path from "node:path";
import zlib from "node:zlib";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const current = path.join(root, "atlas/current");
const relief = path.join(current, "relief");
// Bilinear 30 m sampling keeps the short ridges and coastal folds much clearer
// than the old 40 m mesh while keeping the interactive tile count modest.
const every = 1.5;

function readPng(file) {
  const bytes = fs.readFileSync(file);
  let offset = 8, header, palette, compressed = [];
  while (offset + 12 <= bytes.length) {
    const length = bytes.readUInt32BE(offset), type = bytes.toString("ascii", offset + 4, offset + 8);
    const data = bytes.subarray(offset + 8, offset + 8 + length);
    if (type === "IHDR") header = { width: data.readUInt32BE(0), height: data.readUInt32BE(4), depth: data[8], colorType: data[9], interlace: data[12] };
    if (type === "PLTE") palette = data;
    if (type === "IDAT") compressed.push(data);
    offset += length + 12;
    if (type === "IEND") break;
  }
  if (!header || header.interlace !== 0) throw new Error(`Unsupported PNG layout: ${file}`);
  const channels = ({ 0: 1, 2: 3, 3: 1, 4: 2, 6: 4 })[header.colorType];
  const bpp = channels * header.depth / 8, rowBytes = header.width * bpp;
  const source = zlib.inflateSync(Buffer.concat(compressed));
  if (source.length !== header.height * (rowBytes + 1)) throw new Error(`Invalid PNG scanlines: ${file}`);
  const pixels = new Uint8Array(header.height * rowBytes);
  let input = 0;
  for (let y = 0; y < header.height; y++) {
    const filter = source[input++], start = y * rowBytes;
    for (let x = 0; x < rowBytes; x++) {
      const raw = source[input++], a = x >= bpp ? pixels[start + x - bpp] : 0;
      const up = y ? pixels[start - rowBytes + x] : 0;
      const upperLeft = y && x >= bpp ? pixels[start - rowBytes + x - bpp] : 0;
      let predictor = 0;
      if (filter === 1) predictor = a;
      else if (filter === 2) predictor = up;
      else if (filter === 3) predictor = Math.floor((a + up) / 2);
      else if (filter === 4) {
        const p = a + up - upperLeft, pa = Math.abs(p - a), pb = Math.abs(p - up), pc = Math.abs(p - upperLeft);
        predictor = pa <= pb && pa <= pc ? a : pb <= pc ? up : upperLeft;
      } else if (filter !== 0) throw new Error(`Unsupported PNG filter ${filter}`);
      pixels[start + x] = (raw + predictor) & 255;
    }
  }
  return { ...header, pixels, palette };
}

const evenRound = (value) => {
  const floor = Math.floor(value), fraction = value - floor;
  return fraction < 0.5 ? floor : fraction > 0.5 ? floor + 1 : floor % 2 === 0 ? floor : floor + 1;
};
const distanceToSegment = (x, y, a, b) => {
  const dx = b[0] - a[0], dy = b[1] - a[1], denom = dx * dx + dy * dy;
  const t = denom ? Math.max(0, Math.min(1, ((x - a[0]) * dx + (y - a[1]) * dy) / denom)) : 0;
  return [Math.hypot(x - a[0] - dx * t, y - a[1] - dy * t), t];
};
function insidePolygon(x, y, polygon) {
  let inside = false, previous = polygon.at(-1);
  for (const current of polygon) {
    if ((current[1] > y) !== (previous[1] > y)) {
      const crossing = (previous[0] - current[0]) * (y - current[1]) / (previous[1] - current[1]) + current[0];
      if (x < crossing) inside = !inside;
    }
    previous = current;
  }
  return inside;
}
const round3 = (point) => point.map((value) => Number(Number(value).toFixed(3)));
function transportPaths(file, rail = false) {
  const collection = JSON.parse(fs.readFileSync(file, "utf8")), out = [];
  for (const feature of collection.features || []) {
    const props = feature.properties || {}, geometry = feature.geometry || {};
    const lines = geometry.type === "LineString" ? [geometry.coordinates] : geometry.type === "MultiLineString" ? geometry.coordinates : [];
    for (const [part, points] of lines.entries()) {
      if (points.length < 2) continue;
      out.push(rail ? {
        id: String(props.id || `${props.line || "rail"}-${part + 1}`), line: String(props.line || ""),
        name: String(props.name_cs || props.line || "Railway"), section: String(props.section || "surface"),
        length_m: Number(props.length_m || 0), points: points.map(round3),
      } : {
        id: String(props.id || `road-${part + 1}`), class: String(props.class || "R3"),
        section: String(props.section || "surface"), name: String(props.name_cs || props.id || "Road"),
        length_m: Number(props.length_m || 0), points: points.map(round3),
      });
    }
  }
  return out;
}

const meta = JSON.parse(fs.readFileSync(path.join(relief, "dem_meta.json"), "utf8"));
const origin = meta.origin_xy_km.map(Number), cell = Number(meta.cell_km), maxElevation = Number(meta.max_m);
const dem = readPng(path.join(relief, "dem_20m_u16.png")), landcover = readPng(path.join(relief, "landcover_20m.png"));
if (dem.colorType !== 0 || dem.depth !== 16 || landcover.colorType !== 3 || landcover.depth !== 8 || dem.width !== landcover.width || dem.height !== landcover.height) {
  throw new Error("Unexpected DEM or indexed landcover encoding.");
}
const width = Math.ceil(dem.width / every), height = Math.ceil(dem.height / every), sampleM = cell * every * 1000, meshCell = cell * every;
const heights = new Float64Array(width * height), cover = new Uint8Array(width * height);
const sampleElevation = (sourceRowIndex, sourceColIndex) => {
  const pixel = (sourceRowIndex * dem.width + sourceColIndex) * 2;
  return (dem.pixels[pixel] * 256 + dem.pixels[pixel + 1]) / 100;
};
for (let row = 0; row < height; row++) {
  const sourceRow = row * every, row0 = Math.floor(sourceRow), row1 = Math.min(dem.height - 1, row0 + 1), ty = sourceRow - row0;
  for (let col = 0; col < width; col++) {
    const sourceCol = col * every, col0 = Math.floor(sourceCol), col1 = Math.min(dem.width - 1, col0 + 1), tx = sourceCol - col0, index = row * width + col;
    const a = sampleElevation(row0, col0), b = sampleElevation(row0, col1), c = sampleElevation(row1, col0), d = sampleElevation(row1, col1);
    heights[index] = a * (1 - tx) * (1 - ty) + b * tx * (1 - ty) + c * (1 - tx) * ty + d * tx * ty;
    cover[index] = landcover.pixels[Math.round(sourceRow) * dem.width + Math.round(sourceCol)];
  }
}
const gridSample = (values, x, y) => {
  const gx = Math.max(0, Math.min(width - 1, (x - origin[0]) / meshCell));
  const gy = Math.max(0, Math.min(height - 1, (y - origin[1]) / meshCell));
  const col = Math.min(width - 2, Math.floor(gx)), row = Math.min(height - 2, Math.floor(gy));
  const tx = gx - col, ty = gy - row, a = values[row * width + col], b = values[row * width + col + 1];
  const c = values[(row + 1) * width + col], d = values[(row + 1) * width + col + 1];
  return ty <= 1 - tx ? a * (1 - tx - ty) + b * tx + c * ty : b * (1 - ty) + d * (tx + ty - 1) + c * (1 - tx);
};

const hydro = JSON.parse(fs.readFileSync(path.join(relief, "hydrography.geojson"), "utf8"));
for (const feature of hydro.features) {
  const geometry = feature.geometry || {};
  const lines = geometry.type === "LineString" ? [geometry.coordinates] : geometry.type === "MultiLineString" ? geometry.coordinates : [];
  for (const points of lines) for (let i = 0; i < points.length - 1; i++) {
    const a = points[i], b = points[i + 1], distance = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const steps = Math.max(1, Math.ceil(distance / (meshCell * 0.5)));
    for (let step = 0; step <= steps; step++) {
      const t = step / steps, col = evenRound((a[0] + (b[0] - a[0]) * t - origin[0]) / meshCell);
      const row = evenRound((a[1] + (b[1] - a[1]) * t - origin[1]) / meshCell);
      if (row >= 0 && row < height && col >= 0 && col < width) {
        const index = row * width + col;
        if (cover[index] !== 0) cover[index] = 9;
      }
    }
  }
}

const widthByWaterKind = { main: 64, river: 42, stream: 13 };
const waterFeatures = [];
let lakePolygon = null;
for (const feature of hydro.features) {
  const geometry = feature.geometry || {}, props = feature.properties || {};
  if (geometry.type === "Polygon" && props.id === "W-lake-N04") {
    lakePolygon = geometry.coordinates[0].slice(0, -1);
    waterFeatures.push({ id: props.id, kind: "lake", level_m: Number(props.level_m_model || 67.6), points: geometry.coordinates[0] });
  } else if (geometry.type === "LineString" && String(props.id || "").startsWith("W-")) {
    waterFeatures.push({ id: props.id, part: props.part || "all", kind: String(props.kind || "stream"), width_m: widthByWaterKind[props.kind] || 5.5,
      bed_start_m: Number(props.bed_start_m || 0), bed_end_m: Number(props.bed_end_m || 0), points: geometry.coordinates });
  }
}

if (lakePolygon) {
  const level = waterFeatures.find((feature) => feature.kind === "lake").level_m;
  const minX = Math.min(...lakePolygon.map((point) => point[0])) - 0.12, maxX = Math.max(...lakePolygon.map((point) => point[0])) + 0.12;
  const minY = Math.min(...lakePolygon.map((point) => point[1])) - 0.12, maxY = Math.max(...lakePolygon.map((point) => point[1])) + 0.12;
  for (let row = Math.max(0, Math.floor((minY - origin[1]) / meshCell)); row <= Math.min(height - 1, Math.ceil((maxY - origin[1]) / meshCell)); row++) {
    const y = origin[1] + row * meshCell;
    for (let col = Math.max(0, Math.floor((minX - origin[0]) / meshCell)); col <= Math.min(width - 1, Math.ceil((maxX - origin[0]) / meshCell)); col++) {
      const x = origin[0] + col * meshCell;
      let distance = Infinity;
      for (let i = 0; i < lakePolygon.length; i++) distance = Math.min(distance, distanceToSegment(x, y, lakePolygon[i], lakePolygon[(i + 1) % lakePolygon.length])[0]);
      if (insidePolygon(x, y, lakePolygon)) heights[row * width + col] = Math.min(heights[row * width + col], level - Math.min(24, Math.max(2, distance * 1000 * 0.28)));
      else if (distance * 1000 < 120) heights[row * width + col] = Math.min(heights[row * width + col], level + distance * 1000 * 0.27);
    }
  }
}

for (const feature of waterFeatures) {
  if (feature.kind === "lake") continue;
  const points = feature.points, lengths = [0];
  for (let i = 0; i < points.length - 1; i++) lengths.push(lengths.at(-1) + Math.hypot(points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1]));
  const total = lengths.at(-1) || 1, reference = points.map((point, i) => {
    const mapped = feature.bed_start_m + (feature.bed_end_m - feature.bed_start_m) * lengths[i] / total;
    return Math.max(gridSample(heights, ...point) - 20, Math.min(mapped, gridSample(heights, ...point) - 1.5));
  });
  const radius = Math.max(0.022, feature.width_m / 1000 * 1.15), minCol = Math.max(0, Math.floor((Math.min(...points.map((p) => p[0])) - radius - origin[0]) / meshCell));
  const maxCol = Math.min(width - 1, Math.floor((Math.max(...points.map((p) => p[0])) + radius - origin[0]) / meshCell) + 1);
  const minRow = Math.max(0, Math.floor((Math.min(...points.map((p) => p[1])) - radius - origin[1]) / meshCell));
  const maxRow = Math.min(height - 1, Math.floor((Math.max(...points.map((p) => p[1])) + radius - origin[1]) / meshCell) + 1);
  for (let row = minRow; row <= maxRow; row++) {
    const y = origin[1] + row * meshCell;
    for (let col = minCol; col <= maxCol; col++) {
      const x = origin[0] + col * meshCell;
      for (let i = 0; i < points.length - 1; i++) {
        const [distance, t] = distanceToSegment(x, y, points[i], points[i + 1]);
        if (distance > radius) continue;
        const bed = reference[i] + (reference[i + 1] - reference[i]) * t;
        heights[row * width + col] = Math.min(heights[row * width + col], Math.max(0, bed - 3 + distance / radius * 4));
      }
    }
  }
  feature.surface_m = reference.map((bed) => bed + 0.15);
}

function settlementLights(file) {
  const collection = JSON.parse(fs.readFileSync(file, "utf8")), lights = [], seen = new Set(), spacing = 0.075;
  const hashPoint = (x, y) => {
    let value = (Math.round(x * 1000) * 73856093) ^ (Math.round(y * 1000) * 19349663);
    value = Math.imul(value ^ (value >>> 13), 1274126177);
    return (value ^ (value >>> 16)) >>> 0;
  };
  for (const feature of collection.features || []) {
    const geometry = feature.geometry || {}, polygons = geometry.type === "Polygon" ? [geometry.coordinates] : geometry.type === "MultiPolygon" ? geometry.coordinates : [];
    for (const rings of polygons) {
      const outer = rings[0] || [];
      if (outer.length < 4) continue;
      const minX = Math.min(...outer.map((p) => p[0])), maxX = Math.max(...outer.map((p) => p[0]));
      const minY = Math.min(...outer.map((p) => p[1])), maxY = Math.max(...outer.map((p) => p[1]));
      for (let y = Math.ceil(minY / spacing) * spacing; y <= maxY; y += spacing) {
        for (let x = Math.ceil(minX / spacing) * spacing; x <= maxX; x += spacing) {
          if (!insidePolygon(x, y, outer) || rings.slice(1).some((hole) => insidePolygon(x, y, hole))) continue;
          const hash = hashPoint(x, y);
          if (hash % 100 >= 34) continue;
          const key = `${x.toFixed(3)},${y.toFixed(3)}`;
          if (seen.has(key)) continue;
          seen.add(key);
          lights.push([Number(x.toFixed(3)), Number(y.toFixed(3)), hash % 5 === 0 ? 1 : 0]);
        }
      }
    }
  }
  return lights;
}

const packed = new Uint8Array(width * height * 3);
for (let i = 0; i < heights.length; i++) {
  const normalized = Math.max(0, Math.min(65535, evenRound(heights[i] / maxElevation * 65535)));
  packed[i * 3] = normalized >>> 8;
  packed[i * 3 + 1] = normalized & 255;
  packed[i * 3 + 2] = cover[i];
}
const payload = {
  width, height, sample_m: sampleM, origin_xy_km: origin,
  height_encoding: "u16be-normalized-to-max-elevation", cover_encoding: "u8",
  max_elevation_m: maxElevation, packed: Buffer.from(packed).toString("base64"), water_features: waterFeatures,
  roads: transportPaths(path.join(current, "human/roads.geojson")), railways: transportPaths(path.join(current, "human/rail_lines.geojson"), true),
  settlement_lights: settlementLights(path.join(current, "human/settlements.geojson")),
};
const output = path.join(current, "viewer/terrain-3d-data.js");
fs.writeFileSync(output, `/* Generated from atlas/current/relief; run scripts/build_terrain_3d_payload.mjs. */\nwindow.LARPIDIA_TERRAIN_DATA = ${JSON.stringify(payload)};\n`, "utf8");
console.log(JSON.stringify({ output: path.relative(root, output), width, height, sample_m: sampleM, max_elevation_m: maxElevation, bytes: packed.byteLength, roads: payload.roads.length, railways: payload.railways.length, settlement_lights: payload.settlement_lights.length }));
