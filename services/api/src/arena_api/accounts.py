"""Accounts: the pieces that talk to the outside world or hold secrets.

- Private keys: a long random key the person's password manager keeps; we store only its hash.
- Email: a sign-in link and a six-digit code, sent through Resend.
- Bluesky: "Sign in with Bluesky" over atproto OAuth (PAR, PKCE and DPoP, as a public client).
  We read who signed in (their DID) and then forget the token: we never post or read anything
  on their behalf. Their name and picture come from Bluesky's public profile.

Design: docs/superpowers/specs/2026-11-05-accounts-and-people-map-design.md
"""

from __future__ import annotations

import base64
import hashlib
import ipaddress
import json
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

TIMEOUT = 8
KEY_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O or 1/I to misread
BSKY_APPVIEW = "https://public.api.bsky.app/xrpc"
BSKY_ENTRYWAY = "https://bsky.social"
PLC = "https://plc.directory"
RESEND_API = "https://api.resend.com/emails"


def digest(value: str) -> bytes:
    return hashlib.sha256(value.encode()).digest()


# ---------------------------------------------------------------- private keys


def new_key() -> str:
    """am-XXXX-XXXX-XXXX-XXXX-XXXX: 100 random bits, easy to read aloud or type."""
    groups = ["".join(secrets.choice(KEY_ALPHABET) for _ in range(4)) for _ in range(5)]
    return "am-" + "-".join(groups)


def key_subject(key: str) -> str | None:
    """The stored form of a key: tolerant of case, spaces and dashes; None if it can't be one."""
    body = key.strip().upper().removeprefix("AM").replace("-", "").replace(" ", "")
    if len(body) != 20 or any(ch not in KEY_ALPHABET for ch in body):
        return None
    return hashlib.sha256(f"antimemes-key:{body}".encode()).hexdigest()


# ---------------------------------------------------------------- email


def new_email_code() -> str:
    return f"{secrets.randbelow(10**6):06d}"


def normalise_email(email: str) -> str | None:
    email = email.strip().lower()
    local, _, domain = email.partition("@")
    if not local or "." not in domain or len(email) > 254 or any(c.isspace() for c in email):
        return None
    return email


Sender = Callable[[str, str, str, str], None]  # (to, subject, html, text)


def resend_sender(api_key: str, sender: str) -> Sender:
    def send(to: str, subject: str, html: str, text: str) -> None:
        body = json.dumps(
            {"from": sender, "to": [to], "subject": subject, "html": html, "text": text}
        ).encode()
        request = urllib.request.Request(
            RESEND_API,
            data=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "antimemes-debate/1",
            },
        )
        with urllib.request.urlopen(request, timeout=TIMEOUT):  # noqa: S310 (fixed host)
            pass

    return send


def sign_in_email(link: str, code: str) -> tuple[str, str, str]:
    """Subject, HTML and text of the sign-in email."""
    subject = f"Your antimemes sign-in code: {code}"
    text = (
        "Sign in to The Great AI Debate on antimemes.is.\n\n"
        f"Open this link on the device you're using:\n{link}\n\n"
        f"Or type this code: {code}\n\n"
        "Both work once and expire in 15 minutes. If you didn't ask for this, ignore it."
    )
    html = f"""<div style="font-family:system-ui,sans-serif;background:#121820;color:#dde4eb;
padding:28px">
<p style="font-size:20px;font-weight:600;margin:0 0 16px">antimemes</p>
<p>Sign in to The Great AI Debate.</p>
<p><a href="{link}" style="display:inline-block;background:#dde4eb;color:#121820;padding:12px 18px;
text-decoration:none;font-weight:600">Sign in</a></p>
<p>Or type this code: <b style="font-size:22px;letter-spacing:3px">{code}</b></p>
<p style="color:#9aa7b6;font-size:13px">Both work once and expire in 15 minutes.
If you didn't ask for this, ignore it.</p></div>"""
    return subject, html, text


# ---------------------------------------------------------------- HTTP


@dataclass
class Reply:
    status: int
    headers: dict[str, str]
    body: dict


Http = Callable[[str, str, dict | None, dict[str, str]], Reply]


