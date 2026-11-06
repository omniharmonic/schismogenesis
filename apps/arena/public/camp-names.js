// Camp names. The lab drafted every camp and school name from public figures' words; people who
// sit in a camp can propose a name it would sign and vote on each other's (one Bluesky or X
// account, one vote), and Benjamin accepts names from the admin page. Accepted names replace the
// drafts everywhere a label is shown on the debate site: loadBundle() applies them to the bundle,
// so the map, the camp lists, results and share text all read the same name.
import { esc } from "./map.js";
import { bskyIntentURL, xIntentURL } from "./share-links.js";

export const NAME_MIN = 3, NAME_MAX = 48;
export const CAMP_SHARE_URL = "https://debate.antimemes.is/account.html#results";

// ---------- accepted names (pure) ----------

/**
 * Put accepted names ({nodeId: name}) in place of the drafted labels, everywhere the bundle
 * carries them: the tree, the camp list (schools, camps) and each thinker's school and between.
 * Mutates and returns the bundle; adds bundle.named ({nodeId: true}) and bundle.renamed
 * ({drafted label: accepted name}, for labels the server computed from the drafts).
 */
export function applyCampNames(bundle, names) {
  bundle.named ||= {};
  bundle.renamed ||= {};
  const nodes = bundle.tree?.nodes || {};
  for (const [id, raw] of Object.entries(names || {})) {
    const n = nodes[id], name = typeof raw === "string" ? raw.trim() : "";
    if (!n || !name || name === n.label) continue;
    bundle.renamed[n.label] = name;
    n.drafted ||= n.label;
    n.label = name;
    bundle.named[id] = true;
  }
  const rename = (label) => (typeof label === "string" && bundle.renamed[label]) || label;
  for (const s of bundle.schools || []) s.label = rename(s.label);
  for (const c of Array.isArray(bundle.camps) ? bundle.camps : []) c.label = c.id && nodes[c.id] ? nodes[c.id].label : rename(c.label);
  for (const t of bundle.thinkers || []) {
    if (t.school) t.school = rename(t.school);
    if (Array.isArray(t.between)) t.between = t.between.map(rename);
  }
  return bundle;
}

/** A label the server worked out from the drafts, as it now reads. */
export const relabel = (bundle, label) => (typeof label === "string" && bundle?.renamed?.[label]) || label;

let accepted = null;
/** GET /api/camps/accepted once per page; nothing accepted (or no endpoint yet) is {}. */
export function fetchAccepted() {
  accepted ||= fetch("/api/camps/accepted")
    .then((r) => (r.ok ? r.json() : null))
    .then((d) => (d?.names && typeof d.names === "object" ? d.names : {}))
    .catch(() => ({}));
  return accepted;
}

/** The fingerprint bundle with the accepted camp names in place. */
export async function loadBundle(url = "/fingerprint.json") {
  const [bundle, names] = await Promise.all([fetch(url).then((r) => r.json()), fetchAccepted()]);
  return applyCampNames(bundle, names);
}

// ---------- the naming panel (pure) ----------

/** The server's answer made safe: a missing endpoint or a failure is unavailable. */
export function normaliseNaming(d) {
  if (!d || typeof d !== "object" || !Array.isArray(d.nodes)) return { available: false, nodes: [], verified: false, names: [] };
  const nodes = d.nodes.filter((n) => n && typeof n.id === "string").map((n) => ({ id: n.id, label: String(n.label || n.id) }));
  const names = (Array.isArray(d.names) ? d.names : []).filter((n) => n && n.id && typeof n.name === "string" && nodes.some((x) => x.id === n.node))
    .map((n) => ({ ...n, up: Number(n.up) || 0, down: Number(n.down) || 0, my_vote: n.my_vote === "up" || n.my_vote === "down" ? n.my_vote : null }));
  return { available: true, nodes, verified: Boolean(d.verified), names };
}

/** Proposals for one group, best supported first (up minus down, then more votes, then name). */
export function rankNames(names, node) {
  return names.filter((n) => n.node === node)
    .sort((a, b) => (b.up - b.down) - (a.up - a.down) || (b.up + b.down) - (a.up + a.down) || a.name.localeCompare(b.name));
}

/** What a vote button sends: pressing your current vote again takes it back. */
export function nextVote(current, pressed) {
  if (current === pressed) return null;
  return pressed === "up";
}

/** A proposed name, tidied; or an error message when it won't be accepted. */
export function checkName(raw) {
  const name = String(raw || "").split(/\s+/).filter(Boolean).join(" ");
  if (name.length < NAME_MIN || name.length > NAME_MAX) return { error: `Use ${NAME_MIN} to ${NAME_MAX} characters.` };
  if (/https?:|www\.|@|\.com\b/i.test(name)) return { error: "Use plain words, without links or handles." };
  return { name };
}

