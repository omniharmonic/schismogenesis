"""A measured space of people: graded distance, an embedding, and how stable groupings are.

Positions within a question have graded distances (0 shared, 1 compatible, 2 tension, 3 opposed).
A person's distance from another is the mean over questions both addressed, pulled toward an
uninformative prior when they share few questions, so thin evidence cannot look like agreement.
"""

import random
from collections.abc import Callable, Mapping

import numpy as np

Holdings = Mapping[str, Mapping[str, set[str]]]  # person -> question -> position keys
PositionDistance = Callable[[str, str, str], float]  # question, a, b -> 0..3
PRIOR = 0.5
PRIOR_WEIGHT = 2.0


def pair_distance(
    a: Mapping[str, set[str]],
    b: Mapping[str, set[str]],
    distance: PositionDistance,
    questions: list[str] | None = None,
) -> tuple[float, int]:
    """Return (distance 0..1, shared question count). Blanks never count."""
    pool = questions if questions is not None else list(a.keys() & b.keys())
    values = [
        min(distance(q, x, y) for x in a[q] for y in b[q]) / 3 for q in pool if q in a and q in b
    ]
    shrunk = (sum(values) + PRIOR * PRIOR_WEIGHT) / (len(values) + PRIOR_WEIGHT)
    return shrunk, len(values)


def distance_matrix(
    holdings: Holdings, distance: PositionDistance, questions: list[str] | None = None
) -> tuple[list[str], np.ndarray]:
    people = sorted(holdings)
    matrix = np.zeros((len(people), len(people)))
    for i, a in enumerate(people):
        for j in range(i + 1, len(people)):
            value = pair_distance(holdings[a], holdings[people[j]], distance, questions)[0]
            matrix[i, j] = matrix[j, i] = value
    return people, matrix


def embed(matrix: np.ndarray, dimensions: int = 2) -> tuple[np.ndarray, float]:
    """Classical MDS. Returns coordinates and the share of variance those dimensions explain."""
    n = len(matrix)
    centering = np.eye(n) - np.ones((n, n)) / n
    inner = -0.5 * centering @ (matrix**2) @ centering
    values, vectors = np.linalg.eigh(inner)
    order = np.argsort(values)[::-1]
    values, vectors = values[order], vectors[:, order]
    positive = np.clip(values, 0, None)
    coords = vectors[:, :dimensions] * np.sqrt(positive[:dimensions])
    explained = float(positive[:dimensions].sum() / positive.sum()) if positive.sum() else 0.0
    return coords, explained


def groups(matrix: np.ndarray, cut: float) -> list[int]:
    """Average-linkage clustering, stopping when the closest groups are further apart than cut."""
    clusters = [[i] for i in range(len(matrix))]
    while len(clusters) > 1:
        best, pair = float("inf"), None
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                value = float(np.mean([matrix[a, b] for a in clusters[i] for b in clusters[j]]))
                if value < best:
                    best, pair = value, (i, j)
        if best > cut or pair is None:
            break
        clusters[pair[0]] += clusters.pop(pair[1])
    labels = [0] * len(matrix)
    for label, members in enumerate(clusters):
        for member in members:
            labels[member] = label
    return labels


def co_membership(
    holdings: Holdings,
    distance: PositionDistance,
    questions: list[str],
    cut: float,
    rounds: int = 500,
    seed: int = 20261101,
) -> tuple[list[str], np.ndarray]:
    """How often each pair lands in one group when the questions are resampled with replacement."""
    rng = random.Random(seed)
    people = sorted(holdings)
    together = np.zeros((len(people), len(people)))
    for _ in range(rounds):
        sample = [rng.choice(questions) for _ in questions]
        _, matrix = distance_matrix(holdings, distance, sample)
        labels = groups(matrix, cut)
        for i in range(len(people)):
            for j in range(len(people)):
                together[i, j] += labels[i] == labels[j]
    return people, together / rounds
