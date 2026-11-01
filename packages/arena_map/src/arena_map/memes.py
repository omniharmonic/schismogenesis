"""Count memes and cited figures in public texts. Deterministic: no model involved."""

import re
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Work:
    key: str
    author: str
    year: int | None
    text: str
    words: int


def compile_item(patterns: list[str]) -> re.Pattern[str]:
    return re.compile("|".join(f"(?:{p})" for p in patterns), re.IGNORECASE)


def use_by_author(pattern: re.Pattern[str], works: list[Work]) -> dict[str, dict]:
    """Author -> uses, rate per 10,000 words, first year seen and the works it appears in."""
    words: dict[str, int] = defaultdict(int)
    found: dict[str, dict] = {}
    for work in works:
        words[work.author] += work.words
    for work in works:
        count = len(pattern.findall(work.text))
        if count == 0:
            continue
        entry = found.setdefault(work.author, {"uses": 0, "first": None, "works": []})
        entry["uses"] += count
        entry["works"].append(work.key)
        if work.year is not None and (entry["first"] is None or work.year < entry["first"]):
            entry["first"] = work.year
    for author, entry in found.items():
        entry["rate"] = round(entry["uses"] * 10000 / words[author], 2)
    return found


def contexts(pattern: re.Pattern[str], text: str, width: int = 240) -> list[str]:
    """The sentence-sized window around each hit, for judging stance toward what is mentioned."""
    return [text[max(m.start() - width, 0) : m.end() + width] for m in pattern.finditer(text)]
