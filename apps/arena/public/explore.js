// Click into the map: a card for any thinker (their stated positions, quote by quote, beside
// your answers) and for any school (who is in it, what it agrees on, where it argues inside).
import { agreement, plainStances } from "./fingerprint.js";
import { esc, markSelected, schoolMembers, wireMap } from "./map.js";

const SIDE = { 1: "Agrees", "-1": "Disagrees" };
const YOU = { 1: "You agree", "-1": "You disagree", 0: "You're unsure" };
const CLS = { 1: "agree", "-1": "disagree", 0: "unsure" };
const LEAN = 0.7; // share of a school's readings on one side before we say it leans

function quoteHTML(item) {
  if (!item?.q) return "";
  return `<blockquote class="voice">“${esc(item.q)}”<cite><a href="${esc(item.url)}" target="_blank" rel="noopener">${esc(item.work)}</a></cite></blockquote>`;
}

function chip(v, words) {
  return `<span class="chip ${CLS[v]}">${words[v]}</span>`;
}

/** A thinker's stated positions on the season's statements, with yours alongside. */
export function thinkerCard(bundle, id, answers = {}) {
  const t = bundle.thinkers.find((x) => x.id === id);
  if (!t) return `<p>That thinker isn't on this map.</p>`;
  const rows = bundle.anchors
    .filter((a) => bundle.stances[a.id]?.[id])
    .map((a) => ({ a, item: bundle.stances[a.id][id], you: answers[a.id] }));
  const asked = rows.filter((r) => r.you === 1 || r.you === -1);
  const same = asked.filter((r) => r.you === r.item.a).length;
  const groups = [
    ["Where you split", rows.filter((r) => (r.you === 1 || r.you === -1) && r.you !== r.item.a)],
    ["Where you agree", rows.filter((r) => (r.you === 1 || r.you === -1) && r.you === r.item.a)],
    [asked.length ? "You didn't take a side" : "Their positions", rows.filter((r) => r.you !== 1 && r.you !== -1)],
  ].filter(([, list]) => list.length);
  const summary = asked.length
    ? `<p class="card-score">You agree on <b>${same} of ${asked.length}</b> statements you both took a side on.</p>`
    : "";
  const link = (label) => `<button class="link-button" data-school="${esc(label)}">${esc(label)}</button>`;
  // a voice whose distinctive positions fit two schools about equally is shown between them
  const school = t.school ? link(t.school)
    : t.between ? `between ${link(t.between[0])} and ${link(t.between[1])}`
    : `<button class="link-button" data-school="">not yet grouped</button>`;
  return `<header class="card-head">
      <span class="badge big" aria-hidden="true">${esc(t.initials)}</span>
      <div><h3 tabindex="-1">${esc(t.name)}</h3><p class="small muted">School: ${school}${t.provisional ? ". A newer voice: placed by agreement with the others, and grouped only on the positions that set a school apart." : ""}</p></div>
    </header>
    ${summary}
    ${(bundle.voices?.[id] || []).length ? `<h4>In their own words</h4><ul class="positions voices">${bundle.voices[id].map((v) => `<li>
        <p class="voice-position">${esc(v.position)}</p>
        <blockquote class="voice">“${esc(v.quote)}”<cite><a href="${esc(v.url)}" target="_blank" rel="noopener">${esc(v.work)}</a></cite></blockquote></li>`).join("")}</ul>` : ""}
    ${rows.length ? "" : `<p class="muted">We haven't found this person taking a clear side on any of the 24 statements yet.</p>`}
    ${groups.map(([title, list]) => `<h4>${title}</h4><ul class="positions">${list.map((r) => `<li>
        <p class="serif">${esc(r.a.text)}</p>
        <p class="sides">${chip(r.item.a, SIDE)}${r.you !== undefined ? chip(r.you, YOU) : ""}<a class="small" href="/s/${esc(r.a.id)}">Everyone on this</a></p>
        ${quoteHTML(r.item)}</li>`).join("")}</ul>`).join("")}`;
}

/** A school: members, what it holds together, where it argues, and how you compare. */
export function schoolCard(bundle, label, answers = {}) {
  const ids = schoolMembers(bundle, label);
  if (label === "") {
    return `<header class="card-head"><div><h3 tabindex="-1">Not yet grouped</h3>
      <p class="small muted">${ids.length} thinkers we don't place in a school yet. A voice joins a school only when it clearly holds the positions that set that school apart, not just views most people share. Some sit between two schools; for others we haven't read enough of their work. As we read more, some will join a school and some may start a new one.</p></div></header>
      <ul class="positions">${ids.map((id) => { const t = bundle.thinkers.find((x) => x.id === id); return `<li><button class="person is-new" data-thinker="${esc(id)}"><span class="badge" aria-hidden="true">${esc(t.initials)}</span>${esc(t.name)}</button>
        <p class="small muted" style="margin:6px 0 0">${t.between ? `Between the ${esc(t.between[0])} and the ${esc(t.between[1])}.` : "Too little of their writing so far to tell."}</p></li>`; }).join("")}</ul>`;
  }
  const core = new Set(bundle.schools.find((s) => s.label === label)?.members || []);
  const byId = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t]));
  const plain = plainStances(bundle);
  const agree = agreement(answers, plain);
  const leaning = [], argued = [];
  for (const a of bundle.anchors) {
    const sides = ids.map((m) => plain[a.id]?.[m]).filter((v) => v !== undefined);
    if (sides.length < 2) continue;
    const up = sides.filter((v) => v === 1).length;
    const share = Math.max(up, sides.length - up) / sides.length;
    const entry = { a, side: up * 2 >= sides.length ? 1 : -1, up, n: sides.length, you: answers[a.id] };
    if (share >= LEAN) leaning.push(entry); else argued.push(entry);
  }
  leaning.sort((x, y) => y.n - x.n);
  const yours = leaning.filter((e) => e.you === 1 || e.you === -1);
  const withYou = yours.filter((e) => e.you === e.side).length;
  const member = (id) => {
    const t = byId[id], r = agree[id];
    const score = r && r.n >= 3 ? `<span class="small muted">${r.k}/${r.n}</span>` : "";
    return `<li><button class="person${core.has(id) ? "" : " is-new"}" data-thinker="${esc(id)}"><span class="badge" aria-hidden="true">${esc(t.initials)}</span>${esc(t.name)}${score}</button></li>`;
  };
  const row = (e, argue) => `<li><p class="serif">${esc(e.a.text)}</p><p class="sides">${argue
      ? `<span class="chip split">${e.up} agree, ${e.n - e.up} disagree</span>`
      : `<span class="chip ${CLS[e.side]}">${e.side === 1 ? "Agree" : "Disagree"}, ${e.side === 1 ? e.up : e.n - e.up} of ${e.n}</span>`}${e.you !== undefined ? chip(e.you, YOU) : ""}</p></li>`;
  return `<header class="card-head"><div><h3 tabindex="-1">${esc(label)}</h3>
      <p class="small muted">${ids.length} thinkers${ids.length > core.size ? `, ${ids.length - core.size} of them new voices placed here by agreement` : ""}. A school is a group the data finds, not a label they chose.</p></div></header>
    ${yours.length ? `<p class="card-score">You side with this school on <b>${withYou} of ${yours.length}</b> statements where it leans one way.</p>` : ""}
    <ul class="people-chips">${ids.map(member).join("")}</ul>
    ${leaning.length ? `<h4>What they hold together</h4><ul class="positions">${leaning.slice(0, 8).map((e) => row(e, false)).join("")}</ul>` : ""}
    ${argued.length ? `<h4>Where they argue among themselves</h4><ul class="positions">${argued.slice(0, 5).map((e) => row(e, true)).join("")}</ul>` : ""}`;
}

/** One card per school, ordered by how close you are (or by size before you've answered). */
export function schoolGrid(bundle, result = null) {
  const order = result?.schools?.map((s) => s.label) || [];
  const schools = [...bundle.schools].sort((a, b) => {
    const ia = order.indexOf(a.label), ib = order.indexOf(b.label);
    return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib) || b.members.length - a.members.length;
  });
  const byId = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t]));
  const rank = Object.fromEntries((result?.ranked || []).map((r) => [r.id, r]));
  const loose = schoolMembers(bundle, "");
  const looseCard = loose.length ? `<li><button class="school-card is-loose" data-school="">
      <span class="school-name">Not yet grouped</span>
      <span class="faces" aria-hidden="true">${loose.slice(0, 7).map((id) => `<span class="badge">${esc(byId[id].initials)}</span>`).join("")}${loose.length > 7 ? `<span class="more">+${loose.length - 7}</span>` : ""}</span>
      <span class="small muted">${loose.length} thinkers whose outlook doesn't yet match a school</span></button></li>` : "";
  return `<ul class="school-grid">${schools.map((s) => {
    const ids = schoolMembers(bundle, s.label);
    const best = ids.map((id) => rank[id]).filter(Boolean).sort((a, b) => b.s - a.s)[0];
    const near = order[0] === s.label ? `<span class="tag">Your school</span>` : "";
    return `<li><button class="school-card" data-school="${esc(s.label)}">
      <span class="school-name">${esc(s.label)}</span>${near}
      <span class="faces" aria-hidden="true">${ids.slice(0, 7).map((id) => `<span class="badge">${esc(byId[id].initials)}</span>`).join("")}${ids.length > 7 ? `<span class="more">+${ids.length - 7}</span>` : ""}</span>
      <span class="small muted">${ids.length} thinkers${best ? `. Closest to you: ${esc(best.name)}, ${best.k} of ${best.n}` : ""}</span>
    </button></li>`;
  }).join("")}${looseCard}</ul>`;
}

