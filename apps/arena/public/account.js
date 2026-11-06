// The account page ("You"). Signed out: the ways in. Signed in: two tabs, Your results (your full
// result from the account's saved answers, your share link, your statements) and Settings (name
// and bio, the map switch, ways in, leaving). #results and #settings pick the tab.
import { esc } from "./map.js";
import { LOGIN_NAME, api, getMe, initials, paintNavYou, saveAnswers, signInHTML, takeSignInHash, toast, wireSignIn, xAvailable } from "./auth.js";
import { tabFromHash } from "./nav.js";
import { fingerprint } from "./placement.js";
import { resultHTML, wireResult } from "./result-view.js";
import { socialsHTML, suggestedBio } from "./socials.js";
import { NotYet, accountProfileBody, profileURL, publishAccountProfile, shareLine, shareLinksHTML, wireShareLinks } from "./share-links.js";
import { loadBundle, mountNaming } from "./camp-names.js";
import { bridgeSummary, nextStepHTML } from "./next-step.js";
import "./site-config.js";

const local = {
  get() { try { return JSON.parse(localStorage.getItem("fp.answers")); } catch { return null; } },
  set(v) { try { localStorage.setItem("fp.answers", JSON.stringify(v)); } catch { /* private mode */ } },
};

let bundlePromise = null;
const getBundle = () => (bundlePromise ||= loadBundle("/fingerprint.json"));

// ---------- pure pieces (tests/share.test.mjs) ----------

const STATUS = { pending: "Waiting for review", hidden: "Hidden by a moderator", rejected: "Not accepted", removed: "Removed" };
const SHOWN = new Set(["approved", "active", "live", "visible", "shown", "published", ""]);

// bridge: "passed" = people in different groups agree with it; "leaning" = on its way there
export const BRIDGE = { passed: "Bridges the groups", leaning: "Leaning toward a bridge" };
const BRIDGE_RANK = { passed: 2, leaning: 1 };

/** The numbers for a statement I wrote: the votes, and (if the server gives it) how many groups agree. */
export function statementNumbers(s) {
  const n = (v) => (Number.isFinite(v) ? v : 0);
  const votes = [`${n(s.agree)} agree`, `${n(s.disagree)} disagree`, `${n(s.pass)} pass`].join(", ");
  if (!Number.isFinite(s.groups_agreeing)) return { votes, groups: "" };
  const g = s.groups_agreeing;
  return { votes, groups: g === 0 ? "No group agrees yet" : g === 1 ? "1 group agrees" : `${g} groups agree` };
}

export function statementsHTML(list) {
  const total = (s) => (Number(s.agree) || 0) + (Number(s.disagree) || 0) + (Number(s.pass) || 0);
  const rows = [...(list || [])].filter((s) => s && typeof s.text === "string")
    .sort((a, b) => (BRIDGE_RANK[b.bridge] || 0) - (BRIDGE_RANK[a.bridge] || 0) || total(b) - total(a));
  if (!rows.length) return "";
  const summary = bridgeSummary(rows);
  return `${summary ? `<p class="bridge-summary${rows.some((s) => s.bridge === "passed") ? " has-bridge" : ""}">${summary}</p>` : ""}<ul class="my-statements">${rows.map((s) => {
    const { votes, groups } = statementNumbers(s);
    const status = String(s.status || "").toLowerCase();
    const flag = SHOWN.has(status) ? "" : `<span class="chip unsure">${esc(STATUS[status] || s.status)}</span>`;
    const bridge = BRIDGE[s.bridge] ? `<span class="chip bridge-${esc(s.bridge)}">${BRIDGE[s.bridge]}</span>` : "";
    return `<li${BRIDGE[s.bridge] ? ` class="is-${esc(s.bridge)}"` : ""}><p class="serif my-statement">${esc(s.text)}</p>
      <p class="small muted my-statement-meta">${flag}${bridge}${groups ? `<span><b>${groups}</b></span>` : ""}<span>${votes}</span></p></li>`;
  }).join("")}</ul>`;
}

// ---------- the page ----------

const el = typeof document !== "undefined" ? document.getElementById("account") : null;

