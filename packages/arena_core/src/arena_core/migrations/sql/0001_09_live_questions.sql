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

