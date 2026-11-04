"""Checks on the statement instrument and the schools drawn from it (D-31.20).

Everything here works on one table: thinker -> statement -> +1 (holds) or -1 (rejects), from
audited stances only. Silence is missing, never a view: agreement between two thinkers counts only
statements both took a side on, with the fingerprint's own Laplace smoothing, so a pair with little
in common sits near "unknown" (0.5) rather than looking alike.

The questions it answers:
- statement_stats: does each statement split the voices (both sides well held)?
- redundancy: which statements carry the same information (|phi| high on shared voices)?
- dimensions: how many independent axes the instrument measures (eigenvalues of the pairwise
  statement correlations, against shuffled data)
- draw_schools / stability: groups of voices by agreement, and how far they survive resampling the
  statements
- recovery: answer the quiz as each voice would (their own stances only) and check the fingerprint
  ranks their own school's members first; the end-to-end test of the instrument
"""

import itertools
from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.metrics import adjusted_rand_score, silhouette_score

Table = dict[str, dict[str, int]]  # thinker -> statement -> +1 / -1


def score(same: float, shared: float) -> float:
    return (same + 1) / (shared + 2)


def pair_agreement(a: dict[str, int], b: dict[str, int], weight: dict[str, float] | None = None):
    shared = a.keys() & b.keys()
    w = {s: (weight or {}).get(s, 1.0) for s in shared}
    same = sum(w[s] for s in shared if a[s] == b[s])
    return score(same, sum(w.values())), len(shared)


