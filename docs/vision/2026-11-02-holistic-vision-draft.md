# Dialogos Arena: a holistic vision (wet clay draft)

*For Benjamin Life (@omniharmonic), from his ideas. Drafted by Claude, 2026-11-02. "I" below means the drafter, and every recommendation is a proposal for Benjamin to accept, change or reject. Status: draft v2, revised after an independent critical review. Not adopted.*

**What this is.** One frame that holds the memetic map, the Community Notes behavioral layer, agents, a social contract dialogue, Polis-style clustering and a civic fingerprint, with a purpose, a plan and an implementation strategy.

**What it does to existing decisions.** It proposes amendments, listed in section 14. The spec and decisions log stay in force until Benjamin changes them.

**Evidence** is in two reports, and this document does not repeat their sources:
- `reports/Memetic mapping and computational democracy.md`
- `reports/Social contract and civic fingerprint.md`

Every number marked "proposed" is a starting guess that no study backs. Most recent sources are unreviewed preprints. These documents were drafted by an Anthropic model, and Anthropic's proposals are among those assessed.

## 1. In short

We appear to be at a threshold between world stories. The argument about AI is really an argument about what humans are, what we owe each other and who gets to decide what comes next. Most people cannot see that argument whole, and the camps inside it mostly cannot describe each other fairly.

**Dialogos helps people find out whether they could fairly negotiate a future together, and what they would have to understand about each other first.** It does not write the new social contract. It builds ground a contract would need.

The design has one simple shape:

- **Three spaces:** what public thinkers argue (the map), what groups of people think (rounds), and where one person stands (the mirror).
- **One shared object joining them:** a small public set of tested questions, called anchors here.
- **One rhythm:** seasons, each built around one threshold question.
- **One game:** the existing reputation score, rewarding people for understanding each other.
- **One public record:** the understanding matrix already named in D-31.1, grown into a Record of Understanding showing who has described whom in words the described side signed.

Underneath sits an asymmetry: **keep people's answers private and make understanding public.** Answers are dangerous because they are precise. A signed description is valuable because it is public. Civic tech usually collects opinions and publishes a summary. This does the reverse.

**Where I differ from your framing.** You asked about a public dialogue on the social contract. I recommend running exactly that, without making "social contract" the headline promise, and without any final contract text. Reasons are in section 6. If you disagree, the design still works, and only the public language changes.

## 2. The purpose, as a ladder

A social contract seems to need agreement, and Dialogos rejects convergence. They turn out to be different rungs of one ladder.

| Rung | What it means | Who can do it | Dialogos's role |
|---|---|---|---|
| 1. **Recognition** | Each side can describe the other in words the other signs | Anyone, with the right tools | Core job |
| 2. **Meta-consensus** | Sides agree on what is at stake: which values are legitimate, which beliefs credible, what the options are, while still disagreeing on the answer | Publics in structured dialogue | Core job, harder to measure |
| 3. **Terms** | A real agreement between parties | Only people with a mandate | Hand off, and never claim it |

**Refusal is valid on every rung.** Benjamin's own argument is that consent must include the right to refuse. So "this is the wrong question" and "I reject this frame" are real answers, recorded and reported.

**Only a real signature counts.** Hume and Dworkin argued that hypothetical consent binds no one. "They would sign this" is a forecast and must be labeled that way. Our measure covers rung 1, reciprocal understanding. It should be called the signing score, with meta-consensus as the goal. `CLAUDE.md`'s definition of meta-consensus is narrower than the literature's, and that is listed as a decision.

**This has a risk.** Dryzek warns that meta-consensus can be manipulated, and understanding could become the polite face of terms set elsewhere. Section 16 keeps that objection visible.

### The argument that gives this force

Benjamin's writing holds two theories of why a contract binds:

- **Leverage:** people had rights because their labor was needed.
- **Relationship:** people are owed consent because they are embedded in and affected by a shared world nobody can leave.

If AI does make much human labor unneeded, the first theory leaves those people with no claim. Only the second survives. I think this is the sharpest statement of why this moment matters, but it is a position, and a contested forecast sits inside it. It belongs in his signed essays. If the map carries it as default language, the map places its own home at the summit. On the map it gets placed and rated like everything else.

## 3. How the parts fit

