from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AstroData Lab API"
    app_env: str = "development"
    api_prefix: str = "/api"

    mongodb_uri: str = ""
    mongodb_database: str = "astrodata_lab"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    embedding_model: str = "all-MiniLM-L6-v2"

    nasa_api_key: str = Field(default="DEMO_KEY", repr=False)
    apod_seed_limit: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def mongodb_configured(self) -> bool:
        return bool(self.mongodb_uri.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