// answers this browser has for the current season go up to the account after a sign-in
async function uploadLocal(account) {
  const saved = local.get();
  if (!saved?.answers || !Object.keys(saved.answers).length) return;
  let season = null;
  try { season = (await getBundle()).season; } catch { return; }
  if (saved.season !== season) return;
  const sheet = account?.sheet;
  if (sheet?.season === season && Date.parse(sheet.updated_at || "") >= Date.parse(saved.updated_at || "")) return;
  try { await saveAnswers(saved.answers); } catch { /* the survey page tries again next time */ }
}

async function signedIn() {
  const account = await getMe();
  if (!account) { toast("Couldn't sign in"); return; }
  await uploadLocal(account);
  toast("Signed in");
  render(await getMe() || account);
}

async function renderSignedOut() {
  paintNavYou(null);
  const x = await xAvailable();
  el.innerHTML = `<h1>You</h1>
    <p class="serif lede">Sign in to come back on any device and change your answers, and, if you want, to put your picture on the map.</p>
    <p class="muted">Pick any way in. They all reach the same account, and you can add more later.</p>
    ${signInHTML({ id: "acc", x })}
    <p class="small muted">Signing in is optional. Without it, your answers stay in this browser only. <a href="/privacy.html">Privacy</a></p>`;
  wireSignIn(el.querySelector(".signin"), {
    onSignedIn: async (how) => { if (how !== "key-new") await signedIn(); else { const a = await getMe(); if (a) await uploadLocal(a); } },
    onKeySaved: () => signedIn(),
  });
}

function avatarHTML(a) {
  return a.avatar_url
    ? `<img class="acc-avatar" src="${esc(a.avatar_url)}" alt="" referrerpolicy="no-referrer">`
    : `<span class="acc-avatar" aria-hidden="true">${esc(initials(a.display_name))}</span>`;
}

let onHash = null;

function render(a) {
  a.logins ||= [];
  a.socials ||= [];
  paintNavYou(a);
  el.innerHTML = `<div class="acc-layout">
    <nav class="acc-tabs" aria-label="Your account">
      <a href="#results" data-tab="results">Your results</a>
      <a href="#settings" data-tab="settings">Settings</a>
    </nav>
    <div class="acc-panes">
      <section class="acc-pane" id="pane-results" data-pane="results" aria-label="Your results" hidden></section>
      <section class="acc-pane" id="pane-settings" data-pane="settings" aria-label="Settings" hidden></section>
    </div>
  </div>`;
  const drawn = new Set();
  const show = (tab, { focus = false } = {}) => {
    for (const link of el.querySelectorAll("[data-tab]")) {
      if (link.dataset.tab === tab) link.setAttribute("aria-current", "page"); else link.removeAttribute("aria-current");
    }
    for (const pane of el.querySelectorAll("[data-pane]")) pane.hidden = pane.dataset.pane !== tab;
    if (!drawn.has(tab)) {
      drawn.add(tab);
      if (tab === "results") renderResults(a, el.querySelector("#pane-results"));
      else renderSettings(a, el.querySelector("#pane-settings"));
    }
    if (focus) el.querySelector(`[data-pane="${tab}"] h1`)?.focus({ preventScroll: true });
  };
  if (onHash) removeEventListener("hashchange", onHash);
  onHash = () => { show(tabFromHash(location.hash), { focus: true }); };
  addEventListener("hashchange", onHash);
  show(tabFromHash(location.hash));
}

// ---------- Your results ----------

function identityHTML(a) {
  return `<div class="acc-head">${avatarHTML(a)}<div class="acc-who">
      <h1 class="acc-name" tabindex="-1">${esc(a.display_name || "No name yet")}</h1>
      ${socialsHTML(a.socials, { bio: a.bio })}
    </div></div>`;
}

