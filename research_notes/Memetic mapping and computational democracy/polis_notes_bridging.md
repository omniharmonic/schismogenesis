# Polis clustering, Community Notes bridging, and attempts to combine them with each other and with content-based clustering (state of play, 1 Nov 2026)

Reading guide: "Cited Findings" are established by the linked source. Each is tagged [code/docs] (primary source read), [peer-reviewed], [preprint], or [digest] (seen only through a search summary; paper not opened). "Inferences" are my own reasoning. Web search ran out before the end of this work, so the novelty statements below mean "not found in the searches run", not "does not exist". Searches run and those skipped are listed in the Gaps of Question 6.

This goes beyond `docs/research/B2-computational-democracy.md` and `B3-mechanism-design.md` in three main ways:
- It reads the scorer and Polis source that those briefs could not reach.
- It adds post-B2 attack and theory papers.
- It adds the political-science prior art on votes plus text, which neither brief covers.

## 1. Polis in detail: vote matrix, PCA, k-means, consensus, routing, missing data, known flaws

### Takeaway
Polis is a two-stage pipeline: mean-impute, PCA to 2D, k-means of k-means, then score statements against that single partition. Its weakest link is now measured. Clustering depends on path and cannot be reproduced from exports, three quarters of conversations report just two groups, and group-informed consensus degrades badly at the observation rates Polis actually has.

