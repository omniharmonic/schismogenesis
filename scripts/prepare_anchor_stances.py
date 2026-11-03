"""Write reader tasks: one thinker's accepted claims against the season's fingerprint statements.

Usage: prepare_anchor_stances.py <batch> <person-id> [<person-id> ...]
Tasks go to evals/queue/<batch>/<person>.json; readers answer with prompt anchor_stance_v1 into
evals/results/<batch>/<reader>-<person>.json (docs/fingerprint/05-ATLAS-EXPANSION.md step E6).
"""

import json
import pathlib
import sys

from arena_core.db import get_engine
from sqlalchemy import text

BUNDLE = pathlib.Path("apps/arena/public/fingerprint.json")


def main(batch: str, *people: str) -> None:
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
            task = {"person": person, "prompt": "anchor_stance_v1", "statements": statements,
                    "claims": claims}  # fmt: skip
            (queue / f"{person}.json").write_text(json.dumps(task, ensure_ascii=False, indent=1))
            print(f"{person}: {len(claims)} claims")


if __name__ == "__main__":
    main(*sys.argv[1:])
