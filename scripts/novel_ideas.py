"""Find shared ideas the original atlas lacks, from claims no existing idea covers (E7, part 2).

Usage: novel_ideas.py prepare | check | apply

prepare  claims of the atlas people that are far from every existing idea, grouped by theme, with
         the theme's existing ideas listed so writers don't duplicate them
check    turn the writers' new ideas into one blind-check item per holding
apply    keep a holding only if the blind checker agrees with the writer; keep an idea only if two
         or more people hold it; add the ideas to structure-v2

Writers follow prompts/ideas_v1.md (no roots this round). Nothing is ratified.
"""

import json
import pathlib
import sys

STRUCTURE = pathlib.Path("evals/results/structure-v2/structure.json")
PEOPLE = pathlib.Path("evals/queue/structure-v2/people.json")
QUEUE = pathlib.Path("evals/queue/ideas-v2")
RESULTS = pathlib.Path("evals/results/ideas-v2")
EMBED = "BAAI/bge-large-en-v1.5"
THEMES = {
    "mind": "the nature of intelligence, minds, consciousness, and what machines are",
    "risk": "catastrophic risk from AI, alignment, control, orthogonality, superintelligence",
    "progress": "technology, progress, growth, stagnation, acceleration, and the arc of history",
    "power": "who governs technology: states, companies, sovereignty, democracy, regulation",
    "ends": "what humans are for: flourishing, moral status, posthuman futures, meaning, value",
    "labor": "economy, work, capital, markets, inequality, and present harms to people",
    "knowing": "how we know: forecasting, expertise, science, truth, media, language, hype",
    "conflict": "geopolitics, war, China, nation, civilization, religion, and enemies",
}
UNCOVERED = 0.55  # a claim this far from every existing idea may hold a missing idea
MAX_PER_THEME = 260
CHECK_PARTS = 2


def prepare() -> None:
    import numpy as np
    from arena_core.db import get_engine
    from sentence_transformers import SentenceTransformer
    from sqlalchemy import text

    structure = json.loads(STRUCTURE.read_text())
    people = set(json.loads(PEOPLE.read_text()))
    with get_engine().connect() as c:
        rows = [
            r
            for r in c.execute(
                text(
                    "SELECT c.claim_id::text, c.speaker_person_id, p.display_name,"
                    " coalesce(c.proposed_canonical, c.claim_text), c.quote_public,"
                    " c.argument_role, c.proposed_layer::text, e.title"
                    " FROM claim c JOIN person p ON p.person_id = c.speaker_person_id"
                    " JOIN episode e USING (episode_id) WHERE c.gate_status = 'accepted'"
                    " AND c.tl_attitude NOT IN ('suspends', 'accepts_for_argument')"
                    " AND c.quote_public IS NOT NULL"
                )
            ).all()
            if r[1] in people
        ]
    model = SentenceTransformer(EMBED)
    ideas = structure["ideas"]
    idea_vectors = model.encode([i["canonical"] for i in ideas], normalize_embeddings=True)
    claim_vectors = model.encode([r[3] for r in rows], normalize_embeddings=True, batch_size=32)
    theme_vectors = model.encode(list(THEMES.values()), normalize_embeddings=True)
    nearest = (claim_vectors @ idea_vectors.T).max(1)
    theme_of = np.argmax(claim_vectors @ theme_vectors.T, axis=1)
    names = list(THEMES)
    QUEUE.mkdir(parents=True, exist_ok=True)
    total = 0
    for t, name in enumerate(names):
        picked = [n for n in range(len(rows)) if theme_of[n] == t and nearest[n] < UNCOVERED]
        # spread across people: round-robin so no single prolific author fills the task
        by_person: dict[str, list[int]] = {}
        for n in sorted(picked, key=lambda n: nearest[n]):
            by_person.setdefault(rows[n][1], []).append(n)
        chosen: list[int] = []
        while len(chosen) < MAX_PER_THEME and any(by_person.values()):
            for queue in by_person.values():
                if queue and len(chosen) < MAX_PER_THEME:
                    chosen.append(queue.pop(0))
        claims = [
            {"id": rows[n][0], "who": rows[n][2], "claim": rows[n][3], "quote": rows[n][4],
             "role": rows[n][5], "layer": rows[n][6], "work": rows[n][7]}
            for n in sorted(chosen, key=lambda n: rows[n][2])
        ]  # fmt: skip
        existing = [i["canonical"] for i in ideas if i.get("theme") == name]
        (QUEUE / f"theme-{name}.json").write_text(
            json.dumps(
                {
                    "theme": name,
                    "about": THEMES[name],
                    "existing_ideas": existing,
                    "claims": claims,
                },
                indent=0,
            )  # fmt: skip
        )
        total += len(claims)
        print(name, len(picked), "uncovered,", len(claims), "queued")
    print(total, "claims queued for new ideas")


