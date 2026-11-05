"""Round 5 (2026-11-04): read more of each person, aimed at the statements they are silent on.

Usage: round5.py merge | prepare | check [file] | adjudicate | apply

merge       source drafts evals/queue/round5/sources-*.json -> seed/AI-FUTURES-SOURCES-v6.json,
            dropping URLs and keys already listed, flagged authors and unknown authors
            (then: fetch_texts.py seed/AI-FUTURES-SOURCES-v6.json --only-missing)
prepare     packs of the new works only, read on the 27 season-2 statements by blind readers A, B
check       quotes verbatim in that person's own text (same checker as round 4)
adjudicate  a third reader for stances only one reader found, and for any new reading that
            disagrees with a published (audited) stance
apply       additive: a new stance is added where two independent readings agree (both readers,
            or one confirmed by the third). Published stances are kept exactly as they are unless
            a third reader, shown both, sides with the new reading (then it is replaced, logged)
            or finds neither supported (then it is dropped, logged). New people get signature
            positions; people who have them keep theirs. Log: seed/round5-log.json.

Reuses scripts/stance_round.py with round-5 paths. Code checks quotes; readers decide; nothing is
ratified. Full texts stay in the git-ignored data/texts/.
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stance_round as sr  # noqa: E402

V6 = pathlib.Path("seed/AI-FUTURES-SOURCES-v6.json")
sr.audit.SOURCES.append(str(V6))
SEASON = pathlib.Path("seed/season-2.json")
PUBLISHED = [
    pathlib.Path("seed/season-2-stances.json"),
    pathlib.Path("seed/drafts/round4-stances.json"),
]
VOICES = pathlib.Path("seed/thinker-voices.json")
LOG = pathlib.Path("seed/round5-log.json")
SCRATCH = pathlib.Path("evals/results/round5")
sr.QUEUE = pathlib.Path("evals/queue/round5/stances")
sr.RESULTS = SCRATCH / "stances"
sr.SEASON1_STANCES = PUBLISHED[0]  # "earlier" = the published, audited stances
sr.STANCES_OUT = SCRATCH / "apply-stances.json"
sr.VOICES_OUT = SCRATCH / "apply-voices.json"


def _pool() -> list[dict]:
    return json.loads(SEASON.read_text())["statements"]


sr.pool = _pool


def merge(*_: str) -> None:
    earlier = sr.audit.SOURCES[:-1]
    flagged = sr.flagged()
    seen_urls, seen_keys, known = set(), set(), set()
    for f in earlier:
        if pathlib.Path(f).exists():
            for w in json.loads(pathlib.Path(f).read_text())["works"]:
                seen_urls.add(w["url"].rstrip("/"))
                seen_keys.add(w["key"])
                known.add(w["author"])
    works, skipped = [], []
    for path in sorted(pathlib.Path("evals/queue/round5").glob("sources-*.json")):
        for w in json.loads(path.read_text()).get("works", []):
            url = w["url"].rstrip("/")
            why = (
                "flagged author" if w["author"] in flagged
                else "URL already listed" if url in seen_urls
                else "key already used" if w["key"] in seen_keys
                else f"unknown author {w['author']}" if w["author"] not in known
                else None
            )  # fmt: skip
            if why:
                skipped.append(f"{w['key']}: {why}")
                continue
            seen_urls.add(url)
            seen_keys.add(w["key"])
            works.append({**w, "deliverable": "deepen"})
    doc = {
        "note": "Round 5 (2026-11-04): more of each person's own work, aimed at the survey "
        "statements they were silent on. Found and byline-checked by source researchers.",
        "people": [],
        "works": works,
    }
    V6.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(len(works), "works by", len({w["author"] for w in works}), "people ->", V6)
    for line in skipped:
        print("  skipped", line)


def prepare(*_: str) -> None:
    sr.prepare("--works-from", str(V6))


def _published() -> dict:
    return json.loads(PUBLISHED[0].read_text())


def apply(*_: str) -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    sr.VOICES_OUT.write_text("{}")
    sr.apply()
    result = json.loads(sr.STANCES_OUT.read_text())["stances"]
    pub = _published()
    stances = pub["stances"]
    log: dict[str, list] = {"added": [], "replaced": [], "dropped": []}
    rulings = {}
    for path in sorted(sr.RESULTS.glob("adjudicate-*.json")) + sorted(
        sr.RESULTS.glob("conflict-*.json")
    ):
        for r in json.loads(path.read_text()).get("rulings", []):
            rulings[r["key"]] = r.get("ruling")
    for sid, entry in result.items():
        for pid, s in entry.items():
            old = stances.get(sid, {}).get(pid)
            if s.get("basis") == "season-1 audit":
                continue  # carried published stance, unchanged
            new = {**s, "basis": "round5"}
            if old is None:
                stances.setdefault(sid, {})[pid] = new
                log["added"].append({"statement": sid, "person": pid, "a": s["a"], "q": s["q"]})
            elif old["a"] != s["a"]:
                stances[sid][pid] = new
                log["replaced"].append({"statement": sid, "person": pid, "was": old, "now": new})
    for key, ruled in rulings.items():
        pid, sid = key.split("|")
        old = stances.get(sid, {}).get(pid)
        if old and old.get("basis") != "round5" and ruled in ("silent", "neither", "drop"):
            del stances[sid][pid]
            log["dropped"].append({"statement": sid, "person": pid, "was": old})
    pub["stances"] = {k: dict(sorted(v.items())) for k, v in sorted(stances.items())}
    for path in PUBLISHED:
        path.write_text(json.dumps(pub, indent=1, ensure_ascii=False))
    voices = json.loads(VOICES.read_text())
    fresh = json.loads(sr.VOICES_OUT.read_text())
    new_people = [pid for pid in fresh if pid not in voices]
    for pid in new_people:
        voices[pid] = fresh[pid]
    VOICES.write_text(json.dumps(dict(sorted(voices.items())), indent=1, ensure_ascii=False))
    log["new_voices"] = new_people
    LOG.write_text(json.dumps(log, indent=1, ensure_ascii=False) + "\n")
    print(
        f"added {len(log['added'])}, replaced {len(log['replaced'])}, "
        f"dropped {len(log['dropped'])}; signature positions for {len(new_people)} new people"
    )


if __name__ == "__main__":
    command, *rest = sys.argv[1:]
    {
        "merge": merge,
        "prepare": prepare,
        "check": sr.check,
        "adjudicate": sr.adjudicate,
        "apply": apply,
    }[command](*rest)
