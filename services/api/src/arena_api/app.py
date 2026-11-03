"""The arena web app: static fingerprint pages plus the room API.

See docs/fingerprint/02-ARCHITECTURE.md.
"""

import json
import os
import pathlib
import secrets
import time
from collections import defaultdict, deque

from arena_rounds.report import participant_view, room_report
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import Engine

from arena_api.store import Store
from arena_api.text_rules import check_statement

REPO = pathlib.Path(__file__).resolve().parents[4]
PUBLIC = REPO / "apps/arena/public"
CONSENT_VERSION = "room-v1"
STATEMENTS_PER_DAY = 5


class RateLimit:
    """In-memory sliding window. Enough for a one-process private beta (architecture §8)."""

    def __init__(self) -> None:
        self.hits: dict[str, deque] = defaultdict(deque)

    def check(self, key: str, limit: int, window: float = 3600.0) -> None:
        now = time.monotonic()
        q = self.hits[key]
        while q and now - q[0] > window:
            q.popleft()
        if len(q) >= limit:
            raise HTTPException(429, "Too many requests. Try again later.")
        q.append(now)


class Join(BaseModel):
    key: str = Field(min_length=32, max_length=128)
    handle: str | None = Field(default=None, max_length=40)
    consent_version: str
    answers: dict[str, int] = Field(default_factory=dict)


class Vote(BaseModel):
    statement_id: str
    vote: int = Field(ge=-1, le=1)


class NewStatement(BaseModel):
    text: str = Field(max_length=400)


class Dispute(BaseModel):
    person_id: str
    anchor_id: str | None = None
    body: str = Field(min_length=5, max_length=2000)
    contact: str | None = Field(default=None, max_length=200)


class Fairness(BaseModel):
    rating: int = Field(ge=1, le=5)


class Moderation(BaseModel):
    approve: bool
    reason: str | None = Field(default=None, max_length=200)


