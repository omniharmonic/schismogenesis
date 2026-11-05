"""Portraits for the thinkers on the map (2026-11-04).

Usage: fetch_faces.py [--refresh] [id ...]

Who: every thinker in the fingerprint bundle, plus everyone in the current reading round's
coverage file (people who may join the map later). Held-out landmarks (SEED-v4.json
flags_for_benjamin) are never fetched.

Where from, in order:
1. Wikimedia Commons. Find their Wikidata entry (a human whose label matches the name, or the qid
   in seed/faces-overrides.json), take its image (P18) or the override's "file", and keep it only
   if the Commons licence is free (CC0, public domain, CC BY, CC BY-SA).
2. A photo the person or their employer published as their own profile/press photo (personal
   site, blog author image, GitHub avatar, official bio page). Only through an explicit override:
   {"url": <direct image url>, "source": <page it appears on>, "artist": <who published it>,
    "license": "Self-published profile photo", "license_url": "", "description": <who this is>}.
   Never news or stock-agency photography; for pseudonymous people, only their own chosen image.

Any override may add "crop": [left, top, right, bottom] as fractions of the image, applied before
the square crop, to centre a face in a wider photo.

Saves a 192px square JPEG to apps/arena/public/faces/<id>.jpg and the credit to seed/faces.json,
which the bundle build copies into each thinker. No image is better than a wrong or unlicensed
one: anyone not matched keeps their initials. Every new image is checked by eye before release.
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
COVERAGE = pathlib.Path("evals/queue/round5/COVERAGE.json")
SEED = pathlib.Path("seed/SEED-v4.json")
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


def commons(filename: str, width: int = SIZE * 2) -> dict | None:
    pages = api("https://commons.wikimedia.org/w/api.php", action="query",
                titles=f"File:{filename}", prop="imageinfo", iiprop="url|extmetadata",
                iiurlwidth=width)["query"]["pages"]  # fmt: skip
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


def square(data: bytes, crop: list[float] | None = None) -> bytes:
    from PIL import Image

    img = Image.open(io.BytesIO(data)).convert("RGB")
    if crop:  # fractions of the original: centre a face in a wider photo
        w, h = img.size
        img = img.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    w, h = img.size
    side = min(w, h)
    top = 0 if h > w else (h - side) // 2  # portraits: keep the head, crop from the bottom
    img = img.crop(((w - side) // 2, top, (w - side) // 2 + side, top + side)).resize((SIZE, SIZE))
    out = io.BytesIO()
    img.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    return out.getvalue()


def people() -> list[dict]:
    """Bundle thinkers, then coverage people not yet on the map; held-out landmarks removed."""
    held = {
        f["landmark_id"]
        for f in json.loads(SEED.read_text()).get("flags_for_benjamin", {}).get("landmarks", [])
    }
    out = [{"id": t["id"], "name": t["name"]} for t in json.loads(BUNDLE.read_text())["thinkers"]]
    if COVERAGE.exists():
        seen = {t["id"] for t in out}
        cov = json.loads(COVERAGE.read_text())["people"]
        out += [{"id": p["id"], "name": p["name"]} for p in cov if p["id"] not in seen]
    return [p for p in out if p["id"] not in held]


def self_published(pid: str, override: dict) -> dict:
    """A profile photo the person or their employer published; recorded with where it came from."""
    (OUT_DIR / f"{pid}.jpg").write_bytes(square(get(override["url"]), override.get("crop")))
    return {
        "qid": override.get("qid", ""),
        "description": override.get("description", ""),
        "file": override["url"],
        "source": override["source"],
        "license": override.get("license", "Self-published profile photo"),
        "license_url": override.get("license_url", ""),
        "artist": override["artist"][:200],
    }


def main(*args: str) -> None:
    refresh = "--refresh" in args
    only = {a for a in args if not a.startswith("--")}
    thinkers = people()
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
        if override.get("url"):
            credits[pid] = self_published(pid, override)
            print(f"{pid}: {credits[pid]['description']} [{credits[pid]['license']}]")
            time.sleep(0.5)
            continue
        qid = override.get("qid") or find_entity(override.get("name", t["name"]))
        if not qid and not override.get("file"):
            missed.append(f"{pid}: no Wikidata human with an image")
            continue
        p18 = (entity_claims(qid).get("P18") or []) if qid else []
        filename = override.get("file") or (
            p18[0]["mainsnak"]["datavalue"]["value"] if p18 else None
        )
        if not filename:
            missed.append(f"{pid}: {qid} has no image")
            continue
        info = commons(filename, width=1200 if override.get("crop") else SIZE * 2)
        if not info or not FREE.match(info["license"]):
            missed.append(f"{pid}: licence not free ({info and info['license']})")
            continue
        (OUT_DIR / f"{pid}.jpg").write_bytes(square(get(info["thumb"]), override.get("crop")))
        credits[pid] = {
            "qid": qid,
            "description": override.get("description") or (describe(qid) if qid else ""),
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
