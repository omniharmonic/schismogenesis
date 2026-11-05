import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { hoverCardHTML } from "../public/hovercard.js";
import { fingerprint } from "../public/placement.js";

const bundle = JSON.parse(readFileSync(new URL("../public/fingerprint.json", import.meta.url), "utf8"));
const answers = Object.fromEntries(bundle.anchors.map((a, i) => [a.id, i % 3 ? 1 : -1]));
const result = fingerprint(bundle, answers);

test("every thinker gets a card with a name, a place and a profile link", () => {
  for (const t of bundle.thinkers) {
    const html = hoverCardHTML(bundle, t.id, { answers, result });
    assert.ok(html.includes(t.name.replace(/&/g, "&amp;")), t.id);
    assert.ok(html.includes(`href="/people#${encodeURIComponent(t.id)}"`), t.id);
    assert.match(html, /Camp|Between the|Not yet grouped/, t.id);
    assert.ok((html.match(/<li>/g) || []).length <= 3, t.id);
  }
});

test("the agreement line uses the placement's own numbers", () => {
  const r = result.ranked[0];
  const html = hoverCardHTML(bundle, r.id, { answers, result });
  assert.ok(html.includes(`You agree on <b>${r.k} of ${r.n}</b> shared statements`));
});

test("positions the visitor answered come first, marked like or unlike them", () => {
  const r = result.ranked[0];
  const html = hoverCardHTML(bundle, r.id, { answers, result });
  assert.match(html, /hc-you (same|differ)/);
});

test("without answers there is no agreement line and no marks", () => {
  const t = bundle.thinkers[0];
  const html = hoverCardHTML(bundle, t.id);
  assert.ok(!html.includes("You agree on"));
  assert.ok(!html.includes("hc-you"));
});

test("an unknown id gives nothing", () => {
  assert.equal(hoverCardHTML(bundle, "nobody-here"), "");
});
