"""Audit every thinker's stances on the season statements from their full texts (two blind readers).

Usage: stance_audit.py prepare | check | adjudicate | apply

prepare  one pack of thinkers per reader task (about 45,000 words of their own texts each), with
         the 24 statements as people see them; readers never see the current stances
check    verify each answer file: every quote verbatim in that person's own text, 280 characters
         or fewer, valid statement ids; prints problems per file so a reader can be re-asked
adjudicate  stances only one reader found go to a third reader, who reads the source around the
         quote and answers confirm, wrong_side or silent
         (evals/queue/stance-audit/adjudicate-*.json)
apply    keep a stance when both readers give the same side, or one reader gives it and the third
         reader confirms it; write the validated set to
         seed/season-1-stances.json and the signature positions to seed/thinker-voices.json,
         and report what changed against the current bundle

Protocol: packages/arena_extract/src/arena_extract/prompts/stance_audit_v1.md. Code checks quotes;
readers decide; nothing is ratified. Full texts stay in the git-ignored data/texts/.
"""

import json
import pathlib
import re
import sys
import unicodedata
from collections import defaultdict

BUNDLE = pathlib.Path("apps/arena/public/fingerprint.json")
SEASON = pathlib.Path("seed/season-1.json")
SOURCES = ["seed/WORLDVIEW-CORE-SOURCES.json", "seed/AI-FUTURES-SOURCES.json",
           "seed/AI-FUTURES-SOURCES-v2.json", "seed/AI-FUTURES-SOURCES-v3.json"]  # fmt: skip
QUEUE = pathlib.Path("evals/queue/stance-audit")
RESULTS = pathlib.Path("evals/results/stance-audit")
STANCES_OUT = pathlib.Path("seed/season-1-stances.json")
VOICES_OUT = pathlib.Path("seed/thinker-voices.json")
PACK_WORDS = 45_000
MAX_QUOTE = 280


def works_by_author() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    seen = set()
    for f in SOURCES:
        if not pathlib.Path(f).exists():
            continue
        for w in json.loads(pathlib.Path(f).read_text())["works"]:
            path = pathlib.Path(f"data/texts/{w['key']}.txt")
            if w["key"] in seen or not path.exists() or w.get("exclude") or w.get("duplicate_of"):
                continue
            seen.add(w["key"])
            out[w["author"]].append(
                {"key": w["key"], "title": w["title"], "url": w["url"],
                 "published": w.get("published"), "path": str(path),
                 "words": len(path.read_text().split())}
            )  # fmt: skip
    return out


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "—": "-",
                                         "–": "-", " ": " ", "…": "..."}))  # fmt: skip
    text = text.replace("**", "").replace("*", "")
    return re.sub(r"\s+", " ", text).strip().lower()


def prepare(*args: str) -> None:
    """With `--round r3 id id ...`, pack only those thinkers, as pack-r3-NN (a later round)."""
    round_name = args[args.index("--round") + 1] if "--round" in args else ""
    only = {a for a in args if not a.startswith("--") and a != round_name}
    bundle = json.loads(BUNDLE.read_text())
    statements = json.loads(SEASON.read_text())["statements"]
    shown = [{"id": s["id"], "statement": s.get("display") or s["proposition"],
              "meaning": s["proposition"]} for s in statements]  # fmt: skip
    works = works_by_author()
    names = {t["id"]: t["name"] for t in bundle["thinkers"]}
    ids = sorted(only or names, key=lambda i: -sum(w["words"] for w in works[i]))
    people = [{"id": i, "name": names.get(i, i)} for i in ids if works.get(i)]
    packs: list[list[dict]] = []
    for t in people:
        size = sum(w["words"] for w in works[t["id"]])
        target = next((p for p in packs if sum(x["words"] for x in p) + size <= PACK_WORDS), None)
        entry = {"id": t["id"], "name": t["name"], "words": size,
                 "works": [{k: w[k] for k in ("key", "title", "path")}
                           for w in works[t["id"]]]}  # fmt: skip
        if target is None:
            packs.append([entry])
        else:
            target.append(entry)
    QUEUE.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    for n, pack in enumerate(packs):
        tag = f"{round_name}-" if round_name else ""
        (QUEUE / f"pack-{tag}{n:02d}.json").write_text(
            json.dumps(
                {"pack": n, "statements": shown, "thinkers": pack}, indent=1, ensure_ascii=False
            )  # fmt: skip
        )
    print(len(packs), "packs;", [sum(x["words"] for x in p) for p in packs])


