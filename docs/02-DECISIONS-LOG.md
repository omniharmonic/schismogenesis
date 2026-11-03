# Dialogos Arena: Decisions Log

*Benjamin Life (@omniharmonic) · current as of 2026-10-31*

This log records every decision made after the research synthesis was written, including those from voice design sessions that don't yet appear in the older documents. **Where documents conflict, use this order of precedence:**

1. `01-BUILD-SPEC-v1-SLICE-1.md` (locked 2026-10-31)
2. This decisions log
3. `design-spine/SPINE.md` (shared names, phases and interfaces, including §10 extensions)
4. `07-PRD.md`, `08-TECHNICAL-ARCHITECTURE.md` (+ `08a-APPENDIX-DDL-and-SCORER.md`) and `09-IMPLEMENTATION-PLAN.md`
5. `03-DESIGN-MEMO-2026-10-30.md`
6. `05-DATA-MODEL-and-ENCOUNTER-PLAN.md` and `06-LOCAL-COMPUTE-and-OPERATIONS.md`
7. `04-RESEARCH-SYNTHESIS.md` (its §2 lists the earlier design decisions D1–D22)
8. `research/` briefs (evidence only; their recommendations may be superseded)

---

## Decided on 2026-10-31 (after the synthesis, data model and compute plan)

### D-31.1 One unified metric: a public, Community-Notes-style reputation score
- **The score is the game itself, and it is explicit and visible.** People and agents both play for it.
- **Mechanics.** It is adapted from the Community Notes scorer: matrix factorization with a global mean, a rater intercept, a note intercept and viewpoint factors. The viewpoint dimension is the map's real clusters, not a single inferred left/right axis.
- **Contributions:** cross-cluster notes (describing another cluster), steelmen and syntheses.
- **Ratings:** helpful = 1, somewhat = 0.5, not helpful = 0.
- **Fidelity:** a description counts only when the *described* cluster rates it accurate ("signs it").
- **Portability:** raters from other clusters rate whether it is clarifying.
- **Writer reputation** rises when contributions reach ratified or helpful status, and falls when they reach not helpful.
- **Rater reputation** rises when ratings match final outcomes, which rewards honest rather than tribal rating.
- **Synthesis credit is retroactive, by lineage:** uptake by both parent clusters. A clean mutual disagreement and a better question are both valid outcomes.
- **Supersedes:** the synthesis's separate MOVE reward designs (D/A/B/C) and the Integration-Game objective *as the primary metric*. The mimetic state machine (state vector, regimes, lineage) remains as the analytics and tracking layer. The **understanding matrix** is now derived from the reputation system's ratified descriptions.

### D-31.2 The prediction market bets on reputation trajectories
- Participants back agent strategies (for example steelman-first vs. shared-question) by forecasting how those agents' reputation scores will change between specific cluster pairs over a set window.
- Outcomes are resolved by the same unified reputation metric. There is no separate referee or resolution oracle.
- Payouts are in reputation and prizes, never money. No tradable token for at least two years, and no per-agent tokens.
- **Supersedes:** the synthesis's separate randomized-strategy-tournament resolution design (§9.7–9.8).
- **Open (engineering), OD-08:** whether to randomize which strategy runs on which cluster pair, which the research says is needed for causal claims and for incentive-compatible forecasts. Recommended: yes, but keep it simple in Slice 1.

### D-31.3 Agents
- Agents are disclosed, registered on a public ledger and bound to a verified human operator. The Open Agent Charter (synthesis §8) stays in force.
- Agents earn reputation on **their own leaderboard** under the same metric, tied to their operator.
- **Agents never ratify.** Only people placed in a cluster through real statement reactions can ratify.
- **Directional-shift audit:** agents that consistently move people toward one view lose reward eligibility.
- Agent-touched inputs are flagged, and the map is re-fit without them before release.
- Platform rules are followed. For example, on X an agent may contact someone only after that person engages first.

