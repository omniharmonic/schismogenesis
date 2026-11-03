// The light 2D map: thinkers at their atlas positions, schools as soft regions, you among the
// thinkers you agree with most. Every thinker and school is a button (see wireMap). The full 3D
// atlas lives at /atlas.

export const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

const R = 15; // thinker circle radius in map units

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

// Nudge circles apart so none hide another, keeping each close to its measured spot. Fixed
// iteration count and order, so everyone sees the same map.
function relax(pos, ids, box) {
  const gap = R * 2 + 4;
  const home = Object.fromEntries(ids.map((id) => [id, [...pos[id]]]));
  for (let step = 0; step < 160; step++) {
    for (let i = 0; i < ids.length; i++) {
      for (let j = i + 1; j < ids.length; j++) {
        const a = pos[ids[i]], b = pos[ids[j]];
        let dx = b[0] - a[0], dy = b[1] - a[1];
        let d = Math.hypot(dx, dy);
        if (d >= gap) continue;
        if (d < 0.01) { dx = 1; dy = (i % 2 ? 1 : -1) * 0.5; d = Math.hypot(dx, dy); }
        const push = (gap - d) / 2 / d;
        a[0] -= dx * push; a[1] -= dy * push; b[0] += dx * push; b[1] += dy * push;
      }
    }
    for (const id of ids) {
      const p = pos[id], h = home[id];
      p[0] += (h[0] - p[0]) * 0.02; p[1] += (h[1] - p[1]) * 0.02;
      p[0] = Math.min(box.w - R - 2, Math.max(R + 2, p[0]));
      p[1] = Math.min(box.h - R - 2, Math.max(R + 2, p[1]));
    }
  }
}

// A rounded region around points: the hull drawn with a thick round stroke, so one member is a
// disc, two a capsule, more a padded polygon.
function region(points) {
  const h = hull(points);
  return `M${h.map((p) => p.map((v) => v.toFixed(1)).join(",")).join("L")}${h.length > 2 ? "Z" : ""}`;
}

/** Members of a school for display: its core members plus voices placed into it. */
export function schoolMembers(bundle, label) {
  // "" is the not-yet-grouped set: voices whose outlook no school shares on enough positions
  return bundle.thinkers.filter((t) => (t.school || "") === label).map((t) => t.id);
}

export function mapSVG(bundle, { result = null, marks = [], width = 720, height = 520, selected = null } = {}) {
  const xs = bundle.thinkers.map((t) => t.x), ys = bundle.thinkers.map((t) => t.y);
  const pad = 52;
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const k = Math.min((width - pad * 2) / (maxX - minX), (height - pad * 2) / (maxY - minY));
  const X = (x) => pad + (x - minX) * k + ((width - pad * 2) - (maxX - minX) * k) / 2;
  const Y = (y) => pad + (y - minY) * k + ((height - pad * 2) - (maxY - minY) * k) / 2;
  const ids = bundle.thinkers.map((t) => t.id);
  const pos = Object.fromEntries(bundle.thinkers.map((t) => [t.id, [X(t.x), Y(t.y)]]));
  relax(pos, ids, { w: width, h: height });
  const scoreOf = Object.fromEntries((result?.ranked || []).map((r) => [r.id, r]));
  const near = new Set((result?.nearest || []).map((r) => r.id));
  const label = `Map of ${bundle.thinkers.length} thinkers grouped into schools${result ? ", with your approximate position" : ""}. Select a thinker or a school to see their positions.`;
  let svg = `<svg class="thinker-map" viewBox="0 0 ${width} ${height}" role="group" aria-label="${esc(label)}">`;

  const labels = [];
  bundle.schools.forEach((s, n) => {
    const pts = s.members.map((m) => pos[m]).filter(Boolean);
    if (!pts.length) return;
    const on = selected?.school === s.label ? " is-selected" : "";
    svg += `<path class="map-region${on}" data-school="${esc(s.label)}" style="--i:${n}" d="${region(pts)}" stroke-width="${R * 2 + 26}"/>`;
    const cx = pts.reduce((t, p) => t + p[0], 0) / pts.length;
    const top = Math.min(...pts.map((p) => p[1]));
    labels.push({ s, x: cx, y: top - R - 18 });
  });

  if (result?.position) {
    const x = X(result.position.x), y = Y(result.position.y);
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
    svg += `<g class="map-thinker${on}${dark ? " is-dark" : ""}" data-thinker="${esc(t.id)}" tabindex="0" role="button" aria-label="${esc(`${t.name}, ${what}${note}`)}">`;
    svg += `<circle class="hit" cx="${x}" cy="${y}" r="${R + 5}"/><circle class="dot" cx="${x}" cy="${y}" r="${R}" fill="${fill}" stroke-dasharray="${dash}"/>`;
    svg += `<text x="${x}" y="${y + 3.6}" text-anchor="middle">${esc(t.initials)}</text>`;
    if (near.has(t.id)) svg += `<text class="map-name" x="${x}" y="${y + R + 15}" text-anchor="middle">${esc(t.name.replace(/ \(.*\)/, ""))}</text>`;
    svg += `</g>`;
  }

  if (result?.position) {
    const x = X(result.position.x), y = Y(result.position.y);
    svg += `<g class="map-you-mark" aria-hidden="true"><circle cx="${x}" cy="${y}" r="22" fill="none" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="2 4"/><circle class="map-you" cx="${x}" cy="${y}" r="7"/><text class="map-name" x="${x + 28}" y="${y + 4}" font-weight="700">You</text></g>`;
  }

  // school names last, with a halo, so they read over the circles
  for (const { s, x, y } of labels) {
    const w = s.label.length * 6.6 + 12;
    const lx = Math.min(width - w / 2 - 4, Math.max(w / 2 + 4, x));
    const ly = Math.max(14, y);
    svg += `<g class="map-school-label" data-school="${esc(s.label)}" tabindex="0" role="button" aria-label="${esc(`School: ${s.label}`)}"><text x="${lx}" y="${ly}" text-anchor="middle">${esc(s.label)}</text></g>`;
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
export function wireMap(container, { onThinker, onSchool }) {
  const pick = (target) => {
    const t = target.closest("[data-thinker]");
    if (t) { onThinker?.(t.dataset.thinker); return true; }
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
export function markSelected(container, { thinker = null, school = null } = {}) {
  container.querySelectorAll(".is-selected").forEach((n) => n.classList.remove("is-selected"));
  if (thinker) container.querySelector(`[data-thinker="${CSS.escape(thinker)}"]`)?.classList.add("is-selected");
  if (school) container.querySelectorAll(`[data-school="${CSS.escape(school)}"]`).forEach((n) => n.classList.add("is-selected"));
}
