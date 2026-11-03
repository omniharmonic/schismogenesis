"""Profiles, identity checks, report cache, rate limits and counters (04-LAUNCH.md)."""

from alembic import op
from arena_core.migrations import SQL_DIR, run_script

revision = "0010_profiles"
down_revision = "0009_rooms"


def upgrade() -> None:
    run_script((SQL_DIR / "0010_profiles.sql").read_text())


def downgrade() -> None:
    op.execute(
        "DROP TABLE daily_counter; DROP TABLE rate_hit; DROP TABLE report_cache;"
        " DROP TABLE profile; DROP TABLE identity_check"
    )
