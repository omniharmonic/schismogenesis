import { esc, mapSVG } from "./map.js";
import { explorer, schoolGrid } from "./explore.js";
import { fingerprint } from "./placement.js";

// answers saved by this browser, if the visitor took it here; never sent anywhere from this page
function savedAnswers(bundle) {
  try {
    const saved = JSON.parse(localStorage.getItem("fp.answers"));
    return saved && saved.season === bundle.season ? saved.answers || {} : {};
  } catch { return {}; }
}

async function main() {
  const [bundle, data] = await Promise.all([
    fetch("/fingerprint.json").then((r) => r.json()),
    fetch("/api/people").then((r) => r.json()).catch(() => ({ people: [] })),
  ]);
  const people = data.people || [];
  const names = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t.name]));
  const answers = savedAnswers(bundle);
  const result = Object.keys(answers).length ? fingerprint(bundle, answers) : null;
  const ok = result?.status === "ok" ? result : null;
  document.getElementById("empty").hidden = people.length > 0;
  // each listed person is a number tag on their nearest thinker, like room groups
  const counts = {};
  for (const p of people) counts[p.summary.nearest[0].id] = (counts[p.summary.nearest[0].id] || 0) + 1;
  const marks = Object.entries(counts).map(([id, n]) => ({ near: [id], label: String(n), title: `${n} listed ${n === 1 ? "person is" : "people are"} nearest to ${names[id]}` }));
  const size = innerWidth < 600 ? { width: 400, height: 640 } : { width: 800, height: 640 };
  const mapEl = document.getElementById("people-map");
  mapEl.innerHTML = mapSVG(bundle, { marks, result: ok, ...size });
  document.getElementById("people-schools").innerHTML = schoolGrid(bundle, ok);
  const ex = explorer({
    bundle, answers, mapEl, panelEl: document.getElementById("people-panel"),
    gridEl: document.getElementById("people-schools"),
    mapOptions: { marks, result: ok, ...size },
    intro: `<h3>${bundle.thinkers.length} thinkers, ${bundle.schools.length} camps</h3>
      <p>Each circle is a public thinker, placed by what they've said on the ${bundle.anchors.length} statements and the wider atlas. Select a camp to open the schools inside it, and keep going down to the tightest circles of people who agree on almost everything. Select a person to read their positions in their own words.</p>
      ${ok ? `<p class="small muted">Your saved answers from this browser are shown beside theirs.</p>` : `<p><a class="button primary" href="/">Take the fingerprint</a></p><p class="small muted">Then you'll see your own answers beside theirs.</p>`}`,
  });
  // /people#<thinker-id> opens that thinker's card (linked from shared profiles)
  const fromHash = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (bundle.thinkers.some((t) => t.id === id)) ex.open({ thinker: id });
  };
  fromHash();
  addEventListener("hashchange", fromHash);
  document.getElementById("people-list").innerHTML = people.map((p) => `<li><a href="/p/${esc(p.code)}">
    ${p.avatar_url ? `<img class="avatar" src="${esc(p.avatar_url)}" alt="" referrerpolicy="no-referrer">` : `<span class="avatar"></span>`}
    <span><b>${esc(p.display_name)}</b><br><span class="small">@${esc(p.handle)} is closest to the ${esc(p.summary.home)}</span></span></a></li>`).join("");
}

main();
