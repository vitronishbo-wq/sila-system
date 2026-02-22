"""
Example usage of the centralized SILA configuration system.

This file demonstrates how to use the new configuration system
and how to migrate from the old system.
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# =========================
# OLD WAY (Before migration)
# =========================

# Old import pattern
# from config import settings
# import os
#
# database_url = settings.DATABASE_URL
# secret_key = settings.SECRET_KEY
# debug_mode = settings.DEBUG.lower() == 'true'

# =========================
# NEW WAY (After migration)
# =========================

# New import pattern
from config import settings, get_config_manager

# Basic usage
def basic_configuration_usage():
    """Demonstrate basic configuration access."""
    print("=== Basic Configuration Usage ===")

    # Access configuration values
    project_name = settings.PROJECT_NAME
    environment = settings.ENVIRONMENT
    database_url = settings.DATABASE_URL
    secret_key = settings.SECRET_KEY

    print(f"Project: {project_name}")
    print(f"Environment: {environment}")
    print(f"Database URL: {database_url}")
    print(f"Secret Key Length: {len(secret_key)}")

    # Use computed properties
    async_db_url = settings.ASYNC_DATABASE_URL
    print(f"Async DB URL: {async_db_url}")

    # Environment checking
    if settings.is_production():
        print("Running in production mode")
    elif settings.is_development():
        print("Running in development mode")

    # Get configuration info
    db_info = settings.get_database_info()
    print(f"Database Info: {db_info}")


def advanced_configuration_usage():
    """Demonstrate advanced configuration management."""
    print("\n=== Advanced Configuration Usage ===")

    # Get configuration manager
    manager = get_config_manager()

    # Get configuration summary
    summary = manager.get_config_summary(include_secrets=False)
    print(f"Current Environment: {summary['environment']}")
    print(f"Project: {summary['project']['name']}")

    # List enabled features
    features = summary['features']
    enabled_features = [name for name, enabled in features.items() if enabled]
    print(f"Enabled Features: {enabled_features}")

    # Update settings temporarily
    print(f"Original DEBUG: {settings.DEBUG}")

    with manager.temporary_settings(DEBUG=True, LOG_LEVEL="DEBUG"):
        print(f"Temporary DEBUG: {settings.DEBUG}")
        print(f"Temporary LOG_LEVEL: {settings.LOG_LEVEL}")

    print(f"Restored DEBUG: {settings.DEBUG}")


def environment_switching_example():
    """Demonstrate environment switching."""
    print("\n=== Environment Switching Example ===")

    manager = get_config_manager()
    original_env = settings.ENVIRONMENT

    print(f"Original environment: {original_env}")

    try:
        # Switch to test environment
        test_settings = manager.switch_environment('test')
        print(f"Switched to: {test_settings.ENVIRONMENT}")
        print(f"Test database URL: {test_settings.TEST_DATABASE_URL}")

        # Switch back to original
        manager.switch_environment(original_env)
        print(f"Restored to: {settings.ENVIRONMENT}")

    except Exception as e:
        print(f"Environment switching failed: {e}")


def file_operations_example():
    """Demonstrate file operations."""
    print("\n=== File Operations Example ===")

    manager = get_config_manager()

    # Export configuration template
    template_path = "example_config_template.json"
    manager.export_config_template(template_path)
    print(f"Configuration template exported to: {template_path}")

    # Save current configuration
    config_path = "example_current_settings.json"
    manager.save_to_file(config_path, include_secrets=False)
    print(f"Current configuration saved to: {config_path}")

    # Load configuration from file
    try:
        loaded_settings = manager.load_from_file(config_path)
        print(f"Loaded configuration: {loaded_settings.PROJECT_NAME}")
    except Exception as e:
        print(f"Failed to load configuration: {e}")


def validation_example():
    """Demonstrate configuration validation."""
    print("\n=== Configuration Validation Example ===")

    from config import validate_configuration

    # Validate current configuration
    is_valid, errors, warnings = validate_configuration()

    print(f"Configuration Valid: {is_valid}")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")


def cors_and_upload_example():
    """Demonstrate CORS and upload configuration."""
    print("\n=== CORS and Upload Configuration Example ===")

    # Get CORS origins as list
    allowed_origins = settings.allowed_origins_list
    print(f"Allowed CORS Origins: {allowed_origins}")

    # Get allowed extensions as list
    allowed_extensions = settings.allowed_extensions_list
    print(f"Allowed File Extensions: {allowed_extensions}")

    # Upload configuration
    max_size_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
    print(f"Max Upload Size: {max_size_mb} MB")
    print(f"Upload Path: {settings.UPLOAD_PATH}")


def security_configuration_example():
    """Demonstrate security configuration."""
    print("\n=== Security Configuration Example ===")

    # Security settings
    security_info = settings.get_security_info()
    print(f"JWT Algorithm: {security_info['algorithm']}")
    print(f"Access Token Expires: {security_info['access_token_expire_minutes']} minutes")
    print(f"Password Hash Algorithm: {security_info['password_hash_algorithm']}")
    print(f"Min Password Length: {security_info['password_min_length']}")

    # Session settings
    print(f"Session Timeout: {settings.SESSION_TIMEOUT_MINUTES} minutes")
    print(f"Session Cookie Secure: {settings.SESSION_COOKIE_SECURE}")

    # Production security checks
    if settings.is_production():
        print("Production security checks:")
        print(f"  - Secret key length valid: {len(settings.SECRET_KEY) >= 32}")
        print(f"  - Debug mode disabled: {not settings.DEBUG}")
        print(f"  - Secure cookies enabled: {settings.SESSION_COOKIE_SECURE}")


def external_services_example():
    """Demonstrate external services configuration."""
    print("\n=== External Services Configuration Example ===")

    # BNA API
    print(f"BNA API URL: {settings.BNA_API_URL}")
    print(f"BNA Environment: {settings.BNA_ENVIRONMENT}")
    print(f"BNA Timeout: {settings.BNA_TIMEOUT} seconds")

    # Email configuration
    print(f"SMTP Host: {settings.SMTP_HOST}")
    print(f"SMTP Port: {settings.SMTP_PORT}")
    print(f"SMTP TLS Enabled: {settings.SMTP_USE_TLS}")

    # MinIO storage
    print(f"Storage Backend: {settings.STORAGE_BACKEND}")
    print(f"MinIO Endpoint: {settings.MINIO_ENDPOINT}")
    print(f"MinIO Bucket: {settings.MINIO_BUCKET_NAME}")

    # Redis configuration
    redis_info = settings.get_redis_info()
    print(f"Redis URL: {redis_info['url']}")
    print(f"Redis DB: {redis_info['db']}")


def migration_example():
    """Show how to migrate from old configuration system."""
    print("\n=== Migration Example ===")

    print("OLD CODE:")
    print("""
    from config import settings
    import os

    # Get database URL
    database_url = settings.DATABASE_URL

    # Check if debug mode
    debug = settings.DEBUG.lower() == 'true'

    # Get secret key
    secret_key = settings.SECRET_KEY
    """)

    print("\nNEW CODE:")
    print("""
    from config import settings

    # Get database URL (computed property)
    database_url = settings.DATABASE_URL

    # Check if debug mode (boolean)
    debug = settings.DEBUG

    # Get secret key (validated)
    secret_key = settings.SECRET_KEY

    # Additional benefits
    if settings.is_production():
        # Production-specific logic
        pass

    # Get database info without sensitive data
    db_info = settings.get_database_info()
    """)

    print("\nMIGRATION STEPS:")
    print("1. Replace 'from config import settings
    print("2. Replace os.getenv() calls with direct settings access")
    print("3. Use computed properties for complex values")
    print("4. Add environment-specific logic with is_production(), is_development()")
    print("5. Use validation to ensure configuration is correct")


def main():
    """Run all examples."""
    print("SILA Configuration System - Usage Examples")
    print("=" * 60)

    try:
        basic_configuration_usage()
        advanced_configuration_usage()
        environment_switching_example()
        file_operations_example()
        validation_example()
        cors_and_upload_example()
        security_configuration_example()
        external_services_example()
        migration_example()

        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("\nThe centralized configuration system is ready for use!")
        print("Start migrating your modules to use the new config system.")

    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
