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

