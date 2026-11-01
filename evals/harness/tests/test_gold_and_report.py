import pathlib
import shutil

import pytest
from arena_harness import gold as g
from arena_harness import report as r
from pydantic import ValidationError

FIXTURES = pathlib.Path(__file__).parents[1] / "fixtures"


@pytest.fixture
def version_dir(tmp_path):
    target = tmp_path / "v0"
    shutil.copytree(FIXTURES / "gold-v0", target)
    shutil.copytree(target / "dev", target / "test")
    g.write_manifest(target)
    return target


def predictions():
    lines = (FIXTURES / "predictions.jsonl").read_text().splitlines()
    return [g.PredictedClaim.model_validate_json(line) for line in lines]


def test_gold_rejects_quote_that_is_not_at_its_offsets():
    claim = g.GoldClaim(
        quote="nope",
        char_start=0,
        char_end=4,
        speaker="a",
        speech_act="assert",
        canonical="c",
        layer="empirical",
        attitude="accepts",
        strength="certain",
        source="stated",
    )
    with pytest.raises(ValidationError, match="not at its offsets"):
        g.GoldChunk(chunk_id="c", episode_ref="e", text="real text", claims=[claim])


def test_manifest_detects_tampering(version_dir):
    assert len(g.load_split(version_dir, "dev")) == 1
    (version_dir / "dev/chunks.jsonl").write_text("{}\n")
    with pytest.raises(ValueError, match="differ from the manifest"):
        g.load_split(version_dir, "dev")


def test_test_split_is_sealed_and_access_is_logged(version_dir):
    with pytest.raises(PermissionError):
        g.load_split(version_dir, "test")
    assert not (version_dir / g.ACCESS_LOG).exists()
    g.load_split(version_dir, "test", purpose="bake-off")
    assert "bake-off" in (version_dir / g.ACCESS_LOG).read_text()


def test_fixture_end_to_end_scores_perfectly(version_dir):
    values = r.score(g.load_split(version_dir, "dev"), predictions())
    assert values == {"M1": 1, "M2": 1, "M3": 1, "M4": 1, "M6": 1, "M6b": 1}


def test_predictions_for_unknown_chunks_are_an_error(version_dir):
    wrong = predictions()[0].model_copy(update={"chunk_id": "other"})
    with pytest.raises(ValueError, match="not in gold"):
        r.score(g.load_split(version_dir, "dev"), [wrong])


def test_missing_metrics_never_pass_and_sheet_status_is_shown():
    sheet = r.load_sheet()
    assert set(sheet["metrics"]) == set(r.NAMES)
    lines = r.evaluate({"M2": 0.9, "M3": 0.1}, sheet)
    status = {line.metric: line.status for line in lines}
    assert (status["M2"], status["M3"], status["M5"]) == ("pass", "fail", "not measured")
    text = r.render("t", lines, sheet)
    assert "NOT PASSED" in text and "unsigned" in text


def test_m1_needs_the_reference_and_both_conditions():
    sheet = r.load_sheet()

    def status(value, ref):
        return next(
            line.status for line in r.evaluate({"M1": value}, sheet, ref) if line.metric == "M1"
        )

    assert status(0.8, None) == "not measured"
    assert status(0.8, 0.9) == "pass"
    assert status(0.76, 0.95) == "fail"
    assert status(0.7, 0.7) == "fail"


def test_leakage_is_a_ceiling():
    lines = r.evaluate({"M7": 0.03}, r.load_sheet())
    assert next(line for line in lines if line.metric == "M7").status == "fail"
