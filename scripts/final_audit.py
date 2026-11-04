"""Pre-launch audit of everything the site shows: stances, signature positions and groups.

Usage: final_audit.py prepare | report

prepare  writes packs to evals/queue/final-audit/ (never committed):
         stances-NN.json  every published stance on three statements, with the passage around
                          each quote, for a reader to judge against the statement as shown
         voices-NN.json   every thinker's signature positions, with their passages
         groups.json      the tree, each group's label and note, and every member's sides
report   reads evals/results/final-audit/*.json and prints the verdicts that need action.

Readers judge; nothing is changed automatically. Fixes go through the normal stance files.
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import stance_audit as audit  # noqa: E402

audit.SOURCES.extend(["seed/AI-FUTURES-SOURCES-v4.json", "seed/AI-FUTURES-SOURCES-v5.json"])
BUNDLE = pathlib.Path("apps/arena/public/fingerprint.json")
SEASON = pathlib.Path("seed/season-2.json")
QUEUE = pathlib.Path("evals/queue/final-audit")
RESULTS = pathlib.Path("evals/results/final-audit")
WINDOW = 900  # characters of context on each side of a quote


def _passage(raw: str, quote: str) -> str:
    """The quote with WINDOW characters either side, found by a normalised search."""
    n, q = audit.norm(raw), audit.norm(quote)
    at = n.find(q[:120])
    if at < 0:
        return ""
    return n[max(0, at - WINDOW) : at + len(q) + WINDOW]


def prepare() -> None:
    bundle = json.loads(BUNDLE.read_text())
    statements = {s["id"]: s for s in json.loads(SEASON.read_text())["statements"]}
    names = {t["id"]: t["name"] for t in bundle["thinkers"]}
    works = audit.works_by_author()
    by_url = {(a, w["url"].rstrip("/")): w for a, ws in works.items() for w in ws}

    def source(pid: str, item: dict) -> dict:
        w = by_url.get((pid, item["url"].rstrip("/")))
        if not w:
            return {"text_path": None, "passage": "", "found": False}
        passage = _passage(pathlib.Path(w["path"]).read_text(), item["q"])
        return {"text_path": w["path"], "passage": passage, "found": bool(passage)}

    QUEUE.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    ids = [a["id"] for a in bundle["anchors"]]
    for n in range(0, len(ids), 3):
        pack = []
        for sid in ids[n : n + 3]:
            s = statements[sid]
            rows = []
            for pid, st in sorted(bundle["stances"][sid].items()):
                rows.append({"thinker": pid, "name": names.get(pid, pid),
                             "side": "hold" if st["a"] == 1 else "reject",
                             "quote": st["q"], "work": st["work"], "url": st["url"],
                             **source(pid, st)})  # fmt: skip
            pack.append({"id": sid, "statement": s.get("display") or s["proposition"],
                         "meaning": s["proposition"], "stances": rows})  # fmt: skip
        out = QUEUE / f"stances-{n // 3:02d}.json"
        out.write_text(json.dumps(pack, indent=1, ensure_ascii=False))
    people = sorted(bundle["voices"])
    size = (len(people) + 3) // 4
    for k, chunk in enumerate(people[i : i + size] for i in range(0, len(people), size)):
        rows = [{"thinker": pid, "name": names.get(pid, pid),
                 "positions": [{**v, **source(pid, {"url": v["url"], "q": v["quote"]})}
                               for v in bundle["voices"][pid]]}
                for pid in chunk]  # fmt: skip
        (QUEUE / f"voices-{k:02d}.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    shown = {sid: statements[sid].get("display") or statements[sid]["proposition"] for sid in ids}
    sides = {pid: {sid: ("hold" if bundle["stances"][sid][pid]["a"] == 1 else "reject")
                   for sid in ids if pid in bundle["stances"][sid]} for pid in names}  # fmt: skip
    thinkers = {
        t["id"]: {"name": t["name"], "path": t.get("path"), "between": t.get("between"),
                  "sides_on_survey": sides[t["id"]]}
        for t in bundle["thinkers"]
    }  # fmt: skip
    groups = {"statements": shown, "tree": bundle["tree"], "thinkers": thinkers}
    (QUEUE / "groups.json").write_text(json.dumps(groups, indent=1, ensure_ascii=False))
    missing = sum(1 for f in QUEUE.glob("stances-*.json") for s in json.loads(f.read_text())
                  for r in s["stances"] if not r["found"])  # fmt: skip
    print(
        f"{len(ids)} statements in {(len(ids) + 2) // 3} packs; 4 voice packs; groups.json;"
        f" {missing} quotes not found in their text by a plain search"
    )


def report() -> None:
    for f in sorted(RESULTS.glob("*.json")):
        data = json.loads(f.read_text())
        flagged = [v for v in data.get("verdicts", []) if v.get("verdict") not in ("ok", None)]
        print(f"\n## {f.name}: {len(data.get('verdicts', []))} judged, {len(flagged)} flagged")
        for v in flagged:
            print(" ", json.dumps(v, ensure_ascii=False))


if __name__ == "__main__":
    {"prepare": prepare, "report": report}[sys.argv[1]]()
