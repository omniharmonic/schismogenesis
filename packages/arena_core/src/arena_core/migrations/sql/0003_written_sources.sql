-- Written works (books, essays, blogs, letters, dissertations) as first-class sources. ADR-030.
-- An episode is any content item; a transcript is its text; a segment is a located span.

ALTER TYPE appearance_role ADD VALUE IF NOT EXISTS 'author';
ALTER TYPE appearance_role ADD VALUE IF NOT EXISTS 'co_author';

ALTER TABLE channel DROP CONSTRAINT channel_platform_check;
ALTER TABLE channel ADD CONSTRAINT channel_platform_check CHECK (platform IN
  ('youtube','podcast_rss','substack','bluesky','x','website','blog','book_publisher','journal','filing'));

ALTER TABLE episode DROP CONSTRAINT episode_format_check;
ALTER TABLE episode ADD CONSTRAINT episode_format_check CHECK (format IN
  ('interview','debate','panel','solo','roundtable','clip','compilation','essay','unknown',
   'book','book_chapter','blog_post','op_ed','lecture','letter','dissertation','filing'));

-- How much the text can be taken as the author's own sincere voice. Pseudonyms, ghostwriting,
-- co-authors and corporate letters all change what a stance attribution can claim.
ALTER TABLE episode ADD COLUMN authorship text NOT NULL DEFAULT 'own_name'
  CHECK (authorship IN ('own_name','pseudonymous','co_authored','corporate','ghostwritten_or_edited'));

ALTER TABLE transcript DROP CONSTRAINT transcript_route_check;
ALTER TABLE transcript ADD CONSTRAINT transcript_route_check CHECK (route IN
  ('yt_caption_auto','yt_caption_creator','publisher','stt_selfhosted','opt_in_oauth','written_source'));

-- Written text has no clock. A span is located by time, or by a locator such as
-- {"chapter": 3, "page": 41, "paragraph": 2}. Every span must have one or the other.
ALTER TABLE private.segment ALTER COLUMN start_ms DROP NOT NULL;
ALTER TABLE private.segment ALTER COLUMN end_ms DROP NOT NULL;
ALTER TABLE private.segment ADD COLUMN locator jsonb;
ALTER TABLE private.segment ADD CONSTRAINT segment_located
  CHECK ((start_ms IS NOT NULL AND end_ms IS NOT NULL) OR locator IS NOT NULL);

ALTER TABLE chunk ALTER COLUMN start_ms DROP NOT NULL;
ALTER TABLE chunk ALTER COLUMN end_ms DROP NOT NULL;
ALTER TABLE chunk ADD COLUMN locator jsonb;
ALTER TABLE chunk ADD CONSTRAINT chunk_located
  CHECK ((start_ms IS NOT NULL AND end_ms IS NOT NULL) OR locator IS NOT NULL);

ALTER TABLE claim ADD COLUMN locator jsonb;