def create_app(
    engine: Engine, admin_token: str | None = None, public: pathlib.Path = PUBLIC
) -> FastAPI:
    bundle = json.loads((public / "fingerprint.json").read_text())
    thinker_ids = {t["id"] for t in bundle["thinkers"]}
    anchor_ids = {a["id"] for a in bundle["anchors"]}
    store = Store(engine)
    limits = RateLimit()
    cache: dict[tuple, dict] = {}
    app = FastAPI(title="Dialogos: AI Futures Fingerprint", docs_url=None, redoc_url=None)

    def client(request: Request) -> str:
        return request.client.host if request.client else "unknown"

    def get_room(slug: str) -> dict:
        room = store.room(slug)
        if room is None:
            raise HTTPException(404, "No such room.")
        return room

    def participant(
        slug: str, x_participant: str = Header(...), x_key: str = Header(...)
    ) -> tuple[dict, str]:
        room = get_room(slug)
        if not store.authenticate(room["room_id"], x_participant, x_key):
            raise HTTPException(401, "Unknown participant for this room.")
        return room, x_participant

    def admin(authorization: str | None = Header(default=None)) -> None:
        if not admin_token:
            raise HTTPException(404, "Admin is disabled.")
        supplied = (authorization or "").removeprefix("Bearer ").strip()
        if not secrets.compare_digest(supplied, admin_token):
            raise HTTPException(401, "Wrong admin token.")

    def report_for(room: dict) -> tuple[dict, list, dict, bool]:
        demo = bool(room["config"].get("demo"))
        version = (str(room["room_id"]), *store.vote_version(room["room_id"]))
        rows = store.vote_rows(room["room_id"])
        statements = store.approved_statements(room["room_id"])
        if version not in cache:
            cache.clear()
            cache[version] = room_report(rows, statements, bundle, demo)
        return cache[version], rows, statements, demo

    @app.get("/api/rooms/{slug}")
    def room_info(slug: str):
        room = get_room(slug)
        return {
            "slug": room["slug"],
            "title": room["title"],
            "description": room["description"],
            "status": room["status"],
            "demo": bool(room["config"].get("demo")),
            **store.counts(room["room_id"], bool(room["config"].get("demo"))),
        }

    @app.post("/api/rooms/{slug}/join")
    def join(slug: str, body: Join, request: Request):
        limits.check(f"join:{client(request)}", 30)
        room = get_room(slug)
        if room["status"] != "open":
            raise HTTPException(409, "This room is closed.")
        if body.consent_version != CONSENT_VERSION:
            raise HTTPException(400, "Please reload: the consent text has changed.")
        if bad := set(body.answers) - anchor_ids:
            raise HTTPException(400, f"Unknown statements: {sorted(bad)[:3]}")
        if any(v not in (-1, 0, 1) for v in body.answers.values()):
            raise HTTPException(400, "Votes are -1, 0 or 1.")
        handle = (body.handle or "").strip().lstrip("@") or None
        pid = store.join(room["room_id"], body.key, handle, body.consent_version)
        ids = store.anchor_statements(room["room_id"])
        store.votes_bulk([(pid, ids[a], v) for a, v in body.answers.items() if a in ids])
        return {"participant_id": pid}

    @app.get("/api/rooms/{slug}/next")
    def next_statements(limit: int = 5, who: tuple = Depends(participant)):
        room, pid = who
        return {"statements": store.next_statements(room["room_id"], pid, max(1, min(limit, 20)))}

    @app.post("/api/rooms/{slug}/votes")
    def vote(body: Vote, who: tuple = Depends(participant)):
        room, pid = who
        limits.check(f"vote:{pid}", 600)
        if not store.statement_in_room(room["room_id"], body.statement_id):
            raise HTTPException(404, "No such statement in this room.")
        store.vote(pid, body.statement_id, body.vote)
        return {"ok": True}

    @app.post("/api/rooms/{slug}/statements")
    def write(body: NewStatement, who: tuple = Depends(participant)):
        room, pid = who
        if store.statements_today(pid) >= STATEMENTS_PER_DAY:
            raise HTTPException(429, f"You can add {STATEMENTS_PER_DAY} statements a day.")
        text_ = " ".join(body.text.split())
        if reason := check_statement(text_, store.texts(room["room_id"])):
            raise HTTPException(422, reason)
        auto = bool(room["config"].get("auto_approve"))
        sid = store.add_statement(
            room["room_id"], text_, pid, status="approved" if auto else "pending"
        )
        return {"statement_id": sid, "status": "approved" if auto else "pending"}

    @app.get("/api/rooms/{slug}/report")
    def report(slug: str):
        return report_for(get_room(slug))[0]

    @app.get("/api/rooms/{slug}/me")
    def me(who: tuple = Depends(participant)):
        room, pid = who
        _, rows, statements, demo = report_for(room)
        return participant_view(rows, statements, bundle, demo, pid)

    @app.post("/api/disputes")
    def dispute(body: Dispute, request: Request):
        limits.check(f"dispute:{client(request)}", 20)
        if body.person_id not in thinker_ids:
            raise HTTPException(400, "Unknown thinker.")
        if body.anchor_id and body.anchor_id not in anchor_ids:
            raise HTTPException(400, "Unknown statement.")
        store.add_dispute(body.person_id, body.anchor_id, body.body.strip(), body.contact)
        return {"ok": True}

    @app.post("/api/fairness")
    def fairness(body: Fairness, request: Request):
        limits.check(f"fair:{client(request)}", 20)
        store.add_fairness(bundle["version"], body.rating)
        return {"ok": True}

    @app.get("/api/admin/{slug}/pending", dependencies=[Depends(admin)])
    def pending(slug: str):
        return {
            "pending": store.pending(get_room(slug)["room_id"]),
            "disputes": store.disputes(),
            "fairness": store.fairness(),
        }

    @app.post("/api/admin/{slug}/statements/{statement_id}", dependencies=[Depends(admin)])
    def moderate(slug: str, statement_id: str, body: Moderation):
        if not store.moderate(get_room(slug)["room_id"], statement_id, body.approve, body.reason):
            raise HTTPException(404, "No pending statement with that id.")
        return {"ok": True}

    @app.exception_handler(HTTPException)
    def error(_: Request, exc: HTTPException):
        return JSONResponse({"error": exc.detail}, status_code=exc.status_code)

    @app.get("/atlas")
    def atlas():
        return FileResponse(public / "atlas.html")

    app.mount("/", StaticFiles(directory=public, html=True), name="public")
    return app


def main() -> None:
    import uvicorn
    from arena_core.db import get_engine

    port = int(os.environ.get("ARENA_APP_PORT", "8800"))
    app = create_app(get_engine(), admin_token=os.environ.get("ARENA_ADMIN_TOKEN"))
    uvicorn.run(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
