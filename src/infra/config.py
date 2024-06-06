from typing import Optional

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    DB_URL: Optional[str] = None
    LOG_LEVEL: int = 20
    PROFILE: bool = False


settings = AppConfig()
