"""Polis-style opinion groups: PCA, k-means, representative statements, group-informed consensus.

Follows the published Polis method closely (docs/fingerprint/02-ARCHITECTURE.md section 6).
"""

import math
from dataclasses import dataclass

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

from arena_rounds.matrix import VoteMatrix

MIN_VOTES = 7
MAX_GROUPS = 5
MAX_BASE = 100
MIN_SILHOUETTE = 0.15
Z_90 = 1.2816
STABILITY_RUNS = 20
STABILITY_SAMPLE = 1000
CLEAR = 0.8
TENTATIVE = 0.5


@dataclass(frozen=True)
class Space:
    """The room's opinion space: column means and two components, so others can be projected."""

    means: np.ndarray
    components: np.ndarray  # 2 by statements

    def place(self, values: np.ndarray) -> np.ndarray:
        """Project vote rows (nan for unseen) without refitting, with Polis sparsity scaling."""
        seen = ~np.isnan(values)
        centred = np.where(seen, values - self.means, 0.0)
        counts = np.maximum(seen.sum(1), 1)
        scaled = centred * np.sqrt(values.shape[1] / counts)[:, None]
        return scaled @ self.components.T


@dataclass(frozen=True)
class PolisResult:
    participants: list[str]  # included participants, in matrix order
    projection: np.ndarray  # participants by 2
    labels: np.ndarray  # group per included participant
    k: int
    silhouette: float | None
    pc1: dict[str, float]  # standardised first component, used to seed the bridging fit
    space: Space
    stability: float | None = None  # mean adjusted Rand index over statement bootstraps


def fit_space(m: VoteMatrix) -> Space:
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
    # fix each component's sign so the heavier tail of loadings is positive (stable between runs)
    for i in range(2):
        if components[i][np.argmax(np.abs(components[i]))] < 0:
            components[i] = -components[i]
    return Space(means, components)


def project(m: VoteMatrix) -> tuple[np.ndarray, np.ndarray]:
    """Mean-impute after centring, scale sparse voters up as Polis does, keep two components."""
    space = fit_space(m)
    return space.place(m.values), space.components


def _kmeans(
    points: np.ndarray, k: int, seed: int, weights: np.ndarray | None = None, n_init: int = 10
) -> np.ndarray:
    model = KMeans(k, n_init=n_init, random_state=seed)  # pyright: ignore[reportArgumentType]
    return np.asarray(model.fit_predict(points, sample_weight=weights))


def cluster(projection: np.ndarray, seed: int = 7) -> tuple[np.ndarray, int, float | None]:
    """Polis two-stage clustering: up to 100 base clusters, then 2 to 5 groups by silhouette.

    Returns per-participant labels, the number of groups (1 if none is clear) and the silhouette.
    """
    n = len(projection)
    if n > MAX_BASE:
        base = _kmeans(projection, MAX_BASE, seed, n_init=2)
        centres = np.array([projection[base == b].mean(0) for b in range(MAX_BASE)])
        weights = np.bincount(base, minlength=MAX_BASE).astype(float)
    else:
        base = np.arange(n)
        centres = projection
        weights = np.ones(n)
    best: tuple[float, int, np.ndarray] | None = None
    for k in range(2, min(MAX_GROUPS, n // 5) + 1):
        if k >= len(centres):
            break
        grouped = _kmeans(centres, k, seed, weights)
        if len(set(grouped)) < 2:
            continue
        labels = grouped[base]
        sample = slice(None) if n <= 1500 else np.random.default_rng(seed).choice(n, 1500, False)
        sil = float(silhouette_score(projection[sample], labels[sample]))
        if best is None or sil > best[0] + 1e-9:
            best = (sil, k, labels)
    if best is None or best[0] < MIN_SILHOUETTE:
        return np.zeros(n, int), 1, None if best is None else best[0]
    sil, k, labels = best
    return _relabel(labels, projection), k, sil


def polis_groups(
    m: VoteMatrix, min_votes: int = MIN_VOTES, seed: int = 7, stability: bool = False
) -> PolisResult | None:
    threshold = min(min_votes, len(m.statements))
    keep = m.votes_per_participant() >= threshold
    if keep.sum() < 2:
        return None
    sub = m.subset(keep)
    space = fit_space(sub)
    projection = space.place(sub.values)
    pc1 = projection[:, 0]
    spread = pc1.std() or 1.0
    pc1_map = {
        p: float(v) for p, v in zip(sub.participants, (pc1 - pc1.mean()) / spread, strict=True)
    }
    labels, k, sil = cluster(projection, seed)
    stable = group_stability(sub, labels, k, seed) if stability and k > 1 else None
    return PolisResult(sub.participants, projection, labels, k, sil, pc1_map, space, stable)


def group_stability(m: VoteMatrix, labels: np.ndarray, k: int, seed: int = 7) -> float:
    """Resample statements with replacement, refit, and measure agreement with the original groups.

    Large rooms are measured on a fixed random sample of STABILITY_SAMPLE participants.
    """
    random = np.random.default_rng(seed)
    if len(m.participants) > STABILITY_SAMPLE:
        keep = np.zeros(len(m.participants), bool)
        keep[random.choice(len(m.participants), STABILITY_SAMPLE, replace=False)] = True
        m, labels = m.subset(keep), labels[keep]
    scores = []
    for _ in range(STABILITY_RUNS):
        cols = random.integers(0, len(m.statements), len(m.statements))
        boot = VoteMatrix(m.participants, [m.statements[c] for c in cols], m.values[:, cols])
        again, k2, _ = cluster(fit_space(boot).place(boot.values), seed)
        scores.append(adjusted_rand_score(labels, again) if k2 > 1 else 0.0)
    return float(np.mean(scores))


def stability_label(score: float | None) -> str | None:
    if score is None:
        return None
    return "clear" if score >= CLEAR else "tentative" if score >= TENTATIVE else "unstable"


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
        with np.errstate(invalid="ignore"):
            agree = (rows > 0).sum(0)
            disagree = (rows < 0).sum(0)
        seen = (~np.isnan(rows)).sum(0)
        out[group] = {
            statement: StatementStats(int(agree[j]), int(disagree[j]), int(seen[j]))
            for j, statement in enumerate(m.statements)
        }
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
