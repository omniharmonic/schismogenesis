import re

import pytest
from alembic import command
from arena_core.migrations import SQL_DIR
from conftest import REPO, alembic_config
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

# Row-level provenance, spine §5.
DERIVED = {
    "channel",
    "episode",
    "appearance",
    "encounter",
    "transcript",
    "chunk",
    "proposition",
    "claim",
    "stance",
    "proposition_relation",
    "statement",
    "cluster_snapshot",
    "live_question",
}
# Carry provenance through a parent run or snapshot, as designed in 08a.
DERIVED_VIA_PARENT = {
    "cluster": "snapshot_id",
    "cluster_membership": "snapshot_id",
    "niche_cluster_crosswalk": "snapshot_id",
    "cluster_lineage": "from_cluster_id",
    "live_question_proposition": "run_id",
    "contribution_score": "score_run_id",
    "reputation_score": "score_run_id",
    "understanding_cell": "score_run_id",
}
NOT_DERIVED = {
    "pipeline_run",
    "event_log",
    "stage_item",
    "llm_call",
    "niche",
    "person",
    "landmark",
    "landmark_niche",
    "content_group",
    "app_user",
    "reaction",
    "contribution",
    "rating",
    "agent",
    "agent_action",
    "strategy",
    "strategy_assignment",
    "forecast",
    "flag",
    "api_call",
    "pipeline_release",
    "incident",
    "rate_bucket",
    "gpu_window",
    "admin_approval",
    "alembic_version",
}
PROVENANCE = {
    "run_id",
    "stage",
    "model_name",
    "model_version",
    "prompt_id",
    "prompt_version",
    "created_at",
    "inputs_hash",
}


def public_columns(connection) -> dict[str, set[str]]:
    rows = connection.execute(
        text(
            "SELECT c.table_name, c.column_name FROM information_schema.columns c "
            "JOIN information_schema.tables t USING (table_schema, table_name) "
            "WHERE c.table_schema = 'public' AND t.table_type = 'BASE TABLE'"
        )
    )
    tables: dict[str, set[str]] = {}
    for table, column in rows:
        tables.setdefault(table, set()).add(column)
    return tables


def test_0001_sql_is_verbatim_copy_of_appendix():
    doc = (REPO / "docs/08a-APPENDIX-DDL-and-SCORER.md").read_text()
    blocks = re.findall(r"```sql\n(.*?)```", doc, flags=re.S)
    assert "".join(p.read_text() for p in sorted(SQL_DIR.glob("0001_*.sql"))) == "".join(blocks[:2])


@pytest.mark.db
def test_every_table_is_classified_and_derived_tables_carry_provenance(engine):
    with engine.connect() as connection:
        tables = public_columns(connection)
    assert set(tables) == DERIVED | set(DERIVED_VIA_PARENT) | NOT_DERIVED
    for table in DERIVED:
        assert PROVENANCE <= tables[table], table
    for table, parent in DERIVED_VIA_PARENT.items():
        assert parent in tables[table], table


@pytest.mark.db
def test_downgrade_and_upgrade_round_trip(db_url, engine):
    config = alembic_config(db_url)
    command.downgrade(config, "base")
    with engine.connect() as connection:
        assert set(public_columns(connection)) == {"alembic_version"}
    command.upgrade(config, "head")


@pytest.mark.db
def test_event_log_is_append_only(engine):
    with engine.begin() as connection:
        connection.execute(
            text(
                "INSERT INTO event_log "
                "(type, actor_type, actor_id, entity_type, entity_id, payload) "
                "VALUES ('t', 'admin', 'a', 'e', '1', '{}')"
            )
        )
        connection.execute(text("UPDATE event_log SET type = 'changed'"))
        connection.execute(text("DELETE FROM event_log"))
        assert connection.execute(text("SELECT type FROM event_log")).scalars().all() == ["t"]


@pytest.mark.db
def test_agents_cannot_rate(engine):
    with engine.begin() as connection:
        agent = connection.execute(
            text("INSERT INTO app_user (kind) VALUES ('agent') RETURNING user_id")
        ).scalar_one()
    with pytest.raises(DBAPIError, match="agents never rate"), engine.begin() as connection:
        connection.execute(
            text(
                "INSERT INTO rating (contribution_id, rater_user_id, rater_snapshot_id, "
                "rater_cluster_id, helpfulness) VALUES (gen_random_uuid(), :agent, "
                "gen_random_uuid(), gen_random_uuid(), 'helpful')"
            ),
            {"agent": agent},
        )


@pytest.mark.db
def test_public_api_role_cannot_read_transcript_text(engine):
    with pytest.raises(DBAPIError, match="permission denied"), engine.begin() as connection:
        connection.execute(text("SET LOCAL ROLE arena_api"))
        connection.execute(text("SELECT text FROM private.segment"))


@pytest.mark.db
def test_reconcile_fixes(engine):
    with engine.connect() as connection:
        nullable = connection.execute(
            text(
                "SELECT is_nullable FROM information_schema.columns "
                "WHERE table_name = 'cluster_lineage' AND column_name = 'to_cluster_id'"
            )
        ).scalar_one()
        assert nullable == "YES"
        for index in ("cluster_lineage_edge", "proposition_relation_edge"):
            definition = connection.execute(
                text("SELECT indexdef FROM pg_indexes WHERE indexname = :i"), {"i": index}
            ).scalar_one()
            assert "NULLS NOT DISTINCT" in definition
        assert connection.execute(text("SELECT take_token('k', 1, 0)")).scalar_one() is True
        assert connection.execute(text("SELECT take_token('k', 1, 0)")).scalar_one() is False
