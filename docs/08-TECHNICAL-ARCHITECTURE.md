# Dialogos Arena: Technical Architecture

*Author of record: Benjamin Life (@omniharmonic) · 2026-10-31 · Document 08 of the handoff package*

**Audience.** The Claude Code build swarm that implements Dialogos Arena, and Benjamin, who approves every phase gate. This document says *how* the system is built: containers, schemas, algorithms, job contracts and interfaces. The PRD says *what* and *why*. The Implementation Plan says *in what order*.

**Precedence.** `01-BUILD-SPEC-v1-SLICE-1.md` > `02-DECISIONS-LOG.md` > `design-spine/SPINE.md` > `07-PRD` / `08-TECHNICAL-ARCHITECTURE` (this doc, with its appendix `08a`) / `09-IMPLEMENTATION-PLAN` > `03-DESIGN-MEMO` > `05-DATA-MODEL…` / `06-LOCAL-COMPUTE…` > `04-RESEARCH-SYNTHESIS` > `research/`. Pending decisions are tracked once, as OD-01…OD-34, in `10-OPEN-DECISIONS.md`. Every name in this document (packages, jobs S1–S14, entities, phases P0–P7, the provenance contract, `LLMClient`) is taken from the spine. Anything the spine does not define is listed in **Spine extensions** at the end.

**Appendix.** The full Postgres DDL (§3.3) and the full scorer implementation and simulation test (§4.12) live in `08a-APPENDIX-DDL-and-SCORER.md`. This document keeps a summary and the key excerpts.

**Conventions.**
- Code samples are runnable-quality. They show the real library calls, but they omit logging boilerplate and some imports. Where a third-party API detail could not be checked against a primary source this session, it is marked **UNVERIFIED**.
- Thresholds are **initial values** to be calibrated in P2/P3 against gold data. Each lives in `arena_core.config` and is never hard-coded.
- "Box" means Benjamin's GB10-class 128 GB Blackwell machine (arrives about late November 2026). "Laptop/cloud-dev" means any machine without the box's GPU.

**Conflicts flagged (not silently resolved).**
1. Synthesis §11.2 red line 19 says "no public leaderboards of integration or bridging". The build spec (§8) and D-31.1 require public reputation profiles and leaderboards. The spec wins, with the leaderboard safeguards in SPINE §10 (people and agents on separate boards; per-cluster-pair default view; seasonal with decay; only the top 50 numbered; opt-in handles; ranked by reputation only, never a "bridging rank" of clusters or a developmental ranking of people, so red line 15 still holds). Benjamin's confirmation is open decision **OD-09**.
2. The spine originally said vLLM serves "with `guided_json`". In vLLM v0.12 the `guided_*` request fields were removed in favour of `structured_outputs` (06 §4.2). The `vllm` backend sends only `structured_outputs` and images are pinned at vLLM ≥ 0.12; there is no `guided_json` fallback (§5.2). SPINE §6 is corrected to match.
3. Doc 05 recommends Neon for Postgres. The spine and 06 put Postgres on the box (cloud-dev uses local Docker). Neon is not used.
4. Topology Live's `Stance.attitude` has five values. The spine's stance value has four (`affirm`, `reject`, `conditional`, `steelman_only`). Both are stored, with a fixed mapping (§3.4); `suspends` creates no stance row. The PRD and Plan use only the four spine values.

---

## 1. System overview

### 1.1 Context

```mermaid
flowchart LR
  subgraph Sources["Public sources (read-only)"]
    YT[YouTube Data API v3<br/>+ public caption tracks]
    PI[Podcast Index API]
    RSS[Podcast RSS / Substack feeds]
    IT[Apple iTunes Search]
    WD[Wikidata]
  end
  subgraph People
    B[Benjamin<br/>approves gates, publishing]
    U[Users<br/>react, write, rate]
    L[Landmarks<br/>dispute / annotate]
    OP[Agent operators<br/>register arena agents]
  end
  subgraph Arena["Dialogos Arena"]
    BOX[Box: pipeline, DB, API, models]
    STATIC[Static host: snapshot bundles + web app]
  end
  CC[Claude Code subagents<br/>gold labels, audits, battery]
  TG[Telegram + Parachute<br/>operator reports]

  Sources -->|metadata, captions, audio| BOX
  BOX -->|approved static bundle| STATIC
  U --> STATIC
  STATIC -->|writes: reactions, contributions, ratings| BOX
  L -->|disputes| BOX
  OP -->|agent registry, actions| BOX
  BOX <-->|evals/queue ↔ evals/results| CC
  BOX -->|ops reports| TG
  B -->|approvals| BOX
```

### 1.2 Containers

```mermaid
flowchart TB
  subgraph box["Box profile (docker compose --profile box)"]
    PG[(Postgres 16 + pgvector<br/>arena DB + Procrastinate tables)]
    MINIO[(MinIO<br/>private: transcripts, words, voiceprints)]
    API[services/api<br/>FastAPI]
    W1[services/worker: cpu queues<br/>discover, fetch, extract-cpu, map, reputation]
    W2[services/worker: gpu queues<br/>asr, nli, embed]
    VLLM[vLLM<br/>extractor / critic / embedder]
    NEMO[NeMo + pyannote container<br/>Parakeet, diarization, TitaNet]
    OPA[services/operator<br/>Hermes operator agent]
    PROM[Prometheus + Grafana + Loki]
  end
  subgraph host["Static host (Vercel)"]
    WEB[apps/web Next.js]
    BUNDLE[snapshot bundles<br/>JSON, immutable]
  end
  QUEUE[[evals/queue + evals/results<br/>file queue]]

  API --> PG
  W1 --> PG
  W2 --> PG
  W1 --> MINIO
  W2 --> MINIO
  W1 -->|OpenAI-compatible HTTP| VLLM
  W2 --> NEMO
  W1 --> QUEUE
  OPA -->|read-only role + /ops action API| API
  PROM --> API & W1 & W2 & VLLM & PG
  W1 -->|S13 publish, approved| BUNDLE
  WEB -->|fetch| BUNDLE
  WEB -->|writes over Tailscale Funnel / tunnel| API
```

**Process boundaries.**
- **One Postgres.** Arena tables, the append-only `event_log` and Procrastinate's queue tables all live in it. There is no Redis or second database.
- **Workers are split by queue, not by code.** A worker started with `--queues=asr,nli,embed` gets the GPU-bound tasks. Both worker types import the same packages.
- **The API is the only writer for human data** (reactions, contributions, ratings, flags). Workers are the only writers for derived data. The operator agent writes nothing except through `/ops` actions.
- **The public never touches the box directly for reads.** Reads come from static bundles. Writes (reactions, notes, ratings) go to the API through a narrow, rate-limited ingress (Cloudflare Tunnel or Tailscale Funnel). The choice is open decision **OD-10** (the same item as PRD OQ-10 and Plan PD-11); ADR-014 records the outcome. Until P5 the ingress is private (Tailscale only; beta allow-list from P5).

### 1.3 Environments

