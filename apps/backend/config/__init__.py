# config/__init__.py
"""
Configuração centralizada do sistema SILA (Pydantic V2).
"""

from .settings import settings, Settings, get_settings
from .manager import ConfigManager, get_config_manager
from .validator import (
    validate_configuration,
    SettingsValidator,
    ConfigurationError,
    print_validation_report,
)

# Aliases para compatibilidade legada (core/config.py)
validate_settings = validate_configuration
print_settings_summary = print_validation_report

__all__ = [
    "settings",
    "Settings",
    "get_settings",
    "ConfigManager",
    "get_config_manager",
    "validate_configuration",
    "SettingsValidator",
    "ConfigurationError",
    "print_validation_report",
    "validate_settings",
    "print_settings_summary",
]