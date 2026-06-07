#!/usr/bin/env python3
import asyncio
import os
from pathlib import Path

# Ensure repo root is on sys.path so we can import the apps.backend package
ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "apps" / "backend"
os.chdir(BACKEND)
import sys

# Ensure both backend app package and repo root are importable
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(ROOT))

# Import the backend DB and ensure model modules are imported so metadata is
# registered on Base.metadata before calling create_all.
from apps.backend.app.core.db import Base, engine

try:
    import apps.backend.app.modules.educacao.infrastructure.models  # noqa: F401
except Exception as e:
    print("Warning: could not import educacao models:", e)

async def main():
    print("Connecting to DB and creating metadata tables (if missing)...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Schema creation complete.")

if __name__ == '__main__':
    asyncio.run(main())
