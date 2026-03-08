"""Core Database - SINGLE SOURCE OF TRUTH"""
from typing import AsyncGenerator, Optional, Any
from contextlib import asynccontextmanager
import logging
import os
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine
)
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy import text, Column, Integer, DateTime, String, Boolean
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Configuração centralizada do banco"""
    url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db"
    )
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "20"))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    pool_pre_ping: bool = True
    pool_recycle: int = 3600
    echo: bool = os.getenv("DB_ECHO", "false").lower() == "true"

class Database:
    """Singleton Database Manager"""
    _instance: Optional['Database'] = None
    _engine: Optional[AsyncEngine] = None
    _session_factory: Optional[async_sessionmaker] = None
    
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
            self._engine = create_async_engine(
                self.config.url,
                echo=self.config.echo,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_pre_ping=self.config.pool_pre_ping,
                pool_recycle=self.config.pool_recycle
            )
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
                autoflush=False
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

# Base Model com convenções automáticas
class CoreBase:
    """Base class com convenções automáticas"""
    
    @declared_attr
    def __tablename__(cls):
        """Gera nome da tabela automaticamente"""
        import re
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        if name.endswith('_model'):
            name = name[:-6]
        return name
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(50), nullable=True)
    updated_by = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

Base = declarative_base(cls=CoreBase)

# Singleton instance
db = Database()
engine = db.engine

# Aliases para compatibilidade
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency injection"""
    async for session in db.get_session():
        yield session

get_session = get_db
transaction = db.transaction
AsyncSessionLocal = db.session_factory
importAsyncSessionLocal = db.session_factory
async_session_factory = db.session_factory
get_async_db = get_db


def get_engine() -> AsyncEngine:
    """Compatibility helper for scripts/tests expecting an engine getter."""
    return db.engine


def register_models() -> None:
    """Compatibility hook for suites that force metadata registration."""
    # Lazy import to avoid circular dependencies at module import time.
    import app.db.base  # noqa: F401


__all__ = [
    'Base',
    'db',
    'engine',
    'get_db',
    'get_session',
    'get_async_db',
    'transaction',
    'AsyncSessionLocal',
    'async_session_factory',
    'importAsyncSessionLocal',
    'get_engine',
    'register_models',
    'Database',
    'DatabaseConfig',
    'CoreBase'
]
