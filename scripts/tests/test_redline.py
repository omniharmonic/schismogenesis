import json

from arena_cli.redline import check


def repo(tmp_path):
    (tmp_path / "seed").mkdir()
    seed = {
        "flags_for_benjamin": {"landmarks": [{"landmark_id": "hidden-one", "name": "Hidden One"}]},
        "excluded_landmarks": [{"landmark_id": "gone", "name": "Gone"}],
    }
    (tmp_path / "seed/SEED-v4.json").write_text(json.dumps(seed))
    return tmp_path


def test_clean_repo_passes(tmp_path):
    assert check(repo(tmp_path), tracked=[".env.example", "README.md"]) == []


def test_tracked_secret_and_transcript_are_violations(tmp_path):
    found = check(repo(tmp_path), tracked=[".env", "transcripts/a.txt", "evals/results/x.json"])
    assert len(found) == 3


def test_hidden_landmark_in_public_bundle_is_a_violation(tmp_path):
    root = repo(tmp_path)
    (root / "dist").mkdir()
    (root / "dist/map.json").write_text('{"label": "Hidden One"}')
    assert check(root, tracked=[]) == ["dist/map.json mentions hidden: hidden-one"]
