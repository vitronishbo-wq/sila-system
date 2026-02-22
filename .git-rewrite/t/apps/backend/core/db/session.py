"""Database Session Management.

Provides synchronous and asynchronous session factories, database engines,
and dependency injection utilities for FastAPI.

All database operations must use the appropriate session getter:
  - Sync context: Depends(get_db) → yields Session
  - Async context: Depends(get_async_db) → yields AsyncSession
"""

from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

# Import settings from the correct path
from core.config import settings

# ============================================================================
# DATABASE ENGINES & SESSION FACTORIES
# ============================================================================

# Synchronous and asynchronous engines. Creating engines may import DB drivers
# (psycopg2, asyncpg). If those drivers are not installed in the test/runtime
# environment we avoid raising at import time and create unbound sessionmakers
# so importing modules that reference `get_async_db` doesn't fail during tests.
try:
    # Synchronous engine
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=0,
    )

    SessionLocal: sessionmaker[Session] = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    # Asynchronous engine
    async_engine = create_async_engine(
        settings.ASYNC_DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=0,
    )

    async_session_factory: sessionmaker[AsyncSession] = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
except Exception:
    # Fallback placeholders: sessionmakers without an engine bind. These will
    # raise if used at runtime, but allow tests that only import modules to
    # complete without requiring DB driver packages to be installed.
    engine = None
    SessionLocal = sessionmaker()
    async_engine = None
    async_session_factory = sessionmaker(class_=AsyncSession)

# Alias for backward compatibility
AsyncSessionLocal = async_session_factory

# ============================================================================
# DEPENDENCY INJECTION UTILITIES FOR FASTAPI
# ============================================================================


def get_db() -> Generator[Session, None, None]:
    """Get synchronous database session for FastAPI dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get asynchronous database session for FastAPI dependency injection."""
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
