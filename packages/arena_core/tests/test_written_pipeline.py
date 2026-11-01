"""End to end on a synthetic text, with recorded model output and a stub entailment scorer."""

import json

import numpy as np
import pytest
from arena_core.storage import FileSourceStore
from arena_extract.anchor import locate
from arena_extract.normalize import candidate_pairs, merge_groups
from arena_extract.schema import ClaimItem, ExtractClaimsOutput
from arena_extract.validators import issues, strength_cap
from arena_extract.written import (
    PROMPT_DIR,
    PROMPT_ID,
    PROMPT_VERSION,
    chunk_source,
    decide,
    extract_source,
    gate_source,
    hypothesis,
    plan_chunks,
)
from arena_harness.metrics import quote_invariant
from arena_ingest.written import WrittenWork, ingest_written, paragraphs
from arena_llm import AnthropicApi, BackendDisabled, ClaudeCodeBatch, FakeBackend, PendingBatch
from hypothesis import given
from hypothesis import strategies as st
from sqlalchemy import text

BODY = "The bridge held for ten years without any repairs at all.\n\nI think budgets decide it."
WORK = WrittenWork("https://example.org/a", "A", "scott-alexander", "2009-04-13", "Blog")


@given(st.lists(st.integers(1, 500), min_size=1, max_size=40))
def test_chunk_cores_tile_with_no_gap_or_overlap(words):
    cores = plan_chunks(words)
    assert cores[0][0] == 0 and cores[-1][1] == len(words) - 1
    assert all(b[0] == a[1] + 1 for a, b in zip(cores, cores[1:], strict=False))


def test_locate_exact_normalized_fuzzy_and_refusal():
    source = "We don’t know, and   nobody does yet."

    def match(quote, within):
        anchor = locate(quote, within)
        return anchor and anchor.match

    assert match("nobody does yet", source) == "exact"
    assert match("we don't know and nobody does", source) == "normalized"
    long = "the quick brown fox jumps over the lazy dog near the old river bank today"
    assert match(long.replace("lazy", "lazzy"), long) == "fuzzy"
    assert locate("an entirely invented sentence about something else", source) is None


def test_gate_decisions():
    assert decide("entailment", "stated") == ("accepted", None)
    assert decide("contradiction", "stated")[0] == "rejected"
    assert decide("neutral", "stated")[0] == "escalated"
    assert decide("entailment", "inferred")[0] == "escalated"


def test_belief_reports_become_author_statements():
    quote = "I no longer believe that freedom and democracy are compatible."
    assert hypothesis("Freedom and democracy are compatible.", "rejects", quote) == (
        "The author does not believe that freedom and democracy are compatible."
    )
    assert hypothesis("Rockets are slow.", "rejects", "Rockets are not slow at all") == (
        "It is not the case that Rockets are slow."
    )
    assert hypothesis("Rockets are slow.", "accepts", "Rockets are slow") == "Rockets are slow."


def claim_item(**overrides):
    return ClaimItem.model_validate(item("x" * 25, **overrides))


def test_validators_match_topology_live_codes():
    assert issues(claim_item(proposed_canonical="Taxes rose 40%."), "Taxes rose a lot.") == [
        "new_number"
    ]
    assert "new_entity" in issues(
        claim_item(proposed_canonical="The firm helped Google."), "It helped."
    )
    assert issues(claim_item(quantifier="generic"), "Some labs are reckless.") == ["scope_widened"]
    assert issues(claim_item(quantifier="some"), "Some labs are reckless.") == []
    assert "non_attributable_stance" in issues(claim_item(speech_act="attribute"), "They said so.")
    assert issues(claim_item(speech_act="attribute", source="inferred"), "They said so.") == []
    assert strength_cap("You might say it is so.") == "certain"
    assert strength_cap("I think it might be so.") == "tentative"


def test_paid_backend_refuses():
    with pytest.raises(BackendDisabled, match="opt-in"):
        AnthropicApi().complete_json()


def item(quote, **overrides):
    return {
        "seq": 0, "quote": quote, "speech_act": "assert", "claim_text": "c",
        "proposed_canonical": "A bridge held for a decade.", "tl_type": "empirical",
        "attitude": "accepts", "strength": "certain", "source": "stated",
        "layer": "empirical", "quantifier": "generic",
    } | overrides  # fmt: skip


class Always:
    last_model = "fake"

    def __init__(self, output):
        self.output = output

    def complete_json(self, **_):
        return [self.output]


