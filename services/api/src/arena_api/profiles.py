"""What a published profile may contain, checked against the bundle.

The summary is computed in the publisher's browser, so the server checks its shape and rebuilds
every piece of display text from the bundle. A profile can't put arbitrary words on the site.
"""

import secrets
import string

from pydantic import BaseModel, Field

CODE_ALPHABET = string.ascii_lowercase + string.digits
ANON_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


class Match(BaseModel):
    id: str
    k: int = Field(ge=0)
    n: int = Field(ge=1)


class Twist(BaseModel):
    anchor: str
    answer: int = Field(ge=-1, le=1)
    ally: str


class Camp(BaseModel):
    id: str
    agreed: int = Field(ge=0, le=100)
    opposed: int = Field(ge=0, le=100)
    deepest: str | None = None


class Rare(BaseModel):
    anchor: str
    answer: int = Field(ge=-1, le=1)


class Summary(BaseModel):
    home: str
    answered: int = Field(ge=0, le=100)
    nearest: list[Match] = Field(min_length=1, max_length=3)
    furthest: list[Match] = Field(default_factory=list, max_length=3)
    signature: list[Twist] = Field(default_factory=list, max_length=3)
    camps: list[Camp] = Field(default_factory=list, max_length=5)
    rarest: Rare | None = None


class SummaryError(ValueError):
    pass


def clean_summary(summary: Summary, bundle: dict) -> dict:
    thinkers = {t["id"] for t in bundle["thinkers"]}
    schools = {s["label"] for s in bundle["schools"]}
    anchors = {a["id"]: a["text"] for a in bundle["anchors"]}
    camps = {c["id"]: c["label"] for c in bundle["camps"]}
    layers = set(bundle["layers"])
    if summary.home not in schools:
        raise SummaryError("Unknown school.")
    for match in summary.nearest + summary.furthest:
        if match.id not in thinkers or match.k > match.n or match.n > len(anchors):
            raise SummaryError("A thinker match doesn't fit the statements.")
    for twist in summary.signature:
        if twist.anchor not in anchors or twist.ally not in schools or twist.answer == 0:
            raise SummaryError("A cross-cutting line doesn't fit the statements.")
    for camp in summary.camps:
        if camp.id not in camps or (camp.deepest is not None and camp.deepest not in layers):
            raise SummaryError("Unknown camp.")
    if summary.rarest and (summary.rarest.anchor not in anchors or summary.rarest.answer == 0):
        raise SummaryError("Unknown statement.")
    if summary.answered > len(anchors):
        raise SummaryError("More answers than statements.")
    return {
        "home": summary.home,
        "answered": summary.answered,
        "nearest": [m.model_dump() for m in summary.nearest],
        "furthest": [m.model_dump() for m in summary.furthest],
        "signature": [
            {**t.model_dump(), "text": anchors[t.anchor], "home": summary.home}
            for t in summary.signature
        ],
        "camps": [{**c.model_dump(), "label": camps[c.id]} for c in summary.camps],
        "rarest": None
        if summary.rarest is None
        else {**summary.rarest.model_dump(), "text": anchors[summary.rarest.anchor]},
    }


def clean_answers(answers: dict[str, int], bundle: dict) -> dict[str, int]:
    anchors = {a["id"] for a in bundle["anchors"]}
    if set(answers) - anchors or any(v not in (-1, 0, 1) for v in answers.values()):
        raise SummaryError("Answers don't fit the statements.")
    return dict(answers)


def clean_glyph(glyph: list[int | None], bundle: dict) -> list[int | None]:
    if len(glyph) != len(bundle["anchors"]) or any(v not in (-1, 0, 1, None) for v in glyph):
        raise SummaryError("The print doesn't fit the statements.")
    return glyph


def new_code() -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(8))


def anon_name() -> str:
    return "Fingerprint " + "".join(secrets.choice(ANON_ALPHABET) for _ in range(4))