```
            PUBLIC                                       PRIVATE BY DEFAULT
   ┌───────────────────┐      ┌───────────────────┐    ┌──────────────────┐
   │   THINKER SPACE   │      │   PUBLIC SPACE    │    │  PERSONAL SPACE  │
   │   the memetic map │      │  seasonal rounds  │    │    the mirror    │
   │   quotes, ideas,  │      │  aggregates only  │    │  on your device  │
   │   layers, links   │      │                   │    │                  │
   └─────────┬─────────┘      └─────────┬─────────┘    └────────┬─────────┘
             │                          │                       │
             └───────── ANCHOR QUESTIONS (public, tested) ──────┘
                                        │
                  BRIDGING + SIGNING → one reputation score
                                        │
                  RECORD OF UNDERSTANDING (understanding matrix)
                                        │
                       assemblies and people with mandates
```

**Anchors are shared words, and data stays apart.** A thinker's position on an anchor comes from a quote. A group's comes from a round. Yours stays with you. The hypothesis is that three groups answering the same questions can be compared without merging people into one database. It is only a hypothesis, because thinkers and publics often read the same words differently. Measuring how far that goes is part of the work.

Anchors can be framed as the tested, stable subset of the questions in D-31.13, which already says questions are drawn from claims after extraction. Claims stay the evidence layer. That framing narrows the conflict with D-31.4.

**The gaps between spaces are findings.** The share of public disagreement that falls outside what thinkers argue about, the **elite-blind share**, shows what the map is missing. A question that different sides read differently stays out of the anchors and goes on the map as a finding, joining the existing sense-fork work.

**This corrects a planning assumption.** The design lets thinkers define the terrain and drops newcomers onto it. The evidence says to do it the other way round:

- **Thinker to thinker claims** can stay as they are.
- **Claims placing a person in the terrain** should wait until a real public sample has calibrated the questions, with thinkers then scored into that space.

That collides with the first-60-seconds flow ("land as a dot, nearest landmarks") in the spec and the planned private beta, covered in sections 13 and 14.

### What each part is for

| Part | The one question it answers | What it must never claim |
|---|---|---|
| Memetic map | What do public thinkers hold, and why? | That their camps are the public's camps |
| Sensing | What new fork just opened among tracked voices? | That it knows what the public is asking |
| Anchors | What can everyone be compared on? | That the list is neutral |
| Rounds | What divides this group right now? | That groups last or compare across rounds, except through anchors |
| Mirror | Where do I stand, and how sure is that? | That it is an identity or a type |
| Bridging | Does this text survive across difference? | That survival means truth |
| Signing | Can A describe B in words B signs? | That this is consent to anything |
| Seasons | Could these parties fairly negotiate? | That they have a mandate |
| Agents | Can machines help draft, find and translate? | Any standing to sign |

Every failure in the research came from a tool claiming more than it measures. Keeping this table honest is an architectural rule.

**Existing pieces with a home here:** MEET's notes, steelmen and anti-debates are the formats used in the Describe stage. Priority encounter PE-01 (e/acc × d/acc) is a natural first pair. Event and lineage tracking is the Sense stage. The dispute affordance applies everywhere a person is named or placed.

### A few voices, a few questions

Benjamin's instinct is right, with two corrections. First, Dialogos already reads a watchlist, so the choice is what sits on top of it. A fixed set wins at comparing people, on cost, and at placing someone. It loses at discovering what nobody thought to ask. So it adds a layer and replaces nothing.

Second, a watchlist of famous voices catches **new forks among those voices**. It does not catch **new questions in the public**. The best early-warning evidence concerns network-central ordinary accounts, and US legislators followed public discussion more than they led it. Public-written statements fill that gap. A small sensor layer of central ordinary sources, counted only at topic level and never profiling anyone, is parked as a later test because platform terms are unchecked.

## 4. The metabolic loop: seasons

A season is how the project takes in what is happening, digests it and returns something usable.

1. **Sense.** When a new proposition draws opposed stances from two or more clusters in a short window, it becomes a candidate question. Public-written questions join here.
2. **Seed.** Choose one threshold question. Draft statements from the map, and have critics inside each side review them first. Reserve a share for the public (a quarter, proposed).
3. **React.** An open round. A public "who is missing" gauge runs throughout. Breadth.
4. **Describe.** Small balanced groups write each other's positions, using notes, steelmen and anti-debates. Depth.
5. **Sign.** A second broad round. Each side reads descriptions of itself mixed with real statements and decoys, then signs, corrects or refuses. Breadth.
6. **Publish.** The Record gains what was signed, what was refused, what was named as the real disagreement, who was missing, and which questions enter the anchors. Dissent is reported, with names only for those who choose it.

