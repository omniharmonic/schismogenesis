# Dialogos Arena: Technical Architecture, Appendix A (DDL and scorer)

*Author of record: Benjamin Life (@omniharmonic) · 2026-10-31 · Appendix to `08-TECHNICAL-ARCHITECTURE.md`*

This appendix holds the two longest code listings from the Technical Architecture, moved here so that document stays readable. Nothing was rewritten in the move: the listings are verbatim, except for the changes recorded in `design-spine/REVIEW-NOTES.md` (the `public_surface_allowed` comment, the `judgment_flag` column, the agent-author note on `contribution.author_cluster_id`, `Thresholds.fid_lcb_min`, and the S-honest assertion at 0.75). The prose that explains them stays in 08:

| Listing | Explained in |
|---|---|
| A1 Postgres DDL | 08 §3.1–§3.3 (principles, provenance columns, tables by group), §3.4 (TL mappings), §3.7 (migrations) |
| A1.1 Reconciled additions | 08 §4.1 (quota), Plan §4.4 / §5.2 / §5.3 (releases, incidents) |
| A2.1–A2.2 Scorer | 08 §4.12.1 (Community Notes, verified), §4.12.2 (the Arena adaptation and formulas) |
| A2.3 Coordinated-rater detection | 08 §4.12.4 |
| A2.4 Simulation test | 08 §4.12.5 and the canonical suite in Plan §4.3 |

Precedence and vocabulary are as in 08 and `design-spine/SPINE.md` (including §10).

---

## A1. Postgres DDL (full)

Target of Alembic revision `0001_initial`. Plain SQL so the swarm can review it in one place; Alembic migrations execute it in ordered chunks (08 §3.7).

