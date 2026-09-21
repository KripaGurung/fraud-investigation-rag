from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[5]


class Settings(BaseSettings):
    app_name: str = "Financial Fraud Investigation RAG"
    environment: str = "development"
    database_url: str
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6"

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()