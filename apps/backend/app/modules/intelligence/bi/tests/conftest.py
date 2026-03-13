from __future__ import annotations
import pytest_asyncio
from sqlalchemy.orm import configure_mappers
from apps.backend.app.domain.db import AsyncSessionLocal, register_models
from apps.backend.app.db.base import Base
register_models()
reg = getattr(Base, 'registry', None)
if reg is not None and hasattr(reg, 'configure'):
    reg.configure()
else:
    configure_mappers()

@pytest_asyncio.fixture
async def db_session():
    """Sessao async real para os testes ORM do modulo BI."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()