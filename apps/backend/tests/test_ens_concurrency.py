"""
ENS Concurrency Test — TASK-072

Verifies that ENS-YYYY-XXXXXXXX number generation produces 0 duplicates
under concurrent load of 100, 1000, and 10000 parallel creations.

Uses PostgreSQL's ON CONFLICT / RETURNING for atomicity.
"""

import asyncio
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db")

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from apps.backend.app.modules.educacao.application.student_number_generator import StudentNumberGenerator


async def test_concurrent_ens(count: int) -> dict:
    engine = create_async_engine(os.environ["DATABASE_URL"], pool_size=20, max_overflow=40)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    sem = asyncio.Semaphore(60)

    async def generate_one() -> str | None:
        async with sem:
            try:
                async with session_factory() as session:
                    gen = StudentNumberGenerator(session)
                    ns = await gen.generate()
                    await session.commit()
                    return ns
            except Exception as e:
                return f"ERROR: {e}"

    start = datetime.now(timezone.utc)
    tasks = [generate_one() for _ in range(count)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()

    numbers = [r for r in results if isinstance(r, str) and not r.startswith("ERROR")]
    errors = [r for r in results if isinstance(r, Exception) or (isinstance(r, str) and r.startswith("ERROR"))]
    error_types = {}
    for e in errors:
        key = str(e).split("ERROR: ")[1].split("(")[0].strip()[:80] if "ERROR: " in str(e) else str(e)[:80]
        error_types[key] = error_types.get(key, 0) + 1
    duplicates = len(numbers) - len(set(numbers)) if numbers else 0

    await engine.dispose()

    return {
        "count": count,
        "generated": len(numbers),
        "unique": len(set(numbers)) if numbers else 0,
        "duplicates": duplicates,
        "errors": len(errors),
        "error_types": error_types,
        "elapsed_seconds": round(elapsed, 3),
        "rate_per_second": round(len(numbers) / elapsed, 1) if elapsed > 0 else 0,
        "pass": duplicates == 0 and len(errors) == 0,
    }


async def main():
    print("=" * 60)
    print("ENS CONCURRENCY TEST — TASK-072")
    print("=" * 60)

    for count in [100, 1000, 10000]:
        print(f"\n--- Testing {count} concurrent generations ---")
        result = await test_concurrent_ens(count)
        status = "PASS" if result["pass"] else "FAIL"
        print(f"  Generated: {result['generated']}")
        print(f"  Unique:    {result['unique']}")
        print(f"  Duplicates: {result['duplicates']}")
        print(f"  Errors:    {result['errors']}")
        if result['error_types']:
            for k, v in sorted(result['error_types'].items(), key=lambda x: -x[1])[:5]:
                print(f"    {k}: {v}")
        print(f"  Time:      {result['elapsed_seconds']}s ({result['rate_per_second']}/s)")
        print(f"  Status:    {status}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
