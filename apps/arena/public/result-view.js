// Your full result, drawn from a set of answers: the print and your neighbourhood, the map with
// the thinkers (and the crowd), where you break from your neighbours, you and the camps, and the
// quote mirror. Shared by the survey's reveal (app.js) and Your results on the account page.
import { glyphSVG } from "./glyph.js";
import { badge, esc, mapSVG } from "./map.js";
import { explorer, schoolGrid } from "./explore.js";
import { fetchPeople, mountLayerSwitch } from "./crowd.js";
import { protectedFetch } from "./turnstile.js";

export const ANSWER_LABEL = { 1: "Agree", "-1": "Disagree", 0: "Unsure" };
export const ANSWER_CLASS = { 1: "agree", "-1": "disagree", 0: "unsure" };
export const LAYER_NAME = { ontological: "What AI is", epistemic: "How we know", axiological: "What matters",
  empirical: "What will happen", praxis: "What to do" };

// phones get a taller, narrower map so circles stay big enough to tap
export const mapSize = () => (innerWidth < 600 ? { width: 400, height: 640 } : { width: 800, height: 640 });

function thinkerRow(bundle, t) {
  return `<li><button class="thinker-row" data-thinker="${esc(t.id)}">${badge(t)}
    <span><b>${esc(t.name)}</b><br><span class="small muted">${esc(t.school || "No school")}${bundle.thinkers.find((x) => x.id === t.id)?.provisional ? ", new voice" : ""}</span></span>
    <span class="score"><b>${t.k} of ${t.n}</b><br><span class="small muted">agree</span></span></button></li>`;
}

function signatureHTML(bundle, r) {
  if (!r.signature.length) {
    const weakest = r.nearest.at(-1);
    return `<p>You're consistent with “${esc(r.schools[0].label)}” on every statement we could check.
      Your weakest close match is ${esc(weakest.name)}, at ${weakest.k} of ${weakest.n}.</p>`;
  }
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  return `<ul class="signature">${r.signature.map((s) => `<li>
      <span class="serif">You ${s.answer === 1 ? "agree" : "disagree"}: “${esc(s.text)}”</span>
      <p class="small muted" style="margin-top:6px">Most of the thinkers in “${esc(s.home)}” take the other side. Those in “${esc(s.ally)}” are with you: ${s.allies.map((a) => esc(names[a])).join(", ")}.</p>
    </li>`).join("")}</ul>`;
}

function campsHTML(bundle, r) {
  const layers = bundle.layers.filter((l) => r.camps.some((c) => c.byLayer[l][0] + c.byLayer[l][1]));
  const head = `<tr class="head"><th scope="col">Camp</th>${layers.map((l) => `<th scope="col">${LAYER_NAME[l]}</th>`).join("")}<th scope="col">Deepest split</th></tr>`;
  const rows = r.camps.map((c) => `<tr><th scope="row">${esc(c.label)}</th>${layers.map((l) => {
    const [a, o] = c.byLayer[l];
    if (!a && !o) return `<td class="muted" data-label="${LAYER_NAME[l]}">none</td>`;
    return `<td data-label="${LAYER_NAME[l]}"><span class="cell-agree">${a}</span> / <span class="cell-split">${o}</span></td>`;
  }).join("")}<td data-label="Deepest split">${c.deepest ? LAYER_NAME[c.deepest] : "none"}</td></tr>`).join("");
  return `<div class="table-wrap"><table class="camps-table stacks">${head}${rows}</table></div>
    <p class="small muted">Each cell is <span class="cell-agree">with you</span> / <span class="cell-split">against you</span>: statements where the camp's thinkers lean one way and you answered. Layers run from roots to action, so a split low down runs deeper.</p>`;
}

function mirrorHTML(bundle, answers) {
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  // each name opens that thinker's card beside the map
  const who = (id) => `<button class="link-button inline" data-thinker="${esc(id)}">${esc(names[id])}</button>`;
  return bundle.anchors.filter((a) => answers[a.id] !== undefined).map((a) => {
    const v = answers[a.id];
    const entries = Object.entries(bundle.stances[a.id]);
    const quotes = entries.map(([id, item]) => {
      const side = item.a === 1 ? "agree" : "disagree";
      const body = item.q
        ? `“${esc(item.q)}”<cite>${who(id)}, <a href="${esc(item.url)}" target="_blank" rel="noopener">${esc(item.work)}</a>. Read as ${side === "agree" ? "agreeing" : "disagreeing"}.</cite>`
        : `<cite>${who(id)}: read as ${side === "agree" ? "agreeing" : "disagreeing"}.</cite>`;
      return `<blockquote class="${side}">${body}</blockquote>`;
    }).join("");
    const withYou = v === 0 ? 0 : entries.filter(([, i]) => i.a === v).length;
    return `<details class="mirror"><summary><span class="serif">${esc(a.text)}</span>
      <span class="chip ${ANSWER_CLASS[v]}">${ANSWER_LABEL[v]}</span></summary>
      <p class="small muted" style="margin-top:8px">${v === 0 ? `${entries.length} thinkers took a side.` : `${withYou} of ${entries.length} thinkers we read are with you.`}</p>
      ${quotes}
      <div class="row"><a class="small" href="/s/${esc(a.id)}">Open this statement</a>
      <button class="link-button small" data-dispute="${esc(a.id)}">Report a misreading on this statement</button></div>
    </details>`;
  }).join("");
}

