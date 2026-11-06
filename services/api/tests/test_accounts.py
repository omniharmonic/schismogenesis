"""Accounts: the four ways in, linking, saved answers, the people map and deletion."""

import base64
import json
import pathlib
import urllib.parse

import pytest
from arena_api import accounts
from arena_api.app import Config, create_app
from arena_api.store import Store
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from fastapi.testclient import TestClient
from sqlalchemy import text

PUBLIC = pathlib.Path(__file__).parents[3] / "apps/arena/public"
BUNDLE = json.loads((PUBLIC / "fingerprint.json").read_text())
A = [a["id"] for a in BUNDLE["anchors"]]
SITE = "http://testserver"


def answers(seed: int = 0) -> dict[str, int]:
    return {a: [1, -1, 1, 0, -1][(i + seed) % 5] for i, a in enumerate(A)}


def unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def check_dpop(proof: str, method: str, url: str) -> dict:
    """Verify a DPoP proof the way an authorisation server does."""
    head, body, sig = proof.split(".")
    header, claims = json.loads(unb64(head)), json.loads(unb64(body))
    assert header["typ"] == "dpop+jwt" and header["alg"] == "ES256"
    jwk = header["jwk"]
    public = ec.EllipticCurvePublicNumbers(
        int.from_bytes(unb64(jwk["x"]), "big"), int.from_bytes(unb64(jwk["y"]), "big"),
        ec.SECP256R1(),
    ).public_key()  # fmt: skip
    raw = unb64(sig)
    der = encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"))
    public.verify(der, f"{head}.{body}".encode(), ec.ECDSA(hashes.SHA256()))
    assert claims["htm"] == method and claims["htu"] == url
    return claims


class FakeAtproto:
    """Bluesky's appview, PLC directory, PDS and authorisation server, enough for the flow."""

    ISSUER = "https://auth.example.com"
    PDS = "https://pds.example.com"

    def __init__(self, did: str = "did:plc:alice"):
        self.did = did
        self.nonce_asked = False
        self.issued_code = "the-code"

    def __call__(self, method, url, form, headers):
        R = accounts.Reply
        if "resolveHandle" in url:
            return R(200, {}, {"did": self.did})
        if url.startswith("https://plc.directory/"):
            return R(200, {}, {"service": [{"id": "#atproto_pds", "serviceEndpoint": self.PDS}]})
        if url == f"{self.PDS}/.well-known/oauth-protected-resource":
            return R(200, {}, {"authorization_servers": [self.ISSUER]})
        if url == f"{self.ISSUER}/.well-known/oauth-authorization-server":
            return R(200, {}, {"issuer": self.ISSUER,
                               "pushed_authorization_request_endpoint": f"{self.ISSUER}/par",
                               "authorization_endpoint": f"{self.ISSUER}/authorize",
                               "token_endpoint": f"{self.ISSUER}/token"})  # fmt: skip
        if url == f"{self.ISSUER}/par":
            claims = check_dpop(headers["DPoP"], "POST", url)
            if "nonce" not in claims:  # servers ask for a nonce first
                self.nonce_asked = True
                return R(400, {"dpop-nonce": "n1"}, {"error": "use_dpop_nonce"})
            assert form["scope"] == "atproto" and form["code_challenge_method"] == "S256"
            self.state = form["state"]
            return R(201, {"dpop-nonce": "n2"}, {"request_uri": "urn:req:1", "expires_in": 60})
        if url == f"{self.ISSUER}/token":
            claims = check_dpop(headers["DPoP"], "POST", url)
            assert claims.get("nonce") == "n2"
            assert form["code"] == self.issued_code and form["code_verifier"]
            return R(200, {}, {"access_token": "t", "token_type": "DPoP", "sub": self.did})
        if "getProfile" in url:
            return R(200, {}, {"did": self.did, "handle": "alice.example.com",
                               "displayName": "Alice", "followersCount": 42,
                               "description": getattr(self, "description", ""),
                               "avatar": "https://cdn.bsky.app/img/avatar/a.jpg"})  # fmt: skip
        raise AssertionError(f"unexpected {method} {url}")


