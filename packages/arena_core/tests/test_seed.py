import copy
import json

import pytest
from arena_core.seed import (
    SeedError,
    load_seed,
    merge_inputs,
    niche_aliases,
    niche_lookup,
    person_aliases,
    resolve_niche_refs,
    verify_seed,
)
from conftest import REPO
from sqlalchemy import text

SEED = REPO / "seed/SEED-v4.json"
SLICE = REPO / "seed/SLICE-1-LANDMARKS.json"
TABLES = [
    "niche",
    "person",
    "landmark",
    "landmark_niche",
    "event_log",
    "pipeline_run",
    "stage_item",
]


def counts(engine) -> dict[str, int]:
    with engine.connect() as connection:
        return {
            t: connection.execute(text(f"SELECT count(*) FROM {t}")).scalar_one() for t in TABLES
        }


def test_niche_aliases_mark_outsider_labels():
    assert niche_aliases(["paleocons", "'woke right' (critics' label)"]) == [
        {"text": "paleocons", "kind": "self"},
        {"text": "'woke right' (critics' label)", "kind": "outsider"},
    ]


def test_person_aliases_read_stage_name_and_handle():
    record = {"name": "Ansem (Zion Thomas)", "record_type": "person", "platforms": {"x": "@a_b"}}
    assert [a["text"] for a in person_aliases(record)] == ["Zion Thomas", "@a_b"]
    assert person_aliases({"name": "Duo (Show)", "record_type": "multi-person"}) == []


def test_niche_refs_keep_only_unambiguous_exact_matches():
    niches = [
        {"niche_id": "a", "name": "Alpha", "aliases": ["shared"]},
        {"niche_id": "b", "name": "Beta", "aliases": ["shared"]},
    ]
    lookup = niche_lookup(niches)
    assert resolve_niche_refs(["ALPHA", "beta", "shared", "unknown"], lookup, "b") == ["a"]


def minimal_inputs():
    seed = {
        "niches": [{"niche_id": "n"}],
        "landmarks": [{"landmark_id": "x", "primary_niche": "n"}],
        "excluded_landmarks": [{"landmark_id": "banned"}],
        "flags_for_benjamin": {"landmarks": []},
    }
    return seed, {"niches": [{"niche_id": "n"}], "landmarks": [{"landmark_id": "x"}]}


def test_slice_landmark_must_exist_or_be_marked_added():
    seed, slice_ = minimal_inputs()
    slice_["landmarks"].append({"landmark_id": "typo"})
    with pytest.raises(SeedError, match="typo"):
        merge_inputs(seed, slice_)


def test_excluded_landmark_can_never_enter_through_the_slice():
    seed, slice_ = minimal_inputs()
    slice_["landmarks"].append({"landmark_id": "banned", "added": "x", "primary_niche": "n"})
    with pytest.raises(SeedError, match="banned"):
        merge_inputs(seed, slice_)


def test_flag_list_hides_landmark_even_if_record_field_is_empty():
    seed, slice_ = minimal_inputs()
    seed["flags_for_benjamin"]["landmarks"] = [{"landmark_id": "x", "type": "exclusion-review"}]
    assert merge_inputs(seed, slice_)[0]["flag_type"] == "exclusion-review"


@pytest.mark.db
def test_load_matches_gate_and_second_load_adds_nothing(engine):
    assert load_seed(engine, SEED, SLICE).created == 234 + 819
    assert [r for r in verify_seed(engine) if r[1] != r[2]] == []
    before = counts(engine)
    assert load_seed(engine, SEED, SLICE).skipped
    assert counts(engine) == before


@pytest.mark.db
def test_bayeslord_and_flags_load_as_decided(engine):
    load_seed(engine, SEED, SLICE)
    with engine.connect() as connection:
        row = connection.execute(
            text(
                "SELECT in_slice, seed_version, panel_status FROM landmark "
                "WHERE landmark_id = 'bayeslord'"
            )
        ).one()
        assert tuple(row) == ("slice-1", "SEED-v4+D-31.9", "newcomer")
        hidden = connection.execute(
            text(
                "SELECT in_slice FROM landmark WHERE landmark_id = 'brad-carson'"
                " AND NOT public_surface_allowed"
            )
        ).scalar_one()
        assert hidden == "slice-1"


@pytest.mark.db
def test_reload_with_changed_seed_never_exposes_a_hidden_landmark(engine, tmp_path):
    load_seed(engine, SEED, SLICE)
    with engine.begin() as connection:
        connection.execute(
            text(
                "UPDATE landmark SET public_surface_allowed = false "
                "WHERE landmark_id = 'scott-alexander'"
            )
        )
    data = copy.deepcopy(json.loads(SEED.read_text()))
    data["niches"][0]["description"] = "changed"
    changed = tmp_path / "seed.json"
    changed.write_text(json.dumps(data))

    result = load_seed(engine, changed, SLICE)

    assert (result.created, result.updated) == (0, 1)
    with engine.connect() as connection:
        allowed = connection.execute(
            text(
                "SELECT public_surface_allowed FROM landmark WHERE landmark_id = 'scott-alexander'"
            )
        ).scalar_one()
    assert allowed is False
