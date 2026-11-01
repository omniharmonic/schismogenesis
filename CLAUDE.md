# Dialogos Arena: Claude Code instructions

Project owner: **Benjamin Life (@omniharmonic)**. Attribute all work to him. Never attribute it to OpenCivics or OpenCivics Labs. Benjamin is a technical non-developer acting as lead visionary, so explain decisions in plain language and keep him in the loop on anything consequential.

## What this is
Internet-native democratic infrastructure. It has three layers:
- **SEE:** a living map of US memetic clusters, built from landmark public figures' transcripts.
- **MEET:** cross-cluster dialogue: notes, steelmen, anti-debates.
- **MOVE:** a public Community-Notes-style reputation score that rewards people and agents for helping clusters understand each other.

Success is *meta-consensus*: clusters able to describe each other in terms the described side would sign. It is not convergence.

## Repo layout right now
All handoff docs live in `docs/` (start with `docs/00-README.md`); seed data in `seed/`. The code follows the layout in `docs/design-spine/SPINE.md` §3 (packages/, services/, apps/, contracts/, evals/, infra/). See `docs/adr/ADR-029` and `ADR-030` for where it differs from the docs. The repo/project name is **schismogenesis**; the product name in the docs is **Dialogos Arena**.

## Read first (in this order)
1. `docs/01-BUILD-SPEC-v1-SLICE-1.md`: **the authoritative spec for what to build now.**
2. `docs/02-DECISIONS-LOG.md`: the latest decisions.
3. `docs/design-spine/SPINE.md`: the canonical names, phases (P0–P7), jobs (S1–S14), interfaces and non-negotiables; §10 holds the adopted extensions (tables, fields, enums, CLI, backends, leaderboard safeguards).
4. `docs/10-OPEN-DECISIONS.md`: every decision still waiting on Benjamin (OD-01 … OD-35), with the default to use until he decides.
5. `docs/07-PRD.md`: what to build and why: features, acceptance criteria, safety tests, launch criteria.
6. `docs/08-TECHNICAL-ARCHITECTURE.md`: how to build it: schema, pipeline, scorer, API, web, infrastructure. Its appendix `docs/08a-APPENDIX-DDL-and-SCORER.md` holds the full DDL and scorer code.
7. `docs/09-IMPLEMENTATION-PLAN.md`: in what order: phases, tasks, gates, the build-swarm operating model, runbooks.
8. `seed/SLICE-1-LANDMARKS.md` / `.json`: the Slice 1 inputs.

Background: `docs/03-DESIGN-MEMO-2026-10-30.md`, `docs/05-DATA-MODEL-and-ENCOUNTER-PLAN.md`, `docs/06-LOCAL-COMPUTE-and-OPERATIONS.md`, `docs/04-RESEARCH-SYNTHESIS.md`, `docs/research/`. `docs/design-spine/REVIEW-NOTES.md` lists the 2026-10-31 consistency fixes.

**Order of precedence when docs conflict:** spec (`01`) > decisions log (`02`) > spine (`docs/design-spine/SPINE.md`) > PRD / architecture / plan (`07`, `08` + `08a`, `09`) > design memo (`03`) > data model / local compute (`05`, `06`) > synthesis (`04`) > `docs/research/`. Where the spine is silent, names follow the Architecture's schema. Flag a conflict instead of silently choosing.

## Build order for Slice 1 (from spec §10)
1. **Repo skeleton:**
   - Python 3.12;
   - Postgres + pgvector (docker compose);
   - a Postgres-backed job queue (Procrastinate);
   - schema and migrations from the data model doc.
   Every derived record carries `model_version`, `prompt_version` and provenance.
2. **Seed loader:** import `seed/SEED-v4.json` and mark Slice 1 landmarks from `SLICE-1-LANDMARKS.json`. Keep curated niches separate from data-derived clusters, linked by a crosswalk table.
3. **Discovery crawl** (no GPU): for each landmark, list their own-show episodes (RSS / YouTube channel) and search for their guest appearances. Resolve names to `landmark_id`s with confidence scores, and build the person × episode graph. Never enumerate person pairs. **Search priority encounter PE-01 first** (e/acc × d/acc — any recorded Beff Jezos × Vitalik Buterin conversation; see `seed/SLICE-1-LANDMARKS.json` `priority_encounters` and D-31.9).
4. **Transcript fetch** (no GPU): YouTube captions first, then publisher transcripts. Polite rate limits with backoff. Store full transcripts privately; publish only propositions with short quote anchors and timestamped links.
5. **Gold extraction with Claude** on a small sample: claims → exact quote anchor (checked in code) → neutral proposition → layer tag → stance → relations. This becomes the gold set.
6. **Reputation scoring prototype:** adapt the open-source Community Notes matrix-factorization scorer, using the map's clusters as the viewpoint dimension. Include fidelity and portability signals, writer and rater reputation, and agents on a separate leaderboard. Agents never ratify.
7. **When the GB10 box arrives** (about late Nov 2026): run the local extraction (vLLM ≥ 0.12, constrained JSON via the `structured_outputs` request field; the old `guided_json` was removed in v0.12) and the bake-off against the gold set.

## Engineering rules
- **The pipeline is deterministic code.** LLMs do narrow, schema-constrained steps. Code gates check them: exact or fuzzy quote matching, then an NLI entailment check. Unsupported claims are discarded.
- **Idempotent, re-runnable stages** with an append-only event log, so re-extraction with better models is cheap.
- **No paid APIs or cloud spend without asking Benjamin first.** The budget is near zero; the local box and the Claude subscription are the compute plan.
- **Ask before anything outward-facing:** posting, contacting landmarks, publishing, or deploying a public site.
- **Privacy and red lines** (synthesis §11, decisions log):
  - Public figures are placed only from their public output, with a dispute affordance.
  - No inference about private individuals who haven't opted in.
  - No minors.
  - Never store content from Benjamin's private vaults in the dataset.
  - Respect the 15 flagged landmarks pending his review: keep them out of anything public.
- **Platform terms:** YouTube caption fetching is a known terms-of-service gray area. Pace it, log it, and never redistribute full transcripts. Follow X automation rules for any agent work.
- **Git:** use the `omniharmonic` GitHub account (`gh auth switch --user omniharmonic` if needed; repo `omniharmonic/schismogenesis`, private). Commit in small, descriptive steps.

## Knowledge base
Benjamin's Parachute vault holds the full research record under `vault/research/dialogos-arena/` (32+ notes). It is the long-term home for reports: write human-readable summaries back there, never raw data.