@pytest.fixture
def world(engine):
    sent = []
    atproto = FakeAtproto()
    Store(engine).ensure_room("ai-futures", "AI futures", BUNDLE)
    app = create_app(
        engine,
        config=Config(admin_token="t" * 24, public_url=SITE),
        account_options={"http": atproto, "sender": lambda *m: sent.append(m)},
    )
    return app, sent, atproto


def browser(app) -> TestClient:
    return TestClient(app, base_url=SITE)


def test_key_account_saves_answers_and_signs_in_elsewhere(world, engine):
    app, _, _ = world
    phone = browser(app)
    assert phone.get("/api/me").json() == {"account": None}
    key = phone.post("/api/auth/key/new").json()["key"]
    assert key.startswith("am-") and len(key) == 27
    saved = phone.put("/api/me/answers", json={"answers": answers()}).json()
    assert saved["ok"] and saved["position"]["x"] is not None
    laptop = browser(app)
    assert (
        laptop.post("/api/auth/key", json={"key": key.lower().replace("-", " ")}).status_code == 200
    )
    me = laptop.get("/api/me").json()["account"]
    assert me["sheet"]["answers"] == answers()
    assert me["logins"] == [{"kind": "key", "handle": None}]
    # the saved sheet counts in the public results, once, and follows changes
    with engine.connect() as c:
        votes = c.execute(text("SELECT count(*) FROM room_vote")).scalar()
    laptop.put("/api/me/answers", json={"answers": answers(1)})
    with engine.connect() as c:
        assert c.execute(text("SELECT count(*) FROM room_vote")).scalar() == votes
        assert c.execute(text("SELECT count(*) FROM room_participant")).scalar() == 1
    assert browser(app).post("/api/auth/key", json={"key": "am-" + "A" * 20}).status_code == 404
    assert browser(app).post("/api/auth/key", json={"key": "hello"}).status_code == 422


def test_answers_are_checked_and_need_a_session(world):
    app, _, _ = world
    assert browser(app).put("/api/me/answers", json={"answers": answers()}).status_code == 401
    b = browser(app)
    b.post("/api/auth/key/new")
    assert b.put("/api/me/answers", json={"answers": {"nope": 1}}).status_code == 422
    assert b.put("/api/me/answers", json={"answers": {A[0]: 5}}).status_code == 422


def test_email_code_and_link(world):
    app, sent, _ = world
    b = browser(app)
    assert b.post("/api/auth/email/start", json={"email": " Ann@Example.com "}).json()["ok"]
    to, subject, html, body = sent[-1]
    code = subject.rsplit(" ", 1)[-1]
    assert to == "ann@example.com" and code in body and "/auth/email?t=" in html
    for _ in range(2):
        assert b.post("/api/auth/email/code",
                      json={"email": "ann@example.com", "code": "000000" if code != "000000"
                            else "111111"}).status_code == 403  # fmt: skip
    assert b.post("/api/auth/email/code",
                  json={"email": "ann@example.com", "code": code}).status_code == 200  # fmt: skip
    first = b.get("/api/me").json()["account"]
    assert first["logins"] == [{"kind": "email", "handle": "ann@example.com"}]
    # the code works once; a fresh link signs a new browser into the same account
    other = browser(app)
    other.post("/api/auth/email/start", json={"email": "ann@example.com"})
    link = sent[-1][3].split("\n")[3]
    token = urllib.parse.parse_qs(urllib.parse.urlsplit(link).query)["t"][0]
    r = other.get(f"/auth/email?t={token}", follow_redirects=False)
    assert r.status_code == 302 and r.headers["location"] == "/#signed-in"
    assert other.get("/api/me").json()["account"]["logins"] == first["logins"]
    again = browser(app).get(f"/auth/email?t={token}", follow_redirects=False)
    assert "signin=failed" in again.headers["location"]


def test_wrong_codes_run_out(world):
    app, sent, _ = world
    b = browser(app)
    b.post("/api/auth/email/start", json={"email": "bo@example.com"})
    code = sent[-1][1].rsplit(" ", 1)[-1]
    wrong = "000000" if code != "000000" else "111111"
    for _ in range(5):
        b.post("/api/auth/email/code", json={"email": "bo@example.com", "code": wrong})
    assert b.post("/api/auth/email/code",
                  json={"email": "bo@example.com", "code": code}).status_code == 403  # fmt: skip


