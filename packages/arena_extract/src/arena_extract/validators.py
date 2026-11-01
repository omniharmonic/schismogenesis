"""Deterministic claim validators: the subset of 08 §4.8 needed so far.

Not yet ported: new_entity, scope_widened, attribution_pending.
"""

import re

from arena_extract.schema import ClaimItem

NON_COMMITTING = {"attribute", "steelman_report", "nonliteral", "question", "challenge", "meta"}
COMMITTING_ATTITUDES = {"accepts", "rejects", "accepts_conditionally"}
NUMBER = re.compile(r"\d[\d,.]*")
STRENGTH_ORDER = ["tentative", "leaning", "confident", "certain"]
HEDGE_CAPS = [
    (re.compile(r"\b(maybe|perhaps|possibly|might)\b", re.I), "tentative"),
    (re.compile(r"\b(i think|i believe|probably|likely|seems?)\b", re.I), "leaning"),
]


def strength_cap(quote: str) -> str:
    for pattern, cap in HEDGE_CAPS:
        if pattern.search(quote):
            return cap
    return "certain"


def lowered_strength(item: ClaimItem, quote: str) -> str:
    """Hedge inflation is repaired downward: lowering strength never adds content."""
    cap = strength_cap(quote)
    if STRENGTH_ORDER.index(item.strength) > STRENGTH_ORDER.index(cap):
        return cap
    return item.strength


def issues(item: ClaimItem, quote: str) -> list[str]:
    found = []
    if set(NUMBER.findall(item.proposed_canonical)) - set(NUMBER.findall(quote)):
        found.append("new_number")
    if item.speech_act in NON_COMMITTING and item.attitude in COMMITTING_ATTITUDES:
        found.append("non_committing_stance")
    if item.speech_act == "rhetorical_question" and (
        item.source != "implied_by_act"
        or STRENGTH_ORDER.index(item.strength) > STRENGTH_ORDER.index("leaning")
    ):
        found.append("rhetorical_overcommitted")
    return found
