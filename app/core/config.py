from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

SQLITE_PREFIX = "sqlite:///"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    app_name: str = "GrandLog"
    database_url: str = f"{SQLITE_PREFIX}./grandlog.db"

    @field_validator("database_url")
    @classmethod
    def resolve_sqlite_path(cls, value: str) -> str:
        # Anchor relative SQLite paths to the project root, not the CWD.
        if not value.startswith(SQLITE_PREFIX):
            return value

        path = value.removeprefix(SQLITE_PREFIX)

        if path == ":memory:" or Path(path).is_absolute():
            return value

        return f"{SQLITE_PREFIX}{(BASE_DIR / path).resolve().as_posix()}"


settings = Settings()
