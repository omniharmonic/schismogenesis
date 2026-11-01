# B3 — Mechanism Design for the MOVE Layer

> **Design update (2026-10-30).** The Design Dialogue Memo of 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`) records decisions that supersede earlier research recommendations where they conflict; see `synthesis/SYNTHESIS.md` §2. The research below is unchanged. For this brief:
> - **Re-targeted reward: the integrative gradient is now explicit.** MOVE ascends ratified cross-cluster description (how accurately each cluster describes each other, in terms the described would sign), not bridged endorsement of syntheses (SYNTHESIS §2 D1; §8.6).
> - **Modified: Design A (Bridged Endorsement Credit).** The MF intercept becomes the **portability** signal of a cross-cluster note and the fidelity gate becomes its **fidelity** signal; it no longer credits syntheses at proposal; "long-run membership signals" are replaced by statement-reaction membership (§2 D2, D17).
> - **Promoted: Design C (Retroactive Metabolism Funding).** Lineage-based retroactive credit is the default synthesis reward: uptake by both parent clusters, a new map region; never novelty at proposal; synthesis only after ratified steelmen both ways (§2 D3–D4).
> - **Specified: the within-cluster deepening track.** Scenius is rewarded by within-scene lineage; **hardening** (status earned against an outgroup) earns nothing and is detected (§2 D5).
> - **Retained:** Design D as a cheap measure of understanding; Design B only with a payment leg; groups G now come from reaction-based clusters. The stakes floor and topic normalization still apply.

*Dialogos Arena research brief, wave 1. Author of record: Benjamin Life (@omniharmonic). Task: how to weight preferences and reward the metabolizing of ideas across memetic clusters.*

---

## Summary

The MOVE layer needs to reward people for absorbing and integrating ideas from other clusters, not just for being popular inside their own. Several existing mechanisms already do part of this:

- **Plural QF / connection-oriented cluster matching (CO-QF / COCM)** subsidizes a project only when support comes from different groups. Gitcoin has run it at scale, in about 89% of rounds observed in one study.
- **Community Notes' bridging algorithm** promotes an item only when raters with opposite latent viewpoints both rate it well.
- **Polis's group-informed consensus** multiplies the agreement rates of each opinion group, so one dissenting group can block a high score.

All three use the same move: credit "agreement across difference" and discount agreement within a group. That is the integrative gradient in mechanism form.

They also share three failure modes:

1. They penalize real, tight-knit communities. This is Gitcoin's most-reported COCM harm.
2. They can favor bland, low-stakes content and censor controversial topics.
3. They are only as good as the group map they are given. A gameable map means a gameable mechanism.

So MOVE cannot be designed apart from SEE. Cluster definitions become a political attack surface.

I propose four candidate designs that can be stacked:

- **(A)** bridged endorsement credit, weighted by cluster distance
- **(B)** cluster-pair CO-QF matching pools
- **(C)** retroactive "metabolism" funding, judged by a cross-cluster jury plus AI distillation
- **(D)** outgroup-prediction reputation using peer prediction / Bayesian truth serum (Prelec)

Each design comes with explicit Goodhart risks below.

---

## Findings

### 1. Quadratic voting (QV) and quadratic funding (QF): the base layer

- **QV (Lalley & Weyl).** Each voter buys votes, and the cost is the square of the number of votes. The marginal cost of a vote then rises linearly, so people buy votes roughly in proportion to how much they care. In large populations this gives approximately efficient collective decisions, and it lets intensity of preference be expressed, which 1-person-1-vote cannot do. [Lalley & Weyl 2018, AEA P&P]
- **QF / "Liberal Radicalism" (Buterin, Hitzig & Weyl).** A project's funding is (Σ√cᵢ)². The matching subsidy is that amount minus the sum of contributions, which equals Σ_{i≠j}√(cᵢcⱼ). The abstract claims (near-)optimal, "first best" provision of public goods under a "standard model", and says variations can guard against collusion. [Buterin, Hitzig, Weyl 2019, Management Science 65(11); arXiv 1809.06421]
- **Structural vulnerability.** The QF subsidy is a sum over *pairs* of contributors, and it assumes they act independently. Buterin's 2019 note warns that if even two agents coordinate, there is no bound on how much they can extract. He proposed pairwise-bounded subsidies, where each pair's contribution to the match is capped. [Buterin 2019, ethresear.ch "Pairwise coordination subsidies"]
  - Sybils (one person with many identities) are the extreme case: splitting a donation across fake accounts multiplies the match.
  - The love.fund team states this precisely: without a payment leg, "QF actively subsidizes Sybils". For a costless survey they chose sqrt-weighted allocation of a fixed pot with a per-org cap, *not* QF matching. [Gitcoin Brain: knowledge/love-fund-survey-disbursement-plan]
  - **Implication for MOVE.** If endorsements or "attention credits" cost nothing, do not use superlinear QF matching on them. Use a fixed pot, sublinear weighting, caps, and identity anchoring.
- **Gitcoin field evidence (5 years of forum threads).**
  - Per-grant matching caps are the best-validated lever. In GR12 a 2.5% cap held 10 grants that would have taken ~64% of the pool to 25%.
  - Low-N rounds (few donors) can invert QF's promise: dollar size dominates donor breadth.
  - QF structurally underfunds work that donors find hard to see, such as coordination and infrastructure.
  - [Gitcoin Brain: knowledge/gov-forum-learnings/qf-mechanics]
  - Synthesis work in the Arena is exactly that kind of hard-to-see public good, so expect QF alone to underfund it.

### 2. Plural QF / connection-oriented cluster matching (COCM): the closest existing primitive

- **Lineage.** The idea started with the "correlation discounts" sketched in *Decentralized Society* (Weyl, Ohlhaver, Buterin 2022). Miller, Weyl and Erichsen formalized several plural mechanisms: Cluster Match, Connection-Oriented Cluster Match, Squared Cluster Match and Eigen Match. They argue COCM is resistant under several specific technical definitions of collusion, *not* collusion in general. [RadicalxChange blog, "Designing pluralistic mechanisms for QF"; SSRN 4311507; code at github.com/Jmiller4/plural-qf, which could not be fetched this session]
- **Formal CO-QF used at Gitcoin** (Miller, Kanich, Weyl, EAAMO '25):
  - Inputs: contributions cᵢ, a set of groups G, and soft membership weights w_{i,g} that sum to 1 for each person.
  - For each ordered pair of groups (g, h), sum the weighted contributions from members of g who are *not* in h, and from members of h who are not in g.
  - The subsidy is Σ_{g,h} √(g_sum · h_sum).
  - People who belong to both groups count toward neither side of that pair.
  - If every individual is their own group, this reduces exactly to QF.
  - [Miller, Kanich, Weyl 2025, "Fair Decisions through Plurality", arXiv 2509.18343, DOI 10.1145/3757887.3763019]
- **How Gitcoin defines groups.** The groups are the *projects*: a donor's weight in project p is their donation to p divided by their total giving.
  - A first design was dropped because results were too flat.
  - A design that built groups from donation patterns was dropped because it was open to Sybil attack.
  - [same]
  - **This is the opening for the Arena.** COCM accepts any group structure. Gitcoin had no independent social map, so it used projects as a stand-in. The SEE layer can supply groups from the social graph and the claim graph.
- **Results.** CO-QF was used in 32 of 38 rounds (~$4M of $4.5M). All 8 round managers interviewed preferred it to QF and called it fairer and less of a "popularity contest". In simulations it stayed robust when group membership was only a rough proxy for preferences. [same]
- **Documented harms.**
  1. It penalizes tightly knit or first-time donor bases.
     - In GG22, a project with 27 real donors got $0 match because 23 of them fell in one cluster of new wallets. Gitcoin's core team conceded the cost was real.
     - CCN Climate rejected COCM after it cut top grantees' matching by 60–70%.
     - [Gitcoin Brain: knowledge/gov-forum-learnings/qf-mechanics]
  2. Benjamin's own GG21 OpenCivics retrospective: operators could not explain results to grantees and had to blend 50/50 with standard QF. [Gitcoin Brain: knowledge/gov-forum-learnings/sybil-identity, citing gov.gitcoin.co/t/19313]
  3. It penalizes donors who independently reach the same conclusion, and it weakens grantees' incentive to advertise. [arXiv 2509.18343]
- **Usual pairing.** Gitcoin runs COCM alongside Human Passport model-based Sybil scoring. [human.tech blog, "Defending Gitcoin Grants"]

### 3. Bridging algorithms: Community Notes and Polis

- **Community Notes / Birdwatch.**
  - The model predicts a rating as r̂ = μ + i_user + i_note + f_user·f_note.
  - Intercepts are regularized about 5× more strongly than the factors (λ 0.15 vs 0.03).
  - A note is shown as "helpful" only if its *intercept* is ≥ 0.40. The intercept is the helpfulness that the 1-D viewpoint factor cannot explain.
  - The factor captures rater viewpoint without being told what it is. A second dimension added little.
  - Notes chosen by bridging reduced resharing in a field deployment.
  - [Wojcik et al. 2022, arXiv 2210.15723]
- **Ovadya & Thorburn on "bridging systems".** They define bridging as raising mutual understanding and trust across divides, not erasing conflict. Their listed risks:
  - gaming by fake accounts
  - "bridging-bait"
  - rewarding shallow, low-stakes content
  - harmful bridges (groups uniting against a third group)
  - suppressing conflict that drives legitimate change
  - [arXiv 2301.09976]
- **Empirical warning.** On 70M Facebook URLs, naive bridging raised quality but systematically down-ranked URLs about controversial topics. The authors conclude bridging needs to be topic-aware. [Milli, Thorburn et al., NeurIPS 2024]
  - This is the "performative both-sidesing" risk in measured form: it rewards being unobjectionable, not integrative.
- **Polis group-informed consensus.** For each opinion group, take that group's smoothed agree rate, (agrees+1)/(votes+2). Multiply across groups. One united dissenting group can block a high score. The result is sensitive to how groups are clustered. [compdemocracy.org/group-informed-consensus]

### 4. Pairwise preference, Deep Funding, retroactive funding, conviction voting

- **Pairwise (formerly Budget Box).**
  - Participants choose between two options at a time, and the choices are aggregated into a global ranking. It was used in some Optimism RetroPGF rounds.
  - Limitations: it needs many comparisons, it doesn't capture intensity, and voters get fatigued. [gitcoin.co/mechanisms/pairwise]
  - Optimism's two-year retrospective agrees that humans are good at "which is more valuable", poor at magnitudes, and overwhelmed when asked to allocate across 600+ projects. [gov.optimism.io/t/9239]
- **Deep Funding (Buterin).**
  - AI models propose weights on a dependency graph.
  - A human jury spot-checks random pairs.
  - Models are scored on how well they predict the jury.
  - Known risks: jury bias spreading into the models, gaming the graph's structure, and opacity.
  - [gitcoin.co/mechanisms/deep-funding]
  - Jury analysis: across 611 votes from 51 jurors, agreement was 63–89% depending on the comparison set, and longer deliberation did not improve agreement. [kronosapiens 2025]
  - **This is the most relevant template for "who judges synthesis quality".** A small cross-cluster human jury provides ground truth on sampled pairs, and an AI scales it to the rest.
- **Retroactive funding (Optimism).**
  - Gaming observed: splitting one project into several entries to collect more allocations, and campaigning to clear approval thresholds.
  - By the operators' own admission, there is no data yet showing retro funding gives better outcomes.
  - Recommended direction: metrics propose allocations, experts refine them, and the metrics are backtested against expert judgment.
  - [gov.optimism.io/t/9239]
  - The Gitcoin forum likewise found milestone- and retro-verified funding cleaner than funding based on promises. [Gitcoin Brain: knowledge/gov-forum-learnings/measurement-impact]
- **Conviction voting** (Commons Stack / BlockScience, with Zargham and Emmett).
  - Support builds up over time while tokens stay staked on a proposal, and decays when they are withdrawn.
  - This rewards durable preference over flash mobilization. It is useful if MOVE should favor syntheses that *hold* support over time rather than spike.
  - [BlockScience, "A Brief History of Conviction Voting"; not read in full this session]

### 5. Eliciting honest belief and belief change

- **Peer prediction (Miller, Resnick & Zeckhauser 2005).** Raters are paid according to how well their report predicts a peer's report. This makes truthful reporting an equilibrium even when there is no ground truth. [Management Science 51(9)]
- **Bayesian truth serum (Prelec 2004).**
  - Each respondent gives (a) their answer and (b) a prediction of how others will answer.
  - Answers that are "surprisingly common" (more common than people predicted) score well.
  - This rewards truthfulness under a common-prior, large-population assumption.
  - [Science 306:462]
- **"Surprisingly popular" (Prelec, Seung & McCoy 2017).** Choosing the answer that beats its predicted popularity recovers the right answer even when the majority is wrong. [Nature 541]
- **Relevance to MOVE.** Asking people to *predict the other cluster's judgment* is an ideological Turing test turned into a mechanism. It directly measures understanding across difference, which is a precondition of dialogos.
- **Futarchy and prediction markets (Hanson).** "Vote on values, bet on beliefs": markets estimate which policies would achieve the goals people voted for. [Hanson, J. Political Philosophy 2013; mason.gmu.edu/~rhanson/futarchy.html]
  - For MOVE, conditional markets could forecast whether a synthesis will later be endorsed by its origin clusters.
  - Thin markets and manipulation are the standard caveats.

### 6. AI as mediator and judge

- **Habermas Machine (Tessler et al., Science 2024).** LLM-written group statements were preferred to human-mediator statements and reduced division within groups. [science.adq2852; not read in full this session]
- **Generative social choice (Fish, Gölz, Parkes, Procaccia et al.).** LLMs generate candidate statements, and those are combined with proportional-representation guarantees ("justified representation") so that each sizeable group sees itself represented. [arXiv 2309.01291]
- **Implication.** AI can *propose* syntheses and *estimate* how each cluster will receive them. Final credit should rest on real cross-cluster human endorsement, with AI used the way Deep Funding uses it: distilled from sampled human judgments and scored against them.

### 7. Sybil resistance and identity

- **Proof of personhood (Borge, Kokoris-Kogias, Ford et al. 2017).** "Pseudonym parties": people show up in person at the same time to receive one token each. [bford.info/pub/dec/pop-abs]
- **Social-graph defenses (SybilGuard, Yu et al., SIGCOMM 2006).** These rely on the fact that a Sybil region connects to honest users through only a few "attack edges". [comp.nus.edu.sg/~yuhf/sybilguard-sigcomm06.pdf]
  - The SEE layer's follow graph doubles as a Sybil detector. But X follow graphs are cheaply botted, so treat this as one weak signal among many.
- **Human Passport** (Gitcoin Passport spun out in 2024, acquired by Holonym, renamed December 2024). It combines identity "stamps" with model-based scoring of on-chain history (0–100), and runs alongside COCM in Gitcoin Grants. [human.tech blog]
- **Gitcoin forum lessons.** [Gitcoin Brain: knowledge/gov-forum-learnings/sybil-identity]
  - Verification friction drops about 10–20% of legitimate users, worst for newcomers.
  - "Verify-then-count" vs "count-then-detect" was never resolved.
  - What worked in practice: an ensemble of weak signals plus a "canary" rule (never flag a known-legitimate account), human review, and appeals.
  - Regen Rio's tiered "trusted local list" scaled matching by trust tier.
- **Implication.** Make identity graduated, not binary. Unverified users can participate fully in MEET. Their weight in MOVE rises with personhood and track record.

### 8. Goodhart and gaming

- **Four Goodhart variants (Manheim & Garrabrant).** [arXiv 1803.04585] Each maps onto MOVE:
  - **Regressional:** "endorsed by both clusters" correlates with real synthesis, but the top scorers are partly noise.
  - **Extremal:** at the top of the distribution, bland platitudes win (matches the Milli et al. finding).
  - **Causal:** gaining endorsement by both sides doesn't cause understanding.
  - **Adversarial:** people farm endorsements, fake outgroup identities, and trade endorsements across clusters ("I'll endorse yours if you endorse mine").
- **Specific gaming risks for "reward synthesis":**
  1. Performative both-sidesing: vague statements anyone can endorse.
  2. Strawman synthesis: one side's view dressed up as a bridge.
  3. Cluster-hopping or identity laundering to look like a distant-cluster endorser.
  4. Reciprocal endorsement rings across clusters, which COCM-style pair sums actually *reward*.
  5. Choosing contrived "distant" pairs to farm the distance multiplier.
  6. Pushing toward homogenization. Rewarding convergence alone destroys the requisite variety the thesis depends on.
- **Who judges.** Use a layered answer, not a single judge:
  - Origin-cluster members check whether their own view is represented faithfully (they hold a veto on misrepresentation).
  - Distant-cluster peers check that the result is not trivially one-sided.
  - AI handles scale, triage and prediction, and is regularly scored against held-out human panels.
  - **UNVERIFIED design hypothesis:** no source tests this three-part split end to end.

---

## How this answers the governing question (layering + validation)

**The mechanism *is* a consumer of the map.**

- Every plural mechanism above takes a group structure as input: COCM's G and w_{i,g}, Polis's opinion groups, Community Notes' latent factor.
- So the SEE layer's accuracy determines whether MOVE is fair.
- CO-QF accepts *soft, overlapping* memberships. That matches what layered SEE should produce: a probability distribution over clusters for each person, not a hard label.

**Suggested layering for MOVE inputs:**

1. **Social graph (follows, quotes)** gives membership w_{i,g}: *who someone belongs with*. This is where QF-style collusion actually happens, because people coordinate through social ties.
2. **Claims graph** (ontological, epistemological, axiological and praxis layers) gives the distance d(g,h): *how far apart worldviews are*. Use claim-level distance, not follow-graph distance, so that two clusters that dislike each other socially but agree on substance don't earn a large "bridging" bonus.
3. **Embeddings** should *only* group syntheses by topic, which supports topic-aware bridging (the Milli et al. fix). They are not reliable for stance.
4. **Behavioral latent factor:** a Community Notes-style factorization of in-Arena endorsements, learned from rating behavior.

**Validation via convergent evidence.** The behavioral latent factor in layer 4 is an *independent measure of the same map*, and it is free.

- If SEE's clusters are right, users' learned factor positions f_user should separate cleanly by SEE cluster.
- If they don't, either the map or the mechanism is wrong.

Other validation tests:

- **Predictive test.** SEE should predict which syntheses each cluster will endorse. Score these predictions with held-out endorsements, as Deep Funding scores models against its jury.
- **Self-recognition test** (shared with other briefs). Users and outgroup members rate whether their assigned cluster and claim summary are faithful. The BTS-style outgroup-prediction task in Design D doubles as a measure of how legible each cluster is.
- **Canary sets.** Following Gitcoin's lesson, keep known tight-knit legitimate communities and known Sybil rings as fixtures. Every change to the mechanism must leave the legitimate group unpenalized and the Sybil ring unrewarded.
- **Counterfactual reporting.** Publish results under plain QF, CO-QF and the chosen design side by side. Gitcoin found that opaque labeling, not unfair math, caused most disputes.

---

## Candidate incentive designs for "ascending an integrative gradient"

Notation:

- A *synthesis* S is an artifact produced in MEET (claim, statement, reframing) whose provenance links it to origin clusters g and h.
- d(g,h) ∈ [0,1] is the claim-graph distance between those clusters, from SEE.
- Endorsements come from personhood-weighted users with soft membership vectors.

### A. Bridged Endorsement Credit (Community Notes × Polis × distance)

**Mechanism**

1. Users endorse or reject syntheses.
2. Fit a factorization model, r̂ = μ + i_u + i_S + f_u·f_S, where f is initialized from or constrained by SEE positions.
3. The credit for S is its *intercept* i_S, the cross-viewpoint helpfulness, multiplied by a Polis-style product of per-cluster agree rates over S's origin clusters, multiplied by a bounded distance bonus (1 + α·d(g,h)).
4. Credit accrues as non-transferable reputation to the synthesis's authors and to the endorsers who helped it cross over (first cross-cluster endorsers, scored with a delay).

**Fidelity gate.** Before an endorsement from an origin-cluster member counts, they must confirm "my view is represented faithfully" (a strawman veto).

**Failure modes**

- **Bland-bridging and controversy suppression.** Mitigation: topic-normalize credit within each topic bucket (from embeddings), and add a "stakes" floor using claim-graph centrality (a synthesis must touch a load-bearing claim of each origin cluster).
- **Distance farming** through contrived pairings. Mitigation: provenance must come from an actual MEET session between those clusters; cap α; d must come from the claims graph, not be declared by the author.
- **Outgroup impersonation** (concern trolls claiming to be from cluster h). Mitigation: membership comes from long-run social and behavioral signals, not self-declaration; there is a minimum account age and track record per cluster.
- **Cold start.** The factor model needs ratings density. Use AI-predicted endorsement as a prior, marked as provisional.

### B. Cluster-Pair CO-QF Matching Pool (plural QF with SEE groups)

**Mechanism**

- Each synthesis is a "project" in a recurring round.
- Users spend a *budgeted, scarce* allotment of credits on syntheses: real money, or non-cash credits under a fixed pot.
- Matching uses CO-QF with groups G taken from SEE clusters (not projects), soft weights w_{i,g}, and each pair term weighted by distance: Σ_{g,h} d(g,h)·√(g_sum·h_sum).
- Support from within one cluster earns direct contribution only, no match. Support from distant clusters earns the most.
- Per-synthesis caps apply (Gitcoin's best-validated lever). Publish both raw and matched figures.

**Failure modes**

- **Tight-knit penalty.** This is the single best-documented harm of COCM. A real minority community that independently loves a synthesis gets nothing. Mitigation:
  - blend with plain QF (Gitcoin's 50/50 workaround)
  - keep a separate "within-cluster deepening" pool so MOVE does not only pay for bridging
  - add a floor for underrepresented clusters
- **Costless credits mean Sybil subsidies.** If credits are free, do not use superlinear matching. Fall back to the love.fund pattern: sqrt-weighted allocation of a fixed pot plus caps.
- **Cluster definition becomes a political target.** Actors lobby to have rivals merged into one cluster (less match) or split apart (more match). Mitigation: publish the clustering method, freeze the map for each round snapshot, and run an appeals window.
- **Reciprocal cross-cluster rings** ("you fund mine, I fund yours"). Mitigation: pairwise-bounded subsidies (Buterin 2019), detection of reciprocity within the endorsement graph, and a public challenge window before payout.
- **Low-N noise.** Rounds with few participants are dominated by dollar size. Use minimum participant thresholds.

### C. Retroactive Metabolism Funding (Deep Funding × RetroPGF × prediction markets)

**Mechanism**

Reward syntheses *after the fact* for measured metabolism: evidence that the idea actually entered both origin clusters' belief systems. Evidence includes:

- uptake and citation of the synthesis claim inside each cluster's discourse, measured through claims-graph diffs over time
- new bridge edges in the SEE topology
- self-reported belief updates collected with BTS scoring

**Judging**

- A rotating cross-cluster jury, with seats allocated proportionally by cluster in the spirit of generative social choice's justified representation, gives pairwise judgments ("which synthesis moved the landscape more?") on sampled pairs.
- AI models predict the jury's judgments across all syntheses and are scored against them (the Deep Funding pattern).
- Optionally, conditional prediction markets on "will cluster h endorse S within 6 months?" give an early signal and a reason to scout syntheses that are undervalued.

**Failure modes**

- **Goodhart toward homogenization.** If "movement" means convergence, the mechanism pays for erasing difference. Mitigation:
  - reward *bidirectional* uptake (both clusters change)
  - reward new bridges, not cluster merger
  - track cluster diversity (number of clusters, the claim-graph's spread) as a constraint that must not fall
- **Attribution.** Did S cause the shift, or did events? Mitigation: compare against matched counterfactual topics and accept a noisy signal; Optimism admits there is still no outcome evidence for retro funding.
- **Jury capture and bias spreading into the AI.** Mitigation: rotate juries, have them disclose their clusters, check for disagreement by cluster, and publish model scores.
- **Measurement gaming.** Mitigation: people seed the synthesis's phrasing into their cluster's discourse to fake uptake, so measure *claim-level* adoption (paraphrase-robust), not keyword echoes.
- **Thin and manipulated markets.** Mitigation: use markets only as advisory signals at small scale.

### D. Outgroup-Prediction Reputation ("steelman score" via peer prediction / BTS)

**Mechanism**

1. For each synthesis or contested claim, participants report (a) their own judgment and (b) a *prediction of the distribution of judgments in each other cluster*.
2. Scoring uses BTS (Prelec) or peer-prediction rules, plus accuracy against the outgroup's actual reported distribution.
3. Users build a non-transferable, decaying "understanding reputation" per cluster pair: a measured ability to model the other side (an ideological Turing test).
4. This reputation then *weights* their endorsements in Designs A and B. Endorsements from people who demonstrably understand the other side count more.
5. It also identifies natural bridge-builders for the MEET layer.

**Failure modes**

- **Stereotype learning.** Users may predict the outgroup accurately by modeling caricatures, without real understanding. Mitigation: score predictions of *individual-level* nuance (claim-layer reasons), not just distributions, and mix in qualitative steelman checks rated by the outgroup.
- **BTS assumptions break.** BTS needs a common prior, a large population and independent signals. Clusters with different priors are the *whole point*, so validity is uncertain (UNVERIFIED for this setting). Mitigation: pilot it, and compare with simple accuracy scoring.
- **Collusion between clusters.** Members of h could tell members of g what h will say. Mitigation: elicit at the same time and score on held-out samples.
- **It rewards modeling, not changing.** It only covers a precondition of synthesis. Pair it with C.
- **Exclusion.** The cognitive load is high. Keep it optional and a bonus layer, never a gate.

### Recommended stack

1. Start with **D** (cheap, no money, collects data) and **A** (reputation only).
2. Add **B** with a fixed pot once membership and identity are stable.
3. Run **C** quarterly as the outer loop that backtests whether A and B credit predicts real metabolism. This answers Optimism's lesson that metrics should be backtested against judgment.

---

## Reusable assets and design implications

- **CO-QF reference implementation:** github.com/Jmiller4/plural-qf (could not be fetched this session). Also the Gitcoin qf-calculator / cluster-matching notebook (roundoperations.gitcoin.co). Both accept a custom group structure, so SEE output can drop in.
- **Community Notes open-source scorer:** X publishes its ranking code and data (communitynotes.x.com guide; could not be fetched this session). Its parameters (intercept ≥ 0.40, 1-D factor) are a starting point.
- **Polis group-informed consensus:** a trivial formula, good for in-session MEET scoring.
- **Gitcoin Brain playbooks:**
  - knowledge/gov-forum-learnings/qf-mechanics and /sybil-identity: caps, canary sets, appeals, raw-versus-matched transparency, tiered trust
  - knowledge/love-fund-survey-disbursement-plan: sqrt plus fixed pot plus cap for costless signals; forensic screening done in batches and judged by humans
  - knowledge/local-qf-record-model: atproto records with "the match is a re-derivable computation" (relevant if the Arena publishes allocations as verifiable records)
- **Benjamin's prior writing:** "Fork You!" (Parachute wiki/writing/fork-you) argues for functional pluralism through QV/QF. That is consistent with the constraint that MOVE must preserve variety, not only reward convergence.
- **Design principles carried forward:**
  1. Identity is graduated, not binary.
  2. Cluster maps are frozen per round, published, and open to appeal.
  3. Always report results under plain QF too.
  4. Keep a separate within-cluster "deepening" track.
  5. Cluster diversity is a hard constraint on any reward for convergence.
  6. Synthesis credit needs both a fidelity check (origin clusters agree they were represented faithfully) and a stakes check (it touches a load-bearing claim).

---

## Risks and open questions

1. **Money versus reputation.** Paying for synthesis may crowd out intrinsic motivation and invite professional farming. A known economics finding: price incentives can reduce prosocial behavior (Frey & Oberholzer-Gee 1997, AER). Not re-verified this session. **Open:** start with reputation only?
2. **Who sets d(g,h)?** Distance in the claim graph is a modeling choice with political consequences. A cluster labeled "far" earns more for bridging. That rewards bridging *to* groups mapped as extreme, which may legitimize harmful bridges (Ovadya & Thorburn).
3. **Does COCM generalize from "groups = projects" to "groups = worldview clusters"?** Miller et al. show robustness when groups are rough proxies in simulation, but no field test with social-graph groups exists (UNVERIFIED).
4. **X data dependence.** If membership comes from the X graph, API cost and terms of service can change the mechanism's inputs without notice. Botted follows contaminate both the map and Sybil scoring.
5. **Gitcoin field signal on tight-knit penalties** is the strongest warning in the evidence base. Bioregional and local communities (Benjamin's core constituencies) are exactly the shape that COCM penalizes.
6. **AI as judge.** LLM mediation (the Habermas Machine) may produce majority-flavored consensus. Proportional representation guarantees (generative social choice) help but are untested at Arena scale.
7. **Legal.** Real-money cross-cluster matching on political content may raise campaign-finance or lobbying questions in some jurisdictions. Not researched (UNVERIFIED).
8. **Could not fetch:** the full Miller/Weyl/Erichsen SSRN paper, the plural-qf repo, the Community Notes "ranking notes" guide, and the full text of Buterin's pairwise-subsidies post. The formula claims above come from the EAAMO '25 paper and the Birdwatch arXiv paper, which were fetched.

---

## Sources

**Papers and primary documents**
- Lalley & Weyl, "Quadratic Voting: How Mechanism Design Can Radicalize Democracy," AEA P&P 108 (2018) — https://www.aeaweb.org/doi/10.1257/pandp.20181002
- Buterin, Hitzig & Weyl, "A Flexible Design for Funding Public Goods," Management Science 65(11) 2019 — https://arxiv.org/abs/1809.06421
- Buterin, "Pairwise coordination subsidies: a new quadratic funding design" (2019) — https://ethresear.ch/t/pairwise-coordination-subsidies-a-new-quadratic-funding-design/5553
- Weyl, Ohlhaver & Buterin, "Decentralized Society: Finding Web3's Soul" (2022) — https://papers.ssrn.com/abstract=4105763
- Miller, Weyl & Erichsen, "Beyond Collusion Resistance: Leveraging Social Information for Plural Funding and Voting" — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4311507 ; blog https://radicalxchange.org/media/blog/designing-pluralistic-mechanisms-for-quadratic-funding ; summary https://ethresear.ch/t/collusion-resistance-and-plurality-in-quadratic-mechanisms-paper-summary/14545
- Miller, Kanich & Weyl, "Fair Decisions through Plurality: Results from a Crowdfunding Platform," EAAMO '25 — https://arxiv.org/html/2509.18343v1
- Wojcik et al., "Birdwatch: Crowd Wisdom and Bridging Algorithms…" (2022) — https://arxiv.org/abs/2210.15723
- Ovadya & Thorburn, "Bridging Systems" (2023) — https://arxiv.org/pdf/2301.09976
- Milli, Thorburn et al., "Bridging in Social Media Feeds Censors Controversial Topics," NeurIPS 2024 — https://neurips.cc/virtual/2024/99058
- Computational Democracy Project, "Group informed consensus" — https://compdemocracy.org/group-informed-consensus
- Miller, Resnick & Zeckhauser, "Eliciting Informative Feedback: The Peer-Prediction Method," Management Science 2005 — https://presnick.people.si.umich.edu/papers/elicit/index.html
- Prelec, "A Bayesian Truth Serum for Subjective Data," Science 306 (2004) — https://bibbase.org/network/publication/prelec-abayesiantruthserumforsubjectivedata-2004
- Prelec, Seung & McCoy, "A solution to the single-question crowd wisdom problem," Nature 2017 — https://news.mit.edu/2017/algorithm-better-wisdom-crowds-0125
- Hanson, "Shall We Vote on Values, But Bet on Beliefs?" — https://mason.gmu.edu/~rhanson/futarchy.html
- Manheim & Garrabrant, "Categorizing Variants of Goodhart's Law" — https://arxiv.org/abs/1803.04585v4
- Borge et al., "Proof-of-Personhood: Redemocratizing Permissionless Cryptocurrencies" (2017) — https://bford.info/pub/dec/pop-abs/
- Yu et al., "SybilGuard," SIGCOMM 2006 — https://www.comp.nus.edu.sg/~yuhf/sybilguard-sigcomm06.pdf
- Tessler et al., "AI can help humans find common ground in democratic deliberation," Science 2024 — https://www.technologyreview.com/2024/10/17/1105810/ai-could-help-people-find-common-ground-during-deliberations/ (secondary; primary not fetched)
- Fish, Gölz, Parkes, Procaccia et al., "Generative Social Choice" — https://arxiv.org/abs/2309.01291

**Implementations and operator documentation**
- Gitcoin, Deep Funding — https://gitcoin.co/mechanisms/deep-funding
- Kronosapiens, Deep Funding jury analysis (2025) — https://kronosapiens.github.io/blog/2025/08/03/deepfunding-jury-analysis
- Gitcoin, Pairwise — https://gitcoin.co/mechanisms/pairwise
- Optimism, "Lessons learned from two years of Retroactive Public Goods Funding" (ccerv1, 2024) — https://gov.optimism.io/t/lessons-learned-from-two-years-of-retroactive-public-goods-funding/9239
- BlockScience, "A Brief History of Conviction Voting" — https://medium.com/block-science/a-brief-history-of-conviction-voting-ad4ca4eb4aee
- Human Passport × Gitcoin Grants (model-based detection; rebrand) — https://human.tech/blog/defending-gitcoin-grants
- Gitcoin round ops, cluster matching — https://roundoperations.gitcoin.co/round-operations/post-round/cluster-matching-and-csv-upload
- Gitcoin forum, COCM update nerd post (2024-04-30) — https://gov.gitcoin.co/t/nerd-post-updates-to-cluster-mapping-matching/18705

**Vaults**
- Gitcoin Brain: knowledge/gov-forum-learnings/qf-mechanics ; knowledge/gov-forum-learnings/sybil-identity ; knowledge/gov-forum-learnings/measurement-impact ; knowledge/love-fund-survey-disbursement-plan ; knowledge/local-qf-record-model
- Parachute: wiki/concepts/quadratic-funding ; wiki/writing/fork-you ; vault/projects/localism-fund/PROJECT

**Blocked or unreadable this session:** github.com/Jmiller4/plural-qf ; communitynotes.x.com/guide/en/under-the-hood/ranking-notes
