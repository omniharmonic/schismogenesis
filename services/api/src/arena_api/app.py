"""The arena web app: static fingerprint pages, rooms, published profiles and share images.

See docs/fingerprint/02-ARCHITECTURE.md and 04-LAUNCH.md.
"""

import base64
import datetime
import hashlib
import html
import json
import os
import pathlib
import re
import secrets
import time
import urllib.parse
from dataclasses import dataclass

from arena_rounds.report import Analysis, analyse, personal_view
from arena_rounds.results import results as public_results
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import Engine

from arena_api import account_routes, identity, turnstile
from arena_api.account_store import AccountPages
from arena_api.cards import profile_card, statement_card
from arena_api.profiles import (
    Summary,
    SummaryError,
    anon_name,
    clean_answers,
    clean_glyph,
    clean_summary,
    new_code,
)
from arena_api.store import Store, key_hash
from arena_api.text_rules import check_statement

GATE_PATH = "/__preview"
GATE_COOKIE = "dialogos_preview"


def gate_page(target: str, wrong: bool = False) -> HTMLResponse:
    """The pre-launch password page. Plain HTML so it works in any browser, scripts or not."""
    note = '<p class="no">That password didn\'t match. Try again.</p>' if wrong else ""
    body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Preview: The Great AI Debate</title>
