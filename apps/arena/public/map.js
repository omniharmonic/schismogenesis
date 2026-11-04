// The light 2D map: thinkers at their atlas positions, camps (or, when one is in focus, the groups
// inside it) as soft regions, you among the
// thinkers you agree with most. Every thinker and school is a button (see wireMap). The full 3D
// atlas lives at /atlas.

export const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

const R = 15; // thinker circle radius in map units

/** A person's round badge: their portrait when there is a freely licensed one, else initials. */
export function badge(t, cls = "") {
  const inner = t?.face ? `<img src="${esc(t.face)}" alt="" loading="lazy" decoding="async">` : esc(t?.initials || "");
  return `<span class="badge${cls ? ` ${cls}` : ""}${t?.face ? " has-face" : ""}" aria-hidden="true">${inner}</span>`;
}

let clipSeq = 0;

function hull(points) {
  if (points.length < 3) return points;
  const p = [...points].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lower = [];
  for (const q of p) { while (lower.length >= 2 && cross(lower.at(-2), lower.at(-1), q) <= 0) lower.pop(); lower.push(q); }
  const upper = [];
  for (const q of p.reverse()) { while (upper.length >= 2 && cross(upper.at(-2), upper.at(-1), q) <= 0) upper.pop(); upper.push(q); }
  return lower.slice(0, -1).concat(upper.slice(0, -1));
}

// Nudge circles apart so none hide another, keeping each close to its measured spot, and keep
// them clear of text boxes (group names, the names under the nearest thinkers, the "You" mark).
// Fixed iteration count and order, so everyone sees the same map.
const GAP = R * 2 + 7;
function relax(pos, ids, box, { steps = 220, boxes = () => [] } = {}) {
  const home = Object.fromEntries(ids.map((id) => [id, [...pos[id]]]));
  for (let step = 0; step < steps; step++) {
    for (let i = 0; i < ids.length; i++) {
      for (let j = i + 1; j < ids.length; j++) {
        const a = pos[ids[i]], b = pos[ids[j]];
        let dx = b[0] - a[0], dy = b[1] - a[1];
        let d = Math.hypot(dx, dy);
        if (d >= GAP) continue;
        if (d < 0.01) { dx = 1; dy = (i % 2 ? 1 : -1) * 0.5; d = Math.hypot(dx, dy); }
        const push = (GAP - d) / 2 / d;
        a[0] -= dx * push; a[1] -= dy * push; b[0] += dx * push; b[1] += dy * push;
      }
    }
    const obstacles = boxes();
    for (const id of ids) {
      const p = pos[id], h = home[id];
      p[0] += (h[0] - p[0]) * 0.012; p[1] += (h[1] - p[1]) * 0.012;
      for (const o of obstacles) {
        if (o.owner === id) continue;
        // distance from the circle centre to the box, grown by the radius and a margin
        const left = o.x - R - 4, right = o.x + o.w + R + 4, top = o.y - R - 4, bottom = o.y + o.h + R + 4;
        if (p[0] <= left || p[0] >= right || p[1] <= top || p[1] >= bottom) continue;
        const moves = [[left - p[0], 0], [right - p[0], 0], [0, top - p[1]], [0, bottom - p[1]]];
        const [mx, my] = moves.reduce((best, m) => (Math.abs(m[0] + m[1]) < Math.abs(best[0] + best[1]) ? m : best));
        p[0] += mx * 0.5; p[1] += my * 0.5;
      }
      p[0] = Math.min(box.w - R - 2, Math.max(R + 2, p[0]));
      p[1] = Math.min(box.h - R - 2, Math.max(R + 2, p[1]));
    }
  }
}

const labelWidth = (text, size = 6.6) => text.length * size + 12;

// A rounded region around points: the hull drawn with a thick round stroke, so one member is a
// disc, two a capsule, more a padded polygon.
function region(points) {
  const h = hull(points);
  return `M${h.map((p) => p.map((v) => v.toFixed(1)).join(",")).join("L")}${h.length > 2 ? "Z" : ""}`;
}

/** Everyone in a group of the drill-down tree: those who drew it plus those placed into it. */
export function nodeMembers(bundle, id) {
  const n = bundle.tree?.nodes?.[id];
  return n ? [...n.members, ...n.attached] : [];
}

/** The groups a map shows: the camps, or, when a group is in focus, the groups inside it. */
export function regionsFor(bundle, focus = null) {
  const tree = bundle.tree;
  if (!tree?.roots?.length) return bundle.schools.map((s) => ({ id: null, label: s.label, members: s.members, school: s.label }));
  const node = focus && tree.nodes[focus];
  const ids = node ? (node.children.length ? node.children : [node.id]) : tree.roots;
  return ids.map((id) => ({ id, label: tree.nodes[id].label, members: nodeMembers(bundle, id) }));
}

