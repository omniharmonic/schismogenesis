# Computational Sociology and Cultural Analytics Methods for Describing Worldview Groups (late 2026)

Method notes for this file:
- Fit ratings (High / Medium / Low / None) are my judgment for our setting: 27 thinkers, 93 works, 360 ideas, about 10% fill. They are not published scores.
- Derived figures, from the numbers in the brief and in ADR-035: about 970 filled person-idea cells (27 × 360 × 0.10), about 36 ideas per person, about 2.7 holders per idea, about 3.4 works per person. If fill were independent, two people would share about 3.6 ideas (360 × 0.1 × 0.1). These are estimates, not counts from the database.
- Evidence quality varies. Items marked "snippet" were seen only as search results and the full paper was not read. Marked preprints are not peer reviewed.
- The session's web search budget ran out before the last batch. Remaining holes are listed under Gaps, and no claim was filled in from memory without being marked.

## Which methods should change our pipeline, and in what order?

### Takeaway
No published method fixes 10% fill by clever analysis alone. The biggest gain comes from changing the data: read every work against a small fixed set of contested propositions, so that people are compared on the same items. Our current method is, in effect, a version of Discourse Network Analysis with a distinctive signed-family step. The nearest improvements are treating silence as truly missing, adding an "opposed on the same axis" view, and replacing silhouette with held-out stance prediction.

