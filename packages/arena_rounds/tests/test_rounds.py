import json
import pathlib

import numpy as np
import pytest
from arena_rounds.bridging import bridges, fit_bridging
from arena_rounds.matrix import VoteMatrix
from arena_rounds.polis import consensus, group_stats, polis_groups
from arena_rounds.report import participant_view, room_report
from arena_rounds.synthetic import synthetic_votes
from sklearn.metrics import adjusted_rand_score

BUNDLE = json.loads(
    (pathlib.Path(__file__).parents[3] / "apps/arena/public/fingerprint.json").read_text()
)


def planted(n_per=20, statements=24, seed=1, noise=0.1):
    """Three groups with opposite blocks, plus one bridge (s-bridge) and one divider (s-div)."""
    random = np.random.default_rng(seed)
    base = random.choice([-1, 1], size=(3, statements))
    rows, truth = [], {}
    for g in range(3):
        for i in range(n_per):
            p = f"g{g}-{i:02d}"
            truth[p] = g
            plan = {f"s{j:02d}": int(base[g, j]) for j in range(statements)}
            plan["s-bridge"] = 1
            plan["s-div"] = 1 if g == 0 else -1
            for s, v in plan.items():
                if random.random() < 0.15:
                    continue
                rows.append((p, s, -v if random.random() < noise else v))
    return rows, truth


def test_planted_groups_recovered():
    rows, truth = planted()
    result = polis_groups(VoteMatrix.from_rows(rows))
    assert result is not None and result.k == 3
    assert adjusted_rand_score([truth[p] for p in result.participants], result.labels) >= 0.8


def test_deterministic():
    rows, _ = planted()
    m = VoteMatrix.from_rows(rows)
    a, b = polis_groups(m), polis_groups(m)
    assert a is not None and b is not None
    assert (a.labels == b.labels).all()
    fa, fb = fit_bridging(m, a.pc1), fit_bridging(m, b.pc1)
    assert fa is not None and fb is not None
    assert np.allclose(fa.b_s, fb.b_s)


def test_bridge_passes_and_divider_does_not():
    rows, _ = planted()
    m = VoteMatrix.from_rows(rows)
    polis = polis_groups(m)
    fit = fit_bridging(m, polis.pc1 if polis else None)
    assert fit is not None
    passed, _ = bridges(fit)
    ids = [b["statement"] for b in passed]
    assert "s-bridge" in ids
    assert "s-div" not in ids


def test_consensus_finds_planted_bridge():
    rows, _ = planted()
    m = VoteMatrix.from_rows(rows)
    polis = polis_groups(m)
    assert polis is not None
    members = {
        g: [p for p, lab in zip(polis.participants, polis.labels, strict=True) if lab == g]
        for g in range(polis.k)
    }
    rows_ = consensus(group_stats(m, members))
    common = [r["statement"] for r in rows_ if r["all_agree"]]
    assert "s-bridge" in common and "s-div" not in common


def test_single_cluster_is_reported_as_unclear():
    random = np.random.default_rng(3)
    rows = [(f"p{i}", f"s{j}", int(random.choice([-1, 1]))) for i in range(40) for j in range(12)]
    result = polis_groups(VoteMatrix.from_rows(rows))
    assert result is not None
    assert result.k in (1, 2, 3, 4, 5)
    if result.k == 1:
        assert set(result.labels) == {0}


def _statements(rows):
    ids = sorted({r[1] for r in rows})
    return {s: {"text": f"statement {s}", "origin": "participant", "anchor_id": None} for s in ids}


def test_report_small_room():
    rows = [(f"p{i}", f"s{j}", 1, False) for i in range(4) for j in range(8)]
    report = room_report(rows, _statements(rows), BUNDLE, demo=False)
    assert report["groups"] is None and report["bridges"] is None
    assert any("Groups appear after 10" in n for n in report["notes"])


def test_report_empty_room():
    report = room_report([], {}, BUNDLE, demo=False)
    assert report["participants"] == 0 and report["groups"] is None


def test_synthetic_excluded_outside_demo():
    rows, _ = planted()
    marked = [(p, s, v, True) for p, s, v in rows]
    statements = _statements(rows)
    assert room_report(marked, statements, BUNDLE, demo=False)["participants"] == 0
    assert room_report(marked, statements, BUNDLE, demo=True)["participants"] == 60


def test_report_has_no_participant_ids():
    rows, _ = planted()
    report = room_report([(*r, False) for r in rows], _statements(rows), BUNDLE, demo=False)
    blob = json.dumps(report)
    assert "g0-00" not in blob and "g2-19" not in blob
    assert report["groups"]["k"] == 3
    assert any(b["statement"] == "s-bridge" for b in report["bridges"]["passed"])


def test_participant_view():
    rows, truth = planted()
    marked = [(*r, False) for r in rows]
    view = participant_view(marked, _statements(rows), BUNDLE, False, "g1-03")
    assert view["group"] in "ABC" and view["votes"] > 0


def test_demo_room_maps_groups_to_thinkers_and_labels_axis():
    extra = {"x-bridge": "bridge", "x-div": "divider"}
    rows, _ = synthetic_votes(BUNDLE, extra, n=120)
    statements = {
        a["id"]: {"text": a["text"], "origin": "anchor", "anchor_id": a["id"]}
        for a in BUNDLE["anchors"]
    }
    statements |= {s: {"text": s, "origin": "participant", "anchor_id": None} for s in extra}
    report = room_report([(*r, True) for r in rows], statements, BUNDLE, demo=True)
    assert report["groups"]["k"] >= 2
    assert all(g["thinkers"] for g in report["groups"]["list"])
    assert any(b["statement"] == "x-bridge" for b in report["bridges"]["passed"])
    assert report["bridges"]["axis"] is not None


@pytest.mark.parametrize("n", [8, 30])
def test_bridging_never_crashes_on_small_or_uniform(n):
    rows = [(f"p{i}", f"s{j}", 1) for i in range(n) for j in range(6)]
    fit = fit_bridging(VoteMatrix.from_rows(rows))
    assert fit is not None
    passed, near = bridges(fit)
    assert isinstance(passed, list) and isinstance(near, list)


def test_leaning_bridges_have_a_majority_on_each_side():
    rows, _ = planted()
    m = VoteMatrix.from_rows(rows)
    polis = polis_groups(m)
    fit = fit_bridging(m, polis.pc1 if polis else None)
    assert fit is not None
    passed, near = bridges(fit)
    for row in passed + near:
        assert min(row["agree_by_side"]) > 0.5
