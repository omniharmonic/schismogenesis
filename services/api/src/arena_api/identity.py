"""Verifying who publishes a profile (04-LAUNCH.md section 1.2). Unverified handles are never shown.

Bluesky: the person posts a one-time code from their account; we read their recent posts through
Bluesky's free public API (no key needed) and take their display name and picture from it.

X: "Sign in with X" (OAuth 2.0 with PKCE). It needs an X developer app; without ARENA_X_CLIENT_ID
the option is off.
"""

import base64
import hashlib
import json
import re
import secrets
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

BSKY_API = "https://public.api.bsky.app/xrpc"
X_AUTHORIZE = "https://x.com/i/oauth2/authorize"
X_TOKEN = "https://api.x.com/2/oauth2/token"
X_ME = "https://api.x.com/2/users/me?user.fields=profile_image_url,name,username"
HANDLE = re.compile(r"^[a-z0-9][a-z0-9.-]{1,252}\.[a-z]{2,}$")
TIMEOUT = 8

Fetch = Callable[[str], dict]


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "dialogos-fingerprint/1"})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:  # noqa: S310 (fixed hosts)
        return json.loads(response.read())


def normalise_bsky(handle: str) -> str | None:
    handle = handle.strip().lstrip("@").lower()
    if "." not in handle:
        handle += ".bsky.social"
    return handle if HANDLE.match(handle) else None


def challenge_code() -> str:
    return f"dialogos-{secrets.token_hex(3)}"


@dataclass(frozen=True)
class Verified:
    handle: str
    account_id: str
    display_name: str
    avatar_url: str | None


def check_bsky(handle: str, code: str, fetch: Fetch = fetch_json) -> Verified | None:
    """True when one of the account's 25 latest posts contains the code."""
    q = urllib.parse.quote
    profile = fetch(f"{BSKY_API}/app.bsky.actor.getProfile?actor={q(handle)}")
    did = profile.get("did")
    if not did:
        return None
    feed = fetch(
        f"{BSKY_API}/app.bsky.feed.getAuthorFeed?actor={q(did)}&limit=25&filter=posts_no_replies"
    )
    for item in feed.get("feed", []):
        post = item.get("post", {})
        if post.get("author", {}).get("did") != did:
            continue  # reposts of someone else's post don't count
        if code in post.get("record", {}).get("text", ""):
            avatar = profile.get("avatar")
            return Verified(
                handle=profile.get("handle", handle),
                account_id=did,
                display_name=(profile.get("displayName") or profile.get("handle") or handle)[:80],
                avatar_url=avatar
                if isinstance(avatar, str) and avatar.startswith("https://cdn.bsky.app/")
                else None,
            )
    return None


def pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=")
    return verifier, challenge.decode()


def x_authorize_url(client_id: str, redirect_uri: str, state: str, challenge: str) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "users.read tweet.read",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return f"{X_AUTHORIZE}?{urllib.parse.urlencode(params)}"


def x_exchange(
    code: str, verifier: str, client_id: str, client_secret: str | None, redirect_uri: str
) -> Verified | None:
    """Swap the authorisation code for a token, read the signed-in account, and forget the token."""
    body = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": verifier,
            "client_id": client_id,
        }
    ).encode()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if client_secret:
        basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers["Authorization"] = f"Basic {basic}"
    request = urllib.request.Request(X_TOKEN, data=body, headers=headers)
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:  # noqa: S310
        token = json.loads(response.read()).get("access_token")
    if not token:
        return None
    me_request = urllib.request.Request(X_ME, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(me_request, timeout=TIMEOUT) as response:  # noqa: S310
        data = json.loads(response.read()).get("data") or {}
    if not data.get("id"):
        return None
    avatar = data.get("profile_image_url")
    return Verified(
        handle=data["username"],
        account_id=data["id"],
        display_name=(data.get("name") or data["username"])[:80],
        avatar_url=avatar
        if isinstance(avatar, str) and avatar.startswith("https://pbs.twimg.com/")
        else None,
    )
