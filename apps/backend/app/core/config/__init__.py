import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "4933c102ad45e5ccb82c9bd533bba82edb77f1eb13205755d675b30ca1d84e67"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
