"""Database engine."""

from sqlalchemy import Engine, create_engine

from arena_core.config import Settings


def get_engine(url: str | None = None) -> Engine:
    return create_engine(url or Settings().database_url)
