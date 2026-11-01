"""S6-S8 for written sources: chunk, extract through LLMClient, anchor, gate.

Each step is re-runnable. Finished chunks are recorded in stage_item and skipped.
"""

import hashlib
import json
import pathlib
import re
from collections.abc import Callable
from typing import Any

from arena_core.provenance import code_ref
from arena_llm import LLMClient, PendingBatch
from sqlalchemy import Connection, Engine, text

from arena_extract import validators
from arena_extract.anchor import locate, previous_sentence, public_quote
from arena_extract.schema import ClaimItem, ExtractClaimsOutput

PROMPT_ID = "extract_claims_written"
PROMPT_VERSION = "v1"
TARGET_WORDS = 350
PROMPT_DIR = pathlib.Path(__file__).parent / "prompts"
SKIPS_NLI = {"inferred"}
Scorer = Callable[[list[tuple[str, str]]], list[dict[str, Any]]]


def plan_chunks(words_per_segment: list[int], target: int = TARGET_WORDS) -> list[tuple[int, int]]:
    """Tile segments into inclusive (first, last) cores of about `target` words."""
    cores, first, total = [], 0, 0
    for seq, words in enumerate(words_per_segment):
        total += words
        if total >= target:
            cores.append((first, seq))
            first, total = seq + 1, 0
    if first < len(words_per_segment):
        cores.append((first, len(words_per_segment) - 1))
    return cores


def _segments(connection: Connection, episode_id: str) -> list[Any]:
    rows = connection.execute(
        text(
            "SELECT s.segment_id, s.seq, s.text, s.person_id, s.locator, t.transcript_id "
            "FROM private.segment s JOIN transcript t USING (transcript_id) "
            "WHERE t.episode_id = :e AND t.is_current ORDER BY s.seq"
        ),
        {"e": episode_id},
    ).all()
    return list(rows)


def _start_run(connection: Connection, stage: str, job: str, **fields: Any) -> Any:
    return connection.execute(
        text(
            "INSERT INTO pipeline_run (stage, job_name, trigger, code_ref, model_name,"
            " model_version, prompt_id, prompt_version) VALUES (:stage, :job, 'manual', :code,"
            " :model, :model, :pid, :pv) RETURNING run_id"
        ),
        {
            "stage": stage,
            "job": job,
            "code": code_ref(),
            "model": fields.get("model"),
            "pid": fields.get("prompt_id"),
            "pv": fields.get("prompt_version"),
        },
    ).scalar_one()


def chunk_source(engine: Engine, episode_id: str) -> int:
    with engine.begin() as connection:
        found = connection.execute(
            text("SELECT count(*) FROM chunk WHERE episode_id = :e"), {"e": episode_id}
        ).scalar_one()
        if found:
            return found
        segments = _segments(connection, episode_id)
        run_id = _start_run(connection, "S6", "chunk_transcript")
        cores = plan_chunks([len(s.text.split()) for s in segments])
        for chunk_seq, (first, last) in enumerate(cores):
            window = segments[max(first - 1, 0) : last + 2]
            core = segments[first : last + 1]
            connection.execute(
                text(
                    "INSERT INTO chunk (transcript_id, episode_id, seq, segment_ids, core_from_seq,"
                    " core_to_seq, speakers, token_estimate, locator, run_id, model_version,"
                    " inputs_hash) VALUES (:t, :e, :q, CAST(:ids AS uuid[]), :a, :b, :sp, :tok,"
                    " CAST(:loc AS jsonb), :run, :v, :h)"
                ),
                {
                    "t": segments[0].transcript_id,
                    "e": episode_id,
                    "q": chunk_seq,
                    "ids": [str(s.segment_id) for s in window],
                    "a": first,
                    "b": last,
                    "sp": sorted({s.person_id for s in core}),
                    "tok": sum(len(s.text.split()) for s in core) * 4 // 3,
                    "loc": json.dumps({"paragraphs": [first + 1, last + 1]}),
                    "run": run_id,
                    "v": PROMPT_VERSION,
                    "h": hashlib.sha256("".join(s.text for s in core).encode()).digest(),
                },
            )
        connection.execute(
            text("UPDATE pipeline_run SET status='succeeded', finished_at=now() WHERE run_id=:r"),
            {"r": run_id},
        )
        return len(cores)


def _user_message(
    title: str, published: Any, author: str, segments: list[Any], a: int, b: int
) -> str:
    def block(items: list[Any]) -> str:
        return "\n".join(f"[{s.seq}] {s.text}" for s in items)

    return (
        f"WORK: {title} ({published})\nAUTHOR: {author}\n"
        f"CONTEXT (do not quote):\n{block(segments[max(a - 1, 0) : a])}\n"
        f"CORE:\n{block(segments[a : b + 1])}\n"
        f"CONTEXT (do not quote):\n{block(segments[b + 1 : b + 2])}"
    )


