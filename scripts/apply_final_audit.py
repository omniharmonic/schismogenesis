"""Apply the pre-launch audit (2026-11-04) to the audited stances and the signature positions.

Usage: apply_final_audit.py

Reads the readers' verdicts in evals/results/final-audit/. For each published survey stance:
  ok                         kept
  weak/wrong + better_quote  the quote is replaced (and the side, if the reader gives another),
                             but only when the new quote is found verbatim in one of that
                             figure's texts; the work and link follow the text it was found in
  weak/wrong, no better one  dropped: the bar is that the figure would sign what we show
For each signature position judged overstated, wrong or loaded, the reader's fairer rewrite
replaces our wording; the quote stays. Every change is logged to seed/final-audit-log.json.
Edits both seed/drafts/round4-stances.json and seed/season-2-stances.json (they are identical).
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import stance_audit as audit  # noqa: E402

audit.SOURCES.extend(["seed/AI-FUTURES-SOURCES-v4.json", "seed/AI-FUTURES-SOURCES-v5.json"])
RESULTS = pathlib.Path("evals/results/final-audit")
STANCE_FILES = [pathlib.Path("seed/drafts/round4-stances.json"),
                pathlib.Path("seed/season-2-stances.json")]  # fmt: skip
VOICES = pathlib.Path("seed/thinker-voices.json")
LOG = pathlib.Path("seed/final-audit-log.json")
# Letters lost in PDF extraction of Stuart Russell's Senate testimony (ligatures read as symbols)
DAMAGED = {"stuart-russell"}
REPAIRS = {"*": "ti", "$": "tt", "]": "ft", "M": "ti"}


def find_work(pid: str, quote: str, works: dict, texts: dict) -> dict | None:
    q = audit.norm(quote)
    return next((w for w in works.get(pid, []) if q in texts.get(w["key"], "")), None)


def repair(quote: str) -> str:
    """Fix ligature damage inside words only: a symbol (or a stray capital M) between letters."""
    import re

    out = re.sub(r"(?<=[a-z])[*$\]](?=[a-z])", lambda m: REPAIRS[m.group()], quote)
    out = re.sub(r"(?<=[a-z])5(?=[a-z])", "ti", out)
    return re.sub(r"(?<=[a-z])M(?=[a-z])", "ti", out)


def main() -> None:
    works = audit.works_by_author()
    texts = audit.load_texts()
    doc = json.loads(STANCE_FILES[0].read_text())
    voices = json.loads(VOICES.read_text())
    log: dict[str, list] = {"replaced": [], "dropped": [], "repaired": [], "rewritten": []}
    for f in sorted(RESULTS.glob("*.json")):
        for v in json.loads(f.read_text()).get("verdicts", []):
            if "statement" in v and v.get("verdict") not in (None, "ok"):
                sid, pid = v["statement"], v["thinker"]
                row = doc["stances"].get(sid, {}).get(pid)
                if not row:
                    continue
                better = v.get("better_quote")
                w = (
                    better
                    and len(better) <= audit.MAX_QUOTE
                    and find_work(pid, better, works, texts)
                )
                if w:
                    side = {"hold": 1, "reject": -1}.get(v.get("better_side") or "", row["a"])
                    doc["stances"][sid][pid] = {
                        **row,
                        "a": side,
                        "q": better,
                        "url": w["url"],
                        "work": w["title"],
                        "audit": "final-2026-11-04",
                    }
                    log["replaced"].append(
                        {
                            "statement": sid,
                            "thinker": pid,
                            "was": row["q"],
                            "now": better,
                            "side": side,
                            "why": v.get("reason"),
                        }
                    )
                else:
                    del doc["stances"][sid][pid]
                    log["dropped"].append(
                        {
                            "statement": sid,
                            "thinker": pid,
                            "quote": row["q"],
                            "verdict": v["verdict"],
                            "why": v.get("reason"),
                        }
                    )
            elif "position_index" in v and v.get("verdict") not in (None, "ok"):
                pid, i, new = v["thinker"], v["position_index"], v.get("suggested_position")
                if new and pid in voices and i < len(voices[pid]):
                    log["rewritten"].append(
                        {
                            "thinker": pid,
                            "was": voices[pid][i]["position"],
                            "now": new,
                            "verdict": v["verdict"],
                        }
                    )
                    voices[pid][i]["position"] = new
    for sid, rows in doc["stances"].items():
        for pid, row in rows.items():
            if pid not in DAMAGED:
                continue
            fixed = repair(row["q"])
            if fixed != row["q"]:
                log["repaired"].append(
                    {"statement": sid, "thinker": pid, "was": row["q"], "now": fixed}
                )
                row["q"] = fixed
    for pid, items in voices.items():
        for item in items if pid in DAMAGED else []:
            fixed = repair(item["quote"])
            if fixed != item["quote"]:
                log["repaired"].append({"thinker": pid, "was": item["quote"], "now": fixed})
                item["quote"] = fixed
    for path in STANCE_FILES:
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    VOICES.write_text(json.dumps(voices, indent=1, ensure_ascii=False) + "\n")
    LOG.write_text(json.dumps(log, indent=1, ensure_ascii=False) + "\n")
    print({k: len(v) for k, v in log.items()})


if __name__ == "__main__":
    main()
