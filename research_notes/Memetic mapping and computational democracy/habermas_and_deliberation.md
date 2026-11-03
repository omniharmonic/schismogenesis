# The Habermas Machine and AI-mediated deliberation, as of November 2026

Evidence tags used below: **[PR]** peer-reviewed; **[PP]** preprint, thesis or working paper; **[ESSAY]** non-empirical essay; **[VENDOR]** claim by the tool's maker, unaudited; **[TALK]** author's statement in a recorded talk.
Depth tags: **(full)** I read the document; **(abstract)** I saw only an abstract, a search snippet or a summary of the page, so check it before quoting.

Corrections to the repo's existing docs that come out of this work:
- `docs/research/B2-computational-democracy.md` line 169 says no public code was found, and `BIBLIOGRAPHY.md` line 145 says the same. **Both are out of date.** The code and data are public, though the fine-tuned models are not (see Q1).
- `habermasmachine.ai` is an Oxford research tool, not a DeepMind product (see Q1).
- B2 dates the team's perspective piece to January 2026. It first appeared as a Knight Institute essay on 1 August 2025 (see Q3).

## Q1. What exactly did Tessler et al. (Science 2024) do, and what is habermasmachine.ai?

### Takeaway
The Habermas Machine is two fine-tuned language models plus a Schulze election, run as private "caucus mediation" in groups of about five. It is well validated for one claim: people prefer and endorse its statements, and groups end up less divided. It was never measured on whether people understood each other, and the convergence it reports is largely what Dialogos Arena does not want as a success metric.

### Cited Findings
Source note: science.org returned 403 to my fetch, so all of this comes from a full-text mirror of the published article, not the supplement. **[PR] (full)**: [Science full-text mirror](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf); [official DOI](https://www.science.org/doi/10.1126/science.adq2852).

**Architecture**
- Generator: Chinchilla 70B, fine-tuned on opinions and critiques from earlier rounds, with target statements rated high quality. The training set covered 578 groups, 2,473 participants and 1,630 questions, with questions clustered into 105 groups by k-means on Universal Sentence Encoder embeddings; 12 topics were held out for out-of-distribution tests. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- Personalized reward model (PRM): a 1.4B Chinchilla with an extra linear layer for a scalar reward. Rankings become pairwise preferences fitted with Bradley-Terry, plus an auxiliary classification loss on binarized quality ratings. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- Selection: 16 candidates are generated. The PRM predicts each person's ranking *from that person's opinion and critique*, and the Schulze method picks the winner. It was chosen for "independence of clones", so near-duplicate statements do not split the vote. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- Discrepancy: both talks say about 30 or 32 candidates, while the paper says 16. — [IASEAI talk](https://youtu.be/T77ggzXvX1Y); [Burnes talk](https://www.youtube.com/live/-cCguFRH7f4)

**Protocol**
- Up to five people took three questions in about an hour, each round about 15 minutes. Steps: write a private opinion (5 minutes, 10–200 words, mean 65) → rate and rank candidates → critique the winner privately → rate and rank revised statements → choose between initial and revised → end-of-round survey. Participants never saw each other directly and knew an algorithm wrote the statements. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- Questions: Chinchilla generated 10,000 from 175 seed questions; about 5,500 survived vetting for safety and divisiveness. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- Primary analyses were preregistered at osf.io/uy4z3; UK adults only; mostly convenience sampled from a crowdsourcing platform; approved by an internal ethics committee. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)

**Results (N = 5,734 overall)**
| Test | Sample | Result |
|---|---|---|
| AI vs human mediator | 75 six-person groups, n = 439 | Preferred 56% vs 44% (modelled P̂ = 0.575, CI 0.535–0.614). Endorsement OR 1.36 (b = 0.31, SE 0.07); quality OR 1.54 (b = 0.43, SE 0.08) |
| Length confound | same | HM 125.9 words vs human 105. Rankings, endorsement and quality were all affected by length; endorsement still favoured the HM after controlling for it |
| External judges | n = 155 | Clearer and more informative (b = 0.449), less illogical (b = −0.26), better at the majority view (b = 0.225), less reflective of the writer (b = −0.226). **No significant difference** on fair summary, including the minority view, or being polarizing |
| Revised over initial | Cohorts 1–3, n = 1,692, 349 groups, 1,047 rounds | Preferred 68%, 64%, 66% |
| Effort-justification control | Cohort 4, n = 245, 50 groups | Critique-using statements still won (b = 0.34, SE 0.12, after controlling for length) |
| Group agreement change | Cohorts 1–3 | b = 0.086, 0.093, 0.059, about 8 points. Unanimous groups 22.8% → 38.6% (cohort 1) |
| Unmediated opinion exposure | n = 372, 75 groups | No change (b = −0.005, P = 0.64); exposure-type interaction b = −0.038, P = 0.0058 |
| Self-report | end-of-round surveys | "Closer to the group opinion" 30.1% of rounds; no change 60.3%; other 4.6%. Best expression of own view was the final group opinion in 66.6% vs own original 33.3% |

All from [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf).

**"Group agreement" is the percentage-point gap between sides.** 80/20 scores 60; a 50/50 split scores 0; 3v2 in a group of five scores 20. It is defined by people's side on a seven-point position question, so it measures convergence on positions and nothing else. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf); [IASEAI talk](https://youtu.be/T77ggzXvX1Y)

**Minority findings**
- Method: opinions and statements are embedded with Sentence-T5 (768 dimensions), projected on a line from the negating to the affirming statement for each question, and regressed as convex combinations of the group's opinions. Position score correlated with stated position at r = 0.64 (r² = 0.41). — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- 96% of group statements sat within the range of individual opinions. Initial statements weighted the minority at its true share (0.29). Revised statements raised this to 0.36 (SE 0.03). — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- But movement was asymmetric: the majority grew in 29–32% of rounds and the minority in 20–26%. Majority-aligned ratings rose (cohort 1 b = 0.52). The paper's own phrase is that views were "more likely overall to shift toward a majority view". — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- No link between exposure to majority-leaning statements and shift toward the majority (b = 0.058, P = 0.37). — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)

