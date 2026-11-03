"""Community Notes-style bridging: one-dimensional matrix factorisation over agree and disagree.

rating ≈ μ + b_u + b_s + f_u·f_s, with intercepts regularised more heavily than factors. A
statement bridges when its factor is small and the agreement predicted for someone neutral on the
main split (μ + b_s) is high, and a majority on each side agreed.

Community Notes publishes at intercept ≥ 0.40 with |factor| < 0.50. Its baseline helpfulness is
low, while a room's baseline agreement sits near 0.5, so the same intercept would demand over 90%
agreement. We therefore set the bar on neutral agreement (0.75) and keep the factor bar as is.
"""

from dataclasses import dataclass

import numpy as np

from arena_rounds.matrix import VoteMatrix

MIN_RATERS = 5
MIN_RATINGS = 3
NEUTRAL_AGREE = 0.75
MAX_FACTOR = 0.50
MIN_PER_SIDE = 2


@dataclass(frozen=True)
class BridgeFit:
    mu: float
    participants: list[str]
    statements: list[str]
    b_u: np.ndarray
    f_u: np.ndarray
    b_s: np.ndarray
    f_s: np.ndarray
    ratings: np.ndarray  # participants by statements, 1 agree, 0 disagree, nan otherwise


def _ratings(m: VoteMatrix) -> VoteMatrix:
    """Agree is 1 and disagree 0. Passes and unseen are missing. Prune sparse rows and columns."""
    r = np.where(m.values > 0, 1.0, np.where(m.values < 0, 0.0, np.nan))
    participants, statements = list(m.participants), list(m.statements)
    while True:
        cols = (~np.isnan(r)).sum(0) >= MIN_RATERS
        rows = (~np.isnan(r)).sum(1) >= MIN_RATINGS
        if cols.all() and rows.all():
            return VoteMatrix(participants, statements, r)
        r = r[rows][:, cols]
        participants = [p for p, k in zip(participants, rows, strict=True) if k]
        statements = [s for s, k in zip(statements, cols, strict=True) if k]
        if r.size == 0:
            return VoteMatrix(participants, statements, r)


def _ridge(x: np.ndarray, y: np.ndarray, penalty: np.ndarray) -> np.ndarray:
    return np.linalg.solve(x.T @ x + np.diag(penalty), x.T @ y)


def fit_bridging(
    m: VoteMatrix,
    init: dict[str, float] | None = None,
    lambda_i: float = 0.15,
    lambda_f: float = 0.03,
    sweeps: int = 60,
) -> BridgeFit | None:
    rated = _ratings(m)
    r = rated.values
    if r.size == 0 or r.shape[0] < 2:
        return None
    n_u, n_s = r.shape
    seen = ~np.isnan(r)
    init = init or {}
    f_u = np.array([init.get(p, 0.0) for p in rated.participants])
    if not np.any(f_u):
        f_u = np.linspace(-1, 1, n_u)
    reference = f_u.copy()
    b_u = np.zeros(n_u)
    b_s = np.zeros(n_s)
    f_s = np.zeros(n_s)
    mu = float(np.nanmean(r))
    pen = np.array([lambda_i, lambda_f])
    for _ in range(sweeps):
        for j in range(n_s):
            rows = seen[:, j]
            x = np.column_stack([np.ones(rows.sum()), f_u[rows]])
            b_s[j], f_s[j] = _ridge(x, r[rows, j] - mu - b_u[rows], pen)
        for i in range(n_u):
            cols = seen[i]
            x = np.column_stack([np.ones(cols.sum()), f_s[cols]])
            b_u[i], f_u[i] = _ridge(x, r[i, cols] - mu - b_s[cols], pen)
        prediction = b_u[:, None] + b_s[None, :] + np.outer(f_u, f_s)
        mu = float(np.mean((r - prediction)[seen]))
    if reference.std() and f_u.std() and np.corrcoef(f_u, reference)[0, 1] < 0:
        f_u, f_s = -f_u, -f_s  # keep the sign of the Polis first component
    return BridgeFit(mu, rated.participants, rated.statements, b_u, f_u, b_s, f_s, r)


def bridges(
    fit: BridgeFit, bar: float = NEUTRAL_AGREE, max_factor: float = MAX_FACTOR, leaning: int = 5
) -> tuple[list[dict], list[dict]]:
    """Statements that pass the bar, and the best of those that lean toward it."""
    rows = []
    for j, statement in enumerate(fit.statements):
        col = fit.ratings[:, j]
        raters = ~np.isnan(col)
        pos = raters & (fit.f_u > 0)
        neg = raters & (fit.f_u < 0)
        rows.append(
            {
                "statement": statement,
                "intercept": round(float(fit.b_s[j]), 3),
                "neutral_agree": round(float(fit.mu + fit.b_s[j]), 3),
                "factor": round(float(fit.f_s[j]), 3),
                "raters": int(raters.sum()),
                "sides": [int(neg.sum()), int(pos.sum())],
                "agree_by_side": [
                    round(float(col[neg].mean()), 3) if neg.any() else None,
                    round(float(col[pos].mean()), 3) if pos.any() else None,
                ],
            }
        )

    def both_sides(row: dict) -> bool:
        return min(row["sides"]) >= MIN_PER_SIDE

    def majority_each_side(row: dict) -> bool:
        return all(a is not None and a > 0.5 for a in row["agree_by_side"])

    passed = [
        r
        for r in rows
        if r["neutral_agree"] >= bar
        and abs(r["factor"]) < max_factor
        and both_sides(r)
        and majority_each_side(r)
    ]
    near = [
        r
        for r in rows
        if r not in passed
        and abs(r["factor"]) < max_factor
        and both_sides(r)
        and majority_each_side(r)
    ]
    passed.sort(key=lambda r: (-r["neutral_agree"], r["statement"]))
    near.sort(key=lambda r: (-r["neutral_agree"], r["statement"]))
    return passed, near[:leaning]