def bsky_sign_in(b: TestClient, atproto: FakeAtproto, handle: str = "alice.example.com"):
    r = b.get(f"/auth/bsky/start?handle={handle}", follow_redirects=False)
    assert r.status_code == 302, r.headers.get("location")
    where = urllib.parse.urlsplit(r.headers["location"])
    assert f"{where.scheme}://{where.netloc}{where.path}" == f"{FakeAtproto.ISSUER}/authorize"
    q = urllib.parse.urlencode({"state": atproto.state, "code": atproto.issued_code,
                                "iss": FakeAtproto.ISSUER})  # fmt: skip
    return b.get(f"/auth/bsky/callback?{q}", follow_redirects=False)


def test_bluesky_oauth_signs_in_and_links_to_the_current_account(world):
    app, _, atproto = world
    b = browser(app)
    b.post("/api/auth/key/new")
    r = bsky_sign_in(b, atproto)
    assert r.headers["location"] == "/#signed-in" and atproto.nonce_asked
    me = b.get("/api/me").json()["account"]
    assert {(x["kind"], x["handle"]) for x in me["logins"]} == {
        ("key", None), ("bsky", "alice.example.com")}  # fmt: skip
    assert me["avatar_url"] == "https://cdn.bsky.app/img/avatar/a.jpg"
    assert me["display_name"] == "Alice"
    # a replayed callback is refused: each sign-in state works once
    q = urllib.parse.urlencode({"state": atproto.state, "code": "x", "iss": FakeAtproto.ISSUER})
    assert "failed" in browser(app).get(f"/auth/bsky/callback?{q}",
                                        follow_redirects=False).headers["location"]  # fmt: skip


def test_bluesky_wrong_issuer_or_account_is_refused(world):
    app, _, atproto = world
    b = browser(app)
    b.get("/auth/bsky/start?handle=alice.example.com", follow_redirects=False)
    q = urllib.parse.urlencode({"state": atproto.state, "code": atproto.issued_code,
                                "iss": "https://evil.example.com"})  # fmt: skip
    assert "failed" in b.get(f"/auth/bsky/callback?{q}", follow_redirects=False).headers["location"]
    b.get("/auth/bsky/start?handle=alice.example.com", follow_redirects=False)
    atproto.did_override = True
    real = atproto.did
    atproto.did = "did:plc:mallory"  # the token says someone else signed in
    q = urllib.parse.urlencode({"state": atproto.state, "code": atproto.issued_code,
                                "iss": FakeAtproto.ISSUER})  # fmt: skip
    assert "failed" in b.get(f"/auth/bsky/callback?{q}", follow_redirects=False).headers["location"]
    atproto.did = real
    assert b.get("/api/me").json()["account"] is None


def test_client_metadata_and_cross_site_writes(world):
    app, _, _ = world
    meta = browser(app).get("/oauth/client-metadata.json").json()
    assert meta["dpop_bound_access_tokens"] and meta["scope"] == "atproto"
    evil = browser(app).post("/api/auth/key/new", headers={"Origin": "https://evil.example"})
    assert evil.status_code == 403


def test_people_map_faces_first_and_only_when_shown(world, engine):
    app, _, atproto = world
    people = []
    for i in range(11):
        b = browser(app)
        b.post("/api/auth/key/new")
        b.put("/api/me/answers", json={"answers": answers(i)})
        people.append(b)
    star = browser(app)
    bsky_sign_in(star, atproto)
    star.put("/api/me/answers", json={"answers": answers(3)})
    first = browser(app).get("/api/map/people").json()
    assert first["count"] == 12 and all(set(p) == {"x", "y"} for p in first["people"])
    star.patch("/api/me", json={"show_on_map": True, "bio": "  Thinks   about AI. "})
    app_cache_bust(app, engine)
    shown = browser(app).get("/api/map/people").json()["people"]
    assert shown[0]["face"].startswith("https://cdn.bsky.app/")
    assert shown[0]["handle"] == "alice.example.com" and shown[0]["bio"] == "Thinks about AI."
    assert sum(1 for p in shown if "face" in p) == 1


def app_cache_bust(app, engine=None):
    app.state.people_cache.clear()
    if engine is not None:
        with engine.begin() as c:
            c.execute(text("DELETE FROM public_cache"))