def load_texts() -> dict[str, str]:
    return {w["key"]: norm(pathlib.Path(w["path"]).read_text())
            for ws in works_by_author().values() for w in ws}  # fmt: skip


def check_file(
    path: pathlib.Path, texts: dict[str, str], valid: set[str], owner: dict[str, str]
) -> list[str]:
    problems = []
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"not JSON: {e}"]
    for person in data.get("thinkers", []):
        pid = person.get("id")
        for s in person.get("stances", []):
            where = f"{pid}/{s.get('statement')}"
            if s.get("statement") not in valid:
                problems.append(f"{where}: unknown statement id")
            if s.get("stance") not in ("hold", "reject"):
                problems.append(f"{where}: stance must be hold or reject")
            problems += quote_problems(where, s, pid, texts, owner)
        for v in person.get("signature", []):
            problems += quote_problems(f"{pid}/signature", v, pid, texts, owner)
    return problems


def quote_problems(where: str, item: dict, pid: str, texts: dict, owner: dict) -> list[str]:
    q, work = item.get("quote", ""), item.get("work")
    if owner.get(work) != pid:
        return [f"{where}: work {work!r} is not one of this person's works"]
    if not q or len(q) > MAX_QUOTE:
        return [f"{where}: quote missing or over {MAX_QUOTE} characters"]
    if norm(q) not in texts.get(work, ""):
        return [f"{where}: quote not found verbatim in {work}: {q[:80]!r}"]
    return []


def check(*_: str) -> None:
    texts = load_texts()
    valid = {s["id"] for s in json.loads(SEASON.read_text())["statements"]}
    owner = {w["key"]: a for a, ws in works_by_author().items() for w in ws}
    total = 0
    for path in sorted(RESULTS.glob("*.json")):
        problems = check_file(path, texts, valid, owner)
        total += len(problems)
        print(f"{path.name}: {'ok' if not problems else f'{len(problems)} problems'}")
        for p in problems:
            print("   ", p)
    print(total, "problems in all")