### D-31.4 Extraction is claim-first and granular; question-first is rejected
- Full claim extraction and connection. Every claim carries an exact supporting quote, checked in code, plus an entailment check. Claims are normalized into a shared proposition bank, linked by relations, layer-tagged and linked back to the source clip.
- Question-first scoring (a fixed proposition bank scored by a cheap classifier) was considered and **rejected** for Slice 1, because accuracy matters more than cost at this scale.
- **Jev** (TypeSafe AI's classifier) is at most one contender for cheap labeling tasks, not the plan.

### D-31.5 Slice 1 scope
- **Niches:** rationalists, AI safety, accelerationists/e/acc, techno-optimists, and the terminally online subcultures connected to them (TPOT/post-rationalists, effective altruism, the tech right, degens/Milady-adjacent).
- **Candidate set:** see `seed/SLICE-1-LANDMARKS.md`. It has 8 core plus 7 recommended adjacent niches and 53 landmarks. The adjacent set is pending Benjamin's confirmation.
- Expansion to broader cultural niches happens only after Slice 1 passes its tests.

### D-31.6 Method bake-off on the slice
Three approaches are compared:
- Claude extraction, which serves as the gold standard and quality ceiling.
- Local open-model extraction on the Blackwell box.
- A cheap embedding/classifier baseline.

They are judged on:
- cluster validity by eye;
- landmark self-recognition ("would Eliezer and Beff both nod?");
- quote fidelity;
- cost and time.

The winner, or a combination, becomes production.

### D-31.7 Compute and budget
- No ~$5k cloud spend. The pipeline runs on Benjamin's 128 GB Blackwell box (GB10/DGX-Spark class), which arrives about a month after 2026-10-31.
- Claude (subscription) is used for gold labels, prompt design, audits (about 2%) and the weekly question battery only. It is not used for bulk extraction.
- **Transcripts:** YouTube captions are the primary source. Podcast RSS with local ASR, and landmark opt-in, are complements. YouTube's terms of service are a logged gray-area risk, not a blocker. Publish propositions with short quotes and timestamped links only, never full transcripts.
- Caption fetching at a polite pace is the slowest step (an estimated 3–6 weeks for the full seed), so start it before the box arrives.

### D-31.8 Seed map
- The current seed is **SEED-v4**: 234 niches across 9 domains, 817 landmarks, 72% verified-active and 53 mirror pairs. It supersedes v1–v3.
- **Niches** (curated hypotheses) stay separate from **clusters** (what the data finds), linked by a crosswalk.

---

### D-31.9 Slice 1 composition approved; e/acc strengthened; priority encounter
- **Approved (OD-05):** all 7 adjacent niches join the 8 core niches: agi-frontier-builders, ai-ethics-critics, dacc-pluralist-tech, forecasters-prediction-markets, populist-ai-backlash, neoreaction-vitalist-right, progress-studies-abundance.
- **e/acc roster strengthened:** add **bayeslord** (pseudonymous e/acc co-founder) as a core landmark, verification pending. Nick Land stays, unverified; Garry Tan stays as a booster voice.
- **Priority encounter PE-01 · e/acc × d/acc:** the P1 discovery crawl searches first for any recorded Beff Jezos × Vitalik Buterin conversation, then other e/acc ↔ d/acc exchanges. PE-01 is the leading candidate for the first event map (OD-23).
- **Disclosure:** Dario Amodei (Anthropic CEO) and Brad Carson (group reportedly Anthropic-funded) are on the map. Claude helped build it, so this relationship must be disclosed publicly alongside the collaborator COI disclosures (OD-02).

### D-31.10 Cloud-first until batch scale; light source storage; written works are first-class
Benjamin, 2026-10-31.
- **Infrastructure:** assume basic cloud infrastructure, operated by hand through Claude Code, until the larger batch operations move to self-hosted infrastructure (refined by D-31.11; spec §9 is amended). "No spend without asking" still applies.
- **Source storage:** strict private handling of transcripts is more than needed, since these are public conversations. Raw sources sit on plain disk behind a small interface, with no object-store service (ADR-030). MinIO is dropped: it stopped distributing free images. **Unchanged:** full texts are not republished; public output stays as short quotes and links.
- **Written works** (books, essays, blogs, letters, dissertations) are sources alongside spoken episodes, with the same claim, quote-anchor and entailment gates (ADR-030). This extends SPINE §1 and §2, which say "spoken" and "timestamped".
- **GitHub:** the repo is `omniharmonic/schismogenesis`, private, under the `omniharmonic` account. This replaces the `clawmniharmonic` instruction in Plan §2.4.
- **Open:** tilting the pilot toward the worldview-shaping thinkers is **OD-35**.

### D-31.11 Local compute, cloud data; Neon; extraction rules for written sources
Benjamin, 2026-10-31.
- **Neon Postgres** (project `schismogenesis`, free plan, `us-west-2`, Postgres 16) is the cloud database and system of record. Computing and inference stay local, and everything is pushed to the cloud. The spec's §9 is amended to match.
- The extraction rules in ADR-030 (voice, esoteric writing, co-authors, time, volume, language, lawful copies) are approved.

### D-31.12 Keep and add: a written-first worldview core (OD-35)
Benjamin, 2026-10-31.
- The 15 slice niches and existing landmarks stay. A **worldview core** of 11 goes first, written work first: Peter Thiel, Alex Karp, Curtis Yarvin, Nick Land, Sam Altman, Dario Amodei, Marc Andreessen, David Sacks, Elon Musk, JD Vance, Balaji Srinivasan.
- **Added to the slice:** Karp (new; not in SEED-v4, verification pending), Musk, Vance, Balaji. Counts are now 819 landmarks and 58 slice landmarks. Their primary niches (space, national conservatives, network states) stay outside the 15 slice niches.
- Deceased thinkers enter as lineage rather than placed landmarks. Critics and rival camps stay, since meta-consensus needs them.
- The Anthropic disclosure in D-31.9 applies with more force: Claude extracts claims from Anthropic's CEO.

### D-31.13 Compare through questions and positions (working direction)
Benjamin, 2026-11-01: "Probably a hybrid of positions and questions." Provisional until the first Slice 1 map tests it.
- **Claims** remain the verified evidence layer. Claim-first extraction (D-31.4) is unchanged.
- **Questions** are drawn from the claims after extraction and give authors a shared frame.
- **Positions** are shared, named answers to a question, each backed by quoted claims. A question can hold more than two. People can share a position for different reasons, and those reasons stay visible as separate claims.
- Clustering works from people's positions, not from exact claim matches. This extends SPINE §2 and S11, and the schema change follows once the design is tested.

### D-31.14 Definitions come from the people described
Benjamin, 2026-11-01. Position definitions are self-generated by people within each cultural niche once the system is bootstrapped. Models draft provisional wording only to start. D-31.13 stands as the direction. See ADR-032.

## Earlier decided (2026-10-30 design dialogue; full detail in `03-DESIGN-MEMO-2026-10-30.md` and synthesis §2)
- **Gradient:** how accurately each cluster can describe every other, in terms the described cluster would sign. Success is meta-consensus, not convergence.
- **The map is built from landmark content,** not the follow graph. Follows measure attention, not belief.
- **Individuals are placed by statement reactions** (Polis-like agree/disagree/pass). Placement defines cluster membership for ratification.
- **First 60 seconds:** react, appear as a dot, see the nearest landmarks, the threshold reveal, the twist card, then an invitation to describe the farthest cluster.
- **The live thread or question is the core UX object.** Axes are chosen per question. Feed rule: reciprocal opening (rank by what widens).
- **Time:** everything is timestamped. Nested horizons: daily pulse, weekly weather, monthly deep pass. Cluster lineages and a stable core landmark panel.
- **Event maps:** the extraction runs on any dialogue. Cross-cluster encounters become graph edges. Never-met pairs become invitations for Arena-hosted anti-debates.
- **Public figures** are placed from public output only, with a dispute/annotate affordance. No inference about private individuals who haven't opted in.

---

## Pending decisions (Benjamin)

**All pending decisions now live in [`10-OPEN-DECISIONS.md`](10-OPEN-DECISIONS.md)** (consolidated 2026-10-31): 35 items, OD-01 … OD-35, each with options, a recommendation, what it blocks and a needed-by date. That file merges this list with the open questions in the PRD, the Architecture and the Implementation Plan. When Benjamin decides one, record it here as a new D-entry and mark it decided there.

This log's earlier pending list maps as follows:

1. Exclusion review of the 15 flagged landmarks → **OD-01**
2. Conflict-of-interest sign-off (Samantha Power, Monty Bryant, Kevin Owocki, Griff Green; Brad Carson) → **OD-02**
3. Outside reviewers for 7 niches near Benjamin's own work → **OD-03**
4. Bridger rule → **OD-04**
5. Slice 1 adjacent niches → **OD-05** (needed by 2026-11-03)
6. Girard in public framing → **OD-06**
7. Jake Hartnell's hyperstition position → **OD-07**

The D-31.2 engineering question (randomized strategy assignment) is **OD-08**.

### D-31.15 Lifeworld Atlas direction
Benjamin, 2026-11-01: a thinker is a shape rooted in shared ground, not a dot ("this sounds great, let's fully document the plan and then implement it"). AI futures is the first region, with 14 people added from Slice 1. See the design in `docs/superpowers/specs/2026-11-01-lifeworld-atlas-design.md` and ADR-035. The builder's calls listed there await his review.

### D-31.16 AI Futures Fingerprint for the TPOT conversation
Benjamin, 2026-11-02: "let's produce a scoped implementation plan… scope it to appeal to the EA / e/acc / d/acc TPOT subcultures who will be our early adopters… nail the fingerprint… best in class meme map, real polis-style community note infra… let's not do full citizen assembly scale public deliberation to start." Design and plan: `docs/fingerprint/` and ADR-036. The builder's calls (anchor rule, thresholds, on-device scoring, new room tables) await his review.

### D-31.17 Launch round: Wrapped story, public profiles, production readiness
Benjamin, 2026-11-02: "make it even more robust to prep for a real launch… a serious thinkers version of spotify wrapped… allow someone to publish their profile to the site if they want? anonymous or with their twitter/bsky handle / pfp?… get ready to ship it to production." Plan and builder's calls: `docs/fingerprint/04-LAUNCH.md`. Calls awaiting his review:
- unverified handles are never shown;
- result-only profiles get a scrambled print;
- one live profile per verified account;
- a bridge now also needs its bootstrapped lower bound of 0.65 or more.
Deployment waits on his choice of host and domain.

### D-31.18 Atlas expansion: voices approved, Vercel and Neon, bot protection, slant review
Benjamin, 2026-11-03: "deeper on the statements. voices approved. keep widening. vercel and neon. bot protection is good. blind slant review is needed. keep digging deeper. let's make this robust."
- The 29 candidate voices in `seed/drafts/ATLAS-EXPANSION-CANDIDATES.md` are approved. 18 are new to the seed and 11 were already seed landmarks.
- Conflicts of interest stay disclosed in each record's `conflict_note` and on the About page: Jack Clark (Anthropic co-founder), and possible ones for Divya Siddarth and Anton Korinek.
- Hosting is Vercel with Neon.
- Cloudflare Turnstile is on for bot protection.
- A blind slant review of the 24 statements comes before launch.

### D-31.19 Iron-clad stances: a full-text audit, and schools decided by outlook
Benjamin, 2026-11-03: "we need the stances to be iron clad. please use a swarm to validate all of the claims and make sure the atlas is fully documented with rich, high quality statements from all of the figures. Kingsnorth is OBVIOUSLY not a builder. We may need some additional categories but this is an obvious mismatch."
- **Every stance on the 24 statements is re-read from the full source texts** (protocol `stance_audit_v1`). Two blind readers per thinker cover all 54. A stance is published only if two independent readings support it: both blind readers, or one reader plus a third who checks the passage in context (`stance_adjudicate_v1`). Code checks every quote verbatim against the source. The audited set (`seed/season-1-stances.json`) replaces all older stances on the statements.
- **Each thinker gets signature positions in their own words** (`seed/thinker-voices.json`). They are shown first on the thinker's card.
- **Why Kingsnorth landed among the Builders:**
  - one lament ("the Machine… will consume and colonise everything") was read as three positions, including technological fatalism;
  - his agreement with Altman was all forecasts (AI is transformative, unstoppable, risky), while on values they disagree;
  - the atlas had no school for a religious and ecological critique of technology.
- **Fixes:**
  - forecasts count half in placement;
  - a neighbour can only bring a voice into a school if they share at least two positions on values, action or what AI is;
  - a voice with no such neighbour is shown as "not yet grouped", not forced into a school.
  New schools may come from that group in season 2.
- **Sources found not to be the person's own words are excluded at the root** (seed `exclude`). The first two:
  - Andy Hall's guest essay filed under Jason Crawford (32 claims);
  - a third-party summary filed under Balaji Srinivasan.
