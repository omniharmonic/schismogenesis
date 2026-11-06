// The top bar's "You": when signed in, your picture (accessible name stays "You") linking to your
// results on the account page. Loaded on every page through site-config.js. The one GET /api/me
// it makes is handed to auth.js's first getMe(), so a page asks once.

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

/** Which account tab a hash opens: "#settings" is Settings; anything else is Your results. */
export function tabFromHash(hash) {
  const h = String(hash || "").replace(/^#/, "").toLowerCase();
  return h === "settings" ? "settings" : "results";
}

let first = null;
/** The page's first look at /api/me (account or null). Null outside a browser. */
export function initialMe() {
  if (typeof fetch === "undefined" || typeof document === "undefined") return null;
  first ||= fetch("/api/me", { credentials: "same-origin" })
    .then((r) => (r.ok ? r.json() : null))
    .then((d) => d?.account || null)
    .catch(() => null);
  return first;
}

/** Only http(s) pictures go in an <img>. */
const picture = (u) => (typeof u === "string" && /^https:\/\//i.test(u) ? u : null);

/** Paint the nav's "You" for this account (or signed out). */
export function paintNavYou(account) {
  if (typeof document === "undefined") return;
  const link = document.querySelector('.top-nav a[href^="/account.html"]');
  if (!link) return;
  const src = account ? picture(account.avatar_url) : null;
  link.href = account ? "/account.html#results" : "/account.html";
  if (src) {
    link.classList.add("nav-you");
    link.setAttribute("aria-label", "You");
    link.innerHTML = `<img class="nav-avatar" src="${esc(src)}" alt="" referrerpolicy="no-referrer" width="28" height="28">`;
    // a broken picture falls back to the word
    link.querySelector("img").addEventListener("error", () => paintNavYou({ ...account, avatar_url: null }), { once: true });
  } else {
    link.classList.remove("nav-you");
    link.removeAttribute("aria-label");
    link.textContent = "You";
  }
}

if (typeof document !== "undefined") initialMe()?.then(paintNavYou);
