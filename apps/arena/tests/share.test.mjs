import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { accountProfileBody, bskyIntentURL, profileURL, shareLine, xIntentURL } from "../public/share-links.js";
import { tabFromHash } from "../public/nav.js";
import { cleanSocial, socialsHTML, suggestedBio } from "../public/socials.js";
import { statementNumbers, statementsHTML } from "../public/account.js";
import { fingerprint } from "../public/placement.js";
import { mapSVG } from "../public/map.js";

const bundle = JSON.parse(readFileSync(new URL("../public/fingerprint.json", import.meta.url), "utf8"));
const answers = Object.fromEntries(bundle.anchors.map((a, i) => [a.id, [1, -1, 1, 0][i % 4]]));
const result = fingerprint(bundle, answers);

test("share text is plain, first person, names the school, no hashtags", () => {
  const t = shareLine({ schools: [{ label: "Builders" }] });
  assert.equal(t, "I'm closest to “Builders” in The Great AI Debate. Where do you sit?");
  assert.ok(!t.includes("#"));
  assert.match(shareLine(null), /Where do you sit\?$/);
});

test("X gets text and url apart; Bluesky gets the url inside the text", () => {
  const text = "I'm closest to “A & B” in The Great AI Debate. Where do you sit?";
  const url = "https://debate.antimemes.is/p/abc123";
  const x = new URL(xIntentURL(text, url));
  assert.equal(x.origin + x.pathname, "https://x.com/intent/post");
  assert.equal(x.searchParams.get("text"), text);
  assert.equal(x.searchParams.get("url"), url);
  const b = new URL(bskyIntentURL(text, url));
  assert.equal(b.origin + b.pathname, "https://bsky.app/intent/compose");
  assert.equal(b.searchParams.get("text"), `${text}\n${url}`);
  assert.equal([...b.searchParams.keys()].length, 1);
});

test("the page address is absolute, from the server's url or the code", () => {
  const o = "https://debate.antimemes.is";
  assert.equal(profileURL({ code: "k7q2" }, o), `${o}/p/k7q2`);
  assert.equal(profileURL({ code: "k7q2", url: "/p/k7q2" }, o), `${o}/p/k7q2`);
  assert.equal(profileURL({ code: "x", url: "https://debate.antimemes.is/p/x" }, o), "https://debate.antimemes.is/p/x");
  assert.equal(profileURL(null, o), null);
});

test("the account page body matches what the anonymous flow sends, minus answers", () => {
  assert.equal(result.status, "ok");
  const body = accountProfileBody(bundle, answers, result, true);
  assert.deepEqual(Object.keys(body).sort(), ["glyph", "listed", "summary"]);
  assert.equal(body.listed, true);
  assert.equal(body.summary.home, result.schools[0].label);
  assert.equal(body.glyph.length, bundle.anchors.length);
  assert.equal(accountProfileBody(bundle, answers, result).listed, false);
});

test("account tabs: #settings is Settings, everything else Your results", () => {
  assert.equal(tabFromHash("#settings"), "settings");
  assert.equal(tabFromHash("#Settings"), "settings");
  assert.equal(tabFromHash("#results"), "results");
  assert.equal(tabFromHash(""), "results");
  assert.equal(tabFromHash("#signed-in"), "results");
  assert.equal(tabFromHash(undefined), "results");
});

test("socials: only http(s) links, a real profile address, bare websites made https", () => {
  const s = cleanSocial({ kind: "x", handle: "@ada", url: "javascript:alert(1)", website: "ada.dev/", followers: 1200, description: " Hi " });
  assert.equal(s.handle, "ada");
  assert.equal(s.href, "https://x.com/ada");
  assert.equal(s.website.href, "https://ada.dev/");
  assert.equal(s.website.label, "ada.dev");
  assert.equal(s.description, "Hi");
  assert.equal(cleanSocial({ kind: "bsky", handle: "bo.bsky.social" }).href, "https://bsky.app/profile/bo.bsky.social");
  assert.equal(cleanSocial({ kind: "mastodon", handle: "x" }), null);
  assert.equal(cleanSocial({ kind: "x", handle: "x", website: "ftp://a" }).website, null);
  const html = socialsHTML([{ kind: "x", handle: "ada", description: "<b>bio</b>" }]);
  assert.ok(html.includes("&lt;b&gt;bio&lt;/b&gt;"), "escaped");
  assert.ok(socialsHTML([{ kind: "x", handle: "ada", description: "theirs" }], { bio: "mine" }).includes("mine"));
  assert.ok(!socialsHTML([{ kind: "x", handle: "ada", description: "theirs" }], { bio: "mine" }).includes("theirs"));
  assert.equal(socialsHTML([]), "");
});

test("the provider bio is offered, cut to 160", () => {
  assert.equal(suggestedBio([]), null);
  const s = suggestedBio([{ kind: "bsky", handle: "a", description: "" }, { kind: "x", handle: "b", description: "z".repeat(200) }]);
  assert.equal(s.network, "X");
  assert.equal(s.text.length, 160);
});

test("my statements: bridging first, plain numbers, review status named", () => {
  assert.deepEqual(statementNumbers({ agree: 3, disagree: 1 }), { votes: "3 agree, 1 disagree, 0 pass", groups: "" });
  assert.equal(statementNumbers({ groups_agreeing: 2 }).groups, "2 groups agree");
  const html = statementsHTML([
    { text: "Low", status: "approved", agree: 9, disagree: 0, pass: 0, bridge: null },
    { text: "High", status: "pending", agree: 1, disagree: 0, pass: 0, bridge: "passed" },
  ]);
  assert.ok(html.indexOf("High") < html.indexOf("Low"));
  assert.ok(html.includes("Bridges the groups"));
  assert.ok(html.includes("Waiting for review"));
  assert.equal(statementsHTML([]), "");
});

test("the You mark keeps its word, and draws a picture only from https", () => {
  const plain = mapSVG(bundle, { result, width: 400, height: 640 });
  assert.ok(plain.includes(">You</text>") && plain.includes('class="map-you"'));
  const face = mapSVG(bundle, { result, width: 400, height: 640, youFace: "https://cdn.bsky.app/a.jpg" });
  assert.ok(face.includes("map-you-face") && face.includes(">You</text>") && face.includes("map-you-ring"));
  assert.ok(!face.includes('class="map-you"'));
  const bad = mapSVG(bundle, { result, width: 400, height: 640, youFace: "javascript:x" });
  assert.ok(!bad.includes("map-you-face"));
});
