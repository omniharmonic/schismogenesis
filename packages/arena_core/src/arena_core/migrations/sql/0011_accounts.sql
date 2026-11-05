-- Accounts (docs/superpowers/specs/2026-11-05-accounts-and-people-map-design.md): one account,
-- reached by Bluesky, X, email or a private key; answers saved per season; nothing public unless
-- the person switches on show_on_map.

CREATE TABLE account (
  account_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  display_name text CHECK (length(display_name) <= 80),
  avatar_url   text,
  bio          text CHECK (length(bio) <= 160),
  show_on_map  boolean NOT NULL DEFAULT false,
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE account_login (
  kind       text NOT NULL CHECK (kind IN ('bsky','x','email','key')),
  subject    text NOT NULL,                    -- bsky DID, X user id, lower-cased email, sha256 of key
  account_id uuid NOT NULL REFERENCES account(account_id) ON DELETE CASCADE,
  handle     text,                             -- shown to the owner only, unless show_on_map
  avatar_url text,
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (kind, subject)
);
CREATE INDEX account_login_account ON account_login (account_id);

CREATE TABLE account_session (
  token_hash   bytea PRIMARY KEY,
  account_id   uuid NOT NULL REFERENCES account(account_id) ON DELETE CASCADE,
  created_at   timestamptz NOT NULL DEFAULT now(),
  last_seen_at timestamptz NOT NULL DEFAULT now(),
  expires_at   timestamptz NOT NULL
);
CREATE INDEX account_session_account ON account_session (account_id);

CREATE TABLE auth_flow (                         -- OAuth state, PKCE verifier, DPoP key: 15 minutes
  state      text PRIMARY KEY,
  kind       text NOT NULL,
  data       jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE email_token (
  token_hash bytea PRIMARY KEY,
  email      text NOT NULL,
  code_hash  bytea NOT NULL,
  attempts   int NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now(),
  used_at    timestamptz
);
CREATE INDEX email_token_email ON email_token (email, created_at DESC);

CREATE TABLE account_sheet (
  account_id     uuid NOT NULL REFERENCES account(account_id) ON DELETE CASCADE,
  season         text NOT NULL,
  answers        jsonb NOT NULL,
  x              real,
  y              real,
  nearest        text,
  participant_id uuid REFERENCES room_participant(participant_id) ON DELETE SET NULL,
  updated_at     timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (account_id, season)
);
