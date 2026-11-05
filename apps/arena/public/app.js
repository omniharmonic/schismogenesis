// Flow: landing → three sets of statements → reveal → (opt-in) room.
// Before the person joins the room, the only request this page makes is for fingerprint.json.
import { fingerprint, teaser } from "./placement.js";
import { glyphSVG, glyphValues } from "./glyph.js";
import { badge, esc, mapSVG } from "./map.js";
import { explorer, schoolGrid } from "./explore.js";
import { canvasBlob, drawCard, shareText } from "./card.js";
import { protectedFetch } from "./turnstile.js";
import { handoffHTML } from "./site-config.js";
import { getMe, pickAnswers, saveAnswers, signInHTML, takeSignInHash, wireSignIn, xAvailable } from "./auth.js";
import { fetchPeople, mountLayerSwitch } from "./crowd.js";

const event = (name) => fetch("/api/event", { method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name }) }).catch(() => {});

const $ = (id) => document.getElementById(id);
const store = {
  get(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } },
  set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode */ } },
};
const ANSWER_LABEL = { 1: "Agree", "-1": "Disagree", 0: "Unsure" };
const ANSWER_CLASS = { 1: "agree", "-1": "disagree", 0: "unsure" };
const LAYER_NAME = { ontological: "What AI is", epistemic: "How we know", axiological: "What matters",
  empirical: "What will happen", praxis: "What to do" };

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
  const { openShare } = await import("./share.js");
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
    playStory({ bundle, answers, result: r, onShare: () => share(), onDone: () => window.scrollTo(0, 0) });
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
// phones get a taller, narrower map so circles stay big enough to tap
export const mapSize = () => (innerWidth < 600 ? { width: 400, height: 640 } : { width: 800, height: 640 });

function thinkerRow(t) {
  return `<li><button class="thinker-row" data-thinker="${esc(t.id)}">${badge(t)}
    <span><b>${esc(t.name)}</b><br><span class="small muted">${esc(t.school || "No school")}${bundle.thinkers.find((x) => x.id === t.id)?.provisional ? ", new voice" : ""}</span></span>
    <span class="score"><b>${t.k} of ${t.n}</b><br><span class="small muted">agree</span></span></button></li>`;
}

function signatureHTML(r) {
  if (!r.signature.length) {
    const weakest = r.nearest.at(-1);
    return `<p>You're consistent with “${esc(r.schools[0].label)}” on every statement we could check.
      Your weakest close match is ${esc(weakest.name)}, at ${weakest.k} of ${weakest.n}.</p>`;
  }
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  return `<ul class="signature">${r.signature.map((s) => `<li>
      <span class="serif">You ${s.answer === 1 ? "agree" : "disagree"}: “${esc(s.text)}”</span>
      <p class="small muted" style="margin-top:6px">Most of the thinkers in “${esc(s.home)}” take the other side. Those in “${esc(s.ally)}” are with you: ${s.allies.map((a) => esc(names[a])).join(", ")}.</p>
    </li>`).join("")}</ul>`;
}

function campsHTML(r) {
  const layers = bundle.layers.filter((l) => r.camps.some((c) => c.byLayer[l][0] + c.byLayer[l][1]));
  const head = `<tr class="head"><th scope="col">Camp</th>${layers.map((l) => `<th scope="col">${LAYER_NAME[l]}</th>`).join("")}<th scope="col">Deepest split</th></tr>`;
  const rows = r.camps.map((c) => `<tr><th scope="row">${esc(c.label)}</th>${layers.map((l) => {
    const [a, o] = c.byLayer[l];
    if (!a && !o) return `<td class="muted" data-label="${LAYER_NAME[l]}">none</td>`;
    return `<td data-label="${LAYER_NAME[l]}"><span class="cell-agree">${a}</span> / <span class="cell-split">${o}</span></td>`;
  }).join("")}<td data-label="Deepest split">${c.deepest ? LAYER_NAME[c.deepest] : "none"}</td></tr>`).join("");
  return `<div class="table-wrap"><table class="camps-table stacks">${head}${rows}</table></div>
    <p class="small muted">Each cell is <span class="cell-agree">with you</span> / <span class="cell-split">against you</span>: statements where the camp's thinkers lean one way and you answered. Layers run from roots to action, so a split low down runs deeper.</p>`;
}

