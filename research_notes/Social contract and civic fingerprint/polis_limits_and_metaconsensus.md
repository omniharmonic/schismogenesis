# What limits Polis clustering, what would replace each part, and a prior-art check on the "described side signs" score (2 Nov 2026)

Reading guide. Evidence labels:
- [code/docs]: primary source read.
- [peer-reviewed]: journal or conference paper, full text read through a fetch or extraction.
- [preprint]: unreviewed paper, text read.
- [abstract]: only the abstract or a repository record was read.
- [digest]: seen only through a search summary; the paper was not opened.
- [informal]: blog, forum or discussion.

"Inferences" are my own reasoning.

This builds on `research_notes/Memetic mapping and computational democracy/polis_notes_bridging.md` and does not repeat it. Web search hit the session cap at the very end; the one lost search is noted in Question 1's Gaps. "Not found" below means "not found in the searches run", not "does not exist".

Three important items for the report writer:
- **Report correction.** The report's novelty candidate 3 (fidelity calibrated with real in-group statements and decoys) needs narrowing. See Question 4.
- **Naming correction.** The score should not be called a meta-consensus measure. See Question 4.
- **Unresolved document conflict.** `CLAUDE.md` defines meta-consensus as clusters describing each other in terms the described side would sign. Dryzek and Niemeyer's concept is wider. Flagged rather than resolved.

## 1. What Polis clustering cannot do, limit by limit

### Takeaway
Fifteen limits were checked. Nine have direct evidence in code or the Gelauff corpus. Three rest on inference from the design (person-level uncertainty, small-group erasure, the 2D projection). Three have no direct study at all: statement-order effects, strategic voting against clustering, and whether Polis groups match survey-validated groups. The deepest limit for Arena is identity: 89.1% of participants vote in one session of about four minutes under a cookie, so Polis groups are snapshots that cannot be compared across conversations.

### Cited Findings
**Already covered in the prior notes, one line each.** Hard-coded k of 2 to 5, power-iteration warm start, mean imputation, 2-group share of 74.6% reported vs 62.5% recomputed, and routing asymmetry. New evidence for each limit follows.

