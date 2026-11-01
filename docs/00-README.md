# Dialogos Arena: Handoff Package

> Paths: in this repo, these docs live in `docs/`; `seed/` is at the repo root.

*Benjamin Life (@omniharmonic) · 2026-10-31*

This is everything from the ideation, research and design process, organized for starting the build in Claude Code. Save this folder as the root of a new project directory, then open Claude Code there; it will read `CLAUDE.md` automatically.

## Start here
| File | What it is |
|---|---|
| `CLAUDE.md` | Instructions for Claude Code: read order, order of precedence, Slice 1 build order, engineering rules |
| `01-BUILD-SPEC-v1-SLICE-1.md` | **The locked build spec.** What to build now |
| `02-DECISIONS-LOG.md` | Every decision since the synthesis and the order of precedence when docs conflict; pending decisions point to `10` |
| `design-spine/SPINE.md` | The shared spine: canonical vocabulary, repo layout, jobs S1–S14, provenance, LLM backends, phases P0–P7, non-negotiables, and §10 the adopted extensions (tables, fields, enums, CLI, leaderboard safeguards) |
| `07-PRD.md` | Product Requirements Document: goals, north-star metric (RCU), personas, features with acceptance criteria, UX flows, safety tests, launch criteria, eye-test and self-recognition protocols |
| `08-TECHNICAL-ARCHITECTURE.md` | Technical Architecture: containers, data model, pipeline S1–S14, the Community-Notes-style scorer, `arena_llm`, Procrastinate jobs, API, web, agents and market, infrastructure, security, evals, ADRs |
| `08a-APPENDIX-DDL-and-SCORER.md` | Appendix to 08: the full Postgres DDL and the full scorer implementation and simulation test |
| `09-IMPLEMENTATION-PLAN.md` | Implementation Plan: calendar, build-swarm operating model, agent switch points, phase-by-phase tasks and gates, runbooks, budget, risks |
| `10-OPEN-DECISIONS.md` | The single list of decisions waiting on Benjamin (OD-01 … OD-34), with options, recommendations, what they block and needed-by dates |
| `design-spine/REVIEW-NOTES.md` | The 2026-10-31 cross-document consistency review: every fix made |
| `03-DESIGN-MEMO-2026-10-30.md` | The first-principles design dialogue: gradient, notes, landmark-content map, first 60 seconds, time, event maps |
| `04-RESEARCH-SYNTHESIS.md` | The full research synthesis: reframe, taxonomy, SEE/MEET/MOVE, agents, the integration game, ethics, risks, open questions, spec checklist. Its bibliography is in `research/BIBLIOGRAPHY.md` |
| `05-DATA-MODEL-and-ENCOUNTER-PLAN.md` | Entities, storage, ER diagram, the O(N) encounter crawl, coverage optimization, phased run plan |
| `06-LOCAL-COMPUTE-and-OPERATIONS.md` | The GB10 Blackwell box: measured throughput, model stack, reliability techniques, operations, 30-day pre-arrival plan |

**Order of precedence when docs conflict:** spec (`01`) > decisions log (`02`) > spine (`design-spine/SPINE.md`) > PRD / architecture / plan (`07`, `08` + `08a`, `09`) > design memo (`03`) > data model / local compute (`05`, `06`) > synthesis (`04`) > `research/`.

## `seed/`: the map's seed data
- `SEED-v4.json`: machine-readable seed. 234 niches, 817 landmarks, with platforms, verification status, mirror pairs and flags.
- `SEED-v4.md`: readable niche table by domain.
- `QA-REPORT-v4.md`: merge, rename and placement decisions, the balance audit, and flags.
- `SLICE-1-LANDMARKS.md` / `.json`: the Slice 1 candidate set. 8 core and 7 adjacent niches, 53 landmarks.
- `VERIFICATION-QUEUE-v4.json`: landmarks still to verify.
- `SEED-BRIEF.md`, `GAP-BRIEF.md`: inclusion and exclusion rules and the seed schema.
- `atlas-2026-07-28-partial.md`: Kevin Owocki's Atlas tribe names (partial).
- `scripts/`: the Python scripts that built v1–v4, for regenerating or extending.

## `research/`: evidence base
- `00-RESEARCH-BRIEF.md`, `00-RESEARCH-PLAN.md`: the original brief and plan.
- **A1–A5:** Benjamin's prior work: Ontography, Dialectical Topology / Dialectical.Claims, Anti-Debate / Topology Live, his theory corpus, and the memetic-tribes lineage.
- **B1–B9:** the field:
  - B1: philosophical lineages
  - B2: computational democracy
  - B3: mechanism design
  - B4: mapping science
  - B5: platform, data and ethics
  - B6: agents and ethics
  - B7: Girard, hyperstition and the state machine
  - B8: tokens, markets and the agent registry
  - B9: Vervaeke, Landry, the Society Library, and transcripts
- `BIBLIOGRAPHY.md`, `VERIFICATION.md`: sources and the fact-check log.

## Related repos (prior work)
- `omniharmonic/antidebate-live`: Topology Live. Its ontology is the content core of the data model.
- `omniharmonic/auto-ontography-archive`: Ontography. The `claude/realtime-debate-mapping-3u53xl` branch holds the live-mapping docs.
- `omniharmonic/dialecticalclaims`
- `omniharmonic/dialecticaltopology`

## Also in Parachute
The full record lives under `vault/research/dialogos-arena/` (PROJECT index, synthesis, design memo, briefs, seed notes, data model, local compute).
