"""Quote anchoring (08 §4.8). The stored quote is always cut from the source, never model text."""

import re
import unicodedata
from dataclasses import dataclass

from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

_TRANS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-"})
_PUNCT = re.compile(r"[^\w\s']")


def normalize(s: str) -> tuple[str, list[int]]:
    """Return normalized text and a map from each normalized char index to the original index."""
    out, idx = [], []
    s_nfc = unicodedata.normalize("NFC", s)
    prev_space = True
    for i, ch in enumerate(s_nfc):
        ch = ch.translate(_TRANS).lower()
        if _PUNCT.match(ch):
            continue
        if ch.isspace():
            if prev_space:
                continue
            ch, prev_space = " ", True
        else:
            prev_space = False
        out.append(ch)
        idx.append(i)
    while out and out[-1] == " ":
        out.pop()
        idx.pop()
    return "".join(out), idx


@dataclass
class Anchor:
    char_start: int
    char_end: int
    match: str
    score: float


def locate(
    quote: str, text: str, fuzzy_min: float = 95.0, max_token_edits: int = 2
) -> Anchor | None:
    i = text.find(quote)
    if i >= 0:
        return Anchor(i, i + len(quote), "exact", 100.0)
    nq, _ = normalize(quote)
    nt, m = normalize(text)
    if not nq or not nt:
        return None
    j = nt.find(nq)
    if j >= 0:
        return Anchor(m[j], m[j + len(nq) - 1] + 1, "normalized", 100.0)
    al = fuzz.partial_ratio_alignment(nq, nt, score_cutoff=fuzzy_min)
    if al is None:
        return None
    located = nt[al.dest_start : al.dest_end]
    if Levenshtein.distance(nq.split(), located.split()) > max_token_edits:
        return None
    s, e = m[al.dest_start], m[al.dest_end - 1] + 1
    while s > 0 and text[s - 1].isalnum():
        s -= 1
    while e < len(text) and text[e].isalnum():
        e += 1
    return Anchor(s, e, "fuzzy", float(al.score))


def public_quote(quote: str, limit: int = 280) -> str:
    """Trim to the limit on a word boundary."""
    if len(quote) <= limit:
        return quote
    return quote[:limit].rsplit(" ", 1)[0]


def previous_sentence(text: str, char_start: int) -> str:
    """One sentence of context for the entailment premise."""
    sentences = re.split(r"(?<=[.!?])\s+", text[:char_start].strip())
    return sentences[-1] if sentences and sentences[-1] else ""
