"""
App settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # PostgreSQL
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_host: str = Field("db", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")

    # SQLite in-memory URL for tests
    test_database_url: str = "sqlite+pysqlite:///:memory:"

    @property
    def database_url(self) -> str:
        """Manual creation of db url"""
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def test_db_url(self) -> str:
        """Returns the in-memory SQLite DB URL for testing."""
        return self.test_database_url

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate a global settings object
settings = Settings()
