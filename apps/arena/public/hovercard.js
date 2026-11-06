// A short card about a thinker, shown when you hover, focus or tap their circle on a map drawn by
// mapSVG. One card element serves every map on the page; its content is built only when it opens.
import { badge, esc } from "./map.js";

const SHOW_DELAY = 120; // ms of hover before the card opens
const HIDE_DELAY = 160; // ms of grace to move the pointer from the circle into the card
const GAP = 10;         // px between the circle and the card
const EDGE = 8;         // px the card keeps from the viewport edges

const SIDE = { 1: "Agrees", "-1": "Disagrees" };

/** Where a thinker sits: their camp, and the school inside it when the evidence goes that deep. */
function placeOf(bundle, t) {
  const nodes = bundle.tree?.nodes || {};
  const path = (t.path || []).filter((id) => nodes[id]);
  if (path.length) {
    return { camp: nodes[path[0]].label, school: path.length > 1 ? nodes[path[1]].label : null };
  }
  if (t.school) return { camp: t.school, school: null };
  if (t.between) return { between: t.between };
  return { loose: true };
}

/** Up to three of their positions, sharpest splits first, preferring ones the visitor answered. */
function positionsOf(bundle, id, answers) {
  const rows = bundle.anchors
    .filter((a) => bundle.stances[a.id]?.[id])
    .map((a) => ({ a, side: bundle.stances[a.id][id].a, you: answers[a.id] }));
  const answered = (r) => (r.you === 1 || r.you === -1 ? 1 : 0);
  rows.sort((x, y) => answered(y) - answered(x) || (y.a.split_score || 0) - (x.a.split_score || 0));
  return rows.slice(0, 3);
}

/** The card's inner HTML. Exported for tests. */
export function hoverCardHTML(bundle, id, { answers = {}, result = null } = {}) {
  const t = bundle.thinkers.find((x) => x.id === id);
  if (!t) return "";
  const role = t.role || t.niche || t.tagline || "";
  const p = placeOf(bundle, t);
  const where = p.camp
    ? `<dl class="hc-where"><div><dt>Camp</dt><dd>${esc(p.camp)}</dd></div>${p.school ? `<div><dt>School</dt><dd>${esc(p.school)}</dd></div>` : ""}</dl>`
    : p.between
      ? `<p class="hc-where-line">Between the ${esc(p.between[0])} and the ${esc(p.between[1])}</p>`
      : `<p class="hc-where-line">Not yet grouped in a school</p>`;

  let score = "";
  if (result?.ranked) {
    const r = result.ranked.find((x) => x.id === id);
    score = r
      ? `<p class="hc-score">You agree on <b>${r.k} of ${r.n}</b> shared statements</p>`
      : `<p class="hc-score is-none">Too few shared statements to compare you</p>`;
  }

  const rows = positionsOf(bundle, id, answers);
  let positions = "";
  if (rows.length) {
    positions = `<ul class="hc-positions">${rows.map((r) => {
      const asked = r.you === 1 || r.you === -1;
      const same = asked && r.you === r.side;
      const you = asked
        ? `<span class="hc-you ${same ? "same" : "differ"}">${same ? "✓ like you" : "✗ unlike you"}</span>`
        : "";
      return `<li><span class="hc-side ${r.side === 1 ? "agree" : "disagree"}">${SIDE[r.side]}</span>${you}
        <span class="hc-text">${esc(r.a.text)}</span></li>`;
    }).join("")}</ul>`;
  } else if (bundle.voices?.[id]?.length) {
    positions = `<ul class="hc-positions">${bundle.voices[id].slice(0, 2).map((v) =>
      `<li><span class="hc-text">${esc(v.position)}</span></li>`).join("")}</ul>`;
  }

  return `<div class="hc-head">${badge(t, "hc-badge")}<div>
      <p class="hc-name">${esc(t.name)}</p>
      ${role ? `<p class="hc-role">${esc(role)}</p>` : ""}
      ${t.provisional ? `<p class="hc-role">A newer voice on the map</p>` : ""}
    </div></div>
    ${where}${score}${positions}
    <a class="hc-link" href="/people#${encodeURIComponent(id)}" data-profile="${esc(id)}">See full profile <span aria-hidden="true">→</span></a>`;
}

