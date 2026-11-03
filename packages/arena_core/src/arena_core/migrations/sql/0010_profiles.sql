-- Launch round (docs/fingerprint/04-LAUNCH.md): published profiles, identity checks, report cache,
-- shared rate limits and daily counters.

CREATE TABLE identity_check (
  check_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind          text NOT NULL CHECK (kind IN ('bsky','x')),
  handle        text,
  challenge     text,                          -- bsky: code to post; x: OAuth state
  code_verifier text,                          -- x: PKCE verifier, cleared once used
  display_name  text,
  avatar_url    text,
  account_id    text,                          -- bsky DID or X user id
  verified_at   timestamptz,
  used_at       timestamptz,                   -- a check backs one profile only
  created_at    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX identity_check_challenge ON identity_check (challenge);

CREATE TABLE profile (
  profile_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  code            text UNIQUE NOT NULL CHECK (code ~ '^[a-z0-9]{6,12}$'),
  edit_hash       bytea NOT NULL,              -- sha256 of a key held only by the publisher's browser
  identity        text NOT NULL CHECK (identity IN ('anon','bsky','x')),
  handle          text,
  display_name    text NOT NULL CHECK (length(display_name) <= 80),
  avatar_url      text,
  account_id      text,
  check_id        uuid REFERENCES identity_check(check_id),
  listed          boolean NOT NULL DEFAULT false,
  include_answers boolean NOT NULL DEFAULT false,
  summary         jsonb NOT NULL,
  answers         jsonb,                       -- only when include_answers
  glyph           jsonb NOT NULL,              -- answer values in a scrambled order (result-only)
  bundle_version  text NOT NULL,
  hidden_at       timestamptz,                 -- set by a moderator
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  CHECK ((identity = 'anon') = (handle IS NULL)),
  CHECK (identity = 'anon' OR check_id IS NOT NULL),
  CHECK (include_answers OR answers IS NULL)
);
CREATE INDEX profile_listed ON profile (created_at DESC) WHERE listed AND hidden_at IS NULL;

CREATE TABLE report_cache (
  room_id     uuid PRIMARY KEY REFERENCES room(room_id),
  version     text NOT NULL,
  report      jsonb NOT NULL,
  personal    jsonb NOT NULL,                  -- per-participant measures; served only to each one
  computed_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE rate_hit (
  bucket text NOT NULL,
  at     timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX rate_hit_bucket ON rate_hit (bucket, at);

CREATE TABLE daily_counter (                   -- counts only: no ids, no cookies
  day  date NOT NULL DEFAULT current_date,
  name text NOT NULL,
  n    bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (day, name)
);
