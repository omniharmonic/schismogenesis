// One statement in depth: the thinkers on each side in their own words, and how people answer.
import { esc } from "./map.js";

const LAYER = { ontological: "What AI is", epistemic: "How we know", axiological: "What matters",
  empirical: "What will happen", praxis: "What to do" };
const pct = (x) => `${Math.round(x * 100)}%`;
const store = {
  get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode */ } },
};

function side(entries, names, title, cls) {
  if (!entries.length) return `<div><h3>${title}</h3><p class="muted">None of the thinkers we read.</p></div>`;
  return `<div><h3>${title} <span class="muted small">(${entries.length})</span></h3>${entries.map(([id, item]) =>
    `<blockquote class="${cls}">${item.q ? `“${esc(item.q)}”` : ""}<cite>${esc(names[id])}${item.url ? `, <a href="${esc(item.url)}" target="_blank" rel="noopener">${esc(item.work || "source")}</a>` : ""}</cite></blockquote>`).join("")}</div>`;
}

async function main() {
  const el = document.getElementById("statement");
  const id = el.dataset.id;
  const [bundle, results] = await Promise.all([
    fetch("/fingerprint.json").then((r) => r.json()),
    fetch("/api/results").then((r) => (r.ok ? r.json() : null)).catch(() => null),
  ]);
  const anchor = bundle.anchors.find((a) => a.id === id);
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  const entries = Object.entries(bundle.stances[id]);
  const yes = entries.filter(([, i]) => i.a === 1), no = entries.filter(([, i]) => i.a === -1);
  const camps = bundle.camps.map((c) => {
    const s = c.members.map((m) => bundle.stances[id][m]?.a).filter((v) => v !== undefined);
    const lean = s.reduce((t, v) => t + v, 0);
    return { label: c.label, lean, n: s.length };
  }).filter((c) => c.n);
  const row = results?.statements?.find((s) => s.id === id);
  const saved = store.get("fp.answers");
  const mine = saved?.answers?.[id];

  const people = row && row.agree_share !== null
    ? `<h2>How people answer</h2>
       <div class="bar" role="img" aria-label="${pct(row.agree / row.answered)} agree"><i style="width:${row.agree / row.answered * 100}%;background:var(--yes)"></i><i style="width:${row.unsure / row.answered * 100}%;background:var(--mid)"></i><i style="width:${row.disagree / row.answered * 100}%;background:var(--no)"></i><span class="marker" style="left:calc(${row.thinkers_agree_share * 100}% - 1px)"></span></div>
       <div class="barnote"><span>${row.agree} agree</span><span>${row.answered} answered</span><span>${row.disagree} disagree</span></div>
       <p class="small muted">The dark line marks how the thinkers split. ${row.gap > 0.15 ? "People here agree more than the thinkers do." : row.gap < -0.15 ? "People here agree less than the thinkers do." : "People here split about like the thinkers."}</p>`
    : `<p class="muted small">Results appear once enough people have added their answers.</p>`;

  el.innerHTML = `
    <p class="muted">${LAYER[anchor.layer]}</p>
    <h1 class="serif" style="font-weight:500;max-width:24ch;font-size:clamp(1.9rem,5.5vw,2.8rem);line-height:1.2">“${esc(anchor.text)}”</h1>
    ${anchor.proposition ? `<details class="small muted"><summary>Wording</summary><p>This is a neutral rewording, checked by two blind reviewers to mean the same as the atlas's original: “${esc(anchor.proposition)}”</p></details>` : ""}
    <div class="answers" role="group" aria-label="Your answer" style="margin:22px 0 8px">
      <button class="agree" data-v="1" aria-pressed="${mine === 1}">Agree</button>
      <button class="disagree" data-v="-1" aria-pressed="${mine === -1}">Disagree</button>
    </div>
    <p class="small" id="mine" role="status">${mine === 1 || mine === -1 ? `You ${mine === 1 ? "agree" : "disagree"}, like ${(mine === 1 ? yes : no).length} of the ${entries.length} thinkers we read.` : "Answer to see who's with you. Your answer stays in your browser."}</p>
    <h2>Where the camps lean</h2>
    <ul class="hbars">${camps.map((c) => `<li><span>${esc(c.label)}</span><span class="small">${c.lean > 0 ? "lean agree" : c.lean < 0 ? "lean disagree" : "split"}</span><span class="num">${c.n} read</span></li>`).join("")}</ul>
    <h2>The thinkers, in their own words</h2>
    <div class="cols">${side(yes, names, "Agree", "agree")}${side(no, names, "Disagree", "disagree")}</div>
    ${people}
    <div class="room-card"><h2 style="margin-top:0">Where do you sit on the rest?</h2>
      <p>${saved?.answers ? "Your answer here counts toward your fingerprint." : "Answer 24 statements like this one, with the names hidden, and see which thinkers you agree with."}</p>
      <a class="button primary" href="/">${saved?.answers ? "Back to my fingerprint" : "Take the fingerprint"}</a></div>
    <p class="small muted">Thinkers are read by machine from their public work, and none has reviewed this. Silence is never counted as disagreement.</p>`;
  for (const b of el.querySelectorAll(".answers button")) {
    b.onclick = () => {
      const v = Number(b.dataset.v);
      const s = store.get("fp.answers") || { version: bundle.version, season: bundle.season, answers: {}, index: 0 };
      s.answers[id] = v; s.season = bundle.season;
      store.set("fp.answers", s);
      for (const x of el.querySelectorAll(".answers button")) x.setAttribute("aria-pressed", String(x === b));
      document.getElementById("mine").textContent = `You ${v === 1 ? "agree" : "disagree"}, like ${(v === 1 ? yes : no).length} of the ${entries.length} thinkers we read: ${(v === 1 ? yes : no).map(([i]) => names[i]).slice(0, 5).join(", ")}${(v === 1 ? yes : no).length > 5 ? "…" : ""}.`;
    };
  }
}

main();
