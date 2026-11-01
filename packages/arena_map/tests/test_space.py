import numpy as np
from arena_map.memes import Work, compile_item, contexts, use_by_author
from arena_map.space import co_membership, distance_matrix, embed, groups, pair_distance

SCALE = {frozenset({"x", "y"}): 1, frozenset({"x", "z"}): 3, frozenset({"y", "z"}): 2}


def d(_q, a, b):
    return 0 if a == b else SCALE[frozenset({a, b})]


def test_graded_distance_separates_tension_from_opposition():
    near = pair_distance({"q": {"x"}}, {"q": {"y"}}, d)[0]
    far = pair_distance({"q": {"x"}}, {"q": {"z"}}, d)[0]
    assert near < far


def test_thin_evidence_is_pulled_toward_unknown():
    one = pair_distance({"a": {"x"}}, {"a": {"x"}}, d)[0]
    many = {str(i): {"x"} for i in range(8)}
    assert pair_distance(many, many, d)[0] < one < 0.5


def test_no_shared_questions_is_unknown_not_disagreement():
    assert pair_distance({"a": {"x"}}, {"b": {"x"}}, d) == (0.5, 0)


def test_embedding_recovers_a_line():
    matrix = np.abs(np.subtract.outer(np.arange(4.0), np.arange(4.0)))
    coords, explained = embed(matrix, 1)
    assert explained > 0.99
    gaps = np.abs(np.diff(coords[:, 0]))
    assert np.allclose(gaps, 1.0, atol=1e-6)


def test_groups_respect_the_cut():
    matrix = np.array([[0, 0.1, 0.9], [0.1, 0, 0.9], [0.9, 0.9, 0.0]])
    labels = groups(matrix, 0.5)
    assert labels[0] == labels[1] != labels[2]


def test_stability_is_high_for_clear_structure():
    holdings = {
        "a": {str(i): {"x"} for i in range(10)},
        "b": {str(i): {"x"} for i in range(10)},
        "c": {str(i): {"z"} for i in range(10)},
    }
    people, together = co_membership(holdings, d, [str(i) for i in range(10)], 0.45, rounds=50)
    assert people == ["a", "b", "c"]
    assert together[0, 1] == 1 and together[0, 2] == 0


def test_matrix_is_symmetric():
    _, matrix = distance_matrix({"a": {"q": {"x"}}, "b": {"q": {"z"}}}, d)
    assert np.allclose(matrix, matrix.T)


def test_meme_counts_use_rates_and_first_year():
    works = [
        Work("w1", "a", 2010, "The Cathedral and the cathedral.", 5000),
        Work("w2", "a", 2007, "the Cathedral", 5000),
        Work("w3", "b", None, "nothing here", 100),
    ]
    found = use_by_author(compile_item([r"\bcathedral\b"]), works)
    assert found == {"a": {"uses": 3, "first": 2007, "works": ["w1", "w2"], "rate": 3.0}}
    assert "Cathedral" in contexts(compile_item(["cathedral"]), "the Cathedral rose", 5)[0]