<style>
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#121820;
color:#dde4eb;font:17px/1.5 Georgia,serif}}
form{{width:min(360px,calc(100vw - 32px));border:1px solid #2b3644;background:#161d26;padding:24px}}
.k{{font:13px "Arial Narrow",system-ui,sans-serif;color:#9aa7b6;margin:0 0 8px}}
h1{{font:400 26px/1.15 Georgia,serif;margin:0 0 6px}}
p{{margin:0 0 18px;color:#9aa7b6}} .no{{color:#ff5468}}
label{{display:block;font:14px system-ui,sans-serif;margin-bottom:6px}}
input{{box-sizing:border-box;width:100%;font:16px system-ui,sans-serif;padding:11px 12px;
background:#121820;color:#dde4eb;border:1px solid #3a4757;border-radius:2px;margin-bottom:12px}}
button{{width:100%;font:600 16px system-ui,sans-serif;padding:11px;border:0;border-radius:2px;
background:#dde4eb;color:#121820;cursor:pointer}}
button:focus-visible,input:focus-visible{{outline:3px solid #8fb0ff;outline-offset:2px}}
</style></head><body>
<form method="post" action="{GATE_PATH}">
<p class="k">antimemes.is</p>
<h1>The Great AI Debate is in preview</h1>
<p>Enter the preview password to continue.</p>{note}
<label for="pw">Password</label>
<input id="pw" name="password" type="password" autocomplete="current-password" autofocus required>
<input type="hidden" name="next" value="{html.escape(target, quote=True)}">
<button type="submit">Open the preview</button>
</form></body></html>"""
    return HTMLResponse(body, status_code=401, headers={"Cache-Control": "no-store"})


_HERE = pathlib.Path(__file__).resolve()
# in the repo this is the root; in a flat deploy folder (build/vercel) paths come from the env
REPO = _HERE.parents[4] if len(_HERE.parents) > 4 else _HERE.parent
PUBLIC = pathlib.Path(os.environ.get("ARENA_PUBLIC_DIR") or REPO / "apps/arena/public")
CONSENT_VERSION = "room-v1"
STATEMENTS_PER_DAY = 5
REPORT_MAX_AGE = 60  # seconds a stale report may be served while votes arrive
MAX_BODY = 64 * 1024
EVENTS = {
    "start",
    "finish",
    "story_done",
    "save_story",
    "save_card",
    "share_native",
    "share_x",
    "share_bsky",
    "copy_text",
    "copy_link",
    "join",
    "publish",
}
ATLAS_SCRIPTS = (
    "script-src 'self' 'unsafe-inline' "
    "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js "
    "https://cdn.jsdelivr.net/npm/3d-force-graph@1.79.0/dist/3d-force-graph.min.js"
)
CSP = (
    "default-src 'self'; script-src 'self' https://challenges.cloudflare.com; "
    "frame-src https://challenges.cloudflare.com; "
    "style-src 'self' 'unsafe-inline'; font-src 'self'; "
    "img-src 'self' data: blob: https://cdn.bsky.app https://pbs.twimg.com; "
    "connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
)


def csp_for(atlas: bool = False) -> str:
    """The page's Content-Security-Policy. The 3D atlas page is one self-contained file with an
    inline script and two pinned libraries from CDNs; no other page may load outside scripts.
    Also written into the CDN headers by scripts/build_vercel.py, so both stay identical."""
    if not atlas:
        return CSP
    return (
        CSP.replace("script-src 'self' https://challenges.cloudflare.com", ATLAS_SCRIPTS)
        .replace("style-src 'self'", "style-src 'self' https://fonts.googleapis.com")
        .replace("font-src 'self'", "font-src 'self' https://fonts.gstatic.com")
    )


@dataclass(frozen=True)
class Config:
    admin_token: str | None = None
    public_url: str = "http://localhost:8800"
    x_client_id: str | None = None
    x_client_secret: str | None = None
    trust_proxy: bool = False
    proxy_hops: int = 1  # proxies we control in front of the app
    client_ip_header: str | None = None  # e.g. Fly-Client-IP or CF-Connecting-IP
    production: bool = False
    site_password: str | None = None  # pre-launch gate: every page asks for it while set
    rate_salt: str | None = None  # shared by every instance, so rate limits hold across them
    turnstile_site_key: str | None = None
    turnstile_secret: str | None = None
    resend_key: str | None = None  # email sign-in (Resend, send-only key)
    mail_from: str = "antimemes <signin@omniharmonic.com>"

    @classmethod
    def from_env(cls) -> "Config":
        env = os.environ.get
        config = cls(
            admin_token=env("ARENA_ADMIN_TOKEN") or None,
            public_url=(env("ARENA_PUBLIC_URL") or "http://localhost:8800").rstrip("/"),
            x_client_id=env("ARENA_X_CLIENT_ID") or None,
            x_client_secret=env("ARENA_X_CLIENT_SECRET") or None,
            trust_proxy=env("ARENA_TRUST_PROXY") == "1",
            proxy_hops=int(env("ARENA_PROXY_HOPS") or "1"),
            client_ip_header=env("ARENA_CLIENT_IP_HEADER") or None,
            production=env("ARENA_ENV") == "production",
            rate_salt=env("ARENA_RATE_SALT") or None,
            site_password=env("ARENA_SITE_PASSWORD") or None,
            turnstile_site_key=env("ARENA_TURNSTILE_SITE_KEY") or None,
            turnstile_secret=env("ARENA_TURNSTILE_SECRET") or None,
            resend_key=env("ARENA_RESEND_KEY") or None,
            mail_from=env("ARENA_MAIL_FROM") or "antimemes <signin@omniharmonic.com>",
        )
        if config.production and (not config.admin_token or len(config.admin_token) < 24):
            raise RuntimeError("ARENA_ADMIN_TOKEN of 24+ characters is required in production")
        if config.production and not config.rate_salt:
            raise RuntimeError("ARENA_RATE_SALT is required in production")
        return config


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


class Publish(BaseModel):
    summary: Summary
    glyph: list[int | None]
    answers: dict[str, int] | None = None
    identity: str = Field(pattern="^(anon|bsky|x)$")
    check_id: str | None = None
    listed: bool = False


class ProfileEdit(BaseModel):
    listed: bool


class BskyStart(BaseModel):
    handle: str = Field(max_length=260)


class CheckId(BaseModel):
    check_id: str


class Event(BaseModel):
    name: str


class Hide(BaseModel):
    hidden: bool


def create_app(
    engine: Engine,
    admin_token: str | None = None,
    public: pathlib.Path = PUBLIC,
    config: Config | None = None,
    fetch: identity.Fetch = identity.fetch_json,
    human: turnstile.Verifier = turnstile.verify,
    account_options: dict | None = None,
) -> FastAPI:
    config = config or Config(admin_token=admin_token)
    bundle = json.loads((public / "fingerprint.json").read_text())
    names = {t["id"]: t["name"] for t in bundle["thinkers"]}
    thinker_ids = set(names)
    anchor_ids = {a["id"] for a in bundle["anchors"]}
    store = Store(engine)
    astore = AccountPages(engine)
    # rate-limit buckets hold hashed addresses, never raw ones
    salt = config.rate_salt or secrets.token_hex(16)
    app = FastAPI(title="The Great AI Debate (antimemes.is)", docs_url=None, redoc_url=None)

    @app.middleware("http")
    async def launch_gate(request: Request, call_next):
        """Until launch, the whole site sits behind one shared password.

        People get a small password page that sets a cookie, which works in every browser (some,
        like Dia, never show the built-in basic-auth prompt). Basic auth still works for scripts.
        """
        if not config.site_password or request.url.path == "/api/health":
            return await call_next(request)
        token = hashlib.sha256(f"dialogos-gate:{config.site_password}".encode()).hexdigest()
        if request.url.path == GATE_PATH and request.method == "POST":
            form = urllib.parse.parse_qs((await request.body()).decode(errors="replace"))
            supplied = form.get("password", [""])[0]
            target = form.get("next", ["/"])[0]
            if not target.startswith("/") or target.startswith("//"):
                target = "/"
            if secrets.compare_digest(supplied, config.site_password):
                response = Response(status_code=303, headers={"Location": target})
                response.set_cookie(
                    GATE_COOKIE, token, max_age=30 * 86400, httponly=True,
                    secure=request.url.scheme == "https", samesite="lax",
                )  # fmt: skip
                return response
            return gate_page(target, wrong=True)
        if secrets.compare_digest(request.cookies.get(GATE_COOKIE, ""), token):
            return await call_next(request)
        supplied = ""
        header = request.headers.get("authorization", "")
        if header.startswith("Basic "):
            try:
                supplied = base64.b64decode(header[6:]).decode().split(":", 1)[-1]
            except (ValueError, UnicodeDecodeError):
                supplied = ""
        if secrets.compare_digest(supplied, config.site_password):
            return await call_next(request)
        if request.url.path.startswith("/api/"):
            return JSONResponse({"error": "This site isn't open yet."}, status_code=401)
        path = request.url.path + (f"?{request.url.query}" if request.url.query else "")
        return gate_page(path)

    @app.middleware("http")
    async def guard(request: Request, call_next):
        length = request.headers.get("content-length")
        if length and length.isdigit() and int(length) > MAX_BODY:
            return JSONResponse({"error": "Request too large."}, status_code=413)
        if request.method in ("POST", "PATCH", "PUT") and not length:
            # chunked bodies have no declared length: read up to the cap before handling
            body = b""
            async for chunk in request.stream():
                body += chunk
                if len(body) > MAX_BODY:
                    return JSONResponse({"error": "Request too large."}, status_code=413)
            request._body = body  # starlette reuses this when the route reads the body
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = csp_for(
            request.url.path in ("/atlas", "/atlas.html")
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if config.production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        path = request.url.path
        shared = (
            request.method == "GET"
            and response.status_code == 200
            and (
                path
                in (
                    "/api/results",
                    "/api/people",
                    "/api/config",
                    "/api/map/people",
                    "/api/camps/accepted",
                )
                or path == "/oauth/client-metadata.json"
                or path.startswith(("/s/", "/p/"))
                or (path.startswith("/api/rooms/") and path.count("/") == 3)
            )
        )
        if shared and "Cache-Control" not in response.headers:
            # Public, aggregate answers: the CDN keeps them a minute and serves the last copy
            # while it refreshes, so a visitor never waits on a cold function or database.
            response.headers["Cache-Control"] = (
                "public, max-age=0, s-maxage=60, stale-while-revalidate=600"
            )
        elif path.startswith("/api/"):
            response.headers.setdefault("Cache-Control", "no-store")
        elif request.url.path.startswith("/fonts/"):
            response.headers.setdefault("Cache-Control", "public, max-age=31536000, immutable")
        else:
            # pages, scripts and data change together on each deploy: always revalidate (cheap,
            # the ETag answers 304), so no browser mixes a new page with an old cached module
            response.headers.setdefault("Cache-Control", "no-cache")
        return response

    def client(request: Request) -> str:
        address = request.client.host if request.client else "unknown"
        if config.client_ip_header:
            address = request.headers.get(config.client_ip_header, "").strip() or address
        elif config.trust_proxy:
            # The leftmost entry is whatever the visitor sent; proxies append the real address,
            # so count from the right past our own trusted proxies.
            hops = [
                h.strip()
                for h in request.headers.get("x-forwarded-for", "").split(",")
                if h.strip()
            ]
            if len(hops) >= config.proxy_hops:
                address = hops[-config.proxy_hops]
        return hashlib.sha256(f"{salt}:{address}".encode()).hexdigest()[:24]

    def require_human(request: Request) -> None:
        """Bot protection on actions that write: a Turnstile token, when Turnstile is on."""
        if not config.turnstile_secret:
            return
        token = request.headers.get("x-turnstile", "")
        address = request.client.host if request.client else None
        if not human(config.turnstile_secret, token, address):
            raise HTTPException(403, "The bot check didn't pass. Reload the page and try again.")

    def limit(bucket: str, count: int, window: int = 3600) -> None:
        if not store.hit(bucket, count, window):
            raise HTTPException(429, "Too many requests. Try again later.")

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
        if not config.admin_token:
            raise HTTPException(404, "Admin is disabled.")
        supplied = (authorization or "").removeprefix("Bearer ").strip()
        if not secrets.compare_digest(supplied, config.admin_token):
            raise HTTPException(401, "Wrong admin token.")

    def analysis_for(room: dict) -> Analysis:
        """Serve the cached report when current, or when fresh enough during a burst of votes."""
        version = json.dumps(store.vote_version(room["room_id"]), default=str)
        cached = store.cached_report(room["room_id"])
        if cached and (cached["version"] == version or cached["age"] < REPORT_MAX_AGE):
            return Analysis(cached["report"], cached["personal"])
        with engine.begin() as connection:
            if not store.try_report_lock(connection, room["room_id"]) and cached:
                return Analysis(cached["report"], cached["personal"])  # another worker is on it
            demo = bool(room["config"].get("demo"))
            rows = store.vote_rows(room["room_id"])
            result = analyse(rows, store.approved_statements(room["room_id"]), bundle, demo)
            store.save_report(room["room_id"], version, result.report, result.personal)
        return result

    # ---------- rooms ----------

    @app.get("/api/config")
    def public_config():
        return {
            "turnstile_site_key": config.turnstile_site_key if config.turnstile_secret else None
        }

    @app.get("/api/health")
    def health():
        with engine.connect():
            pass
        return {"ok": True, "bundle": bundle["version"]}

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
        limit(f"join:{client(request)}", 30)
        require_human(request)
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
        store.count("join")
        return {"participant_id": pid}

    @app.get("/api/rooms/{slug}/next")
    def next_statements(limit: int = 5, who: tuple = Depends(participant)):
        room, pid = who
        return {"statements": store.next_statements(room["room_id"], pid, max(1, min(limit, 20)))}

    @app.post("/api/rooms/{slug}/votes")
    def vote(body: Vote, who: tuple = Depends(participant)):
        room, pid = who
        limit(f"vote:{pid}", 600)
        if not store.statement_in_room(room["room_id"], body.statement_id):
            raise HTTPException(404, "No such statement in this room.")
        store.vote(pid, body.statement_id, body.vote)
        return {"ok": True}

    @app.post("/api/rooms/{slug}/statements")
    def write(body: NewStatement, request: Request, who: tuple = Depends(participant)):
        room, pid = who
        require_human(request)
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
        return analysis_for(get_room(slug)).report

    @app.get("/api/rooms/{slug}/me")
    def me(who: tuple = Depends(participant)):
        room, pid = who
        return personal_view(analysis_for(room), pid)

    @app.post("/api/disputes")
    def dispute(body: Dispute, request: Request):
        limit(f"dispute:{client(request)}", 20)
        require_human(request)
        if body.person_id not in thinker_ids:
            raise HTTPException(400, "Unknown thinker.")
        if body.anchor_id and body.anchor_id not in anchor_ids:
            raise HTTPException(400, "Unknown statement.")
        store.add_dispute(body.person_id, body.anchor_id, body.body.strip(), body.contact)
        return {"ok": True}

    @app.post("/api/fairness")
    def fairness(body: Fairness, request: Request):
        limit(f"fair:{client(request)}", 20)
        store.add_fairness(bundle["version"], body.rating)
        return {"ok": True}

    @app.post("/api/event")
    def event(body: Event, request: Request):
        if body.name in EVENTS:
            limit(f"event:{client(request)}", 300)
            store.count(body.name)
        return {"ok": True}

    # ---------- identity ----------

    @app.get("/api/verify/options")
    def verify_options():
        return {"bsky": True, "x": bool(config.x_client_id)}

    @app.post("/api/verify/bsky/start")
    def bsky_start(body: BskyStart, request: Request):
        limit(f"verify:{client(request)}", 20)
        require_human(request)
        handle = identity.normalise_bsky(body.handle)
        if handle is None:
            raise HTTPException(422, "That doesn't look like a Bluesky handle.")
        limit(f"verify-handle:{handle}", 10)
        code = identity.challenge_code()
        check = store.add_check("bsky", handle, code)
        return {"check_id": check, "handle": handle, "code": code}

    @app.post("/api/verify/bsky/check")
    def bsky_check(body: CheckId, request: Request):
        limit(f"verify-check:{client(request)}", 60)
        check = store.get_check(body.check_id)
        if check is None or check["kind"] != "bsky":
            raise HTTPException(404, "That verification has expired. Start again.")
        if check["verified_at"] is None:
            try:
                found = identity.check_bsky(
                    check["handle"], check["challenge"], fetch, after=check["created_at"]
                )
            except Exception as exc:  # network trouble is the person's to retry, not a 500
                raise HTTPException(502, "Couldn't reach Bluesky. Try again in a moment.") from exc
            if found is None:
                return {"verified": False}
            store.verify_check(
                check["check_id"],
                found.handle,
                found.account_id,
                found.display_name,
                found.avatar_url,
            )
            check = store.get_check(body.check_id) or check
        return {
            "verified": True,
            "handle": check["handle"],
            "display_name": check["display_name"],
            "avatar_url": check["avatar_url"],
        }

    @app.get("/auth/x/start")
    def x_start(request: Request):
        if not config.x_client_id:
            raise HTTPException(404, "Sign in with X isn't switched on.")
        limit(f"verify:{client(request)}", 20)
        verifier, challenge = identity.pkce_pair()
        state = secrets.token_urlsafe(24)
        store.add_check("x", None, state, verifier)
        url = identity.x_authorize_url(
            config.x_client_id, f"{config.public_url}/auth/x/callback", state, challenge
        )
        return RedirectResponse(url, status_code=302)

    @app.get("/auth/x/callback")
    def x_callback(request: Request, state: str = "", code: str = "", error: str = ""):
        if state.startswith("acct-"):  # "Sign in with X" for an account, not a share check
            return app.state.x_account_callback(request, state, "" if error else code)
        check = store.check_by_state(state) if state else None
        if error or not code or check is None or not config.x_client_id:
            return RedirectResponse("/#verify=failed", status_code=302)
        try:
            found = identity.x_exchange(
                code,
                check["code_verifier"],
                config.x_client_id,
                config.x_client_secret,
                f"{config.public_url}/auth/x/callback",
            )
        except Exception:
            found = None
        if found is None:
            return RedirectResponse("/#verify=failed", status_code=302)
        store.verify_check(
            check["check_id"], found.handle, found.account_id, found.display_name, found.avatar_url
        )
        return RedirectResponse(f"/#verify={check['check_id']}", status_code=302)

    @app.get("/api/verify/{check_id}")
    def verify_status(check_id: str):
        check = store.get_check(check_id)
        if check is None or check["verified_at"] is None or check["used_at"] is not None:
            raise HTTPException(404, "No verified account here. Start again.")
        return {
            "kind": check["kind"],
            "handle": check["handle"],
            "display_name": check["display_name"],
            "avatar_url": check["avatar_url"],
        }

    # ---------- profiles ----------

    def public_profile(row: dict) -> dict:
        return {
            "code": row["code"],
            "identity": row["identity"],
            "handle": row["handle"],
            "display_name": row["display_name"],
            "avatar_url": row["avatar_url"],
            "listed": row["listed"],
            "summary": row["summary"],
            "answers": row["answers"] if row["include_answers"] else None,
            "glyph": row["glyph"],
            "bundle_version": row["bundle_version"],
            "created_at": row["created_at"].isoformat(),
        }

    def live_profile(code: str) -> dict:
        row = store.profile(code) if code.isalnum() and len(code) <= 12 else None
        if row is None or row["hidden_at"] is not None:
            raise HTTPException(404, "No profile here. It may have been deleted.")
        return row

    @app.post("/api/profiles")
    def publish(body: Publish, request: Request):
        limit(f"publish:{client(request)}", 10)
        require_human(request)
        try:
            summary = clean_summary(body.summary, bundle)
            glyph = clean_glyph(body.glyph, bundle)
            answers = clean_answers(body.answers, bundle) if body.answers is not None else None
        except SummaryError as exc:
            raise HTTPException(422, str(exc)) from exc
        row: dict = {
            "code": new_code(),
            "identity": body.identity,
            "handle": None,
            "display_name": anon_name(),
            "avatar_url": None,
            "account_id": None,
            "check_id": None,
            "listed": body.listed and body.identity != "anon",
            "include_answers": answers is not None,
            "summary": summary,
            "answers": answers,
            "glyph": glyph,
            "bundle_version": bundle["version"],
        }
        if body.identity != "anon":
            check = store.get_check(body.check_id or "")
            if (
                check is None
                or check["kind"] != body.identity
                or check["verified_at"] is None
                or check["used_at"] is not None
            ):
                raise HTTPException(403, "Verify your account first, then publish.")
            row |= {
                "handle": check["handle"],
                "display_name": check["display_name"] or check["handle"],
                "avatar_url": check["avatar_url"],
                "account_id": check["account_id"],
                "check_id": check["check_id"],
            }
        edit_key = secrets.token_urlsafe(32)
        row["edit_hash"] = key_hash(edit_key)
        try:
            store.create_profile(row)
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from exc
        store.count("publish")
        return {
            "code": row["code"],
            "edit_key": edit_key,
            "url": f"{config.public_url}/p/{row['code']}",
        }

    @app.get("/api/profiles/{code}")
    def get_profile(code: str):
        return {**public_profile(live_profile(code)), **(astore.profile_owner_extras(code) or {})}

    @app.patch("/api/profiles/{code}")
    def edit_profile(code: str, body: ProfileEdit, x_edit_key: str = Header(...)):
        row = store.profile(code)
        if row is None or (body.listed and row["identity"] == "anon"):
            raise HTTPException(
                404 if row is None else 422, "Only verified profiles can be listed."
            )
        if not store.update_profile(code, x_edit_key, body.listed):
            raise HTTPException(403, "This browser can't edit that profile.")
        return {"ok": True}

    @app.delete("/api/profiles/{code}")
    def delete_profile(code: str, x_edit_key: str = Header(...)):
        if not store.delete_profile(code, x_edit_key):
            raise HTTPException(403, "This browser can't delete that profile.")
        return {"ok": True}

    results_cache: dict[str, tuple[float, dict]] = {}
    main_room = "ai-futures"
    results_max_age = 300  # seconds

    @app.get("/api/results")
    def results(room: str = main_room):
        now = time.monotonic()
        cached = results_cache.get(room)
        if cached and now - cached[0] < results_max_age:
            return cached[1]
        row = store.room(room)
        if row is None:
            raise HTTPException(404, "No such room.")
        demo = bool(row["config"].get("demo"))

        def compute() -> dict:
            sheets = store.anchor_sheets(row["room_id"], include_synthetic=demo)
            out = public_results(sheets, bundle, [] if demo else store.visible_profiles())
            out["computed_at"] = datetime.datetime.now(datetime.UTC).isoformat()
            out["demo"] = demo
            return out

        data = store.shared(f"results:{room}:{bundle['version']}", results_max_age, compute)
        if len(results_cache) > 20:
            results_cache.clear()
        results_cache[room] = (now, data)
        return data

    @app.get("/results")
    def results_page():
        return FileResponse(public / "results.html")

    @app.get("/api/people")
    def people():
        return {"people": store.listed_profiles()}

    cards: dict[str, bytes] = {}

    @app.get("/p/{code}/card.png")
    def card(code: str, request: Request):
        row = live_profile(code)
        image = cards.get(code)
        if image is None:
            limit(f"card:{client(request)}", 120)
            image = profile_card(public_profile(row), names)
            if len(cards) > 500:
                cards.clear()
            cards[code] = image
        return Response(
            image, media_type="image/png", headers={"Cache-Control": "public, max-age=3600"}
        )

    @app.get("/p/{code}")
    def profile_page(code: str):
        row = live_profile(code)
        data = {**public_profile(row), **(astore.profile_owner_extras(code) or {})}
        who = data["display_name"] + (f" (@{data['handle']})" if data["handle"] else "")
        title = f"{who}: closest to “{data['summary']['home']}”"
        nearest = ", ".join(names[m["id"]] for m in data["summary"]["nearest"])
        description = (
            f"Nearest thinkers: {nearest}. The Great AI Debate: answer "
            f"{len(bundle['anchors'])} statements and see where you sit."
        )
        page = (public / "profile.html").read_text()
        url = f"{config.public_url}/p/{code}"
        safe_json = (
            json.dumps(data).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
        )
        fills = {
            "TITLE": html.escape(title),
            "DESCRIPTION": html.escape(description),
            "URL": html.escape(url),
            "IMAGE": html.escape(f"{url}/card.png"),
            "DATA": safe_json,
        }
        # one pass, so text from a profile can never introduce a placeholder of its own
        return HTMLResponse(re.sub(r"\{\{(\w+)\}\}", lambda m: fills[m[1]], page))

    layer_names = {"ontological": "What AI is", "epistemic": "How we know",
                   "axiological": "What matters", "empirical": "What will happen",
                   "praxis": "What to do"}  # fmt: skip
    anchors_by_id = {a["id"]: a for a in bundle["anchors"]}
    statement_cards: dict[str, bytes] = {}

    def anchor_or_404(anchor_id: str) -> dict:
        anchor = anchors_by_id.get(anchor_id)
        if anchor is None:
            raise HTTPException(404, "No such statement.")
        return anchor

    @app.get("/s/{anchor_id}/card.png")
    def statement_image(anchor_id: str):
        anchor = anchor_or_404(anchor_id)
        if anchor_id not in statement_cards:
            sides = [v["a"] for v in bundle["stances"][anchor_id].values()]
            statement_cards[anchor_id] = statement_card(
                anchor["text"], sides.count(1), sides.count(-1), layer_names[anchor["layer"]]
            )
        return Response(statement_cards[anchor_id], media_type="image/png",
                        headers={"Cache-Control": "public, max-age=86400"})  # fmt: skip

    @app.get("/s/{anchor_id}")
    def statement_page(anchor_id: str):
        anchor = anchor_or_404(anchor_id)
        page = (public / "statement.html").read_text()
        url = f"{config.public_url}/s/{anchor_id}"
        fills = {
            "TITLE": html.escape(f"Where do you stand? “{anchor['text']}”"),
            "DESCRIPTION": html.escape(
                "See which of the thinkers agree, in their own words, and how everyone answers."
            ),
            "URL": html.escape(url),
            "IMAGE": html.escape(f"{url}/card.png"),
            "ID": html.escape(anchor_id),
        }
        return HTMLResponse(re.sub(r"\{\{(\w+)\}\}", lambda m: fills[m[1]], page))

    @app.get("/people")
    def people_page():
        return FileResponse(public / "people.html")

    # ---------- admin ----------

    @app.get("/api/admin/{slug}/pending", dependencies=[Depends(admin)])
    def pending(slug: str):
        return {
            "pending": store.pending(get_room(slug)["room_id"]),
            "disputes": store.disputes(),
            "fairness": store.fairness(),
            "profiles": store.recent_profiles(),
            "counters": store.counters(),
        }

    @app.post("/api/admin/{slug}/statements/{statement_id}", dependencies=[Depends(admin)])
    def moderate(slug: str, statement_id: str, body: Moderation):
        if not store.moderate(get_room(slug)["room_id"], statement_id, body.approve, body.reason):
            raise HTTPException(404, "No pending statement with that id.")
        return {"ok": True}

    @app.post("/api/admin/profiles/{code}", dependencies=[Depends(admin)])
    def hide(code: str, body: Hide):
        if not store.hide_profile(code, body.hidden):
            raise HTTPException(404, "No such profile.")
        return {"ok": True}

    @app.exception_handler(HTTPException)
    def error(_: Request, exc: HTTPException):
        return JSONResponse(
            {"error": exc.detail},
            status_code=exc.status_code,
            headers=getattr(exc, "headers", None),
        )

    @app.get("/atlas")
    def atlas():
        return FileResponse(public / "atlas.html")

    account_routes.register(
        app,
        store=store,
        astore=astore,
        admin=admin,
        config=config,
        bundle=bundle,
        consent_version=CONSENT_VERSION,
        limit=limit,
        client=client,
        **(account_options or {}),
    )

    app.mount("/", StaticFiles(directory=public, html=True), name="public")
    app.state.started = datetime.datetime.now(datetime.UTC).isoformat()
    return app


def main() -> None:
    import uvicorn
    from arena_core.db import get_engine

    config = Config.from_env()
    port = int(os.environ.get("ARENA_APP_PORT", "8800"))
    host = os.environ.get("ARENA_APP_HOST", "127.0.0.1")
    uvicorn.run(create_app(get_engine(), config=config), host=host, port=port)


if __name__ == "__main__":
    main()
