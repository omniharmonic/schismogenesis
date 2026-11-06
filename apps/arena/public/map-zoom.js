// Zoom for a map drawn by mapSVG: Ctrl or ⌘ + scroll (a trackpad pinch sends the same), a
// two-finger pinch, the +, − and Reset buttons under the map, and drag to pan once zoomed. It only
// changes the svg's viewBox, so the live layer, the people and the hover card keep working. Faces
// and names stop growing past FACE_MAX so a deep zoom spreads the crowd out instead of blowing it up.
// Selecting a camp (the explorer's "thinkermap:focus") opens that camp's area.

export const ZOOM_MIN = 1;
export const ZOOM_MAX = 6;
export const FACE_MAX = 1.6;
const STEP = 1.6; // one press of + or −

const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

// ---------- pure (tests/zoom.test.mjs) ----------

/** How far in a view is: 1 is the whole map. */
export const scaleOf = (view, base) => base.w / view.w;

/** What faces are scaled by at zoom k so they appear at most FACE_MAX times their size. */
export const faceScale = (k, max = FACE_MAX) => (k > max ? max / k : 1);

/**
 * A view ({x, y, w, h}) kept to the map's shape, between ZOOM_MIN and ZOOM_MAX, and inside the
 * map. `base` is the whole map's viewBox.
 */
export function clampView(view, base, { min = ZOOM_MIN, max = ZOOM_MAX } = {}) {
  const k = clamp(base.w / view.w, min, max);
  const w = base.w / k, h = base.h / k;
  const cx = view.x + view.w / 2, cy = view.y + view.h / 2;
  return {
    x: clamp(cx - w / 2, base.x, base.x + base.w - w),
    y: clamp(cy - h / 2, base.y, base.y + base.h - h),
    w, h,
  };
}

/** Zoom by `factor` keeping the map point (px, py) where it is on screen. */
export function zoomAt(view, base, factor, px, py, opts = {}) {
  const k = clamp(scaleOf(view, base) * factor, opts.min ?? ZOOM_MIN, opts.max ?? ZOOM_MAX);
  const w = base.w / k, h = base.h / k;
  const x = px - (px - view.x) * (w / view.w), y = py - (py - view.y) * (h / view.h);
  // clampView recentres on the middle, so give it the box whose middle is the one we want
  return clampView({ x, y, w, h }, base, opts);
}

/** The view that frames a box (map units) with some room around it, up to `max` times in. */
export function fitBox(box, base, { pad = 14, max = 3 } = {}) {
  const k = clamp(Math.min(base.w / (box.w + pad * 2), base.h / (box.h + pad * 2)), ZOOM_MIN, max);
  const w = base.w / k, h = base.h / k;
  return clampView({ x: box.x + box.w / 2 - w / 2, y: box.y + box.h / 2 - h / 2, w, h }, base);
}

/** The smallest box around several boxes; null for none. */
export function unionBoxes(boxes) {
  const list = boxes.filter((b) => b && [b.x, b.y, b.w, b.h].every(Number.isFinite));
  if (!list.length) return null;
  const x = Math.min(...list.map((b) => b.x)), y = Math.min(...list.map((b) => b.y));
  return { x, y, w: Math.max(...list.map((b) => b.x + b.w)) - x, h: Math.max(...list.map((b) => b.y + b.h)) - y };
}

/** "x,y,w,h" (mapSVG's data-box) to a box. */
export const parseBox = (s) => {
  const [x, y, w, h] = String(s || "").split(",").map(Number);
  return [x, y, w, h].every(Number.isFinite) ? { x, y, w, h } : null;
};

// ---------- the controls (browser only) ----------

const HANDLES = "[data-thinker], [data-person], [data-node], [data-school]";

/**
 * Give the map inside `mapEl` zoom. The map may be redrawn any number of times (the explorer does
 * on every drill-down); each new svg starts at the whole map unless a camp is being opened.
 */
