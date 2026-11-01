"""Positions, their definition history, and evidenced holdings (D-31.13, ADR-032)."""

from alembic import op
from arena_core.migrations import SQL_DIR, run_script

revision = "0006_positions"
down_revision = "0005_claim_type_and_scope"


def upgrade() -> None:
    run_script((SQL_DIR / "0006_positions.sql").read_text())


def downgrade() -> None:
    op.execute("DROP TABLE position_holding; DROP TABLE position_definition; DROP TABLE position")
