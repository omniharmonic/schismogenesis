// Public results: aggregates only, from people who chose to add their answers.
import { esc } from "./map.js";
import { handoffHTML } from "./site-config.js";

const LAYER = { ontological: "What AI is", epistemic: "How we know", axiological: "What matters",
  empirical: "What will happen", praxis: "What to do" };
const pct = (x) => `${Math.round(x * 100)}%`;
const tip = document.getElementById("tip");

function hover(root) {
  root.addEventListener("pointermove", (e) => {
    const t = e.target.closest("[data-tip]");
    if (!t) { tip.hidden = true; return; }
    tip.textContent = t.dataset.tip; tip.hidden = false;
    tip.style.left = `${Math.min(e.clientX + 14, innerWidth - 300)}px`; tip.style.top = `${e.clientY + 14}px`;
  });
  root.addEventListener("pointerleave", () => (tip.hidden = true));
}

function statementRow(s) {
  const total = s.agree + s.disagree + s.unsure || 1;
  const [a, u, d] = [s.agree / total, s.unsure / total, s.disagree / total];
  const marker = s.agree_share === null ? "" : `<span class="marker" style="left:calc(${s.thinkers_agree_share * 100}% - 1px)" data-tip="Thinkers we read: ${pct(s.thinkers_agree_share)} agree (${s.thinkers} with a stated view)"></span>`;
  return `<div class="srow">
    <div><a class="serif" style="color:inherit" href="/s/${esc(s.id)}">${esc(s.text)}</a><br><span class="small muted">${LAYER[s.layer]}</span></div>
    <div><div class="bar" role="img" aria-label="${pct(a)} agree, ${pct(u)} unsure, ${pct(d)} disagree; thinkers ${pct(s.thinkers_agree_share)} agree">
      <i style="width:${a * 100}%;background:var(--yes)" data-tip="Agree: ${s.agree} (${pct(a)})"></i>
      <i style="width:${u * 100}%;background:var(--mid)" data-tip="Unsure: ${s.unsure} (${pct(u)})"></i>
      <i style="width:${d * 100}%;background:var(--no)" data-tip="Disagree: ${s.disagree} (${pct(d)})"></i>${marker}</div>
      <div class="barnote"><span>${pct(a)} agree</span><span>${s.answered} answered</span><span>${pct(d)} disagree</span></div></div></div>`;
}

function hbars(rows, label, value, tipText) {
  // shares run on a 0–100% scale, so a bar's length means the same thing in every chart
  return `<ul class="hbars">${rows.map((r) => `<li><span>${esc(label(r))}</span>
    <span class="track"><span class="fill" style="display:block;width:${value(r) * 100}%" data-tip="${esc(tipText(r))}"></span></span>
    <span class="num">${pct(value(r))}</span></li>`).join("")}</ul>`;
}

// diverging cell colour: disagree pink, through the panel colour, to agree green
const heatColour = (share) => {
  const t = Math.abs(share - 0.5) * 2;
  const hue = share >= 0.5 ? "var(--yes)" : "var(--no)";
  return `color-mix(in srgb, ${hue} ${Math.round(12 + t * 70)}%, var(--sheet))`;
};

function crosstab(r) {
  const c = r.crosstab;
  const text = Object.fromEntries(r.statements.map((s) => [s.id, s.text]));
  const head = `<tr><th>Statement</th>${c.schools.map((s) => `<th scope="col">${esc(s)}</th>`).join("")}</tr>`;
  const rows = r.statements.map((s) => `<tr><th scope="row" class="stmt">${esc(text[s.id])}</th>${c.schools.map((school) => {
    const cell = c.cells[s.id][school];
    return cell ? `<td style="background:${heatColour(cell.agree_share)}" data-tip="${esc(school)}: ${pct(cell.agree_share)} agree (${cell.n} people)">${pct(cell.agree_share)}</td>` : `<td class="empty" data-tip="Fewer than ${r.min_cell} people">·</td>`;
  }).join("")}</tr>`).join("");
  return `<div class="scroll"><table class="heat">${head}${rows}</table></div>`;
}

// How the public thinkers split on each statement, from the fingerprint bundle: no visitor data.
async function thinkerSplit() {
  const bundle = await (await fetch("/fingerprint.json")).json();
  const rows = bundle.anchors.map((a) => {
    const e = Object.values(bundle.stances[a.id] || {});
    const up = e.filter((i) => i.a === 1).length, down = e.length - up;
    return { a, up, down, n: e.length, split: e.length ? 1 - Math.abs(up - down) / e.length : 0 };
  }).sort((x, y) => y.split - x.split || y.n - x.n);
  document.getElementById("thinker-split").innerHTML = `<div class="legend"><span><i class="key" style="background:var(--yes)"></i>Thinkers who agree</span><span><i class="key" style="background:var(--no)"></i>Thinkers who disagree</span></div>
    ${rows.map(({ a, up, down, n }) => `<div class="srow">
      <div><a class="serif" style="color:inherit" href="/s/${esc(a.id)}">${esc(a.text)}</a><br><span class="small muted">${LAYER[a.layer]}</span></div>
      <div><div class="bar" role="img" aria-label="${up} thinkers agree, ${down} disagree">
        <i style="width:${n ? (up / n) * 100 : 0}%;background:var(--yes)" data-tip="Agree: ${up} thinkers"></i>
        <i style="width:${n ? (down / n) * 100 : 0}%;background:var(--no)" data-tip="Disagree: ${down} thinkers"></i></div>
        <div class="barnote"><span>${up} agree</span><span>${n} with a stated view</span><span>${down} disagree</span></div></div></div>`).join("")}`;
}

