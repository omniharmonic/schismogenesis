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


QUOTE_MARKS = "\"'“”‘’ "


def display_quote(text: str) -> str:
    """The quote as shown: the page adds its own quote marks, so drop the source's outer ones and
    any markdown emphasis left from the text extraction. The stored quote stays exact."""
    text = text.replace("**", "").strip()
    text = text.strip("*").strip()
    if text[:1] in '"“' and text[-1:] in '"”' and text.count(text[0]) + text.count("”") <= 2:
        text = text[1:-1].strip()
    return text


def display_work(title: str, year: str | None = None) -> str:
    if title.lower().startswith("untitled"):
        return "Untitled blog post" + (f", {year}" if year else "")
    return title


def initials(name: str) -> str:
    parts = [p for p in name.replace(".", " ").split() if p[0].isalpha()]
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()


def frozen_anchors(ideas: list[dict], season: list[dict], camps: dict) -> list[dict]:
    """Season anchors: the same statements in the same order, with today's holders."""
    from arena_fingerprint.anchors import split_score

    by_id = {i["id"]: i for i in ideas}
    if missing := [a["id"] for a in season if a["id"] not in by_id]:
        raise BundleError(f"season statements missing from the atlas: {missing}")
    out = []
    for a in season:
        idea = by_id[a["id"]]
        # reviewed display wording (seed/season-1.json), or the wording a built bundle carries
        display = a.get("display") or (a.get("text") if a.get("text") != idea["text"] else None)
        out.append({**idea, "set": a["set"], "display": display,
                    "split_score": split_score(stated_stances(idea), camps)})  # fmt: skip
    return out


PLACE_SHARPNESS = 14  # same weighting as the fingerprint uses to place a person


def place_newcomers(
    stances: dict[str, dict[str, dict]],
    people: dict[str, dict],
    school_of: dict[str, str],
    newcomers: dict[str, str],
    log: list[str],
) -> list[dict]:
    """Place approved voices that aren't in the full atlas yet, from the statements alone.

    A newcomer is placed among the three atlas thinkers they agree with most (the same rule that
    places a quiz taker) and takes the school of the closest. Marked provisional until the full
    structure pass (docs/fingerprint/05-ATLAS-EXPANSION.md, step E7) gives them a real position.
    """
    import math

    from arena_fingerprint.agreement import ranked

    plain = {a: {p: v["a"] for p, v in e.items()} for a, e in stances.items()}
    atlas_only = {a: {p: v for p, v in e.items() if p in people} for a, e in plain.items()}
    placed = []
    for person, name in sorted(newcomers.items()):
        if person in people:
            continue
        answers = {a: e[person] for a, e in plain.items() if person in e}
        if len(answers) < COVER_TARGET:
            log.append(f"newcomer not shown: {person} has {len(answers)} stated stances")
            continue
        top = ranked(answers, atlas_only)[:3]
        if not top:
            log.append(f"newcomer not shown: {person} shares too few statements with the atlas")
            continue
        weights = [math.exp(PLACE_SHARPNESS * (s - 0.5)) for _, _, _, s in top]
        x = sum(w * people[t]["x"] for w, (t, *_rest) in zip(weights, top, strict=True))
        y = sum(w * people[t]["y"] for w, (t, *_rest) in zip(weights, top, strict=True))
        school = next((school_of[t] for t, *_ in top if t in school_of), None)
        placed.append({
            "id": person, "name": name, "initials": initials(name), "school": school,
            "x": round(x / sum(weights), 1), "y": round(y / sum(weights), 1), "provisional": True,
        })  # fmt: skip
    return placed


def build_bundle(
    atlas: dict,
    flagged: set[str],
    season: list[dict] | None = None,
    version: str = VERSION,
    atlas_version: str = "atlas-v1",
    newcomers: dict[str, str] | None = None,
    voices: dict[str, list[dict]] | None = None,
    season_id: str = SEASON,
) -> dict:
    """Build the browser bundle. With `season`, keep those statements instead of reselecting.

    `newcomers` (id -> name) are approved voices not yet in the full atlas. Those with enough
    stated stances on the statements are placed provisionally (see `place_newcomers`).
    """
    newcomers = newcomers or {}
    if bad := flagged & set(newcomers):
        raise BundleError(f"flagged landmarks must not appear: {sorted(bad)}")
    people = {p["id"]: p for p in atlas["people"]}
    if bad := flagged & set(people):
        raise BundleError(f"flagged landmarks must not appear: {sorted(bad)}")
    school_of = {
        m: s["label"]
        for s in atlas["schools"]
        if s["label"]
        for m in s["members"] + s.get("provisional_members", [])
    }
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
                year = str(quote["year"]) if quote.get("year") else None
                item |= {"q": display_quote(quote["q"]), "url": quote["url"],
                         "work": display_work(quote["work"], year)}  # fmt: skip
            entry[person] = item
        stances[idea["id"]] = entry
    placed = place_newcomers(stances, people, school_of, newcomers, log)
    shown = set(people) | {p["id"] for p in placed}
    stances = {a: {p: v for p, v in e.items() if p in shown} for a, e in stances.items()}
    return {
        "version": version,
        "season": season_id,
        "atlas_version": atlas_version,
        "sets": SETS,
        "layers": LAYERS,
        "anchors": [
            {
                "id": i["id"],
                "set": i["set"],
                "layer": i["layer"],
                "text": i.get("display") or i["text"],
                **({"proposition": i["text"]} if i.get("display") not in (None, i["text"]) else {}),
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
                **({"provisional": True} if p.get("provisional") else {}),
                **({"between": p["between"]} if p.get("between") else {}),
            }
            for p in sorted(people.values(), key=lambda p: p["id"])
        ]
        + placed,
        "schools": [
            {"label": s["label"], "members": s["members"]} for s in atlas["schools"] if s["label"]
        ],
        "camps": CAMPS,
        "stances": stances,
        # signature positions in each thinker's own words (seed/thinker-voices.json, checked)
        "voices": {
            p: [{**v, "quote": display_quote(v["quote"])} for v in vs[:6]]
            for p, vs in sorted((voices or {}).items())
            if p in shown and p not in flagged
        },
        "selection_log": log,
        "notes": NOTES,
    }
