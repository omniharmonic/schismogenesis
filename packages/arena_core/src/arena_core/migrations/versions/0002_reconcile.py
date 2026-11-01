"""Add spine tables missing from 08a §A1 and fix two constraint defects (ADR-029)."""

from alembic import op
from arena_core.migrations import SQL_DIR, run_script

revision = "0002_reconcile"
down_revision = "0001_initial"


def upgrade() -> None:
    run_script((SQL_DIR / "0002_reconcile.sql").read_text())


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX proposition_relation_edge;
        ALTER TABLE proposition_relation ADD UNIQUE (from_id, to_id, type, scope, episode_id);
        DROP INDEX cluster_lineage_edge;
        DELETE FROM cluster_lineage WHERE to_cluster_id IS NULL;
        ALTER TABLE cluster_lineage ADD PRIMARY KEY (from_cluster_id, to_cluster_id);
        ALTER TABLE cluster_snapshot DROP COLUMN prompt_id, DROP COLUMN prompt_version;
        ALTER TABLE statement DROP COLUMN prompt_id, DROP COLUMN prompt_version;
        ALTER TABLE encounter DROP COLUMN prompt_id, DROP COLUMN prompt_version;
        ALTER TABLE chunk DROP COLUMN prompt_id, DROP COLUMN prompt_version;
        ALTER DEFAULT PRIVILEGES IN SCHEMA ops REVOKE SELECT ON TABLES FROM arena_operator_ro;
        DROP SCHEMA ops CASCADE;
        DROP TABLE admin_approval;
        DROP TABLE gpu_window;
        DROP FUNCTION take_token(text, real, real);
        DROP TABLE rate_bucket;
        """
    )