Breadth, depth, breadth is the observed shape of the stronger cases, though no controlled study compares sequences.

**A season takes about 20 weeks part-time, not a quarter.** The Spine's quarterly seasons are for leaderboards, so these dialogue seasons are a new proposal. Two a year is realistic.

**Why end on descriptions?** Chile's experience shows that a process owned by one camp reproduces the divide, and a wider public then rejects the text. Descriptions signed by each side avoid giving anyone that single target.

**How "extended" actually works.** No case kept the same people active on one tool for months. Length came from staged programs with replaced members. So the extended dialogue is a chain of seasons. A small returning cohort stays by consent, and new people join each round. The seasonal pseudonyms in section 9 mean a returner has to choose to link their seasons. Whether reputation alone keeps people is an untested bet that the first season measures.

## 5. Polis and Community Notes: what the combination is

The combination is mostly established, and calling it novel would be wrong. The contribution is a staged arrangement in which each method does its own job.

| Stage | Method | Job |
|---|---|---|
| React | Polis-style voting on short statements | Find what divides this group now |
| Group | Soft membership over many splits | Avoid betting everything on one partition |
| Bridge | Community-Notes-style factoring | Find what survives across difference |
| Sign | Described side rates real, description and decoy | Test understanding, not agreement |

### The limits of Polis clustering

Polis is a good one-month instrument and a poor foundation for anything lasting.

1. **No lasting identity.** 89.1% of participants vote in one session, as a cookie. Only shared anchors allow comparison across rounds.
2. **Group counts are partly artifacts.** About 75% of conversations report two groups, 62.5% do on recomputation, and exported clusters cannot be reproduced.
3. **Consensus scoring fails on thin data.** At typical sparse voting levels it can run backward against the true ranking.
4. **Pass hides several states.** It is often how people say a statement is bad.
5. **One hard label per person,** with no uncertainty, and a cluster is not one voice.
6. **Conveners shape the result** through seeds and moderation.
7. **Silence is informative,** because people choose what to answer.

Order effects, strategic voting, and whether Polis groups match survey-validated groups are all unstudied. Better methods exist, and almost none has been tested on Polis data. That can happen offline for free on public exports, and it would be a contribution by itself.

### What to use

**Season Zero should not use Polis.** With 30 to 40 people it adds little, and it cannot collect "wrong question." A small custom form can, and its data stays under our control. Open rounds later can self-host Polis or a successor, with named non-answers, moderation frozen before scoring, reported uncertainty and a published recompute. Third-party hosting needs written deletion terms first, because Polis data is often public.

### Finding what cuts across clusters

This is the part Benjamin most wants, so it needs a named output. A season should publish three different things:

- **Bridges:** statements that survive across several splits. Scored by averaging over the many possible divisions.
- **Slates:** a short set in which every sizable faction finds a statement it can sign, following generative social choice. A slate protects minorities better than one bridging statement.
- **Clean cruxes:** the disagreements that remain once each side has been fairly described.

Bridges alone are dangerous. Consensus-seeking selection can flatten conflict and erase minorities, and over half of Bowling Green's ideas reached 80% agreement, which is pleasant and often says little. So each bridge should be tested for distinctiveness: would it be accepted even if it meant nothing? And clean cruxes get equal billing. Better disagreement is a real result here.

## 6. The social contract track

**Why not a headline.** OpenAI's April 2026 paper made the phrase mainstream, and critics call it a settlement written by its main beneficiary. A headline frame would recruit mostly one cluster. Calling it a contested topic also fits the map: frames become objects in their own right.

**Frames layer.** Contract, treaty, covenant, refounding, New Deal, commons, civilizational race and exit each imply different parties and outcomes. Which cluster accepts or refuses which is untested, and finding out would be cheap and new. Every encounter gets a "refuse the frame" option.

**A public sorting question.** Does this proposal change who decides, or only how the gains are shared? Most lab proposals share gains. Unions and Pope Leo XIV's encyclical press on power. This sort is a useful public service that can be done offline.

**One candidate slate of questions.** Sensing and critics in each side should propose questions too, or this list repeats the error of whoever-picks-the-items. These are a starting point:

