const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const REASONS = ["Duplicate", "Not a statement", "Abuse", "Off topic", "Names a private person"];
try { $("token").value = sessionStorage.getItem("fp.admin") || ""; } catch {}
async function call(path, opts = {}) {
  const res = await fetch(path, { ...opts, headers: { "Content-Type": "application/json", Authorization: `Bearer ${$("token").value}` } });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || res.status);
  return data;
}
async function load() {
  try { sessionStorage.setItem("fp.admin", $("token").value); } catch {}
  const room = $("room").value;
  try {
    const d = await call(`/api/admin/${room}/pending`);
    $("msg").textContent = "";
    $("out").innerHTML = `<h2>Pending statements (${d.pending.length})</h2>` +
      (d.pending.length ? d.pending.map((p) => `<div class="room-card"><p class="serif" style="font-size:1.2rem">${esc(p.text)}</p>
        <div class="row"><button class="primary" data-id="${p.statement_id}" data-ok="1">Approve</button>
        ${REASONS.map((r) => `<button data-id="${p.statement_id}" data-reason="${r}">${r}</button>`).join("")}</div></div>`).join("") : `<p class="muted">Nothing waiting.</p>`) +
      `<h2>Fairness ratings</h2><p>${d.fairness.count} ratings, mean ${d.fairness.mean ?? "none yet"}.</p>` +
      `<h2>Placement reports (${d.disputes.length})</h2>` +
      d.disputes.map((x) => `<div class="room-card"><b>${esc(x.person_id)}</b> <span class="small muted">${esc(x.anchor_id)} ${esc(x.created_at)}</span><p>${esc(x.body)}</p><p class="small muted">${esc(x.contact)}</p></div>`).join("") +
      `<h2>Published profiles (${d.profiles.length} latest)</h2>` +
      d.profiles.map((p) => `<div class="row" style="border-bottom:1px solid var(--line);padding:8px 0"><a href="/p/${esc(p.code)}">${esc(p.display_name)}</a> <span class="small muted">${esc(p.identity)} ${p.handle ? "@" + esc(p.handle) : ""} ${p.listed ? "listed" : ""} ${p.hidden_at ? "hidden" : ""}</span>
        <button data-hide="${esc(p.code)}" data-h="${p.hidden_at ? "" : "1"}">${p.hidden_at ? "Unhide" : "Hide"}</button></div>`).join("") +
      `<h2>Camp names proposed</h2><div id="names"><p class="muted">Loading…</p></div>` +
      `<h2>Daily counts</h2><table class="camps-table">${d.counters.map((c) => `<tr><td>${esc(c.day)}</td><td>${esc(c.name)}</td><td>${c.n}</td></tr>`).join("")}</table>`;
    loadNames();
    for (const b of document.querySelectorAll("[data-hide]")) b.onclick = async () => {
      await call(`/api/admin/profiles/${b.dataset.hide}`, { method: "POST", body: JSON.stringify({ hidden: !!b.dataset.h }) });
      load();
    };
    for (const b of document.querySelectorAll("[data-id]")) b.onclick = async () => {
      await call(`/api/admin/${room}/statements/${b.dataset.id}`, { method: "POST",
        body: JSON.stringify({ approve: !!b.dataset.ok, reason: b.dataset.reason || null }) });
      load();
    };
  } catch (e) { $("msg").className = "small error"; $("msg").textContent = `Couldn't load: ${e.message}`; }
}
$("login").onsubmit = (e) => { e.preventDefault(); load(); };

// Camp names: proposed and voted on by verified people inside each camp; nothing renames the
// public map until it's accepted here.
async function loadNames() {
  const el = $("names");
  try {
    const { names } = await call("/api/admin/camps/names");
    const open = names.filter((n) => n.status === "open");
    const done = names.filter((n) => n.status === "accepted");
    el.innerHTML = (open.length ? open.map((n) => `<div class="row" style="border-bottom:1px solid var(--line);padding:8px 0">
        <span><b>${esc(n.name)}</b> <span class="small muted">for ${esc(n.label || n.node)}: ${n.up} for, ${n.down} against</span></span>
        <button class="primary" data-name="${esc(n.id)}" data-accept="1">Accept</button><button data-name="${esc(n.id)}">Decline</button></div>`).join("")
      : `<p class="muted">No open proposals.</p>`) +
      (done.length ? `<p class="small muted">Accepted: ${done.map((n) => `${esc(n.label || n.node)} → ${esc(n.name)}`).join("; ")}</p>` : "");
    for (const b of el.querySelectorAll("[data-name]")) b.onclick = async () => {
      await call(`/api/admin/camps/names/${b.dataset.name}`, { method: "POST", body: JSON.stringify({ accept: !!b.dataset.accept }) });
      loadNames();
    };
  } catch (e) { el.innerHTML = `<p class="small error">Couldn't load names: ${esc(e.message)}</p>`; }
}
