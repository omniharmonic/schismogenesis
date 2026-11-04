"""Merge the round-4 source drafts into seed/AI-FUTURES-SOURCES-v4.json (D-31.20).

Usage: merge_round4_sources.py [--gap]   (--gap: round 4b drafts -> seed/AI-FUTURES-SOURCES-v5.json)

Reads seed/drafts/sources-round4-*.json. Drops works whose URL or key is already listed in an
earlier source file, works by flagged landmarks, and works whose author is unknown. People keep
the researchers' notes and any conflict-of-interest flag, which goes to Benjamin's review list.
"""

import json
import pathlib

EARLIER = ["seed/WORLDVIEW-CORE-SOURCES.json", "seed/AI-FUTURES-SOURCES.json",
           "seed/AI-FUTURES-SOURCES-v2.json", "seed/AI-FUTURES-SOURCES-v3.json"]  # fmt: skip
OUT = pathlib.Path("seed/AI-FUTURES-SOURCES-v4.json")


def main(*flags: str) -> None:
    gap = "--gap" in flags
    out = pathlib.Path("seed/AI-FUTURES-SOURCES-v5.json") if gap else OUT
    pattern = "sources-round4b-*.json" if gap else "sources-round4-*.json"
    earlier = EARLIER + (["seed/AI-FUTURES-SOURCES-v4.json"] if gap else [])
    flagged = {f["landmark_id"] for f in json.loads(pathlib.Path("seed/SEED-v4.json").read_text())[
        "flags_for_benjamin"]["landmarks"]}  # fmt: skip
    seen_urls, seen_keys, known = set(), set(), set()
    for f in earlier:
        doc = json.loads(pathlib.Path(f).read_text())
        for w in doc["works"]:
            seen_urls.add(w["url"].rstrip("/"))
            seen_keys.add(w["key"])
            known.add(w["author"])
    people, works, skipped = {}, [], []
    for path in sorted(pathlib.Path("seed/drafts").glob(pattern)):
        doc = json.loads(path.read_text())
        for p in doc.get("people", []):
            if p["id"] in flagged:
                skipped.append(f"{p['id']}: flagged landmark")
                continue
            people[p["id"]] = {**p, "group": doc.get("group")}
        for w in doc.get("works", []):
            url = w["url"].rstrip("/")
            if w["author"] in flagged:
                skipped.append(f"{w['key']}: flagged author")
            elif url in seen_urls:
                skipped.append(f"{w['key']}: URL already listed")
            elif w["key"] in seen_keys:
                skipped.append(f"{w['key']}: key already used")
            elif w["author"] not in people and w["author"] not in known:
                skipped.append(f"{w['key']}: unknown author {w['author']}")
            else:
                seen_urls.add(url)
                seen_keys.add(w["key"])
                works.append(w)
    authors = {w["author"] for w in works}
    for pid in [p for p in people if p not in authors]:
        skipped.append(f"{pid}: no usable works")
        del people[pid]
    note = (
        "Round 4b (D-31.20): gap research, figures on the thin side of survey statements."
        if gap
        else "Round 4 (D-31.20, 2026-11-03): voices on AI and the social contract, "
        "whistleblowers and deepened thin voices."
    ) + " Found and byline-checked by source researchers; drafts in seed/drafts/."
    doc = {"note": note, "people": sorted(people.values(), key=lambda p: p["id"]), "works": works}
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(len(people), "people,", len(works), "works ->", out)
    for line in skipped:
        print("  skipped", line)


if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])
