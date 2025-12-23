"""
App settings
"""

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):

    # === Environment ===
    ENV: str = Field(default="dev")
    # === Database ===
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLITE_TEST_DATABASE_URI: str = "sqlite:///test.db"

    @property
    def DATABASE_URL(self) -> str:
        if self.ENV == "test":
            return self.SQLITE_TEST_DATABASE_URI
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"

# Instantiate a global settings object


@lru_cache
def get_settings() -> Settings:
    return Settings()
