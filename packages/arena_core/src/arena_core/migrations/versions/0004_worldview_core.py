"""Mark the landmarks in the written-first worldview core (D-31.12)."""

from alembic import op

revision = "0004_worldview_core"
down_revision = "0003_written_sources"


def upgrade() -> None:
    op.execute("ALTER TABLE landmark ADD COLUMN worldview_core boolean NOT NULL DEFAULT false")


def downgrade() -> None:
    op.execute("ALTER TABLE landmark DROP COLUMN worldview_core")
