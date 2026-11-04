"""Draw the schools and choose the survey's statements from the audited stances (D-31.20).

Usage: draw_schools.py <stances.json> <pool.json> <out.json> [--size N] [--report out.md]

1. Every voice read well enough (MIN_CLUSTER stances on the pool) is grouped by agreement over the
   statements both took a side on (silence is never a view), average linkage, with the number of
   schools chosen by separation and by survival when the statements are resampled.
2. Voices read less well are attached to a school only on clear evidence, shown between two, or
   left ungrouped (`attach`).
3. Everyone is laid out by weighted MDS on the same agreement, so a dot's place and its school come
   from one measure (a dot can no longer sit inside a school it doesn't belong to by accident).
4. The survey's statements are chosen greedily: statements that split the voices, separate the
   schools and add voices not yet covered, with near-duplicates kept out and the three sets
   balanced. Instrument sizes are compared by how well each voice's own answers find their school.
"""

import json
import pathlib
import sys
from collections import Counter

import numpy as np
from arena_fingerprint.instrument import (
    Table,
    correlation_matrix,
    dimensions,
    distances,
    draw_schools,
    pair_agreement,
    phi,
    recovery,
    redundancy,
    smacof,
    stability,
    statement_stats,
)
from scipy.stats import spearmanr

MIN_CLUSTER = 12  # stances on the pool to help draw the schools
MIN_PLACE = 5  # stances to be placed on the map at all
ATTACH_LEAD = 0.05  # agreement lead over the runner-up school needed to attach
ATTACH_FLOOR = 0.6  # mean agreement with the school's members needed to attach
ATTACH_SHARED = 8  # statements shared with the school's members, in all
MAX_PHI = 0.75  # shrunk |phi| above this: near-duplicates (|phi| 1 needs 30 shared voices)
MIN_MINORITY = 0.1  # the smaller side must hold at least this share
MIN_SIDE = 3  # and at least this many figures: both sides on the record
MIN_TAKEN = 7  # voices with a side
FORECAST_WEIGHT = 0.5
LAYOUT_PULL = 0.35  # see the layout step; 0.35 left 2 foreign dots in regions vs 13 at 0


def load(stances_path: str, pool_path: str) -> tuple[Table, list[dict]]:
    stances = json.loads(pathlib.Path(stances_path).read_text())["stances"]
    pool = json.loads(pathlib.Path(pool_path).read_text())["statements"]
    ids = {s["id"] for s in pool}
    table: Table = {}
    for sid, entry in stances.items():
        if sid in ids:
            for pid, v in entry.items():
                table.setdefault(pid, {})[sid] = v["a"]
    return table, pool


def weights(pool: list[dict], table: Table | None = None) -> dict[str, float]:
    """Forecasts count half. With the table, each statement is also divided by how much it
    overlaps the others (sum of |correlation|), so one axis asked many ways (extinction risk,
    pausing, control...) gets about one vote, and social-contract statements aren't drowned out."""
    base = {s["id"]: FORECAST_WEIGHT if s.get("layer") == "empirical" else 1.0 for s in pool}
    if table is None:
        return base
    ids = [s["id"] for s in pool]
    overlap = np.abs(correlation_matrix(table, ids)).sum(1)
    scale = len(ids) / float((1 / overlap).sum())
    return {s: base[s] * scale / float(overlap[i]) for i, s in enumerate(ids)}


def attach(
    person: str, table: Table, groups: list[list[str]], weight: dict[str, float]
) -> tuple[int | None, list[int], list[float]]:
    scores = []
    for g in groups:
        rows = [pair_agreement(table[person], table[m], weight) for m in g]
        rows = [(a, k) for a, k in rows if k >= 2]
        shared = sum(k for _, k in rows)
        mean = sum(a * k for a, k in rows) / shared if shared else 0.5
        scores.append((mean, shared))
    order = sorted(range(len(groups)), key=lambda n: -scores[n][0])
    best, second = order[0], order[1]
    means = [round(s[0], 3) for s in scores]
    if scores[best][0] < ATTACH_FLOOR or scores[best][1] < ATTACH_SHARED:
        return None, [], means
    if scores[best][0] - scores[second][0] < ATTACH_LEAD:
        if scores[second][0] >= ATTACH_FLOOR:
            return None, [best, second], means
        return None, [], means
    return best, [], means


def shrunk_phi(table: Table, s: str, t: str) -> float:
    """|phi| discounted when few voices took a side on both: 14 voices agreeing is a hint of
    overlap, not proof that two statements ask the same thing."""
    r, n = phi(table, s, t)
    return abs(r) * n / (n + 10)


