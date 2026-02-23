#!/usr/bin/env python3
"""
Inspect actual PostgreSQL schema and compare with SQLAlchemy models
"""

import asyncio
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "apps" / "backend"
os.chdir(backend_path)

from app.core.settings import settings
from sqlalchemy import text, inspect as sql_inspect
from sqlalchemy.ext.asyncio import create_async_engine

async def inspect_schema():
    """Inspect database schema"""
    
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    
    try:
        async with engine.connect() as conn:
            # Get all tables
            result = await conn.execute(text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname='public' 
                ORDER BY tablename;
            """))
            
            tables = [row[0] for row in result.fetchall()]
            
            print("\n" + "="*100)
            print("📊 DATABASE SCHEMA INSPECTION")
            print("="*100)
            print(f"\n📋 Tables found: {len(tables)}\n")
            
            for i, table in enumerate(tables, 1):
                # Get columns for each table
                col_result = await conn.execute(text(f"""
                    SELECT 
                        column_name,
                        data_type,
                        is_nullable,
                        column_default
                    FROM information_schema.columns 
                    WHERE table_name = '{table}'
                    ORDER BY ordinal_position;
                """))
                
                columns = col_result.fetchall()
                print(f"\n{i}️⃣  TABLE: {table.upper()}")
                print("-" * 100)
                
                for col in columns:
                    col_name, col_type, nullable, default = col
                    null_str = "✓" if nullable == "YES" else "✗"
                    default_str = default if default else ""
                    print(f"  {col_name:30} {col_type:25} NULL:{null_str} DEFAULT:{default_str}")
                
                # Get foreign keys
                fk_result = await conn.execute(text(f"""
                    SELECT 
                        constraint_name,
                        column_name,
                        foreign_table_name,
                        foreign_column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.table_name='{table}' AND tc.constraint_type='FOREIGN KEY';
                """))
                
                fks = fk_result.fetchall()
                if fks:
                    print("\n  🔗 Foreign Keys:")
                    for fk in fks:
                        constraint, col, fk_table, fk_col = fk
                        print(f"     • {col} → {fk_table}.{fk_col}")
            
            print("\n" + "="*100)
            print(f"✅ TOTAL TABLES: {len(tables)}")
            print("="*100)
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(inspect_schema())
