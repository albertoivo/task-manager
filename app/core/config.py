from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    redis_url: str = "redis://localhost"

settings = Settings()
