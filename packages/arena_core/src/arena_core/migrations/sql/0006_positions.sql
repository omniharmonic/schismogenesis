-- Positions: shared, named answers to a live question (D-31.13). ADR-032.

CREATE TABLE position (
  position_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  live_question_id uuid NOT NULL REFERENCES live_question(live_question_id),
  key              text NOT NULL,                -- stable slug within the question
  status           text NOT NULL DEFAULT 'provisional'
     CHECK (status IN ('provisional','ratified','contested','retired')),
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S11',
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  UNIQUE (live_question_id, key)
);

-- Who defined a position, in whose words. Append-only: a new wording is a new row. Models bootstrap;
-- people placed in the relevant niche or cluster replace those drafts and ratify the result.
CREATE TABLE position_definition (
  definition_id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  position_id      uuid NOT NULL REFERENCES position(position_id),
  version          int NOT NULL,
  label            text NOT NULL CHECK (length(label) BETWEEN 3 AND 120),
  statement        text NOT NULL CHECK (length(statement) BETWEEN 10 AND 600),
  author_kind      text NOT NULL CHECK (author_kind IN ('model','niche_member','steward')),
  author_user_id   uuid REFERENCES app_user(user_id),
  author_model     text,
  niche_id         text REFERENCES niche(niche_id),
  cluster_id       uuid REFERENCES cluster(cluster_id),
  ratified_at      timestamptz,
  created_at       timestamptz NOT NULL DEFAULT now(),
  UNIQUE (position_id, version),
  CHECK ((author_kind = 'model') = (author_model IS NOT NULL)),
  CHECK (author_kind = 'model' OR author_user_id IS NOT NULL),
  CHECK (author_kind <> 'model' OR ratified_at IS NULL)  -- a model's wording is never ratified
);
CREATE RULE position_definition_no_delete AS ON DELETE TO position_definition DO INSTEAD NOTHING;

-- A person's evidenced holding of a position, with the reason kept visible.
CREATE TABLE position_holding (
  position_id      uuid NOT NULL REFERENCES position(position_id),
  person_id        text NOT NULL REFERENCES person(person_id),
  claim_id         uuid NOT NULL REFERENCES claim(claim_id),
  reason           text NOT NULL CHECK (length(reason) BETWEEN 3 AND 200),
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S11',
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  PRIMARY KEY (position_id, person_id, claim_id)
);
