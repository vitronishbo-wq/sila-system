"""
Configuration validation utilities for SILA system.

Provides comprehensive validation of configuration settings,
environment variables, and system requirements.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from .settings import settings


class ConfigurationError(Exception):
    """Raised when configuration validation fails."""

    pass


class SettingsValidator:
    """Comprehensive settings validator for SILA system."""

    def __init__(self, settings_instance: Any = None):
        """Initialize validator with settings instance."""
        self.settings = settings_instance or settings
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate all configuration settings.

        Returns:
            Tuple[bool, List[str], List[str]]:
                (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        # Run all validations
        self._validate_database_settings()
        self._validate_security_settings()
        self._validate_redis_settings()
        self._validate_external_services()
        self._validate_file_settings()
        self._validate_monitoring_settings()
        self._validate_environment_settings()
        self._validate_feature_flags()

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def _validate_database_settings(self) -> None:
        """Validate database configuration."""
        try:
            # Check database URL format
            parsed = urlparse(self.settings.DATABASE_URL)
            if parsed.scheme not in ["postgresql", "postgresql+asyncpg"]:
                self.errors.append("DATABASE_URL must use PostgreSQL protocol")

            if not parsed.hostname:
                self.errors.append("DATABASE_URL missing host")

            if not parsed.username:
                self.errors.append("DATABASE_URL missing username")

            if not parsed.path or parsed.path == "/":
                self.errors.append("DATABASE_URL missing database name")

            # Check for default passwords in production
            if self.settings.is_production():
                if self.settings.POSTGRES_PASSWORD in [
                    "change_me_immediately",
                    "postgres",
                    "password",
                ]:
                    self.errors.append(
                        "POSTGRES_PASSWORD must be changed in production"
                    )

            # Validate pool settings
            if self.settings.DATABASE_POOL_SIZE <= 0:
                self.errors.append("DATABASE_POOL_SIZE must be positive")

            if self.settings.DATABASE_MAX_OVERFLOW < 0:
                self.errors.append("DATABASE_MAX_OVERFLOW cannot be negative")

        except Exception as e:
            self.errors.append(f"Database URL validation failed: {str(e)}")

    def _validate_security_settings(self) -> None:
        """Validate security configuration."""
        # Secret key validation
        if len(self.settings.SECRET_KEY) < 32:
            self.errors.append("SECRET_KEY must be at least 32 characters long")

        if self.settings.SECRET_KEY in ["change_me_immediately", "secret", "test"]:
            if self.settings.is_production():
                self.errors.append("SECRET_KEY must be changed in production")

        # Algorithm validation
        valid_algorithms = ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
        if self.settings.ALGORITHM not in valid_algorithms:
            self.errors.append(f"ALGORITHM must be one of: {valid_algorithms}")

        # Token expiration validation
        if self.settings.ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
            self.errors.append("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")

        if self.settings.REFRESH_TOKEN_EXPIRE_DAYS <= 0:
            self.errors.append("REFRESH_TOKEN_EXPIRE_DAYS must be positive")

        # Password settings validation
        if self.settings.PASSWORD_MIN_LENGTH < 8:
            self.warnings.append("PASSWORD_MIN_LENGTH should be at least 8 characters")

        if self.settings.PASSWORD_HASH_ROUNDS < 10:
            self.warnings.append(
                "PASSWORD_HASH_ROUNDS should be at least 10 for security"
            )

        # Session settings
        if self.settings.is_production() and not self.settings.SESSION_COOKIE_SECURE:
            self.errors.append("SESSION_COOKIE_SECURE must be True in production")

    def _validate_redis_settings(self) -> None:
        """Validate Redis configuration."""
        try:
            parsed = urlparse(self.settings.REDIS_URL)
            if parsed.scheme != "redis":
                self.errors.append("REDIS_URL must use redis:// protocol")

            if not parsed.hostname:
                self.errors.append("REDIS_URL missing host")

            if parsed.port and (parsed.port < 1 or parsed.port > 65535):
                self.errors.append("REDIS_URL port must be between 1 and 65535")

            # Validate connection settings
            if self.settings.REDIS_MAX_CONNECTIONS <= 0:
                self.errors.append("REDIS_MAX_CONNECTIONS must be positive")

            if self.settings.CACHE_TTL_SECONDS <= 0:
                self.errors.append("CACHE_TTL_SECONDS must be positive")

        except Exception as e:
            self.errors.append(f"Redis URL validation failed: {str(e)}")

    def _validate_external_services(self) -> None:
        """Validate external service configurations."""
        # BNA API validation
        if self.settings.BNA_API_KEY == "your-bna-api-key":
            if self.settings.FEATURE_FILE_STORAGE:
                self.warnings.append("BNA_API_KEY should be set for production use")

        try:
            parsed = urlparse(self.settings.BNA_API_URL)
            if parsed.scheme not in ["http", "https"]:
                self.errors.append("BNA_API_URL must use http or https protocol")

            if self.settings.BNA_TIMEOUT <= 0:
                self.errors.append("BNA_TIMEOUT must be positive")
        except Exception as e:
            self.errors.append(f"BNA_API_URL validation failed: {str(e)}")

        # Email validation
        if self.settings.SMTP_USERNAME and not self.settings.SMTP_PASSWORD:
            self.warnings.append("SMTP_USERNAME set but SMTP_PASSWORD missing")

        if self.settings.SMTP_PORT < 1 or self.settings.SMTP_PORT > 65535:
            self.errors.append("SMTP_PORT must be between 1 and 65535")

        # MinIO validation
        if (
            self.settings.MINIO_ACCESS_KEY == "minioadmin"
            and self.settings.is_production()
        ):
            self.errors.append("MINIO_ACCESS_KEY must be changed in production")

        if (
            self.settings.MINIO_SECRET_KEY == "minioadmin"
            and self.settings.is_production()
        ):
            self.errors.append("MINIO_SECRET_KEY must be changed in production")

    def _validate_file_settings(self) -> None:
        """Validate file upload and storage settings."""
        if self.settings.MAX_UPLOAD_SIZE <= 0:
            self.errors.append("MAX_UPLOAD_SIZE must be positive")

        if self.settings.MAX_UPLOAD_SIZE > 104857600:  # 100MB
            self.warnings.append("MAX_UPLOAD_SIZE is very large, consider reducing it")

        if not self.settings.ALLOWED_EXTENSIONS:
            self.errors.append("ALLOWED_EXTENSIONS cannot be empty")

        # Check upload directory
        if not os.path.exists(self.settings.UPLOAD_PATH):
            try:
                os.makedirs(self.settings.UPLOAD_PATH, exist_ok=True)
                self.warnings.append(
                    f"Created upload directory: {self.settings.UPLOAD_PATH}"
                )
            except Exception as e:
                self.errors.append(
                    f"Cannot create upload directory {self.settings.UPLOAD_PATH}: {str(e)}"
                )

    def _validate_monitoring_settings(self) -> None:
        """Validate monitoring and telemetry settings."""
        # Prometheus validation
        if self.settings.PROMETHEUS_ENABLED:
            if (
                self.settings.PROMETHEUS_PORT < 1
                or self.settings.PROMETHEUS_PORT > 65535
            ):
                self.errors.append("PROMETHEUS_PORT must be between 1 and 65535")

        # Jaeger validation
        if self.settings.JAEGER_ENABLED:
            try:
                parsed = urlparse(self.settings.JAEGER_ENDPOINT)
                if parsed.scheme not in ["http", "https"]:
                    self.errors.append(
                        "JAEGER_ENDPOINT must use http or https protocol"
                    )
            except Exception as e:
                self.errors.append(f"JAEGER_ENDPOINT validation failed: {str(e)}")

        # Grafana validation
        if self.settings.GRAFANA_ENABLED:
            try:
                parsed = urlparse(self.settings.GRAFANA_URL)
                if parsed.scheme not in ["http", "https"]:
                    self.errors.append("GRAFANA_URL must use http or https protocol")
            except Exception as e:
                self.errors.append(f"GRAFANA_URL validation failed: {str(e)}")

    def _validate_environment_settings(self) -> None:
        """Validate environment-specific settings."""
        if self.settings.is_production():
            # Production-specific validations
            if self.settings.DEBUG:
                self.errors.append("DEBUG must be False in production")

            if self.settings.LOG_LEVEL == "DEBUG":
                self.warnings.append(
                    "Consider using INFO or WARNING log level in production"
                )

            if self.settings.DATABASE_ECHO:
                self.warnings.append("DATABASE_ECHO should be False in production")

        elif self.settings.is_development():
            # Development-specific validations
            if not self.settings.DEBUG:
                self.warnings.append("DEBUG should be True in development")

        # Log level validation
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.settings.LOG_LEVEL not in valid_log_levels:
            self.errors.append(f"LOG_LEVEL must be one of: {valid_log_levels}")

    def _validate_feature_flags(self) -> None:
        """Validate feature flag configurations."""
        # Check for conflicting features
        if self.settings.FEATURE_EMAIL_NOTIFICATIONS:
            if not self.settings.SMTP_HOST:
                self.errors.append(
                    "SMTP_HOST must be set when FEATURE_EMAIL_NOTIFICATIONS is enabled"
                )

        if self.settings.FEATURE_FILE_STORAGE:
            if self.settings.STORAGE_BACKEND == "minio":
                if not self.settings.MINIO_ENDPOINT:
                    self.errors.append(
                        "MINIO_ENDPOINT must be set when using MinIO storage"
                    )

        # Rate limiting validation
        if self.settings.RATE_LIMIT_ENABLED:
            if self.settings.RATE_LIMIT_PER_MINUTE <= 0:
                self.errors.append(
                    "RATE_LIMIT_PER_MINUTE must be positive when rate limiting is enabled"
                )

            if self.settings.RATE_LIMIT_BURST <= 0:
                self.errors.append(
                    "RATE_LIMIT_BURST must be positive when rate limiting is enabled"
                )


def validate_configuration(
    settings_instance: Any = None,
) -> Tuple[bool, List[str], List[str]]:
    """
    Validate configuration settings.

    Args:
        settings_instance: Settings instance to validate (uses global if None)

    Returns:
        Tuple[bool, List[str], List[str]]: (is_valid, errors, warnings)
    """
    validator = SettingsValidator(settings_instance)
    return validator.validate_all()


def check_environment_variables() -> Dict[str, Any]:
    """
    Check environment variables and their status.

    Returns:
        Dict[str, Any]: Environment variable status report
    """
    env_vars = {
        # Database
        "POSTGRES_USER": settings.POSTGRES_USER,
        "POSTGRES_PASSWORD": settings.POSTGRES_PASSWORD,
        "POSTGRES_DB": settings.POSTGRES_DB,
        "POSTGRES_HOST": settings.POSTGRES_HOST,
        "POSTGRES_PORT": settings.POSTGRES_PORT,
        # Security
        "SECRET_KEY": settings.SECRET_KEY,
        "AUTH_SECRET_KEY": settings.AUTH_SECRET_KEY,
        # Environment
        "ENVIRONMENT": settings.ENVIRONMENT,
        "DEBUG": settings.DEBUG,
        # Redis
        "REDIS_URL": settings.REDIS_URL,
        "REDIS_PASSWORD": settings.REDIS_PASSWORD,
        # External services
        "BNA_API_KEY": settings.BNA_API_KEY,
        "SMTP_USERNAME": settings.SMTP_USERNAME,
        "SMTP_PASSWORD": settings.SMTP_PASSWORD,
        # Storage
        "MINIO_ACCESS_KEY": settings.MINIO_ACCESS_KEY,
        "MINIO_SECRET_KEY": settings.MINIO_SECRET_KEY,
    }

    status = {
        "total": len(env_vars),
        "set": sum(1 for v in env_vars.values() if v is not None),
        "missing": sum(1 for v in env_vars.values() if v is None),
        "details": {},
    }

    for name, value in env_vars.items():
        status["details"][name] = {
            "set": value is not None,
            "value": "***" if value and "PASSWORD" in name or "KEY" in name else value,
        }

    return status


def print_validation_report() -> None:
    """Print a comprehensive validation report."""
    print("=" * 80)
    print("SILA SYSTEM CONFIGURATION VALIDATION REPORT")
    print("=" * 80)

    # Validate settings
    is_valid, errors, warnings = validate_configuration()

    print(f"\n📊 VALIDATION SUMMARY")
    print(f"Status: {'✅ VALID' if is_valid else '❌ INVALID'}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    # Print errors
    if errors:
        print(f"\n❌ ERRORS ({len(errors)})")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")

    # Print warnings
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)})")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")

    # Environment variables status
    print(f"\n🔧 ENVIRONMENT VARIABLES")
    env_status = check_environment_variables()
    print(f"Total variables: {env_status['total']}")
    print(f"Set: {env_status['set']}")
    print(f"Missing: {env_status['missing']}")

    if env_status["missing"] > 0:
        print(f"\nMissing variables:")
        for name, details in env_status["details"].items():
            if not details["set"]:
                print(f"  - {name}")

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    if not is_valid:
        print("  - Fix all errors before proceeding with deployment")
    if warnings:
        print("  - Review and address warnings for optimal configuration")
    if settings.is_production():
        print("  - Ensure all security settings are properly configured")
        print("  - Verify all external service credentials are set")
    else:
        print("  - Consider enabling DEBUG mode for development")
        print("  - Set up development database and Redis instances")

    print("=" * 80)

    # Exit with error code if invalid
    if not is_valid:
        sys.exit(1)


if __name__ == "__main__":
    print_validation_report()