function mirrorHTML() {
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  // each name opens that thinker's card beside the map
  const who = (id) => `<button class="link-button inline" data-thinker="${esc(id)}">${esc(names[id])}</button>`;
  return bundle.anchors.filter((a) => answers[a.id] !== undefined).map((a) => {
    const v = answers[a.id];
    const entries = Object.entries(bundle.stances[a.id]);
    const quotes = entries.map(([id, item]) => {
      const side = item.a === 1 ? "agree" : "disagree";
      const body = item.q
        ? `“${esc(item.q)}”<cite>${who(id)}, <a href="${esc(item.url)}" target="_blank" rel="noopener">${esc(item.work)}</a>. Read as ${side === "agree" ? "agreeing" : "disagreeing"}.</cite>`
        : `<cite>${who(id)}: read as ${side === "agree" ? "agreeing" : "disagreeing"}.</cite>`;
      return `<blockquote class="${side}">${body}</blockquote>`;
    }).join("");
    const withYou = v === 0 ? 0 : entries.filter(([, i]) => i.a === v).length;
    return `<details class="mirror"><summary><span class="serif">${esc(a.text)}</span>
      <span class="chip ${ANSWER_CLASS[v]}">${ANSWER_LABEL[v]}</span></summary>
      <p class="small muted" style="margin-top:8px">${v === 0 ? `${entries.length} thinkers took a side.` : `${withYou} of ${entries.length} thinkers we read are with you.`}</p>
      ${quotes}
      <div class="row"><a class="small" href="/s/${esc(a.id)}">Open this statement</a>
      <button class="link-button small" data-dispute="${esc(a.id)}">Report a misreading on this statement</button></div>
    </details>`;
  }).join("");
}

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
  const home = r.schools[0];
  const mapOptions = { result: r, ...mapSize() };
  el.innerHTML = `
    <div class="reveal-head">
      ${glyphSVG(bundle, answers, { label: "Your fingerprint, drawn from your answers" })}
      <div>
        <p class="muted">Your fingerprint</p>
        <h1 style="max-width:18ch">Closest to “${esc(home.label)}”</h1>
        <p>From ${r.answered} statements you took a side on.</p>
      </div>
    </div>

    <section class="explore" aria-labelledby="sit-title">
      <h2 id="sit-title">Where you sit</h2>
      <p class="muted explore-hint">Select any thinker or school to see where they stand, statement by statement, beside your answers.</p>
      <div class="explore-grid">
        <div class="mapbox" id="reveal-map">${mapSVG(bundle, mapOptions)}
          <p class="map-key small muted"><span><i class="k-dark"></i>agrees with you more</span><span><i class="k-dash"></i>too few shared statements</span><span><i class="k-dot"></i>new voice</span></p>
        </div>
        <aside class="panel" id="reveal-panel" aria-live="polite"></aside>
      </div>
      <h3 class="grid-title">The camps, and the schools inside them</h3>
      <div id="reveal-schools">${schoolGrid(bundle, r)}</div>
      <p class="small"><a href="/atlas">Explore the full 3D atlas of ideas</a></p>
    </section>

    <h2>Where you break from your neighbours</h2>
    ${signatureHTML(r)}

    <h2>You and the camps</h2>
    ${campsHTML(r)}

    <h2>Quote mirror</h2>
    <p class="muted">For each statement you answered, the thinkers' own words. Quotes are short and link to the source.</p>
    ${mirrorHTML()}

    <h2>Share it</h2>
    <canvas id="card" class="card-preview" aria-label="Share card preview"></canvas>
    <div class="row">
      <button class="primary" id="get-link">Get my share link</button>
      <button id="replay">Play my story again</button>
      <button id="download">Save image</button>
      <button id="copy">Copy text</button>
    </div>
    <p class="small muted">A share link makes a page with a preview card for X and Bluesky. You choose what it shows and can delete it any time. Images are made in your browser.</p>

    <div class="room-card save-card" id="save-card"></div>

    <div class="room-card" id="contribute-card">
      <h2 style="margin-top:0">Add your answers to the results</h2>
      <p>See how everyone who took it answers, statement by statement, and where you fall among them. Your answers are counted without your name, and nothing about any group under ten people is shown.</p>
      <div class="row"><button class="primary" id="contribute">Add my answers</button><a class="button" href="/results">See the results</a></div>
    </div>

    <div class="room-card">
      <h2 style="margin-top:0">Join the live room</h2>
      <p>Vote on more statements, including ones other people write, and see the room's own groups and the statements that bridge them.</p>
      <p class="small muted">Joining sends your answers above to the room under a random ID. No name or email. You can add a handle if you like.</p>
      <label class="small" for="handle">Handle (optional)</label>
      <input type="text" id="handle" maxlength="40" autocomplete="off" placeholder="How you'd like to appear, or leave blank">
      <div class="row" style="margin-top:12px"><button class="primary" id="join">Add my answers to the live room</button></div>
    </div>

    <h2>Was this fair to you?</h2>
    <div class="stars" role="group" aria-label="Rate fairness from 1 to 5">${[1, 2, 3, 4, 5].map((n) => `<button data-rate="${n}">${n}</button>`).join("")}</div>
    <p class="small muted">1 is unfair, 5 is fair. Sends only the number.</p>

    <ul class="notes small">${bundle.notes.map((n) => `<li>${esc(n)}</li>`).join("")}
      ${r.unranked.length ? `<li>Not enough shared statements to compare you with: ${r.unranked.map((t) => esc(t.name)).join(", ")}.</li>` : ""}</ul>
    <div class="row"><button class="link-button" id="redo">Change my answers</button></div>
    ${handoffHTML({ far: r.furthest[0]?.school || null })}`;

  const ex = explorer({
    bundle, answers, mapEl: $("reveal-map"), panelEl: $("reveal-panel"), gridEl: $("reveal-schools"),
    mapOptions,
    intro: `<h3>Your nearest thinkers</h3><ul class="thinkers">${r.nearest.map(thinkerRow).join("")}</ul>
      <h3>Furthest from you</h3><ul class="thinkers">${r.furthest.map(thinkerRow).join("")}</ul>
      <p class="small muted">Select anyone here or on the map to compare, statement by statement.</p>`,
  });

  // the people who added their answers, on the same map (Thinkers / People / Both)
  const layer = mountLayerSwitch($("reveal-map"));
  fetchPeople().then((crowd) => {
    layer.set(crowd);
    if (crowd.people.length && $("reveal-map")) { mapOptions.people = crowd.people; ex.redraw(); }
  });
  paintSaveCard();

  el.addEventListener("click", (e) => {
    const t = e.target.closest("details.mirror [data-thinker]");
    if (!t) return;
    ex.open({ thinker: t.dataset.thinker });
    $("reveal-panel").scrollIntoView({ behavior: "smooth", block: "start" });
  });

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
    playStory({ bundle, answers, result: r, onShare: () => share(), onDone: () => {} });
  };
  $("redo").onclick = () => { index = 0; startQuiz(); };
  for (const b of el.querySelectorAll("[data-rate]")) {
    b.onclick = async () => {
      await fetch("/api/fairness", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ rating: Number(b.dataset.rate) }) });
      el.querySelector(".stars").outerHTML = `<p>Thanks. Your rating is recorded.</p>`;
    };
  }
  for (const b of el.querySelectorAll("[data-dispute]")) b.onclick = () => disputeForm(b, b.dataset.dispute);
  $("join").onclick = async () => {
    const { joinRoom } = await import("./room.js");  // the room code loads only on opt-in
    joinRoom({ bundle, answers, handle: $("handle").value, show, toast });
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
  if (me) syncSoon(true);
}
function afterSignIn() {
  if (!me) { toast("Couldn't sign in"); return; }
  toast("Signed in");
  paintSaveCard();
  const c = $("contribute");
  if (c) { $("contribute-card").querySelector("h2").textContent = "Counted in the results"; $("contribute-card").querySelector("p").textContent = "Your saved answers are counted in the results, without your name."; c.remove(); }
}

