"""Deterministic faithfulness validators.

Python port of Topology Live's validate.ts and lexicons.ts (omniharmonic/antidebate-live,
packages/ontology), same codes and word lists. `attribution_pending` is omitted: written sources
have a known author. Sources for names and numbers are the quote plus its paragraph, the "resolved
antecedents" of the original, because a written claim often says "the technology" for a name given
earlier in the paragraph.
"""

import re

from arena_extract.schema import ClaimItem

NON_ATTRIBUTABLE = {"attribute", "steelman_report", "nonliteral"}
NON_COMMITTING = {"question", "challenge", "meta"}
STRENGTH_RANK = {"tentative": 0, "leaning": 1, "confident": 2, "certain": 3}
QUANTIFIER_WIDTH = {
    "none": 0, "few": 1, "some": 2, "many": 3, "most": 4, "all": 5, "generic": 5,
}  # fmt: skip
HEDGES = [
    ("i'm not sure", "tentative"), ("not sure", "tentative"), ("i don't know", "tentative"),
    ("maybe", "tentative"), ("perhaps", "tentative"), ("possibly", "tentative"),
    ("might", "tentative"), ("could be", "tentative"), ("i wonder", "tentative"),
    ("i suspect", "leaning"), ("i think", "leaning"), ("i believe", "leaning"),
    ("i feel like", "leaning"), ("probably", "leaning"), ("likely", "leaning"),
    ("arguably", "leaning"), ("it seems", "leaning"), ("my guess", "leaning"),
    ("i'm fairly confident", "confident"), ("pretty sure", "confident"),
    ("i'm confident", "confident"),
]  # fmt: skip
HEDGE_NEUTRAL = ["you might say", "one might say", "if you will", "so to speak", "less likely",
                 "more likely"]  # fmt: skip
QUANTIFIER_NEUTRAL = ["in some ways", "in some sense", "to some extent", "some kind of",
                      "some sort of", "some form of", "the most", "at most", "at all",
                      "after all", "all right"]  # fmt: skip
QUANTIFIER_WORDS = [
    ("every", "all"), ("all", "all"), ("always", "all"), ("most", "most"), ("usually", "most"),
    ("many", "many"), ("often", "many"), ("some", "some"), ("sometimes", "some"),
    ("a few", "few"), ("few", "few"), ("rarely", "few"), ("no", "none"), ("never", "none"),
    ("none", "none"),
]  # fmt: skip
NUMBER = re.compile(
    r"\b\d+(?:[.,]\d+)?%?|\b(?:two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|fifty"
    r"|hundred|thousand|million|billion|percent)\b",
    re.IGNORECASE,
)
ENTITY = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace("’", "'").replace("‘", "'")).strip()


def _phrase(phrase: str) -> re.Pattern[str]:
    return re.compile(rf"(^|[^a-z']){re.escape(phrase)}(?=[^a-z']|$)")


def _strip(text: str, phrases: list[str]) -> str:
    for phrase in phrases:
        text = _phrase(phrase).sub(r"\1 ", text)
    return text


def strength_cap(quote: str) -> str:
    text = _strip(_norm(quote), HEDGE_NEUTRAL)
    cap = "certain"
    for phrase, limit in HEDGES:
        if _phrase(phrase).search(text) and STRENGTH_RANK[limit] < STRENGTH_RANK[cap]:
            cap = limit
    return cap


def lowered_strength(item: ClaimItem, quote: str) -> str:
    """Hedge inflation is repaired downward: lowering strength never adds content."""
    cap = strength_cap(quote)
    return cap if STRENGTH_RANK[item.strength] > STRENGTH_RANK[cap] else item.strength


def narrowest_quantifier(quote: str) -> str | None:
    text = _strip(_norm(quote), QUANTIFIER_NEUTRAL)
    found = None
    for word, quantifier in QUANTIFIER_WORDS:
        if _phrase(word).search(text) and (
            found is None or QUANTIFIER_WIDTH[quantifier] < QUANTIFIER_WIDTH[found]
        ):
            found = quantifier
    return found


def issues(item: ClaimItem, quote: str, paragraph: str = "") -> list[str]:
    source = _norm(f"{quote} {paragraph}")
    found = []
    if any(_norm(m) not in source for m in NUMBER.findall(item.proposed_canonical)):
        found.append("new_number")
    if any(_norm(m) not in source for m in ENTITY.findall(item.proposed_canonical)):
        found.append("new_entity")
    span_quantifier = narrowest_quantifier(quote)
    if (
        span_quantifier not in (None, "none")
        and QUANTIFIER_WIDTH[item.quantifier] > QUANTIFIER_WIDTH[span_quantifier]
    ):
        found.append("scope_widened")
    if item.source != "inferred":
        if item.speech_act in NON_ATTRIBUTABLE:
            found.append("non_attributable_stance")
        if item.speech_act in NON_COMMITTING:
            found.append("non_committing_stance")
    if item.speech_act == "rhetorical_question" and (
        item.source != "implied_by_act" or STRENGTH_RANK[item.strength] > STRENGTH_RANK["leaning"]
    ):
        found.append("rhetorical_overcommitted")
    return found