```sql
-- ===================================================================
-- 0. Extensions, schemas, enums
-- ===================================================================
CREATE EXTENSION IF NOT EXISTS vector;        -- pgvector >= 0.7 (halfvec)
CREATE EXTENSION IF NOT EXISTS pg_trgm;       -- fuzzy alias search
CREATE EXTENSION IF NOT EXISTS citext;
CREATE SCHEMA IF NOT EXISTS private;          -- transcript text; not granted to arena_public

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

-- ===================================================================
-- 1. Runs and the event log
-- ===================================================================
CREATE TABLE pipeline_run (
  run_id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stage           text NOT NULL CHECK (stage ~ '^S([1-9]|1[0-4])$|^(seed|gold|eval|refit|admin)$'),
  job_name        text NOT NULL,                  -- canonical job name, e.g. 'extract_claims'
  trigger         text NOT NULL,                  -- 'schedule:nightly' | 'manual' | 'ops:<action_id>' | 'parent:<run_id>'
  params          jsonb NOT NULL DEFAULT '{}',
  code_ref        text NOT NULL,                  -- git sha of the deployed image
  model_name      text, model_version text, prompt_id text, prompt_version text,
  status          run_status NOT NULL DEFAULT 'running',
  started_at      timestamptz NOT NULL DEFAULT now(),
  finished_at     timestamptz,
  stats           jsonb NOT NULL DEFAULT '{}',    -- counts, pass rates, timings
  error           text
);
CREATE INDEX pipeline_run_stage_started ON pipeline_run (stage, started_at DESC);

CREATE TABLE event_log (
  event_id        bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  at              timestamptz NOT NULL DEFAULT now(),
  type            text NOT NULL,                  -- 'proposition.merged', 'claim.rejected', 'flag.resolved' …
  actor_type      text NOT NULL CHECK (actor_type IN ('pipeline','user','agent','operator_agent','admin','landmark')),
  actor_id        text NOT NULL,                  -- run_id, user id, agent id
  entity_type     text NOT NULL,
  entity_id       text NOT NULL,
  payload         jsonb NOT NULL,
  run_id          uuid REFERENCES pipeline_run(run_id),
  agent_provenance boolean NOT NULL DEFAULT false
);
CREATE INDEX event_log_entity ON event_log (entity_type, entity_id, at);
CREATE INDEX event_log_type_at ON event_log (type, at);
-- append-only: no UPDATE/DELETE for any application role
CREATE RULE event_log_no_update AS ON UPDATE TO event_log DO INSTEAD NOTHING;
CREATE RULE event_log_no_delete AS ON DELETE TO event_log DO INSTEAD NOTHING;

-- Idempotency ledger: one row per (item, stage, model_version, prompt_version, inputs_hash)
CREATE TABLE stage_item (
  item_type       text NOT NULL,
  item_id         text NOT NULL,
  stage           text NOT NULL,
  model_version   text NOT NULL DEFAULT 'code',
  prompt_version  text NOT NULL DEFAULT '-',
  inputs_hash     bytea NOT NULL,
  run_id          uuid NOT NULL REFERENCES pipeline_run(run_id),
  status          text NOT NULL CHECK (status IN ('started','done','failed','skipped')),
  attempts        int NOT NULL DEFAULT 1,
  updated_at      timestamptz NOT NULL DEFAULT now(),
  detail          jsonb NOT NULL DEFAULT '{}',
  PRIMARY KEY (item_type, item_id, stage, model_version, prompt_version, inputs_hash)
);

CREATE TABLE llm_call (
  call_id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id          uuid REFERENCES pipeline_run(run_id),
  backend         text NOT NULL,                  -- claude_code_batch | vllm | openai_compat | anthropic_api | fake
  engine_version  text, model_name text NOT NULL, model_version text, quant text, adapter_id text,
  prompt_id       text NOT NULL, prompt_version text NOT NULL,
  request_hash    bytea NOT NULL,
  input_tokens    int, output_tokens int, latency_ms int,
  ok              boolean NOT NULL, error text,
  created_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX llm_call_request ON llm_call (request_hash);

-- ===================================================================
-- 2. Seed: niche, person, landmark, landmark_niche
-- ===================================================================
CREATE TABLE niche (
  niche_id        text PRIMARY KEY,               -- kebab slug from SEED-v4
  name            text NOT NULL,
  domain          text NOT NULL,                  -- 'd3-tech-futures'
  cross_domains   text[] NOT NULL DEFAULT '{}',
  aliases         jsonb NOT NULL DEFAULT '[]',    -- [{text, kind: self|outsider}]
  description     text,
  telos           text, sacred_values jsonb, existential_threats jsonb,
  combatant_niche_ids text[] NOT NULL DEFAULT '{}',
  adjacent_niche_ids  text[] NOT NULL DEFAULT '{}',
  placement_prior jsonb,                          -- {left_right, atlas_accelerate_restrain, atlas_institutions_exit, basis}
  slice_tier      text CHECK (slice_tier IN ('core','adjacent')),   -- null = not in Slice 1
  sampling_budget_hours numeric(6,1) NOT NULL DEFAULT 15,
  seed_version    text NOT NULL,                  -- 'SEED-v4'
  version         int NOT NULL DEFAULT 1,
  merged_from     text[] NOT NULL DEFAULT '{}',
  valid_from      date NOT NULL DEFAULT current_date,
  valid_to        date,
  raw             jsonb NOT NULL                  -- full seed record, for audit
);

-- Every named public speaker. Landmarks are persons admitted to the seed panel.
CREATE TABLE person (
  person_id       text PRIMARY KEY,               -- landmark_id for landmarks; 'p-'||uuid for others
  display_name    text NOT NULL,
  aliases         jsonb NOT NULL DEFAULT '[]',    -- [{text, kind: legal|stage|handle|misspelling|nickname, source}]
  wikidata_qid    text,
  is_public_figure boolean NOT NULL,
  ambiguous_name  boolean NOT NULL DEFAULT false,
  voiceprint_ref  text,                           -- MinIO key; internal only
  created_at      timestamptz NOT NULL DEFAULT now(),
  CHECK (is_public_figure)                        -- red line: private individuals are never stored by name
);
CREATE INDEX person_name_trgm ON person USING gin (display_name gin_trgm_ops);

CREATE TABLE landmark (
  landmark_id     text PRIMARY KEY REFERENCES person(person_id),
  name            text NOT NULL,
  primary_niche_id text NOT NULL REFERENCES niche(niche_id),
  role            text NOT NULL CHECK (role IN ('core','bridger','edge')),
  platforms       jsonb NOT NULL DEFAULT '{}',
  longform_output text,
  verification    text NOT NULL,                  -- verified-active | pending | stale | excluded
  in_slice        text,                           -- 'slice-1' | null
  flag_type       text,                           -- exclusion-review | conflict-of-interest | minor-adjacent
  public_surface_allowed boolean NOT NULL,        -- false for all 20 in SEED-v4 flags_for_benjamin: the 15 flagged (14 exclusion-review
                                                  -- + 1 minor-adjacent, OD-01) and the 5 conflict-of-interest checks until signed off (OD-02)
  claim_status    text NOT NULL DEFAULT 'unclaimed' CHECK (claim_status IN ('unclaimed','claimed','opted_in')),
  panel_status    text NOT NULL DEFAULT 'core_panel' CHECK (panel_status IN ('core_panel','newcomer','retired','excluded')),
  gender          text,                           -- aggregate balance audit only; never exported
  seed_version    text NOT NULL,
  raw             jsonb NOT NULL
);
CREATE INDEX landmark_slice ON landmark (in_slice) WHERE in_slice IS NOT NULL;

CREATE TABLE landmark_niche (
  landmark_id     text NOT NULL REFERENCES landmark(landmark_id),
  niche_id        text NOT NULL REFERENCES niche(niche_id),
  role            text NOT NULL CHECK (role IN ('core','bridger','edge')),
  is_primary      boolean NOT NULL,
  weight          real NOT NULL DEFAULT 1.0,      -- 0.5 for secondary (OPEN-4)
  valid_from      date NOT NULL DEFAULT '2024-01-01',
  valid_to        date,
  basis           text,
  PRIMARY KEY (landmark_id, niche_id, valid_from)
);
CREATE UNIQUE INDEX landmark_one_primary ON landmark_niche (landmark_id) WHERE is_primary AND valid_to IS NULL;

-- ===================================================================
-- 3. Media: channel, content_group, episode, appearance, encounter
-- ===================================================================
CREATE TABLE channel (
  channel_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  platform        text NOT NULL CHECK (platform IN ('youtube','podcast_rss','substack','bluesky','x','website')),
  title           text NOT NULL,
  external_ids    jsonb NOT NULL DEFAULT '{}',    -- {yt_channel_id, uploads_playlist_id, podcastindex_feed_id, itunes_collection_id, rss_url, podcast_guid}
  owner_person_id text REFERENCES person(person_id),
  show_format_prior text,
  default_transcript_route text,
  last_crawled_at timestamptz, etag text, block_rate_7d real,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S1',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL
);
CREATE UNIQUE INDEX channel_yt ON channel ((external_ids->>'yt_channel_id')) WHERE external_ids ? 'yt_channel_id';
CREATE UNIQUE INDEX channel_rss ON channel ((external_ids->>'rss_url')) WHERE external_ids ? 'rss_url';

CREATE TABLE content_group (
  content_group_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  canonical_title  text NOT NULL,
  published_at     timestamptz,
  created_at       timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE episode (
  episode_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  channel_id      uuid NOT NULL REFERENCES channel(channel_id),
  content_group_id uuid REFERENCES content_group(content_group_id),
  platform        text NOT NULL,
  external_id     text NOT NULL,                  -- YouTube video id or RSS guid
  url             text NOT NULL,
  title           text NOT NULL,
  description     text,
  published_at    timestamptz,
  duration_s      int,
  language        text DEFAULT 'en',
  format          text CHECK (format IN ('interview','debate','panel','solo','roundtable','clip','compilation','essay','unknown')),
  audio_url       text,                           -- RSS enclosure
  discovered_via  jsonb NOT NULL DEFAULT '[]',    -- [{method, query, api, at}]
  transcript_status text NOT NULL DEFAULT 'unknown'
     CHECK (transcript_status IN ('unknown','yt_caption_available','publisher_transcript','none','queued','fetched','failed','asr_queued')),
  rights_status   text NOT NULL DEFAULT 'public_unlicensed'
     CHECK (rights_status IN ('public_unlicensed','publisher_published_transcript','opted_in','licensed','takedown_requested','removed')),
  selected_for    text[] NOT NULL DEFAULT '{}',   -- coverage | baseline | event_map
  selection_run_id uuid REFERENCES pipeline_run(run_id),
  title_embedding halfvec(1024),
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S1',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  UNIQUE (platform, external_id)
);
CREATE INDEX episode_channel_pub ON episode (channel_id, published_at DESC);
CREATE INDEX episode_selected ON episode USING gin (selected_for);

CREATE TABLE appearance (
  appearance_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),
  person_id       text REFERENCES person(person_id),   -- null until resolved (S2)
  mention_text    text NOT NULL,                       -- raw string from title/description
  role            appearance_role,
  mention_type    mention_type NOT NULL DEFAULT 'present',
  evidence        text[] NOT NULL,                     -- title | description | show_notes | podcast_person_tag | channel_owner | diarization
  resolution_confidence real CHECK (resolution_confidence BETWEEN 0 AND 1),
  resolution_method text,
  speaking_share  real,
  status          text NOT NULL DEFAULT 'candidate'
     CHECK (status IN ('candidate','accepted','review','rejected','verified_by_audio')),
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL,
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  superseded_by   uuid REFERENCES appearance(appearance_id)
);
CREATE INDEX appearance_person ON appearance (person_id) WHERE status IN ('accepted','verified_by_audio');
CREATE INDEX appearance_episode ON appearance (episode_id);

-- Derived edge: one row per cross-niche landmark pair per content group.
CREATE TABLE encounter (
  encounter_id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content_group_id uuid NOT NULL REFERENCES content_group(content_group_id),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),   -- representative episode
  person_a text NOT NULL REFERENCES landmark(landmark_id), person_b text NOT NULL REFERENCES landmark(landmark_id),
  niche_a  text NOT NULL REFERENCES niche(niche_id),       niche_b  text NOT NULL REFERENCES niche(niche_id),
  type            text NOT NULL CHECK (type IN ('host_guest','co_guest','debate','panel')),
  niche_distance_prior real NOT NULL, quality_score real NOT NULL, confidence real NOT NULL,
  sign            text NOT NULL DEFAULT 'unknown' CHECK (sign IN ('unknown','integrative','sparring','mixed')),
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S3',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  CHECK (niche_a < niche_b), CHECK (person_a <> person_b),
  UNIQUE (content_group_id, person_a, person_b, run_id)
);

-- ===================================================================
-- 4. Transcripts: transcript, segment (private), chunk
-- ===================================================================
CREATE TABLE transcript (
  transcript_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),
  route           text NOT NULL CHECK (route IN ('yt_caption_auto','yt_caption_creator','publisher','stt_selfhosted','opt_in_oauth')),
  language        text NOT NULL DEFAULT 'en',
  has_diarization boolean NOT NULL, has_word_timestamps boolean NOT NULL,
  quality         jsonb NOT NULL DEFAULT '{}',    -- {est_wer, caption_kind, asr_model}
  storage_ref     text NOT NULL,                  -- MinIO key: raw caption file / ASR JSON with words
  rights_basis    text NOT NULL,
  retention_until date,
  is_current      boolean NOT NULL DEFAULT true,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL,
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL
);
CREATE UNIQUE INDEX transcript_current ON transcript (episode_id) WHERE is_current;

CREATE TABLE private.segment (                    -- = Topology Live Utterance
  segment_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  transcript_id   uuid NOT NULL REFERENCES transcript(transcript_id) ON DELETE CASCADE,
  seq             int NOT NULL,
  start_ms        int NOT NULL, end_ms int NOT NULL CHECK (end_ms >= start_ms),
  text            text NOT NULL,
  diar_label      text,
  person_id       text REFERENCES person(person_id),     -- null = unknown; never a private individual
  speaker_kind    text NOT NULL DEFAULT 'unknown' CHECK (speaker_kind IN ('person','non_public','unknown')),
  attribution     jsonb NOT NULL DEFAULT '{}',           -- {confidence, signals:{metadata,voiceprint,caption_cue,llm}, confirmed_by}
  attribution_confidence real NOT NULL DEFAULT 0,
  UNIQUE (transcript_id, seq)
);
CREATE INDEX segment_person ON private.segment (person_id, transcript_id);

CREATE TABLE chunk (
  chunk_id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  transcript_id   uuid NOT NULL REFERENCES transcript(transcript_id),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),
  seq             int NOT NULL,
  segment_ids     uuid[] NOT NULL,                -- ordered; core segments + overlap context
  core_from_seq   int NOT NULL, core_to_seq int NOT NULL,   -- claims must anchor inside the core
  start_ms        int NOT NULL, end_ms int NOT NULL,
  speakers        text[] NOT NULL,
  token_estimate  int NOT NULL,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S6',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  superseded_by   uuid REFERENCES chunk(chunk_id),
  UNIQUE (transcript_id, seq, model_version)
);

-- ===================================================================
-- 5. Content: claim, proposition, stance, proposition_relation
-- ===================================================================
CREATE TABLE proposition (
  proposition_id  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  public_id       text UNIQUE NOT NULL,           -- 'P-000381', stable for URLs
  canonical       text NOT NULL CHECK (length(canonical) BETWEEN 3 AND 400),
  tl_type         text NOT NULL,                  -- 10 TL proposition types
  layer           layer NOT NULL,
  validity_tag    text CHECK (validity_tag IN ('truth','rightness','sincerity')),
  scope           jsonb NOT NULL DEFAULT '{"quantifier":"generic"}',
  conditions      jsonb NOT NULL DEFAULT '[]',
  quantities      jsonb NOT NULL DEFAULT '[]',
  forecast        jsonb,
  embedding       halfvec(1024),
  embedding_model text,
  item_status     item_status NOT NULL DEFAULT 'live_provisional',
  first_seen_at   timestamptz, first_seen_claim_id uuid, first_seen_person_id text,
  merged_into     uuid REFERENCES proposition(proposition_id),
  bank_version    int NOT NULL,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S9',
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  agent_provenance boolean NOT NULL DEFAULT false
);
CREATE INDEX proposition_embedding ON proposition USING hnsw (embedding halfvec_cosine_ops)
  WITH (m = 16, ef_construction = 128) WHERE merged_into IS NULL;
CREATE INDEX proposition_layer ON proposition (layer) WHERE merged_into IS NULL;
CREATE INDEX proposition_canonical_trgm ON proposition USING gin (canonical gin_trgm_ops);

CREATE TABLE claim (                              -- raw extracted assertion + quote anchor (= TL ADU + Span)
  claim_id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  chunk_id        uuid NOT NULL REFERENCES chunk(chunk_id),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),
  speaker_person_id text REFERENCES person(person_id),
  speaker_conf    real NOT NULL,
  speech_act      text NOT NULL,                  -- 13 TL speech acts
  claim_text      text NOT NULL,                  -- the model's speaker-relative paraphrase
  proposed_canonical text NOT NULL,               -- the model's neutral proposition draft
  tl_attitude     tl_attitude NOT NULL,
  strength        stance_strength NOT NULL,
  credence        real CHECK (credence BETWEEN 0 AND 1),
  source          stance_source NOT NULL,
  proposed_layer  layer NOT NULL,
  -- quote anchor (S8): the stored quote is ALWAYS the source substring, never model text
  model_quote     text NOT NULL,
  anchor_segment_id uuid REFERENCES private.segment(segment_id),
  anchor_char_start int, anchor_char_end int,
  anchor_match    text CHECK (anchor_match IN ('exact','normalized','fuzzy','none')),
  anchor_score    real,
  quote_full      text,                           -- private: exact substring (may span to 600 chars)
  quote_public    text CHECK (length(quote_public) <= 280),
  t_start_ms      int, t_end_ms int,
  deep_link       text,                           -- url with ?t= / #t=
  -- gates
  validator_issues jsonb NOT NULL DEFAULT '[]',   -- TL validateProposal codes
  nli_label       text CHECK (nli_label IN ('entailment','neutral','contradiction')),
  nli_entail_prob real, nli_model text,
  critic_verdict  text, critic_model text,
  gate_status     text NOT NULL DEFAULT 'proposed'
     CHECK (gate_status IN ('proposed','anchored','accepted','rejected','escalated')),
  reject_reason   text,
  proposition_id  uuid REFERENCES proposition(proposition_id),   -- set by S9
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL,
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text NOT NULL, prompt_version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  agent_provenance boolean NOT NULL DEFAULT false,
  superseded_by   uuid REFERENCES claim(claim_id),
  CHECK (gate_status NOT IN ('anchored','accepted') OR (anchor_segment_id IS NOT NULL AND anchor_match <> 'none')),
  CHECK (anchor_char_end IS NULL OR anchor_char_end > anchor_char_start)
);
CREATE INDEX claim_chunk ON claim (chunk_id);
CREATE INDEX claim_gate ON claim (gate_status) WHERE superseded_by IS NULL;
CREATE INDEX claim_prop ON claim (proposition_id) WHERE gate_status = 'accepted';

CREATE TABLE stance (
  stance_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_kind      actor_kind NOT NULL DEFAULT 'person',
  person_id       text NOT NULL REFERENCES person(person_id),
  proposition_id  uuid NOT NULL REFERENCES proposition(proposition_id),
  value           stance_value NOT NULL,
  tl_attitude     tl_attitude NOT NULL,
  strength        stance_strength NOT NULL,
  strength_num    real NOT NULL CHECK (strength_num BETWEEN 0 AND 1),  -- tentative .25 leaning .5 confident .75 certain 1
  credence        real,
  source          stance_source NOT NULL,
  claim_ids       uuid[] NOT NULL CHECK (cardinality(claim_ids) >= 1),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),
  as_of           date NOT NULL,                  -- episode publish date: a reading at a moment
  item_status     item_status NOT NULL DEFAULT 'live_provisional',
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S9',
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  agent_provenance boolean NOT NULL DEFAULT false,
  superseded_by   uuid REFERENCES stance(stance_id),
  UNIQUE (person_id, proposition_id, episode_id, run_id)
);
CREATE INDEX stance_matrix ON stance (proposition_id, person_id) WHERE superseded_by IS NULL AND source <> 'inferred';

CREATE TABLE proposition_relation (
  relation_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  from_id         uuid NOT NULL REFERENCES proposition(proposition_id),
  to_id           uuid NOT NULL REFERENCES proposition(proposition_id),
  type            relation_type NOT NULL,
  tl_relation_type text NOT NULL,                 -- the finer TL type (rebuts, undercuts, presupposes…)
  scope           text NOT NULL DEFAULT 'bank' CHECK (scope IN ('bank','episode')),
  episode_id      uuid REFERENCES episode(episode_id),    -- for event maps
  evidence_claim_ids uuid[] NOT NULL DEFAULT '{}',
  confidence      real NOT NULL,
  source          stance_source NOT NULL,         -- stated (speaker said "because") vs inferred
  item_status     item_status NOT NULL DEFAULT 'live_provisional',
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S10',
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  CHECK (from_id <> to_id),
  UNIQUE (from_id, to_id, type, scope, episode_id)
);

-- ===================================================================
-- 6. People in the product: app_user, statement, reaction
-- ===================================================================
CREATE TABLE app_user (
  user_id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind            actor_kind NOT NULL DEFAULT 'person',      -- 'agent' rows are arena agents' accounts
  handle          citext UNIQUE,
  email           citext UNIQUE,
  personhood_tier smallint NOT NULL DEFAULT 0 CHECK (personhood_tier BETWEEN 0 AND 3),
  personhood_methods jsonb NOT NULL DEFAULT '[]',            -- [{method, verified_at, evidence_ref}]
  age_gate_passed boolean NOT NULL DEFAULT false,
  consents        jsonb NOT NULL DEFAULT '{}',               -- {reactions: v3, research: null, …}
  landmark_id     text REFERENCES landmark(landmark_id),     -- a landmark who claimed their profile
  created_at      timestamptz NOT NULL DEFAULT now(),
  suspended_at    timestamptz,
  CHECK (kind = 'person' OR personhood_tier = 0)             -- agents never hold a personhood tier
);

CREATE TABLE statement (
  statement_id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  proposition_id  uuid NOT NULL REFERENCES proposition(proposition_id),
  display_text    text NOT NULL,
  primary_claim_id uuid NOT NULL REFERENCES claim(claim_id),  -- source clip (red line 22)
  reveal_person_id text REFERENCES landmark(landmark_id),
  selection_reason text NOT NULL CHECK (selection_reason IN ('cluster_splitter','live_thread','surprising_unifier','onboarding_core')),
  live_question_id uuid,
  active_from     timestamptz NOT NULL DEFAULT now(), active_to timestamptz,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S11',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL
);

CREATE TABLE reaction (
  reaction_id     bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id         uuid NOT NULL REFERENCES app_user(user_id),
  statement_id    uuid NOT NULL REFERENCES statement(statement_id),
  vote            reaction_vote NOT NULL,
  guess_person_id text REFERENCES landmark(landmark_id),
  consent_version text NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now(),
  is_latest       boolean NOT NULL DEFAULT true,
  agent_provenance boolean NOT NULL DEFAULT false   -- true if the user reacted inside an agent-led interaction
);
CREATE UNIQUE INDEX reaction_latest ON reaction (user_id, statement_id) WHERE is_latest;

-- ===================================================================
-- 7. Map: cluster_snapshot, cluster, cluster_membership, crosswalk, lineage
-- ===================================================================
CREATE TABLE cluster_snapshot (                   -- the spine's Snapshot
  snapshot_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  public_id       text UNIQUE NOT NULL,           -- '2026-W48', '2026-11-27-d'
  horizon         snapshot_horizon NOT NULL,
  as_of           timestamptz NOT NULL,
  data_window     tstzrange NOT NULL,
  bank_version    int NOT NULL,
  panel_season    text NOT NULL,
  params          jsonb NOT NULL,                 -- clustering params, thresholds, seeds
  model_versions  jsonb NOT NULL,
  agent_free      boolean NOT NULL DEFAULT false, -- true for the re-fit without agent_provenance inputs
  parent_snapshot_id uuid REFERENCES cluster_snapshot(snapshot_id),
  validity        jsonb NOT NULL DEFAULT '{}',    -- silhouette, stability ARI, eye-test status
  status          text NOT NULL DEFAULT 'built' CHECK (status IN ('built','approved','published','withdrawn')),
  bundle_ref      text,                           -- path/URL of the published bundle
  bundle_sha256   text,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S11',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL
);

CREATE TABLE cluster (
  cluster_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  snapshot_id     uuid NOT NULL REFERENCES cluster_snapshot(snapshot_id),
  local_index     int NOT NULL,
  label           text NOT NULL,                  -- provisional: best-aligned niche name
  label_status    text NOT NULL DEFAULT 'provisional' CHECK (label_status IN ('provisional','ratified')),
  n_landmarks     int NOT NULL, n_users int NOT NULL DEFAULT 0,
  centroid        real[] NOT NULL,                -- in the snapshot's 2-D layout space
  profile         halfvec(1024),                  -- mean proposition-embedding of affirmed propositions
  cohesion        real,
  UNIQUE (snapshot_id, local_index)
);

CREATE TABLE cluster_membership (
  snapshot_id     uuid NOT NULL REFERENCES cluster_snapshot(snapshot_id),
  subject_type    text NOT NULL CHECK (subject_type IN ('landmark','user')),
  subject_id      text NOT NULL,
  cluster_id      uuid NOT NULL REFERENCES cluster(cluster_id),
  weight          real NOT NULL CHECK (weight BETWEEN 0 AND 1),    -- soft membership
  is_primary      boolean NOT NULL,
  coords          real[] NOT NULL,                -- 2-D position
  uncertainty     real NOT NULL,
  basis           text NOT NULL CHECK (basis IN ('content','reactions')),
  n_reactions     int,                            -- users only
  eligible_to_ratify boolean NOT NULL DEFAULT false,
  PRIMARY KEY (snapshot_id, subject_type, subject_id, cluster_id)
);
CREATE INDEX membership_cluster ON cluster_membership (cluster_id) WHERE is_primary;
CREATE INDEX membership_ratifiers ON cluster_membership (cluster_id) WHERE eligible_to_ratify;

CREATE TABLE niche_cluster_crosswalk (
  snapshot_id     uuid NOT NULL REFERENCES cluster_snapshot(snapshot_id),
  niche_id        text NOT NULL REFERENCES niche(niche_id),
  cluster_id      uuid NOT NULL REFERENCES cluster(cluster_id),
  share_of_niche_landmarks real NOT NULL,
  share_of_cluster real NOT NULL,
  jaccard         real NOT NULL,
  PRIMARY KEY (snapshot_id, niche_id, cluster_id)
);

CREATE TABLE cluster_lineage (
  from_cluster_id uuid NOT NULL REFERENCES cluster(cluster_id),
  to_cluster_id   uuid REFERENCES cluster(cluster_id),             -- null for 'fades'
  type            text NOT NULL CHECK (type IN ('continues','splits','merges','born','fades')),
  overlap         real NOT NULL, confidence real NOT NULL,
  computed_on     text NOT NULL DEFAULT 'core_panel',
  PRIMARY KEY (from_cluster_id, to_cluster_id)
);

-- ===================================================================
-- 8. Gradient: contribution, rating, scores, reputation, U matrix
-- ===================================================================
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
CREATE INDEX contribution_target ON contribution (target_cluster_id, status);

CREATE TABLE rating (
  rating_id       bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  contribution_id uuid NOT NULL REFERENCES contribution(contribution_id),
  rater_user_id   uuid NOT NULL REFERENCES app_user(user_id),
  rater_snapshot_id uuid NOT NULL REFERENCES cluster_snapshot(snapshot_id),
  rater_cluster_id uuid NOT NULL REFERENCES cluster(cluster_id),
  helpfulness     helpfulness NOT NULL,                 -- portability channel (all eligible raters)
  helpfulness_value real GENERATED ALWAYS AS (CASE helpfulness WHEN 'helpful' THEN 1.0 WHEN 'somewhat' THEN 0.5 ELSE 0.0 END) STORED,
  fidelity        helpfulness,                          -- only raters placed in the described cluster
  tags            text[] NOT NULL DEFAULT '{}',          -- 'judges_not_describes', 'misattributes', 'strawman', …
  sampled         boolean NOT NULL DEFAULT false,        -- true if rater was randomly invited (population sample)
  created_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (contribution_id, rater_user_id)
);
-- Agents never rate, and self-rating is forbidden. Enforced by trigger (CHECK cannot reference other tables).
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

CREATE TABLE contribution_score (                  -- scorer output per contribution per scoring run
  score_run_id    uuid NOT NULL REFERENCES pipeline_run(run_id),
  contribution_id uuid NOT NULL REFERENCES contribution(contribution_id),
  portability_intercept real, portability_lcb real, portability_ucb real,
  cluster_factors jsonb,                           -- {cluster_id: g_nc}
  factor_spread   real,                            -- max_c g_nc - min_c g_nc over rating clusters
  fidelity_score  real, fidelity_lcb real, fidelity_n int,
  fidelity_subgroup jsonb,                         -- per sub-cluster fidelity if split detected
  status          text NOT NULL,
  n_ratings       int NOT NULL, n_rater_clusters int NOT NULL,
  PRIMARY KEY (score_run_id, contribution_id)
);

CREATE TABLE reputation_score (
  score_run_id    uuid NOT NULL REFERENCES pipeline_run(run_id),
  actor_kind      actor_kind NOT NULL,
  user_id         uuid NOT NULL REFERENCES app_user(user_id),
  writer_impact   real NOT NULL,                   -- Σ +1 ratified/helpful, −1 not_helpful (see §4.12)
  rating_impact   real NOT NULL,
  rater_helpfulness real,                          -- (s − 10h)/t; null until ≥ 10 ratings
  synthesis_credit real NOT NULL DEFAULT 0,        -- retroactive, by lineage
  reputation      real NOT NULL,
  eligible_rater  boolean NOT NULL,
  coordination_flag boolean NOT NULL DEFAULT false,
  reward_eligible boolean NOT NULL DEFAULT true,   -- false after directional-shift audit failure (agents)
  computed_at     timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (score_run_id, user_id)
);
CREATE INDEX reputation_leaderboard ON reputation_score (score_run_id, actor_kind, reputation DESC);

CREATE TABLE understanding_cell (                  -- U[A][B]
  snapshot_id     uuid NOT NULL REFERENCES cluster_snapshot(snapshot_id),
  score_run_id    uuid NOT NULL REFERENCES pipeline_run(run_id),
  cluster_a       uuid NOT NULL REFERENCES cluster(cluster_id),   -- describer
  cluster_b       uuid NOT NULL REFERENCES cluster(cluster_id),   -- described
  u               real NOT NULL,                  -- shrunk mean fidelity of A's contributions about B, 0..1
  u_lcb           real NOT NULL,
  n_contributions int NOT NULL, n_ratified int NOT NULL,
  agent_free      boolean NOT NULL DEFAULT false,
  PRIMARY KEY (score_run_id, cluster_a, cluster_b, agent_free),
  CHECK (cluster_a <> cluster_b)
);

-- ===================================================================
-- 9. Live questions
-- ===================================================================
CREATE TABLE live_question (
  live_question_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  text            text NOT NULL,                  -- neutral, signable by both sides
  parent_id       uuid REFERENCES live_question(live_question_id),
  origin_cluster_id uuid REFERENCES cluster(cluster_id),
  origin_niche_id text REFERENCES niche(niche_id),
  first_seen_claim_id uuid REFERENCES claim(claim_id),
  chosen_axes     jsonb NOT NULL DEFAULT '[]',    -- [{axis_id, proposition_ids[], loadings}] (2–3 per question)
  axes_fit_snapshot_id uuid REFERENCES cluster_snapshot(snapshot_id),
  lifecycle_state text NOT NULL DEFAULT 'emerging'
     CHECK (lifecycle_state IN ('emerging','spreading','forking','crossing','quiet','absorbed')),
  adopted_by_clusters uuid[] NOT NULL DEFAULT '{}',
  battery_week    text,                           -- '2026-W48'
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S11',
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL
);
ALTER TABLE statement ADD FOREIGN KEY (live_question_id) REFERENCES live_question(live_question_id);
ALTER TABLE contribution ADD FOREIGN KEY (live_question_id) REFERENCES live_question(live_question_id);

CREATE TABLE live_question_proposition (          -- the 'answers' relation
  live_question_id uuid NOT NULL REFERENCES live_question(live_question_id),
  proposition_id  uuid NOT NULL REFERENCES proposition(proposition_id),
  answer_pole     smallint NOT NULL CHECK (answer_pole IN (-1, 1)),
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id),
  PRIMARY KEY (live_question_id, proposition_id)
);

-- ===================================================================
-- 10. Agents and market (P6; created in P0 so FKs are stable)
-- ===================================================================
CREATE TABLE agent (
  agent_id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         uuid UNIQUE NOT NULL REFERENCES app_user(user_id),    -- the agent's account (kind='agent')
  operator_user_id uuid NOT NULL REFERENCES app_user(user_id),          -- verified human, tier ≥ 3
  name            text NOT NULL UNIQUE,
  model_disclosure text NOT NULL,                 -- model family/version, public
  charter_version text NOT NULL,
  strategy_id     uuid,                           -- currently assigned strategy (null outside market windows)
  platforms       jsonb NOT NULL DEFAULT '[]',    -- [{platform:'x', handle, automated_label:true}]
  registry_hash   text NOT NULL,                  -- sha256 of the public registry entry
  status          text NOT NULL DEFAULT 'active' CHECK (status IN ('pending','active','suspended','retired')),
  reward_eligible boolean NOT NULL DEFAULT true,
  created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE agent_action (
  action_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id        uuid NOT NULL REFERENCES agent(agent_id),
  type            text NOT NULL CHECK (type IN ('contribution','reply','invite','dm_reply','draft_for_user')),
  target_user_id  uuid REFERENCES app_user(user_id),
  target_cluster_id uuid REFERENCES cluster(cluster_id),
  invoked_by_user boolean NOT NULL,               -- charter A3: must be true for any user-directed action
  contribution_id uuid REFERENCES contribution(contribution_id),
  platform        text NOT NULL DEFAULT 'arena',
  external_ref    text,
  charter_checks  jsonb NOT NULL,                 -- results of enforcement hooks
  allowed         boolean NOT NULL,
  strategy_id     uuid,
  assignment_id   uuid,
  created_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX agent_action_agent ON agent_action (agent_id, created_at);

CREATE TABLE strategy (
  strategy_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  slug            text UNIQUE NOT NULL,           -- 'steelman_first', 'shared_question'
  name            text NOT NULL,
  policy_md       text NOT NULL,                  -- published behaviour policy
  version         int NOT NULL,
  published_at    timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE agent ADD FOREIGN KEY (strategy_id) REFERENCES strategy(strategy_id);

CREATE TABLE strategy_assignment (                 -- randomized: which strategy runs on which pair in which window
  assignment_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  window_id       text NOT NULL,                  -- '2027-W03..2027-W06'
  window_range    tstzrange NOT NULL,
  cluster_a       uuid NOT NULL REFERENCES cluster(cluster_id),
  cluster_b       uuid NOT NULL REFERENCES cluster(cluster_id),
  strategy_id     uuid NOT NULL REFERENCES strategy(strategy_id),
  agent_ids       uuid[] NOT NULL,
  seed_commitment text NOT NULL,                  -- sha256(seed) published before the window
  seed_reveal     text,
  UNIQUE (window_id, cluster_a, cluster_b)
);

CREATE TABLE forecast (
  forecast_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  forecaster_user_id uuid NOT NULL REFERENCES app_user(user_id),
  window_id       text NOT NULL,
  question_key    text NOT NULL,                  -- 'dU:<strategy>:<A>:<B>' etc.
  commitment      text NOT NULL,                  -- sha256 hex of canonical forecast JSON || salt
  committed_at    timestamptz NOT NULL DEFAULT now(),
  revealed_payload jsonb, revealed_salt text, revealed_at timestamptz,
  reveal_valid    boolean,
  resolution_value real, score real, resolved_at timestamptz,
  resolve_run_id  uuid REFERENCES pipeline_run(run_id),
  UNIQUE (forecaster_user_id, window_id, question_key)
);

-- ===================================================================
-- 11. Governance: flag (dispute)
-- ===================================================================
CREATE TABLE flag (
  flag_id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  raised_by_type  text NOT NULL CHECK (raised_by_type IN ('user','landmark','operator','rights_holder','admin')),
  raised_by_id    text NOT NULL,
  kind            text NOT NULL CHECK (kind IN ('thats_not_me','placement_dispute','landmark_annotation','anchor_misattribution',
                     'proposition_unfaithful','niche_label_dispute','takedown','harassment','coordinated_rating','privacy')),
  target_type     text NOT NULL,                  -- claim | proposition | stance | landmark | contribution | episode | cluster
  target_id       text NOT NULL,
  text            text NOT NULL,
  state           text NOT NULL DEFAULT 'open' CHECK (state IN ('open','triaged','accepted','rejected','annotated','withdrawn')),
  sla_due_at      timestamptz NOT NULL,
  public_annotation text,                         -- landmark annotation shown beside a placement
  resolution      text, resolved_by text, resolved_at timestamptz,
  label_example_id uuid,                          -- every accepted correction becomes a gold-style example
  created_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX flag_open ON flag (state, sla_due_at) WHERE state IN ('open','triaged');

-- ===================================================================
-- 12. Roles
-- ===================================================================
CREATE ROLE arena_api        NOLOGIN;  -- read public tables, write human tables
CREATE ROLE arena_worker     NOLOGIN;  -- read all, write derived
CREATE ROLE arena_operator_ro NOLOGIN; -- SELECT on ops.* views only
GRANT USAGE ON SCHEMA private TO arena_worker;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA private TO arena_worker;
REVOKE ALL ON SCHEMA private FROM arena_api, arena_operator_ro;
```

