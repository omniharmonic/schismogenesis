// Fingerprint scoring. Runs entirely in the browser and never touches the network (PRD R3).
// The maths is docs/fingerprint/02-ARCHITECTURE.md section 5. The agreement formula mirrors
// packages/arena_fingerprint/src/arena_fingerprint/agreement.py and both are checked against
// packages/arena_fingerprint/tests/vectors.json.

export const MIN_SHARED = 3;
export const MIN_ANSWERED = 6;
export const MIN_RANKED = 5;
const LAYERS = ["ontological", "epistemic", "axiological", "empirical", "praxis"];

const sign = (x) => (x > 0) - (x < 0);
export const score = (k, n) => (k + 1) / (n + 2);

/** stancesA: anchor -> thinker -> +1|-1. Returns thinker -> {k, n, s}. */
export function agreement(answers, stancesA) {
  const out = {};
  for (const [anchor, answer] of Object.entries(answers)) {
    if (answer !== 1 && answer !== -1) continue;
    for (const [thinker, stance] of Object.entries(stancesA[anchor] || {})) {
      const row = (out[thinker] ||= { k: 0, n: 0 });
      row.n += 1;
      if (stance === answer) row.k += 1;
    }
  }
  for (const row of Object.values(out)) row.s = score(row.k, row.n);
  return out;
}

/** The bundle keeps quotes with stances; reduce to plain signs. */
export function plainStances(bundle) {
  const out = {};
  for (const [anchor, entry] of Object.entries(bundle.stances)) {
    out[anchor] = {};
    for (const [thinker, item] of Object.entries(entry)) out[anchor][thinker] = item.a;
  }
  return out;
}

function majority(entry, members) {
  let total = 0;
  let count = 0;
  for (const m of members) {
    if (entry[m] !== undefined) {
      total += entry[m];
      count += 1;
    }
  }
  return { side: sign(total), count };
}

// share of members on the given side
function sideShare(entry, members, side) {
  let on = 0;
  let count = 0;
  for (const m of members) {
    if (entry[m] === undefined) continue;
    count += 1;
    if (entry[m] === side) on += 1;
  }
  return { on, count, share: count ? on / count : 0 };
}

export function fingerprint(bundle, answers) {
  const stancesA = plainStances(bundle);
  const thinkers = Object.fromEntries(bundle.thinkers.map((t) => [t.id, t]));
  const answered = Object.values(answers).filter((a) => a === 1 || a === -1).length;
  const agree = agreement(answers, stancesA);
  const rows = Object.entries(agree)
    .filter(([, r]) => r.n >= MIN_SHARED)
    .map(([id, r]) => ({ id, name: thinkers[id].name, initials: thinkers[id].initials,
      school: thinkers[id].school, ...r }))
    .sort((a, b) => b.s - a.s || b.n - a.n || (a.id < b.id ? -1 : 1));
  if (answered < MIN_ANSWERED || rows.length < MIN_RANKED) {
    return { status: "not_enough", answered, needed: MIN_ANSWERED, ranked: rows };
  }

  // A school is as close as its closest ranked member. Averaging penalised large, mixed schools
  // (the balance test in apps/arena/tests showed Builders topping at 0.3x their fair share).
  const rank = Object.fromEntries(rows.map((r, i) => [r.id, i]));
  const schools = bundle.schools
    .map((sch) => {
      const members = rows.filter((r) => sch.members.includes(r.id));
      const best = members[0];
      return { label: sch.label, members: sch.members, s: best ? best.s : null,
        best: best ? best.id : null, order: best ? rank[best.id] : Infinity,
        counted: members.length };
    })
    .filter((sch) => sch.s !== null)
    .sort((a, b) => a.order - b.order);
  const unranked = bundle.thinkers
    .filter((t) => rank[t.id] === undefined)
    .map((t) => ({ id: t.id, name: t.name, shared: agree[t.id] ? agree[t.id].n : 0 }));

  // Top three, sharply weighted: the layout is non-linear, so a broad average lands in empty
  // space between schools (seen in the demo room's group placement).
  const top = rows.slice(0, 3);
  let wx = 0, wy = 0, wt = 0;
  for (const r of top) {
    const w = Math.exp(14 * (r.s - 0.5));
    wx += w * thinkers[r.id].x;
    wy += w * thinkers[r.id].y;
    wt += w;
  }
  const position = { x: wx / wt, y: wy / wt, approximate: true };

  const home = schools[0];
  const signature = [];
  for (const anchor of bundle.anchors) {
    const answer = answers[anchor.id];
    if (answer !== 1 && answer !== -1) continue;
    const entry = stancesA[anchor.id];
    const against = sideShare(entry, home.members, -answer);
    if (!against.count || against.share <= 0.5) continue;
    let best = null;
    for (const other of schools.slice(1)) {
      const withUser = sideShare(entry, other.members, answer);
      if (!withUser.count || withUser.share <= 0.5) continue;
      const strength = against.share * withUser.share * Math.min(withUser.on, 3);
      if (!best || strength > best.strength) {
        best = { anchor: anchor.id, text: anchor.text, answer, home: home.label,
          ally: other.label, strength, allies: other.members.filter((m) => entry[m] === answer) };
      }
    }
    if (best) signature.push(best);
  }
  signature.sort((a, b) => b.strength - a.strength || (a.anchor < b.anchor ? -1 : 1));

  const layerOf = Object.fromEntries(bundle.anchors.map((a) => [a.id, a.layer]));
  const camps = bundle.camps.map((camp) => {
    const byLayer = Object.fromEntries(LAYERS.map((l) => [l, [0, 0]]));
    for (const [anchor, answer] of Object.entries(answers)) {
      if ((answer !== 1 && answer !== -1) || !stancesA[anchor]) continue;
      const { side } = majority(stancesA[anchor], camp.members);
      if (!side) continue;
      byLayer[layerOf[anchor]][side === answer ? 0 : 1] += 1;
    }
    const agreed = LAYERS.reduce((t, l) => t + byLayer[l][0], 0);
    const opposed = LAYERS.reduce((t, l) => t + byLayer[l][1], 0);
    const deepest = LAYERS.find((l) => byLayer[l][1] > byLayer[l][0]) || null;
    return { id: camp.id, label: camp.label, byLayer, agreed, opposed, deepest };
  });

  return {
    status: "ok",
    answered,
    ranked: rows,
    nearest: rows.slice(0, 3),
    furthest: rows.slice(-3).reverse(),
    schools,
    position,
    signature: signature.slice(0, 3),
    camps,
    unranked,
  };
}

