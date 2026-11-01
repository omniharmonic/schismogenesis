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

