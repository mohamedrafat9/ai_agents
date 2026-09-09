from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openrouter_model: str
    openrouter_api_key: str
    cerebras_model: str
    cerebras_api_key: str
    cerebras_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
@lru_cache
def get_settings() -> Settings:
    return Settings()