def http(method: str, url: str, form: dict | None, headers: dict[str, str]) -> Reply:
    data = urllib.parse.urlencode(form).encode() if form is not None else None
    hdrs = {"User-Agent": "antimemes-debate/1", "Accept": "application/json", **headers}
    if data is not None:
        hdrs["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:  # noqa: S310
            raw = response.read()
            return Reply(response.status, {k.lower(): v for k, v in response.headers.items()},
                         json.loads(raw) if raw else {})  # fmt: skip
    except urllib.error.HTTPError as err:
        raw = err.read()
        try:
            body = json.loads(raw) if raw else {}
        except ValueError:
            body = {}
        return Reply(err.code, {k.lower(): v for k, v in err.headers.items()}, body)


def safe_https(url: str) -> bool:
    """Only public https hosts: these URLs come from documents other people control."""
    parts = urllib.parse.urlsplit(url)
    host = parts.hostname or ""
    if parts.scheme != "https" or not host or host == "localhost" or host.endswith(".local"):
        return False
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return True
    return ip.is_global


# ---------------------------------------------------------------- DPoP


def b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def new_dpop_key() -> str:
    key = ec.generate_private_key(ec.SECP256R1())
    return key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()


def _public_jwk(key: ec.EllipticCurvePrivateKey) -> dict:
    numbers = key.public_key().public_numbers()
    return {"kty": "EC", "crv": "P-256", "x": b64(numbers.x.to_bytes(32, "big")),
            "y": b64(numbers.y.to_bytes(32, "big"))}  # fmt: skip


def dpop_proof(pem: str, method: str, url: str, nonce: str | None) -> str:
    key = serialization.load_pem_private_key(pem.encode(), password=None)
    assert isinstance(key, ec.EllipticCurvePrivateKey)
    header = {"typ": "dpop+jwt", "alg": "ES256", "jwk": _public_jwk(key)}
    claims = {"jti": secrets.token_urlsafe(16), "htm": method, "htu": url, "iat": int(time.time())}
    if nonce:
        claims["nonce"] = nonce
    signing_input = f"{b64(json.dumps(header).encode())}.{b64(json.dumps(claims).encode())}"
    r, s = decode_dss_signature(key.sign(signing_input.encode(), ec.ECDSA(hashes.SHA256())))
    return f"{signing_input}.{b64(r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))}"


def dpop_post(
    http_: Http, pem: str, url: str, form: dict, nonce: str | None
) -> tuple[Reply, str | None]:
    """POST with a DPoP proof, retrying once with the server's nonce when it asks for one."""
    reply = http_("POST", url, form, {"DPoP": dpop_proof(pem, "POST", url, nonce)})
    fresh = reply.headers.get("dpop-nonce") or nonce
    if reply.status in (400, 401) and reply.body.get("error") == "use_dpop_nonce" and fresh:
        reply = http_("POST", url, form, {"DPoP": dpop_proof(pem, "POST", url, fresh)})
        fresh = reply.headers.get("dpop-nonce") or fresh
    return reply, fresh


# ---------------------------------------------------------------- Bluesky (atproto OAuth)


class BskyError(Exception):
    pass


def client_metadata(public_url: str) -> dict:
    return {
        "client_id": f"{public_url}/oauth/client-metadata.json",
        "client_name": "The Great AI Debate (antimemes.is)",
        "client_uri": public_url,
        "logo_uri": f"{public_url}/apple-touch-icon.png",
        "policy_uri": f"{public_url}/privacy.html",
        "redirect_uris": [f"{public_url}/auth/bsky/callback"],
        "scope": "atproto",
        "grant_types": ["authorization_code"],
        "response_types": ["code"],
        "application_type": "web",
        "token_endpoint_auth_method": "none",
        "dpop_bound_access_tokens": True,
    }


def client_ids(public_url: str) -> tuple[str, str]:
    """(client_id, redirect_uri). Local development uses atproto's loopback client."""
    if public_url.startswith(("http://localhost", "http://127.0.0.1")):
        port = urllib.parse.urlsplit(public_url).port or 80
        redirect = f"http://127.0.0.1:{port}/auth/bsky/callback"
        query = urllib.parse.urlencode({"redirect_uri": redirect, "scope": "atproto"})
        return f"http://localhost?{query}", redirect
    return f"{public_url}/oauth/client-metadata.json", f"{public_url}/auth/bsky/callback"


def resolve_handle(http_: Http, handle: str) -> str:
    if handle.startswith("did:"):
        return handle
    q = urllib.parse.quote(handle)
    reply = http_("GET", f"{BSKY_APPVIEW}/com.atproto.identity.resolveHandle?handle={q}", None, {})
    did = reply.body.get("did")
    if reply.status != 200 or not isinstance(did, str) or not did.startswith("did:"):
        raise BskyError("We couldn't find that Bluesky handle.")
    return did


def pds_of(http_: Http, did: str) -> str:
    if did.startswith("did:plc:"):
        url = f"{PLC}/{urllib.parse.quote(did)}"
    elif did.startswith("did:web:"):
        url = f"https://{did.removeprefix('did:web:')}/.well-known/did.json"
    else:
        raise BskyError("Unsupported account type.")
    if not safe_https(url):
        raise BskyError("Unsupported account host.")
    doc = http_("GET", url, None, {}).body
    for service in doc.get("service", []) or []:
        if str(service.get("id", "")).endswith("#atproto_pds"):
            endpoint = str(service.get("serviceEndpoint", "")).rstrip("/")
            if safe_https(endpoint):
                return endpoint
    raise BskyError("That account has no server we can reach.")


def auth_server(http_: Http, pds: str) -> dict:
    resource = http_("GET", f"{pds}/.well-known/oauth-protected-resource", None, {}).body
    servers = resource.get("authorization_servers") or []
    if not servers or not safe_https(servers[0]):
        raise BskyError("That account's server doesn't offer sign-in.")
    issuer = servers[0].rstrip("/")
    meta = http_("GET", f"{issuer}/.well-known/oauth-authorization-server", None, {}).body
    if meta.get("issuer", "").rstrip("/") != issuer:
        raise BskyError("That account's sign-in server didn't check out.")
    for field in ("pushed_authorization_request_endpoint", "authorization_endpoint",
                  "token_endpoint"):  # fmt: skip
        if not safe_https(meta.get(field, "")):
            raise BskyError("That account's sign-in server didn't check out.")
    return meta


def bsky_start(http_: Http, public_url: str, handle: str | None, state: str) -> tuple[str, dict]:
    """The URL to send the person to, and what to remember until they come back."""
    did = resolve_handle(http_, handle) if handle else None
    pds = pds_of(http_, did) if did else BSKY_ENTRYWAY
    meta = auth_server(http_, pds)
    client_id, redirect = client_ids(public_url)
    verifier = secrets.token_urlsafe(48)
    challenge = b64(hashlib.sha256(verifier.encode()).digest())
    pem = new_dpop_key()
    form = {
        "client_id": client_id,
        "response_type": "code",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
        "redirect_uri": redirect,
        "scope": "atproto",
    }
    if handle and not handle.startswith("did:"):
        form["login_hint"] = handle
    reply, nonce = dpop_post(http_, pem, meta["pushed_authorization_request_endpoint"], form, None)
    request_uri = reply.body.get("request_uri")
    if reply.status not in (200, 201) or not request_uri:
        raise BskyError("Bluesky didn't accept the sign-in request. Try again.")
    query = urllib.parse.urlencode({"client_id": client_id, "request_uri": request_uri})
    flow = {"verifier": verifier, "pem": pem, "nonce": nonce, "issuer": meta["issuer"].rstrip("/"),
            "token_endpoint": meta["token_endpoint"], "did": did}  # fmt: skip
    return f"{meta['authorization_endpoint']}?{query}", flow


@dataclass(frozen=True)
class BskyAccount:
    did: str
    handle: str
    display_name: str
    avatar_url: str | None
    details: dict | None = None


def bsky_details(profile: dict, handle: str) -> dict:
    banner = profile.get("banner")
    return {
        "description": str(profile.get("description") or "")[:300],
        "followers": int(profile.get("followersCount") or 0),
        "banner": banner
        if isinstance(banner, str) and banner.startswith("https://cdn.bsky.app/")
        else None,
        "url": f"https://bsky.app/profile/{handle}",
    }


def bsky_finish(http_: Http, public_url: str, flow: dict, code: str, iss: str) -> BskyAccount:
    if iss.rstrip("/") != flow["issuer"]:
        raise BskyError("The sign-in came back from the wrong server.")
    client_id, redirect = client_ids(public_url)
    form = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect,
        "code_verifier": flow["verifier"],
        "client_id": client_id,
    }
    reply, _ = dpop_post(http_, flow["pem"], flow["token_endpoint"], form, flow.get("nonce"))
    sub = reply.body.get("sub")
    if reply.status != 200 or not isinstance(sub, str) or not sub.startswith("did:"):
        raise BskyError("Bluesky didn't confirm the sign-in.")
    if flow.get("did"):
        if sub != flow["did"]:
            raise BskyError("You signed in as a different account.")
    elif auth_server(http_, pds_of(http_, sub))["issuer"].rstrip("/") != flow["issuer"]:
        # signed in at the entryway: make sure that server really speaks for this account
        raise BskyError("That account's sign-in server didn't check out.")
    q = urllib.parse.quote(sub)
    profile = http_("GET", f"{BSKY_APPVIEW}/app.bsky.actor.getProfile?actor={q}", None, {}).body
    avatar = profile.get("avatar")
    handle = str(profile.get("handle") or sub)
    return BskyAccount(
        did=sub,
        handle=handle,
        display_name=str(profile.get("displayName") or handle)[:80],
        avatar_url=avatar
        if isinstance(avatar, str) and avatar.startswith("https://cdn.bsky.app/")
        else None,
        details=bsky_details(profile, handle),
    )
