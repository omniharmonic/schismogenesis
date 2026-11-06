// Flow: landing → three sets of statements → reveal → (opt-in) room.
// Before the person joins the room, this page asks only for fingerprint.json, the accepted camp
// names and whether you're signed in; nothing about your answers leaves unless you choose.
import { fingerprint, teaser } from "./placement.js";
import { glyphSVG, glyphValues } from "./glyph.js";
import { esc } from "./map.js";
import { resultHTML, wireResult } from "./result-view.js";
import { canvasBlob, drawCard, shareText } from "./card.js";
import { protectedFetch } from "./turnstile.js";
import { handoffHTML } from "./site-config.js";
import { loadBundle } from "./camp-names.js";
import { nextStepHTML } from "./next-step.js";
import { getMe, paintNavYou, pickAnswers, saveAnswers, signInHTML, takeSignInHash, wireSignIn, xAvailable } from "./auth.js";

const event = (name) => fetch("/api/event", { method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name }) }).catch(() => {});

const $ = (id) => document.getElementById(id);
const store = {
  get(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } },
  set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode */ } },
};

let bundle;
let answers = {};
let index = 0;
let me = null; // the signed-in account (GET /api/me), or null

function show(id) {
  for (const s of ["landing", "quiz", "interlude", "reveal", "room"]) $(s).hidden = s !== id;
  window.scrollTo(0, 0);
}

function toast(text) {
  const t = document.createElement("div");
  t.className = "toast"; t.setAttribute("role", "status"); t.textContent = text;
  document.body.append(t); setTimeout(() => t.remove(), Math.max(2200, text.length * 55));
}

// when signed in, answers go up to the account a moment after each change, and at once at the end
let syncTimer = 0;
function syncSoon(now = false) {
  clearTimeout(syncTimer);
  if (!me) return;
  const run = () => saveAnswers(answers)
    .then(() => { if (me) me.sheet = { season: bundle.season, answers: { ...answers }, updated_at: new Date().toISOString() }; })
    .catch(() => {});
  if (now) run(); else syncTimer = setTimeout(run, 1200);
}

function save({ sync = true, updated_at = new Date().toISOString() } = {}) {
  store.set("fp.answers", { version: bundle.version, season: bundle.season, answers, index, updated_at });
  if (sync) syncSoon();
}

// ---------- answering ----------
function renderCard() {
  const a = bundle.anchors[index];
  const set = bundle.sets.find((s) => s.id === a.set);
  const setNo = bundle.sets.indexOf(set) + 1;
  $("set-title").textContent = `Part ${setNo} of 3. ${set.title}`;
  $("count").textContent = `Statement ${index + 1} of ${bundle.anchors.length}`;
  $("bar").style.width = `${(index / bundle.anchors.length) * 100}%`;
  $("statement").textContent = a.text;
  for (const b of document.querySelectorAll(".answers button")) {
    const v = b.dataset.v === "skip" ? undefined : Number(b.dataset.v);
    b.setAttribute("aria-pressed", String(answers[a.id] === v && v !== undefined));
  }
  $("back").disabled = index === 0;
}

function answer(raw) {
  const a = bundle.anchors[index];
  if (raw === "skip") delete answers[a.id]; else answers[a.id] = Number(raw);
  const next = bundle.anchors[index + 1];
  index += 1;
  save();
  if (!next) return finish();
  if (next.set !== a.set) return interlude(a.set);
  renderCard();
}

function interlude(doneSet) {
  const setNo = bundle.sets.findIndex((s) => s.id === doneSet) + 1;
  const t = teaser(bundle, answers);
  $("interlude-step").textContent = `Part ${setNo} of 3 done.`;
  $("interlude-text").textContent = t
    ? `So far you're closer to “${t.closer}” than to “${t.further}”.`
    : "Not enough answers yet to say who you're closer to. Keep going.";
  show("interlude");
  $("continue").focus();
}

function startQuiz() {
  show("quiz");
  index = Math.min(index, bundle.anchors.length - 1);
  renderCard();
}

