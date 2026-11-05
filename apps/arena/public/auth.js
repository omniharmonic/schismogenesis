// Accounts: who is signed in, the four ways in (Bluesky, X, email, a private key), and saving
// answers to the account. Used by the account page and by the survey's "Save your answers" panel.
// The session is an httpOnly cookie the server sets; nothing about it lives in this script.
import { esc } from "./map.js";

const KEY_USER = "antimemes.is"; // the name a password manager files the private key under

export class ApiError extends Error {
  constructor(message, status) { super(message); this.status = status; }
}

/** JSON request to our own API. Throws ApiError with the server's message, or a plain one. */
export async function api(path, { method = "GET", body } = {}) {
  let res;
  try {
    res = await fetch(path, {
      method, credentials: "same-origin",
      headers: body === undefined ? {} : { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch { throw new ApiError("Couldn't reach the server. Check your connection and try again.", 0); }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new ApiError(data.error || data.detail || `That didn't work (${res.status}). Try again.`, res.status);
  return data;
}

/** The signed-in account, or null. A missing endpoint (404) or any failure counts as signed out. */
export async function getMe() {
  try {
    const res = await fetch("/api/me", { credentials: "same-origin" });
    if (!res.ok) return null;
    const data = await res.json();
    return data?.account || null;
  } catch { return null; }
}

/** Only the three valid answers go to the server. */
export function cleanAnswers(answers) {
  return Object.fromEntries(Object.entries(answers || {}).filter(([, v]) => v === 1 || v === -1 || v === 0));
}

/** Sign-ins that leave the site come back to the account page when they started there. */
const fromAccount = (sep = "?") => (location.pathname.startsWith("/account") ? `${sep}next=account` : "");

export function saveAnswers(answers) {
  // if this browser already added its answers to the results anonymously, the account takes
  // over that entry instead of being counted a second time
  let room = null;
  try { room = JSON.parse(localStorage.getItem("fp.room.ai-futures") || "null"); } catch { /* none */ }
  const body = { answers: cleanAnswers(answers) };
  if (room?.participant_id && room?.key) body.room = { participant_id: room.participant_id, key: room.key };
  return api("/api/me/answers", { method: "PUT", body });
}

/**
 * Which copy of the answers to use when the browser and the account both have one: the
 * account's wins when the browser has none, or when the browser's is older (or undated, which
 * means it was saved before accounts existed). Returns "local", "server" or "none".
 */
export function pickAnswers(local, sheet, season) {
  const hasLocal = local && local.season === season && Object.keys(local.answers || {}).length > 0;
  const hasSheet = sheet && sheet.season === season && Object.keys(sheet.answers || {}).length > 0;
  if (!hasSheet) return hasLocal ? "local" : "none";
  if (!hasLocal) return "server";
  const lt = Date.parse(local.updated_at || ""), st = Date.parse(sheet.updated_at || "");
  if (!Number.isFinite(lt)) return "server";
  if (!Number.isFinite(st)) return "local";
  return lt > st ? "local" : "server";
}

export function initials(name) {
  return String(name || "").trim().split(/\s+/).slice(0, 2).map((w) => w[0] || "").join("").toUpperCase() || "?";
}

export const LOGIN_NAME = { bsky: "Bluesky", x: "X", email: "Email", key: "Private key" };

export function toast(text) {
  const t = document.createElement("div");
  t.className = "toast"; t.setAttribute("role", "status"); t.textContent = text;
  document.body.append(t); setTimeout(() => t.remove(), Math.max(2600, text.length * 55));
}

const FAILED = {
  handle: "Couldn't sign in: we couldn't find that Bluesky handle.",
  bsky: "Couldn't sign in: Bluesky didn't confirm it. Try again.",
  x: "Couldn't sign in: X didn't confirm it. Try again.",
  "x-off": "Couldn't sign in: signing in with X isn't switched on yet.",
  expired: "Couldn't sign in: that sign-in expired. Try again.",
};

/** What a #signin=failed&why=… return should say. Exported for tests. */
export function failureMessage(hash) {
  const why = new URLSearchParams(String(hash || "").replace(/^#/, "")).get("why");
  return FAILED[why] || "Couldn't sign in";
}

/**
 * Read and clear a sign-in return: #signed-in, or #signin=failed&why=… . Returns null, or
 * { ok: true }, or { ok: false, message }.
 */
export function takeSignInHash() {
  const h = location.hash;
  const ok = h === "#signed-in", failed = h.startsWith("#signin=failed");
  if (!ok && !failed) return null;
  history.replaceState(null, "", location.pathname + location.search);
  return ok ? { ok: true } : { ok: false, message: failureMessage(h) };
}

let xOption = null;
/** Whether "Sign in with X" is set up on this server (GET /api/verify/options → x: true). */
export function xAvailable() {
  xOption ||= fetch("/api/verify/options").then((r) => (r.ok ? r.json() : {})).then((o) => o.x === true).catch(() => false);
  return xOption;
}

/**
 * The four ways in. Bluesky and X leave the page and come back to /#signed-in. `id` keeps
 * element ids unique if two sets are on a page.
 */
export function signInHTML({ id = "si", x = false } = {}) {
  return `<div class="signin" data-signin="${esc(id)}">
    <form class="si-way" data-way="bsky">
      <h3>Bluesky</h3>
      <label class="small" for="${id}-bsky">Your Bluesky handle</label>
      <div class="si-inline"><input type="text" id="${id}-bsky" name="handle" required autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="you.bsky.social">
      <button class="primary" type="submit">Sign in with Bluesky</button></div>
      <p class="small muted">Bluesky asks you to approve it, then sends you back here. With a Bluesky sign-in your picture can appear on the map.</p>
    </form>
    ${x ? `<div class="si-way" data-way="x">
      <h3>X</h3>
      <a class="button" href="/auth/x/signin${fromAccount()}">Sign in with X</a>
      <p class="small muted">X asks you to approve it, then sends you back here. With an X sign-in your picture can appear on the map.</p>
    </div>` : ""}
    <form class="si-way" data-way="email">
      <h3>Email</h3>
      <div data-step="address">
        <label class="small" for="${id}-email">Your email address</label>
        <div class="si-inline"><input type="email" id="${id}-email" name="email" required autocomplete="email" inputmode="email" spellcheck="false">
        <button type="submit">Email me a link</button></div>
        <p class="small muted">We send a sign-in link and a 6-digit code. Your address is never shown to anyone.</p>
      </div>
      <div data-step="code" hidden>
        <p class="small" data-sent></p>
        <label class="small" for="${id}-code">6-digit code</label>
        <div class="si-inline"><input type="text" id="${id}-code" name="code" inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]{6}" maxlength="6">
        <button class="primary" type="submit">Sign in</button></div>
        <button class="link-button small" type="button" data-restart>Use a different address</button>
      </div>
    </form>
    <div class="si-way" data-way="key">
      <h3>A private key</h3>
      <p class="small muted">No email or social account. We make a long key and your browser's password manager keeps it. Lose the key and the account can't be recovered.</p>
      <div class="row" data-key-start><button type="button" data-key-new>Make me a key</button><button type="button" class="link-button" data-key-have>I have a key</button></div>
      <div data-key-area></div>
    </div>
    <p class="small error si-msg" role="alert" hidden></p>
  </div>`;
}

const keySaveHTML = (key) => `<form class="key-save" data-key-save>
    <p><b>Your key.</b> This is the only time it is shown. Save it now.</p>
    <label class="small" for="ks-user">Saved under</label>
    <input type="text" id="ks-user" name="username" value="${KEY_USER}" autocomplete="username" readonly class="ks-user">
    <label class="small" for="ks-key">Private key</label>
    <div class="si-inline"><input type="password" id="ks-key" name="password" value="${esc(key)}" autocomplete="new-password" readonly spellcheck="false">
    <button type="button" data-key-show aria-pressed="false">Show</button></div>
    <div class="row" style="margin-top:12px"><button class="primary" type="submit">Save to my password manager</button><button type="button" data-key-copy>Copy key</button></div>
    <p class="small muted">You're signed in. To sign in on another device, use "I have a key" and let your password manager fill it in.</p>
  </form>`;

const keyUseHTML = () => `<form class="key-use" data-key-use>
    <label class="small" for="ku-user">Saved under</label>
    <input type="text" id="ku-user" name="username" value="${KEY_USER}" autocomplete="username" class="ks-user">
    <label class="small" for="ku-key">Private key</label>
    <input type="password" id="ku-key" name="password" required autocomplete="current-password" spellcheck="false">
    <div class="row" style="margin-top:12px"><button class="primary" type="submit">Sign in with my key</button></div>
  </form>`;

/**
 * Make a sign-in block work. `onSignedIn()` runs after a same-page sign-in (email code or key);
 * Bluesky and X leave the page and come back with #signed-in. A new key signs in at once
 * (onSignedIn("key-new")), but the key stays on screen until the person has saved it; then
 * `onKeySaved()` runs, so the caller can redraw.
 */
export function wireSignIn(root, { onSignedIn, onKeySaved = null }) {
  const msg = root.querySelector(".si-msg");
  const say = (text) => { msg.textContent = text || ""; msg.hidden = !text; };
  const busy = (form, on) => form.querySelectorAll("button, input").forEach((el) => { if (el.type === "submit") el.disabled = on; });

  // Bluesky: hand over to the person's own authorisation server
  const bsky = root.querySelector('[data-way="bsky"]');
  bsky.addEventListener("submit", (e) => {
    e.preventDefault();
    const input = bsky.querySelector("input");
    const handle = input.value.trim().replace(/^@/, "");
    if (!handle) return;
    location.href = `/auth/bsky/start?handle=${encodeURIComponent(handle)}${fromAccount("&")}`;
  });

  // email: address, then the code (or the link in the email)
  const email = root.querySelector('[data-way="email"]');
  const step = (name) => email.querySelectorAll("[data-step]").forEach((s) => (s.hidden = s.dataset.step !== name));
  let address = "";
  email.addEventListener("submit", async (e) => {
    e.preventDefault();
    say("");
    const codeStep = !email.querySelector('[data-step="code"]').hidden;
    busy(email, true);
    try {
      if (!codeStep) {
        address = email.querySelector('input[name="email"]').value.trim();
        if (!address) return;
        await api("/api/auth/email/start", { method: "POST", body: { email: address } });
        email.querySelector("[data-sent]").textContent = `We sent a link and a code to ${address}. Open the link on this device, or type the code here. It can take a minute.`;
        step("code");
        email.querySelector('input[name="code"]').focus();
      } else {
        const code = email.querySelector('input[name="code"]').value.replace(/\D/g, "");
        if (code.length !== 6) { say("The code is 6 digits."); return; }
        await api("/api/auth/email/code", { method: "POST", body: { email: address, code } });
        await onSignedIn?.("email");
      }
    } catch (err) {
      say(err.status === 404 ? "Email sign-in isn't switched on yet. Try another way." : err.message);
    } finally { busy(email, false); }
  });
  email.querySelector("[data-restart]").onclick = () => { step("address"); say(""); email.querySelector('input[name="email"]').focus(); };

  // a private key: made here and saved by the browser, or typed or filled in from a saved one
  const keyWay = root.querySelector('[data-way="key"]');
  const area = keyWay.querySelector("[data-key-area]");
  keyWay.querySelector("[data-key-new]").onclick = async (e) => {
    say("");
    e.target.disabled = true;
    let key;
    try { ({ key } = await api("/api/auth/key/new", { method: "POST", body: {} })); }
    catch (err) { e.target.disabled = false; say(err.status === 404 ? "Key sign-in isn't switched on yet. Try another way." : err.message); return; }
    keyWay.querySelector("[data-key-start]").hidden = true;
    area.innerHTML = keySaveHTML(key);
    const form = area.querySelector("[data-key-save]");
    const field = form.querySelector("#ks-key");
    form.querySelector("[data-key-show]").onclick = (ev) => {
      const show = field.type === "password";
      field.type = show ? "text" : "password";
      ev.target.textContent = show ? "Hide" : "Show";
      ev.target.setAttribute("aria-pressed", String(show));
    };
    form.querySelector("[data-key-copy]").onclick = async () => {
      try { await navigator.clipboard.writeText(key); toast("Key copied. Keep it somewhere safe."); }
      catch { field.type = "text"; field.select(); }
    };
    form.addEventListener("submit", async (ev) => {
      // the submit itself is what prompts most password managers; Chrome also takes the
      // Credential Management API. Nothing is sent anywhere.
      ev.preventDefault();
      field.type = "password";
      try {
        if ("PasswordCredential" in window && navigator.credentials?.store) {
          await navigator.credentials.store(new window.PasswordCredential({ id: KEY_USER, password: key, name: "antimemes" }));
        }
      } catch { /* the browser declined; the form submit still offers to save */ }
      setTimeout(() => {
        form.outerHTML = `<div class="key-done"><p class="small">If your browser offered to save the key and you said yes, you're set. If it didn't, copy the key now and keep it somewhere safe: it won't be shown again.</p>
          <div class="row"><button type="button" class="primary" data-key-done>Done</button><button type="button" data-key-copy2>Copy key</button></div></div>`;
        const done = area.querySelector("[data-key-done]");
        area.querySelector("[data-key-copy2]").onclick = async () => {
          try { await navigator.clipboard.writeText(key); toast("Key copied. Keep it somewhere safe."); } catch { toast("Copy didn't work in this browser."); }
        };
        done.focus();
        done.onclick = () => onKeySaved?.();
      }, 400);
    });
    await onSignedIn?.("key-new");
  };
  keyWay.querySelector("[data-key-have]").onclick = () => {
    keyWay.querySelector("[data-key-start]").hidden = true;
    area.innerHTML = keyUseHTML();
    const form = area.querySelector("[data-key-use]");
    form.querySelector("#ku-key").focus();
    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      say("");
      busy(form, true);
      try {
        await api("/api/auth/key", { method: "POST", body: { key: form.querySelector("#ku-key").value.trim() } });
        await onSignedIn?.("key");
      } catch (err) {
        say(err.status === 401 || err.status === 403 ? "That key didn't match an account." : err.status === 404 ? "Key sign-in isn't switched on yet. Try another way." : err.message);
      } finally { busy(form, false); }
    });
  };
}
