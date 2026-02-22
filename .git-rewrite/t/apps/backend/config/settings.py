"""
Centralized Settings Configuration using Pydantic V2

This module provides a robust, type-safe configuration management system
for the SILA backend using Pydantic V2 settings with validation.
"""

import os
import secrets
from pathlib import Path  # ← Adicionado import faltante
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    """
    Centralized configuration settings for SILA system.

    Uses Pydantic V2 for type validation, environment variable loading,
    and configuration management with proper defaults and validation.
    """

    # =========================
    # PYDANTIC V2 CONFIGURATION
    # =========================

    # Determinar qual arquivo .env carregar baseado no ambiente
    @staticmethod
    def get_env_file():
        """
        Determina qual arquivo .env carregar baseado no ambiente.
        Prioridade: .env.{ambiente} > .env.template > .env
        """
        env = os.getenv("ENVIRONMENT", "development").lower()
        # Path(__file__) = .../sila-system/apps/backend/config/settings.py
        # .parent = .../sila-system/apps/backend/config
        # .parent = .../sila-system/apps/backend
        # .parent = .../sila-system/apps
        # .parent = .../sila-system (ROOT)
        base_dir = Path(__file__).parent.parent.parent.parent

        # Prioridade de busca
        env_files = [
            base_dir / f".env.{env}",
            base_dir / ".env.template",
            base_dir / ".env",
        ]

        for env_path in env_files:
            if env_path.exists():
                print(f"[OK] Carregando configuracao de: {env_path}")
                return str(env_path)

        print("[WARNING] Nenhum arquivo .env encontrado, usando defaults")
        return None

    model_config = SettingsConfigDict(
        env_file=get_env_file.__func__(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
        validate_assignment=True,
        env_nested_delimiter="__",
        env_priority="env",
    )

    # =========================
    # PROJECT INFORMATION
    # =========================
    PROJECT_NAME: str = Field(default="SILA-System", description="Project name")
    VERSION: str = Field(default="1.0.0", description="Application version")
    DESCRIPTION: str = Field(
        default="Sistema Integrado Local de Administração",
        description="Application description",
    )
    SILA_SYSTEM_ID: str = Field(
        default="sila-2025-marcelo-truman", description="Unique system identifier"
    )

    # =========================
    # API CONFIGURATION
    # =========================
    API_V1_STR: str = Field(default="/api/v1", description="API v1 prefix")
    API_V2_STR: str = Field(default="/api/v2", description="API v2 prefix")

    # CORS Configuration (supports both JSON list and comma-separated string)
    ALLOWED_ORIGINS: Union[List[str], str] = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000",
        description="CORS allowed origins (comma-separated string or JSON list)",
    )

    ALLOWED_METHODS: Union[List[str], str] = Field(
        default="GET,POST,PUT,DELETE,OPTIONS,PATCH",
        description="CORS allowed methods (comma-separated string or JSON list)",
    )

    ALLOWED_HEADERS: Union[List[str], str] = Field(
        default="*",
        description="CORS allowed headers (comma-separated string or JSON list)",
    )

    # CORS Enabled flag
    CORS_ENABLED: bool = Field(default=True, description="Enable CORS middleware")

    # =========================
    # ENVIRONMENT CONFIGURATION
    # =========================
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment (development, staging, production)",
    )

    DEBUG: bool = Field(default=True, description="Debug mode")

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        valid_envs = ["development", "staging", "production", "test"]
        if v.lower() not in valid_envs:
            raise ValueError(f"Environment must be one of: {valid_envs}")
        return v.lower()

    @field_validator(
        "ALLOWED_ORIGINS", "ALLOWED_METHODS", "ALLOWED_HEADERS", mode="before"
    )
    @classmethod
    def parse_comma_separated(cls, v):
        """Parse comma-separated strings into lists."""
        if isinstance(v, str):
            # Handle JSON array format
            if v.startswith("[") and v.endswith("]"):
                import json

                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    # Fallback to comma-separated parsing
                    pass

            # Handle comma-separated string format
            if v == "*":
                return ["*"]
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    # =========================
    # DATABASE CONFIGURATION
    # =========================
    POSTGRES_USER: str = Field(default="sila_prod", description="PostgreSQL user")
    POSTGRES_PASSWORD: str = Field(
        default="change_me_immediately", description="PostgreSQL password"
    )
    POSTGRES_DB: str = Field(default="sila_db", description="PostgreSQL database name")
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    DATABASE_ECHO: bool = Field(default=False, description="Enable SQL query logging")

    # Database Pool Settings
    DATABASE_POOL_SIZE: int = Field(
        default=20, description="Database connection pool size"
    )
    DATABASE_MAX_OVERFLOW: int = Field(
        default=40, description="Database max overflow connections"
    )

    # Fallback admin flag
    ALLOW_FALLBACK_ADMIN: bool = Field(
        default=False, description="Allow fallback admin authentication"
    )

    # Fallback admin password (only used in development)
    FALLBACK_ADMIN_PASSWORD: str = Field(
        default="adm123", description="Fallback admin password for development"
    )

    # Database URLs (computed)
    @property
    def DATABASE_URL(self) -> str:
        """Synchronous PostgreSQL database URL."""
        user_encoded = quote_plus(self.POSTGRES_USER)
        password_encoded = quote_plus(self.POSTGRES_PASSWORD)
        return (
            f"postgresql://{user_encoded}:{password_encoded}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Asynchronous PostgreSQL database URL."""
        user_encoded = quote_plus(self.POSTGRES_USER)
        password_encoded = quote_plus(self.POSTGRES_PASSWORD)
        return (
            f"postgresql+asyncpg://{user_encoded}:{password_encoded}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def TEST_DATABASE_URL(self) -> str:
        """Test database URL."""
        user_encoded = quote_plus(self.POSTGRES_USER)
        password_encoded = quote_plus(self.POSTGRES_PASSWORD)
        return (
            f"postgresql://{user_encoded}:{password_encoded}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/sila_test"
        )

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """Alias for DATABASE_URL for backward compatibility."""
        return self.DATABASE_URL

    # =========================
    # SECURITY CONFIGURATION
    # =========================
    SECRET_KEY: str = Field(
        default="change_me_immediately", description="Secret key for JWT tokens"
    )

    AUTH_SECRET_KEY: str = Field(
        default="change_me_immediately", description="Secret key for authentication"
    )

    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15, description="Access token expiration"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=1, description="Refresh token expiration"
    )
    PASSWORD_HASH_ALGORITHM: str = Field(
        default="bcrypt", description="Password hash algorithm"
    )
    PASSWORD_MIN_LENGTH: int = Field(default=12, description="Minimum password length")

    # Session settings
    SESSION_TIMEOUT_MINUTES: int = Field(default=60, description="Session timeout")
    SESSION_COOKIE_SECURE: bool = Field(
        default=False, description="Secure session cookies"
    )

    # =========================
    # REDIS AND CACHE CONFIGURATION
    # =========================
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis URL")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    REDIS_MAX_CONNECTIONS: int = Field(default=50, description="Redis max connections")

    # Cache settings
    CACHE_BACKEND: str = Field(default="redis", description="Cache backend")
    CACHE_TTL_SECONDS: int = Field(default=3600, description="Cache TTL in seconds")

    # Celery configuration
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1", description="Celery broker URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/2", description="Celery result backend"
    )

    # =========================
    # CORS CONFIGURATION
    # =========================
    BACKEND_CORS_ORIGINS: Union[List[str], str] = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000",
        description="CORS allowed origins (comma-separated string or JSON list)",
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        """Parse origins from string or list."""
        if isinstance(v, str):
            # Handle JSON string format
            if v.startswith("[") and v.endswith("]"):
                import json

                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    # Fallback: split by comma
                    return [
                        origin.strip().strip('"')
                        for origin in v.split(",")
                        if origin.strip()
                    ]
            # Handle comma-separated string
            return [
                origin.strip().strip('"') for origin in v.split(",") if origin.strip()
            ]
        return v

    ALLOWED_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        description="CORS allowed methods",
    )
    ALLOWED_HEADERS: List[str] = Field(
        default=["*"], description="CORS allowed headers"
    )

    # =========================
    # LOGGING CONFIGURATION
    # =========================
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    PYTHONPATH: str = Field(default="backend", description="Python path")
    PYTHONUNBUFFERED: int = Field(default=1, description="Python unbuffered")
    PYTHONDONTWRITEBYTECODE: int = Field(default=1, description="Don't write bytecode")

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()

    # =========================
    # MONITORING AND TELEMETRY
    # =========================
    TELEMETRY_ENABLED: bool = Field(default=True, description="Enable telemetry")

    # Prometheus configuration
    PROMETHEUS_ENABLED: bool = Field(
        default=True, description="Enable Prometheus metrics"
    )
    PROMETHEUS_PORT: int = Field(default=9090, description="Prometheus port")
    PROMETHEUS_GATEWAY: str = Field(
        default="http://localhost:9090", description="Prometheus gateway URL"
    )

    # Jaeger tracing
    JAEGER_ENABLED: bool = Field(default=True, description="Enable Jaeger tracing")
    JAEGER_ENDPOINT: str = Field(
        default="http://localhost:14268", description="Jaeger endpoint"
    )
    JAEGER_SERVICE_NAME: str = Field(
        default="sila-backend", description="Jaeger service name"
    )

    # Grafana
    GRAFANA_ENABLED: bool = Field(default=True, description="Enable Grafana")
    GRAFANA_URL: str = Field(default="http://localhost:3000", description="Grafana URL")
    GRAFANA_USERNAME: str = Field(default="admin", description="Grafana username")
    GRAFANA_PASSWORD: str = Field(default="admin", description="Grafana password")

    # =========================
    # MINIO CONFIGURATION
    # =========================
    STORAGE_BACKEND: str = Field(default="minio", description="Storage backend")
    MINIO_ENDPOINT: str = Field(default="localhost:9000", description="MinIO endpoint")
    MINIO_ACCESS_KEY: str = Field(default="minioadmin", description="MinIO access key")
    MINIO_SECRET_KEY: str = Field(default="minioadmin", description="MinIO secret key")
    MINIO_SECURE: bool = Field(default=False, description="Use HTTPS for MinIO")
    MINIO_BUCKET_NAME: str = Field(
        default="sila-storage", description="MinIO bucket name"
    )

    # =========================
    # BNA INTEGRATION CONFIGURATION
    # =========================
    BNA_API_KEY: str = Field(default="your-bna-api-key", description="BNA API key")
    BNA_API_URL: str = Field(default="https://api.bna.ao", description="BNA API URL")
    BNA_ENVIRONMENT: str = Field(default="sandbox", description="BNA environment")
    BNA_TIMEOUT: int = Field(default=30, description="BNA API timeout")
    MUNICIPALITY_ACCOUNT: str = Field(
        default="AO06004000000000000012345", description="Municipality account number"
    )

    @field_validator("BNA_ENVIRONMENT")
    @classmethod
    def validate_bna_environment(cls, v: str) -> str:
        """Validate BNA environment."""
        valid_envs = ["sandbox", "production", "development"]
        if v.lower() not in valid_envs:
            raise ValueError(f"BNA environment must be one of: {valid_envs}")
        return v.lower()

    # =========================
    # PAYMENT CONFIGURATION
    # =========================
    DEFAULT_CURRENCY: str = Field(default="AOA", description="Default currency")
    PAYMENT_TIMEOUT: int = Field(default=300, description="Payment timeout in seconds")

    # =========================
    # FILE UPLOAD CONFIGURATION
    # =========================
    MAX_UPLOAD_SIZE: int = Field(
        default=52428800, description="Max upload size in bytes"
    )
    ALLOWED_EXTENSIONS: Union[List[str], str] = Field(
        default="jpg,jpeg,png,pdf,doc,docx,txt",
        description="Allowed file extensions (comma-separated string or JSON list)",
    )
    UPLOAD_PATH: str = Field(default="./uploads", description="Upload directory path")

    # =========================
    # RATE LIMITING CONFIGURATION
    # =========================
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_PER_MINUTE: int = Field(default=120, description="Rate limit per minute")
    RATE_LIMIT_BURST: int = Field(default=20, description="Rate limit burst")
    RATE_LIMIT_STORAGE: str = Field(
        default="redis", description="Rate limit storage backend"
    )

    # =========================
    # FEATURE FLAGS
    # =========================
    FEATURE_MONITORING: bool = Field(
        default=True, description="Enable monitoring features"
    )
    FEATURE_BACKUP: bool = Field(default=True, description="Enable backup features")
    FEATURE_AUTO_HEALER: bool = Field(
        default=True, description="Enable auto-healer features"
    )
    FEATURE_AUDIT_LOG: bool = Field(default=True, description="Enable audit logging")
    FEATURE_EMAIL_NOTIFICATIONS: bool = Field(
        default=True, description="Enable email notifications"
    )
    FEATURE_FILE_STORAGE: bool = Field(default=True, description="Enable file storage")

    # =========================
    # SECURITY HEADERS
    # =========================
    SECURITY_HEADERS_ENABLED: bool = Field(
        default=True, description="Enable security headers"
    )
    SECURITY_HSTS_MAX_AGE: int = Field(default=31536000, description="HSTS max age")
    SECURITY_CONTENT_TYPE_NOSNIFF: bool = Field(
        default=True, description="Content type nosniff"
    )
    SECURITY_X_FRAME_OPTIONS: str = Field(default="DENY", description="X-Frame-Options")
    SECURITY_CONTENT_SECURITY_POLICY: str = Field(
        default="default-src 'self'", description="Content Security Policy"
    )

    # =========================
    # FRONTEND CONFIGURATION
    # =========================
    REACT_APP_API_URL: str = Field(
        default="http://localhost:8000", description="React app API URL"
    )
    REACT_APP_ENVIRONMENT: str = Field(
        default="development", description="React app environment"
    )

    # =========================
    # EMAIL CONFIGURATION
    # =========================
    SMTP_HOST: str = Field(default="smtp.gmail.com", description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USERNAME: Optional[str] = Field(default=None, description="SMTP username")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="SMTP password")
    SMTP_USE_TLS: bool = Field(default=True, description="Use TLS for SMTP")
    SMTP_USE_SSL: bool = Field(default=False, description="Use SSL for SMTP")

    # =========================
    # EXTERNAL APIS CONFIGURATION
    # =========================
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    STRIPE_SECRET_KEY: Optional[str] = Field(
        default=None, description="Stripe secret key"
    )
    STRIPE_PUBLISHABLE_KEY: Optional[str] = Field(
        default=None, description="Stripe publishable key"
    )

    # =========================
    # ANALYTICS CONFIGURATION
    # =========================
    ANALYTICS_ID: Optional[str] = Field(
        default=None, description="Analytics tracking ID"
    )

    # =========================
    # ERROR TRACKING
    # =========================
    SENTRY_DSN: Optional[str] = Field(
        default=None, description="Sentry DSN for error tracking"
    )
    REACT_APP_SENTRY_DSN: Optional[str] = Field(
        default=None, description="React Sentry DSN"
    )

    # =========================
    # BACKUP CONFIGURATION
    # =========================
    BACKUP_ENABLED: bool = Field(default=True, description="Enable backup system")
    BACKUP_RETENTION_DAYS: int = Field(
        default=30, description="Backup retention in days"
    )
    BACKUP_SCHEDULE: str = Field(
        default="0 2 * * *", description="Backup schedule (cron)"
    )

    # =========================
    # SSL CONFIGURATION
    # =========================
    SSL_CERT_PATH: str = Field(
        default="./devops/ssl/cert.pem", description="SSL certificate path"
    )
    SSL_KEY_PATH: str = Field(
        default="./devops/ssl/key.pem", description="SSL private key path"
    )
    SSL_ENABLED: bool = Field(default=False, description="Enable SSL")

    # =========================
    # VALIDATION METHODS
    # =========================

    @model_validator(mode="after")
    def validate_security_settings(self) -> "Settings":
        """Validate security settings based on environment."""
        if self.ENVIRONMENT == "production":
            if self.SECRET_KEY == "supersecretkey_2025_sila":
                raise ValueError("SECRET_KEY must be changed in production")
            if not self.SESSION_COOKIE_SECURE:
                raise ValueError("SESSION_COOKIE_SECURE must be True in production")
            if self.DEBUG:
                raise ValueError("DEBUG must be False in production")
        return self

    def get_database_info(self) -> Dict[str, Any]:
        """Get database information without sensitive data."""
        return {
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "environment": self.ENVIRONMENT,
            "echo": self.DATABASE_ECHO,
        }

    def get_redis_info(self) -> Dict[str, Any]:
        """Get Redis information without sensitive data."""
        return {
            "url": self.REDIS_URL,
            "db": 0,
        }

    def get_security_info(self) -> Dict[str, Any]:
        """Get security configuration info."""
        return {
            "algorithm": self.ALGORITHM,
            "access_token_expire_minutes": self.ACCESS_TOKEN_EXPIRE_MINUTES,
            "refresh_token_expire_days": self.REFRESH_TOKEN_EXPIRE_DAYS,
            "session_timeout_minutes": self.SESSION_TIMEOUT_MINUTES,
            "environment": self.ENVIRONMENT,
        }

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"


