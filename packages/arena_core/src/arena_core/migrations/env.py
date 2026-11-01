"""Alembic environment. The database URL comes from arena_core settings."""

from alembic import context
from pgvector.sqlalchemy import HALFVEC, Vector
from sqlalchemy import create_engine, pool

from arena_core.config import load_settings


def render_item(type_, obj, autogen_context):
    if type_ == "type" and isinstance(obj, HALFVEC | Vector):
        autogen_context.imports.add("from pgvector.sqlalchemy import HALFVEC, Vector")
        return repr(obj)
    return False


url = context.config.get_main_option("sqlalchemy.url") or load_settings().database_url
engine = create_engine(url, poolclass=pool.NullPool)
with engine.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=None,
        render_item=render_item,
        transaction_per_migration=True,
    )
    with context.begin_transaction():
        context.run_migrations()