async function share(verified = null) {
  const r = fingerprint(bundle, answers);
  if (r.status !== "ok") return;
  const { openShare, openAccountShare } = await import("./share.js");
  // signed in: the account's own page (same link every time); signed out: the anonymous sheet
  if (me && !verified) return openAccountShare({ bundle, answers, result: r, toast, account: me });
  openShare({ bundle, answers, result: r, toast, verified });
}

async function finish({ story = true } = {}) {
  save();
  syncSoon(true);
  renderReveal();
  show("reveal");
  const r = fingerprint(bundle, answers);
  if (story && r.status === "ok") {
    event("finish");
    const { playStory } = await import("./story.js");
    playStory({ bundle, answers, result: r, youFace: me?.avatar_url || null, onShare: () => share(), onDone: () => window.scrollTo(0, 0) });
  }
}

// ---------- the landing preview: one real statement, a real voice on each side ----------
function heroPreview() {
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name.replace(/ \(.*\)/, "")]));
  const short = (q) => q && q.length <= 170;
  const pairs = bundle.anchors.map((a) => {
    const e = Object.entries(bundle.stances[a.id] || {});
    const yes = e.find(([, i]) => i.a === 1 && short(i.q));
    const no = e.find(([, i]) => i.a === -1 && short(i.q));
    return yes && no ? { a, yes, no, up: e.filter(([, i]) => i.a === 1).length, down: e.filter(([, i]) => i.a === -1).length } : null;
  }).filter(Boolean);
  if (!pairs.length) return;
  let n = Math.floor(Math.random() * pairs.length);
  const side = ([id, i], label, cls) => `<div class="side ${cls}"><span class="side-label">${label}</span>
    <blockquote>“${esc(i.q)}”</blockquote><p class="who">${esc(names[id])}</p></div>`;
  const card = document.createElement("div");
  card.className = "preview-card bracketed";
  $("hero-preview").append(card);
  const draw = () => {
    const p = pairs[n % pairs.length];
    card.innerHTML = `<p class="preview-eyebrow">One of the ${bundle.anchors.length} statements</p>
      <p class="preview-statement serif">${esc(p.a.text)}</p>
      <div class="preview-sides">${side(p.yes, `Agree, ${p.up} thinkers`, "agree")}${side(p.no, `Disagree, ${p.down} thinkers`, "disagree")}</div>
      <button class="link-button small" id="preview-next">Show another</button>`;
    $("preview-next").onclick = () => { n += 1; draw(); stop(); };
  };
  let timer = null;
  const stop = () => { clearInterval(timer); timer = null; };
  draw();
  if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {
    timer = setInterval(() => { n += 1; draw(); }, 7000);
    card.addEventListener("pointerenter", stop);
    $("start").addEventListener("click", stop);
  }
}