**Operational views** for the operator agent live in a schema `ops` (08 §3.3, §10.7).

### A1.1 Reconciled additions

```sql
-- Reconciled additions (2026-10-31 consistency review). The Implementation Plan's tasks need these;
-- W1 adds them in P0 with the rest of 0001_initial. Provenance columns follow §3.2 where a row is derived.

-- Politeness and quota log for every outbound request (the Plan's "crawl log"; PoliteClient writes it).
CREATE TABLE api_call (
  call_id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  at              timestamptz NOT NULL DEFAULT now(),
  api             text NOT NULL,                  -- youtube_data | youtube_captions | podcastindex | itunes | wikidata | rss | web
  host            text NOT NULL,
  endpoint        text NOT NULL,
  quota_units     int NOT NULL DEFAULT 0,         -- YouTube Data API units; 0 elsewhere
  http_status     int,
  latency_ms      int,
  blocked         boolean NOT NULL DEFAULT false, -- 429 / RequestBlocked / IpBlocked
  channel_id      uuid REFERENCES channel(channel_id),
  run_id          uuid REFERENCES pipeline_run(run_id)
);
CREATE INDEX api_call_api_at ON api_call (api, at);
-- YouTube quota resets at midnight Pacific time; S1 stops at 9,000 units/day (§4.1).
CREATE VIEW quota_ledger AS
  SELECT api, (at AT TIME ZONE 'America/Los_Angeles')::date AS quota_day, sum(quota_units) AS units, count(*) AS calls,
         sum(blocked::int) AS blocked
  FROM api_call GROUP BY 1, 2;

-- Active versions pointer: rollback = activate the previous release (Plan §4.4, §5.3).
CREATE TABLE pipeline_release (
  release_id      text PRIMARY KEY,               -- 'r1', 'r2', …
  llm_roles       jsonb NOT NULL,                 -- role -> {backend, model, model_version, adapter_id}
  prompt_versions jsonb NOT NULL,                 -- prompt_id -> version
  created_at      timestamptz NOT NULL DEFAULT now(),
  approved_by     text,                           -- 'benjamin' (cutover and re-extraction need his approval)
  active          boolean NOT NULL DEFAULT false
);
CREATE UNIQUE INDEX pipeline_release_one_active ON pipeline_release (active) WHERE active;

-- Operator incidents (Plan §5.2): one row per detected incident; every row is also a Telegram message.
CREATE TABLE incident (
  incident_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  opened_at       timestamptz NOT NULL DEFAULT now(),
  closed_at       timestamptz,
  kind            text NOT NULL,                  -- caption_blocks | quota | vllm_down | backlog | anchor_drop | nli_drop |
                                                  -- audit_disagreement | disk | thermal | backup | redline | dispute | injection | refit_gate
  severity        text NOT NULL CHECK (severity IN ('info','warn','escalate')),
  detector        text NOT NULL,
  summary         text NOT NULL,                  -- no transcript text, emails or tokens
  refs            jsonb NOT NULL DEFAULT '{}',    -- job ids, run ids, flag ids
  escalated       boolean NOT NULL DEFAULT false
);
```

