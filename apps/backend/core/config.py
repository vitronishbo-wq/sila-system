import warnings

from config.settings import (
    Settings,
    get_settings,
    print_settings_summary,
    settings,
    validate_settings,
)

warnings.warn(
    "⚠️ core.config está obsoleto. Por favor, importe de config.settings.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "Settings",
    "get_settings",
    "settings",
    "validate_settings",
    "print_settings_summary",
]
