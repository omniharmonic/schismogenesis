// A published profile. The data comes embedded in the page; the bundle supplies names and quotes.
import { valuesSVG } from "./glyph.js";
import { badge, esc } from "./map.js";

const LAYER = { ontological: "What AI is", epistemic: "How we know", axiological: "What matters",
  empirical: "What will happen", praxis: "What to do" };
const ANSWER = { 1: "Agree", "-1": "Disagree", 0: "Unsure" };
const CLS = { 1: "agree", "-1": "disagree", 0: "unsure" };

async function main() {
  const p = JSON.parse(document.getElementById("profile-data").textContent);
  const bundle = await (await fetch("/fingerprint.json")).json();
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  const s = p.summary;
  const own = (() => { try { return JSON.parse(localStorage.getItem("fp.profile")); } catch { return null; } })();
  const mine = (() => { try { return JSON.parse(localStorage.getItem("fp.answers"))?.answers; } catch { return null; } })();
  const isOwner = own && own.code === p.code;
  const who = p.handle
    ? `<div class="who">${p.avatar_url ? `<img src="${esc(p.avatar_url)}" alt="" referrerpolicy="no-referrer">` : `<span class="avatar"></span>`}
        <div><b>${esc(p.display_name)}</b><br><span class="small muted">@${esc(p.handle)} on ${p.identity === "x" ? "X" : "Bluesky"}, verified</span></div></div>`
    : `<p class="muted">${esc(p.display_name)}, shared anonymously</p>`;
  // a profile keeps the bundle it was made with, so a thinker may no longer be on today's map
  const row = (m) => {
    const t = bundle.thinkers.find((x) => x.id === m.id);
    const name = names[m.id] || m.name || m.id;
    const initials = t?.initials || name.split(/\s+/).map((w) => w[0]).join("").slice(0, 2);
    const label = t ? `<a href="/people#${esc(m.id)}">${esc(name)}</a>` : esc(name);
    return `<li>${badge(t || { initials })}
    <span><b>${label}</b></span><span class="score"><b>${m.k} of ${m.n}</b><br><span class="small muted">agree</span></span></li>`;
  };

  let compare = "";
  if (mine && p.answers) {
    const shared = Object.keys(p.answers).filter((a) => [1, -1].includes(p.answers[a]) && [1, -1].includes(mine[a]));
    const same = shared.filter((a) => p.answers[a] === mine[a]).length;
    if (shared.length) compare = `<div class="room-card"><h3 style="margin-top:0">You and ${esc(p.display_name)}</h3><p>You agree on <b>${same} of ${shared.length}</b> statements you both took a side on.</p></div>`;
  }
  const answersHTML = p.answers ? `<h2>Every answer</h2>${bundle.anchors.filter((a) => p.answers[a.id] !== undefined).map((a) => {
    const v = p.answers[a.id];
    const withThem = Object.entries(bundle.stances[a.id]).filter(([, i]) => i.a === v).map(([id]) => names[id]);
    return `<div class="mirror" style="border-bottom:1px solid var(--line);padding:12px 0;display:grid;grid-template-columns:1fr auto;gap:12px">
      <span><span class="serif">${esc(a.text)}</span>${v !== 0 && withThem.length ? `<br><span class="small muted">With them: ${withThem.slice(0, 4).map(esc).join(", ")}${withThem.length > 4 ? "…" : ""}</span>` : ""}</span>
      <span class="chip ${CLS[v]}">${ANSWER[v]}</span></div>`;
  }).join("")}` : "";

  document.getElementById("profile").innerHTML = `
    ${who}
    <div class="reveal-head" style="margin-top:24px">
      ${valuesSVG(p.glyph, { label: `${p.display_name}'s fingerprint` })}
      <div><p class="muted">AI futures fingerprint</p><h1 style="max-width:18ch">Closest to the ${esc(s.home)}</h1>
      <p>From ${s.answered} statements, answered with the names hidden.</p></div>
    </div>
    ${compare}
    <h2>Nearest thinkers</h2>
    <div class="cols"><div><ul class="thinkers">${s.nearest.map(row).join("")}</ul></div>
      <div><p class="muted" style="margin:0 0 4px">Furthest</p><ul class="thinkers">${s.furthest.map(row).join("")}</ul></div></div>
    ${s.signature.length ? `<h2>Plot twist</h2><ul class="signature">${s.signature.map((t) => `<li><span class="serif">${t.answer === 1 ? "Agrees" : "Disagrees"}: “${esc(t.text)}”</span>
      <p class="small muted" style="margin-top:6px">Against most of the ${esc(t.home)}, with the ${esc(t.ally)}.</p></li>`).join("")}</ul>` : ""}
    ${s.rarest ? `<h2>Rarest take</h2><p class="serif" style="font-size:1.25rem">${s.rarest.answer === 1 ? "Agrees" : "Disagrees"}: “${esc(s.rarest.text)}”</p>` : ""}
    <h2>The camps</h2>
    <table class="camps-table"><tr><th scope="col">Camp</th><th scope="col">With</th><th scope="col">Against</th><th scope="col">Deepest split</th></tr>
      ${s.camps.map((c) => `<tr><th scope="row">${esc(c.label)}</th><td class="cell-agree">${c.agreed}</td><td class="cell-split">${c.opposed}</td><td>${c.deepest ? LAYER[c.deepest] : "none"}</td></tr>`).join("")}</table>
    ${answersHTML}
    <div class="room-card"><h2 style="margin-top:0">Where do you sit?</h2><p>Answer ${bundle.anchors.length} statements with the names hidden, then see which of ${bundle.thinkers.length} thinkers you agree with.</p>
      <a class="button primary" href="/">Take the fingerprint</a></div>
    ${isOwner ? `<p class="small muted">This is your page. <button class="link-button" id="delete">Delete it</button></p>` : ""}
    <p class="small muted">Result as computed in the publisher's browser. Thinkers are read by machine from their public work and haven't reviewed this.</p>`;
  const del = document.getElementById("delete");
  if (del) del.onclick = async () => {
    if (!confirm("Delete this page? The link will stop working.")) return;
    await fetch(`/api/profiles/${p.code}`, { method: "DELETE", headers: { "X-Edit-Key": own.edit_key } });
    localStorage.removeItem("fp.profile");
    location.href = "/";
  };
}

main();
