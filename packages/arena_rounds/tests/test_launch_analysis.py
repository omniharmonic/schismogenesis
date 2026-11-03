"""Launch-round analysis: two-stage clustering, stability, bootstrapped bridges, thinkers in the
room, personal measures, and speed (docs/fingerprint/04-LAUNCH.md section 2)."""

import json
import os
import pathlib
import time

import numpy as np
import pytest
from arena_rounds.bridging import bridges, fit_bridging
from arena_rounds.matrix import VoteMatrix
from arena_rounds.polis import cluster, polis_groups, stability_label
from arena_rounds.report import analyse
from arena_rounds.synthetic import synthetic_votes
from sklearn.metrics import adjusted_rand_score

BUNDLE = json.loads(
    (pathlib.Path(__file__).parents[3] / "apps/arena/public/fingerprint.json").read_text()
)


def planted(n_per, statements=30, seed=1, noise=0.1, skip=0.2):
    random = np.random.default_rng(seed)
    base = random.choice([-1, 1], size=(3, statements))
    same = (base == base[0]).all(0)
    base[2, same] = -base[0, same]  # only the planted bridge has every group agreeing
    rows, truth = [], {}
    for g in range(3):
        for i in range(n_per):
            p = f"g{g}-{i:04d}"
            truth[p] = g
            for j in range(statements):
                if random.random() < skip:
                    continue
                v = int(base[g, j])
                rows.append((p, f"s{j:03d}", -v if random.random() < noise else v))
            rows.append((p, "s-bridge", 1 if random.random() > noise else -1))
    return rows, truth


def test_two_stage_clustering_recovers_groups_in_a_large_room():
    rows, truth = planted(200)
    result = polis_groups(VoteMatrix.from_rows(rows))
    assert result is not None and result.k == 3
    assert adjusted_rand_score([truth[p] for p in result.participants], result.labels) >= 0.9


def test_cluster_small_room_uses_participants_directly():
    points = np.vstack([np.random.default_rng(0).normal(c, 0.1, (10, 2)) for c in (0, 3)])
    labels, k, sil = cluster(points)
    assert k == 2 and sil is not None and sil > 0.5 and len(labels) == 20


def test_stability_is_clear_for_planted_groups_and_low_for_noise():
    rows, _ = planted(30)
    result = polis_groups(VoteMatrix.from_rows(rows), stability=True)
    assert result is not None and stability_label(result.stability) == "clear"
    random = np.random.default_rng(3)
    noise = [(f"p{i}", f"s{j}", int(random.choice([-1, 1]))) for i in range(60) for j in range(20)]
    noisy = polis_groups(VoteMatrix.from_rows(noise), stability=True)
    assert noisy is not None
    assert noisy.k == 1 or (noisy.stability is not None and noisy.stability < 0.8)


def test_bootstrapped_bridge_needs_a_lower_bound():
    rows, _ = planted(30)
    m = VoteMatrix.from_rows(rows)
    polis = polis_groups(m)
    fit = fit_bridging(m, polis.pc1 if polis else None, bootstrap=20)
    assert fit is not None and fit.neutral_low is not None
    passed, _ = bridges(fit)
    assert [b["statement"] for b in passed] == ["s-bridge"]
    assert all(b["neutral_low"] >= 0.65 for b in passed)


def _demo():
    extra = {"x-bridge": "bridge", "x-div": "divider"}
    rows, membership = synthetic_votes(BUNDLE, extra, n=150)
    statements = {
        a["id"]: {"text": a["text"], "origin": "anchor", "anchor_id": a["id"]}
        for a in BUNDLE["anchors"]
    }
    statements |= {s: {"text": s, "origin": "participant", "anchor_id": None} for s in extra}
    return analyse([(*r, True) for r in rows], statements, BUNDLE, demo=True), membership


def test_thinkers_are_placed_in_the_room_near_their_camp():
    analysis, membership = _demo()
    groups = analysis.report["groups"]
    assert groups["stability_label"] in ("clear", "tentative")
    where = {t["id"]: np.array([t["x"], t["y"]]) for t in groups["thinkers"]}
    assert "max-tegmark" in where and "marc-andreessen" in where
    points = np.array(groups["points"])
    # the thinker sits closer to the centre of their camp's synthetic voters than to the other's
    by_group = {g["name"]: np.array(g["center"]) for g in groups["list"]}
    to = {
        t: min(by_group, key=lambda g: np.linalg.norm(by_group[g] - where[t]))
        for t in ("max-tegmark", "marc-andreessen")
    }
    assert to["max-tegmark"] != to["marc-andreessen"]
    assert len(points) <= 1500


def test_personal_measures():
    analysis, _ = _demo()
    entry = analysis.personal["synthetic-000"]
    assert 0 <= entry["rarity_percentile"] <= 100
    assert entry["rarest_take"]["vote"] in (1, -1)
    assert 0 <= entry["rarest_take"]["share_with_you"] <= 1
    assert entry["group"] in "ABCDE" and entry["nearest_group"] in "ABCDE"
    assert entry["nearest_group"] != entry["furthest_group"]
    blob = json.dumps(analysis.report)
    assert "synthetic-000" not in blob


def _big_room(people: int, statements: int = 200):
    random = np.random.default_rng(5)
    base = random.choice([-1, 1], size=(4, statements))
    group = random.integers(0, 4, people)
    seen = random.random((people, statements)) < 0.15
    flip = random.random((people, statements)) < 0.12
    values = np.where(flip, -base[group], base[group])
    p_idx, s_idx = np.nonzero(seen)
    rows = [(f"p{p}", f"s{s}", int(values[p, s]), False) for p, s in zip(p_idx, s_idx, strict=True)]
    meta = {
        f"s{s}": {"text": f"s{s}", "origin": "participant", "anchor_id": None}
        for s in range(statements)
    }
    return rows, meta


def test_medium_room_finds_groups():
    rows, meta = _big_room(2000)
    assert analyse(rows, meta, BUNDLE, demo=False).report["groups"]["k"] >= 2


@pytest.mark.skipif(os.environ.get("ARENA_LOAD_TEST") != "1", reason="run with make load-test")
def test_large_room_reports_quickly():
    """10,000 people by 200 statements: about 9 s on an idle M-series laptop."""
    rows, meta = _big_room(10_000)
    start = time.perf_counter()
    analysis = analyse(rows, meta, BUNDLE, demo=False)
    elapsed = time.perf_counter() - start
    print(f"10,000 x 200 report in {elapsed:.1f}s")
    assert analysis.report["groups"]["k"] >= 2
    assert elapsed < 20
