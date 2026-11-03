"""Rooms, participants, statements, votes, disputes and fairness ratings (ADR-036)."""

from alembic import op
from arena_core.migrations import SQL_DIR, run_script

revision = "0009_rooms"
down_revision = "0008_memes"


def upgrade() -> None:
    run_script((SQL_DIR / "0009_rooms.sql").read_text())


def downgrade() -> None:
    op.execute(
        "DROP TABLE fairness_rating; DROP TABLE placement_dispute; DROP TABLE room_vote_event;"
        " DROP TABLE room_vote; DROP TABLE room_statement; DROP TABLE room_participant;"
        " DROP TABLE room"
    )
