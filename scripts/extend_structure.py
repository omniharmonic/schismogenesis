"""Extend the checked structure with the widened atlas (docs/fingerprint/05-ATLAS-EXPANSION.md, E7).

Usage: extend_structure.py seed | propose | apply

seed     start structure-v2 from structure-v1/structure-dense.json and fold in every stance on the
         season statements that two blind readers agreed on (anchor-stances-v1..v3)
propose  code proposes holdings: for each person and idea, the person's nearest accepted claims,
         scored by the local entailment model; strong ones are queued for two blind readers
apply    keep a proposed holding only when both readers give the same verdict

Code proposes, readers decide, nothing is ratified. Embeddings only sort.
"""

import json
import pathlib
import sys

V1 = pathlib.Path("evals/results/structure-v1/structure-dense.json")
QUEUE = pathlib.Path("evals/queue/structure-v2")
RESULTS = pathlib.Path("evals/results/structure-v2")
OUT = RESULTS / "structure.json"
PEOPLE = pathlib.Path("evals/queue/structure-v2/people.json")
EMBED = "BAAI/bge-large-en-v1.5"
NLI = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
TOP = 3
MIN_SIMILAR = 0.60
MIN_NLI = 0.80
MAX_PER_PERSON = 60
PARTS = 6
STANCE_BATCHES = ("anchor-stances-v1", "anchor-stances-v2", "anchor-stances-v3")


def seed() -> None:
    from arena_fingerprint.stances import MergeReport, valid_items

    structure = json.loads(V1.read_text())
    ideas = {i["key"]: i for i in structure["ideas"]}
    owner = claim_owners()
    held = {(i["key"], owner.get(h["claim"])) for i in structure["ideas"] for h in i["holdings"]}
    added = 0
    for batch in STANCE_BATCHES:
        queue, results = pathlib.Path("evals/queue") / batch, pathlib.Path("evals/results") / batch
        for task_path in sorted(queue.glob("*.json")):
            task = json.loads(task_path.read_text())
            person = task["person"]
            readings = {
                r: json.loads(p.read_text())
                for r in "AB"
                if (p := results / f"{r}-{person}.json").exists()
            }
            if len(readings) < 2:
                continue
            report = MergeReport()
            a = valid_items(readings["A"], task, report, "A")
            b = valid_items(readings["B"], task, report, "B")
            for statement in set(a) & set(b):
                if a[statement]["stance"] != b[statement]["stance"] or statement not in ideas:
                    continue
                if (statement, person) in held:
                    continue
                attitude = "accepts" if a[statement]["stance"] == "hold" else "rejects"
                ideas[statement]["holdings"].append(
                    {"claim": a[statement]["claim_id"], "attitude": attitude, "source": batch}
                )
                held.add((statement, person))
                added += 1
    structure.setdefault("review", {})["statement_stances_added"] = added
    RESULTS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(structure, ensure_ascii=False, indent=0))
    print(f"structure-v2 seeded: {added} statement stances added as holdings")


def claim_owners() -> dict[str, str]:
    from arena_core.db import get_engine
    from sqlalchemy import text

    with get_engine().connect() as c:
        rows = c.execute(text("SELECT claim_id::text, speaker_person_id FROM claim")).all()
    return {r[0]: r[1] for r in rows}


def propose() -> None:
    import numpy as np
    import torch
    from arena_core.db import get_engine
    from sentence_transformers import SentenceTransformer
    from sqlalchemy import text
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    structure = json.loads(OUT.read_text())
    people = set(json.loads(PEOPLE.read_text()))
    ideas = [i for i in structure["ideas"] if not i["root"]]
    with get_engine().connect() as connection:
        rows = [
            r
            for r in connection.execute(
                text(
                    "SELECT c.claim_id::text, c.speaker_person_id, p.display_name, c.quote_public,"
                    " e.title FROM claim c JOIN person p ON p.person_id = c.speaker_person_id"
                    " JOIN episode e USING (episode_id) WHERE c.gate_status = 'accepted'"
                    " AND c.tl_attitude NOT IN ('suspends', 'accepts_for_argument')"
                    " AND c.quote_public IS NOT NULL"
                )
            ).all()
            if r[1] in people
        ]
    owner = {r[0]: r[1] for r in rows} | claim_owners()
    held = {(i["key"], owner.get(h["claim"])) for i in structure["ideas"] for h in i["holdings"]}
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = SentenceTransformer(EMBED, device=device)
    claims = model.encode([r[3] for r in rows], normalize_embeddings=True, batch_size=32)
    vectors = model.encode([i["canonical"] for i in ideas], normalize_embeddings=True)
    by_person: dict[str, list[int]] = {}
    for n, r in enumerate(rows):
        by_person.setdefault(r[1], []).append(n)

    pairs = []
    for p, index_list in sorted(by_person.items()):
        index = np.array(index_list)
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
                }  # fmt: skip
        if start % 3200 == 0:
            print(start, len(found), flush=True)

    capped = []
    for p in sorted(by_person):
        mine = sorted((v for v in found.values() if v["person"] == p), key=lambda v: -v["score"])
        capped += mine[:MAX_PER_PERSON]
    key = {str(10000 + n): item for n, item in enumerate(capped)}
    QUEUE.mkdir(parents=True, exist_ok=True)
    (QUEUE / "dense-key.json").write_text(json.dumps(key, indent=0))
    tasks = [
        {"n": int(n), **{k: v[k] for k in ("idea", "who", "quote", "work")}} for n, v in key.items()
    ]
    size = len(tasks) // PARTS + 1
    for part in range(PARTS):
        (QUEUE / f"dense-{part}.json").write_text(
            json.dumps(tasks[part * size : (part + 1) * size], indent=0)
        )
    print(len(found), "found,", len(capped), "queued in", PARTS, "parts")


def apply() -> None:
    structure = json.loads(OUT.read_text())
    ideas = {i["key"]: i for i in structure["ideas"]}
    key = json.loads((QUEUE / "dense-key.json").read_text())
    verdicts: dict[str, dict[str, str]] = {"a": {}, "b": {}}
    for reader in "ab":
        for part in range(PARTS):
            path = RESULTS / f"check-dense-{reader}-{part}.json"
            if path.exists():
                for v in json.loads(path.read_text())["verdicts"]:
                    verdicts[reader][str(v["n"])] = v["verdict"]
    agreed = disagreed = missing = 0
    for n, item in key.items():
        a, b = verdicts["a"].get(n), verdicts["b"].get(n)
        if a is None or b is None:
            missing += 1
            continue
        if a != b:
            disagreed += 1
            continue
        if a in ("accepts", "rejects"):
            ideas[item["idea_key"]]["holdings"].append(
                {"claim": item["claim_id"], "attitude": a, "source": "dense-v2"}
            )
            agreed += 1
    review = structure.setdefault("review", {})
    review |= {"dense2_candidates": len(key), "dense2_agreed": agreed,
               "dense2_disagreed": disagreed, "dense2_missing": missing}  # fmt: skip
    OUT.write_text(json.dumps(structure, ensure_ascii=False, indent=0))
    print(
        f"{len(key)} proposed, {agreed} agreed holdings added, {disagreed} split, {missing} missing"
    )


if __name__ == "__main__":
    {"seed": seed, "propose": propose, "apply": apply}[sys.argv[1]]()
