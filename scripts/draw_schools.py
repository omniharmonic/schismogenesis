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
    Node,
    Table,
    consensus,
    correlation_matrix,
    dimensions,
    distances,
    hierarchy,
    pair_agreement,
    phi,
    recovery,
    redundancy,
    smacof,
    statement_stats,
)
from scipy.stats import spearmanr

MIN_CLUSTER = 10  # positions (pool statements plus atlas ideas) to help draw the groups
MIN_IDEA_HOLDERS = 4  # an atlas idea counts as evidence when this many people take a side
LEVELS = (0.25, 0.42, 0.6, 0.78)  # camp, school, branch, tight cluster: share of redrawings
LEVEL_NAMES = ("camp", "school", "branch", "cluster")  # in which a pair lands together
CONSENSUS_RUNS = 300
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
    means = [round(sc[0], 3) for sc in scores]
    best = order[0]
    if len(groups) == 1:  # a single subgroup: join it only on clear agreement
        ok = scores[best][0] >= ATTACH_FLOOR + ATTACH_LEAD and scores[best][1] >= ATTACH_SHARED
        return (best if ok else None), [], means
    second = order[1]
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
    table: Table, pool: list[dict], levels: list[dict[str, int]], size: int
) -> tuple[list[str], list[str]]:
    """`levels`: group membership at each level of the tree (camps, then the finest groups)."""
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
    # a statement earns its place by separating groups at every level, not only the finest
    power = {s: float(np.mean([eta(table, s, lv) for lv in levels])) for s in usable}
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


def augment(table: Table, atlas_path: str | None) -> tuple[Table, list[dict]]:
    """Clustering evidence beyond the survey pool: every idea in the audited atlas that at least
    MIN_IDEA_HOLDERS people hold or reject in their own words, with both sides present. The
    survey itself is chosen from the pool alone."""
    full: Table = {p: dict(v) for p, v in table.items()}
    extra: list[dict] = []
    if not atlas_path:
        return full, extra
    seen = {s for row in table.values() for s in row}
    for idea in json.loads(pathlib.Path(atlas_path).read_text())["ideas"]:
        if idea["id"] in seen:
            continue
        held = {h["p"]: (1 if h["a"] > 0 else -1) for h in idea["holders"] if not h["inf"]}
        if len(held) >= MIN_IDEA_HOLDERS and len(set(held.values())) == 2:
            extra.append({"id": idea["id"], "layer": idea["layer"], "set": "atlas"})
            for p, a in held.items():
                full.setdefault(p, {})[idea["id"]] = a
    return full, extra


