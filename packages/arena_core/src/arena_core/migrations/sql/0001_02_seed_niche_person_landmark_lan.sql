-- ===================================================================
-- 2. Seed: niche, person, landmark, landmark_niche
-- ===================================================================
CREATE TABLE niche (
  niche_id        text PRIMARY KEY,               -- kebab slug from SEED-v4
  name            text NOT NULL,
  domain          text NOT NULL,                  -- 'd3-tech-futures'
  cross_domains   text[] NOT NULL DEFAULT '{}',
  aliases         jsonb NOT NULL DEFAULT '[]',    -- [{text, kind: self|outsider}]
  description     text,
  telos           text, sacred_values jsonb, existential_threats jsonb,
  combatant_niche_ids text[] NOT NULL DEFAULT '{}',
  adjacent_niche_ids  text[] NOT NULL DEFAULT '{}',
  placement_prior jsonb,                          -- {left_right, atlas_accelerate_restrain, atlas_institutions_exit, basis}
  slice_tier      text CHECK (slice_tier IN ('core','adjacent')),   -- null = not in Slice 1
  sampling_budget_hours numeric(6,1) NOT NULL DEFAULT 15,
  seed_version    text NOT NULL,                  -- 'SEED-v4'
  version         int NOT NULL DEFAULT 1,
  merged_from     text[] NOT NULL DEFAULT '{}',
  valid_from      date NOT NULL DEFAULT current_date,
  valid_to        date,
  raw             jsonb NOT NULL                  -- full seed record, for audit
);

-- Every named public speaker. Landmarks are persons admitted to the seed panel.
CREATE TABLE person (
  person_id       text PRIMARY KEY,               -- landmark_id for landmarks; 'p-'||uuid for others
  display_name    text NOT NULL,
  aliases         jsonb NOT NULL DEFAULT '[]',    -- [{text, kind: legal|stage|handle|misspelling|nickname, source}]
  wikidata_qid    text,
  is_public_figure boolean NOT NULL,
  ambiguous_name  boolean NOT NULL DEFAULT false,
  voiceprint_ref  text,                           -- MinIO key; internal only
  created_at      timestamptz NOT NULL DEFAULT now(),
  CHECK (is_public_figure)                        -- red line: private individuals are never stored by name
);
CREATE INDEX person_name_trgm ON person USING gin (display_name gin_trgm_ops);

CREATE TABLE landmark (
  landmark_id     text PRIMARY KEY REFERENCES person(person_id),
  name            text NOT NULL,
  primary_niche_id text NOT NULL REFERENCES niche(niche_id),
  role            text NOT NULL CHECK (role IN ('core','bridger','edge')),
  platforms       jsonb NOT NULL DEFAULT '{}',
  longform_output text,
  verification    text NOT NULL,                  -- verified-active | pending | stale | excluded
  in_slice        text,                           -- 'slice-1' | null
  flag_type       text,                           -- exclusion-review | conflict-of-interest | minor-adjacent
  public_surface_allowed boolean NOT NULL,        -- false for all 20 in SEED-v4 flags_for_benjamin: the 15 flagged (14 exclusion-review
                                                  -- + 1 minor-adjacent, OD-01) and the 5 conflict-of-interest checks until signed off (OD-02)
  claim_status    text NOT NULL DEFAULT 'unclaimed' CHECK (claim_status IN ('unclaimed','claimed','opted_in')),
  panel_status    text NOT NULL DEFAULT 'core_panel' CHECK (panel_status IN ('core_panel','newcomer','retired','excluded')),
  gender          text,                           -- aggregate balance audit only; never exported
  seed_version    text NOT NULL,
  raw             jsonb NOT NULL
);
CREATE INDEX landmark_slice ON landmark (in_slice) WHERE in_slice IS NOT NULL;

CREATE TABLE landmark_niche (
  landmark_id     text NOT NULL REFERENCES landmark(landmark_id),
  niche_id        text NOT NULL REFERENCES niche(niche_id),
  role            text NOT NULL CHECK (role IN ('core','bridger','edge')),
  is_primary      boolean NOT NULL,
  weight          real NOT NULL DEFAULT 1.0,      -- 0.5 for secondary (OPEN-4)
  valid_from      date NOT NULL DEFAULT '2024-01-01',
  valid_to        date,
  basis           text,
  PRIMARY KEY (landmark_id, niche_id, valid_from)
);
CREATE UNIQUE INDEX landmark_one_primary ON landmark_niche (landmark_id) WHERE is_primary AND valid_to IS NULL;

