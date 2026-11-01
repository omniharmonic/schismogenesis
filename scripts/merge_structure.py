"""Combine theme readings. Step 1 lists near-duplicate ideas; step 2 applies a reader's merges.

Usage: merge_structure.py candidates | apply
"""

import json
import pathlib
import sys

from sentence_transformers import SentenceTransformer

RESULTS = pathlib.Path("evals/results/structure-v1")
QUEUE = pathlib.Path("evals/queue/structure-v1")
MODEL = "BAAI/bge-large-en-v1.5"
SIMILAR = 0.84


def load() -> list[dict]:
    ids = json.loads((QUEUE / "ids.json").read_text())
    ideas: dict[str, dict] = {}
    for path in sorted(RESULTS.glob("ideas-*.json")):
        data = json.loads(path.read_text())
        theme = data["theme"]
        for item in data["ideas"] + data.get("roots", []):
            key = item["key"]
            if key in ideas and ideas[key]["theme"] != theme:
                key = f"{theme}-{key}"
            holdings = [
                {"claim": ids[str(h["claim"])], "attitude": h["attitude"]}
                for h in item.get("holdings", [])
            ]
            inferred = [
                {"claim": ids[str(h["claim"])], "attitude": "accepts", "inferred": True,
                 "necessity": h["necessity"]}
                for h in item.get("inferred", [])
            ]  # fmt: skip
            ideas[key] = {
                "key": key, "theme": theme, "canonical": item["canonical"],
                "layer": item["layer"], "tl_type": item["tl_type"],
                "validity": item.get("validity", "truth"),
                "root": bool(inferred) and not holdings, "holdings": holdings + inferred,
            }  # fmt: skip
    return list(ideas.values())


def candidates() -> None:
    ideas = load()
    model = SentenceTransformer(MODEL)
    vectors = model.encode([i["canonical"] for i in ideas], normalize_embeddings=True)
    similar = vectors @ vectors.T
    pairs = []
    for a in range(len(ideas)):
        for b in range(a + 1, len(ideas)):
            if similar[a, b] >= SIMILAR:
                pairs.append(
                    {"a": ideas[a]["key"], "b": ideas[b]["key"],
                     "sim": round(float(similar[a, b]), 3),
                     "a_text": ideas[a]["canonical"], "b_text": ideas[b]["canonical"],
                     "a_layer": ideas[a]["layer"], "b_layer": ideas[b]["layer"]}
                )  # fmt: skip
    (QUEUE / "merge-candidates.json").write_text(json.dumps(pairs, indent=0))
    print(len(ideas), "ideas,", len(pairs), "candidate pairs")


def apply() -> None:
    ideas = {i["key"]: i for i in load()}
    claim_ids = json.loads((QUEUE / "ids.json").read_text())
    recovered = json.loads((RESULTS / "recovered.json").read_text())
    for item in recovered["add"]:
        ideas[item["idea"]]["holdings"].append(
            {"claim": claim_ids[str(item["claim"])], "attitude": item["attitude"]}
        )
    dropped = {claim_ids[str(claim)] for claim in recovered["drop"]}
    for idea in ideas.values():
        idea["holdings"] = [h for h in idea["holdings"] if h["claim"] not in dropped]
    merges = json.loads((RESULTS / "merges.json").read_text())["merges"]
    for keep, *others in merges:
        for other in others:
            if other not in ideas or keep not in ideas:
                continue
            ideas[keep]["holdings"] += ideas.pop(other)["holdings"]
    (RESULTS / "ideas-merged.json").write_text(json.dumps(list(ideas.values()), indent=0))
    print(len(ideas), "ideas after merging")


if __name__ == "__main__":
    {"candidates": candidates, "apply": apply}[sys.argv[1]]()
