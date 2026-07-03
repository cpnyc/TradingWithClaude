from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    SCHWAB_APP_KEY: str = ""
    SCHWAB_APP_SECRET: str = ""
    SCHWAB_CALLBACK_URL: str = "https://127.0.0.1:8182"
    SCHWAB_TOKEN_PATH: str = "data/schwab_token.json"

    @property
    def token_path(self) -> Path:
        p = Path(self.SCHWAB_TOKEN_PATH)
        if p.is_absolute():
            return p
        return (Path(__file__).parent / p).resolve()


settings = Settings()
