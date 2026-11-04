import numpy as np
from arena_fingerprint.instrument import (
    dimensions,
    distances,
    draw_schools,
    recovery,
    redundancy,
    smacof,
    statement_stats,
)

STATEMENTS = [f"s{i}" for i in range(24)]


def planted(seed: int = 1, silent: float = 0.25):
    """Three schools on two independent axes, with silence and a little noise."""
    rng = np.random.default_rng(seed)
    profiles = {
        "a": [1] * 12 + [1] * 12,
        "b": [-1] * 12 + [1] * 12,
        "c": [-1] * 12 + [-1] * 12,
    }
    table, truth = {}, {}
    for school, profile in profiles.items():
        for k in range(8):
            person = f"{school}{k}"
            truth[person] = school
            row = {}
            for s, v in zip(STATEMENTS, profile, strict=True):
                if rng.random() < silent:
                    continue
                row[s] = v if rng.random() > 0.05 else -v
            table[person] = row
    return table, truth


def test_silence_is_not_agreement():
    table = {"x": {"s0": 1}, "y": {"s1": 1}, "z": {"s0": 1, "s1": 1}}
    d, shared = distances(table, ["x", "y", "z"], ["s0", "s1"])
    assert shared[0, 1] == 0 and d[0, 1] == 0.5  # nothing shared: unknown, not alike
    assert d[0, 2] < 0.5


def test_draw_recovers_planted_schools_and_is_stable():
    table, truth = planted()
    people = sorted(table)
    drawing = draw_schools(table, people, STATEMENTS, counts=range(2, 6), runs=40)
    assert drawing.count == 3
    groups = {}
    for p, label in zip(people, drawing.labels, strict=True):
        groups.setdefault(label, set()).add(truth[p])
    assert all(len(v) == 1 for v in groups.values())
    assert drawing.stability > 0.8


def test_redundancy_and_dimensions():
    table, _ = planted()
    for row in table.values():  # dup duplicates s0
        if "s0" in row:
            row["dup"] = row["s0"]
    pairs = redundancy(table, [*STATEMENTS, "dup"])
    dup = next(p for p in pairs if {p["a"], p["b"]} == {"s0", "dup"})
    assert dup["phi"] == 1.0 and abs(pairs[0]["phi"]) >= abs(pairs[-1]["phi"])
    dims = dimensions(table, STATEMENTS, runs=40)
    assert dims["axes_beyond_chance"] >= 1
    stats = statement_stats(table, STATEMENTS)
    assert all(v["minority"] > 0.15 for v in stats.values())


def test_recovery_and_layout():
    table, truth = planted()
    school = {p: "abc".index(s) for p, s in truth.items()}
    result = recovery(table, STATEMENTS, school)
    assert result["top1"] > 0.9
    people = sorted(table)
    d, shared = distances(table, people, STATEMENTS)
    x = smacof(d, shared)
    centre = {s: x[[i for i, p in enumerate(people) if truth[p] == s]].mean(0) for s in "abc"}
    assert np.linalg.norm(centre["a"] - centre["c"]) > np.linalg.norm(centre["a"] - centre["b"])
