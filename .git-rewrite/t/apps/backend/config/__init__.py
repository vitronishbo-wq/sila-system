"""
Configuration module for SILA system.

Centralized configuration management using Pydantic V2 settings.
Provides comprehensive validation, management, and environment switching.
"""

from .settings import settings, get_settings, Settings
from .validator import (
    validate_configuration,
    SettingsValidator,
    ConfigurationError,
    print_validation_report,
)
from .manager import (
    ConfigManager,
    get_config_manager,
    load_config_from_file,
    switch_environment,
    export_config_template,
)

__all__ = [
    # Core settings
    "settings",
    "get_settings",
    "Settings",
    # Validation
    "validate_configuration",
    "SettingsValidator",
    "ConfigurationError",
    "print_validation_report",
    # Management
    "ConfigManager",
    "get_config_manager",
    "load_config_from_file",
    "switch_environment",
    "export_config_template",
]
