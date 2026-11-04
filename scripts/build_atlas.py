"""Measure the checked structure and write the page data.

Usage: build_atlas.py <structure.json> <copy.json> <output.json>
"""

import itertools
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass

import numpy as np
from arena_core.db import get_engine
from arena_map.structure import (
    LAYERS,
    ROOT_LAYERS,
    Holding,
    families,
    fidelity,
    fork_profile,
    layout,
    person_space,
    reasons_load,
    school_stability,
    schools,
    sense_fork,
)
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist, squareform
from sentence_transformers import SentenceTransformer
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sqlalchemy import text

MODEL = "BAAI/bge-large-en-v1.5"
SPREAD = 190.0
FAMILIES = 40
ATTACKS = {"rebuts", "undercuts", "undermines"}
SUPPORT = {
    "supports": 1.0,
    "presupposes": 1.0,
    "exemplifies": 0.7,
    "defines": 0.5,
    "qualifies": 0.3,
}
MIN_HOLDINGS = 8
MIN_PLACED = 4
TERMS = ["safety", "intelligence", "progress", "freedom", "democracy", "alignment", "power",
         "open", "human", "truth", "risk", "accelerat"]  # fmt: skip
SEEDS = ["seed/WORLDVIEW-CORE-SOURCES.json", "seed/AI-FUTURES-SOURCES.json",
         "seed/AI-FUTURES-SOURCES-v2.json", "seed/AI-FUTURES-SOURCES-v3.json",
         "seed/AI-FUTURES-SOURCES-v4.json", "seed/AI-FUTURES-SOURCES-v5.json"]  # fmt: skip


def majority(rows: list[dict]) -> dict:
    """One stance per person and idea. Stated beats inferred; a stated tie goes to accept."""
    stated = [r for r in rows if not r["inf"]]
    pool = stated or rows
    accepts = [r for r in pool if r["a"] > 0]
    rejects = [r for r in pool if r["a"] < 0]
    return (accepts if len(accepts) >= len(rejects) else rejects)[0]


def _embedding_groups(means: np.ndarray, people: list[str], count: int) -> list[int]:
    return [int(x) for x in fcluster(linkage(pdist(means, "cosine"), "average"), count, "maxclust")]


def partition(groups: list[list[str]], names: list[str]) -> list[int]:
    label = {name: i for i, group in enumerate(groups) for name in group}
    return [label[name] for name in names]


def similarity(ideas: list[dict], links: list[dict], model: SentenceTransformer) -> np.ndarray:
    """Meaning plus argument: supports pull ideas together, attacks keep poles apart."""
    vectors = model.encode([i["canonical"] for i in ideas], normalize_embeddings=True)
    out = vectors @ vectors.T
    at = {idea["key"]: n for n, idea in enumerate(ideas)}
    for link in links:
        if link["from"] not in at or link["to"] not in at:
            continue
        a, b = at[link["from"]], at[link["to"]]
        change = -0.5 if link["type"] in ATTACKS else 0.25 * SUPPORT.get(link["type"], 0)
        out[a, b] += change
        out[b, a] += change
    return out


def choose_count(holdings: list[Holding], family: dict[str, int]) -> tuple[int, dict]:
    """Pick the number of schools that holds together best when families are resampled."""
    space = person_space(holdings, family)
    best, best_score = 6, -1.0
    table = {}
    for count in range(4, 10):
        stable = school_stability(holdings, family, count, runs=150)
        groups = schools(space, count)
        within = [stable.get(frozenset(p), 0) for g in groups for p in itertools.combinations(g, 2)]
        between = [
            stable.get(frozenset({a, b}), 0)
            for x, y in itertools.combinations(groups, 2) for a in x for b in y
        ]  # fmt: skip
        score = float(np.mean(within)) - float(np.mean(between))
        table[count] = round(score, 3)
        if score > best_score:
            best, best_score = count, score
    return best, {"count": best, "separation": round(best_score, 3), "by_count": table}


PLACE_SHARPNESS = 14  # the fingerprint's weighting (packages/arena_fingerprint, fingerprint.js)
FORECAST_WEIGHT = 0.5  # forecasts count half as much as values, action and what AI is


@dataclass
class Placement:
    xy: np.ndarray
    top: list[tuple[str, float]]  # nearest three by agreement, with weights: sets the position


