"""Round 4: every voice read on the full statement pool by two blind readers (D-31.20).

Usage: stance_round.py prepare | check | adjudicate | apply

The pool (seed/drafts/round4-pool.json) is the 24 season-1 statements plus candidates on AI and
the social contract. Every thinker, old and new, is read from all their texts on every pool
statement, so the instrument can be chosen from complete, comparable evidence
(scripts/instrument_check.py).

prepare     packs of thinkers (about PACK_WORDS of their own texts each) for blind readers A and B
check       every quote verbatim in that person's own text, valid ids; problems listed per file
adjudicate  a third reader for (1) stances only one reader found and (2) conflicts: the two
            readers disagree, or both agree against the earlier audited stance on a season-1
            statement (the earlier audit is an independent reading too)
apply       a stance counts when two independent readings agree: both blind readers, or one reader
            confirmed by the third. Where round 4 is silent on a season-1 statement, the earlier
            audited stance (itself two agreeing readings) is carried over while its quote still
            checks. Writes seed/drafts/round4-stances.json and updates seed/thinker-voices.json

Protocol: packages/arena_extract/src/arena_extract/prompts/stance_audit_v2.md, with
stance_adjudicate_v1.md and stance_conflict_v1.md for the third reader. Code checks quotes;
readers decide; nothing is ratified. Full texts stay in the git-ignored data/texts/.
"""

import importlib.util
import json
import pathlib
import sys
from collections import defaultdict

_spec = importlib.util.spec_from_file_location(
    "stance_audit", pathlib.Path(__file__).resolve().parent / "stance_audit.py"
)
assert _spec and _spec.loader
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)

audit.SOURCES.extend(["seed/AI-FUTURES-SOURCES-v4.json", "seed/AI-FUTURES-SOURCES-v5.json"])
POOL = pathlib.Path("seed/drafts/round4-pool.json")
SEASON1_STANCES = pathlib.Path("seed/season-1-stances.json")
QUEUE = pathlib.Path("evals/queue/round4/stances")
RESULTS = pathlib.Path("evals/results/round4/stances")
STANCES_OUT = pathlib.Path("seed/drafts/round4-stances.json")
VOICES_OUT = pathlib.Path("seed/thinker-voices.json")
PACK_WORDS = 55_000
FLAGGED_SEED = pathlib.Path("seed/SEED-v4.json")


def pool() -> list[dict]:
    return json.loads(POOL.read_text())["statements"]


def names() -> dict[str, str]:
    out = {t["id"]: t["name"] for t in json.loads(audit.BUNDLE.read_text())["thinkers"]}
    for f in audit.SOURCES:
        if pathlib.Path(f).exists():
            for p in json.loads(pathlib.Path(f).read_text()).get("people", []):
                out.setdefault(p["id"], p["name"])
    return out


def flagged() -> set[str]:
    flags = json.loads(FLAGGED_SEED.read_text())["flags_for_benjamin"]["landmarks"]
    return {f["landmark_id"] for f in flags}


def prepare(*args: str) -> None:
    """With `--works-from FILE --start N`, pack only that source file's works (a later round:
    each thinker is read on those new works only), numbered from pack N."""
    shown = [
        {"id": s["id"], "statement": s["display"], "meaning": s["proposition"]} for s in pool()
    ]
    works = audit.works_by_author()
    if "--works-from" in args:
        only = {
            w["key"]
            for w in json.loads(pathlib.Path(args[args.index("--works-from") + 1]).read_text())[
                "works"
            ]
        }
        works = {a: [w for w in ws if w["key"] in only] for a, ws in works.items()}
        works = {a: ws for a, ws in works.items() if ws}
    start = int(args[args.index("--start") + 1]) if "--start" in args else 0
    who = names()
    hidden = flagged()
    people = sorted(
        (i for i in works if i not in hidden), key=lambda i: -sum(w["words"] for w in works[i])
    )
    packs: list[list[dict]] = []
    for pid in people:
        size = sum(w["words"] for w in works[pid])
        target = next((p for p in packs if sum(x["words"] for x in p) + size <= PACK_WORDS), None)
        entry = {
            "id": pid,
            "name": who.get(pid, pid),
            "words": size,
            "works": [{k: w[k] for k in ("key", "title", "path")} for w in works[pid]],
        }
        if target is None:
            packs.append([entry])
        else:
            target.append(entry)
    QUEUE.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    for n, pack in enumerate(packs, start):
        (QUEUE / f"pack-{n:02d}.json").write_text(
            json.dumps(
                {"pack": n, "statements": shown, "thinkers": pack}, indent=1, ensure_ascii=False
            )
        )
    print(
        len(people),
        "thinkers in",
        len(packs),
        "packs;",
        sorted(sum(x["words"] for x in p) for p in packs),
    )
    missing = sorted(set(who) - set(works) - hidden)
    if missing and "--works-from" not in args:
        print("named but no texts:", missing)


