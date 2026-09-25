from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    trueforge_base_url: str = "http://localhost:8790"
    trueforge_agent_name: str = "greenlight"
    greenlight_api_key: str
    frontend_origin: str
    github_bot_token: str
    github_bot_login: str = "greenlight-agent"
    ledger_path: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
