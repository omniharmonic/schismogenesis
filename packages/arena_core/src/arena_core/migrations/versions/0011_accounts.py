"""Accounts: logins, sessions, saved answers (2026-11-05 accounts and people map design)."""

from alembic import op
from arena_core.migrations import SQL_DIR, run_script

revision = "0011_accounts"
down_revision = "0010_profiles"


def upgrade() -> None:
    run_script((SQL_DIR / "0011_accounts.sql").read_text())


def downgrade() -> None:
    op.execute(
        "DROP TABLE account_sheet; DROP TABLE email_token; DROP TABLE auth_flow;"
        " DROP TABLE account_session; DROP TABLE account_login; DROP TABLE account"
    )
