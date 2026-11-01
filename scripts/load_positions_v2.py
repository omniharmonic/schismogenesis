"""Rebuild live questions and positions from the full pilot corpus. Pilot one-off.

Keeps only placements both readers agree on, then writes questions, provisional definitions and
holdings to the database, and the page data to <output.json>.
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
QUEUE = pathlib.Path("evals/queue/positions-v2")
MIN_AUTHORS = 3


def main(output: str) -> None:
    drafts = json.loads((RESULTS / "positions-v2.json").read_text())["questions"]
    check = json.loads((RESULTS / "positions-v2-check.json").read_text())
    verdicts = {item["id"]: item for item in check["claims"]}
    bundled = {(p["question"], p["key"]) for p in check["positions"] if p.get("bundled")}
    keys_by_text = {q["question"]: q["key"] for q in json.loads((QUEUE / "blind.json").read_text())}
    bundled = {(keys_by_text.get(q, q), k) for q, k in bundled}
    ids = json.loads((QUEUE / "ids.json").read_text())
    engine = get_engine()
    with engine.connect() as connection:
        rows = connection.execute(
            text(
                "SELECT c.claim_id, p.display_name, p.person_id, c.quote_public,"
                " c.proposed_canonical, c.tl_attitude::text, e.title, e.url,"
                " extract(year FROM e.published_at)::int,"
                " e.authorship, c.gate_status FROM claim c JOIN person p"
                " ON p.person_id = c.speaker_person_id JOIN episode e USING (episode_id)"
            )
        ).all()
    claims = {str(r[0]): r for r in rows}

    agreed = differ = none = 0
    built, dropped = [], []
    for draft in drafts:
        kept: dict[str, list[dict]] = {}
        for assignment in draft["assignments"]:
            claim_id = ids[str(assignment["claim"])]
            verdict = verdicts.get(f"{draft['key']}:{assignment['claim']}")
            if verdict is None:
                continue
            if verdict["position"] == "none":
                none += 1
            elif verdict["position"] != assignment["position"]:
                differ += 1
            else:
                agreed += 1
                row = claims[claim_id]
                kept.setdefault(assignment["position"], []).append(
                    {"claim": claim_id, "author": row[1], "person": row[2], "quote": row[3],
                     "prop": row[4], "att": row[5], "title": row[6], "url": row[7], "year": row[8],
                     "authorship": row[9], "reason": assignment["reason"]}
                )  # fmt: skip
        positions = [
            {**p, "holdings": kept[p["key"]], "bundled": (draft["key"], p["key"]) in bundled}
            for p in draft["positions"]
            if p["key"] in kept
        ]
        authors = {h["author"] for p in positions for h in p["holdings"]}
        if len(positions) >= 2 and len(authors) >= MIN_AUTHORS:
            built.append({k: draft[k] for k in ("key", "text", "layer")} | {"positions": positions})
        else:
            dropped.append(draft["key"])

    holdings: dict[str, dict[str, set[str]]] = {}
    for question in built:
        for position in question["positions"]:
            for holding in position["holdings"]:
                holdings.setdefault(holding["author"], {}).setdefault(question["key"], set()).add(
                    position["key"]
                )
    pairs = align(holdings)

    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE position_holding, position_definition, position, "
                 "live_question_proposition, live_question CASCADE")
        )  # fmt: skip
        run_id = connection.execute(
            text(
                "INSERT INTO pipeline_run (stage, job_name, trigger, code_ref, status) VALUES"
                " ('S11', 'build_positions', 'manual', :c, 'succeeded') RETURNING run_id"
            ),
            {"c": code_ref()},
        ).scalar_one()
        common = {"r": run_id, "m": "claude-code-subagent", "v": "pilot-v2"}
        for question in built:
            question_id = connection.execute(
                text(
                    "INSERT INTO live_question (text, chosen_axes, battery_week, run_id,"
                    " model_name, model_version, prompt_id, prompt_version, inputs_hash) VALUES"
                    " (:t, CAST(:a AS jsonb), '2026-W44', :r, :m, :v, 'derive_positions', 'v2', :h)"
                    " RETURNING live_question_id"
                ),
                {**common, "t": question["text"],
                 "a": json.dumps([{"key": question["key"], "layer": question["layer"]}]),
                 "h": hashlib.sha256(question["text"].encode()).digest()},
            ).scalar_one()  # fmt: skip
            for position in question["positions"]:
                digest = hashlib.sha256(position["statement"].encode()).digest()
                position_id = connection.execute(
                    text(
                        "INSERT INTO position (live_question_id, key, run_id, model_name,"
                        " model_version, prompt_id, prompt_version, inputs_hash) VALUES (:q, :k,"
                        " :r, :m, :v, 'derive_positions', 'v2', :h) RETURNING position_id"
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
                            " prompt_version, inputs_hash) VALUES (:p, :person, :c, :why, :r, :m,"
                            " :v, 'derive_positions', 'v2', :h) ON CONFLICT DO NOTHING"
                        ),
                        {**common, "p": position_id, "person": holding["person"],
                         "c": holding["claim"], "why": holding["reason"], "h": digest},
                    )  # fmt: skip
    result = {
        "questions": built, "dropped": dropped,
        "pairs": [{"a": p.a, "b": p.b, "shared": p.shared_questions, "same": p.same_position}
                  for p in pairs],
        "groups": groups(pairs, min_shared=5, min_score=0.6),
        "counts": {"agreed": agreed, "differ": differ, "none": none},
    }  # fmt: skip
    pathlib.Path(output).write_text(json.dumps(result, ensure_ascii=False))
    print(result["counts"], len(built), "dropped", dropped)
    print("groups", result["groups"])
    print("positions", sum(len(q["positions"]) for q in built),
          "bundled kept", sum(p["bundled"] for q in built for p in q["positions"]))  # fmt: skip
    for person, questions in sorted(holdings.items()):
        print(person, len(questions))
    for pair in sorted(pairs, key=lambda p: (-(p.score or 0) * (p.shared_questions >= 5),
                                             -p.shared_questions))[:12]:  # fmt: skip
        print(pair.a, "/", pair.b, pair.same_position, "of", pair.shared_questions)
    print("--- lowest")
    for pair in sorted((p for p in pairs if p.shared_questions >= 5), key=lambda p: p.score or 0)[
        :8
    ]:
        print(pair.a, "/", pair.b, pair.same_position, "of", pair.shared_questions)


if __name__ == "__main__":
    main(*sys.argv[1:])
