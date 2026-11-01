import numpy as np
from arena_map.structure import (
    Holding,
    families,
    fidelity,
    fork_profile,
    layout,
    person_space,
    reasons_load,
    school_stability,
    schools,
    sense_fork,
)


def camps() -> list[Holding]:
    rows = []
    for person in ("a1", "a2", "a3"):
        rows += [Holding(person, "x", True, False), Holding(person, "y", True, False)]
        rows += [Holding(person, "z", False, False)]
    for person in ("b1", "b2", "b3"):
        rows += [Holding(person, "x", False, False), Holding(person, "y", False, False)]
        rows += [Holding(person, "z", True, False)]
    rows += [Holding("a1", "w", True, False), Holding("b1", "v", True, False)]
    return rows


FAMILY = {"x": 0, "y": 1, "z": 2, "w": 3, "v": 4}


def test_families_group_similar_ideas():
    similarity = np.array([[1, 0.9, 0.1], [0.9, 1, 0.1], [0.1, 0.1, 1]])
    labels = families(similarity, 2)
    assert labels[0] == labels[1] != labels[2]


def test_opposing_camps_are_far_apart():
    space = person_space(camps(), FAMILY)
    at = {p: i for i, p in enumerate(space.people)}
    assert space.distance[at["a2"], at["a3"]] < space.distance[at["a2"], at["b2"]]


def test_a_shared_idea_does_not_create_closeness():
    rows = camps() + [Holding(p, "all", True, False) for p in ("a1", "a2", "a3", "b1", "b2", "b3")]
    space = person_space(rows, {**FAMILY, "all": 5})
    assert np.allclose(space.matrix[:, -1], 0)


def test_inferred_stances_weigh_less_than_stated():
    base = camps()
    stated = person_space(base + [Holding("a1", "q", True, False)], {**FAMILY, "q": 5})
    inferred = person_space(base + [Holding("a1", "q", True, True)], {**FAMILY, "q": 5})
    assert abs(inferred.matrix[0, -1]) < abs(stated.matrix[0, -1])


def test_layout_keeps_neighbours_close():
    space = person_space(camps(), FAMILY)
    points = layout(space)
    at = {p: i for i, p in enumerate(space.people)}
    within = np.linalg.norm(points[at["a2"]] - points[at["a3"]])
    across = np.linalg.norm(points[at["a2"]] - points[at["b2"]])
    assert within < across


LAYER = {"root": "ontological", "value": "axiological", "act": "praxis"}


def test_shared_root_and_opposed_values():
    rows = [
        Holding("p", "root", True, False),
        Holding("q", "root", True, False),
        Holding("p", "value", True, False),
        Holding("q", "value", False, False),
    ]
    fork = fork_profile("p", "q", rows, LAYER)
    assert fork.lowest_opposed == "axiological"
    assert fork.shared_roots == ["root"]
    assert fork.by_layer["ontological"] == (1, 0)
    assert fork.by_layer["axiological"] == (0, 1)


def test_no_overlap_means_no_fork():
    rows = [Holding("p", "root", True, False), Holding("q", "act", True, False)]
    fork = fork_profile("p", "q", rows, LAYER)
    assert fork.lowest_opposed is None
    assert fork.shared_roots == []


def test_shared_rejection_counts_as_shared_ground():
    rows = [Holding("p", "root", False, False), Holding("q", "root", False, False)]
    assert fork_profile("p", "q", rows, LAYER).by_layer["ontological"] == (1, 0)


def test_inferred_only_shared_root_is_kept_apart():
    rows = [Holding("p", "root", True, True), Holding("q", "root", True, False)]
    fork = fork_profile("p", "q", rows, LAYER)
    assert fork.shared_roots == []
    assert fork.inferred_roots == ["root"]


def test_schools_and_their_stability():
    rows = camps()
    found = schools(person_space(rows, FAMILY), 2)
    assert sorted(sorted(group) for group in found) == [["a1", "a2", "a3"], ["b1", "b2", "b3"]]
    stable = school_stability(rows, FAMILY, 2, runs=20)
    assert stable[frozenset({"a2", "a3"})] > 0.8


def test_reasons_load():
    assert reasons_load(holders=4, links=2) == 0.5
    assert reasons_load(holders=0, links=2) == 0.0


def test_sense_fork_needs_enough_uses():
    few = {"a": np.ones((2, 4)), "b": np.ones((9, 4))}
    assert sense_fork(few) is None


def test_sense_fork_separates_real_differences():
    random = np.random.default_rng(1)
    apart = {
        "a": random.normal([1, 0, 0], 0.1, (12, 3)),
        "b": random.normal([0, 1, 0], 0.1, (12, 3)),
    }
    mixed = {
        "a": random.normal([1, 0, 0], 0.1, (12, 3)),
        "b": random.normal([1, 0, 0], 0.1, (12, 3)),
    }
    far, near = sense_fork(apart), sense_fork(mixed)
    assert far is not None and far.p < 0.01
    assert near is not None and near.p > 0.05


def test_fidelity_is_perfect_for_the_same_points():
    points = np.random.default_rng(2).normal(size=(30, 2))
    assert fidelity(points, points) > 0.99
