"""Database engine."""

from sqlalchemy import Engine, create_engine

from arena_core.config import load_settings


def get_engine(url: str | None = None) -> Engine:
    # pre-ping: a pooled connection the server closed (restart, idle timeout) is replaced, not used
    return create_engine(url or load_settings().database_url, pool_pre_ping=True)
