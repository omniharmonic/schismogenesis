"""Score predictions against gold and render a Markdown report against the threshold sheet."""

import pathlib
from dataclasses import dataclass
from typing import Any

import yaml

from arena_harness import metrics
from arena_harness.gold import GoldChunk, PredictedClaim

THRESHOLDS = pathlib.Path(__file__).parents[2] / "thresholds.yaml"
NAMES = {
    "M1": "claim-match F1",
    "M2": "attitude accuracy",
    "M3": "source accuracy",
    "M4": "layer macro-F1",
    "M5": "neutral-rewrite fidelity",
    "M6": "anchor pass rate",
    "M6b": "quote invariant",
    "M7": "unsupported leakage",
    "M9": "dedup precision",
}


@dataclass(frozen=True)
class Line:
    metric: str
    value: float | None
    requirement: str
    status: str  # pass | fail | not measured


def score(gold: list[GoldChunk], predicted: list[PredictedClaim]) -> dict[str, float | None]:
    """Compute what a gold + predictions pair can show. Judge-based metrics need judge data."""
    by_chunk: dict[str, list[PredictedClaim]] = {}
    for claim in predicted:
        by_chunk.setdefault(claim.chunk_id, []).append(claim)
    texts = {chunk.chunk_id: chunk.text for chunk in gold}
    unknown = sorted(by_chunk.keys() - texts.keys())
    if unknown:
        raise ValueError(f"predictions for chunks not in gold: {unknown}")

    matched = [
        pair
        for chunk in gold
        for pair in metrics.match_claims(chunk.claims, by_chunk.get(chunk.chunk_id, []))
    ]
    return {
        "M1": metrics.claim_match_f1(
            len(matched), len(predicted), sum(len(chunk.claims) for chunk in gold)
        ),
        "M2": metrics.accuracy((g.attitude, p.attitude) for g, p in matched),
        "M3": metrics.accuracy((g.source, p.source) for g, p in matched),
        "M4": metrics.macro_f1((g.layer, p.layer) for g, p in matched),
        "M6": metrics.anchor_pass_rate(c.anchor_match for c in predicted),
        "M6b": metrics.quote_invariant((c.quote, texts[c.chunk_id]) for c in predicted),
    }


def evaluate(
    values: dict[str, float | None], sheet: dict[str, Any], reference_m1: float | None = None
) -> list[Line]:
    lines = []
    for metric, rule in sheet["metrics"].items():
        value = values.get(metric)
        floor, ceiling = rule.get("min"), rule.get("max")
        ratio = rule.get("min_ratio_of_reference")
        parts = []
        if floor is not None:
            parts.append(f">= {floor}")
        if ceiling is not None:
            parts.append(f"<= {ceiling}")
        if ratio is not None:
            parts.append(f">= {ratio} of reference")
        if value is None or (ratio is not None and reference_m1 is None):
            status = "not measured"
        else:
            ok = (floor is None or value >= floor) and (ceiling is None or value <= ceiling)
            if ratio is not None and reference_m1 is not None:
                ok = ok and value >= ratio * reference_m1
            status = "pass" if ok else "fail"
        lines.append(Line(metric, value, " and ".join(parts), status))
    return lines


def render(title: str, lines: list[Line], sheet: dict[str, Any]) -> str:
    out = [
        f"# {title}",
        "",
        f"Threshold sheet status: **{sheet['status']}**",
        "",
        "| Metric | Name | Value | Required | Status |",
        "|---|---|---|---|---|",
    ]
    for line in lines:
        value = "n/a" if line.value is None else f"{line.value:.3f}"
        out.append(
            f"| {line.metric} | {NAMES[line.metric]} | {value} | "
            f"{line.requirement} | {line.status} |"
        )
    verdict = "PASS" if lines and all(line.status == "pass" for line in lines) else "NOT PASSED"
    return "\n".join([*out, "", f"Overall: **{verdict}**", ""])


def load_sheet(path: pathlib.Path = THRESHOLDS) -> dict[str, Any]:
    return yaml.safe_load(path.read_text())
