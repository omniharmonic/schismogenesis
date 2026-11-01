-- Everything the spine requires that docs/08a §A1 does not provide. See docs/adr/ADR-029.

-- Tables defined in 08 prose (§7, §10.4, §10.5) and listed in SPINE §10.3, absent from §A1.
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

CREATE TABLE gpu_window (
  name       text PRIMARY KEY,
  starts_at  timestamptz NOT NULL,
  ends_at    timestamptz NOT NULL,
  state      text NOT NULL
);

CREATE TABLE admin_approval (
  approval_id  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind         text NOT NULL CHECK (kind IN ('paid_api','public_launch','standing_weekly_publish',
                                             'yt_audio_channel','snapshot_publish','landmark_contact','agent_platform')),
  scope        jsonb NOT NULL DEFAULT '{}',
  approved_by  text NOT NULL,
  approved_at  timestamptz NOT NULL DEFAULT now(),
  expires_at   timestamptz,
  revoked_at   timestamptz
);

-- Operator views land here with the worker; the schema and its grant are the P0 part.
CREATE SCHEMA ops;
GRANT USAGE ON SCHEMA ops TO arena_operator_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA ops GRANT SELECT ON TABLES TO arena_operator_ro;

-- Spine §5: every derived row carries prompt_id and prompt_version (null for code stages).
ALTER TABLE chunk            ADD COLUMN prompt_id text, ADD COLUMN prompt_version text;
ALTER TABLE encounter        ADD COLUMN prompt_id text, ADD COLUMN prompt_version text;
ALTER TABLE statement        ADD COLUMN prompt_id text, ADD COLUMN prompt_version text;
ALTER TABLE cluster_snapshot ADD COLUMN prompt_id text, ADD COLUMN prompt_version text;

-- §A1 says to_cluster_id is null for 'fades', but a primary key forces NOT NULL, so a fading
-- cluster could never be recorded.
ALTER TABLE cluster_lineage DROP CONSTRAINT cluster_lineage_pkey;
ALTER TABLE cluster_lineage ALTER COLUMN to_cluster_id DROP NOT NULL;
CREATE UNIQUE INDEX cluster_lineage_edge ON cluster_lineage (from_cluster_id, to_cluster_id) NULLS NOT DISTINCT;

-- Bank-scope relations have a null episode_id, and plain UNIQUE treats nulls as different,
-- so the same relation could be stored repeatedly.
ALTER TABLE proposition_relation DROP CONSTRAINT proposition_relation_from_id_to_id_type_scope_episode_id_key;
CREATE UNIQUE INDEX proposition_relation_edge ON proposition_relation (from_id, to_id, type, scope, episode_id) NULLS NOT DISTINCT;
