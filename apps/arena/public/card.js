// The share card, drawn on a canvas in the browser and saved as a PNG. Nothing is uploaded.
import { glyphPaths } from "./glyph.js";

function wrap(ctx, text, maxWidth) {
  const words = text.split(" ");
  const lines = [];
  let line = "";
  for (const w of words) {
    const test = line ? `${line} ${w}` : w;
    if (ctx.measureText(test).width > maxWidth && line) { lines.push(line); line = w; } else line = test;
  }
  if (line) lines.push(line);
  return lines;
}

export function drawCard(canvas, bundle, answers, result, { dark = false } = {}) {
  const W = 1200, H = 675;
  canvas.width = W; canvas.height = H;
  const c = canvas.getContext("2d");
  const ink = dark ? "#e3e8ef" : "#1b2430", paper = dark ? "#10151c" : "#e9edf2";
  const ridge = dark ? "#8197ff" : "#2f4bd9", muted = dark ? "#9aa5b4" : "#5d6877";
  c.fillStyle = paper; c.fillRect(0, 0, W, H);
  c.save();
  c.translate(70, 117); c.scale(2.2, 2.2);
  glyphPaths(bundle, answers, 200).forEach((p) => {
    c.strokeStyle = ridge; c.globalAlpha = 1 - p.ring * 0.035; c.lineWidth = 1.7 - p.ring * 0.05;
    c.stroke(new Path2D(p.d));
  });
  c.restore(); c.globalAlpha = 1;
  const left = 600;
  c.fillStyle = muted; c.font = "500 26px 'IBM Plex Sans Condensed', sans-serif";
  c.fillText("My AI futures fingerprint", left, 92);
  c.fillStyle = ink; c.font = "600 50px 'IBM Plex Sans Condensed', sans-serif";
  const home = result.schools[0]?.label || "";
  wrap(c, `Closest to the ${home}`, 540).forEach((l, i) => c.fillText(l, left, 152 + i * 56));
  let y = 152 + Math.min(2, wrap(c, `Closest to the ${home}`, 540).length) * 56 + 18;
  c.font = "500 30px 'IBM Plex Sans Condensed', sans-serif";
  for (const t of result.nearest) {
    c.fillStyle = ink; c.fillText(t.name, left, y);
    c.fillStyle = muted; c.fillText(`${t.k} of ${t.n}`, left + 420, y);
    y += 44;
  }
  if (result.signature[0]) {
    const s = result.signature[0];
    y += 18;
    c.fillStyle = ink; c.font = "italic 400 28px Newsreader, Georgia, serif";
    const line = `…but sides with the ${s.ally} ${s.answer === 1 ? "that" : "against"} “${s.text}”`;
    wrap(c, line, 540).slice(0, 4).forEach((l, i) => c.fillText(l, left, y + i * 36));
  }
  c.fillStyle = muted; c.font = "500 22px 'IBM Plex Sans Condensed', sans-serif";
  c.fillText("Made with Dialogos. Names were hidden while answering. 27 thinkers, read from their public work.", 70, H - 40);
  return canvas;
}

export function cardText(result) {
  const lines = [`My AI futures fingerprint: closest to the ${result.schools[0]?.label}.`];
  lines.push(result.nearest.map((t) => `${t.name} (${t.k}/${t.n})`).join(", "));
  const s = result.signature[0];
  if (s) lines.push(`But I side with the ${s.ally} ${s.answer === 1 ? "that" : "against"} "${s.text}"`);
  return lines.join("\n");
}
