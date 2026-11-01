"""Compute the measured space from the graph data, role gate and position distances.

Usage: build_space.py <graph.json> <final-review.json> <output.json>
"""

import json
import pathlib
import sys

from arena_core.db import get_engine
from arena_map.space import co_membership, distance_matrix, embed, groups
from sqlalchemy import text

CUT = 0.40


def main(graph: str, review: str, output: str) -> None:
    data = json.loads(pathlib.Path(graph).read_text())
    final = json.loads(pathlib.Path(review).read_text())
    distances = json.loads(pathlib.Path("evals/results/distance-v1.json").read_text())
    scale = {
        (q["key"], frozenset({p["a"], p["b"]})): p["distance"]
        for q in distances["questions"]
        for p in q["pairs"]
    }
    with get_engine().connect() as connection:
        accepted = set(
            connection.execute(
                text("SELECT claim_id::text FROM claim WHERE gate_status = 'accepted'")
            ).scalars()
        )
    removed = [tuple(item) for item in final["removed"]]

    def unfair(question: str, holding: dict) -> bool:
        return any(
            question == key and holding["author"].endswith(who) and holding["quote"].startswith(q)
            for key, who, q in removed
        )

    questions = []
    holdings: dict[str, dict[str, set[str]]] = {}
    for question in data["questions"]:
        if question["key"] not in final["keep"]:
            continue
        positions = []
        for position in question["positions"]:
            kept = [
                h
                for h in position["holdings"]
                if h["claim"] in accepted and not unfair(question["key"], h)
            ]
            if kept:
                positions.append({**position, "holdings": kept})
                for holding in kept:
                    holdings.setdefault(holding["author"], {}).setdefault(
                        question["key"], set()
                    ).add(position["key"])
        if len(positions) >= 2:
            questions.append({**question, "positions": positions})

    def distance(question: str, a: str, b: str) -> float:
        return 0 if a == b else scale.get((question, frozenset({a, b})), 2)

    keys = [q["key"] for q in questions]
    people, matrix = distance_matrix(holdings, distance)
    coords, explained = embed(matrix)
    labels = groups(matrix, CUT)
    _, together = co_membership(holdings, distance, keys, CUT)
    shared = [[len(holdings[a].keys() & holdings[b].keys()) for b in people] for a in people]
    result = {
        "people": people, "questions": questions, "coords": coords.round(4).tolist(),
        "explained": round(explained, 3), "labels": labels, "cut": CUT,
        "distance": matrix.round(3).tolist(), "together": together.round(3).tolist(),
        "shared": shared,
    }  # fmt: skip
    pathlib.Path(output).write_text(json.dumps(result, ensure_ascii=False))
    print(len(questions), "questions", sum(len(q["positions"]) for q in questions), "positions")
    print("explained", result["explained"])
    for label in sorted(set(labels)):
        members = [p for p, x in zip(people, labels, strict=True) if x == label]
        print(label, members)
    pairs = sorted(
        ((together[i, j], people[i], people[j], shared[i][j], matrix[i, j])
         for i in range(len(people)) for j in range(i + 1, len(people))),
        reverse=True,
    )  # fmt: skip
    for row in pairs[:14]:
        print(f"{row[0]:.2f} together  {row[1]} / {row[2]}  shared {row[3]}  d {row[4]:.2f}")


if __name__ == "__main__":
    main(*sys.argv[1:])
