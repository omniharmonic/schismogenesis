"""The room report: groups, bridges, common ground, splits, and how the room relates to thinkers.

Every section has a minimum-data rule. Below it the report says what is missing instead of
guessing (docs/fingerprint/02-ARCHITECTURE.md section 6, 04-LAUNCH.md section 2).

`analyse` returns two things: the public report (aggregates only) and a private index of
per-participant measures, which the API serves only to that participant.
"""

import itertools
from dataclasses import dataclass, field

import numpy as np
from arena_fingerprint.agreement import ranked

from arena_rounds.bridging import bridges, fit_bridging
from arena_rounds.matrix import VoteMatrix
from arena_rounds.polis import (
    consensus,
    divisive,
    group_stats,
    polis_groups,
    representative,
    stability_label,
)

MIN_GROUP_PEOPLE = 10
MIN_BRIDGE_PEOPLE = 8
MIN_DESCRIBED = 3
MIN_TAKE_VOTERS = 5
AXIS_MIN_R = 0.4
GROUP_NAMES = "ABCDE"
MAX_POINTS = 1500
BRIDGE_BOOTSTRAP = 20
MIN_THINKER_ANCHORS = 3


@dataclass
class Analysis:
    report: dict
    personal: dict[str, dict] = field(default_factory=dict)


def _stances(bundle: dict) -> dict[str, dict[str, int]]:
    return {a: {t: v["a"] for t, v in e.items()} for a, e in bundle["stances"].items()}


def _group_thinkers(stats: dict, anchor_of: dict[str, str], stances: dict) -> list[dict]:
    answers = {}
    for statement, s in stats.items():
        anchor = anchor_of.get(statement)
        if anchor and s.seen:
            answers[anchor] = 1 if s.pa > s.pd + 0.1 else (-1 if s.pd > s.pa + 0.1 else 0)
    return [
        {"id": t, "k": k, "n": n, "s": round(sc, 3)} for t, k, n, sc in ranked(answers, stances)[:3]
    ]


def _camp_affinity(values: np.ndarray, columns: list[int], sides: np.ndarray) -> np.ndarray:
    """Laplace agreement of each row with a camp's majority sides on the given columns."""
    if not columns:
        return np.full(len(values), 0.5)
    v = values[:, columns]
    voted = ~np.isnan(v) & (v != 0) & (sides != 0)
    agree = (np.nan_to_num(v) == sides) & voted
    return (agree.sum(1) + 1) / (voted.sum(1) + 2)


def _axis_label(fit, m: VoteMatrix, anchor_of: dict[str, str], bundle: dict) -> dict | None:
    """Correlate the bridging factor with camp-affinity differences on anchor votes."""
    stances = _stances(bundle)
    col = {s: j for j, s in enumerate(m.statements)}
    rows = np.array([m.participants.index(p) for p in fit.participants]) if fit.participants else []
    values = m.values[rows]
    statements = [s for s in anchor_of if s in col]
    columns = [col[s] for s in statements]
    affinity = {}
    for camp in bundle["camps"]:
        sides = np.array(
            [
                np.sign(sum(stances[anchor_of[s]].get(x, 0) for x in camp["members"]))
                for s in statements
            ]
        )
        affinity[camp["id"]] = _camp_affinity(values, columns, sides)
    best = None
    labels = {c["id"]: c["label"] for c in bundle["camps"]}
    for a, b in itertools.combinations(sorted(affinity), 2):
        diff = affinity[a] - affinity[b]
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


def _thinkers_in_room(polis, m: VoteMatrix, anchor_of: dict[str, str], bundle: dict) -> list[dict]:
    """Treat each thinker as a participant who voted only on anchors; place without refitting."""
    stances = _stances(bundle)
    col = {s: j for j, s in enumerate(m.statements)}
    out = []
    for thinker in bundle["thinkers"]:
        row = np.full(len(m.statements), np.nan)
        for statement, anchor in anchor_of.items():
            if statement in col and thinker["id"] in stances.get(anchor, {}):
                row[col[statement]] = stances[anchor][thinker["id"]]
        if (~np.isnan(row)).sum() < MIN_THINKER_ANCHORS:
            continue
        x, y = polis.space.place(row[None, :])[0]
        out.append({"id": thinker["id"], "x": round(float(x), 3), "y": round(float(y), 3)})
    return out