// ---------- the reveal ----------
function renderReveal() {
  const r = fingerprint(bundle, answers);
  const el = $("reveal");
  if (r.status !== "ok") {
    el.innerHTML = `<h1>Not enough to place you yet</h1>
      <p>You've taken a side on ${r.answered} statements. We need at least ${r.needed}, with enough of them shared with the thinkers, before comparing you with anyone.</p>
      <button class="primary" id="more">Answer more</button>`;
    $("more").onclick = () => { index = bundle.anchors.findIndex((a) => answers[a.id] === undefined || answers[a.id] === 0); if (index < 0) index = 0; startQuiz(); };
    return;
  }
  el.innerHTML = `${resultHTML(bundle, answers, r)}

    <div id="next-slot">${nextStepHTML({ signedIn: Boolean(me), id: "next-step" })}</div>

    <h2>Share it</h2>
    <canvas id="card" class="card-preview" aria-label="Share card preview"></canvas>
    <div class="row">
      <button class="primary" id="get-link">Get my share link</button>
      <button id="replay">Play my story again</button>
      <button id="download">Save image</button>
      <button id="copy">Copy text</button>
    </div>
    <p class="small muted">${me
      ? "Your share link is one page for your account, with a preview card for X and Bluesky. It keeps up with your answers, and you can take it down from your account."
      : "A share link makes a page with a preview card for X and Bluesky. You choose what it shows and can delete it any time."} Images are made in your browser.</p>

    <div class="room-card save-card" id="save-card"></div>

    <div class="room-card" id="contribute-card">
      <h2 style="margin-top:0">Add your answers to the results</h2>
      <p>See how everyone who took it answers, statement by statement, and where you fall among them. Your answers are counted without your name, and nothing about any group under ten people is shown.</p>
      <div class="row"><button class="primary" id="contribute">Add my answers</button><a class="button" href="/results">See the results</a></div>
    </div>

    <div class="room-card">
      <h2 style="margin-top:0">Vote in the live room</h2>
      <p>Vote on statements other people wrote, and see the room's own groups and the statements that bridge them.</p>
      <p class="small muted">${me ? "You join with your account. Your name is shown only if you show yourself on the map."
      : "Joining sends your answers above to the room under a random ID. No name or email."}</p>
      <div class="row" style="margin-top:12px"><button id="join">Open the live room</button></div>
    </div>

    <h2>Was this fair to you?</h2>
    <div class="stars" role="group" aria-label="Rate fairness from 1 to 5">${[1, 2, 3, 4, 5].map((n) => `<button data-rate="${n}">${n}</button>`).join("")}</div>
    <p class="small muted">1 is unfair, 5 is fair. Sends only the number.</p>

    <ul class="notes small">${bundle.notes.map((n) => `<li>${esc(n)}</li>`).join("")}
      ${r.unranked.length ? `<li>Not enough shared statements to compare you with: ${r.unranked.map((t) => esc(t.name)).join(", ")}.</li>` : ""}</ul>
    <div class="row"><button class="link-button" id="redo">Change my answers</button></div>
    ${handoffHTML({ far: r.furthest[0]?.school || null })}`;

  wireResult(el, { bundle, answers, result: r, youFace: me?.avatar_url || null });
  paintSaveCard();

  const values = glyphValues(bundle, answers);
  const thinkers = bundle.thinkers.length;
  drawCard($("card"), values, r, { thinkers });
  document.fonts?.ready.then(() => drawCard($("card"), values, r, { thinkers }));
  $("download").onclick = async () => {
    const blob = await canvasBlob($("card"));
    const a = document.createElement("a");
    a.download = "great-ai-debate-fingerprint.png"; a.href = URL.createObjectURL(blob); a.click();
    event("save_card");
  };
  $("copy").onclick = async () => {
    try { await navigator.clipboard.writeText(shareText(r, location.origin)); toast("Copied"); event("copy_text"); } catch { toast("Copy failed. Select the text manually."); }
  };
  $("get-link").onclick = () => share();
  if (me) {
    $("contribute-card").querySelector("h2").textContent = "Counted in the results";
    $("contribute-card").querySelector("p").textContent = "Your saved answers are counted in the results, without your name.";
    $("contribute").remove();
  } else if (store.get("fp.room.ai-futures", null)) {
    $("contribute-card").querySelector("p").textContent = "Your answers are counted in the results. Thank you.";
    $("contribute").remove();
  } else {
    $("contribute").onclick = async () => {
      $("contribute").disabled = true;
      const bytes = crypto.getRandomValues(new Uint8Array(32));
      const key = [...bytes].map((b) => b.toString(16).padStart(2, "0")).join("");
      const clean = Object.fromEntries(Object.entries(answers).filter(([, v]) => [1, -1, 0].includes(v)));
      let res;
      try { res = await protectedFetch("/api/rooms/ai-futures/join", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key, consent_version: "room-v1", answers: clean }) }); } catch (e) { $("contribute").disabled = false; toast(e.message); return; }
      if (!res.ok) { $("contribute").disabled = false; toast("That didn't go through. Try again."); return; }
      store.set("fp.room.ai-futures", { participant_id: (await res.json()).participant_id, key });
      $("contribute-card").querySelector("p").textContent = "Added. Results refresh every few minutes.";
      $("contribute").remove();
      toast("Your answers are counted");
    };
  }
  $("replay").onclick = async () => {
    const { playStory } = await import("./story.js");
    playStory({ bundle, answers, result: r, youFace: me?.avatar_url || null, onShare: () => share(), onDone: () => {} });
  };
  $("redo").onclick = () => { index = 0; startQuiz(); };
  for (const b of el.querySelectorAll("[data-rate]")) {
    b.onclick = async () => {
      await fetch("/api/fairness", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ rating: Number(b.dataset.rate) }) });
      el.querySelector(".stars").outerHTML = `<p>Thanks. Your rating is recorded.</p>`;
    };
  }
  $("join").onclick = () => enterRoom();
  wireNextStep();
}

