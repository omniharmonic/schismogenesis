"""Check every quoted holding on the atlas in its source context (the second audit swarm).

Usage: holding_audit.py prepare <atlas.json> | apply

prepare  every stated holding the atlas shows (person, idea, side, quote), except those on the
         season statements (the stance audit covers them), grouped by source work into packs a
         validator can read in full (about 45,000 words each)
apply    collect the rulings; a holding is kept only when ruled `keep`; the dropped pairs go to
         seed/holding-audit-drops.json, which build_atlas.py --drop-holdings reads

Protocol: packages/arena_extract/src/arena_extract/prompts/holding_audit_v1.md. Earlier checks
already matched every quote verbatim, ran an entailment model and a blind second reader; this one
reads the source around the quote: who is speaking, and whether it is their own view.
"""

import json
import pathlib
import sys
from collections import defaultdict

QUEUE = pathlib.Path("evals/queue/holding-audit")
RESULTS = pathlib.Path("evals/results/holding-audit")
DROPS = pathlib.Path("seed/holding-audit-drops.json")
SEASON = pathlib.Path("seed/season-1.json")
SOURCES = ["seed/WORLDVIEW-CORE-SOURCES.json", "seed/AI-FUTURES-SOURCES.json",
           "seed/AI-FUTURES-SOURCES-v2.json", "seed/AI-FUTURES-SOURCES-v3.json"]  # fmt: skip
PACK_WORDS = 45_000


def works_by_url() -> dict[str, dict]:
    out = {}
    for f in SOURCES:
        if pathlib.Path(f).exists():
            for w in json.loads(pathlib.Path(f).read_text())["works"]:
                path = pathlib.Path(f"data/texts/{w['key']}.txt")
                if path.exists() and not w.get("exclude"):
                    out.setdefault(w["url"], {**w, "path": str(path),
                                              "words": len(path.read_text().split())})  # fmt: skip
    return out


def prepare(atlas_path: str) -> None:
    atlas = json.loads(pathlib.Path(atlas_path).read_text())
    season = {s["id"] for s in json.loads(SEASON.read_text())["statements"]}
    names = {p["id"]: p["name"] for p in atlas["people"]}
    works = works_by_url()
    by_work: dict[str, list[dict]] = defaultdict(list)
    missing = 0
    for idea in atlas["ideas"]:
        if idea["id"] in season:
            continue
        for h in idea["holders"]:
            if h["inf"] or not h.get("q"):
                continue
            w = works.get(h["url"])
            if w is None:
                missing += 1
                continue
            by_work[w["key"]].append(
                {"key": f"{h['p']}|{idea['id']}", "thinker": names.get(h["p"], h["p"]),
                 "idea": idea["text"], "side": "accepts" if h["a"] > 0 else "rejects",
                 "quote": h["q"]}
            )  # fmt: skip
    meta = {w["key"]: w for w in works.values()}
    packs: list[dict] = []
    for key in sorted(by_work, key=lambda k: -meta[k]["words"]):
        size = meta[key]["words"]
        target = next((p for p in packs if p["words"] + size <= PACK_WORDS), None)
        if target is None:
            target = {"words": 0, "works": []}
            packs.append(target)
        target["words"] += size
        target["works"].append({"work": key, "title": meta[key]["title"],
                                "author": meta[key]["author"], "path": meta[key]["path"],
                                "holdings": by_work[key]})  # fmt: skip
    QUEUE.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    for n, pack in enumerate(packs):
        (QUEUE / f"pack-{n:02d}.json").write_text(
            json.dumps({"pack": n, "works": pack["works"]}, indent=1, ensure_ascii=False)
        )
    total = sum(len(v) for v in by_work.values())
    print(f"{total} holdings from {len(by_work)} works in {len(packs)} packs; "
          f"{missing} holdings whose source text is excluded or missing")  # fmt: skip


def apply(*_: str) -> None:
    queued = {}
    for path in sorted(QUEUE.glob("pack-*.json")):
        for w in json.loads(path.read_text())["works"]:
            for h in w["holdings"]:
                queued[h["key"] + "|" + w["work"]] = h
    rulings = {}
    for path in sorted(RESULTS.glob("pack-*.json")):
        for r in json.loads(path.read_text()).get("rulings", []):
            rulings[r["key"] + "|" + r.get("work", "")] = r
    kept, dropped, unruled = 0, [], 0
    for key in queued:
        r = rulings.get(key)
        if r is None:
            unruled += 1
            continue
        if r.get("ruling") == "keep":
            kept += 1
        else:
            person, idea, _work = key.split("|")
            dropped.append({"person": person, "idea": idea, "ruling": r.get("ruling"),
                            "reason": r.get("reason", "")})  # fmt: skip
    out = {"protocol": "holding_audit_v1", "dropped": dropped}
    DROPS.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    by = defaultdict(int)
    for d in dropped:
        by[d["ruling"]] += 1
    print(f"{len(queued)} holdings: kept {kept}, dropped {len(dropped)} {dict(by)}, "
          f"no ruling {unruled}")  # fmt: skip


if __name__ == "__main__":
    command, *rest = sys.argv[1:]
    {"prepare": prepare, "apply": apply}[command](*rest)
