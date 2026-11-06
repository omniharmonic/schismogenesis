// Round 2: the density field at scale, zoom, camp names and the guided next step.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { densityMarkup, DENSITY_MAX, mapSVG, nameSpot, seeded } from "../public/map.js";
import { crowdOptions, hasCrowd, hexBins, normaliseBins, normalisePeople, peopleNote } from "../public/crowd.js";
import { clampView, faceScale, fitBox, parseBox, scaleOf, unionBoxes, zoomAt, ZOOM_MAX } from "../public/map-zoom.js";
import { applyCampNames, campShareText, checkName, groupTitle, namingHTML, nextVote, normaliseNaming, rankNames, relabel } from "../public/camp-names.js";
import { bridgeSummary, bridgesStripHTML, nextStepHTML, topBridges } from "../public/next-step.js";
import { statementsHTML } from "../public/account.js";
import { fingerprint } from "../public/placement.js";

const raw = readFileSync(new URL("../public/fingerprint.json", import.meta.url), "utf8");
const fresh = () => JSON.parse(raw);
const bundle = fresh();

/** 5000 fake people around the thinkers, the same every run. */
export function fakeCrowd(n = 5000, seed = 3) {
  const rand = seeded(seed);
  const t = bundle.thinkers;
  return Array.from({ length: n }, () => {
    const a = t[Math.floor(rand() * t.length)];
    return { x: a.x + (rand() - 0.5) * 60, y: a.y + (rand() - 0.5) * 60 };
  });
}

test("hex bins count every point once, in pointy-top cells centred where the server puts them", () => {
  const pts = fakeCrowd();
  const bins = hexBins(pts, 6);
  assert.equal(bins.cells.reduce((t, c) => t + c[2], 0), 5000);
  assert.ok(bins.cells.length > 50 && bins.cells.length < 5000);
  for (let i = 1; i < bins.cells.length; i++) assert.ok(bins.cells[i - 1][2] >= bins.cells[i][2], "fullest first");
  // every point is nearer its own cell's centre than any other (that is what a hex grid means)
  const cells = bins.cells;
  for (const p of pts.slice(0, 200)) {
    const d = cells.map((c) => Math.hypot(c[0] - p.x, c[1] - p.y));
    assert.ok(Math.min(...d) <= 6 + 0.02, "within one cell size of a centre");
  }
  // a lone point at the origin sits in the cell centred on the origin
  assert.deepEqual(hexBins([{ x: 0.5, y: -0.4 }], 6).cells, [[0, 0, 1]]);
});

test("bins from the server are made safe; an empty or broken one is null", () => {
  assert.equal(normaliseBins(null), null);
  assert.equal(normaliseBins({ size: 0, cells: [[1, 2, 3]] }), null);
  assert.equal(normaliseBins({ size: 4, cells: [[1, 2, 0], ["x", 2, 3]] }), null);
  assert.deepEqual(normaliseBins({ size: 4, cells: [[1, 2, 3], [1, 2, -1]] }), { size: 4, cells: [[1, 2, 3]] });
  const d = normalisePeople({ min_cell: 10, count: 5000, people: [], bins: hexBins(fakeCrowd(), 6) });
  assert.ok(hasCrowd(d));
  assert.equal(peopleNote(d), "", "no 'appear once' note when the crowd is binned");
  assert.equal(crowdOptions(d).peopleCount, 5000);
});

test("the density field: one hexagon per cell, sqrt-scaled opacity up to the cap, under the thinkers", () => {
  const bins = hexBins(fakeCrowd(), 6);
  const id = (v) => v;
  const svg = densityMarkup(bins, id, id);
  assert.equal((svg.match(/<path /g) || []).length, bins.cells.length);
  const ops = [...svg.matchAll(/fill-opacity="([\d.]+)"/g)].map((m) => Number(m[1]));
  assert.equal(Math.max(...ops), DENSITY_MAX);
  assert.ok(Math.min(...ops) > 0);
  // a cell with a quarter of the top count gets half the opacity (sqrt)
  const quarter = densityMarkup({ size: 2, cells: [[0, 0, 16], [10, 10, 4]] }, id, id);
  assert.ok(quarter.includes(`fill-opacity="${(DENSITY_MAX / 2).toFixed(3)}"`));
  assert.equal(densityMarkup({ size: 2, cells: [] }, id, id), "");

  const map = mapSVG(bundle, { width: 800, height: 640, people: [], bins, peopleCount: 5000 });
  const at = (s) => map.indexOf(s);
  assert.ok(at("map-density") > 0 && at("map-density") < at("map-thinker"), "hexagons sit under the thinkers");
  assert.ok(map.includes("· 5000 people"), "the readout counts everyone, binned or not");
});