---

## A2. Scorer implementation (full)

### A2.1–A2.2 Cluster-anchored MF and the S12 scorer

The fitting code is numpy so it runs on any profile. Full-batch Adam on ≤ 10^6 ratings takes seconds. A torch port (same loss, CN-style `torch.optim.Adam`) is a drop-in if volume grows.

```python
# packages/arena_reputation/src/arena_reputation/cluster_mf.py
"""Cluster-anchored matrix factorization: the Arena's adaptation of the Community Notes scorer.

r̂_un = μ + i_u + i_n + m_u · g_n + f_u f_n
  m_u ∈ Δ^K   rater's (fixed) soft cluster membership from the snapshot
  g_n ∈ R^K   per-cluster helpfulness offsets for contribution n   (replaces CN's learned viewpoint)
  f_u, f_n    residual 1-D factor (CN-style) for viewpoint structure the clusters miss
  (m_u is centred, m̃_u = m_u − 1/K, inside fit(): see note there)
Loss = mean (r − r̂)² + λ_i·(mean i_u² + mean i_n² + μ²) + λ_g·mean_n ||g_n||² + λ_f·(mean f_u² + mean f_n²)
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass
class MFParams:
    mu: float
    i_u: np.ndarray        # (U,)
    i_n: np.ndarray        # (N,)
    g_n: np.ndarray        # (N, K)
    f_u: np.ndarray        # (U,)
    f_n: np.ndarray        # (N,)


@dataclass
class MFConfig:
    lambda_i: float = 0.15      # CN: intercepts 5× the factor penalty
    lambda_g: float = 0.03      # cluster offsets: same as CN factor penalty
    lambda_f: float = 0.09      # residual factor: 3× CN so clusters explain first (calibrate)
    lr: float = 0.05
    max_epochs: int = 3000
    tol: float = 1e-7
    seed: int = 0


def _adam(params, grads, state, lr, b1=0.9, b2=0.999, eps=1e-8):
    state["t"] += 1
    t = state["t"]
    for k in params:
        m = state["m"].setdefault(k, np.zeros_like(params[k]))
        v = state["v"].setdefault(k, np.zeros_like(params[k]))
        m[...] = b1 * m + (1 - b1) * grads[k]
        v[...] = b2 * v + (1 - b2) * grads[k] ** 2
        params[k] = params[k] - lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + eps)
    return params


def fit(u_idx: np.ndarray, n_idx: np.ndarray, r: np.ndarray, M: np.ndarray, n_items: int,
        cfg: MFConfig = MFConfig(), init: MFParams | None = None) -> MFParams:
    """u_idx, n_idx, r: (R,) arrays of ratings. M: (U, K) rater memberships (rows sum to 1)."""
    rng = np.random.default_rng(cfg.seed)
    U, K = M.shape
    N = n_items
    p = {"mu": np.array(0.0), "i_u": np.zeros(U), "i_n": np.zeros(N), "g_n": np.zeros((N, K)),
         "f_u": rng.normal(0, 0.1, U), "f_n": rng.normal(0, 0.1, N)}
    if init is not None:
        p.update(mu=np.array(init.mu), i_u=init.i_u.copy(), i_n=init.i_n.copy(), g_n=init.g_n.copy(),
                 f_u=init.f_u.copy(), f_n=init.f_n.copy())
    state = {"t": 0, "m": {}, "v": {}}
    Mc = M - 1.0 / K                               # centre: Σ_k m̃_uk = 0, so i_n is identifiable and
    Mr = Mc[u_idx]                                 # equals helpfulness to an equal-weighted "average cluster"
    prev = np.inf
    R = len(r)
    for _ in range(cfg.max_epochs):
        pred = (p["mu"] + p["i_u"][u_idx] + p["i_n"][n_idx]
                + (Mr * p["g_n"][n_idx]).sum(1) + p["f_u"][u_idx] * p["f_n"][n_idx])
        err = pred - r
        loss = (err ** 2).mean() + cfg.lambda_i * ((p["i_u"] ** 2).mean() + (p["i_n"] ** 2).mean() + p["mu"] ** 2) \
            + cfg.lambda_g * (p["g_n"] ** 2).sum(1).mean() + cfg.lambda_f * ((p["f_u"] ** 2).mean() + (p["f_n"] ** 2).mean())
        if abs(prev - loss) < cfg.tol:
            break
        prev = loss
        d = 2 * err / R
        g = {
            "mu": np.array(d.sum() + 2 * cfg.lambda_i * p["mu"]),
            "i_u": np.bincount(u_idx, d, U) + 2 * cfg.lambda_i * p["i_u"] / U,
            "i_n": np.bincount(n_idx, d, N) + 2 * cfg.lambda_i * p["i_n"] / N,
            "f_u": np.bincount(u_idx, d * p["f_n"][n_idx], U) + 2 * cfg.lambda_f * p["f_u"] / U,
            "f_n": np.bincount(n_idx, d * p["f_u"][u_idx], N) + 2 * cfg.lambda_f * p["f_n"] / N,
        }
        gg = np.zeros((N, K))
        np.add.at(gg, n_idx, d[:, None] * Mr)
        g["g_n"] = gg + 2 * cfg.lambda_g * p["g_n"] / N
        p = _adam(p, g, state, cfg.lr)
    # identification, as CN's _flip_factors_for_identification: flip so that >= 50% of rater factors are negative
    if (p["f_u"] < 0).mean() < 0.5:
        p["f_u"], p["f_n"] = -p["f_u"], -p["f_n"]
    return MFParams(float(p["mu"]), p["i_u"], p["i_n"], p["g_n"], p["f_u"], p["f_n"])


def refit_note(params: MFParams, M: np.ndarray, u: np.ndarray, r: np.ndarray, cfg: MFConfig,
               n_items: int, K: int, clusters: list[int] | None = None) -> tuple[float, np.ndarray, float]:
    """Holding rater params fixed, note params (i_n, g_n, f_n) solve a small ridge regression.
    Only clusters that rated the note get a free g_nk (others stay 0); otherwise the constant
    centred column of an unrated cluster is collinear with the intercept.
    Used for pseudo-rater confidence bounds and for scoring new contributions between full fits."""
    cols = list(range(K)) if clusters is None else list(clusters)
    X = np.column_stack([np.ones(len(u)), (M[u] - 1.0 / K)[:, cols], params.f_u[u]])
    y = r - params.mu - params.i_u[u]
    lam = np.r_[cfg.lambda_i / n_items, np.full(len(cols), cfg.lambda_g / n_items), cfg.lambda_f / n_items] * len(u)
    beta = np.linalg.solve(X.T @ X + np.diag(lam), X.T @ y)
    g = np.zeros(K); g[cols] = beta[1:1 + len(cols)]
    return float(beta[0]), g, float(beta[-1])


def pseudo_rater_bounds(params: MFParams, M: np.ndarray, u: np.ndarray, r: np.ndarray, cfg: MFConfig,
                        n_items: int, clusters: list[int] | None = None) -> tuple[float, float]:
    """CN-style uncertainty: add one extreme pseudo-rating (a pure member of each cluster, at either
    residual-factor pole, rating 0 or 1) and refit the note with rater params fixed.
    Only clusters that actually rated the note get a pseudo-rater (`clusters`).
    Returns (lower, upper) bounds on the note intercept."""
    K = M.shape[1]
    lo, hi = np.inf, -np.inf
    for k in (clusters if clusters is not None else range(K)):
        for f in (params.f_u.min(), params.f_u.max()):
            for val in (0.0, 1.0):
                p2 = MFParams(params.mu, np.r_[params.i_u, 0.0], params.i_n, params.g_n,
                              np.r_[params.f_u, f], params.f_n)
                i_n, _, _ = refit_note(p2, np.vstack([M, np.eye(K)[k]]), np.r_[u, len(M)],
                                       np.r_[r, val], cfg, n_items, K, clusters)
                lo, hi = min(lo, i_n), max(hi, i_n)
    return lo, hi
```