CLASHES: dict[str, list[dict]] = {}  # same reader, opposite sides in two rounds


def _readings(texts: dict, owner: dict) -> tuple[dict, dict]:
    valid = {s["id"] for s in pool()}
    reads: dict[str, dict[str, dict]] = {"A": {}, "B": {}}
    voices: dict[str, list[dict]] = {}
    by: dict[str, str] = {}
    for reader in "AB":
        for path in sorted(RESULTS.glob(f"{reader}-pack-*.json")):
            for person in json.loads(path.read_text()).get("thinkers", []):
                pid = person["id"]
                for s in person.get("stances", []):
                    if (
                        s.get("statement") in valid
                        and s.get("stance") in ("hold", "reject")
                        and not audit.quote_problems("", s, pid, texts, owner)
                    ):
                        key = f"{pid}|{s['statement']}"
                        first = reads[reader].get(key)
                        if first and first["stance"] != s["stance"]:
                            CLASHES[key] = [first, s]  # a later, fuller reading disagrees
                        reads[reader].setdefault(key, s)
                good = [
                    v
                    for v in person.get("signature", [])
                    if v.get("position") and not audit.quote_problems("", v, pid, texts, owner)
                ]
                # signature positions come from the first full reading (reader A preferred);
                # a later round that read only a few new works never replaces them
                if good and (pid not in voices or (reader == "A" and by[pid] == "B")):
                    voices[pid], by[pid] = good, reader
    return reads, voices


def _context() -> tuple[dict, dict, dict]:
    texts = audit.load_texts()
    works = audit.works_by_author()
    owner = {w["key"]: a for a, ws in works.items() for w in ws}
    meta = {w["key"]: w for ws in works.values() for w in ws}
    return texts, owner, meta


def check(*args: str) -> None:
    """With a file name (e.g. A-pack-03.json), check only that file: readers stay blind."""
    texts, owner, _meta = _context()
    valid = {s["id"] for s in pool()}
    total = 0
    files = [RESULTS / a for a in args] if args else sorted(RESULTS.glob("*-pack-*.json"))
    for path in files:
        problems = audit.check_file(path, texts, valid, owner)
        total += len(problems)
        print(f"{path.name}: {'ok' if not problems else f'{len(problems)} problems'}")
        for p in problems:
            print("   ", p)
    print(total, "problems in all")


def _earlier() -> dict[str, dict]:
    old = json.loads(SEASON1_STANCES.read_text())["stances"]
    return {f"{p}|{s}": v for s, entry in old.items() for p, v in entry.items()}


