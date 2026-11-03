"""The room report: groups, bridges, common ground, splits, and how groups map to thinkers.

Every section has a minimum-data rule. Below it the report says what is missing instead of
guessing (docs/fingerprint/02-ARCHITECTURE.md section 6). The public report holds aggregates only.
"""

import itertools

import numpy as np
from arena_fingerprint.agreement import ranked

from arena_rounds.bridging import bridges, fit_bridging
from arena_rounds.matrix import VoteMatrix
from arena_rounds.polis import consensus, divisive, group_stats, polis_groups, representative

MIN_GROUP_PEOPLE = 10
MIN_BRIDGE_PEOPLE = 8
MIN_DESCRIBED = 3
AXIS_MIN_R = 0.4
GROUP_NAMES = "ABCDE"


def _group_thinkers(stats: dict, anchor_of: dict[str, str], stances: dict) -> list[dict]:
    answers = {}
    for statement, s in stats.items():
        anchor = anchor_of.get(statement)
        if anchor and s.seen:
            answers[anchor] = 1 if s.pa > s.pd + 0.1 else (-1 if s.pd > s.pa + 0.1 else 0)
    return [
        {"id": t, "k": k, "n": n, "s": round(sc, 3)} for t, k, n, sc in ranked(answers, stances)[:3]
    ]


def _axis_label(fit, m: VoteMatrix, anchor_of: dict[str, str], bundle: dict) -> dict | None:
    """Correlate the bridging factor with camp-affinity differences on anchor votes."""
    stances = {a: {t: v["a"] for t, v in e.items()} for a, e in bundle["stances"].items()}
    index = {p: i for i, p in enumerate(m.participants)}
    col = {s: j for j, s in enumerate(m.statements)}
    affinity: dict[str, list[float]] = {c["id"]: [] for c in bundle["camps"]}
    for participant in fit.participants:
        row = m.values[index[participant]]
        for camp in bundle["camps"]:
            agree = total = 0
            for statement, anchor in anchor_of.items():
                if (
                    statement not in col
                    or np.isnan(row[col[statement]])
                    or row[col[statement]] == 0
                ):
                    continue
                side = sum(stances[anchor].get(x, 0) for x in camp["members"])
                if side:
                    total += 1
                    agree += int(np.sign(side) == row[col[statement]])
            affinity[camp["id"]].append((agree + 1) / (total + 2))
    best = None
    labels = {c["id"]: c["label"] for c in bundle["camps"]}
    for a, b in itertools.combinations(sorted(affinity), 2):
        diff = np.array(affinity[a]) - np.array(affinity[b])
        if diff.std() == 0 or fit.f_u.std() == 0:
            continue
        r = float(np.corrcoef(fit.f_u, diff)[0, 1])
        if best is None or abs(r) > abs(best["r"]):
            best = {
                "negative": labels[b if r > 0 else a],
                "positive": labels[a if r > 0 else b],
                "r": round(abs(r), 3),
            }
    return best if best and best["r"] >= AXIS_MIN_R else None


def room_report(
    rows: list[tuple[str, str, int, bool]],
    statements: dict[str, dict],
    bundle: dict,
    demo: bool,
) -> dict:
    """Build the public report.

    rows: (participant, statement, vote, is_synthetic).
    statements: id -> {text, origin, anchor_id}.
    """
    used = [(p, s, v) for p, s, v, synthetic in rows if demo or not synthetic]
    used = [r for r in used if r[1] in statements]
    m = VoteMatrix.from_rows(used) if used else VoteMatrix([], [], np.zeros((0, 0)))
    active = int((m.votes_per_participant() >= 7).sum()) if used else 0
    anchor_of = {sid: s["anchor_id"] for sid, s in statements.items() if s.get("anchor_id")}
    stances = {a: {t: v["a"] for t, v in e.items()} for a, e in bundle["stances"].items()}
    text = {sid: s["text"] for sid, s in statements.items()}

    def named(items: list[dict]) -> list[dict]:
        return [
            {**i, "text": text[i["statement"]], "origin": statements[i["statement"]]["origin"]}
            for i in items
        ]

    report: dict = {
        "participants": len(m.participants),
        "active": active,
        "votes": len(used),
        "statements": len(statements),
        "demo": demo,
        "groups": None,
        "bridges": None,
        "notes": [],
    }

    polis = polis_groups(m) if used else None
    if polis is None or active < MIN_GROUP_PEOPLE:
        report["notes"].append(
            f"Groups appear after {MIN_GROUP_PEOPLE} people have cast 7 or more votes "
            f"(now {active})."
        )
    else:
        members = {
            g: [p for p, lab in zip(polis.participants, polis.labels, strict=True) if lab == g]
            for g in range(polis.k)
        }
        stats = group_stats(m, members)
        reps = representative(m, members)
        groups = []
        for g, people in members.items():
            described = len(people) >= MIN_DESCRIBED
            groups.append(
                {
                    "name": GROUP_NAMES[g],
                    "size": len(people),
                    "center": [
                        round(float(x), 3) for x in polis.projection[polis.labels == g].mean(0)
                    ],
                    "representative": named(reps[g]) if described else [],
                    "thinkers": _group_thinkers(stats[g], anchor_of, stances) if described else [],
                }
            )
        report["groups"] = {
            "k": polis.k,
            "silhouette": None if polis.silhouette is None else round(polis.silhouette, 3),
            "clear": polis.k > 1,
            "list": groups,
            "points": [
                [round(float(x), 3), round(float(y), 3), int(lab)]
                for (x, y), lab in zip(polis.projection, polis.labels, strict=True)
            ],
            "consensus": named([c for c in consensus(stats) if c["all_agree"]][:5])
            if polis.k > 1
            else [],
            "divisive": named(divisive(stats)[:5]) if polis.k > 1 else [],
        }
        if polis.k == 1:
            report["notes"].append("No clear groups yet: the room's votes don't separate.")

    fit = None
    if used:
        fit = fit_bridging(m, init=polis.pc1 if polis else None)
    if fit is None or len(fit.participants) < MIN_BRIDGE_PEOPLE or not fit.statements:
        report["notes"].append(
            "Bridges need more votes: 8 people rating statements with 5+ raters."
        )
    else:
        passed, near = bridges(fit)
        report["bridges"] = {
            "passed": named(passed),
            "leaning": named(near),
            "axis": _axis_label(fit, m, anchor_of, bundle),
            "rated_participants": len(fit.participants),
        }
    return report


def participant_view(rows, statements, bundle, demo: bool, participant: str) -> dict:
    """What one participant may see about themselves: their group and the bridges they backed."""
    report = room_report(rows, statements, bundle, demo)
    mine = {s: v for p, s, v, _ in rows if p == participant}
    used = [(p, s, v) for p, s, v, syn in rows if (demo or not syn) and s in statements]
    group = None
    if report["groups"] and report["groups"]["clear"] and used:
        m = VoteMatrix.from_rows(used)
        polis = polis_groups(m)
        if polis and participant in polis.participants:
            group = GROUP_NAMES[int(polis.labels[polis.participants.index(participant)])]
    backed = []
    if report["bridges"]:
        backed = [
            b["statement"] for b in report["bridges"]["passed"] if mine.get(b["statement"]) == 1
        ]
    return {"group": group, "votes": len(mine), "backed_bridges": backed}
