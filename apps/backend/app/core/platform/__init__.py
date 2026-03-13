"""Macro-domain: platform primitives (runtime/config/db)."""
from app.core import settings
from app.core.db import get_db
__all__ = ['get_db', 'settings']