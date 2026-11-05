// Share images, drawn on a canvas in the browser and saved as PNG. Nothing is uploaded.
//   drawCard: the 1200x675 landscape card for posts.
//   drawStory: a 1080x1920 story image for one Wrapped slide.
import { pathsFromValues } from "./glyph.js";
import { DEBATE_HOST } from "./site-config.js";

const SANS = "'IBM Plex Sans Condensed', 'Arial Narrow', sans-serif";
const SERIF = "Newsreader, Georgia, serif";
const MACRO = "Anton, Impact, sans-serif";
// the shared antimemes.is ground (docs/brand/BRAND.md); share cards are always dark
const C = { ground: "#121820", ink: "#dde4eb", ink2: "#9aa7b6", recog: "#8fb0ff", heat: "#ff5468", rule: "#2b3644" };

/** The antimemes wordmark, right-aligned at (right, y): one word in Anton, as on the lab. */
function wordmark(c, right, y, size, colour = C.ink) {
  c.save();
  c.font = `400 ${size}px ${MACRO}`;
  c.fillStyle = colour; c.textAlign = "right";
  c.fillText("antimemes", right, y);
  c.restore();
}

function wrap(ctx, text, maxWidth) {
  const lines = [];
  let line = "";
  for (const w of String(text).split(" ")) {
    const test = line ? `${line} ${w}` : w;
    if (ctx.measureText(test).width > maxWidth && line) { lines.push(line); line = w; } else line = test;
  }
  if (line) lines.push(line);
  return lines;
}

function drawPrint(c, values, x, y, size, color) {
  c.save();
  c.translate(x, y); c.scale(size / 200, size / 200);
  for (const p of pathsFromValues(values, 200)) {
    c.strokeStyle = color; c.globalAlpha = 1 - p.ring * 0.035; c.lineWidth = 1.7 - p.ring * 0.05;
    c.stroke(new Path2D(p.d));
  }
  c.restore(); c.globalAlpha = 1;
}

export const twistLine = (s) => `…but sides with “${s.ally}” ${s.answer === 1 ? "that" : "against"} “${s.text}”`;

export function drawCard(canvas, values, result, { thinkers = null } = {}) {
  const W = 1200, H = 675;
  canvas.width = W; canvas.height = H;
  const c = canvas.getContext("2d");
  const { ink, ground: paper, recog: ridge, ink2: muted } = C;
  c.fillStyle = paper; c.fillRect(0, 0, W, H);
  drawPrint(c, values, 50, 95, 470, ridge);
  const left = 600;
  c.fillStyle = muted; c.font = `500 26px ${SANS}`;
  c.fillText("My fingerprint in The Great AI Debate", left, 92);
  c.fillStyle = ink; c.font = `600 54px ${SANS}`;
  const head = wrap(c, `Closest to “${result.schools[0]?.label || ""}”`, 540).slice(0, 2);
  head.forEach((l, i) => c.fillText(l, left, 156 + i * 60));
  let y = 156 + head.length * 60 + 16;
  c.font = `500 30px ${SANS}`;
  for (const t of result.nearest) {
    c.fillStyle = ink; c.fillText(t.name, left, y);
    c.fillStyle = muted; const s = `${t.k} of ${t.n}`; c.fillText(s, W - 60 - c.measureText(s).width, y);
    y += 44;
  }
  if (result.signature[0]) {
    y += 14;
    c.fillStyle = ink; c.font = `italic 400 28px ${SERIF}`;
    wrap(c, twistLine(result.signature[0]), 540).slice(0, 4).forEach((l, i) => c.fillText(l, left, y + i * 36));
  }
  c.fillStyle = C.rule; c.fillRect(50, H - 78, W - 100, 1);
  c.fillStyle = muted; c.font = `500 22px ${SANS}`;
  c.fillText(`Names hidden while answering. ${thinkers ? `${thinkers} thinkers` : "Thinkers"}, read from their public work. ${DEBATE_HOST}`, 50, H - 36);
  wordmark(c, W - 50, H - 34, 30);
  return canvas;
}

/** spec: {bg, fg, eyebrow, title, meme, lede, quote, cite, rows: [[left, right]], big, print} */
export function drawStory(canvas, spec, values) {
  const W = 1080, H = 1920, pad = 96, width = W - pad * 2;
  canvas.width = W; canvas.height = H;
  const c = canvas.getContext("2d");
  // lay out first, then draw the block centred between the header and the footer
  const ops = [];
  let y = 0;
  const text = (str, font, size, gap, alpha = 1, max = 8) => {
    c.font = font;
    for (const l of wrap(c, str, width).slice(0, max)) { y += size; ops.push({ t: "text", l, font, y, alpha }); }
    y += gap;
  };
  if (spec.print) { ops.push({ t: "print", y }); y += 640; }
  if (spec.big) { y += 230; ops.push({ t: "text", l: spec.big, font: `400 300px ${MACRO}`, y, alpha: 1 }); y += 60; }
  if (spec.eyebrow) text(spec.eyebrow, `500 40px ${SANS}`, 52, 24, 0.8, 3);
  if (spec.title) text(spec.meme ? spec.title.toUpperCase() : spec.title, spec.meme ? `400 116px ${MACRO}` : `600 104px ${SANS}`, spec.meme ? 116 : 104, 40, 1, 4);
  if (spec.lede) text(spec.lede, `500 46px ${SANS}`, 60, 30, 1, 6);
  if (spec.quote) text(`“${spec.quote}”`, `italic 400 52px ${SERIF}`, 66, 26, 1, 8);
  if (spec.cite) text(spec.cite, `500 36px ${SANS}`, 48, 20, 0.8, 5);
  for (const [a, b] of spec.rows || []) { y += 82; ops.push({ t: "row", a, b, y }); }
  const top = 220, bottom = H - 200;
  const offset = top + Math.max(0, (bottom - top - y) / 2);
  c.fillStyle = spec.bg; c.fillRect(0, 0, W, H);
  c.fillStyle = spec.fg; c.globalAlpha = 0.75; c.font = `500 34px ${SANS}`;
  c.fillText("The Great AI Debate", pad, 140);
  c.fillText(`Find yours: ${DEBATE_HOST}`, pad, H - 110);
  c.globalAlpha = 1;
  wordmark(c, W - pad, 140, 40, spec.fg);
  for (const op of ops) {
    if (op.t === "print") drawPrint(c, values, pad - 20, offset + op.y - 20, 620, spec.fg);
    if (op.t === "text") { c.globalAlpha = op.alpha; c.font = op.font; c.fillText(op.l, pad, offset + op.y); c.globalAlpha = 1; }
    if (op.t === "row") {
      c.font = `500 46px ${SANS}`; c.fillText(op.a, pad, offset + op.y);
      c.font = `600 46px ${SANS}`; c.fillText(op.b, W - pad - c.measureText(op.b).width, offset + op.y);
      c.globalAlpha = 0.3; c.fillRect(pad, offset + op.y + 26, width, 2); c.globalAlpha = 1;
    }
  }
  return canvas;
}

export function shareText(result, url) {
  const lines = [`My fingerprint in The Great AI Debate: closest to “${result.schools[0]?.label}”.`];
  lines.push(`Nearest: ${result.nearest.map((t) => `${t.name} (${t.k}/${t.n})`).join(", ")}`);
  const s = result.signature[0];
  if (s) lines.push(`Plot twist: I side with “${s.ally}” ${s.answer === 1 ? "that" : "against"} "${s.text}"`);
  if (url) lines.push(url);
  return lines.join("\n");
}

export function canvasBlob(canvas) {
  return new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
}