def adjudicate(*_: str) -> None:
    """Queue every stance only one reader found for a third, independent reading."""
    texts = load_texts()
    valid = {s["id"]: s for s in json.loads(SEASON.read_text())["statements"]}
    works = works_by_author()
    owner = {w["key"]: a for a, ws in works.items() for w in ws}
    path_of = {w["key"]: w["path"] for ws in works.values() for w in ws}
    reads: dict[str, dict[str, dict]] = {"A": {}, "B": {}}
    for reader in "AB":
        for path in sorted(RESULTS.glob(f"{reader}-pack-*.json")):
            for person in json.loads(path.read_text()).get("thinkers", []):
                for s in person.get("stances", []):
                    if (
                        s.get("statement") in valid
                        and s.get("stance") in ("hold", "reject")
                        and not quote_problems("", s, person["id"], texts, owner)
                    ):
                        reads[reader][f"{person['id']}|{s['statement']}"] = s
    names = {t["id"]: t["name"] for t in json.loads(BUNDLE.read_text())["thinkers"]}
    items = []
    for key in sorted(reads["A"].keys() ^ reads["B"].keys()):
        s = reads["A"].get(key) or reads["B"][key]
        pid, statement = key.split("|")
        items.append({"key": key, "thinker": names.get(pid, pid),
                      "statement": valid[statement].get("display")
                      or valid[statement]["proposition"],
                      "meaning": valid[statement]["proposition"], "proposed": s["stance"],
                      "quote": s["quote"], "why": s.get("why", ""), "work": s["work"],
                      "path": path_of[s["work"]]})  # fmt: skip
    size = 30
    for n in range(0, len(items), size):
        (QUEUE / f"adjudicate-{n // size:02d}.json").write_text(
            json.dumps(items[n : n + size], indent=1, ensure_ascii=False)
        )
    print(len(items), "single-reader stances in", (len(items) + size - 1) // size, "files")


def apply(*_: str) -> None:
    texts = load_texts()
    valid = {s["id"] for s in json.loads(SEASON.read_text())["statements"]}
    works = works_by_author()
    owner = {w["key"]: a for a, ws in works.items() for w in ws}
    meta = {w["key"]: w for ws in works.values() for w in ws}
    reads: dict[str, dict[str, dict]] = {"A": {}, "B": {}}
    voices: dict[str, list[dict]] = defaultdict(list)
    for reader in "AB":
        for path in sorted(RESULTS.glob(f"{reader}-pack-*.json")):
            for person in json.loads(path.read_text()).get("thinkers", []):
                pid = person["id"]
                # files sort round 1 (pack-00) before later rounds (pack-r3-00): a later round
                # read all of this thinker's works, so it replaces the earlier reading
                for old in [k for k in reads[reader] if k.startswith(pid + "|")]:
                    del reads[reader][old]
                for s in person.get("stances", []):
                    if (
                        s.get("statement") in valid
                        and s.get("stance") in ("hold", "reject")
                        and not quote_problems("", s, pid, texts, owner)
                    ):
                        reads[reader][f"{pid}|{s['statement']}"] = s
                if reader == "A":
                    voices[pid] = [v for v in person.get("signature", [])
                                   if not quote_problems("", v, pid, texts, owner)]  # fmt: skip
    agreed, split, single = {}, [], []
    for key in reads["A"].keys() | reads["B"].keys():
        a, b = reads["A"].get(key), reads["B"].get(key)
        if a and b and a["stance"] == b["stance"]:
            agreed[key] = a
        elif a and b:
            split.append(key)
        else:
            single.append(key)
    # a stance one reader found counts only if the third reader, reading the source, confirms it
    rulings = {}
    for path in sorted(RESULTS.glob("adjudicate-*.json")):
        for r in json.loads(path.read_text()).get("rulings", []):
            rulings[r["key"]] = r.get("ruling")
    confirmed = 0
    for key in single:
        if rulings.get(key) == "confirm":
            agreed[key] = reads["A"].get(key) or reads["B"][key]
            confirmed += 1
    out: dict[str, dict[str, dict]] = defaultdict(dict)
    for key, s in sorted(agreed.items()):
        pid, statement = key.split("|")
        w = meta[s["work"]]
        out[statement][pid] = {"a": 1 if s["stance"] == "hold" else -1, "q": s["quote"],
                               "url": w["url"], "work": w["title"],
                               "year": (w.get("published") or "")[:4] or None,
                               "why": s.get("why", "")}  # fmt: skip
    STANCES_OUT.write_text(json.dumps(
        {"protocol": "stance_audit_v1", "rule": "two independent readers of the full texts agree "
         "(both blind readers, or one reader and a third who checked the source); quotes "
         "checked verbatim in code", "stances": out}, indent=1, ensure_ascii=False))  # fmt: skip
    VOICES_OUT.write_text(json.dumps(
        {pid: [{"position": v["position"], "quote": v["quote"], "url": meta[v["work"]]["url"],
                "work": meta[v["work"]]["title"]} for v in vs]
         for pid, vs in sorted(voices.items())},
        indent=1, ensure_ascii=False))  # fmt: skip

    old = json.loads(BUNDLE.read_text())["stances"]
    before = {f"{p}|{s}": v["a"] for s, e in old.items() for p, v in e.items()}
    after = {k: (1 if v["stance"] == "hold" else -1) for k, v in agreed.items()}
    kept = sum(1 for k in before if after.get(k) == before[k])
    flipped = sorted(k for k in before if k in after and after[k] != before[k])
    dropped = sorted(k for k in before if k not in after)
    new = sorted(k for k in after if k not in before)
    print(
        f"agreed {len(agreed)} ({confirmed} confirmed by the third reader), split {len(split)}, "
        f"one reader only {len(single)}, rulings {len(rulings)}"
    )
    print(f"vs bundle: kept {kept}, flipped {len(flipped)}, dropped {len(dropped)}, new {len(new)}")
    for k in flipped:
        print("  flipped", k)
    report = {"agreed": len(agreed), "split": sorted(split), "single": len(single),
              "kept": kept, "flipped": flipped, "dropped": dropped, "new": new}  # fmt: skip
    (RESULTS / "report.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    command, *rest = sys.argv[1:]
    {"prepare": prepare, "check": check, "adjudicate": adjudicate, "apply": apply}[command](*rest)