/** Members of a school for display: its core members plus voices placed into it. */
export function schoolMembers(bundle, label) {
  // "" is the not-yet-grouped set: voices whose outlook no school shares on enough positions
  return bundle.thinkers.filter((t) => (t.school || "") === label).map((t) => t.id);
}

export function mapSVG(bundle, { result = null, marks = [], width = 720, height = 520, selected = null, focus = null } = {}) {
  const PX = (p) => p.x, PY = (p) => p.y;
  const xs = bundle.thinkers.map(PX), ys = bundle.thinkers.map(PY);
  const pad = 52;
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  // fit the layout; on a tall screen let it stretch up to 1.6 times taller than wide, so the
  // dots get the room a phone has (distances along each axis keep their order)
  const kx = Math.min((width - pad * 2) / (maxX - minX), (height - pad * 2) / (maxY - minY));
  const ky = Math.min((height - pad * 2) / (maxY - minY), kx * 1.6);
  const X = (x) => pad + (x - minX) * kx + ((width - pad * 2) - (maxX - minX) * kx) / 2;
  const Y = (y) => pad + (y - minY) * ky + ((height - pad * 2) - (maxY - minY) * ky) / 2;
  const ids = bundle.thinkers.map((t) => t.id);
  const pos = Object.fromEntries(bundle.thinkers.map((t) => [t.id, [X(PX(t)), Y(PY(t))]]));
  relax(pos, ids, { w: width, h: height });
  const scoreOf = Object.fromEntries((result?.ranked || []).map((r) => [r.id, r]));
  const near = new Set((result?.nearest || []).map((r) => r.id));
  const label = `Map of ${bundle.thinkers.length} thinkers grouped into schools${result ? ", with your approximate position" : ""}. Select a thinker or a school to see their positions.`;
  const clip = `face-clip-${++clipSeq}`;
  let svg = `<svg class="thinker-map" viewBox="0 0 ${width} ${height}" role="group" aria-label="${esc(label)}">`;
  svg += `<defs><clipPath id="${clip}" clipPathUnits="objectBoundingBox"><circle cx="0.5" cy="0.5" r="0.5"/></clipPath></defs>`;

  // group names sit above their group; then everyone steps out from under the text
  const regions = regionsFor(bundle, focus);
  const inFocus = focus && bundle.tree?.nodes?.[focus] ? new Set(nodeMembers(bundle, focus)) : null;
  const labels = [];
  regions.forEach((g) => {
    const pts = g.members.map((m) => pos[m]).filter(Boolean);
    if (!pts.length) return;
    const cx = pts.reduce((t, p) => t + p[0], 0) / pts.length;
    const top = Math.min(...pts.map((p) => p[1]));
    const w = labelWidth(g.label);
    const x = Math.min(width - w / 2 - 4, Math.max(w / 2 + 4, cx));
    const y = Math.max(14, top - R - 16);
    labels.push({ s: g, key: g.id ? `data-node="${esc(g.id)}"` : `data-school="${esc(g.school)}"`, x, y, w });
  });
  const you = result?.position ? [X(PX(result.position)), Y(PY(result.position))] : null;
  const fixedBoxes = [
    ...labels.map((l) => ({ x: l.x - l.w / 2, y: l.y - 13, w: l.w, h: 18 })),
    ...(you ? [{ x: you[0] - 22, y: you[1] - 22, w: 80, h: 44 }] : []),
  ];
  const nameBoxes = () => [...near].filter((id) => pos[id]).map((id) => {
    const w = labelWidth(bundle.thinkers.find((t) => t.id === id).name, 6);
    return { owner: id, x: pos[id][0] - w / 2, y: pos[id][1] + R + 3, w, h: 16 };
  });
  relax(pos, ids, { w: width, h: height }, { steps: 140, boxes: () => [...fixedBoxes, ...nameBoxes()] });

  regions.forEach((g, n) => {
    const pts = g.members.map((m) => pos[m]).filter(Boolean);
    if (!pts.length) return;
    const key = g.id ? `data-node="${esc(g.id)}"` : `data-school="${esc(g.school)}"`;
    const on = (g.id && selected?.node === g.id) || (!g.id && selected?.school === g.school) ? " is-selected" : "";
    svg += `<path class="map-region${on}" ${key} style="--i:${n}" d="${region(pts)}" stroke-width="${R * 2 + (focus ? 16 : 22)}"/>`;
  });

  if (result?.position) {
    const [x, y] = you;
    for (const t of result.nearest) {
      const [tx, ty] = pos[t.id];
      svg += `<line class="map-tether" x1="${x}" y1="${y}" x2="${tx}" y2="${ty}"/>`;
    }
  }

  for (const t of bundle.thinkers) {
    const [x, y] = pos[t.id];
    const r = scoreOf[t.id];
    const fill = r ? `color-mix(in srgb, var(--ridge) ${Math.round(Math.max(0, r.s - 0.3) * 140)}%, var(--sheet))` : "var(--sheet)";
    const dark = r && r.s > 0.62;
    const what = !result ? (t.school || "no school yet") : r ? `you agree on ${r.k} of ${r.n}` : "too few shared statements to compare";
    const note = t.provisional ? ", new voice" : "";
    const dash = t.provisional ? "1.5 2.5" : r || !result ? "" : "3 3";
    const on = selected?.thinker === t.id ? " is-selected" : "";
    const faded = inFocus && !inFocus.has(t.id) ? " is-faded" : "";
    svg += `<g class="map-thinker${on}${dark ? " is-dark" : ""}${faded}" data-thinker="${esc(t.id)}" tabindex="0" role="button" aria-label="${esc(`${t.name}, ${what}${note}`)}">`;
    svg += `<circle class="hit" cx="${x}" cy="${y}" r="${R + 5}"/><circle class="dot" cx="${x}" cy="${y}" r="${R}" fill="${fill}" stroke-dasharray="${dash}"/>`;
    // the portrait sits inside the dot, leaving a ring that still carries the agreement shade
    const inset = r ? 3.5 : 1.5;
    svg += t.face
      ? `<image class="face" href="${esc(t.face)}" x="${x - R + inset}" y="${y - R + inset}" width="${(R - inset) * 2}" height="${(R - inset) * 2}" clip-path="url(#${clip})" preserveAspectRatio="xMidYMid slice"/>`
      : `<text x="${x}" y="${y + 3.6}" text-anchor="middle">${esc(t.initials)}</text>`;
    if (near.has(t.id)) {
      const name = t.name.replace(/ \(.*\)/, ""), half = labelWidth(name, 6) / 2;
      svg += `<text class="map-name" x="${Math.min(width - half, Math.max(half, x))}" y="${y + R + 14}" text-anchor="middle">${esc(name)}</text>`;
    }
    svg += `</g>`;
  }

  if (result?.position) {
    const [x, y] = you;
    svg += `<g class="map-you-mark" aria-hidden="true"><circle cx="${x}" cy="${y}" r="22" fill="none" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="2 4"/><circle class="map-you" cx="${x}" cy="${y}" r="7"/><text class="map-name" x="${x + 28}" y="${y + 4}" font-weight="700">You</text></g>`;
  }

  // group names last, with a halo, so they read over everything
  for (const { s, key, x, y } of labels) {
    svg += `<g class="map-school-label" ${key} tabindex="0" role="button" aria-label="${esc(`Group: ${s.label}`)}"><text x="${x}" y="${y}" text-anchor="middle">${esc(s.label)}</text></g>`;
  }

  // marks tag thinkers with a letter, e.g. each room group on the thinkers it votes most like.
  // Groups aren't placed as points: their closest thinkers often sit far apart on this
  // non-linear layout, so any average lands in empty space.
  const tags = {};
  for (const m of marks) for (const id of m.near) (tags[id] ||= []).push(m);
  for (const [id, list] of Object.entries(tags)) {
    const [x, y] = pos[id];
    list.forEach((m, i) => {
      const tx = x + 16 + i * 17, ty = y - 15;
      svg += `<g aria-hidden="true"><title>${esc(m.title || m.label)}</title><circle cx="${tx}" cy="${ty}" r="9" fill="var(--ink)"/><text x="${tx}" y="${ty + 4}" text-anchor="middle" fill="var(--paper)" font-weight="700" font-size="11">${esc(m.label)}</text></g>`;
    });
  }
  return svg + "</svg>";
}