def place_by_agreement(
    person: str,
    stated: dict[tuple[str, str], int],
    core: list[str],
    place: dict[str, np.ndarray],
    layer: dict[str, str],
) -> Placement | None:
    """Place a voice outside the core the way the fingerprint places a visitor.

    Agreement with each core voice is (same + 1) / (shared + 2) over stated ideas both hold,
    with forecasts weighted at half, counted when they share three or more. The position is the
    sharply weighted mean of the top three. The school is decided separately (school_fit), on
    distinctive positions only: a critic and a builder can both expect AI to be unstoppable, and
    agreement like that alone once put Kingsnorth among the Builders.
    """
    mine = {idea: a for (idea, p), a in stated.items() if p == person}
    scored = []
    for other in core:
        shared = [i for i in mine if (i, other) in stated]
        if len(shared) < 3:
            continue
        weight = {i: FORECAST_WEIGHT if layer.get(i) == "empirical" else 1.0 for i in shared}
        same = sum(weight[i] for i in shared if mine[i] == stated[(i, other)])
        score = (same + 1) / (sum(weight.values()) + 2)
        scored.append((score, len(shared), other))
    top = sorted(scored, reverse=True)[:3]
    if not top:
        return None

    def weighted(rows: list[tuple[float, int, str]]) -> list[tuple[str, float]]:
        return [(o, float(np.exp(PLACE_SHARPNESS * (s - 0.5)))) for s, _, o in rows]

    near = weighted(top)
    total = sum(w for _, w in near)
    xy = sum(w * place[o] for o, w in near) / total
    return Placement(xy, near)


GROUP_EVIDENCE = 2.5  # distinctive agreement a voice needs before it joins a school
GROUP_MARGIN = 0.6  # the runner-up school must be at most this share of the best


def school_fit(
    person: str, stated: dict[tuple[str, str], int], groups: list[list[str]], layer: dict[str, str]
) -> dict:
    """How far a voice holds the positions that set each school apart.

    For each school and idea, distinctiveness is how far the school's members lean away from the
    core as a whole (forecasts at half weight). A voice's fit to a school sums its own stance times
    that lean. Positions nearly everyone holds count for nothing, and contrary positions count
    against: agreeing that AI should serve people says nothing about which school you are in.
    Returns {"school": index or None, "between": [index, index] or [], "fits": [(fit, index)]}.
    """
    core = [m for g in groups for m in g]
    mine = {i: a for (i, p), a in stated.items() if p == person}
    fits = []
    for n, group in enumerate(groups):
        fit = 0.0
        for idea, a in mine.items():
            everyone = [stated[(idea, m)] for m in core if (idea, m) in stated]
            members = [stated[(idea, m)] for m in group if (idea, m) in stated]
            if not members or (len(members) < 2 and len(group) > 2):
                continue
            lean = sum(members) / len(members) - sum(everyone) / len(everyone)
            fit += a * lean * (FORECAST_WEIGHT if layer.get(idea) == "empirical" else 1.0)
        fits.append((round(fit, 3), n))
    fits.sort(reverse=True)
    (best, top), (second, runner) = fits[0], fits[1]
    if best < GROUP_EVIDENCE:
        return {"school": None, "between": [], "fits": fits}
    if second > GROUP_MARGIN * best:
        return {"school": None, "between": [top, runner], "fits": fits}
    return {"school": top, "between": [], "fits": fits}


def school_stance(members: list[str], table: dict[str, dict[str, int]]) -> dict[str, int]:
    out = {}
    for idea, row in table.items():
        votes = [row[m] for m in members if m in row]
        if len(votes) >= 2 and abs(sum(votes)) / len(votes) >= 0.6:
            out[idea] = 1 if sum(votes) > 0 else -1
    return out