| Question | Why it is a candidate |
|---|---|
| If much human work stops being needed, what do we still owe each other, and why? | Crosses party lines and tests foundations. Carries a premise, so it tests "wrong question" |
| Who should decide what AI is for? | The power question many proposals avoid |
| Who counts as a party: future generations, the excluded, non-humans, agents? | The inclusion question in any renegotiation |
| What would make an agreement legitimate to those who did not write it? | Sets up a handoff to bodies with a mandate |

At two seasons a year, only two or three can finish before the 2028 assemblies, so the order matters. The offline step comes first: read the 27 thinkers against these four and see whether the map shows anything new.

The AI region remains the right start, for the reason Benjamin gives: it is where the argument about humanity is happening in public.

## 7. The civic fingerprint, staged as a mirror

Can questions place someone better than extraction? Conditionally yes. It is measurable, and it is a personal tool.

- **Keep the raw pattern.** One left-right axis explains about a seventh of issue opinion, real personal idiosyncrasy about three sevenths, and instability the rest. Reducing someone to axes discards what is distinctive.
- **Avoid types.** Published counts range from 3 to 9 depending on method. Use continuous positions with soft groupings. No team names, badges or share cards. A mailing that merely mentioned party registration raised party identification by 8.1 points, so a label may harden the tribes it describes. For a project named after schismogenesis, that is the failure to fear most.
- **Use richer answers than Polis.** Agree or disagree with a strength tap, then **torn**, **don't care**, **don't know enough**, **wrong question**, plus skip. That split is untested.
- **Say so when someone does not fit.** One study labels about a fifth of people idiosyncratic, though its method is disputed.
- **Item choice draws the map.** One Belgian party's share of advice ranged from 5% to 32% across statement sets. Publish selection rules, resample, and report how much depends on the set.
- **A stored answer set is a key.** In tests on public Polis data, 94.6 to 99.4% of people in samples of 332 to 2,008 had a pattern nobody else shared at 40 answers. Unique does not mean named, and real populations clump more. But cutting questions buys little safety until you get near 10, so no answer set should ever be called anonymous.

### Three stages

**Stage 1, the Quote Mirror.** You answer anchors with names hidden. On your device you then see, item by item, how thinkers' words read against your answer, with quotes. No distance, no space and no ranking of thinkers. This is the right first version because it uses our unusual asset, quotes a person can check. It is not calibration-free or automatically true. It rests on machine readings of thinkers, which have been fragile, and people may read an item differently from a thinker. So:

- Each comparison reads: "a machine reading of this person's words, unsigned and disputable."
- "No stated position" is shown often and honestly.
- Tallies of who you match most are suppressed, though a person can still count them.
- Flagged and conflict-of-interest landmarks are excluded.
- A small check of thinker stances against real people's answers happens before anything public.

**Stage 2, the Calibrated Mirror.** After about 1,000 recruited adults (proposed, needs spending approval) have calibrated the anchors, the mirror can show a position as a cloud of uncertainty, with the words "you answered like this school on these items."

**Stage 3, the Civic Passport.** Only if it earns it: carrying proof of standing into a dialogue without revealing answers. Expensive and late.

Anchors would amend D16's "no surveys," which ruled out fixed per-person batteries. An opt-in mirror built from real contested statements is close to the spirit of that decision, but it is still a change to it, and that change is Benjamin's to make.

## 8. Who may sign for a side?

This is the deepest tension in the design. Signing requires knowing who belongs to the described side, and that is the thing most worth not holding. Any answer leaves a cost.

**Season Zero: sides by self-identification and sponsorship.** No map placement is needed. People say which side they stand with, and a named insider from that side sponsors them, in the spirit of D-31.14. Results are labeled "self-identified sides, not map clusters." This is small, honest and possible now.

**Open seasons: a chosen, temporary signer role.** Someone who wants to sign opts in for one season, under a seasonal pseudonym, with a short set of reactions held for that season and then deleted. This is much less than keeping reactions while an account exists. Placement in that role needs calibrated anchors and a deck longer than OD-20's. A 12-item deck is only about .67 to .75 reliable on one axis at best, by the report's arithmetic. Signers can see and reject their category, which Audrey Tang's conditions require and the design currently lacks.

**Inviting at random and capping self-selection remain the main guard.** Architecture §4.12.2 already includes both. A device-held claim alone would be too easy to fake.

