"""Shared DB exports for platform modules.

This module re-exports the core database objects to keep a single source of truth.
"""
from app.core.db import (
    Base,
    AsyncSessionLocal,
    async_session_factory,
    db,
    engine,
    get_async_db,
    get_db,
    get_engine,
    get_session,
    register_models,
    transaction,
)

__all__ = [
    "Base",
    "AsyncSessionLocal",
    "async_session_factory",
    "db",
    "engine",
    "get_async_db",
    "get_db",
    "get_engine",
    "get_session",
    "register_models",
    "transaction",
]
