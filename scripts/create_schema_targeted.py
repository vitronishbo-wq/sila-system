#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / 'apps' / 'backend'
# Make both backend package and repo root importable
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(ROOT))

from sqlalchemy.ext.asyncio import create_async_engine

# Import models to ensure they are registered on Base.metadata
import apps.backend.app.modules.educacao.infrastructure.models  # noqa: F401
from apps.backend.app.core.db import Base
from apps.backend.app.core.settings import settings


async def main():
    print('Using DATABASE_URL:', settings.DATABASE_URL)
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print('Targeted schema creation complete')

if __name__ == '__main__':
    asyncio.run(main())
