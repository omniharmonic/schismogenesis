# A1 — Ontography: what it is, what it got right, and what a population-scale memetic map should take from it

> **Design update (2026-10-30).** The Design Dialogue Memo of 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`) records decisions that supersede earlier research recommendations where they conflict; see `synthesis/SYNTHESIS.md` §2. The research below is unchanged. For this brief:
> - **Superseded: claims extracted "per cluster from the top-k central accounts of each L0 social-graph cluster" (§2).** The shared proposition bank is now seeded by quote-anchored extraction from the public output of ~500 curated **landmark** voices (YouTube and podcast transcripts, Substacks, posts), 2–3 per niche, not from social-graph centrality (SYNTHESIS §2 D12–D15, §6.1–6.2).
> - **Confirmed and strengthened: per-person private graphs → shared, speaker-independent proposition bank.** This brief's core recommendation is now decided architecture, with a deterministic quote validator (unsupported claims discarded) and a source-clip link on every statement (§2 D15).
> - **Modified: individuals get stances "from their posts via a cheap classifier."** Individuals are now placed by **statement reactions** (agree / disagree / pass, Polis-like), not by classifying their feeds (§2 D17; SYNTHESIS §6.1 S5).
> - **Superseded: the L0 social graph as the base layer and "bridge nodes from the social graph."** The follow graph is demoted to an attention signal; edges come from content (quotes, appearances, named arguments) (§2 D10, D14).
> - **Superseded: the opt-out / "claim your profile" flow for non-consenting X users.** Private individuals are placed only by their own reactions; public figures are placed only from their public output, with a dispute / annotate affordance (SYNTHESIS §11.2 red line 1).
> - **Modified: the onboarding "5–10 propositions that place you" confirm/amend/reject panel** survives as the "that's not me" correction loop, whose corrections become labeled examples (§2 D16); the dial becomes the first-sixty-seconds flow (SYNTHESIS §6.4).

Author of record: Benjamin Life (@omniharmonic). Research brief for Dialogos Arena, wave 0.
Sources: repo `/home/claude/auto-ontography-archive` (main @ a3d657b; branch `live-docs` @ b4d9a65), Parachute vault notes listed at the end.

---

## Summary

Ontography (live at ontography.vercel.app, July 2026) turns a person's words into a typed graph of claims, values, a-priori assumptions and concepts. Each node sits on one of four layers: ontology, epistemology, axiology, praxis. It then compares two graphs with a "handshake": pgvector suggests candidate node pairs, Claude judges each pair as equivalent, resonant, divergent or drift, plain graph code finds the deepest shared assumption and shortest paths, and an LLM writes a synthesis. It also scores each worldview on 8 fixed philosophical spectrums.

Its best idea is that epistemic status is first-class (`verified / stated / inferred / retracted`), backed by a verification loop where the subject confirms or rejects each inference. Its weaknesses show up in the code, not just the demo:
- **Over-extraction.** A 10k-word essay became about 600 nodes.
- **Dedup that can't see the whole graph.** It only checks against the first 80 nodes, in no particular order.
- **Citations that are never checked.** The prompt asks for verbatim quotes, but nothing verifies them.
- **A capped comparison.** A handshake judges at most 60 pairs, so on large graphs the per-layer "convergence" scores can't rise above a few percent. That is a likely mechanical cause of the 4/3/6/1% overlap Benjamin said felt wrong in the demo.

For a population-scale map, keep the taxonomy, the status model, the judge verdicts and the synthesis doctrine. Replace the per-person private graph with Topology Live's design: shared, speaker-independent propositions with per-person stances. The claim layer then becomes a sparse matrix of people × propositions that sits on top of social-graph clusters, rather than thousands of separate 3D hairballs.

---

## 1. Findings

### 1.1 Lineage and scope
- Ontography is the successor to Dialectical Topology (DT). It turns DT's hand-made, two-speaker analysis of a single debate into a scripted, versioned pipeline over database rows (PRD §2). Things carried over from DT: the claim schema (Toulmin warrants and evidence), the four-root tree (it becomes the four layers), the ontology-dimension schema (it becomes the 8-spectrum fingerprint), the synthesis doctrine, and DT's lesson to embed extracted claims rather than raw chunks (PRD §2.1).
- What v1 ships, plus later additions (README): the elucidation interview, the 3D worldview graph, handshakes, "fingerprinting" from pasted transcripts or URLs, the 8-dimension fingerprint, Neon Auth accounts, reflect mode, N-person "constellations", a celestial/soul-blueprint enrichment, and a Telegram nudge agent.
- The `live-docs` branch (2026-09-28) specifies **Topology Live**, the real-time Anti-Debate mapper. Its ONTOLOGY.md is a much more rigorous argument model, and its REUSE_AUDIT.md says exactly what to port from Ontography. For population scale, the live-docs ontology is the better foundation (§1.9).

### 1.2 Claim taxonomy and data model (main branch, `src/lib/db/schema.ts`, `src/lib/types.ts`)

**Node types:** `claim`, `value` (expresses what matters rather than what is), `assumption` (a priori: what must be true for a claim to hold), `concept` (a load-bearing term plus *this subject's* meaning of it).

**Categories (layers),** defined in `src/lib/protocol/categories.ts`, ordered from bedrock to surface:

| Layer | Question it answers |
|---|---|
| ontology | What is real? |
| epistemology | How do we know? |
| axiology | What matters? |
| praxis | How should we act? |

In the 3D layout these four layers become fixed y-strata.

**Node fields:** `text` (in the subject's register), `gloss` (neutral philosophical restatement), `status`, `confidence` (0–1, self-reported, set on verify), `depth` (0 = surface claim; +1 for each assumption descent), `warrants[]`, `evidence[]`, `provenance`, `embedding vector(1536)` with an HNSW cosine index, and timestamps.
- `warrants[]` entries are `{text, type: logical|empirical|experiential|authoritative}`.
- `evidence[]` entries are `{text, sourceType: anecdote|study|authority|example|analogy, verifiable}`.
- `provenance` is `{interviewId?, messageId?, sourceId?, quote?}`.
- Revisions are logged append-only in `node_revisions`.

**Edges** (per worldview): `grounds` (assumption → claim; forms a descendable DAG), `supports`, `contradicts`, `tension`, `implies`, `about` (node → concept). Each edge has `strength` and `rationale`.

**Comparison tables:**
- `handshakes`, holding `report` jsonb.
- `alignments`: `{nodeA, nodeB, verdict ∈ equivalent|resonant|divergent|drift, similarity, confidence, rationale}`.
- `dimension_scores`: `{dimensionId, position 0–1, summary, keyNodeIds}`.
- `constellations` / `constellation_members`, `worldview_refs` (shared library references), `telegram_links`.

**Audit:** `llm_calls` logs kind, prompt version, model, tokens and latency. No content is stored (NFR-1).

**Key structural fact:** every node belongs to exactly one `worldview_id`. Nothing in the model is shared across people. All cross-person meaning lives in per-pair `alignments` rows.

### 1.3 Extraction pipeline

**Models** (`src/lib/ai/models.ts`), all routed through the Vercel AI Gateway with OIDC:

| Role | Model |
|---|---|
| interviewer, extractor, judge (also synthesis and dimensions) | `anthropic/claude-sonnet-5` |
| fast | `claude-haiku-4.5` (declared but not used on the ingest path I read) |
| embedding | `openai/text-embedding-3-small` (1536-d) |

ARCHITECTURE.md still says Sonnet 4.6; the code says Sonnet 5.

**Prompt** (`src/lib/prompts/extractor.ts`, `extractor-v1`). A Zod schema returns `claims[] {ref, text, gloss, category, type, stated, warrants, evidence, quote}`, `assumptions[] {ref, text, gloss, category, groundsRefs}`, `concepts[] {ref, term, subjectMeaning, aboutRefs}` and `edges[]`. Its discipline rules are good:
- An empty result is valid.
- Assumptions must be singular and phrased so the subject can answer yes or no.
- Never restate a claim as its own assumption.
- In source mode, extract only the subject's own positions, never the host's framing.
- Quotes "must be verbatim substrings".
- Never re-infer an inference the subject already rejected.

**Chunking** (`src/lib/chunking.ts`). Splits on speaker turns or blank lines and packs to about 2,000 characters (≈500 tokens), with a hard maximum of 2,600. This follows DT's lesson to use conversational chunks, not fragments.

**Ingest workflow** (`src/workflows/ingest-source.ts`, Workflow DevKit). Steps: load and chunk; then extract chunks **sequentially**, 3 per durable step; then finalize, which recomputes dimensions.
- Each chunk's prompt includes the current graph, truncated to `MAX_CONTEXT_NODES = 80`.
- That list comes from `getGraph()`, which has **no ORDER BY**, so the 80 nodes are effectively arbitrary.
- The documented "dedupe/merge → assumption descent" steps (ARCHITECTURE §7) are not separate steps in the code. Assumptions come out inline from each chunk, with no global merge pass.

**Dedup and merge** (`persistExtraction` in `src/lib/worldview.ts`). All candidate texts in a chunk are embedded in one batch. Each candidate then runs its own pgvector top-1 query against the same worldview. If cosine ≥ **0.93**, the candidate reuses the existing node id and its new content is dropped; otherwise it is inserted.
- 0.93 is a strict threshold, so paraphrases mostly get through. Combined with the arbitrary 80-node context, this largely explains the 600-node (essay) and 1,200-node (Daniel) graphs (demo transcript).
- An assumption's depth is set to the maximum depth of the nodes it grounds, plus one.
- **Bug:** concepts are always inserted with `category: 'epistemology'` and `status: 'stated'` (`worldview.ts`, the concepts mapping). Every concept piles onto the epistemology layer and counts as "stated".

**Confidence.**
- The extractor gives no confidence score.
- `confidence` on a node is only the subject's slider value at verification.
- The judge gives a per-verdict confidence.
- The dimensions prompt returns `low/medium/high`, but it is **not persisted**.

**Interview path.** Each user message triggers a streamed interviewer turn (`interviewer-v1`, a 7-movement protocol: ground in the concrete → surface claims → descend to assumptions, at most 2 levels → probe concepts → verify gently, at most one per turn → steer coverage toward the thinnest layer → honor contradiction) and an extractor call. Coverage per layer is node count × mean depth.

### 1.4 Separating AI inference from attested belief

This is the strongest part of the design.
- **Status ladder.** `inferred` (the model derived it) → `stated` (said directly; extractor flag `stated=true`) → `verified` (the subject confirmed it in the VerificationPanel or the conversation, with a confidence value) → `retracted`.
- **Assumptions are always `inferred`** when created.
- **Rejected inferences** are fed back so they are never re-proposed.
- **Rendering.** Opacity is verified 1.0, stated 0.85, inferred 0.4, retracted 0.15 (`WorldviewGraph3D.tsx`).
- **Weighting.** Verified status earns a +0.5 bonus in `deepestSharedAssumption`. The dimensions prompt is told verified/stated outweighs inferred.
- **Reflect mode** (`src/lib/reflection.ts`) resurfaces tensions, low-confidence verified nodes, inferences left unruled for more than a day, and verified nodes untouched for more than 14 days.

Where the separation breaks:
1. **`stated` is the model's own judgment** that something was said directly. Nothing in the code checks that the `quote` is a substring of the chunk. In the demo Benjamin said each claim "should" be cited, and that checking the citation was still to be built (Regen Hub transcript). An audience member said they couldn't tell what Nate Hagens actually believes from what the model inferred.
2. **External fingerprints can never reach `verified`.** The subject isn't present. That is correct, but it means a population map built from feeds is almost entirely `stated`/`inferred`.
3. **Handshake candidate generation and judging ignore status**, apart from that small depth bonus. Inferred nodes still drive bridges, convergence scores and the synthesis.
4. **There is no "who said it" speech-act layer.** Topology Live calls attributing quoted or steelmanned content to the speaker "the single most common extraction error" and rules it out by construction (live ONTOLOGY §2.2). Ontography only has a prompt instruction. On X this matters a great deal: quote-tweets, sarcasm, and "imagine believing X".

### 1.5 How embeddings are used

Embeddings are computed on node text: claims, assumptions, and `term — meaning` for concepts. They are used in three places:
1. **Insert-time dedup** at cosine ≥ 0.93 within one worldview.
2. **Handshake candidate nomination.** A lateral join takes each A-node's top **3** B-neighbors with cosine > **0.42**, then a global `LIMIT 60` ordered by similarity (`src/lib/handshake.ts`). The docs say top-5 and > 0.55. The code is deliberately permissive ("embeddings only nominate, the judge decides").
3. **Re-embedding on amend.**

There is no embedding clustering, UMAP or semantic layout in Ontography; DT's claim-anchored UMAP is listed as an "R3 reference" for Topology Live's semantic layout. The judge prompt says it plainly: embeddings capture word-likeness, not meaning. In the demo, an audience member raised the same stance-vs-topic problem: "I hate cats" and "I like cats" land in the same region. Benjamin agreed, while also wondering whether vector maps are "more mathematically correct" than the claim graph.

### 1.6 How two worldviews are compared (`src/lib/handshake.ts`, `src/lib/graph/analytics.ts`)

1. **Candidates.** Embedding nominations as in §1.5.
2. **Adjudication.** The `alignment-judge-v1` prompt runs over batches of 20 pairs and assigns one verdict per pair:

| Verdict | Meaning |
|---|---|
| equivalent | Same commitment, allowing for register |
| resonant | Different claims that reinforce each other |
| divergent | Surface similarity hiding real disagreement |
| drift | Same term, different meaning; flagged as the most valuable verdict |

   The doctrine: never force false equivalence, and distinguish domains and time frames.
3. **Graph math.** The merged graph is A ∪ B plus bridge edges (equivalent or resonant; edge weight = (1 for equivalent, 2 for resonant) ÷ confidence).
   - **Shortest path between beliefs:** an O(n²) Dijkstra over undirected edges (`/api/handshake/[id]/path`).
   - **Deepest shared assumption:** the equivalent bridge with the highest min(depth), plus status bonus.
   - **Per-category convergence:** the sum of aligned weights (1 equivalent, 0.5 resonant) divided by the node count in that category.
4. **Dimensions.** The 8 core spectrums, each scored 0–1 by the LLM from the *whole* node list with key nodes cited: material ↔ mind/spirit; empirical ↔ experiential; constructed ↔ objective morality; individual ↔ relational; linear ↔ cyclical time; conditioned ↔ free agency; disenchanted ↔ enchanted; reform ↔ rupture. Bridging potential is high if the gap < 0.25, medium if < 0.5, otherwise low.
5. **Synthesis.** The `synthesis-v1` prompt writes common ground, domain distinctions, semantic drift, genuine divergences and practical paths, citing node ids, under the "no false synthesis" doctrine.
6. **Fault lines.** These are just `divergent` and `drift` alignments shown in a "faultlines" filter mode (`HandshakeGraph3D.tsx`). There is no structural model of a crux.

**Why the overlap scores were too low.** With at most 60 judged pairs, at most about 120 nodes can be "aligned" out of 600 + 1,200 = 1,800. Convergence per category therefore can't exceed roughly 6–7%, which matches the "4, 3, 6 and 1%" Benjamin read out and doubted ("I think they share a lot more"). An audience member added that sharing the same *orientation* (both "facing in that direction") is most of the similarity, and the pairwise metric doesn't capture it. For a population map, the lesson is that similarity must be measured against a population baseline, not computed from raw pair overlap.

The judge also sees no context beyond node text, and `deepestSharedAssumption.rationale` is always the empty string.

### 1.7 Visualization and its legibility failures

**Main view.** `react-force-graph-3d` draws a force layout with a y-stratum force per layer (strength 0.12, charge −60). Encodings:
- color = layer
- shape = node type (sphere claim/value, cube assumption, octahedron concept)
- size = degree
- opacity = status
- particles flow along `grounds` edges
- labels appear on hover only

The handshake view puts A at x<0 and B at x>0, with violet bridges and amber drift arcs. Constellations arrange N worldviews in radial sectors.

**Failures:**
- **Recorded in the demo and the task note:**
  - 600–1,200 nodes are unreadable.
  - Some pockets are disconnected.
  - Link semantics can't be seen ("I need to get it to better render what the actual links are").
  - There is no zoom-out structure.
  - Even the author didn't remember the visual grammar.
- **Kevin Owocki's feedback (Telegram, 2026-07-04):**
  - The tool is good at high resolution, but Venn diagrams read better at a glance. His suggestion: start with the simplest view and let the user open the high-resolution one later.
  - He asked what graph "relationality" means, i.e. whether nearness is a vector distance. It isn't: positions come from force simulation, so spatial distance carries no meaning beyond the y-stratum.
- **Topology Live's response** (live ARCHITECTURE §6, PRD §6):
  - a deterministic layout instead of force jitter: X = stance polarity, Y = stratum, Z = time
  - shape = proposition type
  - the crux drawn as a fault plane
  - a 2D map and list equivalents for every 3D view
  - a 0–5 audience detail dial (Dark → Frame → Positions → Clash → Map → Full)

  That dial is directly relevant to the governing question's "without overloading the user".

### 1.8 Cost and latency

The repo records nothing measured. `llm_calls` holds per-call tokens but I have no database access. The estimates below are mine and **UNVERIFIED**.
- **Ingest, 10k-word essay.** About 30 chunks × 1 extractor call each, every call with roughly 1k tokens of instructions, 0.5k of chunk and up to about 3k of node context, plus about 1.5–3k output. At Sonnet-class pricing (assuming about $3 in / $15 out per MTok; Sonnet 5 pricing not checked) that is on the order of **$1–2 per essay**. Embeddings cost nothing meaningful.
- **Ingest latency.** Chunks are extracted sequentially, and each node does its own pgvector round-trip, so a run likely takes **10–20+ minutes**. Benjamin's Telegram shows "processing ontology" at 05:56 and "processed" at 06:03 on 2026-07-04, about 7 minutes for some source.
- **Handshake.** 3 judge calls + 2 dimension calls (each with the full node list, which could be 40k+ tokens for 1,200 nodes) + synthesis ≈ **under $1**, finishing inside the 300 s function limit.
- **Constellations.** Run all pairs sequentially, so cost grows with N²: 1,000 people ≈ 500k handshakes. Not viable at scale.
- **Topology Live's estimates** (Opus 5.5 at $4/$20 per MTok): about **$30 per 90-minute live event** plus $20–40 for the canonical pass (live ARCHITECTURE §10). That is the cost of rigor: L1 extraction, an independent L2 critic, L3 linking and L4 insight.

### 1.9 The live-docs ontology (Topology Live) is the better claim layer

What it adds over Ontography:
- **Propositions vs stances (decision D5).** Propositions are speaker-independent and stored in canonical, positive form. Each person holds a *stance* on a proposition: accepts / rejects / suspends / accepts conditionally / accepts for argument's sake. Strength is taken only from explicit hedges; credence only when the speaker states one. Stances carry `stated | implied_by_act | inferred`. Inferred stances are never used for scoring.
- **ADU speech acts.** Content that is attributed to someone else or steelmanned is never assigned to the speaker.
- **Typed propositions.** Ten types (empirical, causal, predictive, normative, prescriptive…), each with a stratum (praxis / axiology / epistemology / ontology, plus empirical).
- **Fifteen types of epistemic basis**, ASPIC+ attack relations, and Walton argument schemes with critical questions.
- **Derived structures:** disagreement (opposing stances on one proposition), crux (a double-crux dependency score weighted by stratum depth), common ground, six "higher ground" constructions, and drift defined over a person's *sense* of a concept.
- **Faithfulness rules** (§8), enforced by deterministic validators and an independent critic: the cited span must exist, entities and numbers must match, hedges and quantifiers must be preserved, and the critic asks "would the speaker sign this?".
- **Identity resolution.** `sameAs` with a strict, polarity-normalized equivalence test. Merges are reversible events.
- **QUALITY.md:** gold sets, inter-annotator κ, and metric gates (faithfulness ≥ 0.97, proposition precision ≥ 0.90, identity-resolution F1 ≥ 0.85, presupposition necessity ≥ 0.85).
- **Status pipeline:** live_provisional → operator_approved → released → canonical → participant_confirmed / contested.

### 1.10 Other context from Parachute

- **Regen Hub demo** (2026-07-10). Product ideas from the room:
  - load your ontology automatically from your ChatGPT or Claude context instead of doing an interview
  - a relationship or marriage "translator"
  - real-time structure overlays for podcasts and video chat
  - a podcast → knowledge-graph pipeline, first target the Emerge podcast

  Benjamin also demoed a separate RAG view: chunks linked by semantic similarity and by sequence, so you can watch a conversation move through semantic space over time. His own verdict was that it looked cool but "didn't actually add anything" for the user.
- **Follow-up tasks.** `simplify-ontography-visualization` and `productize-podcast-knowledge-graph` were both bulk-archived on 2026-08-18 without being done.
- **Kevin Owocki** shared `daily-ontological-map.vercel.app` (2026-07-28). Its content is UNVERIFIED (not fetched). His "mirror mirror" second-brain passes rendered Nate Hagens' ontology as Venn diagrams and as a problem→solution linear map. He proposed comparing Daniel / Nate / Greenpill-Gitcoin as an artifact for a meeting.

---

## 2. How this answers the governing question (layering + validation)

**What Ontography shows about accuracy.** A claim graph is the most *expressive* layer: it gives stance, depth (presupposition → claim), a person's sense of a concept, and the reasons they give. It is also the layer most exposed to model invention. It is only accurate when three things hold:
- every node is anchored to a verified quote,
- stance comes from speech acts, not from the topic, and
- identity resolution makes different people's claims commensurable.

Ontography has the first only in its prompt, lacks the second, and the third only exists per pair.

**Proposed layering for a population-scale map built from X feeds:**

| Layer | Signal | Role | Ontography reuse |
|---|---|---|---|
| L0 Social graph | follows / RT / quote / reply | Belonging; community detection gives *clusters* and *bridge nodes* | none |
| L1 Embeddings | post and claim vectors | Topic terrain; candidate retrieval only ("nominate, don't decide") | pgvector + HNSW pattern, `embedMany`, the "nominate" doctrine |
| L2 Claim layer | canonical propositions × stances | Stance and depth: *what* clusters believe and *where they fork* | taxonomy, extractor discipline, judge verdicts, status ladder |
| L3 Low-dimensional summary | stance matrix → ideal points / dimension scores | Glanceable placement ("where do I sit") | the 8 core spectrums as *named, interpretable* candidate axes |
| L4 Narrative | cluster↔cluster synthesis | Meaning-making for MEET | synthesis doctrine and prompt structure, nudge doctrine |

**How the claim layer sits on top of the others:**
1. **Claims are extracted per cluster, not per person.** Pick the top-k central and high-engagement accounts and posts in each L0 cluster. Extract with the Topology Live ontology so propositions come out in canonical, positive form with speech acts. Resolve identity across clusters into one shared proposition index of perhaps tens of thousands. This replaces Ontography's private per-worldview nodes.
2. **Individuals get stances, not graphs.** For each user, run a cheap stance classifier (an NLI/"decision" model; see B4) over their posts against the K propositions that best tell clusters apart. The result is a sparse stance vector. Ideal-point or matrix-factorization models over the people × propositions matrix give the latent axes. The LLM-scored 8 spectrums can be kept as labels for those axes, not as the measurement itself.
3. **Run handshakes between clusters, not between people.** Ontography's pipeline (nominate → judge → deepest shared presupposition → synthesis) works at a scale of tens to hundreds of clusters. Fault lines become cruxes: propositions with opposing majority stances across clusters and high dependency scores, borrowing Topology Live's crux scoring. Social-graph bridge nodes are the natural first candidates for MEET.
4. **Similarity is measured against a population baseline.** Report overlap as a lift over the population average. That fixes the "facing the same direction is 99%" problem from §1.6.

**Validation:**
- **Faithfulness.** Every proposition must trace to a real span via an automated substring check plus an independent critic, with Topology Live's gates (faithfulness ≥ 0.97 on a blind sample).
- **Self-attestation.** Reuse the VerificationPanel. When a person onboards with their feed, show the 5–10 propositions that place them and record confirm / amend / reject. The confirmation rate is the headline accuracy metric, and rejections feed training data back to the classifier.
- **Predictive validity.** Hold out some of a user's posts and predict their stance on propositions those posts contain.
- **Convergent validity.** Claim-layer clusters should broadly agree with social-graph communities, measured by adjusted mutual information. Disagreements between the two are interesting cases, not automatically errors.
- **Known groups.** Accounts with obvious, self-declared affiliations should land where expected.
- **Inter-annotator κ** on a gold set of X threads, built with Topology Live's red-team cases (irony, quote-tweets, hypotheticals).

---

## 3. Reusable assets and design implications

**Reuse directly:**
- The four-layer taxonomy and its questions and glosses (`protocol/categories.ts`). Add `empirical` as Topology Live does.
- The status ladder `inferred / stated / verified / retracted` and the doctrine of rendering inferred content as translucent. Rejected inferences are never re-proposed.
- The extractor discipline text: empty results are valid, assumptions are singular and answerable yes/no, extract only the subject's own positions, never re-infer.
- The four judge verdicts, especially **drift**, and the "embeddings nominate, the judge decides" pattern.
- The synthesis doctrine and output sections. The nudge doctrine: silence is the default; questions, not verdicts.
- `graph/analytics.ts` (merged graph, path, deepest shared assumption, convergence) as a seed for crux scoring at cluster level. It needs a heap-based Dijkstra and directed `grounds` semantics.
- The 8 core dimensions as interpretable axis *labels*.
- The `llm_calls` audit pattern, versioned prompt modules, and the single file that maps roles to models.

**Port with changes:**
- Use Topology Live's ontology (propositions + stances + speech acts + faithfulness validators) as the schema.
- The extractor gains `speechAct` and span offsets, plus a deterministic quote validator.
- Deterministic stratified 2D/3D layout plus a detail dial, instead of a force graph.

**What must change for scale (thousands of users, not two):**
1. **Shared proposition index.** Replace per-person private nodes with global propositions; identity resolution becomes the core service.
2. **Fix dedup.** Retrieve existing nodes by embedding (top-k nearest) instead of taking the first 80. Add a global merge and cluster pass, a lower merge-candidate threshold with an LLM equivalence check, and polarity normalization.
3. **No pairwise O(N²) handshakes.** Compare clusters, and place individuals by their stance vectors.
4. **Cost tiering.** Use the expensive model for cluster-level extraction and identity resolution, and cheap classifiers or embeddings for per-user stance. Batch API and prompt caching. At the current pipeline's estimated ~$1–2 per 10k words, a full extraction for every user over their timeline would cost too much across thousands of users (UNVERIFIED estimate).
5. **Parallel, batched persistence.** Batch the per-node vector queries and inserts. Parallelize chunk extraction once dedup is order-independent.
6. **Persist confidences** (dimension confidence is currently dropped) and add an extractor confidence.
7. **Fix the concept-category bug** and the always-`stated` status for concepts.
8. **Privacy.** "A worldview is intimate data" (NFR-3). Mapping X users who haven't opted in needs the same machine-inference watermark, plus an opt-out or claim-your-profile flow. Show cluster-level summaries by default; show individuals only when they opt in.

**Legibility at population scale.** Never show the full graph by default. Use a dial:
1. where you sit (2–3 named axes + your cluster)
2. your cluster's 3–5 core propositions with quotes
3. the nearest neighboring cluster: shared ground, top crux, drift terms
4. the cluster map with bridge accounts
5. the full claim graph for any node, on demand

This follows Kevin's "simple first, high-resolution later" and Topology Live's levels 0–5.

---

## 4. Risks and open questions

- **Short, ironic, reply-heavy posts on X** are much harder than essays: quote-tweets, dunks and sarcasm. Without speech-act typing, attribution errors will be systematic. Topology Live's red-team list (QUALITY §7) is a starting gold set.
- **Inferred presuppositions** are the most valuable layer for "depth" and also the least verifiable. Topology Live's rule (never counted until someone states it) protects honesty but may empty the ontology and epistemology layers for feed data. Open question: show these layers at cluster level as clearly labeled hypotheses?
- **Fixed vs emergent axes** (PRD Q2) is unresolved. Fixed axes compare well across people but may not match how X actually divides. Learned axes need post-hoc labeling.
- **Topic vs stance.** Embeddings will cluster by topic. The claim layer must carry polarity, and validation should explicitly test same-topic, opposite-stance pairs.
- **Inflated confidence in a bad map:** "we trust the AI more than ourselves" (an audience member at the demo). Quote anchoring and self-attestation rates should be visible in the UI.
- **UNVERIFIED:** actual token costs and latency (no `llm_calls` data was available); Sonnet 5 pricing; what `daily-ontological-map.vercel.app` contains; whether Topology Live was built and run on 2026-10-11 as planned (a separate `antidebate-live` repo exists per BRIEF; not inspected here).
- **Doc/code drift:** the docs say top-5 / > 0.55 candidates, while the code uses top-3 / > 0.42 / LIMIT 60; the docs list separate merge and descent steps that the code doesn't have. Read the code, not the docs.

---

## Sources

**Repo, main branch** (`/home/claude/auto-ontography-archive`):
- README.md; docs/PRD.md; docs/ARCHITECTURE.md; docs/IMPLEMENTATION_PLAN.md
- src/lib/db/schema.ts; src/lib/types.ts; src/lib/ai/models.ts; src/lib/ai/log.ts
- src/lib/chunking.ts; src/lib/embeddings.ts; src/lib/worldview.ts (persistExtraction, dedup 0.93, concept category)
- src/workflows/ingest-source.ts (MAX_CONTEXT_NODES = 80, sequential chunks)
- src/lib/prompts/extractor.ts; src/lib/prompts/alignment-judge.ts; src/lib/prompts/synthesis.ts; src/lib/prompts/dimensions.ts; src/lib/prompts/interviewer.ts; src/lib/prompts/nudge.ts
- src/lib/handshake.ts (candidates top-3, > 0.42, LIMIT 60, batch 20); src/lib/graph/analytics.ts
- src/lib/dimensions.ts; src/lib/protocol/categories.ts; src/lib/protocol/dimensions.ts
- src/lib/reflection.ts; src/lib/constellation.ts; src/workflows/constellation-pairs.ts
- src/app/api/handshake/[id]/path/route.ts; src/app/api/nodes/[id]/route.ts; src/app/api/ingest/route.ts
- src/components/graph/WorldviewGraph3D.tsx; src/components/handshake/HandshakeGraph3D.tsx; src/components/constellation/ConstellationGraph3D.tsx

**Repo, `live-docs` branch:** docs/live/README.md, ONTOLOGY.md, ARCHITECTURE.md (§3 pipeline, §3.4 identity resolution, §6 rendering, §10 cost), PRD.md (§6 detail dial), QUALITY.md, REUSE_AUDIT.md.

**Parachute vault:**
- vault/meetings/2026-07/2026-07-10_regen-hub-demo-ontography (full transcript: demo, audience feedback)
- vault/tasks/active/simplify-ontography-visualization
- vault/tasks/active/productize-podcast-knowledge-graph
- vault/messages/telegram/kevin-owocki (2026-07-04 feedback on the Venn view; 2026-07-28 daily-ontological-map link)
- vault/tasks/active/topology-live-antidebate-progress-conference (existence only)