async function renderResults(a, pane) {
  pane.innerHTML = `${identityHTML(a)}<p class="muted">Loading your results…</p>`;
  let bundle;
  try { bundle = await getBundle(); } catch { pane.innerHTML = `${identityHTML(a)}<p class="error">Couldn't load the statements. Reload the page to try again.</p>`; return; }
  const ids = new Set(bundle.anchors.map((x) => x.id));
  const sheet = a.sheet?.season === bundle.season ? a.sheet : null;
  const answers = Object.fromEntries(Object.entries(sheet?.answers || {}).filter(([id, v]) => ids.has(id) && [1, -1, 0].includes(v)));
  const result = Object.keys(answers).length ? fingerprint(bundle, answers) : null;

  if (!result) {
    pane.innerHTML = `${identityHTML(a)}
      <div class="room-card acc-invite">
        <h2>Take the survey</h2>
        <p>Answer ${bundle.anchors.length} statements about AI's future with the names hidden. Then see which of ${bundle.thinkers.length} public thinkers you agree with, and where you sit on the map. Your answers save to this account as you go.</p>
        <div class="row"><a class="button primary" href="/">Take the survey</a></div>
      </div>`;
    return;
  }
  if (result.status !== "ok") {
    pane.innerHTML = `${identityHTML(a)}
      <div class="room-card acc-invite">
        <h2>Not enough to place you yet</h2>
        <p>You've taken a side on ${result.answered} statements. We need at least ${result.needed} before comparing you with anyone.</p>
        <div class="row"><button class="primary" type="button" data-change>Answer more</button></div>
      </div>`;
    pane.querySelector("[data-change]").onclick = () => changeAnswers(sheet);
    return;
  }

  const saved = new Date(sheet.updated_at);
  pane.innerHTML = `${identityHTML(a)}
    <section class="acc-share bracketed" aria-labelledby="share-title">
      <h2 id="share-title">Share your results</h2>
      <p class="share-quote serif">${esc(shareLine(result))}</p>
      <div data-share-slot></div>
      <div class="row acc-actions">
        <button type="button" data-replay>Play my story again</button>
        <button type="button" data-change>Change my answers</button>
      </div>
      ${Number.isFinite(saved.getTime()) ? `<p class="small muted">Answers saved ${saved.toLocaleDateString(undefined, { day: "numeric", month: "long", year: "numeric" })}.</p>` : ""}
    </section>
    ${resultHTML(bundle, answers, result, { title: `<h2 class="acc-result-title">Closest to “${esc(result.schools[0].label)}”</h2>` })}
    ${nextStepHTML({ signedIn: true, write: "/#write", id: "acc-next" })}
    <section class="acc-statements" aria-labelledby="st-title" data-statements></section>
    <section data-naming hidden></section>
    <ul class="notes small">${bundle.notes.map((n) => `<li>${esc(n)}</li>`).join("")}
      ${result.unranked.length ? `<li>Not enough shared statements to compare you with: ${result.unranked.map((t) => esc(t.name)).join(", ")}.</li>` : ""}</ul>`;

  wireResult(pane, { bundle, answers, result, youFace: a.avatar_url || null });
  paintSharePanel(a, pane.querySelector("[data-share-slot]"), { bundle, answers, result });
  pane.querySelector("[data-change]").onclick = () => changeAnswers(sheet);
  pane.querySelector("[data-replay]").onclick = async () => {
    const { playStory } = await import("./story.js");
    playStory({
      bundle, answers, result, youFace: a.avatar_url || null, onDone: () => {},
      onShare: async () => { const { openAccountShare } = await import("./share.js"); openAccountShare({ bundle, answers, result, toast, account: a }); },
    });
  };
  paintStatements(pane.querySelector("[data-statements]"));
  mountNaming(pane.querySelector("[data-naming]"), { bundle, toast });
}

function changeAnswers(sheet) {
  // put the saved answers in this browser, then resume the survey with them
  if (sheet?.answers) local.set({ season: sheet.season, answers: sheet.answers, index: 0, updated_at: sheet.updated_at });
  location.href = "/#change";
}

