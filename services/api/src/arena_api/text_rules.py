"""Checks on participant-written statements (PRD R9). Each refusal says why, in plain words."""

import re

MIN_LEN = 10
MAX_LEN = 140
HANDLE = re.compile(r"(^|\s)@\w")
URL = re.compile(r"(https?://|www\.|\b[\w-]+\.(com|org|net|io|ai|xyz|co|gov|edu)\b)", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def normalise(text: str) -> str:
    return " ".join(re.sub(r"[^\w\s]", "", text.lower()).split())


def check_statement(text: str, existing: list[str]) -> str | None:
    """None if acceptable, otherwise the reason it was refused."""
    text = " ".join(text.split())
    if len(text) < MIN_LEN:
        return f"Statements need at least {MIN_LEN} characters."
    if len(text) > MAX_LEN:
        return f"Statements can be at most {MAX_LEN} characters."
    if EMAIL.search(text):
        return "Statements can't include email addresses."
    if HANDLE.search(text):
        return "Statements can't mention @handles. Write about ideas, not people in the room."
    if URL.search(text):
        return "Statements can't include links."
    key = normalise(text)
    if any(normalise(e) == key for e in existing):
        return "That statement is already in the room."
    return None