test("faces stay on top of the density field", () => {
  const bins = hexBins(fakeCrowd(800), 6);
  const face = { x: bundle.thinkers[0].x, y: bundle.thinkers[0].y, name: "Ada", face: "https://cdn.bsky.app/a.jpg" };
  const map = mapSVG(bundle, { width: 800, height: 640, people: [face], bins });
  assert.ok(map.indexOf("map-density") < map.indexOf("map-person"));
});

test("zoom keeps the map's shape, stays between 1x and 6x and inside the map", () => {
  const base = { x: 0, y: 0, w: 400, h: 662 };
  assert.deepEqual(clampView({ x: -50, y: 10, w: 800, h: 10 }, base), base, "never further out than the whole map");
  const deep = clampView({ x: 100, y: 100, w: 10, h: 10 }, base);
  assert.equal(scaleOf(deep, base), ZOOM_MAX);
  assert.ok(Math.abs(deep.w / deep.h - base.w / base.h) < 1e-9);
  // zooming at a point keeps that point still
  const v = zoomAt(base, base, 2, 100, 200);
  assert.ok(Math.abs((100 - v.x) / v.w - 100 / 400) < 1e-9 && Math.abs((200 - v.y) / v.h - 200 / 662) < 1e-9);
  const edge = zoomAt(base, base, 3, 0, 0);
  assert.ok(edge.x === 0 && edge.y === 0, "a corner zoom stays inside");
  assert.equal(faceScale(1), 1);
  assert.equal(faceScale(1.6), 1);
  assert.ok(Math.abs(faceScale(4) * 4 - 1.6) < 1e-9, "faces appear at most 1.6 times their size");
});

test("selecting a camp frames its area", () => {
  const base = { x: 0, y: 0, w: 800, h: 662 };
  const box = unionBoxes([parseBox("100,100,80,60"), parseBox("150,120,100,100"), parseBox("bad")]);
  assert.deepEqual(box, { x: 100, y: 100, w: 150, h: 120 });
  const v = fitBox(box, base);
  assert.ok(scaleOf(v, base) > 1 && scaleOf(v, base) <= 3);
  assert.ok(v.x <= box.x && v.y <= box.y && v.x + v.w >= box.x + box.w && v.y + v.h >= box.y + box.h, "the whole camp is in view");
  // mapSVG gives each region the box to zoom to
  const map = mapSVG(bundle, { width: 800, height: 640 });
  const boxes = [...map.matchAll(/data-box="([^"]+)"/g)].map((m) => parseBox(m[1]));
  assert.ok(boxes.length >= 4 && boxes.every(Boolean));
});

test("a nearest thinker's name moves beside or further off rather than under the You mark", () => {
  const you = { x: 200, y: 200, w: 120, h: 62 };
  const spot = nameSpot({ x: 200, y: 160, w: 60, width: 800, taken: [you] });
  const hits = spot.x < you.x + you.w && you.x < spot.x + spot.w && spot.y < you.y + you.h && you.y < spot.y + spot.h;
  assert.ok(!hits, JSON.stringify(spot));
  assert.equal(nameSpot({ x: 400, y: 100, w: 60, width: 800 }).anchor, "middle", "below the face when free");
});

