"""Merge a finished two-reader stance batch into the atlas and report what changed.

Usage: apply_anchor_stances.py <batch> <atlas in> <atlas out>
"""

import json
import pathlib
import sys
from collections import Counter

from arena_fingerprint.anchors import stated_stances
from arena_fingerprint.stances import merge


def coverage(atlas: dict, statements: list[str]) -> Counter:
    ideas = {i["id"]: i for i in atlas["ideas"]}
    out: Counter = Counter()
    for s in statements:
        out.update(stated_stances(ideas[s]).keys())
    return out


def main(batch: str, source: str, target: str) -> None:
    queue, results = pathlib.Path("evals/queue") / batch, pathlib.Path("evals/results") / batch
    tasks = {p.stem: json.loads(p.read_text()) for p in sorted(queue.glob("*.json"))}
    readings = {}
    for path in sorted(results.glob("[AB]-*.json")):
        reader, person = path.stem.split("-", 1)
        readings[(reader, person)] = json.loads(path.read_text())
    missing = [p for p in tasks for r in "AB" if (r, p) not in readings]
    atlas = json.loads(pathlib.Path(source).read_text())
    statements = [s["id"] for s in next(iter(tasks.values()))["statements"]]
    before = coverage(atlas, statements)
    merged, report = merge(atlas, tasks, readings)
    after = coverage(merged, statements)
    pathlib.Path(target).write_text(json.dumps(merged, ensure_ascii=False, indent=0))
    lines = [f"# {batch}: stances on the season statements", ""]
    if missing:
        lines.append(f"Missing readings: {missing}")
    lines += ["| Person | Before | After | Added |", "|---|---|---|---|"]
    added = Counter(p for p, _, _ in report.added)
    for person in sorted(tasks):
        lines.append(f"| {person} | {before[person]} | {after[person]} | {added[person]} |")
    agreed = len(report.added) + len(report.agreed_existing)
    total = agreed + len(report.readers_disagree) + len(report.one_reader_only)
    lines += [
        "",
        f"- Both readers agreed: {agreed} (of {total} statements either reader marked)",
        f"- Readers took opposite sides: {len(report.readers_disagree)} {report.readers_disagree}",
        f"- Only one reader marked: {len(report.one_reader_only)}",
        f"- Agreed with a stance the atlas already had: {len(report.agreed_existing)}",
        f"- Contradicted the atlas (kept the atlas): {report.conflicts_with_atlas}",
        f"- Failed code checks: {len(report.invalid)}",
        *[f"  - {i}" for i in report.invalid[:30]],
    ]
    (results / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:])
