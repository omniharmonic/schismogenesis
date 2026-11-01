"""Keep position assignments both readers agree on, load them, and compare people. Pilot one-off.

Usage: load_positions.py <page_questions.json> <output.json>
"""

import hashlib
import json
import pathlib
import sys

from arena_core.db import get_engine
from arena_core.provenance import code_ref
from arena_map.positions import align, groups
from sqlalchemy import text

RESULTS = pathlib.Path("evals/results")
REWORD = {
    "educating-the-public-is-futile": (
        "Broad public persuasion will not work",
        "Persuading the wider public is no longer a workable path to change.",
    )
}


def main(page: str, output: str) -> None:
    drafts = json.loads((RESULTS / "positions-v1.json").read_text())["questions"]
    check = json.loads((RESULTS / "positions-v1-check.json").read_text())
    verdicts = {item["id"]: item["position"] for item in check["claims"]}
    claim_ids = json.loads(pathlib.Path("evals/queue/positions-v1/map.json").read_text())
    pages = {q["key"]: q for q in json.loads(pathlib.Path(page).read_text())}

    agreed = differ = none = 0
    built = []
    for draft in drafts:
        kept: dict[str, list[dict]] = {}
        for item in draft["assignments"]:
            verdict = verdicts[item["id"]]
            if verdict == "none":
                none += 1
            elif verdict != item["position"]:
                differ += 1
            else:
                agreed += 1
                number = int(item["id"].rsplit(":", 1)[1])
                claim = pages[draft["key"]]["placements"][number]
                assert claim["claim"] == claim_ids[item["id"]]
                kept.setdefault(verdict, []).append({**claim, "reason": item["reason"]})
        positions = []
        for position in draft["positions"]:
            if position["key"] in kept:
                label, statement = REWORD.get(
                    position["key"], (position["label"], position["statement"])
                )
                positions.append(
                    {"key": position["key"], "label": label, "statement": statement,
                     "holdings": kept[position["key"]]}
                )  # fmt: skip
        if len(positions) >= 2:
            page_question = pages[draft["key"]]
            built.append({k: page_question[k] for k in ("key", "text", "layer")}
                         | {"positions": positions})  # fmt: skip

    holdings: dict[str, dict[str, set[str]]] = {}
    for question in built:
        for position in question["positions"]:
            for holding in position["holdings"]:
                holdings.setdefault(holding["author"], {}).setdefault(question["key"], set()).add(
                    position["key"]
                )
    pairs = align(holdings)
    with get_engine().begin() as connection:
        run_id = connection.execute(
            text(
                "INSERT INTO pipeline_run (stage, job_name, trigger, code_ref, status) VALUES"
                " ('S11', 'build_positions', 'manual', :c, 'succeeded') RETURNING run_id"
            ),
            {"c": code_ref()},
        ).scalar_one()
        common = {"r": run_id, "m": "claude-code-subagent", "v": "pilot"}
        connection.execute(text("DELETE FROM position_holding"))
        connection.execute(text("TRUNCATE position_definition, position CASCADE"))
        for question in built:
            question_id = connection.execute(
                text(
                    "SELECT live_question_id FROM live_question WHERE chosen_axes->0->>'key' = :k"
                ),
                {"k": question["key"]},
            ).scalar_one()
            for position in question["positions"]:
                digest = hashlib.sha256(position["statement"].encode()).digest()
                position_id = connection.execute(
                    text(
                        "INSERT INTO position (live_question_id, key, run_id, model_name,"
                        " model_version, prompt_id, prompt_version, inputs_hash) VALUES (:q, :k,"
                        " :r, :m, :v, 'derive_positions', 'v1', :h) RETURNING position_id"
                    ),
                    {**common, "q": question_id, "k": position["key"], "h": digest},
                ).scalar_one()
                connection.execute(
                    text(
                        "INSERT INTO position_definition (position_id, version, label, statement,"
                        " author_kind, author_model) VALUES (:p, 1, :l, :s, 'model', :m)"
                    ),
                    {"p": position_id, "l": position["label"], "s": position["statement"],
                     "m": common["m"]},
                )  # fmt: skip
                for holding in position["holdings"]:
                    connection.execute(
                        text(
                            "INSERT INTO position_holding (position_id, person_id, claim_id,"
                            " reason, run_id, model_name, model_version, prompt_id,"
                            " prompt_version, inputs_hash) SELECT :p, speaker_person_id, claim_id,"
                            " :why, :r, :m, :v, 'derive_positions', 'v1', :h FROM claim"
                            " WHERE claim_id = :c ON CONFLICT DO NOTHING"
                        ),
                        {**common, "p": position_id, "why": holding["reason"],
                         "c": holding["claim"], "h": digest},
                    )  # fmt: skip
    result = {
        "questions": built,
        "pairs": [
            {"a": p.a, "b": p.b, "shared": p.shared_questions, "same": p.same_position}
            for p in pairs
        ],
        "groups": groups(pairs),
        "counts": {"agreed": agreed, "differ": differ, "none": none},
    }
    pathlib.Path(output).write_text(json.dumps(result, ensure_ascii=False))
    print(result["counts"], len(built), result["groups"])
    for question in built:
        print(question["key"], [(p["key"], len(p["holdings"])) for p in question["positions"]])
    for pair in sorted(pairs, key=lambda p: (-p.shared_questions, -(p.score or 0)))[:16]:
        print(pair.a, "/", pair.b, pair.same_position, "of", pair.shared_questions)


if __name__ == "__main__":
    main(*sys.argv[1:])
