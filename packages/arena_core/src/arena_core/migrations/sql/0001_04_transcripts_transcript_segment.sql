-- ===================================================================
-- 4. Transcripts: transcript, segment (private), chunk
-- ===================================================================
CREATE TABLE transcript (
  transcript_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),
  route           text NOT NULL CHECK (route IN ('yt_caption_auto','yt_caption_creator','publisher','stt_selfhosted','opt_in_oauth')),
  language        text NOT NULL DEFAULT 'en',
  has_diarization boolean NOT NULL, has_word_timestamps boolean NOT NULL,
  quality         jsonb NOT NULL DEFAULT '{}',    -- {est_wer, caption_kind, asr_model}
  storage_ref     text NOT NULL,                  -- MinIO key: raw caption file / ASR JSON with words
  rights_basis    text NOT NULL,
  retention_until date,
  is_current      boolean NOT NULL DEFAULT true,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL,
  model_name text NOT NULL, model_version text NOT NULL, prompt_id text, prompt_version text,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL
);
CREATE UNIQUE INDEX transcript_current ON transcript (episode_id) WHERE is_current;

CREATE TABLE private.segment (                    -- = Topology Live Utterance
  segment_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  transcript_id   uuid NOT NULL REFERENCES transcript(transcript_id) ON DELETE CASCADE,
  seq             int NOT NULL,
  start_ms        int NOT NULL, end_ms int NOT NULL CHECK (end_ms >= start_ms),
  text            text NOT NULL,
  diar_label      text,
  person_id       text REFERENCES person(person_id),     -- null = unknown; never a private individual
  speaker_kind    text NOT NULL DEFAULT 'unknown' CHECK (speaker_kind IN ('person','non_public','unknown')),
  attribution     jsonb NOT NULL DEFAULT '{}',           -- {confidence, signals:{metadata,voiceprint,caption_cue,llm}, confirmed_by}
  attribution_confidence real NOT NULL DEFAULT 0,
  UNIQUE (transcript_id, seq)
);
CREATE INDEX segment_person ON private.segment (person_id, transcript_id);

CREATE TABLE chunk (
  chunk_id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  transcript_id   uuid NOT NULL REFERENCES transcript(transcript_id),
  episode_id      uuid NOT NULL REFERENCES episode(episode_id),
  seq             int NOT NULL,
  segment_ids     uuid[] NOT NULL,                -- ordered; core segments + overlap context
  core_from_seq   int NOT NULL, core_to_seq int NOT NULL,   -- claims must anchor inside the core
  start_ms        int NOT NULL, end_ms int NOT NULL,
  speakers        text[] NOT NULL,
  token_estimate  int NOT NULL,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S6',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
  superseded_by   uuid REFERENCES chunk(chunk_id),
  UNIQUE (transcript_id, seq, model_version)
);

