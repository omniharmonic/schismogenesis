"""Choose the anchor statements: atlas ideas that thinkers hold on both sides (ADR-036).

The rule is deterministic, so the same atlas always gives the same statements. See
docs/fingerprint/02-ARCHITECTURE.md section 4.
"""

from collections import Counter

SETS: list[dict] = [
    {
        "id": "being",
        "title": "What AI is and where it's going",
        "layers": ["ontological", "empirical"],
    },
    {
        "id": "values",
        "title": "What we know and what matters",
        "layers": ["epistemic", "axiological"],
    },
    {"id": "action", "title": "What we should do", "layers": ["praxis"]},
]
MAX_TEXT = 200
FAMILY_CAP_SET = 1
FAMILY_CAP_TOTAL = 2
CAMP_BONUS = 2
COVER_BONUS = 4
COVER_TARGET = 3


def stated_stances(idea: dict) -> dict[str, int]:
    """One stated stance per person: the majority of their stated holdings, ties to accept."""
    votes: dict[str, list[int]] = {}
    for holder in idea["holders"]:
        if not holder["inf"]:
            votes.setdefault(holder["p"], []).append(1 if holder["a"] > 0 else -1)
    return {person: (1 if sum(v) >= 0 else -1) for person, v in votes.items()}


def camp_majority(stances: dict[str, int], members: list[str]) -> int:
    total = sum(stances[m] for m in members if m in stances)
    return (total > 0) - (total < 0)


def split_score(stances: dict[str, int], camps: dict[str, list[str]]) -> int:
    accepts = sum(1 for a in stances.values() if a > 0)
    rejects = len(stances) - accepts
    sides = {camp_majority(stances, m) for m in camps.values()} - {0}
    return accepts * rejects + (CAMP_BONUS if len(sides) > 1 else 0)


def candidates(ideas: list[dict]) -> list[dict]:
    out = []
    for idea in ideas:
        stances = stated_stances(idea)
        accepts = sum(1 for a in stances.values() if a > 0)
        if len(stances) >= 3 and 0 < accepts < len(stances) and len(idea["text"]) <= MAX_TEXT:
            out.append(idea)
    return out


def select_anchors(
    ideas: list[dict], camps: dict[str, list[str]], per_set: int = 8
) -> tuple[list[dict], list[str]]:
    """Fill each set greedily under the family caps; log any relaxation.

    Each pick maximises split score plus a bonus for every holder who is still below
    COVER_TARGET stated stances among the anchors chosen so far, so that no thinker is left
    unrankable when the data allows it.
    """
    pool = sorted(candidates(ideas), key=lambda i: i["id"])
    stances = {i["id"]: stated_stances(i) for i in pool}
    base = {i["id"]: split_score(stances[i["id"]], camps) for i in pool}
    coverage: Counter[str] = Counter()
    chosen: list[dict] = []
    log: list[str] = []
    total: Counter[int] = Counter()

    def gain(idea: dict) -> int:
        under = sum(1 for p in stances[idea["id"]] if coverage[p] < COVER_TARGET)
        return base[idea["id"]] + COVER_BONUS * under

    for spec in SETS:
        in_set: Counter[int] = Counter()
        options = [i for i in pool if i["layer"] in spec["layers"]]
        picked: list[dict] = []
        for relaxed in (False, True):
            cap_set, cap_total = FAMILY_CAP_SET + relaxed, FAMILY_CAP_TOTAL + relaxed
            while len(picked) < per_set:
                allowed = [
                    i
                    for i in options
                    if i not in picked
                    and in_set[i["family"]] < cap_set
                    and total[i["family"]] < cap_total
                ]
                if not allowed:
                    break
                idea = max(
                    allowed, key=lambda i: (gain(i), base[i["id"]], [-ord(c) for c in i["id"]])
                )
                if relaxed:
                    log.append(f"{spec['id']}: family cap relaxed for {idea['id']}")
                picked.append(idea)
                in_set[idea["family"]] += 1
                total[idea["family"]] += 1
                coverage.update(stances[idea["id"]].keys())
        if len(picked) < per_set:
            log.append(f"{spec['id']}: only {len(picked)} candidates")
        chosen += [{**i, "set": spec["id"], "split_score": base[i["id"]]} for i in picked]
    return chosen, log
