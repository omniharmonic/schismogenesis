"""Support written works as sources alongside spoken episodes (ADR-030)."""

from alembic import op
from arena_core.migrations import SQL_DIR, run_script

revision = "0003_written_sources"
down_revision = "0002_reconcile"


def upgrade() -> None:
    run_script((SQL_DIR / "0003_written_sources.sql").read_text())


def downgrade() -> None:
    """Dev and CI only. Postgres cannot drop enum values, so the two new roles remain."""
    op.execute(
        """
        ALTER TABLE claim DROP COLUMN locator;
        DELETE FROM chunk WHERE start_ms IS NULL;
        ALTER TABLE chunk DROP CONSTRAINT chunk_located, DROP COLUMN locator;
        ALTER TABLE chunk ALTER COLUMN start_ms SET NOT NULL, ALTER COLUMN end_ms SET NOT NULL;
        DELETE FROM private.segment WHERE start_ms IS NULL;
        ALTER TABLE private.segment DROP CONSTRAINT segment_located, DROP COLUMN locator;
        ALTER TABLE private.segment ALTER COLUMN start_ms SET NOT NULL,
          ALTER COLUMN end_ms SET NOT NULL;
        DELETE FROM transcript WHERE route = 'written_source';
        ALTER TABLE transcript DROP CONSTRAINT transcript_route_check;
        ALTER TABLE transcript ADD CONSTRAINT transcript_route_check CHECK (route IN
          ('yt_caption_auto','yt_caption_creator','publisher','stt_selfhosted','opt_in_oauth'));
        ALTER TABLE episode DROP COLUMN authorship;
        DELETE FROM episode WHERE format IN ('book','book_chapter','blog_post','op_ed','lecture',
          'letter','dissertation','filing');
        ALTER TABLE episode DROP CONSTRAINT episode_format_check;
        ALTER TABLE episode ADD CONSTRAINT episode_format_check CHECK (format IN
          ('interview','debate','panel','solo','roundtable','clip','compilation','essay',
           'unknown'));
        DELETE FROM channel WHERE platform IN ('blog','book_publisher','journal','filing');
        ALTER TABLE channel DROP CONSTRAINT channel_platform_check;
        ALTER TABLE channel ADD CONSTRAINT channel_platform_check CHECK (platform IN
          ('youtube','podcast_rss','substack','bluesky','x','website'));
        """
    )
