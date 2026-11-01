from dataclasses import dataclass

import pytest
from arena_harness import metrics as m
from hypothesis import given
from hypothesis import strategies as st


@dataclass
class C:
    char_start: int
    char_end: int
    speaker: str = "a"


def test_iou():
    assert m.iou((0, 10), (0, 10)) == 1
    assert m.iou((0, 10), (5, 15)) == pytest.approx(5 / 15)
    assert m.iou((0, 5), (5, 10)) == 0


@given(st.integers(0, 50), st.integers(1, 50), st.integers(0, 50), st.integers(1, 50))
def test_iou_is_symmetric_and_bounded(a, la, b, lb):
    x, y = (a, a + la), (b, b + lb)
    assert m.iou(x, y) == m.iou(y, x)
    assert 0 <= m.iou(x, y) <= 1


def test_match_requires_same_speaker_and_overlap():
    assert m.match_claims([C(0, 10)], [C(0, 10, "b")]) == []
    assert m.match_claims([C(0, 10)], [C(0, 2)]) == []


def test_match_uses_each_claim_once_and_prefers_best_overlap():
    gold = [C(0, 10)]
    near, exact = C(0, 8), C(0, 10)
    assert m.match_claims(gold, [near, exact]) == [(gold[0], exact)]


def test_f1_and_empty_inputs_are_not_measured():
    assert m.claim_match_f1(1, 2, 2) == pytest.approx(0.5)
    assert m.claim_match_f1(0, 0, 2) is None
    assert m.claim_match_f1(0, 3, 2) == 0
    for fn in (
        m.accuracy,
        m.macro_f1,
        m.rewrite_fidelity,
        m.anchor_pass_rate,
        m.quote_invariant,
        m.unsupported_leakage,
    ):
        assert fn([]) is None


def test_macro_f1_weights_labels_equally():
    pairs = [("a", "a")] * 9 + [("b", "a")]
    assert m.macro_f1(pairs) == pytest.approx((18 / 19 + 0) / 2)


def test_rewrite_fidelity_scoring():
    assert m.rewrite_fidelity(["yes", "partly", "no"]) == pytest.approx(0.5)


def test_anchor_metrics_separate_fuzzy():
    matches = ["exact", "normalized", "fuzzy", "none"]
    assert m.anchor_pass_rate(matches) == 0.5
    assert m.fuzzy_share(matches) == 0.25


def test_quote_invariant_catches_altered_quote():
    assert m.quote_invariant([("abc", "xabcx"), ("abd", "xabcx")]) == 0.5


def test_leakage_and_nli_gate():
    assert m.unsupported_leakage([True, True, True, False]) == 0.25
    gate = m.nli_gate([(True, True), (True, False), (False, True)])
    assert (gate.precision, gate.recall) == (0.5, 0.5)


def test_merge_precision_recall_is_pairwise():
    result = m.merge_precision_recall([[1, 2, 3]], [[1, 2], [3]])
    assert result.precision == pytest.approx(1 / 3)
    assert result.recall == 1
