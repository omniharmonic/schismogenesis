import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { DOT_R, FACE_R, MAX_DOTS, mapSVG, peopleMarkup, placePeople, thinDots } from "../public/map.js";
import { personCardHTML } from "../public/hovercard.js";
import { gapsHTML, normalisePeople, peopleNote, topGaps } from "../public/crowd.js";
import { cleanAnswers, failureMessage, pickAnswers } from "../public/auth.js";

const bundle = JSON.parse(readFileSync(new URL("../public/fingerprint.json", import.meta.url), "utf8"));
const id = (x) => x;

test("dots thin evenly to the cap; small crowds are untouched", () => {
  const few = Array.from({ length: 12 }, (_, i) => ({ i }));
  assert.equal(thinDots(few), few);
  const many = Array.from({ length: 1000 }, (_, i) => ({ i }));
  const kept = thinDots(many);
  assert.equal(kept.length, MAX_DOTS);
  assert.equal(kept[0].i, 0);
  assert.ok(kept.at(-1).i > 990, "spread through the whole list");
  assert.deepEqual(thinDots(many), kept, "deterministic");
});

test("people with a name or picture are faces, never thinned; the rest are dots", () => {
  const people = [
    ...Array.from({ length: 500 }, (_, i) => ({ x: i, y: i })),
    { x: 1, y: 2, face: "https://cdn.bsky.app/a.jpg", name: "Ada", handle: "ada.bsky.social" },
    { x: 3, y: 4, name: "Bo" },
    { x: Number.NaN, y: 1 }, null,
  ];
  const { faces, dots, total } = placePeople(people, id, id);
  assert.equal(faces.length, 2);
  assert.equal(dots.length, MAX_DOTS);
  assert.equal(total, 502);
});

test("people on the same spot fan out instead of stacking", () => {
  const same = Array.from({ length: 5 }, () => ({ x: 100, y: 100, name: "N" }));
  const { faces } = placePeople(same, id, id);
  const keys = new Set(faces.map((f) => `${f.px.toFixed(1)},${f.py.toFixed(1)}`));
  assert.equal(keys.size, 5);
  assert.deepEqual([faces[0].px, faces[0].py], [100, 100], "the first keeps its spot");
});

test("the people layer marks up faces with escaped data and dots as plain circles", () => {
  const crowd = placePeople([{ x: 5, y: 5 }, { x: 9, y: 9, name: 'A "b" <c>', bio: "x&y", handle: "h", nearest: "t1", face: "https://pbs.twimg.com/p.jpg" }], id, id);
  const { dotsSvg, facesSvg } = peopleMarkup(crowd, "clip-1");
  assert.equal((dotsSvg.match(/<circle /g) || []).length, 1);
  assert.match(dotsSvg, new RegExp(`r="${DOT_R}"`));
  assert.ok(facesSvg.includes('data-name="A &quot;b&quot; &lt;c&gt;"'));
  assert.ok(facesSvg.includes('data-bio="x&amp;y"'));
  assert.ok(facesSvg.includes('clip-path="url(#clip-1)"'));
  assert.ok(facesSvg.includes(`r="${FACE_R}"`));
  assert.ok(!/camp-/.test(facesSvg), "faces carry no camp colour");
});

test("mapSVG draws people under the thinkers, and only when given", () => {
  const plain = mapSVG(bundle, { width: 400, height: 640 });
  assert.ok(!plain.includes("map-people"));
  const t = bundle.thinkers;
  const people = [{ x: t[0].x, y: t[0].y }, { x: t[1].x, y: t[1].y, name: "Ada", face: "https://cdn.bsky.app/a.jpg" }];
  const svg = mapSVG(bundle, { width: 400, height: 640, people });
  const dots = svg.indexOf("map-people-dots"), faces = svg.indexOf("map-people-faces"), thinker = svg.indexOf('class="map-thinker');
  assert.ok(dots > 0 && dots < faces && faces < thinker);
  assert.match(svg, /2 people<\/text>/);
});

test("a person's card shows name, handle, bio and their nearest thinker by name", () => {
  const t = bundle.thinkers[0];
  const html = personCardHTML({ name: "Ada <L>", handle: "ada.bsky.social", bio: "Bio", nearest: t.id, face: "https://cdn.bsky.app/a.jpg" }, bundle);
  assert.ok(html.includes("Ada &lt;L&gt;"));
  assert.ok(html.includes("@ada.bsky.social"));
  assert.ok(html.includes("Bio"));
  assert.ok(html.includes(t.name.replace(/&/g, "&amp;")));
  assert.ok(!personCardHTML({ name: "N" }, bundle).includes("Nearest"));
});

test("a missing people endpoint means no people", () => {
  assert.deepEqual(normalisePeople(null), { available: false, min_cell: 10, count: 0, people: [], bins: null });
  const d = normalisePeople({ min_cell: 10, count: 4, people: [] });
  assert.equal(peopleNote(d), "People appear here once 10 have added their answers (now 4).");
  assert.equal(peopleNote(normalisePeople({ min_cell: 10, count: 12, people: [{ x: 1, y: 2 }] })), "");
});

test("the gap list is the largest |crowd − thinkers| first, skipping statements with too few answers", () => {
  const s = [
    { id: "a", text: "A", agree_share: 0.5, thinkers_agree_share: 0.4, gap: 0.1 },
    { id: "b", text: "B", agree_share: 0.1, thinkers_agree_share: 0.9, gap: -0.8 },
    { id: "c", text: "C", agree_share: null, thinkers_agree_share: 0.9 },
    { id: "d", text: "D", agree_share: 0.9, thinkers_agree_share: 0.4, gap: 0.5 },
  ];
  assert.deepEqual(topGaps(s).map((x) => x.id), ["b", "d", "a"]);
  assert.equal(topGaps(s, 1).length, 1);
  assert.equal(gapsHTML([]), "");
  const html = gapsHTML(s);
  assert.ok(html.includes('href="/s/b"'));
  assert.ok(html.includes("Where the crowd and the experts split most"));
});

test("saved answers: the account's win when the browser has none or older ones", () => {
  const season = "s1";
  const sheet = { season, answers: { a: 1 }, updated_at: "2026-11-05T10:00:00Z" };
  assert.equal(pickAnswers(null, sheet, season), "server");
  assert.equal(pickAnswers({ season, answers: {} }, sheet, season), "server");
  assert.equal(pickAnswers({ season, answers: { a: -1 } }, sheet, season), "server", "undated local is older");
  assert.equal(pickAnswers({ season, answers: { a: -1 }, updated_at: "2026-11-05T09:00:00Z" }, sheet, season), "server");
  assert.equal(pickAnswers({ season, answers: { a: -1 }, updated_at: "2026-11-05T11:00:00Z" }, sheet, season), "local");
  assert.equal(pickAnswers({ season, answers: { a: -1 } }, { ...sheet, season: "old" }, season), "local");
  assert.equal(pickAnswers(null, null, season), "none");
});

test("only valid answers are sent, and sign-in failures say why", () => {
  assert.deepEqual(cleanAnswers({ a: 1, b: -1, c: 0, d: 2, e: "1", f: null }), { a: 1, b: -1, c: 0 });
  assert.match(failureMessage("#signin=failed&why=handle"), /Bluesky handle/);
  assert.match(failureMessage("#signin=failed&why=expired"), /expired/);
  assert.equal(failureMessage("#signin=failed"), "Couldn't sign in");
});
