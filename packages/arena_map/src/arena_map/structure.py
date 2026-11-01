"""Worldviews as structures: people and ideas in one space, and where two people fork.

Height on the atlas is the layer of an idea. Horizontal position comes from correspondence analysis,
which places people and what they hold in the same space (Benzécri, Bourdieu). Each idea is doubled
into accept and reject columns, so rejecting something is information and not a blank.
"""

from collections import defaultdict
from dataclasses import dataclass

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist
from sklearn.manifold import trustworthiness

LAYERS = ("ontological", "epistemic", "axiological", "empirical", "praxis")
ROOT_LAYERS = {"ontological", "epistemic"}
INFERRED_WEIGHT = 0.5


@dataclass(frozen=True)
class Holding:
    person: str
    idea: str
    accepts: bool
    inferred: bool


@dataclass(frozen=True)
class Coordinates:
    people: dict[str, np.ndarray]
    ideas: dict[str, np.ndarray]  # "x" is accept, "x:reject" is reject
    inertia: np.ndarray


@dataclass(frozen=True)
class Fork:
    by_layer: dict[str, tuple[int, int]]  # layer -> (shared, opposed)
    lowest_opposed: str | None
    shared_roots: list[str]  # both stated
    inferred_roots: list[str]  # shared, but at least one side is inferred


@dataclass(frozen=True)
class SenseFork:
    distance: float
    p: float


def correspondence(holdings: list[Holding], dims: int = 8) -> Coordinates:
    """Correspondence analysis of people by accept and reject columns.

    Columns held by nobody cannot exist, and a single-holder column gets its own axis weight in the
    usual way, so it shapes the space little once mass is accounted for.
    """
    people = sorted({h.person for h in holdings})
    columns = sorted({h.idea if h.accepts else f"{h.idea}:reject" for h in holdings})
    row = {p: i for i, p in enumerate(people)}
    col = {c: i for i, c in enumerate(columns)}
    table = np.zeros((len(people), len(columns)))
    for h in holdings:
        name = h.idea if h.accepts else f"{h.idea}:reject"
        weight = INFERRED_WEIGHT if h.inferred else 1.0
        table[row[h.person], col[name]] = max(table[row[h.person], col[name]], weight)

    p = table / table.sum()
    r, c = p.sum(1), p.sum(0)
    residual = (p - np.outer(r, c)) / np.sqrt(np.outer(r, c))
    u, s, vt = np.linalg.svd(residual, full_matrices=False)
    k = min(dims, int((s > 1e-10).sum()))
    people_xy = (u[:, :k] * s[:k]) / np.sqrt(r)[:, None]
    ideas_xy = (vt.T[:, :k] * s[:k]) / np.sqrt(c)[:, None]
    # A fixed sign makes runs comparable.
    for axis in range(k):
        if people_xy[0, axis] > 0:
            people_xy[:, axis] *= -1
            ideas_xy[:, axis] *= -1
    return Coordinates(
        {name: people_xy[i] for name, i in row.items()},
        {name: ideas_xy[i] for name, i in col.items()},
        s[:k] ** 2,
    )


def fork_profile(a: str, b: str, holdings: list[Holding], layer: dict[str, str]) -> Fork:
    """Where two people stand together and apart, from the deepest layer upward."""
    mine = {h.idea: h for h in holdings if h.person == a}
    yours = {h.idea: h for h in holdings if h.person == b}
    counts = {name: [0, 0] for name in LAYERS}
    shared_roots, inferred_roots = [], []
    for idea in sorted(mine.keys() & yours.keys()):
        level = layer[idea]
        same = mine[idea].accepts == yours[idea].accepts
        counts[level][0 if same else 1] += 1
        if same and level in ROOT_LAYERS:
            either_inferred = mine[idea].inferred or yours[idea].inferred
            (inferred_roots if either_inferred else shared_roots).append(idea)
    lowest = next((name for name in LAYERS if counts[name][1]), None)
    return Fork({k: (v[0], v[1]) for k, v in counts.items()}, lowest, shared_roots, inferred_roots)


def _cluster(names: list[str], points: np.ndarray, cut: float) -> list[list[str]]:
    if len(names) < 2:
        return [names]
    distances = pdist(points)
    scale = distances.max() or 1.0
    labels = fcluster(linkage(distances / scale, "average"), cut, "distance")
    groups: dict[int, list[str]] = defaultdict(list)
    for name, label in zip(names, labels, strict=True):
        groups[int(label)].append(name)
    return list(groups.values())


def schools(coordinates: Coordinates, cut: float) -> list[list[str]]:
    names = sorted(coordinates.people)
    return _cluster(names, np.array([coordinates.people[n] for n in names]), cut)


def school_stability(
    holdings: list[Holding], cut: float, runs: int = 500, seed: int = 7
) -> dict[frozenset[str], float]:
    """Share of reruns, resampling ideas, in which each pair lands in one school."""
    random = np.random.default_rng(seed)
    ideas = sorted({h.idea for h in holdings})
    by_idea: dict[str, list[Holding]] = defaultdict(list)
    for h in holdings:
        by_idea[h.idea].append(h)
    together: dict[frozenset[str], int] = defaultdict(int)
    seen: dict[frozenset[str], int] = defaultdict(int)
    for _ in range(runs):
        sample: list[Holding] = []
        for n, pick in enumerate(random.integers(0, len(ideas), len(ideas))):
            sample += [
                Holding(h.person, f"{h.idea}#{n}", h.accepts, h.inferred)
                for h in by_idea[ideas[pick]]
            ]
        groups = schools(correspondence(sample), cut)
        present = sorted({h.person for h in sample})
        for i, first in enumerate(present):
            for second in present[i + 1 :]:
                seen[frozenset({first, second})] += 1
        for group in groups:
            for i, first in enumerate(group):
                for second in group[i + 1 :]:
                    together[frozenset({first, second})] += 1
    return {pair: together[pair] / count for pair, count in seen.items()}


def reasons_load(holders: int, links: int) -> float:
    """Argument links per holder: how much reasoning an idea carries for the people using it."""
    return links / holders if holders else 0.0


def sense_fork(
    vectors: dict[str, np.ndarray], min_uses: int = 5, permutations: int = 2000, seed: int = 7
) -> SenseFork | None:
    """Do two schools use a term differently? Cosine gap between centroids, by permutation."""
    first, second = sorted(vectors)[:2]
    a, b = vectors[first], vectors[second]
    if len(a) < min_uses or len(b) < min_uses:
        return None

    def gap(x: np.ndarray, y: np.ndarray) -> float:
        p, q = x.mean(0), y.mean(0)
        return 1 - float(p @ q / (np.linalg.norm(p) * np.linalg.norm(q)))

    observed = gap(a, b)
    random = np.random.default_rng(seed)
    pooled = np.vstack([a, b])
    beyond = 0
    for _ in range(permutations):
        order = random.permutation(len(pooled))
        beyond += gap(pooled[order[: len(a)]], pooled[order[len(a) :]]) >= observed
    return SenseFork(observed, (beyond + 1) / (permutations + 1))


def fidelity(full: np.ndarray, layout: np.ndarray, neighbours: int = 5) -> float:
    """How far nearest neighbours in the full space stay neighbours in the layout, from 0 to 1."""
    return float(trustworthiness(full, layout, n_neighbors=neighbours))