# =========================
# GLOBAL SETTINGS INSTANCE
# =========================


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Uses LRU cache to ensure settings are loaded only once
    and reused throughout the application lifecycle.
    """
    return Settings()


# Create global settings instance
settings = get_settings()


# =========================
# SETTINGS VALIDATION
# =========================


def validate_settings() -> bool:
    """
    Validate all critical settings.

    Returns:
        bool: True if all critical settings are valid

    Raises:
        ValueError: If critical settings are missing or invalid
    """
    critical_settings = [
        ("DATABASE_URL", settings.DATABASE_URL),
        ("SECRET_KEY", settings.SECRET_KEY),
        ("ENVIRONMENT", settings.ENVIRONMENT),
    ]

    for name, value in critical_settings:
        if not value:
            raise ValueError(f"Critical setting missing: {name}")

    return True


def print_settings_summary() -> None:
    """Print a summary of current settings (without sensitive data)."""
    print("=" * 80)
    print("SILA SYSTEM SETTINGS SUMMARY")
    print("=" * 80)

    print(f"Project: {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug: {settings.DEBUG}")
    print(f"System ID: {settings.SILA_SYSTEM_ID}")

    print("\n[Database]")
    db_info = settings.get_database_info()
    for key, value in db_info.items():
        print(f"  {key}: {value}")

    print("\n[Redis]")
    redis_info = settings.get_redis_info()
    for key, value in redis_info.items():
        print(f"  {key}: {value}")

    print("\n[Security]")
    security_info = settings.get_security_info()
    for key, value in security_info.items():
        print(f"  {key}: {value}")

    print("\n[Features]")
    features = [
        ("Monitoring", settings.FEATURE_MONITORING),
        ("Backup", settings.FEATURE_BACKUP),
        ("Auto-healer", settings.FEATURE_AUTO_HEALER),
        ("Rate Limiting", True),
        ("Telemetry", settings.TELEMETRY_ENABLED),
    ]

    for name, enabled in features:
        status = "✅" if enabled else "❌"
        print(f"  {status} {name}: {enabled}")

    print("\n[Services]")
    services = [
        ("MinIO", settings.MINIO_ENDPOINT),
        ("BNA API", settings.BNA_API_URL),
        ("Prometheus", settings.PROMETHEUS_GATEWAY),
    ]

    for name, endpoint in services:
        print(f"  {name}: {endpoint}")

    print("=" * 80)


# Auto-validate settings when module is imported
if __name__ == "__main__":
    try:
        validate_settings()
        print_settings_summary()
        print("✅ Settings validated successfully!")
    except ValueError as e:
        print(f"❌ Settings validation failed: {e}")
        raise
