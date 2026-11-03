// Bot protection: fetch a Cloudflare Turnstile token at the moment of a protected action.
// Returns "" when the site runs without Turnstile (local development).
let config = null;
let ready = null;

async function siteKey() {
  if (!config) {
    try { config = await (await fetch("/api/config")).json(); } catch { config = {}; }
  }
  return config.turnstile_site_key || "";
}

function load() {
  ready ||= new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    s.async = true;
    s.onload = () => resolve(window.turnstile);
    s.onerror = () => reject(new Error("Couldn't load the bot check. Check your connection and try again."));
    document.head.append(s);
  });
  return ready;
}

export async function humanToken() {
  const key = await siteKey();
  if (!key) return "";
  const turnstile = await load();
  return new Promise((resolve, reject) => {
    const box = document.createElement("div");
    box.className = "turnstile-box";
    document.body.append(box);
    const id = turnstile.render(box, {
      sitekey: key,
      appearance: "interaction-only",  // invisible unless Cloudflare needs a click
      callback: (token) => { resolve(token); setTimeout(() => { turnstile.remove(id); box.remove(); }, 0); },
      "error-callback": () => { box.remove(); reject(new Error("The bot check failed. Please try again.")); },
    });
  });
}

/** fetch() with the bot-check header added. */
export async function protectedFetch(url, options = {}) {
  const token = await humanToken();
  return fetch(url, { ...options, headers: { ...(options.headers || {}), ...(token ? { "X-Turnstile": token } : {}) } });
}
