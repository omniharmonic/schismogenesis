"""Red-line checks that can run today. S13 adds the transcript-span check once bundles exist."""

import json
import pathlib
import subprocess

PUBLIC_DIRS = ("apps/web/public", "dist", "bundles")
PUBLIC_SUFFIXES = {".json", ".html", ".txt", ".md", ".js", ".csv", ".xml"}
FORBIDDEN_TRACKED_PREFIXES = ("transcripts/", "data/", "evals/queue/", "evals/results/")


def tracked_files(root: pathlib.Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
    )
    return result.stdout.splitlines()


def hidden_landmarks(seed_path: pathlib.Path) -> dict[str, str]:
    seed = json.loads(seed_path.read_text())
    return {
        flag["landmark_id"]: flag["name"] for flag in seed["flags_for_benjamin"]["landmarks"]
    } | {record["landmark_id"]: record["name"] for record in seed["excluded_landmarks"]}


def check(root: pathlib.Path, tracked: list[str] | None = None) -> list[str]:
    """Return one line per violation."""
    problems = []
    for path in tracked_files(root) if tracked is None else tracked:
        name = pathlib.PurePosixPath(path).name
        if (
            name == ".env"
            or (name.startswith(".env.") and name != ".env.example")
            or path.startswith(FORBIDDEN_TRACKED_PREFIXES)
        ):
            problems.append(f"must not be in git: {path}")

    hidden = hidden_landmarks(root / "seed/SEED-v4.json")
    for directory in PUBLIC_DIRS:
        base = root / directory
        files = base.rglob("*") if base.exists() else ()
        for file in files:
            if file.is_file() and file.suffix in PUBLIC_SUFFIXES:
                content = file.read_text(errors="ignore")
                for landmark_id, name in hidden.items():
                    if landmark_id in content or name in content:
                        problems.append(f"{file.relative_to(root)} mentions hidden: {landmark_id}")
    return problems