def distances(
    table: Table, people: list[str], statements: list[str], weight: dict[str, float] | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """1 - smoothed agreement for every pair, and how many statements each pair shares."""
    keep = set(statements)
    rows = [{s: v for s, v in table[p].items() if s in keep} for p in people]
    n = len(people)
    d, shared = np.zeros((n, n)), np.zeros((n, n))
    for i, j in itertools.combinations(range(n), 2):
        agree, k = pair_agreement(rows[i], rows[j], weight)
        d[i, j] = d[j, i] = 1 - agree
        shared[i, j] = shared[j, i] = k
    return d, shared


def statement_stats(table: Table, statements: list[str]) -> dict[str, dict]:
    out = {}
    for s in statements:
        sides = [row[s] for row in table.values() if s in row]
        hold = sum(1 for v in sides if v > 0)
        out[s] = {
            "hold": hold,
            "reject": len(sides) - hold,
            "n": len(sides),
            "minority": round(min(hold, len(sides) - hold) / len(sides), 3) if sides else 0,
        }
    return out


def phi(table: Table, s: str, t: str) -> tuple[float, int]:
    """Correlation of two statements over the voices who took a side on both."""
    pairs = [(row[s], row[t]) for row in table.values() if s in row and t in row]
    if len(pairs) < 4:
        return 0.0, len(pairs)
    x, y = np.array(pairs, float).T
    if x.std() == 0 or y.std() == 0:
        return 0.0, len(pairs)
    return float(np.corrcoef(x, y)[0, 1]), len(pairs)


def redundancy(table: Table, statements: list[str], min_shared: int = 8) -> list[dict]:
    rows = []
    for s, t in itertools.combinations(statements, 2):
        r, n = phi(table, s, t)
        if n >= min_shared:
            rows.append({"a": s, "b": t, "phi": round(r, 3), "n": n})
    return sorted(rows, key=lambda r: -abs(r["phi"]))


def correlation_matrix(table: Table, statements: list[str], min_shared: int = 6) -> np.ndarray:
    """Pairwise-complete correlations, shrunk toward 0 when few voices share both statements."""
    m = np.eye(len(statements))
    for (i, s), (j, t) in itertools.combinations(enumerate(statements), 2):
        r, n = phi(table, s, t)
        shrink = n / (n + 10) if n >= min_shared else 0.0
        m[i, j] = m[j, i] = r * shrink
    return m


def dimensions(
    table: Table, statements: list[str], runs: int = 200, seed: int = 0
) -> dict[str, Any]:
    """Effective number of independent axes, and how many beat shuffled data (parallel analysis)."""
    m = correlation_matrix(table, statements)
    values = np.sort(np.clip(np.linalg.eigvalsh(m), 0, None))[::-1]
    participation = float(values.sum() ** 2 / (values**2).sum())
    rng = np.random.default_rng(seed)
    people = list(table)
    null = []
    for _ in range(runs):
        shuffled: Table = {p: {} for p in people}
        for s in statements:
            holders = [p for p in people if s in table[p]]
            sides = rng.permutation([table[p][s] for p in holders])
            for p, v in zip(holders, sides, strict=True):
                shuffled[p][s] = int(v)
        null.append(np.sort(np.linalg.eigvalsh(correlation_matrix(shuffled, statements)))[::-1])
    threshold = np.percentile(np.array(null), 95, axis=0)
    above = [v > t for v, t in zip(values, threshold, strict=True)]
    beyond = above.index(False) if False in above else len(above)
    return {
        "participation_ratio": round(participation, 2),
        "axes_beyond_chance": beyond,
        "top_eigenvalues": [round(float(v), 2) for v in values[:8]],
    }


MIN_STABILITY = 0.6  # a drawing that resampling breaks more often than this isn't reported
EMBED_DIMS = 5  # schools are drawn in a five-axis embedding of the agreement distances


def embed(d: np.ndarray, shared: np.ndarray, dims: int = EMBED_DIMS) -> np.ndarray:
    """Weighted MDS of the agreement distances: pairs that share more statements count more."""
    return smacof(d, np.minimum(shared, 20) / 20 + 1e-3, dims=dims)


def cluster(d: np.ndarray, count: int, shared: np.ndarray | None = None) -> list[int]:
    """Ward groups in the embedding (steadier under resampling than linkage on raw distances);
    without `shared`, average linkage on the distances."""
    if shared is None:
        labels = fcluster(linkage(squareform(d, checks=False), "average"), count, "maxclust")
    else:
        labels = fcluster(linkage(embed(d, shared), "ward"), count, "maxclust")
    return [int(x) for x in labels]


@dataclass
class Drawing:
    count: int
    labels: list[int]
    silhouette: float
    stability: float  # mean adjusted Rand against the full drawing, statements resampled
    by_count: dict[int, dict[str, float]]


def stability(
    table: Table,
    people: list[str],
    statements: list[str],
    count: int,
    labels: list[int],
    runs: int = 200,
    seed: int = 0,
    weight: dict[str, float] | None = None,
) -> tuple[float, np.ndarray]:
    """Resample the statements with replacement and redraw: how often do pairs stay together?"""
    rng = np.random.default_rng(seed)
    together = np.zeros((len(people), len(people)))
    scores = []
    for _ in range(runs):
        pick = list(rng.choice(statements, size=len(statements), replace=True))
        counts = {s: pick.count(s) for s in set(pick)}
        w = {s: c * (weight or {}).get(s, 1.0) for s, c in counts.items()}
        d, shared = distances(table, people, list(counts), w)
        again = cluster(d, count, shared)
        scores.append(adjusted_rand_score(labels, again))
        same = np.equal.outer(again, again)
        together += same
    return float(np.mean(scores)), together / runs


def draw_schools(
    table: Table,
    people: list[str],
    statements: list[str],
    counts: range = range(4, 13),
    runs: int = 100,
    weight: dict[str, float] | None = None,
    min_size: int = 2,
) -> Drawing:
    """Average-linkage groups on agreement distance; the count is the one that best combines
    separation (silhouette) with survival under resampled statements."""
    d, shared = distances(table, people, statements, weight)
    best, table_out = None, {}
    for count in counts:
        labels = cluster(d, count, shared)
        sizes = [labels.count(c) for c in set(labels)]
        if not 2 <= len(set(labels)) < len(people):
            continue
        sil = float(silhouette_score(d, labels, metric="precomputed"))
        stab, _ = stability(table, people, statements, count, labels, runs, weight=weight)
        small = sum(1 for s in sizes if s < min_size)
        table_out[count] = {
            "silhouette": round(sil, 3),
            "stability": round(stab, 3),
            "singletons": small,
        }
        merit = (sil * stab if stab >= MIN_STABILITY else -1.0) - 0.05 * small
        if best is None or merit > best[0]:
            best = (merit, count, labels, sil, stab)
    assert best is not None
    _, count, labels, sil, stab = best
    return Drawing(count, labels, round(sil, 3), round(stab, 3), table_out)


def recovery(
    table: Table,
    statements: list[str],
    school_of: dict[str, int],
    min_answers: int = 6,
    weight: dict[str, float] | None = None,
) -> dict[str, float]:
    """Each grouped voice takes the quiz with their own stances. How often is the top match (by the
    fingerprint's rule, excluding themselves) in their own school, and how often in the top 3?"""
    keep = set(statements)
    grouped = [p for p in school_of if school_of[p] is not None]
    top1 = top3 = tried = 0
    for p in grouped:
        mine = {s: v for s, v in table[p].items() if s in keep}
        if len(mine) < min_answers:
            continue
        rows = []
        for o in grouped:
            if o == p:
                continue
            agree, shared = pair_agreement(mine, table[o], weight)
            if shared >= 3:
                rows.append((agree, shared, o))
        if not rows:
            continue
        rows.sort(reverse=True)
        tried += 1
        top1 += school_of[rows[0][2]] == school_of[p]
        top3 += any(school_of[o] == school_of[p] for _, _, o in rows[:3])
    return {
        "voices": tried,
        "top1": round(top1 / max(tried, 1), 3),
        "top3": round(top3 / max(tried, 1), 3),
    }


def smacof(d: np.ndarray, w: np.ndarray, dims: int = 2, iters: int = 400, seed: int = 0):
    """Weighted metric MDS (SMACOF): pairs that share more statements count more in the layout."""
    n = len(d)
    rng = np.random.default_rng(seed)
    # start from classical MDS
    j = np.eye(n) - 1 / n
    b = -0.5 * j @ (d**2) @ j
    vals, vecs = np.linalg.eigh(b)
    x = vecs[:, -dims:] * np.sqrt(np.clip(vals[-dims:], 1e-9, None))
    x = x + rng.normal(0, 1e-6, x.shape)
    v = -w.copy()
    np.fill_diagonal(v, w.sum(1))
    vplus = np.linalg.pinv(v)
    for _ in range(iters):
        dist = np.sqrt(((x[:, None] - x[None]) ** 2).sum(-1))
        ratio = np.where(dist > 1e-12, d / np.maximum(dist, 1e-12), 0)
        bz = -w * ratio
        np.fill_diagonal(bz, 0)
        np.fill_diagonal(bz, -bz.sum(1))
        x = vplus @ bz @ x
    return x - x.mean(0)
