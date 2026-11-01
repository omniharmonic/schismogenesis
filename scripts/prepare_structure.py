"""Group accepted claims into themes and write one reader task per theme. Embeddings only sort here.

Usage: prepare_structure.py
"""

import json
import pathlib
from collections import Counter

import numpy as np
from arena_core.db import get_engine
from sentence_transformers import SentenceTransformer
from sqlalchemy import text

QUEUE = pathlib.Path("evals/queue/structure-v1")
MODEL = "BAAI/bge-large-en-v1.5"
THEMES = {
    "mind": "the nature of intelligence, minds, consciousness, and what machines are",
    "risk": "catastrophic risk from AI, alignment, control, orthogonality, superintelligence",
    "progress": "technology, progress, growth, stagnation, acceleration, and the arc of history",
    "power": "who governs technology: states, companies, sovereignty, democracy, regulation",
    "ends": "what humans are for: flourishing, moral status, posthuman futures, meaning, value",
    "labor": "economy, work, capital, markets, inequality, and present harms to people",
    "knowing": "how we know: forecasting, expertise, science, truth, media, language, hype",
    "conflict": "geopolitics, war, China, nation, civilization, religion, and enemies",
}
MIN_SIMILARITY = 0.45


def main() -> None:
    engine = get_engine()
    with engine.connect() as connection:
        rows = connection.execute(
            text(
                "SELECT c.claim_id::text, p.display_name, coalesce(c.proposed_canonical,"
                " c.claim_text), c.quote_public, c.argument_role, c.tl_type::text,"
                " c.proposed_layer::text, e.title, extract(year FROM e.published_at)::int"
                " FROM claim c JOIN person p ON p.person_id = c.speaker_person_id"
                " JOIN episode e USING (episode_id) WHERE c.gate_status = 'accepted'"
            )
        ).all()
    model = SentenceTransformer(MODEL)
    names = list(THEMES)
    themes = model.encode(list(THEMES.values()), normalize_embeddings=True)
    claims = model.encode([r[2] for r in rows], normalize_embeddings=True, batch_size=32)
    scores = claims @ themes.T
    QUEUE.mkdir(parents=True, exist_ok=True)
    ids = {str(i): row[0] for i, row in enumerate(rows)}
    (QUEUE / "ids.json").write_text(json.dumps(ids))
    counts: Counter[str] = Counter()
    tasks: dict[str, list[dict]] = {name: [] for name in names}
    for i, row in enumerate(rows):
        for pick in np.argsort(scores[i])[::-1][:2]:
            if scores[i, pick] < MIN_SIMILARITY:
                continue
            name = names[pick]
            counts[name] += 1
            tasks[name].append(
                {"id": i, "who": row[1], "claim": row[2], "quote": row[3], "role": row[4],
                 "type": row[5], "layer": row[6], "work": row[7], "year": row[8]}
            )  # fmt: skip
    for name, items in tasks.items():
        items.sort(key=lambda item: item["who"])
        (QUEUE / f"theme-{name}.json").write_text(
            json.dumps({"theme": name, "about": THEMES[name], "claims": items}, indent=0)
        )
    print(len(rows), dict(counts))


if __name__ == "__main__":
    main()