```python
# packages/arena_reputation/src/arena_reputation/scorer.py
"""S12 score_reputation: two-channel scoring, ratification, writer impact, rater helpfulness, U matrix."""
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from arena_reputation.cluster_mf import MFConfig, MFParams, fit


@dataclass
class Thresholds:                     # initial values; calibrate by simulation + P3 data
    min_ratings: int = 5              # CN: Needs More Ratings until >= 5
    helpful_intercept: float = 0.40   # CN: Helpful at intercept >= 0.40 ...
    max_spread: float = 0.50          # ... with |f_n| < 0.50; here: cluster spread of g_n (and |f_n|)
    nh_base: float = -0.05            # CN: Not Helpful if i_n < -0.05 - 0.8|f_n|
    nh_slope: float = 0.8
    min_rater_clusters: int = 2       # portability: ratings from >= 2 clusters other than the described one
    min_per_cluster: int = 2
    fid_min_n: int = 5                # fidelity: >= 5 raters placed in the described cluster
    fid_ratify: float = 0.70          # predicted fidelity for an average member of B (μ_B + ī_u + i_n)
    fid_lcb_min: float = 0.60         # §4.12.2 also requires fidelity_lcb >= 0.60 (OD-14); TODO(W5): apply in combined_status
    fid_split_factor: float = 0.50    # within-B factor polarization that signals a split
    rater_helpfulness_min: float = 0.66   # CN round-2 filter
    rater_min_ratings: int = 10           # CN: 10 ratings before helpfulness is computed


@dataclass
class Ratings:
    """Long-form arrays, one row per rating."""
    contrib: np.ndarray      # contribution index (0..N-1)
    rater: np.ndarray        # rater index (0..U-1)
    help: np.ndarray         # helpfulness value in {0, .5, 1}
    fid: np.ndarray          # fidelity value or nan
    rater_cluster: np.ndarray  # primary cluster of rater (0..K-1)


@dataclass
class Contribs:
    author: np.ndarray       # author index into raters/users space
    author_cluster: np.ndarray
    target: np.ndarray       # described cluster B (for synthesis: first parent)
    kind: np.ndarray         # 'note' | 'steelman' | 'synthesis'


def portability_status(i_n: float, spread: float, f_n: float, n: int, n_clusters_ok: int, th: Thresholds) -> str:
    if n < th.min_ratings or n_clusters_ok < th.min_rater_clusters:
        return "needs_ratings"
    phi = max(spread / 2, abs(f_n))
    if i_n >= th.helpful_intercept and spread < th.max_spread and abs(f_n) < th.max_spread:
        return "helpful"
    if i_n < th.nh_base - th.nh_slope * phi:
        return "not_helpful"
    return "needs_ratings"


def score_portability(R: Ratings, C: Contribs, M: np.ndarray, th: Thresholds, cfg: MFConfig,
                      rater_mask: np.ndarray | None = None) -> dict:
    """Fit on helpfulness ratings from raters NOT in the described cluster (portability = clarifying to others)."""
    N, K = len(C.target), M.shape[1]
    # notes/steelmen: exclude raters from the described cluster; synthesis: everyone (both parents rate)
    keep = (R.rater_cluster != C.target[R.contrib]) | (C.kind[R.contrib] == "synthesis")
    if rater_mask is not None:
        keep &= rater_mask[R.rater]
    u, n, r = R.rater[keep], R.contrib[keep], R.help[keep]
    p = fit(u, n, r, M, N, cfg)
    out = {"params": p, "status": [], "spread": np.zeros(N), "n": np.bincount(n, minlength=N)}
    for j in range(N):
        sel = n == j
        clusters, counts = np.unique(R.rater_cluster[keep][sel], return_counts=True)
        rated = clusters[counts >= th.min_per_cluster]
        spread = float(p.g_n[j, rated].max() - p.g_n[j, rated].min()) if len(rated) >= 2 else 0.0
        out["spread"][j] = spread
        out["status"].append(portability_status(p.i_n[j], spread, p.f_n[j], int(sel.sum()), len(rated), th))
    return out


def score_fidelity(R: Ratings, C: Contribs, th: Thresholds, cfg: MFConfig) -> dict:
    """Per described cluster B: fit a CN-style 1-D MF on fidelity votes from raters placed in B.
    F_n = μ_B + mean(i_u) + i_n is the fidelity an average member of B (factor 0) assigns.
    (μ is shrunk by λ_i, so rater intercepts carry part of the mean; adding mean(i_u) restores the scale.)
    |f_n| large with raters on both poles => B is split on n."""
    N = len(C.target)
    F, n_fid, split = np.full(N, np.nan), np.zeros(N, int), np.zeros(N, bool)
    has = ~np.isnan(R.fid)
    for B in np.unique(C.target):
        sel = has & (C.target[R.contrib] == B) & (R.rater_cluster == B)
        if sel.sum() == 0:
            continue
        raters, u = np.unique(R.rater[sel], return_inverse=True)
        notes, n = np.unique(R.contrib[sel], return_inverse=True)
        p = fit(u, n, R.fid[sel], np.ones((len(raters), 1)), len(notes), cfg)  # K=1 → only intercepts + f
        for k, j in enumerate(notes):
            n_fid[j] = int((n == k).sum())
            F[j] = p.mu + p.i_u.mean() + p.i_n[k]
            fu = p.f_u[u[n == k]]
            split[j] = abs(p.f_n[k]) >= th.fid_split_factor and (fu > 0).sum() >= 3 and (fu < 0).sum() >= 3
    return {"F": F, "n": n_fid, "split": split}


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


def rater_helpfulness(R: Ratings, final_status: np.ndarray, first_status_at_rating: np.ndarray,
                      harassment_helpful: np.ndarray, th: Thresholds) -> np.ndarray:
    """CN: RH = (s - 10h) / t over *valid* ratings (made before the contribution's first decided status).
    s = valid ratings matching the final status; t = valid ratings; h = helpful ratings on contributions
    later removed for harassment. Undefined (nan) below th.rater_min_ratings ratings."""
    U = int(R.rater.max()) + 1
    decided = np.isin(final_status[R.contrib], ["helpful", "ratified_helpful", "ratified", "not_helpful"])
    valid = decided & first_status_at_rating          # rating happened while status was still needs_ratings
    positive = np.isin(final_status[R.contrib], ["helpful", "ratified_helpful", "ratified"])
    match = np.where(positive, R.help >= 0.5, R.help == 0.0)   # 'somewhat' counts as helpful-side (UNVERIFIED in CN)
    s = np.bincount(R.rater[valid], match[valid].astype(float), U)
    t = np.bincount(R.rater[valid], minlength=U).astype(float)
    h = np.bincount(R.rater, harassment_helpful.astype(float), U)
    total = np.bincount(R.rater, minlength=U)
    with np.errstate(invalid="ignore", divide="ignore"):
        rh = (s - 10 * h) / t
    rh[(total < th.rater_min_ratings) | (t == 0)] = np.nan
    return rh


def writer_impact(C: Contribs, status: np.ndarray, n_users: int) -> np.ndarray:
    gain = {"ratified_helpful": 2.0, "ratified": 1.0, "helpful": 1.0, "not_helpful": -1.0}
    w = np.array([gain.get(s, 0.0) for s in status])
    return np.bincount(C.author, w, n_users)


def reputation(wi: np.ndarray, rh: np.ndarray, t_valid: np.ndarray, synth_credit: np.ndarray) -> np.ndarray:
    """Reputation = writer impact + synthesis credit + rater component (rater helpfulness scaled by volume,
    capped at 5 points so rating alone cannot dominate writing)."""
    rater_part = np.nan_to_num(rh) * np.minimum(t_valid, 50) / 10
    return wi + synth_credit + rater_part


def understanding_matrix(C: Contribs, F: np.ndarray, status: np.ndarray, K: int,
                         alpha: float = 3.0, prior: float = 0.0, exclude: np.ndarray | None = None):
    """U[A][B] = shrunk mean fidelity of A-authored notes/steelmen about B (unscored → excluded).
    Shrinks toward `prior` (0 = no understanding demonstrated yet) with pseudo-count alpha."""
    U = np.full((K, K), prior); n = np.zeros((K, K), int); nr = np.zeros((K, K), int)
    ok = np.isin(C.kind, ["note", "steelman"]) & ~np.isnan(F)
    if exclude is not None:
        ok &= ~exclude
    for A in range(K):
        for B in range(K):
            if A == B: continue
            sel = ok & (C.author_cluster == A) & (C.target == B)
            n[A, B] = sel.sum()
            nr[A, B] = np.isin(status[sel], ["ratified", "ratified_helpful"]).sum()
            U[A, B] = (np.clip(F[sel], 0, 1).sum() + alpha * prior) / (n[A, B] + alpha)
    return U, n, nr
```

