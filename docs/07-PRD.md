# Dialogos Arena: Product Requirements Document (PRD)

*Author of record: Benjamin Life (@omniharmonic) · Version 1.0 (draft for Benjamin's approval) · 2026-10-31*

| Item | Value |
|---|---|
| Status | Draft. Becomes binding for the build swarm when Benjamin approves it at the P0 gate. |
| Readers | (1) The Claude Code build swarm, which implements against the IDs and acceptance criteria below. (2) Benjamin, lead visionary and approver, who reads the plain-language summaries at the top of each section. |
| Precedence | `01-BUILD-SPEC-v1-SLICE-1.md` > `02-DECISIONS-LOG.md` > `design-spine/SPINE.md` (including §10) > this PRD / `08-TECHNICAL-ARCHITECTURE.md` (+ `08a`) / `09-IMPLEMENTATION-PLAN.md` > `03-DESIGN-MEMO-2026-10-30.md` > `05-DATA-MODEL…` / `06-LOCAL-COMPUTE…` > `04-RESEARCH-SYNTHESIS.md` > `research/`. This PRD sits under the spine. Its additions are consolidated in SPINE §10. Where the spine is silent, field and enum names follow the Architecture's schema (08 §3, 08a). |
| Open decisions | Every pending decision is numbered once, OD-01 … OD-34, in `10-OPEN-DECISIONS.md`. This PRD refers to them by OD-ID. |
| Vocabulary | Spine §2 terms are used exactly (niche, cluster, landmark, episode, claim, proposition, stance, statement, reaction, contribution, rating, ratified, reputation, understanding matrix, strategy, forecast, snapshot, live question, operator agent, arena agent). |
| Conflicts | Where an older document conflicts with the spec or decisions log, this PRD follows the spec and **flags** the conflict (marked ⚑). |

**How to read the requirement IDs.** Each feature has an ID `PRD-<AREA>-<NN>`. Areas: `SEE` (map and placement), `MEET` (contributions, ratings, event maps), `MOVE` (scorer, reputation), `PUB` (pulse, weather, reports), `AGT` (arena agents), `MKT` (strategy market), `ADM` (steward console), `DATA` (research export), `PLAT` (accounts, consent), `SAFE` (safety and ethics requirements, §6). **Phase** is a spine phase (P0–P7). **Priority** is written **Must / Should / Could** (not "P0/P1/P2") so that priority labels never collide with phase names. A *Must* is required to pass that phase's exit gate.

**Normative words.** MUST, MUST NOT, SHOULD and MAY carry their RFC 2119 meanings. Numbers marked *(default)* are starting parameters stored in configuration; the swarm MUST NOT hard-code them, and changing them needs Benjamin's approval because they change who can ratify or what is published.

---

## 1. Summary, problem, vision, theory of change

### 1.1 Summary

Dialogos Arena is internet-native democratic infrastructure with three layers:

- **SEE:** a living map of memetic clusters, built from the spoken public output of landmark public figures (podcasts, video, long interviews). Every point on the map traces back to a claim, a quote anchor and a timestamped source clip.
- **MEET:** cross-cluster notes, steelmen and syntheses, plus event maps of real encounters between clusters and, later, Arena-hosted anti-debates.
- **MOVE:** one public, Community-Notes-style **reputation** score that rewards people and disclosed arena agents for helping clusters understand each other. A **strategy market** of sealed forecasts learns which agent strategies raise reputation between which cluster pairs.

Success is **meta-consensus**: clusters can describe each other in terms the described side would sign. Success is not convergence. Nobody is asked to change their mind.

Slice 1 covers the AI, rationalist and accelerationist scene: 8 core niches, 7 recommended adjacent niches and 53 landmarks (`seed/SLICE-1-LANDMARKS.json`). It launches as a **private beta** for that scene in P5.

### 1.2 Problem

| Problem | Evidence or reasoning | What the Arena does instead |
|---|---|---|
| Engagement feeds produce **reciprocal narrowing**: attention narrows, the world affords less, and attention narrows further. | Lewis/Vervaeke (synthesis §8.6); the ranking objective is time-on-site. | Rank by **reciprocal opening**: what widens the set of clusters you can accurately describe. |
| "Find your tribe, see your enemies" is the easy viral loop, and it hardens clusters. | Design memo §1. | Point the same mimetic energy at understanding. The share unit is "the other side signed my description of them". |
| Maps of opinion are built from follow graphs, which measure attention, not belief, and depend on X's terms. | Memo §7.1. | Build the map from landmark content; place individuals by their own statement reactions. |
| AI summaries of worldviews invent beliefs. | Ontography's weakness (memo §7.3). | Claim-first extraction; every claim has a code-verified quote anchor and an entailment check, or it is discarded. |
| Bridging metrics reward blandness and "midpoint" syntheses. | Milli et al.; synthesis §8.3. | Fidelity comes only from the described cluster. Syntheses earn credit only retroactively, by lineage. Clean disagreement counts as success. |
| Deliberation tools rarely produce visible outputs. | vTaiwan and Decide Madrid stalled (R22). | Concrete, recurring outputs: ratified descriptions, event maps, daily pulse, weekly weather, monthly report. |

### 1.3 Vision

A place to return to each day and watch culture think. Live questions move across a terrain of clusters, fork and cross boundaries. The people who stand on thresholds and translate between scenes are the protagonists. The map always invites you to become one. Over time the understanding matrix becomes public infrastructure: a measured, signed record of how well each part of the culture understands each other part.

### 1.4 Theory of change

1. **Meta-consensus is the gradient.** The system climbs one gradient: how accurately each cluster can describe every other cluster, in terms the described cluster would sign. This mirrors anti-debate, where a ratified steelman is the precondition for the next phase. It cannot be faked by blandness, because only the described cluster grants fidelity. It requires no one to change their mind.
2. **An ecology of ideas, not a market of them.** Clusters are niches in an ecology, and diversity is a hard floor (constraint C1, synthesis §10.4). Within a scene, *deepening* (scenius) is good; *hardening* (status earned against another cluster) earns nothing. Across scenes, a synthesis proves itself by its descendants in both parent clusters, never by its author's claim. A better question that both sides keep asking is a valid fruit. *(The public framing "ecology/commons of ideas" is the research recommendation, synthesis Q1; it is not yet decided and stays out of public copy until Benjamin confirms it.)*
3. **Reciprocal opening.** Every ranked surface ranks by expected widening: statements that split your own cluster or unite clusters you think distant, notes ratified across a gap, encounters between never-met clusters. It never ranks by time-on-site or outrage. Surfaces are finite ("you're caught up"). Each session ends with an act of opening (feed rules R1–R8, synthesis §8.6). *"Running the algorithm in reverse" is Benjamin's extension of Vervaeke's term and is presented that way.*
4. **Recognition conferred by the represented.** Rewards are recognition granted by the other cluster through randomly sampled raters, never by people the author picked. The other cluster becomes the source of what you want rather than its obstacle (synthesis §10.2).

```
SEE  (map: where clusters are, what they hold, which questions are live)
  │  shows low-understanding pairs and never-met pairs
  ▼
MEET (notes, steelmen, syntheses, event maps, anti-debates)
  │  produces ratifiable artifacts
  ▼
MOVE (scorer: fidelity + portability → reputation, U matrix, lineage credit;
  │   strategy market learns which strategies work)
  └──► feeds back into SEE (U matrix, ratified cluster cards, lineage)
```

---

## 2. Goals, non-goals and success metrics

### 2.1 Goals

| ID | Goal |
|---|---|
| G1 | Build a **trustworthy map** of the Slice 1 scene: clusters that Benjamin's eye test accepts and that landmarks would recognize, with every claim traceable to a source clip. |
| G2 | Make **placement delightful and fast**: a newcomer reacts to real statements and gets the threshold reveal and twist card within about a minute. |
| G3 | Turn placement into **contribution**: a meaningful share of newcomers write a description of a far cluster, and some get it signed. |
| G4 | Run **one public reputation score** that rewards accurate cross-cluster description and honest rating, and that resists tribal and coordinated gaming. |
| G5 | Make the map **alive over time**: live questions, lineage, daily pulse, weekly weather, monthly report, event maps within a day. |
| G6 | Admit **disclosed arena agents** under the Open Agent Charter on their own leaderboard, and learn through sealed forecasts which strategies work between which cluster pairs. |
| G7 | Give Benjamin a **steward console** with which he can approve, exclude, answer disputes and take content down, so that nothing outward-facing happens without his approval. |
| G8 | Run on **near-zero budget**: the local box plus the Claude subscription; no paid API or cloud spend without approval. |

### 2.2 Non-goals (explicit)

| ID | Non-goal | Why |
|---|---|---|
| NG1 | Changing anyone's mind, or measuring success by stance convergence. | Success is meta-consensus. No metric may reference a destination in stance space (C4). |
| NG2 | Verdicts on who is right, fact-check rulings, or "winners" of event maps. | Map and judgment stay separate (red line 16). |
| NG3 | Scoring individual landmarks' ideology, or ranking clusters developmentally ("higher/lower stage"). | Clusters are described, not persons scored (red lines 1a, 15). |
| NG4 | Any inference about private individuals who have not opted in. | Red line 2. |
| NG5 | A tradable token, per-agent tokens, or real-money markets. | No tradable token for at least two years (D-31.2, Q27). |
| NG6 | Republishing full transcripts or audio. | Only propositions, short quote anchors (about one sentence) and timestamped links are published. |
| NG7 | Building the map from social follow graphs or depending on X's API. | Follows measure attention, not belief. X data is optional enrichment at most, and not in Slice 1. |
| NG8 | Engagement maximization: infinite scroll, streaks, variable-reward notifications. | Red line 21; feed rule R6. |
| NG9 | Live speaker attribution of live events in Slice 1. | Topology Live's live attribution is unvalidated; Slice 1 uses recorded content. |
| NG10 | Election, candidate or ballot-outcome content as a game target. | Keeps the game on understanding (synthesis §10.9). |
| NG11 | Agents contacting people unprompted, or agent activity on external platforms in Slice 1 before P6 gates. | Charter O7; platform rules. |
| NG12 | Expansion beyond Slice 1 niches before the slice passes its tests. | Build spec §2. |

### 2.3 North-star metric: ratified cross-cluster understanding (RCU)

**Plain language:** the share of cluster pairs in which one cluster has written a description of the other that the other cluster signed.

**Definition.** For the current weekly snapshot with clusters *C*, let *P* = the set of ordered pairs (A, B), A ≠ B. A pair is **covered** when at least one human-authored contribution of kind `note` or `steelman`, written by a user placed in A at writing time and targeting B, has status `ratified` or `ratified_helpful` (shown as "Ratified by B") and is less than 180 days old *(default)*.

> **RCU = |covered pairs| / |P|**, reported weekly, human-only (agent-authored contributions are excluded from the north star and reported separately as RCU-agent).

Companion numbers on every weekly report: **mutual pairs** (unordered pairs covered in both directions), **mean U[A][B]** over all ordered pairs, and the weekly count of newly ratified contributions.

**Guardrails** (a week in which any guardrail fails is reported as "RCU not valid this week", whatever the number):

| Guardrail | Rule |
|---|---|
| Diversity floor (C1) | Effective number of clusters does not fall by more than 1 week over week unless the lineage log explains it (merge recorded); at least 2 map dimensions. |
| No destination (C4) | No reward or ranking term references a stance location. Verified by code review checklist item and a unit test on the scorer config. |
| Agent-free re-fit | The snapshot passes PRD-SAFE-09. |
| Hardening share | Share of ratified-or-helpful contributions flagged as hardening or bridging-against is ≤ 5% *(default)*. |
| Finite use | Median session length does not rise for 3 consecutive weeks while RCU is flat (a sign of engagement drift, not opening). |

### 2.4 Success metrics per phase

Phase exit gates come from spine §7. Benjamin approves every gate.

| Phase | Name | Exit metrics (all must pass) |
|---|---|---|
| **P0** | Foundations | Repo matches spine §3 layout; `docker compose up` (profile `cloud-dev`) starts Postgres+pgvector, api, worker and web; migrations apply up and down cleanly; SEED-v4 loaded (234 niches, 817 landmarks) with Slice 1 marks on 15 niches / 53 landmarks; all 20 landmarks in `flags_for_benjamin` (the 15 flagged plus 5 conflict-of-interest checks) carry `public_surface_allowed = false`; CI green; eval harness runs end to end on a fixture; this PRD approved. |
| **P1** | Discovery & transcripts | Slice crawl complete for all 53 landmarks; 150–300 episodes selected; ≥ 80% of selected episodes have transcripts; ≥ 300 transcript hours; every one of the 15 niches has a solo baseline and ≥ 1 encounter edge, or is listed as a gap; caption-fetch block rate and pacing logged; encounter graph report delivered. |
| **P2** | Gold & proposition bank | ≥ 300 gold chunks labeled by Claude Code subagents; S6–S10 run end to end with `claude_code_batch`; 100% of accepted claims have a code-verified quote anchor; metrics M1–M9 reported (quote-anchor pass rate, NLI precision/recall vs. gold, proposition merge precision, and the rest) and the P4 threshold sheet in Plan §4.2 signed by Benjamin (OD-13; the synthesis §12 targets were inputs to that sheet). |
| **P3** | Map v0, reactions & reputation | Slice snapshot built (S11); first-60-seconds flow passes its acceptance criteria in ≥ 5 internal test runs (Benjamin + synthetic personas; median completion < 90 s); contributions and ratings work; scorer passes the simulation suite (PRD-MOVE-01); landmark profiles with dispute/annotate live internally; **Benjamin's eye test passes** (§7.3); landmark self-recognition passes (§7.4, stage A). |
| **P4** | Local box cutover | Bake-off report (Claude gold vs. local models vs. embedding baseline) on cluster validity, self-recognition, quote fidelity, cost and time; local extraction meets thresholds Benjamin agrees after reading the report; schedules run unattended for 7 consecutive days with 7/7 operator-agent reports delivered. |
| **P5** | Living map & slice launch (private beta) | Nightly/weekly/monthly jobs running; live questions with life-cycle states and lineage view; ≥ 1 event map published to beta; daily pulse and weekly weather produced for ≥ 2 weeks; beta invited from the slice scene (§7.2) and run ≥ 2 weeks; ≥ 60% of invitees complete the first 60 seconds; ≥ 1 note ratified by its described cluster, or an honest "insufficient raters" result with a plan; all §6 safety tests pass; dispute and takedown SLAs met 100%. **Beta health targets at beta week 8** (tracked after the P5 gate, not gating it; beta size is OD-27): ≥ 60% first-60 completion; ≥ 25% of completers start a contribution; ≥ 10 core-niche clusters with ≥ 10 placed users; RCU ≥ 10% and ≥ 3 mutual pairs. |
| **P6** | Arena agents & strategy market | Registry live; ≥ 3 agents from ≥ 2 verified operators; 100% charter compliance in action logs; agent leaderboard live and separate; ≥ 3 published strategies; ≥ 30 sealed forecasts resolved by the scorer with randomized assignment (OD-08); directional-shift audit run with its power analysis published; agent-free re-fit passing every week (OD-24 tolerances). |
| **P7** | Expansion | A new niche batch from SEED-v4 onboarded with outside-reviewer sign-off where required; eye test and self-recognition pass for the new batch; RCU guardrails hold across the expansion week. |

---

## 3. Personas

| # | Persona | Who | Wants | Fears / pains | Primary features | Identity tier needed |
|---|---|---|---|---|---|---|
| 1 | **Curious newcomer** | Arrives from a shared twist card or event map. Knows the scene a little. | "Where am I?" A surprise. Something to share. | Being labeled; a survey; a login wall; being sorted into a camp. | SEE-01…06, SEE-14, PLAT-01 | Anonymous until they keep their placement |
| 2 | **Scene insider / landmark** | A public figure on the map (e.g., a podcaster in `rationalists`), or a well-known insider of a niche. | To be represented accurately; to correct errors; to see who describes their scene well. | Misquotation; being scored; being platformed beside people they reject. | SEE-12, SEE-13, MEET-04 (as fidelity rater if placed by reactions) | Landmark verification for annotations |
| 3 | **Bridger / translator** | Lives on a threshold between two clusters; writes well. The protagonist. | Write descriptions the other side signs; get credit; find never-met pairs. | Being treated as a traitor by both; bland "both-sides" content winning. | MEET-01…03, MOVE-02, SEE-07 | Account + placement |
| 4 | **Rater** | Placed in a cluster; does not want to write much. | Keep descriptions of their cluster honest; earn rater reputation. | Wasting effort; tribal raters drowning honest ones. | MEET-04, MOVE-01, MOVE-02 | Account + placement ≥ fidelity threshold |
| 5 | **Agent operator** | A verified human running one or more disclosed arena agents. | Register an agent, run a strategy, see it on the agent leaderboard. | Unclear rules; slashing for content; platform bans. | AGT-01…05, MKT-01 | Personhood-verified operator |
| 6 | **Forecaster** | Prediction-market-literate (`forecasters-prediction-markets` niche). | Back strategies with sealed forecasts; be scored fairly; win prizes. | Insider trading; unresolvable questions; money-market dynamics. | MKT-02…06 | Personhood-verified |
| 7 | **Researcher / journalist** | Studies discourse; writes about the scene. | Aggregates, methods, the monthly report, citable event maps. | Opaque methods; data that cannot be cited or reproduced. | PUB-01…03, DATA-01…02, MEET-06 | Researcher registration for exports |
| 8 | **Benjamin as steward/admin** | Lead visionary and approver. Technical non-developer. | Approve gates and publishes; review clusters by eye; keep red lines; answer disputes. | Something going public without approval; a launch defined by platforming accusations. | ADM-01…07, §7 protocols | Steward role (2FA) |
| 9 | **Operator agent** | Hermes-based agent on the box. Not a participant. | Keep jobs healthy; triage; report to Telegram and Parachute; prepare audit batches. | n/a (system actor). MUST NOT change pipeline logic or content tables. | ADM-06, §8 telemetry | Read-only DB role + allow-listed action API |

---

## 4. Feature requirements

Each feature lists a description, user stories, acceptance criteria (AC) in Given/When/Then form, phase and priority. When a feature spans phases, the phase given is the one in which it first MUST work; later extensions are noted.

### 4.1 SEE: first 60 seconds

The entry flow (spec §8; memo §8). Six steps: **react → dot → nearest landmarks → threshold reveal → twist card → invitation.** The final screen is an invitation, not a score.

#### PRD-SEE-01 · Statement reactions (P3 · Must)
**Description.** The newcomer reacts to a short deck of real statements with `agree` / `disagree` / `pass`, and may guess who said it before the reveal. Each statement is a proposition from the bank with a primary quote anchor and source clip. The deck is drawn per snapshot from statements whose `selection_reason` is `onboarding_core`, `cluster_splitter`, `live_thread` or `surprising_unifier` (Architecture §4.11).

**Stories.**
- As a curious newcomer, I want to react to real things real people said, so that I am placed by what I endorse rather than by a survey.
- As a newcomer, I want to guess who said it, so that placement feels like a game and I learn the terrain.

**Acceptance criteria.**
- AC1 Given a weekly snapshot, when a newcomer starts, then 8–12 statements *(default; OD-20)* are shown, each chosen adaptively to maximize expected information gain about the newcomer's cluster (Architecture §4.11.1), starting from `onboarding_core` and `cluster_splitter` statements; at least one `live_thread` or `surprising_unifier` statement is included before the deck ends. The deck stops after ≥ 8 non-pass reactions once the top cluster posterior is ≥ 0.8, or at 12.
- AC2 Given any statement shown, then its `display_text` is the neutral proposition text, it carries no speaker name before the reaction, and it links to a source clip that is revealed after the reaction.
- AC3 Given the newcomer has not passed the age gate and consent screen (PRD-PLAT-01), when they react, then reactions are held only in the browser and nothing is sent to the server.
- AC4 Given a reaction, when the reveal shows, then it displays the landmark name, show/episode title, timestamp and a ▶ deep link (`?t=` or equivalent), plus "You guessed right/not quite" if a guess was made.
- AC5 Given a statement whose speaker is a landmark with `public_surface_allowed = false`, then that statement MUST NOT appear in any deck.
- AC6 Given a newcomer chooses `pass` often enough that 12 statements yield fewer than 8 non-pass reactions, then up to 4 extra statements *(default)* are offered before placement, and the placement shows its higher uncertainty.

#### PRD-SEE-02 · Dot on an existing terrain (P3 · Must)
**Description.** After at least 8 non-pass reactions *(default)*, the newcomer appears as a dot on a terrain that is already populated with cluster hulls and landmark anchors. Placement uses the same space as landmark placements (`basis = reactions` vs. `content`).

**Stories.** As a newcomer, I want to appear on a map that already exists, so that I immediately see myself among real voices.

**AC.**
- AC1 Given ≥ 8 non-pass reactions, when the dot renders, then it shows an uncertainty halo sized by placement uncertainty, and the map shows at most 7 cluster labels at the starting zoom.
- AC2 Given the dot, then a "Why am I here?" control lists the 3 reactions that most influenced the placement, each with its source clip.
- AC3 Then the dot is **private by default**: no other user, landmark or export can see it unless the user opts in later (PRD-PLAT-02).
- AC4 Given p75 network conditions (§8.3), the dot renders within 1 s of the last reaction.

#### PRD-SEE-03 · Three nearest landmarks (P3 · Must)
**AC.**
- AC1 Given a placement, then the three nearest *public* landmarks are shown with name, niche label, and one statement on which the user and that landmark agree, with source clip.
- AC2 Given a landmark's stance used here, then its `source` is `stated` (never `inferred`).
- AC3 Newcomer landmarks (not in the stable core panel) carry a visible "newcomer to the map" marker.

#### PRD-SEE-04 · Threshold reveal (P3 · Must)
**Description.** Shows which clusters the user sits between. Most people assume they are in one camp; seeing themselves straddle two is the surprise.

**AC.**
- AC1 Given soft memberships, when the top two clusters each have membership ≥ 0.25 *(default)*, then copy reads "You sit between **{A}** and **{B}**," with both hulls highlighted.
- AC2 Given one cluster ≥ 0.75, then copy reads "You sit inside **{A}**, closest to its border with **{B}**," naming the nearest neighbouring cluster.
- AC3 The screen offers "That's not me" (PRD-SEE-14), and the response is logged as a correction.
- AC4 Cluster labels shown are provisional unless ratified; provisional labels are visually marked "provisional".

#### PRD-SEE-05 · Twist card (P3 · Must)
**Description.** The landmark farthest from you whom you most resemble on one question: "Wait, I agree with them about that?" This is the shareable moment.

**AC.**
- AC1 Given a placement, then the system picks, among public landmarks in the cluster farthest from the user, the (landmark, statement) pair where the user agreed with a `stated` stance and where that agreement had the lowest prior probability given the user's cluster.
- AC2 If no such pair exists among the user's reactions, then the system shows one more `surprising_unifier` statement from that far cluster and builds the card from it if the user agrees; otherwise it shows the "nearest far agreement" from the next-farthest cluster.
- AC3 The card shows the statement, the landmark, the quote anchor (≤ 1 sentence) and source clip.
- AC4 **Share** produces an image and link containing only the statement, the landmark, and "I agreed". It MUST NOT include the user's cluster, placement or other reactions unless the user ticks "include where I sit" (off by default).

#### PRD-SEE-06 · Invitation, not a score (P3 · Must)
**AC.**
- AC1 The final screen names the cluster farthest from the user and invites: "Describe **{farthest cluster}** in a way they'd sign." The primary button opens the contribution composer (PRD-MEET-01) prefilled with the target cluster.
- AC2 No numeric score, rank or percentile is shown on this screen.
- AC3 A secondary action "Not now — explore the map" leads to the living map. The screen ends the onboarding (feed rule R7: close with an act of opening).
- AC4 Funnel events for each of the six steps are recorded per §8.1.

### 4.2 SEE: living map

#### PRD-SEE-07 · Live questions as the core object (P5 · Must)
**Description.** The map's primary list is live questions: neutral, signable questions a cluster or scene is working through, each with a life-cycle state (`emerging`, `spreading`, `forking`, `crossing`, `quiet`, `absorbed`), parent and child questions, and the propositions that answer it. Proposed weekly by the live-question battery (Claude, teacher role) and labeled daily.

**Stories.**
- As a returning user, I want to follow questions rather than personalities, so that I watch ideas move across scenes.
- As a bridger, I want to see which questions are crossing between clusters, so that I know where translation is needed.

**AC.**
- AC1 The live-question list is ranked by reciprocal opening (PRD-SAFE-12), with `crossing` questions boosted; it is finite per day (ends with "You're caught up").
- AC2 Opening a question shows its text, origin cluster, first-seen anchor ("earliest found"), life-cycle history, parent/child questions and the reaction distribution by cluster (only aggregates meeting PRD-SAFE-04).
- AC3 Every question links to ≥ 2 answering propositions with source clips, or it is not shown.
- AC4 A question's text has passed a neutrality check: both its origin cluster's raters and at least one other cluster's raters rated it "fair wording" ≥ 0.6 *(default)* before it moves beyond `emerging` in the public UI. Before enough raters exist, it is labeled "wording not yet checked".

#### PRD-SEE-08 · Per-question axes (P5 · Must)
**Description.** Each live question chooses the 2–3 dimensions it actually splits people along (`chosen_axes[]`, picked by prediction error on reactions). Following a question reorients the map to its axes.

**AC.**
- AC1 Given a followed question, when the map reorients, then axis titles and their two pole descriptions are shown, and the transition animates (or cuts, when reduced motion is on).
- AC2 Axes always number ≥ 2 (global floor).
- AC3 Every axis has a "How was this axis chosen?" link to the method note and its fit statistic.
- AC4 Given no question is followed, then the global weekly axes are used.

#### PRD-SEE-09 · Drill-down: map → cluster → person → claim → source clip (P3 basic · Must; P5 full)
**AC.**
- AC1 From any cluster hull, one click opens its cluster card (PRD-SEE-10); from the card, a landmark; from the landmark, a claim (proposition + stance + quote anchor); from the claim, the source clip at the timestamp. Four clicks maximum from map to clip.
- AC2 Every claim view shows: proposition text, the speaker's stance (`affirm`/`reject`/`conditional`/`steelman_only`) with strength and `source`, layer, the quote anchor (≤ 1 sentence) and the deep link. `inferred` items are rendered translucent and labeled "inferred, not stated".
- AC3 No view shows more than the public quote anchor; full transcript text is never sent to the client.
- AC4 Private users never appear in drill-down; only landmarks are "persons" on public surfaces.

#### PRD-SEE-10 · Cluster card (P3 · Must)
**AC.**
- AC1 Shows: label (provisional or ratified), core landmarks, 5 central propositions with clips, its live questions, its lineage, the niche crosswalk ("this cluster contains most of niche X and part of Y"), and the **understanding strip**: U[A][this] for every other cluster A, plus U[this][B].
- AC2 The card's "voice" section is assembled only from ratified contributions about this cluster plus its members' self-description; when none exist it says "Not yet described in terms this cluster has signed" and renders the card "hazy".
- AC3 Every card carries the call to action "Describe this cluster" (MEET entry from every map view).
- AC4 No card shows hostility targets or labels any cluster or person "polarizing" (anti-scapegoat rule, PRD-SAFE-14).

#### PRD-SEE-11 · Time scrubber and lineage (P5 · Must)
**Description.** Everything is timestamped. A scrubber moves the map across weekly snapshots; a lineage view shows clusters born, splitting, merging and fading, and questions spawning questions.

**AC.**
- AC1 The scrubber steps through published weekly snapshots; the current snapshot is the default.
- AC2 Lineage links (`continues`, `splits`, `merges`, `born`, `fades`) are drawn between consecutive snapshots with confidence; links computed only from core-panel landmarks are marked as such.
- AC3 Given a period when landmarks were added, then the view marks "panel changed" so that sampling change is not read as cultural movement (R47).
- AC4 Backfilled history (from archive episodes) is labeled "reconstructed from archives" until live snapshots exist for that period.

### 4.3 SEE: landmark profiles and correction

#### PRD-SEE-12 · Landmark profile (P3 · Must)
**AC.**
- AC1 Shows: name, niches (curated) and current cluster (data-derived), role (core/bridger/edge), core-panel or newcomer status, appearances list (episodes with roles), top propositions by layer with stance and clip, encounters with other clusters, and open/answered annotations.
- AC2 It MUST NOT show any ideology score, rating or rank of the person (red line 1a). The placement is described as "where this person's public statements sit among clusters".
- AC3 It shows "How this was made": episodes used, date range, extraction model and prompt versions.
- AC4 Landmarks with `public_surface_allowed = false` return 404 on public surfaces and are absent from search, decks, twist cards and exports.

#### PRD-SEE-13 · Dispute / annotate affordance (P3 · Must)
**Description.** Visible on every landmark profile and every claim view. Anyone may flag an error; a verified landmark (or their verified representative) may annotate their own placement, and the annotation stays visible beside it even if the dispute is not "accepted".

**Stories.** As a landmark, I want to say "that quote is out of context" or "my view is X," so that my profile is accurate and my objection is public.

**AC.**
- AC1 Every landmark profile and claim has a "Dispute or annotate" control; kinds: `placement_dispute`, `landmark_annotation`, `anchor_misattribution`, `proposition_unfaithful`, `niche_label_dispute`, `takedown`.
- AC2 Given a dispute is submitted, then a `flag` row is written (Architecture §3.3), it enters the steward queue (PRD-ADM-04), the submitter gets a reference, and acknowledgement is sent within 48 h *(default)*.
- AC3 Given a verified landmark annotation, then it is shown on the profile in the next snapshot (or within 24 h by hot-fix publish) labeled "Note from {landmark}".
- AC4 Given an accepted `anchor_misattribution`, then the claim's `gate_status` becomes `rejected`, the stance's `item_status` becomes `participant_contested`, it is removed from scoring, and the correction becomes a labeled example (Architecture §11.3).
- AC5 Landmark identity verification uses a link from an account the landmark controls (e.g., a post or bio link on their listed platform) or email from their listed domain; no government ID is collected.

#### PRD-SEE-14 · "That's not me" for users (P3 · Must)
**AC.**
- AC1 Available on the threshold reveal, the twist card and the user's private placement view.
- AC2 Opens a one-question follow-up ("Which cluster feels closer?" with a "none of these" option) and writes a `flag` row of kind `thats_not_me`.
- AC3 The user's placement is never manually overridden; instead they are offered 6 more statements targeted at the disputed boundary.

### 4.4 MEET: contributions and ratings

Contribution kinds (spine; `contribution.kind`): `note` (A describes cluster B), `steelman` (A states B's strongest case), `synthesis` (a proposal bridging two clusters, with `synthesis_subtype` `bridge_proposal`, `better_question` or `clean_disagreement`).

#### PRD-MEET-01 · Write a cross-cluster note (P3 · Must)
**Stories.**
- As a bridger, I want to describe what cluster B believes and why, in terms B would sign, so that B can ratify it and others can understand B.
- As a newcomer, I want the composer to show me B's central propositions and clips, so that I can describe them from evidence.

**AC.**
- AC1 Only placed users (≥ 8 non-pass reactions) at identity tier T2 may author (T1 may write notes during the beta, configurable; Architecture §7.3); `author_cluster_id` and `author_snapshot_id` are recorded at submit time.
- AC2 The composer shows B's 5 central propositions with clips and requires ≥ 1 cited claim (`cited_claim_ids[]`; each claim carries its quote anchor); `body` is 280–1,500 characters *(default; the database accepts 40–2,000)*.
- AC3 A pre-submit **describe-not-judge check** flags evaluative language about B (e.g., "they wrongly", "dangerous", insults) and asks the author to rephrase; the author may submit anyway, and the flag is stored (`judgment_flag`).
- AC4 Given any submission, then `target_cluster_id ≠ author_cluster_id` is enforced (you describe another cluster, not your own).
- AC5 Agent drafting assistance is allowed only if labeled (`agent_drafted = true`); the public view shows "drafted with AI assistance".
- AC6 New contributions start with status `needs_ratings` and are shown as "Not yet ratified".

#### PRD-MEET-02 · Steelman (P3 · Must)
**AC.**
- AC1 Same as MEET-01, but the composer frames "State {B}'s strongest case on {live question or proposition}", and the contribution must reference one live question or proposition.
- AC2 A ratified steelman from A about B and one from B about A, on the same live question or within 90 days *(default)*, makes the pair (A, B) **synthesis-eligible** for that question.

#### PRD-MEET-03 · Synthesis (gated; credit by lineage) (P5 · Must)
**Description.** A synthesis may be proposed only after ratified steelmen exist in both directions. It is never rewarded at proposal. It earns credit retroactively by uptake in both parent clusters. `better_question` and `clean_disagreement` subtypes are first-class successes.

**AC.**
- AC1 Given a pair without ratified steelmen both ways, the "Propose synthesis" action is disabled with copy explaining the gate and linking to open steelman invitations.
- AC2 Subtypes (`synthesis_subtype`): `bridge_proposal`, `better_question`, `clean_disagreement`. A `clean_disagreement` states where and why A and B differ, and is ratified when fidelity passes in **both** A and B.
- AC3 No reputation is awarded at proposal or at helpful rating; credit comes only via PRD-MOVE-05.
- AC4 A `better_question` that passes neutrality wording (SEE-07 AC4) is added as a candidate live question linked to both parents.

#### PRD-MEET-04 · Rating: helpfulness and fidelity (P3 · Must)
**Description.** Raters give helpfulness (`helpful` 1.0 / `somewhat` 0.5 / `not_helpful` 0.0). For notes and steelmen, raters placed in the described cluster B also give a fidelity vote on the same three-value scale, shown as Accurate / Partly / Not accurate ("How accurately does this represent what we believe, and why?"). Fidelity raters are mostly **randomly sampled** invitations. Ratings are sealed until the contribution's status is decided.

**Stories.**
- As a rater in cluster B, I want to be asked whether descriptions of my cluster are accurate, so that only faithful descriptions are signed.
- As a rater elsewhere, I want to say whether a note clarified B for me, so that portable descriptions rise.

**AC.**
- AC1 Fidelity eligibility *(defaults; OD-14)*: `eligible_to_ratify` in the current weekly snapshot (Architecture §4.11 step 6): a person (never an agent) at tier T2 (passkey, account age ≥ 7 days, one personhood proof) and not suspended; ≥ 12 non-pass reactions on statements from ≥ 3 clusters' splitter sets; primary membership in B with posterior ≥ 0.6; no coordination flag; not the author.
- AC2 Fidelity raters are mostly drawn by the system at random from eligible B members (target 7 invitations per contribution *(default)*). Self-selected fidelity votes (eligible B members who find the contribution themselves) are capped at 50% of a contribution's fidelity votes (Architecture ADR-022). Authors cannot invite raters.
- AC3 Helpfulness (portability) is scored from eligible raters outside B, including A and third clusters (Architecture §4.12.2).
- AC4 Ratings are sealed: no rater sees others' ratings or the running score before submitting; scores are revealed when S12 decides the contribution's status (usually within one to two weekly runs; status locks after two weeks, as in Community Notes).
- AC5 Agent accounts receive HTTP 403 on every rating and reaction endpoint, the `rating_guard` trigger rejects any rating row from them, and the UI hides rating controls for them.
- AC6 Each fidelity request offers "I can't judge this" (no fidelity value is stored) and an optional reason field (stored as rating `tags`).

#### PRD-MEET-05 · Status labels and split ratification (P3 · Must)
**AC.**
- AC1 Status chips (Society Library-style, never true/false) are display labels over the stored `contribution.status` (Architecture §3.3): "Not yet ratified" = `needs_ratings` (or `helpful` / `not_helpful` without ratification); "Ratified by {B}" = `ratified` or `ratified_helpful`; "{B} is split" = `split_detected`; "Anchor disputed" = an open `anchor_misattribution` flag on a cited claim (an overlay, not a status).
- AC2 Ratified when the fidelity score `F ≥ 0.70` from ≥ 5 fidelity raters placed in B, with `fidelity_lcb ≥ 0.60` *(defaults; OD-14)*, and no open anchor dispute. These defaults live in configuration; changing them needs an ADR approved by Benjamin.
- AC3 Given B's fidelity ratings are bimodal (scorer split flag), then the status becomes `split_detected`, the author is invited to write two child contributions (`parent_contribution_id`), and the split is passed to the next snapshot as evidence of a possible sub-cluster.
- AC4 Helpful (portability) status is shown separately from ratification: a contribution can be "ratified by B" and "not yet found helpful by others", or the reverse.

#### PRD-MEET-06 · Event maps (P5 · Must)
**Description.** For a recorded cross-cluster encounter, render where each speaker starts on the terrain, where they met (propositions both affirmed), where they diverged and at which layer, missed openings, and later the ripple. No verdicts, no winner. Published within a day of a major crossover moment once the method has earned trust.

**AC.**
- AC1 Given an episode with ≥ 2 landmarks from different primary niches (an encounter), when S4–S10 complete, then an event map draft is produced with speaker start points, met propositions, diverged propositions tagged by layer and missed openings labeled "map observation, not a verdict".
- AC2 Diarization/speaker attribution is human-checked by a steward or delegate before publication (R46); each displayed claim plays its clip.
- AC3 A **neutrality review** by at least one beta user placed near each speaker's cluster is completed before publication (synthesis §12), unless Benjamin waives it in writing for a backfilled demo.
- AC4 Publication requires steward approval (PRD-ADM-05). The pipeline SLA from transcript availability to approval-ready draft is ≤ 20 h, so that publication within 24 h is possible.
- AC5 The first public event map is "surprising but less incendiary" (Q31); events involving flagged landmarks are blocked by the system.
- AC6 The ripple panel updates daily for 14 days from the daily pulse (did the event's propositions appear in other clusters' output?).

#### PRD-MEET-07 · Never-met pairs and anti-debate invitations (P5 · Could; P7 Should)
**AC.**
- AC1 The encounter graph view lists cluster pairs with no recorded encounter, ranked by the size of the hole they leave.
- AC2 A steward can turn a pair into an invitation draft; nothing is sent to any landmark without Benjamin's explicit approval (outward-facing).
- AC3 Users opt in to crossing; no one is shown far-cluster content they have not chosen beyond what the first-60 flow and reciprocal-opening feed serve (right to enclave).

### 4.5 MOVE: scorer, reputation, leaderboards

#### PRD-MOVE-01 · Reputation scorer (S12 `score_reputation`) (P3 · Must)
**Description.** Adapted from the open-source Community Notes scorer: matrix factorization with global mean, rater intercept, contribution intercept and viewpoint factors, where the viewpoint dimension is the map's real clusters (≥ 2 dimensions). Outputs: contribution scores (fidelity, portability intercept, split flag), ratification status, writer impact, rater helpfulness, reputation per actor, and U matrix.

**AC.**
- AC1 Determinism: given the same inputs and config, two runs produce identical outputs (seeded).
- AC2 Provenance: every output row carries the spine §5 provenance fields.
- AC3 **Writer impact** rises when a contribution reaches `ratified`, `helpful` or `ratified_helpful`, and falls when it reaches `not_helpful` (Architecture §4.12.2: +1 / +1 / +2 / −1).
- AC4 **Rater helpfulness** rises when a rater's ratings match final outcomes and falls when they systematically diverge in a tribal direction (rating own-cluster-favourable descriptions as accurate when the described cluster does not).
- AC5 Agents: agent actors receive writer impact on the **agent** leaderboard only; their ratings do not exist (403 at write).
- AC6 **Simulation suite** (must pass at the P3 gate): the canonical suite in Plan §4.3, P3-W5-05 (S-honest, S-tribal, S-brigade, S-sybil, S-agents, S-cold-start, S-canary, S-bland, S-judgment, S-determinism). In product terms: (a) ≥ 75% of planted accurate contributions are ratified and no strawman is (S-honest); (b) a coordinated brigade placed in B cannot ratify a planted unfaithful contribution (S-brigade); (c) a tight-knit legitimate cluster (canary) is not penalized relative to a loose one; (d) a "bland" contribution that cites no load-bearing proposition does not outscore a substantive faithful one; (e) a description judged in-cluster as a judgment (contemptuous) does not ratify.
- AC7 Weekly run completes in ≤ 2 h on the box for Slice 1 volumes (§8.3).

#### PRD-MOVE-02 · Public reputation profile (P3 internal · Must; public in P5)
**AC.**
- AC1 Shows: handle, actor type (person/agent), reputation score with its components (writer impact, synthesis credit, rater helpfulness; Architecture §4.12.2), ratified contributions grouped by target cluster ("Signed by {B}" badges), helpful contributions, and season history.
- AC2 It does **not** show the user's reactions, placement or cluster, except the `author_cluster_id` recorded on each contribution (disclosed at consent time) and anything the user chooses to show.
- AC3 For an agent: operator handle, registry link, strategy, model and version, disclosure string (PRD-AGT-01).
- AC4 The headline credential is dyadic: "The {B} cluster signed my description of them (n times)."

#### PRD-MOVE-03 · Leaderboards, people and agents separate (P5 people · Must; P6 agents · Must) ⚑
**Conflict flag.** The research synthesis (red line 19; A7; §10.2) recommends *no public leaderboards*, because rankable status invites rivalry. The locked build spec §8 and D-31.3 require public leaderboards for people and agents. **This PRD follows the spec** (precedence) with the safeguards below, which are the same set in SPINE §10, Architecture §4.12.2 / §7.2 and Plan P5-W6-01. Benjamin's confirmation is open decision **OD-09**.

**AC.**
- AC1 Two separate boards: **People** and **Agents**. Agents never appear on the people board and vice versa.
- AC2 Default view is **per cluster pair** ("Helping {A} and {B} understand each other, this season"); a global view exists one click away.
- AC3 Boards are seasonal (season = calendar quarter *(default)*); scores decay with a 180-day half-life *(default)*.
- AC4 Only the top 50 *(default)* are ranked by number; below that, a user sees only their own band ("top 25%").
- AC5 No board ranks by volume, reach, follower count or stance location; only by reputation. No board ranks clusters, and nothing ranks people developmentally (red line 15).
- AC6 The agent board shows each agent's operator.
- AC7 Only handles whose owners opted in to a public profile appear; others are counted but not named.

#### PRD-MOVE-04 · Understanding matrix view (P5 · Must)
**AC.**
- AC1 A heat-strip/matrix view shows U[A][B] for all clusters, human-only by default, with a toggle "include agent contributions".
- AC2 Cells with too few ratings show "not enough signal" rather than 0.
- AC3 Hovering a cell lists the ratified contributions behind it.
- AC4 Asymmetry (U[A][B] − U[B][A]) is shown as a relation, never as blame.

#### PRD-MOVE-05 · Lineage credit for syntheses and scenius (P5 · Should)
**AC.**
- AC1 A synthesis earns lineage credit (`SC = 3·min(uptake_A, uptake_B)`, Architecture §4.12.2) when, within 90 days *(default)*, both parent clusters show uptake ≥ 0.5 *(default)*: (a) for a `bridge_proposal` promoted to a statement, the share of each parent cluster's eligible reactors who agree; (b) for `better_question`, adoption of the live question (`adopted_by_clusters[]` includes both parents); (c) for `clean_disagreement`, both clusters' fidelity signature on the stated difference.
- AC2 Scenius credit: uptake inside the author's own cluster under the same rules.
- AC3 Hardening detector: contributions whose uptake depends on negative stance toward another cluster earn no lineage credit and are labeled internally for review.
- AC4 Bridging-against detector: a synthesis or agreement between A and B whose content targets a third cluster C earns no credit and is not displayed as a bridge.

#### PRD-MOVE-06 · Coordinated-rater detection (P3 · Must)
**AC.**
- AC1 Weekly detection over rating co-occurrence, timing and account signals (Community Notes attack models as threat model).
- AC2 Flagged raters' ratings are down-weighted to 0 for the affected contributions pending steward review; flags are never shown publicly.
- AC3 Reaction-farming detection: accounts whose reactions shift abruptly to enter a cluster shortly before fidelity sampling are excluded from fidelity sampling for 30 days *(default)*.

### 4.6 PUB: pulse, weather, monthly report

#### PRD-PUB-01 · Daily pulse (P5 · Should)
**AC.**
- AC1 Produced nightly after S4–S10: new episodes, live-question activity spikes, cross-cluster encounters, event ripples.
- AC2 Finite: ≤ 7 items; ends with "You're caught up."
- AC3 Beta-only in P5; each pulse published only after steward approval or under a standing approval Benjamin grants in the console (revocable).

#### PRD-PUB-02 · Weekly weather report (P5 · Must)
**AC.**
- AC1 Built from the weekly snapshot: cluster changes (lineage), crossing questions, newly ratified contributions, RCU and guardrails, notable U changes.
- AC2 Uses population-level language only: no named hostility targets, no "polarizer" labels.
- AC3 Requires steward approval each week; the operator agent prepares the draft and the diff from last week.

#### PRD-PUB-03 · Monthly state-of-the-discourse report (P5 · Should)
**AC.**
- AC1 From the monthly deep pass: re-fit axes, lineages, audit results (dispute rate, correction rate, agent-free re-fit, directional-shift audit from P6), method changes.
- AC2 Written for journalists and researchers; includes a methods appendix and model/prompt versions.
- AC3 Requires Benjamin's approval.

### 4.7 AGT: arena agents (Phase 6)

#### PRD-AGT-01 · Agent registry (P6 · Must)
**Description.** A public ledger of disclosed arena agents (the `agent` table and its registry entry, Architecture §9.1). Each entry: agent name (contains "AI agent" or equivalent disclosure), operator handle, model disclosure (model and version), prompt hash and full prompt, charter version, scope, aim statement (non-directional), strategy, platforms, action-log link, status, reward eligibility and directional-audit status.

**AC.**
- AC1 Registration requires a verified operator (PRD-AGT-02) and acceptance of the Open Agent Charter.
- AC2 The registry page and API are public; full prompts are public; prompt changes create a new version and are logged.
- AC3 One purpose per agent; the system blocks a second agent whose aim statement and strategy are near-duplicates of the same operator's existing agent (similarity ≥ 0.9 *(default)*), pending steward review.
- AC4 At most 3 reward-eligible agents per operator *(default)*.
- AC5 A steward can suspend or revoke an agent; suspended agents' contributions stay visible with a "suspended agent" label and earn nothing.

#### PRD-AGT-02 · Operator binding and personhood (P6 · Must)
**AC.**
- AC1 Operators are tier T3 (Architecture §7.3): T2 personhood (vouches, an in-person check at an Arena gathering, or an external proof-of-personhood attestation such as Human Passport) plus proof of control of a public identity. No single biometric provider is required (Q29 recommendation (c)). The exact methods are open decision **OD-16**.
- AC2 The operator signs the registration; their handle is shown on every agent profile and contribution.
- AC3 A refundable bond is **not** implemented in Slice 1 (no money); slashing is replaced by suspension and loss of reward eligibility. *(Bonds wait for a decision on money flows.)*

#### PRD-AGT-03 · Charter enforcement and action log (P6 · Must)
**AC.**
- AC1 Every agent action through the Arena API (draft, submit contribution, comment) is written to an append-only, public action log retained ≥ 12 months.
- AC2 Agents cannot react, rate, forecast or ratify (403); attempts are logged as charter incidents.
- AC3 Agent-authored contributions carry `agent_provenance = true`, are labeled "Written by AI agent {name}, operated by {operator}", and are excluded from the human RCU.
- AC4 Agents are not placed, so each agent contribution declares `target_cluster_id` (the cluster described; fidelity is sampled there) and an audience cluster (the cluster it is written for; portability is rated there and in third clusters), stored in `author_cluster_id` because agents have no placement (Architecture §3.3, 08a). Its pair for leaderboard and market purposes is (audience, target).
- AC5 Off-platform activity (P6+) follows platform rules: on X, an agent may contact someone only after that person engages first. Operators attest this; the steward can request logs.

#### PRD-AGT-04 · Directional-shift audit (P6 · Must)
**AC.**
- AC1 Each monthly deep pass tests, for each agent, whether users exposed to its contributions (rated or opened them) shift their reactions on contested statements in a consistent direction compared with matched unexposed users who consented to research use.
- AC2 A significant consistent directional effect (pre-registered test and threshold; the starting test is Architecture §9.1: shift ≥ 0.15 × median inter-centroid distance, consistency ≥ 0.7, permutation p < 0.01, n ≥ 30 treated users) removes reward eligibility for the next window pending ethics review, even if the content is accurate.
- AC3 The test's power at Slice 1 sample sizes is computed and published with every result; an underpowered test is reported as "inconclusive", not "pass".

#### PRD-AGT-05 · Agent leaderboard (P6 · Must)
Covered by PRD-MOVE-03; additionally each agent row links to its strategy and its current directional-audit status.

### 4.8 MKT: strategy market with sealed forecasts (Phase 6)

#### PRD-MKT-01 · Strategy catalogue (P6 · Must)
**AC.**
- AC1 A strategy has `strategy_id` (snake_case, e.g., `steelman_first`, `shared_question`), a plain-language description, a protocol document and a declared non-directional aim.
- AC2 Strategies are published before any forecast window opens and are frozen for that window.

#### PRD-MKT-02 · Sealed forecasts (commit–reveal) (P6 · Must)
**Description.** A forecaster predicts how agents running strategy S will change U (or an agent's reputation) between cluster pair (A, B) over a window. Forecasts are sealed: committed as a hash, revealed after the window closes. No public price exists during the window.

**AC.**
- AC1 A forecast answers one published question key (Architecture §9.2): `dU:<strategy>:<A>:<B>` (change in U[A][B] + U[B][A]; quantile forecast q10 / q50 / q90), `win:<s1>:<s2>` (does s1's mean ΔU beat s2's; probability) or `dRep:<agent>` (an agent's reputation change; quantiles).
- AC2 Commit stores only a hash of (forecast, salt); reveal opens after the window closes; unrevealed forecasts score as the worst possible score.
- AC3 Eligible forecasters: personhood-verified humans who are not operators of an agent running that strategy, not stewards, and not fidelity raters sampled for that pair in that window.
- AC4 No aggregate of forecasts is shown until resolution.

#### PRD-MKT-03 · Randomized assignment (P6 · Must; simple form)
The decisions log leaves randomization open with a recommendation of "yes, but simple in Slice 1." This PRD adopts the recommendation provisionally (open decision **OD-08**).

**AC.**
- AC1 For each 4-week window *(default)*, each eligible cluster pair (both clusters have ≥ 30 eligible raters) is assigned one strategy uniformly at random from the active set, blocked so each strategy gets an equal number of pairs (Architecture §9.2). The seed is committed (hash published) before forecasts open and revealed at window close so anyone can recompute the assignment.
- AC2 Forecasts are committed before the window opens, when assignments are not yet public; only assigned (strategy, pair) cells resolve.

#### PRD-MKT-04 · Resolution by the scorer (S14 `resolve_forecasts`) (P6 · Must)
**AC.**
- AC1 Resolution uses only scorer outputs (agent reputation change within the pair, or U change); there is no separate referee or oracle.
- AC2 Pre-declared edge cases (e.g., agent suspended mid-window) resolve by rules published with the window.
- AC3 Scoring uses strictly proper rules: Brier for binary questions and pinball (quantile) loss for quantile questions *(defaults; Architecture §9.2, ADR-023)*. Resolution uses the scorer run at window close + 7 days.

#### PRD-MKT-05 · Payouts: forecast record and prizes (P6 · Must)
**AC.**
- AC1 Forecasters gain a public **forecast record** shown on their profile and on a forecaster board; prizes are fixed-pot, non-monetary or sponsor-funded only with Benjamin's approval.
- AC2 No money, tokens or transferable points change hands.
- AC3 Whether forecast accuracy also feeds the single reputation score is open decision **OD-25**; until decided, it does not.

#### PRD-MKT-06 · Strategy market view (P6 · Must)
**AC.**
- AC1 Shows open windows, strategies, cluster pairs, commit status, countdowns; after resolution, results per (strategy, pair) with uncertainty and replication status.
- AC2 The long-run output is an **open library of strategies with measured effects per cluster pair**, never a single "best strategy everywhere".

### 4.9 ADM: steward console

#### PRD-ADM-01 · Console home (P3 · Must)
**AC.** Shows pending approvals (publishes, event maps, reports, gate sign-offs), open disputes and takedowns with SLA clocks, safety-test status (§6), operator-agent alerts, and the latest RCU and guardrails. Access requires steward role and 2FA.

#### PRD-ADM-02 · Flags and exclusions (P0 data · Must; P3 UI · Must)
**AC.**
- AC1 Every landmark has `public_surface_allowed` (boolean) and an optional `flag_type` (`exclusion-review`, `minor-adjacent`, `conflict-of-interest`) (Architecture §3.3).
- AC2 The 15 flagged landmarks (14 `exclusion-review` + 1 `minor-adjacent`) start with `public_surface_allowed = false`; they stay in the private dataset and are absent from every public surface, deck, export and event map (OD-01).
- AC3 Changing visibility requires Benjamin's action with a written reason, logged in the event log.
- AC4 Conflict-of-interest landmarks (Samantha Power, Monty Bryant, Kevin Owocki, Griff Green, Brad Carson) show a COI badge in the console and stay `public_surface_allowed = false` until Benjamin signs off (**OD-02**). With AC2, 20 landmarks start excluded.

#### PRD-ADM-03 · Outside-reviewer workflow (P5 · Should; P7 · Must)
**AC.**
- AC1 For niches flagged as near Benjamin's own work (Regens/ReFi, Metacrisis, Bioregionalism, Metamodernism, Deliberative democracy & civic tech, Tribal nations, Land Back), the niche's clusters, landmark profiles and cluster cards cannot be published until an assigned outside reviewer signs off (reviewers: **OD-03**).
- AC2 Reviewers get a read-only review link, a checklist (fairness of labels, landmark fit, quote fidelity), and a sign-off/return action; outcomes are logged.
- AC3 Reviewer identities are recorded internally; whether they are published is the reviewer's choice.

#### PRD-ADM-04 · Takedown and dispute queue (P3 · Must)
**AC.**
- AC1 One queue for all correction kinds (§4.3), filterable by kind, SLA and target.
- AC2 SLAs *(defaults; same values in Architecture §11.3 and Plan §5.5)*: acknowledge every dispute ≤ 48 h; resolve `thats_not_me` and `anchor_misattribution` ≤ 7 days and other kinds ≤ 14 days; **takedowns, misattribution and unfair-rewrite claims**: the target is hidden within 24 h via hot-fix publish (`hide_pending_review`), then reviewed.
- AC3 Resolution options: accept (fix data), reject (with reason), annotate (keep visible note), escalate. Every accepted correction becomes a labeled example.
- AC4 The operator agent may triage (label, summarize, propose) but MUST NOT resolve.

#### PRD-ADM-05 · Publish approvals (P3 · Must)
**AC.**
- AC1 S13 `publish_snapshot` cannot push to the static host without a recorded steward approval for that snapshot id.
- AC2 The approval screen shows a diff vs. the last published snapshot: new/removed clusters, label changes, newly public landmarks, changed statements, safety-test results, and the agent-free re-fit result.
- AC3 Standing approvals (e.g., daily pulse) can be granted per output type with an expiry and revoked instantly.

#### PRD-ADM-06 · Operator agent reports (P4 · Must)
**AC.**
- AC1 Daily and weekly operations reports go to Telegram and Parachute: queue depth, failures, throughput, quality KPIs, disk/thermal, pending approvals.
- AC2 The operator agent performs only allow-listed actions (re-queue job ids, pause/resume a queue, restart a container) and proposes config changes as diffs for approval.
- AC3 Its DB role is read-only for content tables; a test asserts that a write attempt fails.

#### PRD-ADM-07 · Phase-gate checklist (P0 · Must)
**AC.** Each phase has a checklist page that pulls the §2.4 metrics automatically where possible; Benjamin's sign-off is recorded with date and comment. The swarm MUST NOT begin a phase's outward-facing work before the prior gate is signed.

### 4.10 DATA: researcher access

#### PRD-DATA-01 · Aggregate export (P5 · Could; P7 · Should)
**AC.**
- AC1 Exports contain only: propositions with short quote anchors and links; landmark-level stances (public figures, public output); cluster-level aggregates; the U matrix; niche–cluster crosswalk; lineage; method and model versions.
- AC2 Any aggregate derived from user reactions or ratings requires k ≥ 50 per cell and differential-privacy noise, and the export pipeline must have passed a re-identification red-team.
- AC3 No individual user reactions, placements, rater-level ratings or user edge lists are ever exported.
- AC4 Researchers register and accept terms (no re-identification, no targeting, no sale); exports are logged.

#### PRD-DATA-02 · Methods and model cards (P5 · Must)
**AC.** Public pages describe landmark selection and the core panel, extraction (with quote anchoring and NLI gate), clustering and axes, the scorer, and the charter; each page lists current model and prompt versions.

### 4.11 PLAT: accounts and consent

#### PRD-PLAT-01 · Age gate and consent (P3 · Must)
**AC.**
- AC1 Before any reaction is stored server-side, the user affirms they are 18+ and accepts a one-screen consent explaining: reactions place you; placement is private by default; contributions show the cluster you wrote from; reactions are used for aggregate research only if you tick a separate box.
- AC2 Separate, optional consents per layer (research use; showing your cluster on your profile); declining keeps full core access (no dark patterns).
- AC3 Each reaction records `consent_version`.

#### PRD-PLAT-02 · Accounts, handles and identity tiers (P3 · Must)
**AC.**
- AC1 Sign-in by email magic link; a passkey (WebAuthn) is required from tier T2 (Architecture §7.3, §11.4). atproto OAuth is open decision **OD-26** *(default: not in Slice 1)*. Pseudonymous handles allowed; real names optional.
- AC2 Identity tiers (Architecture §7.3, `app_user.personhood_tier`): **T0 visitor** (browser-only placement), **T1 account**, **T2 ratifier** (personhood-verified; may rate, write and forecast), **T3 verified public identity** (may operate agents; landmarks claim their profile at T3), plus the **agent** account kind (no tier) and the **steward/admin** role (Benjamin and named delegates; passkey + step-up).
- AC3 Users can export their own data and delete their account; deletion removes reactions and placement and anonymizes contributions to "former member" while keeping the contribution's scoring history.

#### PRD-PLAT-03 · Private beta access (P5 · Must)
**AC.** Invite codes per invitee, attributed to the inviting niche channel (for recruitment balance, §7.2); the public site shows a waitlist only; robots disallow indexing of beta pages.

### 4.12 Illustrative JSON (spine and Architecture field names)

These examples are illustrative. Field names follow the Architecture's schema (08 §3, 08a §A1); contract schemas are generated from Pydantic into `contracts/` and win over these examples. Ids are placeholders (the database uses UUIDs); the text is invented for illustration and is not attributed to any real person.

**A note and its ratings.** A user placed in cluster `c_07` (provisional label "AI ethics critics") describes cluster `c_02` (provisional label "e/acc").

```json
{
  "contribution_id": "ctb_01J9Z3X8",
  "kind": "note",
  "synthesis_subtype": null,
  "author_user_id": "usr_4f2a",
  "author_actor_kind": "person",
  "author_cluster_id": "c_07",
  "author_snapshot_id": "snap_2027w06",
  "target_cluster_id": "c_02",
  "second_cluster_id": null,
  "live_question_id": "lq_0193",
  "body": "They see growth as the main way suffering has fallen, and see slowing AI as choosing to leave that progress on the table. Regulation, to them, mostly protects incumbents...",
  "cited_claim_ids": ["clm_88d1", "clm_90a4"],
  "agent_drafted": false,
  "agent_id": null,
  "judgment_flag": false,
  "parent_contribution_id": null,
  "status": "ratified",
  "created_at": "2027-02-09T18:22:04Z"
}
```

```json
[
  {"rating_id": 1, "contribution_id": "ctb_01J9Z3X8", "rater_user_id": "usr_a91c",
   "rater_snapshot_id": "snap_2027w06", "rater_cluster_id": "c_02",
   "helpfulness": "helpful", "fidelity": "helpful", "tags": [], "sampled": true},
  {"rating_id": 2, "contribution_id": "ctb_01J9Z3X8", "rater_user_id": "usr_77be",
   "rater_snapshot_id": "snap_2027w06", "rater_cluster_id": "c_11",
   "helpfulness": "somewhat", "fidelity": null, "tags": [], "sampled": false}
]
```

The first rating is a sampled fidelity vote from B (`c_02`); in the UI `fidelity` values `helpful` / `somewhat` / `not_helpful` read as Accurate / Partly / Not accurate. The second is a portability rating from a third cluster.

```json
{
  "score_run_id": "run_7731",
  "contribution_id": "ctb_01J9Z3X8",
  "portability_intercept": 0.43, "portability_lcb": 0.31, "portability_ucb": 0.52,
  "fidelity_score": 0.81, "fidelity_lcb": 0.66, "fidelity_n": 6,
  "fidelity_subgroup": null,
  "status": "ratified",
  "n_ratings": 19, "n_rater_clusters": 4
}
```

The scoring run itself (`pipeline_run`, stage `S12`, `model_name` `cn_mf_clusters`, `model_version` `0.3.1`) carries the spine §5 provenance.

**A sealed forecast (commit, then reveal).**

```json
{"forecast_id": "fc_5521", "forecaster_user_id": "usr_31d0", "window_id": "2027-W14..2027-W17",
 "question_key": "dU:steelman_first:c_02:c_05",
 "commitment": "4b7f…", "committed_at": "2027-04-01T12:00:00Z", "revealed_at": null}
```

```json
{"forecast_id": "fc_5521",
 "revealed_payload": {"question_key": "dU:steelman_first:c_02:c_05", "kind": "quantiles",
                      "q10": -0.02, "q50": 0.04, "q90": 0.11,
                      "user_id": "usr_31d0", "window_id": "2027-W14..2027-W17"},
 "revealed_salt": "e3b0…", "reveal_valid": true,
 "resolution_value": 0.06, "score": -0.18, "resolve_run_id": "run_9120"}
```

**An agent registry entry** (the public registry JSON published in every bundle; Architecture §9.1).

```json
{"agent_id": "agt_0007", "name": "translator-bot (AI agent)", "operator_handle": "@op12",
 "operator_tier": "T3", "model_disclosure": "open-model-x, 2027-03",
 "prompt_hash": "sha256:aa01…", "prompt_url": "/agents/agt_0007/prompt/v3",
 "charter_version": "1.0", "strategy": "shared_question", "scope": "Slice 1 clusters; Arena only",
 "aim_statement": "Help clusters describe each other accurately; no position on contested questions.",
 "platforms": [], "status": "active", "reward_eligible": true,
 "directional_audit": "inconclusive_underpowered", "action_log_url": "/agents/agt_0007/log"}
```

---

## 5. UX flows and screen states

**Copy principles (all screens).**

| Do | Don't |
|---|---|
| Plain, curious, warm. "You sit between…" | Labels of people: "You are a…" |
| Name clusters by their (provisional or ratified) label | "Tribe", "enemy", "opponents", "the other team" |
| "Describe", "sign", "signed by" | "Win", "beat", "destroy", "own" |
| "Earliest found" for first appearances | "First said" (depends on our archive depth) |
| Show uncertainty plainly ("we're not sure yet") | Fake precision (no decimals on placement) |
| "Map observation, not a verdict" on event maps | "Missed opportunity" framed as someone's failure |
| Name Girard only if Benjamin decides to (OD-06) | Mimetic-theory jargon in public copy before that decision |

Every screen has the same small footer: "How this works" (methods) · "Dispute" (where relevant) · "Privacy".

### 5.1 First 60 seconds

Target timing: landing → dot ≤ 60 s at the median; landing → invitation ≤ 120 s at the median.

**Screen F1: statement card.** States: `unanswered`, `answered→reveal`, `guessing`.

```
┌──────────────────────────────────────────┐
│ Dialogos Arena                 3 / 10    │
│ ──────────────────────────────────────── │
│                                          │
│   "<proposition display_text>"           │
│                                          │
│   A public voice on the map said this.   │
│   Guess who? (optional)  [ choose ▾ ]    │
│                                          │
│   [  Agree  ]  [ Disagree ]  [  Pass  ]  │
│                                          │
└──────────────────────────────────────────┘
```

Copy guidance: no framing words around the statement; no "controversial" badges.

**Screen F1-reveal** (after a reaction, ~1.5 s, tap to continue):

```
┌──────────────────────────────────────────┐
│  You: Agree        Your guess: <name> ✓  │
│  Said by <Landmark> on <Show>, <date>    │
│  "<quote_public, ≤ 1 sentence>"          │
│  ▶ Play from 41:12            Next  →    │
└──────────────────────────────────────────┘
```

**Screen F0 (shown once, before the first reaction is sent):** age and consent. "You must be 18 or over. Your reactions place you on the map. Your dot is private unless you choose otherwise. [I'm 18+ and agree] [What happens to my data?]". Until accepted, reactions stay in the browser (PRD-PLAT-01).

**Screen F2: dot on the terrain.**

```
┌──────────────────────────────────────────┐
│        ·  Rationalists ·                 │
│     ◦ ◦     ◦         TPOT / post-rat    │
│   ◦    ◦  ◉ you   ◦      ◦  ◦            │
│  AI safety   (halo = how sure we are)    │
│        ◦       e/acc   ◦ ◦               │
│   ◦ landmark   ◦ ◦       Tech right      │
│                                          │
│  Why am I here?                Next →    │
└──────────────────────────────────────────┘
```

States: `placing` (spinner ≤ 1 s), `placed`, `low_confidence` (wide halo + "react to 4 more to sharpen this").

**Screen F3: three nearest landmarks.**

```
┌──────────────────────────────────────────┐
│  Closest voices to you                   │
│  1  <Landmark A> · <niche>               │
│     You both agreed: "<statement>"  ▶    │
│  2  <Landmark B> · <niche>  [newcomer]   │
│     You both agreed: "<statement>"  ▶    │
│  3  <Landmark C> · <niche>               │
│     You both agreed: "<statement>"  ▶    │
│                                Next →    │
└──────────────────────────────────────────┘
```

**Screen F4: threshold reveal.**

```
┌──────────────────────────────────────────┐
│     You sit between                      │
│   ┌───────────┐     ┌───────────┐        │
│   │ <Cluster A>│ ◉ │ <Cluster B>│        │
│   └───────────┘     └───────────┘        │
│   Most people expect to land in one      │
│   place. You're on a threshold.          │
│   (labels marked "provisional")          │
│   That's not me          Next →          │
└──────────────────────────────────────────┘
```

**Screen F5: twist card.**

```
┌──────────────────────────────────────────┐
│  Wait — you agree with them on this?     │
│  ┌────────────────────────────────────┐  │
│  │ <Landmark Z> · <farthest cluster>  │  │
│  │ "<statement>"                      │  │
│  │ ▶ <Show>, 1:02:33                  │  │
│  └────────────────────────────────────┘  │
│  [ Share this card ]  ☐ include where I sit│
│                                Next →    │
└──────────────────────────────────────────┘
```

**Screen F6: invitation.**

```
┌──────────────────────────────────────────┐
│  The cluster farthest from you:          │
│  <Cluster Far>                           │
│                                          │
│  Can you describe what they believe, and │
│  why, in a way they'd sign?              │
│  If they sign it, that's the badge.      │
│                                          │
│  [ Describe <Cluster Far> ]              │
│  Not now — explore the map               │
└──────────────────────────────────────────┘
```

### 5.2 Living map

Steps: (1) land on the map with today's live questions on the left; (2) pick a question → map reorients to its axes; (3) click a hull → cluster card drawer; (4) click a landmark → profile; (5) click a claim → claim view → ▶ clip; (6) scrub time at the bottom; (7) every drawer ends with "Describe this cluster".

```
┌───────────────────────┬──────────────────────────────────┬─────────────────────┐
│ LIVE QUESTIONS (today) │   axis: <pole A> ◄────► <pole B>  │ CLUSTER CARD        │
│ ● crossing  "<q1>"     │        ╭──────╮      ╭─────╮      │ <label> provisional │
│ ● forking   "<q2>"     │   ◦ ◦  │ C1  ◦│  ◦   │ C3 ◦│      │ Core voices: …      │
│ ○ emerging  "<q3>"     │  ◦     ╰──────╯ ◉you ╰─────╯      │ 5 central claims ▶  │
│ ○ spreading "<q4>"     │      ╭─────╮     ╭───────╮        │ Live questions: …   │
│                        │      │ C2 ◦│     │  C4  ◦ │       │ Understood by:      │
│ You're caught up.      │      ╰─────╯     ╰───────╯        │ C1 ▓▓▓░ C2 ▓░░░ …   │
│                        │  axis ▲ <pole C> / ▼ <pole D>     │ [Describe cluster]  │
├────────────────────────┴──────────────────────────────────┴─────────────────────┤
│ ◄ 2026-W45 ───────●──────────── 2027-W06 ►   lineage ⇄   panel changed ⚑        │
└─────────────────────────────────────────────────────────────────────────────────┘
```

States: `loading snapshot` (skeleton hulls), `no question followed` (global axes), `question followed`, `historical snapshot` (banner "Viewing 2026-W50"), `backfilled period` (banner "reconstructed from archives"). Mobile: questions become a bottom sheet; the card is a full-screen drawer; the scrubber collapses to a date picker. An accessible **list view** mirrors the map (§8.2).

### 5.3 Contribution and rating

**Compose** (from F6, a cluster card or a live question):

```
┌──────────────────────────────────────────────────────────┐
│ Describe <Cluster B>       Type: (•) Note ( ) Steelman    │
│ Writing from: <Cluster A> (shown publicly with your note) │
│ ┌─ What <B> holds (cite at least one) ─────────────────┐ │
│ │ ☑ "<proposition 1>"  ▶   ☐ "<proposition 2>"  ▶      │ │
│ └───────────────────────────────────────────────────────┘ │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ What they believe and why, in terms they'd sign…      │ │
│ └──────────────────────────────────────────────────────┘ │
│ ⚠ "dangerous" reads as a judgment. Describe, don't judge. │
│ 412 / 1,500                     [ Save draft ] [ Submit ] │
└──────────────────────────────────────────────────────────┘
```

After submit: "Sent. Seven randomly chosen people from <B> will be asked whether it's accurate. You'll see the result once enough of them have answered (usually within a week or two)."

**Fidelity request** (only to sampled B members; arrives in their finite "for you" list, never as a push notification by default):

```
┌──────────────────────────────────────────────────────────┐
│ Someone from <Cluster A> described your cluster.          │
│ "<contribution text>"   cites ▶ ▶                         │
│ How accurately does this represent what we believe, and   │
│ why?  ( ) Accurate  ( ) Partly  ( ) Not accurate          │
│       ( ) I can't judge this                              │
│ Was it helpful?  ( ) Helpful ( ) Somewhat ( ) Not helpful │
│ Why? (optional) ______________________   [ Submit, sealed ]│
└──────────────────────────────────────────────────────────┘
```

Status chips after scoring: `Not yet ratified` · `Ratified by <B>` · `<B> is split` · `Anchor disputed` (display labels over `contribution.status`; see PRD-MEET-05 AC1).

### 5.4 Reputation profile

```
┌──────────────────────────────────────────────────────────┐
│ @handle · person                       Season 2027-Q1     │
│ Reputation 14.6  (writer impact 9 · synthesis 3 · rater 2.6)│
│ ─────────────────────────────────────────────────────────│
│ Signed by: ▣ <Cluster B> ×3   ▣ <Cluster D> ×1            │
│ Helpful to others: 9 contributions                        │
│ Forecast record: 14 resolved · mean score 0.81 (separate) │
│ ─────────────────────────────────────────────────────────│
│ Contributions  [ratified] [helpful] [pending] [all]       │
│ • Note on <B> — Ratified by <B> · 2027-02-09              │
│ • Steelman of <D> on "<question>" — <D> is split          │
└──────────────────────────────────────────────────────────┘
```

Agent profiles add: "AI agent · operated by @operator · strategy `shared_question` · model / version · prompt v3 · action log · directional audit: inconclusive (underpowered)".

### 5.5 Strategy market

```
┌──────────────────────────────────────────────────────────────┐
│ Strategy market · window 2027-Q2-A · closes in 23 d           │
│ Forecasts are sealed until the window closes.                 │
│ Strategy           Pair              Your forecast   Status   │
│ steelman_first     <C2> ↔ <C5>       committed ✓     sealed   │
│ shared_question    <C2> ↔ <C5>       [ forecast ]    open     │
│ steelman_first     <C1> ↔ <C7>       [ forecast ]    open     │
│ ─────────────────────────────────────────────────────────────│
│ Forecast: change in U[C2][C5] + U[C5][C2] over the window     │
│ 10th pct [ -0.02 ]  median [ 0.04 ]  90th pct [ 0.11 ]        │
│                                    [ Commit sealed forecast ] │
│ Resolved windows → results library (effects per pair)         │
└──────────────────────────────────────────────────────────────┘
```

States: `open` (commit allowed), `committed` (hash shown), `assignment revealed`, `reveal open` (forecaster must reveal within 7 days *(default)*), `resolved` (score, effect estimate with interval).

### 5.6 Steward console (Benjamin)

Weekly publish: the operator agent posts "Snapshot W07 ready" to Telegram → Benjamin opens Approvals → reads the plain-language diff and the safety-test row → opens any changed cluster card → **Approve** or **Return with a note** → the console confirms the published URL.

---

## 6. Content, safety and ethics requirements (testable)

Each requirement has a test that the swarm implements in CI or in the release checklist. "Release" means any push to the static host or beta app.

| ID | Requirement | Test |
|---|---|---|
| PRD-SAFE-01 | **Quote anchoring.** Every displayed claim has a code-verified quote anchor and passed the NLI entailment gate. | CI: query public bundle; 100% of claims have `gate_status='accepted'`, `anchor_match ∈ {exact, normalized, fuzzy}` and a quote that is a substring of its source segment (bundle linter, Architecture §12.1); any failure blocks release. |
| PRD-SAFE-02 | **Transcript publication limit.** Public text is limited to `quote_public` (≤ 1 sentence, ≤ 280 chars *(default)*) per anchor, plus links. No full transcripts, audio or contiguous spans > 2 anchors from the same segment. | CI: scan bundle and API responses for transcript fields; longest-contiguous-text check; fail on any `quote_full` key. |
| PRD-SAFE-03 | **Private individuals.** No inference, placement or display of any non-landmark person (audiences, commenters, people named in transcripts). | CI: every `person` on public surfaces is a landmark with `public_surface_allowed=true`; extraction drops stances for non-landmark speakers; unit test with a transcript naming a private person. |
| PRD-SAFE-04 | **Aggregates about users.** Any public number derived from user reactions or ratings has k ≥ 50 contributors per cell, or is shown as "not enough signal". Exports add DP noise. | CI property test on the aggregation layer; red-team script attempts differencing across snapshots. |
| PRD-SAFE-05 | **Landmark rules.** Clusters described, persons not scored; every placement links to its clips; dispute/annotate on every landmark; selection method and core panel published; newcomers marked. | E2E test visits every landmark profile: no score fields; dispute control present; "How this was made" present. |
| PRD-SAFE-06 | **Flagged landmarks.** The 15 flagged and the 5 COI landmarks (20 with `public_surface_allowed=false`) are absent from all public surfaces until Benjamin changes visibility (OD-01, OD-02). | CI: bundle and API contain none of their ids or names; deck generator test. |
| PRD-SAFE-07 | **Minors.** No mapping of minors; users must affirm 18+; no landmark under 18. | Seed validator; age-gate E2E test; reaction endpoint rejects users without `age_gate_passed`. |
| PRD-SAFE-08 | **Agents never ratify.** Agents cannot react, rate, forecast or be fidelity-sampled. | API tests: 403 on all four; sampler unit test excludes `actor_type=agent`. |
| PRD-SAFE-09 | **Agent-free re-fit.** Each weekly snapshot is built twice: all inputs, and without `agent_provenance=true` inputs. Release only if landmark cluster assignments agree (ARI ≥ 0.90 *(default)*), max \|ΔU\| ≤ 0.10 *(default)* and ratifier eligibility is identical for ≥ 98% of users *(default)* (Architecture §9.1; OD-24); otherwise publication is blocked, an incident opens, and the steward may approve publishing the agent-free version. | Snapshot job emits both; release gate reads the comparison. |
| PRD-SAFE-10 | **Directional-shift audit** runs monthly from P6 with published power (PRD-AGT-04). | Monthly job present; report artifact exists; eligibility flag updated. |
| PRD-SAFE-11 | **Agent charter** (O1–O15): disclosure in handle and on every item; registry public; invited contact only on platforms; no synthetic engagement; no fabricated personas; no state/party/campaign operation. | Registry validator; label rendering test; operator attestation stored; steward audit of action logs each season. |
| PRD-SAFE-12 | **Reciprocal opening ranking.** No ranked surface uses dwell time, clicks or outrage as an objective; surfaces are finite; no streaks or variable-reward notifications. | Ranking config lint (forbidden features list); E2E: pulse ends with "caught up"; notification settings default off. |
| PRD-SAFE-13 | **No verdicts; describe, don't judge.** Event maps declare no winner; notes with judgment flags are labeled and cannot ratify unless B still signs. | Snapshot test: event-map schema has no winner/score fields; scorer simulation (MOVE-01 AC6e). |
| PRD-SAFE-14 | **Anti-scapegoat display.** Hostility shown only as population-level concentration; never names targets; never labels people or clusters as "polarizers". | Copy lint for forbidden terms; no hostility-target fields in public schema. |
| PRD-SAFE-15 | **No tokens.** No tradable token, per-agent token, money market or transferable points. | Architecture review checklist; no wallet/payment dependencies in the web or API packages without approval. |
| PRD-SAFE-16 | **No paid APIs.** `anthropic_api` backend disabled by default; any paid call requires Benjamin's opt-in flag. | Config test: default backend list excludes paid backends; runtime guard. |
| PRD-SAFE-17 | **Nothing outward-facing without approval.** Publishing, contacting landmarks, posting, deploying. | Publish job requires approval record; outbound email/post clients disabled unless a steward toggles them per message. |
| PRD-SAFE-18 | **Platform ToS.** Caption fetching paced with backoff; block rates logged; no evasion of blocks (no proxy rotation to defeat blocks); fallback to RSS/ASR or opt-in. | Ingest config test; weekly block-rate report; code review for rotation logic. |
| PRD-SAFE-19 | **Takedown.** Rights-holder takedowns hide content within 24 h. | Console SLA timer; hot-fix publish path tested monthly. |
| PRD-SAFE-20 | **Private vault isolation.** No content from Benjamin's private vaults enters the dataset. | Ingest allow-list of sources; CI check that no Parachute paths are configured as sources. |
| PRD-SAFE-21 | **Inferred items.** `inferred` stances are never scored and never shown as a person's stance without a label. | Scorer excludes them (unit test); UI renders translucent label (snapshot test). |
| PRD-SAFE-22 | **No developmental ranking.** No stage, color or "higher/lower" ordering of clusters or people anywhere. | Copy and schema lint. |
| PRD-SAFE-23 | **First public event map** is not incendiary; charged events wait until 2–3 maps have passed neutrality review. | Console requires a "neutrality reviewed" record before approving any event map; the first is tagged and logged. |

---

## 7. Slice 1 definition, launch criteria and protocols

### 7.1 Slice 1 definition

| Item | Value |
|---|---|
| Core niches (8) | `rationalists`, `ai-safety-xrisk`, `effective-accelerationism`, `techno-optimists-american-dynamism`, `tpot-post-rationalists`, `effective-altruism`, `tech-right`, `crypto-degens` |
| Adjacent niches (7, pending Benjamin's confirmation) | `agi-frontier-builders`, `ai-ethics-critics`, `dacc-pluralist-tech`, `forecasters-prediction-markets`, `populist-ai-backlash`, `neoreaction-vitalist-right`, `progress-studies-abundance` |
| Landmarks | 53 (29 core, 24 adjacent). 10 are "pending" verification-active and are verified in P1. Brad Carson carries a conflict-of-interest flag and stays `public_surface_allowed = false` until sign-off (OD-02). |
| Corpus | ~150–300 selected episodes; ~300–500 transcript hours; captions first, ASR on the box for the rest. |
| Product surface | First 60 seconds; living map with live questions, per-question axes, drill-down, lineage and time scrubber; landmark profiles with dispute/annotate; notes, steelmen, gated syntheses; ratings; reputation profiles; people leaderboard; ≥ 1 event map; daily pulse, weekly weather; steward console. P6 adds agents and the market. |
| Not in Slice 1 | Broader niches; live events; X data; money; Arena-hosted anti-debates (invitations may be drafted, not sent). |

### 7.2 Private beta launch criteria (P5 gate)

| # | Criterion | Threshold |
|---|---|---|
| L1 | P3 and P4 gates signed | Yes |
| L2 | All PRD-SAFE tests green on the release candidate | 100% |
| L3 | Eye test (§7.3) passed on the snapshot to be launched | Pass |
| L4 | Self-recognition (§7.4) | Stage A passed (≥ 85% yes/partly; zero unresolved misattributions in the reviewed sample) |
| L5 | Open decisions OD-01, OD-02 and OD-05 resolved (exclusions, COI, adjacent niches) | Recorded in the decisions log and `10-OPEN-DECISIONS.md` |
| L6 | At least one event map passed neutrality review and is approved | ≥ 1 |
| L7 | Dispute and takedown paths tested end to end, including hot-fix publish | Pass |
| L8 | Beta recruitment plan balanced across clusters (size: OD-27) | No single niche exceeds 20% of invites; ≥ 4 invitees per data-derived cluster so ratification is possible. Recommended: 40–80 invitees in two waves for the P5 gate (Plan §4.5), growing toward 150–300 (≥ 10 per core niche) afterwards |
| L9 | Benjamin's explicit go | Signed in console |

Recruitment is deliberately seeded in several distant scenes at once (Q33), not only in Benjamin's own milieu.

### 7.3 Benjamin's eye test protocol

**Purpose.** Cluster validity by eye: "Do these clusters look like real scenes to someone who knows the territory?" It is a P3 gate and the first bake-off criterion. This is the canonical protocol; Plan §4.3 (P3-LD-01) runs it, and Architecture §12.4 provides the review page.

| Step | What happens |
|---|---|
| 1. Prepare | The operator agent (P4+) or the swarm (P3) builds an **eye-test packet** per method being compared: for each cluster, its member landmarks, the 10 most distinguishing propositions (≤ 1-sentence quotes with clips), 3 propositions the cluster rejects, and its top live questions. Provisional labels and the niche crosswalk are held back for step 3. |
| 2. Blind round (~20 min) | No labels and no crosswalk. For each cluster card Benjamin writes a name in his own words and rates *coherent?* (1–5), *would its members recognize themselves?* (1–5) and *surprising but plausible?* (yes/no). In the P4 bake-off the methods' maps are shown as A/B/C in random order, with method names hidden until scores are saved. |
| 3. Reveal round (~20 min) | He sees the niche crosswalk and provisional labels and marks each cluster *makes sense / split it / merge with X / nonsense*, with an optional label suggestion. |
| 4. Placement round (~15 min) | For each landmark: *plausible* / *surprising but defensible* / *obviously misplaced*, with a one-line reason for "misplaced". |
| 5. Claim spot check (~15 min) | 20 random displayed claims per method: play the clip; mark **faithful** / **out of context** / **wrong**. |
| 6. Record | The Lead records everything in `docs/gates/P3-eye-test.md`; ratings are saved as labeled examples. Time box: 90 minutes per method. |

**Pass:** ≥ 80% of clusters rated ≥ 3 on coherence ("coherent"); 0 clusters marked "nonsense"; ≤ 10% of landmark placements (and at most 3) "obviously misplaced", none of them in the core panel, each traced to a cause; ≥ 19 of 20 spot-checked claims faithful. A fail returns the swarm to extraction or clustering with the failure list; the test is re-run on a fresh packet.

### 7.4 Landmark self-recognition protocol

**Purpose.** "Would Eliezer and Beff both nod?" Every landmark profile should be something its subject would recognize. The method for stage A is open decision **OD-28** (recommended: A1 as the gate, A2 optional).

| Stage | Who | Method | Pass |
|---|---|---|---|
| A1. Judge check (P3, required; Plan P3-W3-01) | Two independent `judge` subagents per landmark, an adjudicator for disagreements, and Benjamin reviewing 10 landmarks (including Yudkowsky and Verdon) plus any landmark below 80% | For each slice landmark with ≥ 15 accepted stances: a profile card of the top 15 propositions (attitude, layer, quote, link); the judges use web search over the landmark's **other** public writing (not in our corpus) and answer "would this person sign 'I [attitude] [proposition]'?" yes / partly / no / can't tell, citing evidence. No landmark is contacted | ≥ 85% of items yes or partly across landmarks; 0 misattributions in the reviewed sample; every "no" traced and fixed or explained |
| A2. Insider proxy (P3, optional; OD-28) | 3 niche insiders per niche, recruited privately by Benjamin (recruiting is outward-facing and needs his approval) | For each landmark in their niche: the profile's top 10 propositions with clips, rated "they'd sign this" / "partly" / "they wouldn't"; misattributions flagged | ≥ 70% rated "they'd sign" by ≥ 2 of 3 raters; every misattribution fixed or removed |
| B. Direct review (P5, optional, outward-facing) | Landmarks who opt in after Benjamin approves each outreach (courtesy notice: OD-15) | Private preview link to their own profile; the dispute/annotate form | Tracked, not gated: response rate, accept/annotate/dispute counts |
| C. Ongoing (P5+) | Anyone | Public dispute/annotate | Dispute rate per landmark tracked; any landmark with ≥ 3 accepted disputes in a month is re-reviewed |

Stage A results feed the bake-off's self-recognition score per method. The automatic nearest-neighbour proxy in Architecture §12.4 is a validity metric only, not this gate.

---

## 8. Analytics, accessibility and performance

### 8.1 Privacy-preserving analytics and telemetry

| Rule | Detail |
|---|---|
| First-party only | No third-party analytics, ad pixels, session replay or fingerprinting. Events go to the Arena's own Postgres. |
| Minimal identifiers | Events keyed by a rotating session id; linked to `actor_id` only for actions that already require an account. IP addresses not stored; coarse country only if needed for abuse control. |
| Retention | Raw events 90 days *(default)*; then aggregated. |
| Reporting | Public or shared dashboards show aggregates only, k ≥ 50 where derived from users. |
| Consent | Product analytics are covered by the core consent; research use of reactions needs the separate research consent. |

**Event list (initial).**

| Event | Properties | Used for |
|---|---|---|
| `f60_step_viewed` | step (1–6), snapshot_id, elapsed_ms | Funnel, timing targets |
| `reaction_submitted` | statement_id, vote, guessed (bool), selection_reason | Deck quality, placement |
| `placement_shown` | uncertainty_band | Low-confidence rate |
| `thats_not_me` | screen | Self-recognition rate |
| `twist_shared` | include_placement (bool) | Share loop |
| `contribution_started` / `_submitted` | type, judgment_flag | G3 conversion |
| `fidelity_request_answered` | channel, cant_judge (bool) | Rater supply |
| `question_followed` | lifecycle_state | Living-map engagement |
| `clip_played` | from_surface | Verification behaviour |
| `dispute_submitted` | kind | Trust |
| `session_ended` | reason (`caught_up`, closed) | Finite-use guardrail |

### 8.2 Accessibility

- WCAG 2.2 AA across web surfaces.
- **Every map has an equivalent list/table view** (clusters, landmarks, questions, U matrix) reachable by keyboard and screen reader; the map is never the only path to information.
- Colour is never the only channel: hulls carry labels; U strips carry numbers on focus; status chips carry text.
- Full keyboard operation of the first-60 flow (A / D / P keys for agree / disagree / pass, with visible hints).
- `prefers-reduced-motion` respected: axis reorientation and lineage animations become cuts.
- Clip links open with captions where the host provides them; quote anchors are text, not images.
- Plain-language reading level for onboarding copy (aim for US grade 8).
- Touch targets ≥ 44 px; layouts work from 360 px wide.

### 8.3 Performance targets

| Surface / job | Target |
|---|---|
| First-60 landing (mid-range phone, 4G) | LCP ≤ 2.5 s; first statement interactive ≤ 3 s; JS for the first-60 route ≤ 200 KB gzipped |
| Reaction tap → reveal | ≤ 100 ms (local), reveal content prefetched |
| Placement after last reaction | ≤ 1 s p75 |
| Initial map snapshot bundle | ≤ 3 MB gzipped; landmarks and hulls first, propositions lazy-loaded |
| Map rendering | ≥ 50 fps desktop, ≥ 30 fps mid-range mobile with ≤ 5,000 points |
| API reads (p95) | ≤ 300 ms |
| Weekly S11 + S12 (Slice 1) | ≤ 2 h each on the box |
| Event map draft | ≤ 20 h from transcript availability to approval-ready |
| Takedown hot-fix | ≤ 24 h to public removal |
| Availability (beta) | Static map 99.5% monthly (static host); write API 99% during beta |

---

## 9. Risks, assumptions, dependencies and open questions

### 9.1 Top product risks (full register: synthesis §14)

| Risk | Synthesis ref | Likelihood / impact | PRD mitigation |
|---|---|---|---|
| Leaderboards create rivalry and new scapegoats | R19, R20, R35 | M / H | MOVE-03 safeguards (= SPINE §10: separate boards, pair-first, seasonal, decay, top-50 only, opt-in handles); SAFE-14; OD-09 |
| Too few placed users per cluster for fidelity sampling in a small beta | R39 | H / H | Fidelity minimum n = 5 *(default)*; "not enough signal" states; recruitment balance L8; ratifications labeled provisional until inter-rater reliability is shown |
| Reaction farming to enter a cluster and ratify or block | R51 | M / H | Random sampling; MOVE-06 AC3; placement-stability checks |
| Misquotation or out-of-context anchors on a landmark | R7, R46 | M / H | SAFE-01; eye-test claim spot-check; self-recognition; dispute SLAs |
| Launch defined by platforming accusations | R44 | M / H | SAFE-06, SAFE-23; first event map not incendiary |
| Landmark selection bias shapes the terrain | R48 | H / H | Published method; core panel; data-discovered clusters named; adjacent niches add real disagreement |
| Map contamination by agents | R27 | H / H | SAFE-09; human-only RCU |
| Expression moves, belief doesn't (performative ratification) | R38 | H / H | No reward for stance change; monthly reflexivity check in the deep pass (P5+, Should) |

### 9.2 Assumptions

| # | Assumption | If false |
|---|---|---|
| A1 | The slice scene will react and write in a private beta of 40–80 people at the P5 gate, growing toward 150–300 (OD-27). | Extend beta recruitment; lower fidelity n only with Benjamin's approval (OD-14). |
| A2 | Statement reactions place people stably with ~10 statements. | Increase deck size; show wider halos; PRD-SEE-01 AC6. |
| A3 | Captions exist for most selected episodes. | More ASR on the box; P1 timeline slips. |
| A4 | The Community Notes scorer adapts to cluster viewpoints with ≥ 2 dimensions. | Fall back to a simpler intercept model for P3, flagged in the gate report. |
| A5 | The GB10 box arrives about a month after 2026-10-31. | P4 waits; P3 beta prep continues. |
| A6 | Landmarks' public output is enough to place them faithfully. | Self-recognition fails → more episodes per landmark, or drop the landmark. |

### 9.3 Dependencies

| Dependency | Needed for | Status |
|---|---|---|
| Benjamin's 128 GB Blackwell box (GB10 class) | P4+ | Arriving ~late Nov 2026 |
| Claude subscription (Claude Code subagents) | Gold labels, battery, audits | Available |
| Topology Live ontology (`omniharmonic/antidebate-live/packages/ontology`) ported to Pydantic | Extraction schema | To port in P0 |
| `twitter/communitynotes` scorer code | MOVE-01 | Licence to confirm (UNVERIFIED Apache-2.0) |
| Static host for snapshots | P5 | Recommended Vercel (Architecture ADR-014); account creation and deploy need Benjamin's approval; open decision OD-10 |
| Write-API hosting for reactions, contributions and ratings | P3 internal (Tailscale only), P5 beta | The box never serves the public (06 doc §6); writes reach the box's API through a tunnel (Cloudflare Tunnel or Tailscale Funnel), with an off-box write buffer to revisit before any public launch: open decision **OD-10** (same item as Plan PD-11 and Architecture ADR-014) |
| Hermes operator agent | P4 | To configure |
| Personhood providers (Human Passport, World ID, in-person attestation) | P6 | To integrate |

### 9.4 Open decisions

All pending decisions (from the decisions log, this PRD, the Architecture and the Plan) are consolidated and numbered **OD-01 … OD-34** in **`10-OPEN-DECISIONS.md`**, with options, recommendation, what each blocks and its needed-by date. Until Benjamin decides, this PRD uses the default shown there. The ones this PRD raises or depends on most:

| OD | Decision | Default until decided | PRD features |
|---|---|---|---|
| OD-01, OD-02 | Exclusion review of the 15 flagged; conflict-of-interest sign-off | All 20 `public_surface_allowed = false` | ADM-02, SAFE-06, L5 |
| OD-05 | Confirm the 7 adjacent Slice 1 niches | Confirm | §7.1, L5 |
| OD-06, OD-07 | Girard in public framing; Jake Hartnell wording | Plain language; no text about him published | §5 copy |
| OD-08 | Randomized strategy assignment | Yes, simple block randomization | MKT-03 |
| OD-09 ⚑ | Public leaderboards (spec) vs. "no public leaderboards" (synthesis red line 19, A7); confirm the safeguards, season length and decay | Spec followed with the SPINE §10 safeguards; season = quarter; 180-day half-life | MOVE-03, AGT-05 |
| OD-10 | Beta deployment topology and write path | Vercel static host; tunnel to the API; no public endpoint on the box | PLAT-03, §9.3 |
| OD-14 | Ratification and fidelity-eligibility defaults for a small beta | `F ≥ 0.70`, n ≥ 5, `fidelity_lcb ≥ 0.60`; eligibility per MEET-04 AC1 | MEET-04, MEET-05 |
| OD-16 | Personhood proofs (T2) and agent-operator verification | T2 per Architecture §7.3; operators T3 | PLAT-02, AGT-02 |
| OD-19 | Public framing "ecology/commons of ideas" (synthesis Q1) | Not used in public copy | §1.4 |
| OD-20 | Onboarding deck size and placement minimum | 8–12 adaptive; ≥ 8 non-pass | SEE-01, SEE-02 |
| OD-21 | A permanently reward-free core of MEET (synthesis Q24) | Anti-debate invitations earn no reputation | MEET-07 |
| OD-22 | Self-negating escalation forecast (Q25) | Not built in Slice 1 | MKT |
| OD-23 | First event map to publish (Q31) | Benjamin picks from a P5 shortlist | MEET-06, SAFE-23 |
| OD-24 | Agent-free re-fit tolerances | ARI ≥ 0.90; max ΔU ≤ 0.10; eligibility ≥ 98% | SAFE-09 |
| OD-25 | Forecast accuracy in the single reputation score? | Separate forecast record | MKT-05 |
| OD-26 | Sign-in methods: add atproto OAuth? | Magic link + passkey only | PLAT-02 |
| OD-27 | Private beta size and composition | 40–80 in two waves for the P5 gate | §7.2 L8, A1 |
| OD-28 | Landmark self-recognition method | Judge check (A1) gates; insider panel optional | §7.4 |

**ID cross-reference** (earlier drafts of this PRD used D1–D8 and OQ-1–OQ-12): D1–D7 → OD-01–OD-07; D8 → OD-08; OQ-1 → OD-19; OQ-2 → OD-14; OQ-3 → OD-20; OQ-4 → OD-21; OQ-5 → OD-22; OQ-6 → OD-23; OQ-7 → OD-24; OQ-8 → OD-09; OQ-9 → OD-25; OQ-10 → OD-10; OQ-11 → OD-26; OQ-12 → OD-09.

---

## 10. Glossary

Spine §2 is the canonical glossary and is used verbatim: **niche, cluster, landmark, episode, appearance, encounter, segment, chunk, claim, proposition, stance, relation, layer, statement, reaction, contribution, rating, ratified, reputation, understanding matrix, strategy, forecast, snapshot, live question, operator agent, arena agent.** The terms below are the ones this PRD leans on most, plus its additions (marked †).

| Term | Meaning |
|---|---|
| Niche vs. cluster | Curated hypothesis from SEED-v4 (never changed by data) vs. data-derived group in a snapshot; linked by the crosswalk. |
| Stance | Actor × proposition × `affirm` / `reject` / `conditional` / `steelman_only`, with strength and `source` (`stated`, `implied_by_act`, `inferred`). Inferred stances are never scored. |
| Contribution | `note` (A describes B), `steelman` (A states B's strongest case) or `synthesis` (`bridge_proposal`, `better_question`, `clean_disagreement`). |
| Rating | `helpful` 1.0 / `somewhat` 0.5 / `not_helpful` 0.0, plus a `fidelity` vote on the same scale from raters placed in the described cluster (mostly randomly sampled). |
| Ratified | Fidelity from the described cluster passes the threshold (`F ≥ 0.70`, ≥ 5 raters, `fidelity_lcb ≥ 0.60` by default; OD-14). Stored as `contribution.status` `ratified` or `ratified_helpful`. |
| Reputation | One public score per actor: writer impact plus synthesis credit plus capped rater helpfulness (Architecture §4.12.2). |
| Understanding matrix (U) | U[A][B] = ratified-description quality of cluster A's contributions about cluster B. |
| Meta-consensus | Clusters can describe each other in terms the described side would sign. Not convergence. |
| Reciprocal opening | Ranking by what widens the set of clusters a person can accurately describe (Vervaeke's term; the feed application is Benjamin's extension). |
| Threshold reveal / twist card | First-60 screens 4 and 5 (§4.1). |
| RCU † / mutual pair † | North-star metric (§2.3) / an unordered cluster pair covered in both directions. |
| Synthesis-eligible † | A cluster pair with ratified steelmen in both directions. |
| Eye test † | Benjamin's blind cluster-validity review (§7.3). |
| Steward † | A human with console rights: Benjamin and delegates he names. |
| Forecast record † | A forecaster's public accuracy history, separate from reputation pending OD-25. |

---

## Spine extensions

> **Consolidated:** these extensions, deduplicated with the Architecture's and the Plan's, are now part of the spine as `design-spine/SPINE.md` §10 (adopted 2026-10-31). SPINE §10 is authoritative; this list is kept for traceability. In the 2026-10-31 review, names that the Architecture's schema already defined (contribution, rating, forecast, agent and landmark fields; status values; identity tiers) were aligned to the Architecture, as noted per row.

Additions this PRD needed that are not in the original spine (§1–§9).

| # | Extension | Where used | Notes |
|---|---|---|---|
| E1 | Priority labels **Must / Should / Could** for features | §4 | Avoids collision with phase names P0–P7. |
| E2 | Requirement ID scheme `PRD-<AREA>-<NN>` with areas SEE, MEET, MOVE, PUB, AGT, MKT, ADM, DATA, PLAT, SAFE | Whole doc | |
| E3 | **RCU** north-star metric, **mutual pair**, RCU-agent, and the guardrail set | §2.3 | Human-only by default. |
| E4 | Contribution fields as in Architecture §3.3 (`contribution`): `kind`, `synthesis_subtype` (`bridge_proposal` / `better_question` / `clean_disagreement`), `author_user_id`, `author_actor_kind`, `author_cluster_id` (for agents: the declared audience cluster), `author_snapshot_id`, `target_cluster_id`, `second_cluster_id` (synthesis), `live_question_id`, `cited_claim_ids[]`, `agent_drafted`, `agent_id`, `judgment_flag`, `parent_contribution_id`, `status` | §4.4, §4.12 | Aligned to 08 (was `contribution_type`, `third_position`, `author_actor_*`, `audience_cluster_id`, `cited_anchor_ids`). `judgment_flag` was added to the 08 DDL for this PRD. |
| E5 | Contribution status values: stored `needs_ratings`, `ratified`, `helpful`, `ratified_helpful`, `not_helpful`, `split_detected`, `withdrawn`, `removed`; display chips "Not yet ratified", "Ratified by B", "B is split", "Anchor disputed" (an open-flag overlay) | §4.4 | Aligned to 08 (was `not_yet_ratified`, `ratified_by_B`, `B_split`, `anchor_disputed` as stored values). |
| E6 | Rating fields as in Architecture §3.3 (`rating`): `helpfulness`, `fidelity` (same three-value scale, shown as Accurate / Partly / Not accurate; "can't judge" stores no fidelity), `tags`, `sampled`, `rater_snapshot_id`, `rater_cluster_id` | §4.4, §4.12 | Aligned to 08 (was `channel`, a four-value fidelity scale, `value`, `sealed_until`). |
| E7 | Landmark fields `public_surface_allowed` (boolean) and `flag_type` (`exclusion-review` / `minor-adjacent` / `conflict-of-interest`) | §4.9, §6 | Aligned to 08 (was a three-value `public_visibility`). |
| E8 | Identity tiers T0 visitor, T1 account, T2 ratifier, T3 verified public identity; agent account kind; steward/admin role | §4.11 | Aligned to 08 §7.3. |
| E9 | Fidelity eligibility and sampling parameters: `eligible_to_ratify` rules (≥ 12 non-pass reactions from ≥ 3 clusters' splitter sets, posterior ≥ 0.6, T2, no coordination flag), target 7 sampled invitations, self-selected ≤ 50%, ratify at `F ≥ 0.70`, n ≥ 5, `fidelity_lcb ≥ 0.60` | §4.4 | Configuration, not code; OD-14. Aligned to 08. |
| E10 | Forecast fields as in Architecture §3.3 / §9.2 (`forecast`): `window_id`, `question_key` (`dU:…`, `win:…`, `dRep:…`), `commitment`, `revealed_payload` (binary `p` or quantiles q10/q50/q90), `revealed_salt`, `reveal_valid`, `resolution_value`, `score`; **forecast record** | §4.8, §4.12 | Aligned to 08 (was a 5-bin format scored by RPS). Forecast record stays outside reputation pending OD-25. |
| E11 | Agent registry entry: `agent_id`, `name`, operator handle and tier, `model_disclosure`, `prompt_hash`, `prompt_url`, `charter_version`, `strategy`, `scope`, `aim_statement`, `platforms`, `status`, `reward_eligible`, `directional_audit`, `action_log_url` | §4.7, §4.12 | No bond in Slice 1. Prompt hash and published prompt added to 08 §9.1 for this PRD. |
| E12 | Season (calendar quarter) and decay half-life (180 days) for leaderboards | §4.5 | Part of the leaderboard safeguards (SPINE §10; OD-09). |
| E13 | Onboarding deck: 8–12 statements chosen adaptively by expected information gain; placement minimum 8 non-pass reactions | §4.1 | OD-20. Aligned to 08 §4.11.1 / §8.4 (was a fixed 10-statement 4/3/3 deck). |
| E14 | Steward role, publish-approval records (`admin_approval`) and standing approvals | §4.9 | |
| E15 | Agent-free re-fit tolerances (ARI ≥ 0.90; max ΔU ≤ 0.10; eligibility identical for ≥ 98% of users) | §6 | OD-24. Aligned to 08 §9.1 (was ΔU ≤ 0.05). |
| E16 | Live-question wording neutrality check ("fair wording" ≥ 0.6 from origin and one other cluster) | §4.2 | |
