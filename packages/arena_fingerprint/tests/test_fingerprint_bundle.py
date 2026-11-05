import json
import pathlib

import pytest
from arena_fingerprint.agreement import agreement, ranked
from arena_fingerprint.anchors import select_anchors, stated_stances
from arena_fingerprint.bundle import CAMPS, BundleError, build_bundle

HERE = pathlib.Path(__file__).parent
ATLAS = HERE.parents[2] / "apps/arena/source/atlas-v1.json"
CAMP_MAP = {c["id"]: c["members"] for c in CAMPS}


@pytest.fixture(scope="module")
def atlas():
    return json.loads(ATLAS.read_text())


def test_shared_vectors_match():
    vectors = json.loads((HERE / "vectors.json").read_text())
    for case in vectors["cases"]:
        got = agreement(case["answers"], vectors["stances"])
        assert set(got) == set(case["expect"])
        for thinker, (k, n, s) in case["expect"].items():
            assert got[thinker][:2] == (k, n)
            assert got[thinker][2] == pytest.approx(s)


def test_ranked_needs_three_shared():
    vectors = json.loads((HERE / "vectors.json").read_text())
    rows = ranked(vectors["cases"][0]["answers"], vectors["stances"])
    assert [r[0] for r in rows] == ["ann", "cat", "bob"]
    assert ranked(vectors["cases"][1]["answers"], vectors["stances"]) == []


def test_stated_only_and_majority():
    idea = {
        "holders": [
            {"p": "a", "a": 1, "inf": False},
            {"p": "a", "a": -1, "inf": False},
            {"p": "b", "a": -1, "inf": True},
            {"p": "c", "a": -1, "inf": False},
        ]
    }
    assert stated_stances(idea) == {"a": 1, "c": -1}


def test_selection_is_deterministic_and_capped(atlas):
    first, _ = select_anchors(atlas["ideas"], CAMP_MAP)
    second, _ = select_anchors(list(reversed(atlas["ideas"])), CAMP_MAP)
    assert [a["id"] for a in first] == [a["id"] for a in second]
    assert len(first) == 24
    for set_id in ("being", "values", "action"):
        families = [a["family"] for a in first if a["set"] == set_id]
        assert len(families) == 8
        assert max(families.count(f) for f in families) <= 2
    for anchor in first:
        stances = stated_stances(anchor)
        assert len(stances) >= 3 and len(set(stances.values())) == 2


def test_bundle_stated_quotes_and_guards(atlas):
    bundle = build_bundle(atlas, flagged={"nick-fuentes"})
    assert len(bundle["anchors"]) == 24
    for entry in bundle["stances"].values():
        for item in entry.values():
            assert item["a"] in (1, -1)
            assert len(item.get("q", "")) <= 280
            assert ("q" in item) == ("url" in item)
    with pytest.raises(BundleError):
        build_bundle(atlas, flagged={"vitalik-buterin"})


def test_committed_bundle_is_current():
    """The committed bundle is what the committed atlas gives, with the season's statements."""
    committed = json.loads((HERE.parents[2] / "apps/arena/public/fingerprint.json").read_text())
    source = HERE.parents[2] / "apps/arena/source" / f"{committed['atlas_version']}.json"
    atlas = json.loads(source.read_text())
    voices = HERE.parents[2] / "seed/thinker-voices.json"
    rebuilt = build_bundle(
        atlas,
        flagged=set(),
        season=committed["anchors"],
        version=committed["version"],
        atlas_version=committed["atlas_version"],
        newcomers={
            p["id"]: p["name"]
            for name in (
                "AI-FUTURES-SOURCES-v2.json",
                "AI-FUTURES-SOURCES-v4.json",
                "AI-FUTURES-SOURCES-v5.json",
            )  # fmt: skip
            for p in json.loads((HERE.parents[2] / "seed" / name).read_text()).get("people", [])
        },
        voices=json.loads(voices.read_text()) if voices.exists() else {},
        season_id=committed["season"],
    )
    # portraits are added by the build script from seed/faces.json, after the bundle itself
    faces = committed.pop("faces", {})
    committed.pop("camps", None)  # derived from the tree by the build script
    rebuilt.pop("camps", None)
    for t in committed["thinkers"]:
        t.pop("role", None)  # from seed/roles.json, added by the build script
        face = t.pop("face", None)
        assert face is None or (t["id"] in faces and face == f"/faces/{t['id']}.jpg")
    assert committed == json.loads(json.dumps(rebuilt, ensure_ascii=False))


def test_season_keeps_statements_and_order(atlas):
    first = build_bundle(atlas, flagged=set())
    again = build_bundle(atlas, flagged=set(), season=first["anchors"], version="fp-x")
    assert [a["id"] for a in again["anchors"]] == [a["id"] for a in first["anchors"]]
    assert [a["set"] for a in again["anchors"]] == [a["set"] for a in first["anchors"]]
    assert again["stances"] == first["stances"] and again["version"] == "fp-x"


def test_newcomers_are_placed_provisionally_from_their_stances(atlas):
    import copy

    first = build_bundle(atlas, flagged=set())
    grown = copy.deepcopy(atlas)
    # a newcomer who answers exactly like Max Tegmark on his statements, and one with too few
    tegmark = {a["id"]: first["stances"][a["id"]].get("max-tegmark") for a in first["anchors"]}
    for idea in grown["ideas"]:
        stance = tegmark.get(idea["id"])
        if stance:
            idea["holders"].append({"p": "new-voice", "a": stance["a"], "inf": False, "q": "x",
                                    "url": "u", "work": "w"})  # fmt: skip
    one = first["anchors"][0]["id"]
    next(i for i in grown["ideas"] if i["id"] == one)["holders"].append(
        {"p": "thin-voice", "a": 1, "inf": False, "q": "x", "url": "u", "work": "w"}
    )
    bundle = build_bundle(
        grown, flagged=set(), season=first["anchors"],
        newcomers={"new-voice": "New Voice", "thin-voice": "Thin Voice"},
    )  # fmt: skip
    placed = {t["id"]: t for t in bundle["thinkers"] if t.get("provisional")}
    assert set(placed) == {"new-voice"}
    tegmark_row = next(t for t in bundle["thinkers"] if t["id"] == "max-tegmark")
    assert placed["new-voice"]["school"] == tegmark_row["school"]
    assert any("thin-voice" in line for line in bundle["selection_log"])
    assert all("thin-voice" not in e for e in bundle["stances"].values())
    import pytest as _pytest

    with _pytest.raises(BundleError):
        build_bundle(grown, flagged={"new-voice"}, newcomers={"new-voice": "New Voice"})


def test_position_matches_the_browser():
    """Server-side placement (people map) equals placement.js on the same answers; the expected
    values were produced by placement.js fingerprint() on the committed bundle."""
    from arena_fingerprint.agreement import position

    bundle = json.loads((HERE.parents[2] / "apps/arena/public/fingerprint.json").read_text())
    st = {a: {t: v["a"] for t, v in e.items()} for a, e in bundle["stances"].items()}
    co = {t["id"]: (t["x"], t["y"]) for t in bundle["thinkers"]}
    answers = {a["id"]: [1, -1, 1, 0, -1][i % 5] for i, a in enumerate(bundle["anchors"])}
    if bundle["version"] != "fp-2026-11-05.1":
        pytest.skip("expected values belong to bundle fp-2026-11-05.1")
    assert position(answers, st, co) == pytest.approx((-113.0458266047672, -36.62447828082642))
    assert position({}, st, co) is None
