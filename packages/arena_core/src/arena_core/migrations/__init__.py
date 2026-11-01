"""Alembic migrations. SQL lives in sql/ so it can be reviewed and compared with docs/08a."""

import pathlib

SQL_DIR = pathlib.Path(__file__).parent / "sql"


def run_script(sql: str) -> None:
    """Run a multi-statement script exactly as written, with no parameter handling."""
    from alembic import op

    op.get_bind().connection.driver_connection.execute(sql)  # type: ignore[union-attr]
