"""Launch round: publishing, verification, share images, report cache, limits and counters."""

import datetime
import json
import pathlib

import pytest
from arena_api.app import Config, create_app
from arena_api.cards import profile_card
from arena_api.identity import check_bsky, normalise_bsky
from arena_api.store import Store
from fastapi.testclient import TestClient
from sqlalchemy import text

PUBLIC = pathlib.Path(__file__).parents[3] / "apps/arena/public"
BUNDLE = json.loads((PUBLIC / "fingerprint.json").read_text())
A = [a["id"] for a in BUNDLE["anchors"]]
SUMMARY = {
    "home": BUNDLE["schools"][0]["label"],
    "answered": 20,
    "nearest": [{"id": "vitalik-buterin", "k": 5, "n": 6}, {"id": "max-tegmark", "k": 6, "n": 8}],
    "furthest": [{"id": "josh-hawley", "k": 3, "n": 11}],
    "signature": [{"anchor": A[1], "answer": -1, "ally": BUNDLE["schools"][1]["label"]}],
    "camps": [{"id": "eacc", "agreed": 3, "opposed": 5, "deepest": "ontological"}],
    "rarest": {"anchor": A[2], "answer": 1},
}
GLYPH = ([1, -1, 0, None] * 9)[: len(A)]


def NOW() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat()


class FakeBsky:
    def __init__(self, code_holder):
        self.code_holder = code_holder

    def __call__(self, url):
        if "getProfile" in url:
            return {
                "did": "did:plc:abc",
                "handle": "alice.bsky.social",
                "displayName": "Alice",
                "avatar": "https://cdn.bsky.app/img/avatar/alice.jpg",
            }
        posts = [
            {
                "post": {
                    "author": {"did": "did:plc:other"},
                    "record": {"text": self.code_holder[0], "createdAt": NOW()},
                }
            }
        ]
        if self.code_holder[1]:
            posts.append(
                {
                    "post": {
                        "author": {"did": "did:plc:abc"},
                        "record": {"text": f"verifying {self.code_holder[0]}", "createdAt": NOW()},
                    }
                }
            )
        return {"feed": posts}


@pytest.fixture
def setup(engine):
    holder = ["", False]
    Store(engine).ensure_room("ai-futures", "AI futures", BUNDLE)
    app = create_app(engine, config=Config(admin_token="t" * 24), fetch=FakeBsky(holder))
    return TestClient(app), holder


def test_bsky_handle_rules():
    assert normalise_bsky("@Alice") == "alice.bsky.social"
    assert normalise_bsky("bob.example.com") == "bob.example.com"
    assert normalise_bsky("no spaces allowed.com") is None


def test_bsky_check_ignores_reposts_of_the_code():
    holder = ["dialogos-abc123", False]
    assert check_bsky("alice.bsky.social", holder[0], FakeBsky(holder)) is None
    holder[1] = True
    found = check_bsky("alice.bsky.social", holder[0], FakeBsky(holder))
    assert found is not None and found.display_name == "Alice" and found.account_id == "did:plc:abc"


def test_card_renders_png():
    profile = {
        "display_name": "Fingerprint K7Q2",
        "handle": None,
        "glyph": GLYPH,
        "summary": {
            **SUMMARY,
            "signature": [
                {
                    "anchor": A[1],
                    "answer": -1,
                    "ally": BUNDLE["schools"][1]["label"],
                    "text": "Some statement",
                }
            ],
        },
    }
    image = profile_card(profile, {t["id"]: t["name"] for t in BUNDLE["thinkers"]})
    assert image[:8] == b"\x89PNG\r\n\x1a\n" and len(image) > 10_000


@pytest.mark.db
def test_anonymous_publish_view_edit_delete(setup, engine):
    client, _ = setup
    r = client.post(
        "/api/profiles",
        json={"summary": SUMMARY, "glyph": GLYPH, "identity": "anon", "listed": True},
    )
    assert r.status_code == 200, r.text
    code, key = r.json()["code"], r.json()["edit_key"]
    profile = client.get(f"/api/profiles/{code}").json()
    assert profile["display_name"].startswith("Fingerprint ") and profile["handle"] is None
    assert profile["listed"] is False  # anonymous profiles are never listed
    assert profile["answers"] is None
    assert profile["summary"]["signature"][0]["text"] == BUNDLE["anchors"][1]["text"]
    page = client.get(f"/p/{code}")
    assert (
        page.status_code == 200 and "og:image" in page.text and f"/p/{code}/card.png" in page.text
    )
    assert client.get(f"/p/{code}/card.png").headers["content-type"] == "image/png"
    assert (
        client.delete(f"/api/profiles/{code}", headers={"X-Edit-Key": "wrong"}).status_code == 403
    )
    assert client.delete(f"/api/profiles/{code}", headers={"X-Edit-Key": key}).status_code == 200
    assert client.get(f"/api/profiles/{code}").status_code == 404
    with engine.connect() as c:
        assert c.execute(text("SELECT count(*) FROM profile")).scalar() == 0


