from arena_fingerprint.stances import merge

ATLAS = {"ideas": [
    {"id": "s1", "holders": [{"p": "ann", "a": 1, "inf": False}]},
    {"id": "s2", "holders": []},
    {"id": "s3", "holders": []},
]}  # fmt: skip
TASK = {
    "person": "bob",
    "statements": [{"id": "s1"}, {"id": "s2"}, {"id": "s3"}],
    "claims": [
        {
            "id": "c1",
            "quote": "AI could end us all, and that risk is real.",
            "url": "u",
            "work": "w",
        },
        {"id": "c2", "quote": "Regulation will strangle progress.", "url": "u", "work": "w"},
    ],
}


def item(statement, stance, claim, quote):
    return {"statement": statement, "stance": stance, "claim_id": claim, "quote": quote, "why": "x"}


def test_both_readers_must_agree_and_quotes_must_be_verbatim():
    readings = {
        ("A", "bob"): {"stances": [item("s1", "hold", "c1", "that risk is real"),
                                   item("s2", "reject", "c2", "Regulation will strangle progress."),
                                   item("s3", "hold", "c1", "made-up words")]},
        ("B", "bob"): {"stances": [item("s1", "hold", "c1", "AI could end us all"),
                                   item("s2", "hold", "c2", "strangle progress")]},
    }  # fmt: skip
    atlas, report = merge(ATLAS, {"bob": TASK}, readings)
    added = {(p, s): a for p, s, a in report.added}
    assert added == {("bob", "s1"): 1}
    assert ("bob", "s2") in report.readers_disagree
    assert any("verbatim" in i for i in report.invalid)
    holder = next(h for h in atlas["ideas"][0]["holders"] if h["p"] == "bob")
    assert holder["q"] == "that risk is real" and holder["inf"] is False
    assert ATLAS["ideas"][0]["holders"] == [{"p": "ann", "a": 1, "inf": False}]  # input untouched


def test_existing_stances_are_never_overwritten():
    atlas = {"ideas": [{"id": "s1", "holders": [{"p": "bob", "a": -1, "inf": False}]},
                       {"id": "s2", "holders": []}, {"id": "s3", "holders": []}]}  # fmt: skip
    both = {"stances": [item("s1", "hold", "c1", "that risk is real")]}
    out, report = merge(atlas, {"bob": TASK}, {("A", "bob"): both, ("B", "bob"): both})
    assert report.conflicts_with_atlas == [("bob", "s1")] and not report.added
    assert len(out["ideas"][0]["holders"]) == 1


def test_claims_of_other_people_are_refused():
    bad = {"stances": [item("s1", "hold", "someone-elses-claim", "x")]}
    _, report = merge(ATLAS, {"bob": TASK}, {("A", "bob"): bad, ("B", "bob"): bad})
    assert not report.added and len(report.invalid) == 2