const isCamp = (bundle, id, i) => {
  const level = bundle?.tree?.nodes?.[id]?.level;
  return Number.isFinite(level) ? level === 0 : i === 0;
};

/** The words for one of your groups: its name now, and whether its members named it. */
export function groupTitle(bundle, node, i) {
  const kind = isCamp(bundle, node.id, i) ? "camp" : "school";
  const n = bundle?.tree?.nodes?.[node.id];
  const named = Boolean(bundle?.named?.[node.id]);
  const now = named ? n.label : node.label;
  return { kind, named, now, drafted: named ? n.drafted || node.label : node.label };
}

/** The share post asking your camp to vote. */
export function campShareText(title) {
  return title.named
    ? `My ${title.kind} in The Great AI Debate is “${title.now}”, a name its members chose. Are you in it too?`
    : `My ${title.kind} in The Great AI Debate is drafted as “${title.now}”. If it's yours too, help name it: propose a name we'd sign, or vote.`;
}

function proposalHTML(n) {
  const closed = n.status && n.status !== "open";
  const vote = (dir, label, count) => `<button type="button" class="vote-${dir}" data-vote="${dir}" data-id="${esc(n.id)}"
      aria-pressed="${n.my_vote === dir}" ${closed ? "disabled" : ""} aria-label="${esc(`${label} for “${n.name}”, ${count} so far`)}">${label} <span class="num">${count}</span></button>`;
  return `<li class="name-row">
    <p class="serif name-text">${esc(n.name)}${n.proposed_by_me ? ` <span class="chip unsure">Your proposal</span>` : ""}${n.status === "accepted" ? ` <span class="chip bridge-passed">Accepted</span>` : ""}</p>
    <div class="name-votes" role="group" aria-label="${esc(`Votes on “${n.name}”`)}">${vote("up", "Up", n.up)}${vote("down", "Down", n.down)}</div>
  </li>`;
}

/**
 * The naming panel's inner HTML. `data` is normaliseNaming's; `compact` is the short version
 * for the thinkers page; `settings` is where to add a Bluesky or X sign-in.
 */
export function namingHTML(data, { bundle = null, compact = false, settings = "/account.html#settings" } = {}) {
  const intro = compact
    ? `<p>The camp names on this map are drafts the lab wrote from public figures' words. People inside a camp propose a name it would sign and vote on each other's. Benjamin accepts names; until then the map keeps the draft.</p>`
    : `<p>The lab drafted every camp and school name on this map from public figures' own words. They are placeholders. The people inside a camp are better placed to name it: propose a name your camp would sign, vote on the others, or suggest a better one.</p>
      <p class="small muted">Benjamin reviews the proposals and accepts names. Until he does, the map keeps the draft.</p>`;
  if (!data.nodes.length) {
    return `<h2 id="naming-title">Name your camp</h2>${intro}
      <p>Take the survey to find your camp. Then you can help name it.</p>
      <div class="row"><a class="button primary" href="/">Take the survey</a></div>`;
  }
  const titles = data.nodes.map((n, i) => groupTitle(bundle, n, i));
  // the server picks your camp and school by the same rule as your result's headline
  const where = "";
  const head = (t) => t.named
    ? `Your ${t.kind}, named “${esc(t.now)}” by its members`
    : `Your ${t.kind}, drafted as “${esc(t.now)}”`;
  if (!data.verified) {
    return `<h2 id="naming-title">Name your camp</h2>${intro}
      <ul class="name-groups">${titles.map((t) => `<li><h3>${head(t)}</h3></li>`).join("")}</ul>
      ${where}
      <p class="name-gate">Naming is open to people signed in with Bluesky or X, so each vote is one real account. <a href="${esc(settings)}">Add one in Settings</a>.</p>`;
  }
  const blocks = data.nodes.map((node, i) => {
    const t = titles[i];
    const list = rankNames(data.names, node.id);
    const shown = compact ? list.slice(0, 3) : list;
    const fid = `name-${node.id.replace(/[^a-z0-9]/gi, "-")}`;
    return `<section class="name-group" data-node-id="${esc(node.id)}" aria-labelledby="${fid}-h">
      <h3 id="${fid}-h">${head(t)}</h3>
      ${t.named ? `<p class="small muted">Drafted by the lab as “${esc(t.drafted)}”.</p>` : ""}
      ${shown.length ? `<ol class="name-list">${shown.map(proposalHTML).join("")}</ol>` + (list.length > shown.length ? `<p class="small muted">${list.length - shown.length} more on <a href="/account.html#results">your results page</a>.</p>` : "")
        : `<p class="muted">No one has proposed a name yet. Yours could be the first.</p>`}
      <form class="name-form" data-propose="${esc(node.id)}" novalidate>
        <label class="small" for="${fid}-in">Propose a name your ${t.kind} would sign</label>
        <div class="linkbox"><input type="text" id="${fid}-in" name="name" minlength="${NAME_MIN}" maxlength="${NAME_MAX}" autocomplete="off" required>
          <button type="submit" class="primary">Propose</button></div>
        <p class="small muted">Plain words, ${NAME_MIN} to ${NAME_MAX} characters. If someone already proposed it, this counts as your vote for theirs.</p>
        <p class="small error" role="alert" data-msg hidden></p>
      </form>
    </section>`;
  }).join("");
  const share = titles[0];
  const text = campShareText(share);
  return `<h2 id="naming-title">Name your camp</h2>${intro}${where}${blocks}
    <div class="name-share">
      <h3>Ask your camp to vote</h3>
      <p class="small muted">A name means more when many of its members back it. Post a link to your results page; people in your camp can vote from theirs.</p>
      <div class="share-pair">
        <a class="button" data-share="camp-x" href="${esc(xIntentURL(text, CAMP_SHARE_URL))}" target="_blank" rel="noopener">Share on X</a>
        <a class="button" data-share="camp-bsky" href="${esc(bskyIntentURL(text, CAMP_SHARE_URL))}" target="_blank" rel="noopener">Share on Bluesky</a>
      </div>
    </div>`;
}

