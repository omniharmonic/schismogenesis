from arena_map.positions import Alignment, align, groups


def test_blanks_never_count_as_disagreement():
    pair = align({"a": {"q1": {"x"}, "q2": {"y"}}, "b": {"q1": {"x"}, "q3": {"z"}}})[0]
    assert (pair.shared_questions, pair.same_position, pair.score) == (1, 1, 1.0)


def test_no_shared_questions_has_no_score():
    assert align({"a": {"q1": {"x"}}, "b": {"q2": {"x"}}})[0].score is None


def test_holding_several_positions_counts_any_overlap():
    assert align({"a": {"q": {"x", "y"}}, "b": {"q": {"y"}}})[0].same_position == 1


def test_groups_need_enough_evidence():
    thin = Alignment("a", "b", 2, 2)
    strong = Alignment("c", "d", 3, 3)
    weak = Alignment("c", "e", 4, 2)
    assert groups([thin, strong, weak]) == [["c", "d"]]