**Portability uses a learned viewpoint.** Community Notes shows viewpoint can be learned from ratings alone, so portability needs no cluster. Map clusters become one split among many, with a leftover factor reported as a standing audit of what the map missed. That answers part of D-31.1. Which clusters count, and who may draw their boundaries, stays open. Equal weight per cluster means splitting a cluster doubles its voice.

**An idea that did not survive review.** I proposed letting the real-versus-decoy test double as proof of belonging. It fails as a guard: it tests knowledge, not motive, so an informed opponent scores highest. It penalizes dissenters and rewards orthodoxy, and it contaminates the score it feeds. It stays only as an offline experiment, never to set anyone's weight.

## 9. Privacy rules

**The promise: your mirror answers stay on your device by default, and leave only if you choose it, for a named purpose.** I first wrote "never," but the plan itself needs exceptions, and a promise with hidden exceptions is worse than a modest one. So they are listed in public:

| Exception | Why | Rule |
|---|---|---|
| Signer role | Signing | One season, then deleted |
| Calibration panel | Stage 2 | Separate consent, separate instrument |
| Label and usability tests | Stage C | Small consented study |
| Round answers | Anchors also appear in rounds | Held under the round's rules, and not linked to the mirror |
| Bringing mirror answers into an account | Current API allows import | Remove, or make it explicit opt-in |

**Further rules:**

- No per-rater public data. Community Notes' open files would be a serious mistake to copy, because they carry a permanent ID and group on every rating.
- Aggregates only at k ≥ 50, as specified. A panel of 30 to 40 cannot meet that, so Season Zero participants consent to a small-panel disclosure rule in advance.
- Reputation carries forward as a coarse tier, and the project can link people at that moment. This conflicts with public profiles and long decay in the spec, which remains a decision.
- The divide alarm and audits work on comparisons of cohorts over anchors, so they need no long personal histories.
- No third-party scripts, and no demographics stored beside answers.
- Adults only, with the mechanism checked in legal review.
- Legal compulsion is the most concrete live US threat. A voluntary outside ethics review would be cheap and credible.

Nobody can center a view on a brand or an opponent, and no bulk export of person-to-cluster data exists. A public worldview map is also a targeting list.

## 10. MOVE and the game

**D-31.1 survives: one score, and the score is the game.** Bridging is portability. Signing is fidelity. The rest are measures reported alongside it. The Record is what the game produces.

**What changes inside it:**

- **Signal detection replaces the fixed 0.70 bar.** Pass rates in one study ran from 0.32 to 0.71 just from changing the rule. Two numbers per pair: can raters tell real from description (near zero is good), and real from decoy (high proves attention).
- **Decoys carry duties.** Debrief people, and never attach a distorted statement to a named landmark.
- **Wording is separated.** "This is what we think" differs from "this is true," or a side can refuse accurate descriptions it dislikes. A description any side would sign says nothing, so distinctiveness has its own check.
- **The prediction score.** How well does A predict what B endorses? High prediction with low signing suggests accurate contempt, and low prediction with high signing suggests flattery. It needs B's votes held at least in aggregate, and it decays as results are published, so held-out items rotate. Nobody should promise this reduces hostility, because the evidence conflicts.

**The divide alarm.** Rewarding raters for matching outcomes could reward conformity inside a cluster, so the instrument could harden the divide it measures. Track whether alignment within sides rises among players compared with a comparison cohort, and commit in advance to changing the rules if it does. The scorer is unbuilt, so this is cheap to design in now.

### Agents

Agents are disclosed, registered and bound to a human operator, under the Open Agent Charter. They never sign. The directional-shift audit and agent-free re-fit stay.

Audrey Tang's public line matters here and it is stricter than our design. First-pass clustering is fine if people can reject the categories, and an AI bridging draft is fine if people then rate it. But AI should not draft positions, decide which disagreements matter, or turn summaries into decisions, and "simulated personas are not a remedy for people who were never invited." Our agents writing notes about a cluster sits close to that edge. The difference should be stated openly: an agent's draft of a side is a claim awaiting that side's signature, and it never stands in for them.

The evidence pulls both ways. AI writers produce 52% of X's Helpful notes on 22% of ratings. Language models also score minority opinions lower, and tests of AI facilitators mostly show null outcomes.

