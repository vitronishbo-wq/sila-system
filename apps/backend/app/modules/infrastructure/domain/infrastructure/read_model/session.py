from __future__ import annotations
import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from app.core.settings import settings
READ_DATABASE_URL = os.environ.get('READ_DATABASE_URL', settings.DATABASE_URL)
if READ_DATABASE_URL.startswith('postgresql://'):
    READ_DATABASE_URL = READ_DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)
read_engine = create_async_engine(READ_DATABASE_URL, echo=False, poolclass=NullPool)
ReadAsyncSessionLocal = async_sessionmaker(read_engine, expire_on_commit=False, autocommit=False)

async def get_read_session():
    async with ReadAsyncSessionLocal() as session:
        yield session