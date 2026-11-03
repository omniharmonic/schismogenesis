"""Merge two blind readers' stances on the season statements into the atlas (expansion step E6).

A stance is kept only when both readers give the same direction for the same statement, and each
cites a claim of that person whose quote contains the cited text verbatim (280 chars or fewer).
Existing stated stances in the atlas are never overwritten; conflicts are reported instead.
"""

import copy
from dataclasses import dataclass, field

MAX_QUOTE = 280
SIGN = {"hold": 1, "reject": -1}


@dataclass
class MergeReport:
    added: list[tuple[str, str, int]] = field(default_factory=list)
    agreed_existing: list[tuple[str, str]] = field(default_factory=list)
    conflicts_with_atlas: list[tuple[str, str]] = field(default_factory=list)
    readers_disagree: list[tuple[str, str]] = field(default_factory=list)
    one_reader_only: list[tuple[str, str, str]] = field(default_factory=list)
    invalid: list[str] = field(default_factory=list)


def valid_items(reading: dict, task: dict, report: MergeReport, reader: str) -> dict[str, dict]:
    """statement -> item, for items that pass the code checks."""
    statements = {s["id"] for s in task["statements"]}
    claims = {c["id"]: c for c in task["claims"]}
    out: dict[str, dict] = {}
    for item in reading.get("stances", []):
        where = f"{reader}/{task['person']}/{item.get('statement')}"
        claim = claims.get(item.get("claim_id", ""))
        quote = item.get("quote") or ""
        if item.get("statement") not in statements or item.get("stance") not in SIGN:
            report.invalid.append(f"{where}: unknown statement or stance")
        elif claim is None:
            report.invalid.append(f"{where}: cites a claim that isn't this person's")
        elif not quote or len(quote) > MAX_QUOTE or quote not in claim["quote"]:
            report.invalid.append(f"{where}: quote isn't a verbatim part of the claim")
        elif item["statement"] in out:
            report.invalid.append(f"{where}: statement answered twice")
        else:
            out[item["statement"]] = {**item, "claim": claim}
    return out


def merge(
    atlas: dict, tasks: dict[str, dict], readings: dict[tuple[str, str], dict]
) -> tuple[dict, MergeReport]:
    """readings: (reader, person) -> reading. Returns a new atlas and what happened."""
    report = MergeReport()
    out = copy.deepcopy(atlas)
    ideas = {i["id"]: i for i in out["ideas"]}
    for person, task in sorted(tasks.items()):
        a = valid_items(readings.get(("A", person), {}), task, report, "A")
        b = valid_items(readings.get(("B", person), {}), task, report, "B")
        for statement in sorted(set(a) | set(b)):
            if statement not in a or statement not in b:
                only = a.get(statement) or b[statement]
                report.one_reader_only.append((person, statement, only["stance"]))
                continue
            if a[statement]["stance"] != b[statement]["stance"]:
                report.readers_disagree.append((person, statement))
                continue
            sign = SIGN[a[statement]["stance"]]
            idea = ideas[statement]
            existing = [h for h in idea["holders"] if h["p"] == person and not h["inf"]]
            if existing:
                same = all((h["a"] > 0) == (sign > 0) for h in existing)
                (report.agreed_existing if same else report.conflicts_with_atlas).append(
                    (person, statement)
                )
                continue
            pick = min((a[statement], b[statement]), key=lambda i: len(i["quote"]))
            idea["holders"].append({
                "p": person, "a": sign, "inf": False, "q": pick["quote"],
                "url": pick["claim"]["url"], "work": pick["claim"]["work"], "year": None,
                "why": pick.get("why"), "source": "anchor-stances-v1",
            })  # fmt: skip
            report.added.append((person, statement, sign))
    return out, report