/** The result's markup, from the print down to the quote mirror. `r` must have status "ok". */
export function resultHTML(bundle, answers, r, { title = null } = {}) {
  const home = r.schools[0];
  return `<div class="result-core">
    <div class="reveal-head">
      ${glyphSVG(bundle, answers, { label: "Your fingerprint, drawn from your answers" })}
      <div>
        <p class="muted">Your fingerprint</p>
        ${title || `<h1 style="max-width:18ch">Closest to “${esc(home.label)}”</h1>`}
        <p>From ${r.answered} statements you took a side on.</p>
      </div>
    </div>

    <section class="explore" aria-labelledby="sit-title">
      <h2 id="sit-title">Where you sit</h2>
      <p class="muted explore-hint">Select any thinker or school to see where they stand, statement by statement, beside your answers.</p>
      <div class="explore-grid">
        <div class="mapbox" id="reveal-map"><div class="map-slot"></div>
          <p class="map-key small muted"><span><i class="k-dark"></i>agrees with you more</span><span><i class="k-dash"></i>too few shared statements</span><span><i class="k-dot"></i>new voice</span></p>
        </div>
        <aside class="panel" id="reveal-panel" aria-live="polite"></aside>
      </div>
      <h3 class="grid-title">The camps, and the schools inside them</h3>
      <div id="reveal-schools">${schoolGrid(bundle, r)}</div>
      <p class="small"><a href="/atlas">Explore the full 3D atlas of ideas</a></p>
    </section>

    <h2>Where you break from your neighbours</h2>
    ${signatureHTML(bundle, r)}

    <h2>You and the camps</h2>
    ${campsHTML(bundle, r)}

    <h2>Quote mirror</h2>
    <p class="muted">For each statement you answered, the thinkers' own words. Quotes are short and link to the source.</p>
    ${mirrorHTML(bundle, answers)}
  </div>`;
}

/**
 * Make the drawn result work: the map and its side panel, the Thinkers / People / Both switch
 * with "Find me", the crowd, the mirror's names and the misreading reports. `youFace` puts the
 * signed-in person's picture inside the You mark.
 */
export function wireResult(root, { bundle, answers, result: r, youFace = null }) {
  const core = root.querySelector(".result-core");
  const mapEl = core.querySelector("#reveal-map"), panelEl = core.querySelector("#reveal-panel");
  const mapOptions = { result: r, youFace, ...mapSize() };
  core.querySelector(".map-slot").outerHTML = mapSVG(bundle, mapOptions);
  const ex = explorer({
    bundle, answers, mapEl, panelEl, gridEl: core.querySelector("#reveal-schools"),
    mapOptions,
    intro: `<h3>Your nearest thinkers</h3><ul class="thinkers">${r.nearest.map((t) => thinkerRow(bundle, t)).join("")}</ul>
      <h3>Furthest from you</h3><ul class="thinkers">${r.furthest.map((t) => thinkerRow(bundle, t)).join("")}</ul>
      <p class="small muted">Select anyone here or on the map to compare, statement by statement.</p>`,
  });

  // the people who added their answers, on the same map (Thinkers / People / Both)
  const layer = mountLayerSwitch(mapEl, { findMe: true });
  fetchPeople().then((crowd) => {
    layer.set(crowd);
    if (crowd.people.length && mapEl.isConnected) { mapOptions.people = crowd.people; ex.redraw(); }
  });

  core.addEventListener("click", (e) => {
    const t = e.target.closest("details.mirror [data-thinker]");
    if (!t) return;
    ex.open({ thinker: t.dataset.thinker });
    panelEl.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  for (const b of core.querySelectorAll("[data-dispute]")) b.onclick = () => disputeForm(bundle, b, b.dataset.dispute);
  return { ex, mapOptions, layer };
}

function disputeForm(bundle, button, anchorId) {
  const ids = Object.keys(bundle.stances[anchorId]);
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  const form = document.createElement("form");
  form.innerHTML = `<label class="small">Whose position is misread?
      <select name="person" style="display:block;margin:6px 0;min-height:44px">${ids.map((i) => `<option value="${i}">${esc(names[i])}</option>`).join("")}</select></label>
    <label class="small">What's wrong, and where they said otherwise<textarea name="body" required minlength="5" maxlength="2000"></textarea></label>
    <label class="small">Contact, if you'd like a reply (optional)<input type="text" name="contact" maxlength="200"></label>
    <div class="row" style="margin-top:8px"><button class="primary" type="submit">Send report</button></div>`;
  form.onsubmit = async (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const res = await protectedFetch("/api/disputes", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ person_id: f.get("person"), anchor_id: anchorId, body: f.get("body"), contact: f.get("contact") || null }) });
    form.outerHTML = res.ok ? `<p>Report sent. Benjamin's team reviews every one.</p>` : `<p class="error">That didn't send. Try again in a moment.</p>`;
  };
  button.replaceWith(form);
}
