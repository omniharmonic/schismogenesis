"""Settings, read from the environment and .env."""

import pathlib

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ARENA_", env_file=".env", extra="ignore")

    database_url: str
    profile: str = "cloud-dev"
    source_dir: pathlib.Path = pathlib.Path("data/sources")

    @field_validator("database_url")
    @classmethod
    def use_psycopg_driver(cls, value: str) -> str:
        return value.replace("postgresql://", "postgresql+psycopg://", 1)


def load_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]  # values come from the environment