/**
 * The card for a person who chose to be shown on the map: their picture, name, @handle, bio and
 * nearest thinker. `p` is the person's data (from the map's data- attributes). Exported for tests.
 */
export function personCardHTML(p, bundle = null) {
  const nearest = p.nearest ? bundle?.thinkers?.find((t) => t.id === p.nearest)?.name || p.nearest : "";
  const pic = p.face
    ? `<span class="badge hc-badge has-face" aria-hidden="true"><img src="${esc(p.face)}" alt="" referrerpolicy="no-referrer"></span>`
    : `<span class="badge hc-badge" aria-hidden="true">${esc(String(p.name || "").trim().split(/\s+/).slice(0, 2).map((w) => w[0] || "").join("").toUpperCase())}</span>`;
  return `<div class="hc-head">${pic}<div>
      <p class="hc-name">${esc(p.name || "Someone who took it")}</p>
      ${p.handle ? `<p class="hc-role">@${esc(p.handle)}</p>` : ""}
    </div></div>
    ${p.bio ? `<p class="hc-bio">${esc(p.bio)}</p>` : ""}
    ${nearest ? `<p class="hc-score">Nearest: <b>${esc(nearest)}</b></p>` : ""}`;
}

// ---------- the one shared card ----------
let card = null;
let anchor = null;   // the map circle the card is about
let owner = null;    // the options of the map that opened it
let showTimer = 0, hideTimer = 0, shownAt = 0;

function ensureCard() {
  if (card) return card;
  card = document.createElement("div");
  card.className = "hovercard";
  card.id = "thinker-hovercard";
  card.setAttribute("role", "tooltip");
  card.hidden = true;
  card.addEventListener("pointerenter", () => clearTimeout(hideTimer));
  card.addEventListener("pointerleave", (e) => { if (e.pointerType !== "touch") scheduleHide(); });
  card.addEventListener("click", (e) => {
    const link = e.target.closest("[data-profile]");
    if (!link || !owner?.onProfile) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return; // new tab: let the link work
    e.preventDefault();
    const id = link.dataset.profile, open = owner.onProfile;
    hide();
    open(id);
  });
  document.body.append(card);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && anchor) hide(); });
  // a tap or click anywhere outside the card and its circle closes it
  document.addEventListener("pointerdown", (e) => {
    if (anchor && !card.contains(e.target) && !anchor.contains(e.target)) hide();
  }, true);
  // scrolling closes it, except the scroll a browser makes to bring a just-focused circle into view
  addEventListener("scroll", () => {
    if (!anchor) return;
    if (performance.now() - shownAt < 250) place(card, anchor); else hide();
  }, { passive: true });
  addEventListener("resize", () => { if (anchor) hide(); }, { passive: true });
  return card;
}

function place(el, target) {
  // one read of the circle, one of the card, then writes: no layout thrash
  const dot = (target.querySelector(".dot, .ring") || target).getBoundingClientRect();
  const w = el.offsetWidth, h = el.offsetHeight;
  const vw = document.documentElement.clientWidth, vh = innerHeight;
  const cx = dot.left + dot.width / 2, cy = dot.top + dot.height / 2;
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  let x, y, side;
  if (dot.right + GAP + w <= vw - EDGE) { side = "right"; x = dot.right + GAP; y = cy - h / 2; }
  else if (dot.left - GAP - w >= EDGE) { side = "left"; x = dot.left - GAP - w; y = cy - h / 2; }
  else if (dot.bottom + GAP + h <= vh - EDGE) { side = "below"; x = cx - w / 2; y = dot.bottom + GAP; }
  else if (dot.top - GAP - h >= EDGE) { side = "above"; x = cx - w / 2; y = dot.top - GAP - h; }
  else { // no room anywhere: the side with more space, the card shortened (it scrolls) so the circle stays visible
    side = vh - dot.bottom > dot.top ? "below" : "above";
    const room = Math.floor((side === "below" ? vh - dot.bottom : dot.top) - GAP - EDGE);
    el.style.maxHeight = `${room}px`;
    const fit = Math.min(h, room);
    x = cx - w / 2; y = side === "below" ? dot.bottom + GAP : dot.top - GAP - fit;
  }
  x = clamp(x, EDGE, Math.max(EDGE, vw - w - EDGE));
  y = clamp(y, EDGE, Math.max(EDGE, vh - h - EDGE));
  el.style.transform = `translate(${Math.round(x)}px, ${Math.round(y)}px)`;
  el.dataset.side = side;
}

