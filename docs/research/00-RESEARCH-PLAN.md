# Dialogos Arena — Context Assembly & Research Plan

*Benjamin Life ([@omniharmonic](https://github.com/omniharmonic)) · drafted 2026-10-30 · working title, pre-spec*

> **Design update (2026-10-30).** After the research swarm, Benjamin and Claude held a first-principles design dialogue. Its decisions are recorded in `/home/claude/dialogos-arena/design/DESIGN-MEMO-2026-10-30.md` (Parachute `vault/research/dialogos-arena/design-memo-2026-10-30`) and integrated into `/home/claude/dialogos-arena/synthesis/SYNTHESIS.md` (see its new §2). They supersede earlier research recommendations where they conflict. In brief: the gradient is ratified cross-cluster description (cross-cluster notes with fidelity and portability); the map is built from ~500 US landmark voices' public output (YouTube and podcast transcripts, Substacks, posts), not from the social graph; individuals are placed by statement reactions; event maps of recorded cross-cluster encounters are the flagship; syntheses are rewarded retroactively by lineage. The framing below is kept as written for the record.

## 1. The thesis we're researching toward

Civilization is a dialectical process. A free market of ideas matters because co-evolution needs requisite variety and real contact between worldviews. Our democratic institutions were meant to be the conduit for that process; they now run on 250-year-old infrastructure captured by a monoculture of capital. The dialectic has moved online, but there are no internet-native institutions scaffolding it.

The proposed infrastructure has three layers:

1. **See** — map the topology of memetic space: clusters of worldviews (interpretive frameworks), the people who run them, and the bridges between clusters. Entry point: a person offers up their X feed and sees where they sit.
2. **Meet** — structured anti-debate / dialogos across clusters, where each party is changed by the encounter.
3. **Move** — incentives and weighted preference (quadratic / plural mechanisms) that reward metabolizing ideas across tribes, so the landscape itself climbs an integrative gradient over time.

The research goal is not the product yet. It is a context pack complete enough that specs can be written from first principles without re-deriving anything.

## 2. What already exists (found in the vault today)

| Prior work | What it contributes | Where |
|---|---|---|
| **Ontography** | Extracts a person's worldview from source text into a cited graph of ontological, epistemological, axiological and praxis claims; compares two graphs for shared assumptions, fault lines, and shortest path between beliefs. Lessons: 600–1,200 nodes is illegible; hard to separate AI inference from actual belief. | Regen Hub demo transcript (2026-07-10); tasks *simplify-ontography-visualization*, *productize-podcast-knowledge-graph*; repo `omniharmonic/auto-ontography-archive` |
| **Dialectical Topology** | Six-lens analysis of a dialogue: semantic landscape (embeddings), claims analysis, dialogue flow, worldview map, epistemological tree, plus synthesis. Built on the Aubrey Marcus × John Demartini dialogue. | Essay *For Now We See Through a Glass, Darkly*; dialecticaltopology.xyz |
| **Dialectical.Claims** | 50+ thinkers as executable *methods*, run through anti-debate rounds; syntheses classified as resolution, transcendence or paradox. | Essay in `wiki/writing`; repo `omniharmonic/dialecticalclaims` |
| **Topology Live / Anti-Debate** | Real-time debate mapping for Stephanie Lepp's Anti-Debate at Progress Conference (Oct 11). Full doc set: PRD, ONTOLOGY, ARCHITECTURE, UX, QUALITY. | Repo `omniharmonic/antidebate-live` (`docs/`, `docs/client/`) |
| **Thiel–Karp genealogy** | Graph-topology reading of a research vault; Hegel → Kojève → Fukuyama lineage directly relevant to "end of history" vs. ongoing dialectic. | `vault/research/thiel-karp-genealogy/` |
| **Gitcoin / QF context** | Quadratic funding practice, love.fund, Gitcoin Brain vault. | Gitcoin Brain; Kevin threads |

**Gaps I couldn't close from here:** Kevin's memetic-tribes visualizer isn't in your vault or the Gitcoin Brain, and I can't see the Ontography repo name. Both are needed before Wave 0 runs (see §6).

## 3. Methodological spine — the question that governs everything

*How do we accurately depict a worldview?* Every downstream choice (visualization, matching, incentives) inherits the answer. The research must compare at least these approaches against each other, not pick one by default:

- **Embeddings alone** — fast, scalable, but cluster by *topic* more than *stance*; two people who disagree about climate land next to each other.
- **Claims extraction** (Ontography's path) — precise and citable, but slow, and LLM inference can invent beliefs.
- **Network structure** — who follows/retweets/quotes whom (the classic "Twitter tribes" method); captures social belonging, not reasoning.
- **Ideal-point / latent-dimension models** — place people on inferred axes from behaviour (political science's workhorse).
- **Hybrid** — embeddings for coarse placement, claims for the deep layer people actually inspect, network for validation.

Each stream below reports back on how its domain answers this question, including validation: how would we know the map is right?

## 4. The swarm — three waves, 11 agents

### Wave 0 — Your own corpus (5 agents, parallel)

| Agent | Scope | Output |
|---|---|---|
| **A1 Ontography** | Repo, docs, demo transcript, tasks; claim schema; known failure modes | Brief + reusable components list |
| **A2 Dialectical Topology** | Site, essay, code; the six lenses and what each revealed | Brief + lens-by-lens assessment |
| **A3 Anti-Debate & Topology Live** | `antidebate-live` docs, Progress Conference outcome, Stephanie's feedback, Dialectical.Claims | Brief + live-event learnings |
| **A4 Theory in your writing** | Your essays, captures, concepts and meetings on dialectics, sensemaking, meaning crisis, democracy | Map of your existing positions and vocabulary |
| **A5 Kevin's tribes map + Gitcoin** | Kevin's visualizer (method, data, stack), QF / love.fund relevance | Teardown + fit assessment |

### Wave 1 — The field (5 agents, parallel, primary sources first)

| Agent | Scope |
|---|---|
| **B1 Lineages** | Hegel and dialectic; Bohm Dialogue; Habermas (public sphere, communicative action); deliberative vs. agonistic democracy (Fishkin, Mouffe); Dewey; memetics and *The Memetic Tribes of Culture War* (Limberg & Barnes); cultural evolution (Boyd & Richerson); Ashby's requisite variety; metamodernism (Freinacht); open democracy (Landemore) |
| **B2 Computational democracy** | Pol.is and vTaiwan; Talk to the City; Remesh; DeepMind's Habermas Machine; Community Notes bridging; bridging-based ranking (Ovadya); *Plurality* (Tang & Weyl); Collective Intelligence Project; Stanford Online Deliberation; Kialo; what worked, what stalled, why |
| **B3 Mechanism design** | QV/QF, plural QF and connection-oriented cluster matching, pairwise preference, conviction voting, Deep Funding; designing rewards for synthesis without Goodharting it; sybil resistance |
| **B4 Mapping science** | Stance detection, argument mining, ideal-point estimation, community detection, UMAP/HDBSCAN/BERTopic, worldview and moral-foundations frameworks; validation methods; how each answers §3 |
| **B5 Platform, data & ethics** | X API terms and cost in 2026 vs. Bluesky / AT Protocol firehose vs. Farcaster; consent-first feed ingestion; the weaponization risk (a memetic map is also a targeting map); prior art in polarization mapping (More in Common, Graphika); privacy law |

### Wave 2 — Synthesis (1 agent, after Waves 0–1)

**C1 Synthesis** — merges all briefs into: glossary, design principles, a decision matrix for §3, architecture options (not a spec), risk register, open questions, and a spec-readiness checklist.

## 5. Where it lands

All outputs go into Parachute under `vault/research/dialogos-arena/` (tag `research`, `dialogos-arena`):

- `wave-0/*` and `wave-1/*` — one brief per agent, every claim cited
- `bibliography` — annotated, primary sources flagged
- `synthesis` — the C1 document
- `PROJECT` note linking it all, attributed to Benjamin Life (@omniharmonic)

Copies of the synthesis come back here as markdown.

## 6. Before launch — what I need from you

1. **Kevin's visualizer** — a link, repo, or tweet.
2. **Ontography repo name** — or confirm it lives in `auto-ontography-archive`.
3. **"Jev"** — I couldn't place this tool. A name or link?
4. **Go / adjust** — scope, agent count, or naming changes.

Cost: Waves 0–1 run in parallel, so wall-clock is roughly one long session; this is a heavy token run (10 deep-research agents plus synthesis).
