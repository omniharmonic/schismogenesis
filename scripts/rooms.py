"""Create the rooms the app needs, and fill the demo room with labelled synthetic voters.

Usage:
  rooms.py ensure            create room "ai-futures" (real) if missing
  rooms.py demo [n]          create room "demo" and add n synthetic voters (default 120)
Synthetic voters are flagged and only ever counted in rooms whose config says demo (PRD R14).
"""

import json
import pathlib
import secrets
import sys

from arena_api.store import Store
from arena_core.db import get_engine
from arena_rounds.synthetic import DEMO_STATEMENTS, synthetic_votes
from sqlalchemy import text

REPO = pathlib.Path(__file__).resolve().parents[1]
BUNDLE = json.loads((REPO / "apps/arena/public/fingerprint.json").read_text())


def ensure(store: Store) -> None:
    store.ensure_room("ai-futures", "Where the AI futures conversation stands", BUNDLE)
    print("room ai-futures ready")


def demo(store: Store, n: int = 120) -> None:
    room = store.ensure_room(
        "demo", "Demo room: how the report works", BUNDLE, {"demo": True, "auto_approve": True}
    )
    with store.engine.connect() as c:
        config = c.execute(text("SELECT config FROM room WHERE room_id = :r"), {"r": room}).scalar()
        already = c.execute(
            text("SELECT count(*) FROM room_participant WHERE room_id = :r AND is_synthetic"),
            {"r": room},
        ).scalar()
    if not (config or {}).get("demo"):
        raise SystemExit("refusing: room 'demo' exists without demo config")
    if already:
        print(f"demo room already has {already} synthetic voters")
        return
    existing = {
        t: sid for sid, t in ((s, d["text"]) for s, d in store.approved_statements(room).items())
    }
    extra = {}
    for kind, statement in DEMO_STATEMENTS:
        sid = existing.get(statement) or store.add_statement(
            room, statement, None, status="approved"
        )
        extra[sid] = kind
    anchors = store.anchor_statements(room)
    rows, _ = synthetic_votes(BUNDLE, extra, n=n)
    ids: dict[str, str] = {}
    out = []
    for participant, statement, vote in rows:
        if participant not in ids:
            ids[participant] = store.join(
                room, secrets.token_hex(32), None, "synthetic", synthetic=True
            )
        out.append((ids[participant], anchors.get(statement, statement), vote))
    store.votes_bulk(out)
    print(f"demo room: {len(ids)} synthetic voters, {len(out)} votes")


def main(command: str = "ensure", *args: str) -> None:
    store = Store(get_engine())
    if command == "ensure":
        ensure(store)
    elif command == "demo":
        demo(store, int(args[0]) if args else 120)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(*sys.argv[1:])
