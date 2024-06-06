from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    MONGO_URL: str
    MONGO_MAX_CONN: int
    MONGO_MIN_CONN: int
    LOG_LEVEL: int

    PROFILE: bool = False


settings = AppConfig()