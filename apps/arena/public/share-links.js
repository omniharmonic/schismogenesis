// Sharing a signed-in account's results: one public page per account (PUT /api/me/profile, the
// same code every time), then each network's own compose page. Nothing posts on anyone's behalf.
// The pure helpers are tested in tests/share.test.mjs.
import { highlights, profileSummary } from "./placement.js";
import { glyphValues, scrambled } from "./glyph.js";
import { esc } from "./map.js";

/** The post text: plain, first person, no hashtags. */
export function shareLine(result) {
  const home = result?.schools?.[0]?.label;
  return home
    ? `I'm closest to “${home}” in The Great AI Debate. Where do you sit?`
    : "I took The Great AI Debate. Where do you sit?";
}

/** X's compose page; X adds the link after the text. */
export function xIntentURL(text, url) {
  return `https://x.com/intent/post?text=${encodeURIComponent(text)}${url ? `&url=${encodeURIComponent(url)}` : ""}`;
}

/** Bluesky's compose page takes only text, so the link goes at the end of it. */
export function bskyIntentURL(text, url) {
  return `https://bsky.app/intent/compose?text=${encodeURIComponent(url ? `${text}\n${url}` : text)}`;
}

/** An absolute page address from what the server returned ({code, url?}). */
export function profileURL(profile, origin) {
  if (!profile?.code && !profile?.url) return null;
  try { return new URL(profile.url || `/p/${encodeURIComponent(profile.code)}`, origin).href; } catch { return null; }
}

/** The PUT /api/me/profile body: the same summary and scrambled print the anonymous flow sends. */
export function accountProfileBody(bundle, answers, result, listed = false) {
  const h = highlights(bundle, answers, result);
  return { summary: profileSummary(result, h.rarest), glyph: scrambled(glyphValues(bundle, answers)), listed: Boolean(listed) };
}

export class NotYet extends Error {}

/**
 * Create or refresh the account's page. Resolves {code, url}. Throws NotYet when the server has
 * no such endpoint yet (404/405), so callers can fall back to the anonymous share sheet.
 */
export async function publishAccountProfile(body) {
  let res;
  try {
    res = await fetch("/api/me/profile", { method: "PUT", credentials: "same-origin",
      headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  } catch { throw new Error("Couldn't reach the server. Check your connection and try again."); }
  if (res.status === 404 || res.status === 405) throw new NotYet("Account share links aren't switched on yet.");
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || data.detail || `That didn't work (${res.status}). Try again.`);
  return data;
}

const event = (name) => fetch("/api/event", { method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name }) }).catch(() => {});

/** The link, Copy, and the two compose buttons. `id` keeps element ids unique on a page. */
export function shareLinksHTML(url, text, { id = "sl" } = {}) {
  return `<div class="share-links">
    <label class="small muted" for="${id}-url">Your page</label>
    <div class="linkbox"><input type="text" id="${id}-url" readonly value="${esc(url)}"><button type="button" class="primary" data-copy-link>Copy</button></div>
    <div class="share-pair">
      <a class="button" data-share="x" href="${esc(xIntentURL(text, url))}" target="_blank" rel="noopener">Share on X</a>
      <a class="button" data-share="bsky" href="${esc(bskyIntentURL(text, url))}" target="_blank" rel="noopener">Share on Bluesky</a>
    </div>
  </div>`;
}

export function wireShareLinks(root, url, { toast = () => {} } = {}) {
  const box = root.querySelector(".share-links");
  if (!box) return;
  box.querySelector("[data-copy-link]").onclick = async () => {
    try { await navigator.clipboard.writeText(url); toast("Link copied"); event("copy_link"); }
    catch { const i = box.querySelector("input"); i.focus(); i.select(); }
  };
  for (const a of box.querySelectorAll("[data-share]")) a.addEventListener("click", () => event(`share_${a.dataset.share}`));
}