def test_people_map_waits_for_ten(world):
    app, _, _ = world
    b = browser(app)
    b.post("/api/auth/key/new")
    b.put("/api/me/answers", json={"answers": answers()})
    data = browser(app).get("/api/map/people").json()
    assert data["count"] == 1 and data["people"] == []


def test_delete_account_removes_answers_and_logins(world, engine):
    app, _, _ = world
    b = browser(app)
    key = b.post("/api/auth/key/new").json()["key"]
    b.put("/api/me/answers", json={"answers": answers()})
    assert b.delete("/api/me").json()["ok"]
    assert b.get("/api/me").json() == {"account": None}
    assert browser(app).post("/api/auth/key", json={"key": key}).status_code == 404
    with engine.connect() as c:
        assert c.execute(text("SELECT count(*) FROM room_vote")).scalar() == 0
        assert c.execute(text("SELECT count(*) FROM account")).scalar() == 0


def test_key_format():
    key = accounts.new_key()
    assert accounts.key_subject(key) == accounts.key_subject(key.lower().replace("-", ""))
    assert accounts.key_subject("am-0000-0000-0000-0000-0000") is None  # 0 isn't in the alphabet
    assert not accounts.safe_https("https://127.0.0.1/x") and not accounts.safe_https(
        "http://a.com"
    )
    assert accounts.safe_https("https://bsky.social")


def test_signing_in_takes_over_the_earlier_anonymous_entry(world, engine):
    app, _, _ = world
    b = browser(app)
    key = "k" * 40
    joined = b.post("/api/rooms/ai-futures/join", json={"key": key, "consent_version": "room-v1",
                                                         "answers": answers()}).json()  # fmt: skip
    b.post("/api/auth/key/new")
    room = {"participant_id": joined["participant_id"], "key": key}
    b.put("/api/me/answers", json={"answers": answers(2), "room": room})
    with engine.connect() as c:
        assert c.execute(text("SELECT count(*) FROM room_participant")).scalar() == 1
    # someone else can't claim that entry, even knowing its id, without its key
    other = browser(app)
    other.post("/api/auth/key/new")
    other.put("/api/me/answers", json={"answers": answers(), "room": {**room, "key": "x" * 40}})
    with engine.connect() as c:
        assert c.execute(text("SELECT count(*) FROM room_participant")).scalar() == 2


def test_redirect_sign_in_returns_to_the_account_page(world):
    app, _, atproto = world
    b = browser(app)
    r = b.get("/auth/bsky/start?handle=alice.example.com&next=account", follow_redirects=False)
    assert r.status_code == 302
    q = urllib.parse.urlencode({"state": atproto.state, "code": atproto.issued_code,
                                "iss": FakeAtproto.ISSUER})  # fmt: skip
    back = b.get(f"/auth/bsky/callback?{q}", follow_redirects=False)
    assert back.headers["location"] == "/account.html#signed-in"


# ---------- round 2: results pages, socials, statements, camp names, scale

SUMMARY = {
    "home": BUNDLE["schools"][0]["label"],
    "answered": 20,
    "nearest": [{"id": BUNDLE["thinkers"][0]["id"], "k": 5, "n": 6}],
    "furthest": [],
    "signature": [],
    "camps": [],
    "rarest": None,
}
GLYPH = ([1, -1, 0, None] * 20)[: len(A)]


def test_account_results_page_keeps_its_code_and_shows_socials(world):
    app, _, atproto = world
    b = browser(app)
    bsky_sign_in(b, atproto)
    first = b.put("/api/me/profile", json={"summary": SUMMARY, "glyph": GLYPH}).json()
    again = b.put("/api/me/profile", json={"summary": SUMMARY, "glyph": GLYPH, "listed": True})
    assert again.json()["code"] == first["code"]
    me = b.get("/api/me").json()["account"]
    assert me["profile"]["code"] == first["code"] and me["profile"]["listed"]
    assert me["socials"][0]["handle"] == "alice.example.com"
    page = browser(app).get(f"/api/profiles/{first['code']}").json()
    assert page["display_name"] == "Alice" and page["identity"] == "bsky"
    assert page["socials"][0]["url"].startswith("https://bsky.app/profile/")
    assert b.delete("/api/me/profile").json()["ok"]
    assert browser(app).get(f"/api/profiles/{first['code']}").status_code == 404


