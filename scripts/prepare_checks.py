"""Write blind check tasks: the reader sees no first-pass answer. Answers stay in key files.

Usage: prepare_checks.py holdings | links
"""

import json
import pathlib
import random
import sys

from arena_core.db import get_engine
from sqlalchemy import text

QUEUE = pathlib.Path("evals/queue/structure-v1")
RESULTS = pathlib.Path("evals/results/structure-v1")
HOLDINGS = 420
LINKS = 2000


def holdings(mode_rest: bool = False) -> None:
    ideas = json.loads((RESULTS / "ideas-merged.json").read_text())
    with get_engine().connect() as connection:
        rows = connection.execute(
            text(
                "SELECT c.claim_id::text, p.display_name, c.quote_public, c.proposed_canonical,"
                " c.tl_attitude::text, e.title FROM claim c JOIN person p"
                " ON p.person_id = c.speaker_person_id JOIN episode e USING (episode_id)"
            )
        ).all()
    claims = {r[0]: r for r in rows}
    stated, inferred = [], []
    for idea in ideas:
        for h in idea["holdings"]:
            item = {"idea_key": idea["key"], "idea": idea["canonical"], "claim_id": h["claim"]}
            who, quote, positive, attitude, work = claims[h["claim"]][1:]
            item |= {"who": who, "quote": quote, "work": work}
            if h.get("inferred"):
                inferred.append(item | {"necessity": h["necessity"]})
            else:
                stated.append(item | {"attitude": h["attitude"]})
    rejects = [h for h in stated if h["attitude"] == "rejects"]
    accepts = [h for h in stated if h["attitude"] == "accepts"]
    random.Random(11).shuffle(rejects)
    random.Random(12).shuffle(accepts)
    sample = rejects[:120] + accepts[: HOLDINGS - 120]
    random.Random(13).shuffle(sample)
    if mode_rest:
        old = json.loads((QUEUE / "check-holdings-key.json").read_text())
        seen = {(v["idea_key"], v["claim_id"]) for v in old.values()}
        rest = [h for h in stated if (h["idea_key"], h["claim_id"]) not in seen]
        restkey = {str(1000 + n): item for n, item in enumerate(rest)}
        (QUEUE / "check-rest-key.json").write_text(json.dumps(restkey, indent=0))
        tasks = [
            {"n": int(n), **{k: v[k] for k in ("idea", "who", "quote", "work")}}
            for n, v in restkey.items()
        ]
        size = len(tasks) // 4 + 1
        for part in range(4):
            name = f"check-rest-{part}.json"
            (QUEUE / name).write_text(json.dumps(tasks[part * size : (part + 1) * size], indent=0))
        print(len(tasks), "remaining")
        return
    key = {}
    tasks = []
    for n, item in enumerate(sample):
        key[str(n)] = item
        tasks.append({"n": n, **{k: item[k] for k in ("idea", "who", "quote", "work")}})
    half = len(tasks) // 2
    (QUEUE / "check-holdings-key.json").write_text(json.dumps(key, indent=0))
    (QUEUE / "check-holdings-a.json").write_text(json.dumps(tasks[:half], indent=0))
    (QUEUE / "check-holdings-b.json").write_text(json.dumps(tasks[half:], indent=0))
    roots = [{"n": n, **item} for n, item in enumerate(inferred)]
    (QUEUE / "check-roots.json").write_text(json.dumps(roots, indent=0))
    print(len(stated), "stated", len(inferred), "inferred", len(tasks), "sampled")


def links() -> None:
    ideas = {i["key"]: i for i in json.loads((RESULTS / "ideas-merged.json").read_text())}
    found = []
    for name in ("links-support.json", "links-attack.json"):
        found += json.loads((RESULTS / name).read_text())["links"]
    found = [x for x in found if x["from"] in ideas and x["to"] in ideas and x["from"] != x["to"]]
    (RESULTS / "links-all.json").write_text(json.dumps(found, indent=0))
    sample = random.Random(14).sample(found, min(LINKS, len(found)))
    tasks = [
        {"n": n, "a": ideas[x["from"]]["canonical"], "b": ideas[x["to"]]["canonical"]}
        for n, x in enumerate(sample)
    ]
    (QUEUE / "check-links-key.json").write_text(json.dumps(sample, indent=0))
    (QUEUE / "check-links.json").write_text(json.dumps(tasks, indent=0))
    print(len(found), "links", len(tasks), "sampled")


if __name__ == "__main__":
    {"holdings": holdings, "links": links, "rest": lambda: holdings(True)}[sys.argv[1]]()
