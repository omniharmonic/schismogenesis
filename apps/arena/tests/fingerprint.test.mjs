import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { agreement, fingerprint, plainStances, teaser } from "../public/fingerprint.js";

const root = new URL("../../../", import.meta.url);
const read = (p) => JSON.parse(readFileSync(new URL(p, root), "utf8"));
const bundle = read("apps/arena/public/fingerprint.json");
const vectors = read("packages/arena_fingerprint/tests/vectors.json");

function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
}

test("shared vectors match the Python implementation", () => {
  for (const c of vectors.cases) {
    const got = agreement(c.answers, vectors.stances);
    assert.deepEqual(Object.keys(got).sort(), Object.keys(c.expect).sort());
    for (const [t, [k, n, s]] of Object.entries(c.expect)) {
      assert.equal(got[t].k, k);
      assert.equal(got[t].n, n);
      assert.ok(Math.abs(got[t].s - s) < 1e-9);
    }
  }
});

test("too few answers gives not enough, never a placement", () => {
  const unsure = Object.fromEntries(bundle.anchors.map((a) => [a.id, 0]));
  assert.equal(fingerprint(bundle, unsure).status, "not_enough");
  const few = Object.fromEntries(bundle.anchors.slice(0, 5).map((a) => [a.id, 1]));
  const r = fingerprint(bundle, few);
  assert.equal(r.status, "not_enough");
  assert.equal(r.position, undefined);
});

test("ranked thinkers all share at least three statements", () => {
  const all = Object.fromEntries(bundle.anchors.map((a) => [a.id, 1]));
  const r = fingerprint(bundle, all);
  assert.equal(r.status, "ok");
  for (const row of r.ranked) assert.ok(row.n >= 3);
});

test("answering exactly like a thinker puts them first", () => {
  const stances = plainStances(bundle);
  const target = "max-tegmark";
  const answers = {};
  for (const a of bundle.anchors) answers[a.id] = stances[a.id][target] ?? 0;
  const r = fingerprint(bundle, answers);
  assert.equal(r.status, "ok");
  assert.equal(r.nearest[0].id, target);
  assert.equal(r.nearest[0].k, r.nearest[0].n);
});

test("position lies inside the box of the top three thinkers", () => {
  const random = rng(3);
  const answers = Object.fromEntries(bundle.anchors.map((a) => [a.id, random() < 0.5 ? 1 : -1]));
  const r = fingerprint(bundle, answers);
  const pos = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t]));
  const xs = r.ranked.slice(0, 3).map((t) => pos[t.id].x);
  const ys = r.ranked.slice(0, 3).map((t) => pos[t.id].y);
  assert.ok(r.position.x >= Math.min(...xs) - 1e-9 && r.position.x <= Math.max(...xs) + 1e-9);
  assert.ok(r.position.y >= Math.min(...ys) - 1e-9 && r.position.y <= Math.max(...ys) + 1e-9);
});

test("signature lines oppose the home school and side with another", () => {
  const stances = plainStances(bundle);
  const random = rng(11);
  let found = 0;
  for (let i = 0; i < 200; i++) {
    const answers = Object.fromEntries(bundle.anchors.map((a) => [a.id, random() < 0.5 ? 1 : -1]));
    const r = fingerprint(bundle, answers);
    for (const line of r.signature) {
      found += 1;
      assert.notEqual(line.home, line.ally);
      assert.equal(line.home, r.schools[0].label);
      assert.ok(line.allies.length >= 1);
      for (const a of line.allies) assert.equal(stances[line.anchor][a], answers[line.anchor]);
    }
  }
  assert.ok(found > 0);
});

test("camp splits count only decided majorities, deepest is a split layer", () => {
  const all = Object.fromEntries(bundle.anchors.map((a) => [a.id, -1]));
  const r = fingerprint(bundle, all);
  for (const camp of r.camps) {
    if (camp.deepest) {
      const [agreed, opposed] = camp.byLayer[camp.deepest];
      assert.ok(opposed > agreed);
    }
  }
});

test("teaser names two different schools", () => {
  const first = Object.fromEntries(bundle.anchors.slice(0, 8).map((a) => [a.id, 1]));
  const t = teaser(bundle, first);
  assert.ok(t && t.closer !== t.further);
});

test("balance: well-covered schools top random sheets within 0.5x to 2x of fair share", () => {
  // Schools where at least half the members have fewer than 3 stated stances among the anchors can't be fairly
  // reached; they must be disclosed in the selection log instead of tuned away.
  const stances = plainStances(bundle);
  const coverage = {};
  for (const e of Object.values(stances)) for (const t of Object.keys(e)) coverage[t] = (coverage[t] || 0) + 1;
  const thin = new Set(bundle.thinkers.filter((t) => (coverage[t.id] || 0) < 3).map((t) => t.id));
  for (const id of thin) {
    if (bundle.thinkers.find((t) => t.id === id).school) {
      assert.ok(bundle.selection_log.some((l) => l.includes(id)), `${id} undisclosed`);
    }
  }
  const random = rng(7);
  const counts = {};
  let placed = 0;
  for (let i = 0; i < 1000; i++) {
    const answers = Object.fromEntries(
      bundle.anchors.map((a) => [a.id, [1, -1, 0][Math.floor(random() * 3)]]),
    );
    const r = fingerprint(bundle, answers);
    if (r.status !== "ok") continue;
    placed += 1;
    counts[r.schools[0].label] = (counts[r.schools[0].label] || 0) + 1;
  }
  const total = bundle.schools.reduce((t, s) => t + s.members.length, 0);
  const report = bundle.schools.map((s) => ({
    school: s.label,
    thin: s.members.filter((m) => thin.has(m)).length * 2 >= s.members.length,
    ratio: (counts[s.label] || 0) / placed / (s.members.length / total),
  }));
  console.log("balance", JSON.stringify(report.map((r) => [r.school, +r.ratio.toFixed(2), r.thin])));
  for (const r of report.filter((r) => !r.thin)) {
    assert.ok(r.ratio >= 0.5 && r.ratio <= 2, `${r.school} ratio ${r.ratio}`);
  }
});

import { highlights, profileSummary } from "../public/fingerprint.js";

test("highlights pick a real agreeing quote, a disagreeing one, and the rarest take", () => {
  const stances = plainStances(bundle);
  const random = rng(21);
  const answers = Object.fromEntries(bundle.anchors.map((a) => [a.id, random() < 0.5 ? 1 : -1]));
  const r = fingerprint(bundle, answers);
  const h = highlights(bundle, answers, r);
  if (h.topQuote) {
    assert.equal(h.topQuote.thinker, r.nearest[0].id);
    assert.equal(stances[h.topQuote.anchor][h.topQuote.thinker], answers[h.topQuote.anchor]);
    assert.ok(h.topQuote.q.length <= 280 && h.topQuote.url);
  }
  if (h.farQuote) assert.notEqual(stances[h.farQuote.anchor][h.farQuote.thinker], answers[h.farQuote.anchor]);
  assert.ok(h.rarest && h.rarest.with <= h.rarest.of && h.rarest.of >= 3);
  for (const a of bundle.anchors) {
    const v = answers[a.id];
    const e = Object.values(bundle.stances[a.id]);
    if (e.length >= 3) assert.ok(e.filter((x) => x.a === v).length / e.length >= h.rarest.share - 1e-9);
  }
  const s = profileSummary(r, h.rarest);
  assert.equal(s.home, r.schools[0].label);
  assert.deepEqual(Object.keys(s.nearest[0]).sort(), ["id", "k", "n"]);
});
