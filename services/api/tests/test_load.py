"""Volume check (run with `make load-test-api`): tens of thousands of people in the main room.

Times the public endpoints that read everyone's answers (results and the people map) and the
account writes, against a scratch database filled straight through SQL.
"""

import json
import os
import pathlib
import time

import pytest
from arena_api.app import Config, create_app
from arena_api.store import Store
from fastapi.testclient import TestClient
from sqlalchemy import text

pytestmark = pytest.mark.skipif(not os.environ.get("ARENA_LOAD_TEST"), reason="load test")

PUBLIC = pathlib.Path(__file__).parents[3] / "apps/arena/public"
BUNDLE = json.loads((PUBLIC / "fingerprint.json").read_text())
PEOPLE = int(os.environ.get("ARENA_LOAD_PEOPLE", "20000"))


def fill(engine, room_id) -> None:
    """PEOPLE participants, each answering every anchor with a seeded lean."""
    with engine.begin() as c:
        c.execute(
            text("""INSERT INTO room_participant (room_id, key_hash, consent_version, is_synthetic)
                    SELECT :r, sha256(i::text::bytea), 'room-v1', false
                    FROM generate_series(1, :n) AS i"""),
            {"r": room_id, "n": PEOPLE},
        )
        c.execute(
            text("""INSERT INTO room_vote (participant_id, statement_id, vote)
                    SELECT p.participant_id, s.statement_id,
                      (CASE WHEN abs(hashtext(p.participant_id::text || s.statement_id::text))
                                 % 10 < 4 THEN 1
                            WHEN abs(hashtext(p.participant_id::text || s.statement_id::text))
                                 % 10 < 8 THEN -1 ELSE 0 END)
                    FROM room_participant p CROSS JOIN room_statement s
                    WHERE p.room_id = :r AND s.room_id = :r AND s.origin = 'anchor'"""),
            {"r": room_id},
        )


def timed(label: str, fn):
    start = time.perf_counter()
    out = fn()
    took = time.perf_counter() - start
    print(f"  {label}: {took * 1000:.0f} ms")
    return out, took


def test_large_room(engine):
    Store(engine).ensure_room("ai-futures", "AI futures", BUNDLE)
    room = Store(engine).room("ai-futures")
    assert room is not None
    room_id = room["room_id"]
    _, filled = timed(f"fill {PEOPLE} people", lambda: fill(engine, room_id))
    client = TestClient(create_app(engine, config=Config(admin_token="t" * 24)))
    print(f"\n{PEOPLE} people in the room")
    results, t_results = timed("/api/results (cold)", lambda: client.get("/api/results").json())
    assert results["contributors"] == PEOPLE
    people, t_people = timed("/api/map/people (cold)", lambda: client.get("/api/map/people").json())
    assert people["count"] == PEOPLE and people["bins"]
    size = len(json.dumps(people))
    print(f"  people map payload: {size / 1024:.0f} KB, {len(people['bins']['cells'])} cells")
    timed("/api/map/people (warm)", lambda: client.get("/api/map/people"))
    b = TestClient(create_app(engine, config=Config(admin_token="t" * 24)),
                   base_url="http://localhost:8800")  # fmt: skip
    b.post("/api/auth/key/new")
    answers = {a["id"]: 1 for a in BUNDLE["anchors"]}
    timed("PUT /api/me/answers", lambda: b.put("/api/me/answers", json={"answers": answers}))
    timed("GET /api/me", lambda: b.get("/api/me"))
    # budgets: a cold read must finish well inside the function's 60 s limit, and the payload
    # must stay small for phones; the CDN serves the warm copy to everyone else
    assert t_results < 30 and t_people < 30 and size < 400_000
