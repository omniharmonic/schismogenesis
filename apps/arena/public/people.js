import { esc, mapSVG } from "./map.js";

async function main() {
  const [bundle, data] = await Promise.all([
    fetch("/fingerprint.json").then((r) => r.json()),
    fetch("/api/people").then((r) => r.json()),
  ]);
  const people = data.people;
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  document.getElementById("empty").hidden = people.length > 0;
  // each person is a letter-tag on their nearest thinker, like room groups
  const counts = {};
  for (const p of people) counts[p.summary.nearest[0].id] = (counts[p.summary.nearest[0].id] || 0) + 1;
  const marks = Object.entries(counts).map(([id, n]) => ({ near: [id], label: String(n), title: `${n} listed ${n === 1 ? "person is" : "people are"} nearest to ${names[id]}` }));
  document.getElementById("people-map").innerHTML = mapSVG(bundle, { marks, ...(innerWidth < 600 ? { width: 440, height: 520 } : {}) });
  document.getElementById("people-list").innerHTML = people.map((p) => `<li><a href="/p/${esc(p.code)}">
    ${p.avatar_url ? `<img class="avatar" src="${esc(p.avatar_url)}" alt="" referrerpolicy="no-referrer">` : `<span class="avatar"></span>`}
    <span><b>${esc(p.display_name)}</b><br><span class="small">@${esc(p.handle)} is closest to the ${esc(p.summary.home)}</span></span></a></li>`).join("");
}

main();
