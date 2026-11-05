"""Account endpoints (docs/superpowers/specs/2026-11-05-accounts-and-people-map-design.md).

One account, four ways in (Bluesky, X, email, private key). Signing in while signed in adds that
way in to the same account. Saved answers also count in the public results: each account sheet is
a participant in the main room, and its votes follow the answers.
"""

from __future__ import annotations

import secrets
import time
import urllib.parse
from collections.abc import Callable

from arena_fingerprint.agreement import position, ranked
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field

from arena_api import accounts, identity
from arena_api.account_store import AccountStore
from arena_api.profiles import SummaryError, clean_answers

COOKIE = "am_session"
MAIN_ROOM = "ai-futures"


class KeyLogin(BaseModel):
    key: str = Field(max_length=80)


class EmailStart(BaseModel):
    email: str = Field(max_length=254)


class EmailCode(BaseModel):
    email: str = Field(max_length=254)
    code: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class AccountEdit(BaseModel):
    display_name: str | None = Field(default=None, max_length=80)
    bio: str | None = Field(default=None, max_length=160)
    show_on_map: bool | None = None


class RoomEntry(BaseModel):
    participant_id: str = Field(max_length=40)
    key: str = Field(min_length=32, max_length=128)


class Answers(BaseModel):
    answers: dict[str, int]
    room: RoomEntry | None = None  # this browser's earlier anonymous entry, taken over once


