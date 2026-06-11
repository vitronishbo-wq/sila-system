"""Create missing DB tables for assistencia_social and educacao/search modules."""
import sys, os
sys.path.insert(0, '/home/dev03wsl/sila-system')
sys.path.insert(0, '/home/dev03wsl/sila-system/apps/backend')

os.environ['ENV_MODE'] = 'host'

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from apps.backend.app.core.settings import settings
from apps.backend.app.core.db import Base

# Import models to register them in Base.metadata
from apps.backend.app.modules.society.assistencia_social.infrastructure.models import *  # noqa
from apps.backend.app.modules.educacao.marketplace.search.infrastructure.adapters import *  # noqa

import asyncio

async def main():
    db_url = settings.DATABASE_URL
    print(f"DB URL: {db_url}")
    engine = create_async_engine(db_url, echo=False)
    
    async with engine.begin() as conn:
        existing = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        print(f"Existing tables ({len(existing)}): {sorted(existing)[:20]}...")
        
        missing = []
        for name, table in Base.metadata.tables.items():
            if name not in existing:
                missing.append(name)
        
        if missing:
            print(f"\nMissing tables ({len(missing)}): {sorted(missing)}")
            # Create ONLY the specific module tables we need
            assist_tables = [t for t in missing if 'assistencia' in t]
            search_tables = [t for t in missing if 'search' in t.lower() or 'marketplace_search' in t.lower()]
            need = assist_tables + search_tables
            
            if need:
                target = [Base.metadata.tables[n] for n in need]
                print(f"\nCreating {len(target)} tables: {need}")
                await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=target))
                print("Done!")
            else:
                print("\nNo assistencia or search tables to create")
                # Create ALL missing tables for demo completeness
                create_all = [Base.metadata.tables[n] for n in missing]
                await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=create_all))
                print(f"Created all {len(create_all)} missing tables")
        else:
            print("\nAll tables already exist!")
    
    await engine.dispose()

asyncio.run(main())
