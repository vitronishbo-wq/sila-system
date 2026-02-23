"""Core database - SOLUÇÃO DEFINITIVA"""
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
import logging
import os

logger = logging.getLogger(__name__)

# Detectar configuração
db_url = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
)

engine = create_async_engine(db_url, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Base compartilhada
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@asynccontextmanager
async def get_transaction():
    """Transaction context manager"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Alias compatibilidade (CRÍTICO para imports faltantes)
importAsyncSessionLocal = AsyncSessionLocal
