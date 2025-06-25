from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Task Manager API"
    redis_url: str = "redis://localhost"
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = True


settings = Settings()


def is_production() -> bool:
    return settings.environment == Environment.PRODUCTION


def is_testing() -> bool:
    return settings.environment == Environment.TESTING


def is_development() -> bool:
    return settings.environment == Environment.DEVELOPMENT


def is_staging() -> bool:
    return settings.environment == Environment.STAGING


def is_debug() -> bool:
    return settings.debug and not is_production()
