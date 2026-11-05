"""Agreement between an answer sheet and each thinker, over stated positions only.

Mirrors apps/arena/public/placement.js; both are checked against tests/vectors.json.
"""

MIN_SHARED = 3


def score(agreed: int, shared: int) -> float:
    """Laplace-smoothed agreement, so one of one does not beat nine of eleven."""
    return (agreed + 1) / (shared + 2)


def agreement(
    answers: dict[str, int], stances: dict[str, dict[str, int]]
) -> dict[str, tuple[int, int, float]]:
    """Thinker -> (agreed, shared, score). `stances` maps anchor -> thinker -> +1 or -1."""
    counts: dict[str, list[int]] = {}
    for anchor, answer in answers.items():
        if answer not in (1, -1):
            continue
        for thinker, stance in stances.get(anchor, {}).items():
            pair = counts.setdefault(thinker, [0, 0])
            pair[1] += 1
            pair[0] += int(stance == answer)
    return {t: (k, n, score(k, n)) for t, (k, n) in counts.items()}


def ranked(
    answers: dict[str, int], stances: dict[str, dict[str, int]]
) -> list[tuple[str, int, int, float]]:
    rows = [(t, k, n, s) for t, (k, n, s) in agreement(answers, stances).items() if n >= MIN_SHARED]
    return sorted(rows, key=lambda r: (-r[3], -r[2], r[0]))


MIN_ANSWERED = 6
MIN_RANKED = 5


def position(
    answers: dict[str, int],
    stances: dict[str, dict[str, int]],
    coords: dict[str, tuple[float, float]],
) -> tuple[float, float] | None:
    """Where a person sits on the thinker map, as placement.js places "You": the top three
    thinkers by agreement, sharply weighted, since a broad average lands between schools."""
    import math

    answered = sum(1 for v in answers.values() if v in (1, -1))
    rows = [r for r in ranked(answers, stances) if r[0] in coords]
    if answered < MIN_ANSWERED or len(rows) < MIN_RANKED:
        return None
    wx = wy = wt = 0.0
    for thinker, _, _, s in rows[:3]:
        w = math.exp(14 * (s - 0.5))
        wx += w * coords[thinker][0]
        wy += w * coords[thinker][1]
        wt += w
    return wx / wt, wy / wt
