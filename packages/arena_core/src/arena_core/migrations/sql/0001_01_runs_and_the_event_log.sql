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