### A2.3 Coordinated-rater detection

```python
# packages/arena_reputation/src/arena_reputation/coordination.py
"""Coordinated-rater detection (S12 pre-pass). Flags groups of raters whose ratings are near-identical and
near-simultaneous on many shared contributions. Flagged raters get weight 0 in round 2 and a `flag` row."""
from collections import defaultdict
import numpy as np


def coordinated_groups(contrib: np.ndarray, rater: np.ndarray, value: np.ndarray, ts: np.ndarray,
                       min_shared=8, agree_min=0.95, window_s=600, sync_min=0.5, min_group=5) -> list[set[int]]:
    by_c = defaultdict(list)
    for c, u, v, t in zip(contrib, rater, value, ts):
        by_c[int(c)].append((int(u), float(v), float(t)))
    shared, agree, sync = defaultdict(int), defaultdict(int), defaultdict(int)
    for rows in by_c.values():
        if len(rows) > 400:          # very popular items carry little signal; skip (bounded O(n²))
            continue
        for i in range(len(rows)):
            ui, vi, ti = rows[i]
            for j in range(i + 1, len(rows)):
                uj, vj, tj = rows[j]
                k = (min(ui, uj), max(ui, uj))
                shared[k] += 1
                agree[k] += vi == vj
                sync[k] += abs(ti - tj) <= window_s
    parent: dict[int, int] = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for k, n in shared.items():
        if n >= min_shared and agree[k] / n >= agree_min and sync[k] / n >= sync_min:
            parent[find(k[0])] = find(k[1])
    groups = defaultdict(set)
    for x in parent:
        groups[find(x)].add(x)
    return [g for g in groups.values() if len(g) >= min_group]


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    rows = []
    for c in range(60):                                  # 200 honest raters, random times and values
        for u in rng.choice(200, 25, replace=False):
            rows.append((c, u, rng.choice([0, .5, 1]), rng.uniform(0, 86400 * 7)))
        if c % 2 == 0:                                   # a 12-account ring rating together within minutes
            t0 = rng.uniform(0, 86400 * 7)
            for u in range(200, 212):
                rows.append((c, u, 1.0, t0 + rng.uniform(0, 300)))
    a = np.array(rows)
    g = coordinated_groups(a[:, 0], a[:, 1].astype(int), a[:, 2], a[:, 3])
    print([sorted(x) for x in g]); assert g == [set(range(200, 212))]
```

