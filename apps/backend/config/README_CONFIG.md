# SILA Configuration System

## Overview

The SILA Configuration System provides a centralized, type-safe, and validated
configuration management solution using Pydantic V2. This system replaces scattered
environment variable access and provides a single source of truth for all application
settings.

## Features

- **Type Safety**: Full Pydantic V2 validation with automatic type conversion
- **Environment Management**: Support for development, staging, production, and test
  environments
- **Validation**: Comprehensive configuration validation with detailed error reporting
- **Security**: Built-in handling of sensitive data with masking capabilities
- **Flexibility**: Support for JSON configuration files and environment variables
- **Performance**: Cached settings with minimal overhead
- **Migration**: Tools to migrate existing configuration usage

## Architecture

```
config/
├── __init__.py              # Main exports and imports
├── settings.py              # Core Pydantic V2 settings class
├── validator.py             # Configuration validation utilities
├── manager.py               # High-level configuration management
├── migrate_config.py        # Migration tools for existing code
├── test_config.py           # Comprehensive test suite
├── .env.example            # Environment variables template
└── README_CONFIG.md        # This documentation
```

## Quick Start

### 1. Basic Usage

```python
# Import settings
from config import settings

# Access configuration values
project_name = settings.PROJECT_NAME
database_url = settings.DATABASE_URL
is_production = settings.is_production()

# Use computed properties
async_db_url = settings.ASYNC_DATABASE_URL
db_info = settings.get_database_info()
```

### 2. Environment Configuration

```python
# Switch environments
from config import switch_environment

# Switch to production settings
prod_settings = switch_environment("production")

# Check current environment
if settings.is_production():
    print("Running in production mode")
```

### 3. Configuration Validation

```python
# Validate current configuration
from config import validate_configuration

is_valid, errors, warnings = validate_configuration()

if not is_valid:
    print("Configuration errors:", errors)
```

### 4. Advanced Management

```python
# Use configuration manager
from config import get_config_manager

manager = get_config_manager()

# Get configuration summary
summary = manager.get_config_summary(include_secrets=False)

# Update settings temporarily
with manager.temporary_settings(DEBUG=True):
    # Temporary debug mode
    pass

# Export configuration template
manager.export_config_template("my_config.json")
```

## Configuration Categories

### Project Information

- `PROJECT_NAME`: Application name
- `VERSION`: Application version
- `DESCRIPTION`: Application description
- `ENVIRONMENT`: Current environment (development/staging/production/test)

### Database Configuration

- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `POSTGRES_HOST`: Database host
- `POSTGRES_PORT`: Database port
- `DATABASE_URL`: Computed synchronous database URL
- `ASYNC_DATABASE_URL`: Computed asynchronous database URL

### Security Configuration

- `SECRET_KEY`: JWT secret key (minimum 32 characters)
- `AUTH_SECRET_KEY`: Authentication secret key
- `ALGORITHM`: JWT algorithm (HS256, HS384, HS512, RS256, etc.)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration time
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration time
- Password settings with complexity requirements

### Redis and Cache Configuration

- `REDIS_URL`: Redis connection URL
- `REDIS_PASSWORD`: Redis password (optional)
- `CACHE_BACKEND`: Cache backend (redis, memory)
- `CACHE_TTL_SECONDS`: Cache time-to-live
- `CELERY_BROKER_URL`: Celery broker URL

### External Services

- `BNA_API_KEY`: BNA API authentication key
- `BNA_API_URL`: BNA API endpoint URL
- `SMTP_*`: Email configuration settings
- `MINIO_*`: Object storage configuration

### Feature Flags

- `FEATURE_MONITORING`: Enable monitoring features
- `FEATURE_BACKUP`: Enable backup features
- `FEATURE_AUTO_HEALER`: Enable auto-healer features
- `FEATURE_AUDIT_LOG`: Enable audit logging
- `FEATURE_EMAIL_NOTIFICATIONS`: Enable email notifications

## Environment Files

### Development (.env.development)

```bash
ENVIRONMENT=development
DEBUG=true
DATABASE_ECHO=true
LOG_LEVEL=DEBUG
```

### Production (.env.production)

```bash
ENVIRONMENT=production
DEBUG=false
SESSION_COOKIE_SECURE=true
LOG_LEVEL=INFO
```

### Testing (.env.test)

```bash
ENVIRONMENT=test
DEBUG=true
DATABASE_URL=postgresql://test:test@localhost:5432/sila_test
```

## Validation Rules

### Security Validation

- Secret keys must be at least 32 characters in production
- Default passwords are rejected in production environments
- Session cookies must be secure in production

### Database Validation

- Database URLs must use PostgreSQL protocol
- Connection pool settings must be positive
- Host and database name are required

### Environment Validation

- Only valid environment names are accepted
- Debug mode is automatically disabled in production
- Log levels are validated against allowed values

## Migration Guide

### 1. Update Requirements

Ensure `pydantic-settings` is installed:

```bash
pip install pydantic-settings>=2.0.0
```

### 2. Update Imports

Replace old imports:

```python
# Old
from core.config import settings
import os
value = os.getenv('MY_SETTING')

# New
from config import settings
value = settings.MY_SETTING
```