/** The teaser after each set: nearest and furthest school, without names. */
export function teaser(bundle, answers) {
  const stancesA = plainStances(bundle);
  const agree = agreement(answers, stancesA);
  const schools = bundle.schools
    .map((sch) => {
      const rs = sch.members.map((m) => agree[m]).filter((r) => r && r.n >= 2);
      return { label: sch.label, s: rs.length ? rs.reduce((t, r) => t + r.s, 0) / rs.length : null };
    })
    .filter((s) => s.s !== null)
    .sort((a, b) => b.s - a.s);
  if (schools.length < 2) return null;
  return { closer: schools[0].label, further: schools[schools.length - 1].label };
}

/** Story material: a quote from your top match, one from your furthest, and your rarest take. */
export function highlights(bundle, answers, result) {
  const textOf = Object.fromEntries(bundle.anchors.map((a) => [a.id, a]));
  const order = [...bundle.anchors].sort((a, b) => b.split_score - a.split_score);
  const quoteFor = (thinker, agree) => {
    for (const a of order) {
      const v = answers[a.id];
      const item = bundle.stances[a.id][thinker];
      if ((v !== 1 && v !== -1) || !item || !item.q) continue;
      if ((item.a === v) === agree) return { thinker, anchor: a.id, text: a.text, answer: v, ...item };
    }
    return null;
  };
  let rarest = null;
  for (const a of bundle.anchors) {
    const v = answers[a.id];
    if (v !== 1 && v !== -1) continue;
    const entries = Object.values(bundle.stances[a.id]);
    if (entries.length < 3) continue;
    const withYou = entries.filter((e) => e.a === v).length;
    const share = withYou / entries.length;
    if (!rarest || share < rarest.share || (share === rarest.share && entries.length > rarest.of)) {
      rarest = { anchor: a.id, text: textOf[a.id].text, answer: v, with: withYou, of: entries.length, share };
    }
  }
  return {
    topQuote: result.nearest[0] ? quoteFor(result.nearest[0].id, true) : null,
    farQuote: result.furthest[0] ? quoteFor(result.furthest[0].id, false) : null,
    rarest,
  };
}

/** The summary a published profile carries (checked and rebuilt by the server). */
export function profileSummary(result, rarest) {
  const pick = (t) => ({ id: t.id, k: t.k, n: t.n });
  return {
    home: result.schools[0].label,
    answered: result.answered,
    nearest: result.nearest.map(pick),
    furthest: result.furthest.map(pick),
    signature: result.signature.map((s) => ({ anchor: s.anchor, answer: s.answer, ally: s.ally })),
    camps: result.camps.map((c) => ({ id: c.id, agreed: c.agreed, opposed: c.opposed, deepest: c.deepest })),
    rarest: rarest ? { anchor: rarest.anchor, answer: rarest.answer } : null,
  };
}