**Virtual citizens' assembly (n = 200)**
- Stratified random sample by the Sortition Foundation, three weekly one-hour sessions in April–May 2023, same nine questions for all, no fact-finding or expert testimony phase. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- Exploratory convergent shifts on five of nine: reduce prison numbers 60→75%; easier asylum 39→51%; national pride 42→57%; minimum wage 77→85%; net zero 75→80%. Brexit: no change. Childcare from birth moved the other way (opposition 33→41%, not significant). — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)

**The caveat that changes the reading**
- An exploratory analysis found similar convergence with the human mediator on rounds where the human beat the HM, "suggesting that convergence may result from the caucus mediation process per se rather than from distinct properties of the AI mediator." — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)

**Stated limits**
- UK only. No fact-checking, topic control or moderation; ill-informed input can give ill-informed output. Tested only up to five people, though "in theory" scalable. Loses nonverbal cues and relationship-building. Should sit inside a larger process. People may endorse because a process seems fair ("settled disagreement"), and "a plurality of views may persist." — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- A prompted Gemini 1.5 Pro did worse than the small fine-tuned model, so preference data beats raw model size for this task. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- The authors say explicitly that human mediators were incentivized but nonprofessional. B2 calls them "trained human mediators"; that should not be read as professional. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)

**Code and data**
- `google-deepmind/habermas_machine`: about 450 MB of Parquet data, analysis code, questions, and a package that is prompted, not fine-tuned, using Gemini via AI Studio. Apache-2.0 for code, CC-BY 4.0 for other materials. No model weights and no Chinchilla mention on the page. — [GitHub](https://github.com/google-deepmind/habermas_machine)

**habermasmachine.ai**
- A live hosted tool: hosts create a deliberation, participants join by code, and the phases are Opinion → Synthesis → Rating → Critique → Final Consensus. It says it was developed by University of Oxford researchers with the Oxford Research Software Engineering Group, linking the HIP Lab. No papers, data, code, dates or evaluation on the page. — [habermasmachine.ai](https://habermasmachine.ai/) (full)

### Inferences
- The paper's "minority weight" is a position on one embedding axis. It shows the text leans toward minority stances; it does not show minority members would sign it as a description of them. These are different quantities.
- The control is a separate recruited cohort as far as the main text says, so I would not assume random assignment between mediation and opinion exposure. Check the supplement.
- The reward model is the part most worth borrowing, and the least reproducible, because its weights are not public and the public package is prompted only.

### Gaps
- I did not read the supplement (84 figures, 55 tables), so no per-person minority endorsement data, and no PRM accuracy numbers.
- The main text's subtotals do not reconcile to 5,734: training n = 2,473 plus evaluation n = 2,673 gives 5,146. Dates also differ: the paper says January–August 2023; the IASEAI talk says April–October 2023.
- A tension in the paper itself: the structured summary says external judges rated statements higher on "perceived fairness", and the main text reports no significant difference on "fair summary". Possibly different items; unresolved without SM 4.3.7.

## Q2. What are the four videos, and what do they add?

### Takeaway
Two are directly relevant talks by the authors, and I read both from captions. They add candour the paper lacks: "minimally deliberative", shifts of under one person per group, and "clarifying disagreement" as an alternative output. **The other two are short Blackbird.AI marketing clips with no connection to the Habermas Machine**; they look like they belong to a different research question.

### Cited Findings
| URL | Title (oEmbed) | Channel | Date, length | Read? |
|---|---|---|---|---|
| [T77ggzXvX1Y](https://youtu.be/T77ggzXvX1Y) | AI Can Help Humans Find Common Ground in Democratic Deliberation – MH Tessler, IASEAI 2025 | IASEAI | posted 2025-08-12, about 34 min | Description and full captions |
| [-cCguFRH7f4](https://www.youtube.com/live/-cCguFRH7f4) | The Peacemaking Machine with MIT and DeepMind's Tessler and Bakker | Burnes Center | posted 2025-02-28, about 66 min | Description and full captions |
| [8Wixy4aIY9Q](https://youtu.be/8Wixy4aIY9Q) | See How Narrative Intelligence Maps Online Geopolitical Conflict | Blackbird AI | 93 s | Description and captions |
| [5916QROWNZE](https://youtu.be/5916QROWNZE) | How Narrative Attacks Threaten Financial Services | Blackbird AI | 87 s | Description and captions |

Captions are automatic and noisy, so short phrases below may contain errors. No transcripts are kept here. Titles come from [YouTube oEmbed](https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=T77ggzXvX1Y&format=json).

**Burnes Center, 27 Feb 2025 [TALK]** ([video](https://www.youtube.com/live/-cCguFRH7f4); [event write-up](https://rebootdemocracy.ai/blog/habermas-machine-%20workshop))
- Tessler calls the setup "minimally deliberative", conceding text-only exchange loses emotion and bonding, and that hybrids are the attractive route.
- The speakers say average belief change is small, "sub one person" per group, and many rounds do not change at all. Brexit is called a calcified question, and each round is only about 15–20 minutes, so they do not claim it would depolarize strong opinions.
- Jose Luis Marti (Pompeu Fabra) put the central objection: common ground may be found, but "not through deliberation", via aggregation rather than new agreement based on reasons.
- Costas Panagopoulos raised non-attitudes (are the inputs just expressive?) and whether any of this transfers to polarized US politics. The speakers answered the first with the result that opinions text predicts stance; the second was called the harder question and not answered with data.
- Bakker on equity: the PRM may rank non-native English speakers less accurately, giving some groups "less influence". The critique step is offered as partial protection.
- Tessler: "common ground" can also mean "we all agree that we cannot agree on" X, Y and Z, so clarifying disagreement is a valid objective. **This is the closest the authors come to Dialogos's aim.**
- On group polarization (the Sunstein objection): embeddings show statements getting less extreme, but "there's nothing in the mechanism" that enforces this. A group of extremists would find extreme common ground; the model had no guard rails.
- Named follow-ups: University of Washington and X Community Notes; Alliance for Middle East Peace with Remesh; Polis/CompDem. Ideas floated: an AI representing "the missing perspective", or mediators sharing information between small groups. The latter was labelled speculative.

**IASEAI 2025 [TALK]** ([video](https://youtu.be/T77ggzXvX1Y))
- Human mediators took about 8 minutes per statement; the HM takes seconds. Each protocol pass took about 20 minutes per question.
- Five-person groups were chosen partly because of 2022 context-window limits, and because the group is the statistical unit. Tessler says thousands of inputs are possible but it would be "very difficult to evaluate" the outputs.
- He frames the result as "just as good as humans are, perhaps a little bit better", not superhuman.
- He says the open-source prompted version gives flexibility, for example outputs that explicitly highlight what people agree and disagree on.
- An audience member pressed the claim about collective action: text agreement is not an action outcome. Tessler answered that agreed text is itself the output in laws, platforms and similar.
- Also framed as pluralistic alignment for AI safety. — [video description](https://youtu.be/T77ggzXvX1Y)

**Blackbird.AI clips [VENDOR]**
- Geopolitical clip: Constellation network graphs of authors, hashtags and URLs; a "cohort model" marks authors aligned with adversary propaganda, in an example about nuclear hypocrisy narratives. — [video](https://youtu.be/8Wixy4aIY9Q)
- Finance clip: the same graph method on "bank run" mentions during the Silicon Valley Bank collapse, marketed as early warning. The description pitches CFOs and says a company's market value drops about 30% after a major reputational crisis, attributed to the World Economic Forum. — [video](https://youtu.be/5916QROWNZE)
- Neither clip includes any validation.

### Inferences
- Blackbird matters to this project only as a contrast. It maps narratives to label and counter "adversary" clusters, while SEE maps clusters so they can be described fairly. The same graph technique can serve either, so this is a reputational risk to name in Dialogos's own positioning.
- Tessler's "agree that we cannot agree" remark suggests the Habermas architecture could target a description of disagreement rather than a shared stance. Neither talk reports a test of this.

### Gaps
- I did not independently verify the WEF 30% figure, and it comes only from vendor copy, so do not reuse it.
- I could not determine why the Blackbird videos were grouped with these; nothing in them mentions deliberation.

## Q3. What is the follow-up work and critique?

### Takeaway
There is still no independent replication and no published field deployment that I could find. The serious critique is that the machine produces acceptable text, and its validation cannot tell that apart from people reasoning together. Separate evidence shows LLM summaries under-represent minority opinions, and the team itself says the same risk remains open.

### Cited Findings
**The team's own follow-ups**
- Perspective essay "Can AI Mediation Improve Democratic Deliberation?" reports no new experiments, and calls evidence on engagement effects "limited at the moment". Published by the Knight Institute 1 Aug 2025, later [arXiv 2601.05904](https://arxiv.org/pdf/2601.05904). **[ESSAY]** — [Knight Institute](https://knightcolumbia.org/content/can-ai-mediation-improve-democratic-deliberation)
- Essay's definition: "common ground" is propositions accepted for the purposes of conversation "without necessarily holding them as deep personal beliefs". Forms range from "We believe ABC" to "The group agrees on X, but disagrees on Y". It says AI's role is "not to collapse opinions into a forced perspective or to manipulate participants into agreement." — [arXiv 2601.05904](https://arxiv.org/pdf/2601.05904) (full)
- It treats fairness in three layers: aggregation, ranking (the PRM should be equally accurate for everyone), and generation. It concedes strategic misrepresentation and repeated-play gaming are unresolved. — [arXiv 2601.05904](https://arxiv.org/pdf/2601.05904) (full)
- **Supernotes** (De, Bakker, Baxter, Saveski; WWW '25) **[PR] (abstract)**: an LLM drafts candidates and a scoring model trained on Community Notes ratings ranks them. In a study on 100 posts, participants rated them above the best existing notes. They beat plain LLM summaries as more helpful 61.5% of the time. The authors note that 91% of posts with a proposed note never get enough diverse support. — [arXiv 2411.06116](https://arxiv.org/html/2411.06116v1)
- **Peacebuilders** (Konya et al., FAccT 2025) **[PR] (abstract)**: about 138 Israeli and Palestinian civil-society peacebuilders across four cycles, April–July 2024. Three separate-group cycles, then joint; bridging-based ranking found statements, an LLM wrote collective statements, and experts reviewed them. Result: five statements to world leaders and five to residents, each with at least 84% support. It is a case study, not an experiment, and it used separated identity groups. — [arXiv 2503.01769](https://arxiv.org/abs/2503.01769)
- **Bias testing with a co-author from the team**: Zhu, Yang, Bakker, Pentland, Pei, **[PP] (full, first 100k characters)**. DeliberationBank: 3,000 opinions on 10 questions and 4,500 human annotations; 18 LLMs benchmarked. All models scored minority opinions lower. Automatically detected minority gap averaged about 0.036, roughly 34.4× a random-sampling control of about 0.001; a self-reported minority gap reached 0.08 on tariffs. No mitigation tested. The "34×" is a ratio to a tiny control, so 0.036 on a 0–1 scale is the number to keep. — [arXiv 2510.05154](https://arxiv.org/html/2510.05154v5)

**Does it produce convergence or understanding?**
- Flechtner, "The Deliberative Deficit" (Aug 2026, sole author, **[PP]**, and much of it synthesizes his own unpublished benchmark): the HM's validation "cannot tell whether participants engaged with diverging opinions and reasoned their way to common ground or whether the LLM found a framing acceptable enough to all." He says the result is not wrong but "underdetermined", and proposes DRI-type evaluation. — [arXiv 2608.10186](https://arxiv.org/pdf/2608.10186) (key sections read)
- His data, LLM-only groups (1,980 five-agent runs, 12 assembly topics, 11 model configurations): process score AQuA 2.939 vs Europolis humans 2.980, not significant. ΔDRI about 0.029 vs human about 0.099, and it turns negative on contested topics. Perspective diversity about 6.5 vs human 18.8. Dispersion rises through interaction, where it falls in humans. — [arXiv 2608.10186](https://arxiv.org/pdf/2608.10186)
- Kreia Umbelino & Veri 2025, as reported there: 54 LLMs vs 526 human post-deliberation responses across 24 cases; mean 0.18 vs 0.34; humans ahead in 19 of 24 cases. — [arXiv 2608.10186](https://arxiv.org/pdf/2608.10186) (secondary)
- Persona prompting raised diversity but only moved considerations (d = 0.55), not preferences, so it did not restore the human pattern. — [arXiv 2608.10186](https://arxiv.org/pdf/2608.10186)
- The paper itself allows that people may endorse a statement as the outcome of a fair process rather than because it matches their view ("settled disagreement"), and its main text reports no measure of mutual understanding. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)

**Does it erase minority views?**
- The paper's answer is no on text weighting, but with net drift toward majorities. — [Science](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- The team flags that algorithmic bias and opaque ranking could hide marginalization. — [Reboot Democracy write-up](https://rebootdemocracy.ai/blog/habermas-machine-%20workshop)
- General LLM summarization under-represents minority stances, per Zhu et al. above. — [arXiv 2510.05154](https://arxiv.org/html/2510.05154v5)
- One 2026 multi-agent preprint is titled "Emergence of Biased Consensus in Multi-Agent LLM Debates". I saw the title only. — [arXiv 2608.02827](https://arxiv.org/pdf/2608.02827)

**Does a summary replace deliberation?**
- Oleart & Palomo, *Journal of Deliberative Democracy*, Dec 2025 **[PR]**: participants only rank machine statements; the HM "leaves aside human-to-human argumentative and reason-based interaction"; they call it "deliberation without citizens". — [JDD](https://delibdemjournal.org/article/id/1839/)
- Palomo Hernández 2025, AAAI/ACM AIES **[PR] (abstract)**: optimization targets, training data and aggregation methods encode a view of what deliberation is for. Reference given in [arXiv 2608.10186](https://arxiv.org/pdf/2608.10186).
- Sætra in CACM is already covered in B2; I did not revisit it.
- GroupEnvoy (2026) **[PP] (abstract)**: with an agent speaking for the outgroup, a reported pattern was delegating perspective-taking effort to the agent. — [arXiv 2604.16095](https://arxiv.org/pdf/2604.16095)
- A PNAS Nexus study reported by Yale, March 2026 **(abstract)**: chatbot summaries not intended to persuade still shift opinions. It used historical events, not deliberation. — [Yale News](https://news.yale.edu/2026/03/03/ais-hidden-bias-chatbots-can-influence-opinions-without-trying)

**Is it Habermasian at all?**
- Oleart & Palomo: for Habermas, consensus is "a precondition for the kind of discourse", not the goal. With "no discursive or argumentative interaction between participants at all", any shift comes from an algorithm's estimate of acceptability. — [JDD](https://delibdemjournal.org/article/id/1839/)
- Volpe 2025, "Toward an artificial deliberation?": consensus optimization may conflict with deliberation as communicative autonomy. I could read this only secondhand. — [arXiv 2605.26940](https://arxiv.org/pdf/2605.26940); [PhilPapers record](https://philpapers.org/rec/VOLTAA-2)
- Schismenos, "Habermas as a thinker against Google's 'Habermas Machine'" **[PP]**. Title only; SSRN returned 403. — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6426018)
- The authors themselves concede only "minimally deliberative". — [Burnes talk](https://www.youtube.com/live/-cCguFRH7f4)

### Inferences
- The strongest empirical critique is about LLM-only groups, so it does not directly test a human-plus-mediator system. Flechtner's extension to the HM is an argument, not a finding.
- Combining the caucus caveat in Q1 with the critics: what the evidence supports is a claim about *the private-input-then-shared-draft format*, rather than about AI as such.
- Process scores are now close to useless as a sign of quality, because LLMs can match humans on them with little reasoning gain.

### Gaps
- I found no independent replication of the HM, and no peer-reviewed study of it that adds DRI, mutual understanding or attitudes toward other participants.
- A search summary claimed the same 5,734-person study showed lower willingness to join AI-facilitated deliberation. I could not trace this and it does not match the paper, so treat it as an error.
- A [Designing Open Democracy post](https://www.designingopendemocracy.com/blog/2026/08/16/the-habermas-machine-an-ai-mediator-that-beat-humans-at-finding-common-ground/) refers to a team "follow-up". From the snippet this looks like the Knight essay, but I did not confirm it.

## Q4. Who else does this, and what is new since 2024?

### Takeaway
Tools are plentiful and open source, but the outcome evidence is thin and often null: several 2026 experiments found LLM facilitators change the experience more than the result. Nobody in this set scores whether a described group accepts its description. B2 covers most of these; below I add only what is new.

### Cited Findings
**Controlled tests of LLM facilitation (mostly null on outcomes)**
- "Bringing Everyone to the Table", ACM PACMHCI, Sept 2026 **[PR] (abstract)**: preregistered, 281 groups, four conditions, GPT-4o. More distinct facts surfaced; no effect on final decision accuracy from human or AI facilitation; the LLM was rated more distracting than the human. — [ACM](https://dl.acm.org/doi/10.1145/3816907)
- DeliberationBench, IASEAI '26 **[PR status unverified] (abstract)**: preregistered, 4,088 US adults chatting with LLMs on AI policy; polarization did not fall. — [arXiv 2603.10018](https://arxiv.org/pdf/2603.10018)
- Charity allocation **[PP] (abstract)**: two experiments, 879 people, on Deliberate Lab; no significant change in consensus, but people preferred the facilitated process. — [arXiv 2605.14097](https://arxiv.org/html/2605.14097v1)

**Platforms**
- **Jigsaw Sensemaker** / `sensemaking-tools`: Apache-2.0, Gemini by default, with options for Gemma. Finds topics and opinion groups, extracts quotes, scores constructive quality, generates and ranks propositions by simulated jury, and builds a report. README: **"not actively maintained"**, with no benchmark results. **[VENDOR]** — [GitHub](https://github.com/Jigsaw-Code/sensemaking-tools)
- Bowling Green, Kentucky ("What Could BG Be"): 7,890 residents, 1,034,868 interactions, 33 days, AI-categorized and AI-summarized. **[VENDOR] (abstract)** — [project report](https://polygraph-cool.github.io/m2-report); [BG Daily News](https://bgdailynews.com/?p=681840)
- **Deliberate Lab** (Google, PAIR): open-source, no-code real-time human-AI experiments; LLMs can act as participants, moderators or simulated crowds. One-year deployment: 88 experimenters, 9,195 participants. **[PP] (abstract)** — [arXiv 2510.13011](https://arxiv.org/html/2510.13011)
- **Deliberation.io**: Stanford, UC Berkeley and MIT authors including Lily Tsai and Alex Pentland. MIT license. Modular formats, AI Socratic dialogue, and a "Face of Crowd" view showing how answers compare. States that AI "augments rather than replaces human judgment". The paper is a system description. **[PP]** — [system paper](https://digitaleconomy.stanford.edu/app/uploads/2025/12/deliberation_io_system_paper.pdf). Not the same project as Deliberate Lab. — [Civic Tech Field Guide](https://directory.civictech.guide/listing/deliberationio)
- **Stanford Online Deliberation Platform**: small video groups, "AI-assisted" because the group makes key calls. Reported at close to 50,000 participants by Dec 2024, and at over 40,000 hours in 35+ countries in a later write-up. Participant ratings are reported as high or higher than human-moderated projects. **[VENDOR]** — [Civic Tech Field Guide](https://civictech.guide/projects/stanford-online-deliberation-platform); [Freiheit Taiwan](https://www.freiheit.org/taiwan/better-human-ai-assisted-moderation-sparks-innovative-dialogue-deliberative-democracy); [Cambridge](https://www.cambridge.org/core/product/969F1ECDAE76F682F1E61550DEDD891D/core-reader)
- **Polis with LLMs**: the 2023 Small et al. paper tested Claude for facilitation, moderation and summary, and found context limits strongly affect quality. — [Living Library summary](https://thelivinglib.org/opportunities-and-risks-of-llms-for-scalable-deliberation-with-polis/). Polis 2.0 is in B2.
- **Talk to the City**: its own process card says results are accurate but not precise representations of beliefs, because of LLM error. — [process card](https://docs.google.com/document/d/1LzXa4KY3Iuu-nJDJMfafeC8lWMSVLcgsQ_1nZOc-jJE/export?format=pdf)
- Student-run comparison of Polis, Talk to the City, CrowdSmart and Deliberation.io: Polis strongest for broad listening, weaker for actionable ideas. A small informal test. — [TODA](https://toda.org/policy-briefs-and-resources/policy-briefs/report-255-full-text.html)

**Mechanism work since 2024**
- Generative social choice is listed as Journal of the ACM 2026; the PROSE engine (ICML 2025) writes and assesses statements, with slates reported as fragmented. **(abstract)** — [arXiv 2309.01291](https://arxiv.org/pdf/2309.01291); [ICML](https://icml.cc/virtual/2025/poster/45972)
- "Finding Common Ground in a Sea of Alternatives" (Mar 2026) **[PP] (abstract)**: proportional-veto-core guarantees; LLM generative rules did worse when the LLM was not tuned to the population. — [arXiv 2603.16751](https://arxiv.org/html/2603.16751v1)
- Zaghouani (May 2026) **[PP]**: a design blueprint with clause-level provenance, erasure metrics, contestability workflows and human ratification. Proposal only, no results. — [arXiv 2605.26940](https://arxiv.org/pdf/2605.26940) (abstract and sections)
- CONSIDER (Oxford, May 2026) **[PP]**: one-to-one value clarification through disagreement with a generated opposing opinion, on the Mill argument, not consensus. Prototype with risk analysis. — [arXiv 2605.31574](https://arxiv.org/pdf/2605.31574) (abstract)

**Not updated beyond B2:** Remesh's general product, CIP Global Dialogues, Anthropic Collective Constitutional AI, Harmonica and Frankly. I searched and found no new verifiable evaluation since B2.

### Inferences
- Across the set, the pattern is that LLM help reliably improves satisfaction and information surfacing, and rarely improves outcomes. For Dialogos, this supports scoring outcome signals rather than participant satisfaction.
- The Konya design (separate identity groups, then a joint step) fits a cluster-based product better than five random strangers do.
- Jigsaw's "not actively maintained" note means a hard dependency on Sensemaker is a risk, even though its simulated-jury approach is worth reading.

### Gaps
- No independent audit of Sensemaker summaries, and no evidence on whether people accept summaries instead of reading the comments.
- No published results for Stanford's LLM moderator specifically. No formal LLM evaluation of Polis reports in my sources.
- Several entries are abstract-level only, as tagged.

## Q5. What bears on meta-consensus, and which measures could score "the described side would sign this"?

### Takeaway
The best direct instrument is the **Ideological Turing Test**: it has the described side rate the description, and compares it to that side's own arguments. DRI, Q method and DQI each measure something adjacent, and should be used for diagnostics rather than as the score. Note that the Habermas team's use of "meta-consensus" is not the Dryzek-Niemeyer one.

### Cited Findings
**Definitions (Dryzek & Niemeyer, AJPS 2006, full text)** — [ANU repository](https://openresearch-repository.anu.edu.au/server/api/core/bitstreams/13db0edd-bc9e-45ab-ae40-9194d14bd78a/content)
- Normative: "agreement on recognition of the legitimacy of a value, though not extending to agreement on which of two or more values ought to receive priority in a given decision."
- Epistemic: "agreement on the credibility of disputed beliefs, and on their relevance", where credible means "accepted by others as reasonable to hold the belief in question."
- Preference: agreement "on the nature of disputed choices across alternatives", with two aspects: the acceptable range of alternatives, and the structuring of choices, such as single-peakedness along an agreed dimension.
- It "implies reciprocal understanding and recognition of the legitimacy of the values held by other participants."
- Warning from the abstract: "close attention must be paid to the content of meta-consensus and the conditions of its production or discovery." They also discuss cases where it may be the product of political manipulation.
- Real precedent for a *signed* meta-consensus: a Colorado HIV/AIDS dialogue among gay activists, people with AIDS and fundamentalist Christians produced written agreement that prevention methods "need to be appropriate to that range of moral perspectives", while each side kept finding some agreed measures objectionable.
- Before-and-after evidence: McLean et al. (2000) on an Australian republic deliberative poll found preference meta-consensus unchanged by deliberation, though it was already high.

**The Habermas team uses a different meaning**
- Their essay says "meta-consensus" is where "participants accept an outcome as legitimate due to a fair process, even without full agreement", citing Bächtiger et al. 2018. — [arXiv 2601.05904](https://arxiv.org/pdf/2601.05904)

**Measures in use**
| Measure | How it works | What it captures | Status |
|---|---|---|---|
| **Ideological Turing Test** | Each side writes reasons for and against; the *opposite side* rates them; pass if opponents agree with it at least as much as with proponents' own arguments | Accuracy as judged by those described | [Brand, Brady, Stafford, Cognitive Science 2025](https://api.crossref.org/works/10.1111/cogs.70126) **[PR]**: 200 per side, 3 UK topics, N = 1,200. High mutual understanding found. Passers rated opponents less ignorant, immoral or irrational |
| **DRI** | 20–40 consideration items rated, policy preferences ranked, pre and post. Spearman correlation per pair for considerations and for preferences. DRI = 1 − mean of the absolute gaps between them | Whether people's agreements on reasons match their agreements on preferences | Definition per [arXiv 2608.10186](https://arxiv.org/pdf/2608.10186); applied to 19 forums, rising in most, with group building the strongest factor: [Niemeyer et al., APSR](https://cambridge.org/core/journals/american-political-science-review/article/how-deliberation-happens-enabling-deliberative-reason/6558F69855ADA8B15BF2EC2E5D403E71) **[PR] (abstract)** |
| **Q methodology** | Build the concourse of views → select statements → strategic participants → forced-distribution sort → factor analysis → interpret as viewpoints; often pre/post | Discourses as shared reference points, from each person's own arrangement | [Participedia](https://participedia.net/method/4683); [Niemeyer 2019 chapter](https://researchprofiles.canberra.edu.au/en/publications/understanding-deliberative-citizens-the-application-of-q-methodol/) **(abstract)** |
| **DQI** | Human coding of speech for justification, respect, counterarguments and so on | Quality of talk, not of reasoning | Introduced by Steenbergen et al. 2003, per [arXiv 2608.10186](https://arxiv.org/pdf/2608.10186); original not read. The APSR authors position DRI against it: [Niemeyer et al.](https://cambridge.org/core/journals/american-political-science-review/article/how-deliberation-happens-enabling-deliberative-reason/6558F69855ADA8B15BF2EC2E5D403E71) |
| **AQuA / LLM-DQI** | Automated DQI-style scoring | Same, cheaper | [AQuA](https://ar5iv.labs.arxiv.org/html/2404.02761) **[PP]**; [Bosley 2025](https://www.emerald.com/jpipe/article/6/3-4/355/1333222/Towards-Qualitative-Measurement-at-Scale-A-Prompt) **[PR] (abstract)**. A TU Delft student thesis found LLM ensembles reliable for justification and respect, but only a second coder for counterarguments: [TU Delft](https://repository.tudelft.nl/record/uuid:c7c102d2-b3e5-447a-9d05-684bffba0751) |
| **Max-min / bridging** | Keep statements with support across groups, using the lowest group's support | Cross-group acceptability | [Konya et al.](https://arxiv.org/abs/2503.01769); B2 |

**Evidence that the ITT is usable as an intervention target**
- Gamba, Romero, Schoenebeck **[PP] (abstract)**: 2×2, 203 University of Michigan participants. Debating the opposite view durably reduced outgroup animosity; writing it had a large immediate effect that faded. — [arXiv 2512.12187](https://arxiv.org/pdf/2512.12187)
- Walter et al. working paper **[PP] (abstract)**: AI chat had limited effect on affective polarization but raised understanding of those with different views and perceived moral similarity. — [working paper](https://johanneswalter.github.io/Using-AI-Persuasion-to-Reduce-Political-Polarization.pdf)
- GPT-3 rephrasing assistant (Argyle et al., PNAS 2023, cited by the team): policy positions were unchanged while the aim was feeling listened to. — [arXiv 2302.07268](https://arxiv.org/pdf/2302.07268v5.pdf)

### Inferences
These are my recommendations, not sourced findings.

- **Use ITT logic as the primary score.** A description of cluster B earns credit when B's members agree with it at least as much as with B's own in-group statements of the same view. This gives a calibrated baseline, instead of a raw approval number. It is the closest published match to "the described side would sign".
- **Add two explicit items from Dryzek and Niemeyer**, asked of the described side and scored separately: "This describes what we value" (fidelity, normative) and "This describes why we believe it" (fidelity, epistemic). Asked of the describing side: "A reasonable person could hold this" (recognition). That last item separates *accuracy* from *respect*. A cluster can describe an opponent accurately and still think them illegitimate.
- **Track position change as a guard, never a reward.** The HM's "group agreement" rewards exactly what Dialogos rejects. Report it, and flag any note whose acceptance coincides with one side's position moving toward the other, because that may be persuasion rather than understanding.
- **Reuse the HM's shape, with a different target.** Generate candidates, predict the *described* cluster's ranking, then have real members critique and sign. Predictions may only shortlist; humans ratify. This matches the project's "agents never ratify" rule, and the ranker's doubtful accuracy on diverse views (Q3) gives a further reason for it.
- **Guard the sign-off itself.** Three failures appear in this evidence: acceptable blandness (a text that everyone tolerates and no one recognizes), under-weighted minorities inside a cluster, and strategic sign-off. So require clause-level provenance back to quotes, sample dissenters within a cluster, and let the described side name what is missing. A statement should also be testable: does it distinguish this cluster from others? A description any cluster would sign says nothing.
- **Use DRI as a periodic audit, not a live score.** It needs a purpose-built survey of 20–40 items, and it is a group property rather than a score for one text. It could test whether cross-cluster notes actually change how members connect reasons to preferences.
- **Use Q method to validate cluster boundaries.** Its factors are a small-sample, human-sorted check on whether transcript-derived clusters match how people arrange these views. This could help with curated niches vs data-derived clusters.
- **Do not use DQI or AQuA as a success metric.** LLMs now score at human level on these without matching gains in reasoning, so they can be gamed by agents. Keep them, at most, as a civility filter.
- Dialogos's definition is narrower than either published meaning: it is neither a fair-process acceptance (the Habermas team's sense) nor agreement on how issues are structured. It is a checkable claim about *a specific text*, which makes it more measurable than the original concept. Meta-consensus in the D&N sense would then be the aggregate: many such signed descriptions, in both directions, across clusters.

### Gaps
- I found no published study that uses opponent endorsement to score **AI-generated** steelmen or group descriptions. This looks like an open niche, and it is an inference from searches that found nothing, not proof of absence.
- Brand et al.: only the abstract was read (Wiley and PMC blocked my fetch), so pass rates, effect sizes and test-retest reliability are missing. It also tests individuals' arguments on UK topics, not group-level descriptions.
- Niemeyer & Dryzek 2007 (the source for the intersubjective-rationality measure and the Q procedure) could not be read in full, so I cannot give its exact index or thresholds, and I found no accepted numeric threshold for declaring meta-consensus. I did not verify the DRI formula against the APSR text; it comes from Flechtner's restatement.
- Unknown how well a sign-off from a sample stands in for a whole cluster, and how to recruit members of clusters built from public figures' transcripts. This is a design problem for Dialogos, with no literature I could find.