def _personal(m: VoteMatrix, polis, members, stats, text: dict[str, str]) -> dict[str, dict]:
    """Rarity, rarest take, and nearest and furthest group, for every participant."""
    v = m.values
    with np.errstate(invalid="ignore"):
        agree, disagree = (v > 0).sum(0), (v < 0).sum(0)
    decided = agree + disagree
    share_same = np.where(
        v > 0,
        agree / np.maximum(decided, 1),
        np.where(v < 0, disagree / np.maximum(decided, 1), np.nan),
    )
    # rarity: on average, how small a minority you're in when you take a side
    eligible = (decided >= MIN_TAKE_VOTERS)[None, :] & ~np.isnan(share_same)
    shares = np.where(eligible, share_same, np.nan)
    counts = eligible.sum(1)
    rarity = np.where(counts > 0, 1 - np.nansum(shares, 1) / np.maximum(counts, 1), np.nan)
    valid = ~np.isnan(rarity)
    order = np.sort(rarity[valid])
    majorities = None
    if polis is not None and polis.k > 1:
        majorities = np.array(
            [
                [
                    1 if st.pa > st.pd + 0.1 else (-1 if st.pd > st.pa + 0.1 else 0)
                    for st in (stats[g][s] for s in m.statements)
                ]
                for g in range(polis.k)
            ]
        )
    out: dict[str, dict] = {}
    group_of = (
        dict(zip(polis.participants, polis.labels.tolist(), strict=True))
        if polis is not None
        else {}
    )
    for i, participant in enumerate(m.participants):
        entry: dict = {"votes": int((~np.isnan(v[i])).sum())}
        if valid[i] and counts[i] >= 3:
            entry["rarity_percentile"] = round(
                100 * float(np.searchsorted(order, rarity[i], side="right")) / len(order)
            )
            j = int(np.nanargmin(shares[i]))
            entry["rarest_take"] = {
                "statement": m.statements[j],
                "text": text[m.statements[j]],
                "vote": int(v[i, j]),
                "share_with_you": round(float(shares[i, j]), 3),
            }
        if majorities is not None and participant in group_of:
            mine = np.nan_to_num(v[i])
            compared = (mine != 0) & (majorities != 0)
            agreement = ((mine == majorities) & compared).sum(1) / np.maximum(compared.sum(1), 1)
            entry["group"] = GROUP_NAMES[group_of[participant]]
            entry["nearest_group"] = GROUP_NAMES[int(np.argmax(agreement))]
            entry["furthest_group"] = GROUP_NAMES[int(np.argmin(agreement))]
            entry["group_agreement"] = {
                GROUP_NAMES[g]: round(float(a), 3) for g, a in enumerate(agreement)
            }
        out[participant] = entry
    return out


def analyse(
    rows: list[tuple[str, str, int, bool]],
    statements: dict[str, dict],
    bundle: dict,
    demo: bool,
    seed: int = 7,
) -> Analysis:
    """Analyse a room.

    rows: (participant, statement, vote, is_synthetic).
    statements: id -> {text, origin, anchor_id}.
    """
    used = [(p, s, v) for p, s, v, synthetic in rows if (demo or not synthetic) and s in statements]
    m = VoteMatrix.from_rows(used) if used else VoteMatrix([], [], np.zeros((0, 0)))
    active = (
        int((m.votes_per_participant() >= min(7, max(len(m.statements), 1))).sum()) if used else 0
    )
    anchor_of = {sid: s["anchor_id"] for sid, s in statements.items() if s.get("anchor_id")}
    stances = _stances(bundle)
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
    if not used:
        report["notes"].append(f"Groups appear after {MIN_GROUP_PEOPLE} people have voted.")
        report["notes"].append(
            "Bridges need more votes: 8 people rating statements with 5+ raters."
        )
        return Analysis(report)

    polis = polis_groups(m, seed=seed, stability=active >= MIN_GROUP_PEOPLE)
    members: dict[int, list[str]] = {}
    stats = None
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
        label = stability_label(polis.stability)
        clear = polis.k > 1 and label != "unstable"
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
        sample = np.arange(len(polis.participants))
        if len(sample) > MAX_POINTS:
            sample = np.random.default_rng(seed).choice(sample, MAX_POINTS, replace=False)
        report["groups"] = {
            "k": polis.k,
            "silhouette": None if polis.silhouette is None else round(polis.silhouette, 3),
            "stability": None if polis.stability is None else round(polis.stability, 3),
            "stability_label": label,
            "clear": clear,
            "list": groups,
            "points": [
                [
                    round(float(polis.projection[i, 0]), 3),
                    round(float(polis.projection[i, 1]), 3),
                    int(polis.labels[i]),
                ]
                for i in sorted(sample.tolist())
            ],  # fmt: skip
            "thinkers": _thinkers_in_room(polis, m, anchor_of, bundle),
            "consensus": named([c for c in consensus(stats) if c["all_agree"]][:5])
            if clear
            else [],
            "divisive": named(divisive(stats)[:5]) if clear else [],
        }
        if polis.k == 1:
            report["notes"].append("No clear groups yet: the room's votes don't separate.")
        elif label == "unstable":
            report["notes"].append(
                "Groups aren't stable yet: they change when statements are resampled."
            )

    fit = fit_bridging(m, init=polis.pc1 if polis else None, bootstrap=BRIDGE_BOOTSTRAP, seed=seed)
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
    personal = _personal(m, polis if members else None, members, stats, text)
    bridge_ids = {b["statement"] for b in (report["bridges"] or {}).get("passed", [])}
    index = {p: i for i, p in enumerate(m.participants)}
    bridge_cols = {s: m.statements.index(s) for s in bridge_ids}
    for participant, entry in personal.items():
        row = m.values[index[participant]]
        entry["backed_bridges"] = [s for s, j in bridge_cols.items() if row[j] == 1]
    return Analysis(report, personal)


def room_report(rows, statements, bundle, demo: bool) -> dict:
    return analyse(rows, statements, bundle, demo).report


def participant_view(rows, statements, bundle, demo: bool, participant: str) -> dict:
    """What one participant may see about themselves."""
    analysis = analyse(rows, statements, bundle, demo)
    return personal_view(analysis, participant, rows)


def personal_view(analysis: Analysis, participant: str, rows=None) -> dict:
    entry = analysis.personal.get(participant)
    if entry is None:
        votes = sum(1 for r in rows or [] if r[0] == participant)
        return {"group": None, "votes": votes, "backed_bridges": []}
    return {"group": None, **entry}
