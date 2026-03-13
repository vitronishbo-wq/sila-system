#!/usr/bin/env python3
"""
Configuration Validation Script for CI/CD Pipeline

This script validates the SILA configuration system as part of the CI/CD pipeline.
It ensures that:
1. All required configuration is valid
2. Security requirements are met
3. Environment-specific rules are followed
4. No sensitive data is exposed in non-production environments

Usage:
    python scripts/validate_config.py [--environment ENV] [--strict] [--output FORMAT]

Exit Codes:
    0: Success - All validations passed
    1: Warning - Validations passed with warnings
    2: Error - Critical validation failures
    3: Fatal - System errors during validation
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

try:
    from config import (
        settings,
        validate_configuration,
        get_config_manager,
        SettingsValidator,
        ConfigurationError,
    )
except ImportError as e:
    print(f"❌ FATAL: Cannot import configuration system: {e}")
    sys.exit(3)


class CIConfigValidator:
    """Configuration validator for CI/CD pipeline."""

    def __init__(self, environment: str = None, strict_mode: bool = False):
        """Initialize validator with environment and strict mode."""
        self.environment = environment or settings.ENVIRONMENT
        self.strict_mode = strict_mode
        self.validator = SettingsValidator(settings)
        self.results = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "security_issues": [],
            "environment_issues": [],
            "performance_issues": [],
        }

    def validate_all(self) -> Dict[str, Any]:
        """Run all configuration validations."""
        print(f"🔍 Validating SILA Configuration for environment: {self.environment}")
        print("=" * 70)

        # Basic configuration validation
        self._validate_basic_configuration()

        # Security validation
        self._validate_security_configuration()

        # Environment-specific validation
        self._validate_environment_configuration()

        # Performance validation
        self._validate_performance_configuration()

        # External services validation
        self._validate_external_services()

        # Database validation
        self._validate_database_configuration()

        # File system validation
        self._validate_file_system()

        # Calculate overall result
        self._calculate_result()

        return self.results

    def _validate_basic_configuration(self):
        """Validate basic configuration requirements."""
        print("📋 Basic Configuration Validation...")

        try:
            # Use the built-in validation
            is_valid, errors, warnings = validate_configuration()

            if errors:
                self.results["errors"].extend(errors)
                for error in errors:
                    print(f"  ❌ Error: {error}")

            if warnings:
                self.results["warnings"].extend(warnings)
                for warning in warnings:
                    print(f"  ⚠️  Warning: {warning}")

            if is_valid:
                print("  ✅ Basic configuration is valid")
            else:
                print("  ❌ Basic configuration has errors")

        except Exception as e:
            error_msg = f"Basic validation failed: {e}"
            self.results["errors"].append(error_msg)
            print(f"  ❌ {error_msg}")

    def _validate_security_configuration(self):
        """Validate security configuration."""
        print("\n🔒 Security Configuration Validation...")

        security_issues = []

        # Secret key validation
        if len(settings.SECRET_KEY) < 32:
            security_issues.append("SECRET_KEY must be at least 32 characters long")

        # Production security checks
        if self.environment == "production":
            if settings.DEBUG:
                security_issues.append("DEBUG mode must be disabled in production")

            if settings.SECRET_KEY in [
                "change_me_immediately",
                "your-secret-key-here",
                "insecure",
            ]:
                security_issues.append("Default SECRET_KEY detected in production")

            if not settings.SESSION_COOKIE_SECURE:
                security_issues.append(
                    "SESSION_COOKIE_SECURE must be True in production"
                )

            if settings.ALGORITHM != "HS256":
                security_issues.append("JWT algorithm should be HS256 for production")

        # Password policy validation
        if settings.PASSWORD_MIN_LENGTH < 8:
            security_issues.append("PASSWORD_MIN_LENGTH should be at least 8")

        # CORS validation
        allowed_origins = settings.allowed_origins_list
        if self.environment == "production" and "localhost" in str(allowed_origins):
            security_issues.append(
                "localhost origins should not be allowed in production"
            )

        # Database security
        if self.environment == "production":
            if (
                "password" in settings.POSTGRES_PASSWORD.lower()
                or "change" in settings.POSTGRES_PASSWORD.lower()
            ):
                security_issues.append(
                    "Default database password detected in production"
                )

        if security_issues:
            self.results["security_issues"].extend(security_issues)
            for issue in security_issues:
                print(f"  🔴 Security Issue: {issue}")
        else:
            print("  ✅ Security configuration is valid")

    def _validate_environment_configuration(self):
        """Validate environment-specific configuration."""
        print(f"\n🌍 Environment Configuration Validation ({self.environment})...")

        env_issues = []

        # Environment validation
        valid_envs = ["development", "staging", "production", "test"]
        if self.environment not in valid_envs:
            env_issues.append(f"Invalid environment: {self.environment}")

        # Development environment checks
        if self.environment == "development":
            if not settings.DEBUG:
                env_issues.append("DEBUG should be True in development")

        # Production environment checks
        if self.environment == "production":
            if settings.LOG_LEVEL == "DEBUG":
                env_issues.append("LOG_LEVEL should not be DEBUG in production")

            if settings.DATABASE_ECHO:
                env_issues.append("DATABASE_ECHO should be False in production")

        # Test environment checks
        if self.environment == "test":
            if settings.TEST_DATABASE_URL == settings.DATABASE_URL:
                env_issues.append(
                    "Test database should be different from main database"
                )

        if env_issues:
            self.results["environment_issues"].extend(env_issues)
            for issue in env_issues:
                print(f"  🌍 Environment Issue: {issue}")
        else:
            print("  ✅ Environment configuration is valid")

    def _validate_performance_configuration(self):
        """Validate performance-related configuration."""
        print("\n⚡ Performance Configuration Validation...")

        perf_issues = []

        # Database connection pool
        if settings.DATABASE_POOL_SIZE < 5:
            perf_issues.append("DATABASE_POOL_SIZE should be at least 5 for production")

        if settings.DATABASE_MAX_OVERFLOW < 10:
            perf_issues.append(
                "DATABASE_MAX_OVERFLOW should be at least 10 for production"
            )

        # Redis configuration
        if settings.REDIS_MAX_CONNECTIONS < 20:
            perf_issues.append(
                "REDIS_MAX_CONNECTIONS should be at least 20 for production"
            )

        # Rate limiting
        if not settings.RATE_LIMIT_ENABLED and self.environment == "production":
            perf_issues.append("RATE_LIMIT should be enabled in production")

        if settings.RATE_LIMIT_PER_MINUTE < 60 and self.environment == "production":
            perf_issues.append(
                "RATE_LIMIT_PER_MINUTE should be at least 60 for production"
            )

        if perf_issues:
            self.results["performance_issues"].extend(perf_issues)
            for issue in perf_issues:
                print(f"  ⚡ Performance Issue: {issue}")
        else:
            print("  ✅ Performance configuration is valid")

    def _validate_external_services(self):
        """Validate external services configuration."""
        print("\n🌐 External Services Validation...")

        # BNA API validation
        if settings.BNA_API_KEY == "your-bna-api-key":
            if self.environment == "production":
                self.results["errors"].append("BNA_API_KEY must be set in production")
                print("  ❌ BNA_API_KEY must be set in production")
            else:
                self.results["warnings"].append(
                    "BNA_API_KEY should be set for BNA integration"
                )
                print("  ⚠️  BNA_API_KEY should be set for BNA integration")
        else:
            print("  ✅ BNA API configuration is valid")

        # Email configuration
        if self.environment == "production":
            if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
                self.results["errors"].append(
                    "SMTP credentials must be set in production"
                )
                print("  ❌ SMTP credentials must be set in production")
            else:
                print("  ✅ Email configuration is valid")
        else:
            print("  ℹ️  Email configuration skipped (non-production)")

        # Storage configuration
        if (
            settings.MINIO_ACCESS_KEY == "minioadmin"
            and self.environment == "production"
        ):
            self.results["security_issues"].append(
                "Default MinIO credentials detected in production"
            )
            print("  🔴 Default MinIO credentials detected in production")
        else:
            print("  ✅ Storage configuration is valid")

    def _validate_database_configuration(self):
        """Validate database configuration."""
        print("\n🗄️  Database Configuration Validation...")

        # Database URL validation
        if not settings.DATABASE_URL:
            self.results["errors"].append("DATABASE_URL is not set")
            print("  ❌ DATABASE_URL is not set")
        elif not settings.DATABASE_URL.startswith(
            ("postgresql://", "postgresql+asyncpg://")
        ):
            self.results["errors"].append("DATABASE_URL must be a PostgreSQL URL")
            print("  ❌ DATABASE_URL must be a PostgreSQL URL")
        else:
            print("  ✅ Database URL is valid")

        # Test database validation
        if self.environment in ["test", "staging"]:
            if not settings.TEST_DATABASE_URL:
                self.results["errors"].append(
                    "TEST_DATABASE_URL is required for test/staging"
                )
                print("  ❌ TEST_DATABASE_URL is required for test/staging")
            else:
                print("  ✅ Test database URL is valid")

        # Connection validation
        try:
            db_info = settings.get_database_info()
            if db_info["pool_size"] < 1:
                self.results["errors"].append("Database pool size must be at least 1")
                print("  ❌ Database pool size must be at least 1")
            else:
                print("  ✅ Database connection settings are valid")
        except Exception as e:
            self.results["errors"].append(f"Database configuration error: {e}")
            print(f"  ❌ Database configuration error: {e}")

    def _validate_file_system(self):
        """Validate file system configuration."""
        print("\n📁 File System Validation...")

        # Upload directory validation
        upload_path = Path(settings.UPLOAD_PATH)
        try:
            if not upload_path.exists():
                upload_path.mkdir(parents=True, exist_ok=True)
                print(f"  📁 Created upload directory: {upload_path}")
            else:
                if not upload_path.is_dir():
                    self.results["errors"].append(
                        f"UPLOAD_PATH is not a directory: {upload_path}"
                    )
                    print(f"  ❌ UPLOAD_PATH is not a directory: {upload_path}")
                else:
                    print("  ✅ Upload directory is valid")
        except Exception as e:
            self.results["errors"].append(f"Cannot create upload directory: {e}")
            print(f"  ❌ Cannot create upload directory: {e}")

        # File extensions validation
        extensions = settings.allowed_extensions_list
        if not extensions:
            self.results["errors"].append("ALLOWED_EXTENSIONS cannot be empty")
            print("  ❌ ALLOWED_EXTENSIONS cannot be empty")
        else:
            print(f"  ✅ File extensions configured: {len(extensions)} types")

        # Upload size validation
        if settings.MAX_UPLOAD_SIZE <= 0:
            self.results["errors"].append("MAX_UPLOAD_SIZE must be positive")
            print("  ❌ MAX_UPLOAD_SIZE must be positive")
        elif settings.MAX_UPLOAD_SIZE > 100 * 1024 * 1024:  # 100MB
            if self.environment == "production":
                self.results["warnings"].append(
                    "MAX_UPLOAD_SIZE is very large for production"
                )
                print("  ⚠️  MAX_UPLOAD_SIZE is very large for production")
            else:
                print("  ✅ Upload size is valid")
        else:
            print("  ✅ Upload size is valid")

    def _calculate_result(self):
        """Calculate overall validation result."""
        total_errors = (
            len(self.results["errors"])
            + len(self.results["security_issues"])
            + len(self.results["environment_issues"])
        )

        total_warnings = len(self.results["warnings"]) + len(
            self.results["performance_issues"]
        )

        self.results["valid"] = total_errors == 0
        self.results["total_errors"] = total_errors
        self.results["total_warnings"] = total_warnings

        print("\n" + "=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)

        if self.results["valid"]:
            if total_warnings > 0:
                print(f"⚠️  VALID with {total_warnings} warnings")
            else:
                print("✅ VALID - All checks passed")
        else:
            print(f"❌ INVALID - {total_errors} errors, {total_warnings} warnings")

        if self.results["errors"]:
            print(f"\n🚨 Critical Errors ({len(self.results['errors'])}):")
            for error in self.results["errors"]:
                print(f"  - {error}")

        if self.results["security_issues"]:
            print(f"\n🔒 Security Issues ({len(self.results['security_issues'])}):")
            for issue in self.results["security_issues"]:
                print(f"  - {issue}")

        if self.results["environment_issues"]:
            print(
                f"\n🌍 Environment Issues ({len(self.results['environment_issues'])}):"
            )
            for issue in self.results["environment_issues"]:
                print(f"  - {issue}")

        if self.results["warnings"]:
            print(f"\n⚠️  Warnings ({len(self.results['warnings'])}):")
            for warning in self.results["warnings"]:
                print(f"  - {warning}")

        if self.results["performance_issues"]:
            print(
                f"\n⚡ Performance Issues ({len(self.results['performance_issues'])}):"
            )
            for issue in self.results["performance_issues"]:
                print(f"  - {issue}")


def main():
    """Main entry point for the validation script."""
    parser = argparse.ArgumentParser(
        description="Validate SILA configuration for CI/CD"
    )
    parser.add_argument(
        "--environment",
        "-e",
        help="Target environment (development, staging, production, test)",
    )
    parser.add_argument(
        "--strict",
        "-s",
        action="store_true",
        help="Enable strict mode (warnings become errors)",
    )
    parser.add_argument(
        "--output", "-o", choices=["text", "json"], default="text", help="Output format"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Quiet mode (minimal output)"
    )

    args = parser.parse_args()

    try:
        # Initialize validator
        validator = CIConfigValidator(
            environment=args.environment, strict_mode=args.strict
        )

        # Run validation
        results = validator.validate_all()

        # Output results
        if args.output == "json":
            print(json.dumps(results, indent=2))
        elif not args.quiet:
            # Summary already printed in validate_all()
            pass

        # Exit with appropriate code
        if not results["valid"]:
            sys.exit(2)  # Error
        elif results["total_warnings"] > 0 and args.strict:
            sys.exit(1)  # Warning in strict mode
        else:
            sys.exit(0)  # Success

    except KeyboardInterrupt:
        print("\n❌ Validation interrupted by user")
        sys.exit(3)
    except Exception as e:
        print(f"❌ FATAL: Validation system error: {e}")
        if not args.quiet:
            import traceback

            traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    main()
