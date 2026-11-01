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
    "position",
    "position_holding",
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
    "position_definition",
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


WRITTEN_ROWS = """
WITH run AS (
  INSERT INTO pipeline_run (stage, job_name, trigger, code_ref)
  VALUES ('S1', 't', 'manual', 't') RETURNING run_id
), ch AS (
  INSERT INTO channel (platform, title, run_id, model_version, inputs_hash)
  SELECT 'blog', 'A blog', run_id, 'code', '\\x00' FROM run RETURNING channel_id, run_id
), ep AS (
  INSERT INTO episode (channel_id, platform, external_id, url, title, format, authorship,
    run_id, model_version, inputs_hash)
  SELECT channel_id, 'blog', 'post-1', 'https://example.org/post', 'Post', 'blog_post',
    'pseudonymous', run_id, 'code', '\\x00' FROM ch RETURNING episode_id, run_id
)
INSERT INTO transcript (episode_id, route, has_diarization, has_word_timestamps, storage_ref,
  rights_basis, stage, model_name, model_version, run_id, inputs_hash)
SELECT episode_id, 'written_source', false, false, 'file:ab/abc', 'public_web', 'S4', 'code',
  'code', run_id, '\\x00' FROM ep RETURNING transcript_id
"""


@pytest.mark.db
def test_written_source_needs_a_locator_but_no_timestamps(engine):
    with engine.begin() as connection:
        transcript = connection.execute(text(WRITTEN_ROWS)).scalar_one()
        connection.execute(
            text(
                "INSERT INTO private.segment (transcript_id, seq, text, locator) "
                "VALUES (:t, 0, 'A sentence.', '{\"paragraph\": 1}')"
            ),
            {"t": transcript},
        )
    with pytest.raises(DBAPIError, match="segment_located"), engine.begin() as connection:
        connection.execute(
            text("INSERT INTO private.segment (transcript_id, seq, text) VALUES (:t, 1, 'x')"),
            {"t": transcript},
        )


@pytest.mark.db
def test_spoken_segment_still_valid_with_timestamps_only(engine):
    with engine.begin() as connection:
        transcript = connection.execute(text(WRITTEN_ROWS)).scalar_one()
        connection.execute(
            text(
                "INSERT INTO private.segment (transcript_id, seq, start_ms, end_ms, text) "
                "VALUES (:t, 0, 0, 10, 'x')"
            ),
            {"t": transcript},
        )


POSITION_ROWS = """
WITH run AS (
  INSERT INTO pipeline_run (stage, job_name, trigger, code_ref)
  VALUES ('S11', 't', 'manual', 't') RETURNING run_id
), q AS (
  INSERT INTO live_question (text, run_id, model_name, model_version, inputs_hash)
  SELECT 'A question?', run_id, 'm', 'v', '\\\\x00' FROM run RETURNING live_question_id, run_id
)
INSERT INTO position (live_question_id, key, run_id, model_name, model_version, inputs_hash)
SELECT live_question_id, 'p1', run_id, 'm', 'v', '\\\\x00' FROM q RETURNING position_id
"""
DEFINITION = (
    "INSERT INTO position_definition (position_id, version, label, statement, author_kind,"
    " author_model, ratified_at) VALUES (:p, :v, 'A label', 'A neutral statement.', :kind,"
    " :model, :ratified)"
)


@pytest.mark.db
def test_model_definitions_can_never_be_ratified_and_history_is_kept(engine):
    with engine.begin() as connection:
        position = connection.execute(text(POSITION_ROWS)).scalar_one()
        draft = {"p": position, "v": 1, "kind": "model", "model": "m", "ratified": None}
        connection.execute(text(DEFINITION), draft)
        connection.execute(text("DELETE FROM position_definition"))
        count = text("SELECT count(*) FROM position_definition")
        assert connection.execute(count).scalar_one() == 1
    with pytest.raises(DBAPIError, match="check"), engine.begin() as connection:
        connection.execute(text(DEFINITION), {**draft, "v": 2, "ratified": "2027-01-01"})
    with pytest.raises(DBAPIError, match="check"), engine.begin() as connection:
        connection.execute(
            text(DEFINITION), {**draft, "v": 2, "kind": "niche_member", "model": None}
        )
