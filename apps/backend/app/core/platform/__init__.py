"""Macro-domain: platform primitives (runtime/config/db)."""

from apps.backend.app.core import settings
from apps.backend.app.core.db import get_db

__all__ = ["get_db", "settings"]
