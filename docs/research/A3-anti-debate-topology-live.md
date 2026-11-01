# A3: Anti-Debate and Topology Live

> **Design update (2026-10-30).** The Design Dialogue Memo of 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`) records decisions that supersede earlier research recommendations where they conflict; see `synthesis/SYNTHESIS.md` §2. The research below is unchanged. For this brief:
> - **Modified: Topology Live as anti-debate tooling.** The extraction now runs on **any** recorded debate, dialogue, interview, panel or monologue, and is the **main seeding engine** of the map: transcripts of ~500 landmarks' YouTube and podcast output are the baseline (SYNTHESIS §2 D20–D21; §6.2). The shared proposition bank (D5) is the decided core of SEE.
> - **New flagship built on this brief: event maps** of recorded cross-cluster encounters (speakers' positions, meeting points, divergence by stratum, missed openings, the ripple), published within a day (SYNTHESIS §7.6). Live attribution is still uncertified, so **seed from recorded content first** (§2 D21).
> - **Modified: Lepp's crypto vs localism anti-debates as "a natural first arena pilot".** They remain the first *participant* pilot and the model for **Arena-hosted gap-filling anti-debates** between never-met cluster pairs (SYNTHESIS §7.7); the first *public* product is an event map from recorded content, surprising but not incendiary (§2 D20; Q31).
> - **Modified: matching "far in the social graph".** Distance is now measured by statement-reaction placement, and matching prefers never-met pairs and threshold people (SYNTHESIS §7.2).
> - **Strengthened: target-confirmed steelman as the core signal.** It is now the system's **gradient** (ratified cross-cluster description), carried at scale by Community-Notes-style cross-cluster notes; integration (step 7) is gated on two ratified steelmen (§2 D1–D3; SYNTHESIS §7.1, §7.5).
> - **Caveat added:** event participants are usually bridgers, not cluster cores, so landmarks' everyday output remains the baseline for placing clusters (R45).

*Wave-0 research brief for the Dialogos Arena. Author of record: Benjamin Life (@omniharmonic). Compiled 2026-10-30.*

## Summary

Stephanie Lepp (Synthesis Media) designed the Anti-Debate as an open-source (CC BY-SA 4.0) three-phase format. **Clarifying Difference** runs as openings, rebuttals and open debate. **Exploring Synthesis** runs as steel-manning each other, red-teaming yourself ("what would it take to change my position?") and integration questions. **Taking Stock** asks "how did my view expand, if at all?" and can include an optional pre/post audience poll. The stated goal is to expand minds rather than change them.

Benjamin's `antidebate-live` (product name Topology Live) turns live speech into a quote-anchored, event-sourced argument graph. Its rigorous ontology separates speech acts, speaker-independent propositions, per-speaker stances and inferred presuppositions. On top of the graph it derives cruxes, common ground, higher ground, updates and steelman records. It ran over all six recorded Anti-Debates for $0 in API costs (it used the Claude subscription). On the Ball × Kokotajlo replay it recovered 4/4 verified synthesis points. As of 2026-09-30 it was **not certified** for live release.

**I found no record of what happened at the 2026-10-11 Progress Conference event.** There is no commit after Sept 30, the vault task is still "pending", and the agent briefings for Oct 11–12 say nothing about it.

For the arena, the ontology's *commitment store* is the strongest available "accurate worldview" primitive. It is stated, quote-anchored and kept separate from inference. Its *updates ledger* plus *steelman confirmation* give a measurable "being changed" signal.

---

## 1. Findings

### 1.1 The Anti-Debate format: rules and phases

Primary sources: anti-debate.org how-to guide, ground rules and discourse matrix pages, plus the two Google-Doc guides, retrieved 2026-09-28 and summarised in `docs/client/anti-debate-how-to-guide.md`. TED talk transcript. Lepp's own words in the Gitcoin interview.

**What it is.** A debate format "where participants build on each other's insights, so that greater complexity can emerge". It is *not* against debate. It starts like a traditional debate and then keeps going (Synthesis Media, "What is the Anti-Debate?", Feb 2026, via repo summary). The Discourse Matrix places it under **dialectic** ("collaborative inquiry for deeper truth and synthesis"), not under debate (competitive) or dialogue (understanding and connection). Lineage: William MacAskill's 2017 "anti-debates" proposal, popularised by Peter Limberger and Connor Barnes, with Perspectiva running its own since 2022. Lepp also drew on Socratic, Oxford and Bohmian forms.

**Underlying theory (TED, Aug 2025, Bill Heck and Stephanie Lepp).**
- "Meeting in the middle" keeps everyone on a flat plane. The aim is to go "from common ground to higher ground".
- She uses a parallax analogy: each eye's view is true but partial, and together they give depth.
- Synthesis integrates the strongest thesis and antithesis. It is distinct from both-sidesism and from relativism, because some views are more right than others.
- The core move is to assume the other person holds a kernel of insight, then find it and incorporate it.
- Three integration questions:
  1. Flip either/or to both/and.
  2. Shift from "yes or no" to "under what circumstances (if any)".
  3. Look for perverse incentives that make the issue harder to resolve.
- The format grew out of *Faces of X*: short videos where one performer plays the strongest case for each side and then a synthesis.

In June 2026, Lepp described the format to Gitcoin as a debate that assumes the two people "were each holding different parts of the same bigger picture". The structure is "clarifying the different ingredients", then exploring "how you mix them into something new". She offered to run anti-debates on crypto vs. localism, either as a podcast or as a live event in Boulder (Gitcoin Brain transcript, 23:01–25:00).

**Ground rules** (anti-debate.org/ground-rules):
1. Engage in good faith: come to expand your mind, not to dunk. The host must not clip out of context.
2. Practise epistemic humility: update your beliefs on new information.
3. Abide by the format: keep to time limits and don't interrupt.
4. Disclose conflicts of interest.

**Topic criteria.** The topic should be debated, consequential, a place where synthesis is sought, and specific. It is framed as a yes/no motion so that people can track which side they are on and how that changes. The two seats are Affirmative and Negative. Debaters must hold significantly different views but be willing to steel-man. The moderator needs strong facilitation skills and ideally domain expertise. The guide's slogan is "Synthesis is the payload". The moderator holds back areas of agreement until Phase 2.

**Round structure (~90 min):**

| Phase | Round | Who / time | Function |
|---|---|---|---|
| 1 Clarifying Difference (~45') | Intro | Moderator 3–4' | Frame the format and the topic |
| | Pre-poll (opt.) | Audience | Three 1–5 scales: **position**, **comprehensiveness of views**, **faith in public discourse** |
| | Connection before content (opt.) | Neg, then Aff, 3' each | "Why do you personally care?" |
| | Openings | Aff, then Neg, 6' each | Position, with examples |
| | Rebuttals | Aff, then Neg, 3' each | |
| | Open debate | ≤10' | Unstructured; the moderator may seed disagreement |
| 2 Exploring Synthesis (~30') | **Steel-manning each other** | Clarifying Q 1', answer 1', **steel-man 3'**, response 1'; Neg first, then Aff | Present the strongest version of the opponent's view. The moderator calls out bad-faith steel-manning. |
| | **Red-teaming ourselves** | 3' each plus 1' responses | "What would it take to change my position?" The more specific (statistics, evidence), the better. |
| | **Exploring integration** ("the heart") | ≤12' | The moderator reads the three integration questions. Open dialogue to find synthesis. An optional co-created synthesis statement, policy or product. |
| | Audience synthesis (opt.) | ≤5' | Points of synthesis only |
| 3 Taking Stock (~15') | Check-in (opt.) | 1' each | Emotions and body sensations |
| | Contemplation | 1–2' silent | "Whether or how my view has expanded" |
| | **Closings** | Neg, then Aff, 4' each | "How has your position expanded, if at all?" |
| | Post-poll (opt.), Outro, Q&A | | Compare against the pre-poll |

The long guide adds optional extras:
- Judges, a fact-checker (including X Community Notes as a live fact-check) and a "3-strikes" rule.
- **Change the Question**: re-frame the motion as "under what circumstances…" or "to what extent…".
- A Steel Venn or Integral Matrix as the synthesis artifact.
- **Narration for the Tribe**: voicing one's memetic tribe. This is directly relevant to the SEE layer.
- A Socratic Search Space where the audience surfaces synthesis the debaters miss.

**Mapping to the task's three elements:**
- **Steelmanning** is an explicit timed round, and the steelmanned party gets a reply.
- **Finding the kernel of truth** is the TED "nugget of insight" move, operationalised in the integration questions.
- **Being changed** is reframed as "expanding", not "converting". It is elicited three ways: by red-teaming (stated update conditions), by the closing statement (self-report of expansion) and by the poll (audience position and comprehensiveness). The format never requires a stance flip.

**The format in practice (Ball × Kokotajlo, Lighthaven, 2026-03-09, moderated by Liv Boeree).**
- The event was booked out: 85 spots and a 185-person waitlist on the Partiful page.
- The moderator ran the format closely, with drift. Connection took 1 minute instead of 3. Red-teaming took 1–2 minutes instead of 3. Audience participation slid into general Q&A. The closing was merged with a co-created mutual statement.
- The verified convergences were: frontier-lab auditing and verification; preconditions for a US–China deal; concern about power concentration; and alignment as unresolved, with neither markets nor governments to be blindly trusted.
- A documented **update**: Kokotajlo shifted on export controls after Ball's parity question.
- A documented **steel-man success**: Kokotajlo said he felt "very appreciated and understood" after Ball's steel-man.

Source: `docs/client/ball-kokotajlo-reference.md`, which collates Synthesis Media, Jasmine Li's notes and the recording.

### 1.2 The Topology Live ontology (`docs/ONTOLOGY.md` v1.0)

The ontology builds on Toulmin, Walton schemes, ASPIC+ attack types, Hamblin/Walton–Krabbe commitment stores, Searle speech acts, CFAR double crux, Sunstein's incompletely theorized agreements, and Dialectical Topology / Ontography strata.

**Layered model:**

| Layer | Entity | Key fields / rule |
|---|---|---|
| MEDIA | Utterance | Speaker, word timestamps, attribution confidence and signals (channel, diarization, voiceprint), confirmed by auto or operator |
| DISCOURSE | ADU (argumentative discourse unit) | One or more spans plus a **speech act** |
| CONTENT | Proposition | Speaker-independent canonical sentence, positive polarity, type, scope, conditions, quantities, stratum |
| STANCE | Stance(participant, proposition, t) | Attitude, strength (from explicit hedges only), credence (only if stated), source |
| GROUNDS | EpistemicBasis, Presupposition | How the speaker claims to know it; what it requires (always inferred, must pass a necessity test) |
| DIALECTIC | Relation | Proposition↔proposition or ADU↔ADU |
| DERIVED | Disagreement, Crux, CommonGround, Convergence, HigherGround, Drift, Question, Update, Steelman | Computed from commitment stores |

**Speech acts.** Only some acts change a speaker's commitment store.

| Speech act | Enters speaker's store? |
|---|---|
| assert, concede, commit_conditional, answer (if it asserts), retract | Yes |
| rhetorical_question | Only its implied statement, `implied_by_act`, strength capped at `leaning` |
| hypothesize, nonliteral (irony, joke) | No |
| attribute, **steelman_report** | **Never assigned to the speaker** |
| question, challenge, meta | No |

**Proposition type** (epistemic kind of claim) and **stratum** (worldview depth):

| Type | Meaning | | Stratum (top → bottom) | Meaning |
|---|---|---|---|---|
| empirical | What is the case | | *higher ground* (derived) | Synthesis |
| causal | X brings about Y | | **praxis** | Policy, action |
| predictive | What will be (with resolution criteria and horizon) | | **empirical / predictive** | World state |
| counterfactual | What would have been | | **axiology** | Values |
| normative | Good or bad | | **epistemology** | How we know |
| prescriptive | Should be done | | **ontology** | What exists |
| definitional | What a term means | | | |
| conceptual | Relations between concepts | | | |
| modal | Possible or necessary | | | |
| meta | About arguments or evidence | | | |

**Stance.** Attitude ∈ {accepts, rejects, suspends, accepts_conditionally, accepts_for_argument}. Strength ∈ {certain, confident, leaning, tentative}. Source ∈ {stated, implied_by_act, inferred}. Inferred stances are never scored.

**Epistemic basis** (15 types):

| Group | Bases |
|---|---|
| Evidence | empirical_study, statistical, institutional_record |
| Authority / social | expert_testimony, consensus |
| Experience | direct_experience, anecdote |
| Reasoning | deduction, definition, model_or_simulation, analogy, historical_precedent |
| Judgment / intuition | intuition_empirical, moral_intuition, forecast_judgment |

**Argumentation schemes (Walton)** apply to `supports`: expert opinion, positive/negative consequences, cause→effect, sign, analogy, precedent, practical reasoning, values, slippery slope, verbal classification, popular opinion, best explanation, composition/division, commitment. Each scheme's unanswered critical questions become facilitator prompts.

**Relations:**

| Relation | Meaning |
|---|---|
| supports | Premises → conclusion (linked or convergent, with scheme) |
| rebuts | Attacks the conclusion |
| undercuts | Attacks the inference |
| undermines | Attacks a premise |
| qualifies | Narrows scope, adds a condition or lowers strength |
| concedes | Accepts the other's proposition (produces an Update) |
| agrees | Independent acceptance (convergence candidate) |
| equivalent | Identity merge |
| presupposes | Inferred dependency |
| defines | Fixes a concept sense (feeds drift detection) |
| exemplifies | Instance of a general claim |
| answers | Answer → question |
| evades | Shown as "not answered", never as "evaded" |

**Derived structures:**
- **Disagreement**: opposed stances on one shared proposition. Its depth is the proposition's stratum and its kind is the proposition's type, so "values crux" and "forecast crux" render differently.
- **Crux** (double crux): each party's stance on P depends on C, and they differ on C. Candidates are ranked by how many other disagreements route through C, weighted by depth, with at most one inferred link per path. Each crux card carries "A would update if…", "B would update if…" and the kind of evidence that would settle it.
- **Common ground**: shared ends, shared facts or shared framings. **Convergence** is the inferred cousin and is never scored.
- **Higher ground**: H is consistent with both commitment stores and integrates an element from each side. It carries its derivation, the cost to each side, and a status ∈ {candidate, operator-approved, released, confirmed by both}. There are six constructions:

| Construction | Shape |
|---|---|
| domain_partition | Both are right about different domains, times or scales |
| conditionalization | "If C then P" plus crux C |
| value_lift | A higher shared value under which both positions become means |
| incompletely_theorized_agreement | Same action, different reasons |
| sequencing | Both proposals in an agreed order |
| pareto_move | Better by each side's own lights |

- **Updates ledger**: any change in attitude, strength or credence by the same speaker on the same proposition, with its trigger. Every `concede` creates one.
- **Steelman record**: A's steelman of B is compared with B's store as {captured, missed, distorted, added} plus B's confirmation.
- **Provenance** of every item: live_provisional → operator_approved → released → canonical → participant_confirmed | participant_contested.
- **Faithfulness rules (§8)**: span entailment, no new content, hedge and scope preservation, attribution by speech act, signability ("would the speaker sign this?"), minimal and marked inference, neutral register.

### 1.3 How live mapping works (`docs/ARCHITECTURE.md`)

**Capture.**
- Per-person mic channels go through Silero VAD, a channel gate (≥6 dB ownership), Parakeet ASR with word timestamps, a voiceprint check and attribution fusion. Below 0.85 confidence, an utterance is held for the operator.
- The offline path uses FluidAudio diarization plus an operator relabel.
- A browser path exists, with hosts supplying their own Anthropic key.

**Passes.**

| Pass | Trigger | Output |
|---|---|---|
| L0 | Turn closes on a speaker change, a pause over 1.2 s, or a 25 s window | Closed turn |
| L1 | Each turn | Segment and extract ADUs, propositions (including sameAs), stances, relations, bases and questions (target ≤6 s) |
| Code validators | L1 output | Span exists; entities and numbers are a subset of the span; hedge and quantifier lexicons; speech-act guard |
| L2 | Validated items | Independent critic: pass / repair / reject |
| L3 | About every 45 s or 4 turns | Link: identity merges, cross-turn relations, presuppositions, concept senses |
| L4 | Round boundary or about every 3 minutes | Insight: graph-ranked crux, higher ground, drift, prompts, steelman assessment, updates |
| Canonical | After the event | Full re-run at maximum effort |

**Event sourcing and delivery.**
- Everything is an append-only event with a media timestamp, so the system supports playback, undo, and a choice between "as seen live" and "canonical".
- Audiences only receive `release.*` events, which the server filters.
- The facilitator controls a 0–5 **audience detail dial**: Dark, Frame, Positions, Clash, Map, Full.
- Round detection keys on moderator cues, using Anti-Debate templates in `packages/core/src/formats.ts`, including adapted rounds for moderators who run their own structure.
- The 3D topology: X = stance hemisphere, Y = stratum, Z = time. A crux renders as a fault plane, and higher ground floats above.

### 1.4 Quality and evaluation (`docs/QUALITY.md`, `evals/results.md`, QA audit)

**Four quality layers:**

| Layer | Metrics |
|---|---|
| Attribution | 100% after operator review; ≤0.5% A↔B swaps |
| Extraction | Precision ≥0.90, central recall ≥0.85, faithfulness ≥0.97, hedge and scope fidelity ≥0.95, speech-act accuracy ≥0.92 |
| Structure | Identity F1 ≥0.85, relation F1 ≥0.75, presupposition necessity ≥0.85 |
| Insight | Crux top-3 overlap ≥0.6, higher-ground signability ≥0.75, higher-ground recall ≥3/4 on Ball × Kokotajlo, prompt usefulness ≥0.6, L1 latency p50/p90 ≤10/18 s |

**Gold sets.**

| Set | Content |
|---|---|
| G1 | The Dialectical Topology Marcus × Demartini fixture |
| G2 | Ball × Kokotajlo |
| G3 | Two more debates from the playlist |
| G4 | 60 adversarial red-team items: steelman leakage, irony, hypotheticals, scope traps, buried concessions |
| G5 | Live-room audio |

Segments are held out, inter-annotator κ is measured, and participant confirm / amend / contest rates count as a first-class metric.

**Results so far (hand-graded, indicative only).**
- Faithfulness on early Dialectical Topology segments went from ~82% to 94% across prompt versions.
- All six playlist debates were processed: Ball × Kokotajlo, Gender-Affirming Care, Belief in God, Destiny × Shermer, Open-Source AI, and an Ignite talk.
- Higher-ground recall on Ball × Kokotajlo was 4/4 (r3) and ≥3/4 (r5).
- The crux paths landed on each debate's real hinge.
- Recurring finding: **stated disagreements are rare (0–2 per debate)**. Debaters seldom restate each other's claims, so most disagreement is inferred from clashing claims. Shared ground is thin unless the system adds convergence links.
- Fixed failure modes: crux ping-pong (fixed with hysteresis), card churn (stability rule), cruxes about a person rather than the question, and the loss of all higher-ground cards in one run through a name/key bug.

**QA audit, 2026-09-30.** Verdict: "suitable for supervised development and rehearsal; not yet certified".
- The attribution gate held all 28 lines in two one-minute probes, about 19 review lines per minute, which is too much for one operator.
- Short live ASR cuts dropped words.
- There was no physical mic test.
- Human gold sets were not yet built.

### 1.5 What happened at the live event (2026-10-11)

**Not recorded. UNVERIFIED.**

The plan was: Sunday 2026-10-11, 2:00–3:30 pm, Lighthaven, the optional add-on day of Progress Conference (Oct 8–11). The audience dial was set to 0 ("only me, as facilitator"), debaters would see nothing, and the event was in person. Stephanie's must-haves were crux, higher ground and facilitator prompts. Her success criterion: a clear yes if it adds clarity; a clear no if it muddles the experience.

Evidence that nothing was recorded:
- `antidebate-live` has no commit after 2026-09-30, and no session or eval mentions Oct 11.
- The Parachute task is still `status: pending`.
- On Oct 10 the morning briefing said it "can't see its status".
- The Oct 11 and Oct 12 briefings and the Oct 12 evening review don't mention it.
- The Progress Conference site doesn't list the session.
- I could not reach antidebate.xyz: the fetch needed permission and timed out.

The orchestrator should ask Benjamin directly about four things: whether the tool ran, the debaters and topic, Stephanie's 1–5 ratings, and whether a playback exists. Still-open items from the docs: debaters, topic, consent and AV access.

Earlier relationship: Benjamin's calendar shows "Anti-Debate Video || Benjamin + Stephanie" (2023-04-24) and "Anti-Debate || Benjamin + Stephanie" (2023-05-11), plus a 2022 meeting through her Center for Humane Technology address. So the collaboration predates Topology Live by about three years.

---

## 2. How this answers the governing question (layering and validation)

**What this domain adds to "accurately depicting a worldview":**

1. **The commitment store is the accuracy anchor.** Ontography's known failure is that it can't separate AI inference from real belief. The Anti-Debate ontology solves this by construction:
   - Stances are `stated`, `implied_by_act` or `inferred`, and only stated stances count.
   - Presuppositions are always inferred, translucent, and must pass the necessity test.
   - Steelman and attribute speech acts never commit the speaker.

   A worldview map for the arena should keep the same two-tone rendering: *what X has said* (signable, quote-anchored) versus *what X's position seems to require* (inferred, contestable).
2. **The strata are shared.** The ontology / epistemology / axiology / praxis strata match Ontography's four layers, so a cluster map (SEE) and a dialogue map (MEET) can live in one schema. Disagreement **depth** (which stratum) and **kind** (fact, forecast, value, definition) are both computable. They are better cluster descriptors than topic embeddings, which cluster by subject rather than by stance (see BRIEF).
3. **Speaker-independent propositions with polarity in the stance** let people from different clusters attach to the *same* node. This is what makes cross-cluster comparison computable, the "where exactly do they disagree" property (decision D5). It requires identity resolution (sameAs or equivalence), which embeddings can serve for candidate retrieval only.
4. **Layering without overload.** The audience dial (0–5) plus per-module toggles is a tested pattern for progressive disclosure:
   - Frame
   - Positions: 1–3 theses per person
   - Clash: crux plus common ground
   - Map
   - Full, with inferred layers

   The same ladder works for "your place in memetic space":
   - your cluster
   - your core commitments
   - your cruxes with neighbouring clusters
   - full graph

   This addresses the 600–1,200-node illegibility problem.

**Validation methods this domain contributes:**
- **Signability**, by the person or a proxy: "would you sign this canonical sentence?" Participant confirm / amend / contest rates are a direct accuracy metric for any worldview map, and they generalise to "is this you?" on an X-derived profile.
- **Steelman confirmation as an ideological Turing test.** If B confirms A's steelman of B, then A's model of B is validated, and so is the map's model of B if the map generated or scored the steelman. The steelman record's {captured, missed, distorted, added} fields are a ready-made scoring scheme for any automated depiction of a worldview.
- **External synthesis recall.** A published moderator summary served as ground truth for higher-ground recall (4/4). The same approach applies to cluster maps: test whether the map predicts the cruxes and convergences that real cross-cluster conversations later surface.
- **Gold sets with inter-annotator κ.** When κ is low, sharpen the ontology before tuning the prompt.

---

## 3. Reusable assets and design implications: Anti-Debate as the MEET layer

### 3.1 Reusable now
- The `packages/ontology` schema (Zod), validators (span, entity/number diff, hedge/quantifier lexicons, speech-act guard), the L1→L4 prompts, crux ranking (`packages/graph`), the event log and projections, the playback explorer, and the Anti-Debate round templates (`formats.ts`).
- Six fully processed debate sessions plus the Ball × Kokotajlo reference: a seed corpus for testing arena matching and synthesis scoring.
- The Dialectical.Claims "thinkers as methods" agents. Agents could pre-run a synthetic anti-debate between two *clusters* to produce candidate cruxes before any humans meet.

### 3.2 An asynchronous online Anti-Debate (proposed protocol)

| Live round | Async equivalent | Map output |
|---|---|---|
| Pre-poll | Each party, and optionally their cluster cohort, scores position, comprehensiveness and faith in discourse | Baseline |
| Connection | A short "why I care" text or voice note | Not committed; human context |
| Openings / rebuttals | Written or recorded posts with a word or time cap | Commitment stores |
| Open debate | A threaded exchange over 48–72 h, with a turn cap | Clash and questions ledger |
| **Steel-man** | Each party writes the other's steel-man after asking one clarifying question; **the target scores it** | Steelman record; confirmation |
| **Red-team** | Each party states "what would change my mind" as typed update conditions | Crux card update conditions |
| **Integration** | The system proposes 2–3 higher-ground candidates (with derivation and cost to each side); both parties edit them and sign or decline | Higher ground with status `confirmed by both` |
| Closings and post-poll | "How did my view expand?" plus a repeat of the three scales | Updates ledger; delta |

Async lowers the attribution problem to zero, because text is self-attributed. It also gives time for real steel-manning. Two things are lost: live presence and the embodied check-in and somatic rounds. The facilitator role becomes partly AI: Walton critical-question prompts and the three integration questions. A human moderator still gates it.

### 3.3 Matching: who should talk to whom (proposed)

Use the SEE layer to propose pairs (or tribe-delegate pairs) that maximise expected synthesis:
- **Far in the social graph** but **overlapping on propositions**: both have stances on shared high-centrality propositions, so they will actually clash rather than talk past each other.
- **Disagreement at a mid stratum** (praxis or empirical/predictive) and **shared ends** at axiology. Lepp's integration questions work best here. Pure values cruxes are labelled "often irreducible".
- **Bridge and edge nodes** from the cluster map as first participants: they have the highest prior steel-man ability.
- A track record from earlier rounds: steel-man confirmation rate and good-faith flags. This is the Ground Rules made legible.
- The long guide's "Narration for the Tribe" suggests a **delegate model**: each cluster sends someone to voice it, and the cluster cohort polls before and after.

### 3.4 A measurable "being changed" signal

The format's own term is *expanded*, not *changed*. A metric that only rewards stance flips would betray the format and invite fake concessions. Proposed composite:

| Signal | Source | Notes |
|---|---|---|
| **Stated update events** | Updates ledger: attitude, strength or credence change with trigger, `concede` / `retract` | Stated only; one strong signal per event |
| **Steel-man fidelity** | Target-confirmed steelman; captured / missed / distorted | Validates understanding without requiring agreement |
| **Update-condition explicitness** | Crux cards with "would update if…" stated, not "not stated" | Measures falsifiability offered |
| **Higher ground signed by both** | Higher-ground status `confirmed by both` plus construction type | Synthesis quality; the cost to each side shows it isn't a mushy middle |
| **Comprehensiveness delta** | Pre/post poll scale 2 (participants and cluster cohort) | The format's own "expand" measure |
| **Faith-in-discourse delta** | Poll scale 3 | Civic outcome |
| **Retention** | Re-poll after 2–4 weeks; does the person reuse the other side's concepts? | Separates performance from change. UNVERIFIED as practice; proposed |

A synthesis-quality score could combine:
- signability by both sides
- derivation coverage (elements from each store)
- the cost declared to each side
- stratum lifted (for example, a praxis dispute resolved by a value_lift)
- external rater judgment

The MOVE layer should weight **cross-cluster** confirmed steel-mans and signed higher ground, not raw stance change.

---

## 4. Risks and open questions

1. **The live event's outcome is unknown** (§1.5). The format's fitness for MEET is evidenced only by replays and by the March 2026 Ball × Kokotajlo event itself.
2. **Live attribution is not certified.** Async text avoids this problem. Any live arena session inherits the QA audit's P0 blockers.
3. **Most disagreement is clash-inferred, not stated** (0–2 stated per debate). Cruxes are mostly "candidates", not demonstrated double cruxes. Async formats could require explicit stance replies on the other's top propositions to fix this.
4. **Gaming the "being changed" signal.** Rewarded updates invite performative concessions. Mitigate with target-confirmed steel-mans, retention polls, and no reward for flips alone.
5. **False synthesis.** The PRD makes "genuine, irreducible disagreement" a valid output. The arena must honour values cruxes rather than force higher ground.
6. **Consent and representation.** The ground rules ban out-of-context clips. Publishing maps of people's commitments, especially ones derived from their X feeds, needs signability review and contest rights. Debater consent for Oct 11 was itself unresolved.
7. **IP and licence.** The format is CC BY-SA 4.0 (Lepp/Synthesis Media), so derivatives must carry attribution and share-alike. Topology Live is Benjamin's own work and should not be attributed to OpenCivics.
8. **Scale and cost.** About 400–770 LLM calls per 90-minute debate. That was $0 on the subscription, but not at arena scale.
9. **Model drift in the docs.** ARCHITECTURE specifies Opus 5.5 for all passes, but the QA audit says the configured L3/L4 model is Sonnet 5.5. This is minor.
10. **Open:** Would Stephanie co-design an async or online version? In June 2026 she offered to organise topic-specific anti-debates for Gitcoin (crypto vs. localism, possibly live in Boulder). That is a natural first arena pilot.

---

## 5. Sources

**Repo (`/home/claude/omniharmonic/antidebate-live`, HEAD 1f4e1db, 2026-09-30)**
- README.md; docs/README.md (decisions D1–D8); docs/PRD.md (§1–3, §6 dial, §7 formats, §9 metrics)
- docs/ONTOLOGY.md (v1.0, 2026-09-28)
- docs/ARCHITECTURE.md (§1–6)
- docs/QUALITY.md; evals/results.md; docs/QA_AUDIT_2026-09-30.md (§6 blockers)
- docs/NEXT_STEPS.md
- docs/client/stephanie-feedback.md (her answers, 2026-09-28); docs/client/prior-debates.md; docs/client/anti-debate-how-to-guide.md (summary of anti-debate.org and the two guides, retrieved 2026-09-28); docs/client/ball-kokotajlo-reference.md
- packages/core/src/formats.ts

**Primary web**
- Anti-Debate How-To Guide: https://www.anti-debate.org/how-to-guide.html. Ground rules: https://www.anti-debate.org/ground-rules.html. Discourse Matrix: https://www.anti-debate.org/discourse-matrix.html. All via the repo summary. A direct fetch of anti-debate.org (home, about, references) was **blocked** in this session.
- Synthesis Media, "What is the Anti-Debate?" (Feb 2026): https://www.synthesismedia.org/p/what-is-the-anti-debate. Via the repo summary; a direct fetch was blocked.
- Synthesis Media, "Anti-Debate on AI Governance: Dean Ball x Daniel Kokotajlo": https://www.synthesismedia.org/p/anti-debate-on-ai-governance-dean. Via the repo reference.
- Bill Heck and Stephanie Lepp, "Why meeting in the middle isn't enough for today's trickiest debates", TED (Aug 2025): https://www.ted.com/talks/bill_heck_and_stephanie_lepp_why_meeting_in_the_middle_isn_t_enough_for_today_s_trickiest_debates. Transcript read via https://rosetta.to/u/ted/meeting-in-the-middle-isn-t-enough-for-today-s-trickiest-debates-bill-heck-steph
- Partiful, "Anti-Debate on AI" (Lighthaven, Mar 9): https://partiful.com/e/Toy7N2AzrWOqNiBrYhqO
- Josh Szeps, "A Better Way to Debate?" with Stephanie Lepp (Nov 2025): https://uncomfortableconversations.substack.com/p/szeps-live-a-better-way-to-debate (preview only)
- Roots of Progress, Progress Conference 2026 (Oct 8–11, Lighthaven; no anti-debate listed): https://rootsofprogress.org/conference/
- Anti-Debate playlist: https://www.youtube.com/playlist?list=PLRN1pe0US2hS-mWZAiYJ8OMII8BcB6UXc (not fetched)
- antidebate.xyz: the fetch was blocked (permission timeout).

**Parachute (Benjamin's vault)**
- vault/tasks/active/topology-live-antidebate-progress-conference (status pending; milestones)
- vault/agent/insights/2026-10-10, 2026-10-11, 2026-10-12; vault/agent/deliberations/2026-10-12-evening (no mention of the event outcome)
- wiki/writing/dialectical-claims (Benjamin's essay; anti-debate inspiration; "being changed by dialogue (true dialogos)")
- Searches returning nothing relevant after Oct 10: "Stephanie Lepp", "anti-debate", "antidebate", "Progress Conference", "Topology Live", "Lighthaven", "Synthesis Media"

**Gitcoin Brain**
- meetings/2026-06-19_gitcoin-x-stephanie-research-interview, plus /transcript (23:01–25:00)

**Google Calendar** (Benjamin's)
- "Anti-Debate Video || Benjamin + Stephanie" (2023-04-24); "Anti-Debate || Benjamin + Stephanie" (2023-05-11); "Benjamin + Stephanie" (2022-09-21, 2023-04-27)
