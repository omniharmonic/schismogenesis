"""Assemble build/vercel: the web app alone, ready for `vercel deploy` (D-31.18).

Usage: uv run python scripts/build_vercel.py
The uv workspace is too big for Vercel's Python builder (it includes local-model code), so this
copies only the four packages the web app needs, the site and fonts, and pins third-party
dependencies from uv.lock.
"""

import pathlib
import shutil
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[1]
OUT = REPO / "build/vercel"
PACKAGES = {
    "arena_api": "services/api/src/arena_api",
    "arena_core": "packages/arena_core/src/arena_core",
    "arena_fingerprint": "packages/arena_fingerprint/src/arena_fingerprint",
    "arena_rounds": "packages/arena_rounds/src/arena_rounds",
}
ENTRY = '''"""Vercel entry point: the AI Futures Fingerprint web app."""

import os
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
os.environ.setdefault("ARENA_PUBLIC_DIR", str(HERE / "site"))
os.environ.setdefault("ARENA_FONTS_DIR", str(HERE / "fonts"))
os.environ.setdefault("ARENA_ENV", "production")
os.environ.setdefault("ARENA_TRUST_PROXY", "1")

from arena_api.serverless import app  # noqa: E402

__all__ = ["app"]
'''
VERCEL_JSON = """{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "regions": ["iad1"],
  "functions": {
    "main.py": { "maxDuration": 60, "excludeFiles": "{**/__pycache__/**,**/tests/**}" }
  }
}
"""


def main() -> None:
    if OUT.exists():
        keep = OUT / ".vercel"  # the project link survives rebuilds
        saved = None
        if keep.exists():
            saved = OUT.parent / ".vercel-link"
            shutil.rmtree(saved, ignore_errors=True)
            shutil.move(str(keep), saved)
        shutil.rmtree(OUT)
        OUT.mkdir(parents=True)
        if saved:
            shutil.move(str(saved), OUT / ".vercel")
    else:
        OUT.mkdir(parents=True)
    ignore = shutil.ignore_patterns("__pycache__", "tests")
    for name, source in PACKAGES.items():
        shutil.copytree(REPO / source, OUT / name, ignore=ignore)
    shutil.copytree(
        REPO / "apps/arena/public", OUT / "site", ignore=shutil.ignore_patterns("atlas.html.bak")
    )
    shutil.copytree(REPO / "apps/arena/fonts", OUT / "fonts")
    pins = subprocess.run(
        ["uv", "export", "--package", "arena_api", "--no-dev", "--no-hashes", "--frozen",
         "--no-emit-workspace"],
        cwd=REPO, check=True, capture_output=True, text=True,
    ).stdout  # fmt: skip
    lines = [ln for ln in pins.splitlines() if ln and not ln.startswith(("#", " ", "-e"))]
    (OUT / "requirements.txt").write_text("\n".join(lines) + "\n")
    (OUT / "main.py").write_text(ENTRY)
    (OUT / "vercel.json").write_text(VERCEL_JSON)
    (OUT / ".python-version").write_text("3.12\n")
    (OUT / ".vercelignore").write_text("__pycache__\n*.pyc\n")
    size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()) / 1e6
    print(f"build/vercel ready: {size:.1f} MB before dependencies; {len(lines)} pinned packages")


if __name__ == "__main__":
    main()
