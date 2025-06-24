import os
from enum import Enum

from pydantic import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    redis_url: str = "redis://localhost"
    environment: Environment = os.getenv(
        "ENVIRONMENT", Environment.DEVELOPMENT.value
    ).lower()
    debug: bool = True

    class Config:
        env_file = ".env"


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
