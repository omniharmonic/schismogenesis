// Click into the map: a card for any thinker (their stated positions, quote by quote, beside
// your answers) and for any school (who is in it, what it agrees on, where it argues inside).
import { agreement, plainStances } from "./placement.js";
import { badge, esc, mapSVG, markSelected, nodeMembers, schoolMembers, wireMap } from "./map.js";
import { attachHoverCard } from "./hovercard.js";

const LEVEL = ["Camp", "School", "Branch", "Close circle"];

/** The chain of groups from the widest camp down to this one. */
function lineage(bundle, id) {
  const out = [];
  for (let n = bundle.tree?.nodes?.[id]; n; n = bundle.tree.nodes[n.parent]) out.unshift(n);
  return out;
}

/** Clickable steps from a camp down to a group (or to where a person sits). */
function crumbs(bundle, ids) {
  return ids.map((id) => {
    const n = bundle.tree.nodes[id];
    return `<button class="link-button crumb" data-node="${esc(id)}">${esc(n.label)}</button>`;
  }).join(`<span class="crumb-sep" aria-hidden="true">›</span>`);
}

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
  const link = (label) => {
    const camp = bundle.tree?.roots?.find((r) => bundle.tree.nodes[r].label === label);
    return camp ? `<button class="link-button" data-node="${esc(camp)}">${esc(label)}</button>`
      : `<button class="link-button" data-school="${esc(label)}">${esc(label)}</button>`;
  };
  // where they sit: the chain of groups as deep as their evidence goes, or between two camps
  const school = t.path?.length ? crumbs(bundle, t.path)
    : t.school ? link(t.school)
    : t.between ? `between ${link(t.between[0])} and ${link(t.between[1])}`
    : `<button class="link-button" data-school="">not yet grouped</button>`;
  return `<header class="card-head">
      ${badge(t, "big")}
      <div><h3 tabindex="-1">${esc(t.name)}</h3><p class="small muted">${t.path?.length ? "" : "School: "}${school}${t.provisional ? ". A newer voice: placed by agreement with the others, and grouped only on the positions that set a school apart." : ""}</p></div>
    </header>
    ${summary}
    ${(bundle.voices?.[id] || []).length ? `<h4>In their own words</h4><ul class="positions voices">${bundle.voices[id].map((v) => `<li>
        <p class="voice-position">${esc(v.position)}</p>
        <blockquote class="voice">“${esc(v.quote)}”<cite><a href="${esc(v.url)}" target="_blank" rel="noopener">${esc(v.work)}</a></cite></blockquote></li>`).join("")}</ul>` : ""}
    ${rows.length ? "" : `<p class="muted">We haven't found this person taking a clear side on any of the ${bundle.anchors.length} statements yet.</p>`}
    ${groups.map(([title, list]) => `<h4>${title}</h4><ul class="positions">${list.map((r) => `<li>
        <p class="serif">${esc(r.a.text)}</p>
        <p class="sides">${chip(r.item.a, SIDE)}${r.you !== undefined ? chip(r.you, YOU) : ""}<a class="small" href="/s/${esc(r.a.id)}">Everyone on this</a></p>
        ${quoteHTML(r.item)}</li>`).join("")}</ul>`).join("")}`;
}

/** A school: members, what it holds together, where it argues, and how you compare. */
export function schoolCard(bundle, label, answers = {}) {
  const camp = label && bundle.tree?.roots?.find((r) => bundle.tree.nodes[r].label === label);
  if (camp) return nodeCard(bundle, camp, answers);
  const ids = schoolMembers(bundle, label);
  if (label === "") {
    return `<header class="card-head"><div><h3 tabindex="-1">Not yet grouped</h3>
      <p class="small muted">${ids.length} thinkers we don't place in a school yet. A voice joins a school only when it clearly holds the positions that set that school apart, not just views most people share. Some sit between two schools; for others we haven't read enough of their work. As we read more, some will join a school and some may start a new one.</p></div></header>
      <ul class="positions">${ids.map((id) => { const t = bundle.thinkers.find((x) => x.id === id); return `<li><button class="person is-new" data-thinker="${esc(id)}">${badge(t)}${esc(t.name)}</button>
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
    return `<li><button class="person${core.has(id) ? "" : " is-new"}" data-thinker="${esc(id)}">${badge(t)}${esc(t.name)}${score}</button></li>`;
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


/** Where a group's members agree and where they split, on the survey's statements. */
function positionsHTML(bundle, ids, answers) {
  const plain = plainStances(bundle);
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
  const row = (e, argue) => `<li><p class="serif">${esc(e.a.text)}</p><p class="sides">${argue
      ? `<span class="chip split">${e.up} agree, ${e.n - e.up} disagree</span>`
      : `<span class="chip ${CLS[e.side]}">${e.side === 1 ? "Agree" : "Disagree"}, ${e.side === 1 ? e.up : e.n - e.up} of ${e.n}</span>`}${e.you !== undefined ? chip(e.you, YOU) : ""}</p></li>`;
  return `${yours.length ? `<p class="card-score">You side with this group on <b>${withYou} of ${yours.length}</b> statements where it leans one way.</p>` : ""}
    ${leaning.length ? `<h4>What they hold together</h4><ul class="positions">${leaning.slice(0, 8).map((e) => row(e, false)).join("")}</ul>` : ""}
    ${argued.length ? `<h4>Where they argue among themselves</h4><ul class="positions">${argued.slice(0, 5).map((e) => row(e, true)).join("")}</ul>` : ""}`;
}

/** A group anywhere in the drill-down: where it sits, the groups inside it, who is in it. */
export function nodeCard(bundle, id, answers = {}) {
  const n = bundle.tree?.nodes?.[id];
  if (!n) return `<p>That group isn't on this map.</p>`;
  const byId = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t]));
  const agree = agreement(answers, plainStances(bundle));
  const ids = nodeMembers(bundle, id);
  const drew = new Set(n.members);
  const chain = lineage(bundle, id);
  const person = (pid) => {
    const t = byId[pid], r = agree[pid];
    if (!t) return "";
    const score = r && r.n >= 3 ? `<span class="small muted">${r.k}/${r.n}</span>` : "";
    return `<li><button class="person${drew.has(pid) ? "" : " is-new"}" data-thinker="${esc(pid)}">${badge(t)}${esc(t.name)}${score}</button></li>`;
  };
  const kids = n.children.map((c) => bundle.tree.nodes[c]);
  const inKids = new Set(kids.flatMap((k) => nodeMembers(bundle, k.id)));
  const loose = ids.filter((pid) => !inKids.has(pid));
  const together = Math.round(n.cohesion * 100);
  return `<header class="card-head"><div>
      ${chain.length > 1 ? `<p class="crumbs small">${crumbs(bundle, chain.slice(0, -1).map((x) => x.id))}</p>` : ""}
      <p class="eyebrow-level small muted">${LEVEL[Math.min(n.level, LEVEL.length - 1)]}${kids.length ? `, ${kids.length} groups inside` : ""}</p>
      <h3 tabindex="-1">${esc(n.label)}</h3>
      <p class="serif">${esc(n.note)}</p>
      <p class="small muted">${ids.length} thinkers. When we redraw the groups hundreds of times from resampled evidence, two of them land together ${together}% of the time. A group is something the data finds, not a label they chose.</p></div></header>
    ${kids.length ? `<h4>Groups inside</h4><ul class="subgroups">${kids.map((k) => {
      const kidIds = nodeMembers(bundle, k.id);
      return `<li><button class="school-card small" data-node="${esc(k.id)}">
        <span class="school-name">${esc(k.label)}</span>
        <span class="faces" aria-hidden="true">${kidIds.slice(0, 6).map((x) => `${badge(byId[x])}`).join("")}${kidIds.length > 6 ? `<span class="more">+${kidIds.length - 6}</span>` : ""}</span>
        <span class="small muted">${kidIds.length} thinkers, together ${Math.round(k.cohesion * 100)}% of the time</span></button></li>`;
    }).join("")}</ul>` : ""}
    <h4>${kids.length ? "Everyone in it" : "Who is in it"}</h4>
    <ul class="people-chips">${ids.map(person).join("")}</ul>
    ${kids.length && loose.length ? `<p class="small muted">${loose.map((x) => esc(byId[x]?.name || x)).join(", ")} ${loose.length === 1 ? "sits" : "sit"} in this ${LEVEL[Math.min(n.level, 3)].toLowerCase()} without a closer group yet.</p>` : ""}
    ${positionsHTML(bundle, ids, answers)}`;
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
      <span class="faces" aria-hidden="true">${loose.slice(0, 7).map((id) => `${badge(byId[id])}`).join("")}${loose.length > 7 ? `<span class="more">+${loose.length - 7}</span>` : ""}</span>
      <span class="small muted">${loose.length} thinkers whose outlook doesn't yet match a school</span></button></li>` : "";
  const campOf = Object.fromEntries((bundle.tree?.roots || []).map((r) => [bundle.tree.nodes[r].label, r]));
  return `<ul class="school-grid">${schools.map((s) => {
    const node = campOf[s.label];
    const ids = node ? nodeMembers(bundle, node) : schoolMembers(bundle, s.label);
    const best = ids.map((id) => rank[id]).filter(Boolean).sort((a, b) => b.s - a.s)[0];
    const near = order[0] === s.label ? `<span class="tag">Your camp</span>` : "";
    const inside = node ? bundle.tree.nodes[node].children.map((c) => bundle.tree.nodes[c].label) : [];
    return `<li><button class="school-card" ${node ? `data-node="${esc(node)}"` : `data-school="${esc(s.label)}"`}>
      <span class="school-name">${esc(s.label)}</span>${near}
      <span class="faces" aria-hidden="true">${ids.slice(0, 7).map((id) => `${badge(byId[id])}`).join("")}${ids.length > 7 ? `<span class="more">+${ids.length - 7}</span>` : ""}</span>
      <span class="small muted">${ids.length} thinkers${best ? `. Closest to you: ${esc(best.name)}, ${best.k} of ${best.n}` : ""}</span>
      ${inside.length ? `<span class="small inside">Inside: ${inside.map(esc).join(" · ")}</span>` : ""}
    </button></li>`;
  }).join("")}${looseCard}</ul>`;
}

