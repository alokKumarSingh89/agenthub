from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    app_name: str = "AgentHub API"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_url: str = Field(
        default="postgresql+asyncpg://agenthub:agenthub@localhost:5432/agenthub",
    )

    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
