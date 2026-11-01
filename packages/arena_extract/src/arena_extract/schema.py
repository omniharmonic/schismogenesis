"""LLM output contract for claim extraction (08 §4.7)."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SpeechAct = Literal[
    "assert", "concede", "retract", "question", "answer", "hypothesize", "steelman_report",
    "attribute", "challenge", "commit_conditional", "meta", "rhetorical_question", "nonliteral",
]  # fmt: skip


class ClaimItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seq: int
    quote: str = Field(min_length=20, max_length=600)
    speech_act: SpeechAct
    claim_text: str = Field(max_length=300)
    proposed_canonical: str = Field(min_length=3, max_length=400)
    tl_type: Literal[
        "empirical", "causal", "predictive", "counterfactual", "normative", "prescriptive",
        "definitional", "conceptual", "modal", "meta",
    ]  # fmt: skip
    attitude: Literal[
        "accepts", "rejects", "suspends", "accepts_conditionally", "accepts_for_argument"
    ]
    strength: Literal["tentative", "leaning", "confident", "certain"]
    source: Literal["stated", "implied_by_act", "inferred"]
    layer: Literal["ontological", "epistemic", "axiological", "empirical", "praxis"]
    quantifier: Literal["all", "most", "many", "some", "few", "none", "generic"]


class ExtractClaimsOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[ClaimItem] = Field(max_length=40)
