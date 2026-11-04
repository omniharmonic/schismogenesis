"""Build the fingerprint bundle and the atlas page for the arena app.

Usage: build_fingerprint.py [atlas.json] [out_dir] [--season [file]] [--version fp-...]
  --season takes the statements and their reviewed wording from a season file
  (default seed/season-1.json).
"""

import json
import pathlib
import subprocess
import sys

from arena_fingerprint.bundle import build_bundle

REPO = pathlib.Path(__file__).resolve().parents[1]


def flagged_ids() -> set[str]:
    seed = json.loads((REPO / "seed/SEED-v4.json").read_text())
    return {f["landmark_id"] for f in seed["flags_for_benjamin"]["landmarks"]}


def main(*args: str) -> None:
    season_mode = "--season" in args
    version = args[args.index("--version") + 1] if "--version" in args else None
    after = (
        args[args.index("--season") + 1]
        if season_mode and args.index("--season") + 1 < len(args)
        else ""
    )
    season_file = after if after.endswith(".json") and "season" in after else "seed/season-1.json"
    paths = [a for a in args if not a.startswith("--") and a not in (version, season_file)]
    atlas_path = paths[0] if paths else "apps/arena/source/atlas-v1.json"
    out = paths[1] if len(paths) > 1 else "apps/arena/public"
    current = REPO / out / "fingerprint.json"
    previous = json.loads(current.read_text()) if current.exists() else None
    # the reviewed season file decides the statements and their wording
    season_doc = json.loads((REPO / season_file).read_text()) if season_mode else None
    season = season_doc["statements"] if season_doc else None
    version = version or (previous["version"] if previous else None)
    atlas = json.loads((REPO / atlas_path).read_text())
    extra = {"version": version} if version else {}
    atlas_version = pathlib.Path(atlas_path).stem
    newcomers = {
        p["id"]: p["name"]
        for name in (
            "AI-FUTURES-SOURCES-v2.json",
            "AI-FUTURES-SOURCES-v4.json",
            "AI-FUTURES-SOURCES-v5.json",
        )  # fmt: skip
        if (REPO / "seed" / name).exists()
        for p in json.loads((REPO / "seed" / name).read_text()).get("people", [])
    }
    voices_path = REPO / "seed/thinker-voices.json"
    voices = json.loads(voices_path.read_text()) if voices_path.exists() else {}
    bundle = build_bundle(
        atlas,
        flagged_ids(),
        season=season,
        atlas_version=atlas_version,
        newcomers=newcomers,
        voices=voices,
        **({"season_id": season_doc["season"]} if season_doc else {}),
        **extra,
    )
    target = REPO / out
    # portraits from Wikimedia Commons (scripts/fetch_faces.py), each with its credit
    credits_path = REPO / "seed/faces.json"
    credits = json.loads(credits_path.read_text()) if credits_path.exists() else {}
    bundle["faces"] = {}
    for t in bundle["thinkers"]:
        c = credits.get(t["id"])
        if c and (target / "faces" / f"{t['id']}.jpg").exists():
            t["face"] = f"/faces/{t['id']}.jpg"
            bundle["faces"][t["id"]] = {
                k: c[k] for k in ("artist", "license", "license_url", "source")
            }
    (target / "fingerprint.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1))
    subprocess.run(
        [
            sys.executable,
            str(REPO / "apps/atlas/build_page.py"),
            str(REPO / atlas_path),
            str(target / "atlas.html"),
            "--full-document",
        ],
        check=True,
    )
    print(f"{len(bundle['anchors'])} anchors -> {target / 'fingerprint.json'}")
    for line in bundle["selection_log"]:
        print("  note:", line)


def _option(args: tuple[str, ...], name: str) -> str | None:
    return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else None


def _values(args: tuple[str, ...]) -> set[str]:
    return {v for v in [_option(args, "--version")] if v}


if __name__ == "__main__":
    main(*sys.argv[1:])