function disputeForm(button, anchorId) {
  const ids = Object.keys(bundle.stances[anchorId]);
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  const form = document.createElement("form");
  form.innerHTML = `<label class="small">Whose position is misread?
      <select name="person" style="display:block;margin:6px 0;min-height:44px">${ids.map((i) => `<option value="${i}">${esc(names[i])}</option>`).join("")}</select></label>
    <label class="small">What's wrong, and where they said otherwise<textarea name="body" required minlength="5" maxlength="2000"></textarea></label>
    <label class="small">Contact, if you'd like a reply (optional)<input type="text" name="contact" maxlength="200"></label>
    <div class="row" style="margin-top:8px"><button class="primary" type="submit">Send report</button></div>`;
  form.onsubmit = async (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const res = await protectedFetch("/api/disputes", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ person_id: f.get("person"), anchor_id: anchorId, body: f.get("body"), contact: f.get("contact") || null }) });
    form.outerHTML = res.ok ? `<p>Report sent. Benjamin's team reviews every one.</p>` : `<p class="error">That didn't send. Try again in a moment.</p>`;
  };
  button.replaceWith(form);
}

// ---------- start ----------
async function boot() {
  const [b, account] = await Promise.all([fetch("fingerprint.json").then((res) => res.json()), getMe()]);
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
  show("landing");
}

boot();
