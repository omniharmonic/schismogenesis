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

