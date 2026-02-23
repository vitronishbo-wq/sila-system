"""
Configurações do módulo IAM
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/sila_db")
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-min-32-chars")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    JWT_ISSUER: str = os.getenv("JWT_ISSUER", "sila.gov.ao")
    
    # Password Policy
    PASSWORD_MIN_LENGTH: int = int(os.getenv("PASSWORD_MIN_LENGTH", "8"))
    PASSWORD_REQUIRE_UPPERCASE: bool = os.getenv("PASSWORD_REQUIRE_UPPERCASE", "true").lower() == "true"
    PASSWORD_REQUIRE_LOWERCASE: bool = os.getenv("PASSWORD_REQUIRE_LOWERCASE", "true").lower() == "true"
    PASSWORD_REQUIRE_DIGITS: bool = os.getenv("PASSWORD_REQUIRE_DIGITS", "true").lower() == "true"
    PASSWORD_REQUIRE_SPECIAL: bool = os.getenv("PASSWORD_REQUIRE_SPECIAL", "true").lower() == "true"
    
    # MFA
    MFA_REQUIRED: bool = os.getenv("MFA_REQUIRED", "false").lower() == "true"
    MFA_ISSUER: str = os.getenv("MFA_ISSUER", "SILA")
    
    # Redis (para blacklist e cache)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "false").lower() == "true"
    
    # FUC Integration
    FUC_API_URL: Optional[str] = os.getenv("FUC_API_URL")
    FUC_API_KEY: Optional[str] = os.getenv("FUC_API_KEY")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    AUDIT_LOG_ENABLED: bool = os.getenv("AUDIT_LOG_ENABLED", "true").lower() == "true"
    
    # Cache
    PERMISSION_CACHE_TTL: int = int(os.getenv("PERMISSION_CACHE_TTL", "300"))  # 5 minutos
    
    model_config = ConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore"  # Permite campos extras do .env sem causar erro
    )


# Singleton
settings = Settings()