**1. 2D projection of many dimensions.**
- Evidence that real opinion needs more than 2 axes comes from outside Polis. Lauderdale and Clark found best fit at 20 to 30 dimensions for court votes, and Community Notes gains held-out accuracy at rank 2 (both in prior notes).
- An informal Japanese study group saw 592 respondents on 42 questions fall into two parts under PCA and six under UMAP, offered as a preliminary observation and possible over-fragmentation. [Cybozu study group](https://nishio.github.io/quartz_deploy/High-dimensional-data-analysis-study-group) [digest, informal]
- I found no study that compares Polis's 2D groups with higher-dimensional fits on Polis data.

**2. Hard assignment.**
- Group output is one label per person with no membership probability (prior notes on `conversation.py`). Mixed-membership models exist that give per-subject scores on categorical data. [Finding mixed memberships](https://arxiv.org/abs/2312.01565) [abstract]

**3. Number of groups.**
- Beyond the cap, the participant threshold of 7 votes is described as an arbitrary hyperparameter. [Small et al. reading notes](https://kweel.github.io/quartz/Bibliography/smallPolisEscalarDeliberacion2021) [digest, informal]

**4. Groups depend on what was seeded and moderated.**
- Conveners prepared a median of 23 seeds. The median conversation closes with 17.6% of statements seeded from the start, IQR 4 to 32%, maximum 77%. [Gelauff 2026](https://arxiv.org/pdf/2608.28368) [preprint]
- 29.4% of votes on opening seeds are disagreements vs 17.0% for participant statements. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Statements rejected after voting are "zeroed out" of the clustering matrix: 180,944 votes sit on later-rejected statements, 89% of them real. The moderator therefore edits the matrix after people have voted. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Conversations split into two types: exhaustible (48 of 118) and open-ended (64 of 118), with different participant behaviour. Comparing them as if alike is unsafe. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)

**5. Ordering effects.**
- No controlled test of statement order on votes or dropout was found.
- The docs warn that comments arriving after most participants have voted are under-represented. [Polis best practices](https://www.github.com/pol-is/polis-documentation/blob/master/usage/BestPractices.md) [code/docs]
- Contributors argue informally that later items do not suffer position bias because order is neither random nor fixed. [Okumura discussion](https://scrapbox.io/nishio-en/Polis_discussion_with_Dr._Okumura) [digest, informal] That argument does not show order has no effect, since routing makes order depend on the statement.

**6. Response counts.**
- Median participant in the median conversation: 25.5 votes. Median first session: 30 votes in 239 seconds. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- vTaiwan Uber: 197 comments, about 10.57 votes per participant, roughly 5%. [Halpern et al.](https://arxiv.org/pdf/2211.15608) [peer-reviewed]
- Adding statements barely adds votes: elasticity 0.190 [0.122, 0.264]. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)

**7. Missing not at random.**
- Routing depends on prior votes, so missingness is endogenous (prior notes on Blair).
- Latency differs by position: participants take 10.1% longer when disagreeing with the majority (95% CI +9.3 to +11.1%), in 153 of 155 conversations. Attention and cost of expression therefore vary with stance. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- A direct method exists for informative silence in votes: a Latent Block Model with nonignorable missingness, applied to French National Assembly votes, co-clusters MPs and texts and interprets non-voting. [Frisch et al. arXiv 2010.12222](https://arxiv.org/abs/2010.12222) [abstract; author name from memory, check]

**8. Pass ambiguity.**
- PASS enters the denominator and never counts as agree or disagree, so it dilutes both rates and affects z-tests. [repness.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/pca_kmeans_rep/repness.py) [code/docs]
- Pass behaves as disengagement. Statements later rejected drew 9.3 points less agreement (CI 4.4 to 14.1), not significantly more disagreement (+2.6, CI −1.0 to +6.4), and +6.7 points of passes (CI 3.8 to 9.8). Pass is doing the work of "this statement is bad", not "I am neutral". [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- The interface offers only agree, disagree and pass. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)

**9. No intensity.**
- The repness code has no weight or importance field; every vote counts as one. [repness.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/pca_kmeans_rep/repness.py) [code/docs]

**10. No person-level uncertainty.**
- No code path reports a confidence interval on placement. Sparse voters are only pushed outward by a scaling factor (prior notes on `pca.py`). Bayesian IRT gives posterior intervals by construction. [Clinton, Jackman and Rivers](https://cdn.vanderbilt.edu/vu-my/wp-content/uploads/sites/349/2011/10/14093745/CJR_APSR2004.pdf) [digest]

**11. No stable identity across conversations.**
- A participant is "a series of votes submitted with the same identification cookie"; Polis is optimized for ease of access, not identification. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Single-session share is 89.1% [82.0, 93.8]. The author cannot rule out that returners are logged as new. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Each Polis conversation has its own groups and no shared items, so groups in conversation A have no defined relation to those in B. This is the same problem as separate ideal point runs, which land on different latent scales. [Operationalizing Legislative Bodies](https://arxiv.org/pdf/2211.17066) [digest]

**12. Small-group erasure.**
- No direct measurement in Polis was found. The structural evidence is the cap of 5 groups and silhouette selection.
- Consensus-style selection can erase minority voices. [Hafid et al.](https://arxiv.org/pdf/2602.15439) [preprint, prior notes]
- Group-size guarantees exist elsewhere. Balanced justified representation protects any cohesive group of n/k or larger; below that there is no guarantee. [Fish et al.](https://arxiv.org/html/2309.01291v3) [peer-reviewed]

**13. Strategic voting.**
- Two searches, here and in the prior notes, found no study of manipulating Polis clustering.
- Polis injects an automatic agree for a statement's author. Of 6,980 scorable authored statements, 18.5% had a predicted stance of disagreement. So some recorded votes are not real positions. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Baseline authentication is weak: identity is a cookie, so a person who clears cookies can count as many. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)

**14. Statement quality.**
- Moderation is a convener choice, with votes zeroed afterward (item 4). Blair's metrics treat all splits alike and suggest weighting by substantiality as future work (prior notes).

**15. Do Polis groups match survey-validated groups?**
- No validation of Polis groups against survey-validated segments or demographics was found. Self-selection is the standing concern. A convener-independent benchmark does not exist in the sources found.

### Inferences
- Limit 11 is the one no change of clustering algorithm can fix. It needs item design (shared anchors) and identity design, not better math.
- Limit 8 suggests Arena should split pass into at least "unsure", "don't understand or bad statement", and "not my issue". Each has a different use: only the second should feed quality scoring.
- Limit 4 implies any cross-round comparison needs moderation frozen before scoring, not after.
- Authors' auto-agree votes must not be copied. Ask authors to vote like everyone else.

### Gaps
- Whether current Polis has an "important" vote flag: my targeted search was lost to the session search cap, and the first attempt returned nothing relevant. The repness code shows no weight, but a flag could exist elsewhere in the product. Check the Polis client before saying "Polis has no intensity measure" in public.
- No controlled order experiment, no strategic attack study, no survey validation found. Each would be a real contribution.
- The Gelauff preprint is one author's work and unreviewed; the arXiv number should be checked before formal citation.

## 2. Replacements, and which have been tested on Polis-like data

### Takeaway
Almost none of these have been published on Polis data. The closest evidence is on legislative votes. The practical answer is that the public Polis exports let every option be tested offline at no cost, and that is a real open niche. My recommended test order: Bayesian multidimensional IRT with MNAR missingness, then latent block co-clustering, then mixed membership.

### Cited Findings
| Method | Closest tested data | Tested on Polis? | Source |
|---|---|---|---|
| Latent block co-clustering with MNAR | French Assembly votes | No | [arXiv 2010.12222](https://arxiv.org/abs/2010.12222) [abstract] |
| Mixed membership (grade of membership) | Categorical data; political ideology use noted | No | [2312.01565](https://arxiv.org/abs/2312.01565), [1910.04883](https://arxiv.org/pdf/1910.04883) [digest] |
| Bayesian mixture of voting blocs | Longitudinal referendum data | No | [2301.01677](https://arxiv.org/pdf/2301.01677) [digest] |
| Hierarchical Dirichlet mixture with missing values | Survey data | No | [2412.17335](https://arxiv.org/pdf/2412.17335) [digest] |
| Bayesian IRT, fast EM versions | Roll calls; binary and ordinal | No | [Imai, Lo, Olmsted](https://imai.fas.harvard.edu/research/fastideal/) [digest] |
| IRT with subgroup-specific item parameters | Survey and vote scaling | No | [Shiraito, Lo, Olivella](https://ar5iv.arxiv.org/html/2205.05934) [digest] |
| Structured IRT, ideal points dependent on groups | Conference abstract | No | [Goplerud EPSA 2025](https://coms.events/epsa2025/data/abstracts/en/abstract_1034_0511_0976.html) [digest] |
| Stance classification then IRT | Documents | No | [Semantic Scaling](https://arxiv.org/pdf/2405.02472.pdf) [digest] |
| Signed two-mode blockmodel | Supreme Court votes (2009) | No | [Signed two-mode blockmodel](https://informahealthcare.com/doi/abs/10.1080/00222500902946210) [digest] |
| Community detection on projected signed bipartite graphs | Voting and product graphs | No | [2405.08203](https://arxiv.org/pdf/2405.08203v2) [digest] |
| Bipartite SBM, multi-layer degree-corrected | Bipartite networks, unsigned | No | [same search result](https://arxiv.deeppaper.ai/papers/2405.08203v2/similar) [digest, weak] |
| Bayesian Consensus Clustering | Biological data sources | No | [1302.7280](https://arxiv.org/abs/1302.7280) [digest] |
| Hierarchical, Leiden | Listed by Polis's docs | Available, no benchmark found | [compdemocracy algorithms](https://compdemocracy.org/algorithms/) [code/docs] |

- Signed bipartite community detection is reported as "highly dependent on parameter choice", needing careful validation. [2405.08203](https://arxiv.org/pdf/2405.08203v2) [digest]
- Leiden cluster counts swing with resolution: about 23 at 0.2 to over 50 at 0.8 on one biological dataset. [Figure](https://onco.img.cas.cz/novotnyj/scdrake/integration/02_int_clustering/dimred_plots/cluster_graph_leiden_all_umap.pdf) [digest, biology, weak]

**Linkage across conversations with shared anchors.**
- Separate estimates cannot be equated directly; fixes are bridge actors, fixed-preference assumptions, or vignettes. [arXiv 2211.17066](https://arxiv.org/pdf/2211.17066) [digest]; [Shiraito et al.](https://ar5iv.arxiv.org/html/2205.05934) [digest]
- Bridge items have a known failure. Jessee questioned whether shared items create a common space, because legislators and voters may read items and the dimension differently. His check scales each group using the other group's item parameters and compares with joint scaling. [Lewis and Tausanovitch](https://www.vanderbilt.edu/csdi/miller-stokes/05_MillerStokes_LewisTausanovitch.pdf) [digest]
- Differential item functioning is the formal name for this. A 2022 paper estimates differences in item mappings with Bayesian non-parametrics. [Shiraito et al.](https://ar5iv.arxiv.org/html/2205.05934) [digest]
- "Anchors Away" uses bridge decisions to drop assumptions on how actors move. [Political Analysis](https://www.cambridge.org/core/journals/political-analysis/article/anchors-away-a-new-approach-for-estimating-ideal-points-comparable-across-time-and-chambers/D15AF9B8C40A976B816A364E6528C871) [digest]

**Public data, no cost.**
- [compdemocracy/openData](https://github.com/compdemocracy/openData): CC BY 4.0 with an attribution template. 20 conversation folders, README describes 8; some are demos or tests. [code/docs]
- `valency-anndata` loads Polis data from URLs, IDs, Hugging Face slugs or local CSVs, with reference sets including vTaiwan, Klimarat, Chile protest, American Assembly and Aufstehen. [docs](https://patcon.github.io/valency-anndata/api/datasets) [code/docs]
- Halpern et al. used 13 real Polis deliberations of about 87 to 1,000 voters and 31 to 1,719 comments. [arXiv](https://arxiv.org/html/2211.15608v4) [peer-reviewed]
- PrefLib also hosts Polis datasets, with a median 15.5% observation rate (prior notes on Blair).

### Inferences
- Jessee's check is directly usable for Arena's two-population problem: fit item parameters on thinkers' propositions and on participants separately, then compare placements. A gap between them is a measured `sense_fork`. This is a concrete reason to treat `sense_fork` statements as non-anchors.
- For anchors, prefer many short anchor statements across rounds and conversations, each tested for item drift. Remove anchors whose parameters shift between clusters.
- Identity across conversations should be opt-in and pseudonymous, which fits the rule on private individuals. Without opt-in, anchors still allow population-level comparison but not person-level.
- A first offline benchmark: hold out 10% of observed votes on 20 public conversations and compare PCA plus k-means, Bayesian 2D and 5D IRT, latent block with MNAR, and grade of membership. Score held-out log loss, cluster stability under bootstrap, and calibration of uncertainty. This fits the "no paid APIs" rule. Publishing requires Benjamin's approval.

### Gaps
- Multidimensional IRT for Polis data: no published application found. Bayesian uncertainty on Polis placement: none found. Signed bipartite SBM fitted directly to sparse approve-disapprove data: none found. Factor rotation on Polis: none found.
- Which openData exports have full votes files was not checked file by file.
- Most table entries were seen only as digests; open them before quoting.

## 3. Statement routing, active learning and proportional representation of views

### Takeaway
Theory here is stronger than for clustering. Halpern et al. show adaptivity is required for fair representation at realistic vote counts, and generative social choice gives representation guarantees that do not rely on fixed clusters. Both evaluate against imputed or simulated answers more than live humans. Arena should adopt proportional slates for describing a cluster's internal range, but they do not replace bridging.

### Cited Findings
**Adaptive selection under incomplete votes.**
- Non-adaptive querying is impractical: guaranteeing JR needs Ω(m²) queries even for k = 2. [Halpern et al.](https://arxiv.org/html/2211.15608v4) [peer-reviewed]
- Adaptive algorithms achieve approximate Extended Justified Representation. Exact queries need O(m k² log k); noisy queries need O(m k⁶ log k log m) at α = 1. [same]
- On 13 Polis datasets, ucb-α-PAV reached α̂ ≥ 1 in 83% of cases and α̂ ≥ 0.75 in all; plain approval voting fell below 1 in 38%. [same]
- Limits: missing votes were imputed with matrix factorization, comments were assumed known in advance, and late comments lose guarantees unless enough people vote on them. Near-universal comments were removed first. [same]

**Generative social choice.**
- BJR: agents are matched evenly to k statements, and no coalition of n/k or more can all rate some statement above a threshold while all being matched below it. [Fish et al.](https://arxiv.org/html/2309.01291v3) [peer-reviewed]
- Pilot: 100 US residents on abortion, 5-statement slate; a fresh 100 rated. 84 rated their assigned statement "excellently" or "exceptionally". Mean 5.31 vs 5.15 for a GPT baseline on a 7-point scale. [same]
- Three caveats the headline hides. The matching used the same ratings it reports. Generated statements were never shown to their generators. BJR could not be conclusively verified. [same]
- The rating item was "how well does this summary capture your viewpoint?". [same]
- Clustering stays inside: balanced k-means over LLM features picks groups for generation. [same]
- Predicted ratings ordered 86.7% of held-out pairs correctly. [same]
- PROSE adds cost-aware cBJR and takes only raw text and a length budget. [Boehmer, Fish, Procaccia](https://arxiv.org/html/2505.22939v1) [peer-reviewed]
- PROSE violation shares: 0.05 to 0.19, against 0.17 to 0.37 for clustering baselines and up to 0.68 for others. But evaluation is by chain-of-thought predicted utilities, on four instances; the only Polis one is Bowling Green with 41 agents. [same]
- PROSE's limits: GPT-4o queries give no guarantees, and it struggles to find coherent subgroups. [same]

**Related adaptive work.**
- Crowdsourced Adaptive Surveys turn open-ended text into items and use a bandit to prioritize them, finding topics standard surveys miss. [Velez](https://arxiv.org/abs/2401.12986) [abstract]
- General theory: adaptive submodularity gives near-optimal greedy pool-based active learning. [Golovin and Krause](https://www.learningtheory.org/colt2010/papers/111golovin.pdf) [digest]

### Inferences
- GSC gives Arena a tool for a problem the prior notes left open: a cluster is not one voice. Describing a cluster with a BJR-style slate means every n/k faction has a statement it can sign. Asking the described side to sign "at least one of these and most of the slate" reduces faction capture.
- BJR and bridging answer different questions. BJR asks "is everyone represented by something?"; bridging asks "what survives across difference?". Keep both: slates for describing, bridging for what travels.
- GSC's "captures your viewpoint" item is closer to self-description than to outsider-accuracy, but it is the best tested wording. Reuse it, with a separate item for truth.
- Routing for Arena should combine three aims: Bayesian information gain on placement, Halpern-style representation, and held-out anchors. All exposures must be logged, or later propensity corrections are impossible.
- A mixed policy preserves some random exposure. Without it, adaptive routing recreates MNAR.

### Gaps
- Remesh's selection method: no primary source found. Fishkin's work on this: none found. Flanigan's sortition papers: search returned none, so nothing here is sourced; only Procaccia's Panelot mention was seen on [his site](https://procaccia.info/) [digest].
- No Bayesian experimental design for live Polis reactions was found. A Polis-specific search returned generic active learning only.
- GSC has no live test with the people who generated statements rating them.

## 4. Prior art for calibrated intergroup description scoring: does the candidate survive?

### Takeaway
**Verdict: the candidate survives, but narrower, and it should be renamed.** Its core design (in-group judges compare genuine in-group answers with outsiders' imitations) is old: Collins and Evans's Imitation Game, and the Ideological Turing Test's relative passing rule, already do it. What survives as apparently new is a live, persistent, directional cluster-pair reputation score, using quote-anchored real statements and deliberately engineered decoys. It also measures reciprocal understanding, which is one component of meta-consensus, not meta-consensus itself.

### Cited Findings
**Meta-consensus measurement.**
- Meta-consensus has three forms: normative (legitimate values), epistemic (credible beliefs) and preference (acceptable options). [Niemeyer and Dryzek 2007](https://researchportalplus.anu.edu.au/en/publications/the-ends-of-deliberation-meta-consensus-and-inter-subjective-rati/) [abstract]; restated in [Automatic generation of DRI statements](https://arxiv.org/pdf/2511.11655) [preprint]
- In Dryzek and Niemeyer, it is *normative* meta-consensus that "implies reciprocal understanding and recognition of the legitimacy of the values". [AJPS 2006](https://openresearch-repository.anu.edu.au/server/api/core/bitstreams/13db0edd-bc9e-45ab-ae40-9194d14bd78a/content) [peer-reviewed]
- The Deliberative Reason Index is the main operational measure, applied to 19 forums. [Niemeyer et al. APSR 2023](https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/6558F69855ADA8B15BF2EC2E5D403E71/S0003055423000023a.pdf/how_deliberation_happens_enabling_deliberative_reason.pdf) [digest; PDF host unreachable]
- A later analysis covers 22 minipublics. [Veri et al.](https://resolve.cambridge.org/core/services/aop-cambridge-core/content/view/F19135A60561D8925735B44C236E673A/S1755773925000050a.pdf/deliberative-reason-and-the-effect-of-minipublic-configurations.pdf) [digest]
- DRI method: participants rate typically 20 to 40 considerations and rank a smaller set of preferences, before and after. For each pair, Spearman correlations are computed on each set. DRI = 1 − (2/n_p) Σ|ρ(C_i,C_j) − ρ(P_i,P_j)|, ranging −1 to 1. [Flechtner 2026](https://arxiv.org/pdf/2608.10186) [preprint; restatement, original formula not read]
- DRI separates consensus without meta-consensus from meta-consensus without consensus. [Flechtner 2026](https://arxiv.org/pdf/2608.10186)
- Instruments are labour-heavy and unstandardized, and an LLM pipeline has been built to generate statements. [Automatic generation of DRI statements](https://arxiv.org/pdf/2511.11655) [preprint]
- LLM groups match human process quality but show only small, topic-dependent DRI gains. [Flechtner 2026](https://arxiv.org/pdf/2608.10186)
- Nothing found for Himmelroos on this; no meta-consensus scale apart from DRI was found. Most DRI sources are from one research group.

**Imitation Game: the strongest prior art.**
- A judge from a group questions two hidden respondents: a genuine member and a pretender from another group. The pretender "passes" if identified at about chance. [Collins and Evans framing](https://arxiv.org/pdf/1611.04423) [digest]
- It has been applied to gender, national identity, religiosity and sexuality; funded by a €2.26M ERC grant; and a consumer app, Masquerade, runs games. [Frontiers 2021](https://www.frontiersin.org/articles/10.3389/fpsyg.2021.730985/pdf), [Cardiff](https://www.cardiff.ac.uk/news/view/masquerade-27816) [digest; Cardiff page blocked]
- Collins and Evans say it is not a test for individual cases but a group-level measure. [same Frontiers paper](https://www.frontiersin.org/articles/10.3389/fpsyg.2021.730985/pdf) [digest]
- Quantitative and qualitative sides combine in four ways, with players acting as "proxy researchers". [Collins et al. 2017](https://pure.york.ac.uk/portal/en/publications/the-imitation-game-and-the-nature-of-mixed-methods/) [abstract]
- A signal-detection version: 16 actors, 221 judges, 7,072 trials, on blind and sighted people. Sensitivity d′ was 0.937 for blind judges vs 0.441 for sighted in the identify condition, modeled with probit mixed models. [PMC8586539](https://pmc.ncbi.nlm.nih.gov/articles/PMC8586539) [peer-reviewed]

**Ideological Turing Test.**
- Writers: 600, 100 per side per topic. Raters: 1,200, blind to side and author. Each argument received 20 ratings. Raters rated agreement with a reason, not validity. [Brand et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12519043/) [peer-reviewed]
- Absolute pass is agree or stronger. Relative pass uses the in-group's own mean rating, rounded, as threshold. This is calibration against real in-group arguments. [same]
- Pass rates, absolute / relative: vegans 0.32 / 0.71; non-vegans 0.71 / 0.71; anti-vaccine 0.54 / 0.54; pro-vaccine 0.49 / 0.54; Leavers 0.46 / 0.64; Remainers 0.44 / 0.66. No decoys. [same]
- Researching a topic or discussing it with opponents did not predict relative passing, with vaccination discussion ambiguous. [same]
- Passing predicted lower ratings of opponents as immoral or ignorant, more strongly on veganism than Brexit. [same]
- The paper's sample descriptions are inconsistent: the abstract says 200 per topic, the methods 600 writers and 1,200 raters. [same]
- Gamba et al. use ITT as a gamified intervention, reporting +0.91 SD writing and +0.51 SD debate shifts. [arXiv 2512.12187](https://arxiv.org/abs/2512.12187) [digest] Durability reports conflict between summaries; unresolved.

**Target-based accuracy and felt understanding.**
- Accuracy benchmarked on the target's own report exists in interracial interaction research. [Holoien et al.](https://uwaterloo.ca/diversity-intergroup-relations-lab/sites/default/files/uploads/files/holoienbergsiekersheltonalegre2014.pdf) [digest]
- Felt understanding is the belief that an outgroup understands one's perspective; it is a perception, not an accuracy score. [Livingstone](https://ore.exeter.ac.uk/repository/handle/10871/39454) [digest]; [multi-experiment test](https://ore.exeter.ac.uk/repository/handle/10871/122730) [digest]

**Perspective-taking accuracy.**
- Across 25 experiments, instructed perspective taking decreased accuracy overall, while asking the person directly raised it. [Eyal, Steffel and Epley 2018](https://cris.iucc.ac.il/en/publications/perspective-mistaking-accurately-understanding-the-mind-of-anothe/) [digest]
- Stereotypes of liberals and conservatives got direction right but exaggerated magnitude (n = 2,212). [Graham, Nosek and Haidt](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3520939/) [digest]

**Text-based proxies.**
- Conversational receptiveness detects acknowledgment, hedges and subjectivity with ML, and predicts less escalation and fewer personal attacks on Wikipedia. It measures manner, not description accuracy. [Yeomans et al. 2020](https://www.hks.harvard.edu/publications/conversational-receptiveness-improving-engagement-opposing-views) [digest]

**Rapoport's rules and steelmanning in systems.**
- Rule one asks for restatement good enough that the target says "Thanks, I wish I'd thought of putting it that way". [The Mind Collection](https://themindcollection.com/rapoports-rules/) [informal digest]
- No app or forum enforcing restate-and-confirm was found. Nothing was found for a "Reciprocity" tool or Kialo steelman assessment.

**LLMs.**
- Anthropic sets passing the ITT as a goal, but grades even-handedness with AI models on 1,350 prompt pairs, not with people from each side. [Anthropic](https://www.anthropic.com/news/political-even-handedness) [digest]
- LLM judges show perspective-dependent bias. [Farzi et al.](https://www.cs.unh.edu/~dietz/papers/farzi2026sycophancy.pdf) [digest]
- Chain-of-thought can degrade LLM estimates of group judgments. [ACL Findings 2026](https://aclanthology.org/2026.findings-acl.2124.pdf) [digest]
- No experiment was found with LLM steelmen rated by people who hold the view.

**Live scoring check.** Searches for a live system scoring a description by the described group against decoys and real statements found none. Masquerade is the nearest live analogue: a game, not a persistent public reputation.

### Inferences
**What survives and what does not:**

| Component | Status | Nearest prior art |
|---|---|---|
| Described group judges outsiders' text, blind | Not novel | ITT, Imitation Game |
| Mixed with genuine in-group material | Not novel | Imitation Game; Brand relative criterion |
| Group-level, not individual, reading | Not novel | Collins and Evans |
| Signal-detection statistics | Not novel | PMC8586539 |
| Engineered decoys: distorted versions of real statements | Not found | Pretenders are a human analogue |
| Real comparators are quote-anchored statements of public figures | Not found | Thinker-to-cluster link appears new |
| Persistent directional cluster-pair score feeding reputation | Not found | None |
| Clusters derived from a different population's public works | Not found | None |

- So the report's candidate 3 should read: "decoy-calibrated fidelity using quote-anchored comparators, as a persistent cluster-pair score". The bare "in-group comparators" idea is prior art. Candidate 2 survives. Credit Collins and Evans and Brand et al. in any public description.
- **Use signal detection, not a threshold.** Imitation Game practice gives Arena its statistic. For each cluster pair, fit d′ (can described raters tell a real statement from an outsider's description?) and response bias separately. Target d′ near 0 for real vs description, and high d′ for real vs decoy. The second number proves raters are paying attention. A description passing with low decoy discrimination is uninformative. This replaces the fixed 0.70 in OD-14.
- **Brand's data warn against a simple relative rule.** The veganism row more than doubles from 0.32 to 0.71 by changing criterion, and the paper notes vegans 6.00 and non-vegans 4.49 as baselines. As I read it, a described group with ambivalent feelings about its own arguments sets an easy bar. Arena's bar would vary with cluster cohesion unless modeled. Fit it with rater and statement random effects.
- **Agreement is not the right item.** Brand raters judged agreement. Arena needs "does this say what we think?", separately from "is it true?". The prior notes said this; Brand confirms the distinction is untested in ITT.
- **Decoys carry a research ethics cost.** Showing people distorted statements of their own view, even labelled afterward, needs debriefing. A distorted statement must never be attached to a named landmark or shown publicly, given the dispute and privacy rules.
- **Imitation Game pretenders know they pretend.** Arena's writers want to describe sincerely, and can use LLM help. Agents can write but never ratify, which the Farzi digest supports.
- **Naming.** Call it a "reciprocal understanding score" or "signing score". Meta-consensus proper also includes recognizing legitimacy. A group can be accurately described and still judged illegitimate. Under Dryzek and Niemeyer's definition, reciprocal understanding is implied by normative meta-consensus; it is not the same thing.
- **Relation to DRI.** DRI measures the consistency between reasons and preferences among pairs. It cannot be computed from sparse votes, since it needs dense ratings on 20 to 40 items per person. It also says nothing about description. It would be a good external check: run a DRI instrument on a small cross-cluster pilot, and test if the signing score correlates with DRI gain. This is untested.
- **Perspective-getting.** Eyal et al. suggest writers should be given real access to the other side. Do not score only cold writing. Brand's null on self-reported discussion is a contrary signal, so test this.

### Gaps
- The Imitation Game's Step 1 to 4 details and sample scale could not be read (Cardiff PDFs returned 403). Scale figures are therefore not reported. This is the most important single paper to read before any novelty claim: [Collins et al. 2017](https://orca.cardiff.ac.uk/id/eprint/80618/).
- APSR 2023's original DRI equation and results were not read; the host failed. Niemeyer and Veri 2022 was not read.
- Cappella, Price and Nir's argument repertoire measure: search found nothing, but from memory it counts reasons people can give for opposing views, so it should be checked. Ames's work could not be sourced beyond a citation.
- Decoys: I found no literature on distorted-statement detection by in-groups in a scoring role. Absence from a handful of searches is weak evidence. Survey-methods work on attention checks and intergroup "stereotype accuracy" should be searched before publishing a novelty claim.
- Kialo and "Reciprocity": no result. Benjamin's reference may be to something else.

## 5. Perception gap as a metric, and whether correcting misperceptions reduces hostility

### Takeaway
Yes, a measure of how well Cluster A predicts Cluster B's fingerprint is a workable direct score, and it is the natural numeric partner to the signing score. But it measures accuracy about opinions, not understanding of reasons. Evidence that closing the gap reduces hostility is contested, so Arena should treat the gap as a measurement target, not as a claimed cause of reduced hostility.

### Cited Findings
**How it is measured.**
- More in Common surveyed 2,100 Americans via YouGov. For each of seven items, a person's gap is the difference between their estimate of how many partisans hold a view and the actual share. Each person's gap is averaged across items, then across party. [Perception Gap report](https://www.moreincommon.com/media/0fmblxb3/the-perception-gap.pdf) [primary report read]
- Headline: partisans think 55% of opponents hold extreme views; about 30% do. Average gaps shown: 19 for estimating Republicans and 27 for estimating Democrats in the report's two tables (table labels read from extracted text, verify). [same]
- The report warns that each party answered different questions, so "the choice of questions will influence" results, and the gap should not be read as an objective between-party measure. [same]
- News consumers "most of the time" are almost three times as inaccurate as those who consume "only now and then"; the gap is wider at the wings. Correlational. [same]

**Correction experiments.**
| Study | N | Result | Evidence |
|---|---|---|---|
| Lees and Cikara 2020, as described in [Ruggeri et al.](https://www.nature.com/articles/s41562-021-01092-x) | US samples | Disclosing inaccuracy cut attributions of obstructionism | [digest; original not read] |
| [Ruggeri et al. 2021](https://www.nature.com/articles/s41562-021-01092-x) | 10,207; 26 and 10 countries | Modest cut in negative motive attribution; replicates | [digest; full text blocked] |
| [Mernyk et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9169855) | 4 studies | Support for violence down 34%, willingness down 44%, lasting 1 month | [digest] |
| [Voelkel et al. 2024](https://www.hks.harvard.edu/publications/megastudy-testing-25-treatments-reduce-antidemocratic-attitudes-and-partisan-animosity) | 32,059 | Correcting misperceptions among strongest for anti-democratic attitudes; other treatments strongest for animosity | [digest] |
| [Landry et al.](https://labs.psych.ucsb.edu/schooler/jonathan/sites/labs.psych.ucsb.edu.schooler.jonathan/files/pubs/reducing_explicit_blatant_dehumanization_by_correcting_exaggerated_meta-perceptions.pdf) | 4,154 | Correcting meta-dehumanization cut dehumanization | [digest] |
| [Dias et al. 2024](https://pure.au.dk/portal/en/publications/correcting-misperceptions-of-partisan-opponents-is-not-effective-/) | 2,846 + panel 9,810 | No consistent effect; meta-analysis of 67 tests, 12 studies, weak; beliefs unstable, effects could fade in a month | [abstract] |
| [Druckman 2023](https://omicsdi.org/dataset/biostudies-literature/S-EPMC10500162) | not read | No effect when competing information or uncertainty is added | [digest] |
| [Markant et al. 2025](https://arxiv.org/html/2508.00233v1) | 483 | Showing every response beat mean-only; interval display weakest; no follow-up | [preprint] |
| [Dorison et al. 2019](https://www.hks.harvard.edu/publications/selective-exposure-partly-relies-faulty-affective-forecasts) | 2,455 | Correcting affective forecasts cut selective exposure 24 to 34% | [abstract] |

- State legislators (n = 534) also vastly overestimate voters' out-party hostility. [Druckman et al. summary](https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-c422t-ce32da6f3bf4ae157bba6d73ee39f8502fed9dc2cc5601525604fe4b37f808213) [digest]
- Markant cites Voelkel as finding reduced animosity without lower violence support, which seems at odds with the megastudy summary. It may refer to a different Voelkel paper. Unresolved. [Markant et al.](https://arxiv.org/html/2508.00233v1)

### Inferences
**Can it be a direct meta-consensus score?** As an accuracy metric, yes. As meta-consensus, no, for the reasons in Question 4. It is cheaper than the signing score and hard to game by flattery.

A proposed form, untested:
- Cluster A members predict the share of Cluster B that would endorse held-out statements.
- Score with a proper scoring rule (Brier), and report skill against a baseline: 1 − (Brier_A / Brier_baseline). The baseline is the overall population rate, so credit goes to knowing B specifically.
- Report signed error separately, so exaggeration shows as a bias and not just noise. Graham et al. suggest error is mostly magnitude.
- Keep prediction statements held out and rotated, or the published fingerprint turns the score into a memory test. Publishing the fingerprint teaches the answers. That is good for society and bad for the metric, and the metric should give way.
- Require minimum B sample sizes, since small clusters have noisy truth.
- Weight items with care. The report's proviso shows that item choice sets the gap. Use items sampled from a pre-registered pool, not chosen by outcome.

**Two scores, kept separate.**
- Prediction skill: "does A know what B thinks?" Tested against B's votes.
- Signing score: "can A say it in words B signs?" Tested against B's raters.
A disagreement between them is informative. High prediction with low signing suggests contempt or caricature with accurate numbers. Low prediction with high signing suggests flattery or vague language.

**Do not promise reduced hostility.** The honest summary: corrections shift beliefs, sometimes reduce anti-democratic support at about a month's horizon, and do not reliably reduce animosity. Dias's panel data suggest these beliefs are unstable, and Druckman suggests fragility under competing messages, which is the normal state of a live public platform. Voelkel's strongest treatments for animosity were sympathetic individuals and shared identity, not facts. Arena's stated success measure is meta-consensus, not convergence or warmth, so it can honestly report accuracy gains without claiming a hostility effect. If hostility claims matter, measure with a control group.

**Display.** Markant suggests showing the distribution of individual responses over means. Fit this to Arena's cluster pages, as a preliminary result.

### Gaps
- Ruggeri's effect sizes were not reached; Nature's page redirected to a login.
- No study found of a perception gap measured between ideological clusters finer than party, or used as a repeated public score.
- Perception Gap's table values were read from PDF-extracted text and need a visual check.
- No correction durability past about a month.

## 6. Tensor methods and cross-conversation models for sparse person by statement by time data

### Takeaway
Nothing found justifies tensor methods for Arena now. Polis data barely has a time mode at person level, because almost nobody returns. Shared anchors with dynamic IRT is the sensible route, and even that needs repeat participants Arena does not yet have.

### Cited Findings
- The only tensor ideal-point work found is NIPEN (AAAI 2018), a neural tensor model linking bill text and votes. It is static, with no drift over sessions. [NIPEN](https://arxiv.org/pdf/1904.11727) [digest]
- 89.1% of participants have one session; the median is 1.0 sessions per participant. [Gelauff 2026](https://arxiv.org/pdf/2608.28368) [preprint]
- Group-level dynamic IRT exists for aggregated survey data. [MODGIRT](https://core-cms.cambridgecore.org/core/services/aop-cambridge-core/content/view/3D875B3E0C42AE6749456F7EC665F2BF/S1047198724000251a.pdf/modgirt-multidimensional-dynamic-scaling-of-aggregate-survey-data.pdf) [digest]
- A Bayesian mixture captures voting blocs over time in longitudinal referendum data. [arXiv 2301.01677](https://arxiv.org/pdf/2301.01677) [digest]

### Inferences
- With almost no repeat people, a person-by-statement-by-time tensor is close to a set of disconnected slices. The third mode gives no leverage until people return.
- Group-level dynamics fit better: MODGIRT-style models track cluster means over time from repeated cross-sections linked by anchor statements. This suits Arena's frozen rounds, and it does not require identifying individuals, which suits the privacy rules.
- Arena's thinker data has a real time axis: dated public statements. A dynamic ideal point model over dated propositions could track thinkers' drift. Whether it is worthwhile at about 27 thinkers is doubtful.

### Gaps
- Only one tensor search ran before budget limits. Martin and Quinn's dynamic ideal points were suggested by search output but were not read. Temporal tensor factorization for opinion data: nothing found. Treat this as a thin check.
