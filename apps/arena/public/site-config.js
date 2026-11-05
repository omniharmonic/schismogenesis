// antimemes.is is one site in two places: the lab, and The Great AI Debate on its own subdomain.
// Every link between them reads from these two constants (docs/brand/BRAND.md).
export const LAB_URL = "https://antimemes.is";
export const DEBATE_URL = "https://debate.antimemes.is";
export const DEBATE_HOST = new URL(DEBATE_URL).host;

export const LAB_LINKS = {
  home: `${LAB_URL}/`,
  idea: `${LAB_URL}/#turn`,
  instruments: `${LAB_URL}/#instruments`,
  debate: `${LAB_URL}/#debate`,
  loop: `${LAB_URL}/#loop`,
  rules: `${LAB_URL}/#rules`,
};

// Static pages already carry these hrefs so they work without scripts; this keeps them in step.
if (typeof document !== "undefined") {
  for (const a of document.querySelectorAll("a[data-lab]")) a.href = LAB_LINKS[a.dataset.lab] || LAB_LINKS.home;
  // on a phone the nav is its own row that scrolls sideways: keep the current page in view, and
  // fade the right edge only while there is more to scroll to
  const nav = document.querySelector(".top-nav");
  if (nav) {
    const current = nav.querySelector("[aria-current]");
    const edge = () => nav.classList.toggle("has-more", nav.scrollLeft + nav.clientWidth < nav.scrollWidth - 2);
    if (current && nav.scrollWidth > nav.clientWidth) nav.scrollLeft = Math.max(0, current.offsetLeft - nav.offsetLeft - 24);
    edge();
    nav.addEventListener("scroll", edge, { passive: true });
    addEventListener("resize", edge, { passive: true });
  }
}

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

/** The handoff from SEE to MEET and MOVE, at the end of a result. `far`: the school furthest from you. */
export function handoffHTML({ far = null } = {}) {
  const meet = far
    ? `Next: read the strongest case from your far side, the school “${esc(far)}”, then try to describe it in words its members would sign.`
    : "Next: read the strongest case of a camp far from you, then try to describe it in words its members would sign.";
  return `<section class="handoff bracketed" aria-labelledby="handoff-title">
    <h2 id="handoff-title">You've seen the map. Now meet the far side.</h2>
    <p class="handoff-lede">The Great AI Debate is the first of three instruments at antimemes.is. Knowing where you stand is the start, not the point. The point is anti-mimesis: meeting the people across the map without copying them or fighting them.</p>
    <ol class="handoff-steps">
      <li class="hs-see"><span class="hs-key">See</span><p>Done. You know where you stand, and who stands furthest from you, in their own words.</p></li>
      <li class="hs-meet"><span class="hs-key">Meet</span><p>${meet} Steelmen and anti-debates are the lab's next instrument.</p></li>
      <li class="hs-move"><span class="hs-key">Move</span><p>Coming. A description the described side signs earns bridging reputation, the way Community Notes works. Agents get a separate board and never sign.</p></li>
    </ol>
    <a class="button primary" href="${LAB_LINKS.loop}">How the map feeds the rest</a>
  </section>`;
}
