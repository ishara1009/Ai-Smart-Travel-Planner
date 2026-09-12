from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import DEFAULT_LLM_MODEL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    app_name: str = "AI Smart Travel Planner"
    environment: str = "development"
    app_debug: bool = False
    api_v1_prefix: str = "/api/v1"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "ai_travel_planner"
    jwt_secret_key: str = Field(default="change-me-in-production", min_length=16)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    cors_origins: str = "http://localhost:5173"
    openai_api_key: str = ""
    openai_model: str = DEFAULT_LLM_MODEL
    tavily_api_key: str = ""
    weatherstack_api_key: str = ""
    external_api_timeout_seconds: float = 15.0

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if self.is_production and self.jwt_secret_key == "change-me-in-production":
            raise ValueError("JWT_SECRET_KEY must be configured in production")
        return self

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