function show(target, opts) {
  clearTimeout(showTimer); clearTimeout(hideTimer);
  const el = ensureCard();
  if (anchor === target && !el.hidden) return;
  anchor?.removeAttribute("aria-describedby");
  anchor = target; owner = opts;
  el.innerHTML = target.dataset.person !== undefined
    ? personCardHTML(target.dataset, opts.bundle)
    : hoverCardHTML(opts.bundle, target.dataset.thinker, { answers: opts.answers || {}, result: opts.result || null });
  el.classList.remove("is-open");
  el.style.maxHeight = "";
  el.hidden = false;
  place(el, target);
  shownAt = performance.now();
  target.setAttribute("aria-describedby", el.id);
  requestAnimationFrame(() => el.classList.add("is-open"));
}

function hide() {
  clearTimeout(showTimer); clearTimeout(hideTimer);
  if (!card) return;
  card.hidden = true;
  card.classList.remove("is-open");
  anchor?.removeAttribute("aria-describedby");
  anchor = null; owner = null;
}

function scheduleHide() {
  clearTimeout(hideTimer);
  hideTimer = setTimeout(hide, HIDE_DELAY);
}

const wired = new WeakMap(); // container -> its latest options

/**
 * Give every thinker circle in `container` (a map from mapSVG, or an element that holds one and
 * may redraw it) the hover card. `onProfile(id)` opens the full profile in place; without it the
 * link goes to /people#id. Calling it again on the same container just updates the options.
 */
export function attachHoverCard(container, opts) {
  if (!container) return;
  const known = wired.has(container);
  wired.set(container, opts);
  if (known) return;
  const current = () => wired.get(container);
  const circle = (node) => node?.closest?.(".thinker-map [data-thinker], .thinker-map [data-person]");
  let pointer = "mouse";

  container.addEventListener("pointerdown", (e) => { pointer = e.pointerType || "mouse"; }, true);
  container.addEventListener("pointerover", (e) => {
    if (e.pointerType === "touch") return;
    const g = circle(e.target);
    if (!g) return;
    clearTimeout(hideTimer);
    if (g === anchor) return;
    clearTimeout(showTimer);
    showTimer = setTimeout(() => show(g, current()), SHOW_DELAY);
  });
  container.addEventListener("pointerout", (e) => {
    if (e.pointerType === "touch") return;
    const g = circle(e.target);
    if (!g || g.contains(e.relatedTarget)) return;
    clearTimeout(showTimer);
    if (g === anchor && !card?.contains(e.relatedTarget)) scheduleHide();
  });
  // keyboard: focusing a circle shows its card; Enter still opens the full profile
  container.addEventListener("focusin", (e) => {
    const g = circle(e.target);
    if (g && g.matches(":focus-visible")) show(g, current());
  });
  container.addEventListener("focusout", (e) => {
    if (circle(e.target) === anchor && !card?.contains(e.relatedTarget)) hide();
  });
  container.addEventListener("keydown", (e) => {
    if ((e.key === "Enter" || e.key === " ") && circle(e.target)) hide();
  });
  // the live map: dragging a face closes its card; once the graph settles, an open card
  // re-anchors to where its circle came to rest
  container.addEventListener("thinkermap:drag", () => { if (anchor && container.contains(anchor)) hide(); });
  // zooming or panning the map (map-zoom.js) moves the circle: the card follows it
  container.addEventListener("thinkermap:view", () => {
    if (anchor && card && !card.hidden && container.contains(anchor)) place(card, anchor);
  });
  container.addEventListener("thinkermap:settle", () => {
    if (anchor && card && !card.hidden && container.contains(anchor)) place(card, anchor);
  });
  // touch: the first tap on a circle shows its card; a second tap opens the profile as before.
  // Capture phase, so it runs before the map's own click handler.
  container.addEventListener("click", (e) => {
    const g = circle(e.target);
    if (!g) return;
    if (pointer === "touch" && anchor !== g) {
      e.preventDefault();
      e.stopImmediatePropagation();
      show(g, current());
      return;
    }
    hide();
  }, true);
}
