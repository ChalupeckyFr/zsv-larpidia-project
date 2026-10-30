/* Natural-material city view for capital-3d.html. Geometry stays procedural and follows the CP-01 plan. */
window.createLarpidiaCityNatureLayer = function ({ gl, city, toWorld, ground, face, flatFace, triangulate, drawArrays, getExag }) {
  const bufferNames = ['blocks', 'parks', 'lawns', 'roads', 'houses', 'future', 'buildings', 'greenery'];
  const buffers = Object.fromEntries(bufferNames.map((name) => [name, gl.createBuffer()]));
  const counts = Object.fromEntries(bufferNames.map((name) => [name, 0]));
  let built = false;

  const palette = {
    old_rowhouse: { walls: ['#d4c0a3', '#c8bba5', '#b9856e', '#dbccb6'], roofs: ['#9b4f3d', '#77544b', '#a75d43', '#756c60'] },
    residential: { walls: ['#e1d7c3', '#d8c9ae', '#c9c1ad', '#e7e0d2'], roofs: ['#955942', '#76564a', '#7b7770', '#a76c4e', '#655e57'] },
    glass_shopfront: { walls: ['#687a7b', '#777d78', '#766e62'], roofs: ['#596260', '#6c7470', '#74695e'] },
    civic: { walls: ['#d6cbb4', '#bdb6a5', '#c6bca7'], roofs: ['#77746b', '#8a735d', '#8c624d'] },
  };
  const blockColors = {
    residential_low: '#829465', residential_mid: '#71875c', old_town_mixed: '#928a72',
    promenade_retail: '#8e947b', retail_main: '#888a78', transit_mixed: '#80916f',
    civic_mixed: '#829372', school: '#81996a', new_waterfront: '#829274',
  };
  const parkColors = { park: '#75935d', green_wedge: '#819a64', square: '#a49c89', civic_plaza: '#a89f8b', station_plaza: '#a39d90', promenade: '#b3a78f', historic_harbor: '#879477' };
  const hash = (value) => { let h = 2166136261; for (const c of String(value)) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return h >>> 0; };
  const random01 = (value) => { let x = hash(value); x ^= x << 13; x ^= x >>> 17; x ^= x << 5; return (x >>> 0) / 4294967295; };
  const mix = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
  const quad = (out, a, b, c, d, color, raised = false) => {
    if (raised) { face(out, a, b, c, color); face(out, a, c, d, color); }
    else { flatFace(out, a, b, c, color); flatFace(out, a, c, d, color); }
  };
  const meterPoint = ([u, v], height = 0) => {
    const [x, z] = toWorld(u, v);
    return [x, ground(x, z) + height / 1000, z];
  };
  const pointInPolygon = (x, y, points) => {
    let inside = false;
    for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
      const [xi, yi] = points[i], [xj, yj] = points[j];
      if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
    }
    return inside;
  };

  function addWindow(out, pointAt, center, widthM, edgeKm, floor, floors, color = '#8ca8aa') {
    const level = 1 / Math.max(1, floors);
    const bottom = floor * level + level * 0.24;
    const height = level * (floor === 0 ? 0.38 : 0.43);
    // pointAt expects a fraction along the facade, while window dimensions are meters.
    const half = Math.min(widthM / (2000 * edgeKm), 0.42);
    const frameA = pointAt(center - half, bottom - level * 0.035);
    const frameB = pointAt(center + half, bottom - level * 0.035);
    const frameC = pointAt(center + half, bottom + height + level * 0.035);
    const frameD = pointAt(center - half, bottom + height + level * 0.035);
    quad(out, frameA, frameB, frameC, frameD, '#eee7d8', true);
    const inset = Math.min(0.08, widthM * 0.12) / (1000 * edgeKm);
    const paneA = pointAt(center - half + inset, bottom + level * 0.045);
    const paneB = pointAt(center + half - inset, bottom + level * 0.045);
    const paneC = pointAt(center + half - inset, bottom + height - level * 0.045);
    const paneD = pointAt(center - half + inset, bottom + height - level * 0.045);
    quad(out, paneA, paneB, paneC, paneD, color, true);
  }

  function addHouse(out, home, height, style, floors, id, baseColor) {
    const points = home.map(([u, v]) => toWorld(u, v));
    if (points.length < 3) return;
    const base = points.map(([x, z]) => [x, ground(x, z) + 0.00015, z]);
    const rise = height * getExag() / 1000;
    const top = base.map(([x, y, z]) => [x, y + rise, z]);
    const kind = palette[style] || palette.residential;
    const seed = hash(id);
    const wall = kind.walls[seed % kind.walls.length];
    const roof = style === 'glass_shopfront' ? kind.roofs[(seed >>> 3) % kind.roofs.length] : kind.roofs[(seed >>> 5) % kind.roofs.length];
    let centerX = 0, centerZ = 0;
    for (const [x, z] of points) { centerX += x / points.length; centerZ += z / points.length; }

    for (let i = 0; i < base.length; i++) {
      const j = (i + 1) % base.length;
      face(out, base[i], base[j], top[j], wall);
      face(out, base[i], top[j], top[i], wall);
      const a = base[i], b = base[j], dx = b[0] - a[0], dz = b[2] - a[2], edge = Math.hypot(dx, dz);
      const detailFacade = style === 'glass_shopfront' || style === 'civic' || seed % 3 === 0;
      const visibleFacade = style === 'glass_shopfront' || i === seed % base.length;
      if (!detailFacade || !visibleFacade || edge < 0.001 || floors < 1) continue;
      const mx = (a[0] + b[0]) / 2 - centerX, mz = (a[2] + b[2]) / 2 - centerZ, ml = Math.hypot(mx, mz) || 1;
      const nx = mx / ml * 0.000045, nz = mz / ml * 0.000045;
      const pointAt = (t, level) => [a[0] + dx * t + nx, a[1] + (b[1] - a[1]) * t + rise * level, a[2] + dz * t + nz];
      const panes = Math.max(1, Math.min(style === 'glass_shopfront' ? 3 : 2, Math.floor(edge * 1000 / (style === 'glass_shopfront' ? 4.0 : 3.6))));
      for (let floor = 0; floor < floors; floor++) {
        for (let n = 0; n < panes; n++) {
          const width = Math.min(style === 'glass_shopfront' ? 2.3 : 1.05, edge * 1000 / panes * 0.62);
          addWindow(out, pointAt, (n + 0.5) / panes, width, edge, floor, floors, style === 'glass_shopfront' ? '#a9c9ca' : '#879fa5');
        }
      }
    }
    if (style !== 'glass_shopfront' && floors > 0) {
      const a = base[0], b = base[1], dx = b[0] - a[0], dz = b[2] - a[2], edge = Math.hypot(dx, dz);
      const mx = (a[0] + b[0]) / 2 - centerX, mz = (a[2] + b[2]) / 2 - centerZ, ml = Math.hypot(mx, mz) || 1;
      const nx = mx / ml * 0.00006, nz = mz / ml * 0.00006;
      const pointAt = (t, level) => [a[0] + dx * t + nx, a[1] + (b[1] - a[1]) * t + rise * level, a[2] + dz * t + nz];
      const doorWidth = Math.min(0.95, edge * 1000 * 0.22), half = doorWidth / (2 * edge * 1000), center = 0.5;
      const d0 = pointAt(center - half, 0.015), d1 = pointAt(center + half, 0.015), d2 = pointAt(center + half, 0.30 / Math.max(1, floors)), d3 = pointAt(center - half, 0.30 / Math.max(1, floors));
      quad(out, d0, d1, d2, d3, '#655342', true);
    }
    for (const tri of triangulate(home)) flatFace(out, top[tri[0]], top[tri[1]], top[tri[2]], baseColor || roof);
  }

  function addTree(out, u, v, radius, seed, evergreen = false) {
    const [x, z] = toWorld(u, v), y = ground(x, z) + 0.00006, r = radius / 1000;
    const exag = getExag(), trunkHeight = 2.2 * exag / 1000, canopyHeight = (evergreen ? 7.5 : 6.2) * exag / 1000;
    const angle = (seed % 360) * Math.PI / 180, segments = 7;
    const trunkColor = '#66513a', leaves = evergreen ? ['#405d43', '#4c6c49', '#58774c'] : ['#5e7949', '#718951', '#819657', '#637d48'];
    for (let s = 0; s < segments; s++) {
      const a0 = angle + s / segments * Math.PI * 2, a1 = angle + (s + 1) / segments * Math.PI * 2;
      const p0 = [x + Math.cos(a0) * r * 0.13, y, z + Math.sin(a0) * r * 0.13];
      const p1 = [x + Math.cos(a1) * r * 0.13, y, z + Math.sin(a1) * r * 0.13];
      const q0 = [p0[0], y + trunkHeight, p0[2]], q1 = [p1[0], y + trunkHeight, p1[2]];
      face(out, p0, p1, q1, trunkColor); face(out, p0, q1, q0, trunkColor);
    }
    const tiers = evergreen ? [[0.12, 0.52, 0.40], [0.34, 0.76, 0.32], [0.57, 1.0, 0.20]] : [[0.0, 0.57, 0.52], [0.33, 0.86, 0.44], [0.62, 1.0, 0.28]];
    for (let t = 0; t < tiers.length; t++) {
      const [low, high, scale] = tiers[t], bottomY = y + trunkHeight + canopyHeight * low, topY = y + trunkHeight + canopyHeight * high;
      const canopyRadius = r * scale, tipX = x + Math.sin(seed + t) * canopyRadius * 0.08, tipZ = z + Math.cos(seed + t * 2) * canopyRadius * 0.08;
      for (let s = 0; s < segments; s++) {
        const a0 = angle + s / segments * Math.PI * 2, a1 = angle + (s + 1) / segments * Math.PI * 2;
        const p0 = [x + Math.cos(a0) * canopyRadius, bottomY, z + Math.sin(a0) * canopyRadius];
        const p1 = [x + Math.cos(a1) * canopyRadius, bottomY, z + Math.sin(a1) * canopyRadius];
        const tip = [tipX, topY, tipZ];
        face(out, p0, p1, tip, leaves[(seed + s + t) % leaves.length]);
      }
    }
  }

  function addBush(out, u, v, radius, seed) {
    const [x, z] = toWorld(u, v), y = ground(x, z) + 0.00004;
    const r = radius / 1000, h = 1.15 * getExag() / 1000, segments = 7, angle = (seed % 360) * Math.PI / 180;
    const lower = [], upper = [], top = [x + Math.sin(seed) * r * 0.06, y + h, z + Math.cos(seed) * r * 0.06];
    for (let i = 0; i < segments; i++) {
      const a = angle + i / segments * Math.PI * 2, c = Math.cos(a), sn = Math.sin(a);
      lower.push([x + c * r * 0.82, y, z + sn * r * 0.82]);
      upper.push([x + c * r * 0.68, y + h * 0.55, z + sn * r * 0.68]);
    }
    const colors = ['#557447', '#66824c', '#71894f', '#5b7846'];
    for (let i = 0; i < segments; i++) {
      const j = (i + 1) % segments, color = colors[(seed + i) % colors.length];
      face(out, lower[i], lower[j], upper[j], color);
      face(out, lower[i], upper[j], upper[i], color);
      face(out, upper[i], upper[j], top, colors[(seed + i + 1) % colors.length]);
    }
  }

  function addHedge(out, a, b, height = 1.25, width = 0.75) {
    const dx = b[0] - a[0], dy = b[1] - a[1], length = Math.hypot(dx, dy) || 1, nx = -dy / length * width / 2, ny = dx / length * width / 2;
    const corners = [[a[0] + nx, a[1] + ny], [b[0] + nx, b[1] + ny], [b[0] - nx, b[1] - ny], [a[0] - nx, a[1] - ny]].map(([u, v]) => meterPoint([u, v], 0.03));
    const top = corners.map(([x, y, z]) => [x, y + height * getExag() / 1000, z]);
    for (let i = 0; i < 4; i++) { const j = (i + 1) % 4; face(out, corners[i], corners[j], top[j], '#486b43'); face(out, corners[i], top[j], top[i], '#557849'); }
    flatFace(out, top[0], top[1], top[2], '#688650'); flatFace(out, top[0], top[2], top[3], '#688650');
  }

  function addFenceEdge(out, a, b, opening = false) {
    const length = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const steps = Math.max(1, Math.ceil(length / 2.2)), height = 1.0;
    const at = (t, h) => meterPoint([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t], h);
    for (const level of [0.35, 0.78]) for (let i = 0; i < steps; i++) {
      const t0 = i / steps, t1 = (i + 1) / steps;
      quad(out, at(t0, level), at(t1, level), at(t1, level + 0.09), at(t0, level + 0.09), '#806c4f', true);
    }
    const pickets = Math.max(2, Math.ceil(length / 1.05));
    for (let i = 0; i <= pickets; i++) {
      const t = i / pickets;
      if (opening && t > 0.43 && t < 0.57) continue;
      const half = Math.min(0.055 / Math.max(1, length), 0.015);
      quad(out, at(Math.max(0, t - half), 0.03), at(Math.min(1, t + half), 0.03), at(Math.min(1, t + half), height), at(Math.max(0, t - half), height), '#9a805d', true);
    }
  }

  function gardenBounds(home) {
    if (home.points.length !== 4) return null;
    const center = home.points.reduce((c, p) => [c[0] + p[0] / 4, c[1] + p[1] / 4], [0, 0]);
    const p0 = home.points[0], p1 = home.points[1], p2 = home.points[2];
    const uLen = Math.hypot(p1[0] - p0[0], p1[1] - p0[1]), vLen = Math.hypot(p2[0] - p1[0], p2[1] - p1[1]);
    if (uLen < 0.1 || vLen < 0.1) return null;
    const ux = (p1[0] - p0[0]) / uLen, uy = (p1[1] - p0[1]) / uLen, vx = (p2[0] - p1[0]) / vLen, vy = (p2[1] - p1[1]) / vLen;
    const hu = uLen / 2 + 4.0, hv = vLen / 2 + 4.5;
    return [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([a, b]) => [center[0] + ux * hu * a + vx * hv * b, center[1] + uy * hu * a + vy * hv * b]);
  }

  function addRoads(out) {
    const maxSegment = 16;
    const roadStations = (points, halfWidth) => {
      const dense = [];
      for (let i = 0; i < points.length - 1; i++) {
        const a = points[i], b = points[i + 1], len = Math.hypot(b[0] - a[0], b[1] - a[1]);
        if (i === 0) dense.push(a);
        const steps = Math.max(1, Math.ceil(len / maxSegment));
        for (let k = 1; k <= steps; k++) { const t = k / steps; dense.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]); }
      }
      const clean = dense.filter((p, i) => !i || Math.hypot(p[0] - dense[i - 1][0], p[1] - dense[i - 1][1]) > 0.01);
      return clean.map((p, i) => {
        const prev = clean[Math.max(0, i - 1)], next = clean[Math.min(clean.length - 1, i + 1)];
        const unit = (dx, dy) => { const len = Math.hypot(dx, dy) || 1; return [dx / len, dy / len]; };
        const incoming = i === 0 ? unit(next[0] - p[0], next[1] - p[1]) : unit(p[0] - prev[0], p[1] - prev[1]);
        const outgoing = i === clean.length - 1 ? incoming : unit(next[0] - p[0], next[1] - p[1]);
        let tangent = unit(incoming[0] + outgoing[0], incoming[1] + outgoing[1]);
        if (i === 0) tangent = outgoing;
        if (i === clean.length - 1) tangent = incoming;
        const n0 = [-incoming[1], incoming[0]], n1 = [-outgoing[1], outgoing[0]];
        let mx = n0[0] + n1[0], my = n0[1] + n1[1], mlen = Math.hypot(mx, my);
        if (mlen < 0.001) { mx = n1[0]; my = n1[1]; mlen = 1; }
        mx /= mlen; my /= mlen;
        const scale = Math.min(2.5, 1 / Math.max(0.4, Math.abs(mx * n1[0] + my * n1[1])));
        const normal = [mx * scale, my * scale];
        if (i === 0 || i === clean.length - 1) {
          const cap = Math.max(halfWidth, 5);
          p = [p[0] + tangent[0] * (i === 0 ? -cap : cap), p[1] + tangent[1] * (i === 0 ? -cap : cap)];
        }
        return { p, normal };
      });
    };
    const strip = (out, stations, halfWidth, height, color) => {
      const edges = stations.map(({ p, normal }) => [
        [p[0] + normal[0] * halfWidth, p[1] + normal[1] * halfWidth],
        [p[0] - normal[0] * halfWidth, p[1] - normal[1] * halfWidth],
      ]);
      for (let i = 0; i < edges.length - 1; i++) {
        const a = edges[i], b = edges[i + 1];
        quad(out, meterPoint(a[0], height), meterPoint(a[1], height), meterPoint(b[1], height), meterPoint(b[0], height), color);
      }
    };
    for (const road of city.streets) {
      const localPaving = road.cls === 'L' || road.cls === 'P';
      const asphaltColor = road.cls === 'C' ? '#646561' : '#4e5352';
      const stations = roadStations(road.points, road.width / 2), row = road.width / 2;
      if (road.state === 'built') {
        if (localPaving) strip(out, stations, row, 0.43, road.cls === 'P' ? '#b5a88f' : '#89867d');
        else {
          strip(out, stations, row, 0.43, '#b8b1a1');
          strip(out, stations, row * 0.68, 0.50, asphaltColor);
        }
      } else strip(out, stations, row * 0.9, 0.40, '#a99f89');
      if (road.state === 'built' && ['R1', 'A', 'B', 'S'].includes(road.cls)) {
        for (let i = 0; i < stations.length - 1; i++) {
          const a = stations[i].p, b = stations[i + 1].p, len = Math.hypot(b[0] - a[0], b[1] - a[1]);
          if (len < 4) continue;
          const nx = stations[i].normal[0], ny = stations[i].normal[1], dx = (b[0] - a[0]) / len, dy = (b[1] - a[1]) / len;
          const start = 3, end = Math.min(len - 1, 8), halfLine = 0.045;
          if (end <= start) continue;
          const point = (t, side) => [a[0] + dx * t + nx * halfLine * side, a[1] + dy * t + ny * halfLine * side];
          const p0 = point(start, 1), p1 = point(start, -1), p2 = point(end, -1), p3 = point(end, 1);
          quad(out, meterPoint(p0, 0.56), meterPoint(p1, 0.56), meterPoint(p2, 0.56), meterPoint(p3, 0.56), '#e2dfd6');
        }
      }
    }
  }

  function addStreetTrees(out) {
    for (const road of city.streets) {
      if (road.state !== 'built' || !['A', 'B', 'C', 'S'].includes(road.cls)) continue;
      for (let i = 0; i < road.points.length - 1; i++) {
        const a = road.points[i], b = road.points[i + 1], dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy);
        if (len < 35) continue;
        const spacing = road.cls === 'C' ? 54 : 38, nx = -dy / len, ny = dx / len, offset = road.width / 2 + 2.0;
        for (let d = spacing * 0.5; d < len - 8; d += spacing) for (const side of [-1, 1]) {
          const t = d / len, u = a[0] + dx * t + nx * offset * side, v = a[1] + dy * t + ny * offset * side, seed = hash(`${i}:${d}:${road.cls}:${road.points[0][0]}`);
          addTree(out, u, v, 2.1 + random01(seed) * 1.1, seed, seed % 4 === 0);
        }
      }
    }
  }

  function addParkTrees(out) {
    for (const park of city.parks) {
      if (!park.points || park.points.length < 3) continue;
      const xs = park.points.map((p) => p[0]), ys = park.points.map((p) => p[1]);
      const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
      if (park.type === 'historic_harbor' || park.type === 'promenade') continue;
      const open = ['park', 'green_wedge'].includes(park.type), spacing = park.type === 'green_wedge' ? 42 : park.type === 'park' ? 24 : 48;
      for (let row = 0, y = minY + spacing / 2; y < maxY; row++, y += spacing) for (let col = 0, x = minX + spacing / 2; x < maxX; col++, x += spacing) {
        const seed = hash(`${park.id}:${row}:${col}`), u = x + (random01(seed) - 0.5) * spacing * 0.48, v = y + (random01(seed + 1) - 0.5) * spacing * 0.48;
        if (!pointInPolygon(u, v, park.points)) continue;
        if (!open && seed % 3 !== 0) continue;
        addTree(out, u, v, 2.4 + random01(seed + 2) * 1.5, seed, seed % 5 === 0);
        if (seed % 6 === 0) addBush(out, u + spacing * 0.14, v - spacing * 0.1, 0.85 + random01(seed + 4) * 0.4, seed);
      }
    }
  }

  function addGardens(lawnOut, greeneryOut) {
    const lawnTones = ['#8fa273', '#96a779', '#82966c'];
    for (const home of city.houses) {
      if (home.use !== 'residential_low' || home.kind === 'fringe') continue;
      const bounds = gardenBounds(home);
      if (!bounds) continue;
      const seed = hash(home.id), hedge = seed % 3 === 0;
      const lawn = bounds.map((point) => meterPoint(point, 0.025));
      for (const tri of triangulate(bounds)) flatFace(lawnOut, lawn[tri[0]], lawn[tri[1]], lawn[tri[2]], lawnTones[seed % lawnTones.length]);
      for (let i = 0; i < 4; i++) {
        const a = bounds[i], b = bounds[(i + 1) % 4];
        if (hedge) addHedge(greeneryOut, a, b, 1.2, 0.7);
        else addFenceEdge(greeneryOut, a, b, i === 0);
      }
      if (seed % 4 === 1) {
        const p0 = bounds[0], p1 = bounds[1], p3 = bounds[3];
        const u = p0[0] * 0.55 + p1[0] * 0.25 + p3[0] * 0.2, v = p0[1] * 0.55 + p1[1] * 0.25 + p3[1] * 0.2;
        addTree(greeneryOut, u, v, 2.0 + random01(seed) * 0.7, seed, false);
      }
      if (seed % 3 === 1) {
        const edge = (seed >>> 4) % 4, a = bounds[edge], b = bounds[(edge + 1) % 4];
        addBush(greeneryOut, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0.9 + random01(seed + 3) * 0.45, seed);
      }
    }
  }

  function upload(name, vertices) {
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers[name]);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
    counts[name] = vertices.length / 9;
  }

  function rebuild() {
    const blocks = [], parks = [], lawns = [], roads = [], houses = [], future = [], buildings = [], greenery = [];
    for (const block of city.blocks) {
      const p = block.points.map(([u, v]) => meterPoint([u, v], 0.02));
      for (const tri of triangulate(block.points)) flatFace(blocks, p[tri[0]], p[tri[1]], p[tri[2]], blockColors[block.use] || '#81916d');
    }
    for (const park of city.parks) {
      if (!park.points || park.points.length < 3 || park.type === 'historic_harbor' || park.type === 'promenade') continue;
      const p = park.points.map(([u, v]) => meterPoint([u, v], 0.03));
      for (const tri of triangulate(park.points)) flatFace(parks, p[tri[0]], p[tri[1]], p[tri[2]], parkColors[park.type] || '#7f9669');
    }
    addRoads(roads);
    for (const home of city.houses) addHouse(houses, home.points, home.height, home.style, home.floors, home.id, null);
    for (const home of city.future) addHouse(future, home.points, home.height, ['retail_main', 'promenade_retail', 'new_waterfront'].includes(home.use) ? 'glass_shopfront' : 'residential', 3, home.id, '#b88b6d');
    const heights = { parliament: 22, admin: 18, museum: 16, church: 20, market_hall: 10, hotel_premium: 20, school: 10, harbour_office: 9, ferry_terminal: 7 };
    for (const building of city.buildings) addHouse(buildings, building.points, heights[building.subtype] || 10, 'civic', 2, building.id, null);
    addStreetTrees(greenery); addParkTrees(greenery); addGardens(lawns, greenery);
    upload('blocks', blocks); upload('parks', parks); upload('lawns', lawns); upload('roads', roads); upload('houses', houses); upload('future', future); upload('buildings', buildings); upload('greenery', greenery);
    built = true;
  }

  function draw(showFuture = true) {
    drawArrays(buffers.blocks, counts.blocks);
    drawArrays(buffers.parks, counts.parks);
    drawArrays(buffers.lawns, counts.lawns);
    drawArrays(buffers.houses, counts.houses);
    if (showFuture) drawArrays(buffers.future, counts.future);
    drawArrays(buffers.buildings, counts.buildings);
    drawArrays(buffers.greenery, counts.greenery);
    drawArrays(buffers.roads, counts.roads);
  }

  return { rebuild, draw, isBuilt: () => built };
};
