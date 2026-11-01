"""Gold storage format: evals/gold/v<k>/{dev,test}/*.jsonl plus a SHA-256 manifest.

Files are canonical. The test split is sealed: reading it needs a stated purpose, which is logged.
"""

import datetime
import hashlib
import json
import pathlib
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, model_validator

Layer = Literal["ontological", "epistemic", "axiological", "empirical", "praxis"]
Attitude = Literal[
    "accepts", "rejects", "suspends", "accepts_conditionally", "accepts_for_argument"
]
Strength = Literal["tentative", "leaning", "confident", "certain"]
Source = Literal["stated", "implied_by_act", "inferred"]
AnchorMatch = Literal["exact", "normalized", "fuzzy", "none"]
Split = Literal["dev", "test"]
MANIFEST = "MANIFEST.sha256.json"
ACCESS_LOG = "ACCESS.log"


class GoldClaim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quote: str
    char_start: int
    char_end: int
    speaker: str
    speech_act: str
    canonical: str
    layer: Layer
    attitude: Attitude
    strength: Strength
    source: Source


class GoldRelation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_claim: int
    to_claim: int
    type: Literal["supports", "contradicts", "depends_on", "reframes"]


class GoldChunk(BaseModel):
    """One JSONL line."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    episode_ref: str
    text: str
    claims: list[GoldClaim]
    proposition_clusters: list[list[int]] = []
    relations: list[GoldRelation] = []

    @model_validator(mode="after")
    def quotes_are_source_substrings(self) -> Self:
        for claim in self.claims:
            if self.text[claim.char_start : claim.char_end] != claim.quote:
                raise ValueError(f"quote is not at its offsets: {claim.quote!r}")
        return self


class PredictedClaim(BaseModel):
    """Pipeline output scored against gold, keyed by chunk_id."""

    chunk_id: str
    char_start: int
    char_end: int
    quote: str
    speaker: str
    layer: Layer
    attitude: Attitude
    source: Source
    anchor_match: AnchorMatch


def _digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _gold_files(version_dir: pathlib.Path) -> list[pathlib.Path]:
    return sorted(version_dir.glob("*/*.jsonl"))


def write_manifest(version_dir: pathlib.Path) -> None:
    entries = {str(p.relative_to(version_dir)): _digest(p) for p in _gold_files(version_dir)}
    (version_dir / MANIFEST).write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n")


def verify_manifest(version_dir: pathlib.Path) -> None:
    recorded = json.loads((version_dir / MANIFEST).read_text())
    actual = {str(p.relative_to(version_dir)): _digest(p) for p in _gold_files(version_dir)}
    if recorded != actual:
        changed = sorted(
            k for k in recorded.keys() | actual.keys() if recorded.get(k) != actual.get(k)
        )
        raise ValueError(f"gold files differ from the manifest: {changed}")


def load_split(
    version_dir: pathlib.Path, split: Split, purpose: str | None = None
) -> list[GoldChunk]:
    verify_manifest(version_dir)
    if split == "test":
        if not purpose:
            raise PermissionError("the test split is sealed: state a purpose")
        with (version_dir / ACCESS_LOG).open("a") as log:
            log.write(f"{datetime.datetime.now(datetime.UTC).isoformat()}\t{purpose}\n")
    return [
        GoldChunk.model_validate_json(line)
        for path in sorted((version_dir / split).glob("*.jsonl"))
        for line in path.read_text().splitlines()
        if line.strip()
    ]