def sentences(body: str, term: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", body)
    return [p for p in parts if re.search(rf"\b{term}", p, re.I) and 40 <= len(p) <= 260]


def main(structure: str, copy_path: str, output: str, *options: str) -> None:
    core_path = options[options.index("--core") + 1] if "--core" in options else None
    data = json.loads(pathlib.Path(structure).read_text())
    copy = json.loads(pathlib.Path(copy_path).read_text())
    names_path = pathlib.Path("evals/results/structure-v1/family-names.json")
    copy["families"] = json.loads(names_path.read_text()) if names_path.exists() else {}
    with get_engine().connect() as connection:
        rows = connection.execute(
            text(
                "SELECT c.claim_id::text, p.person_id, p.display_name, c.quote_public, e.url,"
                " e.title, extract(year FROM e.published_at)::int, c.proposed_canonical"
                " FROM claim c JOIN person p ON p.person_id = c.speaker_person_id"
                " JOIN episode e USING (episode_id)"
            )
        ).all()
        allowed = set(
            connection.execute(
                text("SELECT landmark_id FROM landmark WHERE public_surface_allowed")
            ).scalars()
        )
        niche_rows = connection.execute(
            text(
                "SELECT l.landmark_id, n.name, l.primary_niche_id FROM landmark l"
                " JOIN niche n ON n.niche_id = l.primary_niche_id"
            )
        ).all()
    # sources found not to be the person's own words (seed "exclude") never count for anyone
    excluded = {w["url"] for seed in SEEDS if pathlib.Path(seed).exists()
                for w in json.loads(pathlib.Path(seed).read_text())["works"]
                if w.get("exclude")}  # fmt: skip
    rows = [r for r in rows if r[4] not in excluded]
    claims = {r[0]: r for r in rows}
    niche = {r[0]: r[1] for r in niche_rows}
    names = {r[1]: r[2] for r in rows}
    # people known only from the audited stances (no extracted claims yet) still need a name
    with get_engine().connect() as connection:
        for pid, name in connection.execute(text("SELECT person_id, display_name FROM person")):
            names.setdefault(pid, name)

    per: dict[tuple[str, str], list[dict]] = defaultdict(list)
    meta = {}
    for idea in data["ideas"]:
        meta[idea["key"]] = idea
        for h in idea["holdings"]:
            claim = claims.get(h["claim"])
            if claim is None:
                continue
            if claim[1] not in allowed:
                continue
            per[(idea["key"], claim[1])].append(
                {"p": claim[1], "a": 1 if h["attitude"] == "accepts" else -1,
                 "inf": bool(h.get("inferred")), "q": None if h.get("inferred") else claim[3],
                 "url": claim[4], "work": claim[5], "year": claim[6],
                 "why": h.get("necessity")}
            )  # fmt: skip
    if "--pool" in options:
        # statements on the survey pool that the claim structure doesn't have yet join the atlas
        # as ideas; their holders come only from the audited stances
        pool = json.loads(pathlib.Path(options[options.index("--pool") + 1]).read_text())
        for st in pool["statements"]:
            if st["id"] not in meta:
                meta[st["id"]] = {"key": st["id"], "canonical": st["proposition"],
                                  "layer": st["layer"], "tl_type": "claim",
                                  "validity": None, "holdings": []}  # fmt: skip
    if "--stances" in options:
        # the audited stances (two blind readers of the full texts, quotes checked in code) are
        # the only source for the season statements: they replace every older holding there
        audited = json.loads(pathlib.Path(options[options.index("--stances") + 1]).read_text())
        for statement, entry in audited["stances"].items():
            for pair in [k for k in per if k[0] == statement]:
                del per[pair]
            for person, s in entry.items():
                if person in allowed:
                    per[(statement, person)].append(
                        {"p": person, "a": s["a"], "inf": False, "q": s["q"], "url": s["url"],
                         "work": s["work"], "year": int(s["year"]) if s.get("year") else None,
                         "why": s.get("why")}
                    )  # fmt: skip
    if "--drop-holdings" in options:
        # holdings a validator, reading the source around the quote, found not to be the person's
        # own view (seed/holding-audit-drops.json, from scripts/holding_audit.py)
        drops = json.loads(pathlib.Path(options[options.index("--drop-holdings") + 1]).read_text())
        for d in drops["dropped"]:
            per.pop((d["idea"], d["person"]), None)
    chosen = {pair: majority(items) for pair, items in per.items()}
    count = Counter(pair[1] for pair in chosen)
    core_ids = (
        {p["id"] for p in json.loads(pathlib.Path(core_path).read_text())["people"]}
        if core_path
        else None
    )
    drawn = (
        json.loads(pathlib.Path(options[options.index("--schools") + 1]).read_text())
        if "--schools" in options
        else None
    )
    # core voices draw the schools and need more evidence; others are only placed by agreement
    keep = {
        p
        for p, n in count.items()
        if n >= MIN_HOLDINGS or (core_ids is not None and p not in core_ids and n >= MIN_PLACED)
    }
    if drawn is not None:
        # schools drawn from the audited stances (scripts/draw_schools.py): everyone placed there
        keep = {p for p in drawn["people"] if p in count}
    dropped = sorted(names[p] for p in names if p in {*count} and p not in keep)
    chosen = {pair: h for pair, h in chosen.items() if pair[1] in keep}

    holdings = [Holding(p, idea, h["a"] > 0, h["inf"]) for (idea, p), h in chosen.items()]
    layer = {k: v["layer"] for k, v in meta.items()}
    idea_ids = sorted({idea for idea, _ in chosen})
    model = SentenceTransformer(MODEL)
    labels = families(similarity([meta[i] for i in idea_ids], data["links"], model), FAMILIES)
    family = dict(zip(idea_ids, labels, strict=True))
    # Schools and the layout come from the core: voices read deeply enough that silence isn't
    # mistaken for a view. Centring turns silence into "minus the average", so thinly read voices
    # look alike and would form a school of their own. Everyone else is placed by agreement.
    core = core_ids & keep if core_ids is not None else set(keep)
    if drawn is not None:
        core = {m for sc in drawn["schools"] for m in sc["members"]} & keep
    all_holdings = holdings
    holdings = [h for h in all_holdings if h.person in core]
    space = person_space(holdings, family)
    people = space.people
    if drawn is not None:
        groups = [[m for m in sc["members"] if m in core] for sc in drawn["schools"]]
        count = len(groups)
        count_info = {"count": count, "separation": drawn["checks"]["silhouette"],
                      "by_count": drawn["checks"]["by_count"]}  # fmt: skip
        stability = {frozenset(k.split("|")): v for k, v in drawn["together"].items()}
    else:
        count, count_info = choose_count(holdings, family)
        groups = sorted(schools(space, count), key=len, reverse=True)
        stability = school_stability(holdings, family, count, runs=500)
    points = layout(space)
    points = points - points.mean(0)
    k = SPREAD / max(float(np.percentile(np.abs(points), 92)), 1e-9)
    place = {p: points[i] * k for i, p in enumerate(people)}
    regroup = None
    if core_path and "--freeze-schools" in options:
        # Schools are fixed for the season, like the statements: keep the core atlas's members and
        # positions, and report how far the new evidence alone would regroup them.
        old = json.loads(pathlib.Path(core_path).read_text())
        frozen = [[m for m in s["members"] if m in place] for s in old["schools"]]
        frozen = sorted((g for g in frozen if g), key=len, reverse=True)
        now = schools(space, count)
        regroup = round(
            float(adjusted_rand_score(partition(frozen, people), partition(now, people))), 3
        )
        groups, count = frozen, len(frozen)
        stability = school_stability(holdings, family, count, runs=500)
        place = {
            p["id"]: np.array([p["x"], p["y"]], float) for p in old["people"] if p["id"] in place
        }
        points = np.array([place[p] for p in people])
    stated = {(idea, p): h["a"] for (idea, p), h in chosen.items() if not h["inf"]}
    placed_by: dict[str, list[tuple[str, float]]] = {}
    if drawn is not None:
        # one measure for place and school: everyone sits where the drawing put them
        place = {p: np.array([drawn["people"][p]["x"], drawn["people"][p]["y"]], float)
                 for p in keep}  # fmt: skip
        points = np.array([place[p] for p in people])
    for person in sorted(keep - core):
        result = place_by_agreement(person, stated, people, place, layer)
        if drawn is not None:
            placed_by[person] = result.top if result else []
            continue
        if result is None:
            dropped.append(names[person])
            continue
        place[person], placed_by[person] = result.xy, result.top
    dropped.sort()
    chosen = {pair: h for pair, h in chosen.items() if pair[1] in place}
    everyone = people + sorted(placed_by)
    full_space = person_space([h for h in all_holdings if h.person in place], family)

    def idea_xy(key: str) -> np.ndarray:
        held = [h for (idea, _), h in chosen.items() if idea == key]
        accept = [place[h["p"]] * (0.5 if h["inf"] else 1) for h in held if h["a"] > 0]
        reject = [place[h["p"]] for h in held if h["a"] < 0]
        centre = np.mean(accept, 0) if accept else -0.6 * np.mean(reject, 0)
        if accept and reject:
            centre = centre + 0.4 * (centre - np.mean(reject, 0))
        return centre

    raw = {i: idea_xy(i) for i in idea_ids}
    middle = {f: np.mean([raw[i] for i in idea_ids if family[i] == f], 0) for f in set(labels)}
    spots = {i: 0.6 * raw[i] + 0.4 * middle[family[i]] for i in idea_ids}

    links = [lk for lk in data["links"] if lk["from"] in idea_ids and lk["to"] in idea_ids]
    degree: Counter[str] = Counter()
    for lk in links:
        degree[lk["from"]] += 1
        degree[lk["to"]] += 1
    ideas_out = []
    for key in idea_ids:
        held = [h for (idea, _), h in chosen.items() if idea == key]
        years = [h["year"] for h in held if h["year"] and not h["inf"]]
        load = reasons_load(len(held), degree[key])
        ideas_out.append(
            {"id": key, "text": meta[key]["canonical"], "layer": meta[key]["layer"],
             "kind": meta[key]["tl_type"], "validity": meta[key]["validity"],
             "x": round(float(spots[key][0]), 1), "y": round(float(spots[key][1]), 1),
             "family": family[key], "year": min(years) if years else None,
             "holders": sorted(held, key=lambda h: -h["a"]),
             "reasons": round(load, 3), "link_count": degree[key],
             "inferred": all(h["inf"] for h in held)}
        )  # fmt: skip
    for item in ideas_out:
        for h in item["holders"]:
            if h["q"] and len(h["q"]) > 280:
                h["q"] = h["q"][:277] + "..."

    label_map = {tuple(sorted(s["members"])): s for s in copy.get("schools", [])}
    # a voice joins a school only on clear, distinctive evidence; otherwise it is shown as between
    # two schools, or as not yet grouped
    fitted = (
        {p: {"school": drawn["people"][p]["school"], "between": drawn["people"][p]["between"]}
         for p in placed_by}
        if drawn is not None
        else {p: school_fit(p, stated, groups, layer) for p in placed_by}
    )  # fmt: skip
    voted = {p: f["school"] for p, f in fitted.items()}
    schools_out = []
    for n, group in enumerate(groups):
        pairs = [stability.get(frozenset(p), 0) for p in itertools.combinations(group, 2)]
        known = next(
            (
                v
                for m, v in label_map.items()
                if set(m) & set(group)
                and len(set(m) & set(group)) >= max(1, len(group) // 2 + (len(group) > 1))
            ),
            None,
        )
        fallback = Counter(niche.get(p, "") for p in group).most_common(1)[0][0]
        schools_out.append(
            {"members": group,
             "provisional_members": sorted(p for p, v in voted.items() if v == n),
             "label": (known or {}).get("label", fallback if len(group) > 1 else ""),
             "note": (known or {}).get("note", ""),
             "cohesion": round(float(np.mean(pairs)), 3) if pairs else None}
        )  # fmt: skip

    table: dict[str, dict[str, int]] = defaultdict(dict)
    for (idea, person), h in chosen.items():
        if not h["inf"]:
            table[idea][person] = h["a"]
    forks = {}
    shown = [h for h in all_holdings if h.person in place]
    by_person: dict[str, dict[str, Holding]] = defaultdict(dict)
    for h in shown:
        by_person[h.person][h.idea] = h
    for a, b in itertools.combinations(everyone, 2):
        fork = fork_profile(a, b, shown, layer)
        mine, yours = by_person[a], by_person[b]
        overlap = mine.keys() & yours.keys()
        forks["|".join(sorted((a, b)))] = {
            "by_layer": fork.by_layer, "lowest_opposed": fork.lowest_opposed,
            "shared": sorted(i for i in overlap if mine[i].accepts == yours[i].accepts),
            "opposed": sorted(i for i in overlap if mine[i].accepts != yours[i].accepts),
            "stable": round(stability.get(frozenset({a, b}), 0), 3),
        }  # fmt: skip

    named = [(i, s) for i, s in enumerate(schools_out) if len(s["members"]) > 1]

    def compare(first: list[str], second: list[str]) -> dict:
        """Two camps, compared over families within each layer, with direct ideas listed."""
        by = {name: [0, 0] for name in LAYERS}
        one, two = defaultdict(int), defaultdict(int)
        shared, opposed = [], []
        for idea, row in table.items():
            mine = [row[m] for m in first if m in row]
            yours = [row[m] for m in second if m in row]
            one[(layer[idea], family[idea])] += sum(mine)
            two[(layer[idea], family[idea])] += sum(yours)
            if mine and yours and sum(mine) * sum(yours) != 0:
                (shared if sum(mine) * sum(yours) > 0 else opposed).append(idea)
        for cell in one.keys() & two.keys():
            if one[cell] * two[cell] != 0:
                by[cell[0]][0 if one[cell] * two[cell] > 0 else 1] += 1
        lowest = next((n for n in LAYERS if by[n][1]), None)
        return {"by_layer": by, "lowest_opposed": lowest, "shared": shared, "opposed": opposed}

    lenses = [{**lens, **compare(lens["a"], lens["b"])} for lens in copy.get("lenses", [])]

    # Honesty checks.
    stated_only = [h for h in holdings if not h.inferred]
    stated_space = person_space(stated_only, family)
    ablate = adjusted_rand_score(
        partition(groups, stated_space.people),
        partition(schools(stated_space, count), stated_space.people),
    )
    root_ideas = [i for i in idea_ids if layer[i] in ROOT_LAYERS]
    inferred_roots = [i["id"] for i in ideas_out if i["inferred"]]

    texts: dict[str, list[str]] = defaultdict(list)
    for c in rows:
        if c[1] in people and c[7]:
            texts[c[1]].append(c[7])
    for person in people:  # voices read only for the stances: use their audited quotes
        if not texts[person]:
            texts[person] = [h["q"] for (_, p), h in chosen.items() if p == person and h["q"]]
    means = np.array(
        [model.encode(texts[p][:200], normalize_embeddings=True).mean(0) for p in people]
    )
    curated = [niche.get(p, "?") for p in people]
    repeated = [i for i, n in enumerate(curated) if curated.count(n) > 1]
    tags = [curated[i] for i in repeated]
    embed_d = squareform(pdist(means[repeated], "cosine"))
    embed_sil = float(silhouette_score(embed_d, tags, metric="precomputed"))
    struct_d = space.distance[np.ix_(repeated, repeated)]
    struct_sil = float(silhouette_score(struct_d, tags, metric="precomputed"))
    embed_groups = _embedding_groups(means, people, count)
    embed_ari = float(adjusted_rand_score(partition(groups, people), embed_groups))

    # Sense forks between the two largest named schools that use a term.
    bodies: dict[str, str] = defaultdict(str)
    for seed in SEEDS:
        if not pathlib.Path(seed).exists():
            continue
        for work in json.loads(pathlib.Path(seed).read_text())["works"]:
            path = pathlib.Path(f"data/texts/{work['key']}.txt")
            if work["author"] in people and path.exists():
                bodies[work["author"]] += "\n" + path.read_text()
    senses = []
    for term in TERMS:
        best = None
        for x, y in itertools.combinations(named[:6], 2):
            a = [s for m in x[1]["members"] for s in sentences(bodies[m], term)]
            b = [s for m in y[1]["members"] for s in sentences(bodies[m], term)]
            if len(a) < 6 or len(b) < 6:
                continue
            va = model.encode(a[:60], normalize_embeddings=True)
            vb = model.encode(b[:60], normalize_embeddings=True)
            result = sense_fork({"a": va, "b": vb})
            if result and (best is None or result.distance > best[0].distance):
                ca, cb = va.mean(0), vb.mean(0)
                best = (result, x[1]["label"], y[1]["label"],
                        a[int(np.argmax(va @ ca))], b[int(np.argmax(vb @ cb))])  # fmt: skip
        if best:
            senses.append(
                {"term": term, "distance": round(best[0].distance, 3), "p": round(best[0].p, 4),
                 "fork": best[0].p < 0.01, "a_label": best[1], "b_label": best[2],
                 "a_example": best[3], "b_example": best[4]}
            )  # fmt: skip
    senses.sort(key=lambda s: -s["distance"])

    median = float(np.median([i["reasons"] for i in ideas_out]))
    belonging = [
        i["id"]
        for i in sorted(ideas_out, key=lambda i: (i["reasons"], -len(i["holders"])))
        if len(i["holders"]) >= 5 and i["reasons"] <= median / 2
    ][:12]
    for item in ideas_out:
        item["carries"] = (
            "belonging"
            if item["id"] in belonging
            else "reasons"
            if item["reasons"] > median * 2
            else ""
        )

    works = defaultdict(set)
    for h in chosen.values():
        works[h["p"]].add(h["work"])
    nearest = {p: [o for o, _ in top] for p, top in placed_by.items()}
    for p in people:
        scored = sorted(
            ((forks["|".join(sorted((p, o)))]["stable"], o) for o in people if o != p), reverse=True
        )
        nearest[p] = [o for _, o in scored[:3]]
    columns = sorted(set(labels))
    row = {p: i for i, p in enumerate(full_space.people)}
    family_scores = {
        p: {
            str(f): round(float(full_space.matrix[row[p], n]), 2)
            for n, f in enumerate(columns)
            if abs(full_space.matrix[row[p], n]) > 0.8
        }
        for p in everyone
    }
    groups_label = [s["label"] for s in schools_out]
    people_out = [
        {"id": p, "name": names[p], "niche": niche.get(p, ""),
         "x": round(float(place[p][0]), 1), "y": round(float(place[p][1]), 1),
         "families": family_scores[p], "works": sorted(works[p]), "nearest": nearest[p],
         **({"provisional": True} if p in placed_by else {}),
         **({"between": [groups_label[n] for n in fitted[p]["between"]]}
            if p in fitted and fitted[p]["between"] else {})}
        for p in everyone
    ]  # fmt: skip
    years = [i["year"] for i in ideas_out if i["year"]]
    fid = fidelity(space.matrix, points, neighbours=4)
    three_share = float(space.explained[:3].sum())
    checks = {
        "layout_fidelity": round(fid, 3), "three_axes_share": round(three_share, 3),
        **count_info, "stated_only_rand": round(float(ablate), 3),
        "embedding_silhouette": round(embed_sil, 3), "structure_silhouette": round(struct_sil, 3),
        "embedding_school_rand": round(embed_ari, 3), "inferred_roots": len(inferred_roots),
        "root_ideas": len(root_ideas),
        "fill": round(len(chosen) / (len(everyone) * len(idea_ids)), 3),
        "core_voices": len(people), "placed_by_agreement": len(placed_by),
        **({"schools_frozen": True, "regroup_rand": regroup} if regroup is not None else {}),
        "review": {**data.get("review", {}), "root_total":
                   data["review"]["root_kept"] + data["review"]["root_dropped"]},
    }  # fmt: skip
    family_out = []
    names_given = copy.get("families", {})
    for f in columns:
        members = [i for i in ideas_out if i["family"] == f]
        members.sort(key=lambda i: -len(i["holders"]))
        family_out.append(
            {"id": f, "name": names_given.get(str(f), members[0]["text"][:48]),
             "size": len(members), "x": round(float(middle[f][0]), 1),
             "y": round(float(middle[f][1]), 1), "ideas": [i["id"] for i in members]}
        )  # fmt: skip
    atlas = {
        "meta": {"first_year": min(years), "last_year": max(years)},
        "people": people_out, "ideas": ideas_out,
        "links": [
            {"s": lk["from"], "t": lk["to"], "type": lk["type"], "source": lk["source"],
             "conf": lk["confidence"]} for lk in links
        ],
        "families": family_out, "schools": schools_out, "forks": forks, "lenses": lenses,
        "senses": senses,
        "belonging": belonging, "dropped": dropped, "rawChecks": checks,
        "checks": [
            {"name": c["name"], "result": c["template"].format(**checks)}
            for c in copy.get("checks", [])
        ],
        "copy": copy,
    }  # fmt: skip
    pathlib.Path(output).write_text(json.dumps(atlas, ensure_ascii=False, indent=0))
    print(json.dumps(checks, indent=1))
    for s in schools_out:
        print(s["label"], s["cohesion"], [names[m] for m in s["members"]],
              "+", [names[m] for m in s["provisional_members"]])  # fmt: skip
    for lens in lenses:
        print(lens["label"], lens["by_layer"], lens["lowest_opposed"])


if __name__ == "__main__":
    main(*sys.argv[1:])
