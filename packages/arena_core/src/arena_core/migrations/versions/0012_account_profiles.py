"""Account results pages, provider profile details, camp-name proposals and votes."""

from alembic import op
from arena_core.migrations import SQL_DIR, run_script

revision = "0012_account_profiles"
down_revision = "0011_accounts"


def upgrade() -> None:
    run_script((SQL_DIR / "0012_account_profiles.sql").read_text())


def downgrade() -> None:
    op.execute(
        "DROP TABLE public_cache; DROP TABLE camp_name_vote; DROP TABLE camp_name;"
        " ALTER TABLE account_login DROP COLUMN details;"
        " ALTER TABLE profile DROP CONSTRAINT profile_verified;"
        " ALTER TABLE profile ADD CONSTRAINT profile_check1"
        "   CHECK (identity = 'anon' OR check_id IS NOT NULL);"
        " ALTER TABLE profile DROP COLUMN owner_id"
    )
