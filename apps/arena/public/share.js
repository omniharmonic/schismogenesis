// The share sheet: publish a profile link (anonymous, or verified Bluesky or X), then share it.
// Nothing is sent until the person presses "Create my link" after seeing what it will show.
import { canvasBlob, drawCard, shareText } from "./card.js";
import { highlights, profileSummary } from "./fingerprint.js";
import { glyphValues, scrambled } from "./glyph.js";
import { esc } from "./map.js";
import { humanToken } from "./turnstile.js";

const KEY = "fp.profile";
const PENDING = "fp.pending-share";
const local = {
  get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode */ } },
  drop(k) { try { localStorage.removeItem(k); } catch { /* ignore */ } },
};
const event = (name) => fetch("/api/event", { method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name }) }).catch(() => {});

const PROTECTED = new Set(["/api/profiles", "/api/verify/bsky/start"]);

async function api(path, opts = {}) {
  const extra = {};
  if (opts.method === "POST" && PROTECTED.has(path)) {
    const token = await humanToken();
    if (token) extra["X-Turnstile"] = token;
  }
  const res = await fetch(path, { ...opts, headers: { "Content-Type": "application/json", ...extra, ...(opts.headers || {}) } });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
  return data;
}

export function savedProfile() { return local.get(KEY); }

