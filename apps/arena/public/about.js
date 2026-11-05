// Photo credits for the About page, from the bundle (scripts/fetch_faces.py fills them in).
import { esc } from "./map.js";
import "./site-config.js";  // keeps the lab links in step with LAB_URL

const bundle = await (await fetch("/fingerprint.json")).json();
const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
const rows = Object.entries(bundle.faces || {}).sort(([a], [b]) => (names[a] || a).localeCompare(names[b] || b));
document.getElementById("credits").innerHTML = rows.map(([id, c]) => {
  const licence = c.license_url ? `<a href="${esc(c.license_url)}" rel="noopener">${esc(c.license)}</a>` : esc(c.license);
  return `<li>${esc(names[id] || id)}: <a href="${esc(c.source)}" rel="noopener">photo</a>${c.artist ? ` by ${esc(c.artist)}` : ""}, ${licence}</li>`;
}).join("") || "<li>No photos yet.</li>";
