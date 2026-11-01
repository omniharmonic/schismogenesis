"""Settings, read from the environment and .env."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ARENA_", env_file=".env", extra="ignore")

    database_url: str
    profile: str = "cloud-dev"

    @field_validator("database_url")
    @classmethod
    def use_psycopg_driver(cls, value: str) -> str:
        return value.replace("postgresql://", "postgresql+psycopg://", 1)
