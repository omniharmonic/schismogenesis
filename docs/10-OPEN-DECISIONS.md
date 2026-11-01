# Dialogos Arena: Open Decisions (consolidated)

*Benjamin Life (@omniharmonic) · consolidated 2026-10-31 · status: 35 open decisions*

This is the **single list** of decisions waiting on Benjamin. It merges and deduplicates the pending items in `02-DECISIONS-LOG.md`, `07-PRD.md` (D1–D8, OQ-1–OQ-12), `08-TECHNICAL-ARCHITECTURE.md` (decisions deferred in the text and ADRs) and `09-IMPLEMENTATION-PLAN.md` (PD-1–PD-15 and the data model's OPEN items it uses). Every other doc now refers to these by **OD-ID**.

**How to use it.** Each entry gives the question, the options, the recommendation (the default the swarm uses until Benjamin decides), what it blocks, and a needed-by date where the Plan gives one (otherwise the phase or event). When Benjamin decides, record the decision in `02-DECISIONS-LOG.md` (as a new D-entry) and mark the OD here as decided; do not renumber.

**Needed-by dates** come from the Plan's calendar (P0 starts 2026-11-02; P2 gate 2026-11-28; P3 gate 2026-12-06; P5 2026-12-28 → 2027-01-31; P6 from 2027-02-01; P7 from 2027-03-15). They are targets and move with the box arrival date.

## Summary by needed-by date

| OD | Decision | Needed by |
|---|---|---|
| OD-05 | Confirm the 7 adjacent Slice 1 niches | ✅ **DECIDED 2026-10-31** (D-31.9) |
| OD-11 | Pre-box ingest host (home Mac Mini) | **2026-11-03** |
| OD-12 | Create the free API keys and accounts | **2026-11-03** |
| OD-35 | Tilt the pilot toward worldview-shaping thinkers | Before P1 discovery starts |
| OD-04 | Bridger rule | 2026-11-17 |
| OD-18 | Hardware purchases (UPS, optional SSD) | 2026-11-23 |
| OD-02 | Conflict-of-interest sign-off | Brad Carson 2026-11-28; others before P7 |
| OD-13 | Sign the P4 extraction threshold sheet | 2026-11-28 (P2 gate) |
| OD-28 | Landmark self-recognition method | 2026-12-02 |
| OD-14 | Ratification and fidelity-eligibility defaults | 2026-12-06 (P3 gate) |
| OD-20 | Onboarding deck size and placement minimum | 2026-12-06 (P3 gate) |
| OD-29 | Niche names vs cluster names on the public map | 2026-12-06 (P3 gate) |
| OD-30 | Season-0 core panel | 2026-12-06 (P3 gate) |
| OD-32 | Speaker-confidence threshold for publication | 2026-12-15 (P4 backfill) |
| OD-34 | Listen Notes paid tier | after the P1 discovery check (2026-11-21) |
| OD-09 | Public leaderboards and their safeguards | 2027-01-04 |
| OD-10 | Beta deployment topology and write path | 2027-01-04 |
| OD-27 | Private beta size and composition | 2027-01-04 |
| OD-24 | Agent-free re-fit tolerances | 2027-01-04 (first gated release) |
| OD-26 | Sign-in methods (atproto OAuth?) | 2027-01-04 |
| OD-15 | Courtesy notice to slice landmarks | 2027-01-11 |
| OD-06 | Girard in public framing | before P5 copy review (≈ 2027-01-04) |
| OD-07 | Jake Hartnell wording | before P5 copy review (≈ 2027-01-04) |
| OD-19 | Public framing "ecology/commons of ideas" | before P5 copy review (≈ 2027-01-04) |
| OD-33 | Parachute sync | 2027-01-04 (P5-W4-04) |
| OD-23 | First event map to publish | during P5 (before the first event map, ≈ 2027-01-18) |
| OD-08 | Randomized strategy assignment | 2027-02-01 |
| OD-16 | Personhood proofs and agent-operator verification | 2027-02-01 (T2 proofs needed earlier, by the beta) |
| OD-21 | Reward-free core of MEET | 2027-02-01 (P6) |
| OD-22 | Self-negating escalation forecast | 2027-02-01 (P6) |
| OD-25 | Forecast accuracy in reputation? | 2027-02-01 (P6) |
| OD-17 | YouTube API quota increase | ≈ 2027-02-22 (3 weeks before P7) |
| OD-31 | Baseline hours per niche (P7 value) | 2027-03-15 (P7) |
| OD-01 | Exclusion review of the 15 flagged landmarks | before the first P7 batch containing one |
| OD-03 | Outside reviewers for 7 niches near Benjamin's work | before those P7 batches |

---

## From the decisions log (Benjamin's pending list)

### OD-01 · Exclusion review: the 15 flagged landmarks
- **Question.** What happens to the 15 flagged landmarks (14 `exclusion-review`, e.g. Fuentes, the Tates, Gaines, Jones, Loomer, Hinkle, Haz Al-Din, Umar Johnson; and 1 `minor-adjacent`)?
- **Options.** (a) Keep in the private dataset, excluded from public surfaces at launch; (b) remove from the dataset; (c) review individually and admit some publicly.
- **Recommendation.** (a). They load with `public_surface_allowed = false`.
- **Blocks.** Visibility changes (PRD-ADM-02, SAFE-06); P7 batches that contain them (d1, d6, …).
- **Needed by.** Before the first P7 batch with a flagged landmark (P7 from 2027-03-15).
- **Was.** 02 pending #1; PRD D1; Plan PD-1.

### OD-02 · Conflict-of-interest sign-off
- **Question.** Keep Samantha Power (The BioFi Project), Monty Bryant, Kevin Owocki and Griff Green as landmarks, and Brad Carson (reported Anthropic funding, unverified)?
- **Options.** Keep / drop / keep with a public COI note, per person.
- **Recommendation.** Brad Carson (in the slice): crawl privately; decide before P3 public-facing cards. Others: decide before P7. All five stay `public_surface_allowed = false` until signed off.
- **Blocks.** P3-W4-05/06 cards for `populist-ai-backlash`; P5 beta surfaces; P7 Regens/ReFi batch; PRD-ADM-02 AC4; launch criterion L5.
- **Needed by.** Brad Carson 2026-11-28; others before P7.
- **Was.** 02 #2; PRD D2; Plan PD-2.

### OD-03 · Outside reviewers for 7 niches near Benjamin's work
- **Question.** Who reviews Regens/ReFi, Metacrisis, Bioregionalism, Metamodernism, Deliberative democracy & civic tech, Tribal nations and Land Back?
- **Options.** Name 1–2 reviewers per niche; or defer those niches.
- **Recommendation.** Name 1–2 reviewers per niche; those batches wait for them.
- **Blocks.** PRD-ADM-03; P7 batches with those niches.
- **Needed by.** Before those P7 batches.
- **Was.** 02 #3; PRD D3; Plan PD-3.

### OD-04 · Bridger rule
- **Question.** Can an edge voice fill a niche's bridger slot?
- **Options.** Yes / no / yes if marked and not counted as core.
- **Recommendation.** Yes, if marked and not counted as core.
- **Blocks.** P1-W2-09 selection constraint ("≥ 1 encounter per niche involving a core landmark"); core-panel composition; P7 seed additions.
- **Needed by.** 2026-11-17 (P1 selection).
- **Was.** 02 #4; PRD D4; Plan PD-4.

### OD-05 · Confirm the 7 adjacent Slice 1 niches — ✅ DECIDED 2026-10-31
- **Decision.** All 7 approved; bayeslord added to e/acc; priority encounter PE-01 (e/acc × d/acc). See `02-DECISIONS-LOG.md` D-31.9.
- **Question.** Confirm `agi-frontier-builders`, `ai-ethics-critics`, `dacc-pluralist-tech`, `forecasters-prediction-markets`, `populist-ai-backlash`, `neoreaction-vitalist-right`, `progress-studies-abundance`?
- **Options.** Confirm all; confirm a subset; swap some.
- **Recommendation.** Confirm all 7 (they supply real disagreement). Until then, crawl the 8 core niches first.
- **Blocks.** P1-W2-01/03/04 for 24 adjacent landmarks; P2 gold strata; P3 clusters; PRD §7.1, L5.
- **Needed by.** **2026-11-03.**
- **Was.** 02 #5; PRD D5; Plan PD-5.

### OD-06 · Girard in public framing
- **Question.** Name Girard, or say "rivalry and scapegoating" plainly (synthesis Q30)?
- **Options.** Name him; plain language; middle path (plain language, Girard credited on the methods page).
- **Recommendation.** Plain language at launch.
- **Blocks.** Public copy (PRD §5), P5-W6-01, beta materials.
- **Needed by.** Before P5 copy review (≈ 2027-01-04).
- **Was.** 02 #6; PRD D6; Plan PD-6.

### OD-07 · Jake Hartnell's hyperstition position
- **Question.** How is his position described before anything is published?
- **Options.** Benjamin approves exact text; omit the reference.
- **Recommendation.** Benjamin reviews the exact text (synthesis §10.5 wording as the starting point).
- **Blocks.** Any public text mentioning him (P5 copy, landmark notice P5-LD-02).
- **Needed by.** Before P5 copy review (≈ 2027-01-04).
- **Was.** 02 #7; PRD D7; Plan PD-7.

### OD-08 · Randomize which strategy runs on which cluster pair? (D-31.2, engineering)
- **Question.** Randomize strategy × cluster-pair assignment in the strategy market?
- **Options.** No randomization; simple block randomization; inverse-probability designs with full support.
- **Recommendation.** Yes, simple: block-randomized per 4-week window with a committed seed (Architecture §9.2, ADR-023). Adopted provisionally in PRD-MKT-03.
- **Blocks.** P6-W5-05; PRD-MKT-03; P6 gate.
- **Needed by.** 2027-02-01 (P6).
- **Was.** D-31.2 open item; PRD D8; Architecture §9.2.

## Raised by the PRD, Architecture and Plan

### OD-09 · Public leaderboards (spec) vs "no public leaderboard" (synthesis red line 19), and the safeguards
- **Question.** The locked spec (§8) and D-31.1/D-31.3 require public leaderboards for people and agents; the synthesis (red line 19, A7, §10.2) said no public leaderboards because rankable status invites rivalry. By precedence the spec wins. Does Benjamin confirm the safeguards, including season length and decay?
- **Options.** (a) Spec with the SPINE §10.5 safeguards; (b) spec with stronger limits (e.g. pair views only, no global board); (c) ask to amend the spec (no leaderboards).
- **Recommendation.** (a): separate People and Agents boards; per-cluster-pair default view; seasonal (calendar quarter) with a 180-day half-life; only the top 50 numbered, others see their band; ranked by reputation only (never volume, reach, followers or stance location; no cluster ranking; no developmental ranking); opt-in handles only.
- **Blocks.** PRD-MOVE-03, AGT-05; Architecture §4.12.2, §7.2 (`/v1/leaderboards`), bundle `leaderboards.json`; Plan P5-W6-01, P6-W5-03.
- **Needed by.** 2027-01-04 (before leaderboards appear to beta users).
- **Was.** PRD OQ-8 and OQ-12; Architecture conflict flag 1.

### OD-10 · Beta deployment topology and write path
- **Question.** The box never serves the public. Where do the static bundles and web app live, and how do beta writes (reactions, contributions, ratings, flags) reach the box's API?
- **Options.** Static host: Vercel / Cloudflare Pages / GitHub Pages. Write path: Cloudflare Tunnel; Tailscale Funnel; an off-box write buffer (a small hosted API that queues writes for the box to pull).
- **Recommendation.** Vercel for the static bundles and web app (Architecture ADR-014); a rate-limited tunnel to the API only, invite-only for the private beta; revisit an off-box write buffer before any public launch. Account creation and any deploy need Benjamin's approval (Plan H2, H3).
- **Blocks.** PRD §9.3 dependencies, PLAT-03; Architecture §1.2, §1.3, §10.5, ADR-014; Plan P5-W1-01, P5-W7-02.
- **Needed by.** 2027-01-04.
- **Was.** PRD OQ-10; Plan PD-11; Architecture ADR-014 ("decided at P5").

### OD-11 · Pre-box ingest host
- **Question.** The Plan assumes Benjamin has an always-on home **Mac Mini** to run the long caption fetch and crawl from a residential connection before the box arrives. Is that true, and may it be used?
- **Options.** (a) Mac Mini (Docker, Tailscale, `discover`/`fetch` queues); (b) another always-on home machine; (c) Claude Code cloud sessions with checkpointing (slower, more block-prone, egress proxy limits).
- **Recommendation.** (a) if the machine exists and is available; otherwise (b), then (c). Recorded as ADR-028. Note: only doc 05 Q15 mentions a home Mac Mini (as a database-host option); nothing else confirms it.
- **Blocks.** P0-W7-03, G0.9, P1-W2-10 caption fetch (critical path), R-E1/R-E2; Architecture §1.3.
- **Needed by.** **2026-11-03.**
- **Was.** Plan PD-8.

### OD-12 · Free API keys and accounts
- **Question.** Create the YouTube Data API key (Google Cloud project), the Podcast Index key and secret, and a Hugging Face token (pyannote terms) in Benjamin's name?
- **Options.** Yes; defer (crawl and ASR wait).
- **Recommendation.** Yes; the swarm guides, Benjamin owns them (~20 min).
- **Blocks.** P0-B-01; P1-W2-01/03/04; P4-W2-01.
- **Needed by.** **2026-11-03.**
- **Was.** Plan PD-9; Architecture §4.1 "keys needed".

### OD-13 · Sign the P4 extraction threshold sheet
- **Question.** Which thresholds must local models meet on the sealed gold-test set to take over bulk extraction?
- **Options.** The Plan §4.2 sheet as proposed; stricter; looser; a documented hybrid (local anchoring/tagging/dedup, Claude neutral rewrite on a capped slice; needs a subscription-budget check because D-31.7 rules out Claude for bulk extraction).
- **Recommendation.** The Plan §4.2 sheet (M1 ≥ 0.85 of Claude's M1 and ≥ 0.75 absolute; M2 ≥ 0.85; M3 ≥ 0.90; M4 ≥ 0.75; M5 ≥ 0.85; M6 ≥ 95% with M6b = 100%; M7 ≤ 2%; M9 ≥ 0.90; downstream ARI ≥ 0.70; ≤ 120 box-seconds per transcript hour). Architecture §12.3 maps to these IDs; later changes need an ADR he approves.
- **Blocks.** P2 gate G2.7; P4 cutover (P4-LD-01, G4.2); PRD §2.4 P2/P4 rows.
- **Needed by.** 2026-11-28 (P2 gate).
- **Was.** Plan PD-10; Architecture §12.3 "Benjamin sets final".

### OD-14 · Ratification and fidelity-eligibility defaults
- **Question.** Are the defaults right for a small beta, and who may change them?
- **Options.** As below; lower n for a small beta; stricter eligibility.
- **Recommendation.** Ratified when `F ≥ 0.70` from ≥ 5 fidelity raters placed in B with `fidelity_lcb ≥ 0.60`; eligibility: person at T2, ≥ 12 non-pass reactions from ≥ 3 clusters' splitter sets, primary posterior ≥ 0.6, no coordination flag, not the author; fidelity raters mostly random invitations (target 7), self-selected ≤ 50%. Values live in configuration; **only Benjamin changes them, via an ADR**.
- **Blocks.** PRD-MEET-04, MEET-05; Architecture §4.11 step 6, §4.12.2; Plan P3-W5-02, P3 gate, P5-W5-01.
- **Needed by.** 2026-12-06 (P3 gate).
- **Was.** PRD OQ-2 (whose 0.70 / n ≥ 5 values were kept; its ≥ 20-reaction, membership ≥ 0.5 eligibility was aligned to the Architecture).

### OD-15 · Private courtesy notice to slice landmarks before the beta
- **Question.** Send slice landmarks a short private note with the dispute link before or at the beta?
- **Options.** Yes (Benjamin sends); no; only to landmarks who will be most visible.
- **Recommendation.** Yes, short and private, sent by Benjamin.
- **Blocks.** P5-LD-02; PRD §7.4 stage B.
- **Needed by.** 2027-01-11.
- **Was.** Plan PD-12.

### OD-16 · Personhood proofs (T2) and Arena-agent operator verification
- **Question.** Which personhood proofs count for T2 (ratifiers, writers, forecasters), and how are agent operators verified?
- **Options.** T2: vouches from two T2+ users in different clusters; in-person check at an Arena event; external attestation (Human Passport, World ID, BrightID-style). Operators: T3 (T2 + proof of a public identity); a lighter "verified social account + signed charter".
- **Recommendation.** T2 per Architecture §7.3 with vouching and in-person checks first; any external provider only after Benjamin's approval and a privacy review. Operators are T3 and sign the charter.
- **Blocks.** PRD-PLAT-02, AGT-02; Architecture §7.3, ADR-021; Plan P6-W5-01 (and T2 rating during the beta).
- **Needed by.** 2027-02-01 for operators; T2 proof methods before beta ratings (≈ 2027-01-18).
- **Was.** Plan PD-13; PRD AGT-02 AC1; Architecture §7.3 provider approval.

### OD-17 · YouTube API quota increase application
- **Question.** File a quota increase (outward-facing)?
- **Options.** File before P7; file now; do not file.
- **Recommendation.** File about 3 weeks before P7 if a batch needs > 10,000 units/day.
- **Blocks.** P7 crawl speed.
- **Needed by.** ≈ 2027-02-22.
- **Was.** Plan PD-14.

### OD-18 · Hardware purchases
- **Question.** Buy a UPS for the box, and optionally an external SSD for model weights?
- **Options.** UPS yes/no; SSD yes/no.
- **Recommendation.** UPS yes (~$100–250); SSD optional (~$100–300).
- **Blocks.** P4 resilience; pre-fetching weights.
- **Needed by.** 2026-11-23.
- **Was.** Plan PD-15.

### OD-19 · Public framing "ecology/commons of ideas"
- **Question.** Use "ecology/commons of ideas" in public copy (synthesis Q1)?
- **Options.** Yes; no; another phrase.
- **Recommendation.** Not in public copy until Benjamin confirms.
- **Blocks.** PRD §1.4 public copy; P5 materials.
- **Needed by.** Before P5 copy review (≈ 2027-01-04).
- **Was.** PRD OQ-1.

### OD-20 · Onboarding deck size and placement minimum
- **Question.** How many statements, and how many non-pass reactions before placement?
- **Options.** Fixed 10-statement deck; adaptive 8–12 by expected information gain.
- **Recommendation.** Adaptive 8–12 (Architecture §4.11.1, §8.4); place after ≥ 8 non-pass reactions once the top posterior ≥ 0.8, or at 12.
- **Blocks.** PRD-SEE-01, SEE-02; Plan P3-W6-01.
- **Needed by.** 2026-12-06 (P3 gate).
- **Was.** PRD OQ-3.

### OD-21 · A permanently reward-free core of MEET?
- **Question.** Should some MEET activity (e.g. anti-debate invitations) never earn reputation (synthesis Q24)?
- **Options.** Yes; no.
- **Recommendation.** Yes for anti-debate invitations.
- **Blocks.** PRD-MEET-07; scorer scope.
- **Needed by.** 2027-02-01 (P6).
- **Was.** PRD OQ-4.

### OD-22 · Self-negating escalation forecast for participants only?
- **Question.** Build the self-negating escalation forecast (synthesis Q25)?
- **Options.** Build for participants only; do not build.
- **Recommendation.** Not built in Slice 1.
- **Blocks.** Strategy market scope.
- **Needed by.** 2027-02-01 (P6).
- **Was.** PRD OQ-5.

### OD-23 · First event map to publish
- **Question.** Which encounter becomes the first beta-visible event map (synthesis Q31)?
- **Options.** A live P5 encounter from the nightly delta; the best backfilled encounter, labelled "retrospective".
- **Recommendation.** Benjamin picks from a swarm shortlist; "surprising but less incendiary". **Leading candidate: PE-01, e/acc × d/acc (Beff Jezos × Vitalik Buterin), per D-31.9.**
- **Blocks.** PRD-MEET-06, SAFE-23; Plan P5-W4-03, G5.3.
- **Needed by.** During P5, before the first event map (≈ 2027-01-18).
- **Was.** PRD OQ-6.

### OD-24 · Agent-free re-fit tolerances
- **Question.** How close must the agent-free re-fit be to the full snapshot for release?
- **Options.** ARI ≥ 0.90 with ΔU ≤ 0.05 (earlier PRD draft); ARI ≥ 0.90, max ΔU ≤ 0.10 and ≥ 98% identical eligibility (Architecture).
- **Recommendation.** Architecture values (§9.1, ADR-027). On failure, publication is blocked, an incident opens, and the steward may approve the agent-free version.
- **Blocks.** PRD-SAFE-09; Plan P6-W4-01; release gate.
- **Needed by.** Before the first gated release (≈ 2027-01-04; binding from P6).
- **Was.** PRD OQ-7.

### OD-25 · Does forecast accuracy feed the single reputation score?
- **Question.** One score, or a separate forecast record?
- **Options.** Separate record; blend into reputation.
- **Recommendation.** Separate forecast record (forecaster track).
- **Blocks.** PRD-MKT-05; Architecture §9.2; Plan P6-W5-06.
- **Needed by.** 2027-02-01 (P6).
- **Was.** PRD OQ-9.

### OD-26 · Sign-in methods
- **Question.** Email magic link and passkeys only, or also atproto OAuth?
- **Options.** Magic link + passkey; add atproto OAuth.
- **Recommendation.** Magic link + passkey (Architecture §7.3, §11.4) for Slice 1; consider atproto later.
- **Blocks.** PRD-PLAT-02; Architecture §7.2 auth endpoints.
- **Needed by.** 2027-01-04.
- **Was.** PRD OQ-11.

### OD-27 · Private beta size and composition
- **Question.** The PRD targeted 150–300 invitees with week-8 health targets in the P5 gate; the Plan invites 40–80 and gates P5 after two weeks. Which?
- **Options.** 40–80 in two waves for the P5 gate, then grow; 150–300 from the start (P5 gate moves later).
- **Recommendation.** 40–80 in two waves (≥ 4 per data-derived cluster; no niche above 20%) for the P5 gate; grow toward 150–300 afterwards; the PRD's week-8 health targets are tracked after the gate.
- **Blocks.** PRD §2.4 P5, §7.2 L8, A1; Plan P5-LD-01, G5.4.
- **Needed by.** 2027-01-04.
- **Was.** New (PRD vs Plan conflict found in review).

### OD-28 · Landmark self-recognition method
- **Question.** The PRD's P3 gate used three private niche insiders per niche (≥ 70% "they'd sign"); the Plan used judge subagents checking each profile against the landmark's other public writing (≥ 85% yes/partly, 0 misattributions). Which gates P3?
- **Options.** Judge check only; insider panel only; both.
- **Recommendation.** Judge check (PRD §7.4 stage A1) gates P3; the insider panel (A2) is optional because recruiting insiders is outward-facing.
- **Blocks.** PRD §2.4 P3, §7.2 L4, §7.4; Plan P3-W3-01, G3.6; Architecture §12.4.
- **Needed by.** 2026-12-02 (start of the P3 review).
- **Was.** New (PRD vs Plan conflict found in review).

## Data-model open items used by the Plan and Architecture (from doc 05)

### OD-29 · Niche names vs cluster names on the public map
- **Question.** Show curated niche names or only data-derived clusters?
- **Options.** Niche names as provisional labels; neutral cluster numbers; ratified labels only.
- **Recommendation.** Data clusters as the shapes; best-aligned niche name as a provisional label until a ratified label exists.
- **Blocks.** Plan P3-W4-03, P5-W6-01; Architecture §4.11 step 7; PRD-SEE-04 AC4, SEE-10.
- **Needed by.** 2026-12-06 (P3 gate).
- **Was.** 05 OPEN-1.

### OD-30 · Season-0 core panel
- **Question.** Which landmarks form the stable core panel?
- **Options.** All seed landmarks; verified-active and unflagged only.
- **Recommendation.** Verified-active, unflagged landmarks; the rest enter as marked newcomers.
- **Blocks.** Plan P3-W4-01 (movement stats), P5-W4-01 (lineage); Architecture §4.11.
- **Needed by.** 2026-12-06 (P3 gate).
- **Was.** 05 OPEN-2.

### OD-31 · Baseline hours per niche
- **Question.** Solo-baseline budget per niche.
- **Options.** 15 h (slice) / 30 h (full seed); other values once yield per hour is measured.
- **Recommendation.** 15 h for Slice 1; 30 h for P7 batches; revisit after P2.
- **Blocks.** Plan P1-W2-09, P7 batches; Architecture §4.3 (`sampling_budget_hours`).
- **Needed by.** Slice value in use now; P7 value by 2027-03-15.
- **Was.** 05 OPEN-3.

### OD-32 · Speaker-confidence threshold for publication
- **Question.** Minimum speaker-attribution confidence for a published quote.
- **Options.** 0.9 publish / 0.7–0.9 internal / < 0.7 discard; stricter.
- **Recommendation.** 0.9 to publish; 0.7–0.9 internal only; below 0.7 discarded.
- **Blocks.** Plan P4-W2-01, P5 publication; Architecture §4.4, §4.5, §4.13.
- **Needed by.** 2026-12-15 (P4 backfill).
- **Was.** 05 OPEN-6.

### OD-33 · Parachute sync
- **Question.** What flows into Benjamin's Parachute vault?
- **Options.** One-way weekly publish under `#arena/*`; two-way sync; none.
- **Recommendation.** One-way weekly publish of reports and cards; Postgres stays the operational store; nothing flows back.
- **Blocks.** Plan P5-W4-04; Architecture §11.1 (private-vault red line).
- **Needed by.** 2027-01-04.
- **Was.** 05 OPEN-9.

### OD-34 · Listen Notes paid tier
- **Question.** Pay for Listen Notes for guest-appearance discovery?
- **Options.** Yes; no.
- **Recommendation.** Decide after the P1 discovery check; only if recall < 0.8 without it (paid, so it needs approval).
- **Blocks.** P1 discovery recall (G1.2); Plan §6 budget.
- **Needed by.** After the P1 discovery check (≈ 2026-11-21).
- **Was.** Architecture §4.1 ("decision after P1"); 05 Q9.

### OD-35 · Tilt the pilot toward the thinkers directing technology and society
- **Question.** Should Slice 1 centre the people whose worldviews most directly steer technology and society, drawing on their written work and intellectual lineages (Thiel-Karp genealogy, Parachute vault), so that those worldviews become visible rather than operating unseen?
- **Options.** (a) Keep Slice 1 and add a written-first worldview core: add Alex Karp and a few others, and pull their written corpora first. (b) Replace Slice 1 with that core. (c) No change.
- **Recommendation.** (a). Four of the central figures are already in the slice. Living figures are placed on the map; deceased thinkers (Girard, Strauss, Schmitt and others) enter as lineage, not as placed landmarks, because they cannot dispute a placement or ratify a description. Influence links use the genealogy's four evidence types.
- **Blocks.** P1 discovery scope; slice counts in `arena seed verify`; P2 gold strata; a spec §2 amendment if adopted.
- **Needed by.** Before P1 discovery starts.
- **Was.** New (Benjamin, 2026-10-31).

---

## Cross-reference: old IDs → OD

| Source | Old ID | OD |
|---|---|---|
| `02-DECISIONS-LOG.md` pending list | 1, 2, 3, 4, 5, 6, 7 | OD-01 … OD-07 |
| PRD §9.4 | D1–D7; D8 | OD-01–OD-07; OD-08 |
| PRD §9.5 | OQ-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | OD-19, 14, 20, 21, 22, 23, 24, 09, 25, 10, 26, 09 |
| Plan §8 | PD-1…PD-7; PD-8; PD-9; PD-10; PD-11; PD-12; PD-13; PD-14; PD-15 | OD-01…OD-07; OD-11; OD-12; OD-13; OD-10; OD-15; OD-16; OD-17; OD-18 |
| Plan §8 (data model) | OPEN-1, 2, 3, 6, 9 | OD-29, 30, 31, 32, 33 |
| Architecture | conflict flag 1; ADR-014 tunnel; ADR-023 randomization; §4.1 Listen Notes; §7.3 providers; §12.3 thresholds | OD-09; OD-10; OD-08; OD-34; OD-16; OD-13 |
