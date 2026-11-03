// The live room. Loaded only after the person chooses "Add my answers to the live room".
import { esc, mapSVG } from "./map.js";

const params = new URLSearchParams(location.search);
const SLUG = /^[a-z0-9-]{2,40}$/.test(params.get("room") || "") ? params.get("room") : "ai-futures";
const KEY = `fp.room.${SLUG}`;
const CONSENT = "room-v1";
const DONE = { 1: "Agreed", "-1": "Disagreed", 0: "Passed" };

let ctx;
let me = null;
let queue = [];

const read = () => { try { return JSON.parse(localStorage.getItem(KEY)); } catch { return null; } };
const write = (v) => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch { /* private mode */ } };

async function api(path, { method = "GET", body } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (me) { headers["X-Participant"] = me.participant_id; headers["X-Key"] = me.key; }
  const res = await fetch(`/api/rooms/${SLUG}${path}`, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw Object.assign(new Error(data.error || `Request failed (${res.status})`), { status: res.status });
  return data;
}

export async function joinRoom({ bundle, answers, handle, show, toast }) {
  ctx = { bundle, show, toast };
  me = read();
  if (!me) {
    const bytes = crypto.getRandomValues(new Uint8Array(32));
    const key = [...bytes].map((b) => b.toString(16).padStart(2, "0")).join("");
    const clean = Object.fromEntries(Object.entries(answers).filter(([, v]) => [1, -1, 0].includes(v)));
    try {
      const res = await api("/join", { method: "POST", body: { key, handle: handle || null, consent_version: CONSENT, answers: clean } });
      me = { participant_id: res.participant_id, key };
      write(me);
    } catch (e) {
      toast(e.message);
      return;
    }
  }
  history.replaceState(null, "", `${location.pathname}${location.search}#room`);
  render();
}

export async function openRoom({ bundle, show, toast }) {
  ctx = { bundle, show, toast };
  me = read();
  render();
}

function leave() {
  try { localStorage.removeItem(KEY); } catch { /* ignore */ }
  me = null;
  history.replaceState(null, "", location.pathname + location.search);
  location.reload();
}

async function render() {
  const el = document.getElementById("room");
  ctx.show("room");
  let info;
  try { info = await api(""); } catch (e) { el.innerHTML = `<p class="error">${esc(e.message)}</p>`; return; }
  el.innerHTML = `
    ${info.demo ? `<div class="demo-banner">Demo room. Most voters here are synthetic, made up to show how the report works.</div>` : ""}
    <p class="muted">The live room</p>
    <h1 style="max-width:20ch">${esc(info.title)}</h1>
    <p class="small muted">${info.people} people, ${info.statements} statements, ${info.votes} votes so far.</p>
    <div class="room-card" id="vote-card" aria-live="polite"></div>
    <div class="room-card">
      <h3>Add a statement</h3>
      <p class="small muted">Write something people who disagree with you might also agree with. Up to 140 characters. A moderator checks it before others see it.</p>
      <textarea id="new-statement" maxlength="140" aria-label="Your statement"></textarea>
      <div class="row" style="margin-top:8px"><button class="primary" id="submit-statement">Add statement</button><span class="small muted" id="chars">0 of 140</span></div>
      <p class="small" id="statement-msg" role="status"></p>
    </div>
    <div id="report"></div>
    <div class="row" style="margin-top:32px">
      <button id="refresh">Refresh the report</button>
      <button class="link-button" id="back-to-print">Back to my fingerprint</button>
      <button class="link-button" id="leave">Leave the room on this device</button>
    </div>`;
  document.getElementById("refresh").onclick = renderReport;
  document.getElementById("leave").onclick = leave;
  document.getElementById("back-to-print").onclick = () => { history.replaceState(null, "", location.pathname + location.search); location.reload(); };
  const box = document.getElementById("new-statement");
  box.oninput = () => { document.getElementById("chars").textContent = `${box.value.length} of 140`; };
  document.getElementById("submit-statement").onclick = submitStatement;
  await nextCard();
  await renderReport();
}

async function nextCard() {
  const card = document.getElementById("vote-card");
  if (!me) {
    card.innerHTML = `<p>You haven't joined this room on this device.</p>`;
    return;
  }
  if (!queue.length) {
    try { queue = (await api("/next?limit=8")).statements; } catch (e) { card.innerHTML = `<p class="error">${esc(e.message)}</p>`; return; }
  }
  const s = queue[0];
  if (!s) {
    card.innerHTML = `<h3>You've voted on everything here</h3><p class="muted">New statements arrive as people write them. Check back, or add one below.</p>`;
    return;
  }
  card.innerHTML = `<span class="tag">${s.origin === "anchor" ? "From the fingerprint" : "Written by a participant"}</span>
    <p class="statement">${esc(s.text)}</p>
    <div class="answers" role="group" aria-label="Your vote">
      <button class="agree" data-v="1">Agree</button><button class="disagree" data-v="-1">Disagree</button>
      <button class="unsure" data-v="0">Pass</button>
    </div>`;
  for (const b of card.querySelectorAll("button")) {
    b.onclick = async () => {
      try {
        await api("/votes", { method: "POST", body: { statement_id: s.statement_id, vote: Number(b.dataset.v) } });
        queue.shift();
        ctx.toast(DONE[b.dataset.v]);
        nextCard();
      } catch (e) { ctx.toast(e.message); }
    };
  }
}

async function submitStatement() {
  const box = document.getElementById("new-statement");
  const msg = document.getElementById("statement-msg");
  try {
    const r = await api("/statements", { method: "POST", body: { text: box.value } });
    box.value = "";
    msg.className = "small";
    msg.textContent = r.status === "approved" ? "Added. It's in the room now." : "Sent for moderation. Others will see it once it's approved.";
    if (r.status === "approved") queue = [];
  } catch (e) {
    msg.className = "small error";
    msg.textContent = e.message;
  }
}

function list(items, extra = () => "") {
  if (!items.length) return `<p class="muted">None yet.</p>`;
  return `<ul class="result-list">${items.map((i) => `<li><span class="serif">${esc(i.text)}</span>
    <span class="small muted">${i.origin === "participant" ? "Written by a participant. " : ""}${extra(i)}</span></li>`).join("")}</ul>`;
}

const pct = (x) => `${Math.round(x * 100)}%`;

async function renderReport() {
  const el = document.getElementById("report");
  let r, mine = null;
  try {
    r = await api("/report");
    if (me) mine = await api("/me");
  } catch (e) { el.innerHTML = `<p class="error">${esc(e.message)}</p>`; return; }
  const bundle = ctx.bundle;
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  let html = `<h2>What the room shows</h2>`;
  if (mine?.group) html += `<p>You're in group <b>${esc(mine.group)}</b>.${mine.backed_bridges.length ? ` You backed ${mine.backed_bridges.length} of the room's bridges.` : ""}</p>`;
  html += `<h3 style="margin-top:28px">Bridges</h3>
    <p class="small muted">Statements that people on both sides of the room's main split agree with, scored the way Community Notes scores notes.</p>`;
  if (r.bridges) {
    const ax = r.bridges.axis;
    if (ax) html += `<p class="small">The room's main split lines up with ${esc(ax.negative)} versus ${esc(ax.positive)} (correlation ${ax.r}).</p>`;
    html += list(r.bridges.passed, (b) => `${b.raters} raters. Agreement on each side: ${pct(b.agree_by_side[0])} and ${pct(b.agree_by_side[1])}.`);
    if (r.bridges.leaning.length) {
      html += `<p class="small muted" style="margin-top:16px">Close, but not over the bar yet:</p>` +
        list(r.bridges.leaning, (b) => `${b.raters} raters. Agreement on each side: ${b.agree_by_side.map((a) => (a === null ? "n/a" : pct(a))).join(" and ")}.`);
    }
  }
  if (r.groups && r.groups.clear) {
    const marks = r.groups.list.filter((g) => g.thinkers.length).map((g) => ({
      near: g.thinkers.map((t) => t.id), label: g.name,
      title: `Group ${g.name} (${g.size} people) votes most like this thinker`,
    }));
    html += `<h3 style="margin-top:28px">Opinion groups</h3>
      <p class="small muted">People who vote alike, found the way Polis finds them. ${r.groups.k} groups, separation ${r.groups.silhouette}.</p>
      <div class="groups">${r.groups.list.map((g) => `<div class="group"><b>Group ${esc(g.name)}</b> <span class="small muted">${g.size} people</span>
        ${g.thinkers.length ? `<p class="small">Votes most like ${g.thinkers.map((t) => esc(names[t.id])).join(", ")}.</p>` : ""}
        ${g.representative.length ? `<p class="small muted" style="margin-bottom:4px">Sets them apart:</p><ul class="small" style="padding-left:18px;margin:0">${g.representative.slice(0, 3).map((s) => `<li>${s.direction === "agree" ? "Agree" : "Disagree"} (${pct(s.p)}): ${esc(s.text)}</li>`).join("")}</ul>` : ""}
      </div>`).join("")}</div>
      <h3 style="margin-top:28px">Which thinkers each group votes like</h3>
      <p class="small muted">Each letter marks one of the three thinkers that group agrees with most on the fingerprint statements.</p>
      <div class="mapbox">${mapSVG(bundle, { marks, ...(innerWidth < 600 ? { width: 440, height: 520 } : {}) })}</div>
      <h3 style="margin-top:28px">Common ground</h3>
      <p class="small muted">Every group leans to agree.</p>
      ${list(r.groups.consensus, (c) => `Agreement by group: ${c.by_group.map(pct).join(", ")}.`)}
      <h3 style="margin-top:28px">Live splits</h3>
      ${list(r.groups.divisive, (c) => `Agreement by group: ${c.by_group.map(pct).join(", ")}.`)}`;
  }
  if (r.notes.length) html += `<ul class="notes small">${r.notes.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>`;
  el.innerHTML = html;
}
