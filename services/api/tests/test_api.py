import json
import pathlib
import secrets

import pytest
from arena_api.app import CONSENT_VERSION, create_app
from arena_api.store import Store
from arena_api.text_rules import check_statement
from fastapi.testclient import TestClient
from sqlalchemy import text

PUBLIC = pathlib.Path(__file__).parents[3] / "apps/arena/public"
BUNDLE = json.loads((PUBLIC / "fingerprint.json").read_text())


def test_text_rules():
    assert check_statement("short", []) is not None
    assert check_statement("x" * 141, []) is not None

    def reason(text: str, existing: list[str] | None = None) -> str:
        return check_statement(text, existing or []) or ""

    assert "@handles" in reason("I think @someone is right about this")
    assert "links" in reason("Read this at example.com before voting")
    assert "email" in reason("Write to me at a.b@example.org please")
    assert "already" in reason("Labs should publish evals!", ["labs should publish evals"])
    assert check_statement("Labs should publish their dangerous capability evals.", []) is None


@pytest.fixture
def client(engine):
    Store(engine).ensure_room("ai-futures", "AI futures", BUNDLE)
    Store(engine).ensure_room("demo", "Demo", BUNDLE, {"demo": True, "auto_approve": True})
    return TestClient(create_app(engine, admin_token="secret-token"))


def join(client, slug="ai-futures", answers=None):
    key = secrets.token_hex(16)
    r = client.post(
        f"/api/rooms/{slug}/join",
        json={"key": key, "consent_version": CONSENT_VERSION, "answers": answers or {}},
    )
    assert r.status_code == 200, r.text
    pid = r.json()["participant_id"]
    return {"X-Participant": pid, "X-Key": key}, pid


@pytest.mark.db
def test_join_stores_only_hash_and_answers_become_votes(client, engine):
    first = BUNDLE["anchors"][0]["id"]
    headers, pid = join(client, answers={first: 1})
    with engine.connect() as c:
        stored = c.execute(
            text("SELECT key_hash FROM room_participant WHERE participant_id = :p"), {"p": pid}
        ).scalar()
        votes = c.execute(
            text("SELECT count(*) FROM room_vote WHERE participant_id = :p"), {"p": pid}
        ).scalar()
    assert headers["X-Key"].encode() not in bytes(stored) and len(bytes(stored)) == 32
    assert votes == 1
    assert (
        client.get(
            "/api/rooms/ai-futures/next", headers={**headers, "X-Key": "wrong" * 8}
        ).status_code
        == 401
    )


@pytest.mark.db
def test_revote_updates_and_logs(client, engine):
    headers, pid = join(client)
    statement = client.get("/api/rooms/ai-futures/next?limit=1", headers=headers).json()[
        "statements"
    ][0]
    for v in (1, -1):
        assert (
            client.post(
                "/api/rooms/ai-futures/votes",
                headers=headers,
                json={"statement_id": statement["statement_id"], "vote": v},
            ).status_code
            == 200
        )
    with engine.connect() as c:
        live = c.execute(
            text("SELECT vote FROM room_vote WHERE participant_id = :p"), {"p": pid}
        ).all()
        events = c.execute(
            text("SELECT count(*) FROM room_vote_event WHERE participant_id = :p"), {"p": pid}
        ).scalar()
    assert live == [(-1,)] and events == 2
    nxt = client.get("/api/rooms/ai-futures/next?limit=20", headers=headers).json()["statements"]
    assert statement["statement_id"] not in [s["statement_id"] for s in nxt]


@pytest.mark.db
def test_statements_pending_until_approved(client):
    headers, _ = join(client)
    r = client.post(
        "/api/rooms/ai-futures/statements",
        headers=headers,
        json={"text": "Labs should publish dangerous capability evaluation results."},
    )
    assert r.status_code == 200 and r.json()["status"] == "pending"
    sid = r.json()["statement_id"]
    # the other participant has answered every anchor, so only new statements remain for them
    other, _ = join(client, answers={a["id"]: 1 for a in BUNDLE["anchors"]})
    ids = [
        s["statement_id"]
        for s in client.get("/api/rooms/ai-futures/next?limit=20", headers=other).json()[
            "statements"
        ]
    ]
    assert sid not in ids
    bad = client.post(
        "/api/rooms/ai-futures/statements", headers=headers, json={"text": "see example.com now ok"}
    )
    assert bad.status_code == 422 and "links" in bad.json()["error"]
    assert client.get("/api/admin/ai-futures/pending").status_code == 401
    admin = {"Authorization": "Bearer secret-token"}
    assert [
        p["statement_id"]
        for p in client.get("/api/admin/ai-futures/pending", headers=admin).json()["pending"]
    ] == [sid]
    assert (
        client.post(
            f"/api/admin/ai-futures/statements/{sid}", headers=admin, json={"approve": True}
        ).status_code
        == 200
    )
    ids = [
        s["statement_id"]
        for s in client.get("/api/rooms/ai-futures/next?limit=30", headers=other).json()[
            "statements"
        ]
    ]
    assert sid in ids


@pytest.mark.db
def test_admin_disabled_without_token(engine):
    Store(engine).ensure_room("ai-futures", "AI futures", BUNDLE)
    c = TestClient(create_app(engine, admin_token=None))
    assert (
        c.get("/api/admin/ai-futures/pending", headers={"Authorization": "Bearer "}).status_code
        == 404
    )


@pytest.mark.db
def test_report_aggregates_only_and_disputes(client):
    pids = []
    for i in range(12):
        answers = {a["id"]: (1 if (i + k) % 3 else -1) for k, a in enumerate(BUNDLE["anchors"])}
        _, pid = join(client, answers=answers)
        pids.append(pid)
    report = client.get("/api/rooms/ai-futures/report").json()
    assert report["participants"] == 12 and report["active"] == 12
    blob = json.dumps(report)
    assert not any(p in blob for p in pids)
    assert (
        client.post(
            "/api/disputes", json={"person_id": "vitalik-buterin", "body": "Misread his view"}
        ).status_code
        == 200
    )
    assert (
        client.post("/api/disputes", json={"person_id": "nobody", "body": "xxxxxx"}).status_code
        == 400
    )
    assert client.post("/api/fairness", json={"rating": 4}).status_code == 200
    assert client.post("/api/fairness", json={"rating": 9}).status_code == 422


@pytest.mark.db
def test_static_and_atlas(client):
    assert client.get("/fingerprint.json").json()["version"] == BUNDLE["version"]
    assert client.get("/api/rooms/demo").json()["demo"] is True
