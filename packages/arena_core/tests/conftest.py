"""Database fixtures. Each test gets a freshly migrated scratch database on the dev server."""

import os
import pathlib

import pytest
from alembic import command
from alembic.config import Config
from arena_core.config import load_settings
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import OperationalError

REPO = pathlib.Path(__file__).parents[3]
ALEMBIC_INI = REPO / "packages/arena_core/alembic.ini"
TEST_DB = "arena_test"


def alembic_config(url: str) -> Config:
    config = Config(str(ALEMBIC_INI))
    config.set_main_option("sqlalchemy.url", url.replace("%", "%%"))
    return config


@pytest.fixture
def db_url():
    base = make_url(load_settings().database_url)
    admin = create_engine(base, isolation_level="AUTOCOMMIT")
    try:
        with admin.connect() as connection:
            connection.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB} WITH (FORCE)"))
            connection.execute(text(f"CREATE DATABASE {TEST_DB}"))
    except OperationalError as error:
        if os.environ.get("CI"):
            raise  # a missing database must fail CI, never skip it into a false green
        pytest.skip(f"no Postgres server: {error}")
    url = base.set(database=TEST_DB).render_as_string(hide_password=False)
    command.upgrade(alembic_config(url), "head")
    yield url
    admin.dispose()


@pytest.fixture
def engine(db_url):
    engine = create_engine(db_url)
    yield engine
    engine.dispose()
