"""Build the browser bundle for the fingerprint from the checked atlas."""

from arena_fingerprint.anchors import COVER_TARGET, SETS, select_anchors, stated_stances

VERSION = "fp-2026-11-02.1"
SEASON = "season-1"  # the statements; answers stay valid across bundle versions in a season
MAX_QUOTE = 280
LAYERS = ["ontological", "epistemic", "axiological", "empirical", "praxis"]
CAMPS = [
    {
        "id": "eacc",
        "label": "e/acc",
        "members": ["guillaume-verdon", "nick-land", "marc-andreessen"],
    },
    {
        "id": "safety",
        "label": "AI safety / EA",
        "members": [
            "eliezer-yudkowsky",
            "daniel-kokotajlo",
            "scott-alexander",
            "max-tegmark",
            "william-macaskill",
        ],
    },
    {
        "id": "dacc",
        "label": "d/acc & pluralists",
        "members": ["vitalik-buterin", "audrey-tang", "e-glen-weyl"],
    },
]
NOTES = [
    "Thinkers are read by machine from about three public works each. "
    "None of them has reviewed this.",
    "Agreement counts only statements where we found a stated position, never silence.",
    "Schools are working labels made by clustering. The people named should replace them.",
    "Your answers stay in your browser unless you choose to join the room.",
]


class BundleError(ValueError):
    pass


def initials(name: str) -> str:
    parts = [p for p in name.replace(".", " ").split() if p[0].isalpha()]
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()


def frozen_anchors(ideas: list[dict], season: list[dict], camps: dict) -> list[dict]:
    """Season anchors: the same statements in the same order, with today's holders."""
    from arena_fingerprint.anchors import split_score

    by_id = {i["id"]: i for i in ideas}
    if missing := [a["id"] for a in season if a["id"] not in by_id]:
        raise BundleError(f"season statements missing from the atlas: {missing}")
    return [
        {**by_id[a["id"]], "set": a["set"],
         "split_score": split_score(stated_stances(by_id[a["id"]]), camps)}
        for a in season
    ]  # fmt: skip


def build_bundle(
    atlas: dict,
    flagged: set[str],
    season: list[dict] | None = None,
    version: str = VERSION,
    atlas_version: str = "atlas-v1",
) -> dict:
    """Build the browser bundle. With `season`, keep those statements instead of reselecting."""
    people = {p["id"]: p for p in atlas["people"]}
    if bad := flagged & set(people):
        raise BundleError(f"flagged landmarks must not appear: {sorted(bad)}")
    school_of = {m: s["label"] for s in atlas["schools"] if s["label"] for m in s["members"]}
    camps = {c["id"]: c["members"] for c in CAMPS}
    for camp in CAMPS:
        if missing := set(camp["members"]) - set(people):
            raise BundleError(f"camp {camp['id']} names unknown thinkers: {sorted(missing)}")
    if season:
        anchors, log = (
            frozen_anchors(atlas["ideas"], season, camps),
            ["statements frozen for the season"],
        )
    else:
        anchors, log = select_anchors(atlas["ideas"], camps)
    for person in sorted(people):
        count = sum(1 for i in anchors if person in stated_stances(i))
        if count < COVER_TARGET:
            log.append(f"coverage: {person} has {count} stated stances among the anchors")
    stances: dict[str, dict[str, dict]] = {}
    for idea in anchors:
        stance = stated_stances(idea)
        entry: dict[str, dict] = {}
        for person, a in sorted(stance.items()):
            quote = next(
                (
                    h
                    for h in idea["holders"]
                    if h["p"] == person and not h["inf"] and (h["a"] > 0) == (a > 0) and h["q"]
                ),
                None,
            )
            item: dict = {"a": a}
            if quote:
                if len(quote["q"]) > MAX_QUOTE:
                    raise BundleError(f"quote over {MAX_QUOTE} characters: {idea['id']}/{person}")
                item |= {"q": quote["q"], "url": quote["url"], "work": quote["work"]}
            entry[person] = item
        stances[idea["id"]] = entry
    return {
        "version": version,
        "season": SEASON,
        "atlas_version": atlas_version,
        "sets": SETS,
        "layers": LAYERS,
        "anchors": [
            {
                "id": i["id"],
                "set": i["set"],
                "layer": i["layer"],
                "text": i["text"],
                "family": i["family"],
                "split_score": i["split_score"],
            }
            for i in anchors
        ],
        "thinkers": [
            {
                "id": p["id"],
                "name": p["name"],
                "initials": initials(p["name"]),
                "school": school_of.get(p["id"]),
                "x": p["x"],
                "y": p["y"],
            }
            for p in sorted(people.values(), key=lambda p: p["id"])
        ],
        "schools": [
            {"label": s["label"], "members": s["members"]} for s in atlas["schools"] if s["label"]
        ],
        "camps": CAMPS,
        "stances": stances,
        "selection_log": log,
        "notes": NOTES,
    }
