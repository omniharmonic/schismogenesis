// The light 2D map: thinkers at their atlas positions, schools as soft hulls, you among the
// thinkers you agree with most. The full 3D atlas lives at /atlas.

export const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

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

// A rounded blob around a set of points: offset each hull vertex outward from the centroid.
function blob(points, pad) {
  const h = hull(points);
  const cx = h.reduce((t, q) => t + q[0], 0) / h.length;
  const cy = h.reduce((t, q) => t + q[1], 0) / h.length;
  if (h.length === 1) return `M${cx - pad},${cy}a${pad},${pad} 0 1,0 ${pad * 2},0a${pad},${pad} 0 1,0 ${-pad * 2},0`;
  const out = h.map(([x, y]) => {
    const dx = x - cx, dy = y - cy, len = Math.hypot(dx, dy) || 1;
    return [x + (dx / len) * pad, y + (dy / len) * pad];
  });
  const mid = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
  const far = h.map(([x, y]) => {
    const dx = x - cx, dy = y - cy, len = Math.hypot(dx, dy) || 1;
    return [x + (dx / len) * pad * 2, y + (dy / len) * pad * 2];
  });
  let d = `M${mid(out.at(-1), out[0]).join(",")}`;
  out.forEach((q, i) => { d += `Q${far[i].join(",")} ${mid(q, out[(i + 1) % out.length]).join(",")}`; });
  return d + "Z";
}

export function mapSVG(bundle, { result = null, marks = [], width = 720, height = 520 } = {}) {
  const xs = bundle.thinkers.map((t) => t.x), ys = bundle.thinkers.map((t) => t.y);
  const pad = 46;
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const k = Math.min((width - pad * 2) / (maxX - minX), (height - pad * 2) / (maxY - minY));
  const X = (x) => pad + (x - minX) * k + ((width - pad * 2) - (maxX - minX) * k) / 2;
  const Y = (y) => pad + (y - minY) * k + ((height - pad * 2) - (maxY - minY) * k) / 2;
  const pos = Object.fromEntries(bundle.thinkers.map((t) => [t.id, [X(t.x), Y(t.y)]]));
  const scoreOf = Object.fromEntries((result?.ranked || []).map((r) => [r.id, r]));
  const near = new Set((result?.nearest || []).map((r) => r.id));
  let svg = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Map of 27 thinkers grouped into schools${result ? ", with your approximate position" : ""}">`;
  for (const s of bundle.schools) {
    const pts = s.members.map((m) => pos[m]).filter(Boolean);
    const [lx, ly] = [Math.min(...pts.map((p) => p[0])), Math.min(...pts.map((p) => p[1]))];
    svg += `<path class="map-school" d="${blob(pts, 34)}"/><text class="map-school-label" x="${lx - 8}" y="${ly - 30}">${esc(s.label)}</text>`;
  }
  for (const t of bundle.thinkers) {
    const [x, y] = pos[t.id];
    const r = scoreOf[t.id];
    const fill = r ? `color-mix(in srgb, var(--ridge) ${Math.round(Math.max(0, r.s - 0.3) * 140)}%, var(--sheet))` : "var(--sheet)";
    const title = !result ? `${t.name}, ${t.school || "no school"}` : r ? `${t.name}: you agree on ${r.k} of ${r.n}` : `${t.name}: not enough shared statements`;
    const note = t.provisional ? " (new voice, placed from the statements only)" : "";
    const dash = t.provisional ? "1 2.5" : r || !result ? "" : "3 3";
    svg += `<g class="map-thinker"><title>${esc(title + note)}</title><circle cx="${x}" cy="${y}" r="15" fill="${fill}" stroke-dasharray="${dash}"/>`;
    svg += `<text x="${x}" y="${y + 3.5}" text-anchor="middle">${esc(t.initials)}</text>`;
    if (near.has(t.id)) svg += `<text class="map-name" x="${x}" y="${y + 30}" text-anchor="middle">${esc(t.name)}</text>`;
    svg += `</g>`;
  }
  if (result?.position) {
    const x = X(result.position.x), y = Y(result.position.y);
    for (const t of result.nearest) {
      const [tx, ty] = pos[t.id];
      svg += `<line x1="${x}" y1="${y}" x2="${tx}" y2="${ty}" stroke="var(--ink)" stroke-opacity="0.35" stroke-width="1.2"/>`;
    }
    svg += `<g><title>You (approximate)</title><circle cx="${x}" cy="${y}" r="22" fill="none" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="2 4"/><circle class="map-you" cx="${x}" cy="${y}" r="7"/><text class="map-name" x="${x + 28}" y="${y + 4}" font-weight="700">You</text></g>`;
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
      svg += `<g><title>${esc(m.title || m.label)}</title><circle cx="${tx}" cy="${ty}" r="9" fill="var(--ink)"/><text x="${tx}" y="${ty + 4}" text-anchor="middle" fill="var(--paper)" font-weight="700" font-size="11">${esc(m.label)}</text></g>`;
    });
  }
  return svg + "</svg>";
}