### Cited Findings
- Stance needs a stated proposition plus a text from which a stance is inferred, and sentiment-based proxies add significant measurement error — [Burnham, Stance Detection guide](https://arxiv.org/abs/2305.01723v2).
- Asking LLMs for positions on a dimension and averaging placed legislators and manifestos at r > .90 against expert, crowd or roll-call benchmarks, generally beating supervised classifiers. The authors still call for empirical validation — [Le Mens and Gallego, Political Analysis 2025](https://arxiv.org/abs/2311.16639v3).
- Zero-shot LLM stance on 1,710 German news paragraphs reached a best weighted F1 of .73, with most statements at medians of about .55 to .58. Human agreement averaged only .55. The authors offer "at best cautious optimism" and require domain-specific evaluation — [Walker and Angst, PLOS ONE](https://pmc.ncbi.nlm.nih.gov/articles/PMC12629487).
- Our own evidence: 80 of 734 machine-proposed holdings survived blind reading, so entailment alone cannot fill gaps — [ADR-035](/Users/benjaminlife/dev/schismogenesis/docs/adr/ADR-035-idea-families-and-two-reader-structure.md).
- ADR-035 says silence is missing data. In `person_space`, silent cells are 0 and each column is then centred, so a silent cell takes the value minus the column mean, and two silent people look alike on it. The module docstring half-admits this — [structure.py](/Users/benjaminlife/dev/schismogenesis/packages/arena_map/src/arena_map/structure.py).

### Inferences
Ranked changes:

| # | Change | Adds or replaces | Why | Effort |
|---|---|---|---|---|
| 1 | Fixed battery of 30 to 60 contested propositions, read against all 93 works, with three outcomes (accepts, rejects, no stated position) plus a quote anchor | Adds a dense matrix next to incidental holdings | Turns "who happened to say what" into a comparable matrix. Directly attacks 10% fill | Medium |
| 2 | Compute distance only over cells both people filled, shrink pairs with little overlap, and report overlap | Replaces centred-zero cosine | Makes the code match ADR-035 | Low |
| 3 | Add a same-axis view (Correlational or Bipolar Class Analysis logic) at family or battery level | Adds to schools | Identifies "opposed but sharing a fault line", the closest numeric stand-in for meta-consensus | Low to medium |
| 4 | Headline validity becomes held-out stance prediction and split-half stability across works | Replaces silhouette against niches | Curated niches are not ground truth, and they are what we are trying to go beyond | Medium |
| 5 | Sense comparison inside a family, with sense induction | Replaces centroid gap in `sense_fork` | Holds topic constant | Low to medium |
| 6 | Specific MCA with silence as a passive category, for the people-and-ideas map | Adds a map; could replace MDS on people | Gives a true joint space | Medium |
| 7 | A small human-coded random sample, Krippendorff's alpha, and design-based correction for any reported percentages | Adds to two readers | Agreement between two models is not independent evidence | Medium |

Change 1 has a real risk: the proposition set is itself a political choice (B4 raised this as "axis selection is political"). Draft it from the existing attack links between ideas, so that the map's own disputes supply the items, and publish it. Do not treat battery answers as ratification; no agent ratifies.

### Gaps
- I could not test any of this on our data, because the task was literature only. The gain from change 1 is unmeasured.
- The share of person-pairs with enough shared families is unknown and should be computed before change 2.
- I do not know whether the "blind second reader" is a person or a model. The ADR does not say. Change 7 matters much more if it is a model.

## Belief structure: what do RCA, CCA, BNA, ResIN, DellaPosta, Baldassarri and Gelman, Converse, Martin, Brandt and Sleegers, and latent class analysis offer?

### Takeaway
This tradition asks a better question than "who agrees with whom": it asks who organises beliefs the same way. Almost all of it assumes a dense table with hundreds or thousands of respondents, so its estimators do not transfer. Its concepts do. The most valuable idea is that exact opposites can share one schema.

### Cited Findings
- **RCA.** Groups respondents who show the same pattern of relationships between answers, so members may hold different opinions but share an understanding of the issues. It is "not designed to address missing data": remove or impute cases first — [Goldberg, RCA page](https://web.stanford.edu/~amirgo/rca.html).
- **CCA.** Shared schemas should produce linear dependence between survey rows, so Pearson correlation replaces relationality. Simulations found CCA reliably more accurate, with no setting where RCA won. On the 1993 GSS (1,532 respondents, 17 items) CCA found four classes to RCA's three, with greatly improved model fit. Two respondents share a schema even if their attitudes are exact inverses — [Boutyline 2017](https://www.sociologicalscience.com/download/vol-4/may/SocSci_v4_353to393.pdf).
- **Bipolar Class Analysis** (arXiv v4, April 2026). Measures similarity in how answers shift between support and rejection. In simulations it consistently outperformed existing methods, and reanalysis found substantively different construals in earlier data. It addresses a known CCA weakness, respondents who give the same answer throughout. It is built for bipolar items, and its empirical analysis includes the same GSS data; at least one application uses listwise deletion — [Cuerno et al.](https://arxiv.org/pdf/2404.17042). Preprint.
- **BNA.** Beliefs are nodes linked by correlation across people. Groups differ mainly in how much their belief systems are organised, not in the logic organising them — [Boutyline and Vaisey, AJS 2017](https://scholars.duke.edu/individual/pub1250743) (full text not read).
- **ResIN.** Treats each response option as its own node, allows attitude asymmetries between groups to be detected, and has a spatial component tied to item response theory — [Carpentras, Lüders and Quayle 2024](https://doaj.org/article/37558af13196435d9cdfe03fb58b597f). Applied to ANES 2000 to 2020, it showed more detailed polarization dynamics than classic BNA — [Chen et al. 2025](https://research.tue.nl/en/publications/a-broken-egg-of-us-political-beliefs-using-response-item-networks/). R package available — [ResIN](https://pwarncke77.r-universe.dev/ResIN).
- **DellaPosta.** Using 44 years of GSS data and opinions as nodes, polarization happens when alignments extend across a wider range of opinions, not only when existing ones intensify. Cross-cutting alignments collapsed into broader clusters — [Pluralistic Collapse, ASR 2020](https://pure.psu.edu/en/publications/pluralistic-collapse-the-oil-spill-model-of-mass-opinion-polariza/).
- **Baldassarri and Gelman; Converse.** Constraint (correlation among a person's opinions, after Converse 1964) rose only slightly while issue partisanship rose more than twice as fast, so parties sort people more than coherence grows — [Partisans without Constraint, AJS 2008](https://zendy.io/title/10.1086/590649).
- **Martin 2002.** Separates tightness from consensus, tying cognitive authority to tightness and clear power structure to consensus, tested on 44 communities — [journal page](https://www.journals.uchicago.edu/doi/10.1086/343192). Abstract paywalled; these details come from a secondary summary seen as a snippet.
- **Brandt and Sleegers.** Implement belief-system networks as a dynamic Ising model and argue this integrates at least six phenomena — [PSPR 2021 record](https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_proquest_miscellaneous_2496242112). Brandt tested network replicability on World Values Survey data from 31 countries — [record](https://openaccess.library.uitm.edu.my/Record/doaj-d74c87db2ffc4d58a47047df9bff9bc4).
- **Latent class analysis.** N = 500 is often enough to recover the class count, though not always; other work finds some settings need 2,000 or more, and fewer indicators or weaker class separation raise the requirement — [Nylund and Henson summary](https://pmc.ncbi.nlm.nih.gov/articles/PMC7328230); [Dziak et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4196274).

### Inferences

| Method | Measures | Data needed | Fit for us | Adds or replaces |
|---|---|---|---|---|
| CCA / BCA | Shared organising logic, including mirror images | Usually hundreds or more; dense rows | Medium, only on a battery or family matrix; None at idea level | Adds "same fault line" pairs |
| RCA | Same, less accurately | Same, and no missing data | Low | Skip in favour of CCA or BCA |
| BNA | Item-to-item structure | Many people per item pair | Low: 40 families means 780 pairs estimated from 27 rows | Do not estimate |
| ResIN | Network of response options | Survey scale | Medium as a picture; Low for inference | Its option-as-node idea supports the map |
| LCA | Latent types | Hundreds to thousands | None | Do not use |
| Constraint (Converse, Baldassarri and Gelman) | Coherence of a person or school | Needs repeated items | Medium on a battery | New descriptive stat for each school |
| Martin tightness and consensus | Two separate properties of a group | Moderate | Medium | Report both per school, and test against who cites whom as an authority |
| DellaPosta | Whether alignments extend to more topics over time | Long time series | Low now; later | Possible warning sign for hardening clusters |

The CCA idea matters most for this project. Our cosine distance puts exact opposites at maximum distance. CCA says two such people may share a schema. On the priority encounter (e/acc × d/acc), that is the difference between "unrelated" and "arguing over one axis". The project's success measure is whether clusters can state their disagreement in shared terms, so this is a candidate pre-dialogue indicator. It has no published validation for this use.

Thinkers are elites, not survey respondents, so their constraint may be much higher than in mass-opinion data, which would help us. That is a hypothesis; I found no direct source.

### Gaps
- The Turner-Zwinkels ResIN or elite-belief-network paper could not be located. The search linked her and Brandt only to other topics. No Galesic link to ResIN was found.
- Searches found no use of any of these methods on elites of about 30 people, or on data with 90% missing cells.
- BNA and Boutyline-Vaisey details rest on abstracts. Correlation with very few shared items is my own concern, not a sourced limit.

## Meaning in text: how can we separate topic from sense, and what do embeddings, topic models, moral lexicons and LLM measurement add?

### Takeaway
Corpus-trained embeddings need far more text than we have, and centroid distance mixes subject with meaning. The workable design is to hold topic constant by comparing uses within one idea family, then induce senses or use a stance-aware model. For measurement, prompted LLMs now beat lexicons and often supervised models, but only with domain gold data. Silicon sampling must stay out of placement.

### Cited Findings
- **Geometry of Culture.** Directions from word contrasts match recognised cultural dimensions, checked against surveys and labelled historical data — [Kozlowski, Taddy and Evans](https://arxiv.org/abs/1803.09288).
- **Concept Mover's Distance.** Measures how engaged a document is with a concept through embeddings — [Stoltz and Taylor 2019](https://scholarhub.vn/publication/Concept-Mover-s-Distance-measuring-concept-engagement-via-word-embeddings-in-texts/81e80f51-abcb-4c8d-b4de-71ea390fd9b1). It extends to poles through semantic directions, and anchor terms must be chosen with theory and domain knowledge — [text2map vignette](https://rdrr.io/cran/text2map/f/inst/doc/CMDist-concept-movers-distance.Rmd).
- **Rodman.** Word-vector successes have largely been confined to massive corpora, whereas political corpora are often small. Best practice for small corpora includes bootstrap resampling of documents and pretrained vectors — [A Timely Intervention, Political Analysis 2020](https://econpapers.repec.org/RePEc:cup:polals:v:28:y:2020:i:1:p:87-111_5).
- **Hamilton.** Tied semantic change to word frequency and polysemy, using six historical corpora over two centuries — [ACL 2016](https://arxiv.org/abs/1605.09096v3). **Garg** used a century of text, validated against Census data — [arXiv](https://alphaxiv.org/abs/1711.08412).
- **Arseniev-Koehler and Foster** argue word embeddings are a formal model of schematic cultural learning — [SMR 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC10653277).
- **Sense-level work.** Most semantic-change approaches measure overall proximity shift without inducing senses, and the field should focus on how and why meaning changes — [Periti and Tahmasebi](https://www.arxiv.org/pdf/2402.12011). Substitute words from a masked model can track shifts in sense prevalence — [Card](https://arxiv.org/pdf/2309.02403v2.pdf). BERT-style models separated senses of "Planck" in a domain corpus — [Simons](https://arxiv.org/pdf/2411.14073).
- **Stance-aware embeddings.** Fine-tuning on Kialo pro and con pairs teaches sentence models to separate opposing views. The study was limited to one base model and one case — [Ghafouri et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.1171.pdf).
- **Computational grounded theory.** A three-step pairing of human interpretation with computational pattern-finding — [Nelson](https://econpapers.repec.org/RePEc:sae:somere:v:49:y:2020:i:1:p:3-42). A later critique argues for computer-assisted rather than computer-led work — [record](https://api.crossref.org/works/10.1177%2F20539517221080146) (snippet).
- **Text as Data.** No method can be assumed to work on a new data set, so validation is essential; unsupervised methods may not give theoretically interesting classes — [Grimmer and Stewart 2013](https://resolve.cambridge.org/core/services/aop-cambridge-core/content/view/F7AAC8B2909441603FEB25C156448F20/S1047198700013401a.pdf/text-as-data-the-promise-and-pitfalls-of-automatic-content-analysis-methods-for-political-texts.pdf). The later book treats discovery and measurement separately and covers validation with and without gold data — [Princeton UP](https://press.princeton.edu/index%2Ephp/node/50738).
- **Moral foundations.** GPT correlated with human annotators at r = .59 to .77 across 15 datasets and 12 languages, against .20 to .30 for English dictionaries — [Rathje et al., PNAS 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11348013). MoralBERT was built from human-annotated Twitter, Reddit and Facebook data — [Preniqi et al.](https://arxiv.org/abs/2403.07678v2). A 2025 preprint reports high LLM false-negative rates of 58% to 90% on moral classification — [arXiv 2507.18523](https://www.arxiv.org/pdf/2507.18523) (snippet). Hoover's corpus had kappa of about .32 by one account, and reported corpus sizes conflict — [Beyond Human Judgment](https://arxiv.org/html/2508.13804v3) (snippet, attribution uncertain).
- **LLM measurement.** Recasting tasks as next-word prediction beat conventional supervised learning in pre-registered tests — [Ornstein et al., PSRM 2025](https://www.cambridge.org/core/product/8EAA8096779B5C9DDBDF1BFC71C63AEC). Generative AI could improve content analysis, but bias, replication and low-quality research are real concerns — [Bail, PNAS 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11127003).
- **Annotation bias.** LLM labels at 80 to 90% accuracy still gave biased estimates and wrong confidence intervals when used directly. Design-based supervised learning fixes this with a small sample of gold labels sent for coding with known probability — [Egami et al., NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d862f7f5445255090de13b825b880d59-Abstract.html).
- **Silicon sampling.** Conditioned models reproduced response distributions, called algorithmic fidelity — [Argyle et al.](https://arxiv.org/abs/2209.06899). Critiques: systematic positive bias across 277,470 synthetic respondents — [arXiv 2606.30085](https://arxiv.org/abs/2606.30085); persona sampling fails to produce real variation — [arXiv 2607.25292](https://www.alphaxiv.org/abs/2607.25292.md); results depend on elicitation method — [arXiv 2603.00059](https://arxiv.org/pdf/2603.00059). All preprints, snippet level.
- **LLM imputation.** Fine-tuned on GSS data (68,846 people, 3,110 opinions), models imputed at AUC .87 but managed only .73 for unasked questions, and were less accurate for low-status, minority and non-partisan people — [Kim and Lee](https://arxiv.org/abs/2305.09620v3).

### Inferences

| Method | Measures | Data needed | Fit for us | Adds or replaces |
|---|---|---|---|---|
| Train our own embeddings, diachronic, Garg | Corpus-wide association | Very large | None | Skip |
| Pretrained semantic axes, Concept Mover's Distance | Closeness to a pole or concept | Works per document | Medium | Cheap secondary check on a family's poles |
| Contextual vectors plus sense induction | Distinct uses of a term | Tens of uses per term and school (my estimate) | Medium, on heavily used terms only | Replaces the centroid gap |
| Stance-aware embeddings | Stance-sensitive similarity | Pro and con pairs; our attack links could supply some | Medium | Improves family formation |
| Structural topic model, BERTopic | Topics, optionally by covariate | Hundreds or more documents | Low, and only for terrain | Do not use for belief |
| Computational grounded theory | Human-led theme building | Scales down well | High | Frame for reviewing families |
| Moral foundations by LLM | Moral framing | Per claim | Medium, as a descriptive tag | Do not use dictionaries |
| Silicon samples | Simulated people | n/a | None for placement | Never show as a person's view |
| LLM imputation | Fills empty cells | Large fitting data | Low; validation only | Benchmark, not map input |

Recommended `sense_fork` change: compare uses inside the same family only, permute within family (a stratified test), and, where a term has enough uses, report which senses differ. The current test can fire simply because two schools discuss different things using the same word. A minimum of 5 uses is also thin. Rodman's document bootstrap should replace use-level permutation, because uses within one work are not independent.

The LLM evidence and our own 80-of-734 result point the same way: LLMs are useful when asked a narrow question about supplied text, and unreliable when proposing what someone believes. Imputation errors falling hardest on non-partisans is a specific warning, because many of our thinkers are off the usual axes.

### Gaps
- Structural topic model details were not returned by search, so no cited statement is made here. BERTopic is covered in B4.
- No source compares these sense methods on claim-length text from long-form thinkers, or gives a minimum number of uses. The "tens of uses" figure is my guess.
- Frame semantics and FrameNet were not returned by search.
- Primary Bisbee et al. was not read; it appears only as cited in [arXiv 2603.00059](https://arxiv.org/pdf/2603.00059).
- I found no source testing moral-foundation validity on long-form intellectual writing.

## Fields and homology: can a Bourdieu-style map with people and ideas in one space work here?

### Takeaway
Yes, as a description rather than a statistical claim, and only at family or battery level with silence handled as a passive category. Specific MCA is the correct tool to try, and it was not what failed in ADR-035. Homology claims need social-position data we do not hold.

### Cited Findings
- Le Roux's specific analysis handles questionnaires with missing answers without complete disjunctive coding, and MCA amounts to a biweighted PCA on indicator variables — [Le Roux 1999](https://www.numdam.org/item/MSH_1999__146__65_0/).
- GDAtools `speMCA` treats NA as "junk" categories by default, or the analyst can recode and select them — [speMCA docs](https://rdrr.io/cran/GDAtools/man/speMCA.html).
- Correspondence analysis on single ideas put 26 of 27 people in one group in our data — [ADR-035](/Users/benjaminlife/dev/schismogenesis/docs/adr/ADR-035-idea-families-and-two-reader-structure.md).
- Martin defends field theory as a coherent approach — [What Is Field Theory?, AJS 2003](https://www.journals.uchicago.edu/doi/10.1086/375201) — and offered provisional techniques for quantifying field effects (Socius 2016) — [Martin's publications](https://home.uchicago.edu/~jlmartin/Topics.htm).
- Mohr's programme: "Four ways to measure culture" and *Measuring Culture* survey formal approaches — [book listing](https://www.lovereading.co.uk/book/9780231180290/isbn/Measuring-Culture-by-John-W-Mohr-Christopher-A-Bail-Margaret-Frye-Jennifer-C-Lena.html). Stoltz and Taylor cite Lee and Martin on "cultural cartography" and Mohr and Duquenne (1997) — [draft](https://arxiv.org/pdf/2007.04508v1).

### Inferences
- **Fit: Medium.** The ADR-035 failure was on single ideas with roughly 2.7 holders each, where rare items dominate. That result says nothing about family-level specific MCA.
- Proposed coding: for each family or battery item, categories accept-leaning, reject-leaning, mixed, silent. Mark silent as passive. Curated niches, work era and layer would be supplementary variables, so that they describe the map without building it.
- What it adds: people and ideas in one space, which `layout` (MDS on people only) cannot give. It could replace MDS for horizontal position while height stays the layer. It is also the natural home for ResIN's response-option idea, since accept and reject are separate points.
- Mohr's duality is already implicit in our structure: people define ideas and ideas define people. Family formation currently uses text and links, not co-holding. Testing families formed partly from co-holding is a cheap extension, though only 2.7 holders per idea makes it noisy.
- Homology needs an independent map of social position (institution, funding, class, training). We could code this for public figures from public biography, and Benjamin should decide whether to.

### Gaps
- No source was found on how specific MCA behaves with about 30 individuals or with most entries passive. Run it, bootstrap it, and do not assume.
- No 2024 to 2026 computational-Bourdieu work on a joint people-and-ideas embedding was returned.
- The Mohr and Duquenne duality paper's content is unverified here; only its citation was seen.
- Le Roux and Rouanet's guidance on inference for geometric data analysis was not retrieved.

## Argument and stance mining: what do stance detection, Project Debater, Key Point Analysis and frame detection add?

### Takeaway
Key Point Analysis is the closest published relative of our merge step and supplies a tested benchmark. Stance detection is usable only per target with local validation. Frame detection by LLM works at a coarse level and tends to generalise.

### Cited Findings
- ArgKP has about 24,000 labelled argument and key point pairs across 28 topics, built from 30,000 crowd arguments on 71 topics. NLI transfer learning reached F1 up to .526, well below direct supervised training — [Bar-Haim et al.](https://arxiv.org/pdf/2005.01619v1).
- Cross-domain work with fine-tuned transformers substantially improved matching — [Bar-Haim et al. 2020](https://arxiv.org/pdf/2010.05369).
- ArgCMV curates about 12,000 arguments from real online debates over about 3,000 topics, and argues ArgKP's limits call for new benchmarks — [ArgCMV 2025](https://www.arxiv.org/pdf/2508.19580).
- Three stance approaches exist (supervised, NLI, in-context learning) — [Burnham](https://arxiv.org/abs/2305.01723v2). Fine-tuning on a small sample lifted zero-shot BART to macro F1 .93 at a .9 confidence threshold, at the cost of dropping about a third of the data — [arXiv 2503.16148](https://arxiv.org/pdf/2503.16148) (snippet).
- GPT models beat BERT for German long-form political stance, though more validation outside social media is pending — [Frontiers 2026](https://www.frontiersin.org/journals/political-science/articles/10.3389/fpos.2026.1745587/full) (snippet).
- Media Frames Corpus uses 14 frame dimensions from Boydstun's codebook — [arXiv 2402.11621](https://ar5iv.labs.arxiv.org/html/2402.11621). On Australian climate coverage, an LLM found 12 frames to human coders' 13, nine in common, and its frames were more general — [AoIR 2025 listing](https://www.snurb.info/node/3527).

### Inferences

| Method | Measures | Data needed | Fit for us | Adds or replaces |
|---|---|---|---|---|
| Key Point Analysis | Which arguments express one point, with counts | Pair labels; hundreds per topic is safer | High | Benchmark for the claim-to-idea merge; report match precision |
| Target-based stance | Position toward a stated proposition | Local gold per target | High, with validation | Engine of the battery |
| Abstaining below a confidence threshold | Trades coverage for precision | Few | High | "No stated position" is a valid output |
| Generic frames | Coarse framing | Per passage | Low to medium | Tag only |
| Issue-specific frames | Debate-specific framing | Hand work | Medium | Same purpose as families |

NLI's weak ArgKP result (.526) is a caution for us: our code gate uses entailment. A gate proves that a statement is supported; it does not prove two statements are the same idea. So the merge into 360 ideas deserves its own human-checked sample.

### Gaps
- No LLM versus BERT head-to-head on ArgKP for 2024 to 2025 was found. ClaimRank was not returned by search, and Project Debater appeared only through these datasets.
- No benchmark for key point analysis on long-form books or podcasts was found.

## Discourse coalitions and adjacent fields: how close is Discourse Network Analysis to our method?

### Takeaway
Very close. DNA's statement (actor, concept, agreement) is our holding, its frames are our families, and its signed "subtract" network resembles our signed matrix. We differ in machine reading, an unusually broad scope, layers, and damping. DNA gives us normalisation logic, a warning about activity bias, and a useful choice between "discourse" and "advocacy" coalition structure.

### Cited Findings
- A statement combines actor, concept and agreement, plus optional variables; this definition can be adapted — [Leifeld 2017](https://eprints.gla.ac.uk/121525/1/121525.pdf).
- Actors linked through shared concepts yield congruence networks; concepts linked through shared actors yield frames, defined as a congruent set of concepts — same source.
- Without normalisation, active or institutionally central actors tie to almost everyone and a core-periphery pattern hides coalitions. Fixes: divide by average concept count, Jaccard, cosine. Vector profiles can feed hierarchical clustering or non-metric scaling, an alternative to community detection — same source.
- The subtract method removes conflict weights from congruence weights, because a congruence-only network can wrongly show one coalition. It also removes institutional bias if positive and negative use are balanced — same source.
- Advocacy coalitions cover multiple issues and stances; discourse coalitions cover one issue and several justifications. Coding arguments on one issue produces two coalitions "by design", while coding across instruments yields many coalitions with different foci — same source.
- Hajer's storylines and discourse coalitions lack clear operational guidance, a gap DNA fills — [hydrogen discourse study](https://arxiv.org/pdf/2311.11421).
- **ACF.** Deep core, policy core and secondary beliefs differ in breadth and resistance to change — [IPPA teaching resource](https://www.ippapublicpolicy.org/teaching-ressource/the-advocacy-coalition-framework/7). Coalitions require shared policy core beliefs plus nontrivial coordination — [Weible and Nohrstedt](https://is.muni.cz/el/fss/podzim2021/MEBn4001/um/povinna_literatura/Weible_Nohrstedt_2012.txt). Deep core beliefs have been called theoretically underspecified — [Ripberger et al.](https://zendy.io/title/10.1111/psj.12074) (snippet).
- **LLM-assisted DNA.** On German actor-claim data, a traditional pipeline beat LLMs on actor identification and a hybrid did best; LLMs often get the right actor with a wrong canonical name — [Barić et al., CODI 2024](https://arxiv.org/pdf/2402.00620). A 2025 study classified actors, stances and claims in 850 submissions and reports — [AoIR listing](https://snurb.info/node/3526).
- **Epistemic communities.** Professionals with recognised expertise and shared normative and causal beliefs — [overview](https://en.wikipedia.org/wiki/Epistemic_community). Co-citation has been used to identify them — [NASKO study](https://journals.lib.washington.edu/index.php/nasko/article/view/15235/12693).
- **Science of science.** Three text-based paradigmaticness metrics, including consensus — [Evans, Gomez and McFarland 2016](https://typeset.io/pdf/measuring-paradigmaticness-of-disciplines-using-text-4zscdq9f7u.pdf). Cue-phrase detection found disagreement in about .31% of citation sentences across over 4 million articles, with precision prioritised and false positives where "conflict" names a topic — [Lamers et al., eLife 2021](https://elifesciences.org/articles/72737). Large teams develop and small teams disrupt, over 65 million works — [Wu, Wang and Evans](https://arxiv.org/abs/1709.02445v2).

### Inferences
Direct comparison:

| Element | DNA | Our method | Which is better for us |
|---|---|---|---|
| Unit | Coded statement | Quote-anchored claim | Ours (anchor checked in code) |
| Coder | Humans under a codebook | Two blind readers | DNA for reliability; ours for scale |
| Concepts | Closed list, one debate | 360 open ideas across all topics | Ours for scope; DNA for comparability |
| Content clusters | Frames from co-use by actors | Families from embeddings and links | Test both |
| Polarity | Concept × agreement as separate columns, or subtract | One signed column | Ours is compact, but mixed holders cancel to zero, the same as silence |
| Similarity | Cosine or Jaccard, plus average-activity normalisation | Cosine after damping and centring | Keep; try DNA's as a comparator |
| Grouping | Community detection, or hierarchical clustering | Average linkage | Same family; add signed community detection |
| Conflict | Subtract network | Implicit in negative cells | Add an explicit conflict matrix |
| Time | Sliding slices | Not yet | Adopt once corpus grows |
| Layers | None | Five | Ours |

Specific actions:
1. Run the subtract network as a direct alternative on the same holdings. It is cheap, and a mature method beating ours would be important to know.
2. Check activity bias: correlate each person's number of holdings with their centrality. If prolific thinkers sit in the middle, that is Leifeld's artefact.
3. Separate zero from cancellation. Store a person's accept and reject counts per family so "mixed" and "silent" stop being the same cell.
4. Leifeld's by-design warning applies to us. Our structure lets many coalitions appear, which suits a map, but families built from attack links can force poles. Keep this in mind when reading any bipolar result.
5. Our "schools" are shared-belief groups. ACF also requires coordination, so call them schools, not coalitions, unless appearance or citation evidence shows real coordination. Our person-by-episode graph could provide this as a second layer.
6. ACF's tiers map onto our layers roughly (deep core to ontological and epistemic; secondary to empirical and praxis). The predicted stability ordering is testable once we have repeated works: do root-layer holdings change less than praxis ones?
7. Co-citation between thinkers (who cites whom as authority) is an independent validation signal, separate from what they claim. Lamers' cue-phrase false positives are a caution on detecting citation of opponents.

**Fit:** DNA High. ACF Medium (concepts yes, coordination data no). Epistemic-community and co-citation methods Medium, as external validation. Paradigmaticness Medium as a per-school consensus statistic. Disruption metrics None.

### Gaps
- "Noy's Field Theory" could not be identified. Search returned unrelated work, so the reference needs a fuller citation from Benjamin.
- "Evans' disagreement": I found no Evans paper specifically on disagreement. Paradigmaticness and Lamers et al. are the nearest. The brief may mean another paper.
- Leifeld's newer tools, such as polarization and backbone measures, could not be searched in this session.
- The 2012 Leifeld and Haunss article was seen only through citations.
- No peer-reviewed 2025 benchmark of full LLM DNA coding was found.

## Who else computes Habermas: are there measures of colonisation, public sphere quality and mediated deliberation?

### Takeaway
Deliberative quality is being automated in earnest, through the Discourse Quality Index. I found no working computational measure of lifeworld colonisation, so anything we build there is new and unvalidated.

### Cited Findings
- LLMs guided by prompt engineering were found viable for scaling the Discourse Quality Index on parliamentary debate — [Bosley, JPIPE](https://www.emerald.com/jpipe/article/6/3-4/355/1333222/Towards-Qualitative-Measurement-at-Scale-A-Prompt).
- AQuA scores comments with adapter models on deliberation facets plus non-expert judgments, noting the DQI (Steenbergen 2003; Bächtiger 2022) as a prominent measure — [arXiv 2404.02761](https://arxiv.org/pdf/2404.02761.pdf).
- LLM contribution ratings on justification, novelty and expansion were validated against eight human annotators and used to evaluate nudges — [arXiv 2408.11936](https://arxiv.org/html/2408.11936v1).
- The DQI needs trained coders, so most studies stay at a few thousand speeches — [TU Delft thesis, 2026](https://repository.tudelft.nl/record/uuid:c7c102d2-b3e5-447a-9d05-684bffba0751) (bachelor thesis, preliminary).
- LLMs reportedly capture complex deliberative dimensions in social media despite class imbalance — [Media and Communication](https://www.cogitatiopress.com/mediaandcommunication/article/view/12494) (snippet).
- Colonisation remains theory-level, for example arguing that fragmentation results from system logics — [Habermas Architecture essay](https://development.everhem.com/habermas-architecture-communicative-rationality-structural-decay-public), weak source; algorithmic curation applied as colonisation — [Algorithmic culture and the colonization of life-worlds, PhilArchive](https://dc2.philarchive.org/rec/GILACA-7) (snippet). "Systematically distorted communication" is proposed as a way to reconstruct the public sphere — [HU Berlin](https://edoc.hu-berlin.de/18452/29641).
- A Hungarian project combined NLP and qualitative analysis to study public discourse — [RC2S2](https://rc2s2.elte.hu/en/project/).

### Inferences
- **DQI fit for MEET: High.** It applies to dialogue, notes and steelmen rather than to thinkers' books. It is a natural supporting input for MOVE, but not a replacement for holder ratification.
- **DQI fit for SEE: Low.** It rates exchanges, not placements.
- A possible colonisation indicator: classify each idea's justification as appealing to money, administrative power, or shared understanding, and track the share over time. The layers and Benjamin's Habermas interest make this attractive. It would be new and should be presented as an experimental lens, not a finding, and never used to rank clusters (B1's warning on hierarchy).

### Gaps
- Gerhards and Neidhardt, Ferree et al. *Shaping Abortion Discourse*, and Wessler's mediated deliberation were not returned by search. I know these works only from memory, so no claims are made here. Their relevance should be checked before citing them.
- Bosley's reliability figures were not retrieved.
- I found no computational measure of colonisation. That is a limit of about two searches, not proof that none exists.

## Validity: how can worldview clusters be validated when no ground truth exists?

### Takeaway
No single test works, so use several independent ones and require them to agree. For us, held-out stance prediction and split-half stability across a person's works are the strongest tests available without any new people. Self-identification and holder ratification remain the true test, but that needs outreach, which Benjamin must approve. Silhouette against curated niches should drop to a secondary check.

### Cited Findings
- Validation must be built for each problem, with or without gold data — [Grimmer and Stewart](https://is.muni.cz/el/fss/podzim2017/MEB421/um/Grimmer_Stewart_2013.txt?lang=en); [Text as Data book](https://press.princeton.edu/index%2Ephp/node/50738).
- Hennig's bootstrap computes Jaccard similarity per cluster. A mean of about .75 or more suggests stability, .6 to .75 suggests patterns with doubtful membership, below .6 should not be trusted, and .5 or less marks dissolution. Stability alone is not validity, since inflexible methods can be stable — [clusterboot docs](https://search.r-project.org/CRAN/refmans/fpc/html/clusterboot.html).
- Krippendorff's alpha handles any number of coders and missing data, since only values from two or more coders enter. Common guides are .800 reliable, .667 to .800 tentative, and the minimum should rise with the cost of error — [overview](https://en.wikipedia.org/wiki/Krippendorff%27s_alpha).
- Multiverse steps: list decisions, identify legitimate alternatives, filter or sample combinations, run all and report failures. Classify decisions as equivalent, non-equivalent or uncertain, and avoid "flooding the zone" with weak specifications — [arXiv 2605.19745](https://arxiv.org/html/2605.19745). Its text and LLM case found effects mostly stable, some LLM failures, and a simple SVM comparable to deep models. It does not cover clustering — same source. Origins: [Steegen et al. via overview](https://en.wikipedia.org/wiki/Multiverse_analysis).
- Community Notes-style leave-topics-out transfer and known-group anchors are established templates in our own research — [B4](/Users/benjaminlife/dev/schismogenesis/docs/research/B4-mapping-science.md).
- Even human "ground truth" on stance is unstable; agreement averaged .55 — [Walker and Angst](https://pmc.ncbi.nlm.nih.gov/articles/PMC12629487).
- Holder ratification and the cross-cluster Turing test are the project's normative standard — [B1](/Users/benjaminlife/dev/schismogenesis/docs/research/B1-lineages.md).

### Inferences
Recommended validation ladder:

| Test | What it shows | Needs | Available now? |
|---|---|---|---|
| Hold out 20% of holdings; predict stance from school or nearest neighbours; compare with family-majority and plain-embedding baselines | The map has predictive content, not just topic | Holdings; more with a battery | Yes |
| Leave-one-family-out | Structure transfers to new topics | Same | Yes |
| Test-retest: split each person's works in half, build two maps, compare placement | Placement reflects the person, not the sample of works | At least two works per person | Yes, at about 3.4 works each, weakly |
| Hennig per-school Jaccard, alongside existing pair stability | Which schools are real | Existing code | Yes |
| Multiverse over families (20 to 80), damping, centring, linkage, schools, reader rules, and silhouette or prediction outcome | How much choices drive results | Compute only | Yes |
| Human coders on a random sample, alpha reported | Reader quality | 100 to 300 items (my estimate) | Needs a person |
| Co-citation, co-appearance as external criteria | Independent signal | Discovery-crawl data | Partly |
| Expert sorting of thinkers, blind | Agreement with informed outsiders | 3 to 5 experts | Needs outreach, ask Benjamin |
| Self-identification and holder ratification | The actual standard | Thinkers or their followers | Needs outreach, ask Benjamin |

Notes on the existing result:
- +0.09 against -0.04 is a difference of 0.13 on 27 points, with no interval reported. It should get a bootstrap interval before anyone leans on it.
- Silhouette against curated niches rewards agreeing with curators. If the curation is wrong, a better map scores worse. It is also a low value in absolute terms, which suggests weak separation or that the niche labels are a poor target.
- Nine schools over 27 people means about three each. A single person changing school moves a lot of the metric. The ADR flags nine as the top of the tested range, so a low-end count should be reported too, and a person should be allowed to be "between schools".
- `school_stability` resamples families. That tests dependence on which ideas are present, which is useful. It does not test dependence on which works were read, so add work-level resampling.
- Use tests with independent error. Two model readers, stance-aware embeddings and LLM imputation share model biases. Human coding, citations and appearances do not.

### Gaps
- I could not retrieve a source on silhouette thresholds or small-sample silhouette behaviour, so the "low value" remark is my judgment.
- No published standard exists, as far as I found, for validating worldview clusters of public thinkers from long-form text. Sample sizes for human coding above are my estimates.
- No multiverse study of text clustering was found; the cited one explicitly leaves out clustering.
- Chapel Hill-style expert surveys for non-partisan intellectual positions were not searched.
- Sources not read in full: several preprints above, as marked. PDFs for Boutyline 2017, Leifeld 2017, Ghafouri 2024 and Cuerno et al. were read as extracted text by keyword and section, not cover to cover.