| Season stage | Agents may | Agents may not |
|---|---|---|
| Sense | Find candidate forks and trace lineage | Decide which disagreement matters |
| Seed | Propose statements, labeled, for people to review | Choose the final set |
| React | Nothing participant-facing | Vote or simulate participants |
| Describe | Draft descriptions, disclosed, and find cruxes | Speak for a side |
| Sign | Build decoys under review | Sign or rate |
| Publish | Summarize, checked against sources | Issue findings unreviewed |

**The agent leaderboard and strategy market** (D-31.3, D-31.2) remain on the books, and they carry the original behavioral experiment: which strategies help clusters understand each other. I would hold both until the core works, because in the assembly stream they would read badly if they led. That is a real cost, since it defers part of the game Benjamin designed.

**Nudges are invitations to understand someone.** Disclosed each time, started by the person, based on reasons rather than weak spots, symmetric across clusters, with no target opinion, on the device, quiet before elections, and publishable. Reciprocal opening fits this. Anything using a fingerprint is off by default.

## 11. Joining the stream

**The landscape.** BLOOM builds citizens' assemblies about AI, with human delegates and AI as tooling, community assemblies from February to July 2027, and a national assembly planned for 2028. Audrey Tang is a senior adviser. Declare Interdependence is a public writing process stewarded by Amelia Rose Barlow. Declaring Our Tech Futures, which Barlow co-stewards, is the connector and names both as partners. That rests on its own page plus a friendly BLOOM citation. Whether the two 2028 assemblies are one event is unknown, and it is the most useful thing to ask.

**The opening.** Nobody found so far measures whether groups can describe each other, though that search was by effort rather than across the field. So the role is **a small measurement offer, not another assembly.** Every success in the record had a route to power. This stream is the nearest such route, and BLOOM's rule that each host names a decision-maker is at least a partial answer to the failures of Iceland and vTaiwan.

**The danger.** This coalition may read as one civic and tech-reform cluster. A measurement layer that joins it loses standing with the camps it needs. So:

- Map the coalition like everyone else, starting offline from public documents. Pro-Human Declaration signers make a good strange-bedfellows test.
- Offer measurement, audit and method, without co-branding.
- Never use the map to pick delegates or stand in for a town. It is built from public figures.
- Skip the BLOOM host application. Hosts need standing in a place and a local decision, and Dialogos has neither.
- Measure against Audrey Tang's conditions first, and consider asking for a critique.

**The 2027 window.** Season Zero will not finish in time, so anything for the February to July 2027 assemblies has to be separated from it. A small "describe the other side" item with one host is possible if a host wants it, and that needs a low-key conversation by about January, when hosts are named. If it does not happen, 2028 is the larger moment and waiting costs little.

Another candidate offer is a consented audit testing whether a woven collective declaration traces to its submissions. Those writers are mostly private people, so nothing may be ingested without their consent.

Contact with anyone is Benjamin's choice. Listening at public sessions costs nothing: 6 and 18 November, plus the 10 November BLOOM host information session.

## 12. People, money and effort

This is the weakest part of the plan, and the research found no shortcut.

- **Team today:** Benjamin and agents. No case shows a volunteer team holding a national, cross-divide dialogue for months.
- **Season Zero needs people Benjamin cannot replace with agents:** a named sponsor on each side, a facilitator, and critics reviewing seeds. Marathon County ran about 100 people over two years and still lost conservatives from 28% enrolled to 23% attending, even with $100 gift cards. Benjamin's own network is also a cluster, so outreach through it risks one-camp ownership.
- **Money:** $3,000 to $4,000 per round if 30 to 40 people are paid $100. Calibration, legal review and hosting are unpriced. These sit above the near-zero budget, so funding is a real decision, and funders also shape perceived ownership.
- **Effort:** unestimated, and every stage below depends on it.

## 13. Implementation strategy

Each stage is useful by itself, and the cheap tests that could kill an idea come first. Dates are estimates. Slice 1 has its own calendar, so the table shows how they meet.

| Stage | When | Slice 1 calendar | Conflict |
|---|---|---|---|
| A. Clear the ground | Now to 6 Dec | P0 to P3 gate | P3's first-60-seconds prototype places people before calibration. Keep it internal and labeled experimental |
| B. Prove it offline | Dec to Mar | P5 beta (28 Dec to 31 Jan) | The beta places people, breaking section 3. Decide before OD-27 on 4 Jan. D-31.5 limits new regions until Slice 1 passes |
| C. Mirror, small circle | Mar to May 2027 | P6 from 1 Feb, P7 from 15 Mar | Scoring work proceeds under the old design unless amended |
| D. Season Zero | About 20 weeks, from summer 2027 | After P7 starts | Misses the 2027 assembly window |
| E. Measurement offer | Separate track | None | Needs someone to talk to |
| F. Calibration | When funded | None | Money |
| G. Regular seasons | From 2028 | Depends on all of the above | Scorer must match amendments |

