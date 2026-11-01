"""Keep only what two blind readings agree on. Writes structure.json with review counts.

Usage: finalize_structure.py <output.json>
"""

import json
import pathlib
import sys
from collections import Counter

QUEUE = pathlib.Path("evals/queue/structure-v1")
RESULTS = pathlib.Path("evals/results/structure-v1")


def verdicts(names: list[str]) -> dict[str, str]:
    out = {}
    for name in names:
        for item in json.loads((RESULTS / name).read_text())["verdicts"]:
            out[str(item["n"])] = item["verdict"]
    return out


def main(output: str) -> None:
    ideas = json.loads((RESULTS / "ideas-merged.json").read_text())
    first = json.loads((QUEUE / "check-holdings-key.json").read_text())
    rest = json.loads((QUEUE / "check-rest-key.json").read_text())
    seen = verdicts(["check-holdings-a.json", "check-holdings-b.json"])
    seen |= verdicts([f"check-rest-{n}.json" for n in range(4)])
    answers = {}
    for n, item in (first | rest).items():
        answers[(item["idea_key"], item["claim_id"])] = seen[n]
    roots = json.loads((QUEUE / "check-roots.json").read_text())
    root_verdicts = verdicts(["check-roots.json"])
    needed = {
        (r["idea_key"], r["claim_id"]) for r in roots if root_verdicts[str(r["n"])] == "needed"
    }

    tally: Counter[str] = Counter()
    kept_ideas = []
    for idea in ideas:
        kept = []
        for h in idea["holdings"]:
            pair = (idea["key"], h["claim"])
            if h.get("inferred"):
                tally["root_kept" if pair in needed else "root_dropped"] += 1
                if pair in needed:
                    kept.append(h)
                continue
            answer = answers.get(pair)
            if answer == h["attitude"]:
                tally["agreed"] += 1
                kept.append(h)
            elif answer == "neither":
                tally["second_reader_neither"] += 1
            else:
                tally["reversed"] += 1
        if kept:
            kept_ideas.append({**idea, "holdings": kept})
    keys = {i["key"] for i in kept_ideas}
    links = json.loads((RESULTS / "links-all.json").read_text())
    kept_links = [x for x in links if x["from"] in keys and x["to"] in keys]
    link_verdicts = verdicts(["check-links.json"])
    sample = json.loads((QUEUE / "check-links-key.json").read_text())
    attacks = {"rebuts", "undercuts", "undermines"}

    def valid(n: int, link: dict) -> bool:
        verdict = link_verdicts[str(n)]
        return verdict != "none" and (verdict == "attacks") == (link["type"] in attacks)

    agreed_links = sum(valid(n, x) for n, x in enumerate(sample))
    tally["links_checked"] = len(sample)
    tally["links_valid"] = agreed_links
    invalid = {(x["from"], x["to"]) for n, x in enumerate(sample) if not valid(n, x)}
    kept_links = [x for x in kept_links if (x["from"], x["to"]) not in invalid]
    tally["ideas_before"] = len(ideas)
    tally["ideas_after"] = len(kept_ideas)
    tally["links_after"] = len(kept_links)
    pathlib.Path(output).write_text(
        json.dumps({"ideas": kept_ideas, "links": kept_links, "review": dict(tally)}, indent=0)
    )
    print(dict(tally))


if __name__ == "__main__":
    main(*sys.argv[1:])
