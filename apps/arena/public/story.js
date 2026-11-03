// The Wrapped story: one idea per full-screen slide, in order, each savable as a story image.
import { drawStory, canvasBlob, twistLine } from "./card.js";
import { highlights } from "./fingerprint.js";
import { glyphValues, valuesSVG } from "./glyph.js";
import { esc, mapSVG } from "./map.js";

const LAYER = { ontological: "what AI is", epistemic: "how we know", axiological: "what matters",
  empirical: "what will happen", praxis: "what to do" };
const T = {
  ultramarine: { bg: "#2f4bd9", fg: "#f7f9fb" },
  ink: { bg: "#1b2430", fg: "#e9edf2" },
  paper: { bg: "#e9edf2", fg: "#1b2430" },
  crimson: { bg: "#9e1f4f", fg: "#fff4f8" },
  night: { bg: "#10151c", fg: "#8fa3ff" },
  teal: { bg: "#126b58", fg: "#effaf6" },
  lilac: { bg: "#c9d2ff", fg: "#18213a" },
};

const event = (name) => fetch("/api/event", { method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name }) }).catch(() => {});

function slides(bundle, answers, r) {
  const h = highlights(bundle, answers, r);
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  const top = r.nearest[0], far = r.furthest[0];
  const out = [];
  out.push({ ...T.ultramarine, print: true,
    eyebrow: "This is your fingerprint.",
    title: `${r.answered} statements. 27 thinkers. One print.`,
    lede: "Every ridge bends with one of your answers. No one else's looks quite like it." });
  out.push({ ...T.ink, eyebrow: "Your neighbourhood",
    title: `The ${r.schools[0].label}`,
    lede: `Your closest thinker sits here. The next nearest schools: ${r.schools.slice(1, 3).map((s) => s.label).join(" and ")}.` });
  out.push({ ...T.paper, eyebrow: "Your top match",
    title: top.name, big: undefined,
    lede: `You agree on ${top.k} of the ${top.n} statements you both took a side on.`,
    quote: h.topQuote?.q,
    cite: h.topQuote ? `${top.name}, ${h.topQuote.work}. You both said ${h.topQuote.answer === 1 ? "yes" : "no"} to “${h.topQuote.text.replace(/\.$/, "")}”` : undefined,
    rows: h.topQuote ? undefined : r.nearest.slice(1).map((t) => [t.name, `${t.k} of ${t.n}`]) });
  if (r.signature[0]) {
    const s = r.signature[0];
    out.push({ ...T.crimson, eyebrow: "Plot twist",
      title: `You break with the ${s.home}.`,
      lede: `On this one you side with the ${s.ally}, with ${s.allies.map((a) => names[a]).slice(0, 2).join(" and ")}:`,
      quote: `${s.answer === 1 ? "Yes:" : "No:"} ${s.text}` });
  } else {
    out.push({ ...T.crimson, eyebrow: "No plot twist",
      title: "You hold the line.",
      lede: `On every statement we could check, you're with the ${r.schools[0].label}. Rare.` });
  }
  out.push({ ...T.night, eyebrow: "Your furthest", title: far.name,
    lede: `You agree on just ${far.k} of ${far.n}.`,
    quote: h.farQuote?.q,
    cite: h.farQuote ? `${far.name}, ${h.farQuote.work}. You said ${h.farQuote.answer === 1 ? "yes" : "no"} to “${h.farQuote.text.replace(/\.$/, "")}”; they said ${h.farQuote.answer === 1 ? "no" : "yes"}.` : undefined });
  out.push({ ...T.teal, eyebrow: "You and the camps",
    title: "Where they split from you",
    rows: r.camps.map((c) => [c.label, c.deepest ? `split at ${LAYER[c.deepest]}` : `${c.agreed} with, ${c.opposed} against`]) });
  if (h.rarest) {
    out.push({ ...T.lilac, eyebrow: "Your rarest take",
      big: `${h.rarest.with}/${h.rarest.of}`,
      lede: `You said ${h.rarest.answer === 1 ? "yes" : "no"}. Only ${h.rarest.with} of the ${h.rarest.of} thinkers we read are with you:`,
      quote: h.rarest.text });
  }
  out.push({ ...T.paper, eyebrow: "Where you sit", title: "Among the thinkers", map: true,
    lede: `Lines run to your three nearest: ${r.nearest.map((t) => t.name).join(", ")}.` });
  out.push({ ...T.ultramarine, print: true, final: true, eyebrow: "That's your fingerprint.",
    title: `Closest to the ${r.schools[0].label}`,
    lede: r.signature[0] ? twistLine(r.signature[0]) : `Nearest: ${r.nearest.map((t) => t.name).join(", ")}.` });
  return out;
}

