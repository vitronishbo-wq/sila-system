"""Core Database - SINGLE SOURCE OF TRUTH"""

import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from apps.backend.app.core.settings import settings
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)


@dataclass
class DatabaseConfig:
    """Configuração centralizada do banco"""

    url: str = settings.DATABASE_URL
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "20"))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    pool_pre_ping: bool = True
    pool_recycle: int = 3600
    echo: bool = os.getenv("DB_ECHO", "false").lower() == "true"


class Database:
    """Singleton Database Manager"""

    _instance: Optional["Database"] = None
    _engine: AsyncEngine | None = None
    _session_factory: async_sessionmaker | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.config = DatabaseConfig()
        self.logger = logging.getLogger(f"{__name__}.Database")
        self._engine = None
        self._session_factory = None

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            engine_kwargs = {
                "echo": self.config.echo,
                "pool_pre_ping": self.config.pool_pre_ping,
                "poolclass": NullPool,
            }
            self._engine = create_async_engine(self.config.url, **engine_kwargs)
            self.logger.info("✅ Database engine initialized")
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker:
        if self._session_factory is None:
            self._session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
        return self._session_factory

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """FastAPI dependency - get async session"""
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    @asynccontextmanager
    async def transaction(self):
        """Context manager for transactions"""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def health_check(self) -> bool:
        """Database health check"""
        try:
            async with self.session_factory() as session:
                await session.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as e:
            self.logger.error(f"Database health check failed: {e}")
            return False

    async def close(self):
        """Close all connections"""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
            self.logger.info("Database connections closed")


class CoreBase:
    """Base class com convenções automáticas"""

    @declared_attr
    def __tablename__(cls):
        """Gera nome da tabela automaticamente"""
        import re

        name = re.sub("(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        if name.endswith("_model"):
            name = name[:-6]
        return name

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        table_args = getattr(cls, "__table_args__", None)
        if table_args is None:
            cls.__table_args__ = {"extend_existing": True}
            return
        if isinstance(table_args, dict):
            table_args.setdefault("extend_existing", True)
            return
        if isinstance(table_args, tuple):
            if table_args and isinstance(table_args[-1], dict):
                last_args = dict(table_args[-1])
                last_args.setdefault("extend_existing", True)
                cls.__table_args__ = (*table_args[:-1], last_args)
            else:
                cls.__table_args__ = (*table_args, {"extend_existing": True})

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(50), nullable=True)
    updated_by = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


Base = declarative_base(cls=CoreBase)
db = Database()
engine = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency injection"""
    async for session in db.get_session():
        yield session


get_session = get_db
transaction = db.transaction


def AsyncSessionLocal(*args, **kwargs):
    """Lazy wrapper that returns a new AsyncSession from the session factory."""

    return db.session_factory(*args, **kwargs)


def importAsyncSessionLocal(*args, **kwargs):
    """Backward-compatible alias that lazily returns a session."""
    return db.session_factory(*args, **kwargs)


def async_session_factory():
    """Return the async_sessionmaker lazily (call to get factory)."""
    return db.session_factory


get_async_db = get_db


def get_engine() -> AsyncEngine:
    """Compatibility helper for scripts/tests expecting an engine getter."""
    return db.engine


def register_models() -> None:
    """Compatibility hook for suites that force metadata registration."""
    import apps.backend.app.db.base
    import apps.backend.app.db.registry


__all__ = [
    "Base",
    "db",
    "engine",
    "get_db",
    "get_session",
    "get_async_db",
    "transaction",
    "AsyncSessionLocal",
    "async_session_factory",
    "importAsyncSessionLocal",
    "get_engine",
    "register_models",
    "Database",
    "DatabaseConfig",
    "CoreBase",
]