/**
 * Wire a map, a panel and (optionally) a school grid together. Selecting anything fills the
 * panel; on narrow screens the panel is scrolled into view. Back returns to the previous card.
 */
export function explorer({ bundle, answers = {}, mapEl, panelEl, gridEl = null, intro = "" }) {
  const history = [];
  let current = null;
  const render = () => {
    const back = history.length ? `<button class="link-button back" data-back>Back</button>` : "";
    const close = current ? `<button class="link-button" data-close>Close</button>` : "";
    panelEl.innerHTML = current
      ? `<div class="panel-bar">${back}${close}</div>${current.thinker ? thinkerCard(bundle, current.thinker, answers) : schoolCard(bundle, current.school, answers)}`
      : intro;
    markSelected(mapEl, current || {});
    if (!current) return;
    panelEl.querySelector("h3")?.focus({ preventScroll: true });
    if (matchMedia("(max-width: 899px)").matches) panelEl.scrollIntoView({ behavior: "smooth", block: "start" });
    else panelEl.scrollTop = 0;
  };
  const open = (next) => {
    if (current && (current.thinker !== next.thinker || current.school !== next.school)) history.push(current);
    current = next;
    render();
  };
  const handlers = { onThinker: (id) => open({ thinker: id }), onSchool: (label) => open({ school: label }) };
  wireMap(mapEl, handlers);
  if (gridEl) wireMap(gridEl, handlers);
  panelEl.addEventListener("click", (e) => {
    if (e.target.closest("[data-back]")) { current = history.pop() || null; render(); return; }
    if (e.target.closest("[data-close]")) { history.length = 0; current = null; render(); return; }
    const t = e.target.closest("[data-thinker]");
    if (t) return open({ thinker: t.dataset.thinker });
    const s = e.target.closest("[data-school]");
    if (s) open({ school: s.dataset.school });
  });
  render();
  return { open };
}
