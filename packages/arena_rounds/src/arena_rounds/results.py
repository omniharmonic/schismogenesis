"""Public results: what the people who shared their answers think, in aggregate only.

Inputs are the anchor-statement votes of people who chose to add their answers (the main room),
plus published profiles. Every figure about a subgroup is suppressed below MIN_CELL people, so no
small group, and no person, can be picked out. Synthetic participants are never counted.
"""

from collections import Counter, defaultdict

from arena_fingerprint.agreement import ranked

MIN_CELL = 10
MIN_ANSWERED = 6


def _home(
    answers: dict[str, int], stances: dict, school_of: dict[str, str]
) -> tuple[str | None, str | None]:
    """The person's nearest thinker and that thinker's school, as the fingerprint computes them."""
    for thinker, _, _, _ in ranked(answers, stances):
        if thinker in school_of:
            return thinker, school_of[thinker]
    return None, None


def results(
    sheets: dict[str, dict[str, int]],
    bundle: dict,
    profiles: list[dict] | None = None,
    min_cell: int = MIN_CELL,
) -> dict:
    """sheets: participant -> {anchor id: -1, 0 or 1} (no ids leave this function)."""
    profiles = profiles or []
    stances = {a: {t: v["a"] for t, v in e.items()} for a, e in bundle["stances"].items()}
    school_of = {m: s["label"] for s in bundle["schools"] for m in s["members"]}
    names = {t["id"]: t["name"] for t in bundle["thinkers"]}
    counted = {
        p: a
        for p, a in sheets.items()
        if sum(1 for v in a.values() if v in (1, -1)) >= MIN_ANSWERED
    }
    n = len(counted)
    out: dict = {
        "contributors": n,
        "min_cell": min_cell,
        "profiles": {
            "published": len(profiles),
            "verified": sum(1 for p in profiles if p["identity"] != "anon"),
        },
        "statements": [],
        "homes": [],
        "nearest": [],
        "crosstab": None,
        "camps": [],
        "notes": [],
    }
    if n < min_cell:
        out["notes"].append(
            f"Results appear once {min_cell} people have added their answers (now {n})."
        )
        return out

    homes: dict[str, str] = {}
    nearest: Counter[str] = Counter()
    for participant, answers in counted.items():
        thinker, school = _home(answers, stances, school_of)
        if thinker:
            nearest[thinker] += 1
        if school:
            homes[participant] = school

    for anchor in bundle["anchors"]:
        votes = [a[anchor["id"]] for a in counted.values() if anchor["id"] in a]
        agree, disagree, unsure = votes.count(1), votes.count(-1), votes.count(0)
        decided = agree + disagree
        thinker_votes = list(stances[anchor["id"]].values())
        thinker_agree = sum(1 for v in thinker_votes if v == 1) / len(thinker_votes)
        row = {
            "id": anchor["id"],
            "text": anchor["text"],
            "layer": anchor["layer"],
            "answered": len(votes),
            "agree": agree,
            "disagree": disagree,
            "unsure": unsure,
            "agree_share": round(agree / decided, 3) if decided >= min_cell else None,
            "thinkers_agree_share": round(thinker_agree, 3),
            "thinkers": len(thinker_votes),
        }
        if row["agree_share"] is not None:
            row["gap"] = round(row["agree_share"] - thinker_agree, 3)
            row["split"] = round(1 - abs(2 * row["agree_share"] - 1), 3)  # 1 = evenly split
        out["statements"].append(row)

    home_counts = Counter(homes.values())
    out["homes"] = [
        {"school": s, "people": c, "share": round(c / n, 3)}
        for s, c in home_counts.most_common()
        if c >= min_cell
    ]
    hidden = sum(c for c in home_counts.values() if c < min_cell)
    if hidden:
        out["notes"].append(f"{hidden} people sit in neighbourhoods too small to show separately.")
    out["nearest"] = [
        {"id": t, "name": names[t], "people": c, "share": round(c / n, 3)}
        for t, c in nearest.most_common()
        if c >= min_cell
    ]

    # how each neighbourhood answers each statement, for neighbourhoods big enough to show
    big = [h["school"] for h in out["homes"]]
    cells: dict[str, dict[str, dict]] = defaultdict(dict)
    tally: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0])  # (anchor, school)
    shown = set(big)
    for p, school in homes.items():
        if school not in shown:
            continue
        for anchor, v in counted[p].items():
            if v in (1, -1):
                pair = tally[(anchor, school)]
                pair[0] += v == 1
                pair[1] += 1
    for anchor in bundle["anchors"]:
        for school in big:
            yes, total = tally.get((anchor["id"], school), (0, 0))
            cells[anchor["id"]][school] = (
                {"agree_share": round(yes / total, 3), "n": total} if total >= min_cell else None
            )
    if len(big) >= 2:
        out["crosstab"] = {"schools": big, "cells": dict(cells)}
    else:
        out["notes"].append(
            "Comparisons between neighbourhoods appear once two have enough people."
        )

    for camp in bundle["camps"]:
        aligned = 0
        # the camp's side on each statement doesn't depend on the person: work it out once
        sides = {}
        for anchor, entry in stances.items():
            side = sum(entry.get(m, 0) for m in camp["members"])
            if side:
                sides[anchor] = side > 0
        for answers in counted.values():
            agree = total = 0
            for anchor, v in answers.items():
                if v not in (1, -1) or anchor not in sides:
                    continue
                total += 1
                agree += int(sides[anchor] == (v > 0))
            if total and agree / total > 0.5:
                aligned += 1
        out["camps"].append(
            {"id": camp["id"], "label": camp["label"], "share_aligned": round(aligned / n, 3)}
        )

    if profiles:
        published = Counter(p["summary"]["home"] for p in profiles)
        out["profiles"]["homes"] = [
            {"school": s, "people": c} for s, c in published.most_common() if c >= min_cell
        ]
    return out
