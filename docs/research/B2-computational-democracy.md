# B2 — Computational Democracy & Deliberation Technology

> **Design update (2026-10-30).** The Design Dialogue Memo of 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`) records decisions that supersede earlier research recommendations where they conflict; see `synthesis/SYNTHESIS.md` §2. The research below is unchanged. For this brief:
> - **Superseded: treating X likes, retweets and quote-tweets as an implicit vote matrix** "alongside the follow graph" as layer 1. The vote matrix is now **explicit and first-party**: people react agree / disagree / pass to real, source-linked statements selected from landmark content (Polis-like, with guess-who-said-it). This placement defines cluster membership for ratification (SYNTHESIS §2 D17; §6.1 S5, moved to phase 1).
> - **Modified: claim extraction "then statements people can vote on".** Now decided: quote-anchored propositions from ~500 landmarks' public output, with statement selection favoring cluster-splitters, scene-internal live threads and surprising unifiers (§2 D15).
> - **Extended: Community Notes as a model.** Community-Notes-style **cross-cluster notes** carry the gradient: fidelity (only the described cluster grants it) and portability (cross-viewpoint clarity via MF) (§2 D2; SYNTHESIS §7.5). vTaiwan's lineage is noted alongside Community Notes; more pending in B9.
> - **Modified: "MOVE should reward unpublished synthesis attempts."** Novelty is not rewarded at proposal; syntheses are rewarded retroactively by lineage (§2 D3–D4).
> - **Kept:** ≥2 dimensions, held-out prediction and out-of-topic transfer; axes are now also chosen per live question (§2 D7).

*Wave-1 research brief for Dialogos Arena (author of record: Benjamin Life). Compiled 2026-10-30.*

## Summary

Over the past 15 years, computational democracy has produced four reusable kinds of mechanism:

1. **Vote-matrix opinion mapping.** Polis runs PCA and k-means on agree/disagree/pass votes, then computes group-aware consensus.
2. **Bridging-based selection.** Community Notes fits matrix factorization to rating data and keeps the content whose approval survives after the rater's ideological axis is accounted for. Remesh uses a "max-min" agreement across groups.
3. **LLM sensemaking.** Talk to the City, Jigsaw Sensemaker, the Polis 2.0 reports, and Harmonica use LLMs to extract and cluster claims.
4. **LLM mediation.** DeepMind's Habermas Machine writes a group statement, has people critique it, and revises it.

The evidence is real but modest. Community Notes cut resharing and moved Democrats and Republicans about equally. The Habermas Machine raised group agreement by 6–9 points, and people preferred its statements to human mediators' about 56% of the time. Deliberative Polls move opinions and reduce affective polarization. Bridging feed ranking reduced affective polarization by about 0.03–0.04 SD.

These systems tend to fail for the same reasons:

- **Low participation and slow results.** Notes appear about 15 hours after a post (median). About 90% are never published.
- **No binding power.** vTaiwan stalled once legislators were free to ignore it.
- **One axis of disagreement.** Two-dimensional or one-dimensional geometry collapses everything onto a single left–right line.
- **The LLM merges distinct ideas** when it summarizes.
- **Every one of them works on a prompt someone chose.**

None of these systems maps worldviews from organic social data at population scale, and none rewards people for synthesizing across camps over time. Those two gaps are where Dialogos Arena's SEE and MOVE layers fit. For MEET, the parts to reuse are the Polis math and Polis 2.0, the Community Notes scorer, Talk to the City and kouchou-ai, and the Habermas-style critique loop.

---

## Findings

### 1. Pol.is / vTaiwan / Join

**How it works.** The method is documented in Small, Bjorkegren, Erkkilä, Shaw & Megill (2021):

- **Vote matrix.** Participants vote on comments, coded +1 (agree), −1 (disagree) or 0 (pass). Comments a person has not seen are filled with the column mean. Anyone with fewer than 7 votes is dropped.
- **Projection.** PCA reduces the matrix to two dimensions, using power iteration seeded with the previous eigenvectors. Sparse voters are rescaled outward to correct for how few votes they cast. The authors call this correction ad hoc.
- **Clustering.** K-means first builds 100 fine clusters. It then re-clusters them for k = 2 to 5 and picks the k with the best silhouette score. A new k must win four times in a row before the display switches, so the group count doesn't flicker.
- **Representative comments.** Each group's representative comments are chosen by comparing how the group votes against how everyone else votes, with pseudocounts and a Fisher-style confidence weight.
- **Group-informed consensus.** Each group's agreement probability is multiplied together. The score is therefore high only when every group agrees, which stops the majority dominating.
- **Comment routing.** Comments are served in a weighted semi-random order. Priority goes to comments with high agreement, few passes, extreme positions (useful for placing people) and few votes so far.
- **Moderation.** Moderators can either approve comments before they appear ("strict") or remove them after.

**Scale.**
- vTaiwan's Uber case had about 2,000 participants. After cleaning, the analysis used 1,238 participants and 98 comments. PC1 explained 22% of variance and PC2 6.2%. *(Small et al. 2021)*
- vTaiwan reportedly involved more than 200,000 people across 26 pieces of national legislation. *(Noveck, via GovLab)*
- CompDem says Polis 1.0 has had more than 10M participants across tens of thousands of conversations since 2012. Its largest single conversation was Aufstehen in Germany, with 33,547 participants. *(CompDem's Polis 2.0 announcement, as reported Feb 2026; secondary sources, UNVERIFIED against compdemocracy.org)*
- Other users: UK national-security consultation, Finnish services, Austria's Klimarat, UNDP youth dialogues (about 30k people), Bowling Green KY. Jigsaw says Bowling Green's 2025 process drew input from 8,000 residents.

**Polis 2.0 (announced around February 2026).**
- Claims 10–30× the scale of Polis 1.0 (millions of participants).
- Topic clustering with the Tutte Institute's EVōC library.
- LLM steps that turn transcripts, emails and social posts into statements people can vote on.
- LLM toxicity filtering and translation, with human review.
- Multi-model narrative reports that cite their sources clause by clause.
- Invite Trees (who invited whom), XID/OIDC identity, and topic selection before voting.
- Still no replies, by design.
- *Source: secondary reporting (GeekNews, LavX). Treat the scale claims as UNVERIFIED.*

**Code.** AGPL-3.0 (compdemocracy.org/open-source). The repository is `compdemocracy/polis`. The math module was historically written in Clojure (UNVERIFIED: GitHub could not be reached from this session).

**Failure modes.**
- **Small groups.** Polis works poorly below dozens of people and tens of comments.
- **Prompt shape.** Binary, narrow or ranking-style prompts work poorly.
- **Early arrivals dominate.** People who join early end up with denser vote records.
- **Missing data.** Filling unseen comments with column means pulls people toward the centre. Nishio describes how large multi-topic conversations collapse into one blob, and suggests per-topic sub-maps or kNN imputation instead.
- **Two dimensions are too few.** In the Uber case PC1 and PC2 together explained under 30% of variance.
- **Duplicates.** Duplicate comments multiply as conversations grow.
- **Moderator bias.** Moderators can skew what people see.

**Why vTaiwan stalled.** Co-creator Jason Hsu says it hasn't been used for a major decision since 2018. Its outputs were non-binding, so legislators did not take them seriously (Daily Beast, Nov 2023; Noveck). Madrid's Decide platform shows the same pattern: of 28,000 proposals, only one became policy, and sign-ups then fell.

Taiwan's government petition platform, Join, is the institutional counterpart to vTaiwan. Its details were not researched here beyond a comparison thesis that exists at NTU (UNVERIFIED).

**Lesson.** The process stops working once there is no binding link to power or no lasting institutional owner.

### 2. Talk to the City (AI Objectives Institute) and its forks

**How it works.** LLMs extract arguments from unstructured input such as surveys, transcripts and video. Similar arguments are grouped into clusters and subclusters, which users can explore and trace back to the source quotes. AOI calls it a proof of concept.

The specific steps (embedding, then dimensionality reduction, then clustering, then LLM labels) are widely described that way but were **UNVERIFIED** in this pass, because the repository could not be fetched.

**Deployments:**
- Recursive Public, which used Polis data as its input.
- GenAI Taiwan 2023, run with the Collective Intelligence Project (CIP) and Audrey Tang.
- Heal Michigan (video interviews).

**Forks.** In Japan, Takahiro Anno's team built **kouchou-ai** (Japanese for "broad-listening AI") on top of Talk to the City. It adds hierarchical drill-down and density-based extraction of tight opinion clusters, a Docker setup, and an interface non-engineers can run. A defence against majority manipulation is planned (Nishio's notes).

Anno's 2024 Tokyo gubernatorial campaign was known for using AI tools. It took 154,638 votes. The movement became the Team Mirai party, which won 1 upper-house seat in 2025 and 11 proportional seats in February 2026 with 3.8M+ votes (Wikipedia). This is the clearest case of broad-listening tools tied to electoral power, although Wikipedia does not name Talk to the City specifically.

**Failure modes** (IE CGC case-study review):
- The main error is the LLM **merging distinct ideas**, which the reviewers rank above hallucination.
- Topic hierarchies are muddy until someone iterates on the prompts.
- Summaries are hard to follow for readers without background.
- It needs large, rich datasets.

### 3. Remesh (and CIP Global Dialogues)

**How it works.**
- Participants answer open questions in real time, vote on samples of each other's answers, and see how their views compare.
- Because each person sees only some answers, "elicitation inference" estimates the full vote matrix.
- **Bridging metric: max-min agreement.** A statement's score is its lowest agreement level across demographic or partisan groups, and the statement with the highest such score wins. This is a Rawlsian (egalitarian) welfare rule.
- GPT-4 turns the bridging statements into policy clauses. Experts refine them, the public refines them again, and a final representative dialogue measures support.

**Evidence.**
- *US policy process* (Konya, Schirch, Irwin, Ovadya 2023). Three runs, each costing about $10k and taking about two weeks, with 1,500+ census-balanced Prolific participants. The final policies won 75–81% support overall and at least 70–75% in every age, gender, religion, race, education and party group. Views moved toward support after deliberation.
- *Israeli and Palestinian peacebuilders* (Konya, Thorburn, Bakker, Procaccia et al. 2025). About 100–120 peacebuilders took part over four cycles. Each of the five joint demands won at least 90% agreement on each side; a ceasefire with hostage release ranked first. Equal-power metrics were used: max-min agreement, Dowdall score, and IRV rank.

**Failure modes.**
- It favours consensus and does not handle issues with no consensus.
- Facilitator judgement is decisive.
- The samples are text-based and tech-literate; the authors estimate true support could be up to about 10% lower.
- Outputs can be vague.
- Remesh is proprietary.

**CIP Global Dialogues** runs recurring global AI-values dialogues on Remesh with Prolific recruiting. It promises an open longitudinal dataset. Participant counts were not stated on the page fetched.

### 4. Stanford Online Deliberation Platform / Deliberative Polling (Fishkin)

**How it works.**
- A random, representative sample is surveyed before deliberation.
- Participants receive balanced briefing materials.
- Small groups deliberate, and questions go to expert panels.
- Participants are surveyed again afterwards, against a control group.
- The online platform runs video small groups with an **automated moderator**: speaking queues, timed agendas and abuse prevention. It needs no human facilitator.

**Scale.** 50,000+ unique users and 100,000+ hours of deliberation in 40+ countries and 40+ languages (Stanford's own figures, fall 2026).

The Meta Community Forum of 2022 had 6,342 treated and 6,101 control participants across 32 countries. The 2024 forum had 1,545 participants in four countries.

**Evidence.**
- *America in One Room* (APSR 2021). 500+ voters with a control group. Policy views depolarized and affective polarization fell sharply.
- *Goyal, Gelauff, Gupta, Goel & Munagala* (arXiv 2601.14221, January 2026). Deliberation mainly **reorders** individual opinions rather than shifting groups together. The rank correlation between people's pre- and post-deliberation opinions fell, relative to controls, on 93–97% of items. Variance-based polarization measures were mixed, and extreme views softened modestly. Support expressed in discussion predicted opinion change, including among people who stayed silent (exposure effect).

**Failure modes.**
- Running these events costs a lot (recruitment, materials, incentives).
- They are one-off events.
- Results are advisory.
- The questions are set from the top down.

### 5. DeepMind "Habermas Machine" (Tessler, Bakker et al., *Science* 2024)

**How it works.**
- Two models fine-tuned from Chinchilla. The generator is 70B and the personalized reward model is 1.4B.
- Each participant privately writes an opinion. The generator produces 16 candidate group statements.
- The reward model predicts each person's ranking of the candidates, and the Schulze method aggregates the rankings to pick a winner.
- Participants write critiques of the winner. The machine then generates revised statements from those critiques and runs the same ranking again. This is "caucus mediation": people never talk to each other directly.

**Evidence.** N = 5,734 in total.
- People preferred its statements to those of trained human mediators 56% to 44%, rating them higher for endorsement (OR 1.36) and quality (OR 1.54). The advantage held after controlling for length.
- Group agreement rose by 6–9 percentage points. In one cohort, unanimous groups rose from 22.8% to 38.6%. In a control condition where people saw each other's opinions without mediation, agreement did not change.
- Participants said they moved toward the group view in 30% of rounds.
- Revised statements gave minority views extra weight (0.36 against a base rate of about 0.29) while majority support also rose.
- A virtual citizens' assembly (200 people, demographically representative of the UK, recruited with the Sortition Foundation) showed convergence on 5 of 9 questions, for example support for reducing prison populations rose from 60% to 75%. Brexit did not move.

**Failure modes and critiques.**
- No fact-checking or topic control.
- Participants were convenience-sampled and the topics were UK-only.
- Sætra (CACM) argues that agreement without human contact is a "linguistic compromise" rather than deliberation. The study did not measure attitudes toward the other participants. People may also over-trust an AI's apparent neutrality.

The same team followed up with a perspective piece, "Can AI mediation improve democratic deliberation?" (arXiv 2601.05904, January 2026). It frames AI mediation against the trilemma of broad participation, meaningful deliberation and political equality, and says further empirical work is still needed.

No public code release was found (UNVERIFIED).

### 6. Community Notes and bridging-based ranking

**How the algorithm works** (Wojcik et al., "Birdwatch", arXiv 2210.15723).
- Ratings are predicted as global intercept + rater intercept + note intercept + (rater factor · note factor):

  r̂ᵤₙ = μ + iᵤ + iₙ + fᵤ·fₙ

- The factor is one-dimensional, and in practice it lines up with left–right politics.
- Intercepts are regularized five times more strongly than factors (λᵢ = 0.15 vs λf = 0.03). This means approval explained by ideology goes into the factor term, and only approval that holds across the axis is left in the note intercept.
- A note is shown as **Helpful** when iₙ ≥ 0.40 and as **Not Helpful** when iₙ ≤ −0.08.

**Production scorer.** It now runs many matrix-factorization (MF) scorers and combines them in a meta-scorer: core, expansion, expansion-plus, a topic scorer, and up to 14 per-group scorers by language or region. Each group scorer requires about 80% of a note's ratings to come from that group. *(DeepWiki summary of `twitter/communitynotes`; the official guide was blocked in this session.)*

**Evidence.**
- Posts shown with a note were 25–34% less likely to be liked or reposted.
- In surveys, notes reduced agreement with misleading tweets by about 26%, with no significant difference between Democrats and Republicans.
- 64% of raters found the notes helpful (78% of Democrats, 48% of Republicans).

**Problems found since launch.**
- *Speed.* The median time to the first helpful note is 15.3 hours, and the mean is 65.7 hours. Notes work as corrections after the fact (Razuvayevskaya et al. 2025).
- *Low publication rate.* Only about 10–11.5% of notes are ever published, and the share is falling (Arjmandi-Lari, Mantzarlis & Stafford 2025).
- *Concentration.* The top 10% of writers produce 58% of notes.
- *Debate instead of notes.* 68% of noted posts carry a "note not needed" flag, a sign the system is being used to argue.
- *A second hidden axis.* Andreou & Sirivianos (arXiv 2609.21496, 2026) refit the model on 212.9M ratings. A second axis, which they read as **trust in institutions** and which is independent of left–right, improves prediction; a third adds almost nothing. Among notes that hardly split raters politically, publication rates fall from 71.5% for notes nearest the second-axis origin to 11.7% for those furthest from it. **The one-dimensional model quietly suppresses disagreement along a second axis.**
- *Language equity.* Small-language communities lack the cross-camp raters that publication needs.

**LLM note writers (launched July 2025).** Li & Bakker (arXiv 2604.02592, 2026) studied 1,614 LLM-written notes against 1,332 human notes, using 108k ratings from 42.5k raters. The LLM notes were rated more helpful across left, centre and right raters, with the biggest gain (about +10 percentage points) among neutral raters. They also cited better sources. Their weakness was taking satire and opinion too literally: 36.6% were flagged "note not needed", against 25.7% for human notes.

**Adoption.**
- YouTube Notes (pilot 2024), Meta Community Notes (2025, replacing US fact-checking), and TikTok Footnotes (2025) all say they build on X's open-source algorithm.
- Only X publishes its code and data, so the others cannot be audited (Lloyd, Nguyen, Levy & Naaman, arXiv 2509.15434).
- Meta's "diverse engagement" ranking signal is cited as a bridging deployment (Jigsaw et al. 2024).
- **Bluesky:** no native bridging ranking or notes system was confirmed. A `blacksky-algorithms/assembly.blacksky.community` repository appears to be a deliberation project on the AT Protocol, but its contents could not be retrieved (UNVERIFIED).

**Bridging theory** (Ovadya & Thorburn, arXiv 2301.09976). Bridging is a property of any system that allocates attention: it should build "mutual understanding and trust across divides". It can be measured in three ways:
- *Interaction motifs*, such as diverse approval (content endorsed by people who usually disagree).
- *Surveys.*
- *Content labels.*

The paper's open problems include how to elicit data about relationships, how to choose a model of the divide, resistance to gaming, causal metrics, and when bridging is the wrong goal.

**Field test of bridging feeds** (Stray et al., Prosocial Ranking Challenge, September 2024 to February 2025). Across all five algorithms, affective polarization fell by 0.027 SD. The arm that both upranked bridging content and downranked toxic content achieved −0.042 SD and raised social trust. **Upranking bridging content alone was not significant.**

### 7. Plurality (Tang & Weyl) and the Plurality Institute

*Plurality* (2024) is in the public domain under CC0 (plurality.net). It sets out the ⿻ paradigm, "collaboration across difference", with chapters on Augmented Deliberation and ⿻ Voting, drawing on Taiwan. Weyl's wider body of work supplies the incentive tools relevant to MOVE: quadratic voting and funding, and plural or connection-oriented quadratic funding. The page fetched did not detail them, so they are cited from general knowledge (UNVERIFIED in this pass).

The Plurality Institute presents itself as a research-community hub. Its specific 2025–26 outputs were not verified. Microsoft Research runs a "Plural Technology Collaboratory".

### 8. Collective Intelligence Project and Anthropic's Collective Constitutional AI

**Alignment assemblies.** CIP ran Polis and Remesh processes on AI values: GenAI Taiwan, an OpenAI dialogue, and the now-recurring Global Dialogues.

**Collective Constitutional AI** (Anthropic and CIP, 2023; FAccT 2024).
- About 1,000 Americans, sampled to represent US adults, wrote 1,127 statements and cast 38,252 votes on Polis.
- Polis found **two opinion groups**. Only statements that met the consensus threshold in *both* groups were kept: 275 statements, merged into a constitution about as long as Anthropic's.
- About 50% of the concepts overlapped with Anthropic's own constitution. The public version stressed objectivity and accessibility.
- The model trained on it matched the baseline on MMLU, GSM8K and helpfulness/harmlessness Elo, and showed **lower bias on all nine BBQ dimensions**.
- Limitations: many subjective judgement calls were made in moderating, deduplicating and rewording statements; the trained model was initially over-cautious; and the evaluations were thin.

### 9. Other platforms

**Kialo** (2017; closed and commercial).
- Debates are trees: a thesis at the root, with pro and con claims of up to 500 characters beneath it, each rated for impact.
- A "Perspectives" view shows how different groups rated the arguments.
- Scale (July 2023): 18,000+ debates, 720,000 claims, 1M votes. Kialo Edu is free for schools.
- Widely used as an argument-mining dataset.
- Criticisms: the format oversimplifies arguments, moderators shape what is visible, and the data cannot be freely reused.

**Generative social choice** (Fish, Gölz, Parkes, Procaccia et al.). An LLM drafts a slate of statements with proportional-representation guarantees. In a test on abortion policy, 84 of 100 people felt "excellently" or "exceptionally" represented by a slate of five statements. This gives a principled alternative to finding a single consensus statement: aim for **proportional coverage** of views instead.

**Jigsaw Sensemaking tools** (open source, around 2025). Gemini-based tools that categorize, summarize and find common ground in public input. Used in Bowling Green's 25-year plan (8,000 residents). The repository is `Jigsaw-Code/sensemaking-tools`; its license and evaluation are UNVERIFIED.

**Harmonica** (MIT license). AI agents hold parallel one-to-one dialogues with participants, work out each person's core position, check it against the others, and synthesize the results. Aimed at co-ops, DAOs and assembly facilitators.

**Frankly** (Harvard Berkman Klein Center Applied Social Media Lab; AGPL; closed beta announced April 2025). Video small-group dialogue with discussion guides, group matching for diversity of perspective, and facilitation support. Built on the Lightning Rod Labs code.

**Loomio** (AGPL; started in New Zealand's Occupy movement in 2012). Group discussion leading to proposals and polls. 20,000+ groups in 100+ countries as of 2016. A tool for small-group governance, not for mapping opinion.

**Decidim** (AGPL; Barcelona). A modular participation framework covering proposals, budgets and assemblies. Barcelona's 2020–23 participatory budget drew 64,571 participants (52,601 online) and 1,982 proposals; 76 projects were funded from €30M. This is the strongest case of tooling tied to binding power. The figures are self-reported.

**Citizens' assemblies tech.** The Sortition Foundation (recruitment) and the Habermas Machine's virtual assembly are covered above. CrownShy's Comhairle is a workflow layer that chains Polis, Talk to the City and other tools together, with a Scottish Government contract (Parachute: `vault/projects/united-independents/docs/Civic Tech Stack Research Draft`; not independently verified).

### 10. Developments in 2025–2026

- **Polis 2.0** (around February 2026): an LLM pipeline, EVōC topic clustering, and a claimed scale of millions.
- **AI note writers on Community Notes** (July 2025 onward): field evidence that their notes are rated more helpful across the political spectrum.
- **Meta and TikTok adopt bridging notes** (2025). The two-axis Community Notes finding (2026).
- **The Prosocial Ranking Challenge** results (2025/26).
- **The Stanford "opinion mixing" re-analysis** (January 2026).
- **DeepMind's AI-mediation perspective** (January 2026).
- **Jigsaw Sensemaking AI** partner program (2025–26).
- **Team Mirai**: Japan's broad-listening party wins Diet seats (2025–26).
- Benjamin's own context (Parachute): he met Polis Labs, a separate group from CompDem, in August 2025 and April 2026, and he has mapped this tool stack for the BGI/United Independents engagement.

---

## How this answers the governing question (layering and validation)

**What a vote matrix captures.** Polis and Community Notes show that *revealed agreement and disagreement on concrete statements* is the most reliable way to locate someone in opinion space. It measures stance rather than topic, because each person is reacting to the same item.

That suggests an analogue for Dialogos Arena. Treat X likes, retweets and quote-tweets as a **noisy, implicit vote matrix** over posts or claims, alongside the follow graph. Then fit Community-Notes-style matrix factorization on it. The rater (user) factors become worldview coordinates, and the item intercepts give "content valued across the divide". This is ideal-point modelling, as in Barberá's follow-graph ideology work (covered in B3/B4, presumably).

Proposed layering, from cheapest to richest:

1. **Social and engagement graph, then matrix factorization or ideal points.** Gives *where you sit*, with several axes. Use at least two dimensions: Andreou & Sirivianos show that one axis hides a second fault line, and a third adds almost nothing on Community Notes data. Choose dimensionality by held-out prediction error, not by eye.
2. **Claim extraction (in the style of Talk to the City or Ontography), then statements people can vote on.** Tells you *what the axes mean*. Label each latent axis by the claims that load most heavily on it. This is the same move as Polis's representative comments, which separate group members from non-members.
3. **LLM synthesis (Habermas loop or generative social choice).** Gives *what could bridge*. Draft candidate bridging statements and score them with the factor model: predicted endorsement on both sides of each axis.
4. **Worldview typing** (Ontography's ontological, epistemological, axiological and praxis layers). Applied *only to the representative claims of each cluster*, not to every node. This avoids illegible graphs of 600 to 1,200 nodes.

To keep the load on users manageable, show one 2D map at a time, chosen from the top axes. Name each axis with three representative claims. Let users drill into subclusters, as kouchou-ai does.

**Validation methods that already exist in these systems:**

- **Held-out prediction.** If the map is right, it predicts unseen votes and ratings (Community Notes, Andreou). This is the main test.
- **Out-of-topic transfer.** An axis learned on topics A should predict reactions on held-out topic B (Andreou's COVID and Ukraine test). This separates *stance* from *topic*, the main risk with embeddings.
- **Self-recognition.** Ask users whether the slate represents them, as generative social choice did (84/100 "excellent" or better), or whether they recognize their placement.
- **Cross-group endorsement.** Max-min or group-informed consensus scores on statements produced by the system, checked with fresh participants.
- **Behavioural outcomes.** Opinion reordering and affective polarization against a control group (Deliberative Polling, the Prosocial Ranking Challenge).
- **Stability.** Polis requires a new number of groups to win four times in a row. Bootstrap the clustering and report how often each person keeps the same assignment.

---

## Reusable assets and design implications

| Need | Reuse | Notes |
|---|---|---|
| SEE: latent axes from engagement | **Community Notes MF scorer** (`twitter/communitynotes`, Python; license reported as Apache-2.0, UNVERIFIED) | Refit with 2+ dimensions; per-group scorers already exist. Feed it X likes and retweets as implicit ratings. |
| SEE / MEET: statement voting + group consensus | **Polis** (AGPL-3.0) or **Polis 2.0** | Group-informed consensus, representative comments, comment routing. AGPL matters if it runs as a networked service. Replace mean-imputation with kNN or MF imputation. |
| SEE: claim clustering from free text | **Talk to the City**, **kouchou-ai**, **Jigsaw sensemaking-tools**, **EVōC** | Watch for the LLM merging distinct ideas; keep links back to source quotes. |
| MEET: AI-mediated synthesis | **Habermas Machine method** (published; no code found), **Harmonica** (MIT), **generative social choice** | Use critique-and-revise loops plus a reward model that predicts each person's endorsement. Prefer proportional slates over a single consensus statement. |
| MEET: synchronous small groups | **Stanford Online Deliberation Platform** (automated moderator), **Frankly** (AGPL) | Video groups that run without a human facilitator. |
| MOVE: bridging-weighted reward | Community Notes intercept, Remesh **max-min** agreement, **Prosocial Ranking Challenge** findings | Rewarding bridging content alone was not significant; it must be paired with downranking toxic content. |
| MOVE: plural weighting | Quadratic and plural quadratic-funding mechanisms (*Plurality*) | Specific implementations should be covered in B-briefs on mechanism design. |
| Governance / binding | **Decidim** | The case where tooling met real budget authority. |

**Design implications.**

- **Plan the link to power from the start.** vTaiwan and Decide Madrid stalled when their outputs had no binding effect. Team Mirai and Barcelona's participatory budget worked because they were tied to an election or a budget. The Arena needs a consequence loop of its own, whether through reputation, money or institutional uptake.
- **Make writing notes rewarding.** Having a note published makes the author more likely to write again (regression-discontinuity evidence). The 90% of notes never published is a waste of contributor effort, so MOVE should reward contributors even for unpublished synthesis attempts.
- **Expect LLM synthesizers to beat the median human** (Habermas, AI note writers). Their risks are false neutrality, reading satire literally, and merging distinct ideas. Keep humans as raters and validators; let LLMs be generators.
- **Measure opinion reordering, not only convergence.** Deliberation mostly reshuffles individual views (Goyal et al. 2026). A dialogos metric should reward "changed by the encounter" in that sense.

---

## Risks and open questions

- **Organic data is not consenting deliberation.** Polis-style tools work because people chose to respond to a shared prompt. X engagement is shaped by the platform's own algorithm, so likes partly reflect what the feed showed. Can the system correct for exposure bias?
- **Access to X data.** The X API's cost and rate limits are covered in another brief; the Community Notes public data dump is a usable alternative training corpus.
- **Gaming.** Bridging signals can be farmed: Community Notes is open to coordinated rating, and the Lloyd et al. framework names contributor bias. Any reward in MOVE will draw sybil attacks. Polis 2.0 is moving toward identity (XID, OIDC, Invite Trees).
- **Consensus-washing.** Max-min and bridging rules favour centrist or vague framings and leave the most divisive content unaddressed. The Arena's thesis is integrative synthesis, not lowest-common-denominator agreement. Generative social choice (proportional slates) and the Habermas Machine's extra weight on minority views partly address this.
- **How many dimensions?** Community Notes data suggests two. Worldview space is likely higher-dimensional and topic-dependent. Polis's 2D maps explain under 30% of variance.
- **AGPL implications** for any hosted fork of Polis, Frankly, Loomio or Decidim.
- **Unverified in this pass** (GitHub repositories and the Community Notes guide were blocked):
  - Repository licenses and languages.
  - Talk to the City's exact pipeline.
  - Polis 2.0 primary source and scale claims.
  - Plurality Institute outputs.
  - Bluesky/Blacksky deliberation work.
  - Join platform details.

---

## Sources

- Small, Bjorkegren, Erkkilä, Shaw, Megill, "Polis: Scaling Deliberation by Mapping High Dimensional Opinion Spaces," *Recerca* 26(2), 2021. https://www.e-revistes.uji.es/index.php/recerca/article/view/5516 ; PDF https://Www.Gwern.net/doc/sociology/2021-small.pdf
- CompDem open source (AGPL-3.0): https://compdemocracy.org/open-source
- Polis 2.0 reporting (secondary): https://news.hada.io/topic?id=26667 ; https://news.lavx.hu/article/polis-2-0-the-open-source-platform-scaling-deliberative-democracy-to-millions
- Nishio, "Phenomenon that Polis with the most votes are lumped together": https://scrapbox.io/nishio-en/Phenomenon_that_Polis_with_the_most_votes_are_lumped_together.
- Aspinwall, "Taiwan Tried to Digitize Democracy…" Daily Beast, Nov 2023: https://www.thedailybeast.com/taiwan-tried-to-digitize-democracy-with-vtaiwan-it-was-a-huge-flop
- Noveck, "Was vTaiwan such a big flop, after all?" (The Living Library): https://thelivinglib.org/?p=57365
- AI Objectives Institute, Talk to the City (archived): https://gwern.net/doc/www/ai.objectives.institute/fa46182a810da5bfde418b21016574027d1dd94f.html
- IE CGC, "Using AI to inform policymaking: 3 use cases of Talk to the City": https://ie.edu/cgc/news-and-events/news/using-ai-to-inform-policymaking-what-we-can-learn-from-3-use-cases-of-talk-to-the-city
- Nishio, "public information AI" (kouchou-ai): https://scrapbox.io/nishio-en/public_information_AI
- Team Mirai (Wikipedia): https://en.wikipedia.org/wiki/Team_Mirai
- Konya, Schirch, Irwin, Ovadya, "Democratic Policy Development using Collective Dialogues and AI" (arXiv 2311.02242): https://ar5iv.labs.arxiv.org/html/2311.02242
- Konya, Thorburn, Almasri, Leshem, Procaccia, Schirch, Bakker, "Using Collective Dialogues and AI to Find Common Ground Between Israeli and Palestinian Peacebuilders" (arXiv 2503.01769): https://arxiv.org/pdf/2503.01769
- CIP Global Dialogues: https://www.cip.org/global-dialogues
- Stanford Online Deliberation Platform: https://deliberation.stanford.edu/tools-resources/online-deliberation-platform
- Fishkin, Siu, Diamond, Bradburn, "Is Deliberation an Antidote to Extreme Partisan Polarization?" APSR 2021: https://deliberation.stanford.edu/publications/journal-articles/deliberation-antidote-extreme-partisan-polarization-reflections
- Meta Community Forum results (Stanford FSI): https://fsi.stanford.edu/node/36099
- Goyal, Gelauff, Gupta, Goel, Munagala, "Beyond Polarization: Opinion Mixing and Social Influence in Deliberation" (arXiv 2601.14221): https://arxiv.org/pdf/2601.14221
- Tessler, Bakker et al., "AI can help humans find common ground in democratic deliberation," *Science* 2024 (PDF mirror): https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf
- Sætra, "Computation and Deliberation: The Ghost in the Habermas Machine," CACM blog: https://cacm.acm.org/blogcacm/computation-and-deliberation-the-ghost-in-the-habermas-machine
- Tessler et al., "Can AI mediation improve democratic deliberation?" (arXiv 2601.05904): https://arxiv.deeppaper.ai/papers/2601.05904v1
- Wojcik et al., "Birdwatch: Crowd Wisdom and Bridging Algorithms…" (arXiv 2210.15723): https://arxiv.org/pdf/2210.15723
- Community Notes group-based scoring (DeepWiki summary of repo): https://deepwiki.com/twitter/communitynotes/2.2-group-based-scoring
- Andreou & Sirivianos, "Two Fault Lines: Latent Polarity Geometry in X Community Notes" (arXiv 2609.21496): https://arxiv.org/pdf/2609.21496
- Razuvayevskaya et al., "Timeliness, Consensus, and Composition of the Crowd: Community Notes on X" (arXiv 2510.12559): https://arxiv.org/html/2510.12559v2
- Arjmandi-Lari, Mantzarlis, Stafford, "Threats to the sustainability of Community Notes on X" (arXiv 2510.00650): https://arxiv.org/abs/2510.00650
- Li & Bakker, "AI Fact-Checking in the Wild: A Field Evaluation of LLM-Written Community Notes on X" (arXiv 2604.02592): https://arxiv.org/abs/2604.02592 ; https://haiwen-li.github.io/ai-fact-checking-in-the-wild/
- Lloyd, Nguyen, Levy, Naaman, "Beyond Community Notes: A Framework for … Crowdsourced Context Systems" (arXiv 2509.15434): https://arxiv.org/html/2509.15434v2
- Ovadya & Thorburn, "Bridging Systems: Open Problems…" (arXiv 2301.09976): https://arxiv.org/pdf/2301.09976
- Stray et al., "The Prosocial Ranking Challenge" (arXiv 2603.19626): https://arxiv.org/html/2603.19626
- Jigsaw/DeepMind et al., "AI and the Future of Digital Public Squares" (arXiv 2412.09988): https://arxiv.org/pdf/2412.09988
- Google.org, Jigsaw Sensemaking AI (Sep 2026): https://blog.google/company-news/outreach-and-initiatives/google-org/sensemaking-ai/
- Weyl, Tang et al., *Plurality* (CC0): https://plurality.net/
- Anthropic & CIP, "Collective Constitutional AI": https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input
- Fish, Gölz, Parkes, Procaccia et al., "Generative Social Choice" (arXiv 2309.01291): https://www.arxiv.org/abs/2309.01291
- Kialo (Wikipedia): https://en.wikipedia.org/wiki/Kialo
- Harmonica (Metagov Deliberative Tool Gallery): https://metagov.org/delib-tools/harmonica
- Frankly (Berkman Klein ASML, Apr 2025): https://cyber.harvard.edu/story/2025-04/asml-invites-open-source-collaborators-to-frankly
- Loomio (Wikipedia): https://en.wikipedia.org/wiki/Loomio
- Decidim Barcelona PB case study: https://decidim.org/case-studies/barcelona-budgeting/
- Parachute: `vault/projects/united-independents/docs/Civic Tech Stack Research Draft` (Comhairle, T3C and Harmonica landscape); `vault/projects/opencivics/meetings/2025-08-27_polis-labs-x-opencivics`; `vault/projects/opencivics-labs/meetings/2026-04-17_polis-labs-opencivics-labs-coordination`

**Blocked in this session (not read):** https://communitynotes.x.com/guide/en/under-the-hood/ranking-notes ; github.com/twitter/communitynotes ; github.com/compdemocracy/polis ; github.com/AIObjectives/talk-to-the-city-reports ; github.com/Jigsaw-Code/sensemaking-tools