def eta(table: Table, statement: str, school_of: dict[str, int]) -> float:
    """How much of the split on a statement lines up with the schools (0 none, 1 all)."""
    rows = [(school_of[p], table[p][statement]) for p in school_of if statement in table[p]]
    if len(rows) < 4:
        return 0.0
    values = np.array([v for _, v in rows], float)
    total = ((values - values.mean()) ** 2).sum()
    if total == 0:
        return 0.0
    within = 0.0
    for g in {s for s, _ in rows}:
        x = np.array([v for s, v in rows if s == g], float)
        within += ((x - x.mean()) ** 2).sum()
    return float(1 - within / total)


def choose(
    table: Table, pool: list[dict], school_of: dict[str, int], size: int
) -> tuple[list[str], list[str]]:
    stats = statement_stats(table, [s["id"] for s in pool])
    sets = {s["id"]: s["set"] for s in pool}
    usable = [
        s["id"]
        for s in pool
        if stats[s["id"]]["n"] >= MIN_TAKEN
        and stats[s["id"]]["minority"] >= MIN_MINORITY
        and min(stats[s["id"]]["hold"], stats[s["id"]]["reject"]) >= MIN_SIDE
    ]
    log = [
        f"left out (too few sides or one-sided): {s['id']} {stats[s['id']]}"
        for s in pool
        if s["id"] not in usable
    ]
    power = {s: eta(table, s, school_of) for s in usable}
    cap = {k: -(-size // 3) for k in ("being", "values", "action")}
    chosen: list[str] = []
    cover: Counter[str] = Counter()
    while len(chosen) < size:
        best = None
        for s in usable:
            if s in chosen or Counter(sets[c] for c in chosen)[sets[s]] >= cap[sets[s]]:
                continue
            alike = [shrunk_phi(table, s, c) for c in chosen]
            if alike and max(alike) > MAX_PHI:
                continue
            gain = sum(1 for p in table if s in table[p] and cover[p] < 8) / len(table)
            merit = power[s] + 0.5 * gain + 0.2 * stats[s]["minority"] - 0.3 * max(alike or [0])
            if best is None or merit > best[0]:
                best = (merit, s)
        if best is None:
            log.append(f"stopped at {len(chosen)}: no statement left within the rules")
            break
        chosen.append(best[1])
        cover.update(p for p in table if best[1] in table[p])
    order = {"being": 0, "values": 1, "action": 2}
    chosen.sort(key=lambda s: (order[sets[s]], [x["id"] for x in pool].index(s)))
    return chosen, log


def main(stances_path: str, pool_path: str, out: str, *options: str) -> None:
    size = int(options[options.index("--size") + 1]) if "--size" in options else 30
    min_cluster = (
        int(options[options.index("--min-cluster") + 1])
        if "--min-cluster" in options
        else MIN_CLUSTER
    )
    table, pool = load(stances_path, pool_path)
    weight = weights(pool, table)
    ids = [s["id"] for s in pool]
    counts = {p: len(v) for p, v in table.items()}
    core = sorted(p for p, n in counts.items() if n >= min_cluster)
    drawing = draw_schools(table, core, ids, weight=weight, runs=100)
    groups = [
        [p for p, lab in zip(core, drawing.labels, strict=True) if lab == g]
        for g in sorted(set(drawing.labels))
    ]
    groups.sort(key=len, reverse=True)
    school_of = {p: n for n, g in enumerate(groups) for p in g}
    _, together = stability(
        table, core, ids, drawing.count, [school_of[p] for p in core], runs=300, weight=weight
    )
    people: dict[str, dict] = {}
    for p in core:
        people[p] = {"school": school_of[p], "between": [], "basis": "drew the schools"}
    for p in sorted(set(table) - set(core)):
        if counts[p] < MIN_PLACE:
            continue
        school, between, means = attach(p, table, groups, weight)
        people[p] = {
            "school": school,
            "between": between,
            "fit": means,
            "basis": "attached"
            if school is not None
            else "between"
            if between
            else "not yet grouped",
        }
    placed = sorted(people)
    d, shared = distances(table, placed, ids, weight)
    # the flat map can't show five axes: pull schoolmates a little together (and push other
    # schools a little apart) so a dot rarely sits in a region it doesn't belong to
    school_at = [people[p]["school"] for p in placed]
    laid = d.copy()
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            if school_at[i] is not None and school_at[j] is not None:
                f = 1 - LAYOUT_PULL if school_at[i] == school_at[j] else 1 + LAYOUT_PULL / 2
                laid[i, j] = laid[j, i] = d[i, j] * f
    xy = smacof(laid, np.minimum(shared, 20) / 20 + 1e-3)
    gaps = np.sqrt(((xy[:, None] - xy[None]) ** 2).sum(-1))
    upper = np.triu_indices(len(placed), 1)
    layout_fidelity = float(spearmanr(gaps[upper], d[upper])[0])  # pyright: ignore[reportArgumentType]
    xy = xy / max(float(np.percentile(np.abs(xy), 92)), 1e-9) * 190
    for p, (x, y) in zip(placed, xy, strict=True):
        people[p].update({"x": round(float(x), 1), "y": round(float(y), 1), "stances": counts[p]})

    # distinctive positions: where a school leans furthest from everyone
    overall = {s: np.mean([table[p][s] for p in core if s in table[p]] or [0]) for s in ids}
    schools = []
    for n, g in enumerate(groups):
        lean = []
        for s in ids:
            votes = [table[p][s] for p in g if s in table[p]]
            if len(votes) >= max(2, len(g) // 3):
                mean = float(np.mean(votes))
                lean.append(
                    {
                        "statement": s,
                        "side": 1 if mean > 0 else -1,
                        "mean": round(mean, 2),
                        "lean": round(mean - overall[s], 2),
                        "n": len(votes),
                    }
                )
        lean.sort(key=lambda r: -abs(r["lean"]))
        pairs = [together[core.index(a), core.index(b)] for a in g for b in g if a < b]
        schools.append(
            {
                "id": n,
                "members": g,
                "attached": sorted(
                    p for p, v in people.items() if v["school"] == n and v["basis"] == "attached"
                ),
                "cohesion": round(float(np.mean(pairs)), 3) if pairs else None,
                "distinctive": lean[:8],
            }
        )

    grouped = {p: v["school"] for p, v in people.items() if v["school"] is not None}
    sizes = {}
    for k in sorted({24, 27, 30, 33, 36, size}):
        chosen_k, _ = choose(table, pool, school_of, k)
        sizes[k] = {
            **recovery(table, chosen_k, grouped),
            "statements": len(chosen_k),
        }
    chosen, log = choose(table, pool, school_of, size)
    season1 = [s["id"] for s in pool if s.get("origin") == "season-1"]
    checks = {
        "voices_with_stances": len(table),
        "drew_schools": len(core),
        "placed": len(placed),
        "attached": sum(1 for v in people.values() if v["basis"] == "attached"),
        "between": sum(1 for v in people.values() if v["basis"] == "between"),
        "not_yet_grouped": sum(1 for v in people.values() if v["basis"] == "not yet grouped"),
        "weights": {k: round(v, 3) for k, v in sorted(weight.items())},
        "layout_rank_fidelity": round(layout_fidelity, 3),
        "schools": drawing.count,
        "silhouette": drawing.silhouette,
        "stability": drawing.stability,
        "by_count": drawing.by_count,
        "dimensions_pool": dimensions(table, ids, runs=100),
        "dimensions_instrument": dimensions(table, chosen, runs=100),
        "dimensions_season1": dimensions(table, season1, runs=100),
        "recovery_pool": recovery(table, ids, grouped),
        "recovery_season1": recovery(table, season1, grouped),
        "recovery_by_size": sizes,
        "near_duplicates": [
            r for r in redundancy(table, ids) if abs(r["phi"]) * r["n"] / (r["n"] + 10) > MAX_PHI
        ],
    }
    pathlib.Path(out).write_text(
        json.dumps(
            {
                "pool": ids,
                "instrument": chosen,
                "schools": schools,
                "people": people,
                "together": {
                    f"{a}|{b}": round(float(together[i, j]), 3)
                    for i, a in enumerate(core)
                    for j, b in enumerate(core)
                    if i < j
                },
                "statements": {
                    s: {**v, "eta": round(eta(table, s, school_of), 3)}
                    for s, v in statement_stats(table, ids).items()
                },
                "checks": checks,
                "log": log,
            },
            indent=1,
            ensure_ascii=False,
        )
    )
    print(json.dumps({k: v for k, v in checks.items() if k != "near_duplicates"}, indent=1))
    print("near duplicates:", checks["near_duplicates"][:12])
    for s in schools:
        print(f"\nSCHOOL {s['id']} cohesion {s['cohesion']}: {s['members']} + {s['attached']}")
        for r in s["distinctive"][:5]:
            sign = "+" if r["side"] > 0 else "-"
            print(f"   {sign} {r['statement']} (lean {r['lean']}, n {r['n']})")
    for p, v in sorted(people.items()):
        if v["basis"] in ("between", "not yet grouped"):
            print(f"  {v['basis']}: {p} {v.get('between')} fit {v.get('fit')} ({v['stances']})")
    print("\ninstrument:", chosen)
    for line in log:
        print(" ", line)


if __name__ == "__main__":
    main(*sys.argv[1:])
