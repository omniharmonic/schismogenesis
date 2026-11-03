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
    rebuilt = build_bundle(
        atlas,
        flagged=set(),
        season=committed["anchors"],
        version=committed["version"],
        atlas_version=committed["atlas_version"],
    )
    assert committed == json.loads(json.dumps(rebuilt, ensure_ascii=False))


def test_season_keeps_statements_and_order(atlas):
    first = build_bundle(atlas, flagged=set())
    again = build_bundle(atlas, flagged=set(), season=first["anchors"], version="fp-x")
    assert [a["id"] for a in again["anchors"]] == [a["id"] for a in first["anchors"]]
    assert [a["set"] for a in again["anchors"]] == [a["set"] for a in first["anchors"]]
    assert again["stances"] == first["stances"] and again["version"] == "fp-x"
