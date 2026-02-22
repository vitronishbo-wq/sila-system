"""
DEPRECATED: Use apps/backend/config/settings.py instead.

This file is kept for backward compatibility only.
All configuration is now managed centrally in settings.py.
"""

import warnings

# Warn about deprecation
warnings.warn(
    "core.config is deprecated. Use config.settings instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export from the new location for backward compatibility
from config.settings import (
    Settings,
    get_settings,
    settings,
    validate_settings,
    print_settings_summary,
)

__all__ = [
    "Settings",
    "get_settings",
    "settings",
    "validate_settings",
    "print_settings_summary",
]