export async function openShare({ bundle, answers, result, toast, verified = null }) {
  const values = glyphValues(bundle, answers);
  const h = highlights(bundle, answers, result);
  const pending = local.get(PENDING);
  const state = {
    identity: verified ? verified.kind : pending?.identity || "anon",
    include: pending?.include || "result",
    listed: pending?.listed ?? false,
    check: verified,
    options: { bsky: true, x: false },
  };
  local.drop(PENDING);
  try { state.options = await api("/api/verify/options"); } catch { /* defaults */ }

  const dialog = document.createElement("dialog");
  dialog.className = "sheet";
  dialog.setAttribute("aria-label", "Share your fingerprint");
  document.body.append(dialog);
  dialog.addEventListener("close", () => dialog.remove());

  function publishedView(p) {
    const url = `${location.origin}/p/${p.code}`;
    const text = shareText(result, url);
    dialog.innerHTML = `<div class="sheet-body">
      <h2>Your link is live</h2>
      <div class="linkbox"><input type="text" readonly value="${esc(url)}" aria-label="Your share link"><button class="primary" id="copy-link">Copy</button></div>
      <div class="share-grid">
        <button id="native">Share…</button>
        <button id="post-x">Post on X</button>
        <button id="post-bsky">Post on Bluesky</button>
        <button id="card">Save image</button>
      </div>
      <p class="small muted">Posts show a preview card with your print and nearest thinkers.</p>
      ${p.identity && p.identity !== "anon" ? `<label class="gate"><input type="checkbox" id="listed" ${p.listed ? "checked" : ""}> <span>List me in the public directory of fingerprints</span></label>` : ""}
      <div class="row" style="margin-top:14px">
        <a class="button" href="/p/${esc(p.code)}" target="_blank" rel="noopener">View my page</a>
        <button class="link-button" id="replace">Make a new link</button>
        <button class="link-button" id="delete">Delete this link</button>
        <button class="link-button" id="close">Close</button>
      </div></div>`;
    const $ = (s) => dialog.querySelector(s);
    $("#copy-link").onclick = async () => { try { await navigator.clipboard.writeText(url); toast("Link copied"); event("copy_link"); } catch { $("input").select(); } };
    $("#native").hidden = !navigator.share;
    $("#native").onclick = async () => { try { await navigator.share({ title: "My AI futures fingerprint", text: shareText(result), url }); event("share_native"); } catch { /* cancelled */ } };
    $("#post-x").onclick = () => { window.open(`https://x.com/intent/post?text=${encodeURIComponent(shareText(result))}&url=${encodeURIComponent(url)}`, "_blank", "noopener"); event("share_x"); };
    $("#post-bsky").onclick = () => { window.open(`https://bsky.app/intent/compose?text=${encodeURIComponent(text)}`, "_blank", "noopener"); event("share_bsky"); };
    $("#card").onclick = async () => {
      const blob = await canvasBlob(drawCard(document.createElement("canvas"), values, result, { thinkers: bundle.thinkers.length }));
      const a = document.createElement("a"); a.download = "ai-futures-fingerprint.png"; a.href = URL.createObjectURL(blob); a.click();
      event("save_card");
    };
    $("#close").onclick = () => dialog.close();
    $("#replace").onclick = () => choose();
    if ($("#listed")) $("#listed").onchange = async (e) => {
      try {
        await api(`/api/profiles/${p.code}`, { method: "PATCH", headers: { "X-Edit-Key": p.edit_key }, body: JSON.stringify({ listed: e.target.checked }) });
        local.set(KEY, { ...p, listed: e.target.checked });
        toast(e.target.checked ? "Listed in the directory" : "Removed from the directory");
      } catch (err) { toast(err.message); e.target.checked = !e.target.checked; }
    };
    $("#delete").onclick = async () => {
      if (!confirm("Delete your share link? Anyone who opens it will see nothing.")) return;
      try { await api(`/api/profiles/${p.code}`, { method: "DELETE", headers: { "X-Edit-Key": p.edit_key } }); } catch { /* already gone */ }
      local.drop(KEY);
      toast("Link deleted");
      dialog.close();
    };
  }

  function preview() {
    const s = result;
    const items = [
      `Your neighbourhood: the ${s.schools[0].label}`,
      `Nearest: ${s.nearest.map((t) => `${t.name} (${t.k} of ${t.n})`).join(", ")}`,
      `Furthest: ${s.furthest.map((t) => t.name).join(", ")}`,
      ...s.signature.map((t) => `Your answer on: “${t.text}”`),
      h.rarest ? `Your rarest take, with your answer: “${h.rarest.text}”` : null,
      "Your camp splits, and a print drawn from your answers in a scrambled order",
      state.include === "answers" ? "All your answers, statement by statement" : null,
    ].filter(Boolean);
    return `<ul class="small">${items.map((i) => `<li>${esc(i)}</li>`).join("")}</ul>`;
  }

  function verifyBlock() {
    if (state.identity === "anon") return `<p class="small muted">You'll appear as a generated name like “Fingerprint K7Q2”.</p>`;
    if (state.check) {
      return `<div class="who">${state.check.avatar_url ? `<img src="${esc(state.check.avatar_url)}" alt="">` : `<span class="avatar"></span>`}
        <div><b>${esc(state.check.display_name || state.check.handle)}</b><br><span class="small muted">@${esc(state.check.handle)}, verified</span></div></div>`;
    }
    if (state.identity === "x") {
      return `<p class="small">We'll ask X to confirm the account is yours. We only read your name, handle and picture, and keep nothing else.</p>
        <button class="primary" id="x-go">Sign in with X</button>`;
    }
    if (state.bsky) {
      const post = `Verifying my AI Futures Fingerprint: ${state.bsky.code}`;
      return `<p class="small">Post this from <b>@${esc(state.bsky.handle)}</b>. You can delete the post once you're verified.</p>
        <p><span class="code">${esc(state.bsky.code)}</span></p>
        <div class="row"><a class="button" target="_blank" rel="noopener" href="https://bsky.app/intent/compose?text=${encodeURIComponent(post)}">Post it on Bluesky</a>
        <button class="primary" id="bsky-check">I've posted it</button></div><p class="small" id="bsky-msg" role="status"></p>`;
    }
    return `<label class="small" for="bsky-handle">Your Bluesky handle</label>
      <div class="linkbox"><input type="text" id="bsky-handle" placeholder="you.bsky.social" autocomplete="off"><button class="primary" id="bsky-start">Get my code</button></div>
      <p class="small error" id="bsky-msg" role="status"></p>`;
  }

  function choose() {
    const canPublish = state.identity === "anon" || !!state.check;
    dialog.innerHTML = `<div class="sheet-body">
      <h2>Get your share link</h2>
      <p class="muted">A page with your result and a preview card for posts. You can delete it any time from this browser.</p>
      <h3>Show it as</h3>
      <div class="choice" role="radiogroup">
        <label><input type="radio" name="who" value="anon" ${state.identity === "anon" ? "checked" : ""}><span>Anonymous<small>A generated name. Nothing links it to you.</small></span></label>
        <label><input type="radio" name="who" value="bsky" ${state.identity === "bsky" ? "checked" : ""}><span>My Bluesky account<small>Verified with a one-time code you post. Shows your name and picture.</small></span></label>
        ${state.options.x ? `<label><input type="radio" name="who" value="x" ${state.identity === "x" ? "checked" : ""}><span>My X account<small>Verified by signing in with X. Shows your name and picture.</small></span></label>` : ""}
      </div>
      <div id="verify">${verifyBlock()}</div>
      <h3 style="margin-top:20px">Include</h3>
      <div class="choice" role="radiogroup">
        <label><input type="radio" name="inc" value="result" ${state.include === "result" ? "checked" : ""}><span>My result<small>Neighbourhood, matches, plot twist, camps and rarest take.</small></span></label>
        <label><input type="radio" name="inc" value="answers" ${state.include === "answers" ? "checked" : ""}><span>My result and every answer<small>Lets others compare with you statement by statement.</small></span></label>
      </div>
      ${state.identity !== "anon" ? `<label class="gate"><input type="checkbox" id="list" ${state.listed ? "checked" : ""}> <span>Also list me in the public directory</span></label>` : ""}
      <details><summary class="small">What the page will show</summary>${preview()}</details>
      <div class="row" style="margin-top:18px"><button class="primary" id="publish" ${canPublish ? "" : "disabled"}>Create my link</button><button class="link-button" id="close">Not now</button></div>
      <p class="small error" id="publish-msg" role="status"></p></div>`;
    const $ = (s) => dialog.querySelector(s);
    dialog.querySelectorAll("input[name=who]").forEach((r) => (r.onchange = () => {
      state.identity = r.value;
      if (state.check && state.check.kind !== r.value) state.check = null;
      choose();
    }));
    dialog.querySelectorAll("input[name=inc]").forEach((r) => (r.onchange = () => { state.include = r.value; choose(); }));
    if ($("#list")) $("#list").onchange = (e) => (state.listed = e.target.checked);
    $("#close").onclick = () => dialog.close();
    if ($("#x-go")) $("#x-go").onclick = () => {
      local.set(PENDING, { identity: "x", include: state.include, listed: state.listed });
      location.href = "/auth/x/start";
    };
    if ($("#bsky-start")) $("#bsky-start").onclick = async () => {
      try {
        const r = await api("/api/verify/bsky/start", { method: "POST", body: JSON.stringify({ handle: $("#bsky-handle").value }) });
        state.bsky = r; choose();
      } catch (e) { $("#bsky-msg").textContent = e.message; }
    };
    if ($("#bsky-check")) $("#bsky-check").onclick = async () => {
      $("#bsky-msg").className = "small"; $("#bsky-msg").textContent = "Checking your recent posts…";
      try {
        const r = await api("/api/verify/bsky/check", { method: "POST", body: JSON.stringify({ check_id: state.bsky.check_id }) });
        if (!r.verified) { $("#bsky-msg").className = "small error"; $("#bsky-msg").textContent = "We couldn't find the code in your latest posts yet. Bluesky can take a minute; try again."; return; }
        state.check = { kind: "bsky", check_id: state.bsky.check_id, ...r }; choose();
      } catch (e) { $("#bsky-msg").className = "small error"; $("#bsky-msg").textContent = e.message; }
    };
    $("#publish").onclick = async () => {
      $("#publish").disabled = true;
      try {
        const body = {
          summary: profileSummary(result, h.rarest),
          glyph: state.include === "answers" ? values : scrambled(values),
          answers: state.include === "answers" ? answers : null,
          identity: state.identity,
          check_id: state.check?.check_id || null,
          listed: state.identity !== "anon" && state.listed,
        };
        const r = await api("/api/profiles", { method: "POST", body: JSON.stringify(body) });
        const saved = { code: r.code, edit_key: r.edit_key, identity: state.identity, listed: body.listed };
        local.set(KEY, saved);
        publishedView(saved);
      } catch (e) { $("#publish-msg").textContent = e.message; $("#publish").disabled = false; }
    };
  }

  const existing = local.get(KEY);
  if (existing && !verified) publishedView(existing); else choose();
  dialog.showModal();
}