def register(
    app: FastAPI,
    *,
    store,
    astore: AccountStore,
    config,
    bundle: dict,
    consent_version: str,
    limit: Callable[[str, int], None],
    client: Callable[[Request], str],
    http: accounts.Http = accounts.http,
    sender: accounts.Sender | None = None,
) -> None:
    season = bundle.get("season") or bundle["version"]
    stances = {a: {t: v["a"] for t, v in e.items()} for a, e in bundle["stances"].items()}
    coords = {t["id"]: (float(t["x"]), float(t["y"])) for t in bundle["thinkers"]}
    names = {t["id"]: t["name"] for t in bundle["thinkers"]}
    secure = config.public_url.startswith("https://")
    if sender is None and getattr(config, "resend_key", None):
        sender = accounts.resend_sender(config.resend_key, config.mail_from)

    # ---------- helpers

    def same_origin(request: Request) -> None:
        """Cookie-authenticated writes must come from our own pages (with SameSite=Lax)."""
        origin = request.headers.get("origin")
        if origin and origin.rstrip("/") not in (config.public_url, "http://127.0.0.1:8800",
                                                 "http://localhost:8800"):  # fmt: skip
            raise HTTPException(403, "Requests must come from the site itself.")

    def current(request: Request) -> str | None:
        return astore.session_account(request.cookies.get(COOKIE))

    def need(request: Request) -> str:
        account = current(request)
        if account is None:
            raise HTTPException(401, "Sign in first.")
        return account

    def set_cookie(response: Response, account_id: str) -> None:
        token = astore.new_session(account_id)
        response.set_cookie(COOKIE, token, max_age=365 * 86400, httponly=True, secure=secure,
                            samesite="lax", path="/")  # fmt: skip

    def signed_in[R: Response](account_id: str, request: Request, response: R) -> R:
        """Start a session unless this browser is already in that account."""
        out = response
        if current(request) != account_id:
            set_cookie(out, account_id)
        return out

    def back(
        request: Request, account_id: str | None, failed: str = "", to: str = ""
    ) -> RedirectResponse:
        if account_id is None:
            return RedirectResponse(f"/account.html#signin=failed{failed}", status_code=302)
        page = "/account.html" if to == "account" else "/"
        return signed_in(account_id, request, RedirectResponse(f"{page}#signed-in", 302))

    # ---------- the account

    @app.get("/api/me")
    def me(request: Request):
        account_id = current(request)
        row = astore.account(account_id) if account_id else None
        if row is None or account_id is None:
            return {"account": None}
        sheet = astore.sheet(account_id, season)
        return {
            "account": {
                "display_name": row["display_name"],
                "avatar_url": row["avatar_url"],
                "bio": row["bio"] or "",
                "show_on_map": row["show_on_map"],
                "logins": row["logins"],
                "sheet": None
                if sheet is None
                else {k: sheet[k] for k in ("season", "answers", "updated_at")},
            }
        }

    @app.patch("/api/me")
    def edit(body: AccountEdit, request: Request):
        same_origin(request)
        account_id = need(request)
        fields = body.model_dump(exclude_none=True)
        for key in ("display_name", "bio"):
            if key in fields:
                fields[key] = " ".join(fields[key].split()) or None
        astore.update_account(account_id, fields)
        return {"ok": True}

    @app.put("/api/me/answers")
    def save_answers(body: Answers, request: Request):
        same_origin(request)
        account_id = need(request)
        limit(f"answers:{account_id}", 600)
        try:
            answers = clean_answers(body.answers, bundle)
        except SummaryError as exc:
            raise HTTPException(422, str(exc)) from exc
        where = position(answers, stances, coords)
        top = ranked(answers, stances)
        nearest = top[0][0] if top else None
        sheet = astore.sheet(account_id, season)
        participant: str | None = sheet["participant_id"] if sheet else None
        room = store.room(MAIN_ROOM)
        if room is not None and room["status"] == "open":
            earlier = body.room
            if (
                participant is None
                and earlier is not None
                and store.authenticate(room["room_id"], earlier.participant_id, earlier.key)
                and earlier.participant_id not in astore.linked_participants(season)
            ):
                participant = earlier.participant_id  # counted once, not twice
            if participant is None:
                participant = store.join(room["room_id"], secrets.token_urlsafe(32), None,
                                         consent_version)  # fmt: skip
            ids = store.anchor_statements(room["room_id"])
            store.votes_bulk([(participant, ids[a], v) for a, v in answers.items() if a in ids])
        astore.save_sheet(account_id, season, answers, where, nearest, participant)
        return {"ok": True, "position": where and {"x": where[0], "y": where[1]}}

    @app.delete("/api/me")
    def delete(request: Request):
        same_origin(request)
        account_id = need(request)
        astore.delete_account(account_id)
        out = JSONResponse({"ok": True})
        out.delete_cookie(COOKIE, path="/")
        return out

    @app.post("/api/auth/logout")
    def logout(request: Request):
        same_origin(request)
        astore.end_session(request.cookies.get(COOKIE))
        out = JSONResponse({"ok": True})
        out.delete_cookie(COOKIE, path="/")
        return out

    # ---------- private key

    @app.post("/api/auth/key/new")
    def key_new(request: Request):
        same_origin(request)
        limit(f"key-new:{client(request)}", 20)
        key = accounts.new_key()
        subject = accounts.key_subject(key)
        assert subject
        account_id = astore.sign_in("key", subject, current(request))
        return signed_in(account_id, request, JSONResponse({"key": key}))

    @app.post("/api/auth/key")
    def key_login(body: KeyLogin, request: Request):
        same_origin(request)
        limit(f"key:{client(request)}", 30)
        subject = accounts.key_subject(body.key)
        if subject is None:
            raise HTTPException(422, "That isn't an antimemes key. It starts with am-.")
        account_id = astore.login_account("key", subject)
        if account_id is None:
            raise HTTPException(404, "No account has that key.")
        return signed_in(account_id, request, JSONResponse({"ok": True}))

    # ---------- email

    @app.post("/api/auth/email/start")
    def email_start(body: EmailStart, request: Request):
        same_origin(request)
        email = accounts.normalise_email(body.email)
        if email is None:
            raise HTTPException(422, "That doesn't look like an email address.")
        limit(f"email:{client(request)}", 10)
        limit(f"email-to:{email}", 5)
        if sender is None:
            raise HTTPException(503, "Email sign-in isn't switched on yet.")
        token, code = secrets.token_urlsafe(32), accounts.new_email_code()
        astore.new_email_token(email, token, code)
        link = f"{config.public_url}/auth/email?t={urllib.parse.quote(token)}"
        subject, html, text = accounts.sign_in_email(link, code)
        try:
            sender(email, subject, html, text)
        except Exception as exc:
            raise HTTPException(502, "We couldn't send the email. Try again in a moment.") from exc
        return {"ok": True}

    @app.post("/api/auth/email/code")
    def email_code(body: EmailCode, request: Request):
        same_origin(request)
        email = accounts.normalise_email(body.email)
        limit(f"email-code:{client(request)}", 30)
        if email is None or not astore.use_email_code(email, body.code):
            raise HTTPException(403, "That code didn't match, or it has expired.")
        account_id = astore.sign_in("email", email, current(request), handle=email)
        return signed_in(account_id, request, JSONResponse({"ok": True}))

    @app.get("/auth/email")
    def email_link(request: Request, t: str = ""):
        email = astore.use_email_link(t) if t and len(t) < 100 else None
        if email is None:
            return back(request, None, "&why=expired")
        return back(request, astore.sign_in("email", email, current(request), handle=email))

    # ---------- Bluesky

    @app.get("/oauth/client-metadata.json")
    def bsky_metadata():
        return accounts.client_metadata(config.public_url)

    @app.get("/auth/bsky/start")
    def bsky_start(request: Request, handle: str = "", next: str = ""):
        limit(f"bsky:{client(request)}", 30)
        clean = identity.normalise_bsky(handle) if handle.strip() else None
        if handle.strip() and clean is None and not handle.strip().startswith("did:"):
            return back(request, None, "&why=handle")
        state = secrets.token_urlsafe(24)
        try:
            who = clean or handle.strip() or None
            url, flow = accounts.bsky_start(http, config.public_url, who, state)
        except (accounts.BskyError, OSError, ValueError, KeyError):
            return back(request, None, "&why=bsky")
        astore.put_flow(state, "bsky", {**flow, "next": next if next == "account" else ""})
        return RedirectResponse(url, status_code=302)

    @app.get("/auth/bsky/callback")
    def bsky_callback(request: Request, state: str = "", code: str = "", iss: str = "",
                      error: str = ""):  # fmt: skip
        flow = astore.take_flow(state, "bsky") if state else None
        if error or not code or flow is None:
            return back(request, None, "&why=bsky")
        try:
            who = accounts.bsky_finish(http, config.public_url, flow, code, iss)
        except (accounts.BskyError, OSError, ValueError, KeyError):
            return back(request, None, "&why=bsky")
        account_id = astore.sign_in("bsky", who.did, current(request), handle=who.handle,
                                    name=who.display_name, avatar=who.avatar_url)  # fmt: skip
        return back(request, account_id, to=flow.get("next", ""))

    # ---------- X (accounts share the one registered callback with the share-verify flow)

    @app.get("/auth/x/signin")
    def x_signin(request: Request, next: str = ""):
        if not config.x_client_id:
            return back(request, None, "&why=x-off")
        limit(f"x:{client(request)}", 20)
        verifier, challenge = identity.pkce_pair()
        state = "acct-" + secrets.token_urlsafe(24)
        astore.put_flow(
            state, "x", {"verifier": verifier, "next": next if next == "account" else ""}
        )
        url = identity.x_authorize_url(config.x_client_id, f"{config.public_url}/auth/x/callback",
                                       state, challenge)  # fmt: skip
        return RedirectResponse(url, status_code=302)

    def x_account_callback(request: Request, state: str, code: str) -> RedirectResponse:
        flow = astore.take_flow(state, "x")
        if flow is None or not code:
            return back(request, None, "&why=x")
        try:
            who = identity.x_exchange(code, flow["verifier"], config.x_client_id,
                                      config.x_client_secret,
                                      f"{config.public_url}/auth/x/callback")  # fmt: skip
        except Exception:
            who = None
        if who is None:
            return back(request, None, "&why=x")
        avatar = who.avatar_url and who.avatar_url.replace("_normal.", "_200x200.")
        account_id = astore.sign_in("x", who.account_id, current(request), handle=who.handle,
                                    name=who.display_name, avatar=avatar)  # fmt: skip
        return back(request, account_id, to=flow.get("next", ""))

    app.state.x_account_callback = x_account_callback

    # ---------- the people map

    people_cache: dict[str, tuple[float, dict]] = {}
    app.state.people_cache = people_cache

    @app.get("/api/map/people")
    def map_people():
        cached = people_cache.get(season)
        if cached and time.monotonic() - cached[0] < 60:
            return cached[1]
        people = astore.map_people(season)
        # people who added answers without an account are dots too, placed the same way
        room = store.room(MAIN_ROOM)
        linked = astore.linked_participants(season)
        if room is not None:
            for pid, sheet in store.anchor_sheets(room["room_id"]).items():
                if pid in linked:
                    continue
                where = position(sheet, stances, coords)
                if where:
                    people.append({"x": round(where[0], 2), "y": round(where[1], 2)})
        min_cell = 10
        for p in people:
            if p.get("nearest"):
                p["nearest"] = names.get(p["nearest"], p["nearest"])
        data = {"min_cell": min_cell, "count": len(people),
                "people": people if len(people) >= min_cell else []}  # fmt: skip
        people_cache[season] = (time.monotonic(), data)
        return data
