import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def fix_schema():
    DATABASE_URL = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db"
    engine = create_async_engine(DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        try:
            # Drop the old table
            await conn.execute(text("DROP TABLE IF EXISTS event_store CASCADE;"))
            print("✓ Dropped old event_store table")
        except Exception as e:
            print(f"Warning: {e}")

    await engine.dispose()
    print("Schema cleanup complete - ready to recreate")


asyncio.run(fix_schema())
