"""Load reviewed live questions into Neon. One-off for the pilot.

Usage: load_questions.py <questions.json> <removals.json>
"""

import hashlib
import json
import pathlib
import sys

from arena_core.db import get_engine
from arena_core.provenance import code_ref
from sqlalchemy import text

POLE = {"a": -1, "b": 1}


def main(path: str, removals: str) -> None:
    questions = json.loads(pathlib.Path(path).read_text())
    with get_engine().begin() as connection:
        connection.execute(text("DELETE FROM live_question_proposition"))
        connection.execute(text("DELETE FROM live_question"))
        run_id = connection.execute(
            text(
                "INSERT INTO pipeline_run (stage, job_name, trigger, code_ref, status, params) "
                "VALUES ('S11', 'live_question_battery', 'manual', :c, 'succeeded', "
                "CAST(:p AS jsonb)) RETURNING run_id"
            ),
            {"c": code_ref(), "p": pathlib.Path(removals).read_text()},
        ).scalar_one()
        for question in questions:
            question_id = connection.execute(
                text(
                    "INSERT INTO live_question (text, chosen_axes, battery_week, run_id,"
                    " model_name, model_version, prompt_id, prompt_version, inputs_hash) VALUES"
                    " (:t, CAST(:axes AS jsonb), '2026-W44', :r, 'claude-code-subagent',"
                    " 'pilot', 'derive_questions', 'v1', :h) RETURNING live_question_id"
                ),
                {
                    "t": question["text"],
                    "axes": json.dumps(
                        [{"key": question["key"], "pole_a": question["pole_a"],
                          "pole_b": question["pole_b"], "layer": question["layer"]}]
                    ),
                    "r": run_id,
                    "h": hashlib.sha256(question["text"].encode()).digest(),
                },
            ).scalar_one()  # fmt: skip
            for placement in question["placements"]:
                if placement["pole"] not in POLE:
                    continue
                connection.execute(
                    text(
                        "INSERT INTO live_question_proposition (live_question_id, proposition_id,"
                        " answer_pole, run_id) SELECT :q, proposition_id, :p, :r FROM claim"
                        " WHERE claim_id = :c ON CONFLICT DO NOTHING"
                    ),
                    {"q": question_id, "p": POLE[placement["pole"]], "r": run_id,
                     "c": placement["claim"]},
                )  # fmt: skip
    print(len(questions), "questions loaded")


if __name__ == "__main__":
    main(*sys.argv[1:])
