"""Portraits for the thinkers on the map, from Wikimedia Commons only (2026-11-04).

Usage: fetch_faces.py [--refresh] [id ...]

For each thinker in the fingerprint bundle: find their Wikidata entry (a human whose label matches
the name, or the id in seed/faces-overrides.json), take its image (P18), and keep it only if the
Commons licence is free (CC0, public domain, CC BY, CC BY-SA). Saves a 192px square-ish JPEG
thumbnail to apps/arena/public/faces/<id>.jpg and the credit to seed/faces.json, which the bundle
build copies into each thinker. No image is better than a wrong or unlicensed one: anyone not
matched keeps their initials.
"""

import io
import json
import pathlib
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

BUNDLE = pathlib.Path("apps/arena/public/fingerprint.json")
OUT_DIR = pathlib.Path("apps/arena/public/faces")
CREDITS = pathlib.Path("seed/faces.json")
OVERRIDES = pathlib.Path("seed/faces-overrides.json")
UA = "DialogosArena/0.1 (https://github.com/omniharmonic; portraits with attribution)"
FREE = re.compile(r"^(cc0|cc[- ]by(-sa)?[- ]?\d|cc[- ]by(-sa)?$|public domain|pd)", re.I)
SIZE = 192


def get(url: str, params: dict | None = None) -> bytes:
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:  # noqa: BLE001 - polite retry on any network error
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed: {url}")


def api(base: str, **params) -> dict:
    return json.loads(get(base, {**params, "format": "json"}))


def plain(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def born(claims: dict) -> int | None:
    for c in claims.get("P569", []):
        t = c["mainsnak"].get("datavalue", {}).get("value", {}).get("time", "")
        if t[1:5].isdigit():
            return int(t[1:5])
    return None


def find_entity(name: str) -> str | None:
    """The first search hit that is a living-era human (P31 = Q5, born 1935 or later, or no
    birth date) whose label or alias matches the name. Namesakes from other centuries are out."""
    hits = api("https://www.wikidata.org/w/api.php", action="wbsearchentities", search=name,
               language="en", type="item", limit=7)["search"]  # fmt: skip
    for h in hits:
        names = [plain(h.get("label", ""))] + [plain(a) for a in h.get("aliases", [])]
        if plain(name) not in names:
            continue
        claims = entity_claims(h["id"])
        human = any(
            c["mainsnak"].get("datavalue", {}).get("value", {}).get("id") == "Q5"
            for c in claims.get("P31", [])
        )
        year = born(claims)
        if human and (year is None or year >= 1935):
            return h["id"]
    return None


def entity_claims(qid: str) -> dict:
    return api("https://www.wikidata.org/w/api.php", action="wbgetclaims", entity=qid)["claims"]


def describe(qid: str) -> str:
    e = api("https://www.wikidata.org/w/api.php", action="wbgetentities", ids=qid,
            props="descriptions", languages="en")["entities"][qid]  # fmt: skip
    return e.get("descriptions", {}).get("en", {}).get("value", "")


def commons(filename: str) -> dict | None:
    pages = api("https://commons.wikimedia.org/w/api.php", action="query",
                titles=f"File:{filename}", prop="imageinfo", iiprop="url|extmetadata",
                iiurlwidth=SIZE * 2)["query"]["pages"]  # fmt: skip
    info = next(iter(pages.values())).get("imageinfo", [None])[0]
    if not info:
        return None
    meta = info.get("extmetadata", {})

    def text(key: str) -> str:
        return re.sub(r"<[^>]+>", "", meta.get(key, {}).get("value", "")).strip()

    return {
        "thumb": info["thumburl"],
        "page": info["descriptionurl"],
        "license": text("LicenseShortName"),
        "license_url": text("LicenseUrl"),
        "artist": text("Artist") or text("Credit"),
    }


def square(data: bytes) -> bytes:
    from PIL import Image

    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    side = min(w, h)
    top = 0 if h > w else (h - side) // 2  # portraits: keep the head, crop from the bottom
    img = img.crop(((w - side) // 2, top, (w - side) // 2 + side, top + side)).resize((SIZE, SIZE))
    out = io.BytesIO()
    img.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    return out.getvalue()


def main(*args: str) -> None:
    refresh = "--refresh" in args
    only = {a for a in args if not a.startswith("--")}
    thinkers = json.loads(BUNDLE.read_text())["thinkers"]
    credits = json.loads(CREDITS.read_text()) if CREDITS.exists() else {}
    overrides = json.loads(OVERRIDES.read_text()) if OVERRIDES.exists() else {}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    missed = []
    for t in thinkers:
        pid = t["id"]
        if only and pid not in only:
            continue
        if pid in credits and not refresh and (OUT_DIR / f"{pid}.jpg").exists():
            continue
        override = overrides.get(pid, {})
        if override.get("skip"):
            continue
        qid = override.get("qid") or find_entity(override.get("name", t["name"]))
        if not qid:
            missed.append(f"{pid}: no Wikidata human with an image")
            continue
        p18 = entity_claims(qid).get("P18") or []
        filename = override.get("file") or (
            p18[0]["mainsnak"]["datavalue"]["value"] if p18 else None
        )
        if not filename:
            missed.append(f"{pid}: {qid} has no image")
            continue
        info = commons(filename)
        if not info or not FREE.match(info["license"]):
            missed.append(f"{pid}: licence not free ({info and info['license']})")
            continue
        (OUT_DIR / f"{pid}.jpg").write_bytes(square(get(info["thumb"])))
        credits[pid] = {
            "qid": qid,
            "description": describe(qid),
            "file": filename,
            "source": info["page"],
            "license": info["license"],
            "license_url": info["license_url"],
            "artist": info["artist"][:200],
        }
        print(f"{pid}: {credits[pid]['description']} [{info['license']}]")
        time.sleep(0.5)
    CREDITS.write_text(
        json.dumps(dict(sorted(credits.items())), indent=1, ensure_ascii=False) + "\n"
    )
    print(len(credits), "portraits;", len(missed), "without:")
    for m in missed:
        print(" ", m)


if __name__ == "__main__":
    main(*sys.argv[1:])