def test_anonymous_account_page_is_anonymous_and_unlisted(world):
    app, _, _ = world
    b = browser(app)
    b.post("/api/auth/key/new")
    code = b.put("/api/me/profile", json={"summary": SUMMARY, "glyph": GLYPH, "listed": True})
    page = browser(app).get(f"/api/profiles/{code.json()['code']}").json()
    assert page["identity"] == "anon" and page["handle"] is None and not page["listed"]


def test_provider_bio_fills_an_empty_bio_only(world):
    app, _, atproto = world
    atproto.description = "Writes about   AI."
    fresh = browser(app)
    bsky_sign_in(fresh, atproto)
    me = fresh.get("/api/me").json()["account"]
    assert me["bio"] == "Writes about AI." and me["socials"][0]["followers"] == 42
    own = browser(app)
    own.post("/api/auth/key/new")
    own.patch("/api/me", json={"bio": "Mine."})
    atproto.did = "did:plc:other"
    bsky_sign_in(own, atproto)
    assert own.get("/api/me").json()["account"]["bio"] == "Mine."


def test_my_room_credentials_and_statements(world):
    app, _, _ = world
    b = browser(app)
    b.post("/api/auth/key/new")
    b.put("/api/me/answers", json={"answers": answers()})
    creds = b.post("/api/me/room").json()
    headers = {"X-Participant": creds["participant_id"], "X-Key": creds["key"]}
    r = b.post("/api/rooms/ai-futures/statements",
               json={"text": "Public labs should publish their safety test results."},
               headers=headers)  # fmt: skip
    assert r.status_code == 200, r.text
    mine = b.get("/api/me/statements").json()["statements"]
    assert mine[0]["text"].startswith("Public labs") and mine[0]["status"] in (
        "pending",
        "approved",
    )
    # a second browser gets fresh credentials; the first browser's key stops working
    again = b.post("/api/me/room").json()
    assert again["participant_id"] == creds["participant_id"]
    assert b.get("/api/rooms/ai-futures/me", headers=headers).status_code == 401
    # the account's map spot survives linking the room entry
    assert b.get("/api/me").json()["account"]["sheet"]["answers"] == answers()


def test_camp_names_inside_the_cluster_only(world):
    app, _, atproto = world
    b = browser(app)
    bsky_sign_in(b, atproto)
    b.put("/api/me/answers", json={"answers": answers()})
    mine = b.get("/api/camps/names").json()
    assert mine["verified"] and mine["nodes"]
    node = mine["nodes"][0]["id"]
    other = next(n for n in BUNDLE["tree"]["roots"] if n != node)
    assert b.post(f"/api/camps/{node}/names", json={"name": "see http://x.com"}).status_code == 422
    assert b.post(f"/api/camps/{other}/names", json={"name": "Not mine"}).status_code == 403
    made = b.post(f"/api/camps/{node}/names", json={"name": "Careful   builders"}).json()
    names = b.get("/api/camps/names").json()["names"]
    assert names[0]["name"] == "Careful builders" and names[0]["up"] == 1
    assert names[0]["my_vote"] == "up" and names[0]["proposed_by_me"]
    # key-only accounts can't propose or vote
    k = browser(app)
    k.post("/api/auth/key/new")
    k.put("/api/me/answers", json={"answers": answers()})
    assert k.post(f"/api/camps/names/{made['id']}/vote", json={"up": True}).status_code == 403
    assert not k.get("/api/camps/names").json()["verified"]
    # Benjamin decides
    admin = {"Authorization": "Bearer " + "t" * 24}
    assert browser(app).post(f"/api/admin/camps/names/{made['id']}", json={"accept": True},
                             headers=admin).json()["ok"]  # fmt: skip
    assert b.post(f"/api/camps/names/{made['id']}/vote", json={"up": False}).status_code == 404
    assert browser(app).get("/api/camps/accepted").json()["names"] == {node: "Careful builders"}


def test_hex_bins_count_everyone():
    from arena_api.account_routes import hex_bins

    pts = [{"x": (i % 50) * 3.0, "y": (i // 50) * 2.0} for i in range(5000)]
    bins = hex_bins(pts, 10.0)
    assert sum(c[2] for c in bins["cells"]) == 5000 and len(bins["cells"]) < 5000
