"""Write the checked structure to the bank: ideas, stances and typed links. Safe to rerun.

Usage: load_structure.py <structure.json>
Everything is provisional. Agents never ratify.
"""

import hashlib
import json
import pathlib
import sys

from arena_core.db import get_engine
from arena_core.provenance import code_ref
from sqlalchemy import text

BANK_VERSION = 2
MODEL = "claude-code-subagent"
PROMPT = "structure_ideas"
VERSION = "v1"
RELATION = {
    "supports": "supports",
    "rebuts": "contradicts",
    "undercuts": "contradicts",
    "undermines": "contradicts",
    "qualifies": "reframes",
    "presupposes": "depends_on",
    "exemplifies": "supports",
    "defines": "depends_on",
}
VALIDITY = {"truth": "truth", "rightness": "rightness"}


def digest(*parts: str) -> bytes:
    return hashlib.sha256("|".join(parts).encode()).digest()


def main(path: str) -> None:
    data = json.loads(pathlib.Path(path).read_text())
    with get_engine().begin() as connection:
        run = connection.execute(
            text("SELECT run_id FROM pipeline_run WHERE job_name = 'load_structure' LIMIT 1")
        ).scalar_one_or_none()
        if run is None:
            run = connection.execute(
                text(
                    "INSERT INTO pipeline_run (stage, job_name, trigger, code_ref, model_name,"
                    " model_version, prompt_id, prompt_version) VALUES ('S9', 'load_structure',"
                    " 'manual', :c, :m, :m, :p, :v) RETURNING run_id"
                ),
                {"c": code_ref(), "m": MODEL, "p": PROMPT, "v": VERSION},
            ).scalar_one()
        common = {"run": run, "m": MODEL, "p": PROMPT, "v": VERSION}
        ids = {}
        for idea in data["ideas"]:
            ids[idea["key"]] = connection.execute(
                text(
                    "INSERT INTO proposition (public_id, canonical, tl_type, layer, validity_tag,"
                    " bank_version, run_id, model_name, model_version, prompt_id, prompt_version,"
                    " inputs_hash) VALUES (:pid, :can, :tl, :layer, :val, :bank, :run, :m, :m, :p,"
                    " :v, :h) ON CONFLICT (public_id) DO UPDATE SET canonical = :can,"
                    " layer = :layer"
                    " RETURNING proposition_id"
                ),
                {
                    "pid": f"A-{idea['key']}"[:60], "can": idea["canonical"],
                    "tl": idea["tl_type"], "layer": idea["layer"],
                    "val": VALIDITY.get(idea["validity"]), "bank": BANK_VERSION,
                    "h": digest(idea["canonical"]), **common,
                },
            ).scalar_one()  # fmt: skip
        stances = 0
        for idea in data["ideas"]:
            for holding in idea["holdings"]:
                inferred = holding.get("inferred", False)
                row = connection.execute(
                    text(
                        "SELECT c.speaker_person_id, c.episode_id, c.strength::text,"
                        " e.published_at::date FROM claim c JOIN episode e USING (episode_id)"
                        " WHERE c.claim_id = :c"
                    ),
                    {"c": holding["claim"]},
                ).one()
                accepts = holding["attitude"] == "accepts"
                stances += connection.execute(
                    text(
                        "INSERT INTO stance (person_id, proposition_id, value, tl_attitude,"
                        " strength, strength_num, source, claim_ids, episode_id, as_of, run_id,"
                        " model_name, model_version, prompt_id, prompt_version, inputs_hash)"
                        " VALUES (:person, :pr, :value, :att, 'confident', 0.75, :src,"
                        " CAST(:ids AS uuid[]), :ep, :asof, :run, :m, :m, :p, :v, :h)"
                        " ON CONFLICT DO NOTHING"
                    ),
                    {
                        "person": row[0], "pr": ids[idea["key"]],
                        "value": "affirm" if accepts else "reject",
                        "att": "accepts" if accepts else "rejects",
                        "src": "inferred" if inferred else "stated", "ids": [holding["claim"]],
                        "ep": row[1], "asof": row[3], "h": digest(idea["key"], holding["claim"]),
                        **common,
                    },
                ).rowcount  # fmt: skip
        links = 0
        for link in data["links"]:
            links += connection.execute(
                text(
                    "INSERT INTO proposition_relation (from_id, to_id, type, tl_relation_type,"
                    " evidence_claim_ids, confidence, source, run_id, stage, model_name,"
                    " model_version, prompt_id, prompt_version, inputs_hash) VALUES (:a, :b, :t,"
                    " :k, CAST(:e AS uuid[]), :c, :s, :run, 'S10', :m, :m, :p, :v, :h)"
                    " ON CONFLICT DO NOTHING"
                ),
                {
                    "a": ids[link["from"]], "b": ids[link["to"]], "t": RELATION[link["type"]],
                    "k": link["type"], "e": link.get("claims", []), "c": link["confidence"],
                    "s": link["source"], "h": digest(link["from"], link["to"], link["type"]),
                    **common,
                },
            ).rowcount  # fmt: skip
    print(len(ids), "ideas,", stances, "new stances,", links, "new links")


if __name__ == "__main__":
    main(*sys.argv[1:])
