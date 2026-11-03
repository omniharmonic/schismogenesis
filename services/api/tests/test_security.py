"""Fixes from the pre-launch security review (2026-11-03)."""

import datetime
import json
import pathlib

import pytest
from arena_api.app import Config, create_app
from arena_api.identity import challenge_code, check_bsky
from arena_api.store import Store, key_hash
from fastapi.testclient import TestClient
from sqlalchemy import text

PUBLIC = pathlib.Path(__file__).parents[3] / "apps/arena/public"
BUNDLE = json.loads((PUBLIC / "fingerprint.json").read_text())
SUMMARY = {
    "home": "Long-term stewards",
    "answered": 20,
    "nearest": [{"id": "vitalik-buterin", "k": 5, "n": 6}],
}


FULL_SUMMARY = {**SUMMARY, "furthest": [], "signature": [], "camps": [], "rarest": None}


def _insert_profile(engine, display_name: str, handle: str = "evil.bsky.social") -> str:
    check = Store(engine).add_check("bsky", handle, "x")
    with engine.begin() as c:
        c.execute(
            text("UPDATE identity_check SET verified_at = now() WHERE check_id = :i"), {"i": check}
        )
        c.execute(
            text("""INSERT INTO profile (code, edit_hash, identity, handle, display_name, check_id,
                    summary, glyph, bundle_version) VALUES ('evil0001', :h, 'bsky', :hd, :n, :c,
                    CAST(:s AS jsonb), CAST(:g AS jsonb), 'v')"""),
            {"h": key_hash("k"), "hd": handle, "n": display_name, "c": check,
             "s": json.dumps(FULL_SUMMARY),
             "g": json.dumps([1] * 24)},
        )  # fmt: skip
    return "evil0001"


@pytest.mark.db
def test_display_name_cannot_inject_into_the_profile_page(engine):
    payload = '{{DATA}}"><script src=//cdn.jsdelivr.net/gh/a/b/x.js></script>'
    code = _insert_profile(engine, payload)
    client = TestClient(create_app(engine, config=Config()))
    page = client.get(f"/p/{code}").text
    assert "<script src=//cdn" not in page
    assert page.count("<script") == 2  # the JSON data block and profile.js, nothing else
    data = page.split('id="profile-data">')[1].split("</script>")[0]
    assert "<" not in data and json.loads(data)["display_name"] == payload
    assert "{{" in page.split("<title>")[1].split("</title>")[0]  # shown literally, not filled


@pytest.mark.db
def test_scripts_from_cdns_only_on_the_atlas(engine):
    client = TestClient(create_app(engine, config=Config()))
    assert "cdn.jsdelivr" not in client.get("/").headers["content-security-policy"]
    atlas = client.get("/atlas").headers["content-security-policy"]
    assert "3d-force-graph@1.79.0" in atlas and "https://cdn.jsdelivr.net " not in atlas + " "


@pytest.mark.db
def test_forged_forwarded_for_does_not_dodge_limits(engine):
    client = TestClient(create_app(engine, config=Config(trust_proxy=True)))
    codes = [
        client.post("/api/fairness", json={"rating": 3},
                    headers={"X-Forwarded-For": f"10.0.0.{i}, 203.0.113.7"}).status_code
        for i in range(21)
    ]  # fmt: skip
    assert codes[-1] == 429


@pytest.mark.db
def test_chunked_body_over_the_cap_is_refused(engine):
    client = TestClient(create_app(engine, config=Config()))

    def chunks():
        for _ in range(100):
            yield b"x" * 1024

    r = client.post("/api/fairness", content=chunks(), headers={"Content-Type": "application/json"})
    assert r.status_code == 413
    ok = client.post("/api/fairness", content=iter([b'{"rating": 4}']),
                     headers={"Content-Type": "application/json"})  # fmt: skip
    assert ok.status_code == 200


def test_bsky_code_is_long_and_old_posts_do_not_count():
    code = challenge_code()
    assert len(code.removeprefix("dialogos-")) == 16
    now = datetime.datetime.now(datetime.UTC)

    def fetch(url):
        if "getProfile" in url:
            return {"did": "did:plc:v", "handle": "victim.bsky.social"}
        old = (now - datetime.timedelta(days=2)).isoformat()
        return {"feed": [{"post": {"author": {"did": "did:plc:v"},
                                   "record": {"text": code, "createdAt": old}}}]}  # fmt: skip

    assert check_bsky("victim.bsky.social", code, fetch, after=now) is None
    assert check_bsky("victim.bsky.social", code, fetch, after=now - datetime.timedelta(days=3))


@pytest.mark.db
def test_turnstile_guards_writes_when_switched_on(engine):
    Store(engine).ensure_room("ai-futures", "AI futures", BUNDLE)
    seen = []

    def human(secret, token, address):
        seen.append(token)
        return token == "good-token"

    on = Config(turnstile_site_key="site", turnstile_secret="secret")
    client = TestClient(create_app(engine, config=on, human=human))
    assert client.get("/api/config").json() == {"turnstile_site_key": "site"}
    body = {"key": "k" * 40, "consent_version": "room-v1", "answers": {}}
    assert client.post("/api/rooms/ai-futures/join", json=body).status_code == 403
    ok = client.post("/api/rooms/ai-futures/join", json=body, headers={"X-Turnstile": "good-token"})
    assert ok.status_code == 200
    dispute = {"person_id": "vitalik-buterin", "body": "Misread this view"}
    assert client.post("/api/disputes", json=dispute).status_code == 403
    assert (
        client.post("/api/fairness", json={"rating": 3}).status_code == 200
    )  # low-stakes stays open
    off = TestClient(create_app(engine, config=Config(), human=human))
    assert off.get("/api/config").json() == {"turnstile_site_key": None}
    assert off.post("/api/rooms/ai-futures/join", json=body).status_code == 200


@pytest.mark.db
def test_launch_gate(engine):
    client = TestClient(create_app(engine, config=Config(site_password="letmein")))
    assert client.get("/").status_code == 401
    assert client.get("/api/health").status_code == 200
    assert client.get("/", auth=("anyone", "letmein")).status_code == 200
    assert client.get("/", auth=("anyone", "wrong")).status_code == 401
