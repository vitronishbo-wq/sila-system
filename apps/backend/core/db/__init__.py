"""Database module compatibility facade.

All ORM models must use the canonical Base from ``app.core.database``.
This package re-exports that Base for legacy imports.
"""

from app.core.db import Base

# Optional session imports - only import when needed
try:
    from .session import (
        AsyncSessionLocal,
        SessionLocal,
        async_engine,
        async_session_factory,
        engine,
        get_async_db,
        get_db,
        SQLALCHEMY_DATABASE_URL,
    )

    _SESSION_AVAILABLE = True
except ImportError:
    AsyncSessionLocal = None
    SessionLocal = None
    async_engine = None
    async_session_factory = None
    engine = None
    get_async_db = None
    get_db = None
    SQLALCHEMY_DATABASE_URL = None
    _SESSION_AVAILABLE = False

__all__ = [
    "Base",
]

# Add session exports only if available
if _SESSION_AVAILABLE:
    __all__.extend(
        [
            "SessionLocal",
            "AsyncSessionLocal",
            "engine",
            "async_engine",
            "async_session_factory",
            "get_db",
            "get_async_db",
            "SQLALCHEMY_DATABASE_URL",
        ]
    )
