-- Accounts round 2 (docs/superpowers/specs/2026-11-05-accounts-round-2-design.md): one public
-- results page per account, profile details from Bluesky/X, and camp-name proposals and votes.

ALTER TABLE profile ADD COLUMN owner_id uuid UNIQUE REFERENCES account(account_id) ON DELETE CASCADE;
ALTER TABLE profile DROP CONSTRAINT profile_check1;
ALTER TABLE profile ADD CONSTRAINT profile_verified
  CHECK (identity = 'anon' OR check_id IS NOT NULL OR owner_id IS NOT NULL);

ALTER TABLE account_login ADD COLUMN details jsonb;   -- public profile fields from the provider

CREATE TABLE camp_name (
  name_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  season      text NOT NULL,
  node        text NOT NULL,                    -- tree node id (camp or school)
  name        text NOT NULL CHECK (length(name) BETWEEN 3 AND 48),
  account_id  uuid REFERENCES account(account_id) ON DELETE SET NULL,
  status      text NOT NULL DEFAULT 'open' CHECK (status IN ('open','accepted','declined')),
  created_at  timestamptz NOT NULL DEFAULT now(),
  decided_at  timestamptz,
  UNIQUE (season, node, name)
);

CREATE TABLE camp_name_vote (
  name_id    uuid NOT NULL REFERENCES camp_name(name_id) ON DELETE CASCADE,
  account_id uuid NOT NULL REFERENCES account(account_id) ON DELETE CASCADE,
  up         boolean NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (name_id, account_id)
);

CREATE TABLE public_cache (                   -- shared copies of public, aggregate answers
  key         text PRIMARY KEY,
  data        jsonb NOT NULL,
  computed_at timestamptz NOT NULL DEFAULT now()
);