### Cited Findings
**Pipeline, verified in code**
- Polis's math engine is now a Python port (`delphi/polismath`) that replaces the Clojure engine, and the repo is AGPL-3.0. Docs: [Polis README](https://raw.githubusercontent.com/compdemocracy/polis/edge/README.md) and [LICENSE](https://raw.githubusercontent.com/compdemocracy/polis/edge/LICENSE). [code/docs]
- Votes are held per participant and statement as agree / disagree / pass. Participants enter clustering only with at least min(7, number of comments) votes. [conversation.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/conversation/conversation.py) [code/docs]
- Missing votes are replaced with column means before PCA. The code comment admits the weakness: column mean "pulls participants toward center", assumes Gaussian data while votes are ternary, is "better than 0", and "future work" is needed. [pca.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/pca_kmeans_rep/pca.py) [code/docs]
- Projection uses only each person's observed coordinates, then multiplies by sqrt(comments / comments_seen) to push sparse voters outward. [pca.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/pca_kmeans_rep/pca.py) [code/docs]
- PCA is by power iteration warm-started from the previous cycle ([Gelauff 2026](https://arxiv.org/pdf/2608.28368)). [preprint]
- Clustering runs in two levels. Participants go into up to 100 base clusters, then base clusters into 2 to 5 groups, with k chosen by silhouette. [conversation.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/conversation/conversation.py) [code/docs]
- Maximum k is min(5, 2 + base_clusters // 12). [conversation.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/conversation/conversation.py) [code/docs]
- A k-smoother only switches k after a run of consecutive ticks at the new value. [group_k_smoother.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/pca_kmeans_rep/group_k_smoother.py) [code/docs]
- Representative statements use Laplace-smoothed rates, pa = (n_agree + 1) / (n_votes + 2), then a group-vs-other ratio and two-proportion z-tests with thresholds at 90 and 95% confidence. [repness.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/pca_kmeans_rep/repness.py) [code/docs]
- Group-informed consensus is the product over groups of (agrees + 1) / (votes + 2). [compdemocracy.org](https://compdemocracy.org/group-informed-consensus), formula restated in [Blair et al.](https://www.cs.toronto.edu/~nisarg/papers/bridging.pdf)
- The separate "consensus" lists use whole-conversation stats, not per-group stats: top 5 with pa > 0.5 and z > 1.2816. [repness.py](https://raw.githubusercontent.com/compdemocracy/polis/edge/delphi/polismath/pca_kmeans_rep/repness.py) [code/docs]

**Comment routing**
- Exact formula, from source, reported by [Gelauff 2026](https://arxiv.org/pdf/2608.28368) [preprint]:
  - p = (P+1)/(S+2) and a = (A+1)/(S+2)
  - importance = (1−p)(E+1)a
  - priority = [importance · (1 + 8·2^(−S/5))]²
  - Here E is the statement's extremity, its distance from the origin in the 2D projection.
  - Meta-statements are fixed at 7² = 49.
- The rule is asymmetric. At equal extremity and 10 votes, an all-agree statement outweighs an all-disagree one by 121 times; at 30 votes, 961 times. A few early passes can bury a statement for a long time. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Between March 2025 and July 2026 priority was uniformly distributed because of a bug, and it was also uniform before January 2018. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- The public docs list the factors (predictiveness, consensus, recency, pass rate) but no weights. [compdemocracy.org](https://compdemocracy.org/comment-routing/) [code/docs]
- PR notes say priorities now use group-based extremity rather than PCA-based values, in the order math, then UMAP, then extremity, then priorities. [PR #2110](https://github.com/compdemocracy/polis/pull/2110) [digest; merge state not confirmed]

**Measured flaws**
- 119 conversations with 100+ participants: median 332 voter IDs, 10,449 votes. Participants see less than half the statements. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Reported group counts (n=114): 2 groups 74.6%, 3 groups 17.5%, 4 groups 5.3%, 5 groups 2.6%. Recomputing on the final matrix without the warm path (n=112): 62.5%, 13.4%, 13.4%, 10.7%. The two agree in 70 of 112 cases; recomputation mostly finds more groups (33 up, 9 down). [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Because of warm-path clustering, exported clusters cannot be reproduced from the votes. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Convener choices are named as a third shaper of results: seed statements, moderation policy, and who is invited. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Grossi calls Polis's average-value imputation "crude" and arguably problematic from a democratic standpoint. [Grossi 2026](https://arxiv.org/pdf/2605.01525) [preprint]
- Blair et al. show group-aware consensus falls behind alternative metrics as data thin out, and turns negatively correlated with the true ranking at low observation rates under simulated Polis routing. Median observation rate across PrefLib Polis datasets is 15.5%, squarely in that range. Their explanation: all sensitivity is concentrated in one clustering step. [The Structure of Bridging](https://www.cs.toronto.edu/~nisarg/papers/bridging.pdf) [preprint or paper; venue not stated in the PDF]
- Polis's public docs state it uses only the opinion matrix and no NLP, and list K-Means, Leiden and hierarchical clustering plus PCA and UMAP. [compdemocracy.org/algorithms](https://compdemocracy.org/algorithms/) [code/docs]
- Delphi uses EVoC and UMAP for topics, with a KMeans fallback. [PR #3199](https://github.com/compdemocracy/polis/pull/3199) [digest]
- Polis-family reimplementations exist, for example Red Dwarf, a Python pipeline used by Agora and Voxit. [Gelauff 2026](https://arxiv.org/pdf/2608.28368)
- Small et al.'s paper is the primary method reference. [Small et al. 2021](https://Www.Gwern.net/doc/sociology/2021-small.pdf)

### Inferences
- Polis's "number of opinion groups" is largely a platform output. Its range is hard-coded and the result is path dependent. We should not treat a 2-group Polis result as evidence that a population has two camps.
- Arena should not copy warm-path clustering. Fixed snapshots with full recompute are needed because rewards and ratification depend on them (reinforces B3's "freeze per round").

### Gaps
- I did not find any study of coordinated manipulation of Polis clustering or consensus; the one search returned nothing direct.
- I read the math through the Python port. Whether current production behaviour matches every Clojure detail depends on PR merge states I did not check.
- The k-smoother buffer value was not read directly. B2 reports four ticks from Small et al.

## 2. Community Notes in detail: equation, thresholds, scorers, reputation, attacks, effects, 1D limits, AI writers

### Takeaway
The core equation is unchanged since 2022, but production is now a stack of guards around it, and since November 2025 a non-MF Gaussian aggregation over the viewpoint axis. Four 2025-26 results matter most: a second axis exists; helpful notes are heavily suppressed even with honest raters; about $30 can defeat the bare MF for low-scoring notes; AI writers now produce about half of what is shown.

### Cited Findings
**Core model** (B2 could not read these; now verified; code is Apache-2.0: [LICENSE](https://raw.githubusercontent.com/twitter/communitynotes/main/LICENSE))
- r̂_un = μ + i_u + i_n + f_u·f_n, with squared loss plus L2. λ_i = 0.15 on intercepts and λ_f = 0.03 on factors. Rating values: Yes 1.0, Somewhat 0.5, No 0.0. The note intercept i_n is the score. Retrained hourly. [ranking-notes.md](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/under-the-hood/ranking-notes.md) [code/docs]
- Default numFactors = 1, in [matrix_factorization.py](https://raw.githubusercontent.com/twitter/communitynotes/main/scoring/src/scoring/matrix_factorization/matrix_factorization.py). [code/docs]
- Thresholds in [mf_base_scorer.py](https://raw.githubusercontent.com/twitter/communitynotes/main/scoring/src/scoring/mf_base_scorer.py) [code/docs]:
  - crhThreshold 0.40, factorThreshold 0.5
  - crnhThresholdIntercept −0.05, note-factor multiplier −0.8, crnhThresholdNMIntercept −0.15, UCB −0.04
  - crhThresholdNoHighVol 0.37, crhThresholdNoCorrelated 0.37
  - lowDiligenceThreshold 0.263
- The Helpful bar: intercept ≥ 0.40 and |f_n| < 0.50, net-helpful minimums on both factor sides, and an intercept ≥ 0.37 when recomputed without the top 0.1% of high-volume raters and on the rater-independence subgraph. [ranking-notes.md](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/under-the-hood/ranking-notes.md)
- Uncertainty comes from pseudo-raters at extreme positions. Correlated raters are coalesced (Post Selection Similarity). Status locks after two weeks. CRH inertia gives 0.01 hysteresis. [ranking-notes.md](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/under-the-hood/ranking-notes.md)

**Multi-model stack** ([ranking-notes.md](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/under-the-hood/ranking-notes.md); scorer list in [run_scoring.py](https://raw.githubusercontent.com/twitter/communitynotes/main/scoring/src/scoring/run_scoring.py)) [code/docs]
- Scorers present: Core, CoreWithTopics, Expansion, ExpansionPlus, Group, MultiGroup, Topic, Reputation, and Gaussian variants.
- Modeling groups are "e.g. based on region, country or language". A group model scores only notes by members with at least 80% of ratings from the group, and only promotes notes whose Core or Expansion intercept is 0.3 to 0.4.
- So X's existing "groups" are geographic and linguistic, not viewpoint clusters. Viewpoint stays latent.
- Topic models: seed terms plus logistic regression. Intercept below 0.24 or |f| > 0.51 caps the status.
- Trial group model: note intercept λ 0.03×30, user intercept λ 0.03×5, factor λs lowered, and a "diamond" penalty λ 0.03×25 between intercept and factor size. Note: my document digest reversed the two intercept values; the code is authoritative.
- Population sampling (September 2025): if the intercept fitted on system-solicited ratings is below i_n − 0.15 and at most 0.3, Helpful is withheld.
- Gaussian model (pilot November 2025, extended July and August 2026): "a numerical approximation of the continuous geometric mean of helpfulness rates" over the factor axis, with 25 bins per side, kernel smoothing, a prior, and overweighted Not Helpful ratings. It avoids "sensitivity to low numbers of votes in certain buckets". [ranking-notes.md](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/under-the-hood/ranking-notes.md), code in [gaussian_scorer.py](https://raw.githubusercontent.com/twitter/communitynotes/main/scoring/src/scoring/gaussian_scorer.py)
- Other lanes: tag-consensus harassment model, note-diligence MF on sourcing tags, and a supervised confidence model that delays flip-prone notes up to 180 minutes.

**Contributor reputation** ([contributor-scores.md](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/under-the-hood/contributor-scores.md)) [code/docs]
- Rater helpfulness = (s − 10h) / t, where s is valid ratings matching final status and h counts Helpful ratings on extreme harassment-score notes. Must be at least 0.66.
- Valid ratings are those made within 48 hours and before the note's first status.
- Authors need a CRH-vs-CRNH ratio ≥ 0 (share CRH minus 5 × share CRNH) and mean note score ≥ 0.05.
- At least 10 ratings are needed.
- The ranking doc describes the harassment penalty as 5.0 × intercept while this doc gives 10; the two pages differ.

**Attacks and failure**
- [Selvam et al. 2026, "Gaming Consensus"](https://arxiv.org/html/2607.01824v1) (X and Stanford authors) [preprint]:
  - Phase 1: controlled accounts rate existing notes to take up diverse factor positions, chosen using a model predicting a note's factor and intercept from its text (Voyage embeddings plus MLP).
  - Phase 2: all rate the target Helpful.
  - Up to 10.7% of below-median notes cross 0.40 with fewer than 10 ratings, costing about $30.50.
  - Notes above median are far safer.
  - Attacks only bare MF, not production guards. Population sampling is their key mitigation.
  - A Not Helpful vote can raise an intercept in some geometries.
- [Truong et al. 2025](https://arxiv.org/html/2511.02615), on simulated data through X's real code [preprint]:
  - More than 40% of genuinely helpful notes are suppressed with honest raters only, and above 80% when rater friendliness varies widely.
  - About 12% indiscriminate bad raters breaks the system.
  - Coordinated raters at about 20% fully suppress a targeted group's helpful notes.
  - With polarization or in-group bias, critical shares fall to 5 to 20%.
  - Root cause: the helpfulness filter stops working once bad raters shift consensus, and bias is assumed 1D.
- [QS-MF, Goyal, Arora and Goel 2026](https://arxiv.org/html/2604.11224) [preprint]:
  - Model: r = μ + α_i + ρ_i β_j + γ_i δ_j, with ρ_i ≥ 0 regularized to 1, so raters differ in how sensitive they are to quality.
  - 2.6% lower out-of-sample MSE.
  - Attack protection 8.2 to 38.8%.
  - ρ̂ separates attackers at AUC 0.95 to 0.975.
  - Identification needs ρ_i ≥ 0 and penalties.

**Limits of the single factor**
- [Andreou & Sirivianos 2026](https://arxiv.org/html/2609.21496) [preprint]:
  - Held-out RMSE on 212.9M ratings: 0.3771 intercept-only, 0.3085 rank 1, 0.2899 rank 2, 0.2892 rank 3.
  - A permutation null shows no gain, and a leave-two-topics-out test shows rater positions predict held-out topics.
  - Notes that barely split axis 1 publish at 71.5% near the second-axis origin and 11.7% far from it.
  - The "institutional trust" label is the authors' reading, and they say the transferring dimension also correlates with axis 1.
- [Bouchaud & Ramaciotti](https://arxiv.org/html/2506.15168v2) [preprint]:
  - The latent axis tracks each country's main divide, and notes that activate it stay unresolved regardless of accuracy.
  - US 2024 election notes reached Helpful at 6.9% vs 14.7% in the same period.
  - Scams reach about 39%.
  - They call this a design choice set by the regularization and the diversity threshold.
- [Social Protocols](https://social-protocols.org/understanding-community-notes/) explains the intercept is not average approval: it is what a politically balanced community would give, and depends on the additive form being right.
- The original paper chose 1D "to avoid overfitting on our small dataset", and contrasted continuous bridging with "the additional assumptions that clustering involves". It deferred manipulation analysis. [Wojcik et al.](https://arxiv.org/pdf/2210.15723) [preprint; publication venue not checked]

**Effects research**
- Drolsbach and Pröllochs (full author list not checked): reposts fall about 36% in the first hour, but only about 15% overall, because notes come late. [Nature Communications 2026](https://www.nature.com/articles/s41467-026-72597-0) [peer-reviewed; digest]
- Slaughter et al.: reductions of 46.1% reposts and 44.1% likes after attachment, but 11.6% over a post's lifespan. [arXiv 2502.13322](https://arxiv.org/pdf/2502.13322) [digest; authorship of exact numbers not confirmed]
- Chuai et al. findings conflict across their own studies (61% reduction vs no effect), which reviewers attribute to timing. [review](https://arxiv.org/html/2510.09585v2) [digest]
- Allen, Martel and Rand: Birdwatch users flag counterpartisans 2 to 3 times more. Preliminary: Democrats rated 83% of copartisan notes helpful vs 43% of Republican-written. [thread](https://threadreaderapp.com/thread/1511409262039220224)
- A 2026 preprint reports copartisan rating persists. [arXiv 2601.22201](https://arxiv.org/html/2601.22201v1) [digest]
- A PNAS commentary surveys strengths and limits. [PNAS 2025](https://www.pnas.org/doi/10.1073/pnas.2524004122) [digest]

**AI writers**
- [Miller et al. 2026](https://arxiv.org/html/2609.40067v1), X authors [preprint]:
  - Earn-in requires 50 notes passing URL, harassment and claim-opinion checks.
  - Of 65 clients starting, 32 published and 19 remain active.
  - The Community Writer yields 41% of proposed notes, 52% of Helpful notes and 55% of views, while using 22% of ratings.
  - 54% of Needs More Ratings notes have fewer than 10 ratings.
  - Humans remain final raters.
- Indicator reported eight AI contributors wrote 50.3% of visible notes in early May 2026. [Indicator](https://indicator.media/p/8-ai-bots-now-write-50-of-x-s-community-notes) [digest]
- Collaborative notes let top writers request Grok drafts. [TechBriefly](https://techbriefly.com/2026/02/06/x-tests-collaborative-ai-notes-for-community-notes-feature/) [digest]
- Li et al. proposed writers trained on community feedback, with humans as deciders. [arXiv 2506.24118](https://arxiv.org/abs/2506.24118) [preprint]

### Inferences
- The intercept is not identified by data alone. Replacing f_u with f_u + c and i_n with i_n − c·f_n leaves every prediction unchanged. Only regularization and factor centring fix it, so the score depends on an implied reference population. The Social Protocols "balanced community" reading is the same point stated informally. For Arena this makes "who counts equally" an explicit choice rather than an accident.
- X's direction of travel (Gaussian scorer, net-helpful on both sides, population sampling) is away from pure MF and towards empirical agreement across positions on the axis, close to a soft Polis group product. That convergence is the strongest evidence that the Polis and Community Notes families are one family.
- Fidelity scoring by a rule like the 0.66 rater filter would reward conformity inside a cluster. Truong's root cause applies directly.

### Gaps
- Meta and TikTok internal thresholds and outcomes (see Question 5).
- Whether Gaussian scoring has been independently evaluated. I found no independent evaluation.
- Peer-review status of most 2025-26 attack papers: all are preprints.

## 3. Bridging-based ranking and the plural-funding lineage

### Takeaway
Bridging now has formal theory. Blair et al. show that metrics relying on one fixed partition are structurally weak, and that averaging over the partitions induced by every statement is more robust. This is the most important new result for Benjamin's idea. Field evidence for bridging ranking stays modest, and controversy suppression remains the top risk.

### Cited Findings
- [The Structure of Bridging](https://www.cs.toronto.edu/~nisarg/papers/bridging.pdf) (Blair, de Raaij, Procaccia, Rubin-Toles, Shah, Si, Wang):
  - Mean split bridging functions are characterized by additivity, anonymity and homogeneity.
  - Each statement y induces a split, and a split evaluator scores x on approvals among y-approvers and y-disapprovers.
  - Polis's product is a connectivity view. Remesh's minimum is a proportionality view. b_Polis prefers unequal splits like (3/7, 1) over (0.6, 0.6).
  - Pairwise disagreement: B_PD(x) is the sum of Hamming disagreement between pairs who approve x, and equals w_x² · Δ_d among approvers. p-mean bridging is the proportional family.
  - Consistent estimators exist under partial votes, with participants needed only logarithmic in comments.
  - The missingness assumption is per-comment random (q_x), and their real Polis case is labelled descriptive because missingness there is endogenous.
  - Discussion: the metric is "deliberately agnostic to semantic content", collapses ideological, salience and strategic disagreement into one signal, and suggests weighting splits by comment substantiality, via "human moderation or LLM support", as future work.
- Remesh groups are typically pre-specified, with score = minimum approval across groups. [Blair et al.](https://www.cs.toronto.edu/~nisarg/papers/bridging.pdf)
- [Hafid, Berriche and Cointet 2026](https://arxiv.org/pdf/2602.15439): consensus-seeking selection can flatten conflict and erase minority voices. No single strategy dominates across democratic criteria, and their social-choice rule gave the best proportional-representation and diversity trade-off. [preprint]
- Ovadya and Thorburn's framing and risks; Prosocial Ranking Challenge (−0.027 SD overall; upranking bridging alone not significant); Milli et al. on suppression of controversial topics: details and links in B2 and B3. [Ovadya & Thorburn](https://arxiv.org/pdf/2301.09976), [Stray et al.](https://arxiv.org/html/2603.19626), [Milli et al.](https://neurips.cc/virtual/2024/99058)
- COCM takes any group structure with soft weights w_{i,g}. Gitcoin used projects as groups because it lacked an independent social map, and its best-documented harm is penalizing tight-knit communities. [Miller, Kanich, Weyl 2025](https://arxiv.org/html/2509.18343v1); see B3.
- Plurality (CC0) is the umbrella framing. [plurality.net](https://plurality.net/)
- vTaiwan is an established Polis deployment that stalled after losing binding link; see B2 and [Noveck](https://thelivinglib.org/?p=57365).

### Inferences
- Community Notes' intercept, Polis's product, Remesh's min, COCM's pair sum, and Blair's PD are all answers to one question: how much approval survives across a chosen structure of difference? They differ in what structure they use (latent axis, one partition, every statement's split, group pairs) and in the aggregator (additive residual, product, min, pair sum).
- Blair's frame gives Arena a route that avoids the single-partition problem: use many splits, not the nine schools alone. See Question 6, Design C.

### Gaps
- No field test of COCM with worldview clusters as groups was found. B3 flagged this; still open.
- Publication status of "The Structure of Bridging" is not shown in the PDF.

## 4. Related matrix methods, and which handle sparse data where silence is not disagreement

### Takeaway
All the models that fit only observed cells avoid treating silence as disagreement, but they still assume silence is uninformative. Only explicit missingness models address the fact that silence depends on position. Arena's own code currently does something closer to imputation.

### Cited Findings
- **NOMINATE and Bayesian IRT.** Clinton, Jackman and Rivers give a Bayesian spatial model for roll calls, and Bayesian IRT is more easily adapted to additional data structures than NOMINATE. [CJR 2004](https://cdn.vanderbilt.edu/vu-my/wp-content/uploads/sites/349/2011/10/14093745/CJR_APSR2004.pdf), [Clinton & Jackman 2009](https://cdn.vanderbilt.edu/vu-my/wp-content/uploads/sites/349/2011/10/14093745/CJ_LSQ2009.pdf) [peer-reviewed; digest]
- Jackman links roll-call analysis, IRT and factor analysis. [Jackman 2001](https://www.cs.princeton.edu/courses/archive/fall09/cos597A/papers/Jackman2001.pdf) [digest]
- **Informative abstention.** Standard estimators typically treat missing votes as ignorable. Rosas and Shomer (2008) model abstention and voting together; Rosas, Shomer and Haptonstahl (AJPS 2015) treat non-response as informative and let actors abstain at different rates. [Rosas et al. 2009](https://macmillan.yale.edu/sites/default/files/files/resources/papers/rosas_etal_2009.pdf), [Hansford appendix](https://sites.ucmerced.edu/files/hansford/files/estimating_ideal_points_of_organized_interests_online_appendix.pdf) [digest]
- Hansford's supreme-court amicus work is close to Arena's setting: actors choose what to address. [same appendix](https://sites.ucmerced.edu/files/hansford/files/estimating_ideal_points_of_organized_interests_online_appendix.pdf) [digest]
- **Recommender MNAR.** Schnabel et al. use propensity weighting for selection bias. [arXiv 1602.05352](https://arxiv.org/pdf/1602.05352.pdf) [digest]
- ExpoMF models exposure as a latent variable, though critics say it handles positive-unlabeled data rather than MNAR in full. [arXiv 1510.07025](https://arxiv.org/pdf/1510.07025.pdf) [digest]
- The deconfounded recommender takes a causal view. [arXiv 1808.06581](https://arxiv.org/pdf/1808.06581.pdf) [digest]
- MNAR-k-means exists as a clustering variant. [arXiv 2606.31253](https://arxiv.org/pdf/2606.31253) [digest; not opened]
- **Cultural consensus theory.** Mixture CCT lets subgroups each hold their own consensus answers, and estimates subgroups, respondent competence, response bias and item difficulty with no external answer key. [Anders, Oravecz & Batchelder 2014](https://sites.socsci.uci.edu/~zoravecz/bayes/data/Articles/ANDORABAT14_MC-CRM.pdf), [CCTpack](https://cranhaven.r-universe.dev/CCTpack/doc/manual.html) [digest]
- **Block models and signed bipartite structure.** Signed voter-bill networks avoid the information loss of projecting to voter similarity. [arXiv 1811.10337](https://arxiv.org/pdf/1811.10337) [digest]
- Bipartite mixed-membership block models were used on Senate cosponsorship. [Imai page](https://imai.fas.harvard.edu/research/binetmix/) [digest]
- A distance-based bipartite alternative appears in [arXiv 2512.11610](https://arxiv.org/pdf/2512.11610v1). [digest]
- **Robust sparse voting.** Mehestan scales voters to a common range and then aggregates robustly, bounding any one voter's effect under sparsity. Tournesol adapts it. [Robust Sparse Voting](https://proceedings.mlr.press/v238/allouah24a/allouah24a.pdf), [Tournesol](https://ar5iv.labs.arxiv.org/html/2211.01179)
- **Arena's current code.** In [`structure.py`](/Users/benjaminlife/dev/schismogenesis/packages/arena_map/src/arena_map/structure.py) lines 70-75, `person_space` starts from a zero table, adds signed weights, damps, then subtracts each family's mean. ADR-035 says "Silence is missing data."

### Inferences
- Observed-cells-only fitting (CN's loss, Bayesian IRT, Blair's estimators) is the minimum bar. It avoids treating silence as disagreement, but it still assumes silence carries no information.
- Arena's silence is not ignorable. Thinkers discuss what their school cares about, so who addresses an idea is itself informative about position. Our best-fit literature is informative abstention, not plain matrix completion. A two-part model (does p address family k; if so, what stance) is a natural test.
- **A concrete finding in our code.** A person silent on a family gets 0 before centring, so −(family mean) afterwards, regardless of who they are. If a family is widely accepted, silence reads as mild dissent. Polis's approach differs: its column-mean imputation leaves a silent cell at 0 after centring, and its own comment warns that zero imputation "biases covariance estimates". So at family level our code is not treating silence as missing, despite the ADR's rule at holding level, and the module docstring only partly says this. Worth a small test: mask silent cells and compare school stability. Size of effect unknown; I did not run it, and no repo code was changed.
- CCT is the closest statistical match to "what would this cluster sign?" because it estimates a group's answer key and who is a reliable informant, without ground truth. I found no use of CCT in a bridging or reputation system.

### Gaps
- Tensor methods: the search was blocked by the session budget. I cannot report on tensor ideal-point work. Sourced material is missing, not absent from the literature.
- NOMINATE specifics, MDS of roll calls, and polarized-subgroup detection: not sourced beyond the items above. Several links above were seen only through search digests.
- The AJPS 2015 model equations were not read.

## 5. Who has joined opinion clustering to text or argument content

### Takeaway
Text and votes are widely combined at two ends: LLMs after Polis for reports, and rich joint models for legislators. Almost nothing joins them in the middle. Most deliberation tools use text to organize and summarize; the vote math stays text-blind, by design in Polis's case.

### Cited Findings
**Published joint models of votes and text (the essential prior art B2 and B3 lack)**
- [Lauderdale & Clark 2014, AJPS](https://www.tomclarkphd.com/files/LauderdaleClarkAJPS2014.pdf): LDA topic weights from opinion text tell which issue dimensions each Supreme Court vote concerns; preferences are then estimated per issue. Best fit came with 20 to 30 dimensions. Motivation: voting data alone blur issue differences through identification and labeling problems. [peer-reviewed; digest]
- [Kim, Londregan & Ratkovic 2018, Political Analysis](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C580ED354853271EFA759E289DC73C3A/S1047198718000074a.pdf/estimating_spatial_preferences_from_votes_and_text.pdf): sparse factor analysis treats votes and words as coming from one latent preference space. Shared speech can impute missing votes, recovering rank-and-file senators' positions when only leadership votes are present. [peer-reviewed; digest]
- [Kraft, Jain & Rush 2016](https://aclanthology.org/D16-1221.pdf): "ideal vectors" tied to word embeddings predict roll calls from bill text. [peer-reviewed; digest]
- [Gerrish & Blei](https://www.researchgate.net/publication/221345284_Predicting_Legislative_Roll_Calls_from_Text): predicting roll calls from text. [title only]
- [Vafa, Naidu & Blei 2020](https://arxiv.org/pdf/2005.04232): text-based ideal points from text alone, using Poisson factorization. Not joint; votes are only used for validation. This corrects the task's wording. [peer-reviewed]
- [ACL 2021 alignment paper](https://aclanthology.org/2021.acl-long.99.pdf): argues voting and speech have been treated separately. [digest]
- Wordfish: word-frequency scaling, no reference texts, works poorly on social media data. [Slapin & Proksch 2008](https://ideas.repec.org/a/wly/amposc/v52y2008i3p705-722.html) [digest]
- Validation against human raters: [Lowe & Benoit](https://resolve.cambridge.org/core/journals/political-analysis/article/validating-estimates-of-latent-traits-from-textual-data-using-human-judgment-as-a-benchmark/8E55A149753CE11CC3388A4408C55F48) [digest]

**Recommender analogues**
- Collaborative topic regression combines LDA with probabilistic MF. [CTR overview](https://www.emergentmind.com/topics/collaborative-topic-regression-ctr) [digest]
- CTR with social MF. [arXiv 1206.4684](https://arxiv.org/pdf/1206.4684) [digest]
- Collective MF shares factors across matrices. [cmfrec](https://libraries.io/pypi/cmfrec/0.3) [digest]

**Text meets preference matrices directly**
- [Blair, Procaccia & Tambe 2026, "Embeddings for Preferences, Not Semantics"](https://www.alphaxiv.org/abs/2605.08360) [NeurIPS 2026 poster per the listing]:
  - Off-the-shelf embeddings score near chance on hard triplets, where one option copies the anchor's words with flipped stance.
  - Decorrelated tuning raised accuracy from 48.3% to 80.0%.
  - A per-topic projection to about 20 dimensions, learned from 50 to 100 labeled triplets, reached 77.6% on natural data across 11 Polis, Remesh and GSC datasets.
  - Model: U(v,j) = −‖u_v − ψ_S(x_j)‖².
- Selvam et al. predict note factor and intercept from text (see Question 2). They built it as an attack, and it is still the closest published text-to-MF model I found. [Gaming Consensus](https://arxiv.org/html/2607.01824v1)
- Supernotes generates notes with an LLM, simulates a rater jury, and scores candidates with the CN algorithm. [arXiv 2411.06116](https://arxiv.org/html/2411.06116v1) [preprint]
- Kim & Lee: an LLM-based model with learned respondent embeddings for survey imputation. AUC 0.868 vs MF 0.856, unasked questions 0.701, weaker for minorities. [arXiv 2305.09620](https://arxiv.org/html/2305.09620) [preprint]
- Small et al. 2023: Claude topic modelling and summaries on Polis. Vote prediction was described as nearly calibrated, but they reject replacing participants. [arXiv 2306.11932](https://arxiv.org/html/2306.11932) [preprint]

**Deployed tools**
- Polis 2.0 / Delphi: EVoC, UMAP and topic narratives over text while vote math stays separate. [PR #3199](https://github.com/compdemocracy/polis/pull/3199) [digest]
- Talk to the City clusters arguments and supports traceability, but the pipeline was not confirmed. [AOI](https://ai.objectives.institute/blog/talk-to-the-city-an-open-source-ai-tool-to-scale-deliberation)
- Jigsaw Sensemaker: learn topics, categorize, summarize, with Polis format support. [Jigsaw guide](https://services.google.com/fh/files/blogs/final_jigsaw_sensemaking_howtoguide.pdf)
- Bridging Bot: LLM tool for Reddit moderators; design only, no outcome data found. [Plurality Institute](https://www.plurality.institute/blog-posts/exploring-opportunities-for-large-language-models-in-public-discourse)
- Tournesol: see Question 4.
- Guided Sensemaking: discourse graphs. It cites Polis only loosely, and has no bridging or MF. [arXiv 2606.02260](https://arxiv.org/html/2606.02260v1)
- Kialo, Decidim, Meta Community Forums: see B2. I found no vote-plus-text joint models.
- TikTok Footnotes is "inspired by the open-sourced system". [TechCrunch](https://techcrunch.com/2025/07/30/tiktoks-crowdsourced-fact-checks-called-footnotes-launch-in-the-u-s)
- Meta runs X's open-source algorithm in the US per a secondary source. [Botnet](https://botnet.com/resources/board-community-notes-what-changed) [digest]

### Inferences
- "Joint factorization of votes and text" as a general idea is not novel. Legislators had it by 2014 to 2018 and recommenders by about 2011. Arena must not describe it as new.
- What changes in Arena's setting: the text comes from one population (thinkers), the votes from another (participants), and the output is not a position estimate but a rule that decides who may ratify what. Kim et al. assume one population; Arena has two.

### Gaps
- Talk to the City's exact pipeline remains unverified, as in B2.
- "Nuanced/Sylvain-type efforts": the search found no platform matching those names. A correct name from Benjamin would help.
- Remesh's reported use of text similarity in a latent factor model appeared only in a search summary. I could not find a primary source.
- Meta 2026 outcome data: search blocked.

## 6. Candidate designs: evaluation, identifiability, attacks, circularity, and novelty

### Takeaway
The four designs are not rivals; they are layers. Keep map clusters out of the core score as a sole viewpoint axis: use them as one structure among several, keep a free residual factor to audit the map, and calibrate "signed by the described side" against the cluster's own quote-anchored statements. The real novelty is a narrow one: measuring and calibrating directional "the described side signs this", using a map built from a different population's public works.

### Cited Findings
Evidence bearing on the designs. All design judgments are under Inferences.
- Decision D-31.1 already says "The viewpoint dimension is the map's real clusters, not a single inferred left/right axis", with fidelity from the described cluster and portability from others, and rater reputation tied to matching outcomes. [`docs/02-DECISIONS-LOG.md`](/Users/benjaminlife/dev/schismogenesis/docs/02-DECISIONS-LOG.md)
- `packages/arena_reputation` holds only an empty `__init__.py`, so this scorer has not yet been built. [repo](/Users/benjaminlife/dev/schismogenesis/packages/arena_reputation/src/arena_reputation/__init__.py)
- Single-partition weakness: [Blair et al.](https://www.cs.toronto.edu/~nisarg/papers/bridging.pdf).
- A text-based position predictor is the attacker's positioning tool: [Selvam et al.](https://arxiv.org/html/2607.01824v1).
- Second-axis loss under too few dimensions: [Andreou & Sirivianos](https://arxiv.org/html/2609.21496).
- ITT prior art:
  - [Brand, Brady & Stafford 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12519043/): 1,200 participants; a person passes if opponents agree with their argument at least as much as with real proponents' arguments; people were broadly competent. [peer-reviewed]
  - [Gamba, Romero & Schoenebeck 2025](https://arxiv.org/html/2512.12187v1) tested ITT as an intervention. [preprint]
  - Dawes, Singer and Lemons 1972: doves exaggerated hawk extremity. [Econlib account](https://www.econlib.org/archives/2013/06/a_hawk-dove_ide.html)
  - A commenter there warns self-identified groups differ from groups as outsiders label them.
- Embeddings fail on stance-flipped wording unless tuned: [Blair et al. 2026](https://www.alphaxiv.org/abs/2605.08360).
- ADR-035: 40 idea families, nine schools at top of tested range, about 10% of person-idea cells filled, "No agent ratifies". [ADR-035](/Users/benjaminlife/dev/schismogenesis/docs/adr/ADR-035-idea-families-and-two-reader-structure.md)

### Inferences
Everything below is my own analysis unless linked.

**Design A. Seed Polis statements from extracted ideas.**
- Status: mostly decided already (B2 update, D15, D17), and not novel; LLM-derived statements are what Polis 2.0 reports doing.
- Identifiability: fine for placing participants, since each statement is the same item for all. But items define the axes, per Gelauff's convener effect. Only axes present in the seeds can appear.
- Attack: low direct risk. The main capture route is agenda control by whoever runs extraction and selection.
- Circularity: moderate and confirmatory. The map can look validated by votes it framed.
- Mitigation: reserve a share of statements from participants, not the map, and test for vote axes not present in thinkers' families.
- Do not copy Polis's routing. Its asymmetry between agree and disagree and its extremity bonus would shape who appears. Log every exposure, because propensity correction is impossible without those logs.

**Design B. One joint factorization over person × idea stance, rater × note, and idea embeddings.**
Sketch:
- r_us = a_u + b_s + x_u·y_s for participants × statements.
- h_pi = a_p + b_i + x_p·y_i for thinkers × ideas.
- h_un = i_u + i_n + f_u·f_n for ratings.
- y_i = W e_i + δ_i, where e_i is the embedding.
- Link by y_s = y_i for statements taken from ideas.

Assessment:
- Identifiability: weak. There are rotation and sign freedoms across all blocks, plus the translation freedom from Question 2. Shared anchor statements are the only link between populations, and they assume a statement means the same to thinkers and participants. Our own `sense_fork` exists because schools use the same words differently, so that assumption fails where it matters most.
- Data scale: about 27 thinkers and 10% fill cannot support this. Birdwatch stayed 1D for this reason on a far larger dataset.
- Embedding prior: raw embeddings measure topic, not stance (Blair 2026, ADR-035). Use only tuned or per-topic projections, and only as a prior for cold start.
- Attack: high. A published text-to-position model is Phase 1 of Gaming Consensus.
- Capture: errors spread between blocks. A wrong map pulls rater positions, and reputation inherits it.
- Verdict: do not make this the production score. It is reasonable offline as a research model for filling gaps, as in Kim et al. Prior art is strong, so it would not be novel.

**Design C. Map clusters as the viewpoint dimension in the scorer (D-31.1).**
Three forms exist, and D-31.1 does not say which:
1. Fixed one-hot clusters replacing factors: r_un = μ + i_u + i_n + Σ_k w_uk g_nk with Σ g_nk weighted to 0. Convex and free of rotation issues, and effectively a shrunken per-cluster approval table, i.e. model-based Polis consensus.
2. Map-initialized free factors: the map's meaning drifts as data arrive.
3. Hybrid: the form in (1) plus a free residual f_u·f_n.

My recommendation is (3) for scoring, plus a Blair-style mean over many splits:
- It stops the map being the only difference that counts. The size of the residual factor is a standing audit: if a large held-out gain remains after cluster terms, the map has missed a real divide, exactly the failure Andreou and Sirivianos document. Use their test design, including the permutation null and leave-topics-out.
- It addresses Blair's critique. A fixed partition of nine schools is a single partition.
- A candidate new variant: define splits by idea families, so each family held or rejected induces a split of raters, and average. Blair suggests weighting comment splits by substantiality as future work; using the structure of thinkers' ideas to choose or weight splits goes one step beyond that. Needs a rater's stance per family, obtained from statement votes.

Attacks and capture, in order of concern:
- Cluster weight. With equal cluster weights, splitting a cluster doubles its voice, so boundaries become political. Whoever controls `count` controls the reference population. ADR-035 says nine was the top of the tested range, and it is open.
- Sleeper entry. Fidelity rights flow from placement, and placement comes from votes on public statements. An attacker can vote their way into a cluster, then ratify or block. A public map and open scorer make this cheaper, as Selvam shows at about $3 per account per month.
- Prototype pressure. If rater reputation means matching outcomes within a cluster, members who dissent internally lose standing, and clusters harden. For a project named after schismogenesis, this is the central circular risk: the instrument could make the divide it measures.
- Label capture of the map. Once clusters confer power, people lobby over them (B3).

Circularity, yes, in three loops:
- Statement selection shapes votes.
- Votes shape membership.
- Membership shapes who ratifies, and hence which descriptions and reputations spread, and those can feed the map.

Break them this way:
- Compute the map only from public-works data, never from Arena scores or ratification outcomes.
- Freeze per round.
- Keep rater placement from a held-out statement set not used to score that rater.
- Publish results with and without cluster terms (B3's counterfactual principle).
- Rotate statement sets, so placement cannot be crammed.

**Design D. Scoring whether a description is signed by the described cluster.**
This is the most distinctive piece and the one best kept separate from portability.
- Do not mix fidelity and portability into one intercept. A faithful description of one side can be repugnant to others. Merging them recreates the suppression that Bouchaud and Milli measure.
- Within the described cluster, require agreement across its internal divisions, so a faction cannot sign for the whole. Early on, with few raters, use Beta-Binomial counts with explicit uncertainty; fit within-cluster factors only once held-out tests justify it.
- Acquiescence risk: people may sign flattering descriptions. Calibrate as follows. Mix each description, blind to author, with real quote-anchored statements from that cluster's landmarks and with deliberately distorted decoys. Count the description as signed only when it scores as well as the cluster's own real statements and beats the decoys. This extends Brand et al.'s passing criterion, and it uses our map's quote-anchored propositions directly.
- Use CCT to estimate each rater's reliability as an informant about the group, instead of a CN-style agreement score. This may reduce prototype pressure, though that is untested. It still rewards fit to the group's answer key, so it does not remove the problem.
- Strategic refusal: a cluster may withhold signature to deny outsiders credit, or to block accurate but uncomfortable descriptions. Allow "accurate but I reject the claim" as a separate vote from "I agree". Note the distinction between "this is what we think" and "this is true". Separate rating wording is essential.
- Identity gap: the people mapped (thinkers) are mostly not raters. A rater near a school is a proxy for it. Report that as a limitation. Where a landmark or their associates respond through the dispute affordance, treat that as a higher-tier check, subject to the rule against contacting landmarks without Benjamin's approval.
- Scale: nine schools make 72 directed pairs. With a CN-like minimum of 5 raters inside the described cluster for each note, rater supply will bind first. X's own data (54% of unresolved notes under 10 ratings) shows this bottleneck even at huge scale.

| Design | Novel? | Identifiability | Attack risk | Circularity | Recommendation |
|---|---|---|---|---|---|
| A. Statements from ideas | No | Good for placement; axes limited by seeds | Low to moderate | Moderate | Do, with open statement share |
| B. Full joint factorization | No in general; two-population form uncommon | Poor at current scale | High | High | Offline research only |
| C. Clusters as sole viewpoint | Partly (exogenous groups exist; public-works map as source not found) | Good | High (boundaries, sleepers) | High | Avoid as sole structure |
| C-hybrid plus many splits | Candidate | Moderate | Moderate | Lower | Prototype |
| D. Described cluster signs, calibrated | Strongest candidate | Moderate; small samples | Moderate | Moderate | Prototype first |

**Honest novelty assessment** (searched for prior art first):
- Not novel: LLM statement generation; joint text and vote models; text and ratings MF; predicting note scores from text; pre-specified groups in bridging; single-partition critique; ITT as measure; multi-group consensus.
- Candidates, no prior art found in these searches:
  1. A viewpoint structure for live bridging derived from a separate population's public works.
  2. A persistent, directional, cluster-pair reputation score for "described side signs".
  3. Fidelity calibrated with real in-group statements and decoys in a live scoring system.
  4. The residual factor as a standing audit of a supplied map.
  5. Splits defined by idea families in mean-split bridging.
- No direct benchmark of stipulated clusters against learned factors, or of the CN scorer against Polis consensus on the same data, was found. This is a cheap, publishable first experiment using public Polis exports.
- Each of these is a small step on existing lines, not a new field. I would call them "untested combinations", not discoveries, until a targeted literature review confirms it.

**Suggested first experiments** (no paid services, all offline):
1. Run CN-style MF, Polis consensus, and Blair PD and p-mean on public Polis exports and compare on held-out votes.
2. Test masking silence in `person_space` against current behaviour.
3. Simulate sleeper and cluster-splitting attacks on a toy Design C before writing the scorer.
4. Pilot calibrated fidelity with a small invited group, subject to Benjamin's approval.

### Gaps
- **Search scope.** Novelty searches run: Polis plus CN joint model; applying CN to Polis data; exogenous groups vs latent factors; text embeddings in CN; LLM plus Polis vote prediction; Remesh text and latent factors; ITT as platform measure; Polis manipulation. Web search then hit the session limit, so these were not run: tensor methods, Meta outcome data, and any search on "meta-consensus" scoring.
- **Meta-consensus prior art.** From memory, unverified: the deliberative-democracy literature uses "meta-consensus" (I recall Dryzek and Niemeyer) and there may be measures such as a deliberative reason index. Check this before any claim of novelty for candidate 2. It is the most likely place for overlooked prior art.
- From memory, unverified: anchor-item methods in IRT and legislative scaling (linking populations via shared items) are the direct formal basis for tying thinkers to voters. Not searched.
- No empirical result exists for any of Designs C-hybrid or D. Attack rankings here are reasoned, not measured.
- The described-cluster mismatch has no sourced solution beyond the Econlib comment.
- Several cited items were read only as search digests, as tagged above, and should be opened before being quoted in anything public.
