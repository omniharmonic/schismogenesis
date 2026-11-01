-- ===================================================================
-- 3. Media: channel, content_group, episode, appearance, encounter
-- ===================================================================
CREATE TABLE channel (
  channel_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  platform        text NOT NULL CHECK (platform IN ('youtube','podcast_rss','substack','bluesky','x','website')),
  title           text NOT NULL,
  external_ids    jsonb NOT NULL DEFAULT '{}',    -- {yt_channel_id, uploads_playlist_id, podcastindex_feed_id, itunes_collection_id, rss_url, podcast_guid}
  owner_person_id text REFERENCES person(person_id),
  show_format_prior text,
  default_transcript_route text,
  last_crawled_at timestamptz, etag text, block_rate_7d real,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S1',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL
);
CREATE UNIQUE INDEX channel_yt ON channel ((external_ids->>'yt_channel_id')) WHERE external_ids ? 'yt_channel_id';
CREATE UNIQUE INDEX channel_rss ON channel ((external_ids->>'rss_url')) WHERE external_ids ? 'rss_url';

CREATE TABLE content_group (
  content_group_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  canonical_title  text NOT NULL,
  published_at     timestamptz,
  created_at       timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE episode (
  episode_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  channel_id      uuid NOT NULL REFERENCES channel(channel_id),
  content_group_id uuid REFERENCES content_group(content_group_id),
  platform        text NOT NULL,
  external_id     text NOT NULL,                  -- YouTube video id or RSS guid
  url             text NOT NULL,
  title           text NOT NULL,
  description     text,
  published_at    timestamptz,
  duration_s      int,
  language        text DEFAULT 'en',
  format          text CHECK (format IN ('interview','debate','panel','solo','roundtable','clip','compilation','essay','unknown')),
  audio_url       text,                           -- RSS enclosure
  discovered_via  jsonb NOT NULL DEFAULT '[]',    -- [{method, query, api, at}]
  transcript_status text NOT NULL DEFAULT 'unknown'
     CHECK (transcript_status IN ('unknown','yt_caption_available','publisher_transcript','none','queued','fetched','failed','asr_queued')),
  rights_status   text NOT NULL DEFAULT 'public_unlicensed'
     CHECK (rights_status IN ('public_unlicensed','publisher_published_transcript','opted_in','licensed','takedown_requested','removed')),
  selected_for    text[] NOT NULL DEFAULT '{}',   -- coverage | baseline | event_map
  selection_run_id uuid REFERENCES pipeline_run(run_id),
  title_embedding halfvec(1024),
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S1',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  UNIQUE (platform, external_id)
);
CREATE INDEX episode_channel_pub ON episode (channel_id, published_at DESC);
CREATE INDEX episode_selected ON episode USING gin (selected_for);

CREATE TABLE appearance (
  appearance_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),
  person_id       text REFERENCES person(person_id),   -- null until resolved (S2)
  mention_text    text NOT NULL,                       -- raw string from title/description
  role            appearance_role,
  mention_type    mention_type NOT NULL DEFAULT 'present',
  evidence        text[] NOT NULL,                     -- title | description | show_notes | podcast_person_tag | channel_owner | diarization
  resolution_confidence real CHECK (resolution_confidence BETWEEN 0 AND 1),
  resolution_method text,
  speaking_share  real,
  status          text NOT NULL DEFAULT 'candidate'
     CHECK (status IN ('candidate','accepted','review','rejected','verified_by_audio')),
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL,
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  superseded_by   uuid REFERENCES appearance(appearance_id)
);
CREATE INDEX appearance_person ON appearance (person_id) WHERE status IN ('accepted','verified_by_audio');
CREATE INDEX appearance_episode ON appearance (episode_id);

-- Derived edge: one row per cross-niche landmark pair per content group.
CREATE TABLE encounter (
  encounter_id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content_group_id uuid NOT NULL REFERENCES content_group(content_group_id),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),   -- representative episode
  person_a text NOT NULL REFERENCES landmark(landmark_id), person_b text NOT NULL REFERENCES landmark(landmark_id),
  niche_a  text NOT NULL REFERENCES niche(niche_id),       niche_b  text NOT NULL REFERENCES niche(niche_id),
  type            text NOT NULL CHECK (type IN ('host_guest','co_guest','debate','panel')),
  niche_distance_prior real NOT NULL, quality_score real NOT NULL, confidence real NOT NULL,
  sign            text NOT NULL DEFAULT 'unknown' CHECK (sign IN ('unknown','integrative','sparring','mixed')),
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S3',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  CHECK (niche_a < niche_b), CHECK (person_a <> person_b),
  UNIQUE (content_group_id, person_a, person_b, run_id)
);