/** Make a rendered map clickable: one listener for every thinker and school, mouse or keyboard. */
export function wireMap(container, { onThinker, onSchool, onNode }) {
  const pick = (target) => {
    const t = target.closest("[data-thinker]");
    if (t) { onThinker?.(t.dataset.thinker); return true; }
    const g = target.closest("[data-node]");
    if (g) { onNode?.(g.dataset.node); return true; }
    const s = target.closest("[data-school]");
    if (s) { onSchool?.(s.dataset.school); return true; }
    return false;
  };
  container.addEventListener("click", (e) => pick(e.target));
  container.addEventListener("keydown", (e) => {
    if ((e.key === "Enter" || e.key === " ") && pick(e.target)) e.preventDefault();
  });
}

/** Mark the selection on an already drawn map without redrawing it. */
export function markSelected(container, { thinker = null, school = null, node = null } = {}) {
  container.querySelectorAll(".is-selected").forEach((n) => n.classList.remove("is-selected"));
  if (node) container.querySelectorAll(`[data-node="${CSS.escape(node)}"]`).forEach((n) => n.classList.add("is-selected"));
  if (thinker) container.querySelector(`[data-thinker="${CSS.escape(thinker)}"]`)?.classList.add("is-selected");
  if (school) container.querySelectorAll(`[data-school="${CSS.escape(school)}"]`).forEach((n) => n.classList.add("is-selected"));
}
