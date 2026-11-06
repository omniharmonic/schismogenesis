// An account's Bluesky / X identity, as GET /api/me and GET /api/profiles/{code} give it:
// [{kind: "bsky"|"x", handle, url, description, location, website, followers}]. Made safe here
// (only http(s) links, a real profile address) and drawn the same on the account and profile pages.
import { esc } from "./map.js";

const NETWORK = { bsky: "Bluesky", x: "X" };

function httpURL(u) {
  if (typeof u !== "string" || !u.trim()) return null;
  const raw = /^[a-z][a-z0-9+.-]*:/i.test(u.trim()) ? u.trim() : `https://${u.trim()}`;
  try {
    const url = new URL(raw);
    return url.protocol === "https:" || url.protocol === "http:" ? url : null;
  } catch { return null; }
}

/** One social, cleaned: {kind, network, handle, href, description, location, website, followers}. */
export function cleanSocial(s) {
  if (!s || !NETWORK[s.kind] || typeof s.handle !== "string" || !s.handle.trim()) return null;
  const handle = s.handle.trim().replace(/^@/, "");
  const own = s.kind === "x" ? `https://x.com/${encodeURIComponent(handle)}` : `https://bsky.app/profile/${encodeURIComponent(handle)}`;
  const site = httpURL(s.website);
  return {
    kind: s.kind, network: NETWORK[s.kind], handle,
    href: httpURL(s.url)?.href || own,
    description: typeof s.description === "string" ? s.description.trim() : "",
    location: typeof s.location === "string" ? s.location.trim() : "",
    website: site ? { href: site.href, label: (site.host.replace(/^www\./, "") + site.pathname).replace(/\/$/, "") } : null,
    followers: Number.isFinite(s.followers) && s.followers >= 0 ? s.followers : null,
  };
}

export function cleanSocials(list) {
  return (Array.isArray(list) ? list : []).map(cleanSocial).filter(Boolean);
}

/** The first provider bio, for "Use this" when the account has none. */
export function suggestedBio(socials) {
  const s = cleanSocials(socials).find((x) => x.description);
  return s ? { text: s.description.slice(0, 160), network: s.network } : null;
}

const count = (n) => `${n.toLocaleString("en-US")} ${n === 1 ? "follower" : "followers"}`;

/**
 * The identity block under a name: the bio (the account's own, else the first provider bio),
 * then each network's handle linked to the profile there, with location, website and followers.
 */
export function socialsHTML(socials, { bio = "" } = {}) {
  const list = cleanSocials(socials);
  const text = (bio || "").trim() || list.find((s) => s.description)?.description || "";
  if (!list.length && !text) return "";
  return `<div class="socials">
    ${text ? `<p class="social-bio serif">${esc(text)}</p>` : ""}
    ${list.map((s) => `<p class="social-line small"><span><a href="${esc(s.href)}" target="_blank" rel="noopener nofollow">@${esc(s.handle)}</a> <span class="muted">on ${s.network}</span></span>${s.location ? `<span class="muted">${esc(s.location)}</span>` : ""}${s.website ? `<a href="${esc(s.website.href)}" target="_blank" rel="noopener nofollow ugc">${esc(s.website.label)}</a>` : ""}${s.followers !== null ? `<span class="muted num">${count(s.followers)}</span>` : ""}</p>`).join("")}
  </div>`;
}
