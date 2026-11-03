"""Write reader tasks: one thinker's accepted claims against the season's fingerprint statements.

Usage: prepare_anchor_stances.py <batch> [--top N] <person-id> [<person-id> ...]
With --top N, each task keeps the N claims closest in meaning to any statement (bge-large, local),
so readers see the evidence that matters; quotes are still checked in code.
Tasks go to evals/queue/<batch>/<person>.json; readers answer with prompt anchor_stance_v1 into
evals/results/<batch>/<reader>-<person>.json (docs/fingerprint/05-ATLAS-EXPANSION.md step E6).
"""

import json
import pathlib
import sys

from arena_core.db import get_engine
from sqlalchemy import text

BUNDLE = pathlib.Path("apps/arena/public/fingerprint.json")


_MODEL = []


def _model():
    if not _MODEL:
        from sentence_transformers import SentenceTransformer

        _MODEL.append(SentenceTransformer("BAAI/bge-large-en-v1.5"))
    return _MODEL[0]


def shortlist(claims: list[dict], statements: list[dict], top: int) -> list[dict]:
    if len(claims) <= top:
        return claims
    model = _model()
    c = model.encode([x["text"] for x in claims], normalize_embeddings=True)
    s = model.encode([x["text"] for x in statements], normalize_embeddings=True)
    best = (c @ s.T).max(1)
    keep = sorted(range(len(claims)), key=lambda i: -best[i])[:top]
    return [claims[i] for i in sorted(keep)]


def main(batch: str, *args: str) -> None:
    top = int(args[args.index("--top") + 1]) if "--top" in args else 0
    people = [a for a in args if not a.startswith("--") and not a.isdigit()]
    bundle = json.loads(BUNDLE.read_text())
    statements = [{"id": a["id"], "text": a["text"]} for a in bundle["anchors"]]
    queue = pathlib.Path("evals/queue") / batch
    queue.mkdir(parents=True, exist_ok=True)
    with get_engine().connect() as c:
        for person in people:
            rows = c.execute(
                text("""SELECT c.claim_id, c.claim_text, c.quote_public, c.deep_link, e.title
                        FROM claim c JOIN episode e USING (episode_id)
                        WHERE c.speaker_person_id = :p AND c.gate_status = 'accepted'
                        ORDER BY e.title, c.created_at"""),
                {"p": person},
            ).all()
            claims = [
                {"id": str(r[0]), "text": r[1], "quote": r[2], "url": r[3], "work": r[4]}
                for r in rows
                if r[2]
            ]
            if top:
                claims = shortlist(claims, statements, top)
            task = {"person": person, "prompt": "anchor_stance_v1", "statements": statements,
                    "claims": claims}  # fmt: skip
            (queue / f"{person}.json").write_text(json.dumps(task, ensure_ascii=False, indent=1))
            print(f"{person}: {len(claims)} claims")


if __name__ == "__main__":
    main(*sys.argv[1:])
