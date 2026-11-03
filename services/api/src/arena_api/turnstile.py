"""Cloudflare Turnstile bot protection (D-31.18). Off unless ARENA_TURNSTILE_SECRET is set."""

import json
import urllib.parse
import urllib.request
from collections.abc import Callable

VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
# Cloudflare's published test keys: they always pass, for local runs and tests.
TEST_SITE_KEY = "1x00000000000000000000AA"
TEST_SECRET = "1x0000000000000000000000000000000AA"

Verifier = Callable[[str, str, str | None], bool]


def verify(secret: str, token: str, address: str | None) -> bool:
    if not token:
        return False
    fields = {"secret": secret, "response": token}
    if address:
        fields["remoteip"] = address
    request = urllib.request.Request(VERIFY_URL, data=urllib.parse.urlencode(fields).encode())
    try:
        with urllib.request.urlopen(request, timeout=8) as response:  # noqa: S310 (fixed host)
            return bool(json.loads(response.read()).get("success"))
    except Exception:
        return False  # fail closed: a protected action needs a confirmed human
