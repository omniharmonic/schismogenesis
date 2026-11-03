"""Build the fingerprint bundle and the atlas page for the arena app.

Usage: build_fingerprint.py [atlas.json] [out_dir] [--season] [--version fp-...]
  --season keeps the statements in the current bundle (docs/fingerprint/05-ATLAS-EXPANSION.md).
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
    paths = [a for a in args if not a.startswith("--") and a != version]
    atlas_path = paths[0] if paths else "apps/arena/source/atlas-v1.json"
    out = paths[1] if len(paths) > 1 else "apps/arena/public"
    current = REPO / out / "fingerprint.json"
    previous = json.loads(current.read_text()) if current.exists() else None
    season = previous["anchors"] if season_mode and previous else None
    version = version or (previous["version"] if previous else None)
    atlas = json.loads((REPO / atlas_path).read_text())
    extra = {"version": version} if version else {}
    atlas_version = pathlib.Path(atlas_path).stem
    bundle = build_bundle(atlas, flagged_ids(), season=season, atlas_version=atlas_version, **extra)
    target = REPO / out
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