function paintSharePanel(a, slot, { bundle, answers, result }) {
  const p = a.profile;
  const url = p ? profileURL(p, location.origin) : null;
  if (!url) {
    slot.innerHTML = `<p class="small muted">Makes one public page for your account: your result, picture, name and bio. The link stays the same when your answers change.</p>
      <div class="row"><button type="button" class="primary" data-get-link>Get my share link</button></div>
      <p class="small error" role="alert" data-share-msg hidden></p>`;
    const go = slot.querySelector("[data-get-link]");
    go.onclick = async () => {
      go.disabled = true;
      const msg = slot.querySelector("[data-share-msg]");
      try {
        const page = await publishAccountProfile(accountProfileBody(bundle, answers, result, false));
        a.profile = { code: page.code, url: page.url, listed: false };
        paintSharePanel(a, slot, { bundle, answers, result });
        slot.querySelector("[data-copy-link]")?.focus();
        toast("Your link is live");
      } catch (e) {
        go.disabled = false;
        if (e instanceof NotYet) {
          // until the account endpoint exists, the anonymous sheet still makes a link
          const { openShare } = await import("./share.js");
          openShare({ bundle, answers, result, toast });
        } else { msg.textContent = e.message; msg.hidden = false; }
      }
    };
    return;
  }
  slot.innerHTML = `${shareLinksHTML(url, shareLine(result), { id: "acc-share" })}
    <label class="gate small"><input type="checkbox" data-listed ${p.listed ? "checked" : ""}> <span>List my page in the public directory of fingerprints</span></label>
    <p class="small"><a href="${esc(url)}" target="_blank" rel="noopener">View my page</a> <button type="button" class="link-button small" data-unpublish>Take my page down</button></p>`;
  wireShareLinks(slot, url, { toast });
  const listed = slot.querySelector("[data-listed]");
  listed.onchange = async () => {
    listed.disabled = true;
    try {
      await publishAccountProfile(accountProfileBody(bundle, answers, result, listed.checked));
      a.profile = { ...p, listed: listed.checked };
      toast(listed.checked ? "Listed in the directory" : "Removed from the directory");
    } catch (e) { listed.checked = !listed.checked; toast(e.message); }
    finally { listed.disabled = false; }
  };
  slot.querySelector("[data-unpublish]").onclick = async () => {
    if (!confirm("Take your page down? Anyone who opens the link will see nothing. You can make it again later.")) return;
    try { await api("/api/me/profile", { method: "DELETE" }); } catch (e) { if (e.status !== 404) { toast(e.message); return; } }
    a.profile = null;
    toast("Page taken down");
    paintSharePanel(a, slot, { bundle, answers, result });
  };
}

async function paintStatements(box) {
  let list = [];
  try {
    const res = await fetch("/api/me/statements", { credentials: "same-origin" });
    if (res.ok) list = (await res.json()).statements || [];
  } catch { /* none yet */ }
  const mine = statementsHTML(list);
  box.innerHTML = `<h2 id="st-title">Your statements</h2>
    ${mine || `<p class="muted">None yet. When you write one, it shows here with its votes, and a badge once people in different groups agree with it.</p>`}
    ${mine ? `<p class="small"><a href="/#write">Write another</a> <span class="muted">or</span> <a href="/#room">vote in the live room</a></p>` : ""}`;
}

// ---------- Settings ----------