### 3. Run Migration Tool

```bash
# Dry run to see what will be changed
python config/migrate_config.py --dry-run

# Apply changes
python config/migrate_config.py --apply
```

### 4. Update Environment Files

Copy the example environment file:

```bash
cp config/.env.example .env
# Edit .env with your values
```

## Advanced Usage

### Custom Settings Classes

```python
from config import Settings

class CustomSettings(Settings):
    CUSTOM_FEATURE: bool = Field(default=False, description="Custom feature flag")

    @field_validator("CUSTOM_FEATURE")
    @classmethod
    def validate_custom_feature(cls, v: bool, info: Any) -> bool:
        if info.data.get("ENVIRONMENT") == "production" and not v:
            raise ValueError("Custom feature must be enabled in production")
        return v
```

### Dynamic Configuration

```python
from config import get_config_manager

manager = get_config_manager()

# Load configuration from file
new_settings = manager.load_from_file("custom_config.json")

# Update specific setting
manager.update_setting("LOG_LEVEL", "DEBUG")

# Save current configuration
manager.save_to_file("backup_config.json", include_secrets=False)
```

### Configuration Profiles

```python
# Development profile
dev_config = {
    "DEBUG": True,
    "LOG_LEVEL": "DEBUG",
    "DATABASE_ECHO": True
}

# Production profile
prod_config = {
    "DEBUG": False,
    "LOG_LEVEL": "INFO",
    "SESSION_COOKIE_SECURE": True
}

# Apply profile
with manager.temporary_settings(**dev_config):
    # Development settings active
    pass
```

## Testing

### Run Configuration Tests

```bash
python config/test_config.py
```

### Test Coverage

- Basic imports and functionality
- Settings instance validation
- Configuration validation
- Manager functionality
- File operations
- Environment switching
- Cross-module imports
- Performance testing

## Security Considerations

### Sensitive Data Handling

- Passwords and keys are automatically masked in logs
- Configuration files can exclude sensitive data
- Environment variables take precedence over files

### Production Security

- Secret keys must be properly set
- Default passwords are rejected
- Debug mode is automatically disabled
- Session cookies must be secure

### Access Control

- Use environment-specific configuration files
- Limit access to production secrets
- Rotate secrets regularly
- Monitor configuration changes

## Performance Optimization

### Settings Caching

Settings are cached using LRU cache for optimal performance:

```python
from config import get_settings

# This returns the same cached instance
settings1 = get_settings()
settings2 = get_settings()  # No additional overhead
```

### Lazy Loading

Computed properties are only evaluated when accessed:

```python
# Database URL is only computed when needed
if some_condition:
    db_url = settings.DATABASE_URL  # Computed here
```

## Troubleshooting

### Common Issues

1. **Import Errors**

   - Ensure backend directory is in Python path
   - Check that pydantic-settings is installed

2. **Validation Errors**

   - Check environment variables are set
   - Review validation error messages
   - Use configuration validator for detailed analysis

3. **Performance Issues**
   - Use cached settings instance
   - Avoid repeated configuration loading
   - Profile configuration access patterns

### Debug Mode

Enable debug mode for detailed configuration information:

```python
from config import print_validation_report

print_validation_report()
```

### Environment Variable Debugging

Check environment variable status:

```python
from config.validator import check_environment_variables

env_status = check_environment_variables()
print(f"Variables set: {env_status['set']}/{env_status['total']}")
```

## Best Practices

### 1. Environment Management

- Use separate environment files for each environment
- Never commit production secrets to version control
- Use environment-specific validation rules

### 2. Configuration Structure

- Group related settings together
- Use descriptive names and documentation
- Provide sensible defaults

### 3. Security

- Always use strong secret keys
- Enable security features in production
- Regularly rotate sensitive values

### 4. Performance

- Use cached settings instance
- Avoid repeated validation
- Profile configuration access

### 5. Maintenance

- Keep documentation updated
- Use configuration validation
- Monitor configuration changes

## API Reference

### Settings Class

The main settings class with all configuration options.

#### Methods

- `is_production()`: Check if running in production
- `is_development()`: Check if running in development
- `is_testing()`: Check if running in test environment
- `get_database_info()`: Get database configuration (without password)
- `get_redis_info()`: Get Redis configuration (without password)
- `get_security_info()`: Get security configuration

### ConfigManager Class

High-level configuration management.

#### Methods

- `load_from_file(path)`: Load configuration from JSON file
- `save_to_file(path, include_secrets)`: Save configuration to file
- `update_setting(key, value)`: Update specific setting
- `switch_environment(environment)`: Switch to different environment
- `get_config_summary(include_secrets)`: Get configuration summary
- `export_config_template(path)`: Export configuration template

### Validation Functions

- `validate_configuration(settings)`: Validate configuration
- `check_environment_variables()`: Check environment variable status
- `print_validation_report()`: Print detailed validation report

## Contributing

When adding new configuration options:

1. Add field to Settings class with proper type hints
2. Add validation rules if needed
3. Update documentation
4. Add tests for new options
5. Update migration tools if needed

## License

This configuration system is part of the SILA system and follows the same license terms.