test("the map's names never sit on the You mark or its Find me ring", () => {
  const answers = Object.fromEntries(bundle.anchors.map((a, i) => [a.id, i % 3 ? 1 : -1]));
  const result = fingerprint(bundle, answers);
  for (const size of [{ width: 400, height: 560 }, { width: 800, height: 560 }]) {
    const map = mapSVG(bundle, { ...size, result });
    const you = map.match(/class="map-you-mark[^"]*" transform="translate\(([\d.]+) ([\d.]+)\)/);
    assert.ok(you, "the You mark is drawn around its own origin");
    const [ux, uy] = [Number(you[1]), Number(you[2])];
    for (const m of map.matchAll(/<g class="map-thinker[^"]*" data-thinker="[^"]+" transform="translate\(([\d.]+) ([\d.]+)\)"[^>]*>(?:(?!<\/g><\/g>|<g class="map-thinker).)*?<text class="map-name" x="([-\d.]+)" y="([-\d.]+)" text-anchor="(\w+)">([^<]+)<\/text>/gs)) {
      const [x, y, dx, dy, anchor, name] = [Number(m[1]), Number(m[2]), Number(m[3]), Number(m[4]), m[5], m[6]];
      const w = name.length * (size.width < 600 ? 6.8 : 6) + 12;
      const left = anchor === "middle" ? x + dx - w / 2 : anchor === "start" ? x + dx : x + dx - w;
      const top = y + dy - 12;
      const ring = 22 * 1.35;
      const nx = Math.max(left, Math.min(ux, left + w)), ny = Math.max(top, Math.min(uy, top + 16));
      assert.ok(Math.hypot(nx - ux, ny - uy) >= ring - 0.5, `${name} overlaps the ring at ${size.width}`);
    }
  }
});

test("accepted camp names replace the drafts everywhere in the bundle", () => {
  const b = fresh();
  const old = b.tree.nodes.c1.label;
  const school = Object.values(b.tree.nodes).find((n) => n.level === 1);
  applyCampNames(b, { c1: "  The careful ones ", [school.id]: "Brakes first", nope: "x", c2: "" });
  assert.equal(b.tree.nodes.c1.label, "The careful ones");
  assert.equal(b.tree.nodes.c1.drafted, old);
  assert.ok(b.named.c1 && b.named[school.id] && !b.named.c2);
  assert.ok(b.schools.some((s) => s.label === "The careful ones") && !b.schools.some((s) => s.label === old));
  assert.ok(b.thinkers.filter((t) => t.school === old).length === 0);
  assert.ok(b.thinkers.some((t) => t.school === "The careful ones"));
  assert.equal(b.camps.find((c) => c.id === "c1").label, "The careful ones");
  assert.equal(relabel(b, old), "The careful ones");
  assert.equal(relabel(b, "Something else"), "Something else");
  // the result reads the new name too, and the map draws it
  const answers = Object.fromEntries(b.anchors.map((a, i) => [a.id, i % 2 ? 1 : -1]));
  const r = fingerprint(b, answers);
  assert.ok(r.schools.every((s) => s.label !== old));
  assert.ok(mapSVG(b, {}).includes("The careful ones"));
  assert.ok(!mapSVG(b, {}).includes(`>${old}<`));
});

const NAMING = {
  nodes: [{ id: "c1", label: "AI as a new kind of risk" }, { id: "c1.1", label: "Slow it down and govern it" }],
  verified: true,
  names: [
    { id: "n1", node: "c1", name: "The careful", status: "open", up: 2, down: 1, my_vote: null, proposed_by_me: false },
    { id: "n2", node: "c1", name: "Brakes & <b>", status: "open", up: 5, down: 0, my_vote: "up", proposed_by_me: true },
    { id: "n3", node: "c9", name: "Elsewhere", status: "open", up: 9, down: 0 },
  ],
};

test("the naming panel: your camp and school, proposals ranked with your vote, a field to propose, a share", () => {
  const d = normaliseNaming(NAMING);
  assert.equal(d.names.length, 2, "names for groups you aren't in are dropped");
  assert.deepEqual(rankNames(d.names, "c1").map((n) => n.id), ["n2", "n1"]);
  const html = namingHTML(d, { bundle });
  assert.ok(html.includes("Your camp, drafted as “AI as a new kind of risk”"));
  assert.ok(html.includes("Your school, drafted as “Slow it down and govern it”"));
  assert.ok(html.includes("Brakes &amp; &lt;b&gt;") && !html.includes("<b>"), "escaped");
  assert.match(html, /data-vote="up" data-id="n2"[^>]*aria-pressed="true"/);
  assert.ok(html.includes("Your proposal"));
  assert.equal((html.match(/data-propose=/g) || []).length, 2);
  assert.ok(html.includes("x.com/intent/post") && html.includes("bsky.app/intent/compose"));
  assert.ok(html.includes(encodeURIComponent("https://debate.antimemes.is/account.html#results")));
  assert.ok(!/—/.test(html), "no em-dash fragments");
});

test("naming is explained, and gated, when you can't take part yet", () => {
  const unverified = namingHTML(normaliseNaming({ ...NAMING, verified: false, names: [] }), { bundle });
  assert.ok(unverified.includes("signed in with Bluesky or X") && unverified.includes("/account.html#settings"));
  assert.ok(!unverified.includes("data-propose"));
  const none = namingHTML(normaliseNaming({ nodes: [], verified: true, names: [] }), { bundle });
  assert.ok(none.includes("Take the survey"));
  assert.equal(normaliseNaming(null).available, false);
  assert.equal(normaliseNaming({ detail: "Not Found" }).available, false);
  const compact = namingHTML(normaliseNaming(NAMING), { bundle, compact: true });
  assert.ok(compact.length < namingHTML(normaliseNaming(NAMING), { bundle }).length);
});

test("an accepted name shows as named by its members, with the draft beside it", () => {
  const b = applyCampNames(fresh(), { c1: "The careful ones" });
  const t = groupTitle(b, { id: "c1", label: "AI as a new kind of risk" }, 0);
  assert.deepEqual(t, { kind: "camp", named: true, now: "The careful ones", drafted: "AI as a new kind of risk" });
  const html = namingHTML(normaliseNaming(NAMING), { bundle: b });
  assert.ok(html.includes("named “The careful ones” by its members") && html.includes("Drafted by the lab as “AI as a new kind of risk”"));
  assert.ok(campShareText(t).includes("a name its members chose"));
});

test("votes toggle, and names are checked the way the server checks them", () => {
  assert.equal(nextVote(null, "up"), true);
  assert.equal(nextVote("up", "down"), false);
  assert.equal(nextVote("up", "up"), null, "pressing your vote again takes it back");
  assert.deepEqual(checkName("  Brakes   first "), { name: "Brakes first" });
  assert.ok(checkName("ab").error);
  assert.ok(checkName("x".repeat(49)).error);
  assert.ok(checkName("see www.example").error && checkName("@me camp").error);
});

test("the next step is one clear action, with sign-in first when signed out", () => {
  const inside = nextStepHTML({ signedIn: true });
  assert.ok(inside.includes("Write a statement both sides can sign"));
  assert.equal((inside.match(/data-next=/g) || []).length, 1);
  assert.ok(inside.includes('href="/#write"') && inside.includes("Community Notes"));
  const outside = nextStepHTML({ signedIn: false });
  assert.ok(outside.includes('data-next="signin"') && outside.includes("Continue without an account"));
  assert.ok(!/—/.test(inside + outside));
});

test("bridges so far: passed first, then leaning, and a plain note when there are none", () => {
  const report = { bridges: {
    passed: [{ text: "Both <sides>", raters: 12, agree_by_side: [0.8, 0.7] }],
    leaning: [{ text: "Almost", raters: 6, agree_by_side: [0.7, null] }, { text: "Third" }, { text: "Fourth" }],
  } };
  assert.deepEqual(topBridges(report).map((b) => b.kind), ["passed", "leaning", "leaning"]);
  const html = bridgesStripHTML(report);
  assert.ok(html.includes("Both &lt;sides&gt;") && html.includes("12 people voted") && html.includes("80% and 70%") && html.includes("n/a"));
  assert.ok(html.includes("8 or more people"));
  for (const empty of [null, { bridges: null }, { bridges: { passed: [], leaning: [] } }]) {
    assert.ok(bridgesStripHTML(empty).includes("None yet"));
  }
});

test("your statements lead with what they earned", () => {
  assert.equal(bridgeSummary([]), "");
  assert.ok(bridgeSummary([{ text: "a", bridge: "passed" }]).startsWith("One of your statements bridges the groups"));
  assert.ok(bridgeSummary([{ text: "a", bridge: "passed" }, { text: "b", bridge: "passed" }, { text: "c", bridge: "leaning" }]).includes("2 of your statements bridge") );
  assert.ok(bridgeSummary([{ text: "a", bridge: "leaning" }]).includes("leaning toward a bridge"));
  assert.ok(bridgeSummary([{ text: "a", bridge: null }]).startsWith("None of yours"));
  const html = statementsHTML([{ text: "a", bridge: null, agree: 1 }, { text: "b", bridge: "passed", agree: 9 }]);
  assert.ok(html.indexOf("bridge-summary") < html.indexOf("my-statements"));
  assert.ok(html.includes('class="is-passed"'));
});