def adjudicate(*_: str) -> None:
    texts, owner, meta = _context()
    reads, _voices = _readings(texts, owner)
    statements = {s["id"]: s for s in pool()}
    who = names()
    earlier = _earlier()
    singles, conflicts = [], []
    for key in sorted(reads["A"].keys() | reads["B"].keys()):
        a, b = reads["A"].get(key), reads["B"].get(key)
        pid, sid = key.split("|")
        base = {
            "key": key,
            "thinker": who.get(pid, pid),
            "statement": statements[sid]["display"],
            "meaning": statements[sid]["proposition"],
        }
        old = earlier.get(key)
        if key in CLASHES:
            conflicts.append(
                {
                    **base,
                    "readings": [_reading(r, meta) for r in CLASHES[key]]
                    + [_reading(r, meta) for r in (a, b) if r],
                }
            )
            continue
        if a and b and a["stance"] != b["stance"]:
            conflicts.append({**base, "readings": [_reading(a, meta), _reading(b, meta)]})
        elif a and b and old and (1 if a["stance"] == "hold" else -1) != old["a"]:
            conflicts.append({**base, "readings": [_reading(a, meta), _old_reading(old)]})
        elif not (a and b):
            s = a or b
            side = 1 if s["stance"] == "hold" else -1
            if old and side == old["a"]:
                continue  # one new reader agrees with the earlier audit: two independent readings
            if old:
                conflicts.append({**base, "readings": [_reading(s, meta), _old_reading(old)]})
                continue
            singles.append(
                {
                    **base,
                    "proposed": s["stance"],
                    "quote": s["quote"],
                    "why": s.get("why", ""),
                    "work": s["work"],
                    "path": meta[s["work"]]["path"],
                }
            )
    size = 30
    for label, items in (("adjudicate", singles), ("conflict", conflicts)):
        for n in range(0, len(items), size):
            (QUEUE / f"{label}-{n // size:02d}.json").write_text(
                json.dumps(items[n : n + size], indent=1, ensure_ascii=False)
            )
    print(len(singles), "single-reader stances;", len(conflicts), "conflicts")


def _reading(s: dict, meta: dict) -> dict:
    return {
        "stance": s["stance"],
        "quote": s["quote"],
        "why": s.get("why", ""),
        "work": s["work"],
        "path": meta[s["work"]]["path"],
    }


def _old_reading(old: dict) -> dict:
    return {
        "stance": "hold" if old["a"] > 0 else "reject",
        "quote": old["q"],
        "why": old.get("why", ""),
        "work_title": old["work"],
        "url": old["url"],
    }


def _conflict(
    key: str, new: dict, old: dict, ruled: str | None, agreed: dict, keep_old: set, counts: dict
) -> None:
    """A new reading against the earlier audit: the third reader decides; silent drops both."""
    if ruled == new["stance"]:
        agreed[key] = new
        counts["conflict_new_side"] += 1
    elif ruled == ("hold" if old["a"] > 0 else "reject"):
        keep_old.add(key)
        counts["conflict_earlier_side"] += 1
    else:
        counts["conflict_silent" if ruled else "conflict_unruled"] += 1