**The simplest way through these conflicts:** let Slice 1 finish as the evidence engine, and treat the public-facing parts of P5 to P7 as the items most likely to change. That is Benjamin's call.

### Stage A: Clear the ground. No outreach, no spend.

- Decide the items in section 15 that fall due at the P3 gate. OD-11 and OD-12 are due 3 November, separately from this work.
- With his go-ahead, fix the map's trust issues: compare silence handling side by side, fix the 54% line, resolve Karp's seed status, and correct the Habermas Machine doc errors.
- Read the Imitation Game paper before any novelty claim.
- Confirm the source of "framing is power," which could not be verified as a Karp quote.

**Done when:** we know which of the nine schools survive proper silence handling.

### Stage B: Prove it offline. No outreach, near-zero cost.

- Draft 60 to 80 candidate anchors from the map's attack links and the candidate questions. These are thinker-origin, so they are a draft until public-written statements join.
- Read the thinkers against them, with "no stated position" allowed. People hand-code a sample.
- Add the frames layer and the "who decides or who gains" sort.
- Test replacement clustering on public Polis exports, and benchmark Community Notes factoring, Polis consensus and many-splits scoring.
- Build the decoy generator with safeguards, and simulate sleeper and cluster-splitting attacks.
- Backtest the new-fork trigger on past months.
- If Slice 1 has passed, add open source, national security and Catholic social teaching.

**Done when:** thinker stances are stable across works, humans find decoys believable, and the trigger beats a simple baseline.

### Stage C: Quote Mirror and a small circle. Needs approval to invite anyone.

- Check thinker stances against a small group's answers on the same items.
- Build the browser-only Quote Mirror.
- Try it with a small consented circle, including critics outside Benjamin's world.
- Run a small randomized test with arms for labels, no labels and name reveal.

**Done when:** people find it true and useful, wrong-question answers show biased items, and labels do not visibly harden identity. The sample will be too small to prove safety, so this only rules out obvious harm.

### Stage D: Season Zero. Needs approval, legal review, and possibly stipends.

- 30 to 40 adults, self-identified, sponsored, in at least two or three sides. PE-01 is a natural pair.
- Critics on each side review seeds.
- Run one question through all six stages with a small custom form.
- Publish a first Record, with consent and Benjamin's approval.

**Done when:** at least one side signs a description of itself written by another, participants call the process fair even where they lost, and we know whether reputation kept them.

### Stage E: Measurement offer.

See section 11. Runs only if Benjamin opens that conversation.

### Stage F: Calibration and the public space.

Recruit about 1,000 adults, since an open web sample can be faked cheaply by language models. Calibrate anchors, score thinkers in, and report the elite-blind share for the first time.

### Stage G: Regular seasons and MOVE.

About two seasons a year. Turn on the amended scorer with the divide alarm, bring agents in under the charter, widen beyond AI, and contribute to the 2028 assemblies if the stream is open.

## 14. Amendments this vision would make

| Document | Current | Proposed |
|---|---|---|
| D-31.1 | Clusters as viewpoint | Many splits with learned factor |
| D-31.1, OD-14 | Fidelity by fixed bar | Signal detection, plus decoys |
| D-31.3 | Ratify only if placed through reactions | Self-identified and sponsored in Season Zero, signer role after |
| D-31.2, D-31.3, OD-08, OD-09, OD-25 | Market and agent board in the game | Held until the core works |
| D-31.4, D-31.13 | Question-first rejected, questions drawn from claims | A tested anchor subset added on top |
| D-31.5 | New regions after Slice 1 | Unchanged, and Stage B waits for it |
| D16 | No surveys | Opt-in mirror on anchors, no trait batteries |
| Spec first-60-seconds | Land as a dot, nearest landmarks | Quote comparison until calibrated |
| Spec public profiles, Spine 180-day decay | Long reputation | Seasonal pseudonyms with coarse tier, open |
| Architecture reactions | Kept while account exists | One-season signer role |
| Spine seasons | Quarterly | Dialogue seasons of about 20 weeks, leaderboards unchanged |
| `CLAUDE.md` | Meta-consensus as signing | Signing as rung 1 of a ladder |