function renderSettings(a, pane) {
  const hasFace = a.logins.some((l) => l.kind === "bsky" || l.kind === "x");
  const hint = !a.bio ? suggestedBio(a.socials) : null;
  pane.innerHTML = `
    <h1 class="acc-pane-title" tabindex="-1">Settings</h1>
    <section class="acc-section" aria-labelledby="acc-about">
      <h2 id="acc-about">Name and bio</h2>
      <form id="profile-form">
        <label class="small" for="acc-display">Name</label>
        <input type="text" id="acc-display" maxlength="80" autocomplete="nickname" value="${esc(a.display_name || "")}">
        <label class="small" for="acc-bio" style="display:block;margin-top:12px">Bio <span class="muted">(up to 160 characters)</span></label>
        <textarea id="acc-bio" maxlength="160" rows="3">${esc(a.bio || "")}</textarea>
        ${hint ? `<div class="bio-hint" data-hint><p class="small muted">Your ${hint.network} bio:</p><p class="serif">${esc(hint.text)}</p>
          <button type="button" data-use-hint>Use this</button></div>` : ""}
        <div class="row" style="margin-top:12px"><button class="primary" type="submit">Save</button><span class="small muted" id="bio-count"></span></div>
      </form>
      <p class="small muted">Shown on your share page, and on the map when “Show me on the map” is on.</p>
    </section>

    <section class="acc-section" aria-labelledby="acc-map">
      <h2 id="acc-map">On the map</h2>
      <label class="switch-row" for="show-on-map">
        <span><b>Show me on the map</b><br><span class="small muted">${hasFace ? "Puts your picture, name and bio on the public map, near the thinkers you agree with most." : "Puts your picture, name and bio on the public map once you add a Bluesky or X sign-in below: that's where the picture comes from."}</span></span>
        <input type="checkbox" role="switch" id="show-on-map" ${a.show_on_map ? "checked" : ""}>
      </label>
      <p class="small muted">Either way, once ten people have added answers, yours count as one plain, unnamed dot among everyone's. This switch only decides whether your picture, name and bio are shown.</p>
    </section>

    <section class="acc-section" aria-labelledby="acc-logins">
      <h2 id="acc-logins">Ways in</h2>
      <ul class="acc-logins">${a.logins.map((l) => `<li><b>${esc(LOGIN_NAME[l.kind] || l.kind)}</b>${l.handle ? ` <span class="muted">${l.kind === "bsky" || l.kind === "x" ? "@" : ""}${esc(l.handle)}</span>` : ""}</li>`).join("")}</ul>
      <details class="acc-add"><summary>Add another way in</summary>
        <p class="small muted">Sign in another way while you're signed in here and it joins this account.</p>
        <div id="add-way"></div></details>
    </section>

    <section class="acc-section" aria-labelledby="acc-leave">
      <h2 id="acc-leave">Leave</h2>
      <div class="row"><button id="signout">Sign out</button><button class="danger" id="delete">Delete my account</button></div>
      <p class="small muted">Deleting removes your account, your ways in, your saved answers, your share page and anything shown on the map. It can't be undone.</p>
    </section>`;

  const sw = pane.querySelector("#show-on-map");
  sw.onchange = async () => {
    sw.disabled = true;
    try { await api("/api/me", { method: "PATCH", body: { show_on_map: sw.checked } }); a.show_on_map = sw.checked; toast(sw.checked ? "You're on the map" : "Hidden from the map"); }
    catch (e) { sw.checked = !sw.checked; toast(e.message); }
    finally { sw.disabled = false; }
  };

  const form = pane.querySelector("#profile-form");
  const bio = pane.querySelector("#acc-bio"), count = pane.querySelector("#bio-count");
  const left = () => { count.textContent = `${160 - bio.value.length} left`; };
  bio.oninput = left; left();
  form.onsubmit = async (e) => {
    e.preventDefault();
    const display_name = pane.querySelector("#acc-display").value.trim(), text = bio.value.trim();
    try {
      await api("/api/me", { method: "PATCH", body: { display_name, bio: text } });
      a.display_name = display_name; a.bio = text;
      // the results header shows the new name and bio next time it's opened
      const head = el.querySelector("#pane-results .acc-head");
      if (head) head.outerHTML = identityHTML(a);
      if (text) pane.querySelector("[data-hint]")?.remove();
      toast("Saved");
    } catch (err) { toast(err.message); }
  };
  const use = pane.querySelector("[data-use-hint]");
  if (use) use.onclick = () => { bio.value = hint.text; left(); form.requestSubmit(); };

  const addEl = pane.querySelector("#add-way");
  pane.querySelector(".acc-add").addEventListener("toggle", async (e) => {
    if (!e.target.open || addEl.childElementCount) return;
    addEl.innerHTML = signInHTML({ id: "add", x: await xAvailable() });
    wireSignIn(addEl.querySelector(".signin"), {
      onSignedIn: async (how) => { if (how !== "key-new") { toast("Added"); render(await getMe() || a); } },
      onKeySaved: async () => { toast("Added"); render(await getMe() || a); },
    });
  });

  pane.querySelector("#signout").onclick = async () => {
    try { await api("/api/auth/logout", { method: "POST", body: {} }); } catch { /* the cookie may already be gone */ }
    toast("Signed out");
    leave();
  };
  pane.querySelector("#delete").onclick = async () => {
    if (!confirm("Delete your account? This removes your saved answers, your ways in, your share page and anything shown on the map. It can't be undone.")) return;
    try { await api("/api/me", { method: "DELETE" }); } catch (e) { toast(e.message); return; }
    toast("Account deleted");
    leave();
  };
}

function leave() {
  if (onHash) { removeEventListener("hashchange", onHash); onHash = null; }
  history.replaceState(null, "", location.pathname);
  renderSignedOut();
}

async function main() {
  const back = takeSignInHash();
  const account = await getMe();
  if (back && !back.ok) toast(back.message);
  if (account) {
    if (back?.ok) { await uploadLocal(account); toast("Signed in"); }
    render(back?.ok ? (await getMe() || account) : account);
  } else {
    if (back?.ok) toast("Couldn't sign in");
    renderSignedOut();
  }
}

if (el) main();
