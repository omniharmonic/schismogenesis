# Dialogos Arena — Shared Brief for Research Agents

Author of record: Benjamin Life (@omniharmonic). Never attribute this work to OpenCivics or OpenCivics Labs.

> **Design update (2026-10-30).** After the research swarm, Benjamin and Claude held a first-principles design dialogue. Its decisions are recorded in `/home/claude/dialogos-arena/design/DESIGN-MEMO-2026-10-30.md` (Parachute `vault/research/dialogos-arena/design-memo-2026-10-30`) and integrated into `/home/claude/dialogos-arena/synthesis/SYNTHESIS.md` (see its new §2). They supersede earlier research recommendations where they conflict. In brief: the gradient is ratified cross-cluster description (cross-cluster notes with fidelity and portability); the map is built from ~500 US landmark voices' public output (YouTube and podcast transcripts, Substacks, posts), not from the social graph; individuals are placed by statement reactions; event maps of recorded cross-cluster encounters are the flagship; syntheses are rewarded retroactively by lineage. The framing below is kept as written for the record.

## Thesis
Civilization is a dialectical process. A free market of ideas matters because co-evolution needs requisite variety and real contact between worldviews. Democratic institutions were meant to conduit that process; they run on 250-year-old infrastructure and are captured by a monoculture of capital (Citizens United, two-party lock-in). The dialectic now happens online, with no internet-native institutions scaffolding it as public dialogos — dialogue where each party is changed by the encounter.

Proposed infrastructure, three layers:
1. SEE — map the topology of memetic space: clusters of worldviews (interpretive frameworks), the people who run them, and the bridges/edge-nodes between clusters. Entry point: a person offers their X (Twitter) feed and sees where they sit.
2. MEET — structured anti-debate / dialogos across clusters.
3. MOVE — incentives and weighted preference (quadratic / plural mechanisms) rewarding the metabolizing of ideas across tribes, so the landscape climbs an integrative gradient over time.

## The governing research question
How do we ACCURATELY depict a worldview — and how can multiple methods be LAYERED to give richer information without overloading the user? Candidate layers:
- Social graph (follows / retweets / quotes via X API) — likely the most powerful signal of belonging.
- Embeddings — semantic landscape; risk: clusters by topic, not stance.
- Claims extraction — claims forming a graph of belief systems, typed by ontological / epistemological / axiological / praxis layers (taxonomy from Ontography and Anti-Debate).
- Cheap classifier/"decision" models that return categories without an embedding step (Benjamin calls one "Jev" — identity unverified; see B4).
- Ideal-point / latent-dimension models.
Every brief must say how its domain answers this question and how we'd VALIDATE that a map is right.

## Prior work (Benjamin's)
- Ontography: repo /home/claude/auto-ontography-archive (main = Ontography app; branch `live-docs` = realtime debate mapping docs under docs/live/). Extracts worldview → cited claim graph (ontological, epistemological, axiological, praxis); compares two people (shared assumptions, fault lines, shortest path). Known issues: 600–1,200-node graphs illegible; hard to separate AI inference from real belief.
- Dialectical Topology: /home/claude/omniharmonic/dialecticaltopology (six lenses: semantic landscape, claims analysis, dialogue flow, worldview map, epistemological tree, synthesis), essay "For Now We See Through a Glass, Darkly" (Parachute: wiki/writing/for-now-we-see-through-a-glass-darkly), site dialecticaltopology.xyz.
- Dialectical.Claims: /home/claude/omniharmonic/dialecticalclaims (thinkers as executable methods; syntheses as resolution / transcendence / paradox).
- Topology Live / Anti-Debate: /home/claude/omniharmonic/antidebate-live (docs/, docs/client/) — real-time map for Stephanie Lepp's Anti-Debate at Progress Conference 2026-10-11.
- Kevin Owocki (Gitcoin) has built a visualizer of memetic tribes on Twitter (repo not accessible).

## Tools available to you
- Parachute vault (Benjamin's second brain): load with ToolSearch "select:mcp__parachute__query-notes" (and mcp__parachute__create-note to write). Gitcoin team vault: mcp__Gitcoin_Brain__query-notes.
- WebSearch / WebFetch for primary sources. Prefer original papers, author sites, official docs over aggregators.

## Output contract
1. Write your brief as markdown to the file path given in your task. Structure: Summary (≤200 words) · Findings · How this answers the governing question (layering + validation) · Reusable assets / design implications · Risks & open questions · Sources (title + URL or vault path for every claim).
2. Paraphrase; quote sparingly (<15 words, max one quote per source).
3. Mark anything you could not verify as UNVERIFIED. Never invent citations.
4. Do NOT write to Parachute — the orchestrator files everything. Do NOT contact anyone or post anything.
5. Your final reply to the orchestrator: ≤300 words — the 5–8 most important findings and the file path.
