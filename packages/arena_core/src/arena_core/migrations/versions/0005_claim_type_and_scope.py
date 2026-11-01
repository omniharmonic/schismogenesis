"""Keep tl_type and quantifier on claims, since propositions are built from them later."""

from alembic import op

revision = "0005_claim_type_and_scope"
down_revision = "0004_worldview_core"


def upgrade() -> None:
    op.execute("ALTER TABLE claim ADD COLUMN tl_type text, ADD COLUMN quantifier text")


def downgrade() -> None:
    op.execute("ALTER TABLE claim DROP COLUMN tl_type, DROP COLUMN quantifier")
