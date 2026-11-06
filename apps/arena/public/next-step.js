// The one next step after you've seen yourself on the map: write a statement both sides can sign.
// It goes to the live room; it becomes a bridge only when people in different groups agree with
// it (Community Notes style). Shown at the end of the reveal, on Your results and on /results.
// Plus "Bridges so far" for the results page. Pure markup here; pages wire the buttons.
import { esc } from "./map.js";

export const MIN_BRIDGE_PEOPLE = 8; // the room scores bridges once this many people have voted

// two groups (camp colours) and one statement between them, joined to both: a bridge
const DIAGRAM = `<svg class="next-diagram" viewBox="0 0 148 64" aria-hidden="true" focusable="false">
  <g class="nd-a"><circle cx="16" cy="20" r="6"/><circle cx="10" cy="38" r="6"/><circle cx="26" cy="48" r="6"/></g>
  <g class="nd-b"><circle cx="132" cy="16" r="6"/><circle cx="138" cy="34" r="6"/><circle cx="122" cy="46" r="6"/></g>
  <path class="nd-link" d="M26 34 L58 32 M122 30 L90 32"/>
  <rect class="nd-statement" x="58" y="24" width="32" height="16" rx="2"/>
  <path class="nd-lines" d="M63 30h22M63 34.5h15"/>
</svg>`;

/**
 * The next-step card. Signed in: one button into the room's write step. Signed out: sign in
 * first, or carry on without an account. `write`, `signin` and `anon` are where the links go
 * (pages that hold the room themselves catch the clicks on [data-next]).
 */
export function nextStepHTML({ signedIn = false, write = "/#write", signin = "/account.html", id = "next-step" } = {}) {
  const reward = signedIn
    ? "Your bridges show on your results page."
    : "Sign in and your bridges show on your results page.";
  return `<section class="next-step bracketed" id="${esc(id)}" aria-labelledby="${esc(id)}-title">
    ${DIAGRAM}
    <h2 id="${esc(id)}-title">Write a statement both sides can sign</h2>
    <p class="next-lede">You've seen where you sit. Now say something people across the map could agree with.</p>
    <p>Statements go to everyone in the live room, who vote on them. One becomes a bridge only when people in different groups agree with it, the way Community Notes works. ${reward}</p>
    <div class="row">${signedIn
      ? `<a class="button primary" href="${esc(write)}" data-next="write">Write a statement</a>`
      : `<a class="button primary" href="${esc(signin)}" data-next="signin">Sign in first</a>
         <a class="button" href="${esc(write)}" data-next="anon">Continue without an account</a>`}</div>
    ${signedIn ? "" : `<p class="small muted">Without an account your statement still counts, under a random ID, but it can't show on a results page.</p>`}
  </section>`;
}

const pct = (x) => (Number.isFinite(x) ? `${Math.round(x * 100)}%` : "n/a");

/** The top bridging statements from a room report: passed first, then leaning. */
export function topBridges(report, n = 3) {
  const b = report?.bridges;
  if (!b) return [];
  const rows = [
    ...(b.passed || []).map((s) => ({ ...s, kind: "passed" })),
    ...(b.leaning || []).map((s) => ({ ...s, kind: "leaning" })),
  ].filter((s) => typeof s?.text === "string");
  return rows.slice(0, n);
}

/** "Bridges so far" for the results page. Says plainly when there are none yet, and why. */
export function bridgesStripHTML(report, { n = 3, room = "/#room" } = {}) {
  const rows = topBridges(report, n);
  const need = `A statement can be scored as a bridge once ${MIN_BRIDGE_PEOPLE} or more people have voted in the live room.`;
  return `<section class="bridges-strip" aria-labelledby="bridges-title">
    <h2 id="bridges-title">Bridges so far</h2>
    <p class="muted">Statements from the live room that people on both sides of its main split agree with. ${need}</p>
    ${rows.length ? `<ol class="bridge-list">${rows.map((s) => `<li class="is-${s.kind}">
        <p class="serif bridge-text">${esc(s.text)}</p>
        <p class="small muted bridge-meta"><span class="chip bridge-${s.kind}">${s.kind === "passed" ? "Bridges the groups" : "Leaning toward a bridge"}</span>
          ${Number.isFinite(s.raters) ? `<span>${s.raters} people voted</span>` : ""}
          ${Array.isArray(s.agree_by_side) ? `<span>Agreement on each side: ${s.agree_by_side.map(pct).join(" and ")}</span>` : ""}</p></li>`).join("")}</ol>`
      : `<p>None yet. Vote on the room's statements, or write one, and the first bridges will show here.</p>`}
    <p><a href="${esc(room)}">Vote in the live room</a></p>
  </section>`;
}

/** The line above "Your statements": what your statements have earned so far. */
export function bridgeSummary(list) {
  const rows = (list || []).filter((s) => s && typeof s.text === "string");
  if (!rows.length) return "";
  const passed = rows.filter((s) => s.bridge === "passed").length, leaning = rows.filter((s) => s.bridge === "leaning").length;
  if (passed) {
    return `${passed === 1 ? "One of your statements bridges" : `${passed} of your statements bridge`} the groups: people who usually disagree both agree with ${passed === 1 ? "it" : "them"}.${leaning ? ` ${leaning} more ${leaning === 1 ? "is" : "are"} leaning that way.` : ""}`;
  }
  if (leaning) return `${leaning === 1 ? "One of your statements is" : `${leaning} of your statements are`} leaning toward a bridge. A few more votes from the other side could tip ${leaning === 1 ? "it" : "them"} over.`;
  return "None of yours bridges the groups yet. That takes votes from people in different groups, so give it time.";
}
