"""Build the fingerprint bundle and the atlas page for the arena app.

Usage: build_fingerprint.py [atlas.json] [out_dir]
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


def main(
    atlas_path: str = "apps/arena/source/atlas-v1.json", out: str = "apps/arena/public"
) -> None:
    atlas = json.loads((REPO / atlas_path).read_text())
    bundle = build_bundle(atlas, flagged_ids())
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


if __name__ == "__main__":
    main(*sys.argv[1:])