export function mountZoom(mapEl) {
  if (!mapEl || mapEl.dataset.zoom) return;
  mapEl.dataset.zoom = "1";
  const bar = document.createElement("div");
  bar.className = "map-zoom";
  bar.innerHTML = `<div class="map-zoom-buttons" role="group" aria-label="Zoom the map">
      <button type="button" data-zoom="out" aria-label="Zoom out">−</button>
      <button type="button" data-zoom="in" aria-label="Zoom in">+</button>
      <button type="button" data-zoom="reset" disabled>Reset</button></div>
    <p class="small muted map-zoom-hint">${matchMedia("(pointer: coarse)").matches ? "Pinch to zoom. Drag to move around once zoomed." : "Ctrl or ⌘ and scroll to zoom. Drag empty space to move around once zoomed."}</p>`;
  let svg = null, base = null, view = null;

  const apply = (next, { announce = true } = {}) => {
    if (!svg) return;
    view = next;
    const k = scaleOf(view, base);
    svg.setAttribute("viewBox", `${view.x.toFixed(2)} ${view.y.toFixed(2)} ${view.w.toFixed(2)} ${view.h.toFixed(2)}`);
    svg.style.setProperty("--fk", faceScale(k).toFixed(4));
    svg.style.setProperty("--dk", (1 / Math.sqrt(k)).toFixed(4));
    svg.classList.toggle("is-zoomed", k > 1.001);
    bar.querySelector('[data-zoom="reset"]').disabled = k <= 1.001;
    bar.querySelector('[data-zoom="in"]').disabled = k >= ZOOM_MAX - 0.001;
    bar.querySelector('[data-zoom="out"]').disabled = k <= 1.001;
    if (announce) svg.dispatchEvent(new CustomEvent("thinkermap:view", { bubbles: true, detail: { k } }));
  };
  const centre = () => [view.x + view.w / 2, view.y + view.h / 2];

  const bind = (el) => {
    if (el === svg) return;
    svg = el;
    const vb = svg.viewBox.baseVal;
    base = { x: vb.x, y: vb.y, w: vb.width, h: vb.height };
    view = { ...base };
    svg.classList.add("is-zoomable");
    apply(view, { announce: false });
    wire(svg);
  };
  const ensureBar = () => { if (bar.parentNode !== mapEl || bar.previousElementSibling !== svg) svg?.after(bar); };
  const look = () => {
    const el = mapEl.querySelector("svg.thinker-map");
    if (el) { bind(el); ensureBar(); }
  };
  new MutationObserver(look).observe(mapEl, { childList: true });
  look();

  bar.addEventListener("click", (e) => {
    const b = e.target.closest("[data-zoom]");
    if (!b || !svg) return;
    if (b.dataset.zoom === "reset") apply({ ...base });
    else apply(zoomAt(view, base, b.dataset.zoom === "in" ? STEP : 1 / STEP, ...centre()));
  });

  // the explorer opened a camp (or closed it): frame the groups now drawn, or the whole map
  mapEl.addEventListener("thinkermap:focus", (e) => {
    look();
    if (!svg) return;
    const box = e.detail?.node ? unionBoxes([...svg.querySelectorAll(".map-region[data-box]")].map((r) => parseBox(r.dataset.box))) : null;
    apply(box ? fitBox(box, base) : { ...base });
  });
  // "Find me" on a zoomed map: bring the mark into the view
  mapEl.addEventListener("thinkermap:reveal", (e) => {
    if (!svg || scaleOf(view, base) <= 1.001) return;
    const m = e.target.transform?.baseVal?.consolidate?.()?.matrix;
    if (m) apply(clampView({ ...view, x: m.e - view.w / 2, y: m.f - view.h / 2 }, base));
  });

  function wire(el) {
    const toMap = (cx, cy) => {
      const r = el.getBoundingClientRect();
      return [view.x + ((cx - r.left) / r.width) * view.w, view.y + ((cy - r.top) / r.height) * view.h];
    };
    el.addEventListener("wheel", (e) => {
      if (!(e.ctrlKey || e.metaKey) || el !== svg) return;
      e.preventDefault();
      apply(zoomAt(view, base, Math.exp(-clamp(e.deltaY, -60, 60) * 0.012), ...toMap(e.clientX, e.clientY)));
    }, { passive: false });

    const pointers = new Map();
    let pan = null, pinch = null, moved = false;
    el.addEventListener("pointerdown", (e) => {
      if (el !== svg) return;
      pointers.set(e.pointerId, [e.clientX, e.clientY]);
      if (pointers.size === 2) {
        const [a, b] = [...pointers.values()];
        pinch = { d: Math.hypot(a[0] - b[0], a[1] - b[1]) || 1 };
        pan = null;
        return;
      }
      if (scaleOf(view, base) <= 1.001 || e.button !== 0) return;
      // a mouse on a face drags the face (map.js); a finger pans from anywhere
      if (e.pointerType !== "touch" && e.target.closest(HANDLES)) return;
      pan = { id: e.pointerId, x: e.clientX, y: e.clientY };
      moved = false;
    });
    el.addEventListener("pointermove", (e) => {
      if (!pointers.has(e.pointerId)) return;
      pointers.set(e.pointerId, [e.clientX, e.clientY]);
      if (pinch && pointers.size === 2) {
        const [a, b] = [...pointers.values()];
        const d = Math.hypot(a[0] - b[0], a[1] - b[1]) || 1;
        apply(zoomAt(view, base, d / pinch.d, ...toMap((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)));
        pinch.d = d; moved = true;
        return;
      }
      if (!pan || e.pointerId !== pan.id) return;
      const dx = e.clientX - pan.x, dy = e.clientY - pan.y;
      if (!moved && Math.hypot(dx, dy) < 5) return;
      if (!moved) { moved = true; el.setPointerCapture?.(e.pointerId); el.classList.add("is-panning"); }
      const r = el.getBoundingClientRect();
      pan.x = e.clientX; pan.y = e.clientY;
      apply(clampView({ ...view, x: view.x - (dx / r.width) * view.w, y: view.y - (dy / r.height) * view.h }, base));
    });
    const end = (e) => {
      pointers.delete(e.pointerId);
      if (pointers.size < 2) pinch = null;
      if (pan && e.pointerId === pan.id) {
        pan = null;
        el.classList.remove("is-panning");
        if (moved) {
          // a pan ends in a click: swallow it, so letting go doesn't open whatever is under it
          const swallow = (ev) => { ev.stopPropagation(); ev.preventDefault(); };
          addEventListener("click", swallow, { capture: true, once: true });
          setTimeout(() => removeEventListener("click", swallow, { capture: true }), 0);
        }
      }
    };
    el.addEventListener("pointerup", end);
    el.addEventListener("pointercancel", end);
  }
}
