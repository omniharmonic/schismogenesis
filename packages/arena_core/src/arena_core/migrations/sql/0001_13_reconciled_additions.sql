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
