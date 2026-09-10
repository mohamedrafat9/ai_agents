from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    default_provider: str

    openai_api_key: str | None = None
    openai_model: str 

    xai_api_key: str | None = None
    xai_model: str 

    google_api_key: str | None = None
    google_model: str

    openrouter_api_key: str | None = None
    openrouter_model: str 

    llm_temperature: float = 0.6
    llm_max_tokens: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()