let sort = "split";

function render(r) {
  const el = document.getElementById("results");
  const notes = r.notes.length ? `<ul class="notes small">${r.notes.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>` : "";
  const tiles = `<div class="tiles">
    <div class="tile"><b>${r.contributors}</b><span>people added their answers</span></div>
    <div class="tile"><b>${r.profiles.published}</b><span>published a share link</span></div>
    <div class="tile"><b>${r.profiles.verified}</b><span>with a verified account</span></div></div>`;
  if (!r.statements.length) {
    const need = r.min_cell || 10;
    const rest = r.notes.filter((n) => !n.startsWith("Results appear"));
    const notes = rest.length ? `<ul class="notes small">${rest.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>` : "";
    el.innerHTML = `${tiles}
      <div class="waiting"><p><b>${r.contributors} of ${need}</b> people so far. Results appear at ${need}, so no one can be picked out.</p>
        <div class="meter" role="progressbar" aria-valuemin="0" aria-valuemax="${need}" aria-valuenow="${r.contributors}"><span style="width:${Math.min(100, (r.contributors / need) * 100)}%"></span></div>
        <p><a class="button primary" href="/">Take it, and add your answers</a></p></div>
      <h2>Meanwhile: how the thinkers split</h2>
      <p class="muted">Each statement, with the public thinkers we read on each side. Most divided first. Select a statement to read their own words.</p>
      <div id="thinker-split"><p class="muted">Loading…</p></div>${notes}`;
    thinkerSplit();
    return;
  }
  const sorted = [...r.statements].sort((a, b) => {
    if (sort === "order") return 0;
    const key = sort === "split" ? "split" : "gap";
    const av = a[key] ?? -1, bv = b[key] ?? -1;
    return sort === "gap" ? Math.abs(bv) - Math.abs(av) : bv - av;
  });
  el.innerHTML = `${tiles}
    <h2>Statement by statement</h2>
    <div class="legend"><span><i class="key" style="background:var(--yes)"></i>Agree</span><span><i class="key" style="background:var(--mid)"></i>Unsure</span><span><i class="key" style="background:var(--no)"></i>Disagree</span><span><i class="key" style="background:var(--ink);width:3px"></i>How the thinkers split</span></div>
    <div class="sortbar" role="group" aria-label="Sort statements">
      <button data-sort="split" aria-pressed="${sort === "split"}">Most divided first</button>
      <button data-sort="gap" aria-pressed="${sort === "gap"}">Furthest from the thinkers</button>
      <button data-sort="order" aria-pressed="${sort === "order"}">Survey order</button></div>
    <div id="rows">${sorted.map(statementRow).join("")}</div>
    ${r.homes.length ? `<h2>Neighbourhoods</h2><p class="muted">The school of each person's nearest thinker.</p>
      ${hbars(r.homes, (h) => h.school, (h) => h.share, (h) => `${h.people} people`)}` : ""}
    ${r.nearest.length ? `<h2>Most-matched thinkers</h2><p class="muted">How often each thinker is someone's nearest.</p>
      ${hbars(r.nearest, (t) => t.name, (t) => t.share, (t) => `${t.people} people`)}` : ""}
    ${r.camps.length ? `<h2>Who leans with each camp</h2><p class="muted">Share of people who agree with a camp's thinkers on most statements where the camp takes a side.</p>
      ${hbars(r.camps, (c) => c.label, (c) => c.share_aligned, (c) => `${pct(c.share_aligned)} lean with ${c.label}`)}` : ""}
    ${r.crosstab ? `<h2>How each neighbourhood answers</h2><p class="muted">Share agreeing, among people whose nearest thinker is in that school. Green leans agree, pink leans disagree.</p>${crosstab(r)}` : ""}
    <details style="margin-top:28px"><summary>Table of every statement</summary><div class="scroll"><table class="camps-table">
      <tr><th>Statement</th><th>Agree</th><th>Unsure</th><th>Disagree</th><th>Thinkers agree</th></tr>
      ${r.statements.map((s) => `<tr><td>${esc(s.text)}</td><td>${s.agree}</td><td>${s.unsure}</td><td>${s.disagree}</td><td>${pct(s.thinkers_agree_share)}</td></tr>`).join("")}</table></div></details>
    ${notes}
    <p class="small muted">Updated ${new Date(r.computed_at).toLocaleString()}. People who add their answers aren't a random sample, so read this as "the people here", not "the public".</p>`;
  for (const b of el.querySelectorAll("[data-sort]")) b.onclick = () => { sort = b.dataset.sort; render(r); };
}

async function main() {
  hover(document.body);
  const room = new URLSearchParams(location.search).get("room");
  const r = await (await fetch(`/api/results${room ? `?room=${encodeURIComponent(room)}` : ""}`)).json();
  if (r.demo) document.getElementById("lede").outerHTML = `<div class="demo-banner">Demo results. These people are synthetic, made up to show how the page works.</div>`;
  render(r);
  document.getElementById("handoff").innerHTML = handoffHTML();
}

main();
