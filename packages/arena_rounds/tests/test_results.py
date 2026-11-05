import json
import pathlib

import numpy as np
from arena_rounds.results import results

BUNDLE = json.loads(
    (pathlib.Path(__file__).parents[3] / "apps/arena/public/fingerprint.json").read_text()
)
STANCES = {a: {t: v["a"] for t, v in e.items()} for a, e in BUNDLE["stances"].items()}


def like(thinker: str, n: int, seed: int = 0) -> dict[str, dict[str, int]]:
    """n people who answer like a thinker where they have a stance, randomly elsewhere."""
    random = np.random.default_rng(seed)
    out = {}
    for i in range(n):
        sheet = {}
        for a in BUNDLE["anchors"]:
            v = STANCES[a["id"]].get(thinker)
            sheet[a["id"]] = (
                v if v is not None and random.random() > 0.1 else int(random.choice([-1, 1]))
            )
        out[f"{thinker}-{i}"] = sheet
    return out


def test_small_numbers_show_nothing():
    r = results(like("max-tegmark", 5), BUNDLE)
    assert r["contributors"] == 5 and r["statements"] == [] and r["notes"]


def test_homes_crosstab_and_suppression():
    sheets = (
        like("max-tegmark", 30) | like("marc-andreessen", 25, seed=1) | like("karen-hao", 4, seed=2)
    )
    r = results(sheets, BUNDLE)
    assert r["contributors"] == 59
    schools = {h["school"]: h["people"] for h in r["homes"]}
    assert all(c >= 10 for c in schools.values())
    assert sum(schools.values()) < 59  # the small group is folded away, not shown
    assert any("too small" in n for n in r["notes"])
    assert r["crosstab"] is not None and len(r["crosstab"]["schools"]) >= 2
    for cells in r["crosstab"]["cells"].values():
        for cell in cells.values():
            assert cell is None or cell["n"] >= 10
    row = r["statements"][0]
    assert row["agree"] + row["disagree"] + row["unsure"] == row["answered"]
    blob = json.dumps(r)
    assert "max-tegmark-0" not in blob and "marc-andreessen-3" not in blob


def test_camp_alignment_tracks_who_answered():
    r = results(like("guillaume-verdon", 20) | like("marc-andreessen", 10, seed=4), BUNDLE)
    shares = {c["label"]: c["share_aligned"] for c in r["camps"]}
    assert shares["Market optimists"] > shares["AI as a new kind of risk"]
