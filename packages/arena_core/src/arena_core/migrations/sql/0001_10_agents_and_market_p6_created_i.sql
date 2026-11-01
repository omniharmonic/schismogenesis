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