def check() -> None:
    items = []
    n = 20000
    for path in sorted(RESULTS.glob("ideas-*.json")):
        data = json.loads(path.read_text())
        task = json.loads((QUEUE / f"theme-{data['theme']}.json").read_text())
        claims = {c["id"]: c for c in task["claims"]}
        for idea in data.get("ideas", []):
            for h in idea.get("holdings", []):
                claim = claims.get(h["claim"])
                if claim is None:
                    continue
                items.append({"n": n, "idea": idea["canonical"], "who": claim["who"],
                              "quote": claim["quote"], "work": claim["work"],
                              "_key": f"{data['theme']}/{idea['key']}", "_claim": h["claim"],
                              "_attitude": h["attitude"]})  # fmt: skip
                n += 1
    (QUEUE / "check-key.json").write_text(json.dumps(items, indent=0))
    public = [{k: v for k, v in i.items() if not k.startswith("_")} for i in items]
    size = len(public) // CHECK_PARTS + 1
    for part in range(CHECK_PARTS):
        (QUEUE / f"check-{part}.json").write_text(
            json.dumps(public[part * size : (part + 1) * size], indent=0)
        )
    print(len(items), "holdings to check in", CHECK_PARTS, "parts")


def apply() -> None:
    structure = json.loads(STRUCTURE.read_text())
    items = json.loads((QUEUE / "check-key.json").read_text())
    verdicts = {}
    for part in range(CHECK_PARTS):
        path = RESULTS / f"check-{part}.json"
        if path.exists():
            for v in json.loads(path.read_text())["verdicts"]:
                verdicts[v["n"]] = v["verdict"]
    owner = _owners()
    kept: dict[str, list[dict]] = {}
    for item in items:
        if verdicts.get(item["n"]) == item["_attitude"]:
            kept.setdefault(item["_key"], []).append(
                {"claim": item["_claim"], "attitude": item["_attitude"], "source": "ideas-v2"}
            )
    existing = {i["key"] for i in structure["ideas"]}
    added = dropped = 0
    for path in sorted(RESULTS.glob("ideas-*.json")):
        data = json.loads(path.read_text())
        for idea in data.get("ideas", []):
            holdings = kept.get(f"{data['theme']}/{idea['key']}", [])
            holders = {owner.get(h["claim"]) for h in holdings}
            if len(holders) < 2:
                dropped += 1
                continue
            key = idea["key"] if idea["key"] not in existing else f"{idea['key']}-2"
            existing.add(key)
            structure["ideas"].append({
                "key": key, "theme": data["theme"], "canonical": idea["canonical"],
                "layer": idea["layer"], "tl_type": idea.get("tl_type", "conceptual"),
                "validity": idea.get("validity", "truth"), "root": False,
                "holdings": holdings, "source": "ideas-v2",
            })  # fmt: skip
            added += 1
    review = structure.setdefault("review", {})
    review |= {
        "new_ideas_added": added, "new_ideas_dropped": dropped,
        "new_holdings_checked": len(items),
        "new_holdings_agreed": sum(len(v) for v in kept.values()),
    }  # fmt: skip
    STRUCTURE.write_text(json.dumps(structure, ensure_ascii=False, indent=0))
    print(f"{added} new ideas added, {dropped} dropped (fewer than two confirmed holders)")


def _owners() -> dict[str, str]:
    from arena_core.db import get_engine
    from sqlalchemy import text

    with get_engine().connect() as c:
        return {
            r[0]: r[1]
            for r in c.execute(text("SELECT claim_id::text, speaker_person_id FROM claim"))
        }


if __name__ == "__main__":
    {"prepare": prepare, "check": check, "apply": apply}[sys.argv[1]]()