// into the room (the room code loads only on opt-in); `write` opens straight on writing
async function enterRoom({ write = false } = {}) {
  const { joinRoom } = await import("./room.js");
  joinRoom({ bundle, answers, handle: "", show, toast, write });
}

// the next step's buttons: write (signed in, or carrying on without an account), or sign in first
function wireNextStep() {
  const slot = $("next-slot");
  if (!slot) return;
  slot.onclick = (e) => {
    const a = e.target.closest("[data-next]");
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault();
    if (a.dataset.next === "signin") {
      const open = $("save-open");
      if (open && $("save-ways").hidden) open.click();
      $("save-card").scrollIntoView({ block: "start", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
      setTimeout(() => $("save-card").querySelector(".signin input:not([type=hidden]), .signin a, .signin button")?.focus({ preventScroll: true }), 400);
      return;
    }
    enterRoom({ write: true });
  };
}

// "Save your answers": the four ways in while signed out; a quiet note once signed in
async function paintSaveCard() {
  const card = $("save-card");
  if (!card) return;
  if (me) {
    card.innerHTML = `<h2 style="margin-top:0">Your answers are saved</h2>
      <p>They save to your account as you change them, so you can come back on any device. Choose whether to show yourself on the map from <a href="/account.html">your account</a>.</p>`;
    return;
  }
  card.innerHTML = `<h2 style="margin-top:0">Save your answers</h2>
    <p>Sign in to come back on any device and change your answers. Saved answers are also counted in the results, without your name. Your name and picture go on the map only if you switch that on.</p>
    <div class="row"><button class="primary" id="save-open" aria-expanded="false" aria-controls="save-ways">Choose how to sign in</button></div>
    <div id="save-ways" hidden></div>`;
  $("save-open").onclick = async () => {
    const ways = $("save-ways");
    if (!ways.childElementCount) {
      ways.innerHTML = signInHTML({ id: "save", x: await xAvailable() });
      wireSignIn(ways.querySelector(".signin"), {
        onSignedIn: async (how) => { await signedInHere(); if (how !== "key-new") afterSignIn(); },
        onKeySaved: () => afterSignIn(),
      });
    }
    ways.hidden = !ways.hidden;
    $("save-open").setAttribute("aria-expanded", String(!ways.hidden));
  };
}

// a same-page sign-in (email code or key): upload what this browser has
async function signedInHere() {
  me = await getMe();
  paintNavYou(me);
  if (me) syncSoon(true);
}
function afterSignIn() {
  if (!me) { toast("Couldn't sign in"); return; }
  toast("Signed in");
  paintSaveCard();
  const slot = $("next-slot");
  if (slot) slot.innerHTML = nextStepHTML({ signedIn: true, id: "next-step" });
  const c = $("contribute");
  if (c) { $("contribute-card").querySelector("h2").textContent = "Counted in the results"; $("contribute-card").querySelector("p").textContent = "Your saved answers are counted in the results, without your name."; c.remove(); }
}

// ---------- start ----------
async function boot() {
  const [b, account] = await Promise.all([loadBundle("/fingerprint.json"), getMe()]);
  bundle = b; me = account;
  const back = takeSignInHash();
  const saved = store.get("fp.answers", null);
  // answers stay valid while the statements stay the same (one season), across bundle rebuilds
  const sameSeason = saved && (saved.season ? saved.season === bundle.season : saved.version === "fp-2026-11-02.1");
  if (saved && (saved.version === bundle.version || sameSeason)) {
    const ids = new Set(bundle.anchors.map((a) => a.id));
    answers = Object.fromEntries(Object.entries(saved.answers).filter(([id]) => ids.has(id)));
    index = saved.index || 0;
  }
  // the account's saved answers win when this browser has none, or older ones; right after a
  // sign-in, this browser's answers are the ones the person meant to save
  const ids = new Set(bundle.anchors.map((a) => a.id));
  const mine = { season: bundle.season, answers, updated_at: saved?.updated_at };
  const pick = back?.ok && Object.keys(answers).length ? "local" : pickAnswers(mine, me?.sheet, bundle.season);
  if (pick === "server") {
    answers = Object.fromEntries(Object.entries(me.sheet.answers).filter(([id, v]) => ids.has(id) && [1, -1, 0].includes(v)));
    index = bundle.anchors.length;
    save({ sync: false, updated_at: me.sheet.updated_at });
  } else if (pick === "local" && me) syncSoon(true);
  $("hero-print").innerHTML = glyphSVG(bundle, Object.fromEntries(bundle.anchors.map((a, k) => [a.id, [1, -1, 0, 1][k % 4]])), { label: "" });
  $("hero-print").firstElementChild.classList.add("hero-print");
  heroPreview();
  $("thinker-count").textContent = String(bundle.thinkers.length);
  $("adult").onchange = () => { $("start").disabled = !$("adult").checked; };
  $("start").onclick = () => { if (index >= bundle.anchors.length) index = 0; event("start"); startQuiz(); };
  if (Object.keys(answers).length && index >= bundle.anchors.length) {
    $("resume").hidden = false;
    $("resume").onclick = () => finish({ story: false });
    $("start").textContent = "Start again";
  }
  $("back").onclick = () => { if (index > 0) { index -= 1; renderCard(); } };
  $("finish-early").onclick = () => finish();
  $("continue").onclick = () => { show("quiz"); renderCard(); };
  for (const b of document.querySelectorAll(".answers button")) b.onclick = () => answer(b.dataset.v);
  document.addEventListener("keydown", (e) => {
    if ($("quiz").hidden || e.metaKey || e.ctrlKey || e.altKey) return;
    const key = { a: "1", d: "-1", u: "0", s: "skip" }[e.key.toLowerCase()];
    if (key) { e.preventDefault(); answer(key); }
    if (e.key === "ArrowLeft") $("back").click();
  });
  // returning from a Bluesky, X or email-link sign-in
  if (back) {
    if (!back.ok) toast(back.message);
    else if (!me) toast("Couldn't sign in");
    else {
      toast("Signed in");
      if (Object.keys(answers).length && index >= bundle.anchors.length) { finish({ story: false }); $("save-card")?.scrollIntoView({ block: "center" }); return; }
    }
  }
  // "Change my answers" from the account page: back into the survey with the saved answers
  if (location.hash === "#change") {
    history.replaceState(null, "", location.pathname + location.search);
    if (Object.keys(answers).length) { index = 0; startQuiz(); return; }
  }
  // returning from "Sign in with X" to verify a share link
  const verify = location.hash.match(/^#verify=(.+)$/);
  if (verify) {
    history.replaceState(null, "", location.pathname + location.search);
    if (verify[1] === "failed") toast("X didn't confirm the account. Try again, or share anonymously.");
    else if (Object.keys(answers).length) {
      try {
        const res = await fetch(`/api/verify/${encodeURIComponent(verify[1])}`);
        if (res.ok) {
          finish({ story: false });
          return share({ ...(await res.json()), check_id: verify[1] });
        }
      } catch { /* fall through */ }
      toast("That sign-in has expired. Try again.");
    }
  }
  if (location.hash === "#room") {
    const { openRoom } = await import("./room.js");
    return openRoom({ bundle, show, toast });
  }
  // "Write a statement" from your results or the results page: straight to the room's write step
  if (location.hash === "#write") {
    const { openRoom, joinRoom } = await import("./room.js");
    if (me || store.get("fp.room.ai-futures", null)) return openRoom({ bundle, show, toast, write: true });
    if (fingerprint(bundle, answers).status === "ok") return joinRoom({ bundle, answers, handle: "", show, toast, write: true });
    history.replaceState(null, "", location.pathname + location.search);
    toast("Take the survey first. Then you can write a statement.");
  }
  show("landing");
}

boot();
