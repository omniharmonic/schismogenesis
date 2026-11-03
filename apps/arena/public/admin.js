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
      `<h2>Daily counts</h2><table class="camps-table">${d.counters.map((c) => `<tr><td>${esc(c.day)}</td><td>${esc(c.name)}</td><td>${c.n}</td></tr>`).join("")}</table>`;
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
