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
    bins: ok ? normaliseBins(d.bins) : null,
  };
}

/** Hex-bin counts ({size, cells: [[x, y, n], ...]}) made safe; null when absent or empty. */
export function normaliseBins(b) {
  if (!b || typeof b !== "object" || !(Number(b.size) > 0) || !Array.isArray(b.cells)) return null;
  const cells = b.cells.filter((c) => Array.isArray(c) && Number.isFinite(c[0]) && Number.isFinite(c[1]) && Number.isFinite(c[2]) && c[2] > 0);
  return cells.length ? { size: Number(b.size), cells } : null;
}

/** Whether there is any crowd to draw: people, or hexagon counts. */
export const hasCrowd = (crowd) => Boolean(crowd?.people?.length || crowd?.bins);

/** The map options for a crowd (mapSVG's people, bins and the head count). */
export const crowdOptions = (crowd) => ({ people: crowd.people, bins: crowd.bins, peopleCount: crowd.count });

/**
 * Pointy-top hexagon bins, the same way the server makes them (account_routes.hex_bins): `size`
 * is centre to corner in the points' own units. Returns {size, cells: [[x, y, n], ...]}, the
 * fullest cell first. Used by tests and to check what the server sends.
 */
export function hexBins(points, size) {
  const counts = new Map();
  for (const p of points || []) {
    if (!Number.isFinite(p?.x) || !Number.isFinite(p?.y)) continue;
    const x = (Math.sqrt(3) / 3 * p.x - p.y / 3) / size, z = (2 / 3 * p.y) / size, y = -x - z;
    let rx = Math.round(x), ry = Math.round(y), rz = Math.round(z);
    const dx = Math.abs(rx - x), dy = Math.abs(ry - y), dz = Math.abs(rz - z);
    if (dx > dy && dx > dz) rx = -ry - rz; else if (dy <= dz) rz = -rx - ry;
    const key = `${rx},${rz}`;
    counts.set(key, (counts.get(key) || 0) + 1);
  }
  const r2 = (v) => Math.round(v * 100) / 100;
  const cells = [...counts].map(([k, n]) => {
    const [q, r] = k.split(",").map(Number);
    return [r2(size * Math.sqrt(3) * (q + r / 2)), r2(size * 1.5 * r), n];
  });
  return { size: Math.round(size * 1000) / 1000, cells: cells.sort((a, b) => b[2] - a[2]) };
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
export function peopleNote({ min_cell, count, people, bins = null }) {
  if (people.length || bins) return "";
  return `People appear here once ${min_cell} have added their answers (now ${count}).`;
}

export const LAYERS = [["thinkers", "Thinkers"], ["people", "People"], ["both", "Both"]];

export function layerSwitchHTML(current = "both") {
  return `<div class="layer-switch" role="group" aria-label="Show on the map">${LAYERS.map(([v, label]) =>
    `<button type="button" data-layer-pick="${v}" aria-pressed="${v === current}">${label}</button>`).join("")}</div>`;
}

/**
 * Put the switch above a map. `mapEl` keeps the chosen layer in data-layer, which survives the
 * map being redrawn (map.css hides or fades by it). `findMe` adds a "Find me" button (pass it
 * only when the map draws your "You" mark). Returns { set(crowd), pick(layer) }.
 */
export function mountLayerSwitch(mapEl, { initial = "both", onChange = null, findMe = false } = {}) {
  const wrap = document.createElement("div");
  wrap.className = "layer-bar";
  wrap.innerHTML = `${layerSwitchHTML(initial)}${findMe ? `<button type="button" class="find-me" data-find-me>Find me</button>` : ""}<p class="small muted layer-note" role="status"></p>`;
  (mapEl.closest(".explore-grid") || mapEl).before(wrap);
  mapEl.dataset.layer = initial;
  const note = wrap.querySelector(".layer-note");
  let crowd = null, found = "";
  const paint = () => {
    const mode = mapEl.dataset.layer;
    note.textContent = found || (mode !== "thinkers" && crowd ? peopleNote(crowd) : "");
    note.hidden = !note.textContent;
  };
  const pick = (mode) => {
    mapEl.dataset.layer = mode;
    for (const x of wrap.querySelectorAll("[data-layer-pick]")) x.setAttribute("aria-pressed", String(x.dataset.layerPick === mode));
    paint();
    onChange?.(mode);
  };
  wrap.addEventListener("click", (e) => {
    const b = e.target.closest("[data-layer-pick]");
    if (b) { found = ""; pick(b.dataset.layerPick); return; }
    if (e.target.closest("[data-find-me]")) {
      if (mapEl.dataset.layer !== "both") pick("both");
      found = findYou(mapEl) ? "You're ringed in blue on the map." : "Answer a few more statements to appear on the map.";
      paint();
      setTimeout(() => { found = ""; paint(); }, 5000);
    }
  });
  paint();
  return { set(c) { crowd = c; paint(); }, pick };
}

let foundTimer = 0;
/**
 * Ring your "You" mark (a pulse, or a still ring with reduced motion) and bring it into view.
 * Returns whether there was a mark to find.
 */
export function findYou(mapEl) {
  const mark = mapEl.querySelector(".map-you-mark");
  if (!mark) return false;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  mapEl.querySelectorAll(".map-you-mark.is-found").forEach((m) => m.classList.remove("is-found"));
  void mark.getBoundingClientRect(); // restart the pulse on a second press
  mark.classList.add("is-found");
  // a zoomed map pans to you first (map-zoom.js)
  mark.dispatchEvent(new CustomEvent("thinkermap:reveal", { bubbles: true }));
  mark.scrollIntoView({ block: "center", inline: "center", behavior: reduce ? "auto" : "smooth" });
  clearTimeout(foundTimer);
  foundTimer = setTimeout(() => mark.classList.remove("is-found"), 6000);
  return true;
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
