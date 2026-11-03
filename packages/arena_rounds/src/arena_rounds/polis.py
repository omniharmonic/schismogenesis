"""Polis-style opinion groups: PCA, k-means, representative statements, group-informed consensus.

Follows the published Polis method closely (docs/fingerprint/02-ARCHITECTURE.md section 6).
"""

import math
from dataclasses import dataclass

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from arena_rounds.matrix import VoteMatrix

MIN_VOTES = 7
MAX_GROUPS = 5
MIN_SILHOUETTE = 0.15
Z_90 = 1.2816


@dataclass(frozen=True)
class PolisResult:
    participants: list[str]  # included participants, in matrix order
    projection: np.ndarray  # participants by 2
    labels: np.ndarray  # group per included participant
    k: int
    silhouette: float | None
    pc1: dict[str, float]  # standardised first component, used to seed the bridging fit


def project(m: VoteMatrix) -> tuple[np.ndarray, np.ndarray]:
    """Mean-impute after centring, scale sparse voters up as Polis does, keep two components."""
    values = m.values
    seen = ~np.isnan(values)
    means = np.where(seen.any(0), np.nansum(values, 0) / np.maximum(seen.sum(0), 1), 0.0)
    centred = np.where(seen, values - means, 0.0)
    counts = np.maximum(seen.sum(1), 1)
    scaled = centred * np.sqrt(values.shape[1] / counts)[:, None]
    _, _, vt = np.linalg.svd(scaled, full_matrices=False)
    components = vt[:2]
    if components.shape[0] < 2:
        components = np.vstack([components, np.zeros((2 - components.shape[0], values.shape[1]))])
    return scaled @ components.T, components


def polis_groups(m: VoteMatrix, min_votes: int = MIN_VOTES, seed: int = 7) -> PolisResult | None:
    keep = m.votes_per_participant() >= min_votes
    if keep.sum() < 2:
        return None
    sub = m.subset(keep)
    projection, _ = project(sub)
    pc1 = projection[:, 0]
    spread = pc1.std() or 1.0
    pc1_map = {
        p: float(v) for p, v in zip(sub.participants, (pc1 - pc1.mean()) / spread, strict=True)
    }
    n = len(sub.participants)
    best: tuple[float, int, np.ndarray] | None = None
    for k in range(2, min(MAX_GROUPS, n // 5) + 1):
        model = KMeans(k, n_init=10, random_state=seed)  # pyright: ignore[reportArgumentType]
        labels = np.asarray(model.fit_predict(projection))
        if len(set(labels)) < 2:
            continue
        sil = float(silhouette_score(projection, labels))
        if best is None or sil > best[0] + 1e-9:
            best = (sil, k, labels)
    if best is None or best[0] < MIN_SILHOUETTE:
        silhouette = None if best is None else best[0]
        return PolisResult(sub.participants, projection, np.zeros(n, int), 1, silhouette, pc1_map)
    sil, k, labels = best
    return PolisResult(sub.participants, projection, _relabel(labels, projection), k, sil, pc1_map)


def _relabel(labels: np.ndarray, projection: np.ndarray) -> np.ndarray:
    """Name groups in order of their mean first coordinate so labels are stable between runs."""
    order = sorted(set(labels), key=lambda g: projection[labels == g, 0].mean())
    mapping = {g: i for i, g in enumerate(order)}
    return np.array([mapping[g] for g in labels])


@dataclass(frozen=True)
class StatementStats:
    agree: int
    disagree: int
    seen: int

    @property
    def pa(self) -> float:
        return (1 + self.agree) / (2 + self.seen)

    @property
    def pd(self) -> float:
        return (1 + self.disagree) / (2 + self.seen)


def group_stats(
    m: VoteMatrix, members: dict[int, list[str]]
) -> dict[int, dict[str, StatementStats]]:
    index = {p: i for i, p in enumerate(m.participants)}
    out: dict[int, dict[str, StatementStats]] = {}
    for group, people in members.items():
        rows = m.values[[index[p] for p in people]]
        out[group] = {}
        for j, statement in enumerate(m.statements):
            column = rows[:, j]
            column = column[~np.isnan(column)]
            out[group][statement] = StatementStats(
                int((column > 0).sum()), int((column < 0).sum()), int(column.size)
            )
    return out


def _z(p1: float, n1: int, p2: float, n2: int) -> float:
    pooled = (p1 * n1 + p2 * n2) / max(n1 + n2, 1)
    se = math.sqrt(max(pooled * (1 - pooled) * (1 / max(n1, 1) + 1 / max(n2, 1)), 1e-12))
    return (p1 - p2) / se


def representative(
    m: VoteMatrix, members: dict[int, list[str]], top: int = 5
) -> dict[int, list[dict]]:
    """Statements that set each group apart from everyone else, agree or disagree."""
    out: dict[int, list[dict]] = {}
    for group, people in members.items():
        rest = [p for g, ps in members.items() if g != group for p in ps]
        if not rest:
            out[group] = []
            continue
        inside = group_stats(m, {0: people})[0]
        outside = group_stats(m, {0: rest})[0]
        rows = []
        for statement in m.statements:
            a, b = inside[statement], outside[statement]
            if a.seen < 2:
                continue
            for direction, p_in, p_out in (("agree", a.pa, b.pa), ("disagree", a.pd, b.pd)):
                ratio = p_in / p_out
                if ratio > 1 and p_in > 0.5 and _z(p_in, a.seen, p_out, b.seen) > Z_90:
                    rows.append(
                        {
                            "statement": statement,
                            "direction": direction,
                            "p": round(p_in, 3),
                            "ratio": round(ratio, 3),
                            "score": ratio * p_in,
                            "seen": a.seen,
                        }
                    )
        rows.sort(key=lambda r: (-r["score"], r["statement"]))
        seen_statements: set[str] = set()
        kept = []
        for row in rows:
            if row["statement"] not in seen_statements:
                seen_statements.add(row["statement"])
                kept.append(row)
        out[group] = kept[:top]
    return out


def consensus(stats: dict[int, dict[str, StatementStats]], min_seen: int = 2) -> list[dict]:
    """Group-informed consensus: the product of each group's agree probability."""
    statements = next(iter(stats.values())).keys() if stats else []
    rows = []
    for s in statements:
        per = [stats[g][s] for g in stats]
        if any(x.seen < min_seen for x in per):
            continue
        rows.append(
            {
                "statement": s,
                "gic": math.prod(x.pa for x in per),
                "all_agree": all(x.pa > 0.5 for x in per),
                "by_group": [round(x.pa, 3) for x in per],
            }
        )
    return sorted(rows, key=lambda r: (-r["gic"], r["statement"]))


def divisive(stats: dict[int, dict[str, StatementStats]], min_seen: int = 2) -> list[dict]:
    statements = next(iter(stats.values())).keys() if stats else []
    rows = []
    for s in statements:
        per = [stats[g][s] for g in stats]
        if any(x.seen < min_seen for x in per):
            continue
        pas = [x.pa for x in per]
        rows.append(
            {"statement": s, "spread": max(pas) - min(pas), "by_group": [round(p, 3) for p in pas]}
        )
    return sorted(rows, key=lambda r: (-r["spread"], r["statement"]))
