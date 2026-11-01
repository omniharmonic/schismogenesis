# B4 — The Science of Mapping Worldviews, and How to Layer the Methods

> **Design update (2026-10-30).** The Design Dialogue Memo of 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`) records decisions that supersede earlier research recommendations where they conflict; see `synthesis/SYNTHESIS.md` §2. The research below is unchanged. For this brief:
> - **Re-ranked: the five-layer SEE stack.** The **content-derived proposition bank** (L3, now built from ~500 landmarks' transcripts and texts, not on demand), the **Jev question battery** (L1, now a weekly, model-proposed live battery with layer tagging, no surveys) and **statement reactions** (path C / L4 MF, now phase 1) are primary; **content edges** (quotes, appearances, named arguments) are secondary; the **follow graph (L0) is demoted to an attention signal**; stance-aware embeddings (L2) are optional (SYNTHESIS §2 D10–D17; §6.1).
> - **Superseded: the recommended path "B (graph-only) → B+L1 → L3 on demand → C as MEET data accrues".** The decided path starts from landmark content plus reactions; graph-only v0 is dropped (SYNTHESIS §6.7).
> - **Superseded: "the social graph … is the most reliable signal of tribe membership"** as the basis of placement. Follows are attention, not belief (§2 D10).
> - **Modified: L1 battery content.** MFQ-2, Schwartz and Koltko-Rivera items are no longer onboarding surveys; questions come from what the culture is contesting now, and corrections ("that's not me") become labels (§2 D16).
> - **Modified: "default to opt-in plus public figures".** Public figures are placed from their public output with a dispute affordance; private individuals only by their own reactions (SYNTHESIS §11.2).
> - **Added:** axes chosen per live question (§2 D7); timestamped propositions, cluster lineages and nested daily / weekly / monthly horizons (§2 D19; SYNTHESIS §6.5–6.6).

Stream B4 · Wave 1 · Dialogos Arena (author of record: Benjamin Life / @omniharmonic) · compiled 2026-10-30

---

## Summary

No single signal captures a worldview. Each method measures a different thing:
- **The social graph** (follows, retweets) measures *belonging*: who you listen to and amplify. It is the most reliable and cheapest-to-validate signal of tribe membership, and it underpins two decades of polarization research (Conover 2011, Barberá 2015, Garimella 2018, Cinelli 2021).
- **Off-the-shelf text embeddings** measure *topic*, not stance. Standard sentence transformers put "I love X" and "I hate X" close together (Ghafouri et al., EMNLP 2024).
- **Stance, value and moral classifiers** measure *position* on named axes.
- **LLM claim extraction** measures *reasons*, and it is where hallucination and over-inference live.
- **Disagreement/agreement data** (Community Notes, Polis-style votes) reveals *latent axes*. A 2026 refit of the Community Notes model found at least two independent axes: left/right, plus one the authors read as institutional trust.

"Jev" is a real product. It is **TypeSafe's Jev**, a closed-weight "System One" decision model launched 15 Sept 2026. It returns calibrated probabilities over choices you define, with no embedding step on your side, at about $0.042 per million input tokens. It is a good fit for mass-labeling posts along Ontography's axes. It is not a measurement instrument until validated.

**Recommendation:** a five-layer SEE stack.
- **L0** graph backbone
- **L1** stance and value coordinates (cheap classifier)
- **L2** a clustered "constellation" map with stance-aware embeddings
- **L3** claim graphs only on demand, for a selected person or cluster, with provenance
- **L4** bridge and broker analytics

Show them progressively: overview map, then cluster card, then person, then claim graph.

---

## Findings

### 1. Social-graph methods

**1.1 The core empirical result: networks polarize; content mixes.**
- **Conover et al. (ICWSM 2011, Test-of-Time award).** The retweet network of US political Twitter splits into two highly segregated partisan communities. The mention network does not: users @-mention across lines. *Design implication:* edge type matters. Retweets mean endorsement. Mentions, replies and quotes are often contact or conflict. Source access was blocked by a bot wall; the summary is from the paper's well-known abstract and the IU OSoMe award note. **Re-verify the exact wording.**
- **Barberá, Jost, Nagler, Tucker & Bonneau (Psych. Science 2015).**
  - Data: about 150M tweets on 12 issues, 3.8M users.
  - On overtly political events, retweeting stayed within ideology. On non-political events (Boston Marathon bombing, Super Bowl), information flowed like a "national conversation."
  - Liberals crossed ideological lines more than conservatives.
  - *Implication:* belonging is topic-conditional. A single global cluster label hides this.
- **Cinelli, De Francisci Morales, Galeazzi, Quattrociocchi & Starnini (PNAS 118(9), 2021).**
  - Data: over 100M posts on Facebook, Twitter, Reddit and Gab (2010–2018), on controversial topics such as abortion, guns and vaccines.
  - Facebook and Twitter show homophilic clustering in interactions and biased diffusion toward like-minded users.
  - Reddit shows much weaker echo-chamber effects, which the authors tie to feed design.
  - Leaning was inferred from the outlets users shared, scored against external media-bias ratings (from the arXiv version; the PNAS page was blocked here, so **re-verify the method detail**).
- **Garimella, De Francisci Morales, Gionis & Mathioudakis, "Quantifying Controversy" (ACM TSC 2018).**
  - Pipeline: build a topic conversation graph, partition it into two sides (METIS), then score.
  - **Random Walk Controversy (RWC)** separated controversial from non-controversial topics best. A restart-based approximation matched it (r = 0.96) and ran up to 200× faster.
  - Retweet and follow graphs worked. Content graphs (shared hashtags or URLs) were sparse and useless.
  - Sentiment *variance*, not bag-of-words, distinguished controversy.
  - *Implication:* graph-first, not content-first, for the backbone.

**1.2 Ideal-point (latent-dimension) estimation from follows.**
- **Barberá, "Birds of the Same Feather Tweet Together" (Political Analysis 23(1), 2015).**
  - A Bayesian spatial-following model. A user's latent position is inferred from which political elites they follow.
  - Assumption: following is homophilic.
  - Validated against legislators' conventional ideology scores, users' self-declared preferences, and party-registration records. Applied to the US and five European countries.
  - Code: `pablobarbera/twitter_ideology` (the `tweetscores` R package).
  - *Strength:* one interpretable continuous axis, few parameters, computable from a user's following list alone (the "offer your feed" entry point).
  - *Weakness:* it needs a curated elite set and assumes one dominant dimension. Non-political communities (crypto, regenerative, spiritual) need their own elite anchor set and probably more axes.
- **Wu, Nagler, Tucker & Messing (arXiv 2303.12057).**
  - An LLM makes pairwise comparisons ("which senator is more liberal on guns?"), and a Bradley–Terry model scales the results.
  - The scale correlates strongly with DW-NOMINATE and yields issue-specific scales (guns, abortion) that predict votes better than general ideology.
  - *Implication:* a cheap way to place *anchor accounts* on bespoke axes such as Ontography's dimensions. Barberá-style propagation then places everyone else.
- **Waller & Anderson (Nature 2021, arXiv 2010.00590).**
  - Community embeddings built from co-commenting on 5.1B Reddit comments across about 10k subreddits.
  - Interpretable "social dimensions" (age, gender, partisanship) are defined by seed-pair *differences* in the embedding space.
  - Reddit's polarization around 2016 came from new users, not individuals moving. Code: `CSSLab/social-dimensions`.
  - *Directly reusable pattern:* behavioral embedding + anchor-pair axes = interpretable worldview coordinates.
- **SimClusters (Satuluri et al., KDD 2020).** X's own production recommender. It finds about 145k "KnownFor" communities of producers from the follow graph, then derives "InterestedIn" vectors for consumers. The open-sourced `twitter/the-algorithm` documents it. Detail is from memory and an unretrieved doc page: **UNVERIFIED specifics**. It matters because it shows that community-from-follow scales to hundreds of millions of users.

**1.3 Community detection.**
- **Louvain → Leiden (Traag, Waltman & van Eck, Sci. Rep. 2019).** Louvain can return up to 25% badly connected and up to 16% *disconnected* communities. Leiden guarantees connected communities and runs faster. **Use Leiden** (`leidenalg`, `igraph`, `graspologic`), with a resolution parameter to make a cluster hierarchy.
- **Stochastic block models (Peixoto, `graph-tool`, nested SBM).**
  - Principled Bayesian inference picks the number of blocks by minimum description length and gives a *hierarchy* for free, which fits a zoomable map.
  - SBMs also find non-assortative structure, such as "audience" blocks that follow a group without being followed back.
  - Slower than Leiden; feasible to about 10^6 edges on one machine.
  - Tutorial: Peixoto arXiv 1705.10225.
- **Signed networks.** When edges carry agreement (+) or disagreement (−), use signed modularity (Traag & Bruggeman 2009, arXiv 0811.2329) or SignedLouvain variants. Results on bipartite signed networks are highly parameter-sensitive (arXiv 2405.08203), so report robustness.

**1.4 Graph embeddings.**
- **node2vec (Grover & Leskovec, KDD 2016).** Biased random walks interpolate between homophily (BFS-like) and structural equivalence (DFS-like). The embeddings feed UMAP for a 2D map and give similarity search over people.
- Alternatives: spectral or SVD embedding of the follow matrix (the Barberá/correspondence-analysis family), or GraphSAGE when you have node text features.

**1.5 Bridges and brokers.**
- **Betweenness centrality** finds nodes on many shortest paths. It is expensive (exact is O(nm)), so use sampled or approximate versions.
- **Burt, structural holes ("Structural Holes and Good Ideas," AJS 2004).** People whose ties span otherwise disconnected groups have more ideas judged good. Metrics: network **constraint** (low = broker) and **effective size**.
- *Cluster-aware bridging metrics* are more useful for SEE: the fraction of a node's engagement edges that land in other clusters, *participation coefficient*, or RWC computed per user.
- *Caveat:* a "bridge" in the graph can be a **conflict node** (quote-dunker) rather than an integrator. Edge semantics are needed to tell them apart. This is the main reason to fuse text stance onto edges (see §4).

**1.6 Data access (Oct 2026).**
- X API is now pay-per-use. Third-party summaries, checked against docs.x.com on 2026-10-10, report:
  - post read $0.005 per resource
  - user read $0.010
  - followers/following read $0.010 per resource
  - **owned reads** of the authenticated user's own followers/following $0.001
  - a cap of 3M post reads per cycle before Enterprise
  - Treat the X Developer Console as authoritative.
  - Cost of one user's 1,000 follows plus 1,000 recent posts: about $1 (owned) to $15 (third-party lookup). Mapping a 50k-account landscape purely via API is in the tens of thousands of dollars. That favors user-donated data.
- **User-donated X archives.** The standard X data export includes the user's following and follower ID lists, so self-onboarding needs zero API spend. (This is from the archive format; **re-verify current export contents**.)
  - **Community Archive** (`TheExGenesis/community-archive`, MIT, Supabase plus Parquet export) is an existing open, consent-based pool of uploaded archives, socially close to the "TPOT" milieu. Its README describes tweets and profiles. Whether follow lists are shared is **UNVERIFIED**.
- **Bluesky / AT Protocol.** Its follow graph and posts are public via firehose and Jetstream, free. It is a natural second source and aligns with Benjamin's AT Protocol work (Free School).

### 2. Text methods

**2.1 The topic-vs-stance failure of embeddings.**
- Ghafouri et al., *"I love pineapple on pizza" != "I hate pineapple on pizza"* (EMNLP 2024).
  - Standard sentence transformers group by topic and fail to separate opposing viewpoints. KL divergence between agree and oppose similarity distributions was about 0.004 for base `all-mpnet-base-v2`.
  - Fine-tuning with Siamese, triplet or hybrid loss plus LoRA on Kialo pro/con pairs raised it to about 0.44 while keeping STS-B at about 0.80 (base 0.83).
  - Stance-aligned retrieval on congressional abortion tweets improved from 76% to 91% (pro) and 67% to 80% (anti).
  - Caveat: one base model, one case study.
- *Implication:* raw embeddings are fine for "what do they talk about" (topic terrain). Do not use them for "what do they believe." Use a stance-aware model, or project embeddings onto anchor-pair axes (the Waller & Anderson trick applied to text).

**2.2 Topic pipelines.**
- **BERTopic (Grootendorst, arXiv 2203.05794).** Embed, reduce with UMAP, cluster with HDBSCAN, then label with class-based TF-IDF (optionally an LLM).
- Good for a terrain layer; it inherits the topic-not-stance bias above.
- HDBSCAN leaves a large "noise" cluster (often 30–50% of short tweets in practice; **UNVERIFIED as a general figure**). Plan UX for unassigned points.

**2.3 Stance detection.**
- Classical target-specific benchmark: SemEval-2016 Task 6.
- Recent surveys cover LLM-based zero-shot stance (arXiv 2409.15690, 2409.13594).
- Törnberg (arXiv 2304.06588) found GPT-4 zero-shot beat expert and crowd coders on party-affiliation annotation of tweets.
- Stance is *target-relative*. You must define the targets (propositions) first. Ontography's claims or dimensions supply exactly that target list.
- A PMC paper on the promises and pitfalls of LLM actor-stance detection (PMC12629487) was blocked by a captcha, so it was not read. **UNVERIFIED.**

**2.4 Argument mining and LLM claim extraction.**
- **Claimify (Metropolitansky & Larson, Microsoft Research, ACL 2025, arXiv 2502.10855).**
  - Evaluates extracted claims on three criteria: **entailment** (supported by source), **element-level coverage**, and **decontextualization** (enough context to verify).
  - It flags ambiguous sentences and extracts only when the meaning is resolvable.
  - Its *selection* stage (filtering for checkable content first) contributed most.
  - Directly addresses Ontography's known issue of separating AI inference from real belief: adopt entailment checking and an "ambiguous → do not extract" rule.
- Hallucination risk is highest in Ontography's "assumption descent" step, where the LLM infers unstated premises. Those nodes must be typed as *inferred*, visually distinct, and confirmable by the person (Ontography already has verify/edit/retract endpoints).

**2.5 Moral and value lenses.**
- **Moral Foundations.**
  - Original MFD (Graham, Haidt & Nosek 2009).
  - **eMFD** (Hopp et al., Behavior Research Methods 2021): crowd-annotated, probabilistic word weights.
  - **MFQ-2** (Atari et al. 2023): six foundations, with fairness split into *equality* and *proportionality*. Attribution from memory; **verify**.
  - **MoralBERT** (Preniqi et al., arXiv 2403.07678): in-domain F1 about 0.66 single-label vs 0.18 for the MoralStrength lexicon. Large out-of-domain drops across platforms; domain-adversarial training only partly helps.
  - *Lexicons are nearly useless on tweets; fine-tuned or LLM classifiers are needed, and they are platform-sensitive.*
- **Schwartz values.** SemEval-2023 Task 4 (ValueEval) covers 20 value categories behind arguments. Best main-test F1 was 0.56 vs a BERT baseline of 0.42. Robustness sets (NYT 0.34, Nahj al-Balagha 0.40) show steep drops. Values are detectable, but noisily.
- **Koltko-Rivera, "The Psychology of Worldviews" (Rev. Gen. Psych. 2004).**
  - 42 dimensions in 7 groups: Human Nature, Will, Cognition, Behavior, Interpersonal, Truth, and World & Life (ontology, cosmos, deity, humanity–nature, purpose, etc.).
  - This is the most complete *theoretical* scaffold for "worldview" beyond politics. It maps cleanly to Ontography's ontological, epistemological, axiological and praxis layers.
  - No validated text classifier for it exists, as far as found. LLM or Jev questions per dimension would be novel and need validation.

### 3. Cheap classification without embeddings: what "Jev" is

**Identified with high confidence: Jev by TypeSafe AI.**
- **Who and when.** TypeSafe came out of two years of stealth. Co-founder and CEO Diogo Almeida is ex-OpenAI, described as a co-inventor of RLHF/InstructGPT. The company raised a $40M seed led by DCVC. Launch post dated **15 Sept 2026**. TypeSafe brands it the first "System One" model. The Batch (DeepLearning.AI) covered it as taking "the developer world by storm" and inspiring imitators.
- **What it does.** It takes text (`state`) plus named questions. Each question is evaluated in parallel and returns structured probabilities. It never generates text.
  - Choice questions return a label, confidence, and per-label probabilities.
  - Score questions (2–10 ordered levels) return an expected value and a distribution.
  - "noul" (yes/no) questions return P(true).
- **Architecture.**
  - Undisclosed. Described as transformer-based but *not* an autoregressive LLM, with a new sampler and training method, **RLCD (Reinforcement Learning for Calibrated Decisions)**.
  - No user-side embedding or encoding step: you send text and questions and get a category back. That matches Benjamin's description.
  - Whether it internally uses an encoder is undisclosed.
- **Cost and latency.**
  - Pricing: $0.042 per million input tokens; output is free.
  - Most calls take about 100 ms.
  - LiteLLM's auto-router benchmark (80 cases × 3 runs): p50 127 ms vs Claude Haiku 4.5 at 688 ms, about 96% lower classifier cost. Caveat: single-author labels.
  - Context window is 32K (NanoGPT docs pin `jev-1.13`). Text only.
- **Accuracy caveats.**
  - The Batch: on TypeSafe's internal sets, about 67% accuracy, comparable to frontier LLMs, at about $0.0007 per example.
  - An independent "JevBench" sealed hard set: Jev 36.7%, open `decider-4b v2` 34.7%, a frontier LLM 95.5% at 3.4× Jev's cost. **Treat this third-party benchmark as low-confidence.**
  - TypeSafe's own limitations list dates, arithmetic and adversarial input. "Can't hallucinate" only means it can't answer outside your options. It can still be wrong. Access: waitlist dropped 20 Sept, new signups paused 22 Sept 2026, so **check availability**.
- **Open imitators.**
  - **Laya**: ModernBERT-large encoder, CPU-runnable.
  - **decider-4b**, **Winnow-12B**, **Kev** (a Qwen 3.5 reconstruction), **Bespoke Nimble** (fine-tuned Qwen-3.5-9B).
  - The do-it-yourself pattern: one forward pass of any instruct LLM, constrain logits to option letters, read probabilities, and calibrate with temperature scaling.

**Other candidates (if "Jev" meant something else):**

| Candidate | What it is | Embedding step? | Fit for SEE |
|---|---|---|---|
| **GLiClass** (Knowledgator, arXiv 2508.07662) | Open uni-encoder zero-shot classifier; labels and text in one forward pass | Encoder internally; no separate embedding pipeline | Large model F1 0.719 vs 0.682 for the best cross-encoder. Throughput drops only 7–20% from 1 to 128 labels. Apache-2.0, self-hostable |
| **SetFit** (Tunstall et al., arXiv 2209.11055) | Contrastive fine-tune of a sentence transformer from about 8–16 examples per class, plus a logistic head | Yes | Cheapest *trainable* option; good for a fixed taxonomy once you have a few labels |
| **gzip + kNN** (Jiang et al., ACL Findings 2023) | Compression-distance classifier | No | Not recommended. Reported results relied on optimistic top-2 tie-breaking; corrected, it ranks below TF-IDF + LR (Sinai 2023) |
| **LLM-as-classifier** | Prompted frontier or small LLM, logprobs over options | No | Most accurate on hard items; 10–100× costlier per item |
| **JEPA** (LeCun) | Self-supervised joint-embedding *predictive architecture* | It *is* an embedding approach | Not a classifier; name collision only |

### 4. Multi-layer / multiplex fusion

- **Multiplex community detection.** Mucha et al., *Science* 2010 (arXiv 0911.1824), generalizes modularity to multislice networks: layers coupled by inter-layer edges of strength ω. Run on layers such as follow, retweet, quote and reply, plus a *text-similarity kNN layer* and a *claim-agreement layer*, all over the same node set. Sweeping ω shows which communities hold across all layers (robust tribes) vs one layer only. Kivelä et al. (2014) review the formalism. Implementations: `leidenalg` multiplex, and `graph-tool` layered SBM.
- **Signed agreement graph.** Edge sign comes from stance:
  - retweet = +
  - quote-with-negative-stance = −
  - reply with disagreement = −
  - same-claim, opposite-stance = −

  Garimella, Weber & De Choudhury (WebSci 2016, arXiv 1603.07933) showed quote-RTs increased political discourse. Whether they mostly encode disagreement is **not established by the abstract**; classify each quote's stance rather than assuming. Signed clustering then separates *allies* from *frequent sparring partners*, which plain modularity merges.
- **Joint embeddings.** Concatenate or align node2vec (graph) with mean stance vectors (text), or train a graph neural net with text node features. Simplest robust option is **late fusion**: compute each layer's coordinates separately and show their *agreement* (e.g., adjusted mutual information between graph clusters and stance clusters) as a confidence signal.
- **Latent-axis discovery from disagreement.**
  - Polis: participant × statement agree/disagree matrix, PCA, k-means (newer forks use Leiden and UMAP), groups plus "consensus" statements.
  - Community Notes: rater × note matrix factorization (Wojcik et al., arXiv 2210.15723). Andreou & Sirivianos (arXiv 2609.21496, 2026) refit it with **two** latent dimensions on about 213M ratings. They found:
    - a left/right axis
    - an independent second axis (provisionally *trust in institutions*) that transfers to held-out topics
    - notes that are polarized only on axis 2 publish far less (71.5% → 11.7%)
  - *Implication for SEE:* do not force one axis; at least two are empirically present in X's own population.
- **Progressive disclosure.**
  1. **Constellation overview.** 2D map with nodes colored by L0 cluster. Show only cluster hulls and auto labels, plus the user's own "you are here" dot and 3–5 nearest bridges. Hard cap of about 7 visible clusters at a zoom level. The hierarchy comes from the Leiden resolution sweep or nested SBM.
  2. **Cluster profile card.** Exemplar accounts (highest within-cluster centrality), top topics (BERTopic labels), position on L1 axes (radar or strip plots with uncertainty bars), MFT/Schwartz fingerprint, representative claims, and "what this cluster disagrees with [neighbor] about" (highest-variance claims between clusters, as in Polis group-informed statements).
  3. **Person view.** Graph coordinates, axis positions with confidence, who they bridge to, and the share of their engagement that crosses clusters.
  4. **Claim graph.** On demand, for one person or a dyad (Ontography handshake). Cap at about 50–80 nodes by default, with the deepest assumptions first, inferred nodes visually distinct, and every node linked to its source post.

  This fixes the illegibility of 600–1,200-node graphs: those are never the entry view.

### 5. Validation

**Ground-truth options, strongest first:**
1. **Self-report.** Onboarding asks a short instrument: MFQ-2 items, a few Koltko-Rivera or Ontography dimensions, self-placement, and "which of these clusters feels like home?" Correlate it with the inferred position. Barberá validated against self-declared preferences and party registration.
2. **Known-group / anchor accounts.** Accounts with public, unambiguous positions (elected officials, org accounts, authors of manifestos). Check that they land where expected. Wu et al. used DW-NOMINATE correlation. For non-political axes, use expert-labeled anchors.
3. **Expert or crowd labels.** Labeled post subsets for each classifier (Jev or GLiClass), with inter-annotator agreement reported. Calibration check: does a confidence of 0.8 mean about 80% correct? (RLCD's claim is testable.)
4. **Stability tests.** Re-run clustering across seeds, resolutions, time windows and subsampled edges (bootstrap). Report cluster-level Jaccard stability; hide clusters below threshold. Multiplex ω sweeps double as stability tests.
5. **Predictive validity.** Positions should predict *held-out behavior*: future retweets, which Community-Notes-style statements a user agrees with, and (in MEET) dialogue moves. Andreou & Sirivianos' leave-topics-out transfer test is a model to copy.
6. **Face validity / member checking.** Users rate "this describes me" on their profile card. This also generates training labels. It is an Ontography-style verify/retract loop applied to cluster summaries.

**Known pitfalls:**
- **Homophily ≠ shared worldview.** People follow for news, professional reasons, hate-follows and celebrity. Graph proximity measures audience overlap, not belief. Mitigate by weighting retweets (endorsement) above follows and by fusing with stance.
- **Topic ≠ stance** in embeddings (§2.1).
- **Lurkers and skew.** Pew (2019): the top 10% of US adult tweeters produce about 80% of tweets. Text layers will cover a minority, so lurkers can be placed only by the graph. Show "graph-only estimate" honestly.
- **Bots and coordinated accounts.** Rauchfleisch & Kaiser (PLOS ONE 2020) showed Botometer has substantial false positives and negatives, sensitive to thresholds and language. The paper text was not retrieved here, so **re-verify specifics**. Botometer access was effectively ended by X API changes. Prefer behavioral filters (coordination, posting cadence) plus manual review of high-centrality nodes.
- **Sarcasm, irony, quote-dunks.** These flip stance. LLM or Jev questions should include "is this ironic or quoting to mock?" as a separate yes/no.
- **Exposure effects.** Bail et al. (PNAS 2018): Republicans paid to follow a liberal bot became *more* conservative. A map that pushes cross-cluster exposure without MEET-style structure can backfire.
- **Temporal drift.** Waller & Anderson found polarization shifts came from new entrants. Maps need time-stamped versions.
- **Reflexivity and harm.** A public "who belongs to which tribe" map enables targeting and doxxing-adjacent harms. Default to consent-based (self-onboarded or public-figure) placement. Show non-consenting private accounts only in aggregate.

### 6. Practical pipeline at scale

**Rough cost and latency for one user onboarding** (≈1,000 follows, 2,000 posts, about 60k tokens):

| Step | Tool | Cost / latency |
|---|---|---|
| Fetch follows | X archive upload (free) or owned API read | $0–$1; seconds |
| Place on graph | Precomputed landscape: project the user's follow vector onto the stored community model (Barberá-style or kNN over follow-vectors) | ms |
| Classify posts on ~20 axis questions | Jev (≈60k tokens × 20 Q ≈ 1.2M tokens ≈ $0.05) or self-hosted GLiClass (GPU seconds) | ~seconds batched |
| Claim extraction (on demand only) | Frontier LLM with Claimify-style entailment check | ~$0.10–$1, 30–120 s |
| Render | Precomputed tiles plus user overlay | instant |

**Landscape build (offline, ~10^5 accounts, ~10^7 edges):** Leiden in igraph takes minutes. Nested SBM in graph-tool takes hours. node2vec plus UMAP takes about 10–30 minutes on a GPU. Text classification of about 10^7 posts × 20 questions via Jev is about 10^10 tokens, roughly $400. Graph data acquisition dominates cost, so seed from consenting uploads, Bluesky, and a curated anchor set (about 2–5k accounts) via API.

**Visualization tooling:**
- **sigma.js + graphology.** WebGL 2D graphs, about 10^5 nodes comfortably; graphology has Louvain/Leiden-adjacent layout and metrics in JS. Good default for the interactive overview.
- **Cosmograph (cosmos.gl).** GPU force simulation in-browser. The vendor claims force layout beyond 50k points and rendering past 1M. Native Parquet. Good for a live "watch it settle" landscape.
- **deck.gl.** ScatterplotLayer/TextLayer for precomputed coordinates at 10^6 or more; maximal control, pairs with tiles.
- **Datamapplot** (McInnes). Static and interactive "data maps" with multi-level labels, about 500k points smooth, outputs standalone HTML. Best for the cluster-labeled overview aesthetic.
- **Nomic Atlas / deepscatter.** Hosted embedding maps with millions of points. Fast to prototype; vendor lock-in.
- **Apple Embedding Atlas** (Ren et al., arXiv 2505.06386). Open source; 4M points at 60 fps on an M1 Pro, cross-filtering and auto-labeling. A strong open alternative to Nomic.
- **react-force-graph-3d** (Ontography's current choice). Fine for claim graphs under about 1k nodes; not for the landscape.

---

## How this answers the governing question (layering + validation)

**Recommended SEE architecture: five layers, each with an explicit job.**

| Layer | Signal | Method | Good at | Bad at |
|---|---|---|---|---|
| **L0 Belonging backbone** | Follow + retweet (+ quote/reply as typed edges) | Leiden hierarchy (or nested SBM) on a weighted multiplex; node2vec → UMAP coordinates; Barberá-style projection to place new users | Tribe membership, cheap, works for lurkers, well validated in the literature | Says nothing about *why*; hate-follows and professional follows; needs a graph corpus |
| **L1 Axis coordinates** | Posts → fixed question battery | Jev (or GLiClass / SetFit self-hosted) answering ~10–30 calibrated questions: Ontography dimensions, MFQ-2 foundations, Schwartz higher-order values, 2–3 Koltko-Rivera items, irony flag. Anchor-account scaling via LLM pairwise + Bradley–Terry | Interpretable, comparable positions with probabilities; cheap at scale; directly feeds MEET matchmaking | Only as good as the question design; platform drift; lurkers have no text |
| **L2 Terrain** | Post text | Stance-aware sentence model (Kialo-tuned, EMNLP 2024 recipe) + BERTopic labels | What clusters talk about; labels for the map; finding shared topics across tribes | Raw embeddings conflate stance (use only for terrain and labels) |
| **L3 Reason graphs** (on demand) | Selected posts or long-form | Ontography extraction with Claimify-style selection, entailment and ambiguity gating; inferred-vs-stated typing; user verification | The *why*: assumptions, fault lines, shortest paths between two people | Expensive, slow, hallucination-prone in assumption descent; illegible if shown whole |
| **L4 Bridges and axes** | L0 + L1 combined | Signed agreement graph; per-user cross-cluster share, participation coefficient, Burt constraint; 2-D matrix factorization on agree/disagree data (Community-Notes style) once MEET produces it | Finds integrators vs sparrers; discovers non-left/right axes | Needs edge stance; MF needs interaction data that MEET will generate |

**Alternatives:**
- **(A) Text-first:** skip the graph and map embeddings plus stance. Cheaper data but weaker validity; it maps topics.
- **(B) Graph-only:** Barberá plus Leiden. Fastest MVP and very defensible, but it gives "who," not "what they believe." Good v0.
- **(C) Polis-native:** have users vote on claim statements and run MF/PCA. The highest-validity *belief* map, but it needs participation. This is the natural bridge to the MEET layer. The recommended path is B → B+L1 → add L3 on demand → add C as MEET data accrues.

**Layer validation:**
- Each layer is validated independently: L0 by anchor accounts and stability; L1 by labeled sets and calibration plus self-report correlation; L3 by entailment rate and user-verification rate.
- The map shows the *agreement between layers* as a confidence cue. When graph cluster and axis profile disagree, show it ("structurally in cluster X, but voices positions closer to Y"). That disagreement is often itself the interesting edge-node signal.

---

## Reusable assets / design implications

- **Ontography already has** the L3 machinery (extractor, assumption descent, handshake, verify/retract), the 8 "core spectrums" in `src/lib/protocol/dimensions.ts`, and a four-layer category model. Its dimensions can become L1 Jev question batteries almost verbatim. (Repo: `/home/claude/auto-ontography-archive`, `docs/ARCHITECTURE.md`.)
- **Dialectical Topology** has a pipeline (`generate_embeddings.py`, `project_umap.py`, `cluster_by_claims.py`) for the L2 terrain lens. Swap in a stance-aware model. (Path: `/home/claude/omniharmonic/dialecticaltopology/pipeline/`.)
- **Libraries:** `tweetscores` / `twitter_ideology` (R, Barberá); `CSSLab/social-dimensions` (anchor-axis method); `leidenalg`, `graph-tool`, `graspologic`; `bertopic`; `gliclass`; `setfit`; `datamapplot`; Embedding Atlas; sigma.js/graphology; cosmos.gl.
- **Data:** user X archive upload (own follows, free); Community Archive (consenting archives); Bluesky Jetstream (free public graph); X pay-per-use for the anchor set.
- **UX rule:** never render more than about 7 clusters or about 80 claim nodes at once. Always show provenance and confidence. Mark inferred items visually.
- **Jev usage pattern:** one `state` (user's recent posts, chunked to under 32K tokens), many named `score` questions (0–10 on each axis) plus `noul` irony and bot-likeness checks. Store the probability vectors, not only argmax, so uncertainty can be shown.

---

## Risks & open questions

1. **Jev dependency.** Closed weights, US-hosted, signups paused at the time of writing, internal-only accuracy claims. Mitigate with a provider-agnostic interface (`classify(state, questions) → probs`) and a GLiClass or open decider fallback. Run a 300-item labeled pilot comparing Jev, GLiClass and a frontier LLM on Ontography axes before committing.
2. **Axis selection is political.** Which dimensions define the map shapes what people see. Expose the axes, allow user-proposed axes, and prefer data-discovered axes (MF on agreement data) over imposed ones over time.
3. **Consent and ethics.** Placing non-consenting private individuals on a tribal map is risky. Default to opt-in plus public figures.
4. **X data cost and terms.** Check the X Developer Agreement on deriving and displaying political inferences about users (**not reviewed here**).
5. **Open question.** Does the TPOT-adjacent milieu (Owocki's tribes visualizer audience) cluster meaningfully on left/right at all? Likely the second axis (institutional trust) and Koltko-Rivera-type metaphysical axes dominate. Test empirically.
6. **Blocked sources to re-verify:** PNAS Cinelli full text, PMC12629487 (LLM stance pitfalls), PMC Rauchfleisch & Kaiser full text, ICWSM Conover page, SimClusters details, MFQ-2 attribution, Community Archive follow-data availability, X export contents.

---

## Sources

- Conover et al., "Political Polarization on Twitter," ICWSM 2011 — https://ojs.aaai.org/index.php/icwsm/article/view/14126 (blocked; see also https://cnets.indiana.edu/news/icwsm-test-of-time-award)
- Barberá et al., "Tweeting From Left to Right," Psychological Science 2015 — https://www.sciencedaily.com/releases/2015/08/150827083423.htm ; https://www.psychologicalscience.org/journals/psychological-science/0956797615594620/
- Barberá, "Birds of the Same Feather Tweet Together," Political Analysis 2015 — https://csmapnyu.org/research/academic-research/birds-of-the-same-feather-tweet-together-bayesian-ideal-point-estimation-using-twitter-data ; code https://github.com/pablobarbera/twitter_ideology
- Cinelli et al., "The echo chamber effect on social media," PNAS 2021 — https://www.isi.it/news/2021-02-de-francisci-morales-starnini ; https://pubmed.ncbi.nlm.nih.gov/33622786/
- Garimella et al., "Quantifying Controversy in Social Media" — https://arxiv.org/abs/1507.05224
- Garimella, Weber, De Choudhury, "Quote RTs on Twitter" — https://www.arxiv.org/abs/1603.07933
- Waller & Anderson, "Quantifying social organization and political polarization in online platforms" — https://arxiv.org/abs/2010.00590 ; https://github.com/CSSLab/social-dimensions
- Wu, Nagler, Tucker, Messing, "LLMs Can Be Used to Estimate the Latent Positions of Politicians" — https://arxiv.org/abs/2303.12057
- Satuluri et al., SimClusters, KDD 2020 — https://dblp.uni-trier.de/rec/conf/kdd/SatuluriWZQWDTJ20.html (details UNVERIFIED)
- Traag, Waltman, van Eck, "From Louvain to Leiden" — https://arxiv.org/abs/1810.08473
- Peixoto, Bayesian stochastic blockmodeling — https://arxiv.org/abs/1705.10225 ; https://graph-tool.skewed.de
- Traag & Bruggeman, community detection with positive and negative links — https://arxiv.org/abs/0811.2329 ; signed bipartite sensitivity https://arxiv.org/abs/2405.08203
- Grover & Leskovec, node2vec — https://arxiv.org/abs/1607.00653
- Burt, "Structural Holes and Good Ideas" — https://snap.stanford.edu/class/cs224w-readings/Burt04StructureHole.pdf
- Mucha et al., multislice community structure — https://arxiv.org/abs/0911.1824
- Wojcik et al., Birdwatch / bridging — https://arxiv.org/abs/2210.15723
- Andreou & Sirivianos, "Two Fault Lines: Latent Polarity Geometry in X Community Notes" (2026) — https://arxiv.org/abs/2609.21496
- Polis algorithms (secondary) — https://societyspeaks.io/help/polis-algorithms ; Small et al. 2021 https://www.gwern.net/doc/sociology/2021-small.pdf
- Ghafouri et al., Stance-Aware Sentence Transformers, EMNLP 2024 — https://aclanthology.org/2024.emnlp-main.1171.pdf
- Grootendorst, BERTopic — https://arxiv.org/abs/2203.05794
- Stance detection surveys — https://arxiv.org/abs/2409.15690 ; https://arxiv.org/abs/2409.13594
- Törnberg, ChatGPT-4 annotating political tweets — https://arxiv.org/abs/2304.06588
- Metropolitansky & Larson, Claimify — https://arxiv.org/abs/2502.10855
- Preniqi et al., MoralBERT — https://arxiv.org/html/2403.07678v1
- Hopp et al., eMFD — https://www.pubmed.gov/32666393/
- Kiesel et al., SemEval-2023 Task 4 ValueEval — https://touche.webis.de/semeval23/touche23-web/
- Koltko-Rivera, "The Psychology of Worldviews" (summary) — https://integralleadershipreview.com/5395-feature-article-leadership-and-worldview-what-in-the-world-is-a-worldview/ ; PDF https://lup.lub.lu.se/search/files/5733804/3738786.pdf
- Jev — The Batch: https://www.deeplearning.ai/the-batch/models-built-to-do-one-thing-well ; The New Stack: https://thenewstack.io/typesafe-jev-system-one/ ; LiteLLM benchmark: https://docs.litellm.ai/blog/jev-auto-router-benchmark ; NanoGPT API docs: https://docs.nano-gpt.com/api-reference/endpoint/jev-decisions.md ; reality check / JevBench / imitators (secondary): https://www.modemguides.com/blogs/ai-news/jev-typesafe-reality-check-run-locally
- GLiClass — https://www.arxiv.org/abs/2508.07662 ; https://huggingface.co/knowledgator/gliclass-modern-large-v3.0
- SetFit — https://arxiv.org/abs/2209.11055
- gzip+kNN critique (Sinai) — https://liorsinai.github.io/machine-learning/2023/08/13/gzip-knn.html
- Pew, Twitter users 2019 — https://www.pewresearch.org/short-reads/2019/04/24/key-takeaways-from-our-new-study-of-how-americans-use-twitter/
- Bail et al., PNAS 2018 (opposing views) — https://www.niemanlab.org/2018/08/republicans-who-follow-liberal-twitter-bots-actually-become-more-conservative/
- Rauchfleisch & Kaiser, bot-detection false positives — https://cyber.harvard.edu/publication/2020/false-positive-problem-automatic-bot-detection-social-science-research
- X API pricing (third-party summary of docs.x.com) — https://opentweet.io/x-api-pricing
- Community Archive — https://github.com/TheExGenesis/community-archive
- Bluesky data — https://arxiv.org/abs/2408.03146
- Cosmograph comparison (vendor) — https://cosmograph.app/docs-lib/comparison/
- Embedding Atlas (Apple) — https://arxiv.org/abs/2505.06386
- DataMapPlot — https://datamapplot.readthedocs.io/en/latest/intro_splash.html
- Nomic data mapping — https://home.nomic.ai/blog/posts/data-mapping
- Ontography — /home/claude/auto-ontography-archive/docs/ARCHITECTURE.md ; Dialectical Topology — /home/claude/omniharmonic/dialecticaltopology/pipeline/, META_ANALYSIS.md
