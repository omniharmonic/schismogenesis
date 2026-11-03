// The fingerprint glyph: closed ridges bent by each answer at its own angle. Agree pushes the
// ridges out, disagree pulls them in, unsure leaves a small ripple, skip leaves them smooth.
// Mirrored in services/api/src/arena_api/cards.py for server-drawn share images.

const RINGS = 15;

/** Answer values in statement order: +1, -1, 0, or null for skipped. */
export function glyphValues(bundle, answers) {
  return bundle.anchors.map((a) => (answers[a.id] === undefined ? null : answers[a.id]));
}

/** The same values in a random order, so a published print can't be read back into answers. */
export function scrambled(values) {
  const out = [...values];
  const rand = new Uint32Array(out.length);
  crypto.getRandomValues(rand);
  for (let i = out.length - 1; i > 0; i--) {
    const j = rand[i] % (i + 1);
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function ridgePath(cx, cy, ring, values, scale) {
  const base = (8 + ring * 5.4) * scale;
  const n = values.length;
  const points = [];
  for (let i = 0; i <= 180; i++) {
    const t = (i / 180) * Math.PI * 2;
    let bend = 0;
    values.forEach((v, k) => {
      if (v === undefined || v === null) return;
      const theta = (k / n) * Math.PI * 2 + ring * 0.035;
      const d = Math.atan2(Math.sin(t - theta), Math.cos(t - theta));
      const width = 0.22 + (k % 3) * 0.05;
      const amp = v === 0 ? 0.25 : v * (1.1 + ring * 0.12);
      bend += amp * Math.exp(-(d * d) / (2 * width * width));
    });
    const r = base + bend * scale * 2.2;
    const x = cx + r * Math.cos(t) * 0.86;
    const y = cy + r * Math.sin(t) * 1.04 + (Math.sin(t) > 0 ? ring * 0.25 * scale : 0);
    points.push([x, y]);
  }
  return "M" + points.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join("L") + "Z";
}

export function pathsFromValues(values, size = 200) {
  const scale = size / 200;
  return Array.from({ length: RINGS }, (_, ring) => ({ d: ridgePath(size / 2, size / 2, ring, values, scale), ring }));
}

export function glyphPaths(bundle, answers, size = 200) {
  return pathsFromValues(glyphValues(bundle, answers), size);
}

export function valuesSVG(values, { size = 200, label = "Fingerprint", cls = "" } = {}) {
  const paths = pathsFromValues(values, size)
    .map((p) => `<path d="${p.d}" fill="none" stroke="var(--ridge)" stroke-width="${(1.7 - p.ring * 0.05).toFixed(2)}" stroke-linecap="round" opacity="${(1 - p.ring * 0.035).toFixed(2)}"/>`)
    .join("");
  return `<svg class="${cls}" viewBox="0 0 ${size} ${size}" role="img" aria-label="${label}">${paths}</svg>`;
}

export function glyphSVG(bundle, answers, opts = {}) {
  return valuesSVG(glyphValues(bundle, answers), { label: "Your fingerprint", ...opts });
}