def lean(table: Table, group: list[str], base: list[str], ids: list[str]) -> list[dict]:
    """Where a group leans furthest from the people around it (its parent group, or everyone)."""
    rows = []
    for s in ids:
        votes = [table[p][s] for p in group if s in table[p]]
        around = [table[p][s] for p in base if s in table[p]]
        if len(votes) >= max(2, len(group) // 3) and around:
            mean = float(np.mean(votes))
            rows.append(
                {
                    "statement": s,
                    "side": 1 if mean > 0 else -1,
                    "mean": round(mean, 2),
                    "lean": round(mean - float(np.mean(around)), 2),
                    "n": len(votes),
                }
            )
    # furthest from the people around it first; then what the group holds most firmly
    return sorted(rows, key=lambda r: (-abs(r["lean"]), -abs(r["mean"]), -r["n"]))[:8]


def main(stances_path: str, pool_path: str, out: str, *options: str) -> None:
    size = int(options[options.index("--size") + 1]) if "--size" in options else 30
    atlas_path = options[options.index("--atlas") + 1] if "--atlas" in options else None
    table, pool = load(stances_path, pool_path)
    ids = [s["id"] for s in pool]
    full, extra = augment(table, atlas_path)
    full_ids = ids + [x["id"] for x in extra]
    weight = weights(pool + extra, full)
    counts = {p: len(v) for p, v in table.items()}
    evidence = {p: len(v) for p, v in full.items()}
    core = sorted(
        p for p, n in evidence.items() if n >= MIN_CLUSTER and counts.get(p, 0) >= MIN_PLACE
    )
    together = consensus(full, core, full_ids, weight, runs=CONSENSUS_RUNS)
    camps = hierarchy(together, core, levels=LEVELS)

    nodes: dict[str, Node] = {}
    path: dict[str, list[str]] = {p: [] for p in core}

    def walk(level_nodes: list[Node]) -> None:
        for node in level_nodes:
            nodes[node.id] = node
            for m in node.members:
                path[m].append(node.id)
            walk(node.children)

    walk(camps)
    people: dict[str, dict] = {}
    for p in core:
        people[p] = {
            "path": path[p],
            "between": [],
            "basis": "drew the schools" if path[p] else "not yet grouped",
        }
    # everyone else goes down the tree as far as the evidence clearly points
    for p in sorted(set(table) - set(core)):
        if counts[p] < MIN_PLACE:
            continue
        level, route, between = camps, [], []
        while level:
            choice, close, _ = attach(p, full, [n.members for n in level], weight)
            if choice is None:
                between = [level[i].id for i in close]
                break
            route.append(level[choice].id)
            level = level[choice].children
        people[p] = {
            "path": route,
            "between": between,
            "basis": "attached" if route else "between" if between else "not yet grouped",
        }
    camp_index = {c.id: n for n, c in enumerate(camps)}
    for v in people.values():
        v["school"] = camp_index[v["path"][0]] if v["path"] else None
        v["between_camps"] = [camp_index[b] for b in v["between"] if b in camp_index]

    placed = sorted(people)
    d, shared = distances(full, placed, full_ids, weight)
    # the flat map can't show many axes: pull members of the same camp together, more so the
    # deeper the group they share, and push camps a little apart
    routes = [people[p]["path"] for p in placed]
    laid = d.copy()
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            a, b = routes[i], routes[j]
            if not a or not b:
                continue
            depth = sum(1 for x, y in zip(a, b, strict=False) if x == y)
            f = 1 - LAYOUT_PULL - 0.1 * max(depth - 1, 0) if depth else 1 + LAYOUT_PULL / 2
            laid[i, j] = laid[j, i] = d[i, j] * f
    xy = smacof(laid, np.minimum(shared, 20) / 20 + 1e-3)
    gaps = np.sqrt(((xy[:, None] - xy[None]) ** 2).sum(-1))
    upper = np.triu_indices(len(placed), 1)
    layout_fidelity = float(spearmanr(gaps[upper], d[upper])[0])  # pyright: ignore[reportArgumentType]
    xy = xy / max(float(np.percentile(np.abs(xy), 92)), 1e-9) * 190
    for p, (x, y) in zip(placed, xy, strict=True):
        people[p].update({"x": round(float(x), 1), "y": round(float(y), 1), "stances": counts[p]})

    def node_out(node: Node, parent: list[str]) -> dict:
        attached = sorted(
            p for p, v in people.items() if v["basis"] == "attached" and node.id in v["path"]
        )
        return {
            "id": node.id,
            "level": node.level,
            "members": node.members,
            "attached": attached,
            "cohesion": node.cohesion,
            "distinctive": lean(table, node.members, parent, ids),
            "children": [node_out(c, node.members) for c in node.children],
        }

    tree = [node_out(c, core) for c in camps]
    schools = [
        {
            "id": n,
            "node": t["id"],
            "members": t["members"],
            "attached": t["attached"],
            "cohesion": t["cohesion"],
            "distinctive": t["distinctive"],
        }
        for n, t in enumerate(tree)
    ]

    # the survey should separate groups at the finest level the data supports
    finest = {p: v["path"][-1] for p, v in people.items() if v["path"] and p in core}
    finest_index = {nid: n for n, nid in enumerate(sorted(set(finest.values())))}
    school_of = {p: finest_index[nid] for p, nid in finest.items()}
    camp_level = {
        p: v["school"] for p, v in people.items() if v["school"] is not None and p in core
    }
    levels_of = [camp_level, school_of]
    by_level = {}
    for level, name in enumerate(LEVEL_NAMES):
        grouped = {p: v["path"][level] for p, v in people.items() if len(v["path"]) > level}
        by_level[name] = {
            "groups": sum(1 for n in nodes.values() if n.level == level),
            "cohesion": round(
                float(np.mean([n.cohesion for n in nodes.values() if n.level == level] or [0])), 3
            ),
            "people": len(grouped),
        }
    sizes = {}
    chosen, log = choose(table, pool, levels_of, size)
    for k in sorted({24, 27, 30, 33, size}):
        chosen_k, _ = choose(table, pool, levels_of, k)
        sizes[k] = {
            lvl: recovery(
                table, chosen_k, {p: v["path"][n] for p, v in people.items() if len(v["path"]) > n}
            )
            for n, lvl in enumerate(("camp", "school"))
        }
    season1 = [s["id"] for s in pool if s.get("origin") == "season-1"]
    camp_of = {p: v["path"][0] for p, v in people.items() if v["path"]}
    school_level = {p: v["path"][1] for p, v in people.items() if len(v["path"]) > 1}
    checks = {
        "voices_with_stances": len(table),
        "evidence_statements": len(full_ids),
        "atlas_ideas_added": len(extra),
        "drew_schools": len(core),
        "placed": len(placed),
        "attached": sum(1 for v in people.values() if v["basis"] == "attached"),
        "between": sum(1 for v in people.values() if v["basis"] == "between"),
        "not_yet_grouped": sum(1 for v in people.values() if v["basis"] == "not yet grouped"),
        "levels": dict(zip(LEVEL_NAMES, LEVELS, strict=True)),
        "by_level": by_level,
        "schools": len(camps),
        "silhouette": by_level["camp"]["cohesion"],
        "by_count": {},
        "layout_rank_fidelity": round(layout_fidelity, 3),
        "weights": {k: round(v, 3) for k, v in sorted(weight.items()) if k in set(ids)},
        "dimensions_pool": dimensions(table, ids, runs=100),
        "dimensions_instrument": dimensions(table, chosen, runs=100),
        "dimensions_season1": dimensions(table, season1, runs=100),
        "recovery_instrument": {
            "camp": recovery(table, chosen, camp_of),
            "school": recovery(table, chosen, school_level),
        },
        "recovery_season1": {
            "camp": recovery(table, season1, camp_of),
            "school": recovery(table, season1, school_level),
        },
        "recovery_by_size": sizes,
        "near_duplicates": [
            r for r in redundancy(table, ids) if abs(r["phi"]) * r["n"] / (r["n"] + 10) > MAX_PHI
        ],
    }
    doc = {
        "pool": ids,
        "instrument": chosen,
        "tree": tree,
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
    }
    pathlib.Path(out).write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    print(
        json.dumps(
            {k: v for k, v in checks.items() if k not in ("near_duplicates", "weights")}, indent=1
        )
    )

    def show(node: dict, depth: int = 0) -> None:
        tops = ", ".join(
            f"{'+' if r['side'] > 0 else '-'}{r['statement']}" for r in node["distinctive"][:4]
        )
        print(
            "  " * depth + f"{node['id']} ({node['cohesion']}) {node['members']}"
            f" + {node['attached']}\n" + "  " * depth + f"   {tops}"
        )
        for c in node["children"]:
            show(c, depth + 1)

    for t in tree:
        show(t)
    for p, v in sorted(people.items()):
        if v["basis"] in ("between", "not yet grouped"):
            print(f"  {v['basis']}: {p} {v['between']} ({v['stances']})")
    print("\ninstrument:", chosen)
    for line in log:
        print(" ", line)


if __name__ == "__main__":
    main(*sys.argv[1:])
