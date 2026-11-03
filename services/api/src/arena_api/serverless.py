"""Entry point for serverless hosting (Vercel). Each request may land on a fresh instance, so
database connections are opened per use and closed straight after (Neon's pooler does the pooling).
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from arena_api.app import Config, create_app

url = os.environ["ARENA_DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://", 1)
engine = create_engine(url, poolclass=NullPool)
app = create_app(engine, config=Config.from_env())
