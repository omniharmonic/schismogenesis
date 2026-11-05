import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { campOf, forceStep, FORCES, kinLinks, mapSVG, seeded, settle, settlingStart } from "../public/map.js";
import { fingerprint } from "../public/placement.js";

const bundle = JSON.parse(readFileSync(new URL("../public/fingerprint.json", import.meta.url), "utf8"));
const answers = Object.fromEntries(bundle.anchors.map((a, i) => [a.id, i % 3 ? 1 : -1]));
const result = fingerprint(bundle, answers);

test("kin links follow the lab's rule: agreement score, shared statements, a few per person", () => {
  const links = kinLinks(bundle);
  assert.ok(links.length > 50, `only ${links.length} links`);
  const ids = new Set(bundle.thinkers.map((t) => t.id));
  const keys = new Set();
  for (const l of links) {
    assert.ok(ids.has(l.s) && ids.has(l.t) && l.s < l.t);
    assert.ok(l.w >= 0.34 && l.w <= 1 && l.n >= 4);
    keys.add(`${l.s}|${l.t}`);
    // recompute the score from the stances
    let n = 0, sum = 0;
    for (const row of Object.values(bundle.stances)) {
      if (row[l.s] && row[l.t]) { n++; sum += row[l.s].a * row[l.t].a; }
    }
    assert.equal(n, l.n);
    assert.ok(Math.abs(sum / n - l.w) < 0.001);
  }
  assert.equal(keys.size, links.length, "no duplicate links");
  assert.deepEqual(kinLinks(bundle), links, "deterministic");
});

test("every thinker has a camp colour index matching the camp order", () => {
  for (const t of bundle.thinkers) {
    const c = campOf(bundle, t);
    assert.ok(c >= 0 && c <= 4);
    if (t.school) assert.equal(bundle.schools[c - 1].label, t.school, t.id);
  }
  assert.equal(campOf(bundle, { school: null }), 0);
});

const box = { w: 800, h: 640 };
const grid = () => {
  const nodes = [];
  for (let i = 0; i < 6; i++) for (let j = 0; j < 5; j++) {
    const x = 100 + i * 60, y = 100 + j * 60;
    nodes.push({ x, y, vx: 0, vy: 0, hx: x, hy: y, fixed: false });
  }
  const links = [{ a: 0, b: 1, rest: 60 }, { a: 1, b: 7, rest: Math.hypot(60, 60) }, { a: 7, b: 13, rest: Math.hypot(60, 60) }];
  return { nodes, links };
};

test("the settled layout is an equilibrium: no force moves it", () => {
  const { nodes, links } = grid();
  const e = forceStep(nodes, links, { box });
  assert.equal(e, 0);
  for (const n of nodes) assert.deepEqual([n.x, n.y], [n.hx, n.hy]);
});

test("from the gathered entrance the graph blooms out and comes to rest at home within about two seconds", () => {
  const { nodes, links } = grid();
  const half = nodes.map((_, i) => i);
  settlingStart(nodes, [half.slice(0, 15), half.slice(15)], { box });
  assert.ok(nodes.every((n) => Math.hypot(n.x - n.hx, n.y - n.hy) < 70), "starts near home");
  assert.ok(nodes.some((n) => Math.hypot(n.x - n.hx, n.y - n.hy) > 10), "but visibly gathered");
  let steps = 0, e = Infinity;
  while (e > 0.15 && steps < 600) { e = forceStep(nodes, links, { box }); steps++; }
  assert.ok(steps <= 150, `took ${steps} steps (60 a second)`);
  for (const n of nodes) assert.ok(Math.hypot(n.x - n.hx, n.y - n.hy) < 1.5);
});

test("faces never overlap while one is dragged through the others, and it springs back", () => {
  const { nodes, links } = grid();
  const d = nodes[0];
  d.fixed = true;
  for (let s = 0; s < 240; s++) {
    // drag across the grid at 2 map units a frame
    d.x = Math.min(400, 100 + s * 2); d.y = 160;
    forceStep(nodes, links, { box });
  }
  for (let s = 0; s < 20; s++) forceStep(nodes, links, { box });
  for (let i = 0; i < nodes.length; i++) for (let j = i + 1; j < nodes.length; j++) {
    const g = Math.hypot(nodes[i].x - nodes[j].x, nodes[i].y - nodes[j].y);
    assert.ok(g > FORCES.r * 2 - 2, `nodes ${i} and ${j} overlap: ${g.toFixed(1)}`);
  }
  // its kin was pulled along
  assert.ok(nodes[1].x > nodes[1].hx + 5);
  d.fixed = false;
  let e = Infinity, steps = 0;
  while (e > 0.15 && steps < 900) { e = forceStep(nodes, links, { box }); steps++; }
  assert.ok(Math.hypot(d.x - d.hx, d.y - d.hy) < 3, "springs back home");
});

test("settling a crowded layout pushes touching faces apart, then holds still", () => {
  const nodes = [[100, 100], [110, 102], [104, 95], [300, 300]].map(([x, y]) => ({ x, y, vx: 0, vy: 0, hx: x, hy: y, fixed: false }));
  const steps = settle(nodes, [], { box });
  assert.ok(steps < 400, `still moving after ${steps} steps`);
  for (let i = 0; i < 3; i++) for (let j = i + 1; j < 3; j++) {
    assert.ok(Math.hypot(nodes[i].x - nodes[j].x, nodes[i].y - nodes[j].y) >= FORCES.r * 2, `${i}/${j}`);
  }
  assert.ok(forceStep(nodes, [], { box }) < 0.05, "settled is an equilibrium");
});

test("the seeded generator is repeatable", () => {
  const a = seeded(3), b = seeded(3);
  for (let i = 0; i < 5; i++) assert.equal(a(), b());
});

test("the map markup keeps every thinker a focusable, labelled button at its place", () => {
  const svg = mapSVG(bundle, { result, width: 800, height: 640 });
  const thinkers = svg.match(/<g class="map-thinker[^>]*>/g);
  assert.equal(thinkers.length, bundle.thinkers.length);
  for (const g of thinkers) {
    assert.match(g, /tabindex="0" role="button" aria-label="[^"]+"/);
    assert.match(g, /transform="translate\([\d.]+ [\d.]+\)"/);
    assert.match(g, /camp-[0-4]/);
  }
  assert.match(svg, /class="map-kin"[^>]*d="M/);
  assert.match(svg, /class="map-tether" data-to="/);
  // the same input draws the same map (apart from the per-map ids)
  const strip = (s) => s.replace(/(face-clip|thinker-map)-\d+/g, "");
  assert.equal(strip(mapSVG(bundle, { result, width: 800, height: 640 })), strip(svg));
});

test("no two faces overlap in the settled layout", () => {
  for (const size of [{ width: 800, height: 640 }, { width: 400, height: 640 }]) {
    const svg = mapSVG(bundle, { result, ...size });
    const pts = [...svg.matchAll(/class="map-thinker[^>]*transform="translate\(([\d.]+) ([\d.]+)\)"/g)].map((m) => [+m[1], +m[2]]);
    for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
      assert.ok(Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]) >= FORCES.r * 2 - 0.5, `${i}/${j} at ${size.width}`);
    }
  }
});
