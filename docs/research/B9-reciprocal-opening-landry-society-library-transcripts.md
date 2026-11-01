# B9: Reciprocal Opening, Landry's EGP, the Society Library, and the Transcript Pipeline

*Research brief for the Dialogos Arena. Author of record: Benjamin Life (@omniharmonic). Prepared 2026-10-30 as wave-1 task B9, following the Design Memo of 2026-10-30.*

> **Correction (2026-10-30, decided by Benjamin).** This brief originally said YouTube transcripts were effectively off the table, because the official Data API's `captions.download` requires video ownership and YouTube's Terms of Service ban scrapers. That overstates it. The accurate position:
> - **(a) Feasible and widely practiced.** Pulling the public captions and auto-captions of other people's public videos is routine. Transcript libraries such as `youtube-transcript-api` read the same captions YouTube shows in its own transcript panel, and commercial transcript services do the same. Benjamin has done this many times.
> - **(b) A ToS gray area.** YouTube's Terms of Service prohibit automated access outside the official API, so this route is not ToS-compliant in the strict sense. It is a contract and account risk, not a blocker.
> - **(c) Operational limits at scale.** At hundreds of channels, ongoing, expect rate limits and IP blocks (especially from cloud IPs). Mitigate with a paid transcript service and a paced backfill.
> - **(d) Publication rule.** Publish only propositions with short quote anchors and timestamped links, never full transcripts.
>
> **Decision.** YouTube transcripts remain the **primary source**. Podcast RSS with speech-to-text, publisher transcripts, and landmark opt-in channel connection are **complements and fallbacks**. The ToS risk goes in the risk register, not on the list of blockers. The rest of this brief (cost estimates, copyright analysis, schema) stands; §4's "Recommended pipeline" has been revised to the decided hybrid.

---

## Summary

This brief covers the four items the design memo left open.

1. **Reciprocal narrowing and reciprocal opening.** "Reciprocal narrowing" is Marc Lewis's account of addiction, which Vervaeke adopts. Agent and world shrink each other in a self-reinforcing loop. Vervaeke coined the inverse, "reciprocal opening": a mutually accelerating disclosure between a person and the world, which he ties to love and flourishing. Neither man has published a specification for feeds, so the ranking rules in this brief are our own translation. "Rank by what widens" becomes concrete as: optimize for growth in the set of clusters a person can *accurately describe*, not for time held.
2. **Ephemeral Group Process (EGP).** Its public documentation is thin. A community of about 30 to 300 people ranks questions and is routed into small groups. Each group develops "branch questions" under an Inquiry Coach, and recordings go into a question archive. Two parts are usable: the question genealogy and the routing. Benjamin's critique holds: no published outputs or case studies were found.
3. **The Society Library.** Jamie Joyce's group runs analyst-driven deliberation mapping: positions, arguments, claims, evidence, with one ID per claim and every source quote attached. That is effectively a proposition bank with quote anchors, built by hand. Its weakness is scale (about 8,000 hours for one map). It also has no step where the described side ratifies the description. That gap is what cross-cluster notes would add.
4. **Transcripts** (*revised per the correction above*). The official YouTube API does not let third parties download captions, and the YouTube Terms of Service prohibit automated access outside the API. Even so, pulling public captions through transcript libraries or commercial services is routine and feasible; it is a ToS gray area with rate-limit and IP-block risk at scale, not a blocker. **Decided:** YouTube transcripts are the primary source, with podcast RSS + speech-to-text, publisher transcripts and opt-in channel connections from landmarks as complements and fallbacks. Where speech-to-text is needed, a 10,000-hour backfill costs roughly **$1.7k–$4.6k** for speech-to-text plus about **$0.1k–$1.1k** for LLM extraction (estimates). Publish propositions with short quote anchors and timestamped links, never full transcripts.

---

## Findings

### 1. John Vervaeke: reciprocal narrowing and reciprocal opening

**Definitions (from the sources)**

