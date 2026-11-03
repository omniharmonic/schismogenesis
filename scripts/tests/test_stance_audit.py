"""The stance audit's quote check: the code gate that makes a reader's stance publishable."""

import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location(
    "stance_audit", pathlib.Path(__file__).resolve().parents[1] / "stance_audit.py"
)
assert spec and spec.loader
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

TEXT = audit.norm(
    "The rise of the **Machine** was never going to stop where we might want it to.\n"
    "We  must “resist” it — always."
)
TEXTS = {"kingsnorth-essay": TEXT}
OWNER = {"kingsnorth-essay": "paul-kingsnorth", "other-essay": "someone-else"}


def problems(quote: str, work: str = "kingsnorth-essay", person: str = "paul-kingsnorth"):
    return audit.quote_problems("x", {"quote": quote, "work": work}, person, TEXTS, OWNER)


def test_verbatim_quote_passes_despite_typography():
    # curly quotes, dashes, markdown emphasis and line breaks don't block an exact quote
    assert problems("The rise of the Machine was never going to stop") == []
    assert problems('We must "resist" it - always.') == []


def test_paraphrase_is_rejected():
    assert problems("The Machine will never stop") != []


def test_quote_must_come_from_the_persons_own_work():
    assert problems("The rise of the Machine", work="other-essay") != []
    assert problems("The rise of the Machine", person="sam-altman") != []


def test_quote_length_limit():
    assert problems("x" * 281) != []
    assert problems("") != []
