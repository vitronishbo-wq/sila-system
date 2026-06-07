"""Quick DB schema check."""
import asyncio, os
os.environ["DATABASE_URL"] = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db"
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def main():
    engine = create_async_engine(os.environ["DATABASE_URL"])
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT column_name, data_type, is_nullable "
            "FROM information_schema.columns "
            "WHERE table_name = 'educacao_student_number_counters' "
            "ORDER BY ordinal_position"
        ))
        for row in result:
            print(f"{row[0]}: {row[1]} nullable={row[2]}")
    await engine.dispose()

asyncio.run(main())