### A2.4 Scorer simulation test

Synthetic world (08 §4.12.5): 4 clusters × 100 raters with soft memberships; 80 notes of four true types; 24 portability raters and 12 sampled fidelity raters per note; a 15-account brigade variant.

```python
# evals/harness/test_scorer_sim.py
"""Synthetic-data simulation test for the S12 scorer (evals/harness/test_scorer_sim.py)."""
import numpy as np
from arena_reputation.cluster_mf import MFConfig
from arena_reputation.scorer import (Ratings, Contribs, Thresholds, score_portability, score_fidelity,
                    combined_status, understanding_matrix)

def simulate(seed=0, K=4, per_cluster=100, n_notes=80, brigade=0, raters_per_note=24, fid_raters=12):
    rng = np.random.default_rng(seed)
    U = K * per_cluster + brigade
    home = np.r_[np.repeat(np.arange(K), per_cluster), np.ones(brigade, int)]   # brigade placed in cluster 1
    M = np.full((U, K), 0.0); M[np.arange(U), home] = 0.85; M += 0.15 / K       # soft memberships
    M /= M.sum(1, keepdims=True)
    author_c = rng.integers(0, K, n_notes)
    target = (author_c + rng.integers(1, K, n_notes)) % K
    # note types: 0 bridging-accurate, 1 tribal (pleases author cluster only), 2 strawman (inaccurate), 3 dull
    typ = rng.choice(4, n_notes, p=[.35, .25, .25, .15])
    rows = []
    for j in range(n_notes):
        others = np.where((home != target[j]) & (np.arange(U) < K * per_cluster))[0]
        for u in rng.choice(others, raters_per_note, replace=False):
            if typ[j] == 0:   base = 0.85
            elif typ[j] == 1: base = 0.95 if home[u] == author_c[j] else 0.05
            elif typ[j] == 2: base = 0.6 if home[u] == author_c[j] else 0.15
            else:             base = 0.35
            v = np.clip(base + rng.normal(0, .2), 0, 1)
            rows.append((j, u, [0, .5, 1][int(np.digitize(v, [.4, .7]))], np.nan, home[u]))
        members = np.where((home == target[j]) & (np.arange(U) < K * per_cluster))[0]
        for u in rng.choice(members, fid_raters, replace=False):
            fb = {0: .9, 1: .3, 2: .1, 3: .6}[typ[j]]
            v = np.clip(fb + rng.normal(0, .2), 0, 1)
            rows.append((j, u, np.nan, [0, .5, 1][int(np.digitize(v, [.4, .7]))], home[u]))
        if brigade and typ[j] == 2 and target[j] == 1:        # sybils sign strawmen of cluster 1
            for u in range(K * per_cluster, U):
                rows.append((j, u, np.nan, 1.0, 1))
    a = np.array(rows, dtype=float)
    R = Ratings(a[:, 0].astype(int), a[:, 1].astype(int), a[:, 2], a[:, 3], a[:, 4].astype(int))
    C = Contribs(rng.integers(0, U, n_notes), author_c, target, np.array(["note"] * n_notes))
    return R, C, M, typ

def run(brigade=0, seed=0):
    R, C, M, typ = simulate(seed=seed, brigade=brigade)
    th, cfg = Thresholds(), MFConfig()
    hmask = ~np.isnan(R.help)
    Rh = Ratings(R.contrib[hmask], R.rater[hmask], R.help[hmask], R.fid[hmask], R.rater_cluster[hmask])
    port = score_portability(Rh, C, M, th, cfg)
    fid = score_fidelity(R, C, th, cfg)
    st = np.array([combined_status(port["status"][j], fid["F"][j], fid["n"][j], fid["split"][j], "note", th)
                   for j in range(len(typ))])
    return typ, st, port, fid, C

def test_status_by_type():
    typ, st, port, fid, C = run()
    good = np.isin(st[typ == 0], ["ratified_helpful", "ratified"]).mean()
    tribal_pass = np.isin(st[typ == 1], ["helpful", "ratified_helpful"]).mean()
    straw_ratified = np.isin(st[typ == 2], ["ratified", "ratified_helpful"]).mean()
    print(f"accurate-bridging ratified: {good:.2f}  tribal marked helpful: {tribal_pass:.2f}  strawman ratified: {straw_ratified:.2f}")
    print("mean i_n by type:", [round(float(port['params'].i_n[typ == t].mean()), 3) for t in range(4)])
    print("mean F by type:  ", [round(float(np.nanmean(fid['F'][typ == t])), 3) for t in range(4)])
    assert good >= 0.75 and tribal_pass == 0 and straw_ratified == 0    # 0.75 = the S-honest threshold (Plan §4.3)

def test_brigade_cannot_ratify_strawman():
    typ, st, port, fid, C = run(brigade=15)
    sel = (typ == 2) & (C.target == 1)
    print("brigaded strawmen statuses:", sorted(set(st[sel])), "F:", np.round(fid["F"][sel], 2))
    assert not np.isin(st[sel], ["ratified", "ratified_helpful"]).any()

if __name__ == "__main__":
    test_status_by_type(); test_brigade_cannot_ratify_strawman(); print("ok")
```
