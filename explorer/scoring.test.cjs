const assert = require("node:assert/strict");
const { scoreRound, totalScore } = require("./scoring.js");
const target = { x: 10000, y: 8000 };
const scoreAt = (dx, dy) => scoreRound({ x: target.x + dx, y: target.y + dy }, target);
assert.deepEqual(scoreAt(0, 0), { distanceMeters: 0, points: 5000, perfect: true });
for (const [dx, dy] of [[1.5, 1.5], [1.5, -1.5], [-1.5, 1.5], [-1.5, -1.5]]) assert.equal(scoreAt(dx, dy).points, 5000);
assert.equal(scoreAt(1.500001, 0).perfect, false);
assert.equal(scoreAt(1.500001, 0).points, 4999);
assert.equal(scoreAt(100, 0).points, Math.round(5000 * (1 - 100 / 15000) ** 2));
assert.equal(scoreAt(1000, 0).points, 4356);
assert.equal(scoreAt(5000, 0).points, 2222);
assert.deepEqual(scoreAt(15000, 0), { distanceMeters: 15000, points: 0, perfect: false });
assert.equal(scoreAt(15001, 0).points, 0);
assert.deepEqual(scoreRound(null, null, true), { distanceMeters: null, points: 0, perfect: false });
assert.equal(totalScore([{ points: 5000 }, { points: 5000 }, { points: 5000 }, { points: 5000 }]), 20000);
assert.equal(totalScore([{ points: 5000 }, { points: 5000 }, { points: 5000 }, { points: 9000 }]), 20000);
assert.throws(() => scoreRound({ x: NaN, y: 0 }, target), TypeError);
for (const distance of [0, 1.5, 1.5001, 100, 1000, 5000, 14999, 15000, 30000]) {
  const result = scoreAt(distance, 0);
  assert.ok(Number.isInteger(result.points) && result.points >= 0 && result.points <= 5000, `Neplatné body při ${distance} m.`);
}
console.log("Scoring: přesná shoda, hranice 3×3 m, vzdálenosti, přeskočení a limit 20 000 bodů prošly.");