def apply(*_: str) -> None:
    texts, owner, meta = _context()
    reads, voices = _readings(texts, owner)
    rulings: dict[str, str] = {}
    for path in sorted(RESULTS.glob("adjudicate-*.json")) + sorted(RESULTS.glob("conflict-*.json")):
        for r in json.loads(path.read_text()).get("rulings", []):
            rulings[r["key"]] = r.get("ruling")
    earlier = _earlier()
    agreed: dict[str, dict] = {}
    keep_old: set[str] = set()
    counts: dict[str, int] = defaultdict(int)
    for key in reads["A"].keys() | reads["B"].keys():
        a, b = reads["A"].get(key), reads["B"].get(key)
        old = earlier.get(key)
        if key in CLASHES:
            ruled = rulings.get(key)
            pick = next((r for r in [*CLASHES[key], a, b] if r and r["stance"] == ruled), None)
            if pick:
                agreed[key], counts["clash_resolved"] = pick, counts["clash_resolved"] + 1
            else:
                counts["clash_silent"] += 1
            continue
        if a and b and a["stance"] == b["stance"]:
            if old and (1 if a["stance"] == "hold" else -1) != old["a"]:
                _conflict(key, a, old, rulings.get(key), agreed, keep_old, counts)
                continue
            agreed[key], counts["both"] = a, counts["both"] + 1
        elif a and b:
            ruled = rulings.get(key)
            pick = a if ruled == a["stance"] else b if ruled == b["stance"] else None
            if pick:
                agreed[key], counts["split_resolved"] = pick, counts["split_resolved"] + 1
            else:
                counts["split_silent"] += 1
        elif old and (1 if (a or b)["stance"] == "hold" else -1) == old["a"]:
            agreed[key], counts["single_matches_audit"] = a or b, counts["single_matches_audit"] + 1
        elif old:
            _conflict(key, a or b, old, rulings.get(key), agreed, keep_old, counts)
        elif rulings.get(key) == "confirm":
            agreed[key], counts["confirmed"] = a or b, counts["confirmed"] + 1
        else:
            counts["single_dropped"] += 1
    out: dict[str, dict[str, dict]] = defaultdict(dict)
    for key, s in sorted(agreed.items()):
        pid, sid = key.split("|")
        w = meta[s["work"]]
        out[sid][pid] = {
            "a": 1 if s["stance"] == "hold" else -1,
            "q": s["quote"],
            "url": w["url"],
            "work": w["title"],
            "year": (w.get("published") or "")[:4] or None,
            "why": s.get("why", ""),
            "basis": "round4",
        }
    # silent in round 4: carry the earlier audited stance while its quote is still in its source
    carried = 0
    by_url = {w["url"]: w for w in meta.values()}
    for key, old in earlier.items():
        pid, sid = key.split("|")
        if pid in out[sid] or (key in rulings and key not in keep_old):
            continue
        w = by_url.get(old["url"])
        if w and w["key"] in texts and audit.norm(old["q"]) in texts[w["key"]]:
            out[sid][pid] = {**old, "basis": "season-1 audit"}
            carried += 1
    STANCES_OUT.write_text(
        json.dumps(
            {
                "protocol": "stance_audit_v2",
                "rule": "two independent readings agree (both blind readers, or one reader "
                "and a third who checked the source); conflicts with the earlier audit go to "
                "a third reader; quotes checked verbatim in code",
                "stances": {k: dict(sorted(v.items())) for k, v in sorted(out.items())},
            },
            indent=1,
            ensure_ascii=False,
        )
    )
    old_voices = json.loads(VOICES_OUT.read_text()) if VOICES_OUT.exists() else {}
    for pid, vs in voices.items():
        old_voices[pid] = [
            {
                "position": v["position"],
                "quote": v["quote"],
                "url": meta[v["work"]]["url"],
                "work": meta[v["work"]]["title"],
            }
            for v in vs
        ]
    VOICES_OUT.write_text(
        json.dumps(dict(sorted(old_voices.items())), indent=1, ensure_ascii=False)
    )
    season1 = {s["id"] for s in pool() if s.get("origin") == "season-1"}
    now = {f"{p}|{s}": v["a"] for s, e in out.items() for p, v in e.items() if s in season1}
    kept = sum(1 for k, v in earlier.items() if now.get(k) == v["a"])
    flipped = sorted(k for k, v in earlier.items() if k in now and now[k] != v["a"])
    print(dict(counts), "carried from season-1 audit:", carried)
    print(
        f"season-1 statements vs earlier audit: kept {kept} of {len(earlier)}, flipped "
        f"{len(flipped)}, new {sum(1 for k in now if k not in earlier)}"
    )
    for k in flipped:
        print("  flipped", k)
    total = sum(len(v) for v in out.values())
    print(
        total,
        "stances on",
        len(out),
        "statements for",
        len({p for v in out.values() for p in v}),
        "thinkers",
    )
    report = {
        "counts": dict(counts),
        "carried": carried,
        "kept": kept,
        "flipped": flipped,
        "stances": total,
    }
    (RESULTS / "report.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    command, *rest = sys.argv[1:]
    {"prepare": prepare, "check": check, "adjudicate": adjudicate, "apply": apply}[command](*rest)
