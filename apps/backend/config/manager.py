"""
Configuration management utilities for SILA system.

Provides high-level configuration management, environment switching,
and dynamic configuration updates.
"""

import json
import os
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from contextlib import contextmanager

from .settings import Settings, get_settings
from .validator import validate_configuration, ConfigurationError


logger = logging.getLogger(__name__)


class ConfigManager:
    """
    High-level configuration manager for SILA system.

    Provides methods for loading, saving, and managing configuration
    across different environments and deployment scenarios.
    """

    def __init__(self, settings_instance: Optional[Settings] = None):
        """Initialize configuration manager."""
        self.settings = settings_instance or get_settings()
        self._config_history: List[Dict[str, Any]] = []

    def load_from_file(self, config_path: Union[str, Path]) -> Settings:
        """
        Load configuration from JSON file.

        Args:
            config_path: Path to configuration file

        Returns:
            Settings: Loaded settings instance

        Raises:
            ConfigurationError: If loading fails
        """
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                raise ConfigurationError(f"Configuration file not found: {config_path}")

            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            # Create new settings instance with loaded data
            loaded_settings = Settings(**config_data)

            # Validate loaded settings
            is_valid, errors, warnings = validate_configuration(loaded_settings)
            if not is_valid:
                raise ConfigurationError(f"Invalid configuration: {errors}")

            # Store in history
            self._config_history.append(
                {
                    "timestamp": str(self.settings.model_dump()),
                    "source": str(config_path),
                    "environment": loaded_settings.ENVIRONMENT,
                }
            )

            logger.info(f"Configuration loaded from {config_path}")
            return loaded_settings

        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

    def save_to_file(
        self, config_path: Union[str, Path], include_secrets: bool = False
    ) -> None:
        """
        Save current configuration to JSON file.

        Args:
            config_path: Path to save configuration
            include_secrets: Whether to include sensitive data
        """
        try:
            config_path = Path(config_path)
            config_path.parent.mkdir(parents=True, exist_ok=True)

            config_data = self.settings.model_dump()

            # Remove sensitive data if requested
            if not include_secrets:
                sensitive_keys = [
                    "SECRET_KEY",
                    "AUTH_SECRET_KEY",
                    "POSTGRES_PASSWORD",
                    "REDIS_PASSWORD",
                    "SMTP_PASSWORD",
                    "MINIO_SECRET_KEY",
                    "BNA_API_KEY",
                    "GRAFANA_PASSWORD",
                ]
                for key in sensitive_keys:
                    if key in config_data:
                        config_data[key] = "***"

            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, default=str)

            logger.info(f"Configuration saved to {config_path}")

        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")

    def update_setting(self, key: str, value: Any) -> None:
        """
        Update a specific setting value.

        Args:
            key: Setting key (supports nested keys with dots)
            value: New value
        """
        try:
            # Handle nested keys
            if "." in key:
                keys = key.split(".")
                current = self.settings.model_dump()

                # Navigate to nested location
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]

                # Set the final value
                current[keys[-1]] = value

                # Create new settings instance
                self.settings = Settings(**self.settings.model_dump())
            else:
                # Set top-level value
                setattr(self.settings, key, value)

            logger.info(f"Setting updated: {key} = {value}")

        except Exception as e:
            raise ConfigurationError(f"Failed to update setting {key}: {e}")

    def get_environment_config(self, environment: str) -> Dict[str, Any]:
        """
        Get configuration for specific environment.

        Args:
            environment: Target environment

        Returns:
            Dict[str, Any]: Environment-specific configuration
        """
        env_files = {
            "development": ".env.development",
            "staging": ".env.staging",
            "production": ".env.production",
            "test": ".env.test",
        }

        env_file = env_files.get(environment)
        if not env_file:
            raise ConfigurationError(f"Unknown environment: {environment}")

        config = {}
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()

        return config

    def switch_environment(self, new_environment: str) -> Settings:
        """
        Switch to different environment configuration.

        Args:
            new_environment: Target environment

        Returns:
            Settings: New settings instance
        """
        try:
            # Load environment-specific configuration
            env_config = self.get_environment_config(new_environment)

            # Create new settings with environment config
            current_config = self.settings.model_dump()
            current_config.update(env_config)
            current_config["ENVIRONMENT"] = new_environment

            new_settings = Settings(**current_config)

            # Validate new settings
            is_valid, errors, warnings = validate_configuration(new_settings)
            if not is_valid:
                raise ConfigurationError(
                    f"Invalid configuration for {new_environment}: {errors}"
                )

            # Update current settings
            self.settings = new_settings

            logger.info(f"Switched to {new_environment} environment")
            return new_settings

        except Exception as e:
            raise ConfigurationError(f"Failed to switch environment: {e}")

    def get_config_summary(self, include_secrets: bool = False) -> Dict[str, Any]:
        """
        Get configuration summary.

        Args:
            include_secrets: Whether to include sensitive data

        Returns:
            Dict[str, Any]: Configuration summary
        """
        config = self.settings.model_dump()

        if not include_secrets:
            # Mask sensitive values
            sensitive_patterns = ["SECRET", "PASSWORD", "KEY", "TOKEN"]

            for key, value in config.items():
                if any(pattern in key.upper() for pattern in sensitive_patterns):
                    config[key] = "***"

        return {
            "environment": self.settings.ENVIRONMENT,
            "debug": self.settings.DEBUG,
            "project": {
                "name": self.settings.PROJECT_NAME,
                "version": self.settings.VERSION,
                "description": self.settings.DESCRIPTION,
            },
            "database": self.settings.get_database_info(),
            "redis": self.settings.get_redis_info(),
            "security": self.settings.get_security_info(),
            "features": {
                "monitoring": self.settings.FEATURE_MONITORING,
                "backup": self.settings.FEATURE_BACKUP,
                "auto_healer": self.settings.FEATURE_AUTO_HEALER,
                "audit_log": self.settings.FEATURE_AUDIT_LOG,
                "email_notifications": self.settings.FEATURE_EMAIL_NOTIFICATIONS,
                "file_storage": self.settings.FEATURE_FILE_STORAGE,
                "rate_limiting": self.settings.RATE_LIMIT_ENABLED,
                "telemetry": self.settings.TELEMETRY_ENABLED,
            },
            "full_config": config,
        }

    def export_config_template(self, output_path: Union[str, Path]) -> None:
        """
        Export configuration template with descriptions.

        Args:
            output_path: Path to save template
        """
        template = {
            "_description": "SILA System Configuration Template",
            "_instructions": [
                "Copy this file and fill in your values",
                "Remove sensitive data before committing to version control",
                "Use environment-specific files: .env.development, .env.staging, .env.production",
            ],
            "PROJECT_NAME": "SILA System",
            "VERSION": "1.0.0",
            "ENVIRONMENT": "development",
            "DEBUG": True,
            "POSTGRES_USER": "your_db_user",
            "POSTGRES_PASSWORD": "your_secure_password",
            "POSTGRES_DB": "sila_db",
            "POSTGRES_HOST": "localhost",
            "POSTGRES_PORT": 5432,
            "SECRET_KEY": "your_32_character_secret_key",
            "AUTH_SECRET_KEY": "your_32_character_auth_secret",
            "REDIS_URL": "redis://localhost:6379/0",
            "BNA_API_KEY": "your_bna_api_key",
            "BNA_API_URL": "https://api.bna.ao",
            "SMTP_HOST": "smtp.gmail.com",
            "SMTP_PORT": 587,
            "SMTP_USERNAME": "your_email@gmail.com",
            "SMTP_PASSWORD": "your_email_password",
            "MINIO_ENDPOINT": "localhost:9000",
            "MINIO_ACCESS_KEY": "your_minio_access_key",
            "MINIO_SECRET_KEY": "your_minio_secret_key",
            "LOG_LEVEL": "INFO",
            "RATE_LIMIT_ENABLED": True,
            "RATE_LIMIT_PER_MINUTE": 60,
            "MAX_UPLOAD_SIZE": 10485760,
            "FEATURE_MONITORING": True,
            "FEATURE_BACKUP": True,
            "FEATURE_AUTO_HEALER": True,
            "FEATURE_AUDIT_LOG": True,
        }

        try:
            output_path = Path(output_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(template, f, indent=2)

            logger.info(f"Configuration template exported to {output_path}")

        except Exception as e:
            raise ConfigurationError(f"Failed to export template: {e}")

    @contextmanager
    def temporary_settings(self, **kwargs):
        """
        Context manager for temporary settings changes.

        Args:
            **kwargs: Temporary setting overrides
        """
        original_settings = self.settings.model_dump()

        try:
            # Apply temporary settings
            for key, value in kwargs.items():
                self.update_setting(key, value)

            yield self.settings

        finally:
            # Restore original settings
            self.settings = Settings(**original_settings)

    def get_config_history(self) -> List[Dict[str, Any]]:
        """
        Get configuration change history.

        Returns:
            List[Dict[str, Any]]: History of configuration changes
        """
        return self._config_history.copy()


# Global configuration manager instance
config_manager = ConfigManager()


def get_config_manager() -> ConfigManager:
    """Get global configuration manager instance."""
    return config_manager


def load_config_from_file(config_path: Union[str, Path]) -> Settings:
    """
    Load configuration from file using global manager.

    Args:
        config_path: Path to configuration file

    Returns:
        Settings: Loaded settings
    """
    return config_manager.load_from_file(config_path)


def switch_environment(environment: str) -> Settings:
    """
    Switch environment using global manager.

    Args:
        environment: Target environment

    Returns:
        Settings: New settings instance
    """
    return config_manager.switch_environment(environment)


def export_config_template(
    output_path: Union[str, Path] = "config_template.json",
) -> None:
    """
    Export configuration template using global manager.

    Args:
        output_path: Path to save template
    """
    config_manager.export_config_template(output_path)


if __name__ == "__main__":
    # Example usage
    print("SILA Configuration Manager")
    print("=" * 40)

    # Get current configuration summary
    summary = config_manager.get_config_summary()
    print(f"Current Environment: {summary['environment']}")
    print(f"Project: {summary['project']['name']} v{summary['project']['version']}")

    # Export template
    export_config_template()
    print("Configuration template exported to config_template.json")

    # Validate current configuration
    is_valid, errors, warnings = validate_configuration()
    print(f"Configuration Valid: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    if warnings:
        print(f"Warnings: {warnings}")
