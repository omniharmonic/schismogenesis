"""Check claude_code_batch results against their tasks: schema, plus quotes present in the text."""

import json
import pathlib
import sys

import jsonschema


def main(batch: str, shard: str | None = None) -> int:
    queue = pathlib.Path("evals/queue") / batch
    results = pathlib.Path("evals/results") / batch
    ids = (
        pathlib.Path(shard).read_text().split() if shard else [p.stem for p in queue.glob("*.json")]
    )
    problems, claims = 0, 0
    for task_id in ids:
        task = json.loads((queue / f"{task_id}.json").read_text())
        path = results / f"{task_id}.json"
        if not path.exists():
            print(f"MISSING {task_id}")
            problems += 1
            continue
        result = json.loads(path.read_text())
        core = task["user"].split("CORE:\n", 1)[1].split("CONTEXT (do not quote):")[0]
        for output in result["outputs"]:
            try:
                jsonschema.validate(output, task["schema"])
            except jsonschema.ValidationError as error:
                print(f"SCHEMA {task_id}: {error.message[:120]}")
                problems += 1
                continue
            for item in output["items"]:
                claims += 1
                if item["quote"] not in core:
                    print(f"QUOTE {task_id}: {item['quote'][:80]}")
                    problems += 1
    print(f"{len(ids)} tasks, {claims} claims, {problems} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
