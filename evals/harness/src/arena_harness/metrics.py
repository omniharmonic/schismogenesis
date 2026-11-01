"""Extraction metrics M1-M9 and M6b (Plan §4.2, Architecture §12.3).

Every function returns None when it has nothing to measure. None is "not measured", which is
different from a score of zero and can never pass a threshold.
"""

from collections.abc import Hashable, Iterable, Sequence
from dataclasses import dataclass
from itertools import combinations
from typing import Protocol


class Span(Protocol):
    char_start: int
    char_end: int
    speaker: str


def iou(a: tuple[int, int], b: tuple[int, int]) -> float:
    overlap = max(0, min(a[1], b[1]) - max(a[0], b[0]))
    union = (a[1] - a[0]) + (b[1] - b[0]) - overlap
    return overlap / union if union else 0.0


def match_claims[G: Span, P: Span](
    gold: Sequence[G], predicted: Sequence[P], min_iou: float = 0.5
) -> list[tuple[G, P]]:
    """Pair each claim at most once, best overlap first, same speaker only."""
    candidates = sorted(
        (
            (score, g, p)
            for g, gold_claim in enumerate(gold)
            for p, pred_claim in enumerate(predicted)
            if gold_claim.speaker == pred_claim.speaker
            and (
                score := iou(
                    (gold_claim.char_start, gold_claim.char_end),
                    (pred_claim.char_start, pred_claim.char_end),
                )
            )
            >= min_iou
        ),
        key=lambda item: (-item[0], item[1], item[2]),
    )
    used_gold, used_pred, pairs = set(), set(), []
    for _, g, p in candidates:
        if g not in used_gold and p not in used_pred:
            used_gold.add(g)
            used_pred.add(p)
            pairs.append((gold[g], predicted[p]))
    return pairs


@dataclass(frozen=True)
class PrecisionRecall:
    precision: float | None
    recall: float | None

    @property
    def f1(self) -> float | None:
        if self.precision is None or self.recall is None:
            return None
        total = self.precision + self.recall
        return 2 * self.precision * self.recall / total if total else 0.0


def precision_recall(true_positive: int, predicted: int, actual: int) -> PrecisionRecall:
    return PrecisionRecall(
        true_positive / predicted if predicted else None,
        true_positive / actual if actual else None,
    )


def claim_match_f1(n_matched: int, n_predicted: int, n_gold: int) -> float | None:
    """M1."""
    return precision_recall(n_matched, n_predicted, n_gold).f1


def accuracy(pairs: Iterable[tuple[Hashable, Hashable]]) -> float | None:
    """M2 attitude and M3 source: pass (gold, predicted) label pairs from matched claims."""
    items = list(pairs)
    return sum(gold == pred for gold, pred in items) / len(items) if items else None


def macro_f1(pairs: Iterable[tuple[Hashable, Hashable]]) -> float | None:
    """M4 layer macro-F1, over labels that occur in gold or predictions."""
    items = list(pairs)
    if not items:
        return None
    labels = {label for pair in items for label in pair}
    scores = []
    for label in labels:
        true_positive = sum(g == label and p == label for g, p in items)
        predicted = sum(p == label for _, p in items)
        actual = sum(g == label for g, _ in items)
        scores.append(precision_recall(true_positive, predicted, actual).f1 or 0.0)
    return sum(scores) / len(scores)


def rewrite_fidelity(verdicts: Iterable[str]) -> float | None:
    """M5: blind judge verdicts; yes = 1, partly = 0.5, no = 0."""
    value = {"yes": 1.0, "partly": 0.5, "no": 0.0}
    items = [value[verdict] for verdict in verdicts]
    return sum(items) / len(items) if items else None


def anchor_pass_rate(anchor_matches: Iterable[str]) -> float | None:
    """M6: accepted claims with exact or normalized anchors."""
    items = list(anchor_matches)
    return sum(m in ("exact", "normalized") for m in items) / len(items) if items else None


def fuzzy_share(anchor_matches: Iterable[str]) -> float | None:
    """Reported beside M6."""
    items = list(anchor_matches)
    return sum(m == "fuzzy" for m in items) / len(items) if items else None


def quote_invariant(quote_and_source: Iterable[tuple[str, str]]) -> float | None:
    """M6b: stored quote is a substring of its source segment text. Must be 1.0."""
    items = list(quote_and_source)
    return sum(quote in source for quote, source in items) / len(items) if items else None


def unsupported_leakage(supported: Iterable[bool]) -> float | None:
    """M7: share of sampled accepted claims a blind judge marks as unsupported by the quote."""
    items = list(supported)
    return sum(not s for s in items) / len(items) if items else None


def nli_gate(passed_and_gold: Iterable[tuple[bool, bool]]) -> PrecisionRecall:
    """M8: (gate passed, gold says supported) pairs."""
    items = list(passed_and_gold)
    return precision_recall(
        sum(p and g for p, g in items), sum(p for p, _ in items), sum(g for _, g in items)
    )


def _pairs(clusters: Iterable[Iterable[Hashable]]) -> set[frozenset[Hashable]]:
    return {frozenset(pair) for cluster in clusters for pair in combinations(set(cluster), 2)}


def merge_precision_recall(
    predicted: Iterable[Iterable[Hashable]], gold: Iterable[Iterable[Hashable]]
) -> PrecisionRecall:
    """M9: pairwise over claims, same bank proposition vs same gold cluster."""
    predicted_pairs, gold_pairs = _pairs(predicted), _pairs(gold)
    return precision_recall(
        len(predicted_pairs & gold_pairs), len(predicted_pairs), len(gold_pairs)
    )