- **Reciprocal narrowing** comes from neuroscientist Marc Lewis (*The Biology of Desire*; Vervaeke's University of Toronto colleague). Lewis treats addiction as a developmental, self-organizing loop, not a disease. Narrower attention makes the world afford fewer things, which narrows the person further, until a single object carries all the reward [Olshonsky 2022; Theo Von #462]. On the Theo Von show, Vervaeke credits "a colleague's theory" and describes the substance eroding cognitive capacity while the world seems ever more threatening [Theo Von #462].
- In Vervaeke's framework, this is the negative mode of **relevance realization**: the self-organizing process by which a mind decides what is salient. He links it to **parasitic processing** (from his Buddhism lectures, *Awakening from the Meaning Crisis* Ep. 13) and to self-deception. The Petersonsphere glossary lists "Parasitic Processing (psychological view)" and "addiction-forming process" as aliases of Reciprocal Narrowing [Petersonsphere glossary; AFTMC Ep. 13 listing]. The exact AFTMC episode where he first sets out reciprocal narrowing is UNVERIFIED.
- **Reciprocal opening** is Vervaeke's inversion. He reasons that if agent and world can narrow each other, they can also open each other. He describes it as a mutually accelerating disclosure between a person and another person or situation, and identifies it with love, flexibility and peace of mind [Jim Rutt EP 143; Theo Von #462]. Olshonsky glosses it as a progressive widening of what brings a person joy [Olshonsky 2022].
- The underlying frame is the **agent–arena relationship**: meaning lives in the fit between agent and world, so narrowing and opening are properties of that *relationship*, not of the person alone. This also appears in the Henriques–Vervaeke *Psychopathology and Wellbeing* series, but only the glossary index was reachable; the transcript content is UNVERIFIED.
- **Application to social media and algorithms.** Vervaeke names social media as one driver of the meaning crisis and mentions a "virtual exodus" [Jim Rutt EP 143; Theo Von #462]. No text was found in which he or Mastropietro or Henriques apply reciprocal narrowing to ranking algorithms (UNVERIFIED / likely absent). The "algorithm in reverse" framing is Benjamin's extension, and should be presented that way.

**Translation into design.** An engagement feed is an outsourced relevance-realization machine optimized to *hold* attention. It narrows what the user finds salient, and the user's narrowed clicks narrow what the model serves back. That is reciprocal narrowing between a person and a recommender (our inference). Running it in reverse means the system's objective is the growth of the user's *affordances*: the number of perspectives they can see from and accurately describe.

**Ranking and feed rules ("rank by what widens")**

| # | Rule | Mechanism |
|---|---|---|
| R1 | Objective = predicted gain in *describable clusters*, not dwell time | Score an item by how likely it is to raise the user's perspective-taking accuracy on a cluster where that accuracy is currently low (see metrics below). |
| R2 | Information gain over confirmation | Down-rank statements whose reaction is near-certain given the user's position (as in Polis, a predictable reaction says little about the user). Up-rank statements that split the user's own cluster, or that unite clusters the user thinks are distant (the memo's "twist" statements). |
| R3 | Graduated distance (a zone of proximal opening) | Serve the next-adjacent cluster first and widen step by step. Maximum-distance content is likely to provoke backlash and hardening (design hypothesis, not tested here). |
| R4 | Bridging over in-group applause | Weight items by cross-cluster approval, as Community Notes does, not raw likes. In-group-only applause carries a mild penalty. |
| R5 | Penalize hardening | Propositions defined *against* an outgroup (negation-framed, contempt-laden) are excluded from the "widening" pool even when popular. This uses the memo's deepening/hardening distinction. |
| R6 | Finite surfaces | The daily pulse ends ("you're caught up"). No infinite scroll, no streaks, no variable-reward notifications. Narrowing is a loop and these are its gears. |
| R7 | Close each session with an act of opening | The last card invites the user to *produce* something: describe a far cluster, or adopt a question from a far cluster. |
| R8 | Thread-first, not person-first | Follow questions, not personalities. Following a person tends to collapse salience onto one source. Questions branch. |

**Measuring opening and narrowing**

*Person-level* (all can be computed passively; no surveys, per the memo):
- **Perspective-taking accuracy (primary).** In "guess who said it" and "how would cluster B react?" cards, track prediction accuracy per cluster. Opening is rising accuracy across more clusters. Weight far clusters more.
- **Ratified-description count.** The number of the user's notes about other clusters that those clusters have signed. This person-level version of the gradient is the strongest signal of opening.
- **Breadth.** Entropy of the clusters the user reacts to, writes about, or adopts questions from over a rolling 30 days. Narrowing is falling entropy.
- **Hardening share.** The fraction of the user's endorsed or authored propositions classified as outgroup-defined.
- **Usage shape.** Many short, compulsive sessions (an addiction signature) versus fewer, completed sessions. This is a guardrail metric, not a reward.

*Cluster-level:*
- **The description-fidelity matrix** (the memo's gradient): the ratification rate of A's notes about B, for every pair. Opening is the mean rising and the off-diagonal gaps closing.
- **Deepening vs. hardening**: the number of live internal threads and internally worked disagreements, against the share of the cluster's new propositions defined against an outgroup.
- **Permeability**: the share of members who react to and engage with far-cluster statements. Also the import rate of questions and propositions with lineage to other clusters.
- **Validation**: A/B test the reverse-ranked feed against a plain engagement-ranked baseline on perspective-taking accuracy, measured with held-out cards. Opening should beat the baseline on accuracy while taking *less* time.

### 2. Forrest Landry's Ephemeral Group Process (EGP)

**What is publicly documented**
- **egp.community.** It describes EGP as a technology-assisted but face-to-face process for communities working on chronic problems. It puts *inquiry first*: better questions before answers. The site names no creator, events or archive [egp.community; /what-is-egp/].
- **Steps** (from the site and the Life Itself wiki):
  1. Arrive and receive a digital ID card plus a list of community-level questions.
  2. Rank the questions by interest; the system routes each person to a forming small group on a shared "base question".
  3. Spend 45–60 minutes in a group, guided by an **Inquiry Coach**. Unlike a facilitator, the coach helps people find their curiosity. The phases are: explore experiences, brainstorm **branch questions** (sub-questions that would need answering), then summarize the essential questions and insights.
  4. Rotate to another group.
  5. Upload the recordings to the EGP server, where **archivists** process them into a dynamic, open-source archive. Questions feed later rounds.

  Scale is about 30–300 people [Life Itself wiki; egp.community/what-is-egp/].
- **Landry and the larger stack.** On the Jim Rutt Show (EP 153, about 2022), Landry sets out his separate *Small Group Method*. Its parts:
  - consensus for internal matters;
  - role-based meritocracy for external action;
  - democracy only as a "red button" recall or a petition to break a stalemate;
  - groups of about 9–12 (up to about 16), with an architecture he says becomes viable only near 150–200 people.

  He refers to "EGP" as a later "level two" stage of a broader body of work, and says it will take years to articulate fully [Jim Rutt EP 153]. This supports the memo's claim that EGP is one method in a larger stack. No public document lists the stack.
- **The Stoa session (2020).** No recording or transcript could be located (UNVERIFIED). The Stoa's archives are largely on YouTube and Peter Limberg's *Less Foolish* Substack.

**What is usable**
- **Question genealogy.** Base question → branch questions → archived and fed into later rounds. This maps directly onto the memo's "genealogy of questions". Treat each live thread as a *base question* with typed child questions, with lineage edges recorded.
- **Routing by question ranking.** Ranking questions and getting matched into small groups on shared questions is a good template for the Arena's MEET layer. Group people by *question*, then deliberately mix their *clusters* within the group.
- **The coach as a role.** A role whose job is better questions, not turn-taking. An LLM "inquiry coach" in Arena sessions could propose branch questions and hand them to people to ratify.
- **Ephemerality.** Groups dissolve; questions persist. Persistent groups ossify into identities, so this is a guard against hardening.

**Limits (stated honestly)**
- No published outputs, evaluations or case studies were found, which matches Benjamin's experience (general, no concrete deliverable).
- In-person, synchronous, and coach-intensive; it does not scale cheaply online.
- The archive is a pile of recordings plus human archivists. It has no structured schema for how questions relate to each other, or to propositions and clusters.
- It produces questions but has no mechanism for *uptake* or reward. The memo's lineage incentive supplies exactly that.

### 3. Jamie Joyce and the Society Library

**Method**
- **A nonprofit "library" of societal debate.** It extracts arguments, claims and evidence from news, scholarship, documentaries, books, TV, podcasts, social posts and politicians' statements [Deep Tech Week profile; YANSS 292; Jim Rutt Currents 076].
- **Topic flyover.** Collect materials, find subtopics, repeat. For climate, the result was 278 subtopics under six fundamental questions: five *is*-questions and one *ought*-question [Currents 076].
- **Structure.** Positions are supported or refuted by arguments, which break into claims; each claim can carry its own pro and con arguments. The ontology has 20+ relation types: supports, refutes, qualifies, is evidence for, counterexample, and so on [Joyce, "Your Attempt to Refute Argument Maps Will Not Work", 2026-05-06].
- **Claim identity.** Each claim gets an ID, and *every* phrasing and medium expressing it links to one node, with quotes from every source kept. Each claim has a mini-page with source quotes, Internet Archive snapshots and media artifacts [Currents 076]. This is functionally the memo's **shared proposition bank with quote anchors**.
- **Steelmanning.** Analysts invert claims and steelman the inversion, a devil's-advocacy technique adapted from a CIA tradecraft primer [Currents 076].
- **Neutrality.** They search across sources that lean in different directions, use multiple reviewers, list 22 bias-mitigation methods, and publish their policies. They do not label claims true or false; instead they show status such as "no evidence found" or "not yet fact-checked" [Currents 076]. This matches the memo's rule that notes carry no judgments.
- **Outputs.** "Society Library papers": interactive documents where clicking a sentence reveals the argumentation under it. Also debate maps, a search engine, *Vote By Reason*, a catalog, and consulting for city councils and officials [Currents 076; Deep Tech Week profile].
- **Scale.** The Diablo Canyon map took roughly 5,000 references, about 5,862 claims and arguments, and about 8,000 research hours, and is still unfinished [Joyce 2026].
- **AI.** Earlier work was manual. Joyce now frames the future as semi-automated, AI-assisted extraction and research agents with humans in the loop. Their profile lists fact-checking models, claim collectors and autonomous research agents [Joyce 2026; Deep Tech Week profile; Currents 076].
- **Unverified points.** The exact phrase "papers of record" could not be verified (UNVERIFIED; "Society Library papers" is verified). No Community-Notes-style or crowd-ratification work by the Society Library was found (UNVERIFIED / likely absent). societylibrary.org itself could not be fetched in this session.

**Relation to cross-cluster notes and the proposition bank**
- **Adopt**: claim IDs with many quote anchors; the *is/ought* split of fundamental questions (a close cousin of the anti-debate layers); "status, not verdict" labels; Internet Archive snapshots for source durability.
- **Add what the Society Library lacks**:
  1. **Ratification by the described side.** The Library's analysts steelman *on behalf of* positions; the Arena makes the described cluster sign. That is the fidelity signal.
  2. **Scale through automation plus correction.** Quote-anchored LLM extraction, with users' "that's not me" corrections as labels, against the Library's 8,000 analyst-hours per map.
  3. **People and time.** Its maps are issue-centred and largely static; the Arena's are cluster-centred and lineage-tracked.
- **Opportunity**: the Society Library is a natural partner, either as an external audit of the Arena's proposition-bank fidelity or as a source of seed maps on shared issues. Benjamin has a prior friendly relationship with Jamie Joyce (vault Twitter DM thread, 2021–2024). No outreach was made, per the brief.

**Lineage: Community Notes / Birdwatch and Audrey Tang**
- **Community Notes (Birdwatch).** Wojcik, Coleman et al. (2022) describe a *bridging* algorithm. Matrix factorization models each rating as a note-helpfulness intercept plus a rater-viewpoint × note-viewpoint term. A note is shown only when its intercept, the helpfulness *not explained by viewpoint*, is high, meaning raters who usually disagree both found it helpful [arXiv 2210.15723]. This is exactly the memo's **portability** signal.
- **Fidelity is new.** Community Notes asks "helpful across viewpoints?" The Arena also asks "does the *described* group sign it?". It restricts one rating channel to members of cluster B, as defined by their statement reactions. A within-B split surfaces sub-clusters, which follows the same factorization logic run inside B.
- **AI note writers.** A 2025 paper proposes LLM-written notes with human rating as the gate ("Scaling human judgment in Community Notes"; arXiv 2506.24118, authors UNVERIFIED; page not fetched). This is relevant if the Arena lets an LLM draft cross-cluster notes for humans to ratify.
- **Audrey Tang, vTaiwan and Polis.** Polis clusters participants from their agree/disagree/pass votes on short statements, and surfaces "group-informed consensus" statements that win across clusters [compdemocracy.org; vTaiwan]. This is the direct ancestor of the memo's statement-reaction placement and the bridging rule R4. These details are from prior knowledge; the pages were not fetched in this session.

### 4. Transcript pipeline for about 500 landmark figures

> **Correction (2026-10-30, decided by Benjamin).** The YouTube findings below are accurate about the *official API* and the *letter of the ToS*, but the original conclusion ("do not build the core pipeline on them"; podcasts as "the primary route") overstated the barrier. Pulling public captions and auto-captions of other people's public videos via transcript libraries (e.g., `youtube-transcript-api`, which reads the same captions shown in YouTube's transcript panel) or commercial transcript services is routine and feasible; Benjamin has done it many times. It is (a) technically feasible and widely practiced; (b) a ToS gray area, since YouTube's ToS prohibits automated access outside the official API; (c) subject to rate limits and IP blocks at scale (hundreds of channels, ongoing), mitigated by a paid transcript service and a paced backfill; and (d) publishable only as propositions with short quote anchors and timestamped links, never full transcripts. **Decision:** YouTube transcripts are the primary source; podcast RSS + speech-to-text and landmark opt-in channel connection are complements and fallbacks; the ToS risk belongs in the risk register, not among blockers.

**YouTube**
- **API.** `captions.list` exposes track metadata, but `captions.download` returns 403 "permissions… not sufficient" for videos you don't own. In practice only the owner, or someone with edit rights on the channel, can download tracks, including auto-captions [YouTube API error reference; Stack Overflow Q41087864]. The official docs page could not be fetched; the owner-only behaviour is strongly corroborated but not quoted from the docs.
- **Terms of Service.** These bar accessing the Service "using any automated means (such as robots… or scrapers)" except public search engines per robots.txt or with prior written permission. They also bar downloading Content except as expressly authorized [YouTube ToS]. yt-dlp and `youtube-transcript-api` (which reads the internal timedtext endpoint) therefore fall outside the ToS. They are a contract and account risk, and operationally fragile because YouTube blocks cloud IPs. ~~*Do not build the core pipeline on them.*~~ *Superseded by the correction above: this is a ToS gray area to log in the risk register, not a blocker. Use a paid transcript service and a paced backfill to manage rate limits and IP blocks.*
- **Transcript libraries and commercial services (primary, per the correction).** These read the public caption tracks (creator-uploaded or auto-generated) that YouTube already shows in its transcript panel. Feasible and widely used; quality of auto-captions varies, and they carry no speaker labels, so diarization or metadata-based speaker naming is still needed for multi-speaker shows.
- **Fully ToS-compliant YouTube routes** (complements):
  1. **Landmark opt-in.** A landmark connects their channel via OAuth, and the Arena downloads their captions as an authorized delegate. This pairs naturally with the memo's "landmarks can dispute or annotate their placement".
  2. **Prior written permission or partnership** with YouTube (unlikely early).
  3. **Linking and embedding.** The public embed player with `?start=` timestamps is permitted for *showing* source clips.

**Podcasts (originally "the primary route"; now a complement and fallback per the correction)**
- RSS feeds publish audio enclosures *for download*, which is how the medium works. Many YouTube-first figures also publish audio feeds (UNVERIFIED share: the seed-list work should tag each landmark's available channels).
- **Publisher transcripts.** Prefer these where they exist: the Podcasting 2.0 `<podcast:transcript>` tag, show-site transcripts (e.g., lexfridman.com), and Substack text. They are free and already authorized for public reading.
- **Speech-to-text with diarization.** Vendor list prices as reported by a June 2026 comparison (verify on the vendors' live pages):

  | Option | Price | Diarization |
  |---|---|---|
  | AssemblyAI Universal-2 | $0.15/h | +$0.02/h |
  | AssemblyAI Universal-3.5 Pro | $0.21/h | |
  | Deepgram Nova-3 | about $0.46/h | supported |
  | Google Chirp batch | about $0.24/h | |
  | OpenAI gpt-4o-mini-transcribe | about $0.18/h | separate diarize model |

  [convertaudiototext.com 2026, a vendor-adjacent source]. Self-hosting WhisperX (faster-whisper plus pyannote) is the open option.
- **Speaker identification.** Diarization yields "Speaker A/B", not names. Map speakers to names using episode metadata plus voiceprint enrollment from each landmark's solo content. Keep a confidence score; the memo notes that Topology Live's speaker attribution was not fully validated.

**Third-party transcript services.** Podcast transcript/search APIs exist (e.g., Podscan, Listen Notes, Taddy; their features and pricing are UNVERIFIED). Use them only if their terms grant redistribution or analysis rights. *Per the correction:* paid YouTube-transcript services are the preferred way to pull YouTube captions at scale (they absorb rate limits and IP blocks). They do not remove the underlying ToS gray area, which stays in the risk register.

**Cost arithmetic (all ESTIMATES)**

*Note (2026-10-30 correction):* with YouTube captions as the primary source, speech-to-text is needed only for audio-only content, for shows where auto-captions are poor, and where diarization matters. The STT figures below are therefore an upper bound for the full-STT route. The per-hour price of commercial YouTube-transcript services was not researched (UNVERIFIED); add it to the cost model in the scoping spike.

*Backfill: 500 landmarks × 20 h = 10,000 h = 600,000 min*

| Item | Arithmetic | Cost |
|---|---|---|
| AssemblyAI U-2 + diarization | 10,000 h × $0.17 | **≈ $1,700** |
| Deepgram Nova-3 | 10,000 h × $0.46 | **≈ $4,600** |
| gpt-4o-mini-transcribe (no diarization) | 10,000 h × $0.18 | ≈ $1,800 |
| Self-hosted WhisperX | Assume about 40× real time on one rented GPU at about $2/h: 10,000 / 40 = 250 GPU-h → $500, plus engineering time | ≈ $300–700 (ESTIMATE) |
| LLM proposition extraction | Speech ≈ 150 wpm ≈ 9,000 words/h ≈ 12k tokens/h → 120M transcript tokens. × 1.5 for chunk overlap and prompts = 180M input; output ≈ 20% = 36M. A cheap tier (≈ $0.25–0.5 per M in, $1–2 per M out) costs ≈ $80–160; a mid tier (≈ $3 per M in, $15 per M out) costs ≈ $540 + $540 = **≈ $1,080** | ≈ $0.1k–1.1k (illustrative prices, not verified) |
| Storage | Text ≈ 60k words × 10,000 h ≈ 600M words ≈ 4 GB. Audio is not retained | negligible |

*Backfill total: about $2k–6k.*

*Ongoing, assuming 3 h/week of new output per landmark (UNVERIFIED; the seed list should measure it): 500 × 3 = 1,500 h/week*

- Speech-to-text: AssemblyAI ≈ $255/week ≈ $13k/year; Deepgram ≈ $690/week ≈ $36k/year.
- Extraction at a mid tier: 1,500 / 10,000 × $1,080 ≈ $160/week.
- Daily Jev-style tagging against existing questions should be far cheaper than full extraction.
- Cost control: transcribe only what extraction needs. Sample per niche (the memo's representative-sampling rule) instead of exhaustively. Publisher transcripts cost $0.

**Copyright and fair use (not legal advice; get counsel)**
- Recorded speech is copyrighted expression; a full transcript is a reproduction or derivative of it. *Ideas and propositions are not copyrightable* (17 U.S.C. §102(b), the idea/expression distinction). A neutral, speaker-independent proposition is unprotected *idea*.
- **Internal, non-public** processing of full transcripts to extract information is transformative, non-expressive use. Analogies: *Authors Guild v. Google* (2d Cir. 2015), where full-text scanning for search plus snippets was held fair use; and *Bartz v. Anthropic* (N.D. Cal., June 2025), where training on lawfully acquired books was held fair use but use of pirated copies was not. That last ruling means **lawful acquisition matters**. *Per the correction:* public captions pulled outside the official API are a ToS gray area rather than pirated copies, but this is one reason to keep the counsel read in scope and to keep full transcripts internal.
- **Public layer.** Publish propositions (paraphrase), short quote anchors (about one sentence, enough to verify), speaker, date, and a deep link with timestamp to the original. Never publish full transcripts or audio. This drives traffic *to* the source, which also helps the fourth fair-use factor (market effect). Honor takedowns, and let landmarks annotate or dispute placement.
- **Retention.** Keep full transcripts as an internal, access-controlled cache only as long as needed for re-extraction and audit. Store word-level timestamps for the anchored spans permanently.

**Recommended pipeline (revised 2026-10-30 to the decided hybrid)**
1. **Seed list → source registry.** For each landmark, record YouTube channel, podcast RSS, publisher transcript URLs, Substack, and an opt-in status.
2. **Acquire (hybrid)**:
   - **Primary: YouTube public captions/auto-captions** via a paid transcript service (preferred at scale) or a transcript library such as `youtube-transcript-api`, with a **paced backfill** (throttled per channel, spread over weeks) to stay under rate limits and avoid IP blocks.
   - **Complements:** publisher transcripts (free, already public); podcast RSS audio → STT with diarization, used where content is audio-only, where auto-captions are poor, or where speaker separation matters.
   - **Fallbacks:** landmark opt-in channel connection via OAuth (fully ToS-compliant; also unlocks creator-uploaded tracks); licensed vendor data with redistribution terms.
   - Log the YouTube ToS gray area in the risk register; monitor block rates and switch a channel to the RSS/STT or opt-in route if it becomes unreliable.
3. **Normalize** to a word-timestamped, speaker-labelled transcript, plus voiceprint- or metadata-based speaker naming with confidence.
4. **Extract**: Topology Live-style quote-anchored propositions. Drop any proposition whose anchor span does not string-match the transcript. Rewrite neutrally, merge into the proposition bank (Society Library-style claim IDs with many anchors), and tag layers with Jev.
5. **Publish** propositions + anchor quote + timestamped link/embed. The full transcript stays internal.
6. **Govern**: takedown channel, landmark dispute/annotation, and a corrections loop feeding classifier labels.
7. **Flagship event maps**: YouTube captions are acceptable as the fast first source (speed to publish matters); re-check speaker attribution against the official podcast audio or an opt-in source before publication where available.

---

## How this answers the governing question (layering + validation)

- **Layering.** This brief adds a *dynamic* layer on top of the static map: reciprocal opening and narrowing measured over time per person and per cluster. It also adds a *question layer*: EGP-style base → branch genealogy, which sits above propositions and selects which axes to show (the memo's "each live question chooses its axes"). The Society Library model fixes the bottom layer: one proposition node, many quote anchors.
- **Overload control.** Users see a question, a handful of statements, and their nearest clusters. The 20+ relation types and full anchor sets stay behind a "show sources" affordance, much as Society Library papers sit over their maps.
- **Validation**:
  1. *Fidelity*: the described cluster's ratification rate of notes and proposition paraphrases.
  2. *Extraction precision*: the anchor string-match rate, plus human audits against a sample of Society Library-mapped claims where topics overlap (an external benchmark).
  3. *Opening*: perspective-taking accuracy on held-out cards, compared against an engagement-ranked baseline.
  4. *Placement*: the landmark dispute rate, and "that's not me" corrections per 1,000 placements.

---

## Reusable assets / design implications

- **Ranking objective.** `score(item, user) = E[Δ perspective-taking accuracy on under-described clusters] + λ·bridging_score − μ·hardening_prob − ν·predictability`, subject to finite-session constraints (R1–R8).
- **Schema additions.**
  - `Question{id, parent_id, base_question_id, origin_cluster, created_at, adopted_by[]}`, giving EGP branch genealogy plus lineage.
  - `Proposition{id, neutral_text, layer, anchors[]}` with `Anchor{source_url, t_start, t_end, speaker_id, speaker_conf, quote ≤ ~1 sentence}`.
  - `Note{author_cluster, target_cluster, fidelity_votes(from target), portability_votes(bridging MF)}`.
- **Status labels, not verdicts** (Society Library): "not yet ratified", "ratified by B", "B is split", "anchor disputed".
- **Opt-in landmark portal**: connect a channel, dispute placement, annotate. This gives a fully ToS-compliant fallback for YouTube captions and builds trust.
- **Partnership candidate**: the Society Library as a fidelity benchmark and seed-map source (do not contact without Benjamin).

## Risks & open questions

- **Measurement gaming.** Users could learn to predict outgroup reactions cynically without understanding them. Mitigation: ratified descriptions remain the primary reward; prediction is only a feed signal.
- **Graduated-distance rule (R3).** It is a hypothesis and needs an A/B test. Some people open faster from a shock.
- **Coverage gap.** ~~Landmarks who are YouTube-only cannot be ingested compliantly without opt-in.~~ *Revised per the correction:* with YouTube captions as the primary source, YouTube-only landmarks are covered. The remaining gap is short-form/TikTok-native scenes (e.g., looksmaxxing) and channels where captions are blocked or poor. Measure the gap in the seed-list work.
- **YouTube ToS gray area and blocking.** Automated caption pulls are outside YouTube's ToS; at scale expect rate limits and IP blocks. Mitigation: paid transcript service, paced backfill, per-channel fallback to RSS/STT or opt-in. Tracked in the risk register, not a blocker.
- **Diarization errors.** Speakers misattributed in multi-speaker shows would put words in the wrong mouths, the highest-harm failure. Require speaker confidence thresholds for publication.
- **Legal.** Counsel should review the fair-use posture for internal transcript caches and public quote anchors, alongside the existing X political-inference legal read.
- **Unverified items:**
  - the AFTMC episode that first states reciprocal narrowing;
  - any Vervaeke text applying it to algorithms;
  - the Landry Stoa 2020 recording;
  - EGP outputs;
  - "papers of record" as Society Library terminology;
  - Society Library crowd or Community-Notes-like work;
  - authors of arXiv 2506.24118;
  - third-party transcript API terms;
  - per-landmark weekly output volume.
- **Not fetched (permission prompts timed out):** societylibrary.org; developers.google.com/youtube/v3/docs/captions/download; arxiv.org/abs/2506.24118; the Foresight Institute Working Group 7 summary (Society Library automated mapping).
- **Vault**: Parachute has only a short Twitter DM thread with Jamie Joyce (friendly, 2021–2024). A Fathom note, "Civic Innovation Summit!" (2024-02-14), ranked high for her name, but its content was not reviewed. No vault notes were found on Landry or reciprocal opening.

## Sources

- Olshonsky, A. "Addiction Is Between You and the World," *Deep Fix*, 2022-12-23. https://deepfix.substack.com/p/addiction-is-between-you-and-the
- John Vervaeke on *This Past Weekend w/ Theo Von* #462 (transcript). https://rosetta.to/u/theovon/john-vervaeke-this-past-weekend-w-theo-von-462
- Jim Rutt Show EP 143, John Vervaeke Part 1 (transcript). https://jimruttshow.blubrry.net/?p=3299
- Petersonsphere glossary, "Reciprocal Narrowing." https://petersonsphere.github.io/Petersonsphere/Glossary-of-Terms/Reciprocal-Narrowing
- AFTMC Ep. 13, "Buddhism and Parasitic Processing" (listing). https://metacast.app/podcast/dr-john-vervaeke/0YbNdI5Y/ep-13---awakening-from-the-meaning-crisis---buddhism-and-parasitic-processing/rIcFQ22k
- EGP site. https://egp.community/ and https://egp.community/what-is-egp/
- Life Itself wiki, "Ephemeral Group Process." https://notes.lifeitself.org/ephemeral-group-process
- Jim Rutt Show EP 153, Forrest Landry on Small Group Method (transcript). https://jimruttshow.blubrry.net/?p=3679
- Jim Rutt Show Currents 076, Jamie Joyce on The Society Library (transcript). https://jimruttshow.blubrry.net/?p=4187
- Joyce, J. "Your Attempt To Refute Argument Maps Will Not Work," 2026-05-06. https://justjamiejoyce.substack.com/p/your-attempt-to-refute-argument-maps
- Deep Tech Week, Society Library profile. https://www.deep-tech-week.com/organizations/the-society-library
- YANSS 292, Society Library. https://youarenotsosmart.com/2024/07/22/yanss-292-how-one-organization-is-attempting-to-end-analysis-paralysis-by-creating-a-library-of-our-collective-arguing/
- Wojcik, Coleman et al., "Birdwatch: Crowd Wisdom and Bridging Algorithms…" (2022). https://arxiv.org/abs/2210.15723
- "Scaling human judgment in Community Notes" (2025; not fetched). https://arxiv.org/abs/2506.24118
- Polis / Computational Democracy Project (not fetched). https://compdemocracy.org/ ; vTaiwan (not fetched). https://info.vtaiwan.tw/
- YouTube Data API error reference. https://developers.google.com/youtube/data/reference/rest/v3/errors
- Stack Overflow Q41087864, third-party caption download (Kiwix mirror). https://kaweah.freedombox.rocks/kiwix/content/stackoverflow.com_en_all_2023-11/questions/41087864/youtube-api-v3-download-captions-from-third-party-videos-without-asking-for-au
- YouTube Terms of Service. https://www.youtube.com/terms
- Speech-to-Text API Pricing 2026 (vendor-adjacent). https://convertaudiototext.com/blog/speech-to-text-api-pricing-2026
- 17 U.S.C. §102(b); *Authors Guild v. Google*, 804 F.3d 202 (2d Cir. 2015); *Bartz v. Anthropic* (N.D. Cal., June 2025). Cited from prior knowledge; not fetched in this session.
- Parachute vault: `vault/messages/twitter/jamie-joyce-twitter`; `vault/meetings/2024-02/2024-02-14_civic-innovation-summit` (not reviewed).