/**
 * Wire a map, a panel and (optionally) a school grid together. Selecting anything fills the
 * panel; on narrow screens the panel is scrolled into view. Back returns to the previous card.
 */
export function explorer({ bundle, answers = {}, mapEl, panelEl, gridEl = null, intro = "", mapOptions = null }) {
  const history = [];
  let current = null;
  let drawnFocus = null, focusNow = null;
  const render = () => {
    const back = history.length ? `<button class="link-button back" data-back>Back</button>` : "";
    const close = current ? `<button class="link-button" data-close>Close</button>` : "";
    panelEl.innerHTML = current
      ? `<div class="panel-bar">${back}${close}</div>${current.thinker ? thinkerCard(bundle, current.thinker, answers)
        : current.node ? nodeCard(bundle, current.node, answers) : schoolCard(bundle, current.school, answers)}`
      : intro;
    // drilling into a group redraws the map around it: its inner groups become the regions
    const focus = current?.node || (current?.thinker ? null : focusNow);
    if (mapOptions && focus !== drawnFocus) {
      mapEl.innerHTML = mapSVG(bundle, { ...mapOptions, focus });
      drawnFocus = focus;
    }
    markSelected(mapEl, current || {});
    if (!current) return;
    panelEl.querySelector("h3")?.focus({ preventScroll: true });
    if (matchMedia("(max-width: 899px)").matches) panelEl.scrollIntoView({ behavior: "smooth", block: "start" });
    else panelEl.scrollTop = 0;
  };
  const open = (next) => {
    if (current && (current.thinker !== next.thinker || current.school !== next.school || current.node !== next.node)) history.push(current);
    current = next;
    if (next.node) focusNow = next.node;
    else if (next.school !== undefined) focusNow = null;
    render();
  };
  const handlers = { onThinker: (id) => open({ thinker: id }), onSchool: (label) => open({ school: label }),
    onNode: (id) => open({ node: id }) };
  wireMap(mapEl, handlers);
  if (gridEl) wireMap(gridEl, handlers);
  // hovering a circle shows a short card; its "See full profile" opens this panel's full card
  attachHoverCard(mapEl, { bundle, answers, result: mapOptions?.result || null, onProfile: handlers.onThinker });
  panelEl.addEventListener("click", (e) => {
    if (e.target.closest("[data-back]")) {
      current = history.pop() || null;
      focusNow = current?.node || (current?.thinker ? focusNow : null);
      render();
      return;
    }
    if (e.target.closest("[data-close]")) { history.length = 0; current = null; focusNow = null; render(); return; }
    const t = e.target.closest("[data-thinker]");
    if (t) return open({ thinker: t.dataset.thinker });
    const g = e.target.closest("[data-node]");
    if (g) return open({ node: g.dataset.node });
    const s = e.target.closest("[data-school]");
    if (s) open({ school: s.dataset.school });
  });
  render();
  // redraw the map in place (e.g. once the people layer has loaded into mapOptions)
  const redraw = () => {
    if (!mapOptions) return;
    mapEl.innerHTML = mapSVG(bundle, { ...mapOptions, focus: drawnFocus });
    markSelected(mapEl, current || {});
  };
  return { open, redraw };
}
