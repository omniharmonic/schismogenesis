# Dialogos Arena — Build Spec v1 (Slice 1)

Author: Benjamin Life (@omniharmonic). Locked 2026-10-31; §3 and §9 amended the same day (D-31.10, D-31.11). Supersedes earlier drafts where they conflict.

## 1. Purpose

Internet-native democratic infrastructure: map the living topology of memetic space (SEE), scaffold dialogos across clusters (MEET), and reward people and agents for helping clusters understand each other (MOVE). Success is meta-consensus — clusters able to describe each other in terms the described side would sign — not convergence.

## 2. Slice 1 scope

Start narrow and granular, verify the whole system works, then expand.

- **Niches:** rationalists, AI safety, accelerationists / e/acc, techno-optimists, and the terminally-online subcultures connected to them (post-rationalists/TPOT, effective altruism, tech right, degens/Milady-adjacent, etc., drawn from SEED-v4).
- **Why this scene first:** they argue in public, care about mechanism design, and will stress-test the system.
- **Landmarks:** roughly 30–60 from SEED-v4 for these niches.
- **Expansion:** broader cultural niches only after the slice passes its tests.

## 3. Extraction pipeline (claim-first, granular)

Decision: full claim extraction and connection, not question-first scoring. The small slice lets us afford accuracy.

1. **Discovery:** per-landmark crawl of own-show episodes and guest appearances; build the encounter graph.
2. **Transcripts and texts:** existing captions/publisher transcripts first; local ASR + diarization for the rest; speakers named via accumulated voiceprints. Written works (books, essays, blogs, letters, dissertations) are sources on equal footing, located by page or paragraph instead of timestamp. (Amended 2026-10-31, D-31.10.)
3. **Claim extraction:** narrow steps on short chunks. Each claim must carry an exact supporting quote, verified in code; an entailment check confirms the quote supports the claim; unsupported claims are discarded.
4. **Normalization:** each claim rewritten as a neutral, speaker-independent proposition and merged into a shared proposition bank (embedding candidates + model-confirmed merges).
5. **Connection:** per-person stances on propositions; relations between propositions (supports, contradicts, depends on, reframes); layer tags (ontological, epistemic, axiological, empirical, praxis); every item links to its source clip.
6. **Map:** clusters derived from stance data, kept separate from curated niche labels with a crosswalk.

**Method bake-off on the slice:** Claude extraction (gold standard and quality ceiling), local open-model extraction on the Blackwell box, and a cheap embedding/classifier baseline. Judged on cluster validity by eye, landmark self-recognition, quote fidelity, cost and time. The winner or combination becomes the production pipeline.

## 4. The unified metric: public reputation score

One score, adapted from Community Notes, made explicit and visible as the game itself. People and agents both play for it.

**Mechanics (adapted):**

- Contributions: cross-cluster notes (describing another cluster), steelmen, and syntheses.
- Ratings: helpful = 1, somewhat = 0.5, not helpful = 0.
- Model: matrix factorization with global mean, rater intercept, note intercept, and viewpoint factors. Instead of a single inferred left/right axis, the viewpoint dimension is the map's real clusters.
- **Fidelity:** a description counts only when the described cluster rates it accurate (signs it).
- **Portability:** raters from other clusters rate whether it is clarifying.
- **Writer reputation:** rises when contributions reach ratified/helpful status, falls when they reach not helpful.
- **Rater reputation:** rises when ratings match final outcomes, rewarding honest rather than tribal rating.
- **Synthesis credit:** retroactive, by lineage — uptake by both parent clusters. Clean mutual disagreement and a better question are valid outcomes.

**Anti-gaming:**

- Only people placed in a cluster through real statement reactions can ratify.
- Agent accounts never ratify.
- Coordinated-rater detection; known Community Notes attack models used as threat model.

## 5. Agents

- Disclosed, registered on a public ledger, bound to a verified human operator.
- Agents earn reputation on their own leaderboard under the same metric, tied to their operator.
- Platform rules followed (e.g. on X, contact only after the person engages first).
- Directional-shift audit: agents that consistently move people toward one view lose reward eligibility.
- Agent-touched inputs are flagged; the map is re-fit without them before release.

## 6. Prediction market on strategies

- Participants back agent strategies (e.g. steelman-first vs shared-question) by forecasting how those agents' reputation scores will change between specific clusters over a set window.
- Outcomes are measured by the same unified reputation metric — no separate referee.
- Paid in reputation and prizes, not money; no tradable token for at least two years.
- Over time this produces causal knowledge of which bridging strategies work between which clusters.

## 7. Map dynamics over time

- Everything timestamped; nightly ingest of new episodes, weekly re-cluster and question battery, monthly deep pass (axes, lineages, audits, re-runs with improved models).
- State tracked per cluster pair: understanding matrix (from the reputation system), cohesion, cross-edges, hostility, ratified differences.
- Lineage view: clusters born, splitting, merging, fading; live questions spawning new questions.

## 8. Front end

- **First 60 seconds:** react to real statements, land as a dot on the terrain, see nearest landmarks, threshold reveal, twist card, invitation to describe the farthest cluster.
- **Living map:** live threads/questions as the core object; drill-down from map → cluster → person → claim → source clip.
- **Reputation surfaces:** public profiles and leaderboards for people and agents; strategy market view.
- **Event maps:** published within a day of major crossover conversations.

## 9. Infrastructure

- **Compute is local, data lives in the cloud.** Inference and heavy processing run on local machines: Benjamin's laptop now, and his 128 GB Blackwell box for batch work (vLLM-served open models, local ASR). Results are pushed to the cloud database, Neon Postgres + pgvector, as the system of record. (Amended 2026-10-31, D-31.11.)
- Until batch scale, Benjamin operates the pipeline by hand through Claude Code. The job queue and the Hermes-based operator agent that monitors, triages and reports arrive with batch operations. The pipeline stays deterministic throughout.
- Static snapshots published off-box.
- Claude used for gold labels, prompt design, audits and the weekly question battery.

## 10. Next steps

1. Select the slice landmark list from SEED-v4.
2. Discovery crawl and caption fetching (no GPU needed).
3. Claude gold extraction on a sample.
4. Build the reputation scoring prototype.
5. Local model bake-off when the box arrives.
