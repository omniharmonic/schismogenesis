// The 2D map: thinkers at their atlas positions, camps (or, when one is in focus, the groups
// inside it) as soft regions, you among the thinkers you agree with most. Every thinker and
// school is a button (see wireMap). The full 3D atlas lives at /atlas.
//
// mapSVG returns markup for the settled layout, so the map reads the same with or without
// script, motion or a frame loop. In a browser it then comes alive in the house graph language
// shared with the lab home page: faces ringed in camp colour, hairline kin links where their
// published words agree, a gentle gravity that settles in about two seconds, drag a face to pull
// it (its kin follow a little) and it springs back, crosshair and readout. prefers-reduced-motion
// keeps the settled layout still. The simulation sleeps when settled or off-screen.

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
  const at = ids.map((id) => pos[id]); // the same point arrays, by index: no string lookups in the loop
  for (let step = 0; step < steps; step++) {
    for (let i = 0; i < ids.length; i++) {
      const a = at[i];
      for (let j = i + 1; j < ids.length; j++) {
        const b = at[j];
        let dx = b[0] - a[0], dy = b[1] - a[1];
        if (dx >= GAP || dx <= -GAP || dy >= GAP || dy <= -GAP) continue; // too far apart to touch
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

// ------------------------------------------------------------------ graph helpers (pure)

/**
 * Which camp a thinker belongs to, as a 1-based index in camp order (c1..c4, the same order as
 * bundle.schools and the lab), or 0 when they are not grouped yet.
 */
export function campOf(bundle, t) {
  const roots = bundle.tree?.roots || [];
  const root = t?.path?.[0];
  if (root && roots.includes(root)) return roots.indexOf(root) + 1;
  const i = bundle.schools.findIndex((s) => s.label === t?.school);
  return i >= 0 ? i + 1 : 0;
}

/** The camp index of a drill-down group id ("c2.1.3" belongs to camp 2), or of a school label. */
export function campOfGroup(bundle, g) {
  const roots = bundle.tree?.roots || [];
  if (g.id) {
    const root = roots.find((r) => g.id === r || g.id.startsWith(`${r}.`));
    return root ? roots.indexOf(root) + 1 : 0;
  }
  const i = bundle.schools.findIndex((s) => s.label === g.school);
  return i >= 0 ? i + 1 : 0;
}

/**
 * Kin links, computed the way the lab computes them (apps/antimemes/build.py): for every pair
 * with at least `minShared` statements both took a side on, the score is the mean product of
 * their sides (-1..1). Each person keeps their `perNode` strongest links scoring at least
 * `minKin`. Deterministic: ties break on the number of shared statements, then on ids.
 */
export function kinLinks(bundle, { perNode = 3, minKin = 0.34, minShared = 4 } = {}) {
  const ids = bundle.thinkers.map((t) => t.id).sort();
  const sides = Object.fromEntries(ids.map((id) => [id, {}]));
  for (const [sid, row] of Object.entries(bundle.stances || {})) {
    for (const [pid, s] of Object.entries(row)) if (sides[pid] && (s.a === 1 || s.a === -1)) sides[pid][sid] = s.a;
  }
  const mine = Object.fromEntries(ids.map((id) => [id, []]));
  for (let i = 0; i < ids.length; i++) {
    const a = ids[i], sa = sides[a];
    for (let j = i + 1; j < ids.length; j++) {
      const b = ids[j], sb = sides[b];
      let n = 0, sum = 0;
      for (const sid in sa) if (sid in sb) { n++; sum += sa[sid] * sb[sid]; }
      if (n < minShared) continue;
      const w = Math.round((sum / n) * 1000) / 1000;
      if (w < minKin) continue;
      const link = { s: a, t: b, w, n };
      mine[a].push(link); mine[b].push(link);
    }
  }
  const out = new Map();
  for (const id of ids) {
    mine[id].sort((x, y) => y.w - x.w || y.n - x.n || (x.s + x.t).localeCompare(y.s + y.t));
    for (const l of mine[id].slice(0, perNode)) out.set(`${l.s}|${l.t}`, l);
  }
  return [...out.values()];
}

/** A small seeded random generator (mulberry32), so the settling jiggle is the same for everyone. */
export function seeded(seed = 1) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export const FORCES = {
  home: 0.028,     // weak pull back to the settled spot
  spring: 0.012,   // kin links: soft springs whose rest length is their settled distance
  collide: 0.6,    // share of an overlap undone per step (the rest next step)
  minGap: R * 2 + 3, // faces keep this far apart, centre to centre
  damping: 0.8,
  r: R,
};

/**
 * One step of the force simulation. `nodes` are {x, y, vx, vy, hx, hy, fixed}, where h is the
 * node's anchor (its measured, relaxed spot); `links` are {a, b, rest} with node indexes;
 * `obstacles` are boxes ({x, y, w, h}) the faces stay clear of; `box` is {w, h}. Mutates the
 * nodes and returns how far they moved this step (sum of |dx| + |dy|).
 */
export function forceStep(nodes, links, { box, obstacles = [], f = FORCES } = {}) {
  for (const n of nodes) {
    n.ox = n.x; n.oy = n.y;
    if (n.fixed) continue;
    // the pull grows with distance up to a cap, so a face shoved far away drifts home gently
    // instead of slamming back into whatever pushed it
    const dx = n.hx - n.x, dy = n.hy - n.y, d = Math.hypot(dx, dy), c = d > 60 ? 60 / d : 1;
    n.vx += dx * c * f.home; n.vy += dy * c * f.home;
  }
  for (const l of links) {
    const a = nodes[l.a], b = nodes[l.b];
    const dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy) || 0.01;
    const k = ((d - l.rest) / d) * f.spring;
    if (!a.fixed) { a.vx += dx * k; a.vy += dy * k; }
    if (!b.fixed) { b.vx -= dx * k; b.vy -= dy * k; }
  }
  const r = f.r;
  for (const n of nodes) {
    if (n.fixed) { n.vx = n.vy = 0; continue; }
    for (const o of obstacles) {
      const left = o.x - r - 2, right = o.x + o.w + r + 2, top = o.y - r - 2, bottom = o.y + o.h + r + 2;
      if (n.x <= left || n.x >= right || n.y <= top || n.y >= bottom) continue;
      const moves = [[left - n.x, 0], [right - n.x, 0], [0, top - n.y], [0, bottom - n.y]];
      const [mx, my] = moves.reduce((best, m) => (Math.abs(m[0] + m[1]) < Math.abs(best[0] + best[1]) ? m : best));
      n.vx += mx * 0.1; n.vy += my * 0.1;
    }
    n.vx *= f.damping; n.vy *= f.damping;
    n.x += n.vx; n.y += n.vy;
  }
  // collisions as a position pass: faces never overlap, and a dragged (fixed) face is immovable,
  // so its neighbours take the whole push. The velocity into the contact is dropped (no bounce).
  const minD = f.minGap;
  for (let pass = 0; pass < 2; pass++) for (let i = 0; i < nodes.length; i++) {
    const a = nodes[i];
    for (let j = i + 1; j < nodes.length; j++) {
      const b = nodes[j];
      let dx = b.x - a.x;
      if (dx > minD || dx < -minD) continue;
      let dy = b.y - a.y;
      if (dy > minD || dy < -minD) continue;
      let d = Math.hypot(dx, dy);
      if (d >= minD) continue;
      if (a.fixed && b.fixed) continue;
      if (d < 0.01) { dx = 1; dy = (i % 2 ? 1 : -1) * 0.5; d = Math.hypot(dx, dy); }
      const ux = dx / d, uy = dy / d, gap = (minD - d) * (a.fixed || b.fixed ? 1 : f.collide);
      const wa = a.fixed ? 0 : b.fixed ? 1 : 0.5, wb = 1 - wa;
      a.x -= ux * gap * wa; a.y -= uy * gap * wa; b.x += ux * gap * wb; b.y += uy * gap * wb;
      const rel = (b.vx - a.vx) * ux + (b.vy - a.vy) * uy;
      if (rel < 0) {
        if (!a.fixed) { a.vx += ux * rel * wa; a.vy += uy * rel * wa; }
        if (!b.fixed) { b.vx -= ux * rel * wb; b.vy -= uy * rel * wb; }
      }
    }
  }
  let moved = 0;
  for (const n of nodes) {
    n.x = Math.min(box.w - r - 2, Math.max(r + 2, n.x));
    n.y = Math.min(box.h - r - 2, Math.max(r + 2, n.y));
    moved += Math.abs(n.x - n.ox) + Math.abs(n.y - n.oy);
  }
  return moved;
}

/**
 * Run the simulation from rest until it stops moving: the settled layout. Deterministic, so
 * everyone sees the same map, and the live map comes back to exactly this after any jiggle.
 */
export function settle(nodes, links, opts = {}, { maxSteps = 400, rest = 0.01 } = {}) {
  let steps = 0;
  while (steps < maxSteps && forceStep(nodes, links, opts) > rest) steps++;
  return steps;
}

/**
 * The entrance: each face starts part of the way in toward its camp's centre (the unplaced
 * toward the middle of the map), with a little seeded jitter, so the map gathers and then
 * blooms out under gravity into its settled layout. Seeded, so it is the same for everyone.
 * Uses each node's settled spot (t, else its anchor h) as where it is going.
 */
export function settlingStart(nodes, groups, { seed = 7, gather = 0.32, jitter = 9, box = null } = {}) {
  const rand = seeded(seed);
  const tx = (n) => n.tx ?? n.hx, ty = (n) => n.ty ?? n.hy;
  const all = nodes.map((_, i) => i);
  const mid = box ? [box.w / 2, box.h / 2]
    : [all.reduce((s, i) => s + tx(nodes[i]), 0) / nodes.length, all.reduce((s, i) => s + ty(nodes[i]), 0) / nodes.length];
  const centre = nodes.map(() => mid);
  for (const g of groups) {
    if (!g.length) continue;
    const c = [g.reduce((s, i) => s + tx(nodes[i]), 0) / g.length, g.reduce((s, i) => s + ty(nodes[i]), 0) / g.length];
    for (const i of g) if (centre[i] === mid) centre[i] = c;
  }
  nodes.forEach((n, i) => {
    const [cx, cy] = centre[i];
    n.x = tx(n) + (cx - tx(n)) * gather + (rand() - 0.5) * jitter * 2;
    n.y = ty(n) + (cy - ty(n)) * gather + (rand() - 0.5) * jitter * 2;
    n.vx = (rand() - 0.5) * 2; n.vy = (rand() - 0.5) * 2;
  });
}

// ------------------------------------------------------------------ the markup

const live = new Map(); // svg id -> what the live layer needs, until the svg is in the page

const kinPath = (links, P) => links.map((l) => `M${P[l.a][0].toFixed(1)},${P[l.a][1].toFixed(1)}L${P[l.b][0].toFixed(1)},${P[l.b][1].toFixed(1)}`).join("");
const tr = (x, y) => `translate(${x.toFixed(1)} ${y.toFixed(1)})`;

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
  const seq = ++clipSeq;
  const clip = `face-clip-${seq}`, svgId = `thinker-map-${seq}`;
  let svg = `<svg class="thinker-map${focus ? " has-focus" : ""}" id="${svgId}" viewBox="0 0 ${width} ${height}" role="group" aria-label="${esc(label)}">`;
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

  // the graph the live layer moves: node i is bundle.thinkers[i]
  const index = Object.fromEntries(ids.map((id, i) => [id, i]));
  const anchors = ids.map((id) => [...pos[id]]);
  const links = kinLinks(bundle).map((l) => ({ a: index[l.s], b: index[l.t], w: l.w })).filter((l) => l.a !== undefined && l.b !== undefined)
    .map((l) => ({ ...l, rest: Math.hypot(anchors[l.b][0] - anchors[l.a][0], anchors[l.b][1] - anchors[l.a][1]) }));
  // settle the relaxed layout under the live forces, so the drawn map is the very state the
  // live graph comes back to (on a phone the relaxed layout can still have faces touching)
  const box = { w: width, h: height };
  const simNodes = anchors.map(([x, y]) => ({ x, y, vx: 0, vy: 0, hx: x, hy: y, fixed: false }));
  settle(simNodes, links, { box, obstacles: fixedBoxes });
  simNodes.forEach((n, i) => { pos[ids[i]] = [n.x, n.y]; });
  const P = ids.map((id) => pos[id]);
  const regionIdx = [];

  svg += `<g class="map-regions">`;
  regions.forEach((g, n) => {
    const members = g.members.map((m) => index[m]).filter((i) => i !== undefined);
    const pts = members.map((i) => P[i]);
    if (!pts.length) return;
    regionIdx.push(members);
    const key = g.id ? `data-node="${esc(g.id)}"` : `data-school="${esc(g.school)}"`;
    const on = (g.id && selected?.node === g.id) || (!g.id && selected?.school === g.school) ? " is-selected" : "";
    svg += `<path class="map-region camp-${campOfGroup(bundle, g)}${on}" ${key} style="--i:${n}" d="${region(pts)}" stroke-width="${R * 2 + (focus ? 16 : 22)}"/>`;
  });
  svg += `</g>`;

  // hairline kin links where their published words agree; the hovered face's links light up
  svg += `<path class="map-kin" aria-hidden="true" d="${kinPath(links, P)}"/><path class="map-kin is-on" aria-hidden="true" d=""/>`;

  if (you) {
    const [x, y] = you;
    for (const t of result.nearest) {
      const [tx, ty] = pos[t.id];
      svg += `<line class="map-tether" data-to="${esc(t.id)}" x1="${x}" y1="${y}" x2="${tx.toFixed(1)}" y2="${ty.toFixed(1)}"/>`;
    }
  }

  for (const t of bundle.thinkers) {
    const [x, y] = pos[t.id];
    const r = scoreOf[t.id];
    const share = r ? Math.round(Math.max(0, r.s - 0.3) * 140) : 0;
    const fill = r ? `color-mix(in srgb, var(--tm-agree) ${Math.min(100, share)}%, var(--tm-node))` : "var(--tm-node)";
    const dark = r && r.s > 0.62;
    const what = !result ? (t.school || "no school yet") : r ? `you agree on ${r.k} of ${r.n}` : "too few shared statements to compare";
    const note = t.provisional ? ", new voice" : "";
    const dash = t.provisional ? "1.5 2.5" : r || !result ? "" : "3 3";
    const on = selected?.thinker === t.id ? " is-selected" : "";
    const faded = inFocus && !inFocus.has(t.id) ? " is-faded" : "";
    svg += `<g class="map-thinker camp-${campOf(bundle, t)}${on}${dark ? " is-dark" : ""}${faded}" data-thinker="${esc(t.id)}" transform="${tr(x, y)}" tabindex="0" role="button" aria-label="${esc(`${t.name}, ${what}${note}`)}">`;
    svg += `<circle class="hit" r="${R + 5}"/><g class="tm-body"><circle class="dot" r="${R}" fill="${fill}"${dash ? ` stroke-dasharray="${dash}"` : ""}/>`;
    // the portrait sits inside the dot, leaving a ring that still carries the agreement shade
    const inset = r ? 3.5 : 1.5;
    svg += t.face
      ? `<image class="face" href="${esc(t.face)}" x="${inset - R}" y="${inset - R}" width="${(R - inset) * 2}" height="${(R - inset) * 2}" clip-path="url(#${clip})" preserveAspectRatio="xMidYMid slice"/>`
      : `<text y="3.6" text-anchor="middle">${esc(t.initials)}</text>`;
    svg += `</g>`;
    if (near.has(t.id)) {
      const name = t.name.replace(/ \(.*\)/, ""), half = labelWidth(name, 6) / 2;
      const nx = Math.min(width - half, Math.max(half, x)) - x;
      svg += `<text class="map-name" x="${nx.toFixed(1)}" y="${R + 14}" text-anchor="middle">${esc(name)}</text>`;
    }
    svg += `</g>`;
  }

  if (you) {
    const [x, y] = you;
    svg += `<g class="map-you-mark" aria-hidden="true"><circle cx="${x}" cy="${y}" r="22" fill="none" stroke-width="1.5" stroke-dasharray="2 4"/><circle class="map-you" cx="${x}" cy="${y}" r="7"/><text class="map-name" x="${x + 28}" y="${y + 4}" font-weight="700">You</text></g>`;
  }

  // group names last, with a halo, so they read over everything
  for (const { s, key, x, y } of labels) {
    svg += `<g class="map-school-label camp-${campOfGroup(bundle, s)}" ${key} tabindex="0" role="button" aria-label="${esc(`Group: ${s.label}`)}"><text x="${x}" y="${y}" text-anchor="middle">${esc(s.label)}</text></g>`;
  }

  // marks tag thinkers with a letter, e.g. each room group on the thinkers it votes most like.
  // Groups aren't placed as points: their closest thinkers often sit far apart on this
  // non-linear layout, so any average lands in empty space.
  const tags = {};
  for (const m of marks) for (const id of m.near) (tags[id] ||= []).push(m);
  for (const [id, list] of Object.entries(tags)) {
    if (!pos[id]) continue;
    const [x, y] = pos[id];
    svg += `<g class="map-tag" data-at="${esc(id)}" transform="${tr(x, y)}" aria-hidden="true">`;
    list.forEach((m, i) => {
      const tx = 16 + i * 17, ty = -15;
      svg += `<g><title>${esc(m.title || m.label)}</title><circle cx="${tx}" cy="${ty}" r="9"/><text x="${tx}" y="${ty + 4}" text-anchor="middle" font-weight="700" font-size="11">${esc(m.label)}</text></g>`;
    });
    svg += `</g>`;
  }

  // ops-console furniture: focus brackets, crosshair and a small readout (live layer only)
  const s = R + 7, l = 6;
  const br = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([sx, sy]) => `M${sx * s},${sy * (s - l)}L${sx * s},${sy * s}L${sx * (s - l)},${sy * s}`).join("");
  svg += `<path class="map-brackets" aria-hidden="true" d="${br}" visibility="hidden"/>`;
  svg += `<g class="map-cross" aria-hidden="true" visibility="hidden"><line class="h" x1="0" x2="${width}" y1="0" y2="0"/><line class="v" y1="0" y2="${height}" x1="0" x2="0"/></g>`;
  svg += `<text class="map-readout" aria-hidden="true" x="${width - 12}" y="${height - 12}" text-anchor="end">${ids.length} thinkers · ${links.length} kin links</text>`;

  live.set(svgId, { P, anchors, links, regionIdx, obstacles: fixedBoxes, box, ids });
  if (typeof document !== "undefined") activateSoon(svgId);
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

// ------------------------------------------------------------------ the live layer (browser only)

let cssAdded = false;
function addStyles() {
  if (cssAdded || document.querySelector('link[href$="map.css"]')) { cssAdded = true; return; }
  cssAdded = true;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = new URL("./map.css", import.meta.url).href;
  document.head.append(link);
}

// mapSVG returns a string the caller puts in the page; pick the svg up once it is there.
function activateSoon(svgId, tries = 0) {
  const run = () => {
    const el = document.getElementById(svgId);
    if (el) { const m = live.get(svgId); live.delete(svgId); activate(el, m); return; }
    if (tries < 30) requestAnimationFrame(() => activateSoon(svgId, tries + 1));
    else live.delete(svgId); // never placed in the page
  };
  if (tries === 0) { addStyles(); queueMicrotask(run); } else run();
}

const STEP_MS = 1000 / 60;
const REST = 0.15;   // energy below which the map counts as settled
const MAX_STEPS = 260; // about 4.3 s: a hard stop so a stubborn jiggle can't keep the loop awake

function activate(svg, m) {
  if (!m || svg.dataset.live) return;
  svg.dataset.live = "1";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)");
  const fine = matchMedia("(pointer: fine)").matches;
  const groups = [...svg.querySelectorAll(".map-thinker")];
  // x, y: where the face is now; h: its anchor (pulled toward); t: the settled spot it lands on
  const nodes = m.P.map(([x, y], i) => ({ x, y, vx: 0, vy: 0, hx: m.anchors[i][0], hy: m.anchors[i][1], tx: x, ty: y, fixed: false, sx: x, sy: y }));
  const links = m.links;
  const byId = Object.fromEntries(m.ids.map((id, i) => [id, i]));
  const regionEls = [...svg.querySelectorAll(".map-region")];
  const kinEl = svg.querySelector(".map-kin:not(.is-on)"), kinOn = svg.querySelector(".map-kin.is-on");
  const tethers = [...svg.querySelectorAll(".map-tether")].map((el) => ({ el, i: byId[el.dataset.to] }));
  const tags = [...svg.querySelectorAll(".map-tag")].map((el) => ({ el, i: byId[el.dataset.at] }));
  const brackets = svg.querySelector(".map-brackets"), cross = svg.querySelector(".map-cross");
  const crossH = cross.querySelector(".h"), crossV = cross.querySelector(".v");
  const readout = svg.querySelector(".map-readout");
  const baseReadout = readout.textContent;
  const adj = nodes.map(() => []);
  links.forEach((l, k) => { adj[l.a].push(k); adj[l.b].push(k); });

  let raf = 0, last = 0, acc = 0, steps = 0, visible = false, active = -1, drag = null;
  let state = "settled";
  svg.classList.add("is-live");

  const render = () => {
    const P = nodes.map((n) => [n.x, n.y]);
    nodes.forEach((n, i) => {
      if (Math.abs(n.x - n.sx) < 0.05 && Math.abs(n.y - n.sy) < 0.05) return;
      n.sx = n.x; n.sy = n.y;
      groups[i].setAttribute("transform", tr(n.x, n.y));
    });
    regionEls.forEach((el, k) => el.setAttribute("d", region(m.regionIdx[k].map((i) => P[i]))));
    kinEl.setAttribute("d", kinPath(links, P));
    renderActive(P);
    for (const t of tethers) if (t.i !== undefined) { t.el.setAttribute("x2", P[t.i][0].toFixed(1)); t.el.setAttribute("y2", P[t.i][1].toFixed(1)); }
    for (const t of tags) if (t.i !== undefined) t.el.setAttribute("transform", tr(P[t.i][0], P[t.i][1]));
  };
  const renderActive = (P = null) => {
    if (active < 0) { kinOn.setAttribute("d", ""); brackets.setAttribute("visibility", "hidden"); return; }
    const pts = P || nodes.map((n) => [n.x, n.y]);
    kinOn.setAttribute("d", kinPath(adj[active].map((k) => links[k]), pts));
    brackets.setAttribute("transform", tr(nodes[active].x, nodes[active].y));
    brackets.setAttribute("visibility", "visible");
  };
  const setState = (s) => {
    if (s === state) return;
    state = s;
    readout.textContent = `${baseReadout} · ${s}`;
    if (s === "settled") svg.dispatchEvent(new CustomEvent("thinkermap:settle", { bubbles: true }));
  };

  const frame = (t) => {
    raf = 0;
    if (!svg.isConnected) { stop(); return; }
    acc += Math.min(64, t - last); last = t;
    let energy = Infinity, n = 0;
    while (acc >= STEP_MS && n < 4) {
      energy = forceStep(nodes, links, { box: m.box, obstacles: m.obstacles });
      acc -= STEP_MS; n++; steps++;
    }
    if (n) render();
    if (drag && n && energy < REST) { setState("held"); return; } // a pointer move wakes it again
    if (!drag &&((n && energy < REST) || steps > MAX_STEPS)) {
      // land exactly on the settled layout the labels were placed for
      for (const nd of nodes) { nd.x = nd.tx; nd.y = nd.ty; nd.vx = nd.vy = 0; }
      render(); steps = 0; setState("settled");
      return;
    }
    if (visible) raf = requestAnimationFrame(frame);
  };
  const wake = () => {
    if (reduce.matches || raf || !visible) return;
    setState(drag ? "pulled" : "settling");
    last = performance.now(); acc = STEP_MS;
    raf = requestAnimationFrame(frame);
  };
  const io = new IntersectionObserver((entries) => {
    visible = entries.some((e) => e.isIntersecting);
    if (!visible) { cancelAnimationFrame(raf); raf = 0; return; }
    if (state !== "settled") wake();
  }, { threshold: 0.05 });
  if (!reduce.matches) {
    // activation runs before the browser paints the new map, so the gathered start never jumps
    settlingStart(nodes, m.regionIdx, { box: m.box });
    render();
    setState("settling");
  }
  io.observe(svg);
  function stop() { cancelAnimationFrame(raf); raf = 0; io.disconnect(); }

  // ---- pointer: hover lights a face's kin links; drag pulls a face (mouse and pen only, so a
  // finger still scrolls the page and the first tap opens the hover card)
  let rect = null;
  const toMap = (e) => {
    rect ||= svg.getBoundingClientRect();
    return [((e.clientX - rect.left) / rect.width) * m.box.w, ((e.clientY - rect.top) / rect.height) * m.box.h];
  };
  const forget = () => { rect = null; };
  addEventListener("scroll", forget, { passive: true });
  addEventListener("resize", forget, { passive: true });
  const indexOf = (target) => {
    const g = target?.closest?.("[data-thinker]");
    return g && svg.contains(g) ? byId[g.dataset.thinker] ?? -1 : -1;
  };
  const setActive = (i) => { if (i !== active) { active = i; renderActive(); } };

  svg.addEventListener("pointerover", (e) => { if (!drag) setActive(indexOf(e.target)); });
  svg.addEventListener("pointerout", (e) => { if (!drag && indexOf(e.relatedTarget) < 0) setActive(-1); });
  svg.addEventListener("focusin", (e) => setActive(indexOf(e.target)));
  svg.addEventListener("focusout", (e) => { if (indexOf(e.relatedTarget) < 0) setActive(-1); });
  svg.addEventListener("pointerenter", forget);
  svg.addEventListener("pointerleave", () => { cross.setAttribute("visibility", "hidden"); readout.textContent = `${baseReadout} · ${state}`; });

  svg.addEventListener("pointerdown", (e) => {
    if (reduce.matches || e.pointerType === "touch" || e.button !== 0) return;
    const i = indexOf(e.target);
    if (i < 0) return;
    const [x, y] = toMap(e);
    drag = { i, id: e.pointerId, ox: nodes[i].x - x, oy: nodes[i].y - y, x0: e.clientX, y0: e.clientY, moving: false };
  });
  svg.addEventListener("pointermove", (e) => {
    const [x, y] = toMap(e);
    if (fine) {
      crossH.setAttribute("y1", y.toFixed(1)); crossH.setAttribute("y2", y.toFixed(1));
      crossV.setAttribute("x1", x.toFixed(1)); crossV.setAttribute("x2", x.toFixed(1));
      cross.setAttribute("visibility", "visible");
      const f = (v) => (v < 0 ? "−" : "+") + Math.abs(v).toFixed(0).padStart(3, "0");
      readout.textContent = `x ${f(x - m.box.w / 2)}  y ${f(m.box.h / 2 - y)} · ${state}`;
    }
    if (!drag || e.pointerId !== drag.id) return;
    if (!drag.moving) {
      if (Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0) < 5) return;
      drag.moving = true;
      nodes[drag.i].fixed = true;
      svg.setPointerCapture?.(e.pointerId);
      svg.classList.add("is-dragging");
      groups[drag.i].classList.add("is-dragged");
      setActive(drag.i);
      svg.dispatchEvent(new CustomEvent("thinkermap:drag", { bubbles: true }));
    }
    const n = nodes[drag.i];
    n.x = Math.min(m.box.w - R - 2, Math.max(R + 2, x + drag.ox));
    n.y = Math.min(m.box.h - R - 2, Math.max(R + 2, y + drag.oy));
    steps = 0;
    wake();
  });
  const release = (e) => {
    if (!drag || e.pointerId !== drag.id) return;
    const d = drag; drag = null;
    if (!d.moving) return;
    nodes[d.i].fixed = false;
    svg.classList.remove("is-dragging");
    groups[d.i].classList.remove("is-dragged");
    // the drag ends in a click on the face: swallow it, so letting go doesn't open the profile
    const swallow = (ev) => { ev.stopPropagation(); ev.preventDefault(); };
    addEventListener("click", swallow, { capture: true, once: true });
    setTimeout(() => removeEventListener("click", swallow, { capture: true }), 0);
    if (indexOf(e.target) !== d.i) setActive(-1);
    steps = 0;
    setState("settling");
    wake();
  };
  svg.addEventListener("pointerup", release);
  svg.addEventListener("pointercancel", release);

  reduce.addEventListener?.("change", () => {
    if (!reduce.matches) return;
    cancelAnimationFrame(raf); raf = 0;
    for (const nd of nodes) { nd.x = nd.tx; nd.y = nd.ty; nd.vx = nd.vy = 0; nd.fixed = false; }
    drag = null; render(); setState("settled");
  });
}