// ---------- wiring (browser only) ----------

async function send(path, body) {
  let res;
  try {
    res = await fetch(path, { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  } catch { throw new Error("Couldn't reach the server. Check your connection and try again."); }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = Array.isArray(data.detail) ? `Use plain words, ${NAME_MIN} to ${NAME_MAX} characters.` : data.detail;
    throw new Error(data.error || detail || `That didn't work (${res.status}). Try again.`);
  }
  return data;
}

/**
 * Fill `el` (a <section>) with the naming panel for the signed-in person. Hides it when the
 * server has no naming yet. Returns a promise that settles once it is drawn.
 */
export async function mountNaming(el, { bundle = null, compact = false, toast = () => {} } = {}) {
  if (!el) return;
  const load = async () => {
    try {
      const r = await fetch("/api/camps/names", { credentials: "same-origin" });
      return normaliseNaming(r.ok ? await r.json() : null);
    } catch { return normaliseNaming(null); }
  };
  let state = null;
  const draw = (data, focus = null) => {
    state = data;
    if (!data.available) { el.hidden = true; el.innerHTML = ""; return; }
    el.hidden = false;
    el.classList.add("naming", "bracketed");
    if (compact) el.classList.add("is-compact");
    el.setAttribute("aria-labelledby", "naming-title");
    el.innerHTML = namingHTML(data, { bundle, compact });
    if (focus) el.querySelector(focus)?.focus();
  };
  draw(await load());

  el.addEventListener("click", async (e) => {
    const b = e.target.closest("[data-vote]");
    if (!b || b.disabled) return;
    const row = state?.names.find((n) => n.id === b.dataset.id);
    b.disabled = true;
    try {
      await send(`/api/camps/names/${encodeURIComponent(b.dataset.id)}/vote`, { up: nextVote(row?.my_vote ?? null, b.dataset.vote) });
      draw(await load(), `[data-id="${CSS.escape(b.dataset.id)}"][data-vote="${b.dataset.vote}"]`);
    } catch (err) { b.disabled = false; toast(err.message); }
  });
  el.addEventListener("submit", async (e) => {
    const form = e.target.closest("[data-propose]");
    if (!form) return;
    e.preventDefault();
    const msg = form.querySelector("[data-msg]"), input = form.querySelector("input"), go = form.querySelector("button");
    const checked = checkName(input.value);
    if (checked.error) { msg.textContent = checked.error; msg.hidden = false; input.focus(); return; }
    go.disabled = true; msg.hidden = true;
    try {
      await send(`/api/camps/${encodeURIComponent(form.dataset.propose)}/names`, { name: checked.name });
      toast("Proposed. Your vote is on it.");
      draw(await load(), `[data-propose="${CSS.escape(form.dataset.propose)}"] input`);
    } catch (err) { go.disabled = false; msg.textContent = err.message; msg.hidden = false; }
  });
}
