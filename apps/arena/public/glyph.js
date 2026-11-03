// The fingerprint glyph: closed ridges bent by each answer at that statement's own angle.
// Agree pushes the ridges outward, disagree pulls them in, unsure leaves a small ripple, skip
// leaves them smooth. Deterministic: the same answers always draw the same print.

const RINGS = 15;

function ridgePath(cx, cy, ring, anchors, answers, scale) {
  const base = (8 + ring * 5.4) * scale;
  const points = [];
  const steps = 180;
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps) * Math.PI * 2;
    let bend = 0;
    anchors.forEach((a, k) => {
      const v = answers[a.id];
      if (v === undefined || v === null) return;
      const theta = (k / anchors.length) * Math.PI * 2 + ring * 0.035;
      const d = Math.atan2(Math.sin(t - theta), Math.cos(t - theta));
      const width = 0.22 + (k % 3) * 0.05;
      const amp = v === 0 ? 0.25 : v * (1.1 + ring * 0.12);
      bend += amp * Math.exp(-(d * d) / (2 * width * width));
    });
    // a whorl is taller than it is wide, and opens slightly at the base like a real print
    const r = base + bend * scale * 2.2;
    const x = cx + r * Math.cos(t) * 0.86;
    const y = cy + r * Math.sin(t) * 1.04 + (Math.sin(t) > 0 ? ring * 0.25 * scale : 0);
    points.push([x, y]);
  }
  return "M" + points.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join("L") + "Z";
}

export function glyphPaths(bundle, answers, size = 200) {
  const scale = size / 200;
  const anchors = bundle.anchors;
  const out = [];
  for (let ring = 0; ring < RINGS; ring++) {
    out.push({ d: ridgePath(size / 2, size / 2, ring, anchors, answers, scale), ring });
  }
  return out;
}

export function glyphSVG(bundle, answers, { size = 200, label = "Your fingerprint" } = {}) {
  const paths = glyphPaths(bundle, answers, size)
    .map((p) => `<path d="${p.d}" fill="none" stroke="var(--ridge)" stroke-width="${(1.7 - p.ring * 0.05).toFixed(2)}" stroke-linecap="round" opacity="${(1 - p.ring * 0.035).toFixed(2)}"/>`)
    .join("");
  return `<svg viewBox="0 0 ${size} ${size}" role="img" aria-label="${label}">${paths}</svg>`;
}
