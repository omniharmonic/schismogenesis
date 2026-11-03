-- Rooms: Polis-style voting with Community Notes-style bridging (ADR-036).
-- Separate from the Slice 1 statement/reaction tables, which need pipeline claims and accounts.
CREATE TABLE room (
  room_id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  slug           text UNIQUE NOT NULL CHECK (slug ~ '^[a-z0-9-]{2,40}$'),
  title          text NOT NULL,
  description    text NOT NULL DEFAULT '',
  status         text NOT NULL DEFAULT 'open' CHECK (status IN ('open','closed')),
  bundle_version text NOT NULL,
  config         jsonb NOT NULL DEFAULT '{}',
  created_at     timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE room_participant (
  participant_id  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id         uuid NOT NULL REFERENCES room(room_id),
  key_hash        bytea NOT NULL,                -- sha256 of a secret held only by the browser
  handle          text CHECK (handle IS NULL OR length(handle) <= 40),  -- self-declared, unverified
  is_synthetic    boolean NOT NULL DEFAULT false,
  consent_version text NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE room_statement (
  statement_id  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id       uuid NOT NULL REFERENCES room(room_id),
  text          text NOT NULL,
  origin        text NOT NULL CHECK (origin IN ('anchor','participant','agent')),
  anchor_id     text,
  author_id     uuid REFERENCES room_participant(participant_id),
  status        text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected')),
  reject_reason text,
  created_at    timestamptz NOT NULL DEFAULT now(),
  moderated_at  timestamptz,
  UNIQUE (room_id, anchor_id),
  CHECK ((origin = 'anchor') = (anchor_id IS NOT NULL))
);
CREATE INDEX room_statement_room ON room_statement (room_id, status);

CREATE TABLE room_vote (
  participant_id uuid NOT NULL REFERENCES room_participant(participant_id),
  statement_id   uuid NOT NULL REFERENCES room_statement(statement_id),
  vote           smallint NOT NULL CHECK (vote IN (-1, 0, 1)),
  updated_at     timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (participant_id, statement_id)
);
CREATE INDEX room_vote_statement ON room_vote (statement_id);

CREATE TABLE room_vote_event (                  -- append-only history of every vote
  event_id       bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  participant_id uuid NOT NULL REFERENCES room_participant(participant_id),
  statement_id   uuid NOT NULL REFERENCES room_statement(statement_id),
  vote           smallint NOT NULL,
  created_at     timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE placement_dispute (
  dispute_id  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  person_id   text NOT NULL,
  anchor_id   text,
  body        text NOT NULL CHECK (length(body) BETWEEN 5 AND 2000),
  contact     text CHECK (contact IS NULL OR length(contact) <= 200),
  status      text NOT NULL DEFAULT 'open' CHECK (status IN ('open','answered','closed')),
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE fairness_rating (
  rating_id      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  bundle_version text NOT NULL,
  rating         smallint NOT NULL CHECK (rating BETWEEN 1 AND 5),
  created_at     timestamptz NOT NULL DEFAULT now()
);
