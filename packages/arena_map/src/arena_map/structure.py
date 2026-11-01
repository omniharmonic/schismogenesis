"""Worldviews as structures: people and ideas in one space, and where two people fork.

Height on the atlas is the layer of an idea. Horizontal position compares people over families of
related ideas. Thinkers rarely address the same exact proposition (about 10% of person-idea cells
are filled), so comparing idea by idea mostly measures silence. Families make comparison possible
and are the clusters of ideas that worldviews are built from. A person's score on a family is the
signed, damped count of ideas held there, centred so that ground everyone shares does not count as
closeness. Silence stays zero after centring only for people near the average, and bootstrap
stability shows how far to trust the result.
"""

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import MDS, trustworthiness

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
class Space:
    people: list[str]
    matrix: np.ndarray  # people by families, signed, damped and centred
    distance: np.ndarray  # square cosine distance between people
    explained: np.ndarray  # share of variance on each axis


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


def families(similarity: np.ndarray, count: int) -> list[int]:
    """Group ideas by average linkage over a similarity matrix."""
    distance = np.clip(1 - similarity, 0, 2)
    np.fill_diagonal(distance, 0)
    model = AgglomerativeClustering(count, metric="precomputed", linkage="average")
    return [int(label) for label in model.fit_predict(distance)]


def person_space(holdings: list[Holding], family: dict[str, int]) -> Space:
    people = sorted({h.person for h in holdings})
    row = {p: i for i, p in enumerate(people)}
    columns = sorted(set(family.values()))
    col = {c: i for i, c in enumerate(columns)}
    table = np.zeros((len(people), len(columns)))
    for h in holdings:
        weight = INFERRED_WEIGHT if h.inferred else 1.0
        table[row[h.person], col[family[h.idea]]] += weight if h.accepts else -weight
    damped = np.sign(table) * np.sqrt(np.abs(table))
    centred = damped - damped.mean(0)
    values = np.linalg.svd(centred, compute_uv=False) ** 2
    return Space(people, centred, squareform(pdist(centred, "cosine")), values / values.sum())


def layout(space: Space, seed: int = 7) -> np.ndarray:
    """Two-dimensional positions that preserve the measured distances as far as possible."""
    model = MDS(
        2, dissimilarity="precomputed", random_state=seed, n_init=8, normalized_stress="auto"
    )
    return np.asarray(model.fit_transform(space.distance))


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


def _cluster(names: list[str], distance: np.ndarray, count: int) -> list[list[str]]:
    labels = fcluster(linkage(squareform(distance, checks=False), "average"), count, "maxclust")
    groups: dict[int, list[str]] = defaultdict(list)
    for name, label in zip(names, labels, strict=True):
        groups[int(label)].append(name)
    return list(groups.values())


def schools(space: Space, count: int) -> list[list[str]]:
    return _cluster(space.people, space.distance, count)


def school_stability(
    holdings: list[Holding],
    family: dict[str, int],
    count: int,
    runs: int = 500,
    seed: int = 7,
) -> dict[frozenset[str], float]:
    """Share of reruns, resampling families, in which each pair lands in one school."""
    random = np.random.default_rng(seed)
    names = sorted(set(family.values()))
    by_family: dict[int, list[Holding]] = defaultdict(list)
    for h in holdings:
        by_family[family[h.idea]].append(h)
    together: dict[frozenset[str], int] = defaultdict(int)
    seen: dict[frozenset[str], int] = defaultdict(int)
    for _ in range(runs):
        sample: list[Holding] = []
        drawn: dict[str, int] = {}
        for n, pick in enumerate(random.integers(0, len(names), len(names))):
            for h in by_family[names[int(pick)]]:
                key = f"{h.idea}#{n}"
                drawn[key] = n
                sample.append(Holding(h.person, key, h.accepts, h.inferred))
        space = person_space(sample, drawn)
        groups = schools(space, count)
        for first, second in combinations(space.people, 2):
            seen[frozenset({first, second})] += 1
        for group in groups:
            for first, second in combinations(group, 2):
                together[frozenset({first, second})] += 1
    return {pair: together[pair] / number for pair, number in seen.items()}


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
