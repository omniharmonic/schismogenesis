# Lifeworld Atlas: design

Owner: Benjamin Life (@omniharmonic). Status: approved by Benjamin in chat, 2026-11-01 ("this sounds
great, let's fully document the plan and then implement it"). The name is the builder's working name.

## Why
Benjamin wants to see, at a glance, how clusters of thinkers and ideas relate, for example how
accelerationism relates to AI safety; to place a person in that landscape and understand them through
how their ideas connect; and to see how worldviews are built from clusters of ideas. It must keep the
project goal in view: meta-consensus, with "the hyperspace of cyberspace legible and metabolic".

Dialectical Topology stalled because raw embeddings measure topic, not belief (silhouette −0.009 on
its own data, docs/research/A2). The current page reduces each person to a dot on a 2D map from 25
questions.

## The central idea
A worldview is a structure, not a point. A thinker appears as a shape rooted in shared ground: a set
of ideas spanning layers from root assumptions up to action, joined by typed links.

## Goals
1. A 3D force-directed atlas of one region, AI futures, built only from real public works.
2. People and ideas in one space, so schools appear as measured regions.
3. Selecting a person lights their structure. Selecting two shows where they share roots and fork.
4. Typed links between ideas: supports, rebuts, undercuts, presupposes, and others from the existing
   13-relation set.
5. Reasons versus belonging, per idea (Habermas against Karp's dissertation).
6. Sense forks: the same word used differently by different schools.
7. A first metabolic layer: each idea's arrival and spread through time.
8. The map's own assumptions shown on the map.

## Non-goals
- All 234 niches, or the full 819 landmarks. One region proves the form.
- Live updating, accounts, a public site, or dispute workflows. The page stays private.
- Measuring "integration" events. We lack the longitudinal data, and the page says so.
- Scoring anyone. Nothing here feeds MOVE yet.

## Anti-goals (a failure even if it runs)
- A beautiful hairball, or a map that looks precise but is not.
- Shared roots that exist only because a model worded them alike.
- Embeddings presented as belief.
- People flattened into objects: the map is a threshold to encounter.
- Ranking worldviews or implying the middle is right.

## Constraints
- CLAUDE.md red lines hold. Public output only. Flagged landmarks stay out. Short quotes (≤280
  characters) with links, never full texts. Nothing from Benjamin's vaults enters the dataset; the
  vault informs the design only.
- No paid APIs. Model work goes through the Claude subscription with the existing file-queue pattern.
- The extraction pipeline is reused unchanged: a quote anchor and the NLI gate decide what is a claim.
- Agents never ratify. Inferred stances are never scored and are visibly different.
- Pronouns on the page stay neutral.

## Cohort (decided by the builder; all unflagged, checked in Neon)
Existing 13 plus 14 new from Slice 1: Daniel Kokotajlo, Max Tegmark (AI safety); Scott Alexander
(rationalists); William MacAskill (EA); Guillaume Verdon (e/acc); E. Glen Weyl, Audrey Tang
(d/acc, plural); Emily M. Bender, Timnit Gebru, Karen Hao (AI critics); Robin Hanson, Tyler Cowen,
Jason Crawford (progress, forecasting); Josh Hawley (populist backlash). Two or three own-name public
works each, about AI, technology or society. Anyone with no suitable public text is dropped and the
page says so.

## Ontology of meaning
Reuses the Topology Live ontology already in the schema and names its lineage.

| Element | Field | Built on |
|---|---|---|
| Idea | `proposition`, speaker-independent, positive polarity | Toulmin, AIF |
| Depth | `proposition.layer`: ontology, epistemology, axiology, empirical, praxis | Apostel and Aerts's worldview components, Bourdieu's doxa, Habermas's lifeworld |
| Kind | `proposition.tl_type` | Topology Live |
| Validity | `proposition.validity_tag`: truth, rightness, intelligibility | Habermas |
| Link | `proposition_relation.tl_relation_type` | Walton, ASPIC+ |
| Holding | `stance`, with `source` stated or inferred | commitment stores |
| Term | `meme`, `meme_use` | existing |

An **idea** merges claims that assert the same thing at the same layer. A **root** is an idea at
ontology or epistemology. A root is *stated* when a quoted claim asserts it, and *inferred* when a
reader finds the author's accepted claims presuppose it. Inferred roots need a written necessity
argument ("if this were false, claim X could not stand") and are drawn dashed.

## Geometry
- **Height is fixed by layer.** It is not learned.
- **Horizontal position** comes from correspondence analysis of people × ideas, with each idea doubled
  into accept and reject columns. Inferred stances have half weight. People and ideas get coordinates
  in the same space. The first two dimensions seed the layout.
- **Forces** refine it in the browser: supports attract, rebuts and undercuts repel, presupposes pulls
  horizontally only, and an anchor spring holds each node near its measured position so that the
  layout cannot wander from the evidence.
- **Embeddings** are used only for grouping claims into themes, for finding sense forks, and as the
  baseline that structure must beat.

## Measures
- `fork_profile(a, b)`: per layer, shared and opposed ideas; the lowest opposed layer; shared roots.
- `schools`: people clustered on correspondence coordinates, with 500 bootstrap reruns over ideas.
- `reasons_load(idea)`: argument links per person who holds it. High holders with few reasons reads as
  "belonging"; the label is descriptive and comes with the numbers.
- `sense_fork(term)`: contextual embeddings of one term by school, tested by permutation.
- Honesty checks, reported on the page and in the status note:
  - fidelity of the layout: trustworthiness of the 2D seed against full correspondence space;
  - **stated-only ablation:** rerun schools and fork profiles without inferred roots;
  - **embedding baseline:** niche silhouette for raw embeddings against structure;
  - blind check: a second reader verifies a sample of holdings, links and all inferred roots.

## The page
- Default view: a stable, labelled angle where schools read as regions. Links hidden until selected.
- Levels: school, then idea, then claim with quote and link.
- Select a person: their structure lights up. Select a second: the fork view.
- Select an idea: holders, links, reasons load, first year, quotes.
- Search, layer toggles, a time slider, sense-fork panel, "how this map was made", and a node for the
  map's own assumptions. Works with reduced motion, on a phone, and with a text list as a fallback.
- Library: `3d-force-graph` over three.js from an allowed CDN.

## Left to the builder
Theme list, exact thresholds, visual design, and how many works each person needs, provided the
checks above are reported.

## Hypothesis under test
Accelerationists and AI safety people share roots and fork at values. If the data does not show that,
the page says so.

## Decisions from the builder check (builder's calls, for Benjamin to review)
1. **Merging test.** An idea is looser than exact equivalence, which found nothing in the pilot (0 of
   1,188 pairs). The test: would someone who holds claim A accept this idea as a fair statement of
   part of their view, with no added content? Ideas stay specific enough that a thoughtful person
   could reject them. Topic labels are not ideas. The stated-only ablation guards against over-merging.
2. **Rejection and silence.** A person rejects an idea only when a quoted claim of theirs contradicts
   it. Silence is missing data, never rejection or a zero. Inferred stances exist only for roots.
3. **Readers.** Blind readers are separate Claude agents. Everything they produce is provisional, and
   the page says no person has ratified it. Agents never ratify.
4. **Time.** Two or three works per person cannot show drift. Dates mean "first appearance in this
   sample", and the page says so.
