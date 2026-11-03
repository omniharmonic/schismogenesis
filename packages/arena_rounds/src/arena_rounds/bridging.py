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
NEUTRAL_LOW = 0.65
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
    neutral_low: np.ndarray | None = None  # 10th percentile of μ + b_s over participant bootstraps


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


def _solve(n, sf, sff, sy, sfy, lambda_i: float, lambda_f: float):
    """Vectorised 2x2 ridge solves for many rows at once: intercept and factor."""
    a, b, d = n + lambda_i, sf, sff + lambda_f
    det = a * d - b * b
    return (d * sy - b * sfy) / det, (a * sfy - b * sy) / det


def _als(r, seen, f_u, lambda_i, lambda_f, sweeps):
    w = seen.astype(float)
    filled = np.where(seen, r, 0.0)
    n_u, n_s = r.shape
    b_u, b_s, f_s = np.zeros(n_u), np.zeros(n_s), np.zeros(n_s)
    mu = float(filled.sum() / max(w.sum(), 1))
    for _ in range(sweeps):
        y = (filled - mu - b_u[:, None]) * w
        b_s, f_s = _solve(
            w.sum(0), w.T @ f_u, w.T @ f_u**2, y.sum(0), y.T @ f_u, lambda_i, lambda_f
        )
        y = (filled - mu - b_s[None, :]) * w
        b_u, f_u = _solve(w.sum(1), w @ f_s, w @ f_s**2, y.sum(1), y @ f_s, lambda_i, lambda_f)
        prediction = b_u[:, None] + b_s[None, :] + np.outer(f_u, f_s)
        mu = float(((filled - prediction) * w).sum() / max(w.sum(), 1))
    return mu, b_u, f_u, b_s, f_s


def fit_bridging(
    m: VoteMatrix,
    init: dict[str, float] | None = None,
    lambda_i: float = 0.15,
    lambda_f: float = 0.03,
    sweeps: int = 60,
    bootstrap: int = 0,
    seed: int = 7,
) -> BridgeFit | None:
    rated = _ratings(m)
    r = rated.values
    if r.size == 0 or r.shape[0] < 2:
        return None
    n_u = r.shape[0]
    seen = ~np.isnan(r)
    init = init or {}
    f_u = np.array([init.get(p, 0.0) for p in rated.participants], dtype=float)
    if not np.any(f_u):
        f_u = np.linspace(-1, 1, n_u)
    reference = f_u.copy()
    mu, b_u, f_u, b_s, f_s = _als(r, seen, f_u, lambda_i, lambda_f, sweeps)
    if reference.std() and f_u.std() and np.corrcoef(f_u, reference)[0, 1] < 0:
        f_u, f_s = -f_u, -f_s  # keep the sign of the Polis first component
    low = None
    if bootstrap:
        # Resample participants; the 10th percentile of neutral agreement guards against
        # statements that pass only because of a few raters, like Community Notes'
        # uncertainty checks.
        random = np.random.default_rng(seed)
        draws = []
        for _ in range(bootstrap):
            rows = random.integers(0, n_u, n_u)
            mu_b, _, _, b_s_b, _ = _als(
                r[rows], seen[rows], f_u[rows].copy(), lambda_i, lambda_f, 25
            )
            draws.append(mu_b + b_s_b)
        low = np.percentile(np.array(draws), 10, axis=0)
    return BridgeFit(mu, rated.participants, rated.statements, b_u, f_u, b_s, f_s, r, low)


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
                "neutral_low": None
                if fit.neutral_low is None
                else round(float(fit.neutral_low[j]), 3),
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
        and (r["neutral_low"] is None or r["neutral_low"] >= NEUTRAL_LOW)
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
