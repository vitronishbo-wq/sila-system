from pathlib import Path
from typing import List, Optional, Union
from functools import lru_cache
import json
from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    PROJECT_NAME: str = "SILA-System"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "SILA System - Centralized Configuration"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    ADMIN_EMAIL: str = "admin.nacional@sila.gov.ao"
    ADMIN_PASSWORD: str = "Angola2025!"

    SECRET_KEY: str = "4933c102ad45e5ccb82c9bd533bba82edb77f1eb13205755d675b30ca1d84e67"
    AUTH_SECRET_KEY: str = "default-secret"
    ALGORITHM: str = "HS256"
    # 90 dias em minutos (90 * 24 * 60 = 129600)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 129600
    # Refresh token também ajustado para 90 dias
    REFRESH_TOKEN_EXPIRE_DAYS: int = 90
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_HASH_ROUNDS: int = 12
    SESSION_COOKIE_SECURE: bool = False

    # PostgreSQL
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "sila_user"
    POSTGRES_PASSWORD: str = "Trumanmarcelo_1983"
    POSTGRES_DB: str = "sila_db"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: str = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db"
    DATABASE_ECHO: bool = True
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis & Cache
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_PASSWORD: Optional[str] = None
    REDIS_MAX_CONNECTIONS: int = 20
    CACHE_BACKEND: str = "redis"
    CACHE_TTL_SECONDS: int = 3600
    CELERY_BROKER_URL: str = "redis://redis:6379/0"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    # Integrações
    BNA_API_KEY: str = "your-bna-api-key"
    BNA_API_URL: str = "https://api.bna.ao"
    BNA_TIMEOUT: int = 30
    PAYMENT_WEBHOOK_SECRET: str = "whsec_test123"

    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    SMTP_FROM: str = "no-reply@sila.ao"

    # Storage
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    UPLOAD_PATH: str = "uploads"
    UPLOAD_DIR: str = "/app/uploads"
    ALLOWED_EXTENSIONS: Union[List[str], str] = ["jpg", "jpeg", "png", "pdf", "docx"]
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB

    # Monitoring & Features
    LOG_LEVEL: str = "INFO"
    PROMETHEUS_ENABLED: bool = True
    FEATURE_MONITORING: bool = True
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, v: Union[str, bool]) -> bool:
        if isinstance(v, str):
            return v.strip().lower() in ('true', '1', 'yes')
        return v

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            try:
                # Try to parse as JSON
                return json.loads(v)
            except (json.JSONDecodeError, ValueError):
                # Fallback to comma-separated
                return [x.strip() for x in v.split(",")]
        return v

    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def assemble_allowed_extensions(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v

    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return settings