def extract_source(engine: Engine, llm: LLMClient, episode_id: str) -> dict[str, int]:
    """Run S7 and S8 for each unfinished chunk. Queued requests are counted, not errors."""
    system = (PROMPT_DIR / f"{PROMPT_ID}_{PROMPT_VERSION}.md").read_text()
    schema = ExtractClaimsOutput.model_json_schema()
    counts = {"pending": 0, "claims": 0, "skipped": 0}
    with engine.begin() as connection:
        segments = _segments(connection, episode_id)
        episode = connection.execute(
            text("SELECT title, published_at::date AS d, url FROM episode WHERE episode_id = :e"),
            {"e": episode_id},
        ).one()
        chunks = connection.execute(
            text(
                "SELECT chunk_id, core_from_seq, core_to_seq FROM chunk WHERE episode_id = :e "
                "AND superseded_by IS NULL ORDER BY seq"
            ),
            {"e": episode_id},
        ).all()
        author = segments[0].person_id
        name = connection.execute(
            text("SELECT display_name FROM person WHERE person_id = :a"), {"a": author}
        ).scalar_one()

    for chunk in chunks:
        user = _user_message(
            episode.title, episode.d, name, segments, chunk.core_from_seq, chunk.core_to_seq
        )
        digest = hashlib.sha256((system + user).encode()).digest()
        with engine.begin() as connection:
            done = connection.execute(
                text(
                    "SELECT 1 FROM stage_item WHERE item_type = 'chunk' AND item_id = :c "
                    "AND stage = 'S8' AND prompt_version = :p AND inputs_hash = :h"
                ),
                {"c": str(chunk.chunk_id), "p": PROMPT_VERSION, "h": digest},
            ).first()
            if done:
                counts["skipped"] += 1
                continue
            try:
                outputs = llm.complete_json(
                    prompt_id=PROMPT_ID, prompt_version=PROMPT_VERSION, system=system,
                    user=user, schema=schema,
                )  # fmt: skip
            except PendingBatch:
                counts["pending"] += 1
                continue
            model = getattr(llm, "last_model", "unknown")
            run_id = _start_run(
                connection, "S8", "anchor_and_verify", model=model, prompt_id=PROMPT_ID,
                prompt_version=PROMPT_VERSION,
            )  # fmt: skip
            core = segments[chunk.core_from_seq : chunk.core_to_seq + 1]
            items = ExtractClaimsOutput.model_validate(outputs[0]).items
            for item in items:
                _store_claim(connection, item, chunk.chunk_id, episode_id, episode.url, author,
                             core, run_id, model, digest)  # fmt: skip
            connection.execute(
                text(
                    "INSERT INTO stage_item (item_type, item_id, stage, model_version,"
                    " prompt_version, inputs_hash, run_id, status) VALUES ('chunk', :c, 'S8', :m,"
                    " :p, :h, :r, 'done')"
                ),
                {"c": str(chunk.chunk_id), "m": model, "p": PROMPT_VERSION, "h": digest,
                 "r": run_id},
            )  # fmt: skip
            connection.execute(
                text(
                    "UPDATE pipeline_run SET status='succeeded', finished_at=now() "
                    "WHERE run_id = :r"
                ),
                {"r": run_id},
            )
            connection.execute(
                text(
                    "INSERT INTO llm_call (run_id, backend, model_name, model_version, prompt_id,"
                    " prompt_version, request_hash, ok) VALUES (:r, :b, :m, :m, :pid, :pv, :h,"
                    " true)"
                ),
                {"r": run_id, "b": type(llm).__name__, "m": model, "pid": PROMPT_ID,
                 "pv": PROMPT_VERSION, "h": digest},
            )  # fmt: skip
            counts["claims"] += len(items)
    return counts


def _find_anchor(item: ClaimItem, core: list[Any]) -> tuple[Any, Any] | None:
    ordered = sorted(core, key=lambda s: s.seq != item.seq)  # the cited paragraph first
    for segment in ordered:
        anchor = locate(item.quote, segment.text)
        if anchor:
            return segment, anchor
    return None


