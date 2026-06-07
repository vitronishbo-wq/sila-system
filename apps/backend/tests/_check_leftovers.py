import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def main():
    e = create_async_engine("postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db")
    async with e.connect() as c:
        r = await c.execute(text("SELECT full_name, national_student_number FROM educacao_academic_identities ORDER BY created_at"))
        for row in r:
            print(f"  {row[0]:40s} {row[1]}")
        r2 = await c.execute(text("SELECT COUNT(*) FROM educacao_academic_identities"))
        print(f"\nTotal: {r2.fetchone()[0]}")
    await e.dispose()

asyncio.run(main())