function slideHTML(s, bundle, answers, r) {
  let html = "";
  if (s.print) html += valuesSVG(glyphValues(bundle, answers), { cls: "print", label: "Your fingerprint" });
  if (s.eyebrow) html += `<p class="eyebrow">${esc(s.eyebrow)}</p>`;
  if (s.big) html += `<p class="big-number">${esc(s.big)}</p>`;
  if (s.title) html += `<h2>${esc(s.title)}</h2>`;
  if (s.lede) html += `<p class="lede">${esc(s.lede)}</p>`;
  if (s.quote) html += `<p class="quote">“${esc(s.quote)}”</p>`;
  if (s.cite) html += `<p class="cite">${esc(s.cite)}</p>`;
  if (s.rows) html += `<ul class="rows">${s.rows.map(([a, b]) => `<li><span>${esc(a)}</span><b>${esc(b)}</b></li>`).join("")}</ul>`;
  if (s.map) {
    html += `<div class="mini-map" style="--ridge:${s.fg};--ink:${s.fg};--sheet:${s.bg};--paper:${s.bg};--muted:${s.fg}">${mapSVG(bundle, { result: r, width: 440, height: 400 })}</div>`;
  }
  return html;
}

export function playStory({ bundle, answers, result, onShare, onDone }) {
  const specs = slides(bundle, answers, result);
  const values = glyphValues(bundle, answers);
  let i = 0;
  const root = document.createElement("div");
  root.className = "story";
  root.setAttribute("role", "dialog");
  root.setAttribute("aria-modal", "true");
  root.setAttribute("aria-label", "Your fingerprint, as a story");
  root.innerHTML = `
    <div class="story-bars" aria-hidden="true">${specs.map(() => "<span><i></i></span>").join("")}</div>
    <div class="story-top"><span class="small" id="story-count"></span><button id="story-close">See full results</button></div>
    <div class="story-stage" aria-live="polite">
      <div class="slide"></div>
      <button class="tap prev" aria-label="Previous slide"></button>
      <button class="tap next" aria-label="Next slide"></button>
      <div class="story-actions"></div>
    </div>`;
  document.body.append(root);
  document.body.style.overflow = "hidden";
  const slide = root.querySelector(".slide");
  const actions = root.querySelector(".story-actions");

  async function saveSlide() {
    const canvas = drawStory(document.createElement("canvas"), specs[i], values);
    const blob = await canvasBlob(canvas);
    const file = new File([blob], `fingerprint-${i + 1}.png`, { type: "image/png" });
    if (navigator.canShare?.({ files: [file] })) {
      try { await navigator.share({ files: [file] }); event("share_native"); return; } catch { /* cancelled */ }
    }
    const a = document.createElement("a");
    a.download = file.name; a.href = URL.createObjectURL(blob); a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    event("save_story");
  }

  function close() {
    document.removeEventListener("keydown", keys);
    document.body.style.overflow = "";
    root.remove();
    event("story_done");
    onDone();
  }

  function show(n) {
    i = Math.max(0, Math.min(specs.length - 1, n));
    const s = specs[i];
    root.style.setProperty("--slide-bg", s.bg);
    root.style.setProperty("--slide-fg", s.fg);
    slide.className = "slide";
    slide.innerHTML = slideHTML(s, bundle, answers, result);
    void slide.offsetWidth;  // restart the entrance animation
    slide.classList.add("enter");
    root.querySelectorAll(".story-bars span").forEach((b, k) => { b.className = k < i ? "done" : k === i ? "now" : ""; });
    root.querySelector("#story-count").textContent = `${i + 1} of ${specs.length}`;
    actions.innerHTML = s.final
      ? `<button id="share-link">Get my share link</button><button class="ghost" id="save-slide">Save this slide</button><button class="ghost" id="done">See full results</button>`
      : `<button class="ghost" id="save-slide">Save this slide</button>`;
    actions.querySelector("#save-slide").onclick = saveSlide;
    if (s.final) {
      actions.querySelector("#share-link").onclick = () => onShare();
      actions.querySelector("#done").onclick = close;
    }
  }

  function keys(e) {
    if (document.querySelector("dialog[open]")) return;
    if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); show(i + 1); }
    if (e.key === "ArrowLeft") show(i - 1);
    if (e.key === "Escape") close();
  }
  root.querySelector(".tap.prev").onclick = () => show(i - 1);
  root.querySelector(".tap.next").onclick = () => (i === specs.length - 1 ? null : show(i + 1));
  root.querySelector("#story-close").onclick = close;
  document.addEventListener("keydown", keys);
  show(0);
  root.querySelector("#story-close").focus();
  return { close };
}
