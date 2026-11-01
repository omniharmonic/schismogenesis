"""S9 and S10 for the pilot: shared propositions, stances and relations.

Candidates come from embeddings. A model confirms them. Only code writes to the bank.
"""

import hashlib
import json
import pathlib
from collections.abc import Callable, Sequence
from typing import Any, Literal

from arena_llm import LLMClient, PendingBatch
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Connection, Engine, text

from arena_extract.written import _start_run

PROMPT_ID = "relate_propositions"
PROMPT_VERSION = "v1"
PROMPT_DIR = pathlib.Path(__file__).parent / "prompts"
EMBED_MODEL = "BAAI/bge-large-en-v1.5"
MIN_SIMILARITY = 0.58
MAX_PAIRS_PER_CLAIM = 5
PAIRS_PER_REQUEST = 25
BANK_VERSION = 1
STANCE_VALUE = {
    "accepts": "affirm",
    "rejects": "reject",
    "accepts_conditionally": "conditional",
    "accepts_for_argument": "steelman_only",
}
STRENGTH_NUM = {"tentative": 0.25, "leaning": 0.5, "confident": 0.75, "certain": 1.0}
Embedder = Callable[[list[str]], Any]


class PairVerdict(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pair: int
    relation: Literal[
        "equivalent", "contradicts", "supports", "depends_on", "reframes", "unrelated"
    ]
    confidence: float = Field(ge=0, le=1)


class RelateOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verdicts: list[PairVerdict]


def candidate_pairs(
    vectors: Any, authors: Sequence[str], min_similarity: float = MIN_SIMILARITY,
    limit: int = MAX_PAIRS_PER_CLAIM,
) -> list[tuple[int, int, float]]:  # fmt: skip
    """Most similar claims by different authors. Vectors must be unit length."""
    similarity = vectors @ vectors.T
    chosen: set[tuple[int, int]] = set()
    scores: dict[tuple[int, int], float] = {}
    for i in range(len(authors)):
        ranked = sorted(range(len(authors)), key=lambda j: -similarity[i][j])
        taken = 0
        for j in ranked:
            if taken == limit or similarity[i][j] < min_similarity:
                break
            if j == i or authors[i] == authors[j]:
                continue
            key = (min(i, j), max(i, j))
            chosen.add(key)
            scores[key] = float(similarity[i][j])
            taken += 1
    return [(a, b, scores[(a, b)]) for a, b in sorted(chosen)]


def merge_groups(n: int, equivalent: list[tuple[int, int]]) -> list[int]:
    """Union-find: return a group id per item."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in equivalent:
        parent[find(a)] = find(b)
    return [find(i) for i in range(n)]


def _accepted(connection: Connection) -> list[Any]:
    rows = connection.execute(
        text(
            "SELECT c.claim_id, c.proposed_canonical, c.speaker_person_id, c.tl_attitude,"
            " c.strength, c.source, c.proposed_layer, c.tl_type, c.quantifier, c.episode_id,"
            " e.published_at::date AS as_of, c.model_name, c.created_at FROM claim c"
            " JOIN episode e USING (episode_id) WHERE c.gate_status = 'accepted'"
            " AND c.superseded_by IS NULL ORDER BY c.created_at, c.claim_id"
        )
    ).all()
    return list(rows)


def compare(engine: Engine, llm: LLMClient, embed: Embedder) -> tuple[list[Any], list[dict]]:
    """Return accepted claims and verdicts, queueing any comparisons still unanswered."""
    with engine.connect() as connection:
        claims = _accepted(connection)
    vectors = embed([c.proposed_canonical for c in claims])
    pairs = candidate_pairs(vectors, [c.speaker_person_id for c in claims])
    system = (PROMPT_DIR / f"{PROMPT_ID}_{PROMPT_VERSION}.md").read_text()
    verdicts, pending = [], 0
    for start in range(0, len(pairs), PAIRS_PER_REQUEST):
        group = pairs[start : start + PAIRS_PER_REQUEST]
        user = "\n\n".join(
            f"PAIR {n}\nA: {claims[a].proposed_canonical}\nB: {claims[b].proposed_canonical}"
            for n, (a, b, _) in enumerate(group)
        )
        try:
            output = llm.complete_json(
                prompt_id=PROMPT_ID, prompt_version=PROMPT_VERSION, system=system, user=user,
                schema=RelateOutput.model_json_schema(),
            )[0]  # fmt: skip
        except PendingBatch:
            pending += 1
            continue
        for verdict in RelateOutput.model_validate(output).verdicts:
            a, b, _ = group[verdict.pair]
            verdicts.append({"a": a, "b": b, **verdict.model_dump()})
    if pending:
        raise PendingBatch("relations", f"{pending} requests queued")
    return claims, verdicts


def build_bank(engine: Engine, claims: list[Any], verdicts: list[dict], model: str) -> dict:
    """Write propositions, stances and relations. Ends with a bank rebuilt from these inputs."""
    equivalent = [(v["a"], v["b"]) for v in verdicts if v["relation"] == "equivalent"]
    groups = merge_groups(len(claims), equivalent)
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM proposition_relation"))
        connection.execute(text("DELETE FROM stance"))
        connection.execute(text("UPDATE claim SET proposition_id = NULL"))
        connection.execute(text("DELETE FROM proposition"))
        run_id = _start_run(
            connection, "S9", "normalize_propositions", model=model, prompt_id=PROMPT_ID,
            prompt_version=PROMPT_VERSION,
        )  # fmt: skip
        ids: dict[int, Any] = {}
        for number, group in enumerate(sorted(set(groups)), start=1):
            members = [c for c, g in zip(claims, groups, strict=True) if g == group]
            first = members[0]
            ids[group] = connection.execute(
                text(
                    "INSERT INTO proposition (public_id, canonical, tl_type, layer, scope,"
                    " bank_version, first_seen_claim_id, first_seen_person_id, run_id, model_name,"
                    " model_version, prompt_id, prompt_version, inputs_hash) VALUES (:pid, :can,"
                    " :tl, :layer, CAST(:scope AS jsonb), :bank, :claim, :person, :run, :m, :m,"
                    " :p, :v, :h) RETURNING proposition_id"
                ),
                {
                    "pid": f"P-{number:06d}", "can": first.proposed_canonical,
                    "tl": first.tl_type or "empirical", "layer": first.proposed_layer,
                    "scope": json.dumps({"quantifier": first.quantifier or "generic"}),
                    "bank": BANK_VERSION, "claim": first.claim_id,
                    "person": first.speaker_person_id, "run": run_id, "m": model,
                    "p": PROMPT_ID, "v": PROMPT_VERSION,
                    "h": hashlib.sha256(first.proposed_canonical.encode()).digest(),
                },
            ).scalar_one()  # fmt: skip
            connection.execute(
                text(
                    "UPDATE claim SET proposition_id = :p WHERE claim_id = ANY(CAST(:c AS uuid[]))"
                ),
                {"p": ids[group], "c": [str(m.claim_id) for m in members]},
            )
        stances = {}
        for claim, group in zip(claims, groups, strict=True):
            value = STANCE_VALUE.get(claim.tl_attitude)
            if value and claim.source != "inferred":
                key = (claim.speaker_person_id, ids[group], claim.episode_id)
                stances.setdefault(key, (claim, value, []))[2].append(str(claim.claim_id))
        for (person, proposition, episode), (claim, value, claim_ids) in stances.items():
            connection.execute(
                text(
                    "INSERT INTO stance (person_id, proposition_id, value, tl_attitude, strength,"
                    " strength_num, source, claim_ids, episode_id, as_of, run_id, model_name,"
                    " model_version, prompt_id, prompt_version, inputs_hash) VALUES (:person, :pr,"
                    " :value, :att, :st, :num, :src, CAST(:ids AS uuid[]), :ep, :asof, :run, :m,"
                    " :m, :pi, :pv, :h)"
                ),
                {
                    "person": person, "pr": proposition, "value": value,
                    "att": claim.tl_attitude, "st": claim.strength,
                    "num": STRENGTH_NUM[claim.strength], "src": claim.source, "ids": claim_ids,
                    "ep": episode, "asof": claim.as_of, "run": run_id, "m": claim.model_name,
                    "pi": PROMPT_ID, "pv": PROMPT_VERSION,
                    "h": hashlib.sha256("".join(claim_ids).encode()).digest(),
                },
            )  # fmt: skip
        relations = 0
        kinds = {"contradicts": "rebuts", "supports": "supports", "depends_on": "presupposes",
                 "reframes": "reframes"}  # fmt: skip
        for verdict in verdicts:
            kind = kinds.get(verdict["relation"])
            first_id = ids[groups[verdict["a"]]]
            second_id = ids[groups[verdict["b"]]]
            if not kind or first_id == second_id or verdict["confidence"] < 0.6:
                continue
            relations += connection.execute(
                text(
                    "INSERT INTO proposition_relation (from_id, to_id, type, tl_relation_type,"
                    " evidence_claim_ids, confidence, source, run_id, stage, model_name,"
                    " model_version, prompt_id, prompt_version, inputs_hash) VALUES (:a, :b, :t,"
                    " :k, CAST(:e AS uuid[]), :c, 'inferred', :run, 'S10', :m, :m, :p, :v, :h)"
                    " ON CONFLICT DO NOTHING"
                ),
                {
                    "a": first_id, "b": second_id, "t": verdict["relation"], "k": kind,
                    "e": [str(claims[verdict["a"]].claim_id), str(claims[verdict["b"]].claim_id)],
                    "c": verdict["confidence"], "run": run_id, "m": model, "p": PROMPT_ID,
                    "v": PROMPT_VERSION, "h": b"\x00",
                },
            ).rowcount  # fmt: skip
        return {
            "claims": len(claims), "propositions": len(ids), "stances": len(stances),
            "relations": relations,
        }  # fmt: skip