| Profile | Where | Runs | LLM backend | ASR | Phases |
|---|---|---|---|---|---|
| `cloud-dev` (laptop profile) | Claude Code cloud sessions, Benjamin's MacBook; the long-running crawl and caption fetch run on the pre-box ingest host (Benjamin's home Mac Mini, an unverified assumption pending **OD-11**) | postgres, minio, api, worker (cpu queues), web | `claude_code_batch` (gold, prompt design); `openai_compat` → llama.cpp/Ollama for smoke tests | none (captions and publisher transcripts only); `asr_episode` jobs stay queued | P0–P3 |
| `box` | GB10 box, DGX OS | everything in `cloud-dev` + vllm, nemo, gpu worker, operator, observability | `vllm` (bulk), `claude_code_batch` (gold, 2% audit, battery) | Parakeet TDT 0.6B v3 + pyannote community-1 | P4–P7 |
| `static` | Vercel (pending **OD-10**) | `apps/web` build + snapshot bundles | — | — | P5+ (in P3 bundles stay local; any password-protected preview deploy is outward-facing and needs Benjamin's approval, Plan H3) |
| `ci` | GitHub Actions | postgres service container, unit + integration tests, contract drift check | `fake` backend (fixtures) | — | all |

Configuration is one Pydantic `Settings` object (`arena_core.config`) read from env vars with the prefix `ARENA_`. Profiles change values, never code paths, except for the two capability flags `ARENA_GPU=0|1` and `ARENA_LLM_BACKEND`.

### 1.4 End-to-end data flow

```mermaid
sequenceDiagram
  autonumber
  participant Seed as seed loader
  participant S1 as S1 discover_landmark
  participant S2 as S2 resolve_entities
  participant S3 as S3 select_episodes
  participant S4 as S4 fetch_transcript / S5 asr_episode
  participant X as S6–S10 extract
  participant M as S11 build_snapshot
  participant R as S12 score_reputation
  participant P as S13 publish_snapshot
  participant Web as web app
  Seed->>S1: niches, landmarks (slice flag)
  S1->>S2: channels, episodes, candidate appearances
  S2->>S3: appearances with landmark_id + confidence
  S3->>S4: selected episodes (coverage + baseline)
  S4->>X: transcript → segments
  X->>X: chunks → claims → anchored + NLI → propositions + stances → relations + layers
  X->>M: stance matrix (landmarks × propositions)
  Web->>M: reactions (via API)
  M->>R: clusters, memberships, crosswalk
  Web->>R: contributions, ratings (via API)
  R->>M: ratification, reputation, U matrix
  M->>P: snapshot
  P->>Web: static JSON bundle (after approval)
```

A claim's journey, concretely: an episode of a landmark's podcast (S1) gets a caption transcript (S4). The transcript is cut into segments, then chunks (S6). The extractor proposes "Speaker says AI labs should pause frontier training", with the quote "I think we should just stop training bigger models" (S7). Code finds that quote inside segment 412 at characters 18–61 (S8 anchor). DeBERTa says the quote entails "Frontier AI training should be paused" at 0.93 (S8 NLI). The claim maps to existing proposition P-0381 (S9), with stance `affirm`, strength `leaning` (hedge "I think"), source `stated`. The weekly snapshot (S11) uses the stance in the landmark × proposition matrix. If the proposition is selected as a statement, users react to it, and the reactions place them in clusters.

---

## 2. Repository layout and dependency rules

### 2.1 Layout and responsibilities

```
dialogos-arena/
  CLAUDE.md                  # swarm rules (from handoff CLAUDE.md, plus this doc's §2.2 rules)
  docs/                      # 00–09, research/, adr/ (ADR-001… from §13)
  seed/                      # SEED-v4.json, SLICE-1-LANDMARKS.json, briefs (read-only inputs)
  contracts/                 # *.schema.json generated from Pydantic; CI fails on drift
  packages/                  # uv workspace members
    arena_core/              # config, db, models, ontology, provenance, event log, storage
    arena_ingest/            # S1–S5
    arena_extract/           # S6–S10
    arena_llm/               # LLMClient + backends
    arena_map/               # S11, S13, placement, lineage, live questions
    arena_reputation/        # S12 scorer, fidelity/portability, U matrix
    arena_agents/            # P6 registry, charter hooks, directional-shift audit
    arena_market/            # P6 strategies, forecasts, randomization, S14
  services/
    api/                     # FastAPI app: public read/write endpoints, auth, /ops actions
    worker/                  # Procrastinate app, task registrations, schedules
    operator/                # Hermes config, skills, read-only tools (P4)
  apps/web/                  # Next.js 15 App Router, TS, Tailwind
  evals/
    gold/                    # versioned gold labels (gold-v0, gold-v1…)
    harness/                 # metrics, bake-off runner, reports
    queue/  results/         # claude_code_batch file queue (gitignored except README)
  infra/
    docker-compose.yml       # profiles: cloud-dev, box
    vllm/                    # per-model serve configs, pinned images
    grafana/ prometheus/     # dashboards and scrape configs
  scripts/                   # the `arena` CLI (typer; uv workspace member `arena_cli`): arena seed load, arena run S1 …, arena gold …, arena contracts export
```

| Package | Owns | Must not |
|---|---|---|
| `arena_core` | `Settings`; SQLAlchemy engine/session; ORM tables; Pydantic models incl. `arena_core.ontology` (the Topology Live port); `Provenance`; `event_log` writer; `ObjectStore` (MinIO/local); idempotency helper `stage_once()`; hashing; ids | import any other arena package |
| `arena_llm` | `LLMClient` protocol, backends, prompt registry (`prompts/<prompt_id>/<version>.md`), `llm_call` logging | touch content tables (it writes only `llm_call`) |
| `arena_ingest` | S1–S5; source adapters (YouTube, Podcast Index, RSS, iTunes, Wikidata); entity resolver; coverage selector; transcript adapters; ASR/diarization runners | call extraction code |
| `arena_extract` | S6–S10; chunker; extraction prompts and schemas; quote locator; NLI gate; validators (port of TL `validate.ts`); normalizer; relation and layer linker | read reactions or ratings |
| `arena_map` | S11, S13; stance matrix; clustering; crosswalk; placement; axes; lineage; live questions; bundle writer | write ratings or reputation |
| `arena_reputation` | S12; the scorer; fidelity/portability; ratification; writer impact; rater helpfulness; U matrix; coordinated-rater detection | write clusters |
| `arena_agents` | registry, operator binding, charter enforcement hooks, directional-shift audit, agent-free re-fit trigger | ratify or rate (enforced in SQL too) |
| `arena_market` | strategies, sealed forecasts, randomized assignment, S14 | read individual reactions (only aggregates from the scorer) |

### 2.2 Dependency rules

```
arena_core  ←  arena_llm  ←  arena_ingest
                         ←  arena_extract
arena_core  ←  arena_map  ←  arena_reputation  ←  arena_agents  ←  arena_market
services/*  →  any package          apps/web  →  contracts/ only (generated TS)
```

- Packages depend only "leftward" in that graph. `arena_reputation` may read `arena_map` outputs (clusters, memberships) through `arena_core` tables, and may import `arena_map.placement` types. `arena_map` never imports `arena_reputation`: the U matrix is written by S12 into `understanding_cell`, and S11/S13 read the table.
- No package imports from `services/`.
- `apps/web` never imports Python-derived code except generated types in `contracts/ts/`.
- Enforced in CI by `import-linter`:

```toml
# pyproject.toml (workspace root)
[tool.importlinter]
root_packages = ["arena_core","arena_llm","arena_ingest","arena_extract","arena_map",
                 "arena_reputation","arena_agents","arena_market"]

[[tool.importlinter.contracts]]
name = "core is a leaf"
type = "forbidden"
source_modules = ["arena_core"]
forbidden_modules = ["arena_llm","arena_ingest","arena_extract","arena_map",
                     "arena_reputation","arena_agents","arena_market"]

[[tool.importlinter.contracts]]
name = "layered pipeline"
type = "layers"
layers = ["arena_market","arena_agents","arena_reputation","arena_map",
          "arena_extract | arena_ingest","arena_llm","arena_core"]

[[tool.importlinter.contracts]]
name = "map does not depend on reputation"
type = "forbidden"
source_modules = ["arena_map"]
forbidden_modules = ["arena_reputation","arena_agents","arena_market"]
```

**uv workspace.** The root `pyproject.toml` declares `[tool.uv.workspace] members = ["packages/*", "services/*", "scripts"]` (`scripts` is the `arena_cli` member that provides the `arena` console script; Plan §4.0). Heavy GPU dependencies (`nemo_toolkit`, `pyannote.audio`, `torch`) are an optional extra `arena_ingest[asr]` installed only inside the NGC container image. `cloud-dev` never installs them.

---

## 3. Data model

### 3.1 Principles

1. **Spine vocabulary is the table vocabulary.** Table names are the spine's terms in snake_case: `niche`, `landmark`, `episode`, `claim`, `proposition`, `stance`, and so on. Topology Live terms survive as column values (`speech_act`, `tl_attitude`, `tl_relation_type`, `item_status`).
2. **Curated vs derived.** Seed tables (`niche`, `landmark`, `landmark_niche`) are loaded from `seed/` and never changed by data. Derived tables carry the provenance contract.
3. **Append-only truth, projected tables.** Every create, merge or status change writes an `event_log` row in the same transaction. Derived tables can be rebuilt from inputs plus events. Rows are superseded, never updated in place for content (status columns are the exception, and their changes are events).
4. **Versioned re-runs.** A re-run with a new model or prompt writes new rows with a new `run_id`. `superseded_by` links old to new. Readers select `WHERE superseded_by IS NULL`.
5. **Private vs public.** Full transcripts, word timings and voiceprints live in MinIO (`transcript.storage_ref`). Postgres holds segment text (needed for anchoring) in a schema `private` that the public API role cannot read. Only `claim.quote_public` (≤ 1 sentence, ≤ 280 chars) is ever exported.

### 3.2 Provenance contract as columns

Every derived table has these columns (spine §5):

| Column | Type | Meaning |
|---|---|---|
| `run_id` | `uuid` FK → `pipeline_run` | The run that produced the row |
| `stage` | `text` | `S1`…`S14` |
| `model_name`, `model_version` | `text` | e.g. `qwen3.6-35b-a3b`, `nvfp4@sha256:…`; `code` for deterministic stages |
| `prompt_id`, `prompt_version` | `text` | `null` for non-LLM stages |
| `created_at` | `timestamptz` | |
| `inputs_hash` | `bytea` | sha256 of the canonical JSON of all inputs (see §4.0) |
| `source` | `stance_source` | where relevant: `stated`, `implied_by_act`, `inferred` |
| `agent_provenance` | `boolean` | true if any input was touched by an arena agent |

### 3.3 Postgres DDL

The complete DDL (the target of Alembic revision `0001_initial`, 786 lines, 41 tables plus enums, the `rating_guard` trigger and roles) is in **[`08a-APPENDIX-DDL-and-SCORER.md` §A1](08a-APPENDIX-DDL-and-SCORER.md#a1-postgres-ddl-full)**. It is written as plain SQL so the swarm can review it in one place; Alembic migrations execute it in ordered chunks (§3.7). The appendix also holds three small tables added in the 2026-10-31 consistency review at the Plan's request (`api_call` + `quota_ledger` view, `pipeline_release`, `incident`; §A1.1).

**Tables by group.**

| Group | Tables |
|---|---|
| 0. Extensions, schemas, enums | extensions (`vector`, `pg_trgm`, `citext`), schema `private`, all enums (excerpt below) |
| 1. Runs and the event log | `pipeline_run`, `event_log`, `stage_item`, `llm_call` |
| 2. Seed: niche, person, landmark, landmark_niche | `niche`, `person`, `landmark`, `landmark_niche` |
| 3. Media: channel, content_group, episode, appearance, encounter | `channel`, `content_group`, `episode`, `appearance`, `encounter` |
| 4. Transcripts: transcript, segment (private), chunk | `transcript`, `private.segment`, `chunk` |
| 5. Content: claim, proposition, stance, proposition_relation | `proposition`, `claim`, `stance`, `proposition_relation` |
| 6. People in the product: app_user, statement, reaction | `app_user`, `statement`, `reaction` |
| 7. Map: cluster_snapshot, cluster, cluster_membership, crosswalk, lineage | `cluster_snapshot`, `cluster`, `cluster_membership`, `niche_cluster_crosswalk`, `cluster_lineage` |
| 8. Gradient: contribution, rating, scores, reputation, U matrix | `contribution`, `rating`, `contribution_score`, `reputation_score`, `understanding_cell` |
| 9. Live questions | `live_question`, `live_question_proposition` |
| 10. Agents and market (P6; created in P0 so FKs are stable) | `agent`, `agent_action`, `strategy`, `strategy_assignment`, `forecast` |
| 11. Governance: flag (dispute) | `flag` |
| 12. Roles | roles only: `arena_api`, `arena_worker`, `arena_operator_ro` |

**Key excerpt 1: enums** (the closed vocabularies every other doc must use).

```sql
CREATE TYPE stance_source      AS ENUM ('stated','implied_by_act','inferred');
CREATE TYPE stance_value       AS ENUM ('affirm','reject','conditional','steelman_only');
CREATE TYPE tl_attitude        AS ENUM ('accepts','rejects','suspends','accepts_conditionally','accepts_for_argument');
CREATE TYPE stance_strength    AS ENUM ('tentative','leaning','confident','certain');
CREATE TYPE layer              AS ENUM ('ontological','epistemic','axiological','empirical','praxis');
CREATE TYPE relation_type      AS ENUM ('supports','contradicts','depends_on','reframes');
CREATE TYPE item_status        AS ENUM ('live_provisional','operator_approved','released','canonical',
                                        'participant_confirmed','participant_contested','rejected','retracted');
CREATE TYPE appearance_role    AS ENUM ('host','co_host','guest','panelist','moderator','debater','clip_subject');
CREATE TYPE mention_type       AS ENUM ('present','discussed_only','clip_only');
CREATE TYPE reaction_vote      AS ENUM ('agree','disagree','pass');
CREATE TYPE contribution_kind  AS ENUM ('note','steelman','synthesis');
CREATE TYPE synthesis_subtype  AS ENUM ('bridge_proposal','better_question','clean_disagreement');
CREATE TYPE helpfulness        AS ENUM ('helpful','somewhat','not_helpful');
CREATE TYPE snapshot_horizon   AS ENUM ('daily','weekly','monthly');
CREATE TYPE actor_kind         AS ENUM ('person','agent');
CREATE TYPE run_status         AS ENUM ('running','succeeded','failed','partial','cancelled');
```

**Key excerpt 2: `contribution`** (status values are the canonical contribution statuses; the PRD's status chips are display labels over them, see SPINE §10).

```sql
CREATE TABLE contribution (
  contribution_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind            contribution_kind NOT NULL,
  synthesis_subtype synthesis_subtype,
  author_user_id  uuid NOT NULL REFERENCES app_user(user_id),
  author_actor_kind actor_kind NOT NULL,                       -- denormalized for agent leaderboard split
  author_snapshot_id uuid NOT NULL REFERENCES cluster_snapshot(snapshot_id),
  author_cluster_id uuid NOT NULL REFERENCES cluster(cluster_id),   -- agents are not placed: for agent authors this holds the
                                                                   -- declared audience cluster (PRD-AGT-03 AC4)
  target_cluster_id uuid NOT NULL REFERENCES cluster(cluster_id),        -- B (described) for note/steelman
  second_cluster_id uuid REFERENCES cluster(cluster_id),                 -- synthesis: the other parent
  body            text NOT NULL CHECK (length(body) BETWEEN 40 AND 2000),
  cited_claim_ids uuid[] NOT NULL DEFAULT '{}',
  live_question_id uuid,
  parent_contribution_id uuid REFERENCES contribution(contribution_id),  -- revision / re-target after split
  agent_drafted   boolean NOT NULL DEFAULT false,                        -- a person used an agent to draft
  judgment_flag   boolean NOT NULL DEFAULT false,                        -- describe-not-judge pre-submit check fired (PRD-MEET-01 AC3)
  agent_id        uuid,                                                  -- set when author is an agent
  status          text NOT NULL DEFAULT 'needs_ratings'
     CHECK (status IN ('needs_ratings','ratified','helpful','ratified_helpful','not_helpful','split_detected','withdrawn','removed')),
  created_at      timestamptz NOT NULL DEFAULT now(),
  CHECK (kind <> 'synthesis' OR (second_cluster_id IS NOT NULL AND synthesis_subtype IS NOT NULL)),
  CHECK (kind = 'synthesis' OR author_cluster_id <> target_cluster_id)
);
```

**Key excerpt 3: the `rating_guard` trigger** (agents never rate; fidelity only from the described cluster; raters must be reaction-placed).

```sql
CREATE FUNCTION rating_guard() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE k actor_kind; t smallint; author uuid; target uuid; elig boolean;
BEGIN
  SELECT kind, personhood_tier INTO k, t FROM app_user WHERE user_id = NEW.rater_user_id;
  IF k <> 'person' THEN RAISE EXCEPTION 'agents never rate (rater %)', NEW.rater_user_id; END IF;
  IF t < 2 THEN RAISE EXCEPTION 'personhood tier 2 required to rate'; END IF;
  SELECT author_user_id, target_cluster_id INTO author, target FROM contribution WHERE contribution_id = NEW.contribution_id;
  IF author = NEW.rater_user_id THEN RAISE EXCEPTION 'no self-rating'; END IF;
  SELECT eligible_to_ratify INTO elig FROM cluster_membership
   WHERE snapshot_id = NEW.rater_snapshot_id AND subject_type = 'user'
     AND subject_id = NEW.rater_user_id::text AND cluster_id = NEW.rater_cluster_id AND is_primary;
  IF NOT coalesce(elig, false) THEN RAISE EXCEPTION 'rater not reaction-placed in snapshot'; END IF;
  IF NEW.fidelity IS NOT NULL AND NEW.rater_cluster_id <> target THEN
    RAISE EXCEPTION 'fidelity votes only from the described cluster'; END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER rating_guard BEFORE INSERT OR UPDATE ON rating FOR EACH ROW EXECUTE FUNCTION rating_guard();
```

**Operational views** for the operator agent live in a schema `ops` (queue depth, failure rates, pass rates per model version, open flags past SLA). They expose counts and ids only, never segment text or user emails.

### 3.4 Topology Live → spine mappings

| TL field | Spine field | Mapping |
|---|---|---|
| `Attitude` | `stance.value` | `accepts`→`affirm`; `rejects`→`reject`; `accepts_conditionally`→`conditional`; `accepts_for_argument`→`steelman_only`; `suspends`→ **no stance row** (claim kept, `gate_status='accepted'`, used only for live-question labelling) |
| `SpeechAct ∈ {attribute, steelman_report, nonliteral}` | — | Never commits the speaker. `steelman_report` yields `steelman_only` with weight 0 in the stance matrix. The others yield no stance. |
| `Stratum` | `layer` | `ontology`→`ontological`, `epistemology`→`epistemic`, `axiology`→`axiological`, `empirical`→`empirical`, `praxis`→`praxis` |
| `RelationType` | `relation_type` | `supports`→`supports`; `rebuts`,`undercuts`,`undermines`→`contradicts`; `presupposes`→`depends_on`; `qualifies`,`defines`,`exemplifies`→`reframes`; `equivalent`→ merge in S9 (not a relation); `agrees`,`concedes`,`answers`,`evades`→ episode-scoped dialogue relations stored with `scope='episode'` and mapped to `supports`/`contradicts`/`reframes` for event maps only |
| `Strength` | `strength_num` | `tentative` .25, `leaning` .5, `confident` .75, `certain` 1.0 |
| `Utterance` | `private.segment` | same shape; `words[]` kept in MinIO |
| `Span` + `Adu` | `claim` anchor columns | one span per claim in v1 (multi-span ADUs split into one claim per span, linked by `chunk_id` + `speech_act`) |

### 3.5 Entity–relationship diagram

```mermaid
erDiagram
  NICHE ||--o{ LANDMARK_NICHE : has
  LANDMARK ||--o{ LANDMARK_NICHE : plays
  PERSON ||--o| LANDMARK : "is (panel member)"
  PERSON ||--o{ CHANNEL : owns
  CHANNEL ||--o{ EPISODE : publishes
  CONTENT_GROUP ||--|{ EPISODE : "same conversation"
  EPISODE ||--o{ APPEARANCE : features
  PERSON ||--o{ APPEARANCE : appears
  CONTENT_GROUP ||--o{ ENCOUNTER : yields
  EPISODE ||--o{ TRANSCRIPT : versions
  TRANSCRIPT ||--|{ SEGMENT : utterances
  TRANSCRIPT ||--|{ CHUNK : windows
  CHUNK ||--o{ CLAIM : proposes
  SEGMENT ||--o{ CLAIM : anchors
  CLAIM }o--o| PROPOSITION : "maps to"
  PERSON ||--o{ STANCE : holds
  PROPOSITION ||--o{ STANCE : on
  PROPOSITION ||--o{ PROPOSITION_RELATION : "from/to"
  PROPOSITION ||--o{ STATEMENT : "shown as"
  APP_USER ||--o{ REACTION : reacts
  STATEMENT ||--o{ REACTION : receives
  CLUSTER_SNAPSHOT ||--|{ CLUSTER : contains
  CLUSTER ||--o{ CLUSTER_MEMBERSHIP : members
  NICHE ||--o{ NICHE_CLUSTER_CROSSWALK : maps
  CLUSTER ||--o{ NICHE_CLUSTER_CROSSWALK : maps
  APP_USER ||--o{ CONTRIBUTION : writes
  CLUSTER ||--o{ CONTRIBUTION : "author / target"
  CONTRIBUTION ||--o{ RATING : rated
  APP_USER ||--o{ RATING : rates
  CONTRIBUTION ||--o{ CONTRIBUTION_SCORE : scored
  APP_USER ||--o{ REPUTATION_SCORE : earns
  CLUSTER ||--o{ UNDERSTANDING_CELL : "A or B"
  LIVE_QUESTION ||--o{ LIVE_QUESTION : parent
  LIVE_QUESTION ||--o{ LIVE_QUESTION_PROPOSITION : answers
  APP_USER ||--o| AGENT : "agent account"
  APP_USER ||--o{ AGENT : operates
  AGENT ||--o{ AGENT_ACTION : performs
  STRATEGY ||--o{ STRATEGY_ASSIGNMENT : assigned
  APP_USER ||--o{ FORECAST : forecasts
  PIPELINE_RUN ||--o{ EVENT_LOG : emits
  APP_USER ||--o{ FLAG : raises
```

### 3.6 Pydantic models (ontology port)

`arena_core.ontology` is a faithful port of `antidebate-live/packages/ontology/src/{enums,entities}.ts`. Enums are `StrEnum`s with identical values; Zod `.default()` becomes a Pydantic default; Zod `.min()` becomes `Field(min_length=…)`. The validators in `validate.ts` and the lexicons in `lexicons.ts` are ported to `arena_extract.validators` with the same tests (`validate.test.ts` → `test_validators.py`, same cases).

```python
# packages/arena_core/src/arena_core/ontology/enums.py
from enum import StrEnum

class SpeechAct(StrEnum):
    assert_ = "assert"; concede = "concede"; retract = "retract"; question = "question"
    answer = "answer"; hypothesize = "hypothesize"; steelman_report = "steelman_report"
    attribute = "attribute"; challenge = "challenge"; commit_conditional = "commit_conditional"
    meta = "meta"; rhetorical_question = "rhetorical_question"; nonliteral = "nonliteral"

COMMITTING_ACTS = {SpeechAct.assert_, SpeechAct.rhetorical_question, SpeechAct.concede,
                   SpeechAct.retract, SpeechAct.commit_conditional, SpeechAct.answer}
NON_COMMITTING_ACTS = {SpeechAct.question, SpeechAct.challenge, SpeechAct.meta}
NON_ATTRIBUTABLE_ACTS = {SpeechAct.attribute, SpeechAct.steelman_report, SpeechAct.nonliteral}

class PropositionType(StrEnum):
    empirical = "empirical"; causal = "causal"; predictive = "predictive"
    counterfactual = "counterfactual"; normative = "normative"; prescriptive = "prescriptive"
    definitional = "definitional"; conceptual = "conceptual"; modal = "modal"; meta = "meta"

class Stratum(StrEnum):           # TL vocabulary
    praxis = "praxis"; empirical = "empirical"; axiology = "axiology"
    epistemology = "epistemology"; ontology = "ontology"

class Layer(StrEnum):             # spine vocabulary
    ontological = "ontological"; epistemic = "epistemic"; axiological = "axiological"
    empirical = "empirical"; praxis = "praxis"

STRATUM_TO_LAYER = {Stratum.ontology: Layer.ontological, Stratum.epistemology: Layer.epistemic,
                    Stratum.axiology: Layer.axiological, Stratum.empirical: Layer.empirical,
                    Stratum.praxis: Layer.praxis}

class Attitude(StrEnum):
    accepts = "accepts"; rejects = "rejects"; suspends = "suspends"
    accepts_conditionally = "accepts_conditionally"; accepts_for_argument = "accepts_for_argument"

class StanceValue(StrEnum):
    affirm = "affirm"; reject = "reject"; conditional = "conditional"; steelman_only = "steelman_only"

ATTITUDE_TO_VALUE: dict[Attitude, StanceValue | None] = {
    Attitude.accepts: StanceValue.affirm, Attitude.rejects: StanceValue.reject,
    Attitude.accepts_conditionally: StanceValue.conditional,
    Attitude.accepts_for_argument: StanceValue.steelman_only, Attitude.suspends: None}

class Strength(StrEnum):
    tentative = "tentative"; leaning = "leaning"; confident = "confident"; certain = "certain"

STRENGTH_RANK = {Strength.tentative: 0, Strength.leaning: 1, Strength.confident: 2, Strength.certain: 3}
STRENGTH_NUM = {Strength.tentative: .25, Strength.leaning: .5, Strength.confident: .75, Strength.certain: 1.0}

class StanceSource(StrEnum):
    stated = "stated"; implied_by_act = "implied_by_act"; inferred = "inferred"

class Quantifier(StrEnum):
    all = "all"; most = "most"; many = "many"; some = "some"; few = "few"; none = "none"; generic = "generic"
```

```python
# packages/arena_core/src/arena_core/ontology/entities.py
from datetime import datetime
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator
from .enums import *

class Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

class Provenance(Frozen):
    run_id: UUID
    stage: Annotated[str, Field(pattern=r"^S([1-9]|1[0-4])$")]
    model_name: str
    model_version: str
    prompt_id: str | None = None
    prompt_version: str | None = None
    created_at: datetime
    inputs_hash: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    agent_provenance: bool = False

class Scope(Frozen):
    quantifier: Quantifier = Quantifier.generic
    domain: str | None = None
    time_horizon: str | None = None

class QuoteAnchor(Frozen):
    segment_id: UUID
    char_start: Annotated[int, Field(ge=0)]
    char_end: Annotated[int, Field(gt=0)]
    quote: Annotated[str, Field(min_length=1)]   # always the source substring
    match: str                                   # exact | normalized | fuzzy
    t_start_ms: int
    t_end_ms: int

    @model_validator(mode="after")
    def _range(self):
        if self.char_end <= self.char_start:
            raise ValueError("char_end must exceed char_start")
        return self

class Proposition(Frozen):
    proposition_id: UUID
    public_id: str
    canonical: Annotated[str, Field(min_length=3, max_length=400)]
    tl_type: PropositionType
    layer: Layer
    scope: Scope = Scope()
    conditions: list[str] = []
    quantities: list[dict] = []
    forecast: dict | None = None
    provenance: Provenance

class Stance(Frozen):
    person_id: str
    proposition_id: UUID
    value: StanceValue
    tl_attitude: Attitude
    strength: Strength
    credence: Annotated[float, Field(ge=0, le=1)] | None = None   # only if stated
    source: StanceSource
    claim_ids: Annotated[list[UUID], Field(min_length=1)]
    as_of: datetime
    provenance: Provenance

    @model_validator(mode="after")
    def _consistent(self):
        if ATTITUDE_TO_VALUE[self.tl_attitude] != self.value:
            raise ValueError("value must follow ATTITUDE_TO_VALUE")
        if self.credence is not None and self.source != StanceSource.stated:
            raise ValueError("credence is only recorded when stated")
        return self
```

### 3.7 Alembic migration pattern

- One Alembic environment in `arena_core/migrations`. Autogenerate is allowed for ordinary columns, but **every migration is reviewed by hand**, and anything touching enums, pgvector, triggers, rules or roles is written as explicit `op.execute()`.
- Migrations are forward-only in production. `downgrade()` exists for dev/CI only.
- Enum additions use `ALTER TYPE … ADD VALUE` in a migration with `transaction_per_migration = True` (Postgres cannot use a new enum value inside the same transaction that added it).
- Large backfills are never done in migrations. They run as `admin` pipeline runs.

```python
# packages/arena_core/src/arena_core/migrations/versions/0007_claim_anchor_score.py
"""claim: add anchor_score and nli_model; widen quote_public check"""
from alembic import op
import sqlalchemy as sa

revision = "0007_claim_anchor_score"
down_revision = "0006_live_question_axes"

def upgrade() -> None:
    op.add_column("claim", sa.Column("anchor_score", sa.REAL(), nullable=True))
    op.add_column("claim", sa.Column("nli_model", sa.Text(), nullable=True))
    op.execute("ALTER TABLE claim DROP CONSTRAINT IF EXISTS claim_quote_public_check")
    op.execute("ALTER TABLE claim ADD CONSTRAINT claim_quote_public_check "
               "CHECK (length(quote_public) <= 280) NOT VALID")
    op.execute("ALTER TABLE claim VALIDATE CONSTRAINT claim_quote_public_check")

def downgrade() -> None:
    op.drop_column("claim", "nli_model")
    op.drop_column("claim", "anchor_score")
```

```python
# migrations/env.py (excerpt): make pgvector types render in autogenerate
from pgvector.sqlalchemy import HALFVEC, Vector
def render_item(type_, obj, autogen_context):
    if type_ == "type" and isinstance(obj, (HALFVEC, Vector)):
        autogen_context.imports.add("from pgvector.sqlalchemy import HALFVEC, Vector")
        return repr(obj)
    return False
context.configure(..., render_item=render_item, transaction_per_migration=True)
```

### 3.8 Contracts: JSON Schema export and TypeScript generation

Pydantic is the single source. `arena contracts export` (implemented in `scripts/export_contracts.py`) writes one schema per public model into `contracts/public/` and LLM output schemas into `contracts/llm/`, and `json-schema-to-typescript` generates `contracts/ts/*.d.ts` for `apps/web`. The same schemas are the `schema` argument of `LLMClient.complete_json` for extraction (so Claude and local models share one contract, per 06 §4.2). CI runs the export and fails if `git diff --exit-code contracts/` is non-empty.

```python
# scripts/export_contracts.py
import json, pathlib, typer
from pydantic import TypeAdapter
from arena_core.contracts import PUBLIC_MODELS, LLM_OUTPUT_MODELS  # dict[name, type]

app = typer.Typer()

@app.command()
def main(out: pathlib.Path = pathlib.Path("contracts")) -> None:
    out.mkdir(exist_ok=True)
    for group, models in (("public", PUBLIC_MODELS), ("llm", LLM_OUTPUT_MODELS)):
        (out / group).mkdir(exist_ok=True)
        for name, model in sorted(models.items()):
            schema = TypeAdapter(model).json_schema(mode="serialization")
            schema["$id"] = f"https://dialogos-arena/contracts/{group}/{name}.schema.json"
            (out / group / f"{name}.schema.json").write_text(
                json.dumps(schema, indent=2, sort_keys=True) + "\n")

if __name__ == "__main__":
    app()
```

```jsonc
// apps/web/package.json (excerpt)
{
  "scripts": {
    "contracts": "json2ts -i '../../contracts/public/*.schema.json' -o ../../contracts/ts --unreachableDefinitions --additionalProperties false"
  },
  "devDependencies": { "json-schema-to-typescript": "^15.0.0" }
}
```

LLM output schemas are kept **flat and closed** (`additionalProperties: false`, no `$ref` cycles, enums inline) because constrained decoders (xgrammar) and Claude both handle them reliably. `arena_core.contracts.llm_schema(model)` inlines `$defs` before passing a schema to a backend.

---

## 4. Pipeline S1–S14

### 4.0 The stage framework (shared by every job)

Each stage is a pure-ish function `run(ctx, item) -> Outcome`, wrapped by a Procrastinate task (§6). The wrapper does four things:

1. **Opens a `pipeline_run`**, or reuses the parent run for fan-out.
2. **Computes `inputs_hash`.** It hashes the canonical JSON (sorted keys, UTF-8, no whitespace) of the input row ids *and their content hashes*, the stage params, `model_version` and `prompt_version`.
3. **Claims the idempotency key** `(item_type, item_id, stage, model_version, prompt_version, inputs_hash)` in `stage_item` with `INSERT … ON CONFLICT DO NOTHING`. If the row exists with `status='done'`, the task returns `skipped`. Re-running with the same inputs is free; a new model or prompt version, or changed inputs, gives a new key.
4. **Writes outputs and events in one transaction,** then marks `stage_item.status='done'`.

```python
# packages/arena_core/src/arena_core/stage.py
import hashlib, json
from contextlib import contextmanager
from dataclasses import dataclass
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session

def canonical_hash(obj) -> bytes:
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).digest()

@dataclass(frozen=True)
class StageKey:
    item_type: str; item_id: str; stage: str
    model_version: str = "code"; prompt_version: str = "-"

@dataclass
class StageContext:
    session: Session
    run_id: UUID
    stage: str
    model_name: str = "code"
    model_version: str = "code"
    prompt_id: str | None = None
    prompt_version: str | None = None

    def prov(self, inputs_hash: bytes, **extra) -> dict:
        return dict(run_id=self.run_id, stage=self.stage, model_name=self.model_name,
                    model_version=self.model_version, prompt_id=self.prompt_id,
                    prompt_version=self.prompt_version, inputs_hash=inputs_hash, **extra)

    def emit(self, type_: str, entity_type: str, entity_id: str, payload: dict,
             agent_provenance: bool = False) -> None:
        self.session.execute(text(
            "INSERT INTO event_log (type, actor_type, actor_id, entity_type, entity_id, payload, run_id, agent_provenance)"
            " VALUES (:t,'pipeline',:a,:et,:eid,CAST(:p AS jsonb),:r,:ap)"),
            dict(t=type_, a=str(self.run_id), et=entity_type, eid=entity_id,
                 p=json.dumps(payload, default=str), r=self.run_id, ap=agent_provenance))

@contextmanager
def stage_once(ctx: StageContext, key: StageKey, inputs: dict):
    """Yields inputs_hash if this (key, inputs) has not completed; yields None to skip."""
    h = canonical_hash({"inputs": inputs, "mv": key.model_version, "pv": key.prompt_version})
    row = ctx.session.execute(text("""
        INSERT INTO stage_item (item_type,item_id,stage,model_version,prompt_version,inputs_hash,run_id,status)
        VALUES (:it,:iid,:st,:mv,:pv,:h,:r,'started')
        ON CONFLICT (item_type,item_id,stage,model_version,prompt_version,inputs_hash)
        DO UPDATE SET attempts = stage_item.attempts + 1, run_id = EXCLUDED.run_id, updated_at = now()
           WHERE stage_item.status <> 'done'
        RETURNING status"""), dict(it=key.item_type, iid=key.item_id, st=key.stage,
                                   mv=key.model_version, pv=key.prompt_version, h=h, r=ctx.run_id)).first()
    if row is None:                       # already done: the WHERE clause suppressed the update
        yield None
        return
    try:
        yield h
        ctx.session.execute(text("UPDATE stage_item SET status='done', updated_at=now() WHERE item_type=:it "
                                 "AND item_id=:iid AND stage=:st AND model_version=:mv AND prompt_version=:pv "
                                 "AND inputs_hash=:h"), dict(it=key.item_type, iid=key.item_id, st=key.stage,
                                 mv=key.model_version, pv=key.prompt_version, h=h))
        ctx.session.commit()
    except Exception:
        ctx.session.rollback()
        raise
```

Stage summary (all job names canonical):

| # | Job | Item | Idempotency key `item_id` | Queue | Box-only |
|---|---|---|---|---|---|
| S1 | `discover_landmark` | landmark | `landmark_id` + window | `discover` | no |
| S2 | `resolve_entities` | episode | `episode_id` | `discover` | no |
| S3 | `select_episodes` | slice | `slice_id` + selection params | `map` | no |
| S4 | `fetch_transcript` | episode | `episode_id` + route | `fetch` | no |
| S5 | `asr_episode` | episode | `episode_id` + asr model | `asr` | **yes** |
| S6 | `chunk_transcript` | transcript | `transcript_id` | `extract_cpu` | no |
| S7 | `extract_claims` | chunk | `chunk_id` | `llm` | no |
| S8 | `anchor_and_verify` | chunk | `chunk_id` (all its claims) | `nli` | no (CPU-slow) |
| S9 | `normalize_propositions` | chunk | `chunk_id` | `llm` | no |
| S10 | `link_relations_layers` | proposition batch | sorted ids hash | `llm` | no |
| S11 | `build_snapshot` | snapshot | horizon + `as_of` | `map` | no |
| S12 | `score_reputation` | snapshot | `snapshot_id` + ratings watermark | `map` | no |
| S13 | `publish_snapshot` | snapshot | `snapshot_id` + bundle sha | `publish` | no |
| S14 | `resolve_forecasts` | window | `window_id` | `map` | no |

### 4.1 S1 `discover_landmark`

**Purpose.** For one landmark, find its channels, list own-show episodes in the backfill window (from 2024-01-01, OPEN-8), and search for guest appearances elsewhere. This is the O(N) crawl of doc 05 Part 2: never enumerate person pairs.

**Inputs → outputs.** `landmark.platforms` (free text and URLs) → `channel`, `episode`, `appearance(status='candidate')` rows with `discovered_via`.

**Algorithm.**
1. *Registry.* Resolve stable ids: YouTube `channels.list(forHandle=…)` (1 quota unit) when a handle or URL exists, `search.list` (100 units) only when not; Podcast Index `search/byterm` for the show; iTunes Search for `collectionId` and the feed URL; Wikidata for the QID and aliases.
2. *Own show.* YouTube uploads playlist via `playlistItems.list` (50 per page) + `videos.list` for durations; RSS via `feedparser` (enclosures, `podcast:person` and `podcast:transcript` tags).
3. *Guest appearances.* Podcast Index `search/byperson` (uses `podcast:person` tags and text), then iTunes episode search; YouTube `search.list` only for landmarks whose podcast results are thin (fewer than 5 hits in the window).
4. *Guest mention extraction* from titles and descriptions: rules first ("with", "ft.", "feat.", "guest:", " vs ", " x "), then a small constrained LLM call that classifies each mention as `present` / `discussed_only` / `clip_only`.

**Keys needed (obtain before P1).** Google Cloud project + YouTube Data API v3 key (`ARENA_YT_API_KEY`); Podcast Index key and secret (`ARENA_PODCASTINDEX_KEY/SECRET`, free); none for RSS, iTunes or Wikidata. Listen Notes is deferred (decision after P1; **OD-34**).

**Rate limits.** YouTube default quota 10,000 units/day: a token bucket in Postgres (`quota_ledger` view over `llm_call`-like `api_call` rows) stops S1 YouTube calls at 9,000 units/day. Podcast Index ≤ 1 req/s (the provider's limit is UNVERIFIED; we stay conservative, matching Plan §4.1). iTunes ≤ 15/min. RSS and show-notes hosts ≤ 1 req/s per host, robots.txt respected.

**Failure modes.** Quota exhausted (`403 quotaExceeded`) → task retries at next UTC midnight. Feed 404 or moved → `channel.last_crawled_at` set, `event_log: channel.unreachable`. Handle ambiguity (several candidate channels) → no auto-pick; the candidates go to the `ops.discovery_review` queue for a person to choose. An over-broad name search (common names) → all hits routed to review because `person.ambiguous_name`.

```python
# packages/arena_ingest/src/arena_ingest/sources/podcastindex.py
import hashlib, time, httpx

BASE = "https://api.podcastindex.org/api/1.0"

class PodcastIndex:
    """Podcast Index auth: X-Auth-Key, X-Auth-Date (unix seconds), Authorization = sha1(key+secret+date)."""
    def __init__(self, key: str, secret: str, ua: str = "DialogosArena/0.1 (+contact)"):
        self.key, self.secret, self.ua = key, secret, ua
        self.client = httpx.Client(timeout=30)

    def _headers(self) -> dict[str, str]:
        now = str(int(time.time()))
        auth = hashlib.sha1((self.key + self.secret + now).encode()).hexdigest()
        return {"X-Auth-Key": self.key, "X-Auth-Date": now, "Authorization": auth, "User-Agent": self.ua}

    def get(self, path: str, **params) -> dict:
        r = self.client.get(f"{BASE}/{path}", params=params, headers=self._headers())
        r.raise_for_status()
        return r.json()

    def search_by_person(self, name: str, max_: int = 100) -> list[dict]:
        return self.get("search/byperson", q=name, max=max_).get("items", [])

    def search_feeds(self, term: str) -> list[dict]:
        return self.get("search/byterm", q=term).get("feeds", [])

    def episodes_by_feed(self, feed_id: int, since: int, max_: int = 1000) -> list[dict]:
        return self.get("episodes/byfeedid", id=feed_id, since=since, max=max_).get("items", [])
```

```python
# packages/arena_ingest/src/arena_ingest/sources/rss.py
from datetime import datetime, timezone
import feedparser, httpx

def list_rss_episodes(rss_url: str, since: datetime, etag: str | None = None) -> tuple[list[dict], str | None]:
    resp = httpx.get(rss_url, headers={"If-None-Match": etag} if etag else {}, timeout=30,
                     follow_redirects=True)
    if resp.status_code == 304:
        return [], etag
    resp.raise_for_status()
    feed = feedparser.parse(resp.content)
    out = []
    for e in feed.entries:
        pub = datetime(*e.published_parsed[:6], tzinfo=timezone.utc) if e.get("published_parsed") else None
        if pub and pub < since:
            continue
        enclosure = next((l.href for l in e.get("links", []) if l.get("rel") == "enclosure"), None)
        out.append({
            "external_id": e.get("id") or e.get("guid") or e.link,
            "url": e.get("link"), "title": e.get("title", ""),
            "description": e.get("summary", ""), "published_at": pub,
            "duration_s": _itunes_duration(e.get("itunes_duration")),
            "audio_url": enclosure,
            # Podcasting 2.0 tags: feedparser exposes unknown namespaces loosely; parse raw XML when present
            "transcript_urls": [t.get("url") for t in e.get("podcast_transcript", []) if isinstance(t, dict)],
        })
    return out, resp.headers.get("ETag")

def _itunes_duration(v: str | None) -> int | None:
    if not v: return None
    parts = [int(p) for p in str(v).split(":") if p.isdigit()]
    s = 0
    for p in parts: s = s * 60 + p
    return s or None
```

```python
# packages/arena_ingest/src/arena_ingest/sources/youtube.py
import isodate, httpx
YT = "https://www.googleapis.com/youtube/v3"
UNIT_COST = {"channels": 1, "playlistItems": 1, "videos": 1, "search": 100}

class YouTubeData:
    def __init__(self, key: str, quota):          # quota: QuotaLedger with .spend(units) -> bool
        self.key, self.quota, self.c = key, quota, httpx.Client(timeout=30)

    def _get(self, resource: str, **params) -> dict:
        if not self.quota.spend(UNIT_COST[resource]):
            raise QuotaExhausted(resource)
        r = self.c.get(f"{YT}/{resource}", params={**params, "key": self.key})
        r.raise_for_status()
        return r.json()

    def channel_by_handle(self, handle: str) -> dict | None:
        items = self._get("channels", part="id,snippet,contentDetails", forHandle=handle.lstrip("@")).get("items", [])
        return items[0] if items else None

    def uploads(self, uploads_playlist_id: str, since_iso: str):
        token = None
        while True:
            page = self._get("playlistItems", part="contentDetails,snippet", maxResults=50,
                             playlistId=uploads_playlist_id, pageToken=token)
            ids = [i["contentDetails"]["videoId"] for i in page["items"]
                   if i["contentDetails"].get("videoPublishedAt", "") >= since_iso]
            if ids:
                vids = self._get("videos", part="snippet,contentDetails", id=",".join(ids))["items"]
                for v in vids:
                    yield {"external_id": v["id"], "title": v["snippet"]["title"],
                           "description": v["snippet"].get("description", ""),
                           "published_at": v["snippet"]["publishedAt"],
                           "duration_s": int(isodate.parse_duration(v["contentDetails"]["duration"]).total_seconds()),
                           "url": f"https://www.youtube.com/watch?v={v['id']}"}
            # uploads are newest-first: stop paging once the page is older than the window
            if len(ids) < len(page["items"]) or not (token := page.get("nextPageToken")):
                return

class QuotaExhausted(RuntimeError): ...
```

### 4.2 S2 `resolve_entities`

**Purpose.** Turn mention strings into `person_id`s with a calibrated `resolution_confidence`, and decide `accepted` / `review` / `rejected`.

**Algorithm** (doc 05 §2.4):
1. Normalize: NFKC, casefold, strip honorifics ("Dr.", "Sen."), punctuation and possessives.
2. Candidates: exact alias hit (alias index over `person.aliases` + Wikidata labels + handles) → token-sort fuzzy (`rapidfuzz.fuzz.token_sort_ratio ≥ 88`) → handle match → nickname table.
3. Context features: alias match score; is channel owner; landmark's niche == channel owner's niche; `why` keyword overlap with the description; date within active window; co-mentioned landmarks; `ambiguous_name`; evidence type (title > `podcast:person` tag > description > show notes).
4. Score: logistic regression trained on P1 hand-labelled mentions; until trained, a hand-weighted prior (below). `ambiguous_name` caps confidence at 0.89 so it always routes to review.
5. Decide: **≥ 0.90 accept · 0.60–0.90 review · < 0.60 drop** (doc 05 §2.4).
6. After transcription, S5 can promote to `verified_by_audio` (voiceprint match + speaking share > 10%) or reject "present" mentions with no matching voice.

**Idempotency.** Key per episode; the resolver's model version is the LR weights file hash.

```python
# packages/arena_ingest/src/arena_ingest/resolve.py
import math, re, unicodedata
from dataclasses import dataclass
from rapidfuzz import fuzz, process

HONORIFICS = re.compile(r"\b(dr|prof|sen|rep|gov|mr|mrs|ms|sir)\.?\s+", re.I)

def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).casefold()
    s = HONORIFICS.sub("", s)
    s = re.sub(r"['’]s\b", "", s)
    s = re.sub(r"[^\w\s@]", " ", s)
    return " ".join(s.split())

@dataclass
class Candidate:
    person_id: str; alias_score: float; method: str

class AliasIndex:
    def __init__(self, rows: list[tuple[str, str]]):         # (alias, person_id)
        self.exact = {}
        for alias, pid in rows:
            self.exact.setdefault(norm_name(alias), set()).add(pid)
        self.keys = list(self.exact)

    def candidates(self, mention: str, limit: int = 5) -> list[Candidate]:
        m = norm_name(mention)
        if m in self.exact:
            return [Candidate(pid, 100.0, "exact") for pid in self.exact[m]]
        hits = process.extract(m, self.keys, scorer=fuzz.token_sort_ratio, limit=limit, score_cutoff=88)
        return [Candidate(pid, score, "fuzzy") for key, score, _ in hits for pid in self.exact[key]]

# Prior weights until the P1 logistic regression is trained (then replaced by fitted coefs).
PRIOR = dict(bias=-3.0, alias=4.0, owner=2.5, same_niche=0.8, keyword=0.6, in_window=0.4,
             co_mention=0.5, title_evidence=0.7, tag_evidence=1.2)

def confidence(c: Candidate, f: dict[str, float], ambiguous: bool, w=PRIOR) -> float:
    z = (w["bias"] + w["alias"] * (c.alias_score / 100) + w["owner"] * f["is_owner"]
         + w["same_niche"] * f["same_niche"] + w["keyword"] * f["keyword_overlap"]
         + w["in_window"] * f["in_window"] + w["co_mention"] * f["co_mention"]
         + w["title_evidence"] * f["in_title"] + w["tag_evidence"] * f["podcast_person_tag"])
    p = 1 / (1 + math.exp(-z))
    return min(p, 0.89) if ambiguous else p

def decide(p: float) -> str:
    return "accepted" if p >= 0.90 else "review" if p >= 0.60 else "rejected"
```

### 4.3 S3 `select_episodes`

**Purpose.** Choose the transcription set for the slice: an encounter **coverage** set that connects every niche (value-weighted spanning forest + redundancy + long-range chords), plus a fixed **solo baseline budget per niche**. Slice 1 target: ~150–300 episodes, ~300–500 hours.

**Inputs.** Accepted appearances (`mention_type='present'`), episode metadata, niche priors. **Outputs.** `encounter` rows; `episode.selected_for`, `selection_run_id`; a coverage report and gap list (JSON in `pipeline_run.stats` and a Markdown report under `evals/reports/`).

**Algorithm.**
- Distance prior `d(i,j)`: 0.9 if combatants; 0.2 if adjacent; else 0.4 + 0.3·[different domain] + 0.3·|placement differences|/3; clipped to [0.1, 1].
- Quality `q(e)`: product of duration factor (≥ 45 min → 1.0; 20–45 → 0.6; else 0.2), format (interview/debate/panel 1.0; solo 0.3; clip/compilation 0), both present (1.0 vs 0), transcript route available (caption/publisher 1.0, audio-only 0.7), recency.
- Value `v(e) = d·q / hours`.
- Backbone: Kruskal on niche pairs in decreasing value with union-find. Panels merging several components count once.
- Redundancy: each niche gets ≥ 2 distinct partner niches where candidates exist.
- Chords: add the highest-distance encounter that most reduces mean hop distance until the coverage budget (hours) is spent.
- Constraints throughout: ≤ 5 selected per host channel, ≤ 3 per landmark, at least one encounter per niche involving a `core` landmark; secondary-niche links (weight 0.5) never close a gap alone.
- Baseline: per niche `sampling_budget_hours` (slice: 15 h), split core 50 / bridger 30 / edge 20, then evenly across landmarks; stratified by quarter and by title-embedding topic clusters; excludes episodes already in coverage.

**Failure modes.** Disconnected niche graph → the report lists isolated niches at the top of the gap list (they become anti-debate invitation candidates, never forced). Budget too small to reach every niche → the run is `partial` with the uncovered list.

```python
# packages/arena_ingest/src/arena_ingest/select.py
from collections import defaultdict
from dataclasses import dataclass, field

class DSU:
    def __init__(self, items): self.p = {i: i for i in items}
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        self.p[ra] = rb; return True

@dataclass
class Cand:
    episode_id: str; host_channel: str; hours: float; quality: float
    niches: frozenset[str]                     # primary niches of present landmarks
    landmarks: frozenset[str]; has_core: dict[str, bool]   # niche -> any core landmark present
    value: float = 0.0

@dataclass
class Selection:
    chosen: list[str] = field(default_factory=list); hours: float = 0.0
    per_host: dict = field(default_factory=lambda: defaultdict(int))
    per_landmark: dict = field(default_factory=lambda: defaultdict(int))

def pair_distance(a: str, b: str, prior: dict) -> float: ...   # §4.3 formula, from niche rows

def select_coverage(cands: list[Cand], niches: set[str], prior: dict, budget_h: float,
                    max_per_host=5, max_per_landmark=3) -> tuple[Selection, list[str]]:
    for c in cands:
        ds = [pair_distance(a, b, prior) for a in c.niches for b in c.niches if a < b]
        c.value = (max(ds) if ds else 0) * c.quality / max(c.hours, 0.25)
    sel, dsu = Selection(), DSU(niches)

    def ok(c: Cand) -> bool:
        return (sel.per_host[c.host_channel] < max_per_host and sel.hours + c.hours <= budget_h
                and all(sel.per_landmark[l] < max_per_landmark for l in c.landmarks))

    def take(c: Cand):
        sel.chosen.append(c.episode_id); sel.hours += c.hours; sel.per_host[c.host_channel] += 1
        for l in c.landmarks: sel.per_landmark[l] += 1

    # 1. backbone: greedy by "components merged per hour × value"
    remaining = sorted(cands, key=lambda c: c.value, reverse=True)
    for c in remaining:
        roots = {dsu.find(n) for n in c.niches}
        if len(roots) > 1 and ok(c):
            ns = list(c.niches)
            for n in ns[1:]: dsu.union(ns[0], n)
            take(c)
    # 2. redundancy: every niche ≥ 2 distinct partners
    partners = defaultdict(set)
    for c in cands:
        if c.episode_id in sel.chosen:
            for a in c.niches: partners[a] |= c.niches - {a}
    for n in sorted(niches, key=lambda n: len(partners[n])):
        for c in remaining:
            if len(partners[n]) >= 2:
                break
            if n in c.niches and c.episode_id not in sel.chosen and (c.niches - {n}) - partners[n] and ok(c):
                take(c)
                for a in c.niches:
                    partners[a] |= c.niches - {a}
    # 3. chords: highest value long-range additions until budget
    for c in remaining:
        if c.episode_id not in sel.chosen and ok(c) and c.value > 0:
            take(c)
    isolated = sorted(n for n in niches if not partners[n])   # → top of the gap list
    return sel, isolated
```

### 4.4 S4 `fetch_transcript`

**Purpose.** Get a transcript for a selected episode by the cheapest compliant route: publisher transcript (`podcast:transcript` tag, show-notes page) → YouTube captions (creator before auto) → queue `asr_episode` (box only). Store the raw file in MinIO; write `transcript` + `private.segment` rows.

**Politeness.** Caption fetching is the binding constraint (3–6 weeks for the full seed), so it starts in P1. Defaults: one request every 20–40 s with jitter, a daily cap (`ARENA_CAPTIONS_PER_DAY=800`), exponential backoff on `RequestBlocked`/`IpBlocked` (5 min → 6 h), and a **circuit breaker**: three blocks in an hour pause the `fetch` queue for 12 h and alert the operator. We never rotate IPs or use proxies to evade blocks (red line 4). Every fetch is logged (`event_log: transcript.fetched`, route, latency) for the R49 risk register.

**Segment shape for captions.** Caption cues have no speaker labels. For solo content (`format='solo'`, or channel owner is the only accepted appearance), `person_id = owner` with `attribution_confidence = 0.8` (metadata only; enough for internal use, not publication, OPEN-6). Multi-speaker caption transcripts get `speaker_kind='unknown'` and are queued for ASR+diarization on the box when they are coverage episodes; until then they produce no stances.

```python
# packages/arena_ingest/src/arena_ingest/transcripts/youtube_captions.py
import random, time
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (NoTranscriptFound, TranscriptsDisabled,
                                            VideoUnavailable, RequestBlocked, IpBlocked)

class CaptionsBlocked(RuntimeError): ...

class PoliteCaptionFetcher:
    def __init__(self, min_gap_s=20.0, max_gap_s=40.0):
        self.api = YouTubeTranscriptApi()          # youtube-transcript-api >= 1.0 instance API
        self.min_gap, self.max_gap, self._last = min_gap_s, max_gap_s, 0.0

    def _pace(self):
        wait = self._last + random.uniform(self.min_gap, self.max_gap) - time.monotonic()
        if wait > 0: time.sleep(wait)
        self._last = time.monotonic()

    def fetch(self, video_id: str) -> dict | None:
        self._pace()
        try:
            listing = self.api.list(video_id)
            try:
                t = listing.find_manually_created_transcript(["en", "en-US", "en-GB"]); kind = "creator"
            except NoTranscriptFound:
                t = listing.find_generated_transcript(["en"]); kind = "auto"
            fetched = t.fetch()
        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
            return None
        except (RequestBlocked, IpBlocked) as e:
            raise CaptionsBlocked(str(e)) from e
        cues = [{"text": s.text, "start_ms": int(s.start * 1000),
                 "end_ms": int((s.start + s.duration) * 1000)} for s in fetched.snippets]
        return {"route": f"yt_caption_{kind}", "language": fetched.language_code, "cues": cues}
```

Caption cues are 2–7 s fragments. `segments_from_cues()` merges cues into sentence-like segments (split on terminal punctuation when present, else on pauses > 1.2 s, max 30 s) and keeps a cue-offset map so that any character offset maps back to a timestamp for `?t=` deep links.

### 4.5 S5 `asr_episode` (box only)

**Purpose.** Audio → word-timestamped, diarized, speaker-named segments. Used for coverage episodes with several speakers, for audio-only podcasts, and for poor captions.

**Pipeline.**
1. Fetch audio from the RSS enclosure (download-intended). YouTube-only audio via yt-dlp is **off by default** (`ARENA_ALLOW_YT_AUDIO=false`; stronger ToS exposure, R49) and needs Benjamin's approval per channel.
2. `ffmpeg -ac 1 -ar 16000` → WAV; Silero VAD is optional (Parakeet handles silence).
3. **ASR:** Parakeet TDT 0.6B v3 via NeMo with local attention for long-form (up to ~3 h per pass), native word timestamps.
4. **Diarization:** pyannote `speaker-diarization-community-1`, using its *exclusive* output to assign each word to exactly one speaker.
5. **Speaker naming** (highest-harm failure). Fuse four signals per diarized speaker:
   - metadata prior (episode appearances: host/guest list);
   - voiceprint cosine similarity to enrolled landmark voiceprints (TitaNet-large embeddings, enrolled from ≥ 3 solo clips each);
   - LLM self-identification pass over the first 5 minutes ("I'm X", "welcome Y");
   - diarizer agreement / speaking share.

   Publish threshold 0.9; 0.7–0.9 internal only; < 0.7 → `person_id=null`, `speaker_kind='unknown'` (OPEN-6). Unmatched voices are `non_public` unless they match a known public person.
6. Delete raw audio after success; keep words JSON in MinIO.

**GPU scheduling.** `asr` queue workers run only inside the `nemo` container and only in the ASR window (§10.4).

```python
# packages/arena_ingest/src/arena_ingest/asr/parakeet.py   (runs in the NGC NeMo container)
import nemo.collections.asr as nemo_asr

class ParakeetASR:
    MODEL = "nvidia/parakeet-tdt-0.6b-v3"

    def __init__(self, device: str = "cuda"):
        self.m = nemo_asr.models.ASRModel.from_pretrained(self.MODEL).to(device).eval()
        # long-form: local attention + chunked subsampling (model card; up to ~3 h per pass)
        self.m.change_attention_model("rel_pos_local_attn", [256, 256])
        self.m.change_subsampling_conv_chunking_factor(1)

    def transcribe(self, wav_path: str) -> list[dict]:
        out = self.m.transcribe([wav_path], timestamps=True)[0]
        # words: [{'word': str, 'start': sec, 'end': sec, ...}]
        return [{"w": w["word"], "s": int(w["start"] * 1000), "e": int(w["end"] * 1000)}
                for w in out.timestamp["word"]]
```

```python
# packages/arena_ingest/src/arena_ingest/asr/diarize.py
import numpy as np, torch
from pyannote.audio import Pipeline

class Diarizer:
    def __init__(self, hf_token: str):
        self.p = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1", token=hf_token)
        self.p.to(torch.device("cuda"))

    def turns(self, wav_path: str) -> list[tuple[int, int, str]]:
        out = self.p(wav_path)
        ann = out.exclusive_speaker_diarization          # pyannote.audio 4.x; 3.x returns an Annotation (UNVERIFIED attr names)
        return [(int(t.start * 1000), int(t.end * 1000), spk) for t, _, spk in ann.itertracks(yield_label=True)]

def assign_words(words: list[dict], turns: list[tuple[int, int, str]]) -> list[dict]:
    """Assign each word to the turn covering its midpoint (exclusive diarization => no overlaps)."""
    starts = np.array([t[0] for t in turns]); i = 0
    for w in words:
        mid = (w["s"] + w["e"]) // 2
        i = max(int(np.searchsorted(starts, mid, side="right")) - 1, 0)
        s, e, spk = turns[i]
        w["spk"] = spk if s <= mid <= e else None
    return words
```

```python
# packages/arena_ingest/src/arena_ingest/asr/speakers.py
import numpy as np

W = dict(meta=0.35, voice=0.45, llm=0.15, share=0.05)     # initial; calibrate on P1 gold episodes

def name_speakers(spk_embs: dict[str, np.ndarray],          # diar label -> mean TitaNet embedding (L2-normed)
                  enrolled: dict[str, np.ndarray],          # person_id -> voiceprint (L2-normed)
                  meta_prior: dict[str, float],             # person_id -> prior from appearances (host .9, guest .7)
                  llm_selfid: dict[str, str],               # diar label -> person_id claimed in transcript
                  share: dict[str, float]) -> dict[str, tuple[str | None, float]]:
    """Returns diar label -> (person_id or None, confidence). One-to-one via greedy assignment."""
    scores = []
    for lab, e in spk_embs.items():
        for pid, v in enrolled.items():
            if pid not in meta_prior:            # only people plausibly on this episode
                continue
            cos = float(e @ v)
            voice = np.clip((cos - 0.35) / (0.75 - 0.35), 0, 1)   # map cosine to 0..1 (calibrate)
            s = (W["meta"] * meta_prior[pid] + W["voice"] * voice
                 + W["llm"] * (1.0 if llm_selfid.get(lab) == pid else 0.0)
                 + W["share"] * min(share.get(lab, 0) / 0.1, 1.0))
            scores.append((s, lab, pid))
    out, used_l, used_p = {}, set(), set()
    for s, lab, pid in sorted(scores, reverse=True):
        if lab in used_l or pid in used_p: continue
        out[lab] = (pid, s) if s >= 0.7 else (None, s)
        used_l.add(lab); used_p.add(pid)
    for lab in spk_embs:
        out.setdefault(lab, (None, 0.0))
    return out
```

### 4.6 S6 `chunk_transcript`

**Purpose.** Cut segments into extraction windows of ~2–4 minutes (spine), aligned to speaker turns, with overlap for context.

**Algorithm.** Walk segments in order; accumulate a *core* window until ≥ 120 s and ≥ 1,200 tokens, then close it at the next speaker change or sentence end, hard cap 240 s / 2,400 tokens. Prepend up to 30 s (≈ 500 tokens) of preceding context and append 15 s of following context. Claims may quote context but must **anchor in the core** (prevents duplicates across overlapping chunks). Segments with `speaker_kind='unknown'` and attribution < 0.7 are included as context but marked "do not attribute" in the prompt.

**Idempotency.** Deterministic given segments; `model_version = "chunker-v{N}"`.

```python
# packages/arena_extract/src/arena_extract/chunk.py
from dataclasses import dataclass

def est_tokens(text: str) -> int: return int(len(text.split()) * 1.3) + 1

@dataclass
class Seg: seq: int; start_ms: int; end_ms: int; text: str; speaker: str | None

def chunk(segs: list[Seg], min_s=120, max_s=240, min_tok=1200, max_tok=2400,
          pre_ctx_s=30, post_ctx_s=15) -> list[dict]:
    chunks, i, n = [], 0, len(segs)
    while i < n:
        j, tok = i, 0
        while j < n:
            tok += est_tokens(segs[j].text)
            dur = (segs[j].end_ms - segs[i].start_ms) / 1000
            nxt_spk_change = j + 1 < n and segs[j + 1].speaker != segs[j].speaker
            if dur >= max_s or tok >= max_tok: break
            if dur >= min_s and tok >= min_tok and (nxt_spk_change or segs[j].text.rstrip().endswith((".", "?", "!"))):
                break
            j += 1
        j = min(j, n - 1)
        pre = i
        while pre > 0 and (segs[i].start_ms - segs[pre - 1].start_ms) / 1000 <= pre_ctx_s: pre -= 1
        post = j
        while post + 1 < n and (segs[post + 1].end_ms - segs[j].end_ms) / 1000 <= post_ctx_s: post += 1
        chunks.append({"seqs": [s.seq for s in segs[pre:post + 1]], "core_from": segs[i].seq,
                       "core_to": segs[j].seq, "start_ms": segs[i].start_ms, "end_ms": segs[j].end_ms,
                       "speakers": sorted({s.speaker for s in segs[i:j + 1] if s.speaker})})
        i = j + 1
    return chunks
```

### 4.7 S7 `extract_claims`

**Purpose.** Propose candidate claims from one chunk. Decomposed per 06 §4: a single call returns ADU-level items with a **verbatim quote**, a speaker-relative claim, a neutral proposition draft and closed-vocabulary attributes. A separate critic call (different model family on the box) runs in S8. On the box, the coverage set gets k = 2 self-consistency runs.

**Prompt (excerpt; `prompt_id=extract_claims`, versioned file `prompts/extract_claims/v3.md`).**

```text
SYSTEM
You extract the claims speakers commit to in a transcript excerpt, for a map of public worldviews.
Rules (binding; from the Topology Live ontology):
1. Quote: copy the speaker's exact words from the CORE section, 6–60 words, no ellipses, no edits.
   If you cannot quote it exactly, do not output the item.
2. speech_act: one of the 13 acts. attribute / steelman_report / nonliteral never commit the speaker.
   question / challenge / meta do not commit the speaker. A rhetorical_question commits only to its
   implied statement, source=implied_by_act, strength at most "leaning".
3. proposed_canonical: a neutral, speaker-independent sentence that the speaker would sign as a fair
   statement of what they asserted. No new names, numbers, time frames or causal claims beyond the quote.
   Do not widen quantifiers ("some labs" never becomes "labs"). Keep a loaded term in quotes if it carries weight.
4. strength must not exceed the quote's hedges ("I think" → at most leaning; "maybe" → tentative).
5. layer: ontological (what is real) | epistemic (how we know) | axiological (what matters)
   | empirical (what is the case) | praxis (what to do).
6. Only speakers marked ATTRIBUTABLE may receive claims. Never attribute words to a speaker marked UNKNOWN.
Return JSON matching the schema. Return {"items": []} if nothing qualifies.

USER
EPISODE: {title} ({published_at})
SPEAKERS: {key: name, ATTRIBUTABLE|UNKNOWN}
NEARBY BANK PROPOSITIONS (for wording consistency only; do not copy unless equivalent):
{top_k_neighbor_canonicals}
CONTEXT (do not quote):
{pre_context}
CORE:
[{seq}] {speaker_key}: {text}
...
CONTEXT (do not quote):
{post_context}
```

**Output schema** (generated from `arena_core.contracts.llm.ExtractClaimsOutput`; shown inlined):

```json
{
  "type": "object", "additionalProperties": false, "required": ["items"],
  "properties": {
    "items": {
      "type": "array", "maxItems": 40,
      "items": {
        "type": "object", "additionalProperties": false,
        "required": ["speaker_key","seq","quote","speech_act","claim_text","proposed_canonical",
                     "tl_type","attitude","strength","source","layer","quantifier"],
        "properties": {
          "speaker_key": {"type": "string"},
          "seq": {"type": "integer", "description": "segment seq in CORE where the quote starts"},
          "quote": {"type": "string", "minLength": 20, "maxLength": 600},
          "speech_act": {"enum": ["assert","concede","retract","question","answer","hypothesize","steelman_report",
                                  "attribute","challenge","commit_conditional","meta","rhetorical_question","nonliteral"]},
          "claim_text": {"type": "string", "maxLength": 300},
          "proposed_canonical": {"type": "string", "minLength": 3, "maxLength": 400},
          "tl_type": {"enum": ["empirical","causal","predictive","counterfactual","normative","prescriptive",
                               "definitional","conceptual","modal","meta"]},
          "attitude": {"enum": ["accepts","rejects","suspends","accepts_conditionally","accepts_for_argument"]},
          "strength": {"enum": ["tentative","leaning","confident","certain"]},
          "credence": {"type": ["number","null"], "minimum": 0, "maximum": 1},
          "source": {"enum": ["stated","implied_by_act","inferred"]},
          "layer": {"enum": ["ontological","epistemic","axiological","empirical","praxis"]},
          "quantifier": {"enum": ["all","most","many","some","few","none","generic"]},
          "conditions": {"type": "array", "items": {"type": "string"}, "maxItems": 3}
        }
      }
    }
  }
}
```

```python
# packages/arena_extract/src/arena_extract/extract.py
from arena_llm import LLMClient, prompts
from arena_core.contracts import llm_schema
from arena_core.contracts.llm import ExtractClaimsOutput

PROMPT_ID = "extract_claims"

def extract_claims(llm: LLMClient, chunk_view: dict, neighbors: list[str], n: int = 1) -> list[dict]:
    p = prompts.load(PROMPT_ID)                     # -> Prompt(version, system, user_template)
    user = p.render(**chunk_view, top_k_neighbor_canonicals="\n".join(f"- {c}" for c in neighbors[:12]))
    outs = llm.complete_json(prompt_id=PROMPT_ID, prompt_version=p.version, system=p.system,
                             user=user, schema=llm_schema(ExtractClaimsOutput), temperature=0.0 if n == 1 else 0.7, n=n)
    runs = [ExtractClaimsOutput.model_validate(o).items for o in outs]   # schema-valid ≠ true: S8 gates
    return merge_votes(runs) if n > 1 else [i.model_dump() for i in runs[0]]

def merge_votes(runs) -> list[dict]:
    """Keep items found in >= 2 runs: same speaker and quote overlap >= 50% (character Jaccard on normalized text)."""
    from arena_extract.anchor import normalize
    def ov(a, b):
        A, B = set(normalize(a.quote)[0].split()), set(normalize(b.quote)[0].split())
        return len(A & B) / max(1, len(A | B))
    kept = []
    for item in runs[0]:
        votes = 1 + sum(any(o.speaker_key == item.speaker_key and ov(o, item) >= 0.5 for o in r) for r in runs[1:])
        if votes >= 2:
            kept.append(item.model_dump() | {"votes": votes})
    return kept
```

**Failure modes.** Invalid JSON (rare with constrained decoding) → one retry at temperature 0.2, then `stage_item.failed`. Empty output on a dense chunk (< 1 claim per 1,000 tokens of committed speech) → logged as a yield anomaly for the quality dashboard, not retried.

### 4.8 S8 `anchor_and_verify`

**Purpose.** Code-verify every claim's quote, then gate it with deterministic validators, the NLI entailment check and (on the box) a cross-family critic. Unsupported claims are discarded with a reason. This is where fidelity lives.

**Quote anchoring** (06 §4.3; TL's invariant "nothing is repaired into a span"):
1. **Exact:** `str.find` of the model quote in each core segment's text (and across adjacent core segments joined with a single space, for quotes spanning a boundary).
2. **Normalized:** NFC, curly→straight quotes and apostrophes, lowercase, punctuation stripped, whitespace collapsed; match in normalized space and map back to original offsets via an offset map.
3. **Fuzzy (locate only):** `rapidfuzz.fuzz.partial_ratio_alignment` on normalized text, accept **score ≥ 95** and **≤ 2 token edits** (Levenshtein on token sequences). The stored quote is `segment.text[char_start:char_end]`, never the model's text.
4. Otherwise `anchor_match='none'` → rejected (`reject_reason='no_anchor'`).
5. Quote must start inside the chunk core and belong to the claimed speaker's segment(s).

Store `anchor_segment_id`, `anchor_char_start/end`, `quote_full`, `t_start_ms`/`t_end_ms` (word timestamps when present; else cue map interpolation), `deep_link` (`https://youtu.be/{id}?t={sec}` or the podcast URL with `#t=`), and `quote_public` (the sentence containing the core of the quote, trimmed to ≤ 280 characters on a word boundary).

```python
# packages/arena_extract/src/arena_extract/anchor.py
import re, unicodedata
from dataclasses import dataclass
from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

_TRANS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-"})
_PUNCT = re.compile(r"[^\w\s']")

def normalize(s: str) -> tuple[str, list[int]]:
    """Return normalized text and a map from each normalized char index to the original index."""
    out, idx = [], []
    s_nfc = unicodedata.normalize("NFC", s)
    prev_space = True
    for i, ch in enumerate(s_nfc):
        ch = ch.translate(_TRANS).lower()
        if _PUNCT.match(ch):
            continue
        if ch.isspace():
            if prev_space: continue
            ch, prev_space = " ", True
        else:
            prev_space = False
        out.append(ch); idx.append(i)
    while out and out[-1] == " ":
        out.pop(); idx.pop()
    return "".join(out), idx

@dataclass
class Anchor:
    char_start: int; char_end: int; match: str; score: float

def locate(quote: str, text: str, fuzzy_min=95.0, max_token_edits=2) -> Anchor | None:
    i = text.find(quote)
    if i >= 0:
        return Anchor(i, i + len(quote), "exact", 100.0)
    nq, _ = normalize(quote)
    nt, m = normalize(text)
    if not nq or not nt:
        return None
    j = nt.find(nq)
    if j >= 0:
        return Anchor(m[j], m[j + len(nq) - 1] + 1, "normalized", 100.0)
    al = fuzz.partial_ratio_alignment(nq, nt, score_cutoff=fuzzy_min)
    if al is None:
        return None
    located = nt[al.dest_start:al.dest_end]
    if Levenshtein.distance(nq.split(), located.split()) > max_token_edits:
        return None
    # snap to word boundaries in the original text
    s, e = m[al.dest_start], m[al.dest_end - 1] + 1
    while s > 0 and text[s - 1].isalnum(): s -= 1
    while e < len(text) and text[e].isalnum(): e += 1
    return Anchor(s, e, "fuzzy", float(al.score))
```

**Deterministic validators** (port of TL `validateProposal`): `span_quote_mismatch` (always re-checked on the stored substring), `new_number`, `new_entity`, `hedge_inflated`, `scope_widened`, `non_attributable_stance`, `non_committing_stance`, `rhetorical_overcommitted`, `attribution_pending` (segment attribution < 0.85 for auto-confirmed). `hedge_inflated` is auto-repaired *downward* (strength lowered to the cap and logged), because lowering strength never adds content; every other code rejects.

**NLI gate.** Premise = the stored quote plus one preceding sentence of context (same speaker). Hypothesis = the speaker-committed form: the proposed canonical for `accepts`/`accepts_conditionally`; "It is not the case that …" for `rejects` (the bank is polarity-normalized). Model: `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` (MIT).

- **Decision:** contradiction prob ≥ 0.5 → reject; entailment ≥ **0.80** → pass; otherwise → `escalated` (critic; Claude audit queue in P2–P3).
- **Calibration:** in P2, against gold, pick the entailment threshold that gives ≥ 0.95 precision on gold-accepted claims.
- `steelman_only` and `inferred` items skip NLI (they do not commit the speaker) but still need an anchor.

```python
# packages/arena_extract/src/arena_extract/nli.py
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class NLIGate:
    MODEL = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"

    def __init__(self, device: str | None = None, entail_min=0.80, contra_max=0.50):
        self.tok = AutoTokenizer.from_pretrained(self.MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL).eval()
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        lab = {v.lower(): k for k, v in self.model.config.id2label.items()}
        self.i_ent, self.i_neu, self.i_con = lab["entailment"], lab["neutral"], lab["contradiction"]
        self.entail_min, self.contra_max = entail_min, contra_max

    @torch.inference_mode()
    def score(self, pairs: list[tuple[str, str]], batch_size: int = 32) -> list[dict]:
        out = []
        for k in range(0, len(pairs), batch_size):
            prem, hyp = zip(*pairs[k:k + batch_size])
            enc = self.tok(list(prem), list(hyp), truncation="only_first", max_length=512,
                           padding=True, return_tensors="pt").to(self.device)
            probs = self.model(**enc).logits.softmax(-1).cpu()
            for p in probs:
                ent, con = float(p[self.i_ent]), float(p[self.i_con])
                label = ("contradiction" if con >= self.contra_max else
                         "entailment" if ent >= self.entail_min else "neutral")
                out.append({"label": label, "entail": ent, "contra": con})
        return out

def hypothesis(canonical: str, attitude: str) -> str:
    if attitude == "rejects":
        return f"It is not the case that {canonical[0].lower()}{canonical[1:].rstrip('.')}."
    return canonical
```

**Critic (box).** A different model family from the extractor (e.g. Qwen extractor → gpt-oss critic) answers TL's signability question ("Would the speaker sign this canonical sentence as a fair statement of what they asserted?") plus scope/hedge/new-content checks, via constrained choice (`pass`/`fail_unfaithful`/`fail_scope`/`fail_attribution`/`unsure`). In P2–P3 on `claude_code_batch`, the critic runs as a separate Claude subagent pass on a sample and on all escalations.

**Outcome.** `gate_status = accepted` only if anchored, validators pass, NLI passes (where required) and the critic does not fail it. A fixed 2% random sample of accepted claims, plus all escalations, is written to the Claude audit queue (§5.1).

**Idempotency.** Key per chunk with `model_version = f"{nli_model}|{critic_model}|anchor-v{N}"`.

### 4.9 S9 `normalize_propositions`

**Purpose.** Map each accepted claim to a bank proposition: reuse an equivalent one or create a new one. Then create the stance.

**Algorithm.**
1. Embed `proposed_canonical` with Qwen3-Embedding-4B (MRL-truncated to 1024 dims, instruction "Represent this claim to find claims with the same truth conditions"). On `cloud-dev`, use Qwen3-Embedding-0.6B on CPU (also 1024-d), so vectors are comparable only within one `embedding_model`. A model change triggers a full re-embed run (monthly deep pass).
2. Candidates: pgvector HNSW top-20 by cosine among `merged_into IS NULL`, cosine ≥ 0.80; rerank with Qwen3-Reranker on the box; keep top 5.
3. **Equivalence judge** (LLM, constrained): for each candidate, `equivalent` / `negation` / `narrower` / `broader` / `related` / `different`, under TL §3.4's strict test: same truth conditions, same scope, polarity-normalized. Embeddings confuse "X" with "not X", which is why the judge is required.
4. `equivalent` → link claim to that proposition. `negation` → link to it with the stance value flipped (`affirm`↔`reject`). Otherwise create a new proposition with `public_id` from a sequence; the polarity-normalized form is chosen by the judge (prefer the positive statement).
5. `narrower`/`broader` become `reframes` candidates for S10.
6. Stance: one row per (person, proposition, episode); multiple claims in the episode aggregate (`claim_ids[]`, strongest strength, source = the strongest of `stated > implied_by_act > inferred`). `inferred` stances are stored but **never scored and never shown without a label** (spine §5).
7. Merges between existing propositions (found later) are events (`proposition.merged`), never deletes; `merged_into` is set and stances are re-pointed by a projection.

```python
# packages/arena_extract/src/arena_extract/normalize.py
from sqlalchemy import text

CANDIDATE_SQL = text("""
  SELECT proposition_id, public_id, canonical, 1 - (embedding <=> CAST(:q AS halfvec)) AS cos
  FROM proposition
  WHERE merged_into IS NULL AND embedding_model = :em
  ORDER BY embedding <=> CAST(:q AS halfvec)
  LIMIT 20""")

JUDGE_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["verdicts"],
  "properties": {"verdicts": {"type": "array", "items": {"type": "object", "additionalProperties": False,
    "required": ["candidate", "relation"], "properties": {
      "candidate": {"type": "string"},
      "relation": {"enum": ["equivalent", "negation", "narrower", "broader", "related", "different"]}}}}}}

def normalize_claim(ctx, llm, embedder, claim: dict, em: str) -> tuple[str, bool]:
    """Returns (proposition_id, flipped_polarity)."""
    vec = embedder.embed([claim["proposed_canonical"]])[0]
    rows = [r for r in ctx.session.execute(CANDIDATE_SQL, {"q": str(list(vec)), "em": em}) if r.cos >= 0.80][:5]
    if rows:
        listing = "\n".join(f"{r.public_id}: {r.canonical}" for r in rows)
        v = llm.complete_json(prompt_id="prop_equivalence", prompt_version="v2",
              system=EQUIV_SYSTEM, user=f"NEW: {claim['proposed_canonical']}\nCANDIDATES:\n{listing}",
              schema=JUDGE_SCHEMA)[0]["verdicts"]
        by = {x["candidate"]: x["relation"] for x in v}
        for r in rows:                                  # nearest first
            if by.get(r.public_id) == "equivalent": return str(r.proposition_id), False
            if by.get(r.public_id) == "negation":   return str(r.proposition_id), True
    return create_proposition(ctx, claim, vec, em), False

EQUIV_SYSTEM = ("Decide whether NEW and each CANDIDATE have the same truth conditions. "
                "equivalent: same claim, same scope, same polarity. negation: same claim with opposite polarity. "
                "narrower/broader: one strictly entails the other. related: same topic, different claim. "
                "Wording differences do not matter; scope and polarity do.")
```

**Metrics (P2 gate).** Merge precision and recall against gold pairs (§12.3).

### 4.10 S10 `link_relations_layers`

**Purpose.** Add proposition → proposition relations (`supports`, `contradicts`, `depends_on`, `reframes`) and confirm layer tags.

**Sources of relations.**
1. *Stated within a chunk:* the extractor already sees "because", "so", "which means". A second constrained call per chunk links its accepted claims' propositions with TL relation types (mapped per §3.4), `source='stated'`, with the evidence claim ids.
2. *Bank-level, inferred:* for each new proposition, retrieve 10 nearest neighbours with different `public_id`; a judge proposes `contradicts` / `depends_on` / `reframes` / none. Relations from this route are `source='inferred'` and are used for navigation only, not for clustering.
3. *From S9:* `narrower`/`broader` verdicts become `reframes` candidates.

**Layer tags.** The extractor's `layer` is a first pass. A classifier (constrained-choice LLM with logprobs on the box, later a distilled GLiClass/SetFit model per 06 §3) re-tags; disagreements with margin < 0.2 go to the audit queue. The proposition's layer is the majority over its accepted claims, ties broken by the classifier.

**Idempotency.** Key = hash of the sorted proposition ids in the batch + bank version.

### 4.11 S11 `build_snapshot`

**Purpose.** Turn stances and reactions into a versioned map state: clusters, landmark and user placements, memberships (which define who may ratify), the niche crosswalk, lineage links, per-question axes, statements for reaction, and live-question updates. Weekly (`weekly` horizon) is the full re-cluster. Daily snapshots hold pulse metrics only and reuse the latest weekly clustering. Monthly re-fits axes and lineage with the full bank.

**Inputs.** Current stances (`superseded_by IS NULL`, `source <> 'inferred'`, `item_status` not `rejected`/`retracted`, landmarks with `panel_status='core_panel'` for clustering; newcomers are placed but do not shape clusters in their first season); latest reactions (`is_latest`); previous snapshot (for alignment and lineage).

**Algorithm.**

1. **Stance matrix** `X ∈ [−1, 1]^{L×P}` (landmarks × propositions). Entry = Σ_k w_k·s_k / Σ_k w_k over the landmark's stances on that proposition in the data window, where
   - `s = +strength_num` for `affirm`, `−strength_num` for `reject`, `+0.5·strength_num` for `conditional`, and 0 for `steelman_only`;
   - `w = recency_decay(as_of; half-life 365 d) × (1.0 stated | 0.7 implied_by_act)`.

   Missing entries stay missing. Keep propositions with stances from ≥ 3 landmarks in ≥ 2 niches (informative columns).
2. **Similarity.** Landmarks rarely state the *same* proposition, so direct agreement is sparse. Blend two signals:
   - Direct: `s_dir(a,b) = Σ_p x_ap x_bp / √(Σ x_ap² Σ x_bp²)` over co-stanced propositions.
   - Semantic: each landmark's signed embedding profile `v_a = Σ_p x_ap e_p / Σ_p |x_ap|` (proposition embeddings `e_p`), then cosine.
   - Blend: `s = α s_dir + (1−α) s_sem`, with `α = n_shared/(n_shared + 20)`.
3. **Clustering.** Build a kNN graph (k = 8, edges weighted by `max(s, 0)`), then run Leiden (`RBConfigurationVertexPartition`) over a resolution sweep. For each resolution, run 30 seeds × bootstrap (80% of propositions). Choose the resolution with the highest mean pairwise ARI (stability), tie-break on modularity. Consensus assignment = co-association matrix → average-linkage cut. **HDBSCAN** on a UMAP embedding is run as a cross-check; disagreements are reported for Benjamin's eye test, not auto-resolved.
4. **Layout.** Classical MDS on `1 − s` gives 2-D coordinates. UMAP is optional for display at larger N. Orthogonal Procrustes aligns the layout to the previous snapshot (rotation/reflection only), so the terrain does not spin week to week.
5. **User placement** (logistic ideal-point model, anchored on landmarks). For each active statement `s` (proposition `p`), fit `P(agree | x) = σ(a_s·x + b_s)` by L2-regularized logistic regression on landmark coordinates `x_a`, with labels from their stance sign on `p` (plus previously placed users, weighted 0.5, once there are enough). Each user's position is the MAP estimate `x_u = argmax Σ_s log P(vote_us | x) − λ‖x − x̄‖²` (`pass` ignored), solved by Newton's method; uncertainty is the trace of the inverse Hessian.
6. **Cluster membership for users** (naive Bayes over clusters, which is robust with few votes): `P(agree | c, s)` = Beta(1,1)-smoothed share of `c`'s landmarks affirming `p`, and `posterior_c ∝ π_c Π_s P(vote_us | c, s)`. Memberships are soft weights. `eligible_to_ratify` is true when **all** of these hold:
   - ≥ 12 non-pass reactions on statements from ≥ 3 clusters' splitter sets;
   - max posterior ≥ 0.6;
   - `app_user.kind='person'`, personhood tier ≥ 2, not suspended;
   - no coordination flag.
7. **Crosswalk.** For each niche × cluster: share of the niche's landmarks in the cluster, share of the cluster from the niche, Jaccard. Cluster labels default to the best-aligned niche name, `label_status='provisional'` (OPEN-1).
8. **Lineage.** Compare to the previous weekly snapshot on **core-panel landmarks only**: Jaccard ≥ 0.5 one-to-one → `continues`; one old cluster sending ≥ 0.3 of its members to two or more new ones → `splits`; the reverse → `merges`; no predecessor ≥ 0.3 → `born`; no successor → `fades`.
9. **Statements.** Three selection rules (memo §7.3), each scored over propositions with ≥ 1 publishable anchor:
   - `cluster_splitter`: high between-cluster variance of `P(affirm | c)`;
   - `live_thread`: high within-cluster variance on a live question's propositions;
   - `surprising_unifier`: high agreement across the two most distant clusters.

   Only claims with speaker confidence ≥ 0.9, `public_surface_allowed` landmarks and `rights_status` not in (`takedown_requested`, `removed`) are eligible as the source clip.
10. **Per-question axes** (§4.11.2) and **live-question lifecycle** (§4.11.3).
11. **Validity metrics** go into `cluster_snapshot.validity`: silhouette on `1 − s`; bootstrap ARI; crosswalk purity; the fraction of landmarks whose nearest three landmarks share their niche ("self-recognition proxy"); agent-free ARI (P6).

```python
# packages/arena_map/src/arena_map/cluster.py
import igraph as ig
import leidenalg as la
import numpy as np
from sklearn.metrics import adjusted_rand_score

def similarity(X: np.ndarray, E: np.ndarray, k_shrink: float = 20.0) -> np.ndarray:
    """X: (L, P) stance matrix with np.nan for missing. E: (P, D) unit proposition embeddings."""
    mask = ~np.isnan(X); Xz = np.nan_to_num(X)
    num = Xz @ Xz.T
    sq = Xz ** 2
    den = np.sqrt((sq @ mask.T) * (mask @ sq.T)) + 1e-9      # norms over co-stanced columns only
    s_dir = num / den
    n_shared = mask.astype(float) @ mask.T.astype(float)
    V = (Xz @ E) / (np.abs(Xz).sum(1, keepdims=True) + 1e-9)
    V /= np.linalg.norm(V, axis=1, keepdims=True) + 1e-9
    s_sem = V @ V.T
    alpha = n_shared / (n_shared + k_shrink)
    S = alpha * s_dir + (1 - alpha) * s_sem
    np.fill_diagonal(S, 1.0)
    return S

def knn_graph(S: np.ndarray, k: int = 8) -> ig.Graph:
    L = len(S); edges, w = [], []
    for i in range(L):
        for j in np.argsort(-S[i])[1:k + 1]:          # union kNN; duplicates (i,j)/(j,i) merged below
            if S[i, j] > 0:
                edges.append((i, int(j))); w.append(float(S[i, j]))
    g = ig.Graph(n=L, edges=edges); g.es["weight"] = w
    g.simplify(combine_edges="max")
    return g

def leiden(g: ig.Graph, resolution: float, seed: int) -> np.ndarray:
    part = la.find_partition(g, la.RBConfigurationVertexPartition, weights="weight",
                             resolution_parameter=resolution, seed=seed)
    return np.array(part.membership)

def stable_partition(X, E, resolutions=(0.5, 0.75, 1.0, 1.25, 1.5), seeds=30, frac=0.8, rng_seed=7):
    rng = np.random.default_rng(rng_seed)
    P = X.shape[1]; best = None
    for res in resolutions:
        runs = []
        for s in range(seeds):
            cols = rng.choice(P, int(frac * P), replace=False)
            runs.append(leiden(knn_graph(similarity(X[:, cols], E[cols])), res, seed=s))
        ari = np.mean([adjusted_rand_score(runs[i], runs[j]) for i in range(seeds) for j in range(i + 1, seeds)])
        if best is None or ari > best[0]:
            best = (ari, res, runs)
    ari, res, runs = best
    L = X.shape[0]; co = np.zeros((L, L))
    for r in runs: co += (r[:, None] == r[None, :])
    co /= len(runs)
    from scipy.cluster.hierarchy import linkage, fcluster
    from scipy.spatial.distance import squareform
    Z = linkage(squareform(1 - co, checks=False), method="average")
    labels = fcluster(Z, t=0.5, criterion="distance") - 1
    return labels, {"resolution": res, "bootstrap_ari": float(ari)}
```

```python
# packages/arena_map/src/arena_map/placement.py
import numpy as np
from scipy.linalg import orthogonal_procrustes
from sklearn.linear_model import LogisticRegression

def mds2(S: np.ndarray) -> np.ndarray:
    D2 = (1 - S) ** 2; n = len(S)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ D2 @ J
    w, V = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1][:2]
    return V[:, idx] * np.sqrt(np.maximum(w[idx], 1e-9))

def align_to_previous(Y: np.ndarray, Y_prev: np.ndarray) -> np.ndarray:
    """Rows must be the same landmarks in the same order (core panel present in both snapshots)."""
    mu, mu_p = Y.mean(0), Y_prev.mean(0)
    R, _ = orthogonal_procrustes(Y - mu, Y_prev - mu_p)
    return (Y - mu) @ R + mu_p

def fit_items(Y_landmarks: np.ndarray, stance_sign: np.ndarray, C: float = 1.0) -> np.ndarray:
    """stance_sign: (L, S) in {+1, -1, 0=missing}. Returns (S, 3) rows [a1, a2, b] per statement."""
    out = np.zeros((stance_sign.shape[1], 3))
    for s in range(stance_sign.shape[1]):
        m = stance_sign[:, s] != 0
        y = (stance_sign[m, s] > 0).astype(int)
        if m.sum() < 4 or y.min() == y.max():          # too few or one-sided: intercept-only item
            p = (y.sum() + 1) / (m.sum() + 2)           # Beta(1,1)-smoothed agree rate
            out[s] = [0.0, 0.0, np.log(p / (1 - p))]
            continue
        lr = LogisticRegression(C=C).fit(Y_landmarks[m], y)
        out[s] = [*lr.coef_[0], lr.intercept_[0]]
    return out

def place_user(items: np.ndarray, votes: dict[int, int], prior_mean: np.ndarray, lam: float = 1.0,
               iters: int = 25) -> tuple[np.ndarray, float]:
    """votes: statement index -> +1 agree / -1 disagree (pass omitted). MAP ideal point by Newton's method."""
    x = prior_mean.copy()
    idx = np.array(list(votes)); y = (np.array([votes[i] for i in idx]) > 0).astype(float)
    A, b = items[idx, :2], items[idx, 2]
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(A @ x + b)))
        grad = A.T @ (y - p) - 2 * lam * (x - prior_mean)
        H = -(A.T * (p * (1 - p))) @ A - 2 * lam * np.eye(2)
        step = np.linalg.solve(H, grad)
        x = x - step
        if np.linalg.norm(step) < 1e-6:
            break
    return x, float(np.trace(np.linalg.inv(-H)))

def cluster_posterior(p_affirm: np.ndarray, votes: dict[int, int], prior: np.ndarray) -> np.ndarray:
    """p_affirm: (K, S) smoothed P(agree | cluster, statement). Returns posterior over K clusters."""
    logp = np.log(prior).copy()
    for s, v in votes.items():
        logp += np.log(p_affirm[:, s] if v > 0 else 1 - p_affirm[:, s])
    logp -= logp.max()
    w = np.exp(logp)
    return w / w.sum()
```

#### 4.11.1 Onboarding statement choice (expected information gain)

The first-60-seconds flow (§8.4) asks about 8–12 statements. Each next statement maximizes the expected reduction in entropy of the user's cluster posterior, restricted to `onboarding_core` and `cluster_splitter` statements. It runs client-side on the static bundle (the `p_affirm` table is published; it contains cluster-level aggregates only).

```python
def next_statement(p_affirm: np.ndarray, post: np.ndarray, asked: set[int]) -> int:
    H = lambda q: -(q * np.log(q + 1e-12)).sum()
    best, best_gain = -1, -1.0
    for s in range(p_affirm.shape[1]):
        if s in asked: continue
        pa = float(post @ p_affirm[:, s])
        post_a = post * p_affirm[:, s]; post_a /= post_a.sum()
        post_d = post * (1 - p_affirm[:, s]); post_d /= post_d.sum()
        gain = H(post) - (pa * H(post_a) + (1 - pa) * H(post_d))
        if gain > best_gain: best, best_gain = s, gain
    return best
```

#### 4.11.2 Per-question axes

A live question `q` has linked propositions with poles (`live_question_proposition.answer_pole`). Its axes are chosen per question (D7):

- **Axis 1** ("the question itself"): each subject's mean signed stance on `q`'s propositions times the pole.
- **Axes 2–3** (the layer where the clusters actually diverge): take propositions within cosine 0.75 of `q`'s propositions, group them by `layer`, and compute each layer's first principal component of the stance sub-matrix. Pick the 1–2 layers whose component has the largest between-cluster variance ratio (F-statistic). Store the loadings in `live_question.chosen_axes`.

This is what lets an event map say "they diverged at the axiological layer, not the empirical one".

#### 4.11.3 Live questions and the weekly battery

- **Weekly battery.** The worker samples niche-balanced chunks from the week's accepted claims (≤ 6 chunks per niche) and writes a `claude_code_batch` task with prompt `live_question_battery`. It asks for neutral, two-sided questions that both sides would sign, each with supporting claim ids. Returned questions are deduplicated against existing ones by embedding (cosine ≥ 0.88 → same question; ≥ 0.75 and narrower → child with `parent_id`), and linked to propositions by an equivalence-style judge.
- **Lifecycle** (per snapshot):
  - `emerging`: answered by claims from one cluster;
  - `spreading`: ≥ 3 landmarks in the origin cluster;
  - `forking`: children created;
  - `crossing`: claims from ≥ 2 clusters in the window (the moment that matters most; it raises a pulse event);
  - `quiet`: no new claims for 4 weeks;
  - `absorbed`: merged into a parent.

  Transitions are events.

### 4.12 S12 `score_reputation`

**Purpose.** Score every contribution on two channels, decide ratification and helpfulness, update writer impact, rating impact and rater helpfulness, produce one public reputation per actor (separate leaderboards for persons and agents), and compute the understanding matrix U.

#### 4.12.1 What the Community Notes scorer actually does (verified)

Sources: `twitter/communitynotes` `documentation/under-the-hood/ranking-notes.md`, `contributor-scores.md`, `contributing/writing-and-rating-impact.md`, `contributing/writing-ability.md`, and `scoring/src/scoring/matrix_factorization/matrix_factorization.py`, all fetched 2026-10-31. The public guide page at communitynotes.x.com did not load in this session; the same documents were read from the GitHub repository.

| Item | Community Notes | Status |
|---|---|---|
| Model | `r̂_un = μ + i_u + i_n + f_u·f_n` | verified |
| Factor dimension | 1 | verified |
| Loss | `Σ(r_un − r̂_un)² + λ_i(i_u² + i_n² + μ²) + λ_f(‖f_u‖² + ‖f_n‖²)`; in code, data loss is a **mean** (MSELoss) and the penalties are **means** of squared parameters | verified |
| λ | `λ_i = 0.15`, `λ_f = 0.03` (intercepts penalized 5× factors) | verified |
| Optimizer | Adam, lr 1.0 (0.2 when warm-started), grad-norm clip 1.0, stop when Δloss < 1e-7 | verified (code) |
| Sign identification | flip factors so ≥ 50% of rater factors are negative | verified (code) |
| Rating values | Yes 1.0, Somewhat 0.5, No 0.0 | verified |
| Helpful (CRH) | `i_n ≥ 0.40` and `|f_n| < 0.50` | verified |
| Not Helpful | `i_n < −0.05 − 0.8·|f_n|`, or upper confidence bound < −0.04 | verified |
| Needs More Ratings | until ≥ 5 ratings, and between thresholds | verified |
| Uncertainty | extreme pseudo-raters refit the note to get intercept bounds | verified (method); details UNVERIFIED |
| CRH inertia | a CRH note loses status only if `i_n` falls > 0.01 below threshold | verified |
| Status lock | notes older than 2 weeks have status locked | verified |
| Tag outlier filter | tag weight `1/(1 + (‖f_u − f_n‖/f̃)^5)`, `f̃` = 40th-percentile distance; high tag weight forces intercept > 0.5 | verified |
| Rater Helpfulness | `(s − 10h)/t`; s = valid ratings matching final status, h = helpful ratings on notes with very high harassment-abuse tag score, t = valid ratings | verified |
| Valid rating | made before the note's first status other than Needs More Ratings (post-May-2022 rule) | verified |
| Second-round rater filter | ≥ 10 ratings, Rater Helpfulness ≥ 0.66; authors also need CRH − 5·CRNH ratio ≥ 0 and mean note score ≥ 0.05 | verified |
| Writing Impact | rises when a note reaches Helpful, falls when Not Helpful; NMR has no effect | verified (qualitative); exact increments UNVERIFIED (we use ±1) |
| Rating Impact | rises when a pre-status rating matches the final status, falls when opposite; non-pivotal opposite ratings discounted | verified (qualitative); formula UNVERIFIED |
| Writing lock | 3 of last 5 decided notes Not Helpful, or Writing Impact ≤ 0 and a note goes Not Helpful; unlock by +5 Rating Impact (+5 more each repeat) | verified |
| Multiple scorers | Core, Expansion, ExpansionPlus, Group, Topic models, Gaussian, population-sample filter, supervised confidence delay | verified (list); not adopted in Slice 1 |

#### 4.12.2 The Arena adaptation

Two rating channels per contribution (D-31.1):
- **Portability** (helpfulness, all eligible raters except members of the described cluster B): "Is this clarifying to you?"
- **Fidelity** (only raters reaction-placed in B): "Would your side sign this as an accurate description of what you believe and why?" A note or steelman is **ratified** when B signs it.

**Portability model: cluster-anchored MF.** Community Notes learns a viewpoint factor `f_u` from ratings alone. The Arena already knows each rater's viewpoint: their snapshot cluster membership `m_u ∈ Δ^K` (soft weights from reactions). The factor term is replaced by cluster offsets and keeps a weak residual factor:

```
r̂_un = μ + i_u + i_n + m̃_u · g_n + f_u f_n,      m̃_u = m_u − 1/K   (centred)

L = mean_(u,n)∈R (r_un − r̂_un)²
    + λ_i (mean_u i_u² + mean_n i_n² + μ²)
    + λ_g mean_n ‖g_n‖²
    + λ_f (mean_u f_u² + mean_n f_n²)

λ_i = 0.15 (CN)   λ_g = 0.03 (CN's factor penalty)   λ_f = 0.09 (3× CN, so clusters explain first)
```

- **Why centring matters.** `Σ_k m_uk = 1`, so with an uncentred `m_u` a constant added to every `g_nk` is indistinguishable from the intercept, and the cheaper penalty would drain `i_n`. With `m̃_u`, `i_n` is identifiable and means **helpfulness to an equal-weighted average cluster**: every cluster counts equally regardless of size. That is the bridging notion the Arena wants.
- **Spread.** `spread_n = max_k g_nk − min_k g_nk` over clusters with ≥ 2 raters on `n` replaces `|f_n|` as the polarization measure. The effective factor is `φ_n = max(spread_n/2, |f_n|)`.
- **Status** (initial thresholds = CN's where an analogue exists):
  - `helpful`: `i_n ≥ 0.40`, `spread_n < 0.50`, `|f_n| < 0.50`, ≥ 5 ratings from ≥ 2 rater clusters (≥ 2 raters each).
  - `not_helpful`: `i_n < −0.05 − 0.8·φ_n`, or `ucb < −0.04`.
  - Otherwise `needs_ratings`.
  - CN's CRH inertia (0.01) and the two-week lock apply.

**Fidelity model: per described cluster.** For each cluster B, fit a CN-style 1-D MF on fidelity votes from raters placed in B (K = 1, so only intercepts and one residual factor):
- `F_n = μ_B + mean(i_u) + i_n` is the fidelity an average member of B assigns. μ is shrunk by `λ_i`, so rater intercepts carry part of the mean, and `mean(i_u)` restores the scale.
- **Ratified:** `F_n ≥ 0.70` with ≥ 5 fidelity raters and `fidelity_lcb ≥ 0.60`. These are config defaults (`arena_core.config`), shared verbatim by PRD-MEET-05 and the Plan; changing them needs an ADR approved by Benjamin (**OD-14**).
- **Split detected:** `|f_n| ≥ 0.50` with ≥ 3 raters on each pole. Here B disagrees with itself about the description (doc 05's `B_split`). The note shows per-subgroup fidelity, and the next snapshot checks whether B itself has split.
- **Raters are sampled.** Fidelity raters are mostly **invited by random sample** from B's eligible members (`rating.sampled = true`). Self-selected fidelity votes are capped at 50% of a note's fidelity votes. This is the main defence against sybils who place themselves in B.

**Combined status** (stored in `contribution.status`): `split_detected` > `ratified_helpful` > `ratified` > `not_helpful` > `helpful` > `needs_ratings`. Syntheses have no single "described" cluster. They are scored on portability with the extra condition that both parent clusters' predicted helpfulness (`μ + i_n + g_nA − ḡ_n` and the same for B) is ≥ 0.6. Their main credit is retroactive (below).

**Two rounds** (as CN):
- Round 1 uses all eligible raters.
- Round 2 drops raters with Rater Helpfulness < 0.66 (once they have ≥ 10 ratings), raters in coordinated groups, and authors whose CRH − 5·CRNH ratio < 0.
- Round 2 statuses are final for the run.

**Writer impact.** `WI_a = Σ_n gain(status_n)`, with `ratified_helpful` +2, `ratified` +1, `helpful` +1, `not_helpful` −1, others 0. A writing lock follows CN: 3 of the last 5 decided contributions `not_helpful`, or WI ≤ 0 and a new `not_helpful`. Unlock with +5 rating impact, +5 more per repeat.

**Rating impact and rater helpfulness.** A rating is valid if it was made while the contribution was `needs_ratings`. Rating values are sealed (hidden from other raters) until status is decided, to prevent herding.
- `RI` = matching valid ratings − opposite valid ratings, with opposite non-pivotal ratings weighted 0.5.
- `RH = (s − 10h)/t` exactly as CN, where `h` counts helpful ratings on contributions later removed for harassment.

**Reputation (public, one per actor).**

```
reputation_a = WI_a + SC_a + RH_a · min(t_a, 50)/10
```

`SC` is synthesis credit. The rater component is capped at 5 points so rating alone cannot outrank writing. Persons and agents get separate leaderboards (`actor_kind`). Agents have no rater component because they never rate. Leaderboard views apply the safeguards in SPINE §10 (OD-09): season = calendar quarter, `WI` and `SC` decayed with a 180-day half-life for leaderboard ordering, top 50 numbered, opt-in handles only.

**Synthesis credit (retroactive, by lineage).** When a synthesis is promoted (a `bridge_proposal` becomes a statement; a `better_question` becomes a live question; a `clean_disagreement` becomes a pinned "ratified difference" on the cluster-pair page), uptake is measured in later snapshots:
- `uptake_c` = share of cluster c's eligible reactors who agree with the derived statement (or who adopt the question, i.e. answer it in contributions).
- `SC = 3·min(uptake_A, uptake_B)` when both ≥ 0.5, else 0.
- For `clean_disagreement`, uptake is both clusters' fidelity signature on the stated difference.

Credit is added in the snapshot where it is earned and is attributed back to the original author.

**Understanding matrix.** `U[A][B]` = the shrunk mean of `clip(F_n, 0, 1)` over notes and steelmen authored by members of A about B, with pseudo-count α = 3 toward prior 0 ("no understanding demonstrated yet"). The scorer also stores the count, the number ratified and a lower bound. An `agent_free` variant excludes agent-authored and agent-drafted contributions. U feeds the cluster-pair pages, the strategy market and the weekly weather report.

#### 4.12.3 Implementation (numpy, tested)

The fitting code is numpy so it runs on any profile. Full-batch Adam on ≤ 10^6 ratings takes seconds. A torch port (same loss, CN-style `torch.optim.Adam`) is a drop-in if volume grows.

The full numpy implementation is in **[`08a-APPENDIX-DDL-and-SCORER.md` §A2](08a-APPENDIX-DDL-and-SCORER.md#a2-scorer-implementation-full)**:

- `packages/arena_reputation/src/arena_reputation/cluster_mf.py`: `MFParams`, `MFConfig`, an Adam step, `fit()` (the cluster-anchored MF loss above), `refit_note()` and `pseudo_rater_bounds()` (CN-style extreme pseudo-raters for intercept bounds).
- `packages/arena_reputation/src/arena_reputation/scorer.py`: `Thresholds` (all defaults in one dataclass), `Ratings`, `Contribs`, `portability_status()`, `score_portability()`, `score_fidelity()`, `combined_status()`, `rater_helpfulness()`, `writer_impact()`, `reputation()` and `understanding_matrix()`.

**Key excerpt: `combined_status`** (how the two channels become one stored status).

```python
def combined_status(port: str, F: float, n_fid: int, split: bool, kind: str, th: Thresholds) -> str:
    if kind in ("note", "steelman"):
        if split:
            return "split_detected"
        ratified = n_fid >= th.fid_min_n and F >= th.fid_ratify
        if ratified and port == "helpful":
            return "ratified_helpful"
        if ratified:
            return "ratified"
        if port == "not_helpful" or (n_fid >= th.fid_min_n and F < 0.3):
            return "not_helpful"
        return "helpful" if port == "helpful" else "needs_ratings"
    return port                        # synthesis: portability across both parents; lineage credit later
```

#### 4.12.4 Anti-gaming

| Threat (CN attack models + Arena-specific) | Control |
|---|---|
| Sybils place themselves in B to sign strawmen | Personhood tier ≥ 2 to rate; ≥ 12 reactions to be eligible; random-sample invitations for fidelity (self-selected ≤ 50%); rater intercepts absorb indiscriminate raters; coordinated-rater detection; split detector (a brigade shows up as one pole) |
| Agents ratify or rate | Impossible by construction: `rating_guard` trigger rejects `kind='agent'`; `cluster_membership.eligible_to_ratify` is never true for agents; API scopes for agent tokens exclude `/ratings` |
| Tribal rating (rate own side helpful) | The cluster-anchored model attributes that to `g_nk`, not `i_n`; raters who consistently rate against final outcomes lose RH and fall below 0.66 |
| Coordinated rings | Pairwise co-rating detector (below); group flagged, weight 0 in round 2, `flag(kind='coordinated_rating')` for admin review |
| Self-promotion | No self-rating (trigger); no rating your own cluster's description of another cluster on the fidelity channel (only B rates fidelity) |
| Reaction farming to move clusters | Placement uses the latest vote per statement; reactions from flagged accounts are excluded from the next snapshot; agent-led reactions carry `agent_provenance` and are dropped from the agent-free re-fit |
| Herding | Ratings sealed until status decided |

The detector `coordinated_groups()` (`packages/arena_reputation/src/arena_reputation/coordination.py`) links rater pairs who share ≥ 8 contributions with ≥ 95% identical values and ≥ 50% of ratings within 10 minutes, and flags connected groups of ≥ 5. Full code with its self-test (a 12-account ring among 200 honest raters): **[08a §A2.3](08a-APPENDIX-DDL-and-SCORER.md#a23-coordinated-rater-detection)**.

#### 4.12.5 Simulation test (in `evals/harness/test_scorer_sim.py`; part of the P3 gate)

Synthetic world:
- 4 clusters × 100 raters with soft memberships (0.85 home);
- 80 notes of four true types: accurate-bridging, tribal (pleases only the author's cluster), strawman (inaccurate about B) and dull;
- 24 portability raters and 12 sampled fidelity raters per note;
- noisy three-level ratings.

The test asserts that ≥ 75% of accurate-bridging notes are ratified, no tribal note is marked helpful, and no strawman is ratified. It also asserts that a 15-account brigade placed in B, signing every strawman of B, still cannot ratify one. On seed 0 the run gives 0.92 / 0.00 / 0.00, and the brigaded strawmen end at `F ≈ 0.30–0.40` (not ratified). Seeds 1–3 give 0.77–0.90 / 0.00 / 0.00. The sweep in CI runs 20 seeds and reports the distribution.

Full test code: **[08a §A2.4](08a-APPENDIX-DDL-and-SCORER.md#a24-scorer-simulation-test)**. This test implements S-honest/S-tribal (`test_status_by_type`) and S-brigade (`test_brigade_cannot_ratify_strawman`) of the canonical simulation suite in Plan §4.3; the other named tests (S-sybil, S-agents, S-cold-start, S-determinism, S-canary, S-bland, S-judgment) are added by W5 in P3-W5-05.

### 4.13 S13 `publish_snapshot`

**Purpose.** Export an approved snapshot as an immutable, static JSON bundle and push it to the static host. **Nothing outward-facing without approval**: S13 refuses to run unless `cluster_snapshot.status = 'approved'`, which only Benjamin can set (admin endpoint, logged). Until P5 there is no deployment: S13 writes a local bundle, and a password-protected preview deploy happens only with Benjamin's recorded approval (Plan H3).

**Bundle layout** (`/snapshots/{public_id}/`, content-addressed files; `latest.json` points at the current one):

```
manifest.json                 # snapshot meta, file list with sha256, schema versions, counts
map.json                      # clusters (id, label, label_status, centroid, hull), landmark nodes (coords, cluster)
clusters/{cluster_id}.json    # card: top propositions with stances, landmarks, crosswalk, live questions, U row/col
landmarks/{landmark_id}.json  # placement, top stances (stated only, labelled), clips, dispute/annotation, panel status
propositions/{shard}.json     # sharded by public_id prefix: canonical, layer, relations, per-cluster affirm share, ≤ 3 clips
statements.json               # active statements + p_affirm table (K × S) + item params (a1, a2, b) for client placement
live_questions.json           # questions, lifecycle, axes, linked propositions
understanding.json            # U matrix (and agent-free variant), counts, lower bounds
lineage.json                  # cluster lineage graph across published snapshots
leaderboards.json             # top-N persons and agents by reputation (handles that opted in only)
events/{episode_id}.json      # event maps (§4.13.1)
```

**Exclusions enforced in the exporter** (and re-checked by a bundle linter in CI):
- landmarks with `public_surface_allowed = false` are absent;
- claims with speaker confidence < 0.9 are absent;
- `inferred` stances appear only with `"label": "inferred"` and are never in landmark summaries;
- quotes are `quote_public` (≤ 280 characters), never `quote_full`;
- no user ids or personal placements (users fetch their own placement from the API);
- aggregate cells involving users require k ≥ 50 raters/reactors, else they are suppressed.

```json
{
  "$id": "https://dialogos-arena/contracts/public/Manifest.schema.json",
  "type": "object", "additionalProperties": false,
  "required": ["snapshot", "horizon", "as_of", "bundle_version", "files", "counts", "exclusions"],
  "properties": {
    "snapshot": {"type": "string", "pattern": "^\\d{4}-(W\\d{2}|\\d{2}-\\d{2}-d|\\d{2}-m)$"},
    "horizon": {"enum": ["daily", "weekly", "monthly"]},
    "as_of": {"type": "string", "format": "date-time"},
    "bundle_version": {"const": 1},
    "agent_free": {"type": "boolean"},
    "files": {"type": "array", "items": {"type": "object", "required": ["path", "sha256", "bytes"],
      "properties": {"path": {"type": "string"}, "sha256": {"type": "string"}, "bytes": {"type": "integer"}}}},
    "counts": {"type": "object", "additionalProperties": {"type": "integer"}},
    "exclusions": {"type": "object", "properties": {
      "flagged_landmarks_excluded": {"type": "integer"}, "min_k": {"const": 50},
      "min_speaker_confidence": {"const": 0.9}}}
  }
}
```

```python
# packages/arena_map/src/arena_map/publish.py
import hashlib, json, pathlib, subprocess
from arena_core.config import settings

class NotApproved(RuntimeError): ...

def write_bundle(snapshot, out_root: pathlib.Path, docs: dict[str, object]) -> dict:
    if snapshot.status != "approved":
        raise NotApproved(snapshot.public_id)
    root = out_root / "snapshots" / snapshot.public_id
    files = []
    for rel, doc in sorted(docs.items()):
        p = root / rel; p.parent.mkdir(parents=True, exist_ok=True)
        blob = json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        p.write_bytes(blob)
        files.append({"path": rel, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)})
    manifest = {"snapshot": snapshot.public_id, "horizon": snapshot.horizon, "as_of": snapshot.as_of.isoformat(),
                "bundle_version": 1, "agent_free": snapshot.agent_free, "files": files,
                "counts": snapshot.counts, "exclusions": snapshot.exclusions}
    (root / "manifest.json").write_text(json.dumps(manifest, indent=1))
    (out_root / "snapshots" / "latest.json").write_text(json.dumps({"snapshot": snapshot.public_id}))
    return manifest

def deploy(out_root: pathlib.Path, production: bool) -> str:
    """Vercel CLI with a scoped token from the secret store. production=True requires the P5 gate flag."""
    if production and not settings.public_launch_approved:
        raise NotApproved("production deploy before P5 approval")
    args = ["vercel", "deploy", str(out_root), "--yes", "--token", settings.vercel_token.get_secret_value()]
    if production:
        args.append("--prod")
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()   # deployment URL
```

The web app reads bundles from `NEXT_PUBLIC_BUNDLE_BASE` (a separate static Vercel project or a `/snapshots` path on the same project). Bundles are immutable and cached forever (`Cache-Control: public, max-age=31536000, immutable`). `latest.json` is cached for 60 s.

#### 4.13.1 Event maps

An event map is the same pipeline (S4–S10) on one encounter episode, plus an episode-scoped projection: each speaker's starting position (placement from their baseline stances), the propositions both affirmed (met), the propositions where they diverged and at which layer, the episode-scoped dialogue relations, and "missed openings" (pairs of contradicting propositions where one side's steelman is absent; proposed by a `claude_code_batch` pass and labelled as analysis, never as a verdict). Target: published within a day of a major crossover conversation (P5). The first public pick is surprising but less incendiary (memo §11.1). The ripple (pulse tracking over following days) is a daily-snapshot metric keyed to the episode's propositions.

### 4.14 S14 `resolve_forecasts` (P6)

Specified with the market in §9.2.

---

## 5. `arena_llm`: interface and backends

```python
# packages/arena_llm/src/arena_llm/base.py  (the spine interface, verbatim)
from typing import Protocol

class LLMClient(Protocol):
    def complete_json(self, *, prompt_id: str, prompt_version: str, system: str,
                      user: str, schema: dict, temperature: float = 0.0,
                      n: int = 1) -> list[dict]: ...

class PendingBatch(Exception):
    """Raised by asynchronous backends (claude_code_batch) when the result is not ready yet."""
    def __init__(self, task_id: str, batch_id: str):
        super().__init__(task_id); self.task_id, self.batch_id = task_id, batch_id

class BackendDisabled(RuntimeError): ...
```

All backends share a wrapper that (a) computes `request_hash = sha256(prompt_id, prompt_version, system, user, schema, temperature, n, model)`, (b) returns a cached result from `llm_call`/result store when the same hash already succeeded (re-runs are free), (c) validates every output against `schema` with `jsonschema` (`Draft202012Validator`) and retries once on failure, and (d) writes an `llm_call` row. Prompts live in `packages/arena_llm/prompts/<prompt_id>/<version>.md` with front matter (`version`, `schema`, `owner`, `changelog`). Changing a prompt without bumping the version fails a CI test that hashes prompt files against a lock file.

```python
# packages/arena_llm/src/arena_llm/registry.py
from arena_core.config import settings
from .base import BackendDisabled, LLMClient

def get_client(role: str = "extract") -> LLMClient:
    """role ∈ {extract, critic, judge, tag, battery, gold, audit}; settings map roles to backend + model."""
    cfg = settings.llm_roles[role]                     # e.g. {"backend": "vllm", "model": "qwen3.6-35b-a3b", "base_url": ...}
    match cfg.backend:
        case "claude_code_batch":
            from .backends.claude_code_batch import ClaudeCodeBatch; return ClaudeCodeBatch(cfg)
        case "vllm":
            from .backends.vllm import VLLMClient; return VLLMClient(cfg)
        case "openai_compat":
            from .backends.vllm import VLLMClient; return VLLMClient(cfg, structured="response_format")
        case "anthropic_api":
            if not settings.anthropic_api_enabled:
                raise BackendDisabled("anthropic_api is disabled by default; Benjamin must opt in (costs money)")
            from .backends.anthropic_api import AnthropicAPI; return AnthropicAPI(cfg)
        case "fake":
            from .backends.fake import FakeLLM; return FakeLLM(cfg)
    raise ValueError(cfg.backend)
```

### 5.1 `claude_code_batch`: the file-queue protocol

**Why.** Gold labels, prompt design, the 2% audit, escalations and the weekly question battery run inside Benjamin's Claude subscription, through Claude Code sessions he starts, not through a metered API (D-31.7). The pipeline therefore cannot call Claude synchronously. It writes **task files**, and a Claude Code session processes them with subagents and writes **result files**. The backend is asynchronous: if the result is missing, `complete_json` raises `PendingBatch`, and the stage task parks itself (§6.3).

**Directory layout** (`evals/queue/` and `evals/results/`, gitignored except READMEs; on the box under `/srv/arena/evals`):

```
evals/queue/<batch_id>/BATCH.md              # human/agent-readable instructions for this batch
evals/queue/<batch_id>/<task_id>.json        # one task per file
evals/queue/<batch_id>/<task_id>.claim       # lease: {"session": "...", "at": "..."}  (stale after 2 h)
evals/results/<batch_id>/<task_id>.json      # result (written atomically: .tmp then rename)
evals/results/<batch_id>/<task_id>.error.json
evals/results/<batch_id>/DONE                # written by the session when every task has a result or error
```

**Task file** (`contracts/llm/ClaudeCodeTask.schema.json`):

```json
{
  "protocol": "arena.ccbatch/1",
  "task_id": "sha256 hex of the request (idempotency key)",
  "batch_id": "2026-11-12-gold-ai-safety-03",
  "kind": "gold | audit | escalation | battery | prompt_design | critic",
  "prompt_id": "extract_claims",
  "prompt_version": "v3",
  "system": "…full system prompt…",
  "user": "…full user message, including the chunk with [seq] markers…",
  "schema": { "…JSON Schema the output must satisfy…": true },
  "n": 1,
  "temperature_hint": 0.0,
  "context": {"chunk_id": "…", "episode_url": "https://youtu.be/…", "stage": "S7"},
  "instructions": "Return only JSON valid against `schema`. Copy quotes exactly from CORE.",
  "created_at": "2026-11-12T03:14:00Z",
  "deadline": "2026-11-15T00:00:00Z"
}
```

**Result file:**

```json
{
  "protocol": "arena.ccbatch/1",
  "task_id": "…same…",
  "outputs": [ { "items": [ … ] } ],
  "model": "claude-opus-5-5",
  "produced_by": "claude-code-subagent",
  "session_id": "…",
  "completed_at": "2026-11-12T05:02:11Z",
  "validated": true,
  "notes": "optional free text: ambiguities the labeler wants a human to see"
}
```

**How a Claude Code session processes a batch.** The repo ships a slash command `.claude/commands/process-batch.md`. Benjamin (or an operator-prepared reminder) opens Claude Code in the repo and runs `/process-batch <batch_id>`. The command instructs the session to:

1. List `evals/queue/<batch_id>/*.json` without a result or a fresh `.claim`.
2. Write a `.claim` for up to 8 tasks at a time, then spawn up to 8 parallel subagents (Task tool), each given exactly one task file's `system`, `user`, `schema` and `instructions`. A subagent has no other context, which keeps labels independent.
3. Validate each subagent's JSON with `uv run arena llm validate-result <task_file> <json>` (jsonschema + the deterministic quote check for extraction tasks). On failure, the subagent gets one retry with the validator's error message. After that, write `.error.json`.
4. Write results atomically, remove the claim, repeat until done, then write `DONE` and print a summary (counts, validator failures, notable `notes`).

Gold labels additionally pass **Benjamin's review**. `arena gold review <batch_id>` renders a side-by-side HTML report (chunk, quotes highlighted, proposed propositions), and his accept/edit/reject decisions write `evals/gold/gold-vN/*.jsonl`. Only reviewed items count as gold (06 §7a).

```python
# packages/arena_llm/src/arena_llm/backends/claude_code_batch.py
import json, os, pathlib, time
from ..base import PendingBatch
from ..hashing import request_hash

class ClaudeCodeBatch:
    def __init__(self, cfg):
        self.queue = pathlib.Path(cfg.queue_dir); self.results = pathlib.Path(cfg.results_dir)
        self.batch_id = cfg.batch_id                  # set per run by the stage (e.g. date + kind + niche)
        self.model = "claude-code-subagent"

    def complete_json(self, *, prompt_id, prompt_version, system, user, schema, temperature=0.0, n=1):
        tid = request_hash(prompt_id, prompt_version, system, user, schema, temperature, n, self.model)
        res = self.results / self.batch_id / f"{tid}.json"
        if res.exists():
            return json.loads(res.read_text())["outputs"]
        err = self.results / self.batch_id / f"{tid}.error.json"
        if err.exists():
            raise RuntimeError(f"claude_code_batch task {tid} failed: {err.read_text()[:500]}")
        qdir = self.queue / self.batch_id; qdir.mkdir(parents=True, exist_ok=True)
        task = qdir / f"{tid}.json"
        if not task.exists():
            tmp = task.with_suffix(".tmp")
            tmp.write_text(json.dumps({
                "protocol": "arena.ccbatch/1", "task_id": tid, "batch_id": self.batch_id,
                "kind": os.environ.get("ARENA_BATCH_KIND", "gold"), "prompt_id": prompt_id,
                "prompt_version": prompt_version, "system": system, "user": user, "schema": schema,
                "n": n, "temperature_hint": temperature,
                "instructions": "Return only JSON valid against `schema`.",
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=1))
            os.replace(tmp, task)
        raise PendingBatch(tid, self.batch_id)
```

### 5.2 `vllm`

OpenAI-compatible HTTP to the box's vLLM servers. Structured output uses the current `structured_outputs: {"json": schema}` request field. The older `guided_json` / `guided_*` fields were **removed in vLLM v0.12**, so they are never sent and images are pinned at vLLM ≥ 0.12. `openai_compat` servers (llama.cpp, Ollama) use `response_format: {type: json_schema}` instead. With reasoning models (gpt-oss, Qwen thinking), the server runs with `--reasoning-parser`, and only the final content is constrained. Batching is client-side concurrency (vLLM batches continuously): an `asyncio.Semaphore(cfg.max_concurrency)` (default 48) per model. The frozen system prompt sits first so prefix caching applies (06 §5).

```python
# packages/arena_llm/src/arena_llm/backends/vllm.py
import asyncio, json
import httpx
from jsonschema import Draft202012Validator
from openai import AsyncOpenAI, APIStatusError, APITimeoutError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

class InvalidJSON(Exception): ...

class VLLMClient:
    def __init__(self, cfg, structured: str = "structured_outputs"):
        self.cfg, self.mode = cfg, structured
        self.client = AsyncOpenAI(base_url=cfg.base_url, api_key=cfg.api_key or "EMPTY",
                                  timeout=httpx.Timeout(cfg.timeout_s, connect=10))
        self.sem = asyncio.Semaphore(cfg.max_concurrency)

    def _extra(self, schema: dict) -> dict:
        if self.mode == "response_format":
            return {"response_format": {"type": "json_schema",
                                        "json_schema": {"name": "out", "schema": schema, "strict": True}}}
        return {"extra_body": {"structured_outputs": {"json": schema}}}

    @retry(retry=retry_if_exception_type((APITimeoutError, APIStatusError, InvalidJSON, httpx.TransportError)),
           wait=wait_exponential_jitter(initial=2, max=60), stop=stop_after_attempt(4), reraise=True)
    async def _one(self, system: str, user: str, schema: dict, temperature: float, n: int) -> list[dict]:
        async with self.sem:
            r = await self.client.chat.completions.create(
                model=self.cfg.model, temperature=temperature, n=n, max_tokens=self.cfg.max_tokens,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                **self._extra(schema))
        outs, v = [], Draft202012Validator(schema)
        for ch in r.choices:
            try:
                obj = json.loads(ch.message.content)
            except (json.JSONDecodeError, TypeError) as e:
                raise InvalidJSON(str(e)) from e
            if errs := list(v.iter_errors(obj)):
                raise InvalidJSON(errs[0].message)
            outs.append(obj)
        return outs

    async def acomplete_json(self, *, prompt_id, prompt_version, system, user, schema, temperature=0.0, n=1):
        return await self._one(system, user, schema, temperature, n)

    def complete_json(self, **kw) -> list[dict]:
        return asyncio.run(self.acomplete_json(**kw))

    async def map_json(self, requests: list[dict]) -> list[list[dict] | Exception]:
        """Fan out many requests; the semaphore bounds concurrency. Used by stage tasks that process a whole
        episode's chunks at once to keep vLLM's batch full."""
        return await asyncio.gather(*(self.acomplete_json(**r) for r in requests), return_exceptions=True)
```

**Throughput practice.** Stage tasks for S7–S10 take *batches* (all chunks of an episode, or 64 claims) rather than single items, call `map_json`, and write results per item with per-item idempotency keys. Target concurrency is c ≈ 32–64 (06 §5).

### 5.3 `anthropic_api` (disabled by default)

Implemented so the bake-off and emergency escalations *can* use it, but `ARENA_ANTHROPIC_API_ENABLED` defaults to `false`. Enabling it also requires a row in `admin_approval(kind='paid_api', approved_by='benjamin', budget_usd, expires_at)`. Every call checks the remaining budget from `llm_call` token counts. JSON is obtained by forcing a single tool whose `input_schema` is the output schema.

```python
# packages/arena_llm/src/arena_llm/backends/anthropic_api.py
import anthropic
from arena_core.approvals import require_approval

class AnthropicAPI:
    def __init__(self, cfg):
        require_approval("paid_api")                    # raises unless an unexpired approval with budget exists
        self.cfg, self.client = cfg, anthropic.Anthropic(api_key=cfg.api_key.get_secret_value())

    def complete_json(self, *, prompt_id, prompt_version, system, user, schema, temperature=0.0, n=1):
        outs = []
        for _ in range(n):
            msg = self.client.messages.create(
                model=self.cfg.model, max_tokens=self.cfg.max_tokens, temperature=temperature, system=system,
                messages=[{"role": "user", "content": user}],
                tools=[{"name": "emit", "description": "Return the result.", "input_schema": schema}],
                tool_choice={"type": "tool", "name": "emit"})
            outs.append(next(b.input for b in msg.content if b.type == "tool_use"))
        return outs
```

`openai_compat` reuses `VLLMClient` with `response_format` (llama.cpp server, Ollama, LM Studio) for laptop smoke tests. `fake` replays fixtures keyed by `request_hash` for CI.

---

## 6. Job orchestration (Procrastinate)

### 6.1 App, queues, priorities

| Queue | Workers | Concurrency | Tasks |
|---|---|---|---|
| `schedule` | cpu | 1 | periodic fan-out tasks (nightly/weekly/monthly) |
| `discover` | cpu | 4 | S1, S2 |
| `fetch` | cpu | 1 (paced) | S4 |
| `asr` | gpu (nemo container) | 1 | S5 |
| `extract_cpu` | cpu | 4 | S6 |
| `llm` | cpu (I/O-bound to vLLM) | 6 tasks × 48 in-flight requests | S7, S9, S10, live-question jobs |
| `nli` | gpu or cpu | 1 | S8 (batched NLI + critic) |
| `embed` | gpu | 1 | re-embed jobs |
| `map` | cpu | 1 (lock `snapshot`) | S3, S11, S12, S14, audits |
| `publish` | cpu | 1 | S13 (approval-gated) |
| `ops` | cpu | 2 | sweeps, reports, backups, restore test |

Priority (higher runs first, per queue): event maps 100 > escalations/audits 50 > nightly new episodes 20 > backfill 0.

```python
# services/worker/src/worker/app.py
import httpx
from procrastinate import App, PsycopgConnector, RetryStrategy
from arena_core.config import settings

app = App(connector=PsycopgConnector(conninfo=settings.database_url.get_secret_value()),
          import_paths=["worker.tasks.ingest", "worker.tasks.extract", "worker.tasks.map",
                        "worker.tasks.reputation", "worker.tasks.ops", "worker.tasks.schedules"])

NET_RETRY = RetryStrategy(max_attempts=6, exponential_wait=15,
                          retry_exceptions={httpx.TransportError, httpx.HTTPStatusError, TimeoutError})
LLM_RETRY = RetryStrategy(max_attempts=4, exponential_wait=30)
NO_RETRY = RetryStrategy(max_attempts=1)
```

### 6.2 Stage tasks and fan-out

Each task: open or attach a run, call the package function inside `stage_once`, then defer the next stage with a **queueing lock** (one pending job per item and stage) and inherit the run id.

```python
# services/worker/src/worker/tasks/extract.py
from procrastinate import JobContext
from arena_core.db import session_scope
from arena_core.runs import attach_run
from arena_llm import get_client
from arena_llm.base import PendingBatch
from arena_extract import pipeline as X
from ..app import app, LLM_RETRY, NO_RETRY

@app.task(name="chunk_transcript", queue="extract_cpu", retry=NO_RETRY, pass_context=True)
def chunk_transcript(context: JobContext, transcript_id: str, run_id: str | None = None):
    with session_scope() as s:
        ctx = attach_run(s, run_id, stage="S6", job_name="chunk_transcript")
        chunk_ids = X.chunk_transcript(ctx, transcript_id)          # idempotent via stage_once
    for cid in chunk_ids:
        extract_claims.configure(queueing_lock=f"S7:{cid}", priority=context.job.priority or 0) \
                      .defer(chunk_id=cid, run_id=str(ctx.run_id))

@app.task(name="extract_claims", queue="llm", retry=LLM_RETRY, pass_context=True)
def extract_claims(context: JobContext, chunk_id: str, run_id: str | None = None):
    llm = get_client("extract")
    with session_scope() as s:
        ctx = attach_run(s, run_id, stage="S7", job_name="extract_claims", llm=llm)
        try:
            X.extract_claims(ctx, llm, chunk_id)
        except PendingBatch as p:
            X.park(ctx, item=("chunk", chunk_id), stage="S7", batch_id=p.batch_id)   # stage_item.detail.pending
            return                                                                 # resumed by collect_batches
    anchor_and_verify.configure(queueing_lock=f"S8:{chunk_id}").defer(chunk_id=chunk_id, run_id=run_id)

@app.task(name="anchor_and_verify", queue="nli", retry=NO_RETRY, pass_context=True)
def anchor_and_verify(context: JobContext, chunk_id: str, run_id: str | None = None):
    with session_scope() as s:
        ctx = attach_run(s, run_id, stage="S8", job_name="anchor_and_verify")
        X.anchor_and_verify(ctx, chunk_id)
    normalize_propositions.configure(queueing_lock=f"S9:{chunk_id}").defer(chunk_id=chunk_id, run_id=run_id)

@app.task(name="normalize_propositions", queue="llm", retry=LLM_RETRY, pass_context=True)
def normalize_propositions(context: JobContext, chunk_id: str, run_id: str | None = None): ...

@app.task(name="link_relations_layers", queue="llm", retry=LLM_RETRY, pass_context=True)
def link_relations_layers(context: JobContext, proposition_ids: list[str], run_id: str | None = None): ...
```

### 6.3 Parked work (`claude_code_batch`) and dead letters

- **Parked.** A `PendingBatch` leaves the `stage_item` as `started` with `detail.pending_batch`. The periodic `collect_batches` (every 15 min) checks `evals/results/<batch_id>/` and re-defers the parked stage tasks whose results now exist. Because results are keyed by `request_hash`, the re-run hits the result file and proceeds. A parked item older than its task `deadline` raises an operator alert.
- **Dead letter.** Procrastinate marks a job `failed` after `max_attempts`. The periodic `sweep_failed` (hourly) reads `procrastinate_jobs WHERE status = 'failed'` into the view `ops.dead_letter` (task name, args, last error, attempts), classifies the error (network / quota / blocked / schema / code bug / OOM), and posts new entries to the operator agent.
- **Requeue.** The operator requeues through the `/ops/requeue` action, which **defers a fresh job with the same args**. Idempotency keys make this safe.

```python
# services/worker/src/worker/tasks/ops.py
@app.periodic(cron="*/15 * * * *", periodic_id="collect_batches")
@app.task(name="collect_batches", queue="ops", retry=NO_RETRY)
def collect_batches(timestamp: int):
    for item in parked_items_with_results():          # joins stage_item.detail->>'pending_batch' with results dir
        TASKS[item.stage].configure(queueing_lock=f"{item.stage}:{item.item_id}").defer(**item.task_args)

@app.periodic(cron="7 * * * *", periodic_id="sweep_failed")
@app.task(name="sweep_failed", queue="ops", retry=NO_RETRY)
def sweep_failed(timestamp: int):
    with session_scope() as s:
        new = s.execute(SQL_NEW_FAILED_JOBS).all()     # procrastinate_jobs failed since last sweep, not yet in ops.dead_letter_seen
        for job in new:
            record_dead_letter(s, job, classify(job.error))
    notify_operator("dead_letter", [j.id for j in new]) if new else None
```

### 6.4 Locks and idempotency

- **Queueing locks** (`queueing_lock=f"{stage}:{item_id}"`) stop duplicate *pending* jobs for the same item.
- **Execution locks** (`lock="snapshot"`) serialize S11/S12/S13 so one snapshot is built at a time.
- **Advisory locks** inside S4 (`pg_advisory_xact_lock(hashtext('fetch:'||host))`) enforce per-host pacing across workers.
- **The `stage_item` ledger** (§4.0) makes every stage safe to re-run.
- **Content writes** use natural unique keys, so even a crash between write and ledger update cannot duplicate rows: `(platform, external_id)` for episodes, `(transcript_id, seq, model_version)` for chunks, `(person_id, proposition_id, episode_id, run_id)` for stances.

### 6.5 Schedules

All cron expressions are UTC (containers run `TZ=UTC`); comments give Mountain Time.

```python
# services/worker/src/worker/tasks/schedules.py
from ..app import app, NO_RETRY
from arena_core.config import settings

@app.periodic(cron="17 9 * * *", periodic_id="nightly")          # 02:17 MST
@app.task(name="nightly", queue="schedule", retry=NO_RETRY)
def nightly(timestamp: int):
    for lm in slice_landmarks():                                   # S1 delta: only new items since last crawl
        discover_landmark.configure(queueing_lock=f"S1:{lm}", priority=20).defer(landmark_id=lm, mode="delta")
    select_episodes.configure(queueing_lock="S3:nightly").defer(mode="incremental")   # baseline for new items
    # S4 runs continuously under its own pacing; S5 ASR window opens if box profile:
    if settings.gpu:
        open_asr_window.defer(hours=5)
    build_snapshot.configure(queueing_lock="S11:daily", lock="snapshot").defer(horizon="daily")
    ops_report.defer(kind="daily")

@app.periodic(cron="43 10 * * 0", periodic_id="weekly")         # Sunday 03:43 MST
@app.task(name="weekly", queue="schedule", retry=NO_RETRY)
def weekly(timestamp: int):
    live_question_battery.defer(week=iso_week(timestamp))          # claude_code_batch; parks until processed
    audit_sample.defer(rate=0.02)                                  # 2% random accepted claims → Claude audit
    chain = build_snapshot.configure(queueing_lock="S11:weekly", lock="snapshot")
    chain.defer(horizon="weekly", then=["score_reputation", "weather_report"])   # S12, then report draft
    # S13 publish is NOT scheduled: it runs when Benjamin approves the snapshot (or under a standing approval after P5)

@app.periodic(cron="11 11 1 * *", periodic_id="monthly")        # 1st of month 04:11 MST
@app.task(name="monthly", queue="schedule", retry=NO_RETRY)
def monthly(timestamp: int):
    reembed_bank.defer()                                           # current embedder over the whole bank
    rededup_bank.defer()                                           # proposition merges with fresh candidates
    build_snapshot.configure(queueing_lock="S11:monthly", lock="snapshot").defer(horizon="monthly", refit_axes=True)
    eval_models_on_gold.defer()                                    # bake-off for new open releases
    retrain_classifiers.defer()                                    # from corrections and "that's not me" labels
    agent_free_refit.defer()                                       # P6
    restore_test.defer()                                           # backup restore into a scratch DB
    prune_retention.defer()                                        # transcripts past retention_until
```

---

## 7. API (FastAPI, `services/api`)

### 7.1 Conventions

- JSON over HTTPS, versioned under `/v1`. Request and response models are the Pydantic contracts (TS types generated from them).
- Reads that the static bundle already serves are **not** duplicated in the API except where personalization is needed (my placement, my contributions).
- Errors use RFC 9457 problem+json. Pagination uses `?cursor=&limit=` (max 200).
- Every write is one transaction that writes the row plus an `event_log` entry.

### 7.2 Endpoints

| Area | Method + path | Auth / tier | Request → response (summary) |
|---|---|---|---|
| Map | `GET /v1/snapshots/latest` | public | → `{snapshot, bundle_base, as_of}` |
| | `GET /v1/me/placement` | T1 | → `{snapshot, coords:[x,y], uncertainty, memberships:[{cluster_id, weight}], nearest_landmarks:[3], threshold:{between:[c1,c2]}, twist:{landmark_id, statement_id}, eligible_to_ratify}` |
| Clusters | `GET /v1/clusters/{id}` | public | live counterpart of bundle card, for the current snapshot only |
| | `GET /v1/clusters/{a}/pair/{b}` | public | → `{u_ab, u_ba, n, ratified_notes:[…], live_questions:[…], encounters:[…]}` |
| Landmarks | `GET /v1/landmarks/{id}` | public | → card (excluded landmarks → 404) |
| | `POST /v1/landmarks/{id}/annotations` | T3 + `landmark_id` claim | `{text, target_type, target_id}` → `flag(kind='landmark_annotation')` |
| Propositions | `GET /v1/propositions/{public_id}` | public | → canonical, layer, relations, clips (`quote_public`, `deep_link`) |
| | `GET /v1/search?q=` | public | trigram + vector search over propositions |
| Statements | `GET /v1/statements/next?session=` | public/T1 | → next statement by expected information gain (server version of §4.11.1) |
| Reactions | `POST /v1/reactions` | T1 (T0 batches on sign-up) | `{statement_id, vote, guess_person_id?, consent_version}` → `{placement?}` (recomputed with cached item params) |
| | `POST /v1/reactions/import` | T1 | upload the T0 local reactions after sign-up |
| Contributions | `POST /v1/contributions` | T2 (T1 for notes in beta, configurable) | `{kind, target_cluster_id, second_cluster_id?, synthesis_subtype?, body, cited_claim_ids[], live_question_id?}` → `{contribution_id, status:'needs_ratings'}`; rejected if writing-locked |
| | `GET /v1/contributions?target=&status=` | public | list (author handles only if opted in) |
| | `GET /v1/me/contributions` | T1 | own contributions with scores |
| Ratings | `GET /v1/me/rating-queue` | T2, person | → sampled contributions to rate (fidelity invitations for my cluster first) |
| | `POST /v1/ratings` | T2, person, `eligible_to_ratify` | `{contribution_id, helpfulness, fidelity?, tags[]}` → `204`; DB trigger enforces no agents, no self-rating, fidelity only from B |
| Reputation | `GET /v1/reputation/{handle}` | public (opt-in profiles) | → `{reputation, writer_impact, rating_impact, rater_helpfulness, synthesis_credit, history[]}` |
| | `GET /v1/leaderboards?kind=person|agent&pair=` | public | top 50 numbered, per cluster pair by default, opt-in handles only (SPINE §10 safeguards; bundle has the same) |
| Live questions | `GET /v1/live-questions?state=` · `GET /v1/live-questions/{id}` | public | lifecycle, axes, linked propositions, contributions |
| Event maps | `GET /v1/events/{episode_id}` | public after approval | → speakers, starting positions, met/diverged by layer, missed openings, ripple |
| Agents (P6) | `POST /v1/agents` | T3 operator | `{name, model_disclosure, charter_version, platforms[]}` → `{agent_id, api_token (scoped)}` |
| | `GET /v1/agents` · `GET /v1/agents/{id}` | public | public registry entry, leaderboard, audit status |
| | `POST /v1/agents/{id}/actions` | agent token | `{type, target_user_id?, invoked_by_user, …}` → charter hooks → `{allowed, reasons[]}` |
| Market (P6) | `GET /v1/strategies` · `GET /v1/windows/{id}` | public | strategies, assignments (after seed reveal) |
| | `POST /v1/forecasts` | T2 | `{window_id, question_key, commitment}` → `{forecast_id}` (before window opens) |
| | `POST /v1/forecasts/{id}/reveal` | T2 | `{payload, salt}` → `{reveal_valid}` (after window closes) |
| Flags | `POST /v1/flags` | T1 (landmarks/rights holders via verified email) | `{kind, target_type, target_id, text}` → `{flag_id, sla_due_at}` |
| Auth | `POST /v1/auth/magic-link` · `GET /v1/auth/callback` · `POST /v1/auth/passkey/register/{begin,finish}` · `POST /v1/auth/passkey/login/{begin,finish}` · `POST /v1/auth/logout` | public | sessions as HttpOnly, Secure, SameSite=Lax cookies |
| | `POST /v1/personhood/vouch` | T2 | `{vouchee_handle}` |
| Admin | `POST /v1/admin/snapshots/{id}/approve` | admin (Benjamin, passkey + step-up) | → status `approved`, triggers S13 |
| | `GET/PATCH /v1/admin/flags` | admin | triage, resolve, annotate |
| | `POST /v1/admin/approvals` | admin | paid API, public launch, standing weekly approval, YouTube audio per channel |
| Ops | `GET /v1/ops/status` · `POST /v1/ops/{requeue,pause_queue,resume_queue,trigger_job}` | operator token (Hermes) | allow-listed actions only (§10.7) |

### 7.3 Auth and the personhood tier model

| Tier | How it is reached | Can |
|---|---|---|
| **T0 visitor** | nothing | react in the browser (first 60 seconds); placement computed client-side from the bundle; nothing stored server-side |
| **T1 account** | email magic link (15-min single-use token, hashed at rest) + 18+ age attestation + reactions consent | store reactions (count toward own placement); flag; write notes in beta if enabled |
| **T2 ratifier** | T1 + a **passkey** (WebAuthn, `py_webauthn`) + account age ≥ 7 days + ≥ 12 non-pass reactions + **one personhood proof**: (a) vouches from two T2+ users in different clusters (vouchers lose reputation if a vouchee is later found coordinated); (b) an in-person check at an Arena event; or (c) an external proof-of-personhood attestation (e.g. a Human Passport / BrightID-style score; integration needs Benjamin's approval and a privacy review; providers UNVERIFIED; **OD-16**) | write contributions; rate (portability); rate fidelity when placed in the described cluster; forecast |
| **T3 verified public identity** | T2 + proof of control of a public identity (DNS TXT on own domain, a signed post on a public profile, or OAuth to own YouTube channel) | operate arena agents (operator verification method: **OD-16**); claim a landmark profile and annotate |
| **agent** | created by a T3 operator | act via scoped token: contribute (own leaderboard), reply when invoked; **never** react-for-placement, rate or forecast |

`app_user.personhood_tier` is derived from `personhood_methods` by a pure function and re-evaluated on every change. It is never set by hand except by an admin action, which is logged.

```python
# services/api/src/api/deps.py
from fastapi import Depends, HTTPException, Request, status

def require_tier(min_tier: int, person_only: bool = True):
    async def dep(request: Request, user=Depends(current_user)):
        if user is None or user.suspended_at is not None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        if person_only and user.kind != "person":
            raise HTTPException(status.HTTP_403_FORBIDDEN, "agents cannot perform this action")
        if user.personhood_tier < min_tier:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"personhood tier {min_tier} required")
        await rate_limit(request, user)
        return user
    return dep

@router.post("/v1/ratings", status_code=204)
async def post_rating(body: RatingIn, user=Depends(require_tier(2)), db=Depends(db_session)):
    m = await db.current_membership(user.user_id)
    if not m or not m.eligible_to_ratify:
        raise HTTPException(403, "react to more statements to be placed before rating")
    await db.insert_rating(body, user, m)          # DB trigger re-checks every rule (defence in depth)
```

### 7.4 Rate limits

Token buckets in Postgres (one row per key; `SELECT … FOR UPDATE`), so limits hold across API processes without Redis:

| Key | Capacity / refill |
|---|---|
| `ip:signup` | 5 / hour |
| `ip:magic-link` | 5 / hour, plus per-email 3 / hour |
| `user:reaction` | 120 / hour |
| `user:contribution` | T1: 2 / day; T2: 5 / day (writing lock overrides) |
| `user:rating` | 60 / day |
| `user:flag` | 20 / day |
| `agent:action` | per charter, default 30 / day, and only when `invoked_by_user` |
| `ops:*` | 60 / hour |

```sql
CREATE TABLE rate_bucket (key text PRIMARY KEY, tokens real NOT NULL, updated_at timestamptz NOT NULL);
CREATE FUNCTION take_token(k text, capacity real, refill_per_s real) RETURNS boolean LANGUAGE plpgsql AS $$
DECLARE t real; u timestamptz;
BEGIN
  INSERT INTO rate_bucket VALUES (k, capacity, now()) ON CONFLICT (key) DO NOTHING;
  SELECT tokens, updated_at INTO t, u FROM rate_bucket WHERE key = k FOR UPDATE;
  t := least(capacity, t + extract(epoch FROM now() - u) * refill_per_s);
  IF t < 1 THEN UPDATE rate_bucket SET tokens = t, updated_at = now() WHERE key = k; RETURN false; END IF;
  UPDATE rate_bucket SET tokens = t - 1, updated_at = now() WHERE key = k; RETURN true;
END $$;
```

---

## 8. Web app (`apps/web`)

### 8.1 Stack and data sources

- Next.js 15 App Router, TypeScript strict, Tailwind. The repo's `AGENTS.md` warns that the installed Next.js may differ from training data: read `node_modules/next/dist/docs/` before writing routes. In recent versions `params`/`searchParams` are Promises, and `middleware` may be renamed `proxy`.
- **Reads:** static snapshot bundles (`NEXT_PUBLIC_BUNDLE_BASE`), fetched in Server Components with `fetch(url, { cache: 'force-cache' })` for immutable files and `{ next: { revalidate: 60 } }` for `latest.json`. Pages are statically generated per snapshot where possible (`generateStaticParams` over `map.json` ids).
- **Writes and personal data:** the API, from Client Components, with cookies (`credentials: 'include'`).
- Generated types from `contracts/ts` are the only shared code with Python.

### 8.2 Routes

| Route | Purpose |
|---|---|
| `/` | Living map: terrain, cluster hulls, live questions rail (the core object), weekly weather summary |
| `/start` | First 60 seconds (§8.4) |
| `/q/[questionId]` | Live question: lifecycle, per-question axes view, contributions, statements to react to |
| `/c/[clusterId]` | Cluster card: what it affirms/rejects by layer, landmarks, crosswalk to niches, U row/column, ratified descriptions of it |
| `/c/[a]/[b]` | Cluster pair: U[a][b] and U[b][a], ratified notes both ways, clean disagreements, encounters, "conversations that haven't happened yet" |
| `/l/[landmarkId]` | Landmark: placement, stances with clips (stated only; inferred labelled), panel status, dispute/annotate |
| `/p/[publicId]` | Proposition: canonical, layer, relations, per-cluster affirm share, source clips |
| `/e/[episodeId]` | Event map |
| `/write` · `/rate` | Contribution editor (note/steelman/synthesis); rating queue |
| `/u/[handle]` · `/leaderboards` · `/agents` · `/agents/[id]` · `/market` | Reputation profiles; person and agent leaderboards; agent registry; strategy market |
| `/about/method` · `/about/landmarks` | Published method, selection rules, core panel, newcomers (red line 12) |
| `/flag` | Dispute/takedown form (also linked from every landmark, clip and proposition) |
| `/admin/*` | Snapshot approval, flags triage (passkey + step-up) |

### 8.3 Component tree and map rendering

```
app/layout.tsx
└─ <BundleProvider snapshot>                  # loads manifest + map.json; exposes typed selectors
   ├─ <MapCanvas>                              # deck.gl, OrthographicView (2-D layout space, not geo)
   │   ├─ PolygonLayer   cluster hulls (convex hull of member coords, padded)
   │   ├─ ScatterplotLayer landmarks (radius by panel status; newcomers outlined)
   │   ├─ ScatterplotLayer users (aggregated heat at k ≥ 50, never individual dots except "you")
   │   ├─ LineLayer      encounters (on demand)
   │   └─ TextLayer      cluster labels (provisional styling until ratified)
   ├─ <LiveQuestionRail>                       # questions ranked by reciprocal opening, not engagement
   ├─ <DrillPanel>                             # map → cluster → landmark → proposition → clip
   │   └─ <ClipLink quote deepLink />          # ≤ 1 sentence + timestamped link out
   ├─ <PairView a b />                         # U cells, ratified notes, clean disagreements
   └─ <YouDot />                               # the user's own placement (client state)
```

**Renderer choice (ADR-011).** deck.gl for the terrain: WebGL instanced layers handle ~10³ nodes trivially and 10⁵ points at interactive frame rates with binary attributes (`data.attributes` typed arrays), with picking for hover. Sigma.js (graphology) is used for *graph* views where force layout and edge rendering matter: lineage, the proposition relation neighbourhood, the encounter graph. At 10⁵ scale the bundle ships points as a binary `Float32Array` file (`map.points.bin`) plus a sidecar index, and hulls are precomputed server-side.

```tsx
// apps/web/components/MapCanvas.tsx
'use client';
import DeckGL from '@deck.gl/react';
import { OrthographicView } from '@deck.gl/core';
import { PolygonLayer, ScatterplotLayer, TextLayer } from '@deck.gl/layers';
import type { MapBundle } from '@/contracts/ts/MapBundle';

export function MapCanvas({ map, you, onPick }: { map: MapBundle; you?: [number, number]; onPick: (id: string) => void }) {
  const layers = [
    new PolygonLayer({ id: 'hulls', data: map.clusters, getPolygon: (c) => c.hull,
      getFillColor: (c) => [...c.color, 40], getLineColor: (c) => [...c.color, 160], lineWidthMinPixels: 1,
      pickable: true, onClick: ({ object }) => object && onPick(`c:${object.id}`) }),
    new ScatterplotLayer({ id: 'landmarks', data: map.landmarks, getPosition: (l) => l.xy,
      getRadius: (l) => (l.panel === 'newcomer' ? 5 : 7), radiusUnits: 'pixels',
      getFillColor: (l) => map.clusterColor[l.cluster], stroked: true,
      getLineColor: (l) => (l.panel === 'newcomer' ? [20, 20, 20, 255] : [0, 0, 0, 0]),
      pickable: true, onClick: ({ object }) => object && onPick(`l:${object.id}`) }),
    new TextLayer({ id: 'labels', data: map.clusters, getPosition: (c) => c.centroid, getText: (c) => c.label,
      getSize: 14, getColor: (c) => (c.labelStatus === 'provisional' ? [90, 90, 90] : [10, 10, 10]) }),
    ...(you ? [new ScatterplotLayer({ id: 'you', data: [you], getPosition: (d) => d, getRadius: 9,
      radiusUnits: 'pixels', getFillColor: [0, 0, 0], stroked: true, getLineColor: [255, 255, 255] })] : []),
  ];
  return <DeckGL views={new OrthographicView({ flipY: false })} controller layers={layers}
                 initialViewState={{ target: [0, 0, 0], zoom: 5 }} />;
}
```

### 8.4 First-60-seconds flow (state machine)

Steps (memo §8): react to statements → land as a dot → nearest three landmarks → threshold reveal → twist card → invitation to describe the farthest cluster. It runs entirely client-side for T0 visitors from the bundle's `statements.json` (item parameters and `p_affirm`). Nothing leaves the browser until the visitor signs up and consents.

```ts
// apps/web/lib/onboarding.ts
import { clusterPosterior, nextStatement, placeUser, nearestLandmarks, twistCard, farthestCluster }
  from './placement';                       // TS ports of the §4.11 functions, operating on the bundle
import type { StatementsBundle } from '@/contracts/ts/StatementsBundle';

export type Vote = 'agree' | 'disagree' | 'pass';
type Ctx = { asked: number[]; votes: Record<number, Vote>; posterior: number[]; xy?: [number, number] };

export type State =
  | { tag: 'intro' }
  | { tag: 'reacting'; ctx: Ctx; current: number }
  | { tag: 'landing'; ctx: Ctx }
  | { tag: 'nearest'; ctx: Ctx; landmarks: string[] }
  | { tag: 'threshold'; ctx: Ctx; between: [number, number] | null }
  | { tag: 'twist'; ctx: Ctx; landmarkId: string; statement: number }
  | { tag: 'invite'; ctx: Ctx; farthestCluster: number }
  | { tag: 'signup'; ctx: Ctx };

export type Event = { type: 'START' } | { type: 'VOTE'; vote: Vote } | { type: 'NEXT' } | { type: 'SIGN_UP' };

const MIN_VOTES = 8, MAX_VOTES = 12, CONFIDENT = 0.8, STRADDLE = 0.3;

function straddle(post: number[]): [number, number] | null {
  const [a, b] = post.map((p, i) => [p, i] as const).sort((x, y) => y[0] - x[0]);
  return b && b[0] >= STRADDLE ? [a[1], b[1]] : null;          // "you sit between these two"
}

export function reduce(s: State, e: Event, b: StatementsBundle): State {
  switch (s.tag) {
    case 'intro': {
      if (e.type !== 'START') return s;
      const prior = b.clusterPrior;                            // uniform over clusters by default
      return { tag: 'reacting', ctx: { asked: [], votes: {}, posterior: prior },
               current: nextStatement(b, prior, []) };
    }
    case 'reacting': {
      if (e.type !== 'VOTE') return s;
      const votes = { ...s.ctx.votes, [s.current]: e.vote };
      const asked = [...s.ctx.asked, s.current];
      const posterior = clusterPosterior(b, votes);
      const nonPass = Object.values(votes).filter((v) => v !== 'pass').length;
      const ctx: Ctx = { asked, votes, posterior };
      if ((nonPass >= MIN_VOTES && Math.max(...posterior) >= CONFIDENT) || asked.length >= MAX_VOTES) {
        return { tag: 'landing', ctx: { ...ctx, xy: placeUser(b, votes) } };
      }
      return { tag: 'reacting', ctx, current: nextStatement(b, posterior, asked) };
    }
    case 'landing':
      return e.type === 'NEXT' ? { tag: 'nearest', ctx: s.ctx, landmarks: nearestLandmarks(b, s.ctx.xy!, 3) } : s;
    case 'nearest':
      return e.type === 'NEXT' ? { tag: 'threshold', ctx: s.ctx, between: straddle(s.ctx.posterior) } : s;
    case 'threshold':
      return e.type === 'NEXT' ? { tag: 'twist', ctx: s.ctx, ...twistCard(b, s.ctx.votes, s.ctx.xy!) } : s;
    case 'twist':
      return e.type === 'NEXT' ? { tag: 'invite', ctx: s.ctx, farthestCluster: farthestCluster(b, s.ctx.xy!) } : s;
    case 'invite':
      return e.type === 'SIGN_UP' ? { tag: 'signup', ctx: s.ctx } : s;   // then POST /v1/reactions/import
    default:
      return s;
  }
}
```

The **twist card** is "the landmark farthest from you whom you most resemble on one question": among landmarks in the cluster farthest from the user, find a statement where the user's vote matches that landmark's stance (stated, publishable, `public_surface_allowed`), preferring `surprising_unifier` statements. The **invitation** opens `/write?kind=note&target=<farthest>` after sign-up. The final screen is an invitation, not a score (memo §8).

### 8.5 Accessibility and copy rules

WCAG 2.2 AA: every map interaction has a list equivalent (clusters → landmarks → propositions as navigable lists). Copy follows the no-slop rules of Topology Live (no filler, no unverifiable numbers). Clusters are never ranked or coloured on a good/bad scale (red line 15).

---

## 9. Agents (P6) and the strategy market (P6)

### 9.1 Agents (`arena_agents`)

**Registry.** An `agent` row plus a public registry entry (JSON, content-hashed into `registry_hash`) with:
- name and operator handle (T3);
- model disclosure, charter version, assigned strategy, platforms and handles;
- prompt hash and the published full prompt, versioned (PRD-AGT-01);
- reward eligibility and audit history.

The registry is published in every bundle (`agents.json`) and as `/agents`. Changes are events, so the ledger is append-only and public.

**Operator binding.** `agent.operator_user_id` must be a T3 person. An operator may run at most 3 agents (configurable). An agent's reputation is shown on the agent leaderboard *and* on the operator's profile ("operates: …"). If the operator is suspended, their agents are suspended.

**Charter enforcement hooks.** Every agent action goes through `POST /v1/agents/{id}/actions` before it happens (Arena-native actions) or is reported there (off-platform actions, e.g. an X reply). Hooks are pure functions returning `(allowed, reasons)`; all results are stored in `agent_action.charter_checks`.

```python
# packages/arena_agents/src/arena_agents/charter.py
from dataclasses import dataclass

@dataclass
class ActionCtx:
    agent: "Agent"; type: str; invoked_by_user: bool; target_user_id: str | None
    platform: str; body: str | None; daily_count: int; target_engaged_first: bool

def disclosed(a: ActionCtx):           # A1: identifies as AI, names operator, links registry
    ok = a.body is None or ("[AI agent" in a.body and a.agent.registry_url in a.body)
    return ok, "A1: missing disclosure footer"

def no_unsolicited(a: ActionCtx):      # A3: engage only people who invoked it / opted in
    if a.type in ("reply", "dm_reply", "invite") and not a.invoked_by_user:
        return False, "A3: target did not invoke the agent"
    if a.platform == "x" and not a.target_engaged_first:
        return False, "X automation rules: contact only after the person engages first"
    return True, ""

def no_ratify(a: ActionCtx):           # D-31.3: agents never ratify or rate
    return a.type not in ("rating", "fidelity_vote", "reaction_for_placement"), "agents never ratify"

def rate_cap(a: ActionCtx):
    return a.daily_count < a.agent.daily_cap, "daily action cap reached"

def eligible(a: ActionCtx):
    return a.agent.status == "active", "agent not active"

HOOKS = [eligible, disclosed, no_unsolicited, no_ratify, rate_cap]

def check(a: ActionCtx) -> tuple[bool, list[str]]:
    reasons = [msg for hook in HOOKS for ok, msg in [hook(a)] if not ok]
    return not reasons, reasons
```

Content-level checks (no fabricated personas or lived experience, A2; no tribe-targeted framing of non-participants, A4) are classifier checks on the body, run by `arena_agents.content_guard` with the local LLM. Failures block the action and add a strike; 3 strikes in 30 days suspend the agent pending review.

**Directional-shift audit.** Agents that consistently move people toward one view lose reward eligibility (D-31.3). For agent *a* in window *W*:
1. Treated users: those with ≥ 1 invoked interaction with *a* in *W* and ≥ 8 reactions both before and after the first interaction.
2. For each treated user, Δx = position after − position before (ideal points in the snapshot's layout, both computed with the same item parameters) and Δp = the change in cluster posterior.
3. Controls: users matched on starting cluster and activity level, with no agent interactions in *W* (nearest neighbours on pre-position + reaction count).
4. Shift vector `s_a = mean(Δx_treated) − mean(Δx_control)`. Consistency: the fraction of treated users whose Δx projects positively on `s_a/‖s_a‖`.
5. Fail if `‖s_a‖ ≥ 0.15 × (median inter-cluster centroid distance)`, consistency ≥ 0.7, and a permutation test (treated/control labels shuffled 2,000 times) gives p < 0.01, with n_treated ≥ 30. Failing removes reward eligibility for the next window (not a ban) and is published on the registry entry.

Note the asymmetry the design wants: moving people toward *understanding* (better fidelity ratings of the other side, more accurate notes) is rewarded via reputation, while moving people's *positions* in one direction is what the audit penalizes.

```python
# packages/arena_agents/src/arena_agents/audit.py
import numpy as np

def directional_shift(dx_treated: np.ndarray, dx_control: np.ndarray, scale: float,
                      n_perm: int = 2000, seed: int = 0) -> dict:
    """dx_*: (n, 2) position changes. scale: median inter-centroid distance of the snapshot."""
    rng = np.random.default_rng(seed)
    s = dx_treated.mean(0) - dx_control.mean(0)
    norm = float(np.linalg.norm(s))
    unit = s / (norm + 1e-12)
    consistency = float((dx_treated @ unit > 0).mean())
    pooled = np.vstack([dx_treated, dx_control]); nt = len(dx_treated)
    null = np.empty(n_perm)
    for i in range(n_perm):
        idx = rng.permutation(len(pooled))
        null[i] = np.linalg.norm(pooled[idx[:nt]].mean(0) - pooled[idx[nt:]].mean(0))
    p = float((null >= norm).mean())
    fail = nt >= 30 and norm >= 0.15 * scale and consistency >= 0.7 and p < 0.01
    return {"shift": s.tolist(), "magnitude": norm / scale, "consistency": consistency, "p": p, "fail": fail}
```

**Agent-free re-fit.** Before any snapshot is released after P6, S11 runs twice:
- normally;
- with `agent_free=true`, which excludes reactions with `agent_provenance`, contributions and ratings from agent-led interactions, and any claims or stances derived from agent-hosted dialogue.

The release gate compares the two: ARI(clusters) ≥ 0.9 on landmarks, max |ΔU| ≤ 0.1, and identical eligibility for ≥ 98% of users. A failure blocks publication and opens an operator incident with the diff; the steward may then approve publishing the agent-free variant instead (PRD-SAFE-09). Tolerances are open decision **OD-24**. The published bundle carries both U matrices.

### 9.2 Strategy market (`arena_market`) and S14 `resolve_forecasts`

**Objects.**
- `strategy`: a published policy, e.g. `steelman_first` (open by stating the other cluster's strongest case and asking for correction) or `shared_question` (open with a live question both clusters care about).
- `strategy_assignment`: which strategy runs on which cluster pair in which window.
- `forecast`: a sealed prediction.

**Randomized assignment (Slice 1: simple).** For each window (4 weeks) and each eligible cluster pair (both clusters have ≥ 30 eligible raters), assign one strategy uniformly at random from the active set, blocked so each strategy gets an equal number of pairs. Agents opt into strategies; each pair gets the agents registered for its strategy.

The seed is committed before forecasts open: `commitment = sha256(seed)`, published with the window. `seed = sha256(bundle_sha256(snapshot at window open) || window_id || secret_nonce)`, and `secret_nonce` is revealed at window close so anyone can recompute the assignment. Randomization is what makes the outcome a causal estimate (D-31.2 open question, **OD-08**: recommended yes, simple in Slice 1).

**Forecast questions.** Generated per window from assignments, e.g.:
- `dU:<strategy>:<A>:<B>`: the change in `U[A][B] + U[B][A]` over the window for pairs assigned the strategy (continuous);
- `win:<s1>:<s2>`: whether strategy s1's mean ΔU beats s2's (binary);
- `dRep:<agent>`: an agent's reputation change.

**Sealed forecasts (commit–reveal).**
- **Commit** (before window open): `commitment = sha256(canonical_json(payload) || salt)`, where `payload = {question_key, kind: "binary"|"quantiles", p | q10,q50,q90, user_id, window_id}`.
- **Reveal** (after window close, before resolution): the user posts payload and salt; the server recomputes the hash. Unrevealed forecasts score as the worst score (prevents selective revealing). The commitment alone reveals nothing, so forecasts cannot herd.

**Resolution (S14).** The resolution value is computed **only** from the scorer's U and reputation tables (no separate referee, D-31.2), using the `agent_free=false` U, since agents' effect is the thing being measured, and the scorer run at window close + 7 days so ratings can settle.

Scoring uses strictly proper rules:
- Binary: the **Brier score** (reported as `1 − Brier` so higher is better).
- Quantile forecasts: the **pinball (quantile) loss** averaged over q10/q50/q90, which approximates CRPS. It is normalized per question by the spread of all forecasts so questions are comparable.

Payouts are a public forecast record on a separate *forecaster* track (it does not feed the single reputation score unless Benjamin decides otherwise, OD-25) and prizes, never money; no token (spine §9).

```python
# packages/arena_market/src/arena_market/forecast.py
import hashlib, hmac, json

def commitment(payload: dict, salt: str) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode() + salt.encode()
    return hashlib.sha256(blob).hexdigest()

def verify_reveal(stored_commitment: str, payload: dict, salt: str) -> bool:
    return hmac.compare_digest(stored_commitment, commitment(payload, salt))

def brier_skill(p: float, outcome: int) -> float:
    return 1.0 - (p - outcome) ** 2                       # strictly proper; higher is better

def pinball(qs: dict[float, float], y: float) -> float:
    return sum(max(q * (y - v), (q - 1) * (y - v)) for q, v in qs.items()) / len(qs)

def score_forecast(payload: dict, y: float, scale: float) -> float:
    if payload["kind"] == "binary":
        return brier_skill(payload["p"], int(y))
    qs = {0.1: payload["q10"], 0.5: payload["q50"], 0.9: payload["q90"]}
    return -pinball(qs, y) / max(scale, 1e-6)              # higher is better
```

```python
# packages/arena_market/src/arena_market/resolve.py  (S14 resolve_forecasts)
def resolve_window(ctx, window_id: str) -> None:
    w = load_window(ctx, window_id)
    U0 = load_U(ctx, snapshot_at(ctx, w.start), agent_free=False)
    U1 = load_U(ctx, snapshot_at(ctx, w.end_plus_settle), agent_free=False)
    outcomes = {}
    for a in w.assignments:
        d = (U1[a.cluster_a, a.cluster_b] + U1[a.cluster_b, a.cluster_a]) - \
            (U0[a.cluster_a, a.cluster_b] + U0[a.cluster_b, a.cluster_a])
        outcomes[f"dU:{a.strategy}:{a.cluster_a}:{a.cluster_b}"] = d
    by_strategy = group_mean(outcomes)                       # mean ΔU per strategy (the causal estimate)
    for s1, s2 in pairs(by_strategy):
        outcomes[f"win:{s1}:{s2}"] = float(by_strategy[s1] > by_strategy[s2])
    for f in forecasts_for(ctx, window_id):
        y = outcomes.get(f.question_key)
        if y is None: continue
        if not f.reveal_valid:
            score = worst_score(f.question_key)
        else:
            score = score_forecast(f.revealed_payload, y, spread_of_forecasts(f.question_key))
        save_score(ctx, f.forecast_id, y, score)
    publish_strategy_effects(ctx, window_id, by_strategy)    # the accumulating causal knowledge base
```

---

## 10. Infrastructure

### 10.1 docker-compose (both profiles)

```yaml
# infra/docker-compose.yml
name: dialogos-arena
x-app-env: &app-env
  ARENA_DATABASE_URL: postgresql://arena:${PG_PASSWORD}@postgres:5432/arena
  ARENA_OBJECT_STORE_URL: http://minio:9000
  ARENA_PROFILE: ${ARENA_PROFILE:-cloud-dev}
  TZ: UTC

services:
  postgres:
    image: pgvector/pgvector:0.8.0-pg16          # pin by digest in production
    profiles: [cloud-dev, box]
    environment: { POSTGRES_USER: arena, POSTGRES_PASSWORD: ${PG_PASSWORD}, POSTGRES_DB: arena }
    command: ["postgres", "-c", "shared_buffers=4GB", "-c", "max_connections=200",
              "-c", "wal_level=replica", "-c", "archive_mode=on",
              "-c", "archive_command=pgbackrest --stanza=arena archive-push %p"]
    volumes: [pgdata:/var/lib/postgresql/data, ./pgbackrest:/etc/pgbackrest:ro]
    healthcheck: { test: ["CMD-SHELL", "pg_isready -U arena"], interval: 10s }

  minio:
    image: minio/minio:RELEASE.2025-09-07T16-13-09Z
    profiles: [cloud-dev, box]
    command: server /data --console-address ":9001"
    environment: { MINIO_ROOT_USER: arena, MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD} }
    volumes: [minio:/data]

  migrate:
    build: { context: .., dockerfile: infra/Dockerfile.app }
    profiles: [cloud-dev, box]
    command: ["uv", "run", "alembic", "-c", "packages/arena_core/alembic.ini", "upgrade", "head"]
    environment: *app-env
    depends_on: { postgres: { condition: service_healthy } }

  api:
    build: { context: .., dockerfile: infra/Dockerfile.app }
    profiles: [cloud-dev, box]
    command: ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
    environment: *app-env
    ports: ["127.0.0.1:8000:8000"]                  # exposed publicly only via the tunnel (ADR-014)
    depends_on: [migrate]

  worker-cpu:
    build: { context: .., dockerfile: infra/Dockerfile.app }
    profiles: [cloud-dev, box]
    command: ["uv", "run", "procrastinate", "--app=worker.app.app", "worker",
              "--queues=schedule,discover,fetch,extract_cpu,llm,map,publish,ops", "--concurrency=8"]
    environment:
      <<: *app-env
      ARENA_LLM_ROLES: ${ARENA_LLM_ROLES:-config/llm.cloud-dev.yaml}
    volumes: [../evals:/srv/arena/evals]            # claude_code_batch queue/results
    depends_on: [migrate]

  worker-gpu:
    build: { context: .., dockerfile: infra/Dockerfile.nemo }   # FROM nvcr.io/nvidia/pytorch:25.11-py3 + nemo_toolkit[asr]
    profiles: [box]
    command: ["procrastinate", "--app=worker.app.app", "worker", "--queues=asr,nli,embed", "--concurrency=1"]
    environment: { <<: *app-env, ARENA_GPU: "1", HF_TOKEN_FILE: /run/secrets/hf_token }
    secrets: [hf_token]
    deploy: { resources: { reservations: { devices: [{ driver: nvidia, count: all, capabilities: [gpu] }] } } }

  vllm-main:
    image: ${VLLM_IMAGE}                             # Spark-specific recipe image, pinned by digest (06 §1.4)
    profiles: [box]
    command: ["vllm", "serve", "${MAIN_MODEL}", "--served-model-name", "main",
              "--gpu-memory-utilization", "${MAIN_GPU_UTIL:-0.55}", "--max-model-len", "16384",
              "--max-num-seqs", "64", "--enable-prefix-caching", "--port", "8001"]
    ipc: host
    volumes: [hf-cache:/root/.cache/huggingface]
    deploy: { resources: { reservations: { devices: [{ driver: nvidia, count: all, capabilities: [gpu] }] } } }

  vllm-embed:
    image: ${VLLM_IMAGE}
    profiles: [box]
    command: ["vllm", "serve", "Qwen/Qwen3-Embedding-4B", "--served-model-name", "embed",
              "--task", "embed", "--gpu-memory-utilization", "0.08", "--port", "8002"]
    volumes: [hf-cache:/root/.cache/huggingface]
    deploy: { resources: { reservations: { devices: [{ driver: nvidia, count: all, capabilities: [gpu] }] } } }

  operator:
    image: ${HERMES_IMAGE}                           # Hermes Agent, pinned
    profiles: [box]
    environment:
      OPENAI_BASE_URL: http://vllm-main:8001/v1      # or a small resident model (gpt-oss-20b)
      ARENA_OPS_URL: http://api:8000/v1/ops
      ARENA_OPS_TOKEN_FILE: /run/secrets/ops_token
      ARENA_RO_DSN_FILE: /run/secrets/operator_ro_dsn
    secrets: [ops_token, operator_ro_dsn, telegram_bot_token]
    volumes: [../services/operator:/config:ro]

  prometheus: { image: prom/prometheus:v3.5.0, profiles: [box], volumes: [./prometheus:/etc/prometheus:ro] }
  grafana:    { image: grafana/grafana:12.1.0, profiles: [box], volumes: [./grafana:/etc/grafana/provisioning:ro] }
  loki:       { image: grafana/loki:3.5.0, profiles: [box] }
  alloy:      { image: grafana/alloy:v1.10.0, profiles: [box], volumes: [/var/run/docker.sock:/var/run/docker.sock:ro] }
  node-exporter: { image: prom/node-exporter:v1.9.1, profiles: [box], pid: host }

volumes: { pgdata: {}, minio: {}, hf-cache: {} }
secrets:
  hf_token: { file: /etc/arena/secrets/hf_token }
  ops_token: { file: /etc/arena/secrets/ops_token }
  operator_ro_dsn: { file: /etc/arena/secrets/operator_ro_dsn }
  telegram_bot_token: { file: /etc/arena/secrets/telegram_bot_token }
```

Image tags above are examples to be pinned by digest at P0/P4. `web` is not in compose for production (it runs on Vercel); `pnpm dev` is used locally.

### 10.2 vLLM serve commands for candidate models (box)

Exact checkpoint names, quantizations and flags change quickly on GB10. Each command below is a **starting point** for the day-1 benchmark (06 §7a). Flags marked † are UNVERIFIED for the pinned image.

```bash
# Extractor candidate A: small-active MoE (06 §7: best tokens/s per quality)
vllm serve Qwen/Qwen3.6-35B-A3B --served-model-name main \
  --gpu-memory-utilization 0.35 --max-model-len 16384 --max-num-seqs 64 \
  --enable-prefix-caching --reasoning-parser qwen3 --kv-cache-dtype fp8 --port 8001     # checkpoint/quant per Spark recipe†

# Extractor/critic candidate B: gpt-oss-120b (MXFP4)
vllm serve openai/gpt-oss-120b --served-model-name critic \
  --gpu-memory-utilization 0.55 --max-model-len 16384 --max-num-seqs 64 \
  --enable-prefix-caching --port 8003                                                   # reasoning parser flag per image†

# Hard-slice candidate: Qwen3.5-122B-A10B INT4 AutoRound (~38 tok/s single stream with MTP, 06 §1.2)
vllm serve <int4-autoround-checkpoint> --served-model-name hard \
  --gpu-memory-utilization 0.70 --max-model-len 16384 --max-num-seqs 16 --port 8004     # not co-resident with B

# Embeddings (and reranker as a second pooling server)
vllm serve Qwen/Qwen3-Embedding-4B --served-model-name embed --task embed --gpu-memory-utilization 0.08 --port 8002   # newer images: --runner pooling†
vllm serve Qwen/Qwen3-Reranker-0.6B --served-model-name rerank --task score --gpu-memory-utilization 0.05 --port 8005  †
```

Co-residency plan (128 GB unified; leave 15–20 GB for OS, Postgres and page cache):

| Window | Resident | Approx. memory |
|---|---|---|
| **Extraction** (default, most of the day) | extractor A (≈ 20–25 GB) + critic B (≈ 61 GB + KV) + embed + NLI | ≈ 100 GB |
| **ASR** (night, 00:30–05:30 MT, only when the `asr` queue is non-empty) | extractor A + embed + NeMo Parakeet + pyannote (≈ 6–10 GB); critic B stopped | ≈ 45 GB |
| **Hard slice / bake-off** | one large model at a time, others stopped | ≤ 90 GB |

### 10.3 Embedding client

```python
# packages/arena_llm/src/arena_llm/embed.py
import numpy as np
from openai import OpenAI

class Embedder:
    INSTRUCT = "Instruct: Represent this claim to find claims with the same truth conditions\nQuery: "
    def __init__(self, base_url: str, model: str = "embed", dim: int = 1024):
        self.c, self.model, self.dim = OpenAI(base_url=base_url, api_key="EMPTY"), model, dim

    def embed(self, texts: list[str]) -> np.ndarray:
        r = self.c.embeddings.create(model=self.model, input=[self.INSTRUCT + t for t in texts])
        v = np.array([d.embedding for d in r.data], dtype=np.float32)[:, : self.dim]   # MRL truncation
        return v / np.linalg.norm(v, axis=1, keepdims=True)
```

On `cloud-dev`, `Embedder` points at a local `sentence-transformers` shim serving Qwen3-Embedding-0.6B (1024-d) on CPU. `proposition.embedding_model` records which model made each vector; candidate search never mixes models.

### 10.4 GPU scheduling between ASR and LLM

A small table `gpu_window(name, starts_at, ends_at, state)` and the `open_asr_window` task implement the windows:
1. Stop the critic container (through the docker socket proxy, allow-listed).
2. Start the `asr` queue consumers.
3. At window end (or when the `asr` queue is empty), stop the ASR consumers and restart the critic.

GPU-queue tasks check the window state on start and re-defer themselves with `schedule_in={"minutes": 30}` when outside it. Thermal guard: if GPU temperature exceeds a threshold for 10 minutes (from the nvidia-smi exporter), the operator pauses the `llm` and `asr` queues and alerts.

### 10.5 Backups, secrets, static publishing

- **Postgres:** pgBackRest with WAL archiving + nightly full/differential to an off-box S3-compatible bucket, client-side encrypted (repo cipher `aes-256-cbc`). Retention: 7 daily, 4 weekly, 6 monthly.
- **MinIO:** `restic` nightly to a second disk and off-box.
- **Restore test:** monthly `restore_test` into a scratch container, then row counts and a checksum query compared with production; failure alerts.
- **Model weights:** pinned by digest, with a copy on an external SSD.
- **UPS** on the box; remote admin only over Tailscale.
- **Secrets:** never in git. On the box, files under `/etc/arena/secrets` (root-owned, 0400), mounted as compose secrets. The canonical store is `sops`-encrypted `infra/secrets.box.enc.yaml` with an age key held by Benjamin.
  - Keys: YouTube API, Podcast Index, HF token, Vercel deploy token (scoped to the one project), Telegram bot token, ops token, Postgres role passwords, backup repo keys.
  - `cloud-dev` uses `.env` files that hold only dev keys.
- **Static publishing:** S13 writes `dist/` and runs `vercel deploy` with the scoped token. No deployment before P5 except a password-protected preview with Benjamin's recorded approval (Plan H3). `--prod` requires `settings.public_launch_approved`, which is read from an `admin_approval` row Benjamin creates at the P5 gate.

```sql
CREATE TABLE admin_approval (
  approval_id  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind         text NOT NULL CHECK (kind IN ('paid_api','public_launch','standing_weekly_publish',
                                             'yt_audio_channel','snapshot_publish','landmark_contact','agent_platform')),
  scope        jsonb NOT NULL DEFAULT '{}',       -- e.g. {"channel_id": ...} or {"budget_usd": 20}
  approved_by  text NOT NULL,                     -- 'benjamin'
  approved_at  timestamptz NOT NULL DEFAULT now(),
  expires_at   timestamptz,
  revoked_at   timestamptz
);
```

### 10.6 Observability

- **Logs:** `structlog` JSON to stdout with `run_id`, `stage`, `job_id`, `item_id`, `model_version`; collected by Alloy into Loki. Never log segment text, emails or tokens; a log filter redacts known fields.
- **Metrics** (`prometheus_client` in workers and API):
  - `arena_stage_items_total{stage,status}`, `arena_stage_seconds{stage}`;
  - `arena_queue_depth{queue}` (from `procrastinate_jobs`);
  - `arena_captions_blocked_total`, `arena_youtube_quota_units{day}`;
  - `arena_anchor_match_total{match}`, `arena_nli_label_total{label}`, `arena_claims_rejected_total{reason}`;
  - `arena_escalations_total`, `arena_audit_disagreement_ratio{model_version}`;
  - `arena_speaker_conf_bucket`;
  - `arena_snapshot_validity{metric}`;
  - `arena_ratings_total{channel}`, `arena_coordination_flags_total`.

  vLLM `/metrics`, `postgres_exporter`, `node_exporter` and an nvidia-smi exporter (DCGM on GB10 is UNVERIFIED) complete the set.
- **Dashboards** (provisioned JSON in `infra/grafana`):
  1. **Pipeline:** throughput, queue depth, failures, parked batches.
  2. **Quality per model version:** anchor exact/normalized/fuzzy rates, NLI pass, critic reject, escalation, audit disagreement (06 §6).
  3. **Box:** GPU utilization/temperature, memory, disk, vLLM TTFT and tokens/s.
  4. **Product:** reactions, eligible ratifiers per cluster, contributions by status, U coverage.
- **Alerts** (Alertmanager → webhook to the operator agent → Telegram; a direct Telegram fallback route fires if the operator heartbeat is stale):
  - any queue failure rate > 10% over 1 h;
  - captions circuit breaker open;
  - YouTube quota > 90%;
  - parked batch past deadline;
  - backup or restore-test failure;
  - disk > 85%;
  - GPU thermal;
  - flags past SLA;
  - snapshot validity regression (bootstrap ARI drop > 0.15);
  - agent-free re-fit gate failure.

### 10.7 Operator agent (Hermes) interface

The operator agent watches, triages and reports. **It is never in the data path** (06 §6, spine §2). Its powers are exactly these:

| Tool (Hermes skill) | Kind | Backing |
|---|---|---|
| `arena_status` | read | `GET /v1/ops/status`: queue depths, run summaries, parked batches, dead letters |
| `quality_kpis(model_version?, days)` | read | SQL on `ops.quality_daily` (read-only role) |
| `box_health` | read | Prometheus HTTP API queries (GPU, disk, memory, thermals) |
| `dead_letters(since)` | read | `ops.dead_letter` |
| `flags_past_sla` | read | `ops.flags_sla` (ids, kinds, ages; no text) |
| `requeue(job_ids, reason)` | action | `POST /v1/ops/requeue` (re-defers with same args) |
| `pause_queue(q, reason)` / `resume_queue(q)` | action | `POST /v1/ops/pause_queue` |
| `trigger_job(name, args, reason)` | action | allow-list: `collect_batches`, `ops_report`, `audit_sample`, `restore_test`, `open_asr_window`, `discover_landmark` (delta only) |
| `restart_container(name, reason)` | action | allow-list: `worker-cpu`, `worker-gpu`, `vllm-main`, `vllm-embed` |
| `prepare_review_batch(kind)` | action | writes a `claude_code_batch` audit/gold/battery batch and a reminder for Benjamin |
| `set_channel_route(channel_id, route)` | action | **downgrade only**: `yt_caption → rss_audio / publisher / paused` (Plan §3.2) |
| `hide_pending_review(target)` | action | disputes and takedowns only: hide the target and trigger the pre-approved emergency republish (Plan §5.5, §11.3) |
| `propose_change(diff, rationale)` | proposal | opens a GitHub issue/PR draft; never merges |
| `report(kind)` | output | daily/weekly ops report → Telegram + Parachute (`#arena/ops`) |

It holds only the `arena_operator_ro` DSN (SELECT on `ops.*` views) and an ops token whose scopes are the actions above. Every action is rate-limited, logged as `event_log(actor_type='operator_agent')`, and echoed to Telegram. It cannot write content tables, approve snapshots, publish, change thresholds or contact anyone outside Benjamin's channels.

---

## 11. Security, privacy and compliance

### 11.1 Red lines → controls

| Red line (spine §9, synthesis §11.2, CLAUDE.md) | Implementation control |
|---|---|
| Every claim has a code-verified quote anchor | `claim` CHECK: `anchored/accepted` require `anchor_segment_id` and `anchor_match <> 'none'`; S8 re-validates the stored substring; bundle linter checks every published quote is a substring of its segment |
| Publish short quotes and timestamped links only, never full transcripts | Segment text in schema `private` (no grant to `arena_api`); exporter uses `quote_public` (≤ 280 chars, CHECK); linter rejects any string > 280 chars in quote fields |
| No paid APIs or cloud spend without approval | `anthropic_api` disabled + `admin_approval('paid_api')` with budget; no paid transcript service adapter enabled without approval; Vercel on the existing plan |
| Nothing outward-facing without approval | S13 requires `cluster_snapshot.status='approved'` (admin-only); `--prod` requires `public_launch`; landmark contact and agent platform actions require approvals |
| Public figures placed only from public output, with a dispute affordance | Only `landmark` rows are clustered; dispute link on every landmark/clip/proposition; `flag` SLA |
| No inference about non-consenting private individuals | `person.is_public_figure` CHECK; diarized unknown voices are `non_public` with no name; no stances for `person_id IS NULL`; reactions are first-party and consented |
| No minors | 18+ attestation at T1; the `minor-adjacent` flagged landmark is excluded from public surfaces |
| 15 flagged landmarks excluded from public surfaces | `landmark.public_surface_allowed=false` for `flag_type IN ('exclusion-review','minor-adjacent')` (14 + 1, OD-01) **and** for the 5 `conflict-of-interest` landmarks until Benjamin signs off (OD-02): 20 in all, set by the seed loader; exporter and API filter; linter test |
| Never store content from Benjamin's private vaults | Ingest adapters accept only public URLs from `channel`/`episode`; the Parachute integration is publish-only (Postgres → Parachute) |
| Agents never ratify; only reaction-placed users ratify | `rating_guard` trigger; `eligible_to_ratify` rules; agent token scopes |
| Directional-shift audit; agent-free re-fit | §9.1 audit job; release gate in S11/S13 |
| Reputation and prizes only; no token | No payment or wallet code in the repo; ADR-020 |
| Aggregates only, k ≥ 50, for user-derived data | Exporter suppresses cells < 50; users never appear as individual points to others |
| No scraping circumvention | Captions circuit breaker; no proxy/IP rotation code; robots.txt respected; YouTube audio off by default |

### 11.2 Data retention

| Data | Where | Retention |
|---|---|---|
| Raw audio | MinIO tmp | deleted after successful ASR (≤ 7 days on failure) |
| Full transcripts, caption files, word timings | MinIO + `private.segment` | `retention_until` = 3 years from fetch (reviewed annually); purged immediately on takedown |
| Anchored quote spans and word timings for anchors | Postgres | permanent unless taken down |
| Voiceprints | MinIO, encrypted | while the landmark is in the panel; deleted on removal or request |
| Reactions | Postgres | while the account exists; account deletion removes them and recomputes placement next snapshot (event log keeps a tombstone without the vote) |
| Contributions and ratings | Postgres | contributions are public works under the user's chosen handle; on deletion, the body is removed and the scoring record anonymized |
| Event log | Postgres | permanent (no personal payloads; user events carry ids only) |
| Logs | Loki | 30 days |

### 11.3 Takedown and dispute workflow

```mermaid
stateDiagram-v2
  [*] --> open: POST /v1/flags
  open --> triaged: acknowledge ≤ 48 h (all kinds); takedown / misattribution / unfair rewrite hidden ≤ 24 h; resolve thats_not_me / misattribution ≤ 7 d, other ≤ 14 d
  triaged --> accepted: valid
  triaged --> rejected: not valid (reason published to raiser)
  triaged --> annotated: landmark annotation shown beside placement
  accepted --> [*]: correction job
  annotated --> [*]
  rejected --> [*]
```

On `accepted`:
- **Takedown:** set `episode.rights_status='removed'`, purge MinIO objects and `private.segment` rows for the episode, mark its claims `retracted`, re-derive stances, and exclude it from the next snapshot. An emergency republish of the current bundle without the item happens within 24 h.
- **Anchor misattribution / that's not me:** set `claim.gate_status='rejected'`, stance `item_status='participant_contested'` → re-derive, and add the item as a labelled example for evals (`label_example_id`).
- **Proposition unfaithful:** a new proposition version, re-linked claims, and an audit of the merge history.

Every state change is an event. The landmark's page shows open/resolved dispute counts and any annotation.

### 11.4 Application security

- **Auth:** magic-link tokens hashed (sha256) with 15-minute expiry; WebAuthn passkeys; session cookies `HttpOnly; Secure; SameSite=Lax`; CSRF double-submit token on all state-changing requests; admin requires passkey re-auth within 5 minutes.
- **Ingress:** the API is reachable publicly only through the tunnel, with a Cloudflare/Tailscale ACL. CORS is restricted to the web origin. Request bodies are capped at 32 KB.
- **Database:** roles separated (§3.3); the API never uses the worker role. Row-level reads of `app_user.email` only via auth functions.
- **Dependencies:** `uv lock` / `pnpm-lock` pinned; Renovate weekly; `pip-audit` and `pnpm audit` in CI; containers pinned by digest.
- **Prompt injection:** transcripts are untrusted input to the LLM stages. Outputs are schema-constrained and code-gated, so injected text can at most produce a claim that still needs an exact anchor and NLI entailment. No LLM stage has tools.
- **Compliance notes:** a DPIA before any EU landmark or EU audience (synthesis §11.1; counsel needed, UNVERIFIED sufficiency). Fair use for the public layer is UNVERIFIED; get counsel before scale. CC-BY-4.0 attribution for Parakeet and pyannote goes on `/about/method`.

---

## 12. Testing and evals

### 12.1 Test layers

| Layer | Tooling | What |
|---|---|---|
| Unit | `pytest`, `hypothesis` | validators (port of TL `validate.test.ts`, same cases), `locate()` property tests (inject ASR-style noise: case, punctuation, apostrophes, ≤ 2 token edits → must locate; > 2 → must not), chunker invariants (cores tile the transcript, no gaps or overlaps), resolver scoring, selection constraints, commit–reveal, scoring rules |
| Contract | `export_contracts.py` + `git diff --exit-code` | Pydantic ↔ JSON Schema ↔ TS drift |
| Integration | `pytest` + Postgres service container | migrations up from empty; seed load (234 niches, 817 landmarks, 53 slice, 20 with `public_surface_allowed=false`); each stage on fixtures with the `fake` LLM; idempotency (run every stage twice → no new rows; bump `prompt_version` → new rows, old superseded) |
| Golden | fixture episode (a public, short, permissively usable clip transcript) → expected claims/propositions/stances JSON | detects unintended behaviour changes; updated only with a reviewed diff |
| DB guards | SQL tests | `rating_guard` rejects agents, self-ratings, non-eligible raters and cross-cluster fidelity; `event_log` is append-only; `private` schema not readable by `arena_api` |
| Bundle linter | `arena bundle lint` in CI and S13 | schema validity, quote length, flagged landmarks absent, k ≥ 50, every quote is a substring of its source segment (checked against the DB at publish time) |
| Web | Vitest (reducer, placement ports agree with Python on shared fixtures), Playwright (first-60-seconds flow on a fixture bundle), axe accessibility checks | |
| Scorer simulation | §4.12.5 over 20 seeds; the full named suite (S-honest … S-judgment) is Plan §4.3 | P3 gate |

### 12.2 Gold data

`evals/gold/v<N>/{dev,test}/` holds JSONL (Plan §4.2 owns the protocol). One line per chunk: chunk text with seq markers, gold claims (quote, char offsets, speaker, speech act, canonical, layer, attitude, strength, source), gold proposition clusters (which canonicals are equivalent), and gold relations. Gold is produced by `claude_code_batch` subagents (two annotators + adjudicator) and **spot-checked by Benjamin** (P2 gate: ≥ 300 adjudicated gold chunks). Each version is frozen. Splits are by episode: **gold-dev 30%** for prompt iteration and calibration, **gold-test 70% sealed** (SHA-256 manifest, access-logged) and used only by the bake-off and gate runs. The tables `gold_item`, `gold_label`, `gold_adjudication` are a queryable mirror of these files, loaded by `arena gold` tooling; the files are canonical.

### 12.3 Extraction metrics

Metric IDs (M1–M9, M6b) and thresholds are the Plan's §4.2 P4 threshold sheet, which Benjamin signs at the P2 gate (**OD-13**). The table below gives the definitions this architecture computes and maps each to that sheet; where an earlier draft of this table had different numbers, the Plan's sheet wins.

| Metric | Definition | Plan ID and proposed threshold |
|---|---|---|
| Anchor pass rate | accepted claims with exact or normalized anchors ÷ accepted claims; fuzzy share reported separately | M6 ≥ 95%; M6b (stored quote is a source substring) = 100% |
| Anchor precision | anchored spans overlapping a gold span (IoU ≥ 0.5, same speaker) ÷ anchored | reported (feeds M1) |
| Claim-match F1 | vs adjudicated gold, anchor IoU ≥ 0.5 | M1 ≥ 0.85 of the Claude pipeline's own M1 and ≥ 0.75 absolute |
| NLI precision vs gold | among claims the NLI gate passes, the share gold marks supported | M8; τ calibrated to ≥ 0.95 precision (ADR-008) |
| NLI recall vs gold | among gold-supported claims, the share the gate passes | M8, reported; unsupported leakage M7 ≤ 2% |
| Proposition merge precision / recall | pairwise over claims: same bank proposition vs same gold cluster | M9 precision ≥ 0.90; recall reported |
| Stance accuracy | attitude and source (3-way) accuracy on matched claims; strength within one step | M2 attitude ≥ 0.85; M3 source ≥ 0.90 |
| Layer accuracy | layer label on matched propositions; macro-F1 | M4 ≥ 0.75 macro-F1 |
| Speaker attribution accuracy | segments with confidence ≥ 0.9 whose person is correct (gold episodes) | ≥ 0.98 (highest-harm failure; publish threshold 0.9 is OD-32) |
| Neutral-rewrite fidelity | blind judge + Benjamin sample: "same truth conditions and neutral?" | M5 ≥ 0.85 |

### 12.4 Map validity metrics

- **Stability:** bootstrap ARI over propositions (≥ 0.7) and week-over-week ARI on the core panel.
- **Separation:** silhouette on `1 − s`.
- **Crosswalk purity** (informative, not a target: low purity can mean the data found something the seed missed).
- **Landmark self-recognition:**
  - automatic proxy (validity metric only, not a gate): the share of landmarks whose 3 nearest neighbours include a same-niche landmark;
  - the gate protocol is PRD §7.4 (judge subagents checking each profile against the landmark's other public writing; method choice is OD-28);
  - real: once landmarks engage, their own rating of their placement and nearest neighbours ("would Eliezer and Beff both nod?", D-31.6).
- **Benjamin's eye test** (P3 gate): the protocol and pass criteria are PRD §7.3 (blind, reveal and placement rounds plus a 20-claim spot check), served by a structured review page listing every cluster with its top affirmed/rejected propositions per layer, landmarks and clips. His ratings are stored as labels.
- **Agent-free agreement** (P6): ARI ≥ 0.9, max |ΔU| ≤ 0.1, ratifier eligibility identical for ≥ 98% of users (OD-24).

### 12.5 Bake-off harness (P4)

```yaml
# evals/harness/bakeoff.yaml
gold: evals/gold/v1/test/            # sealed gold-test (Plan §4.2); every access is logged
arms:
  - id: claude_gold_ceiling
    backend: claude_code_batch
    prompt: extract_claims@v3
  - id: local_qwen36_35b
    backend: vllm
    base_url: http://localhost:8001/v1
    model: main
    prompt: extract_claims@v3
    critic: {backend: vllm, base_url: http://localhost:8003/v1, model: critic}
    votes: 1
  - id: local_gptoss120b
    backend: vllm
    base_url: http://localhost:8003/v1
    model: critic
    prompt: extract_claims@v3
    critic: {backend: vllm, base_url: http://localhost:8001/v1, model: main}
  - id: baseline_embed_classifier          # cheap baseline: sentence split + GLiClass/SetFit tags + embedding stance
    backend: classifier
    pipeline: baseline_v1
metrics: [anchor_pass_rate, anchor_precision, claim_recall, nli_precision, merge_pr, stance_acc, layer_f1, speaker_acc]
map_metrics: [bootstrap_ari, silhouette, self_recognition_proxy]
cost: {measure: [wall_clock_s, gpu_hours, tokens_in, tokens_out, kwh]}
report: evals/reports/bakeoff-{date}.md
```

`uv run arena eval bakeoff evals/harness/bakeoff.yaml` runs every arm over the sealed gold-test split, builds a slice snapshot per arm (for cluster validity by eye), and writes a Markdown report with a metrics table, per-metric bootstrap confidence intervals, cost and time, and a side-by-side cluster comparison page for Benjamin. The winner (or a combination, e.g. a local extractor plus Claude rewrite for low-confidence items) becomes production by changing `config/llm.box.yaml`. **Nothing is promoted on feel** (TL `models.ts` rule).

---

## 13. Architecture Decision Records

Each ADR is a file `docs/adr/ADR-0NN-<slug>.md` (context, decision, consequences, status). One-line decisions:

| ADR | Decision |
|---|---|
| ADR-001 | Monorepo with a `uv` workspace (Python) and pnpm (web); layout exactly as spine §3. |
| ADR-002 | One Postgres 16 + pgvector database for content, queue (Procrastinate) and event log; no Redis, no graph DB. |
| ADR-003 | Append-only `event_log` + versioned derived rows (`superseded_by`); content is never updated in place. |
| ADR-004 | Idempotency key `(item, stage, model_version, prompt_version, inputs_hash)` in `stage_item` for every stage. |
| ADR-005 | Pydantic is the single schema source; JSON Schema in `contracts/`; TS generated; TL Zod ontology ported, not re-invented. |
| ADR-006 | Spine stance values stored alongside TL attitudes with a fixed mapping (§3.4); `suspends` creates no stance. |
| ADR-007 | Quote anchors are located by code (exact → normalized → fuzzy ≥ 95, ≤ 2 token edits); the stored quote is always the source substring. |
| ADR-008 | NLI gate with DeBERTa-v3-large mnli-fever-anli-ling-wanli; entailment threshold calibrated to ≥ 0.95 precision on gold. |
| ADR-009 | Proposition identity = embedding candidates (Qwen3-Embedding, 1024-d halfvec) + reranker + LLM equivalence judge; merges are reversible events. |
| ADR-010 | Clustering = blended direct/semantic similarity → kNN → Leiden with bootstrap-stability resolution choice; HDBSCAN as a cross-check. |
| ADR-011 | deck.gl (OrthographicView) for the terrain; Sigma.js for graph views. |
| ADR-012 | Users placed by a landmark-anchored logistic ideal-point model; cluster membership by naive-Bayes posterior; eligibility rules for ratifiers. |
| ADR-013 | Reputation scorer = Community Notes MF adapted: centred cluster-membership offsets replace the learned viewpoint factor, with a weak residual factor; CN thresholds where analogous. |
| ADR-014 | The box never serves public reads; static bundles on Vercel; writes via a tunnel to the API (Cloudflare Tunnel vs Tailscale Funnel: open decision OD-10, needed by 2027-01-04). |
| ADR-015 | `claude_code_batch` is an asynchronous file-queue backend processed by Claude Code subagents; stages park on `PendingBatch`. |
| ADR-016 | vLLM ≥ 0.12 with the `structured_outputs` request field (`guided_*` was removed in v0.12 and is never sent), client-side concurrency 32–64, prefix caching. |
| ADR-017 | `anthropic_api` implemented but disabled; requires an approval row with budget. |
| ADR-018 | Procrastinate for jobs; queues per resource class; UTC cron; dead letters via `ops.dead_letter`; requeue = fresh job. |
| ADR-019 | Hermes operator agent outside the data path: read-only role + allow-listed `/ops` actions only. |
| ADR-020 | Reputation and prizes only; no wallets, payments or tokens in the codebase for ≥ 2 years. |
| ADR-021 | Personhood tiers T0–T3; rating requires T2 (passkey + age + reactions + one personhood proof); agents hold no tier; operators are T3 (proof methods: OD-16). |
| ADR-022 | Fidelity raters are mostly random-sample invitations from the described cluster; self-selected fidelity votes capped at 50%. |
| ADR-023 | Forecasts are commit–reveal with strictly proper scoring (Brier, pinball); strategy assignment block-randomized with a committed seed (OD-08). |
| ADR-024 | Captions are fetched politely with a circuit breaker and no evasion; YouTube audio download off by default (R49). |
| ADR-025 | Parakeet TDT 0.6B v3 + pyannote community-1 + TitaNet voiceprints in NGC containers; speaker publish threshold 0.9. |
| ADR-026 | Full transcripts private (MinIO + `private` schema); public layer = propositions, ≤ 280-char quotes, timestamped links. |
| ADR-027 | Agent-free re-fit is a release gate after P6 (ARI ≥ 0.9, max ΔU ≤ 0.1, eligibility ≥ 98%; OD-24). |
| ADR-028 | Pre-box ingest host for the crawl and caption fetch (Benjamin's Mac Mini, pending OD-11); proposed by the Plan. |

---

## Spine extensions

> **Consolidated:** these extensions, deduplicated with the PRD's and the Plan's, are now part of the spine as `design-spine/SPINE.md` §10 (adopted 2026-10-31). SPINE §10 is authoritative; this list is kept for traceability.

Everything below is used in this document but not defined in `SPINE.md`. Other docs (PRD, Implementation Plan) should adopt these names.

**Tables and entities**
- `person` (every named public speaker; landmarks are a subset). The spine's Appearance is "Person × episode", but Person had no table.
- `content_group` (same conversation across platforms).
- `encounter` as a stored, derived table.
- `cluster_snapshot` is the table name for the spine's **Snapshot** (named as the build request listed it).
- `cluster_lineage`; `live_question_proposition` (the `answers` relation); `contribution_score`; `strategy_assignment`.
- `stage_item` (idempotency ledger); `llm_call`; `rate_bucket`; `admin_approval`; `gpu_window`.
- Schema `private` (segment text); schema `ops` (operator views).

**Fields and values**
- `stance.value` (spine) + `stance.tl_attitude` (TL), with the mapping in §3.4.
- `proposition.tl_type`, `proposition.public_id`, `proposition_relation.tl_relation_type`, `proposition_relation.scope` (`bank` | `episode`).
- `claim` anchor fields `anchor_match` and `quote_public`; `gate_status` values (`proposed`, `anchored`, `accepted`, `rejected`, `escalated`).
- `contribution.status` values (`needs_ratings`, `ratified`, `helpful`, `ratified_helpful`, `not_helpful`, `split_detected`, `withdrawn`, `removed`) and `synthesis_subtype` (`bridge_proposal`, `better_question`, `clean_disagreement`).
- `rating.tags` and `rating.sampled`.
- `cluster_membership.eligible_to_ratify`.
- `landmark.public_surface_allowed` (false for all 20 flagged-for-Benjamin entries: the 15 flagged, 14 exclusion-review + 1 minor-adjacent, plus the 5 conflict-of-interest checks until signed off).
- `flag.kind` values listed in §3.3.

**Jobs and queues (beyond S1–S14)**
- Schedules: `nightly`, `weekly`, `monthly`.
- Ops: `collect_batches`, `sweep_failed`, `open_asr_window`, `ops_report`.
- Batch work: `live_question_battery`, `audit_sample`, `weather_report`.
- Bank maintenance: `reembed_bank`, `rededup_bank`, `retrain_classifiers`, `eval_models_on_gold`.
- Lifecycle and gates: `agent_free_refit`, `restore_test`, `prune_retention`.
- Queues: `schedule`, `discover`, `fetch`, `asr`, `extract_cpu`, `llm`, `nli`, `embed`, `map`, `publish`, `ops`.

**Interfaces**
- `PendingBatch` and `BackendDisabled` exceptions in `arena_llm`.
- The `arena.ccbatch/1` task/result file protocol and the `/process-batch` Claude Code command.
- The `fake` LLM backend for CI.
- The `/v1/ops/*` action API for the operator agent.

**Scoring terms**
- Portability (cluster-anchored MF intercept `i_n`), cluster offsets `g_n`, `spread_n`, effective factor `φ_n`.
- Fidelity score `F_n`; `split_detected`.
- Rating impact; synthesis credit `SC`; the reputation formula `WI + SC + RH·min(t,50)/10`.
- Personhood tiers T0–T3.
- Forecast question keys (`dU:…`, `win:…`, `dRep:…`).

**Correction to spine wording (applied).** Spine §6 said vLLM serves "with `guided_json`". The implementation sends only `structured_outputs` (vLLM ≥ 0.12; `guided_*` was removed in v0.12). SPINE §6 now says this.

---

## Sources

- Community Notes (accessed 2026-10-31):
  - `twitter/communitynotes`, `documentation/under-the-hood/ranking-notes.md`, `contributor-scores.md`, `documentation/contributing/writing-and-rating-impact.md`, `writing-ability.md`, and `scoring/src/scoring/matrix_factorization/matrix_factorization.py` — https://github.com/twitter/communitynotes
  - The guide page https://communitynotes.x.com/guide/en/under-the-hood/ranking-notes could not be fetched in this session; the same documentation was read from the repository.
- Topology Live ontology: `omniharmonic/antidebate-live/packages/ontology/src/{enums,entities,validate,lexicons}.ts`, `docs/ONTOLOGY.md`.
- Handoff docs 01, 02, 03 (§7–9, §11), 05, 06 and `design-spine/SPINE.md`; `seed/SEED-v4.json` and `seed/SLICE-1-LANDMARKS.json` (inspected: 234 niches, 817 landmarks, 53 slice landmarks in 15 niches; 20 flagged landmarks: 14 exclusion-review + 1 minor-adjacent ("the 15 flagged") and 5 conflict-of-interest checks, all 20 excluded from public surfaces until Benjamin decides OD-01 / OD-02).
- Library APIs from training knowledge, to be checked against pinned versions at P0:
  - youtube-transcript-api ≥ 1.0;
  - Podcast Index auth headers;
  - YouTube Data API v3 (`channels.list forHandle`, `playlistItems`, `videos`);
  - NeMo Parakeet `transcribe(timestamps=True)`;
  - pyannote.audio 4 `exclusive_speaker_diarization`;
  - Procrastinate `App`/`RetryStrategy`/`periodic`;
  - leidenalg/igraph;
  - deck.gl layers;
  - vLLM `structured_outputs`.
