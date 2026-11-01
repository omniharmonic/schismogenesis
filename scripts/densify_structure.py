"""Find holdings the theme readers missed. Code proposes, a blind reader confirms.

For each person and idea: take the person's nearest accepted claims, score quote against idea with
the local entailment model, and queue the strong ones.

Usage: densify_structure.py
"""

import json
import pathlib

import numpy as np
import torch
from arena_core.db import get_engine
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from transformers import AutoModelForSequenceClassification, AutoTokenizer

QUEUE = pathlib.Path("evals/queue/structure-v1")
RESULTS = pathlib.Path("evals/results/structure-v1")
EMBED = "BAAI/bge-large-en-v1.5"
NLI = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
TOP = 3
MIN_SIMILAR = 0.60
MIN_NLI = 0.70
MAX_PER_PERSON = 110


def main() -> None:
    structure = json.loads((RESULTS / "structure.json").read_text())
    ideas = [i for i in structure["ideas"] if not i["root"]]
    with get_engine().connect() as connection:
        rows = connection.execute(
            text(
                "SELECT c.claim_id::text, c.speaker_person_id, p.display_name, c.quote_public,"
                " e.title FROM claim c JOIN person p ON p.person_id = c.speaker_person_id"
                " JOIN episode e USING (episode_id) WHERE c.gate_status = 'accepted'"
                " AND c.tl_attitude NOT IN ('suspends', 'accepts_for_argument')"
            )
        ).all()
    owner = {r[0]: r[1] for r in rows}
    held = {(i["key"], owner.get(h["claim"])) for i in structure["ideas"] for h in i["holdings"]}
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = SentenceTransformer(EMBED, device=device)
    claims = model.encode([r[3] for r in rows], normalize_embeddings=True, batch_size=32)
    vectors = model.encode([i["canonical"] for i in ideas], normalize_embeddings=True)
    people = sorted({r[1] for r in rows})
    by_person = {p: [n for n, r in enumerate(rows) if r[1] == p] for p in people}

    pairs = []
    for p in people:
        index = np.array(by_person[p])
        scores = vectors @ claims[index].T
        for i, idea in enumerate(ideas):
            if (idea["key"], p) in held:
                continue
            for j in np.argsort(scores[i])[::-1][:TOP]:
                if scores[i, j] >= MIN_SIMILAR:
                    pairs.append((p, i, int(index[j]), float(scores[i, j])))
    print(len(pairs), "pairs to score", flush=True)

    tokenizer = AutoTokenizer.from_pretrained(NLI)
    nli = AutoModelForSequenceClassification.from_pretrained(NLI).to(device).eval()
    labels = {v.lower(): k for k, v in nli.config.id2label.items()}
    entail, contra = labels["entailment"], labels["contradiction"]
    found: dict[tuple[str, str], dict] = {}
    for start in range(0, len(pairs), 16):
        batch = pairs[start : start + 16]
        tokens = tokenizer(
            [rows[c][3] for _, _, c, _ in batch],
            [ideas[i]["canonical"] for _, i, _, _ in batch],
            truncation=True, padding=True, return_tensors="pt",
        ).to(device)  # fmt: skip
        with torch.no_grad():
            probs = nli(**tokens).logits.softmax(-1).cpu().numpy()
        for (p, i, c, _), prob in zip(batch, probs, strict=True):
            score = max(float(prob[entail]), float(prob[contra]))
            if score < MIN_NLI:
                continue
            key = (p, ideas[i]["key"])
            if key not in found or score > found[key]["score"]:
                found[key] = {
                    "person": p, "idea_key": ideas[i]["key"], "idea": ideas[i]["canonical"],
                    "claim_id": rows[c][0], "who": rows[c][2], "quote": rows[c][3],
                    "work": rows[c][4], "score": round(score, 3),
                    "hint": "accepts" if prob[entail] >= prob[contra] else "rejects",
                }  # fmt: skip
        if start % 3200 == 0:
            print(start, len(found), flush=True)

    capped = []
    for p in people:
        mine = sorted((v for v in found.values() if v["person"] == p), key=lambda v: -v["score"])
        capped += mine[:MAX_PER_PERSON]
    key = {str(5000 + n): item for n, item in enumerate(capped)}
    (QUEUE / "dense-key.json").write_text(json.dumps(key, indent=0))
    tasks = [
        {"n": int(n), **{k: v[k] for k in ("idea", "who", "quote", "work")}} for n, v in key.items()
    ]
    size = len(tasks) // 5 + 1
    for part in range(5):
        (QUEUE / f"dense-{part}.json").write_text(
            json.dumps(tasks[part * size : (part + 1) * size], indent=0)
        )
    print(len(found), "found,", len(capped), "queued")


if __name__ == "__main__":
    main()