def _store_claim(
    connection: Connection, item: ClaimItem, chunk_id: Any, episode_id: str, url: str, author: str,
    core: list[Any], run_id: Any, model: str, digest: bytes,
) -> None:  # fmt: skip
    found = _find_anchor(item, core)
    row: dict[str, Any] = {
        "chunk": chunk_id, "episode": episode_id, "author": author, "act": item.speech_act,
        "tl": item.tl_type, "quant": item.quantifier,
        "claim": item.claim_text, "canonical": item.proposed_canonical, "att": item.attitude,
        "strength": item.strength, "src": item.source, "layer": item.layer, "mq": item.quote,
        "seg": None, "cs": None, "ce": None, "am": "none", "score": None, "qf": None, "qp": None,
        "loc": None, "link": None, "issues": "[]", "status": "rejected", "reason": "no_anchor",
        "run": run_id, "model": model, "pid": PROMPT_ID, "pv": PROMPT_VERSION, "h": digest,
    }  # fmt: skip
    if found:
        segment, anchor = found
        stored = segment.text[anchor.char_start : anchor.char_end]
        problems = validators.issues(item, stored, segment.text)
        row |= {
            "seg": segment.segment_id, "cs": anchor.char_start, "ce": anchor.char_end,
            "am": anchor.match, "score": anchor.score, "qf": stored,
            "qp": public_quote(stored), "loc": json.dumps(segment.locator), "link": url,
            "strength": validators.lowered_strength(item, stored),
            "issues": json.dumps(problems),
            "status": "rejected" if problems else "anchored",
            "reason": problems[0] if problems else None,
        }  # fmt: skip
    connection.execute(
        text(
            "INSERT INTO claim (tl_type, quantifier, chunk_id, episode_id, speaker_person_id,"
            " speaker_conf, speech_act,"
            " claim_text, proposed_canonical, tl_attitude, strength, source, proposed_layer,"
            " model_quote, anchor_segment_id, anchor_char_start, anchor_char_end, anchor_match,"
            " anchor_score, quote_full, quote_public, locator, deep_link, validator_issues,"
            " gate_status, reject_reason, run_id, stage, model_name, model_version, prompt_id,"
            " prompt_version, inputs_hash) VALUES (:tl, :quant, :chunk, :episode, :author, 1, :act,"
            " :claim,"
            " :canonical, :att, :strength, :src, :layer, :mq, :seg, :cs, :ce, :am, :score, :qf,"
            " :qp, CAST(:loc AS jsonb), :link, CAST(:issues AS jsonb), :status, :reason, :run,"
            " 'S8', :model, :model, :pid, :pv, :h)"
        ),
        row,
    )


BELIEF_REPORT = re.compile(
    r"\b(i|we)\s+(?:\w+\s+){0,2}(believe|think|suspect|hope|fear|doubt|expect|see|hold)\b",
    re.IGNORECASE,
)


def hypothesis(canonical: str, attitude: str, quote: str = "") -> str:
    """The speaker-committed form of a claim (08 §4.8), reworded for first-person belief reports.

    "I no longer believe X" entails that the author rejects X, not that X is false (ADR-031).
    """
    bare = canonical.rstrip(".")
    if BELIEF_REPORT.search(quote):
        lowered = bare if bare[:2].isupper() else bare[0].lower() + bare[1:]
        verb = "does not believe that" if attitude == "rejects" else "believes that"
        return f"The author {verb} {lowered}."
    return f"It is not the case that {bare}." if attitude == "rejects" else canonical


def decide(label: str, source: str) -> tuple[str, str | None]:
    if source in SKIPS_NLI:
        return "escalated", "inferred_needs_review"
    if label == "entailment":
        return "accepted", None
    if label == "contradiction":
        return "rejected", "nli_contradiction"
    return "escalated", "nli_neutral"


def gate_source(engine: Engine, score: Scorer, model_name: str, episode_id: str) -> dict[str, int]:
    """Apply the entailment gate to anchored claims."""
    with engine.begin() as connection:
        claims = connection.execute(
            text(
                "SELECT c.claim_id, c.quote_full, c.proposed_canonical, c.tl_attitude, c.source,"
                " c.anchor_char_start, s.text FROM claim c JOIN private.segment s"
                " ON s.segment_id = c.anchor_segment_id WHERE c.episode_id = :e"
                " AND c.gate_status = 'anchored' AND c.superseded_by IS NULL"
            ),
            {"e": episode_id},
        ).all()
        if not claims:
            return {}
        pairs = [
            (
                f"{previous_sentence(c.text, c.anchor_char_start)} {c.quote_full}".strip(),
                hypothesis(c.proposed_canonical, c.tl_attitude, c.quote_full),
            )
            for c in claims
        ]
        tally: dict[str, int] = {}
        for claim, verdict in zip(claims, score(pairs), strict=True):
            status, reason = decide(verdict["label"], claim.source)
            tally[status] = tally.get(status, 0) + 1
            connection.execute(
                text(
                    "UPDATE claim SET nli_label = :l, nli_entail_prob = :p, nli_model = :m,"
                    " gate_status = :s, reject_reason = :r WHERE claim_id = :c"
                ),
                {"l": verdict["label"], "p": verdict["entail"], "m": model_name, "s": status,
                 "r": reason, "c": claim.claim_id},
            )  # fmt: skip
        return tally
