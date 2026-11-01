"""Initial schema: the full DDL of docs/08a §A1 and §A1.1, executed in its ordered chunks.

The sql/0001_*.sql files are a verbatim copy of the appendix (tests/test_schema.py compares them).
Fixes and additions belong in later revisions, never here.
"""

import re

from alembic import op
from arena_core.migrations import SQL_DIR, run_script

revision = "0001_initial"
down_revision = None

ROLES = ("arena_api", "arena_worker", "arena_operator_ro")


def _guard_create_role(sql: str) -> str:
    """Roles belong to the whole Postgres server, so they can pre-exist from another database."""
    return re.sub(
        r"CREATE ROLE (\w+)\s+NOLOGIN;",
        r"DO $do$ BEGIN CREATE ROLE \1 NOLOGIN; "
        r"EXCEPTION WHEN duplicate_object THEN NULL; END $do$;",
        sql,
    )


def upgrade() -> None:
    for path in sorted(SQL_DIR.glob("0001_*.sql")):
        run_script(_guard_create_role(path.read_text()))


def downgrade() -> None:
    """Dev and CI only. Production migrations are forward-only (08 §3.7)."""
    op.execute(
        """
        DROP SCHEMA private CASCADE;
        DROP VIEW quota_ledger;
        DO $do$
        DECLARE r record;
        BEGIN
          FOR r IN SELECT tablename FROM pg_tables
                   WHERE schemaname = 'public' AND tablename <> 'alembic_version' LOOP
            EXECUTE format('DROP TABLE %I CASCADE', r.tablename);
          END LOOP;
          FOR r IN SELECT t.typname FROM pg_type t
                   JOIN pg_namespace n ON n.oid = t.typnamespace
                   JOIN pg_enum e ON e.enumtypid = t.oid
                   WHERE n.nspname = 'public' GROUP BY 1 LOOP
            EXECUTE format('DROP TYPE %I', r.typname);
          END LOOP;
        END $do$;
        DROP FUNCTION rating_guard();
        DROP EXTENSION citext;
        DROP EXTENSION pg_trgm;
        DROP EXTENSION vector;
        """
    )
    for role in ROLES:
        # A role can still hold grants in another database on this server; leave it there.
        op.execute(
            f"DO $do$ BEGIN DROP ROLE IF EXISTS {role}; "
            "EXCEPTION WHEN dependent_objects_still_exist THEN NULL; END $do$;"
        )