def setup(engine, tmp_path):
    from arena_core.seed import load_seed
    from conftest import REPO

    load_seed(engine, REPO / "seed/SEED-v4.json", REPO / "seed/SLICE-1-LANDMARKS.json")
    source = tmp_path / "work.txt"
    source.write_text(BODY)
    episode = ingest_written(engine, FileSourceStore(tmp_path / "store"), WORK, source)
    chunk_source(engine, episode)
    return episode, source


def claims(engine):
    with engine.connect() as connection:
        return connection.execute(
            text(
                "SELECT c.gate_status, c.reject_reason, c.anchor_match, c.quote_full, c.strength,"
                " s.text FROM claim c LEFT JOIN private.segment s"
                " ON s.segment_id = c.anchor_segment_id ORDER BY c.created_at, c.claim_id"
            )
        ).all()


@pytest.mark.db
def test_pipeline_keeps_real_quotes_and_discards_invented_ones(engine, tmp_path):
    episode, _ = setup(engine, tmp_path)
    output = {
        "items": [
            item("The bridge held for ten years without any repairs"),
            item("The bridge collapsed in the very first winter storm"),
            item("I think budgets decide it.", seq=1, proposed_canonical="Budgets decide it."),
            item("The bridge held for ten years", speech_act="attribute", attitude="accepts"),
        ]
    }
    assert extract_source(engine, Always(output), episode)["claims"] == 4
    assert extract_source(engine, Always(output), episode) == {
        "pending": 0, "claims": 0, "skipped": 1,
    }  # fmt: skip

    rows = claims(engine)
    assert sorted(r.gate_status for r in rows) == ["anchored", "anchored", "rejected", "rejected"]
    assert {r.reject_reason for r in rows} == {None, "no_anchor", "non_attributable_stance"}
    assert next(r for r in rows if r.quote_full and "budgets" in r.quote_full).strength == "leaning"
    kept = [(r.quote_full, r.text) for r in rows if r.quote_full]
    assert quote_invariant(kept) == 1.0  # M6b

    def entail_all(pairs):
        return [{"label": "entailment", "entail": 0.9, "contra": 0.0} for _ in pairs]

    assert gate_source(engine, entail_all, "stub", episode) == {"accepted": 2}


@pytest.mark.db
def test_reingesting_the_same_url_adds_nothing(engine, tmp_path):
    episode, source = setup(engine, tmp_path)
    store = FileSourceStore(tmp_path / "store")
    assert ingest_written(engine, store, WORK, source) == episode
    with engine.connect() as connection:
        count = connection.execute(text("SELECT count(*) FROM private.segment")).scalar_one()
    assert count == len(paragraphs(BODY))


@pytest.mark.db
def test_claude_batch_queues_then_collects(engine, tmp_path):
    episode, _ = setup(engine, tmp_path)
    backend = ClaudeCodeBatch("b1", "gold", root=tmp_path)
    assert extract_source(engine, backend, episode)["pending"] == 1
    task = json.loads(next((tmp_path / "queue/b1").glob("*.json")).read_text())
    assert task["protocol"] == "arena.ccbatch/1" and task["prompt_id"] == PROMPT_ID
    results = tmp_path / "results/b1"
    results.mkdir(parents=True)
    (results / f"{task['task_id']}.json").write_text(
        json.dumps({"outputs": [{"items": []}], "model": "m"})
    )
    assert extract_source(engine, backend, episode) == {"pending": 0, "claims": 0, "skipped": 0}


def test_pending_batch_and_fake_backend_are_exported():
    assert issubclass(PendingBatch, Exception) and FakeBackend({}).last_model == "fake"
    assert (PROMPT_DIR / f"{PROMPT_ID}_{PROMPT_VERSION}.md").exists()
    assert ExtractClaimsOutput.model_json_schema()["type"] == "object"


def test_merge_groups_are_transitive():
    groups = merge_groups(4, [(0, 1), (1, 2)])
    assert groups[0] == groups[1] == groups[2] != groups[3]


def test_candidates_only_cross_authors_above_threshold():
    vectors = np.array([[1.0, 0.0], [1.0, 0.0], [0.99, 0.141], [0.0, 1.0]])
    pairs = candidate_pairs(vectors, ["a", "a", "b", "c"])
    assert [(x, y) for x, y, _ in pairs] == [(0, 2), (1, 2)]