**Stays:** the map, extraction pipeline, quote anchors, layers and typed links. Agents never ratify. Public figures only from public output, with a dispute route. The 15 flagged landmarks stay out of anything public. The Atlas stays, as an explorer view, while a 2D map with cards and fault cross-sections is tested as the lead view.

**Parked, not dropped:** whole-population claims, the sensor layer, a custom open-round tool, zero-knowledge passports, and terrain or 3D as lead views.

## 15. Decisions for Benjamin

In the order they bite.

| # | Decision | My recommendation | By |
|---|---|---|---|
| 1 | BLOOM host application | Skip it | 20 Nov |
| 2 | Is this draft the direction, with the Record of Understanding as what the game produces? | Yes, to test | Soon |
| 3 | May we fix the map's trust issues? | Yes | Soon |
| 4 | Mirror privacy promise: "stays on your device by default, listed exceptions" | Yes | Before OD-14, 6 Dec |
| 5 | D-31.1: which clusters count, and who draws boundaries? | Many splits, map clusters as one split, boundaries reported with sensitivity | With OD-14 |
| 6 | OD-20 deck size, given reliability | Larger, or not used for ratification | 6 Dec |
| 7 | What do P3 and the P5 beta show people, given the placement rule? | Keep placement internal or clearly experimental | Before OD-27, 4 Jan |
| 8 | Hold back the agent market and leaderboard? | Yes | OD-09 and OD-25 dates |
| 9 | D16 and D-31.4: allow anchors on top of extraction? | Yes, after Slice 1 for anything public | Before Stage B |
| 10 | "Social contract" in public | A named topic with the frame contestable | Before outreach |
| 11 | Rename the score, and reword `CLAUDE.md`? | Signing score, ladder as the definition | Before public copy |
| 12 | Stream posture | Listen first, then a small measurement offer | When you choose |
| 13 | Launch scope | US-only, built to GDPR standard | Before any public use |
| 14 | Funding, and who sponsors each side | Decide before Stage D | Before Stage D |
| 15 | One scoped legal review | Yes, before Season Zero publishes | Before Stage D |

## 16. How we would know, and what could make this wrong

| Measure | What it tells us | First possible |
|---|---|---|
| Who is missing | Which groups fell away, since dropout is not neutral | Stage D |
| Wrong-question rate | Refusals by item and side | Stage C |
| Signing score | Does a side sign a description of itself? | Stage D |
| Prediction score | Does A know what B thinks? | Stage D |
| Frame sensitivity | How much results move as anchors are resampled | Stage B, for thinkers |
| Divide alarm | Is alignment within sides rising? | Stage G, needs cohorts |
| Elite-blind share | What thinkers fail to argue about | Stage F |

**Stop or rethink if:**

- Anchor resampling gives different pictures of the same people most of the time.
- Thinker stances fail to match real people's answers on the same items.
- Sides sign anything flattering, so signing cannot tell good from pleasant.
- The divide alarm rises and rule changes do not bring it down.
- Only one side shows up.

**The strongest objections:**

- **Recognition may lead nowhere.** Understanding transfers no power. Nothing in the record shows an unmandated process gaining power through understanding alone.
- **The people mapped are not the people signing.** Someone near a school is a proxy for it, and thinkers may never sign.
- **Scale may not arrive.** Nine schools make 72 directed pairs, and rater supply may run out first.
- **The frame is one culture's.** Layers, legibility and meta-consensus are themselves a position, and refusals should be recorded and not explained away.
- **Publishing changes what is mapped.** Classifying people changes them, which is the mechanism in the project's name.
- **Novelty is modest.** What survives the prior-art check is narrow: engineered decoys, quote-anchored comparators, and a persistent directional score between sides drawn from a different population's public works. Comparing real and imitated text is prior art.

## 17. Open wet clay

- Is the Record of Understanding a document, a map layer or a public ledger?
- Should thinkers be invited to sign descriptions of themselves, and when?
- What does "meaning hyperspace" mean to Turquoise Sound? It appeared nowhere in the research, and she is the person to ask.
- Is there a treaty or covenant form better than a record? Those traditions should follow Benjamin's own rule of asking before borrowing.
- Could a person share their mirror with a study circle they trust?
- Is Dialogos ultimately a product, a public utility, or a method others run?
