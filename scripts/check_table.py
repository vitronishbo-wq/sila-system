#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import asyncpg

from apps.backend.app.core.settings import settings


async def main():
    url = settings.DATABASE_URL
    print('Checking DB URL:', url)
    # Parse DSN for asyncpg
    dsn = url.replace('+asyncpg','')
    conn = await asyncpg.connect(dsn=dsn)
    try:
        row = await conn.fetchrow("SELECT to_regclass('public.educacao_institution_capacities') as exists")
        print('to_regclass result:', row)
        exists = row['exists']
        print('Table exists:', exists is not None)
    finally:
        await conn.close()

if __name__ == '__main__':
    asyncio.run(main())
