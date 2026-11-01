"""Count memes and cited figures across full public texts, and sample passages for stance judging.

Usage: count_memes.py <output.json> <stance_tasks.json>
"""

import json
import pathlib
import random
import sys

from arena_map.memes import Work, compile_item, contexts, use_by_author

MAX_CONTEXTS = 3


def main(output: str, tasks_path: str) -> None:
    sources = json.loads(pathlib.Path("seed/WORLDVIEW-CORE-SOURCES.json").read_text())["works"]
    works = []
    for source in sources:
        body = pathlib.Path(f"data/full/{source['key']}.txt").read_text()
        year = int(source["published"][:4]) if source.get("published") else None
        works.append(Work(source["key"], source["author"], year, body, len(body.split())))
    items = json.loads(pathlib.Path("evals/results/memes-v1.json").read_text())
    rng = random.Random(20261101)
    tasks, counted = [], {"memes": [], "figures": []}
    for group, name_key in (("memes", "label"), ("figures", "name")):
        for item in items[group]:
            pattern = compile_item(item["patterns"])
            use = use_by_author(pattern, works)
            counted[group].append({**item, "use": use})
            for author, entry in use.items():
                passages = [
                    text
                    for work in works
                    if work.author == author
                    for text in contexts(pattern, work.text)
                ]
                rng.shuffle(passages)
                tasks.append({
                    "id": f"{group}|{item.get('key', item.get('name'))}|{author}",
                    "kind": "concept" if group == "memes" else "person",
                    "item": item[name_key],
                    "gloss": item.get("gloss", ""),
                    "author": author,
                    "uses": entry["uses"],
                    "passages": passages[:MAX_CONTEXTS],
                })  # fmt: skip
    pathlib.Path(output).write_text(json.dumps(counted, ensure_ascii=False))
    pathlib.Path(tasks_path).write_text(json.dumps(tasks, ensure_ascii=False, indent=0))
    print(len(tasks), sum(len(json.dumps(t)) for t in tasks))


if __name__ == "__main__":
    main(*sys.argv[1:])
