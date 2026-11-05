// The crowd beside the thinkers: people who added their answers (GET /api/map/people), the
// "Thinkers / People / Both" switch above a map, and where the crowd and the thinkers split most.
// Nothing here sends anything about the visitor.
import { esc } from "./map.js";

/** The server's answer, made safe to use: a missing endpoint (404) or a failure is "no people". */
export function normalisePeople(d) {
  const ok = d && typeof d === "object";
  return {
    available: Boolean(ok),
    min_cell: ok && Number.isFinite(d.min_cell) ? d.min_cell : 10,
    count: ok && Number.isFinite(d.count) ? d.count : 0,
    people: ok && Array.isArray(d.people) ? d.people.filter((p) => Number.isFinite(p?.x) && Number.isFinite(p?.y)) : [],
  };
}

let cached = null;
/** Fetched once per page. */
export function fetchPeople() {
  cached ||= fetch("/api/map/people")
    .then((r) => (r.ok ? r.json() : null))
    .catch(() => null)
    .then(normalisePeople);
  return cached;
}

/** The line under the switch while there are too few people to show any. */
export function peopleNote({ min_cell, count, people }) {
  if (people.length) return "";
  return `People appear here once ${min_cell} have added their answers (now ${count}).`;
}

export const LAYERS = [["thinkers", "Thinkers"], ["people", "People"], ["both", "Both"]];

export function layerSwitchHTML(current = "both") {
  return `<div class="layer-switch" role="group" aria-label="Show on the map">${LAYERS.map(([v, label]) =>
    `<button type="button" data-layer-pick="${v}" aria-pressed="${v === current}">${label}</button>`).join("")}</div>`;
}

/**
 * Put the switch above a map. `mapEl` keeps the chosen layer in data-layer, which survives the
 * map being redrawn (map.css hides or fades by it). Returns { set(crowd) } to fill in the note.
 */
export function mountLayerSwitch(mapEl, { initial = "both", onChange = null } = {}) {
  const wrap = document.createElement("div");
  wrap.className = "layer-bar";
  wrap.innerHTML = `${layerSwitchHTML(initial)}<p class="small muted layer-note" role="status"></p>`;
  (mapEl.closest(".explore-grid") || mapEl).before(wrap);
  mapEl.dataset.layer = initial;
  const note = wrap.querySelector(".layer-note");
  let crowd = null;
  const paint = () => {
    const mode = mapEl.dataset.layer;
    note.textContent = mode !== "thinkers" && crowd ? peopleNote(crowd) : "";
    note.hidden = !note.textContent;
  };
  wrap.addEventListener("click", (e) => {
    const b = e.target.closest("[data-layer-pick]");
    if (!b) return;
    mapEl.dataset.layer = b.dataset.layerPick;
    for (const x of wrap.querySelectorAll("[data-layer-pick]")) x.setAttribute("aria-pressed", String(x === b));
    paint();
    onChange?.(b.dataset.layerPick);
  });
  paint();
  return { set(c) { crowd = c; paint(); } };
}

/**
 * Where the crowd and the thinkers split most: statements by |people's agree share − thinkers'
 * agree share|, largest first. Uses the results' own `gap` (only present once a statement has
 * enough decided answers), so nothing is shown about too few people.
 */
export function topGaps(statements, n = 5) {
  return (statements || [])
    .filter((s) => typeof s.gap === "number" && typeof s.agree_share === "number")
    .sort((a, b) => Math.abs(b.gap) - Math.abs(a.gap) || a.id.localeCompare(b.id))
    .slice(0, n);
}

const pct = (x) => `${Math.round(x * 100)}%`;

export function gapsHTML(statements, n = 5) {
  const rows = topGaps(statements, n);
  if (!rows.length) return "";
  return `<section class="gaps" aria-labelledby="gaps-title">
    <h2 id="gaps-title">Where the crowd and the experts split most</h2>
    <p class="muted">The statements where the share of people here who agree is furthest from the share of thinkers who agree.</p>
    <ol class="gap-list">${rows.map((s) => {
      const lo = Math.min(s.agree_share, s.thinkers_agree_share), hi = Math.max(s.agree_share, s.thinkers_agree_share);
      return `<li><a href="/s/${esc(s.id)}"><span class="serif gap-text">${esc(s.text)}</span>
        <span class="gap-track" role="img" aria-label="People here ${pct(s.agree_share)} agree; thinkers ${pct(s.thinkers_agree_share)} agree">
          <span class="gap-span" style="left:${lo * 100}%;width:${(hi - lo) * 100}%"></span>
          <span class="gap-dot crowd" style="left:${s.agree_share * 100}%"></span>
          <span class="gap-dot thinkers" style="left:${s.thinkers_agree_share * 100}%"></span></span>
        <span class="gap-note small"><span><i class="gap-key crowd" aria-hidden="true"></i>People here: <b>${pct(s.agree_share)}</b> agree</span><span><i class="gap-key thinkers" aria-hidden="true"></i>Thinkers: <b>${pct(s.thinkers_agree_share)}</b> agree</span></span></a></li>`;
    }).join("")}</ol>
  </section>`;
}
