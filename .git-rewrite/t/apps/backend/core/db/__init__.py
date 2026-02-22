"""Database Module.

Exports the Base class and session management utilities for SQLAlchemy ORM.
"""

from .base_class import Base

# Optional session imports - only import when needed
try:
    from apps.backend.core.db.session import (
        AsyncSessionLocal,
        SessionLocal,
        async_engine,
        async_session_factory,
        engine,
        get_async_db,
        get_db,
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
        ]
    )