@pytest.mark.db
def test_summary_text_is_rebuilt_and_bad_input_refused(setup):
    client, _ = setup
    bad = {**SUMMARY, "home": "<script>alert(1)</script>"}
    assert (
        client.post(
            "/api/profiles", json={"summary": bad, "glyph": GLYPH, "identity": "anon"}
        ).status_code
        == 422
    )
    bad = {**SUMMARY, "nearest": [{"id": "vitalik-buterin", "k": 9, "n": 3}]}
    assert (
        client.post(
            "/api/profiles", json={"summary": bad, "glyph": GLYPH, "identity": "anon"}
        ).status_code
        == 422
    )
    assert (
        client.post(
            "/api/profiles", json={"summary": SUMMARY, "glyph": [1, 2], "identity": "anon"}
        ).status_code
        == 422
    )


@pytest.mark.db
def test_verified_bsky_publish_listed_once_per_account(setup):
    client, holder = setup
    assert (
        client.post(
            "/api/profiles", json={"summary": SUMMARY, "glyph": GLYPH, "identity": "bsky"}
        ).status_code
        == 403
    )
    start = client.post("/api/verify/bsky/start", json={"handle": "alice"}).json()
    holder[0] = start["code"]
    assert (
        client.post("/api/verify/bsky/check", json={"check_id": start["check_id"]}).json()[
            "verified"
        ]
        is False
    )
    holder[1] = True
    done = client.post("/api/verify/bsky/check", json={"check_id": start["check_id"]}).json()
    assert done["verified"] and done["display_name"] == "Alice"
    answers = {A[0]: 1, A[1]: -1}
    r = client.post(
        "/api/profiles",
        json={
            "summary": SUMMARY,
            "glyph": GLYPH,
            "identity": "bsky",
            "check_id": start["check_id"],
            "listed": True,
            "answers": answers,
        },
    )
    assert r.status_code == 200, r.text
    first = r.json()["code"]
    profile = client.get(f"/api/profiles/{first}").json()
    assert profile["handle"] == "alice.bsky.social" and profile["answers"] == answers
    assert [p["code"] for p in client.get("/api/people").json()["people"]] == [first]
    # the same check can't be reused
    again = client.post(
        "/api/profiles",
        json={
            "summary": SUMMARY,
            "glyph": GLYPH,
            "identity": "bsky",
            "check_id": start["check_id"],
        },
    )
    assert again.status_code == 403
    # a new verification replaces the account's old profile
    start2 = client.post("/api/verify/bsky/start", json={"handle": "alice"}).json()
    holder[0] = start2["code"]
    client.post("/api/verify/bsky/check", json={"check_id": start2["check_id"]})
    second = client.post(
        "/api/profiles",
        json={
            "summary": SUMMARY,
            "glyph": GLYPH,
            "identity": "bsky",
            "check_id": start2["check_id"],
        },
    ).json()["code"]
    assert client.get(f"/api/profiles/{first}").status_code == 404
    assert client.get(f"/api/profiles/{second}").status_code == 200
    # admin can hide
    admin = {"Authorization": "Bearer " + "t" * 24}
    assert (
        client.post(
            f"/api/admin/profiles/{second}", headers=admin, json={"hidden": True}
        ).status_code
        == 200
    )
    assert client.get(f"/p/{second}").status_code == 404


@pytest.mark.db
def test_x_sign_in_off_without_keys(setup):
    client, _ = setup
    assert client.get("/api/verify/options").json() == {"bsky": True, "x": False}
    assert client.get("/auth/x/start", follow_redirects=False).status_code == 404


@pytest.mark.db
def test_report_cache_and_counters_and_limits(setup, engine):
    client, _ = setup
    client.get("/api/rooms/ai-futures/report")
    with engine.connect() as c:
        assert c.execute(text("SELECT count(*) FROM report_cache")).scalar() == 1
    client.post("/api/event", json={"name": "finish"})
    client.post("/api/event", json={"name": "not-a-real-event"})
    with engine.connect() as c:
        rows = dict(c.execute(text("SELECT name, n FROM daily_counter")).all())
    assert rows == {"finish": 1}
    codes = [client.post("/api/fairness", json={"rating": 3}).status_code for _ in range(21)]
    assert codes[-1] == 429 and codes[0] == 200
    r = client.get("/")
    assert "default-src 'self'" in r.headers["content-security-policy"]


def test_production_requires_admin_token(monkeypatch):
    monkeypatch.setenv("ARENA_ENV", "production")
    monkeypatch.delenv("ARENA_ADMIN_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        Config.from_env()
