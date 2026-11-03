"""Reuse the core database fixtures: a freshly migrated scratch database per test."""

import importlib.util
import pathlib

_path = pathlib.Path(__file__).parents[3] / "packages/arena_core/tests/conftest.py"
_spec = importlib.util.spec_from_file_location("arena_core_fixtures", _path)
assert _spec and _spec.loader
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)

db_url = _core.db_url
engine = _core.engine
