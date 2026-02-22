from sqlalchemy import inspect as sa_inspect
from app.core.database import engine
import asyncio

async def check():
    async with engine.connect() as conn:
        def _inspect(sync_conn):
            insp = sa_inspect(sync_conn)
            cols = insp.get_columns("citizen_fuc")
            for c in cols:
                print(f"  {c['name']}: {c['type']}")
        await conn.run_sync(_inspect)

asyncio.run(check())
