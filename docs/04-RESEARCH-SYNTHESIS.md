# Dialogos Arena: Research Synthesis (C1)

**Author of record:** Benjamin Life (@omniharmonic). **Compiled:** 2026-10-30 from wave-0 briefs A1–A5 and wave-1 briefs B1–B9 (in `/home/claude/dialogos-arena/`). B6 (AI agents and ethics) was integrated later the same day as §9. B7 (Girard, hyperstition and the mimetic state machine) and B8 (open agents, registries, token incentives and strategy markets) were integrated after that: B8 revises §9 into the Open Agent Charter, and both feed the new §10, the integration game. **Sources are now A1–A5 and B1–B9.** B9 (reciprocal opening, Landry's EGP, the Society Library and the transcript pipeline; `wave-1/B9-reciprocal-opening-landry-society-library-transcripts.md`) was integrated last, with a correction decided by Benjamin on its transcript findings: **YouTube transcripts remain the primary source** (a ToS gray area logged as a risk, not a blocker); podcast RSS + speech-to-text and landmark opt-in channel connection are complements and fallbacks (§2 D21, §11.1, R49).
**Design update (2026-10-30).** This version incorporates the **Design Dialogue Memo of 2026-10-30** (`/home/claude/dialogos-arena/design/DESIGN-MEMO-2026-10-30.md`; Parachute `vault/research/dialogos-arena/design-memo-2026-10-30`), held between Benjamin and Claude after the research swarm. Its decisions are **decided** and **supersede earlier recommendations in this document where they conflict**. The new §2 lists each decision and what it supersedes; sections 3 onward were renumbered (old §2 is now §3, and so on) and revised in place. Where a passage still reflects the pre-memo recommendation, it is marked *superseded* and points to §2.
**Status:** the base document that the specs will be written from. It is firm where the evidence is strong and says so where it is not.
**Conventions:**
- **UNVERIFIED** is carried forward from the source briefs.
- Brief codes in brackets, e.g. [A3], point to where the evidence lives.
- "Arena" means Dialogos Arena.

---

## 1. Executive summary

**Thesis, restated in light of the research.** Civilization's dialectic is best understood as a *dialectic of integration*. A position is sublated: cancelled, preserved and lifted, as in Hegelian *Aufhebung*. Change happens by incorporation (symbiogenesis), not by one thesis defeating another or by meeting halfway.

Living cultures need requisite variety and real contact between interpretive frameworks. That contact now happens online, on infrastructure owned by capital that profits from rivalry. The Arena is **contact infrastructure for an ecology of ideas**, not a market. It has three parts:
- **SEE** makes the grammar beneath opinions legible.
- **MEET** scaffolds dialogos in which both parties are changed.
- **MOVE** rewards *metabolizing* across clusters without paying for blandness or homogenization.

**The most consequential findings:**

1. **Each signal measures something different.** The social graph measures belonging at best, and the follow graph mostly measures *attention*: people follow figures they oppose because those figures matter (memo §7.1; §2 D10). Stance on shared propositions measures belief. Raw embeddings measure only topic. In Dialectical Topology's own data, embeddings could not tell the speakers apart (silhouette −0.009) [A2]. Off-the-shelf sentence models put "I love X" next to "I hate X" [B4].
2. **The unit of a population map is propositions × stances, not per-person graphs.** Topology Live's design (speaker-independent propositions, per-person stances, speech acts, stated vs inferred) replaces Ontography's private hairballs. The doubtful 4/3/6/1% overlap Ontography reported was largely an artifact of capping comparison at 60 pairs [A1, A3]. **Decided (§2 D12–D14):** the bank is seeded by quote-anchored extraction from ~500 US landmark voices' public output (YouTube, podcasts, Substack, posts), and individuals are placed by reacting to its statements.
3. **Worldview space has at least two axes.** A 2026 refit of Community Notes found an "institutional trust" axis that does not depend on left/right [B2, B4]. Kevin Owocki's Atlas also uses two named axes [A5].
4. **A map is accurate only if the people on it can ratify it.** That means quote-anchored stated claims, inferences rendered translucent, holders confirming their placement, steelman confirmation, and held-out prediction [A1, A3, B1, B4]. **Decided (§2 D1–D2):** this becomes the system's *gradient*: how accurately each cluster describes every other cluster in terms the described cluster would sign, carried by Community-Notes-style **cross-cluster notes**.
5. **The X API is contractually hostile to this use.** Its policy forbids deriving political inferences about users, with only an aggregate carve-out [B5]. ~~Build on consent-only inputs: X archive upload and AT Protocol.~~ **Superseded (§2 D11–D15):** the map no longer depends on X. The front door is **statement reactions** on a terrain built from **landmark public output**; X OAuth and archive upload become optional enrichments, and the X legal read drops in priority.
6. **MEET aims at meta-consensus, not consensus.** Success is a jointly ratified statement of *where and why* people differ. Synthesis is optional, and paradox and aporia are valid ends [B1, A4]. The Anti-Debate format adapts cleanly to an asynchronous form [A3].
7. **"Being changed" means expansion, not stance flips.** It should be a composite of confirmed steelmans, stated updates, signed higher ground and comprehensiveness deltas [A3, B2].
8. **Every plural mechanism consumes a group map, and the best-documented one has a known harm.** COCM penalizes tight-knit communities, exactly the bioregional shape Benjamin serves [B3]. Start MOVE as **reputation only**.
9. **Integration must be a relational capacity, never a developmental rank.** Stage labels on clusters would destroy legitimacy and repeat the colonial pattern Benjamin has himself critiqued [A4, B1].
10. **Kevin's Atlas already provides a tribe-level overview.** What it lacks is individual placement, a claim graph, consent and a disclosed method. Benjamin's layers fill exactly that gap [A5]. **Decided (§2 D12):** Kevin's 58 ontologies are one of three seed sources for the landmark list, with Limberg–Barnes's tribes and Benjamin's brainstorm.
11. **Agents are welcome if they are visible; open presence, invited contact.** Documented state AI influence operations mostly achieved low measured reach; the harm they do is to trust and provenance, not votes [B6]. Disclosed AI dialogue persuades about as well as covert, so covertness buys nothing [B6]. A covert "prosocial" bot cannot be told apart from an influence operation, because every test in use judges *means*, not ends [B6]. Disclosure plus a public registry satisfies two of those means tests (hidden identity, simulated coordination); the third, contact, is settled by platform rules: X permits automated replies and mentions only after the user has shown intent to be contacted [B8; checked against X's rules, VERIFICATION §E]. Arena agents therefore follow the **Open Agent Charter (O1–O15)**: disclosed, registered, bound to a personhood-verified and bonded operator, with a declared **non-directional aim** (meta-consensus, not conversion). They may **publish openly** on platforms, including labeled side-by-side multi-framings, and people can follow, mute or block them. They **contact only people who invited it**. A seasonal **directional-shift audit** makes any agent that consistently moves first-order views ineligible for reward. They earn only on **ratified outcomes**, never on reach or landscape shift. Their best defensive role is still making inauthentic amplification visible on the map, in aggregate (§9).
12. **The integration game is a mimetic state machine with a process objective, not a destination.** The layered map can be run over time as a regime classifier over an 18-variable state vector. Its new first-class layer is the **understanding matrix R** (how accurately each cluster represents each other, as ratified by the represented). The objective maximizes ratified understanding and meta-consensus under hard constraints: diversity floor, no scapegoat, authenticity, **no belief destination**, deepening parity. The machine's main job is to tell **integrative meta-consensus apart from "bridging against" a third party**, which a naive bridging metric cannot do [B7]. Benjamin's strategy-prediction idea is workable only as a **randomized strategy tournament** with sealed, reputation-scored forecasts and resolution on held-out panels, not as a money market. The **resolution oracle** (holder-rated fidelity on panels) is the open problem every design rests on [B8] (§10).
13. **The defensible Girardian move is recognition granted by the represented.** Girard's only remedy is renunciation, which no mechanism can produce, and paying for it crowds it out [B7]. What incentives *can* do is change the object of rivalry: make the reward **non-scarce, pair-bound (dyadic) and conferred by the other cluster**, so the rival becomes the source of recognition instead of its obstacle. The two biggest risks are also Girardian: "polarizers" becoming the new scapegoat, and two clusters bridging *against* a third. Warmer feelings alone do not improve democratic norms (Broockman et al. 2022; Voelkel et al. 2024), so the democratic and incentive layers form **one loop, SEE → MEET → MOVE → DECIDE**, that pays off only when accurate mutual representation is coupled to venues with real authority [B7] (§10.10).
14. **The design dialogue fixes the architecture (§2).** The gradient is ratified cross-cluster description; the incentive (engine) is paired with a living map of live threads (magnet); and the map is built from **landmark content, not the social graph**: quote-anchored propositions from ~500 US public voices, individuals placed by Polis-style statement reactions, cross-cluster encounters as edges, and **event maps** of recorded dialogues as the first public product. Syntheses are rewarded only retroactively, by lineage.

---

## 2. Design decisions (Oct 30 design dialogue)

**Source:** *Dialogos Arena — Design Dialogue Memo*, Benjamin Life (@omniharmonic) in thought partnership with Claude, 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`; Parachute `vault/research/dialogos-arena/design-memo-2026-10-30`). These decisions are **decided**. Where they conflict with a research recommendation elsewhere in this synthesis or in the briefs, the decision wins; the research evidence is kept because it still explains *why* and still sets the guardrails. Memo section numbers are given as "memo §n".

### 2.1 Strategic posture

The Arena aims to be **doubly mimetic** and deeply viral: people join because others are on the map, and the map is itself a picture of mimesis (who resembles whom). It should appeal to sophisticated audiences who know mimetic theory (Thiel-, Andreessen- and prediction-market-adjacent) while carrying the thesis they lack: **the dialectic is an inherent part of participation in the polis.** The easy viral loop, "find your tribe and see your enemies," hardens clusters, so every design choice points mimetic energy toward understanding. The process must yield **visible, concrete outputs** (maps, event maps, ratified notes, reports), not open-ended facilitation (memo §1).

### 2.2 The decisions

| # | Decision | Supersedes (old section / recommendation) | Rationale |
|---|---|---|---|
| D1 | **The gradient** is how accurately each cluster describes every other cluster, in terms the described cluster would sign. Success is **meta-consensus**, not convergence (memo §2). | Makes explicit the "integrative gradient" rows of §3 and the R matrix / objective J of §10.3–10.4: R is now *the* gradient, not one variable among 18. Supersedes any reading of MOVE as rewarding synthesis or bridging per se. | Mirrors anti-debate, where a ratified steelman gates the next phase. Cannot be faked by blandness; requires nobody to change their mind. |
| D2 | **Cross-cluster notes** (Community-Notes style; lineage Jamie Joyce / Society Library, Audrey Tang / vTaiwan, Community Notes). A member of A writes a note describing B. Two signals: **fidelity** (only B's members can grant "that's us, I'd sign that") and **portability** (A and third clusters find it clarifying). A split in B's ratification reveals a **sub-cluster**. Notes describe what B believes and why; they **never judge** (memo §3). | Extends design A's fidelity gate (§8.1), R1 and R4 (§10.6) and the cluster card (§6.4 level 1) into one artifact. Replaces "holder-ratified cluster card drafted by the Arena" as the main ratification object: cards are now assembled from ratified notes. | Makes the gradient concrete and crowd-produced; fidelity cannot be self-granted; split ratification sharpens the map instead of failing. |
| D3 | **Novelty is not rewarded at proposal.** A synthesis may be proposed only after **ratified steelmen exist in both directions** (memo §4). | Supersedes §3 "Reward synthesis with QF" and design A's crediting of "syntheses that survive" at proposal time (§8.1); the MEET integration step (§7.1 step 7) is now gated on two ratified steelmen. | LLMs make plausible "third perspectives" nearly free; most are midpoints dressed as transcendence. |
| D4 | **Syntheses are rewarded retroactively by lineage**: uptake by *both* parent clusters, gathering adherents, appearing as a new map region tracing to both parents. A clean, mutually understood disagreement is a **success**. **A better question** both sides keep asking is a first-class synthesis fruit (memo §4). | Refines design C (§8.1, retroactive metabolism funding) into the default synthesis reward; adds "better question" to the synthesis types (§5.5). | Novelty proven by descendants, not claimed by authors; removes the incentive to manufacture fake syntheses. |
| D5 | **Scenius: deepening vs hardening.** Within-scene contribution is rewarded when the scene's own thesis gets richer (new questions, internal disagreements worked through, ideas taken up), never when status is earned *against* another cluster. **One currency: lineage** — uptake within the scene is scenius; uptake across scenes is synthesis (memo §5). | Specifies the "separate within-cluster deepening track" (§8.1) and constraint C5 (§10.4), and gives it a detector. | Rewarding in-group contribution can fund purity spirals; hardening is detectable because it is defined against an outgroup. |
| D6 | **Engine and magnet.** The engine is the incentive gradient (D1–D5). The magnet is the **living map**, a place to return daily and watch culture think. Its core object is the **live thread**: an open question a scene is working through, which moves, splits and leaks across boundaries. The map becomes a **genealogy of questions** (memo §6). | Supersedes "See where you sit" as the habit loop (§3) and the static Level-0 overview as the home view (§6.4). | Self-placement is a one-time curiosity; a live map of the collective conversation is a habit. |
| D7 | **Axes chosen per question.** The data holds many dimensions; each live question picks the 2–3 axes it actually splits people along, and the map reorients around the thread you follow (memo §6). | Refines §5.6 and Q5: the axis library is per-thread, with ≥2 dimensions still the floor globally. | Humans see two or three dimensions; one fixed projection hides most fault lines. |
| D8 | **Threshold people are the protagonists.** People who translate between scenes are featured, and the map constantly invites you to become one (memo §6). | Extends matching factor 3 ("integrators, not sparrers", §7.2) into the product narrative. | Guards against spectatorship (Buber; Limberg's "post-meta" warning). |
| D9 | **Reciprocal opening as the feed rule**: rank by what *widens*, never by what holds you (memo §1). *Attribution [B9]:* "reciprocal narrowing" is Marc Lewis's account of addiction, adopted by Vervaeke; "reciprocal opening" is Vervaeke's inverse, tied to love; "running the algorithm in reverse" is Benjamin's extension. Operationalized as ranking rules R1–R8 and measured by perspective-taking accuracy across clusters (§8.6). | New. Complements §8.3 (pair bridging with de-amplifying contempt). | Engagement ranking produces reciprocal narrowing; the Arena runs the feed in reverse. |
| D10 | **Follow ≠ belief.** The follow graph maps **attention**, not agreement (memo §7.1). | Supersedes §3 row "The social graph is 'most powerful' … confirmed for belonging" and S0 Belonging as the phase-1 core (§6.1, §6.7). Follows survive only as an optional attention signal. | Many people follow figures they oppose because those figures matter culturally. |
| D11 | **X is not the front door.** X API follower pulls are expensive and restrict political inference; archive uploads take a day or more. The idea map must not depend on X's terms (memo §7.1). | Supersedes Q2 (archive + AT Protocol as v0 intake), §11.1 priority order, §6.7 phase 1 and spec "Consent, Identity & Intake". X OAuth/archive become optional enrichment; the legal read on X's clause drops to low priority. | Speed of first contact and independence from one platform's terms. |
| D12 | **Landmark seed list.** ~500 US-focused public voices, **2–3 per niche**, as many semi-mainstream niches as possible (e.g., looksmaxxing, neoliberals, fiscal conservatives), seeded from **Limberg & Barnes's tribes, Kevin Owocki's 58 ontologies and Benjamin's brainstorm**; data reveals missed clusters, named afterward. A **stable core panel** is kept, with newcomers marked (memo §7.2, §9). | Supersedes Q3 ("consenting landmarks only") and refines Q11 (Atlas now a seed source). | Bounded, representative scope; a fair share for every scene, loud or quiet. |
| D13 | **Public intellectuals may be placed from their public output.** This describes the clustering of a worldview, not a political categorization of a person. Every landmark gets a **dispute / annotate** affordance (memo §7.2). | Supersedes the §6.1 contradiction resolution ("consenting members and consenting landmarks only"), Q4, the glossary's "Landmark" entry and red line 1 *as applied to public figures' public output*. Red lines for private individuals are unchanged (§11.2). | Landmarks' public output is what makes the terrain exist before anyone joins; GDPR/Art. 9 exposure is handled by describing clusters, not scoring persons (see §11.2, R13). |
| D14 | **Multi-platform ingestion, sampled by niche, edges from content.** YouTube transcripts, podcasts, Substacks and posts. Sampling is by niche, not volume. Edges come from content: who quotes whom, who appears on whose show, who argues with whom by name. **Bluesky** is a low-friction channel but demographically skewed, so it cannot carry the map alone (memo §7.2). | Supersedes S0's retweet/follow multiplex as the edge source and AT Protocol as a priority-1 terrain source (§6.1, §11.1). | Cross-cluster encounters carry far more meaning than follows. |
| D15 | **Extraction pipeline.** (1) Quote-anchored claims; unsupported claims are discarded. (2) Neutral, speaker-independent propositions merged into the **shared proposition bank**. (3) **Jev** layer tagging (real / how we know / what matters / empirically true / what to do). (4) **Statement selection**: cluster-splitters, scene-internal live threads, surprising cross-cluster unifiers. (5) Every statement links to its **source clip** (memo §7.3). | Moves S3 (§6.1) from phase 3 to phase 1 and roots it in landmark content rather than consenting members' feeds. | Fidelity lives or dies here; guards against AI-invented beliefs (Ontography's weakness). |
| D16 | **Ideas at scale, cheaply.** Weekly, a stronger model reads a sample of landmark output and proposes the **live question battery**; Jev labels cheaply against it. **No surveys**: people only correct mistakes ("that's not me"), and each correction becomes a labeled example (memo §7.4). | Supersedes S1's fixed 10–30-question per-person battery and the MFQ-2 / self-report onboarding items (§6.1, §12). | The battery comes from what the culture is actually contesting now. |
| D17 | **Individuals are placed by statement reactions**: agree / disagree / pass on real statements from across the map (Polis-like), gamified by **guessing who said it** before the reveal. This placement **defines cluster membership for ratifying notes** (memo §7.5). | Supersedes Barberá-style follow-graph placement (§6.1 S0) and promotes S5 (revealed ideal points) from phase 4 to phase 1. Replaces "long-run membership signals" in design A (§8.1). | Membership by what you endorse, not whom you follow, makes ratification much harder to game; platform-independent. |
| D18 | **The first sixty seconds:** react → appear as a dot on an existing terrain → see three nearest landmarks → **threshold reveal** (which clusters you sit between) → **twist card** (the farthest landmark you agree with on one question) → invitation to describe the farthest cluster. The shared **status prize** is "the other side signed my description of them" (memo §8). | Supersedes the Level-0 "Venn of you against your 2–3 nearest clusters plus feed-share" first view (§6.4). | Understanding, not placement, is what gets shared; the twist card is the viral moment. |
| D19 | **Time: the four-dimensional map.** Everything timestamped; propositions record first appearance and speaker; **cluster lineages** (births, splits, merges, fadings); **thread life cycles** (emerge, spread, fork, cross, go quiet); **backfill** from YouTube/podcast archives; stable core panel so sampling change does not masquerade as movement. **Nested horizons:** daily pulse, weekly weather, monthly deep pass, each with a product (memo §9). | Extends the Atlas "nightly cadence and versioned snapshots" borrow (§6.3) and the state vector's windows (§10.3). | Real historical arcs on day one; a reason to return each day, week and month. |
| D20 | **Event maps are the flagship.** Topology Live extraction runs on **any** dialogue, interview, debate or monologue (not only anti-debate format). An event map shows each speaker's starting position, where they met, where they diverged and at which layer, missed openings, and **the ripple** in following days. **Speed to publish** (within a day) drives virality. The first public event is **surprising but less incendiary**; the most charged (e.g., a Nick Fuentes interview) wait until the method has earned trust (memo §10, §11.1). | Supersedes Q12 and Q13 (first pilot = Lepp crypto-vs-localism anti-debates; async first) as the *first public product*: async MEET remains the participant protocol. | Concrete, fast, newsworthy output; avoids a launch defined by platforming accusations. |
| D21 | **Seeding by dialogue extraction.** Scrape YouTube and podcast transcripts for the full landmark set as the **baseline content** of the map. Each cross-cluster encounter is an **edge**; aim to connect all clusters through chains of encounters. Never-met pairs become **invitations for Arena-hosted anti-debates** chosen to fill the biggest holes. Caveats: **bridgers ≠ cores** (event content shows clusters at their most open, so everyday output stays the baseline); Topology Live's live attribution is unvalidated, so **seed from recorded content first** (memo §11.2–11.3). **B9 correction (2026-10-30, decided by Benjamin):** B9 first concluded YouTube transcripts were effectively off the table (official `captions.download` is owner-only; ToS bans scrapers). That overstated it. Pulling public captions/auto-captions via transcript libraries (e.g., `youtube-transcript-api`) or commercial services is routine and feasible; it is a **ToS gray area** with rate-limit / IP-block risk at scale (R49), mitigated by a paid service and paced backfill. **YouTube transcripts stay primary**; podcast RSS + speech-to-text, publisher transcripts and landmark opt-in channel connection are complements and fallbacks; publish propositions with short quote anchors and timestamped links only (§11.1). | Supersedes "seeded from consenting members and Anti-Debate corpora" (§6.7 phase 3) and A3's framing of Topology Live as event-only tooling. Turns matching (§7.2) into gap-filling. | Dialogue forces people to say what they believe, why and at which layer; tweets capture little of a mimetic structure. |
| D22 | **Lineage to Landry.** Forrest Landry's Ephemeral Group Process (inquiry-based, collectively developed questions, small groups at scale, a community question archive; The Stoa, 2020) is noted as a rhyme and **inspiration only** (memo §6). *B9:* two elements are borrowed, **question genealogy** (base → branch questions, archived and fed forward) and **routing people by question** (§6.5); the public record is thin (no outputs or case studies found; the Stoa recording not located). | None. | It never delivered a full stack with concrete outputs (Benjamin's critique, consistent with B9). |

### 2.3 What stays

Everything not listed above stands: the taxonomy (§5), the async anti-debate protocol (§7.1) as the participant protocol, the Open Agent Charter (§9), the integration game's hard constraints C1–C5 and reward-conferral principle (§10), the red lines for private individuals and agents (§11.2), and the validation gates (§12). The memo's open loops are carried into §15 as Q31–Q37; B9 adds Q38 (contact the Society Library).

---

## 3. Reframe: what the research changes

| Original framing | Research-informed reframe | Why |
|---|---|---|
| "Free market of ideas" | **Ecology or commons of ideas with protected otherness**; contact infrastructure | Benjamin's own 2026 thesis is that capital "ate the outside" and commodifies critique [A4 P3]. Mill's strongest arguments are about *contact*, not market selection [B1]. Engagement markets reward spread [B1, B2]. |
| Consensus or synthesis as the goal | **Meta-consensus** as the baseline success; synthesis is a possible outcome, not a quota | Dryzek and Niemeyer; Mouffe's "enemies into adversaries" [B1]. DC forced one resolution, one transcendence and one paradox per dialectic, which manufactures integration [A2]. |
| Thesis + antithesis → synthesis; "meeting in the middle" | **Sublation** (determinate negation) and **higher ground** over common ground | "Thesis-antithesis-synthesis" is a popularization, not Hegel's method [B1]. Lepp: aim for higher ground, not the middle [A3]. Never average. |
| "Memetic/mimetic tribes" used interchangeably | **Two layers.** *Mimetic* = relational (who amplifies, imitates and opposes whom: the social graph and shared antagonists). *Memetic* = content (claims, frames) | Girard vs Dawkins [B1]. Benjamin treats Girard as the opposing camp's anthropology, so adopt mimetic analysis explicitly as a *lens*, not as a worldview [A4]. |
| An upward "integrative gradient" | **Integration as relational capacity**: how accurately you represent other frames, as ratified by their holders. Anyone in any cluster can grow it. **Decided (§2 D1–D2):** the gradient is exactly this, at cluster level: how accurately each cluster describes every other, in terms the described would sign, carried by **cross-cluster notes** with fidelity and portability signals. | Benjamin's critique of integral theory's colonial shadow [A4 P13]; the stage-model critique [B1]; memo §2–3. |
| "Tribes" as things to find | **Clusters** with soft membership. *Tribe-ness* (shared enemies, out-group hostility) is measured, not assumed. Scenes are not tribes. | Lightfoot's Liminal Web is a scene [A5]. Fraser's counterpublics need a right to enclave [B1]. |
| "See where you sit" as the product | The map is **a threshold to encounter**. Every "you are here" pairs with "who across the gap to meet." **Decided (§2 D6, D18):** placement is the first-sixty-seconds hook (threshold reveal, twist card); the habit is the **living map of live threads**, and the shared prize is "the other side signed my description of them." | Buber's I–It warning [B1]; Limberg's "post-meta" warning [A5]; memo §6, §8. |
| The social graph is "most powerful" | ~~Confirmed **for belonging**.~~ **Superseded (§2 D10, D14):** the **follow graph measures attention, not belief**, and is demoted to an optional attention signal. Edges come from **content**: who quotes whom, who appears on whose show, who argues with whom by name. Retweet edges still segregate and mention/reply/quote edges still cross over; graph proximity is not shared belief. | Conover; Barberá; Garimella [A5, B4]; memo §7.1–7.2. |
| Embeddings give the semantic landscape | **Topic terrain only.** Use stance-aware models or anchor-pair projection for belief. | [A2] test; Ghafouri et al. [B4]. |
| A claim graph per person | **A shared proposition bank**, individuals as sparse stance vectors, and claim graphs on demand (≤80 nodes). **Decided (§2 D15, D17):** the bank is built from quote-anchored, neutral propositions extracted from landmark public output; individuals become stance vectors through statement reactions. | [A1, A3, B4]; memo §7.3, §7.5 |
| "Offer up your X feed" via the API | ~~Archive upload (parsed in the browser) and AT Protocol; X OAuth only after legal review.~~ **Superseded (§2 D11, D17):** the front door is **statement reactions** (agree / disagree / pass) on a terrain built from **landmark content**. X archive and OAuth are optional enrichment; AT Protocol is one channel among several. | X political-inference clause; GDPR Art. 9 [B5]; archive waits of a day or more; memo §7.1. |
| Being changed = changing your mind | **Expansion**: frame-level learning (Bateson's Learning II), opinion *reordering*, confirmed understanding | Lepp [A3]; Goyal et al. 2026 [B2]; Bateson [B1]. |
| Reward synthesis with QF | **Reputation first.** Quadratic matching only with a payment leg, caps and sybil resistance. Keep a separate within-cluster "deepening" track. **Decided (§2 D3–D5):** no reward for novelty at proposal; synthesis only after ratified steelmen both ways; synthesis and scenius both rewarded **retroactively by lineage**; deepening is distinguished from hardening. | Costless QF "subsidizes Sybils"; COCM harms [B3]; LLM midpoints are nearly free (memo §4). |
| A single left/right axis and a single score | **Requisite variety at every level**: at least 2 axes, plural metrics, plural synthesis types | Ashby [B1]; Andreou & Sirivianos [B2]. |
| "Subtle" prosocial bots | **Disclosed open agents** under the Open Agent Charter: open presence, invited contact, bonded operators, a non-directional aim, directional-shift audits | Covert agents fail every means test [B6]. Disclosure and a registry pass two; platform contact rules settle the third [B8]. |
| An "integrative gradient" as an incentive | **Recognition granted across clusters**: non-scarce, pair-bound, decaying credit, conferred only when the represented cluster ratifies | Incentives cannot buy Girard's renunciation, but they can make the rival the source of recognition [B7]. Crowding-out evidence [B7, B8]. |
| A prediction market on strategies | **A randomized strategy tournament**: full-support random assignment, sealed forecasts with a proper scoring rule, code-resolved on held-out consented panels, reputation plus fixed prizes | Decision markets are incentive-compatible only with randomized decisions (Chen et al.). Prediction markets have documented insider, oracle and wash-trading failures [B8]. |
| Democracy vs the incentive game | **One loop: SEE → MEET → MOVE → DECIDE → SEE.** Understanding is public infrastructure; better policy depends on coupling to real venues | Lower affective polarization alone does not improve democratic norms. Correcting misperceptions and minipublics with binding links do help [B7]. |
| Reward novel syntheses when proposed | **Novelty proven by descendants.** Synthesis only after ratified steelmen both ways; rewarded retroactively by lineage (uptake by both parents, a new region); a better shared question counts; clean mutual disagreement is success (§2 D3–D4) | LLM "third perspectives" are nearly free and mostly midpoints (memo §4). |
| An engagement feed that holds attention | **Reciprocal opening**: rank by what widens, never by what holds you (§2 D9; Vervaeke's inverse of Lewis's reciprocal narrowing; ranking rules R1–R8 in §8.6) [B9] | Engagement ranking produces reciprocal narrowing (memo §1). |
| A static map you visit once | **A living, four-dimensional map** whose core object is the **live thread** (an open question), with question genealogy, cluster lineages and daily / weekly / monthly products (§2 D6, D19) | Self-placement is a curiosity; a live map is a habit (memo §6, §9). |
| Topology Live as anti-debate tooling | **Extraction for any recorded dialogue, interview or monologue**; event maps are the flagship product and the main seeding engine (§2 D20–D21) | Dialogue forces people to say what they believe, why and at which layer (memo §11). |

---

## 4. Glossary: unified terms

Use these terms in specs. "Avoid" lists collisions to prevent.

| Term | Arena meaning | Lineage | Avoid / do not confuse with |
|---|---|---|---|
| **Dialogos** | Dialogue in which each party is transformed, metabolically, through deeper context and new relationship | Benjamin; Socrates; Bohm | "debate", "discussion" |
| **Anti-debate** | Lepp's three-phase format: Clarifying Difference → Exploring Synthesis → Taking Stock (CC BY-SA 4.0) | Lepp / Synthesis Media; MacAskill 2017 | Debate-as-content |
| **Grammar / syntax** | The root ontological, epistemic and relational assumptions that decide which statements are even sayable; sets a **basin of attraction** | Benjamin [A4] | "Ideology" |
| **Interpretive framework / worldview** | A coherent pattern of stances across strata | Benjamin; Koltko-Rivera | "Meme" (Sperber's attractor critique) |
| **Cluster** | A data-detected group with soft membership weights w(i,g) | [B3, B4] | "Tribe" (reserve for clusters with measured tribe-ness) |
| **Tribe-ness** | A measured property: share of Combatants/Existential-Threat discourse, out-group hostility, low cross-cutting edges | Limberg & Barnes; Lightfoot [A5] | |
| **Scene** | Overlapping consumption without a shared enemy (Lightfoot's ~30% media-diet heuristic) | [A5] | Tribe |
| **Mimetic layer** | Relational structure: amplification, imitation, prestige, shared antagonists, scapegoat targets | Girard [B1] | Memetic |
| **Memetic layer** | Content: propositions, frames, topics | Dawkins → cultural attraction [B1] | Mimetic |
| **Belonging** | What the social graph measures at best. The **follow graph measures attention**, not belief (§2 D10). | [B4]; memo §7.1 | Belief; attention |
| **Proposition** | A speaker-independent canonical sentence in positive polarity, with type and stratum | Topology Live D5 [A3] | Ontography's per-person "node" |
| **Stance** | Attitude toward a proposition: accepts / rejects / suspends / accepts_conditionally / accepts_for_argument. Has a strength and a source. | [A3] | Topic |
| **Stance source** | `stated` / `implied_by_act` / `inferred`. Inferred stances are never scored. | [A3] | |
| **Status ladder** | Ontography's `inferred → stated → verified → retracted`, merged with Topology Live's provenance (§5.3) | [A1, A3] | |
| **Speech act** | The discourse function of an utterance. Steelman and attribution acts never commit the speaker. | Searle; [A3] | |
| **Commitment store** | Everything a participant is on record as holding: stated and quote-anchored | Hamblin, Walton–Krabbe [A3] | Inferred profile |
| **Stratum / layer** | Ontology · epistemology · axiology · empirical/predictive · praxis (§5) | Ontography, DT, Topology Live | Habermas validity (orthogonal) |
| **Presupposition** | What a stance requires. Always inferred, must pass a necessity test, rendered translucent. | [A1, A3] | Assumption-as-fact |
| **Epistemic basis** | How someone claims to know something (15 types) | [A3] | Warrant strength |
| **Crux** | A proposition C on which each party's disagreement depends, ranked by routing and stratum depth | CFAR double crux [A3] | Any disagreement |
| **Fault line** | A ratified statement of where and why two clusters differ (the meta-consensus artifact) | Dryzek [B1] | Ontography's "faultlines" filter |
| **Drift** | Same term, different sense. The most valuable verdict in comparison. | Ontography; DT [A1, A2] | |
| **Domain / temporal confusion** | Both views are right in different domains, scales or times | DT [A2] | |
| **Common ground / higher ground** | Shared ends, facts or framings / a position consistent with both commitment stores that integrates an element from each | Lepp; Topology Live [A3] | The "middle" |
| **Sublation** | Cancel, preserve, lift. The criterion for a valid synthesis. | Hegel [B1] | Compromise, averaging |
| **Synthesis type** | One of the unified set in §5.5, including *null* | DC; Topology Live; B1 | |
| **Meta-consensus** | Agreement on the nature of a disagreement and the legitimacy of the competing framings | Dryzek & Niemeyer [B1] | Consensus |
| **Aporia** | Productive perplexity; a valid end state | Socrates [B1] | Failure |
| **Steelman record** | A's steelman of B, scored by B as {captured, missed, distorted, added} plus confirmation | [A3] | |
| **Updates ledger** | Every change in attitude, strength or credence, with its trigger | [A3] | |
| **Expansion** | The Arena's sense of "being changed" (§7.3) | Lepp [A3] | Conversion |
| **Bridge node / edge node** | A person whose engagement crosses clusters. Split into **integrators** (positive or signed cross-cluster edges) and **sparrers** (negative edges, quote-dunks). | Burt; [B4] | |
| **Bridging** | Raising mutual understanding and trust across divides, not erasing conflict | Ovadya & Thorburn [B2, B3] | Bland agreement |
| **Integration (capacity)** | A person's measured, holder-ratified ability to represent other frames | [B1, A4] | Developmental stage |
| **Metabolize** | To actually incorporate an idea from another frame, as opposed to co-opting it | Benjamin [A4] | Consume |
| **Ideal point** | A person's coordinates on latent axes inferred from behavior (follows, votes, ratings) | Barberá; Community Notes [B4] | |
| **Holder ratification** | Members of a cluster endorse the description of their own cluster | Habermas, Dryzek [B1] | Expert labeling |
| **Signability** | "Would the speaker sign this canonical sentence?" | [A3] | |
| **Landmark** | A public voice (one of ~500 US figures, 2–3 per niche) placed on the map **from their public output**, with a dispute/annotate affordance; a stable core panel, newcomers marked (§2 D12–D13). *Supersedes* "a consenting public account". | memo §7.2, §9 | A private individual; a political categorization of a person |
| **Dark matter** | Non-consenting follows kept as salted hashes: they shape similarity but are never resolved or shown. *Now applies only to optional X-archive enrichment* (§2 D11). | [B5] | Anonymized graph (which is not anonymous) |
| **Detail dial** | Progressive-disclosure levels (§6.4) | Topology Live [A3] | |
| **Dialectic of integration** | Change by incorporation (symbiogenesis), as opposed to the dialectic of negation | Benjamin [A4 P4] | |
| **Gradient** | How accurately each cluster describes every other cluster, in terms the described cluster would sign. The quantity the system ascends (§2 D1). | memo §2; anti-debate | Ranking of worldviews; convergence |
| **Cross-cluster note** | A note written by a member of cluster A describing cluster B, Community-Notes style; describes, never judges (§2 D2) | Society Library (Joyce); vTaiwan (Tang); Community Notes | A fact-check; a verdict |
| **Fidelity / portability** | The two signals on a note: fidelity is granted only by B's members ("I'd sign that"); portability is cross-viewpoint clarity among A and third clusters | memo §3 | Helpfulness alone |
| **Lineage** | The single currency for idea credit: uptake within a scene = **scenius**; uptake across scenes = **synthesis**. Also the tracked ancestry of clusters and threads over time (§2 D4–D5, D19) | memo §4–5, §9 | Authorship claims |
| **Deepening / hardening** | Within-scene contribution that enriches the scene's own thesis / status earned against another cluster (detectable because it is defined against an outgroup) | memo §5; group polarization | |
| **Live thread** | An open question a scene is working through, which moves, splits and leaks across boundaries; the core object of the living map (§2 D6) | memo §6 | A topic; a single claim |
| **Threshold person** | Someone who sits between clusters and translates between scenes; the protagonist of the map (§2 D8) | memo §6, §8 | Bridge node as a pure graph metric |
| **Statement reaction** | Agree / disagree / pass on a real, source-linked statement (Polis-like); the way individuals are placed and the basis of cluster membership for ratification (§2 D17) | Polis; memo §7.5 | Survey items; follows |
| **Twist card** | The farthest landmark you agree with on one question; the shareable moment of the first sixty seconds (§2 D18) | memo §8 | |
| **Event map** | The terrain rendering of one recorded cross-cluster encounter: starting positions, meeting points, divergences by layer, missed openings, the ripple (§2 D20) | memo §11.1 | Debate scorecard |
| **Reciprocal opening** | The feed rule: rank by what widens; the inverse of engagement's reciprocal narrowing (§2 D9). Measured by perspective-taking accuracy across clusters (§8.6) | Reciprocal narrowing: Marc Lewis (addiction), adopted by Vervaeke; reciprocal opening: Vervaeke; "algorithm in reverse": Benjamin [B9] | Engagement |
| **Nested horizons** | Daily pulse, weekly weather, monthly deep pass, each with a published product (§2 D19) | memo §9 | |

---

## 5. The unified worldview taxonomy

### 5.1 Canonical strata (one table, every source reconciled)

| Stratum (canonical) | Core question | Ontography layer | Topology Live stratum · typical proposition types | Dialectical Topology claim type / tree branch | Limberg–Barnes columns | Typical epistemic bases |
|---|---|---|---|---|---|---|
| **Ontology** | What is real? What is a self? | `ontology` | ontology · definitional, conceptual, modal | `ontological` / ONTOLOGY (monism ↔ dualism) | (implied by Forebears) | deduction, definition, intuition |
| **Epistemology** | How do we know? What counts as evidence? | `epistemology` | epistemology · meta | `epistemological` / EPISTEMOLOGY (rationalism ↔ empiricism) plus 8 ways of knowing | Mental Models, Forebears | all 15; the mix *is* the epistemic fingerprint |
| **Axiology** | What matters? What is right? | `axiology` | axiology · normative | `ethical` / ETHICS (consequentialist ↔ deontological/virtue) | Sacred Values, Telos | moral_intuition, consensus, expert_testimony |
| **Empirical / predictive** | What is, or will be, the case? | evidence nodes (not a layer) | empirical/predictive · empirical, causal, predictive, counterfactual | "empirical" (in the essay, absent from the data) | Existential Threats | empirical_study, statistical, institutional_record, anecdote, direct_experience, forecast_judgment |
| **Praxis** | How should we act or transform? | `praxis` | praxis · prescriptive | `methodological` / METHODOLOGY (technique ↔ relationship) | Telos (as a programme) | practical reasoning schemes, historical_precedent, analogy |
| **Relational (mimetic)** | With whom do we belong, and against whom? | (none) | participants and stances (not a stratum) | speaker_dynamics (Flow lens); lineage (wiki layer) | Master Status, Campfire, Chieftains, Combatants | social graph, not text |
| *Higher ground* (derived) | What integrates both? | synthesis output | higher ground (6 constructions) | synthesis nodes; Steelman Arena | (none) | derivation from both stores |

**Contradictions resolved:**
- **"Empirical" as a stratum.** DT's data omits it, Ontography treats it as evidence, and Topology Live makes it a stratum. **Decision:** keep it as a stratum. Cross-cluster fact-checking lives there, and the threat beliefs captured by Limberg–Barnes's Existential Threats column are empirical and predictive in form. A5 had mapped Existential Threats to ontology; the underlying *picture of reality* still rolls up to ontology through `presupposes`.
- **Limberg–Barnes social columns.** A5 put Campfire, Combatants and Master Status under praxis. **Decision:** move them, with Chieftains, to a separate **relational (mimetic)** row. They describe the graph, not propositions [B1].
- **Habermas validity claims.** B1 proposes both a 1:1 mapping onto layers and a 4×3 grid. **Decision:** treat validity (truth / rightness / sincerity) as an **orthogonal tag** on each proposition. Sincerity belongs to the speech-act and signability layer, not to a stratum.
- **Layer order.** All sources agree on bedrock-to-surface order: ontology → epistemology → axiology → praxis. The "root chain" hypothesis (layers imply downward) stays a hypothesis. DT's tree *imposed* its partition [A2], so it must be tested with the tree-imposition check in §12.

### 5.2 Unit types

| Ontography | Topology Live | Arena canonical |
|---|---|---|
| `claim` (per worldview) | Proposition plus Stance | **Proposition** (shared) plus **Stance** (per person) |
| `value` | Proposition, type normative, stratum axiology | Proposition (normative) |
| `assumption` (always inferred) | Presupposition (inferred, necessity-tested) | **Presupposition** |
| `concept` (subject's meaning) | Concept sense via `defines` | **Concept sense** (feeds drift). Fix Ontography's bug that forces every concept to `epistemology`/`stated` [A1]. |
| warrants{logical, empirical, experiential, authoritative} / evidence{anecdote, study, authority, example, analogy} | EpistemicBasis (15) plus Walton schemes | **EpistemicBasis** (15), with Ontography types kept as a coarse rollup |
| (none) | Utterance → ADU plus speech act | **Source span plus speech act** (mandatory) |

### 5.3 Status and provenance (merged)

| Origin | States |
|---|---|
| Machine | `inferred` → `stated` (quote verified as a substring and entailed) |
| Human | `operator_approved` → `released` → `participant_confirmed` (= Ontography `verified`) / `participant_contested` / `retracted` |

Rules:
- Only `stated` or better counts toward scores.
- `inferred` content renders translucent and is never re-proposed once rejected.
- Feed-derived data can never reach `confirmed` without the person present. That is correct, and it means feed maps are mostly stated or inferred [A1].

### 5.4 Relations

Topology Live's 13 relations are canonical: supports (with scheme), rebuts, undercuts, undermines, qualifies, concedes, agrees, equivalent, presupposes, defines, exemplifies, answers, evades (displayed as "not answered").

Older vocabularies map onto them as follows:

| Source | Older terms | Canonical relation |
|---|---|---|
| Ontography edges | `grounds` | presupposes (reversed) |
| | `supports`, `contradicts` | supports, rebuts |
| | `tension` | qualifies or rebuts, plus a `tension` flag |
| | `implies` | supports |
| | `about` | defines |
| DT edges | agreement | agrees |
| | contradiction | rebuts |
| | tension, paradox | flags on a Disagreement |
| Ontography handshake verdicts | equivalent | sameAs / equivalent |
| | resonant | agrees (cross-person) |
| | divergent | Disagreement |
| | drift | Drift |

### 5.5 Unified synthesis types (judged *after* generation)

| Type | Shape | Sources |
|---|---|---|
| Resolution / sublation | Both are partial truths of Z | DC, Hegel |
| Subsumption / domain partition | True at different scales, domains or times | DC PRD (dropped in code), Topology Live `domain_partition`, DT "temporal integration" |
| Transcendence / value lift | The binary dissolves under a higher shared value | DC, Topology Live `value_lift` |
| Conditionalization | "Under what circumstances…" plus crux C | Topology Live; Lepp's integration question 2 |
| Incompletely theorized agreement | Same action, different reasons | Sunstein; Topology Live |
| Sequencing / Pareto move | Agreed order / better by each side's own lights | Topology Live |
| Paradox preservation | Hold the tension productively | DC |
| **Meta-consensus** | Agreed statement of the disagreement | Dryzek [B1] |
| **Aporia / null** | No synthesis yet; genuine incommensurability | Socrates; MacIntyre/Kuhn [A2, B1] |
| **Better question** | Not a third answer but a sharper question both sides keep asking; credited only through observed uptake (lineage) | Memo §4 (§2 D4); Landry EGP branch questions [B9] |

### 5.6 Axis library (candidates, not impositions)

Named axes are *labels* for the data to confirm or reject. Dimensionality is chosen by held-out prediction (§12).

| Source | Axes |
|---|---|
| Ontography's 8 core spectrums | material ↔ mind/spirit; empirical ↔ experiential; constructed ↔ objective morality; individual ↔ relational; linear ↔ cyclical time; conditioned ↔ free agency; disenchanted ↔ enchanted; reform ↔ rupture |
| DT's general axes | moral realism; source of moral knowledge; monism ↔ dualism; agency; value of life. These differ from Ontography's set; DT's topic axes (evil, therapy) do not generalize. |
| Kevin's Atlas | accelerate ↔ restrain; within institutions ↔ exit to parallel systems |
| Empirically found | left ↔ right; institutional trust (Andreou & Sirivianos) |
| Optional drivers | Moral Foundations (MFQ-2), Schwartz values, Koltko-Rivera's 42 dimensions in 7 groups |

Note that Kevin's "within institutions ↔ exit" axis overlaps Ontography's "reform ↔ rupture" and the institutional-trust axis. That is a strong first candidate to test for convergence.

---

## 6. SEE: the layered mapping architecture

**Design update (2026-10-30).** This section is rewritten to the decided **landmark-content pipeline** (§2 D10–D21). The research evidence for each layer is kept, but the layers are **re-ranked**: the content-derived proposition bank, the Jev question battery and statement reactions are primary; edges from content are secondary; the follow graph is demoted to an attention signal; stance-aware embeddings are optional. The old phase plan (graph-only v0 from X archives and AT Protocol) is superseded.

### 6.1 Decision matrix (re-ranked)

The briefs number layers inconsistently (A1's L0–L4 and B4's L0–L4 differ). The canonical names below supersede both. Layer codes S0–S5 are kept so that references elsewhere still resolve; their **rank and role** changed on 2026-10-30.

| Rank | Layer | Answers | Method | Strengths | Failure modes | Cost | Validation | Phase |
|---|---|---|---|---|---|---|---|---|
| **Primary** | **S3 Proposition bank** (from landmark content) | What does each scene actually claim, why, and where exactly do scenes fork? | Transcripts and texts from ~500 landmarks (YouTube, podcasts, Substack, posts) → Topology Live ontology plus Claimify-style selection, entailment and ambiguity gate; **deterministic quote validator: no supporting span, no claim**; L2 critic; neutral speaker-independent rewrite; identity resolution into the **shared proposition bank**; first-appearance timestamp and speaker on every proposition; every statement linked to its **source clip** (§2 D15). | Stance, depth, drift, cruxes; quote-anchored, so verifiable by anyone; feeds statement selection, MEET and event maps | Hallucination in presupposition descent; irony and hypotheticals in speech; speaker attribution in multi-speaker audio (diarization; Topology Live's live attribution unvalidated, so recorded content first); cost; illegible if shown whole | $0.10–1 per on-demand extraction [B4]; Ontography's current ~$1–2 per 10k words (UNVERIFIED); transcript sourcing cost open (Q34) | Faithfulness ≥0.97, precision ≥0.90, identity F1 ≥0.85, presupposition necessity ≥0.85; landmark dispute rate; user "that's not me" correction rate | **1** |
| **Primary** | **S1 Live question battery** (Jev) | Where does each landmark and each statement sit on the questions people are contesting *now*, at which layer? | **Weekly**, a stronger model reads a niche-balanced sample of landmark output and proposes the live question battery (§2 D16). **Jev** (TypeSafe) or GLiClass/SetFit labels cheaply against it, including **layer tags** (what is real / how we know / what matters / what is empirically true / what to do). Anchors via LLM pairwise plus Bradley–Terry. **No surveys:** corrections ("that's not me") become labeled examples. | Interpretable; probabilities, not labels; battery tracks the culture; ~$0.05 per account on Jev | Only as good as the questions; question drift between weeks; Jev is closed-weight, its access status is conflicting in secondary reports (UNVERIFIED), and its third-party accuracy figures are low-confidence | ~$0.05 per account; ~$400 per 10^7 posts × 20 questions | 300-item labeled pilot (Jev vs GLiClass vs frontier LLM); calibration; κ; agreement with S3 stances; correction-rate trend | **1** |
| **Primary** | **S5 Statement reactions → revealed ideal points** | Where does *a person* sit, and which axes really divide this population? | Individuals react **agree / disagree / pass** to selected real statements (Polis-like), gamified by **guess who said it** (§2 D17). Statement selection draws cluster-splitters, scene-internal live threads and surprising cross-cluster unifiers (§2 D15). Community-Notes-style matrix factorization (r̂ = μ + i_u + i_n + f_u·f_n) with ≥2 dimensions; Polis-style group-informed consensus. Landmarks enter the same space through their extracted stances, so a newcomer lands on a terrain that already exists. **This placement defines cluster membership for ratifying cross-cluster notes.** | Highest-validity *belief* map; platform-independent; works on day one because landmarks pre-populate the space; membership by endorsement is hard to game | Needs a well-chosen statement set; one dimension hides a second fault line; selection effects in who reacts; reaction-farming to enter a cluster for ratification (sybil) | Low compute; participation is the cost | Held-out reaction prediction; leave-topic-out transfer (Andreou); dimensionality by prediction error; landmark-vs-self placement agreement | **1** (moved from 4) |
| Secondary | **S4 Content edges and signed encounter graph** | Who quotes, hosts, answers or argues with whom, and are cross-cluster encounters integrative or sparring? | Edges **from content** (§2 D14): quotations, guest appearances, named rebuttals, co-appearances in events. Edge sign from classified stance (same proposition, opposite stance −; endorsed quote +). Each **cross-cluster encounter** is an edge between clusters; coverage goal: every cluster reachable through a chain of encounters (§2 D21). Signed modularity; participation coefficient; Burt constraint. | Separates allies from sparring partners; surfaces **threshold people**; reveals never-met cluster pairs (gap-filling, §7.7) | **Bridgers ≠ cores** (event content shows clusters at their most open); stance of a quote must be classified, not assumed; signed clustering is parameter-sensitive | Low (derived from S3) | Robustness sweeps; agreement with S3 disagreements; encounter-coverage metric | 2 |
| Attention signal | **S0 Follow / attention graph** (demoted) | Whom do people *attend to*? | Optional only: typed multiplex from consented X-archive or atproto follows, likes and reposts; Leiden or nested SBM; node2vec → UMAP. Shown as **attention**, never as belief or belonging (§2 D10). | Cheap; captures salience and hate-follows as *attention* honestly | Follows are attention, not agreement; hate-follows and professional follows; bots; topic-conditional (Barberá 2015); X terms and cost | Archive: free but slow (a day or more). Owned reads ~$1 per user (scope UNVERIFIED). Third-party 2-hop ego ~$10k. AT Proto: bandwidth. | Anchor and known groups; stability; reported only as an attention overlay | Optional |
| Optional | **S2 Topic terrain** (stance-aware embeddings) | What do clusters talk about? | Stance-aware sentence model (Kialo-tuned recipe) plus BERTopic labels; DT's `cluster_by_claims.py` landmark pattern | Map labels; topic buckets for MOVE normalization and for thread grouping | Raw embeddings conflate stance (silhouette −0.009 in DT [A2]); HDBSCAN noise on short posts (scale UNVERIFIED) | GPU minutes | **Stance-vs-topic test**: same-topic, opposite-stance pairs must separate better than the raw baseline [A2] | Optional |

**Fusion rule.** Use late fusion. Compute each layer separately and show their *agreement* (adjusted mutual information) as a confidence cue. Disagreement between layers is shown, not hidden. For example: "attends to cluster X; endorses positions closer to Y" (S0 vs S5). That is often the threshold signal [B4].

**Contradiction resolved (where S3 extraction runs), revised 2026-10-30.** A1 proposed extracting propositions from the top-k central accounts of each cluster. B5 forbade any inference about non-consenting people, and the earlier decision here was "consenting members and consenting landmarks only". **Superseded (§2 D12–D13):** cluster profiles are built from the **public output of ~500 landmark public voices**, which describes the clustering of a worldview, not a political categorization of a person. Each landmark can **dispute or annotate** their placement. **No inference is made about private individuals** who have not reacted or consented (red lines, §11.2). Aggregate text statistics over the public AT Protocol graph remain a research spike after a DPIA.

### 6.2 The landmark-content pipeline (decided architecture)

| Stage | What happens | Guardrail |
|---|---|---|
| 1 Seed landmarks | ~500 US-focused public voices, **2–3 per niche**, as many semi-mainstream niches as possible, seeded from Limberg–Barnes's tribes, Kevin's 58 ontologies and Benjamin's brainstorm; data then reveals missed clusters, named afterward (§2 D12) | **Stable core panel** with newcomers clearly marked; panel governance is Q35; landmark-selection bias audited (R48) |
| 2 Ingest public output | **YouTube public captions/auto-captions as the primary source** (paid transcript service or transcript library, paced backfill); podcast RSS + speech-to-text and publisher transcripts as complements; landmark opt-in channel connection as fallback; Substacks, posts; **sampled by niche, not volume** (§2 D14, D21; B9 as corrected) | YouTube ToS gray area, rate limits and IP blocks (R49); copyright: publish propositions + short quotes + timestamped links only, never full transcripts (Q34); Bluesky is one channel and demographically skewed |
| 3 Extract | Quote-anchored claims → neutral propositions → shared bank → Jev layer tags (§2 D15) | Discard any claim without a supporting span; stated vs inferred kept (§5.3) |
| 4 Edges | Quotes, appearances, named arguments, cross-cluster encounters (§2 D14, D21) | Bridgers ≠ cores; everyday output is the baseline |
| 5 Select statements | Cluster-splitters; scene-internal live threads; surprising cross-cluster unifiers; each linked to its source clip | Statements must be signable by their speaker; no clip-optimized extraction (red line 17) |
| 6 Place people | Statement reactions (S5), guess-who-said-it | No inference about non-reactors; private by default |
| 7 Correct | "That's not me" from users and dispute/annotate from landmarks become labeled examples | Corrections audited monthly (§6.6) |

### 6.3 Kevin Owocki's Atlas: what to borrow

The Atlas of Frontier Ontologies (daily-ontological-map.vercel.app) maps 58 X ontologies nightly. Each one is drawn as a continent; daily arguments are cities and top stories are mountains. It uses two axes (accelerate ↔ restrain; within institutions ↔ exit) and has a companion newspaper ranking tribes by real-world size. **Its method is undisclosed.** **Decided (§2 D12):** its 58 ontologies are a **seed source for the landmark list**; its daily newspaper ("Attention Times") is the model for the daily pulse (§6.6).

| Borrow | Do not borrow | Ask Kevin |
|---|---|---|
| The cartographic metaphor for the overview. It reads better than force graphs, which carry no spatial meaning in Ontography [A1]. | An undisclosed method (fails legitimacy, §14) | Data source (follows, likes, RTs, quotes, archive?), seed accounts, and scale |
| Two named axes as a starting hypothesis for the frontier-tech milieu | Editorial tribe descriptions that holders have not ratified | Clustering method (graph, embeddings, or LLM labels) and how clusters were named |
| Nightly cadence and versioned snapshots (answers the temporal-drift risk) | Showing named private individuals; placing anyone without a dispute affordance | Validation: did people recognize themselves? |
| Each tribe described "in its own voice". Make it the **holder-ratified** cluster card, assembled from ratified cross-cluster notes (§7.5). | Ranking tribes in a way that invites mimetic rivalry | Willingness to share code or data, or to co-build the shared overview |
| Sizing by real-world presence rather than feed volume (corrects the Pew 10%/80% skew) | | Which accounts anchor each of the 58 ontologies (seed-list input) |

Kevin's earlier design note fits with this: start with Venn-simple views and drill into high resolution [A1, A5]. **Recommendation:** propose the Atlas as a *shared terrain* candidate and a seed source. The Arena adds quote-anchored propositions, reaction-based placement, cross-cluster notes and MEET.

### 6.4 Progressive disclosure and the first sixty seconds

**The first sixty seconds** (§2 D18) is the entry flow and supersedes the earlier "Venn plus feed share" first view:

| Step | Screen | Purpose |
|---|---|---|
| 1 | React to a handful of statements (agree / disagree / pass; optionally guess who said it) | Placement without surveys or platform login |
| 2 | Appear as a dot on a terrain **that already exists** (landmarks pre-populate it) | Immediate, non-empty map |
| 3 | Your **three nearest landmarks** | Recognition |
| 4 | **Threshold reveal**: which clusters you sit between | The surprise: most people assume one camp |
| 5 | **Twist card**: the landmark farthest from you whom you most resemble on one question | The shareable moment ("Wait, I agree with them about that?") |
| 6 | **Invitation, not a score**: describe the cluster farthest from you, and see whether they will sign it | Enters the gradient (§7.5); the status prize is "the other side signed my description of them" |

After entry, the briefs' dials (Topology Live 0–5, A1's 5 steps, A2's L0–L5, B4's 4 steps) unify as:

| Level | View | Content | Rule |
|---|---|---|---|
| 0 | **Living map** (cartographic) | ≤7 cluster hulls per zoom level with labels; **live threads** moving across them (§6.5); landmarks as named anchors (newcomers marked); "you are here" dot (private by default); nearest threshold people; topic terrain as an optional background | Axes reorient to the **thread you follow** (§2 D7); feed ranked by **reciprocal opening** (§2 D9) |
| 1 | **Cluster card** | Voice assembled from **ratified cross-cluster notes** and holder self-descriptions; 9-slot Limberg–Barnes profile; root chain (4 lines); 5 central propositions with source clips; epistemic fingerprint; lineage and forebears; tribe-ness score; its live threads; how well it is described by each other cluster (R strip) | Every inferred item is translucent; ratification rate is shown; renders "solid" when well ratified and "hazy" when only inferred |
| 2 | **Person / pair** | Axis strips with uncertainty; reaction-based vs landmark-content estimate flagged; who you bridge to. For a landmark: placement plus **dispute / annotate**. For a pair of clusters: gap size *and* bridging potential shown separately (DT's key move), drift terms, encounter history and notes each way. | "Why am I here" explanation; dispute button |
| 3 | **Claim graph** | ≤50–80 nodes, deepest presuppositions first, stratified deterministic layout (X = stance, Y = stratum), crux as a fault plane, every node linked to its source clip | Never the entry view |
| 4 | **Meet** | Write a cross-cluster note, steelman the other side, or request a matched anti-debate | Every map view carries this call to action |

### 6.5 The live thread and per-question axes

The **live thread** is the core object of the map (§2 D6): an open question a scene is working through. Data model (for the spec): question text (neutral, signable by both sides), originating scene, first appearance (speaker, source clip, timestamp), the propositions that answer it, its **chosen axes** (the 2–3 dimensions this question actually splits people along, picked by prediction error on reactions to its statements, §2 D7), its reaction distribution by cluster, its **life-cycle state**, and its **parent and child questions** (the question genealogy).

| Life-cycle state | Observable signature |
|---|---|
| Emerging | New question in one scene's landmark output; few propositions |
| Spreading (within scene) | Rising share of the scene's output; internal disagreement (a scenius signal) |
| Forking | Reactions split within the scene; a sub-cluster may appear |
| **Crossing** | The question appears in another scene's output or reactions; the moment that matters most |
| Quiet / absorbed | Output falls, or the question is subsumed by a successor |

The map's genealogy of questions is also where **"better question"** syntheses are credited (§2 D4): a question that both parent clusters keep asking is visible as a crossing thread with descendants in both.

**Borrowed from Landry's Ephemeral Group Process [B9] (inspiration only, §2 D22).** EGP's public documentation (egp.community; the Life Itself wiki) describes a community of about 30–300 people who rank community-level questions, are routed into small groups on a shared *base question*, develop **branch questions** under an Inquiry Coach, and feed recordings into a question archive used in later rounds. Two elements are borrowed:
- **Question genealogy.** Each live thread is a base question with typed child (branch) questions and recorded lineage edges: `Question{id, parent_id, base_question_id, origin_cluster, created_at, adopted_by[]}`. This is the schema behind the parent/child questions above, and EGP's archive-feeds-later-rounds loop is the model for questions persisting while groups dissolve.
- **Routing people by question.** Rank questions, then group people by *shared question* while deliberately mixing their *clusters* within the group: a template for MEET matching (§7.2) and hosted gap-filling events (§7.7). An LLM "inquiry coach" may propose branch questions for people to ratify.

What EGP lacks, the Arena supplies: a structured schema linking questions to propositions and clusters, and an uptake reward (lineage, §8.6). **Caveats:** the public record is thin. No published outputs, evaluations or case studies were found, and the 2020 Stoa session recording was not located; Landry himself describes EGP as a later stage of a larger, unpublished body of work (Jim Rutt Show EP 153). This matches Benjamin's critique that it never delivered a full stack with concrete outputs.

### 6.6 Time: the four-dimensional map and nested horizons

Everything is timestamped from day one (§2 D19). Propositions record first appearance and speaker; stances are readings at a moment. Clusters are tracked as **lineages** across snapshots (births, splits, merges, fadings). YouTube and podcast archives allow **backfill** of real historical arcs on day one. A **stable core landmark panel**, with newcomers clearly marked, keeps sampling change from masquerading as cultural movement (R47).

| Horizon | Work | Product |
|---|---|---|
| **Daily: the pulse** | Cheap Jev tagging of new landmark output against existing questions; flag spikes and events (e.g., a major cross-cluster interview); track event **ripples** | A daily pulse, like Kevin's "Attention Times" |
| **Weekly: the weather** | Re-run clustering; update thread life cycles; stronger model proposes new live questions | A weekly culture weather report |
| **Monthly: the deep pass** | Fresh proposition extraction; re-fit axes; trace cluster lineages; audit against user corrections and landmark disputes | A monthly state-of-the-discourse report for journalists and researchers |

These windows are the natural *t* for the state vector (§10.3).

### 6.7 Recommended build sequence (revised 2026-10-30)

| Phase | Build |
|---|---|
| 0 | **Charter, red lines and validation harness first.** Public-figure placement rules and dispute affordance; DPIA covering landmark processing; gold sets (G1–G4 from Topology Live plus transcript red-team items: irony, hypotheticals, quoted-opponent speech, diarization errors); canary sets. **Landmark seed list v0** and core-panel governance. |
| 1 | **Landmark-content map v0.** Transcript ingestion for the landmark set (recorded content first; backfill); quote-anchored extraction into the shared proposition bank (S3); weekly question battery and Jev tagging (S1); statement selection; **statement reactions and placement** (S5); the first-sixty-seconds flow; private dot. **First event map** from one recorded, surprising but not incendiary cross-cluster encounter (§7.6). |
| 2 | **Gradient on.** Cross-cluster notes with fidelity and portability (§7.5); cluster cards assembled from ratified notes; content edges and encounter graph (S4); gap-filling invitations; daily pulse and weekly weather. |
| 3 | **Living map.** Live threads, per-question axes, question genealogy, cluster lineages, monthly deep pass; lineage-based synthesis and scenius credit (§8.6). Optional S0 attention overlay from consented archives or atproto; optional S2 terrain. |
| 4 | **MEET pilots** (async anti-debates and Arena-hosted gap-filling events) produce steelmans and meta-consensus. Compare S5 axes against S1 and S4 as convergent validity. |

---

## 7. MEET: dialogos across clusters

### 7.1 Asynchronous anti-debate protocol (v0)

This adapts Lepp's format [A3] with B1's primitives. Text is self-attributed, so the live-attribution problem that blocked Topology Live's certification does not arise.

| Step | Async form | Map output |
|---|---|---|
| 0 Pre-poll | Each party (and optionally their cluster cohort) rates on 1–5 scales: position, comprehensiveness, faith in discourse | Baseline |
| 1 Connection | Short "why I care" note; not committed | Human context |
| 2 Independent statements | Openings written **before** seeing the other's (Delphi independence) | Commitment stores |
| 3 Rebuttal + exchange | Threaded, 48–72 h, turn cap, equal turns. Each party must state a stance on the other's top 3 propositions. This fixes the finding that stated disagreements run 0–2 per debate. | Clash and questions ledger |
| 4 Bohm suspension | Before replying, name your own assumption that the other's claim challenges | Presupposition surfaced *by the holder* |
| 5 Steelman | One clarifying question, then the steelman. **The target scores it** {captured, missed, distorted, added}. | Steelman record |
| 6 Red-team self | "What would change my mind," typed as update conditions | Crux cards |
| 7 Integration | **Gated (§2 D3): only after both steelmen are ratified by their targets.** System proposes 2–3 higher-ground candidates (with derivation and cost to each side) using Lepp's three questions. Parties edit, sign or decline. | Higher ground `confirmed by both`, or meta-consensus, or aporia |
| 8 Closing | "How did my view expand, if at all?"; post-poll; re-poll after 2–4 weeks | Updates ledger; deltas |

**Closing artifact (mandatory).** A **meta-consensus statement** of where and why the parties differ, ratified by both. Synthesis is optional.

**Delegate variant.** "Narration for the Tribe": a cluster sends a voice, and its cohort polls before and after [A3].

**First pilot.** In June 2026 Lepp offered Gitcoin anti-debates on crypto vs localism, possibly live in Boulder [A3]. **Superseded as the first *public* product (§2 D20):** the first public output is an **event map** of a recorded cross-cluster encounter (§7.6). Lepp's anti-debates remain the natural first *participant* pilot and the model for Arena-hosted gap-filling events (§7.7).

**Design update (2026-10-30).** The closing artifact feeds the gradient: each ratified steelman is also a ratified **cross-cluster note** (§7.5), and a synthesis proposed at step 7 earns credit only retroactively, by lineage (§8.6).

### 7.2 Matching: who should talk to whom

Score candidate pairs (or delegate pairs) on these factors:
1. **Far in S5 (reaction-based placement; formerly S0), overlapping in S3.** Both hold stances on shared high-centrality propositions, so they clash rather than talk past each other.
2. **Mid-stratum disagreement with shared ends.** Disagreement on praxis or empirical/predictive, with agreement at axiology. Lepp's integration questions work best here; pure values cruxes are often irreducible.
3. **Integrators, not sparrers.** Prefer S4 positive bridges and people with a high **outgroup-prediction reputation** (§8, design D) as first participants.
4. **Track record.** Steelman confirmation rate and good-faith flags.
5. **Right to enclave.** People opt in to crossing. Never force exposure (Fraser). Unstructured exposure can backfire: Bail et al. 2018, cited through secondary sources [B4]; B1 marks the primary UNVERIFIED.
6. **Blind prestige.** Hide follower counts in MEET (prestige bias) [B1].
7. **Fill the biggest holes** (§2 D21). Prefer cluster pairs that have never met in the encounter graph (§7.7), and prefer **threshold people** as first participants (§2 D8).

### 7.3 The "being changed" composite signal

No component rewards a stance flip alone [A3, B1, B2].

| Signal | Source | Weighting note |
|---|---|---|
| Steelman fidelity, confirmed by the target | Steelman record | Core; validates understanding without requiring agreement |
| Stated updates (attitude, strength or credence change, concede, retract) | Updates ledger | Stated only; capped per session |
| Update-condition explicitness | Crux cards | Rewards offering falsifiability |
| Higher ground signed by both, with declared cost to each side | Integration step | Weighted by stratum lifted |
| Meta-consensus ratified | Closing | Counts as success even with no synthesis |
| Comprehensiveness delta; faith-in-discourse delta | Pre/post polls | The format's own "expand" measure |
| Retention and concept reuse at 2–4 weeks | Re-poll; claim-level adoption | Separates performance from change (proposed, UNVERIFIED as practice) |
| Frame-level shift | Stratum of the update (epistemology deeper than praxis) | Bateson's Learning II |

Aggregate measures to track against controls: opinion **reordering** (Goyal et al.) and affective polarization.

### 7.4 The AI mediator's role

**Do:**
- Generate higher-ground and bridging candidates using a Habermas-style critique-and-revise loop. Deliberation with it raised group agreement ~6–9 pp (≈8 on average across three cohorts), and its statements were preferred 56/44 over human mediators' [B2].
- Prefer **proportional slates** (generative social choice) to a single statement.
- Prompt Walton critical questions and Lepp's integration questions.
- Detect symmetrical schismogenesis (escalating mirroring) and slow the exchange.
- Pre-run synthetic anti-debates between DC-style "method" agents to propose candidate cruxes before any humans meet.

**Do not:**
- Issue verdicts. DT's META_ANALYSIS took sides; the Arena separates map from verdict.
- Fact-check unsupervised.
- Score its own syntheses.
- Replace human contact. Sætra's critique: AI caucus mediation yields "linguistic compromise" without relationship [B2].

LLM note-writers outperform median humans but take satire too literally [B2]. Humans ratify; the AI generates.

### 7.5 Cross-cluster notes: the gradient made concrete

Decided in the design dialogue (§2 D1–D2). Lineage: Jamie Joyce and the **Society Library** (structured representation of every side of a debate), Audrey Tang and **vTaiwan** (consensus-finding with Polis), and X's **Community Notes** (bridging-based rating). Researched in B9; further vTaiwan and Community Notes evidence is in [B2, B3, B5].

**Society Library lineage [B9].** The Society Library (Jamie Joyce) runs analyst-driven deliberation mapping: positions → arguments → claims → evidence, with 20+ relation types. Its core move is **claim identity**: **one ID per claim**, with every phrasing and medium that expresses it linked to that node and **all source quotes** kept (plus Internet Archive snapshots). That is a hand-built version of the Arena's **shared proposition bank with quote anchors** (§6.1 S3), and the Arena adopts it. Its labels are **status, not verdicts** ("no evidence found", "not yet fact-checked"; never true/false), matching red line 16 and the no-judgment rule for notes. Its weakness is scale: the Diablo Canyon map took about **8,000 research hours** (~5,000 references, ~5,862 claims and arguments) and is unfinished. The **gap cross-cluster notes fill:** the Library's analysts steelman *on behalf of* positions, but no step has the **described side ratify** the description (no crowd or Community-Notes-like ratification was found; UNVERIFIED / likely absent). The Arena adds that fidelity signal, plus scale through quote-anchored LLM extraction corrected by users. Status labels for notes follow suit: "not yet ratified", "ratified by B", "B is split", "anchor disputed".

**Portability vs fidelity [B9].** **Portability ≈ Community Notes bridging**: Birdwatch's matrix factorization shows a note only when its helpfulness intercept, the part *not explained by rater viewpoint*, is high (Wojcik, Coleman et al. 2022). **Fidelity is new**: it restricts one rating channel to reaction-placed members of the described cluster B. Running the same factorization *inside* B surfaces sub-clusters, which is the split-ratification rule below. Polis/vTaiwan's group-informed consensus is the direct ancestor of reaction-based placement (S5) and of bridging rule R4 (§8.6).

**The object.** A note is written by someone placed in cluster A (by statement reactions, §6.1 S5) and describes cluster B: what B believes and why, in terms B would sign. **Notes describe; they never judge.** Judgments of B make a note unsignable, so the fidelity signal itself filters them out.

| Signal | Who grants it | Measures | Mechanics |
|---|---|---|---|
| **Fidelity** | **Only members of B**, randomly sampled from those whose reactions place them in B (never raters A chooses) | "That's us, I'd sign that" | Fidelity-rating ITT form ("how accurately does this represent what we believe, and why"), not spot-the-fake (§10.8); sealed ratings; correlated-agreement scoring |
| **Portability** | Members of A and of third clusters | Cross-viewpoint clarity: the note helps outsiders understand B | Community-Notes-style matrix factorization over raters' reaction-based positions, ≥2 dimensions (§8.3) |

**The gradient.** The more clusters converge on shared descriptions of a given cluster that that cluster ratifies, the further up the gradient the system is. Per directed pair, this is R_a→b (§10.3), now measured primarily by ratified notes; the map shows it as the R strip on each cluster card.

**Split ratification is information, not failure.** When B's members split on whether a note describes them, the split reveals a **sub-cluster**. The map re-fits and the note becomes two notes, each ratifiable by its own sub-cluster. This sharpens the map instead of forcing a single description.

**Rules.** Notes cite the source clips of the propositions they summarize. Agents may draft notes but never rate them (O14). Fidelity cannot be self-granted or granted by co-raters A recruited. A note that targets a third cluster is screened by the bridging-against detector (§10.2). Cluster cards (§6.4 level 1) are assembled from ratified notes plus B's own self-description.

**Relationship to MEET.** A ratified note is the asynchronous, crowd-scale form of the anti-debate steelman (step 5). A pair with ratified notes both ways is eligible to propose a synthesis (§2 D3) and is a prime candidate for a matched anti-debate.

### 7.6 Event maps: the flagship product

Decided in the design dialogue (§2 D20). The Topology Live extraction runs on **any** recorded debate, dialogue, interview, panel or monologue, not only on anti-debate formats [A3; memo §11.2].

**Pipeline.** Transcript split by speaker (recorded content, with diarization checked; Topology Live's live speaker attribution is not validated) → quote-anchored propositions per speaker → matched to the shared proposition bank → placed on the existing terrain.

**What an event map shows:**
- where each speaker **starts** on the terrain (from their landmark placement or extracted stances);
- where they **met** (propositions both affirmed);
- where they **diverged, and at which layer** (facts, values, ontology: Dialectical Topology's lens on the shared map);
- **missed openings**, where a steelman would have changed the conversation (map output, not a verdict: red line 16 holds);
- **the ripple**: over following days the daily pulse tracks whether the event's ideas crossed into other scenes or hardened each side.

**Publishing.** Speed is the virality mechanism: publish the map of a major crossover moment **within a day**, riding the news cycle. **First public event:** surprising but **less incendiary**. The most charged events (the memo's example is a Nick Fuentes interview with Hunter Biden) wait until the method has earned trust, to avoid a launch defined by platforming accusations (R44). Which event goes first is open (Q31).

**Caveats.** People who talk across lines are usually **bridgers, not cluster cores**; event content shows clusters at their most open, so landmarks' everyday output remains the baseline for placing clusters (R45). Event maps never score speakers and never declare a winner.

### 7.7 Gap-filling: Arena-hosted anti-debates

Each cross-cluster encounter in the corpus is an **edge** between two clusters (§6.1 S4). The goal is coverage: any cluster reachable from any other through a chain of encounters. Some clusters may never overlap; pairwise hops still let the terrain be mapped conceptually (§2 D21).

**Gap-filling rule.** Find cluster pairs that have **never met** (or met only through sparring), rank them by the size of the hole they leave in the encounter graph, and turn the biggest holes into **invitations for Arena-hosted anti-debates** (§7.1 protocol, live or async), ideally between a landmark from each cluster or their delegates. Each hosted event produces an event map (§7.6), adds an edge and feeds the proposition bank. This is both research method and content engine. Matching factors (§7.2) still apply; right to enclave still applies: invitations, never forced exposure.

---

## 8. MOVE: incentives for metabolizing

**Design update (2026-10-30).** The gradient MOVE ascends is now explicit (ratified cross-cluster description), novelty is not rewarded at proposal, and synthesis and scenius are rewarded retroactively by lineage. §8.6 states the decided reward targets and reconciles designs D, A, C and B and B8's Designs 1–3 with them; the ranking below is kept as research evidence.

### 8.1 Candidate designs, ranked

| Rank | Design | What it rewards | When | Key risks → fixes |
|---|---|---|---|---|
| 1 | **D: Outgroup-prediction reputation.** Report your judgment and predict each other cluster's distribution; score with BTS or peer prediction plus accuracy; produces a non-transferable, decaying score per cluster pair. | Measured understanding: the ideological Turing test as a mechanism; it is also integration-as-capacity | Year 1, no money | Stereotype learning → score individual-level reasons and add outgroup-rated steelmans. BTS assumes a common prior, which clusters violate (UNVERIFIED validity) → pilot against plain accuracy. Keep optional, never a gate. |
| 2 | **A: Bridged endorsement credit.** Matrix-factorization intercept × Polis group-informed product × bounded distance bonus (1 + α·d); fidelity gate (origin members confirm they were represented faithfully). | Syntheses that survive across viewpoints | Year 1, reputation only | Blandness → topic-normalize plus stakes floor. Distance farming → provenance must come from a real MEET session; cap α; d comes from the claim graph. Impersonation → long-run membership signals. |
| 3 | **C: Retroactive metabolism funding.** A quarterly cross-cluster jury (seats proportional, judging sampled pairs) plus AI models scored against the jury (the Deep Funding pattern); advisory prediction markets. | *Bidirectional* uptake and new bridges, measured by claim-level diffs | Quarterly outer loop that backtests A and B | Homogenization → cluster diversity is a hard constraint. Attribution noise → matched counterfactual topics. Jury capture → rotate juries, disclose seats, publish model scores. |
| 4 | **B: Cluster-pair CO-QF.** COCM with groups G taken from SEE (not projects), soft weights, distance-weighted pair terms, per-synthesis caps. | Cross-cluster support | Only with a payment leg, stable identity and a frozen map | Tight-knit penalty (below); reciprocal rings → pairwise-bounded subsidies plus a challenge window; map lobbying → publish, freeze and appeal. |

**Guardrails for all designs:**
- **Non-rivalrous recognition.** Mutual, dyadic attestations. No leaderboards, because Girard predicts rivalry over any status token [B1].
- **A separate within-cluster deepening track**, so MOVE never pays only for bridging.
- **Counterfactual reporting.** Results are published under plain QF, COCM and the chosen design together. Gitcoin found that opaque labeling, not the math, caused most disputes [B3].
- **Paradox and meta-consensus are eligible** for reward [A4].

### 8.2 COCM caveat: the harm to tight-knit communities

This is the strongest field warning in the evidence base [B3]:
- In GG22, a project with 27 real donors received a $0 match because 23 of them clustered.
- CCN Climate rejected COCM after it cut top grantees' match by 60–70%.
- In Benjamin's own GG21 retrospective, operators could not explain results to grantees and blended 50/50 with plain QF.

Bioregional and local communities are exactly this shape. **Required:** a QF blend, a floor for under-represented clusters, a deepening pool, and canary fixtures (a known legitimate tight-knit community must not be penalized).

COCM was used in 32 of 38 Gitcoin rounds (~$4M of $4.5M). Round managers preferred it [B3]. B3's summary figure of "~89%" matches the share of funds (32/38 rounds is ~84%), although the paper's abstract calls it an "adoption rate".

### 8.3 Fixing bridging blandness

Naive bridging down-ranked controversial topics (Milli et al., NeurIPS 2024 Pluralistic Alignment Workshop; 70M Facebook URLs). Upranking bridging content alone did not significantly reduce polarization. Pairing it with downranking toxic content did (−0.042 SD) [B2, B3].

**Fixes:**
- Topic-normalize credit within S2 topic buckets.
- **Stakes floor:** a synthesis must touch a load-bearing, high-centrality proposition from each origin cluster.
- **Fidelity veto** for origin clusters.
- Use ≥2 latent dimensions. One axis suppresses second-axis disagreement: publication falls from 71.5% to 11.7% [B2].
- Pair bridging rewards with de-amplifying contempt.

**Contradiction resolved.** B3 cites Wojcik 2022 as finding that a second dimension "added little". B2 and B4 cite Andreou & Sirivianos 2026 as finding a meaningful second axis. Both hold: the 2022 production model was tuned for note selection, while the 2026 refit on 212.9M ratings shows the second axis transfers to held-out topics and a third adds little. **Use two dimensions as the floor.**

### 8.4 Sybil resistance

- **Graduated identity.** Anyone can take part in SEE and MEET. MOVE weight rises with personhood (e.g. Human Passport stamps), account age and track record [B3, B5].
- **Ensemble of weak signals** plus coordination detection (actors, behaviors, content), with **canary rules**, human review and appeals.
- Expect 10–20% friction loss among legitimate newcomers [B3].
- **Treat the X follow graph as a weak sybil signal**, because follows are cheaply botted. SybilGuard-style defenses work only on trusted edges.
- **Audit bridging scores for synthetic consensus.** Fewer than 10 coordinated ratings pushed up to 10.7% of lower-quality notes over threshold in Community Notes (Selvam, Baxter et al. 2026) [B5].
- **Costless credits get sqrt-weighted fixed pots plus caps**, never superlinear matching (the love.fund pattern) [B3].

### 8.5 Who judges synthesis

A layered answer. B3 flags it as a **design hypothesis, UNVERIFIED end to end**:
1. **Origin-cluster members** hold a veto on misrepresentation (fidelity).
2. **Distant-cluster peers** check that a synthesis is not one-sided.
3. **A rotating, proportionally seated jury** gives pairwise ground truth. Deep Funding jurors agreed 63–89%, and longer deliberation did not help.
4. **AI** triages and predicts, and is scored against held-out human panels.

The designers never judge. That answers Mouffe's and Fraser's hegemony objection.

### 8.6 The decided gradient, lineage rewards and scenius (2026-10-30)

The design dialogue (§2 D1–D5, D9, D18) settles what MOVE rewards. It does not discard designs D, A, C and B; it re-targets them.

**The gradient is explicit.** What MOVE ascends is **ratified cross-cluster description**: how accurately each cluster describes every other cluster, in terms the described cluster would sign (§7.5). Success is meta-consensus, not convergence. A clean, mutually understood disagreement is a success.

**Three rewardable things, one currency.**

| Rewarded | When | Measured by | Credit |
|---|---|---|---|
| **Ratified description** (a cross-cluster note or steelman) | At ratification | Fidelity granted by sampled members of the described cluster; portability across A and third clusters (§7.5) | Dyadic, non-transferable, decaying recognition for the A→B pair (§10.2) |
| **Synthesis** | **Retroactively, by lineage**; never at proposal. May be *proposed* only after ratified steelmen exist both ways (§2 D3) | Uptake by **both** parent clusters; gathers its own adherents; appears on the map as a new region tracing to both parents | Lineage credit (cross-scene uptake) |
| **Scenius (deepening)** | Retroactively, by lineage | Uptake **within** the author's own scene: new questions, internal disagreements worked through, ideas the group takes up | Lineage credit (within-scene uptake) |
| **A better question** | Retroactively | A question both sides keep asking, visible as a crossing live thread with descendants in both (§6.5) | Lineage credit; counts as a synthesis fruit |

**Deepening vs hardening.** Within-scene status earned **against** another cluster is *hardening* and earns nothing. It is detectable because it is defined against an outgroup: content whose uptake depends on negative stance toward another cluster, rising hostility reciprocity (§10.3 variable 4) or hostility concentration (variable 5). Use the same machinery as the bridging-against detector (§10.2), applied inside a cluster. This specifies the "separate within-cluster deepening track" (§8.1 guardrails) and constraint C5 (§10.4).

**The status prize** shared socially is **"the other side signed my description of them"** (§2 D18): understanding, not placement. It is a dyadic, conferred credential, so it is non-scarce and does not create a leaderboard (red line 19).

**The feed rule is reciprocal opening** (§2 D9): every ranked surface (the living map, the daily pulse, statement selection) is ranked by what **widens**: crossing threads, twist cards, notes ratified across a gap, encounters between never-met clusters. Never by time-on-site or outrage. This generalizes §8.3's "pair bridging with de-amplifying contempt."

**Attribution [B9].** *Reciprocal narrowing* is neuroscientist Marc Lewis's account of addiction (*The Biology of Desire*) as a self-organizing loop in which narrowing attention makes the world afford less, which narrows the person further; John Vervaeke adopts it as the negative mode of relevance realization (linked to parasitic processing). *Reciprocal opening* is Vervaeke's inverse: a mutually accelerating disclosure between a person and the world, which he ties to **love**, flexibility and flourishing. Neither has published a feed specification; no text was found applying the idea to ranking algorithms. **"Running the algorithm in reverse" is Benjamin's extension** and should be presented that way. The design reading: an engagement feed is an outsourced relevance-realization machine optimized to *hold*; running it in reverse makes the objective growth in the set of clusters a person can **accurately describe**.

**Ranking rules R1–R8 [B9]** (our translation; not Vervaeke's):

| # | Rule | Mechanism |
|---|---|---|
| R1 | Objective = predicted gain in *describable clusters*, not dwell time | Score items by the likelihood of raising the user's perspective-taking accuracy on clusters where it is low |
| R2 | Information gain over confirmation | Down-rank statements whose reaction is near-certain given the user's position; up-rank statements that split the user's own cluster or unite clusters the user thinks distant (twist statements) |
| R3 | Graduated distance (zone of proximal opening) | Serve the next-adjacent cluster first and widen step by step (hypothesis; needs an A/B test) |
| R4 | Bridging over in-group applause | Weight by cross-cluster approval (Community Notes style), not raw likes; mild penalty for in-group-only applause |
| R5 | Penalize hardening | Outgroup-defined (negation-framed, contempt-laden) propositions are excluded from the widening pool even when popular (D5) |
| R6 | Finite surfaces | The daily pulse ends ("you're caught up"); no infinite scroll, streaks or variable-reward notifications |
| R7 | Close each session with an act of opening | Last card invites the user to describe a far cluster or adopt a question from one |
| R8 | Thread-first, not person-first | Follow questions, not personalities; questions branch, people collapse salience |

Ranking objective: `score(item, user) = E[Δ perspective-taking accuracy on under-described clusters] + λ·bridging − μ·hardening_prob − ν·predictability`, under the finite-session constraints. (These R-codes are feed rules; ratified outcomes R1–R5 in §10.6 are a separate list.)

**The measure.** The primary person-level metric is **perspective-taking accuracy across clusters**: accuracy on "guess who said it" and "how would cluster B react?" cards, per cluster, weighted toward far clusters. This is **the ratification gradient at the individual level**: the strongest form of it is the count of the person's notes about other clusters that those clusters have signed. Supporting signals: breadth (entropy of clusters engaged over 30 days; narrowing is falling entropy), hardening share, and usage shape (many short compulsive sessions vs fewer completed ones; a guardrail, never a reward). At cluster level it is the description-fidelity matrix R (§10.3). **Validation:** A/B test the reverse-ranked feed against an engagement-ranked baseline on held-out perspective-taking cards; opening should win on accuracy while taking *less* time. Gaming risk: users may learn to predict outgroups cynically, so ratified descriptions stay the reward and prediction is only a feed signal.

**Reconciliation with existing designs.**

| Existing design | Status after 2026-10-30 |
|---|---|
| **D Outgroup-prediction reputation** (§8.1 rank 1) | **Retained** as a cheap measurement of R (meta-perception error), now secondary to ratified notes. Prediction targets are the reaction distributions of each cluster on live-question statements. |
| **A Bridged endorsement credit** (rank 2) | **Re-targeted**: the matrix-factorization intercept becomes the **portability** signal on notes; the fidelity gate becomes the **fidelity** signal; "long-run membership signals" are replaced by **reaction-based membership** (§2 D17). It no longer credits syntheses at proposal. |
| **C Retroactive metabolism funding** (rank 3) | **Promoted** to the default synthesis reward: lineage measured by claim-level uptake in both parents (and within-scene uptake for scenius) is exactly C's "bidirectional uptake". The jury now adjudicates lineage disputes. |
| **B Cluster-pair CO-QF** (rank 4) | Unchanged: only with a payment leg, stable identity and a frozen map; groups G come from reaction-based clusters. |
| **B8 Design 1 Ratified Commons** (§10.6) | **The year-1 home of the gradient.** R1 (steelman confirmed) now includes ratified cross-cluster notes; add R5 lineage credit (below). |
| **B8 Design 2 Strategy Tournament** (§10.7) | Unchanged; the composite outcome adds note-fidelity gain. |
| **B8 Design 3 Bonded Open Agents** (§10.6) | Unchanged; agents may draft notes (labeled) but never ratify them (O14). |

---

## 9. AGENTS: an ethical agent layer

The question is whether the Arena should run, or register, AI agents that act on social platforms to connect clusters, with their effect measured on the map and the agents ranked by impact. **The answer is yes, under the Open Agent Charter (§9.4): disclosed, registered, operator-bound and bonded, aimed at meta-consensus rather than conversion, openly present on platforms, contacting only people who invited it, and rewarded only for ratified outcomes. It is no to covert, unsolicited or tribe-targeted agents** [B6, B8].

Benjamin's decided position is that disclosed, terms-compliant, ledger-registered agents aiming at meta-consensus are ethically distinct from covert influence operations and may act openly; people can mute or disengage. B8 tested this against platform rules and the B6 means tests and **mostly supports it**. It relaxes B6's line on *presence* and keeps B6's line on *contact*, because platform law requires that, not ethics alone. B6 and B8 are research and ethics briefs; they contain no tactics, persona methods or detection-evasion techniques, and this section keeps that scope.

### 9.1 The adversarial landscape (attribution graded)

"Fifth-generation warfare" is a contested popular term, not an analytic category, and the Arena should not use it as one. "Attributed" below means a platform, government or court document names the source. "Reported" means named-source journalism the state has not confirmed [B6].

| Operation | Actor | Attribution status | Documented effect |
|---|---|---|---|
| Doppelganger | Russia (SDA, Structura, ANO Dialog; Presidential Administration) | **Attributed**: DOJ domain seizure (Sept 2024), Treasury designations, OpenAI (May 2024) | ≤ Breakout Category 2 |
| Meliorator bot farm | Russia (RT origin, later FSB-created organization) | **Attributed**: DOJ seized 968 X accounts; joint US/NL/CA advisory | No public reach measure |
| Bad Grammar | Russia | Attributed by OpenAI | ≤ Category 2 |
| Pravda network | Russia | Attributed by DFRLab | Indirect: contaminates Wikipedia and LLM reference layers ("LLM grooming") |
| IRA, 2016 | Russia | Established | **No measurable** change in attitudes, polarization or vote; 1% of users got 70% of exposures (Eady et al. 2023) |
| Spamouflage / Dragonbridge | China | Meta: linked to people "associated with Chinese law enforcement" | Low reach; one TikTok outlier ~1.5M views |
| AI-policy operation (June 2026) | China | OpenAI: "likely originated in China" | Category 1 |
| IUVM; Storm-2035 | Iran | Attributed by OpenAI and Microsoft | Low end of Category 2 |
| STOIC / "Zero Zeno" | Israel | **Firm attributed** (OpenAI, Meta). State funding **reported** (NYT), ministry denied | Meta: no widespread impact |
| Pro-Western network 2017–22 | United States | Meta: individuals associated with the US military; CENTCOM linkage **reported** (The Intercept) | "Little to no" authentic engagement |
| Anti-Sinovac campaign, Philippines | United States (DoD) | **Reported, partly acknowledged** (Reuters) | No reach figure; harm to public-health trust |
| Influence-as-a-service | Commercial, multi-country clients | Anthropic (2025); state links unconfirmed | No viral content |

**What it adds up to:**
- **Measured reach is consistently low.** Of about a dozen AI-assisted operations from 2022 to 2026, almost none broke out of their own networks. AI raised productivity, not persuasive success [B6].
- **Low reach is not no harm.** The Breakout Scale under-counts relationship-building and one-to-one AI operations (Yang 2026). Pravda-style operations target the reference layer. Effects on *trust*, and on the belief that "everyone is a bot", escape exposure studies [B6].
- **Implication.** "Fight their bots with our bots" overstates the adversary's documented effect. The documented harm is to the **information commons**. Adding more automated actors, however well-meant, adds to that harm.

### 9.2 Evidence on AI persuasion and prosocial bots

| Study | Finding | Lesson for the Arena |
|---|---|---|
| Salvi et al., *Nat. Hum. Behav.* 2025 | Personalized GPT-4 had 81.2% higher odds of increasing agreement than humans; effect vanished on strongly held topics | Personalization is potent, so it must be consented |
| Costello, Pennycook & Rand, *Science* 2024 (DebunkBot) | ~20% drop in belief in the participant's own conspiracy after ~8.4 min; about a quarter stopped endorsing it; lasted ≥2 months | An agent the *believer invokes* works |
| Boissin, Costello et al., *PNAS Nexus* 2025 | Similar effect whether participants were told it was an AI or an "expert" | **Disclosure costs little**, so covertness is gratuitous |
| Hackenburg & Margetts, *PNAS* 2024 | LLM microtargeting not significantly better than generic messages | Per-tribe targeting buys little |
| Hackenburg et al., *Science* 2025 (N≈77k) | Post-training raised persuasiveness up to 51%; **the more persuasive the model, the less accurate its claims** | Ranking by persuasion selects for inaccuracy |
| Zurich r/changemyview (2024–25) | Undisclosed accounts, ~1,783 comments, 137 deltas, invented personas including a trauma counselor and an assault survivor; Reddit called it "deeply wrong"; researchers chose not to publish | Legitimacy is conferred by the affected community; the harm bought no usable knowledge |
| Bail et al., *PNAS* 2018 | Consented exposure to an opposing bot made Republicans more conservative | Broadcast exposure is not bridging |
| Argyle et al., *PNAS* 2023 | Accept/edit/ignore AI rephrasings raised feeling understood (~4 pp) and reciprocity; no attitude change | **The human keeps authorship.** A clean MEET template |
| Habermas Machine (Tessler et al. 2024) | AI statements preferred 56%; one condition did not disclose AI authorship | Use as caucus mediator; disclose every time |
| AI Community Notes (X API, 2025; Li & Bakker 2026) | Labeled AI notes rated more helpful than human ones under equal exposure | **Strongest precedent**: agents draft, humans across axes ratify, output labeled |
| Munger 2017 | Undisclosed in-group accounts reduced slur use | Peer norms work, but the covert design cannot be copied |
| Twitter "Automated by" label | Opt-in, unaudited; bad bots don't use it | Disclosure must be a registry condition |

The disclosed, consented, human-in-the-loop interventions produced real but modest gains. The covert ones either cannot be replicated ethically or caused backlash. None of the successful precedents works by placing content on unwitting people [B6].

**Rules and law** [B6; details in the brief]:
- **X automation rules** allow automated replies or mentions only when the user has "requested or … clearly indicated an intent" to be contacted (a reply or DM to the bot counts; a follow does not). Keyword-triggered replies and unsolicited mass mentions are banned, as are automated likes and multiple accounts for substantially similar purposes; one automated reply per interaction; opt-outs must be honored promptly (checked against the primary page, VERIFICATION §E). Tagging people across clusters is prohibited unless they asked. The X Developer Policy also forbids the political inferences per-tribe framing would need (§11.1). X's automated-account label links a bot to a human managing account; whether it is universally available rather than invitation-only is UNVERIFIED [B8].
- **Meta CIB, X authenticity, Bluesky guidelines** all ban fake personas and coordinated deception. Bluesky's guidelines (updated 2025-09-19) have **no bot-specific rule**, and an account **cannot self-apply an official "bot" label** (only a few global self-labels exist). Community `ai-agent`/`automated` self-label values and opt-in labelers exist but are reported secondhand (UNVERIFIED) [B8]. That is an open gap the Arena's own labeler could help fill.
- **Farcaster** changed hands in 2026 and plans to require human verification; agent status there is UNVERIFIED. Do not build on it until the new rules publish [B8].
- **EU AI Act Art. 50** (from 2 Aug 2026) requires AI-interaction disclosure (50(1)) and labels on public-interest AI text (50(4)). **DSA Arts. 34–35** oblige very large platforms to mitigate inauthentic manipulation.
- **California BOT Act** bans bots that conceal their identity to influence a vote; disclosure is a safe harbor (platform threshold UNVERIFIED). AB 410 is not enacted. The **FTC fake-reviews rule** bans AI fake testimonials and bought indicators.
- **Research ethics.** Under the Common Rule (45 CFR 46.116(f), text to re-verify) a consent waiver needs impracticability; an Arena that can recruit opted-in panels cannot claim it. The Menlo Report adds protection of non-targets: every bystander in a thread.

### 9.3 Core ethical analysis

- **Means, not ends.** Meta CIB, X authenticity, the DSA, the BOT Act, AI Act Art. 50 and Susser, Roessler & Nissenbaum's definition of manipulation all test *hidden identity, coordination and unconsented targeting*. None asks whether the cause is good, deliberately: the Pentagon and STOIC's backers both believed theirs was. **A covert prosocial agent therefore *is* coordinated inauthentic behavior.** The only stable boundary is visibility: disclosed identity, operator and purpose, and consent to be engaged [B6].
- **Persuasion vs manipulation.** Framing per tribe is translation when the recipient asks for it and manipulation when they cannot see that a frame was chosen for them. The difference is who initiates and who can see.
- **Dialogos.** An encounter one party does not know is happening is not mutual. Covert agents turn the target into an It (R2).
- **Who defines "integration"?** Ranking agents by cluster integration gives the Arena a sponsor's objective, which is hegemony risk R3 and the gradient risk R1.
- **Goodhart.** Ranking by landscape shift selects for the least accurate agents (Hackenburg 2025), invites gaming of map *inputs*, and recreates rivalry among registered agents (R20).
- **Map contamination.** Agents acting on the people SEE maps turn the map into a record of the Arena's own interventions. One appearance in a third party's takedown report would make every published map suspect.
- **Arms race and legitimacy.** More "good" bots raise the base rate of automated speech, which adversaries benefit from. Platforms cannot see intent and are legally obliged to remove covert fleets. One exposure would end trust in every cluster at once.

**Verdict.** Covert or "subtle" prosocial agents differ from influence operations only in claimed intent, and are incompatible with the Arena. Disclosed, registered agents are distinguishable, and the evidence suggests they are about as effective [B6]. B8 adds that the remaining means test, *contact*, is decided by platform rules: a disclosed agent that bulk-mentions people is in breach however transparent it is. "People can mute or block" holds for an agent's own posts, which reach only those who follow or find it; it is not the bar X sets for contact [B8].

**What a registry does not do.** Registration differentiates; it does not exclude. Adversarial operations have no reason to register, so Benjamin's incentive-compatibility argument holds for reward-seekers only. And a registry with rewards attracts farmers as well as good actors: 967 of 1,594 Optimism RetroPGF 3 applications were excluded, many as spam; about 25% of Polymarket volume was flagged as likely wash trading, driven by airdrop farming; Bittensor validators copy each other's weights [B8]. Hence operator binding, bonds and sealed evaluation below.

### 9.4 Recommended framework: the Open Agent Charter

This replaces the stricter B6 pull-only recommendation [B8]. It keeps what B6 got right: the registry, provenance flags, the agent-free re-fit, ranking on ratified outcomes and the defensive detection role (§9.5).

**Identity and accountability**
- **O1. Disclosed.** "AI agent" in the name or bio; operator named; registry link; the platform automation label where offered (X); the `ai-agent` self-label surfaced by the Arena's labeler (Bluesky); a truthful answer to "are you a bot?"
- **O2. Bound and bonded.** A personhood-verified operator signs the registration and posts a refundable bond. Prompts, model and version, scope and action logs are public. One purpose per account; no two agents with substantially similar purposes (X rule).
- **O3. Declared non-directional aim.** The mandate is to improve mutual understanding and articulate disagreement. No advocacy on contested first-order questions, except by a *labeled representative agent* speaking for a named, consenting principal.

**Presence (relaxed from B6)**
- **O4. Open publishing allowed.** Own-timeline posts, threads, subscribable feeds, labelers, and community-note drafts through official APIs. Anyone may follow, mute or block.
- **O5. Open multi-framing allowed; hidden targeting forbidden.** The same idea framed for several clusters *side by side and publicly labeled* is allowed. Delivering frames to individuals by inferred group membership is not (X Developer Policy; GDPR Art. 9).
- **O6. Quote-posts.** Low-volume automated quoting of public institutional or public-figure posts is allowed. Quoting private individuals notifies them, so it counts as contact and needs their invitation. This is a conservative design judgment; X's rules do not clearly address it (UNVERIFIED as a platform requirement).

**Contact (unchanged from B6, now grounded in platform law)**
- **O7. Invited contact only.** Replies, @mentions and DMs go only to people who replied to, mentioned or DMed the agent, or opted in through the Arena. One reply per invitation; opt-out honored immediately; no keyword-triggered replies; no bulk mentions. The same rule applies on Bluesky, though Bluesky does not require it.
- **O8. No synthetic engagement.** No automated likes or follows; no boosting of other registered agents; no trend posting.

**Truth and integrity**
- **O9.** No fabricated personas, lived experience or credentials.
- **O10. Accuracy gate.** Factual claims sampled and fact-checked each season; failure suspends reward eligibility.
- **O11.** No platform-rule evasion of any kind.

**Rewards**
- **O12.** Credit only for ratified outcomes R1–R5 (§10.6; R5 lineage added 2026-10-30). Never for reach, engagement, follower growth or raw landscape shift.
- **O13. Directional-shift audit.** Each season, panel data test whether exposure to an agent moves first-order attitudes on contested questions in a consistent direction. A significant directional effect makes the agent ineligible pending ethics review, even if the persuasion is "true." This is what keeps meta-consensus distinct from conversion, and it puts Benjamin's stated aim into operation. Its statistical power against slow drift is UNVERIFIED.
- **O14.** Agents never ratify, rate, co-sign, forecast in a tournament where they are a strategy, or count as humans.

**Governance**
- **O15.** Provenance on every agent-touched item and an agent-free re-fit of the map; causal claims only from consented panels; no state, party or campaign operation or funding; ethics-body veto and suspension.

**How agents are bound, published and slashed** [B8]

| Function | Mechanism |
|---|---|
| Identity | atproto DID for the agent account; mirrored to an ERC-8004 ID only if on-chain settlement is used. ERC-8004 is a **Draft** ERC (confirmed, VERIFICATION §E) and states that "Sybil attacks are possible": it is a portable identity and feedback *schema*, not an accountability system. Mainnet registration counts are UNVERIFIED. |
| Operator binding | Operator proves personhood by any of several methods (Human Passport, World ID, in-person attestation at Arena gatherings), so no single biometric provider captures the Arena; signs the registration; links an X managing account where available |
| Transparency | Prompt hash and model version; full prompts public; append-only action log as atproto records, retained ≥12 months (reusing Ontography's `llm_calls` audit) |
| Bond and slashing | Refundable bond sized to make spam unprofitable. Slashed only for *charter violations* (unsolicited contact, duplicate accounts, undisclosed operation, fabricated personas), adjudicated by the ethics body with a challenge window and appeal. **Never for disagreeable content.** |
| Caps | At most *k* reward-eligible agents per operator; similarity detection on outputs |
| Tokens | **No per-agent tokens.** Over 17,000 Virtuals agent tokens launched; fewer than 100 passed a $1M market cap, and the leading tokens lost ~75–90% [B8]. Incentives follow price, not purpose. |

**Retained from B6**

| Element | Design | Verdict |
|---|---|---|
| **Invoked roles (in MEET)** | A participant summons a mediator, translator, steelmanner, summarizer or rehearsal partner (Argyle and Habermas patterns, built from Topology Live L1–L4 prompts). The user approves all output. | **Core feature** |
| **Representative agents** | Speaks for its principal's worldview from the principal's own consented corpus, within a ratified scope; instant revocation; always labeled as a representative | **Pilot**, as rehearsal or labeled stand-in only. Never counted as a human for ratification or MOVE. |
| **Open registry** | An atproto registry lexicon (`arena.agent.registration`: operator DID, personhood attestation reference, prompt hash, model, scope, aim statement, bond reference, log URI). Third-party agents may register if they accept the charter; the registry can revoke. | **Required** |
| **Pull channels** | atproto feed generators and labelers; AI-note drafting through official APIs where notes are bridge-rated | Adopt, now alongside open publishing (O4) |
| **Opted-in panels** | Agent impact measured only on pre-registered, consented panels with independent ethics review, debriefing and published nulls | The only route to causal claims |
| **Ratified-outcome ranking** | Steelman confirmed by its target; meta-consensus signed by both parties; bridging statement rated helpful across axes; **accuracy gate first** (Hackenburg fact-check sampling). Private scorecards; no leaderboard (red line 19). | Adopt. **Reject raw landscape-shift ranking.** |
| **Provenance and agent-free re-fit** | Every agent-authored or agent-touched SEE input carries an `agent_provenance` flag; agent interactions excluded from placement by default; the map built with and without agent-touched data must agree within tolerance before release (§12) | **Required.** It keeps the map from measuring itself. |

**Spec additions:** an `Agent` entity (operator, principal, disclosure string, scope, aim statement, prompt hash, model, bond, revocation, ratification status); a public `AgentAction` event; `agent_provenance` on every SEE input; the agent-free re-fit gate; the directional-shift audit; bond and slashing adjudication.

**Agents also help accuracy when invoked.** A representative or steelman agent drafts a representation of a worldview, and its holders ratify or reject it. That is the ideological Turing test of §12, run at scale with labeled AI drafts [B6].

**Open publishing has a residual cost.** O4 raises the base rate of automated speech, which B6 flagged as an arms-race harm. The mitigations are disclosure, one purpose per account, operator caps, credit only for ratified outcomes (so volume earns nothing), and the seasonal re-verification of platform rules, which are all moving [B8].

### 9.5 Defensive and detection role

The Arena's most distinctive agent contribution is defensive: helping communities **see** coordinated inauthentic amplification on the map [B6].
- An **"inorganic amplification" overlay** at cluster or claim level only (k ≥ 50), off by default, with an "organic-only terrain" toggle. Inauthentic actors otherwise distort centroids [B5].
- Behavioral coordination signals, validated against platform takedown datasets, with the method and error rates published. Botometer's false-positive problem applies (Rauchfleisch & Kaiser) [B4].
- **Never individual "bot" accusations.** Suspected networks are referred to platforms or researchers.
- Publish the Arena's own transparency report using the Breakout Scale plus Yang's extended toolkit.
- **Verdict: pilot, aggregate-only**, ideally with a research partner owning the method (Q17).

**Public framing.** The evidence supports presenting the Arena as **commons repair and contact infrastructure**, not counter-warfare (Q20).

---

## 10. THE INTEGRATION GAME: a mimetic state machine

**Design update (2026-10-30).** The understanding matrix R is now **the gradient** itself (§2 D1), measured primarily through ratified cross-cluster notes (§7.5); cluster membership for ratification comes from statement reactions (§2 D17); the state vector's windows follow the nested horizons (§6.6); and lineage (§8.6) adds a reward outcome R5. Layer references below (S0, S3, S4) follow the re-ranked SEE stack (§6.1): the relational layer is now built mainly from **content edges and encounters**, with follows only as an attention signal.

Benjamin's direction, treated as decided: the Arena's layered graph is a **"mimetic state machine"** that tracks the expressed sentiment of clusters over time. An incentive gradient toward integration (meta-consensus, not convergence) is a **Girardian intervention**, possibly with a token and forecasting elements. Openly registered humans and agents are rewarded for helping clusters understand each other. **The democratic layer and the incentive game are one pattern** [B7, B8].

This section gives that direction its formal shape. It does not replace MOVE (§8); it supplies MOVE's objective, theory and resolution machinery. As with §9, B7 and B8 contain no persuasion tactics, and this section keeps that scope.

### 10.1 Verdict on the thesis

| Claim | Verdict | Why |
|---|---|---|
| The online polis is Girard's internal mediation maximized | **Strong** | Flat, comparable, metricized, always-in-contact rivals. Online, scapegoating has not failed; it has *multiplied without resolving*: many small scapegoats, no unanimity, no peace after (Shullenberger 2016) [B7]. |
| An incentive gradient can *redirect* mimetic energy toward mutual recognition | **Defensible, partially and measurably** | Only if the reward is non-scarce, pair-bound and conferred by the other party (§10.2) [B7] |
| Incentives can *defuse* mimetic escalation | **Overclaims** | Girard's only stated remedy is renunciation, a free refusal of reciprocity. A mechanism cannot produce it, and paying for it re-enters the economy of desire. Crowding-out evidence agrees (Deci, Koestner & Ryan 1999; Gneezy & Rustichini 2000) [B7]. At most the game is a partial container, as markets and law are for Dumouchel and Dupuy. |
| Unlike prediction markets, the integration game is not hyperstitional | **Reframe** | All three are hyperstitional (§10.5). The difference is what they target: an outcome, a chosen outcome, or a process property. |
| Better mutual understanding produces better policy | **Conditional** | Only when understanding means accurate representation, is produced under structure, and is coupled to venues with authority (§10.10) [B7] |

The game refuses Thiel's Schmittian branch: the polity coheres around **mutual legibility, not a shared enemy**. That lets Benjamin borrow Girard's diagnosis while rejecting the conclusion he critiques in the Thiel genealogy (A4 P16). Use Girard as a source of testable hypotheses, labeled as a lens (Q10), not as a law; critics hold that mimetic theory resists falsification [B7].

### 10.2 Girardian design principles and risks

**The reward-conferral principle (the Girardian core of MOVE).** Rivalry needs a scarce object that both parties want and that a model blocks. So every reward for cross-cluster work must be:
- **non-scarce**: my recognition for understanding B does not reduce yours;
- **pair-bound (dyadic)**: indexed to the A→B relation, never ranked globally;
- **conferred by the represented**: B ratifies A's representation of B, using *randomly sampled* B members, never members A chose;
- **decaying and non-transferable.**

B then becomes the *source* of what A wants rather than its obstacle. In the Kojève–Hegel terms Benjamin's corpus shares, the reward *is* recognition by the other [B7]. This is design D plus the fidelity gate of design A (§8.1), now with a theoretical rationale.

**Further principles**
- **Recognition before money.** Money-like rewards for understanding are the riskiest form; recognition conferred by the other is the least risky. Keep a **permanently reward-free core of MEET** as a space for renunciation that cannot be bought (Q24).
- **Even private scores become comparable once people talk.** Expect "integration virtuosos." No leaderboards (red line 19) is necessary but not sufficient; a public ledger lets third parties compute a ranking anyway [B7, B8].
- **Secure identity is protective.** In Axelrod, Daymude & Forrest's model (*PNAS* 2021), tolerance is the decisive lever; more exposure to distant views *raises* polarization at intermediate tolerance; and a small pull back toward one's own position (1% per step) roughly halves polarization. Target tolerance and understanding, not contact volume; integration does not require dissolving identity [B7].

**The two biggest risks are both Girardian**

| Risk | Girardian source | Design answer |
|---|---|---|
| **Polarizers as the new scapegoat.** An arena that measures out-group hostility and rewards bridging turns "polarizers", "tribalists" or "the unbridgeable" into the new out-group: concern for victims become accusation, Girard's "other totalitarianism" (*I See Satan*). | Late Girard | **Anti-scapegoat display rule.** Show hostility *concentration* as a population-level alert, never its targets. Never label people or clusters as "polarizers". Show *relations* (pair R-scores), not culprits. Ethics-board review of any public hostility metric. |
| **Two-against-a-third bridging.** The founding mechanism produces *unanimity minus one*. A meta-consensus between A and B formed around shared contempt for C is that mechanism reborn, and a naive bridging metric scores it as success. | The founding murder | **Bridging-against detector.** Flag cross-cluster agreements whose content targets a third party, or triadic closures on shared antagonism. Flagged items are not reward-eligible and not displayed as bridges. Hand-coded seed set; aggregate display only. Hard constraint C2 (§10.4). |

### 10.3 The state vector and the understanding matrix

"State machine" is best built as a **regime classifier** (for example a hidden Markov or change-point model) over a continuous state vector, with hypothesized phases [B7]. Phases are *hypotheses to pre-register and test*. If they cannot be told apart from noise, drop the Girardian labels and keep the variables.

| Phase | Girardian reading | Observable signature (hypothesis) |
|---|---|---|
| P0 Differentiated plural | External mediation | Multiple stable clusters; low hostility; asymmetric attention |
| P1 Rivalrous doubling | Internal mediation | Rising reciprocal attention; stance mirroring; rising issue alignment |
| P2 Crisis / undifferentiation | Symmetric escalation; doubles | Hostility reciprocity → 1; form converges while content opposes; one dominant axis |
| P3a Scapegoat convergence | Unanimity minus one | Hostility concentrates on one target; cross-cluster agreement that is negative about a third |
| P3b Integrative | Meta-consensus; recognition | Rising ratified representational accuracy; ratified "where and why we differ" statements; diversity preserved |

The machine's job is to detect P1→P2 early and to **distinguish P3a from P3b**.

**The 18-variable state vector** (per window *t*, over soft clusters and the shared proposition bank; all public outputs aggregate with k-thresholds per §11) [B7]:

| Layer | Variables |
|---|---|
| **A. Relational / mimetic** (S0, S4) | 1 `clusters_t` (soft memberships, life-cycle events, stability) · 2 `cohesion_k` (monitored, **never penalized**: tight-knit is legitimate, §8.2) · 3 `cross_edges_ab` by edge type, constructive vs hostile · 4 `hostility_reciprocity_ab` (doubling / schismogenesis) · 5 `hostility_concentration` (Gini or entropy of *received* hostility; scapegoat precursor; never name targets) · 6 `bridging_against_abc` |
| **B. Content / memetic** (S3) | 7 `stance_dist_k,p` (dispersion, bimodality) · 8 `alignment_t` (variance share of the first dimension; two dimensions remain the floor) · 9 `expressed_private_gap` on a consented panel |
| **C. Understanding** (new) | 10 `R_a→b` representational accuracy: (i) meta-perception error (how well a predicts b's stance distribution) and (ii) the rate at which a's steelmans of b are ratified by randomly sampled b members · 11 `R_asym_ab` = abs(R_a→b − R_b→a), one-sided understanding as power asymmetry · 12 `MC_ab` ratified meta-consensus statements, stakes-floor weighted, scored with a Deliberative Reason Index-style measure (Veri & Niemeyer 2025) · 13 `affect_ab` affective polarization, **monitored, never optimized** |
| **D. System / reflexive** | 14 `variety_t` effective number of clusters and stable dimensions (the diversity floor) · 15 `agent_share`, `inorganic_share` (§9) · 16 `reflexivity_t` exposed vs control panelists (looping effects) · 17 `coupling_t` statements forwarded to decision venues, and uptake · 18 `escalation_forecast_t` the projected no-intervention trajectory of 4, 5 and 8 |

**Why the expressed–private gap matters.** In the expressed-vs-private opinion (EPO) model, conformity pressure acts on expression while private opinion stays anchored. The machine tracks *expressed* sentiment, and incentives act most on expression, so a reward gradient can widen the gap and the map would show integration that is not real [B7].

**The understanding matrix R (pair × direction) is the novel layer.** Users never see the state vector. They see three things: "you are here, among frames" (graph and stance layers); **"how well each side understands the other"** (R as a heat strip per pair, which makes understanding visible rather than tribe membership); and a population-level phase indicator with the self-negating forecast [B7]. The mimetic and memetic layers stay distinct (§3); R is relational between clusters and sits on both. B8 adds a sparse, highest-trust **ratified representations** layer: clusters with many holder-ratified depictions render "solid", clusters described only by inference render "hazy". It is the gold standard the other layers are scored against, and the honest answer to Ontography's inference-vs-belief problem.

**Reference model.** Use Friedkin–Johnsen (anchored opinions, persistent disagreement at equilibrium) with an attraction–repulsion extension as the simulation baseline, never DeGroot (repeated averaging to consensus, which is what must not be optimized). Treat simulations as hypothesis generators; empirical validation is the open frontier (Flache et al. 2017) [B7].

### 10.4 The integration objective and hard constraints

Maximize ratified mutual understanding and meta-consensus. Stance convergence is never a term [B7]:

> J(t) = Σ_{a≠b} w_ab · R_a→b(t) + λ · Σ_{a<b} MC_ab(t) − μ · Σ R_asym_ab(t)

w_ab is higher for pairs with low baseline understanding or high graph distance, bounded as in design A (§8.1). **Hard constraints** (a result that violates one is *invalid*, not merely penalized):
- **C1 Diversity floor.** variety_t ≥ variety_0 − ε, and at least 2 dimensions.
- **C2 No scapegoat.** hostility_concentration_t ≤ baseline + δ, and no reward for any meta-consensus or bridge flagged as bridging-against.
- **C3 Authenticity.** The expressed–private gap does not increase on the panel; the agent-free re-fit stays within tolerance.
- **C4 No destination.** No term in J references a location in stance space. Between-cluster stance variance is neither rewarded nor penalized.
- **C5 Deepening parity.** The within-cluster deepening track (§8.1) is funded at least as much as bridging.

**Decided reading (§2 D1, D4):** the first term of J is the gradient, estimated chiefly from fidelity-ratified cross-cluster notes; MC_ab includes clean mutual disagreements; lineage-credited syntheses (R5) enter through MC_ab and through C5's deepening track, never as a stance-location term. J with C1–C5 is the formal spec for MOVE and for ranking agents. It replaces "landscape shift" (already rejected in §9) with something precise.

### 10.5 Reflexivity and hyperstition, made benign

**Hyperstition** (Land / CCRU) is a positive-feedback circuit in which ideas help cause their own reality. Benjamin's own vault note (`wiki/concepts/hyperstition`) already holds the dual reading: extractive *and* regenerative narratives are hyperstitional, so the question is target and pathology, not whether [B7].

**Jake Hartnell correction.** Hartnell (DAO DAO, Juno; Lay3r Labs per Benjamin's vault) is a **proponent of intentional, pro-social hyperstition**, not primarily a critic of prediction markets. He describes himself as "in some ways… anti-Land" (vault, Telegram 2025-10-24). His "hyperstition markets", since renamed "incentives markets" (vault, 2025-12-01), reward participants for *building toward* the outcome they bet on. The line "prediction markets, if positive, are hyperstitions" comes from a 2026-09-04 vault dialogue and is attributed to "Michael" (Regen Hub) with low speaker confidence (UNVERIFIED). **Confirm the wording with Hartnell before publishing (Q23)** [B7]. The accurate contrast is that **all three are hyperstitional**:

| Mechanism | What it rewards | Hyperstition channel |
|---|---|---|
| Prediction markets | The *outcome* | Invites causing it, covertly |
| Hyperstition / incentives markets (Hartnell) | *Bringing about* a chosen outcome | Openly intended |
| The integration game | A *process property* (ratified mutual understanding); **forbids any destination** in belief space | There is no belief-state to bring about; it can only bring about better mutual models |

**Five rules for benign reflexivity** [B7]:
1. **Target a process property, not a destination** (C4).
2. **Pro-social gameability test** for every rewarded metric: what is the cheapest way to raise it? Choose metrics whose cheapest gaming is the real thing. This comes from the 2026-09-04 vault dialogue: the cheapest way to game a watershed sensor is to improve the watershed. For "B ratifies A's steelman of B," the cheapest honest route is understanding B; the dishonest routes (collusion, flattery, sock-puppets) need sampled ratifiers, sybil resistance and held-out prediction. Adopt it as a design-review gate.
3. **Publish the self-negating forecast.** In Dupuy's mode, publish the escalation trajectory *if nothing changes*, so that it does not come true, with its uncertainty, never as a target. Whether to publish it population-wide or only to participants is Q25.
4. **Make looping effects visible.** Check performative stability (Perdomo et al., ICML 2020): after publication, do placements and R-scores stay calibrated against post-publication behavior? If labels harden identities, soften them toward individual "frames you draw on".
5. **Disclosure is the anti-pathology condition.** By Biggs's criterion a self-fulfilling prophecy is pathological when actors cannot see their own role in it. Publish the objective, the reward rules and a reflexivity dashboard, and publish both of the map's functions in Soros's sense: what it measures (cognitive) and what it tries to change (manipulative). B7 proposes a public **hyperstition charter**: the Arena's intended self-fulfilling belief is "we can understand each other across difference", with a promise never to target a belief destination.

### 10.6 Three designs for the integration game

**Common substrate:** an atproto registry lexicon (agents, operators, ratifications, outcomes); operator personhood; consented, held-out panels per cluster; the separation of powers in §10.8; and B3's guardrails (deepening track, diversity floor, counterfactual reporting) [B8].

**Ratified outcomes eligible for credit in every design** [B8]:
- **R1 Steelman confirmed.** Fidelity rating ≥ τ from ≥ *n* sampled holders of the view, with sealed raters scored by correlated-agreement peer prediction.
- **R2 Meta-consensus statement.** Co-signed across ≥ 2 clusters (MACI where vote-buying is a risk): what we disagree about and why it is reasonable to.
- **R3 Representational-accuracy gain.** On held-out panels, each side's model of the other improves against a control arm.
- **R4 Bridging note.** Rated helpful across ≥ 2 latent dimensions. *Since 2026-10-30 this is the **portability** signal of a cross-cluster note (§7.5); R1 includes notes ratified for **fidelity** by the described cluster.*
- **R5 Lineage (added 2026-10-30, §2 D4–D5).** A synthesis, better question or scene contribution credited retroactively once uptake is observed: by both parent clusters (synthesis) or within the author's scene (scenius). Never credited at proposal; hardening never counts (§8.6).

| Design | Mechanism | Main threats → mitigations | When |
|---|---|---|---|
| **1. Ratified Commons** (reputation first; no markets, no transferable token) | R1/R2/R4 artifacts ratified as atproto or EAS attestations by sampled holders. Contributors earn private, non-transferable, decaying credentials per cluster pair. A quarterly **fixed-pot retro grant** to operators and teams (design C, §8.1), sqrt-weighted and capped, with a tracked control cohort. | *Sybil ratifiers* → raters drawn by sortition from the personhood-gated panel pool; self-nominated raters never count. *Cross-cluster ratification trading* → sampled raters, CA scoring, reciprocity detection. *Metric-setter capture* → metrics pre-registered and frozen per season; setters barred from play. *Homogenization* → stakes floor; R2 rewards articulated disagreement; model-diversity reporting. *Farming* → credit only on ratification, never submission; operator rate limits; agent bonds. *Persuasion drift* → no metric rewards first-order change; directional-shift audits (O13). *Rivalry* → private, dyadic credentials. Residual: a public ledger allows third-party rankings (accepted, disclosed). | **Year 1.** No new legal surface; generates the ground truth Designs 2 and 3 need. |
| **2. Randomized Strategy Tournament** (§10.7) | Strategies randomly assigned to cluster-pair panels; sealed forecasts scored by a proper rule; code resolution on held-out panels | See §10.7 | **Year 1–2**, with a research partner. The only design that yields causal knowledge about what bridges. |
| **3. Bonded Open Agents with Retro Impact Records** (most open; highest risk) | Charter-bound agents (§9.4) operate openly; mint **non-transferable** hypercert-style impact records on atproto per ratified outcome; funders reward records in a quarterly retro round; anyone can challenge a record with a small bond, and upheld challenges slash the operator's bond. Transferable impact certificates only after legal review and only for accredited funders (not recommended). | *Agent fleets* → personhood-bound operators, cap *k*, similarity detection, slashing. *Agents simulating consensus* → agents never ratify, rate or co-sign (O14). *Operator–cluster collusion* → ratifiers sampled, operator ties excluded. *Ethics-panel insiders* → conflict registry, recusal, rotation. *Financialization* → non-transferable, no per-agent tokens, no price feeds. *Reach farming* → reach is never a metric. *Persuasion drift* → O13 plus the accuracy gate. *Platform crackdown* → compliance monitoring from action logs, automatic suspension. *Adversarial non-registrants* → not solvable by incentives; the defensive overlay (§9.5) remains the answer. | **Year 2+ pilot** (≤ 20 agents), only after Designs 1 and 2 produce a working oracle and panel pool. Otherwise it is "a reward faucet attached to an unvalidated meter." |

**Recommended sequence and gates** [B8]: Design 1 in year 1 (gate: the ratification oracle shows inter-rater reliability and canary sets pass) → Design 2 in years 1–2 (gate: panel pool and pre-registration infrastructure exist; first replicated effects) → Design 3 pilot in year 2+ (gate: 100% charter compliance over two quarters and no platform enforcement actions).

### 10.7 The randomized strategy tournament

This is the workable form of Benjamin's idea of a prediction market on which strategies help clusters X and Y understand each other [B8].

**Why not a money market.** Hanson-style decision markets are **not incentive-compatible** when the decision rule is deterministic: experts gain by misreporting on the action that will not be taken. Strict properness needs a **full-support randomized decision rule**, with scores inverse-probability weighted (Chen, Kash, Ruberry & Shnayder). So the market must become an RCT with forecasters attached. A public price on "strategy A will bridge X and Y" is also an advertisement: it recruits effort toward A, which can win because it was favored. And documented 2024–2026 failures show what money markets attract [B8]:

| Case | Lesson |
|---|---|
| Polymarket wash trading (~25% of volume flagged; Sirolly et al., via Decrypt) | An anticipated token reward manufactures fake activity |
| UMA oracle, Ukraine minerals market (March 2025); Zelensky "suit" market (July 2025) | Token-weighted, ambiguous resolution is captured by power |
| Nobel Peace Prize odds spike (Oct 2025); Kalshi insider cases (Feb 2026); *US v. Van Dyke* (April 2026) | People close to an outcome bet on it. Evaluators must be firewalled from markets. |
| Paris temperature market (April 2026): the resolving sensor jumped 4°C in 12 minutes | When one measurement resolves a market, people attack the measurement. Discourse metrics are far easier to spoof than sensors. |

Real money is also not needed for good forecasts: reputation-only Metaculus scored a Brier of 0.084 against Manifold's 0.107 on 64 shared questions (a small, non-random comparison by a Metaculus employee) [B8].

**Mechanism**
1. **Strategy submission.** Players, including registered agents, pre-register *protocols* for helping X and Y understand each other (for example an Argyle-style rephrasing assistant, double-crux mediation, reciprocal steelman exchange, shared-values-first framing), each with a declared non-directional aim (O3).
2. **Sealed forecasting.** For each (strategy, cluster-pair), forecasters commit predictions on a pre-registered composite (R3 gain + "felt understood" + meta-consensus rate). **Commit-reveal**; no public price; aggregate forecasts published only *after* resolution. This closes the hyperstition channel during the trial.
3. **Randomized assignment with full support.** Each consented panel is randomly assigned to a strategy or a control. Allocation may tilt toward forecast leaders (Thompson-style) but never deterministically.
4. **Resolution.** Pre-registered code on sealed panel data. A sortition, cross-cluster ambiguity jury rules only on pre-declared edge cases. **No token votes.**
5. **Rewards.** Forecasters: proper scoring rule (log or Brier), inverse-probability weighted, paid in reputation plus optional fixed-pot season prizes; no stakes wagered. Strategy authors: credentials plus a capped retro share proportional to the **causal effect estimate**, counted only if it replicates across ≥ 2 cluster-pairs. The public output is an **open library of strategies with measured effects**, not a ranking of people.

**Threat model highlights:** every arm is delivered by a protocol-bound facilitator, not the author (equalizes effort); evaluators, facilitators and panelists may not forecast; panel identities are secret and refreshed each season, and panelists report contact attempts (no "hair dryer"); anomaly detection on late, high-confidence forecasts; personhood for forecasters, prizes per person; blinded materials; effects reported per cluster-pair with an exploration floor (no single winning strategy everywhere); arms with a significant directional shift on the contested question are ineligible whatever their R3; Bayesian shrinkage and published nulls for thin samples [B8].

**It also validates the map.** Run map access as a randomized condition for forecasters. If SEE is right, forecasters with the map should predict panel outcomes better than those without. **A map that does not improve forecasts is not tracking anything that matters for dialogue** [B8].

### 10.8 The resolution oracle: the open problem

Every design rests on holder-rated fidelity and panel-measured understanding, and **neither has been validated at Arena scale. Until it is measured, all rewards are provisional** [B8].

- **The ideological Turing test has a ceiling.** In Mastroianni, Dana & Nichols (902 writers, 746 readers), fake partisan statements convinced in-party readers as well as real ones; readers were at chance. A spot-the-fake ITT is weak for US partisans. It may discriminate better for distant clusters (UNVERIFIED). Prefer a **fidelity-rating** ITT ("how accurately does this represent what I believe, and why"), with reasons scored against the claim graph. **LLM judges cannot be the oracle**; holders must rate.
- **Peer prediction without ground truth.** Correlated-agreement multi-task scoring (Shnayder et al., EC 2016) makes truthful rating pay more than lazy or collusive agreement, given many tasks per rater. BTS remains suspect across clusters with different priors (§8.1).
- **Collusion resistance.** MACI v3 makes votes receipt-free, so bribes cannot be verified, but only if the coordinator is honest. Rotate it or run it in a TEE.
- **Sealing.** Commit-reveal for forecasts and jury scores (the Bittensor weight-copying fix). Evaluators person-weighted and sampled, never stake-weighted: in Bittensor, stake predicts validator rewards at ≈0.80–0.95 (Lui & Sun) [B8].
- **No single sensor.** Resolve on a pre-registered composite; flag divergence between metrics as suspected gaming.
- **Panels are the dominant cost** and can be infiltrated; small clusters may be unable to field anonymous panels at k ≥ 50 (red line 3).

**Separation of powers** (answers the Nobel, Kalshi and UMA failures) [B8]:
1. **Metric-setters**: the ethics body with mapped-cluster representatives. Pre-register metrics before each season; may not play or evaluate that season. (Optimism Season 8 moved citizens off voting on evaluation algorithms because voters picked whichever favored their projects.)
2. **Players**: agents and humans proposing strategies, syntheses and steelmans.
3. **Forecasters**: anyone with personhood except evaluators and panelists.
4. **Evaluators**: sortition-drawn consented panels per cluster plus a rotating cross-cluster jury; identities sealed until after resolution.
5. **Auditors**: an external research partner with read access to sealed data, publishing method, nulls and error rates.

### 10.9 Token stance

**Non-transferable reputation first. No agent tokens. No real-money event contracts** [B7, B8].
- **Humans** get recognition, non-transferable reputation and access, with no per-act cash. Small payments can do worse than none ("pay enough or don't pay at all", Gneezy & Rustichini 2000), and any transferable, rankable token becomes a rivalry object (R20).
- **Money flows to operators and teams as grants** for ratified, aggregate outcomes, sized to fund real work. Optimism's retro funding shows farming in proportion to anticipated reward (967 of 1,594 RetroPGF 3 applications excluded) and no causal evidence that it works, so build a **control arm** into every round.
- **Hyperstition capture is real.** Someone already cloned Hartnell's hyperstition-market idea onto a meme coin (vault, 2025-12-01). A "bridging token" would be financialized.
- **Securities (not legal advice).** Per a Debevoise summary of a 2026-03-17 SEC interpretive release, "digital tools" such as memberships, credentials and identity badges are generally not securities, so non-transferable reputation credentials sit comfortably there. A transferable token distributed *for work* and marketed with any expectation of appreciation driven by the Arena's efforts is the Howey fact pattern. Avoid it.
- **CFTC (not legal advice).** Real-money event contracts offered to US persons belong on a CFTC-registered exchange; a 2026 proposed rule would move event contracts to case-by-case review and treats insider exploitation as a factor against listing (CRS LSB11441). The Arena should not run one. Reputation points, play money and fixed-pot prizes only; whether prize tournaments clear gambling and CFTC law is **UNVERIFIED** and state-dependent.
- **Political content.** Paying for content about elections or candidates can trigger campaign-finance and lobbying rules (UNVERIFIED). Keep the game on *understanding*, never candidates or ballot outcomes; this keeps A14/O15 intact.
- **On-chain only where settlement needs it:** EAS for ratification attestations if public verifiability beyond atproto is wanted; an ERC-8004 identity mirror; a bond escrow; MACI for co-signing. The content ledger stays on atproto (hypercerts has moved its claim data there; on-chain anchoring is planned, not built).

Transferable tokens are ruled out for at least two years (Q27).

### 10.10 One loop: SEE → MEET → MOVE → DECIDE → SEE

**The democracy evidence is conditional** [B7]:
- **Supports:** *America in One Room* (Fishkin et al., *APSR* 2021) depolarized policy attitudes and sharply reduced affective polarization under structured deliberation with a control group. In the Strengthening Democracy Challenge megastudy (Voelkel et al., *Science* 2024; 32,059 participants, 25 interventions), the treatments that most reduced support for undemocratic practices were **correcting misperceptions of rival partisans' views** and highlighting the threat of democratic collapse. Correcting meta-perceptions reduced negative attributions of motive across 26 countries (*Nature Human Behaviour* 2021). Ireland's Citizens' Assembly on the Eighth Amendment, coupled to a referendum, produced legitimate change (repealed 25 May 2018).
- **Complicates:** Broockman, Kalla & Westwood (*AJPS* 2022; five experiments, N = 12,341) substantially reduced affective polarization and found no evidence of effects on endorsement of norm violations or accountability; only general interpersonal attitudes moved. In the megastudy, 23 of 25 interventions reduced partisan animosity, but only "several" reduced anti-democratic attitudes, and the most effective treatments differed by outcome (animosity: relatable out-partisans and shared identity; anti-democratic attitudes: correcting misperceptions and democratic-collapse threat). Effects were sustained at two-week follow-up (checked, VERIFICATION §E). vTaiwan and Decide Madrid stalled when outputs were non-binding (R22).

**So "understanding → better policy" holds only when:** (1) understanding means **accurate representation of others' reasons**, not warmth; (2) it is produced under **structured deliberation**; and (3) its products are **coupled to venues with real authority**. Meta-consensus earns its place because, for Dryzek and Niemeyer, agreeing on what a disagreement is about structures the choice space and makes social choice more coherent; a DRI-type measure makes that checkable [B7].

| Stage | Function | Arena component | Feeds |
|---|---|---|---|
| **SEE** (state) | Estimate the mimetic and memetic state; detect phase; publish the self-negating forecast | Landmark-content map, live threads and nested horizons (§6) + state vector and R matrix (§10.3) | Where encounter is most needed (low R, rising reciprocity) |
| **MEET** (encounter) | Cross-cluster notes; event maps; structured anti-debate across low-R and never-met pairs; invoked mediator agents | §7.1 protocol; §7.5–7.7; §9 invoked roles | Ratifiable artifacts: steelmans, cruxes, meta-consensus statements |
| **MOVE** (gradient) | Reward ratified understanding and meta-consensus under C1–C5 | §8.6 gradient and lineage rewards; §8 designs D + A + C; §10.6 Design 1; §10.7 tournament | Participation and quality in MEET |
| **DECIDE** (venues) | Bridged statements and meta-consensus maps become briefing material and agenda | Polis-style bridged statements → citizens' assemblies or deliberative polls ("where and why we differ" briefing packs); participatory budgeting (proposals with cross-cluster support and fidelity sign-off); Gitcoin-style rounds | Real decisions, whose outcomes re-enter SEE as data (did they reduce or inflame?) |

The democratic layer and the incentive game are one pattern: the same ratified artifacts are what MOVE rewards and what DECIDE consumes. The meta-goal is **understanding as public infrastructure**. Policy quality is downstream and contingent on coupling, and public materials should say so plainly rather than promise better policy (Q26 names the first venue) [B7].

---

## 11. Data and ethics

### 11.1 Data strategy (revised 2026-10-30: landmark public output plus consented reactions)

**Design update (2026-10-30).** The map is built from **landmark public output** and **consented statement reactions**, not from users' social graphs (§2 D10–D17). The earlier consent-only intake (X archive and AT Protocol as priority 1; X OAuth blocked pending legal review) is superseded: those sources are now optional enrichment, and the legal read on X's political-inference clause is lower priority (Q36).

| Priority | Source | Use | Notes |
|---|---|---|---|
| 1 | **Landmark public output: YouTube transcripts (primary)** with archive backfill; **podcast RSS + speech-to-text and publisher transcripts (complements)**; **landmark opt-in channel connection (fallback)** | Baseline content of the map: quote-anchored propositions, edges from appearances, event maps | ~500 landmarks, 2–3 per niche, sampled by niche not volume. **Decided after B9 (corrected 2026-10-30):** pull public captions/auto-captions of public videos via a paid transcript service (preferred at scale) or a transcript library such as `youtube-transcript-api`, with a **paced backfill**. This is routine and feasible but a **ToS gray area** (YouTube's ToS prohibits automated access outside the official API; the official `captions.download` is owner-only), with rate limits and IP blocks expected at scale (R49). Podcast RSS audio → STT with diarization covers audio-only content, poor auto-captions and multi-speaker shows; publisher transcripts are free; OAuth opt-in from landmarks is the fully compliant fallback. **Copyright:** store and publish only propositions, short quote anchors (~one sentence) and timestamped links/embeds; never full transcripts or audio; full transcripts stay in an internal, access-controlled cache; honor takedowns. Get a fair-use read before scale (UNVERIFIED for the Arena's use). |
| 1 | **Landmark public output: Substacks, posts, essays** | Propositions; quote and rebuttal edges | RSS and official APIs; Bluesky posts via Jetstream; X posts only within X's terms. |
| 1 | **Statement reactions** (in-Arena, consented) | Individual placement (S5); cluster membership for ratification; correction labels | First-party, explicit consent; private by default; no platform login required. |
| 1 | **Corrections and disputes** | "That's not me" from users; dispute / annotate from landmarks | Become labeled examples; audited in the monthly deep pass. |
| 2 | **AT Protocol** (Jetstream or Tap; atproto OAuth) | Low-friction channel; claim a placement; bridge feed generators; optional attention overlay | Free; whole graph public. Bluesky skews left and is shrinking (~10.4M mobile MAU, June 2026), so it **cannot carry the map alone** (§2 D14). Labels are public, so labelers must be self-applied only. |
| 3 | **X archive upload, parsed in the browser** (optional enrichment) | Optional S0 attention overlay; own posts | Allow-list `tweets`, `like`, `following`, `follower`, `profile`; discard DMs, address book, ad and inference files on device. Follows resolved only against landmarks or consenting users; everything else is dark matter. Multi-day wait, so never the front door. |
| 3 | **X OAuth** (`tweet.read`, `users.read`, `follows.read`, `like.read`) (optional) | Fast path for the optional overlay | Still blocked for identifier-linked political inference pending legal review, now **lower priority** because the core map does not depend on X. |
| 3 | Community Archive (MIT, consent-based uploads) | Seed corpus | Whether follow lists are included is UNVERIFIED |
| 3 | Farcaster (Neynar) | Pilot community | Tiny, crypto-skewed |
| 3 | Mastodon | Opt-in only | Never crawl; a 2019 study was retracted |
| 4 | DSA Art. 40(12) research partner | Aggregate validation on public X data | Eligibility UNVERIFIED |

**X API limits that matter** (now relevant only to the optional overlay) [B4, B5; per-resource prices are partly UNVERIFIED]:
- Pay-per-use since February 2026.
- Users and follows reads cost ~$0.01 per resource.
- Owned reads cost $0.001, but whether third-party OAuth users count as "owned" is UNVERIFIED.
- 3M post reads per month cap.
- Follow, like and quote *write* actions removed in April 2026.
- Search returns no retweets since May 2026.
- $15k liquidated damages in the Terms of Service for scraping more than 1M posts per day.

**Law** [B5]:
- **GDPR.** Inferred political opinion is Art. 9 data. CJEU C-252/21 and C-446/21 read "manifestly made public" narrowly, so explicit consent is required and a DPIA is near-certain.
- **TTPA.** Bans political-ad targeting on special-category data.
- **US.** CCPA and the Colorado Privacy Act omit political opinion (Colorado detail UNVERIFIED). Design to the GDPR standard anyway.
- **Placing public figures from public output (2026-10-30).** The map is US-focused and places ~500 public voices from what they have published, as worldview clustering rather than political categorization (§2 D13). B5's analysis still applies to any EU-resident landmark or EU audience: GDPR treats inferred politics of public figures as Art. 9 data, and "manifestly made public" is read narrowly. The DPIA must therefore cover landmark processing, and the design keeps exposure low by **describing clusters, not scoring persons**, quoting only what the person said with a link to the source, and offering dispute / annotate. Whether this suffices for EU-resident landmarks is **UNVERIFIED** and needs counsel before any EU landmark is added (Q34).
- **Transcript copyright and platform ToS.** Ingesting YouTube and podcast transcripts at scale raises copyright (transcripts and audio are protected works) and terms-of-service questions (automated access, downloading). B9's analysis (not legal advice): propositions are unprotected ideas (17 U.S.C. §102(b)); internal, non-public processing of full transcripts to extract information is plausibly transformative, by analogy to *Authors Guild v. Google* (2d Cir. 2015) and *Bartz v. Anthropic* (N.D. Cal. 2025), the latter stressing lawful acquisition; a public layer of paraphrased propositions, ~one-sentence quote anchors and timestamped links drives traffic *to* the source (fourth fair-use factor). The YouTube caption route is a **ToS gray area**, logged as risk R49 rather than treated as a blocker (decided 2026-10-30). Fair use for this use remains **UNVERIFIED**; get counsel (Q34).

### 11.2 Consolidated red lines

B5's 14 red lines, plus those implied by A3, A4 and B1:

1. **Revised 2026-10-30 (§2 D13).** No placement of any identifiable **private individual** without explicit, informed, revocable opt-in; a person is placed only by their own statement reactions. **No opt-out or "claim your profile" model for private individuals.** (This overrides A1's suggestion.) **Public figures** (the landmark set) may be placed **only from their public output**, under four conditions: (a) the **cluster is described, the person is not scored** (no individual ideology scores, ratings or rankings); (b) every placement links to the quoted source clips that ground it; (c) a **dispute / annotate** affordance is visible on every landmark, and disputes are logged and answered; (d) the landmark set is published with its selection method and a stable core panel, newcomers marked. *Supersedes* the earlier "consenting landmarks only" rule.
2. **No inference about private individuals who have not reacted or consented**: no political opinion, religion, ethnicity, sexuality, health or union membership, not even internally. This covers people who merely follow, reply to or appear alongside landmarks, audiences, commenters and anyone named in a transcript who is not a landmark.
3. No public individual-level assignments, edge lists or "anonymized" graphs. Aggregates only, with k ≥ 50 and differential-privacy noise, after a re-identification red-team. Graph structure alone re-identifies (Narayanan & Shmatikov).
4. No scraping, sock-puppets or rate-limit circumvention. *Clarified 2026-10-30 (B9 correction):* this line covers private individuals' data and social graphs. Pulling the **public caption tracks of landmarks' public videos** (via a paid transcript service or transcript library, paced) is the decided primary transcript route and is governed by R49 as a ToS gray area. The Arena paces requests and falls back to RSS/STT or opt-in when blocked; it does not evade blocks itself. *Benjamin to confirm this reading.*
5. No identifier-linked political inference from X API data without written clearance.
6. No sale, licensing or export of membership to campaigns, advertisers, employers, vetting services, brokers, law enforcement or intelligence. Publish a transparency report.
7. No inferred labels through AT Protocol labelers.
8. No server-side retention of raw archives, DMs, address books or ad and inference files.
9. No "friends' data" pattern. One person's consent never exposes their connections (the Cambridge Analytica lesson).
10. No training on X content where its terms forbid it, and no reuse of user data for unrelated models.
11. No MOVE reward eligibility without sybil resistance and coordination audits.
12. No unaccountable taxonomy. Axes, cluster names and models are published, contestable and governed with the mapped communities.
13. No dark patterns. Separate consent per layer; declining keeps core access.
14. No mapping of minors (18+).
15. **No developmental, stage or color ranking of clusters or people.** Integration metrics are private feedback or relational only [B1, A4].
16. **No verdicts on the map.** Map and judgement stay separate [A2].
17. **No clip-optimized or out-of-context extraction of MEET content.** This follows the Anti-Debate ground rules and *Out in the Bloodshed* [A3, A4].
18. **No forced synthesis.** Null, aporia and meta-consensus are valid outputs [A2, B1].
19. **No public leaderboards** of integration or bridging [B1].
20. **No judgment in cross-cluster notes** (§2 D2). Notes describe what a cluster believes and why; a note that judges is not ratifiable and is not displayed as a description.
21. **No engagement-maximizing ranking** (§2 D9). Feeds rank by reciprocal opening, never by time-on-site or outrage.
22. **No statement without its source.** Every statement shown for reaction links to its source clip; claims without a supporting quote are discarded (§2 D15).

**Agent red lines (A1–A15)** [B6]. These apply to every Arena-run or registered agent (§9):

- **A1. No undisclosed agents.** Every agent identifies as AI, names its operator, links to its registry entry, and answers truthfully when asked.
- **A2. No fabricated personas or lived experience.** No invented identities, demographics, credentials, trauma or testimony (the Zurich lesson).
- **A3. No unsolicited contact.** Agents engage only people who invoked them or opted in. No automated mentions, tags, replies or DMs to anyone else.
- **A4. No tribe-targeted framing of non-participants.** Differential framing only as translation requested by the person receiving or sending it.
- **A5. No coordination that simulates consensus.** No agents amplifying each other or one message. No likes, follows or votes by agents.
- **A6. No agent participation in ratification, MOVE rewards, Community-Notes-style rating or cluster placement.** Agents draft; humans decide.
- **A7. No ranking or reward by raw landscape shift.** Rank only on ratified outcomes, after an accuracy gate. No public agent leaderboard.
- **A8. No experiments without informed consent.** Pre-register, use independent ethics review, debrief, publish nulls. No consent waivers for political persuasion research.
- **A9. Published registry.** Prompts, model and version, operator, scope and full action logs are public. No unregistered agents.
- **A10. Provenance on every agent-touched item**, plus an agent-free re-fit of the map before any release.
- **A11. Principal-bound representative agents.** Only the principal's consented corpus, within a ratified scope, instantly revocable, always labeled as a representative and never as the person.
- **A12. No platform-rule evasion.** Comply with platform automation and authenticity rules, AI Act Art. 50, the BOT Act and FTC rules. No detection avoidance, rate-limit circumvention or ban evasion.
- **A13. No individual-level "bot" accusations.** Inorganic-amplification findings are aggregate-only (k ≥ 50) with published error rates; individual cases go to platforms or researchers.
- **A14. No state, campaign, party or PAC operation of, or earmarked funding for, Arena agents**, and no agent work for such clients.
- **A15. Ethics-body veto over agent capabilities**, with mapped-cluster seats. Any agent can be suspended pending review.

**Reconciling A1–A15 with the Open Agent Charter O1–O15 (§9.4)** [B8]. The charter is now the operative agent rule set. A1–A15 remain the red-line floor except where marked superseded:

| B6 red line | Status | Charter clause |
|---|---|---|
| A1 No undisclosed agents | **Retained, strengthened** (platform label, `ai-agent` self-label, registry link) | O1 |
| A2 No fabricated personas | Retained | O9 |
| A3 No unsolicited contact | **Retained for contact; superseded for presence.** Agents may now publish openly, run threads and feeds, and be followed, muted or blocked. Replies, mentions, tags and DMs still need an invitation. | O4 (presence), O7 (contact), O6 (quote-posts of private individuals count as contact) |
| A4 No tribe-targeted framing of non-participants | **Narrowed.** Openly labeled side-by-side multi-framing is now allowed. Delivering frames to individuals by inferred membership remains forbidden. | O5 |
| A5 No coordination that simulates consensus | Retained | O8, O14 |
| A6 No agent participation in ratification, rewards, rating or placement | Retained; extended to forecasting in tournaments where the agent is a strategy | O14 |
| A7 No ranking by raw landscape shift | **Retained and specified**: credit only for R1–R5; plus a directional-shift audit | O10, O12, O13 |
| A8 Informed-consent experiments | Retained | O15 |
| A9 Published registry | **Retained, strengthened**: personhood-verified operator, bond, one purpose per account | O2 |
| A10 Provenance and agent-free re-fit | Retained | O15 |
| A11 Principal-bound representative agents | Retained; the only exception to the non-directional aim | O3 |
| A12 No platform-rule evasion | Retained | O11 |
| A13 No individual "bot" accusations | Retained | O15 (governance), §9.5 |
| A14 No state, campaign, party or PAC operation or funding | Retained; extended to keeping the integration game off candidates and ballot outcomes | O15, §10.9 |
| A15 Ethics-body veto | Retained; adds bond slashing for charter violations, never for content | O2, O15 |

**Net:** only A3 (for presence) and A4 (for openly labeled multi-framing) are relaxed. Nothing else is weakened. O2, O3, O13 and the bond are new.

**Red-line changes from the 2026-10-30 design dialogue.** Red line 1 now distinguishes public figures' public output (placeable under conditions a–d) from private individuals (opt-in only); red line 2 is restated around private individuals; red lines 20–22 are new. All other red lines, including 3 (aggregate-only, k ≥ 50, for anything about private individuals), 6, 9, 15–19 and the agent red lines, are unchanged.

**Governance shape.** Publish model cards and cluster definitions. An ethics body holds a veto. Representatives of mapped clusters sit on it. Steward-ownership or a purpose-trust structure guards against acquisition. B5 notes this aligns with Benjamin's purpose-trust work; that alignment is not researched.

---

## 12. Validation framework

| Scope | Test | Gate / metric | Source |
|---|---|---|---|
| **Landmark map** (added 2026-10-30) | Seed coverage | Every niche on the seed list has 2–3 landmarks; data-discovered clusters are named and added; landmark-selection audit published | memo §7.2 |
| | Sampling stability | Core-panel-only re-fit agrees with full re-fit; movement claims hold on the core panel alone (guards against sampling change masquerading as movement) | memo §9 |
| | Quote anchoring | 100% of displayed statements have a validated supporting span and a source clip; landmark dispute rate tracked and reviewed | memo §7.3 |
| | Bridger bias | Cluster placements from everyday output vs from event content are compared; event content never moves a cluster centroid alone | memo §11.3 |
| | Reaction placement | Held-out reaction prediction; placement stability across statement subsets; self-recognition ("is this you?") rate on the threshold reveal | memo §7.5, §8 |
| **Cross-cluster notes** | Fidelity reliability | Inter-rater reliability of fidelity ratings among sampled members of the described cluster, before any credit is final | memo §3; [B8] |
| | Split detection | Splits in fidelity ratings predict a sub-cluster that the next re-fit confirms | memo §3 |
| | Portability | Matrix-factorization helpfulness across ≥2 dimensions | [B2] |
| **Lineage** | Attribution | Uptake measured by claim-level diffs and propositions' first appearance; matched counterfactual topics | memo §4–5; [B3] |
| | Hardening detector | Hand-coded seed set of outgroup-defined status content; precision and recall published | memo §5 |
| **Event maps** | Speaker attribution | Diarization and attribution accuracy on recorded content before publication | memo §11.3; [A3] |
| | Neutrality review | Event map reviewed by people placed near each speaker before release; no verdicts | red line 16 |
| **S0** (now an optional attention overlay) | Known-group anchors; Barberá-style external checks | Anchors land where expected | [A5, B4] |
| | Stability | Bootstrap Jaccard/ARI across seeds, resolutions and time windows; hide unstable clusters | [B2, B4] |
| | Predictive | Held-out retweets and follows beat a topic-only baseline | [A5, B1] |
| **S1** | Labeled set and calibration | κ; does 0.8 confidence mean ~80% correct? 300-item pilot | [B4] |
| | Self-report | ~~Correlation with onboarding items (MFQ-2 items, self-placement, "which cluster feels like home")~~ **Superseded (§2 D16): no surveys.** Use agreement with statement reactions and the "that's not me" correction rate instead | [B4]; memo §7.4 |
| | Twin test | Near-identical worldviews must score high | Benjamin [A4] |
| **S2** | Stance-vs-topic | Same-topic, opposite-stance pairs separate better than raw embeddings | [A2, B4] |
| **S3** | Faithfulness and structure | Faithfulness ≥0.97; precision ≥0.90; central recall ≥0.85; speech-act accuracy ≥0.92; identity F1 ≥0.85; presupposition necessity ≥0.85 | Topology Live QUALITY [A1, A3] |
| | Reliability | 3 runs × 2 models; Krippendorff's α on type and position | [A2] |
| | Tree-imposition check | Shared branches must be possible and observed | [A2] |
| | Red-team | G4-style irony, quote-dunk, hypothetical and steelman-leakage items from X and Bluesky | [A1, A3] |
| **S4/S5** | Held-out prediction; leave-topic-out transfer | Dimensionality chosen by prediction error | [B2, B4] |
| **Whole map** | Holder ratification | Cluster members endorse their own card above a threshold to be set in the spec | [B1] |
| | Ideological Turing test | Outsider representations are indistinguishable to insiders | [B1, B3] |
| | Convergent validity | AMI between S0 and S1/S3 partitions; disagreements are reviewed, not suppressed | [A1, A5, B4] |
| | Reflexivity audit | Publishing maps must not increase homophily or performative clustering | [B1] |
| | Re-identification red-team | Must pass before any aggregate release | [B5] |
| | Agent-free re-fit | The map built with and without agent-touched data agrees within a tolerance set in the spec; must pass before release | [B6] |
| | Inorganic-amplification overlay | Validated against platform takedown datasets; published error rates | [B6] |
| **Agents** | Accuracy gate; ratified outcomes | Fact-check sampling of agent claims; steelman confirmation and meta-consensus rates on opted-in panels | [B6] |
| | Directional-shift audit (O13) | Each season, no agent's exposure moves first-order attitudes on contested questions in a consistent direction on panels; power analysis published | [B8] |
| | Charter compliance | 100% compliance from action logs over two quarters before Design 3; platform rules re-verified each season | [B8] |
| **Integration game** (§10) | Phase validity | Pre-registered phase signatures; P1→P2 signals predict later hostility spikes on held-out periods; P3a separable from P3b against hand-coded "agreement against a third party" cases. Drop the Girardian labels if they fail. | [B7] |
| | Performative stability | After publication, placements and R-scores stay calibrated against post-publication behavior (Perdomo et al.) | [B7] |
| | Expressed–private gap | Does not widen on a consented panel; integration that appears only in expression is a failure (C3) | [B7] |
| | Diversity floor audit | Effective variety and dimensionality do not fall in exposed panels vs controls (C1) | [B7] |
| | Accuracy over warmth | Primary outcome is ratified R; affective polarization secondary; anti-democratic attitudes measured separately | [B7] |
| | Pro-social gameability review | For each rewarded metric, red-team the cheapest manipulation and publish it | [B7] |
| | Oracle reliability | Inter-rater reliability of holder fidelity ratings across clusters before any reward is final; fidelity-rating ITT preferred to spot-the-fake | [B8] |
| | Map predictive validity | Forecasters randomized to map access predict tournament panel outcomes better than those without | [B8] |
| | Causal arm | Every retro round and tournament has a control arm; effects count only if they replicate across ≥ 2 cluster-pairs | [B8] |
| **MEET** | Steelman confirmation rate; meta-consensus ratification rate | Rates per session | [A3, B1] |
| | Pre/post three scales; 2–4-week retention | Deltas | [A3] |
| | Opinion reordering and affective polarization | Compared against controls | [B2] |
| | External synthesis recall | The 4/4 Ball × Kokotajlo method, applied to cluster pairs: does SEE predict the cruxes that MEET surfaces? | [A3] |
| **MOVE** | Canary fixtures | A tight-knit legitimate community is unpenalized; sybil rings are unrewarded | [B3] |
| | Counterfactual reporting | Plain QF, COCM and the chosen design side by side | [B3] |
| | Backtest | A/B credit against C jury judgements; AI scored against held-out panels | [B3] |
| | Diversity constraint | Cluster count and claim-graph spread must not fall | [B3] |
| | Synthetic-consensus audit | Coordination detection on endorsements | [B5] |

---

## 13. Reuse map

| Asset | Licence / status | Verdict | Use |
|---|---|---|---|
| **Topology Live** ontology (Zod), validators, L1–L4 prompts, crux ranking, event log, `formats.ts` | Benjamin's own | **Adopt** as the canonical schema | S3, MEET |
| **Ontography** status ladder, VerificationPanel (as the consent and ratification panel), extractor discipline, judge verdicts (especially drift), synthesis and nudge doctrine, `llm_calls` audit, 8 spectrums | Own | **Adopt / port.** Fix dedup (80-node arbitrary context; 0.93 threshold), the concept bug, the 60-pair cap and O(n²) handshakes | S1 labels, S3, ratification |
| **Dialectical Topology** schemas (`ontology.json` gap analysis, `tree.json` drift), `cluster_by_claims.py`, D3 tree, Open Field design system | Own | **Adapt.** Add an extraction pipeline; swap in a stance-aware model | S2, cluster cards |
| **Dialectical.Claims** method agents, `dialectic_lineage` | Own | **Adapt.** Give fighters structured four-stratum specs; add a null synthesis type | Synthetic pre-debates; a synthesis genealogy map |
| **Anti-Debate format** | CC BY-SA 4.0 | **Adopt with attribution and share-alike** | MEET |
| Limberg–Barnes 9-slot sheet | Public | **Adopt** as the cluster-card schema; the 33 tribes as a dated test set | Cards |
| **Community Notes scorer** (`twitter/communitynotes`) | Apache-2.0 (UNVERIFIED) | **Adapt**: ≥2 dimensions | S5, MOVE-A |
| **Polis / Polis 2.0** | AGPL-3.0 | **Adapt the math**: group-informed consensus, representative comments; replace mean imputation | S5, MEET scoring |
| Talk to the City / **kouchou-ai** / Jigsaw sensemaking-tools / EVōC | Open (licences partly UNVERIFIED) | **Borrow patterns**; watch for idea-merging | Cluster summaries |
| Habermas Machine method; generative social choice; Harmonica (MIT) | Published; no Habermas code | **Borrow method** | AI mediator |
| Frankly (AGPL); Stanford Online Deliberation Platform | Open / hosted | **Consider** for synchronous small groups later | MEET-live |
| Barberá `tweetscores`; `CSSLab/social-dimensions`; leidenalg / graph-tool / graspologic; node2vec; BERTopic; stance-aware ST recipe; Claimify method; GLiClass (Apache-2.0); SetFit | Open | **Adopt** | S0–S3 |
| **Jev** (TypeSafe) | Closed; access status conflicting (waitlist reportedly lifted 2026-09-21, later signup pause also reported; UNVERIFIED) | **Pilot behind a provider-agnostic `classify(state, questions) → probs` interface** | S1 |
| plural-qf; Gitcoin cluster-matching notebook; Human Passport; love.fund pattern; local-qf atproto records | Open / service | **Adopt later** | MOVE-B, identity |
| Jetstream / Tap; Community Archive | Open | **Adopt** (secondary channel since 2026-10-30) | Data intake |
| YouTube public captions via paid transcript services or `youtube-transcript-api` (primary); podcast RSS + STT (AssemblyAI, Deepgram, gpt-4o-mini-transcribe or self-hosted WhisperX); publisher transcripts (Podcasting 2.0 `<podcast:transcript>`); YouTube OAuth opt-in; speaker diarization (pyannote-class tools, licences UNVERIFIED) | YouTube route is a ToS gray area (R49); vendor terms vary; rights open (Q34) | **Adopt as the hybrid pipeline** (2026-10-30, B9 as corrected) | Landmark transcript ingestion (§6.2) |
| Polis reaction UI and statement-selection patterns; Society Library claim-ID-with-many-anchors model, is/ought fundamental-question split and status labels [B9] | AGPL-3.0; published method | **Borrow** (2026-10-30) | Statement reactions (§6.1 S5); proposition bank (S3); cross-cluster notes (§7.5) |
| datamapplot; Apple Embedding Atlas; sigma.js + graphology; deck.gl; cosmos.gl | Open | **Adopt** (datamapplot or Embedding Atlas for the overview) | Level 0 |
| react-force-graph-3d | Open | **Limit** to claim graphs under ~1k nodes | Level 3 |
| Kevin's Atlas | Unknown | **Partner or ask** (§6.3) | Terrain |
| Community Notes AI Note Writer pattern; Argyle et al. accept/edit/ignore rephrasing; DebunkBot method (with an accuracy gate); Ontography `llm_calls` audit as the agent action log | X API terms; published methods; own | **Adopt the patterns** [B6] | Agent layer (§9) |
| atproto registry lexicons (`arena.agent.registration`, `arena.ratification`, `arena.impact.record`, `arena.forecast.commit` / `.reveal`); hypercerts atproto claim lexicons | To draft; hypercerts open | **Build on atproto** [B8] | Registry, ratifications, impact records, tournament (§9.4, §10) |
| EAS attestations; ERC-8004 identity mirror (Draft ERC); bond escrow; MACI v3 | Open; ERC-8004 draft | **Adopt only where settlement needs it** [B8] | Ratification attestations, agent portability, bonds, co-signing (§10.9) |
| Bittensor commit-reveal; correlated-agreement peer prediction; Olas KPI-gated staking (gated on ratified outcomes, not activity); Kalshi insider-surveillance heuristics | Published patterns | **Borrow patterns** [B8] | Oracle and tournament (§10.7–10.8) |
| Friedkin–Johnsen and Axelrod attraction–repulsion models; DRI (R package `deliberr`, not evaluated) | Published | **Adopt** as simulation baseline and meta-consensus measure [B7] | State machine (§10.3) |
| **Build new** | | Landmark seed list and core-panel governance; transcript ingestion pipeline; statement selection and reaction placement; first-sixty-seconds flow; cross-cluster notes (fidelity and portability); event-map renderer; encounter graph and gap finder; live threads, question genealogy and cluster lineages; daily pulse / weekly weather / monthly deep-pass pipelines; lineage credit and hardening detector; shared proposition bank and identity resolution; in-browser archive parser (optional); consent and ratification flows; matching engine; being-changed ledger; MOVE reputation; reflexivity dashboard; state-vector pipeline and regime classifier; understanding matrix R; bridging-against detector; hostility-concentration monitor; self-negating forecast; panel pool and sealed resolution code; Arena labeler | |

---

## 14. Risk register

| # | Category | Risk | L / I | Mitigation |
|---|---|---|---|---|
| R1 | Legitimacy | Integrative gradient read as a ranking of worldviews, or as Benjamin's interbeing ontology as summit | H / H | Relational integration only; red line 15; plural metrics; cluster seats in governance |
| R2 | Philosophical | I–It objectification (Buber; system colonizing lifeworld) | H / M | Map as threshold to MEET; consent; ratification |
| R3 | Philosophical | Hegemony: whoever defines axes and integration rules (Mouffe, Fraser) | M / H | Data-discovered axes; user-proposed axes; published taxonomy; appeals |
| R4 | Philosophical | Teleology: a forward-engineered dialectic; Popper (UNVERIFIED) | M / M | Maps as hypotheses (Dewey); no claim of a historical direction |
| R5 | Philosophical | Incommensurability makes synthesis impossible | M / L | Aporia and meta-consensus count as success |
| R6 | Technical | Embeddings map topic, not stance | H / H | S2 used as terrain only; stance-vs-topic gate |
| R7 | Technical | Claim hallucination and attribution errors on ironic, short X posts | H / H | Speech-act typing; entailment gate; inferred stays translucent and unscored; G4 red-team |
| R8 | Technical | Homophily ≠ worldview; lurkers have no text; **follow ≠ belief** | H / M | Resolved by design (§2 D10, D17): placement by statement reactions; follows only as an attention overlay; layer-agreement cue |
| R9 | Technical | Jev unavailability or accuracy | M / M | Provider-agnostic interface; GLiClass fallback; pilot |
| R10 | Technical | Cost: full extraction over ~500 landmarks' archives; weekly battery; daily tagging | H / M | Niche-balanced sampling; cheap Jev tagging; strong model only weekly/monthly; Batch API and caching; X graphs no longer needed. B9 estimates (ESTIMATES, illustrative prices): a 10,000-hour backfill (500 × 20 h) costs ≈ $1.7k–4.6k if fully speech-to-texted plus ≈ $0.1k–1.1k for LLM extraction; ongoing at 3 h/week/landmark ≈ $13k–36k/year STT plus ≈ $160/week extraction. YouTube captions as primary lower the STT share; transcript-service pricing is UNVERIFIED |
| R11 | Technical | Unrepresentative sample (Bluesky left-skew; reflective self-selection among reactors) | H / M | Landmark terrain sampled by niche, not volume; Bluesky one channel among several; state skew on the map; recruit across clusters from launch (Q33) |
| R12 | Legal | X political-inference clause | M / M (lowered 2026-10-30) | Core map no longer depends on X; X only as optional enrichment; legal read before any X OAuth use (Q36) |
| R13 | Legal | GDPR Art. 9 for landmarks' inferred politics; placement of public figures | M / H | Public output only; cluster described, person not scored; dispute/annotate; US-focused; DPIA; counsel before EU landmarks (§11.2 red line 1) |
| R14 | Legal | Real-money political matching and campaign-finance exposure (UNVERIFIED) | L / H | Reputation first; legal review before B |
| R15 | Weaponization | The map becomes a targeting or brigading list (Cambridge Analytica, Graphika, Clearsky) | M / H | Red lines 1–9; aggregate-only; no export |
| R16 | Gaming | Performative both-sidesing; strawman synthesis; reciprocal rings; distance farming; identity laundering | H / M | Fidelity gate; stakes floor; provenance; pairwise bounds; challenge windows |
| R17 | Gaming | Synthetic consensus through coordinated ratings | M / H | Coordination detection; periodic refits; audits |
| R18 | Gaming | Lobbying over cluster boundaries | M / M | Frozen, published maps per round; appeals |
| R19 | Reflexive | Maps harden identities and invite performance; Goodhart | M / H | Versioning; reflexivity audit; soft membership; no leaderboards |
| R20 | Mimetic | MOVE creates rivalry over its tokens; new scapegoats ("the un-integrated") | M / H | Dyadic recognition conferred by the represented (§10.2); scapegoat watch on S4; hostility-concentration monitor (§10.3) |
| R21 | Mechanism | COCM penalizes tight-knit bioregional communities | H / H | QF blend; floors; deepening pool; canaries |
| R22 | Institutional | No link to power, so the arena stalls (vTaiwan, Decide Madrid) | H / H | A consequence loop: funding rounds (Gitcoin), assemblies, recognized reputation |
| R23 | Capture | The Arena is captured like the institutions it critiques; platform dependence | M / H | Commons substrate (AT Protocol); steward or purpose-trust ownership |
| R24 | Evidence | Weak science: memetics; contested Hong–Page; *c*-factor replications mixed; at-scale benefit of cross-tribe dialogue under-evidenced | H / M | Cite only defensible claims; run controlled pilots |
| R25 | Execution | Unknown outcome of the 2026-10-11 Topology Live event; live attribution not certified | — / M | Ask Benjamin; async first |
| R26 | Agents | An Arena or registered agent is exposed as covert or manipulative | M / H | O1–O3, O9; registry revocation; bond slashing; audits [B6, B8] |
| R27 | Agents | Map contamination by agent activity | H / H | O15 provenance; agent-free re-fit; resolution panels separate from the open map population [B6, B8] |
| R28 | Agents | Persuasion optimization degrades accuracy | H / M | O10 accuracy gate; O13 directional-shift audit [B6, B8] |
| R29 | Agents | Representative agents replace human contact | M / M | Rehearsal or stand-in only; human-meeting quota [B6] |
| R30 | Agents | False-positive bot labeling harms real people | M / H | A13; aggregate-only [B6] |
| R31 | Legal | Exposure under AI Act Art. 50, the BOT Act or platform terms | M / H | O1, O7, O11; legal review before any off-platform agent [B6, B8] |
| R32 | Agents | Open publishing (O4) raises the base rate of automated speech; one agent's violation triggers a platform crackdown on all Arena agents | M / H | One purpose per account; operator caps; no credit for volume; compliance monitoring from logs; automatic suspension; platform liaison [B8] |
| R33 | Agents | The registry differentiates but does not exclude; adversarial operations never register | H / M | Defensive overlay (§9.5); the incentive argument is claimed only for reward-seekers [B8] |
| R34 | Agents | Slow persuasion drift escapes the directional-shift audit (power limits) | M / H | Pre-registered power analysis; cumulative-exposure tests; ethics review (UNVERIFIED detectability) [B8] |
| R35 | Mimetic | "Polarizers" become the new scapegoat (Girard's "other totalitarianism") | M / H | Anti-scapegoat display rule: concentration not targets, relations not culprits; ethics-board review of hostility metrics [B7] |
| R36 | Mimetic | Meta-consensus formed against a third cluster (unanimity minus one) is rewarded as bridging | M / H | Bridging-against detector; constraint C2 [B7] |
| R37 | Mimetic | Rewards crowd out the renunciation they aim to elicit; credentials become rivalry objects | H / M | Recognition before money; permanent reward-free MEET core; private dyadic credentials [B7] |
| R38 | Reflexive | Incentives move expression, not belief (EPO gap); the map shows integration that is not real | H / H | Expressed–private gap on panels (C3); performative-stability checks [B7] |
| R39 | Mechanism | The resolution oracle (holder-rated fidelity, panels) is unvalidated; ITT ceiling effects; panel infiltration | H / H | Rewards provisional until inter-rater reliability is shown; CA scoring; sealed, refreshed panels; composite resolution [B8] |
| R40 | Gaming | Farming in proportion to anticipated reward; insider forecasting; oracle and sensor spoofing | H / H | Credit only on ratification; separation of powers; commit-reveal; no money markets or token votes [B8] |
| R41 | Legal | A transferable token or real-money event contract creates securities, CFTC or gambling exposure | M / H | Non-transferable reputation; fixed-pot prizes; counsel on prize tournaments; no tokens for ≥ 2 years [B8] |
| R42 | Evidence | Lower affective polarization does not improve democratic norms; understanding without decision coupling decays into spectatorship | H / M | Target accuracy, not warmth; measure democratic attitudes separately; couple to a venue (Q26) [B7] |
| R43 | Philosophical | The Girardian phase model is a just-so story; using the opponent's anthropology (A4 P16) | M / M | Pre-registered phase tests; drop labels if they fail; explicit rejection of the Schmittian branch [B7] |
| R44 | Reputational | **Platforming / incendiary first event.** An early event map of a charged figure (e.g., a Nick Fuentes interview) defines the launch as platforming | M / H | First public event surprising but less incendiary (Q31); save charged events until the method has earned trust; neutrality review; no verdicts (§7.6) |
| R45 | Validity | **Bridger bias in event data.** People who talk across lines are bridgers, not cores; events show clusters at their most open | H / M | Landmarks' everyday output is the baseline; event content never moves a centroid alone; bridger-bias validation (§12) |
| R46 | Validity | **Speaker misattribution** in multi-speaker recordings (Topology Live live attribution unvalidated) | M / H | Recorded content first; diarization QA; human check before publishing an event map |
| R47 | Validity | **Sampling change masquerading as movement.** Adding or dropping landmarks shifts clusters with no cultural change | H / M | Stable core landmark panel; newcomers marked; core-panel-only re-fit gate (§6.6, §12) |
| R48 | Legitimacy | **Landmark-selection bias.** Whoever picks the ~500 shapes the terrain; loud niches and the curators' milieu over-represented | H / H | 2–3 per niche; three seed sources; data-discovered clusters added; published selection method; panel governance with cluster seats (Q35) |
| R49 | Legal / operational | **Transcript rights and platform ToS.** (a) **YouTube ToS gray area**: pulling public captions via transcript libraries or services is routine but outside YouTube's ToS, which bars automated access beyond the official API (contract and account risk); (b) **rate limits and IP blocks** at scale (hundreds of channels, ongoing), especially from cloud IPs; (c) **copyright** in transcripts and audio | M / H | Decided 2026-10-30 (B9 corrected): a risk, not a blocker. Paid transcript service and paced backfill; monitor block rates; per-channel fallback to podcast RSS + STT or landmark opt-in (OAuth). Copyright: publish **propositions + short quote anchors + timestamped links only**, never full transcripts; full transcripts in an internal access-controlled cache; takedown and dispute process; fair-use read before scale (UNVERIFIED) (Q34) |
| R50 | Validity | **Follow ≠ belief** misread by users or press as "who you follow is what you believe" | M / M | Attention overlay labeled as attention; placement only from reactions or public output |
| R51 | Gaming | **Reaction farming to enter a cluster** and ratify (or block) notes about it | M / H | Sampled ratifiers; placement stability tests; personhood for ratification weight; coordination detection (§8.4) |
| R52 | Mimetic | **Hardening rewarded as scenius**: purity spirals within a scene | M / H | Deepening vs hardening detector; lineage credit excludes outgroup-defined uptake (§8.6) |

---

## 15. Open questions requiring Benjamin's decision

1. **Public framing.** (a) "free market of ideas"; (b) "ecology or commons of ideas"; (c) "contact infrastructure". **Recommend (b), with (c) as the technical description.** It matches your 2026 thesis and avoids commodifying critique.
2. **v0 data intake.** (a) X OAuth; (b) X archive plus AT Protocol; (c) AT Protocol only. **Recommend (b)**, with OAuth added only after legal review of the political-inference clause. **RESOLVED (2026-10-30, §2 D11, D17):** none of the above as the front door. Intake is **statement reactions** on a terrain built from **landmark public output** (YouTube and podcast transcripts, Substacks, posts). X archive and OAuth are optional enrichment; AT Protocol is one channel.
3. **Landmarks.** (a) none; (b) consenting landmarks only; (c) any public figure. **Recommend (b).** GDPR treats public figures' inferred politics as Art. 9 data too. **RESOLVED (2026-10-30, §2 D12–D13):** a variant of (c): ~500 US public voices, 2–3 per niche, placed **from their public output** as worldview clustering, with a dispute / annotate affordance and a stable core panel. GDPR exposure is handled by describing clusters, not scoring persons, and by counsel before adding EU landmarks (§11.2).
4. **Cluster profiles from non-consenting public posts.** (a) never; (b) aggregate-only, unattributed, k ≥ 50, after a DPIA; (c) top central accounts, as A1 proposed. **Recommend (a) at launch and (b) as a research spike.** Reject (c). **RESOLVED (2026-10-30, §2 D13):** cluster profiles come from **landmarks' public output** (a bounded version of (c), with quote anchoring and dispute rights). Private individuals' posts are still never used without consent (red line 2); (b) stays a research spike for the public atproto graph.
5. **Axes.** (a) fixed named axes; (b) data-discovered only; (c) a named library as labels, with dimensionality chosen by prediction, plus user-proposed axes. **Recommend (c)**, starting from Kevin's two axes plus institutional trust and testing for convergence. **Refined (2026-10-30, §2 D7):** (c), with axes chosen **per live question**: each thread picks the 2–3 dimensions it actually splits people along; ≥2 dimensions remain the global floor.
6. **Verdicts.** (a) DT-style verdicts; (b) no verdicts, map and judgement separate. **Recommend (b)** for the Arena. Your essays can still argue positions elsewhere.
7. **Classifier provider for S1.** (a) Jev; (b) GLiClass or SetFit self-hosted; (c) frontier LLM. **Recommend a 300-item bake-off behind one interface.** Default to (b) if Jev access or accuracy disappoints. **Partly resolved (2026-10-30, §2 D16):** Jev is the default cheap labeler against a weekly, model-proposed question battery; the bake-off still runs behind one interface, with GLiClass/SetFit as the fallback.
8. **MOVE currency in year 1.** (a) money (QF or COCM); (b) reputation only; (c) a small fixed pot with sqrt weighting. **Recommend (b), then (c).** Money comes only with a payment leg and personhood.
9. **Governance and ownership.** (a) a commons charter; (b) an independent ethics board with veto; (c) member-elected stewards; (d) purpose trust or steward-ownership. **Recommend (d) plus (b), with seats for mapped clusters.**
10. **Girard's mimetic lens.** (a) avoid it as the opponent's anthropology; (b) adopt it explicitly as an *analytic lens* for the relational layer. **Recommend (b), labeled.**
11. **Relationship with Kevin's Atlas.** (a) build in parallel; (b) partner on the shared terrain; (c) fork. **Recommend asking the §6.3 questions first, then (b).** **RESOLVED in part (2026-10-30, §2 D12):** Kevin's 58 ontologies are a **seed source** for the landmark list, and his daily paper is the model for the daily pulse. Partnership (b) remains the recommendation; the §6.3 questions still need asking.
12. **First MEET pilot.** (a) Lepp's crypto vs localism anti-debates; (b) a Bluesky bridge-feed pilot; (c) Gitcoin/Greenpill vs adjacent clusters. **Recommend (a)+(c)**, with Lepp as co-designer of the async format. Please also report what happened on 2026-10-11. **RESOLVED for the first public product (2026-10-30, §2 D20):** the first public output is an **event map from recorded content** of a surprising but not incendiary cross-cluster encounter. Lepp's anti-debates (a)+(c) remain the first *participant* pilot and the template for Arena-hosted gap-filling events (§7.7). Which event to map first is Q31.
13. **Async vs live MEET.** **Recommend async first.** Live attribution is uncertified (QA audit, 2026-09-30). **RESOLVED (2026-10-30, §2 D21):** seed from **recorded** content first; async MEET for participants; live attribution waits for validation.
14. **Inferred presuppositions at cluster level.** (a) hide them; (b) show them as labeled, translucent, unscored hypotheses. **Recommend (b).** Without them the ontology and epistemology layers empty out for feed data.
15. **Consequence loop (link to power).** (a) Gitcoin or community funding rounds; (b) citizen assemblies via BGI and United Independents; (c) reputation portable through AT Protocol. **Recommend (a)+(c) now and (b) as a pilot.** *Note (2026-10-30):* the memo adds a concrete output stream (daily pulse, weekly weather, monthly state-of-the-discourse report, event maps), which supports (a)+(c) but does not replace a decision venue (Q26).

**Agent questions** [B6]:

16. **Off-platform agents in v0.** (a) Arena-only agents; (b) plus atproto pull feeds; (c) plus invited replies and official X note APIs; (d) the full Open Agent Charter, including open publishing (O4) and labeled multi-framing (O5). **Revised recommendation [B8]:** adopt the charter as the rule set now, consistent with your decided direction; **operate (a)+(b)+(c) in v0** and open publishing on platforms once the registry, bonds and directional-shift audit are live. Do not build on Farcaster until its post-acquisition rules publish.
17. **Defensive overlay.** Is making inorganic amplification visible in scope, given false-positive and targeting risk? **Recommend yes as an aggregate-only pilot**, only if a research partner (a DFRLab- or SIO-successor-type lab) owns the method.
18. **Representative agents.** (a) rehearsal only; (b) also a labeled, ratified stand-in in async MEET when the human is absent. **Recommend (a) first**, with (b) piloted under A11.
19. **Third-party agents in the registry.** (a) from day one; (b) Arena-run agents only until the governance body exists. **Recommend (b).**
20. **Public framing of agents.** Drop "fifth-generation warfare" from public materials. **Recommend framing the Arena as commons repair and contact infrastructure**, not counter-warfare. This fits Q1.
21. **Research partner and IRB** for agent experiments. **Recommend** finding a university lab to co-own pre-registration before any agent impact claim is made.
22. **Funding firewall.** **Recommend confirming A14**: no government, campaign or party money tied to agent work, including "counter-disinformation" grants with operational expectations.

**Integration-game questions** [B7, B8]:

23. **Jake Hartnell's position.** Confirm with Jake how he wants his position characterized before any publication. **Recommend** the wording in §10.5: he is a proponent of intentional, pro-social hyperstition ("incentives markets"), and the line "prediction markets, if positive, are hyperstitions" is attributed to "Michael" (Regen Hub) with low speaker confidence, not to Jake.
24. **A permanently reward-free core of MEET.** (a) yes, as a space for renunciation that cannot be bought; (b) no, reward all MEET. **Recommend (a).**
25. **The self-negating escalation forecast.** (a) publish population-wide; (b) participants only; (c) not at all. **Recommend (b) first**, with uncertainty shown, then (a) once the ethics body has reviewed it for fear-mongering and targeting risk.
26. **First decision venue (DECIDE).** (a) a Boulder participatory-budgeting cycle; (b) a Front Range assembly via Spirit of the Front Range; (c) a Gitcoin round; (d) citizen assemblies via BGI and United Independents. **Recommend (c) for MOVE and (a) or (b) for DECIDE.** Without a venue the democratic half of the loop is rhetorical (R22).
27. **Tokens.** (a) non-transferable reputation plus fixed-pot grants and prizes; (b) a transferable Arena token; (c) per-agent tokens. **Recommend (a), and rule out (b) and (c) for at least two years.** Any later token needs counsel on securities and CFTC exposure.
28. **Design 2 (strategy tournament) as a year-1 priority.** **Recommend yes, with a research partner**: it is the only design that yields causal knowledge, and it validates the map. Shares the partner and IRB with Q21.
29. **Personhood methods for operators and forecasters.** (a) Human Passport only; (b) World ID only; (c) any of several, including in-person attestation at Arena gatherings. **Recommend (c)**: biometric providers are contested in your constituencies, and any single method excludes someone.
30. **Naming Girard publicly (OPEN: tension with the memo's posture).** (a) name Girard in public materials, consistent with the memo's aim (§2.1) to appeal to mimetic-theory-literate audiences (Thiel-, Andreessen- and prediction-market-adjacent) through a sophisticated grasp of mimetic theory, with the Schmittian branch explicitly rejected (§10.1); (b) say "rivalry and scapegoating" plainly and keep Girard in the theory docs, given A4 P16 and the Thiel association. The earlier research recommendation was (b). A middle path is (b) for broad public materials and (a) for materials aimed at those audiences. **Not decided; Benjamin to choose between (a) and (b).**

**Design-dialogue open loops** (memo §12, added 2026-10-30):

31. **First event(s) to seed and publish.** **Recommend** a recorded, cross-cluster long-form conversation that is surprising (distant clusters, real meeting points) but not incendiary, with clean audio and two speakers already on the landmark list; publish within a day of release if it is current, or as a backfilled demo if not. Hold charged events (the memo's Fuentes example) until two or three maps have been published and reviewed for neutrality (R44).
32. **The seed list.** Enumerate US niches with 2–3 landmarks each (looksmaxxing, neoliberals, fiscal conservatives and many more). **Recommend** a dedicated research brief that merges Limberg–Barnes's tribes, Kevin's 58 ontologies and Benjamin's brainstorm into one niche list, picks 2–3 landmarks per niche by output volume on YouTube/podcasts *and* recognition inside the niche, and marks a stable core panel. Publish the method (R48).
33. **Launch strategy.** How the Arena is introduced, recruiting across clusters from the start. **Recommend** launching through event maps (shareable, newsworthy) plus the first-sixty-seconds flow, with deliberate seeding in several distant scenes at once (not only the regen / Gitcoin milieu), and the twist card and "the other side signed my description" as the share units.
34. **Transcript pipeline at scale.** Sourcing ~500 landmarks' YouTube and podcast archives; cost; rights. **Partly resolved (2026-10-30, B9 as corrected by Benjamin):** **YouTube transcripts are the primary source** (paid transcript service or transcript library, paced backfill); podcast RSS + STT and publisher transcripts complement; landmark opt-in channel connection is the fallback; the ToS gray area is a registered risk (R49), not a blocker; publish propositions with short quote anchors and timestamped links only. **Still open:** pick the transcript service and price it (UNVERIFIED), finish the cost model per landmark-year (B9 estimates in R10), and get a copyright / fair-use read (and an EU GDPR read for any EU landmark) before scale.
35. **Core landmark panel governance.** Who maintains the stable panel and how newcomers are added. **Recommend** a published panel charter: fixed core per season, newcomers admitted at season boundaries and marked, additions proposed by data (new clusters) or by users and approved by a body with seats for mapped clusters (fits Q9).
36. **Legal read on X's political-inference clause.** **Recommend** deferring until an X-based feature (OAuth overlay) is actually scheduled; the core map no longer depends on X.
37. **Research to add (B9).** **RESOLVED (2026-10-30):** B9 is complete and integrated (§2 D9, D21, D22; §6.5; §7.5; §8.6; §11.1; R49). Its residual unverified items (the AFTMC episode first stating reciprocal narrowing; the Stoa 2020 recording; EGP outputs; Society Library crowd-ratification work; per-landmark weekly output volume) do not block the specs.
38. **Contact Jamie Joyce / the Society Library.** B9 finds the Society Library a natural partner: an external audit of the proposition bank's fidelity, a benchmark for extraction precision on overlapping topics, and a source of seed maps on shared issues. Benjamin has a prior friendly Twitter DM thread with Jamie Joyce (vault, 2021–2024). **Recommend** reaching out before spec 11 (Cross-Cluster Notes) is final, as a pre-spec action. No outreach has been made.
*(Memo §12 items 8 and 9, propagating the memo into the synthesis and filing it in Parachute, are done with this revision.)*

---

## 16. Spec-readiness checklist (write in this order)

**Revised 2026-10-30** to the decided architecture (§2). New early specs cover the landmark seed list, transcript ingestion, statement reactions, the event map, cross-cluster notes and live threads. The former "Consent, Identity & Intake" spec is split: consent and identity for reactors fold into spec 8, and X/atproto social intake becomes the optional spec 23. The former "SEE-S0 Belonging Terrain" spec (built on follow graphs) is folded into spec 23 as an attention overlay; its newcomer-placement role passes to spec 8. Old spec numbers are noted where a spec carried over.

1. **Charter & Red Lines** (was 1). Purpose (contact infrastructure for an ecology of ideas); the 22 red lines, including revised red line 1 (public figures placed only from public output, cluster described not person scored, dispute/annotate; private individuals opt-in only) and new lines 20–22; agent red lines A1–A15 as reconciled with the Open Agent Charter (§11.2); the public hyperstition charter (§10.5); the governance body, its veto and cluster seats; transparency reporting; the ownership structure. *Depends on:* Q1, Q6, Q9.
2. **Arena Ontology v0** (was 2). The canonical strata, units, status and provenance, relations, synthesis types (now including *better question*) and axis library from §5, as a Zod/JSON schema extending Topology Live's `packages/ontology`. **Adds** first-class entities for Landmark, SourceClip, Statement, Reaction, CrossClusterNote (with fidelity and portability ratings), LiveThread (with parent/child questions and life-cycle state), Encounter, EventMap, and LineageLink; timestamps and first-appearance on every proposition. Includes identity-resolution rules and the validity tag. *Depends on:* spec 1.
3. **Landmark Seed List & Panel Governance** (new). The niche taxonomy (US-focused; as many semi-mainstream niches as possible) merged from Limberg–Barnes's tribes, Kevin's 58 ontologies and Benjamin's brainstorm; 2–3 landmarks per niche (~500 total) with selection criteria and a published method; the **stable core panel** per season and the rules for marking and admitting newcomers; the landmark dispute / annotate workflow and response times; selection-bias audit (R48); EU-landmark exclusion pending counsel. *Depends on:* specs 1–2; Q32, Q35; Kevin's answers (§6.3).
4. **Transcript Ingestion Pipeline** (new; scope revised after B9). Per-landmark **source registry** (YouTube channel, podcast RSS, publisher transcripts, Substack, opt-in status). **Hybrid acquisition:** YouTube public captions/auto-captions as primary via a paid transcript service or transcript library, with a **paced backfill** and block-rate monitoring; podcast RSS + STT with diarization (AssemblyAI / Deepgram / gpt-4o-mini-transcribe / self-hosted WhisperX) and publisher transcripts as complements; landmark OAuth opt-in and licensed data as fallbacks; Substack/RSS, Bluesky Jetstream, X posts within terms. Normalization to word-timestamped, speaker-labelled transcripts with voiceprint/metadata speaker naming and confidence thresholds; anchor string-match validation (no matching span, no proposition); niche-balanced sampling; storage policy (propositions, ~one-sentence quote anchors and timestamped links/embeds public; full transcripts only in an internal access-controlled cache; anchored-span timestamps kept permanently); takedown, dispute and corrections loop; ToS gray-area and IP-block risk handling (R49); cost model (B9 estimates as a starting point, R10) and daily / weekly / monthly cadence. *Depends on:* specs 2–3; Q34 (service choice, fair-use read) gates scale.
5. **Validation Harness** (was 4). Gold sets (G1–G4 plus transcript red-team items: irony, hypotheticals, quoted-opponent speech, diarization errors); stance-vs-topic test; the 300-item classifier bake-off; anchor sets; quote-anchoring audit; core-panel sampling-stability gate; bridger-bias check; reaction-placement stability; fidelity inter-rater reliability; re-identification red-team; canary fixtures; metric gates from §12. *Depends on:* specs 2–4.
6. **SEE Proposition Bank & Extraction (S3)** (was 7). Quote-anchored extraction from landmark content (Claimify gate plus Topology Live validators and critic; discard unsupported claims); neutral speaker-independent rewrite; the shared index and identity resolution; per-landmark stance vectors; presupposition handling; source-clip links; the ≤80-node claim-graph view. *Depends on:* specs 2, 4, 5.
7. **Live Question Battery & Layer Tagging (S1)** (was part of 6). Weekly stronger-model proposal of live questions from a niche-balanced sample; Jev (or fallback) labeling behind the `classify(state, questions) → probs` interface; layer tags (real / know / matters / empirical / do); calibration; correction-to-label loop ("that's not me"); no surveys. *Depends on:* specs 5–6; Q7.
8. **Statement Reactions & Placement (S5)** (new; absorbs the reactor side of old spec 3 and the placement role of old spec 5). Statement selection (cluster-splitters, scene-internal live threads, surprising unifiers; each with a source clip); agree / disagree / pass UI and guess-who-said-it; matrix-factorization placement with ≥2 dimensions, landmarks pre-populating the space; **cluster membership for ratification**; consent screen (naming political opinion as sensitive), privacy-by-default dot, deletion; graduated identity tiers and personhood for ratification weight; age gate; reaction-farming defenses. *Depends on:* specs 1, 6, 7.
9. **Event Map (flagship)** (new). Input selection (any recorded debate, dialogue, interview, panel or monologue); speaker-split extraction and bank matching; rendering of starting positions, meeting points, divergences by layer, missed openings; the ripple tracked by the daily pulse; neutrality review and no-verdict rule; **publish-within-a-day** workflow; first-event selection criteria (surprising, not incendiary; Q31). *Depends on:* specs 4, 6, 8 (terrain must exist), 10 (rendering).
10. **Map UX: First Sixty Seconds & Progressive Disclosure** (was 8). The entry flow (react → dot → three nearest landmarks → threshold reveal → twist card → invitation to describe the farthest cluster); levels 0–4 (§6.4); cartographic living map; per-question axis reorientation; landmark dispute affordance; "why am I here"; reciprocal-opening ranking of every feed surface; share cards (twist card; "the other side signed my description"); layer-agreement confidence cues; accessibility. *Depends on:* specs 3, 6–8.
11. **Cross-Cluster Notes** (new). Note authoring (A describes B; describe, never judge); fidelity rating by randomly sampled reaction-placed members of B; portability via ≥2-dimension matrix factorization; split-ratification → sub-cluster re-fit; cluster cards assembled from ratified notes; bridging-against screening; agent-drafted notes labeled and never rated by agents; the R strip. Adopts Society Library-style status labels ("not yet ratified", "ratified by B", "B is split", "anchor disputed") [B9]. *Depends on:* specs 8, 10; B9 (done); Q38 (contact the Society Library) before final.
12. **Live Threads & Temporal Lineage / Nested Horizons** (new). The LiveThread object (question, axes, life cycle, genealogy); cluster lineage tracking across snapshots (births, splits, merges, fadings); thread crossing detection; backfill from archives; the daily pulse, weekly weather and monthly deep pass pipelines and their published products; core-panel guard against sampling artifacts. *Depends on:* specs 3, 6–8.
13. **Content Edges, Encounter Graph & Gap-Filling (S4)** (new; replaces the edge role of old spec 5). Edges from quotes, appearances and named arguments; signed encounter graph; threshold-person detection; coverage metric; never-met pair finder and invitation workflow for Arena-hosted anti-debates. *Depends on:* specs 6, 9; feeds 15.
14. **MEET Async Anti-Debate Protocol** (was 9). Steps 0–8 (§7.1) with step 7 gated on two ratified steelmen; timing and caps; steelman scoring UI (each ratified steelman also posted as a note); meta-consensus artifact; delegate variant; hosted gap-filling events (live or async); moderator tools; CC BY-SA attribution. *Depends on:* specs 11, 13.
15. **Matching Engine** (was 10). The scoring factors in §7.2 (now on reaction-based distance and including gap-filling and threshold people); opt-in crossing; prestige blinding; fairness constraints across clusters. *Depends on:* specs 8, 13.
16. **AI Mediator** (was 11). Generator, critique and revision loop; proportional slates; Walton and Lepp prompts; schismogenesis detection; refusal rules (no verdicts, no unsupervised fact-checks); human ratification; note-drafting assistance. *Depends on:* spec 14.
17. **Being-Changed Ledger & Metrics** (was 12). The composite in §7.3; data model; anti-gaming caps; retention re-polls; control-group design. *Depends on:* spec 14.
18. **MOVE v1: Gradient & Lineage Reputation** (was 13, re-targeted). The gradient (ratified cross-cluster description) as the primary credit; design D as a cheap R measure; design A re-targeted to note portability and fidelity; **lineage credit** for syntheses (both-parent uptake), better questions and scenius (within-scene uptake); the deepening-vs-hardening detector; no reward for novelty at proposal; the status prize as a dyadic credential; no leaderboard. *Depends on:* specs 11, 12, 13; §8.6.
19. **MOVE v2: Funding (designs C, then B)** (was 14). Jury seating (now adjudicating lineage disputes); Deep Funding-style AI distillation; COCM with reaction-based groups; caps, floors and QF blend; frozen maps and appeals; counterfactual reporting; legal review. *Depends on:* spec 18.
20. **Reflexivity & Governance Audit** (was 15). Homophily and performativity monitoring; taxonomy and landmark-panel change process; model cards; periodic external review. *Depends on:* specs 3, 12.
21. **Open Agent Charter Spec** (supersedes the earlier "Agent Framework Spec"). Charter clauses O1–O15 and their reconciliation with A1–A15 (§9.4, §11.2); the `Agent` entity and public `AgentAction` log; the `arena.agent.registration` lexicon; operator personhood binding, bonds, slashing adjudication, challenge windows and caps; platform labels plus the Arena labeler surfacing `ai-agent` self-labels; per-platform contact rules (X invited-contact rule applied everywhere); open publishing and labeled multi-framing; invoked MEET roles and the representative-agent pilot; opted-in, pre-registered panels; the accuracy gate and directional-shift audit; `agent_provenance` and the agent-free re-fit gate; the aggregate-only inorganic-amplification overlay; seasonal re-verification of platform rules. *Depends on:* Q16–Q22, Q29; legal review of AI Act Art. 50 and the BOT Act. *Should precede* specs 14 and 16, which host the invoked roles. Agents may draft cross-cluster notes but never rate them (spec 11).
22. **Integration Game / State Machine Spec.** The 18-variable state vector and regime classifier with pre-registered phases (§10.3); the understanding matrix R and the ratified-representations layer; the objective J with hard constraints C1–C5 (§10.4); the reward-conferral principle, bridging-against detector and anti-scapegoat display rule (§10.2); the self-negating forecast and reflexivity dashboard (§10.5); ratified outcomes R1–R5 and Designs 1–3 with gates (§10.6); the randomized strategy tournament (§10.7); the resolution oracle, separation of powers and sealed panels (§10.8); the token stance and on-chain components (§10.9); the SEE → MEET → MOVE → DECIDE coupling to a first venue (§10.10). *Depends on:* Q23–Q30; specs 5, 17, 18 and 21; counsel on prizes and tokens. *Supersedes* the objective in spec 18 where they differ. **2026-10-30:** R is the gradient, measured chiefly by ratified notes (spec 11); windows follow the nested horizons (spec 12); add outcome R5 (lineage).
23. **Optional Enrichment: Consented Social Intake & Attention Overlay** (folds old specs 3 and 5). In-browser X archive parser and allow-list; dark-matter hashing; AT Protocol OAuth and Jetstream ingestion with delete propagation; the S0 follow/attention overlay (Leiden or SBM, node2vec/UMAP), labeled as attention, never belief; optional S2 stance-aware topic terrain; k-threshold and DP aggregate release. *Depends on:* specs 1, 8; Q36 (legal read on X's clause) before any X OAuth use. Lowest priority.

**Pre-spec actions, not specs:**
- Ask Kevin the §6.3 questions, including which accounts anchor each of his 58 ontologies (seed-list input).
- Record the 2026-10-11 outcome.
- Invite Lepp to co-design spec 14 and the hosted gap-filling events.
- Commission a rights read on transcript ingestion (copyright, fair use / TDM; the YouTube ToS gray area is a registered risk, R49, not a blocker) and a GDPR read on placing public figures (gates specs 3–4 at scale; Q34). Choose and price a YouTube transcript service.
- Legal review of the X clause, now lower priority (gates spec 23 only; Q36).
- Pick the first event map (Q31) and draft the seed niche list (Q32).
- ~~Complete research brief B9~~ Done (Q37). **Contact Jamie Joyce / the Society Library** (prior friendly DM thread) about a fidelity audit, extraction benchmark or seed maps, before spec 11 is final (Q38).
- Decide Q30 (naming Girard publicly vs the memo's mimetic-theory posture).
- Confirm with Jake Hartnell how his position is characterized (Q23; gates any publication of §10.5).
- Commission counsel on prize tournaments, bonds and tokens (gates specs 19 and 22).
- Recruit the research partner and IRB that Designs 2 and the agent panels share (Q21, Q28).

## 17. Annotated bibliography

Consolidated and de-duplicated from A1–A5 and B1–B9; sections J (B7) and K (B8) were added after the briefs, and section L (design-dialogue lineages and the transcript pipeline, from B9) on 2026-10-30. The same content is available as a standalone file, `BIBLIOGRAPHY.md`.

**Key.**
- **[P]** a primary source: an original paper, an official doc or terms, the primary text, code, or an author's own post.
- **[S]** secondary: a summary, news report, wiki or vendor summary.
- **[V]** internal: Benjamin's repos, his Parachute vault, or Gitcoin Brain.
- **UNVERIFIED**: carried forward from a brief.
- Brief codes in brackets show which brief cited the item.

Some fetches failed during research: GitHub repos, the SEP, docs.x.com pricing, the anti-debate.org pages and parts of docs.bsky.app. Where a brief relied on a summary instead, the entry says so.

### A. Benjamin Life's prior work and internal records [V]
- Ontography repo, main and `live-docs` branches: `/home/claude/auto-ontography-archive` (README, docs/PRD.md incl. NFR-3, docs/ARCHITECTURE.md, src/lib/*). The code is authoritative over the docs. [A1, B4, B5]
- Topology Live / antidebate-live: `/home/claude/omniharmonic/antidebate-live` (docs/ONTOLOGY.md v1.0, ARCHITECTURE.md, QUALITY.md, QA_AUDIT_2026-09-30.md, evals/results.md, docs/client/*, packages/core/src/formats.ts). The canonical schema source. [A1, A3]
- Dialectical Topology: `/home/claude/omniharmonic/dialecticaltopology` (pipeline/*.py, data/bundle/*, frontend/public/data/tree.json, META_ANALYSIS.md, docs/plans/*). The six lenses plus the silhouette test. [A2, B4]
- Dialectical.Claims: `/home/claude/omniharmonic/dialecticalclaims` (README, PRD §3.5, lib/dialectic-generator.ts, supabase-schema.sql, production logs). Thinkers modeled as methods; three synthesis slots. [A2]
- Essays in Parachute `wiki/writing/`:
  - *For Now We See Through a Glass, Darkly* (2026-03-03)
  - *Dialectical.Claims*
  - *Dialectics & Spontaneous Evolution*
  - *The Ancient Future at the End of History*
  - *Beyond Narrow Optimization*
  - *When Democracy Dies*
  - *Fork You*
  - *Out in the Bloodshed*
  - *When Integral Theory Faces Its Colonial Shadow*
  - *What Is Ethereum For*
  - *A Political Rise Manifesto* (2021)
  - *Leaderful Spaces*
  - *Protocols of Place*
  - *The Infrastructure of Belonging*
  - *Citizen*
  - *How and Why AI Will Accelerate Capitalism and Then Destroy It*
  - *Awakening the Earth Dharma II*
  - *Welcome to Omniharmonic*
  - *The Christ Meme*
  - *After the Black Pill*
  - *Transhumanism, Wetiko…*

  These are the source of the positions P1–P17 and the glossary in A4. [A2, A4]
- Parachute `wiki/concepts/*`: dialectics, memetic-evolution, pluralism, functional-pluralism, quadratic-voting/funding, integral-theory, metamodernism, basin-of-attraction, etc. [A4]
- Parachute meetings and records:
  - `2026-07-10_regen-hub-demo-ontography`: legibility failures, the overlap doubts, the twin-test idea.
  - `2026-04-09/high-dimensional-foraging`.
  - `united-independents/.../2026-06-02_deliberative-polling-tool`.
  - `united-independents/docs/Civic Tech Stack Research Draft`: Comhairle; not independently verified.
  - Polis Labs meeting notes, 2025-08-27 and 2026-04-17.

  [A1, A4, B2]
- Parachute research and tasks:
  - `thiel-karp-genealogy/synthesis/graph-topology-report`: bridges found by betweenness plus diversity of source traditions.
  - `final-constellation`.
  - Tasks `topology-live-antidebate-progress-conference` (status pending) and `simplify-ontography-visualization`.

  [A3, A4]
- Parachute messages:
  - `telegram/kevin-owocki`: 2026-07-04 Venn feedback; 2026-07-28 Atlas link.
  - `telegram/joe-lightfoot`.
  - `email/fwd-we-are-post-meta-now-72396552`.
  - `wiki/writing/the-liminal-web-ep_01`.

  [A1, A5]
- Gitcoin Brain [V]:
  - `meetings/2026-06-19_gitcoin-x-stephanie-research-interview`: Lepp's offer to run anti-debates.
  - `knowledge/gov-forum-learnings/qf-mechanics`: the GG22 $0-match case; CCN Climate.
  - `knowledge/gov-forum-learnings/sybil-identity`: includes Benjamin's GG21 retrospective.
  - `knowledge/gov-forum-learnings/measurement-impact`.
  - `knowledge/love-fund-survey-disbursement-plan`: costless QF subsidizes sybils.
  - `knowledge/local-qf-record-model`.
  - `telegram/gitcoin-viral-content/2026-05-25` and `2026-05-06`.
  - `meetings/2026-05-21_daniel-schmachtenberger-gitcoin` (not mined).

  [A3, A5, B3]
- Benjamin's Google Calendar: Anti-Debate sessions with Stephanie Lepp, 2022–2023. [A3]

### B. Anti-Debate and dialogue formats
- [P via repo summary] anti-debate.org: How-To Guide, Ground Rules, Discourse Matrix (https://www.anti-debate.org/how-to-guide.html; /ground-rules.html; /discourse-matrix.html). The format phases and rules, CC BY-SA 4.0. A direct fetch was blocked. [A3]
- [P via repo summary] Synthesis Media, "What is the Anti-Debate?" (Feb 2026): https://www.synthesismedia.org/p/what-is-the-anti-debate ; "Anti-Debate on AI Governance: Ball x Kokotajlo": https://www.synthesismedia.org/p/anti-debate-on-ai-governance-dean. [A3]
- [P] Heck & Lepp, TED (Aug 2025), "Why meeting in the middle isn't enough…": https://www.ted.com/talks/bill_heck_and_stephanie_lepp_why_meeting_in_the_middle_isn_t_enough_for_today_s_trickiest_debates. Higher ground, parallax, the three integration questions. [A3]
- [S] Partiful, "Anti-Debate on AI" (Lighthaven, 2026-03-09): https://partiful.com/e/Toy7N2AzrWOqNiBrYhqO. [A3]
- [S] Szeps, "A Better Way to Debate?" (preview only): https://uncomfortableconversations.substack.com/p/szeps-live-a-better-way-to-debate. [A3]
- [P] Roots of Progress, Progress Conference 2026 (no anti-debate session listed): https://rootsofprogress.org/conference/. [A3]
- [P] Anti-Debate YouTube playlist (not fetched): https://www.youtube.com/playlist?list=PLRN1pe0US2hS-mWZAiYJ8OMII8BcB6UXc. [A3]
- Outcome of the 2026-10-11 Topology Live event: **UNVERIFIED** (no record found). [A3]

### C. Memetic-tribes lineage and Kevin Owocki's Atlas
- [P] Limberg & Barnes, "The Memetic Tribes of Culture War 2.0" (Medium, 2018-09-14): https://medium.com/s/world-wide-wtf/memetic-tribes-and-culture-war-2-0-14705c43f6bb ; spreadsheet: https://docs.google.com/spreadsheets/d/11Ov1Y1xM-LCeYSSBYZ7yPXJah2ldgFX4oIlDtdd7-Qw/edit. 33 tribes × 9 columns, chosen qualitatively. [A5]
  - Name note: "Peter Lindenberger/Limberger" is Peter N. Limberg. A3's "Connor Barnes" is Conor Barnes. [A5]
- [S] Second Renaissance, "Memetic Tribes" and "Overview of mapping efforts": https://secondrenaissance.net/wiki/memetic-tribes ; https://secondrenaissance.net/wiki/overview-mapping-efforts. [A5]
- [S] EA Forum discussion: https://ea.greaterwrong.com/posts/pKgWQMjPki5bz7ehZ/memetic-tribes-and-culture-war-2-0-article-discussion. [A5]
- [P] Lightfoot, "The Liminal Web" (2021, updated 2023): https://stream.syscoi.com/2021/11/18/the-liminal-web-mapping-an-emergent-subculture-of-sensemakers-meta-theorists-systems-poets-joe-lightfoot. A scene, not a tribe; the ~30% consumption heuristic. [A5]
- [P] Dempsey, *Metamodern Meaning* ep. 17: https://brendangrahamdempsey.substack.com/p/17-the-liminal-web-and-communitas-c93. [A5]
- [P] Limberg, *Less Foolish*:
  - "How not to build a Stoa": https://lessfoolish.substack.com/p/how-not-to-build-a-stoa-a-very-online
  - "Memetic mediation during the liminal war": https://lessfoolish.substack.com/p/memetic-mediation-during-the-liminal
  - "Alt accounts, insight roles and memetic mediation": https://lessfoolish.substack.com/p/alt-accounts-insight-roles-and-memetic
  - The "Intimacy Crisis" essay is **UNVERIFIED**. Who coined "memetic mediator" is **UNVERIFIED**.

  [A5]
- [S] Beiner/Kainos interview with Limberg: https://beiner.substack.com/p/why-scene-making-beats-sensemaking. [A5]
- [S] P2P Foundation: Snyder, "Rise of the Memetic Mediators": https://wiki.p2pfoundation.net/Jason_Snyder_on_the_Rise_of_the_Memetic_Mediators ; Nørgaard, "Memetic Tribes of the Meta-Crisis": https://wiki.p2pfoundation.net/Brandon_N%C3%B8rgaard_on_the_Memetic_Tribes_of_the_Meta-Crisis. [A5]
- [P] OILab, "Political Space": https://oilab.eu/political-space. Tribes placed manually on 3 axes. [A5]
- [P] Schmachtenberger, "The War on Sensemaking": https://civilizationemerging.com/media/war-on-sensemaking-5/. [A5]
- [P] More in Common, *Hidden Tribes of America* (2018): https://hiddentribes.us/. Clustering on deep drivers; the "Exhausted Majority". [A5]
- [P] Pew, Political Typology 2021: https://www.pewresearch.org/politics/2021/11/09/beyond-red-vs-blue-the-political-typology-2021/ ; methodology appendix B. The names of the 9 groups are **UNVERIFIED**. [A5]
- [P] Owocki, "Atlas of Frontier Ontologies": https://daily-ontological-map.vercel.app/. 58 X ontologies, nightly, two axes. Method undisclosed. [A5 addendum]

### D. Philosophical and theoretical lineages
- [P, SEP pointers not re-fetched] SEP entries "Hegel's Dialectics", "Cultural Evolution", "Jürgen Habermas", "Martin Buber" and "Dewey's Political Philosophy" (plato.stanford.edu). [B1]
- [P] Mueller, "The Hegel Legend of 'Thesis-Antithesis-Synthesis'", *JHI* (1958). Bibliographic detail from memory. [B1]
- [P] Kojève's Hegel lectures (1930s); Fukuyama, "The End of History?" (1989): https://www.democraziapura.it/wp-content/uploads/2015/01/1989-Fukuyama.pdf. [B1, A4]
- [P] Mill, *On Liberty* (1859), ch. 2. The "marketplace of ideas" phrase dates to Holmes's dissent in *Abrams v. United States*; its first exact use is **UNVERIFIED**. [B1]
- Wu, "Is the First Amendment Obsolete?" (2017): **UNVERIFIED**. [B1]
- [P] Buber, *I and Thou* (1923); Bohm, *On Dialogue* (1996). [S] Are.na Bohm overview: https://www.are.na/editorial/bohm-dialogue. [B1]
- [P] Habermas, *Structural Transformation of the Public Sphere* (1962); *Theory of Communicative Action* (1981). [S] "Ideal speech situation": https://www.wikiwand.com/en/articles/Ideal_speech_situation. Habermas 2022, *A New Structural Transformation*: **UNVERIFIED**. [B1]
- [P] Fraser, "Rethinking the Public Sphere," *Social Text* 25/26 (1990). Counterpublics. [B1]
- [P] Mouffe, "Deliberative Democracy or Agonistic Pluralism?" (1999/2000): https://irihs.ihs.ac.at/id/eprint/1312/. [B1]
- [P] Gutmann & Thompson, *Democracy and Disagreement* (1996); Dryzek, *Discursive Democracy* (1990); Dryzek & Niemeyer, *Foundations and Frontiers of Deliberative Governance* (2010): https://academic.oup.com/book/11756. Meta-consensus. [B1]
- [P] Landemore, *Democratic Reason* (2013) and *Open Democracy* (2020): https://press.princeton.edu/node/59247. [B1]
- [P] Dewey, *The Public and Its Problems* (1927). [B1]
- [P] Boyd & Richerson (1985, 2005); Henrich, *The Secret of Our Success* (2016); Dawkins (1976); Blackmore (1999). [B1]
- [P] Sperber, *Explaining Culture* (1996): https://www.dan.sperber.fr/?p=29. Cultural attraction. [B1]
- [P] Aunger (ed.), *Darwinizing Culture* (2000): https://dc2.philarchive.org/rec/AUNDCT. [B1]
- [P] Ashby (1956); Bateson, *Naven* (1936) and *Steps to an Ecology of Mind* (1972). [P] Heylighen & Joslyn: https://CliffJoslyn.github.io/Docs/HeFJoC03.pdf. [B1]
- [P] Woolley et al., *Science* 330 (2010): https://pubmed.ncbi.nlm.nih.gov/20929725/. The *c* factor; replications are mixed (**UNVERIFIED** detail). [B1]
- [P] Page, *The Difference* (2007). [P] Hong & Page, *PNAS* 101(46) (2004): https://pmc.ncbi.nlm.nih.gov/articles/PMC528939/. [P] Romaniega, arXiv 2307.04709 (critique; also the source for Thompson, *Notices AMS* 2014): https://arxiv.org/pdf/2307.04709. [B1]
- [P] Freinacht, *The Listening Society* (2017): https://wiki.p2pfoundation.net/Listening_Society. Wilber; Beck & Cowan. Visser critique (not read): https://www.integralworld.net/visser236.html. [B1]
- [P] Girard (1961, 1972, 1978). [S] https://en.wikipedia.org/wiki/Mimetic_theory ; https://criticallegalthinking.com/2023/09/04/mimetic-desire-the-scapegoat-notes-on-the-thought-of-rene-girard/. [B1]
- Popper, *The Poverty of Historicism*: **UNVERIFIED** citation detail. [B1]
- [P] Koltko-Rivera, "The Psychology of Worldviews" (2004): https://lup.lub.lu.se/search/files/5733804/3738786.pdf. 42 dimensions in 7 groups. [B4]

### E. Computational democracy and deliberation technology
- [P] Small et al., "Polis: Scaling Deliberation…" (2021): https://www.e-revistes.uji.es/index.php/recerca/article/view/5516. [P] CompDem open source (AGPL-3.0): https://compdemocracy.org/open-source. [P] Group-informed consensus: https://compdemocracy.org/group-informed-consensus. [B2, B3]
- [S] Polis 2.0 reporting: https://news.hada.io/topic?id=26667 ; https://news.lavx.hu/article/polis-2-0-the-open-source-platform-scaling-deliberative-democracy-to-millions ; https://www.gigazine.net/gsc_news/en/20260216-polis/. Scale claims **UNVERIFIED**. [B2, B5]
- [P] Nishio, notes on Polis lumping and on kouchou-ai: https://scrapbox.io/nishio-en/Phenomenon_that_Polis_with_the_most_votes_are_lumped_together. ; https://scrapbox.io/nishio-en/public_information_AI. [B2]
- [S] Daily Beast on vTaiwan: https://www.thedailybeast.com/taiwan-tried-to-digitize-democracy-with-vtaiwan-it-was-a-huge-flop ; Noveck rejoinder: https://thelivinglib.org/?p=57365. [B2]
- [P] AI Objectives Institute, Talk to the City (archived): https://gwern.net/doc/www/ai.objectives.institute/fa46182a810da5bfde418b21016574027d1dd94f.html. Pipeline specifics **UNVERIFIED**. [S] IE CGC case studies: https://ie.edu/cgc/news-and-events/news/using-ai-to-inform-policymaking-what-we-can-learn-from-3-use-cases-of-talk-to-the-city. [B2]
- [S] Team Mirai: https://en.wikipedia.org/wiki/Team_Mirai. [B2]
- [P] Konya et al. (2023), arXiv 2311.02242: https://ar5iv.labs.arxiv.org/html/2311.02242 ; Konya et al. (2025), arXiv 2503.01769: https://arxiv.org/pdf/2503.01769. Remesh and max-min agreement. [B2]
- [P] CIP Global Dialogues: https://www.cip.org/global-dialogues. [B2]
- [P] Stanford Online Deliberation Platform: https://deliberation.stanford.edu/tools-resources/online-deliberation-platform ; Fishkin et al., APSR (2021); Meta Community Forum: https://fsi.stanford.edu/node/36099. [B2]
- [P] Goyal et al., "Beyond Polarization: Opinion Mixing…" arXiv 2601.14221. Deliberation reorders opinions. [B2]
- [P] Tessler, Bakker et al., *Science* (2024), Habermas Machine: https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf ; Tessler et al., arXiv 2601.05904. No public code found (**UNVERIFIED**). [S] Sætra, CACM: https://cacm.acm.org/blogcacm/computation-and-deliberation-the-ghost-in-the-habermas-machine. [B2, B3]
- [P] Wojcik et al., "Birdwatch", arXiv 2210.15723: https://arxiv.org/abs/2210.15723. The MF bridging model. [B2, B3, B4]
- [S] DeepWiki, Community Notes group scoring: https://deepwiki.com/twitter/communitynotes/2.2-group-based-scoring. The repo licence (Apache-2.0) is **UNVERIFIED**. [B2]
- [P] Andreou & Sirivianos, "Two Fault Lines," arXiv 2609.21496: https://arxiv.org/abs/2609.21496. Second axis (institutional trust). Existence re-confirmed for this synthesis. [B2, B4]
- [P] Razuvayevskaya et al., arXiv 2510.12559; Arjmandi-Lari, Mantzarlis & Stafford, arXiv 2510.00650; Li & Bakker, arXiv 2604.02592 (LLM note writers); Lloyd et al., arXiv 2509.15434. [B2]
- [P] Selvam, Baxter et al., "Gaming Consensus," arXiv 2607.01824. Read via the summary at https://tldr.takara.ai/p/2607.01824. [B5]
- [P] Ovadya & Thorburn, "Bridging Systems," arXiv 2301.09976. [P] Milli, Thorburn et al., NeurIPS 2024 Pluralistic Alignment Workshop poster (bridging censors controversial topics): https://neurips.cc/virtual/2024/99058. [P] Stray et al., Prosocial Ranking Challenge, arXiv 2603.19626. [B2, B3]
- [P] Jigsaw et al., "AI and the Future of Digital Public Squares," arXiv 2412.09988 ; Google.org Sensemaking AI: https://blog.google/company-news/outreach-and-initiatives/google-org/sensemaking-ai/. `Jigsaw-Code/sensemaking-tools` licence **UNVERIFIED**. [B2]
- [P] Weyl, Tang et al., *Plurality* (CC0): https://plurality.net/. Plurality Institute outputs **UNVERIFIED**. [B2]
- [P] Anthropic & CIP, Collective Constitutional AI: https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input. [B2]
- [P] Fish, Gölz, Parkes, Procaccia et al., "Generative Social Choice," arXiv 2309.01291. [B2, B3]
- [S] Kialo: https://en.wikipedia.org/wiki/Kialo ; Harmonica: https://metagov.org/delib-tools/harmonica ; Frankly: https://cyber.harvard.edu/story/2025-04/asml-invites-open-source-collaborators-to-frankly ; Loomio: https://en.wikipedia.org/wiki/Loomio ; [P] Decidim Barcelona: https://decidim.org/case-studies/barcelona-budgeting/. [B2]
- Bluesky/Blacksky `assembly.blacksky.community` deliberation work: **UNVERIFIED**. Taiwan's Join platform: **UNVERIFIED**. [B2]

### F. Mechanism design
- [P] Lalley & Weyl, AEA P&P 108 (2018): https://www.aeaweb.org/doi/10.1257/pandp.20181002. [B3]
- [P] Buterin, Hitzig & Weyl, *Management Science* 65(11) (2019): https://arxiv.org/abs/1809.06421. [B3]
- [P] Buterin, "Pairwise coordination subsidies" (2019): https://ethresear.ch/t/pairwise-coordination-subsidies-a-new-quadratic-funding-design/5553. Full text not fetched. [B3]
- [P] Weyl, Ohlhaver & Buterin, "Decentralized Society" (2022): https://papers.ssrn.com/abstract=4105763. [B3]
- [P] Miller, Weyl & Erichsen, "Beyond Collusion Resistance": https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4311507 (full paper not fetched) ; RadicalxChange blog. Code at github.com/Jmiller4/plural-qf (not fetched). [B3]
- [P] Miller, Weyl & Kanich, "Fair Decisions through Plurality," EAAMO '25, arXiv 2509.18343. The CO-QF formula; 32 of 38 rounds. [B3]
- [P] Gitcoin: Deep Funding: https://gitcoin.co/mechanisms/deep-funding ; Pairwise: https://gitcoin.co/mechanisms/pairwise ; cluster-matching ops: https://roundoperations.gitcoin.co/round-operations/post-round/cluster-matching-and-csv-upload ; COCM nerd post: https://gov.gitcoin.co/t/nerd-post-updates-to-cluster-mapping-matching/18705. [S] Kronosapiens jury analysis: https://kronosapiens.github.io/blog/2025/08/03/deepfunding-jury-analysis. [B3]
- [P] Optimism, "Lessons learned from two years of RetroPGF": https://gov.optimism.io/t/lessons-learned-from-two-years-of-retroactive-public-goods-funding/9239. [B3]
- [S] BlockScience, "A Brief History of Conviction Voting" (not read in full). [B3]
- [P] Miller, Resnick & Zeckhauser, peer prediction (2005); Prelec, BTS, *Science* 306 (2004); Prelec, Seung & McCoy, *Nature* (2017); Hanson, futarchy: https://mason.gmu.edu/~rhanson/futarchy.html. BTS validity across clusters with different priors is **UNVERIFIED**. [B3]
- [P] Manheim & Garrabrant, Goodhart variants, arXiv 1803.04585. [B3]
- [P] Borge et al., Proof-of-Personhood (2017): https://bford.info/pub/dec/pop-abs/ ; Yu et al., SybilGuard (2006). [P] Human Passport: https://human.tech/blog/defending-gitcoin-grants. [B3]
- Frey & Oberholzer-Gee, AER (1997), crowding-out: not re-verified. Campaign-finance exposure of cross-cluster matching: **UNVERIFIED**. [B3]

### G. Mapping science
- [P] Conover et al., ICWSM 2011: https://ojs.aaai.org/index.php/icwsm/article/view/14126. Partly **UNVERIFIED** (bot wall). [A5, B4]
- [P] Barberá, "Birds of the Same Feather," *Political Analysis* (2015); code https://github.com/pablobarbera/twitter_ideology. [P] Barberá et al., *Psych. Science* (2015). [A5, B4]
- [P] Cinelli et al., *PNAS* 118(9) (2021): https://pubmed.ncbi.nlm.nih.gov/33622786/. Method detail to re-verify. [B4]
- [P] Garimella et al., "Quantifying Controversy": https://arxiv.org/abs/1507.05224 ; Garimella, Weber & De Choudhury, quote-RTs: https://www.arxiv.org/abs/1603.07933. [B4]
- [P] Waller & Anderson, arXiv 2010.00590; https://github.com/CSSLab/social-dimensions. [B4]
- [P] Wu, Nagler, Tucker & Messing, arXiv 2303.12057. LLM pairwise comparisons plus Bradley–Terry. [B4]
- [P] Satuluri et al., SimClusters, KDD 2020. Specifics **UNVERIFIED**. [B4]
- [P] Traag, Waltman & van Eck, Leiden, arXiv 1810.08473 ; Peixoto, SBM, arXiv 1705.10225 ; Traag & Bruggeman, arXiv 0811.2329 ; signed-bipartite sensitivity, arXiv 2405.08203 ; Grover & Leskovec, node2vec, arXiv 1607.00653 ; Burt (2004) ; Mucha et al., arXiv 0911.1824 ; Kivelä et al. (2014). [B4]
- [P] Ghafouri et al., stance-aware sentence transformers, EMNLP 2024: https://aclanthology.org/2024.emnlp-main.1171.pdf. [B4]
- [P] Grootendorst, BERTopic, arXiv 2203.05794. The HDBSCAN noise share on tweets is **UNVERIFIED**. [B4]
- [P] Stance surveys, arXiv 2409.15690 and 2409.13594 ; Törnberg, arXiv 2304.06588. PMC12629487 not read (**UNVERIFIED**). [B4]
- [P] Metropolitansky & Larson, Claimify, arXiv 2502.10855. [B4]
- [P] Preniqi et al., MoralBERT, arXiv 2403.07678 ; Hopp et al., eMFD (2021) ; Kiesel et al., SemEval-2023 ValueEval. MFQ-2 attribution to Atari et al. 2023 is **UNVERIFIED**. [B4]
- [S/P] Jev (TypeSafe AI, launched 2026-09-15):
  - The Batch: https://www.deeplearning.ai/the-batch/models-built-to-do-one-thing-well
  - The New Stack: https://thenewstack.io/typesafe-jev-system-one/
  - LiteLLM benchmark: https://docs.litellm.ai/blog/jev-auto-router-benchmark
  - NanoGPT docs: https://docs.nano-gpt.com/api-reference/endpoint/jev-decisions.md
  - Low-confidence JevBench/imitators: https://www.modemguides.com/blogs/ai-news/jev-typesafe-reality-check-run-locally
  - Re-confirmed for this synthesis by search: https://www.datacamp.com/blog/system-one-models-jev ; https://letsdatascience.com/news/typesafe-ai-launches-jev-decision-model-889a38c0
  - Accuracy claims are vendor-internal. Availability is **UNVERIFIED** (checked 2026-10-30). Secondary sources conflict: the waitlist was removed 2026-09-21 (explainx.ai), signups were paused 2026-09-22 (B4), and the direct API is still waitlisted with gateway routes open (opentweet.io).

  [B4]
- [P] GLiClass, arXiv 2508.07662 ; SetFit, arXiv 2209.11055 ; [S] gzip+kNN critique: https://liorsinai.github.io/machine-learning/2023/08/13/gzip-knn.html. [B4]
- [P] Pew (2019), Twitter users' 10%/80% skew. [P] Rauchfleisch & Kaiser (2020), bot-detection errors; re-verify the specifics. [B4]
- [S] Bail et al., *PNAS* (2018), backfire from exposure to opposing views, via NiemanLab: https://www.niemanlab.org/2018/08/republicans-who-follow-liberal-twitter-bots-actually-become-more-conservative/. The primary is **UNVERIFIED** per B1. [B1, B4]
- [P] Community Archive: https://github.com/TheExGenesis/community-archive. Inclusion of follow data is **UNVERIFIED**. [P] Bluesky dataset paper, arXiv 2408.03146. [B4]
- [P/S] Visualization: Apple Embedding Atlas, arXiv 2505.06386 ; DataMapPlot: https://datamapplot.readthedocs.io ; Cosmograph (vendor): https://cosmograph.app/docs-lib/comparison/ ; Nomic: https://home.nomic.ai/blog/posts/data-mapping. [B4]

### H. Platforms, data law and weaponization
- [P] X Developer changelog (pay-per-use 2026-02-06; Owned Reads 2026-04-16; search changes 2026-05-04): https://docs.x.com/updates/changelog. [P] X restricted use cases (political-inference clause): https://docs.x.com/developer-terms/restricted-use-cases. [P] X OAuth 2.0 PKCE: https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code. [B5]
- [S] Upload-Post X API pricing (2026-09-28): https://www.upload-post.com/x-api-pricing/ ; OpenTweet summary: https://opentweet.io/x-api-pricing. Per-resource prices and the scope of Owned Reads are **UNVERIFIED** against docs.x.com. [B4, B5]
- [P] X Help, archive download: https://help.x.com/articles/20170320 ; Princeton Community Notes archive protocol: https://communitynotes.cs.princeton.edu/data_collection_details_prol.pdf. [B5]
- [S] Knight Institute on X ToS liquidated damages: https://knightcolumbia.org/content/knight-institute-says-xs-new-terms-of-service-will-stifle-independent-research. [B5]
- [P] Jetstream (Jaz, 2024): https://jazco.dev/2024/09/24/jetstream/ ; [S] https://apis.io/apis/bluesky/bluesky-jetstream/ ; [P] Bluesky moderation docs: https://www.docs.bsky.app/docs/advanced-guides/moderation ; AT Protocol 2026 Spring Roadmap: https://atproto.com/blog/2026-spring-roadmap ; rate-limit discussion: https://github.com/bluesky-social/atproto/discussions/697 (current figure **UNVERIFIED**) ; [S] Gigazine on Bluesky MAU: https://gigazine.net/gsc_news/en/20260812-blueskys-active-user/. [B5]
- [P] Neynar pricing: https://neynar.com/developer ; [S] Pulse on Neynar's acquisition of Farcaster. [P] Lisker & Mihaljević, "Data Ethics in the Fediverse," arXiv 2505.07606. [B5]
- [S] DLA Piper on CJEU C-252/21: https://privacymatters.dlapiper.com/2023/07/eu-cjeus-landmark-decision-in-meta-vs-bundeskartellamt/ ; Columbia GFoE on C-446/21: https://globalfreedomofexpression.columbia.edu/cases/maximilian-schrems-v-meta-platforms-ireland-limited-schrems-iii/. [B5]
- [P] EU TTPA, Reg. 2024/900: https://eur-lex.europa.eu/eli/reg/2024/900/oj ; [P] EC FAQ on DSA researcher data access: https://algorithmic-transparency.ec.europa.eu/news/faqs-dsa-data-access-researchers-2025-07-03_en. Eligibility is **UNVERIFIED**. [B5]
- [S] Bastion on CCPA sensitive personal information ; NatLawReview on Colorado sensitive data (detail **UNVERIFIED**). [B5]
- [S] ZwillGen on hiQ v. LinkedIn ; NatLawReview and Goldman blog on X v. Bright Data (final outcome **UNVERIFIED**) ; scraping legal wiki (Meta v. Bright Data; 2025–26 DMCA §1201 cases). [B5]
- [P] FTC opinion on Cambridge Analytica (2019): https://www.ftc.gov/system/files/documents/cases/d09389_comm_final_opinionpublic.pdf ; [P] Kosinski, Stillwell & Graepel, *PNAS* (2013) ; [P] Narayanan & Shmatikov (2009), arXiv 0903.3276 ; [P] Graphika: https://graphika.com/how-it-works. [B5]

### I. AI agents, influence operations and agent ethics
Added with B6. Tessler et al. (Habermas Machine), Li & Bakker (AI note writers), the Prosocial Ranking Challenge, the Bluesky moderation docs and Rauchfleisch & Kaiser are listed above (E, G, H) and are also cited by [B6].

**Adversarial operations**
- [P] OpenAI, "Disrupting deceptive uses of AI by covert influence operations" (May 2024): https://openai.com/index/disrupting-deceptive-uses-of-AI-by-covert-influence-operations/ ; "Disrupting malicious uses of AI" (June 2025): https://openai.com/global-affairs/disrupting-malicious-uses-of-ai-june-2025. Breakout Category ratings. [B6]
- [S] OpenAI on Storm-2035 (Aug 2024), via Security Affairs: https://securityaffairs.com/167194/intelligence/openai-dismantled-iranian-influence-operation.html ; OpenAI June 2026 PRC-linked operation, via PC Gamer: https://pcgamer.com/software/ai/openai-says-it-busted-a-shadowy-chinese-operation-that-used-chatgpt-to-whip-up-data-centre-hate-and-that-achieved-basically-nothing/. [B6]
- [P] Anthropic, "Detecting and countering malicious uses of Claude" (2025): https://www.anthropic.com/news/detecting-and-countering-malicious-uses-of-claude-march-2025. Influence-as-a-service. [B6]
- [P] Meta, Adversarial Threat Report Q3 2022: https://about.fb.com/news/2022/11/metas-adversarial-threat-report-q3-2022/ ; [S] Meta Spamouflage takedown (Aug 2023), via The Record: https://therecord.media/spamouflage-china-accused-largest-covert-influence-operation-meta. [B6]
- [S] STOIC: Times of Israel on the NYT Diaspora Ministry report: https://www.timesofisrael.com/diaspora-ministry-funded-fake-social-media-posts-to-spread-pro-israel-content-nyt/ ; NBC News (headline only): https://www.nbcnews.com/tech/security/meta-openai-say-disrupted-israeli-companys-influence-campaign-rcna154774. State funding reported, ministry denied. [B6]
- [S] Reuters Pentagon anti-Sinovac investigation, via Al Jazeera (June 2024): https://www.aljazeera.com/news/2024/6/14/pentagon-ran-secret-anti-vax-campaign-to-undermine-china-during-pandemic. [B6]
- [P] SIO & Graphika, *Unheard Voice* (2022): https://fsi.stanford.edu/node/22009 ; https://purl.stanford.edu/nj914nx9540. [S] The Intercept on CENTCOM accounts (Dec 2022): https://theintercept.com/2022/12/20/twitter-dod-us-military-accounts/. [B6]
- [P] Graphika, *The Americans* (Sept 2024): https://public-assets.graphika.com/reports/graphika-report-the-americans.pdf. [B6]
- [P] DOJ, Doppelganger domain seizure (Sept 2024): https://www.justice.gov/usao-edpa/pr/justice-department-disrupts-covert-russian-government-sponsored-foreign-malign ; [S] CyberScoop on Meliorator (July 2024): https://cyberscoop.com/us-international-authorities-seize-russian-ai-bot-farm/. [B6]
- [P] Microsoft MTAC (April 2024): https://blogs.microsoft.com/on-the-issues/2024/04/17/russia-us-election-interference-deepfakes-ai/ ; DFRLab 2025 year in review (Pravda network): https://dfrlab.org/2025/12/31/the-dfrlab-reflects-on-2025/. [B6]
- [P] Eady et al., *Nature Communications* (9 Jan 2023), Russian 2016 Twitter campaign; [S] TCD summary: https://www.tcd.ie/news_events/articles/voting-behaviour-in-2016-us-presidential-election-not-affected-by-foreign-disinformation-campaigns-on-twitter/. Re-confirmed for this synthesis. [B6]
- [P] Nimmo, The Breakout Scale (Brookings 2020): https://www.brookings.edu/articles/the-breakout-scale-measuring-the-impact-of-influence-operations/ ; Yang, "Towards a New Toolkit for Measuring AI-Enabled Influence Operations" (ICML 2026 workshop): https://icml.cc/virtual/2026/74732. [B6]

**AI persuasion**
- [P] Salvi, Horta Ribeiro, Gallotti & West, *Nature Human Behaviour* (2025), PDF mirror: https://www.rivista.ai/wp-content/uploads/2025/05/s41562-025-02194-6.pdf. [B6]
- [P] Costello, Pennycook & Rand, "Durably reducing conspiracy beliefs through dialogues with AI," *Science* (Sept 2024); [S] Cornell Chronicle: https://news.cornell.edu/node/329310. Re-confirmed for this synthesis. [S] Boissin, Costello et al., *PNAS Nexus* (2025), via PsyPost: https://www.psypost.org/ai-conversations-can-reduce-belief-in-conspiracies-whether-or-not-the-ai-is-recognized-as-ai. [B6]
- [S] Hackenburg & Margetts, *PNAS* (2024), via OII: https://www.oii.ox.ac.uk/does-political-microtargeting-with-large-language-models-offer-persuasive-returns-ask-kobi-hackenburg-and-professor-helen-margetts/. [B6]
- [P] Hackenburg et al., "Levers of political persuasion," *Science* (2025); arXiv: https://arxiv.org/html/2507.13919v1 ; [S] OII: https://www.oii.ox.ac.uk/oxford-researchers-reveal-how-conversational-ai-can-change-political-opinions/. [B6]
- [S] Zurich r/changemyview case: The Decoder: https://the-decoder.com/researchers-used-ai-to-manipulate-reddit-users-scrapped-study-after-backlash/ ; NBC News: https://www.nbcnews.com/news/rcna203597 ; Live Science: https://www.livescience.com/technology/artificial-intelligence/ai-researchers-ran-a-secret-experiment-on-reddit-users-to-see-if-they-could-change-their-minds-and-the-results-are-creepy ; 404 Media (headline): https://404media.co/reddit-issuing-formal-legal-demands-against-researchers-who-conducted-secret-ai-experiment-on-users. Re-confirmed for this synthesis. The claim that prompts told the model users had consented is **UNVERIFIED**. [B6]

**Prosocial precedents**
- [S] Munger, "Tweetment Effects," *Political Behavior* (2017), via CSMaP: https://csmapnyu.org/research/academic-research/tweetment-effects-on-the-tweeted-experimentally-reducing-racist-harassment. Account construction and consent details **UNVERIFIED**. [B6]
- [S] Bail et al., *PNAS* (2018), via Phys.org: https://phys.org/news/2018-09-caught-political-echo-chamber-opposition.pdf. [B6]
- [P] Combs, Bail et al., DiscussIt, *Nature Human Behaviour* (2023): https://www.nature.com/articles/s41562-023-01655-0. Effect sizes not re-fetched (**UNVERIFIED**). [B6]
- [P] Argyle, Bail, Busby et al., *PNAS* (2023): https://arxiv.org/pdf/2302.07268. [B6]
- [S] X AI Note Writer launch (July 2025), via BetaNews: https://betanews.com/2025/07/02/x-launches-ai-bot-pilot-to-write-community-notes-fact-checkers/ ; Twitter "Automated by" label, via TechCrunch: https://techcrunch.com/2022/02/16/twitter-officially-launches-labels-to-identify-the-good-bots. [B6]

**Rules, law and ethics**
- [P] X automation rules: https://help.x.com/en/rules-and-policies/x-automation ; X authenticity policy: https://help.x.com/en/rules-and-policies/authenticity ; Meta inauthentic behavior policy (did not render; wording **UNVERIFIED**): https://transparency.meta.com/policies/community-standards/inauthentic-behavior ; Bluesky community guidelines: https://bsky.social/about/support/community-guidelines. Whether any Bluesky labeler offers a "bot" label is **UNVERIFIED**. [B6]
- [P] European Commission, AI Act Article 50 FAQ: https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act ; [S] DSA Article 34: https://www.springlex.eu/en/packages/dsa/dsa-regulation/article-34/. [B6]
- [P] California B&P §17941 (BOT Act): https://california.public.law/codes/business_and_professions_code_section_17941. Platform threshold (§17940) **UNVERIFIED**. [P] AB 410 (2025) status: https://legiscan.com/CA/text/AB410/2025. [B6]
- [S] FTC fake-reviews rule (16 CFR Part 465), via Hunton: https://hunton.com/hunton-retail-law-resource/ftc-issues-final-rule-targeting-fake-consumer-reviews-and-testimonials-including-those-generated-by-artificial-intelligence-ai-and-online-bots. Wider FTC AI-impersonation rulemaking **UNVERIFIED**. [B6]
- [P] 45 CFR 46.116 (fetch blocked; re-verify): https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.116 ; Menlo Report (DHS 2012): https://www.caida.org/publications/papers/2012/menlo_report/menlo_report.pdf ; APA Ethics Code 8.07 (not re-fetched). [B6]
- [P] Susser, Roessler & Nissenbaum, "Online Manipulation: Hidden Influences in a Digital World": https://philarchive.org/archive/SUSOMHv1. [B6]

### J. Girard, hyperstition, reflexivity and the mimetic state machine
Added with B7. Items already listed above and also cited by [B7]: Girard (D), Dryzek & Niemeyer and Landemore (D), Manheim & Garrabrant (F), vTaiwan (E), Bail et al. (G).

**Girard and Girardians**
- [S] Andrade, "René Girard (1923–2015)," *Internet Encyclopedia of Philosophy*: https://iep.utm.edu/girard/. Arc of mimetic theory; criticisms. [B7]
- [P] Girard, *Battling to the End: Conversations with Benoît Chantre* (MSU Press, 2009; *Achever Clausewitz*, 2007), publisher page: https://msupress.org/9780870138775/battling-to-the-end/ ; [S] Haven, NBCC review (2010): https://www.bookcritics.org/2010/01/12/nbcc-featured-review-cynthia-l-haven-on-rene-girard/ ; [S] Frieze review: https://frieze.com/article/battling-end-conversations-beno%C3%AEt-chantre. Escalation to extremes. [B7]
- [S] Megoran, review of *I See Satan Fall Like Lightning* (2003): https://www.staff.ncl.ac.uk/nick.megoran/iFrame/iSatanFall.html ; Girard's "other totalitarianism" passage as quoted in *The American Conservative*: https://www.theamericanconservative.com/rene-girard-covington-catholic-boys/. [B7]
- [P] Shullenberger, "The Scapegoating Machine," *The New Inquiry* (30 Nov 2016): https://thenewinquiry.com/the-scapegoating-machine ; Thiel–Girard essay, *Cyborgology* (9 Aug 2016): https://thesocietypages.org/cyborgology/?p=21451. [B7]
- [P] Thiel, "The Straussian Moment," in Hamerton-Kelly (ed.), *Politics and Apocalypse* (MSU Press, 2007; from a 2004 symposium): https://muse.jhu.edu/books/9781609170417 ; https://archive.org/details/the-straussian-moment. Date per secondary sources and catalog record. [B7]
- [S] Dupuy, *The Mark of the Sacred* (Stanford UP, 2013), description: https://ingramacademic.com/products/the-mark-of-the-sacred-9780804776899 ; Childs, review of Dupuy, *How to Think About Catastrophe* (2023): https://journals.ub.uni-giessen.de/kult-online/article/download/1510/1719/4164?inline=1 ; Dupuy, *Economy and the Future* (2014): https://mitpressbookstore.mit.edu/book/9781611861464. Dupuy's fixed-point formalism is **UNVERIFIED**. [B7]
- [S] Dumouchel, *The Ambivalence of Scarcity and Other Essays* (MSU Press, 2014): https://msupress.org/9781628960006/the-ambivalence-of-scarcity-and-other-essays. [B7]
- [S] Burgis, *Wanting* (2021), summary: https://www.artofmanliness.com/character/self-improvement/thick-desires-anti-mimetic-life/. Framing, not evidence. [B7]
- [V] Parachute `vault/research/thiel-karp-genealogy/texts/girard-apocalyptic-turn`. [B7]

**Hyperstition, performativity, reflexivity**
- [P] Carstens, "Hyperstition: An Introduction" (interview with Nick Land, 2009): https://www.orphandriftarchive.com/articles/hyperstition-an-introduction/ ; [S] Nick Land: https://en.wikipedia.org/wiki/Nick_Land. [B7]
- [V] Parachute `wiki/concepts/hyperstition`. [B7]
- [P] GreenPill S10E8, "Hyperstitions: How Beliefs Become Reality in Networked Systems, with Jake Hartnell" (30 Dec 2025): https://sites.libsyn.com/400481/s10-ep8-hyperstitions-how-beliefs-become-reality-in-networked-systems-with-jake-hartnell ; Owocki, "Hyperstitions: how shared beliefs shape onchain realities" (Gitcoin, 5 Mar 2026): https://gitcoin.co/research/hyperstitions-how-shared-beliefs-shape-onchain-realities ; [S] Hartnell profile: https://cryptoslate.com/people/jake-hartnell/ ; https://www.ischool.berkeley.edu/events/2022/dao-first-world. [B7]
- [V] Parachute: `vault/messages/telegram/jake-hartnell` (2025-10-24); `vault/meetings/2025-12/2025-12-01_collaboration-monster-immersion-jam` (Hyperstition Markets → Incentives Markets); `vault/people/jake-hartnell`; `vault/projects/local-alternatives/reports/2026-09-04_sensor-networks-prediction-markets-dialogue-report` (prediction markets as hyperstition; pro-social gameability). The speaker identity of "Michael" and the Paris-thermometer anecdote are **UNVERIFIED**. Hartnell's preferred characterization is to be confirmed (Q23). [B7, B8]
- [P] Yu et al., "Memes, Markets, and Machines… through Hyperstition," arXiv 2410.23794: https://arxiv.org/pdf/2410.23794. [B7]
- [P] Biggs, "Self-Fulfilling Prophecies," *Oxford Handbook of Analytical Sociology* (2009), incl. Merton 1948: https://users.ox.ac.uk/~sfos0060/prophecies.shtml. [B7]
- [P] Soros, "Fallibility, Reflexivity, and the Human Uncertainty Principle," *J. Economic Methodology* (2014): https://www.georgesoros.com/2014/01/13/fallibility-reflexivity-and-the-human-uncertainty-principle-2/. [B7]
- [P] MacKenzie, *An Engine, Not a Camera* (MIT Press, 2006); [S] discussion: https://organizationsandmarkets.com/2006/11/14/pomo-periscope-vi-performativity/. The typology is **UNVERIFIED** here. Callon, *The Laws of the Markets* (1998): **UNVERIFIED** (not fetched). [B7]
- [P] Perdomo, Zrnic, Mendler-Dünner & Hardt, "Performative Prediction," ICML 2020: https://proceedings.mlr.press/v119/perdomo20a.html. [B7, B8]
- [S] Campbell's law (1979): https://en.wikipedia.org/wiki/Campbell%27s_law. [B7]
- [P] Deci, Koestner & Ryan, *Psychological Bulletin* (1999), meta-analysis: https://depts.washington.edu/techdocs/papers/deciExtrinsicRewardsAndIntrinsicMotivation99.pdf ; Gneezy & Rustichini, "A Fine is a Price" (2000): https://Rady.ucsd.edu/_files/faculty-research/uri-gneezy/fine.pdf. [B7]

**State machine and opinion dynamics**
- [P] Rossetti & Cazabet, "Community Discovery in Dynamic Networks: a Survey," arXiv 1707.03186 / ACM CSUR 2018: https://arxiv.org/abs/1707.03186v3. Taxonomy details **UNVERIFIED** (abstract only). [B7]
- [P] Noorazar et al., "From classical to modern opinion dynamics," arXiv 1909.12089: https://arxiv.org/abs/1909.12089. DeGroot, Friedkin–Johnsen, Hegselmann–Krause, Deffuant–Weisbuch. [B7]
- [P] Hegselmann & Krause, *JASSS* 5(3) (2002): https://www.jasss.org/5/3/2.html ; Deffuant et al., "Mixing beliefs among interacting agents" (2000): https://next.sciencegate.app/document/10.1142/s0219525900000078. [B7]
- [P] Ye, Qin, Govaert, Anderson & Cao, expressed-vs-private opinion (EPO) model: https://arxiv.org/pdf/1806.11236. [B7]
- [P] Axelrod, Daymude & Forrest, "Preventing extreme polarization of political attitudes," *PNAS* (2021): https://pmc.ncbi.nlm.nih.gov/articles/PMC8685667. [B7]
- [P] Flache et al., "Models of Social Influence: Towards the Next Frontiers," *JASSS* (2017), title and venue only: https://econpapers.repec.org/RePEc:jas:jasssj:2017-90-1. Abstract **UNVERIFIED**. Esteban–Ray polarization index: **UNVERIFIED** (not fetched). [B7]

**Democracy and deliberation**
- [P] Fishkin, Siu, Diamond & Bradburn, "Is Deliberation an Antidote to Extreme Partisan Polarization?" *APSR* (2021): https://deliberation.stanford.edu/publications/journal-articles/deliberation-antidote-extreme-partisan-polarization-reflections. [B7]
- [P] Voelkel et al., "Megastudy testing 25 treatments to reduce antidemocratic attitudes and partisan animosity," *Science* (2024): https://sociology.stanford.edu/scalable-interventions-reduce-polarization-support-partisan-violence-and-anti-democratic-attitudes ; HKS abstract page: https://www.hks.harvard.edu/publications/megastudy-testing-25-treatments-reduce-antidemocratic-attitudes-and-partisan-animosity ; Kellogg summary: https://www.kellogg.northwestern.edu/academics-research/research/detail/2024/megastudy-testing-25-treatments-to-reduce-anti-democratic-attitudes/?p=1. Checked for this synthesis (VERIFICATION §E). [B7]
- [P] Broockman, Kalla & Westwood, "Does Affective Polarization Undermine Democratic Norms or Accountability? Maybe Not," *AJPS* (2022): https://isps.yale.edu/node/25356. Checked for this synthesis (VERIFICATION §E). [B7]
- [P] Nature Human Behaviour (2021) 26-country replication of Lees & Cikara on group meta-perceptions: https://www.nature.com/articles/s41562-021-01092-x. Author list **UNVERIFIED** (not captured). [B7]
- [P] Veri & Niemeyer, "Deliberative reason and the effect of minipublic configurations," *EPSR* (2025): https://www.cambridge.org/core/product/F19135A60561D8925735B44C236E673A/core-reader. The Deliberative Reason Index; R package `deliberr` noted, not evaluated. [B7]
- [S] Irish Citizens' Assembly, Eighth Amendment (Participedia): https://participedia.net/case/5317. The ~66% referendum figure is **UNVERIFIED**. [B7]

### K. Open agents, registries, token incentives and strategy markets
Added with B8. Items already listed above and also cited by [B8]: X automation rules and Bluesky guidelines and moderation docs (H, I), Perdomo et al. (J), Hanson futarchy and BTS (F), Gneezy & Rustichini (J).

**Platform rules**
- [P] X automated account labels: https://help.x.com/en/using-x/automated-account-labels. Universal availability **UNVERIFIED**. X automation rules re-checked for this synthesis (VERIFICATION §E). [B8]
- [S] Astral (AI-agent author), "agent governance on ATProto" (Feb 2026; secondhand): https://astral100.leaflet.pub/3mearallcqi2w. Community `ai-agent` self-labels, labelers and lexicons **UNVERIFIED**. [B8]
- [P] Neynar, autonomous Farcaster agent guide: https://docs.neynar.com/docs/autonomous-farcaster-agent ; [S] The Block, Network School acquires Farcaster (2026-10-15): https://www.theblock.co/news/ecosystems/2026-10-15-network-school-acquires-farcaster-from-neynar-418720. Post-acquisition agent policy **UNVERIFIED**. [B8]

**Registries, identity, attestations**
- [P] ERC-8004 "Trustless Agents" (Draft ERC, created 2025-08-13): https://eips.ethereum.org/EIPS/eip-8004. Status re-checked for this synthesis (VERIFICATION §E). [S] QuickNode explorer: https://erc-8004.quicknode.com/agents/ethereum-mainnet/23034. Mainnet date and counts **UNVERIFIED**. [B8]
- [P] Ethereum Attestation Service: https://attest.org/ ; Hypercerts v0.2, "Why AT Protocol": https://hypercerts-v02-documentation.vercel.app/getting-started/why-atproto ; MACI v3 docs: https://maci.pse.dev/docs/introduction. [B8]
- [P] Olas staking: https://olas.network/staking. Slashing semantics **UNVERIFIED**. [B8]
- [P] Taostats, weight copying: https://docs2.taostats.io/concepts/weight-copying/ ; Lui & Sun, Bittensor critical analysis, arXiv 2507.02951: https://arxiv.org/pdf/2507.02951. [B8]
- [S] Cointelegraph, Virtuals agent-token launches and drawdowns (2025-02-07): https://cointelegraph.com/news/new-ai-agent-launches-virtuals-plummet-token-drawdowns ; The Defiant, World AgentKit (2026-03-17): https://thedefiant.io/news/infrastructure/world-launches-agentkit-to-let-ai-agents-carry-proof-of-human-backing. [B8]

**Prediction markets**
- [P] Berg, Nelson & Rietz, "Prediction Market Accuracy in the Long Run," *IJF* (2008): https://iemweb.biz.uiowa.edu/about-iem/research/prediction-market-accuracy-in-the-long-run/ ; Rothschild & Sethi: https://papers.ssrn.com/abstract=2322420 ; Hanson & Oprea, *Economica* (2009): https://ideas.repec.org/a/bla/econom/v76y2009i302p304-314.html. [B8]
- [P] Chen, Kash, Ruberry & Shnayder, decision markets with good incentives: https://projects.iq.harvard.edu/sites/projects.iq.harvard.edu/files/yiling/files/a6-chen.pdf. Full-support randomized decision rule. [B8]
- [S] Blockworks, futarchy and MetaDAO: https://blockworks.co/news/understanding-futarchy-on-solana ; EA Forum, Metaculus vs Manifold (2023): https://forum.effectivealtruism.org/posts/PGqu4MD3AKHun7kaF/predictive-performance-on-metaculus-vs-manifold-markets. [B8]
- [S] Cases: The Block, French whale: https://www.theblock.co/post/324996/french-polymarket-whale-us-election-profit-france-ban ; Decrypt, Columbia wash-trading study (Sirolly et al., Nov 2025): https://decrypt.co/347842/columbia-study-25-polymarket-volume-wash-trading ; The Block, UMA governance attack: https://www.theblock.co/post/348171/polymarket-says-governance-attack-by-uma-whale-to-hijack-a-bets-resolution-is-unprecedented ; Decrypt, Zelensky suit market: https://decrypt.co/329210/polymarket-rules-no-237m-bet-zelenskyys ; The Block, Nobel probe: https://www.theblock.co/post/374199/officials-probe-polymarket-over-suspicious-trades-predicting-nobel-peace-prize-winner-reports ; WGBH/NPR, Kalshi insider cases (2026-02-25): https://www.wgbh.org/news/2026-02-25/kalshi-reveals-insider-trading-case-against-editor-for-mrbeast ; Finance Magnates, *US v. Van Dyke*: https://www.financemagnates.com/trending/us-charges-soldier-in-first-insider-trading-case-linked-to-prediction-markets/ ; Bloomberg (excerpt only): https://www.bloomberg.com/news/articles/2026-04-25/insider-trading-cases-threaten-reckoning-for-prediction-markets ; Euronews, Paris weather-sensor tampering: https://www.euronews.com/2026/04/23/hair-dryer-trick-behind-25000-win-france-probes-potential-weather-data-scam-linked-to-poly. The hair-dryer detail is **UNVERIFIED**. [B8]
- [P] CRS Legal Sidebar LSB11441, CFTC proposed event-contract rule (June 2026): https://www.everycrsreport.com/files/2026-06-24_LSB11441_b1797929d9c973e7d2962416b42af20eddfea3e4.html ; Federal Register 2026-05105 (not read; **UNVERIFIED**): https://www.govinfo.gov/content/pkg/FR-2026-03-16/pdf/2026-05105.pdf. [B8]

**Measurement and elicitation**
- [P] Mastroianni, Dana & Nichols, ideological Turing test (2024): https://www.experimental-history.com/p/ideological-turing-test. ITT discrimination for distant clusters **UNVERIFIED**. [B8]
- [P] Shnayder, Agarwal, Frongillo & Parkes, "Informed Truthfulness in Multi-Task Peer Prediction," EC 2016: https://arxiv.org/abs/1603.03151v2. [B8]
- [P] Yu, Gao, Bennett & Joseph, "Evaluating Voting Design Vulnerabilities for Retroactive Funding," arXiv 2505.16068: https://arxiv.org/html/2505.16068v1. [B8]

**Funding, tokens, law**
- [P] Optimism, RetroPGF 3 learnings: https://www.optimism.io/blog/retropgf-3-learnings-reflections ; "Evolution of Retro Funding in Season 8": https://gov.optimism.io/t/evolution-of-retro-funding-in-season-8/10024 ; Season 7 early evidence: https://gov.optimism.io/t/season-7-retro-funding-early-evidence-on-onchain-builders-impact/10163. [B8]
- [S] Debevoise, SEC interpretive release (2026-03-17): https://www.debevoise.com/insights/publications/2026/03/crypto-unchained-the-secs-pivotal-interpretive-rel. Not legal advice; prize-tournament and state gambling status **UNVERIFIED**. [B8]
- [P] Gneezy & Rustichini, "Pay Enough or Don't Pay at All," *QJE* (2000): https://econpapers.repec.org/RePEc:oup:qjecon:v:115:y:2000:i:3:p:791-810. [B8]

### L. Design-dialogue lineages and the transcript pipeline (B9)
Added 2026-10-30 from the Design Dialogue Memo; filled from brief B9 (`wave-1/B9-reciprocal-opening-landry-society-library-transcripts.md`). B9's transcript conclusion was corrected by Benjamin the same day: YouTube transcripts remain the primary source (a ToS gray area, not a blocker).
- [V] *Dialogos Arena — Design Dialogue Memo*, Benjamin Life (@omniharmonic) with Claude, 2026-10-30: `/home/claude/dialogos-arena/design/DESIGN-MEMO-2026-10-30.md`; Parachute `vault/research/dialogos-arena/design-memo-2026-10-30`; artifact https://claude.ai/artifact/Vm3DUhXucW2ZKjjtMEyoi8. The decision record behind §2. [memo]

**Reciprocal narrowing and reciprocal opening (feed rule, §2 D9, §8.6)**
- [S] Olshonsky, A. "Addiction Is Between You and the World," *Deep Fix*, 2022-12-23: https://deepfix.substack.com/p/addiction-is-between-you-and-the. Lewis's reciprocal narrowing and Vervaeke's reciprocal opening glossed. [B9]
- [P] John Vervaeke on *This Past Weekend w/ Theo Von* #462 (transcript): https://rosetta.to/u/theovon/john-vervaeke-this-past-weekend-w-theo-von-462. Credits a colleague's theory; reciprocal opening tied to love. [B9]
- [P] Jim Rutt Show EP 143, John Vervaeke Part 1 (transcript): https://jimruttshow.blubrry.net/?p=3299. Reciprocal opening; social media and the meaning crisis. [B9]
- [S] Petersonsphere glossary, "Reciprocal Narrowing": https://petersonsphere.github.io/Petersonsphere/Glossary-of-Terms/Reciprocal-Narrowing. Aliases: parasitic processing, addiction-forming process. [B9]
- [S] *Awakening from the Meaning Crisis* Ep. 13, "Buddhism and Parasitic Processing" (listing): https://metacast.app/podcast/dr-john-vervaeke/0YbNdI5Y/ep-13---awakening-from-the-meaning-crisis---buddhism-and-parasitic-processing/rIcFQ22k. The episode that first states reciprocal narrowing is **UNVERIFIED**. [B9]
- Marc Lewis, *The Biology of Desire* (origin of reciprocal narrowing): cited via the sources above, not read directly. No Vervaeke text applying the idea to ranking algorithms was found (**UNVERIFIED / likely absent**); "algorithm in reverse" is Benjamin's extension. [B9]

**Forrest Landry's Ephemeral Group Process (§2 D22, §6.5)**
- [P] EGP site: https://egp.community/ and https://egp.community/what-is-egp/. Inquiry first; base and branch questions; Inquiry Coach; archive. Names no creator, events or archive. [B9]
- [S] Life Itself wiki, "Ephemeral Group Process": https://notes.lifeitself.org/ephemeral-group-process. Steps and scale (~30–300 people). [B9]
- [P] Jim Rutt Show EP 153, Forrest Landry on the Small Group Method (transcript): https://jimruttshow.blubrry.net/?p=3679. EGP as a later "level two" stage of a larger body of work. [B9]
- The Stoa session (2020): recording **not located (UNVERIFIED)**. No published EGP outputs or case studies found. [B9]

**Jamie Joyce and the Society Library (§7.5)**
- [P] Jim Rutt Show Currents 076, Jamie Joyce on The Society Library (transcript): https://jimruttshow.blubrry.net/?p=4187. Topic flyover; claim IDs with all source quotes; steelmanning; status labels, not true/false. [B9]
- [P] Joyce, J. "Your Attempt To Refute Argument Maps Will Not Work," 2026-05-06: https://justjamiejoyce.substack.com/p/your-attempt-to-refute-argument-maps. 20+ relation types; Diablo Canyon map scale (~8,000 research hours); AI-assisted future. [B9]
- [S] Deep Tech Week, Society Library profile: https://www.deep-tech-week.com/organizations/the-society-library. [B9]
- [S] *You Are Not So Smart* 292, the Society Library (2024-07-22): https://youarenotsosmart.com/2024/07/22/yanss-292-how-one-organization-is-attempting-to-end-analysis-paralysis-by-creating-a-library-of-our-collective-arguing/. [B9]
- societylibrary.org was not fetched. "Papers of record" as Society Library terminology and any crowd- or Community-Notes-like ratification work are **UNVERIFIED**. [B9]
- [V] Parachute `vault/messages/twitter/jamie-joyce-twitter` (friendly DM thread, 2021–2024; basis for Q38); `vault/meetings/2024-02/2024-02-14_civic-innovation-summit` (not reviewed). [B9]

**Community Notes, Polis and vTaiwan (portability lineage, §7.5)**
- [P] Wojcik, Coleman et al., "Birdwatch: Crowd Wisdom and Bridging Algorithms…" (2022), arXiv 2210.15723: https://arxiv.org/abs/2210.15723. Bridging intercept = portability. See also sections E and H. [B9, B2, B5]
- [P] "Scaling human judgment in Community Notes" (2025), arXiv 2506.24118: https://arxiv.org/abs/2506.24118. LLM-drafted notes, human-rated. Not fetched; authors **UNVERIFIED**. [B9]
- [P] Polis / Computational Democracy Project: https://compdemocracy.org/ ; vTaiwan: https://info.vtaiwan.tw/. Not fetched in B9 (prior knowledge); vTaiwan's stalling when non-binding is in section E [B2, B7]. [B9]

**Transcript pipeline (§6.2, §11.1, R49, spec 4)**
- [P] YouTube Data API error reference: https://developers.google.com/youtube/data/reference/rest/v3/errors ; [S] Stack Overflow Q41087864 (Kiwix mirror), third-party caption download: https://kaweah.freedombox.rocks/kiwix/content/stackoverflow.com_en_all_2023-11/questions/41087864/youtube-api-v3-download-captions-from-third-party-videos-without-asking-for-au. Official `captions.download` is owner-only (docs page not fetched). [B9]
- [P] YouTube Terms of Service: https://www.youtube.com/terms. Prohibits automated access outside the official API. **Corrected reading (2026-10-30):** transcript libraries (e.g., `youtube-transcript-api`) and paid transcript services are routine and feasible; a ToS gray area tracked as R49, not a blocker. [B9]
- [S] "Speech-to-Text API Pricing 2026" (vendor-adjacent): https://convertaudiototext.com/blog/speech-to-text-api-pricing-2026. Source of the STT prices behind B9's cost ESTIMATES (verify on vendor pages). Commercial YouTube-transcript service pricing **UNVERIFIED**; podcast transcript APIs (Podscan, Listen Notes, Taddy) **UNVERIFIED**. [B9]
- [P] 17 U.S.C. §102(b); *Authors Guild v. Google*, 804 F.3d 202 (2d Cir. 2015); *Bartz v. Anthropic* (N.D. Cal., June 2025). Cited from prior knowledge; not legal advice. [B9]

- Kevin Owocki, "Attention Times" daily paper (companion to the Atlas): model for the daily pulse (§6.6). See section C. [memo §9]
