"""Record what job a claim's sentence does in its author's argument (ADR-033)."""

from alembic import op

revision = "0007_claim_argument_role"
down_revision = "0006_positions"


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE claim ADD COLUMN argument_role text CHECK (argument_role IN
          ('own_assertion','concession','others_view','setup','conditional','hypothetical',
           'ironic','unclear'));
        ALTER TABLE claim ADD COLUMN role_fair boolean;
        """
    )


def downgrade() -> None:
    op.execute("ALTER TABLE claim DROP COLUMN argument_role, DROP COLUMN role_fair")
