#!/usr/bin/env python3
"""
Simple schema inspection using psycopg2
"""

import psycopg2
import os
from pathlib import Path

# Get credentials
DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "sila_db")
DB_USER = os.getenv("POSTGRES_USER", "sila_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Trumanmarcelo_1983")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    cursor = conn.cursor()
    
    print("\n" + "="*100)
    print("📊 DATABASE SCHEMA INSPECTION")
    print("="*100)
    
    # Get tables
    cursor.execute("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname='public' 
        ORDER BY tablename;
    """)
    
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n📋 Tables found: {len(tables)}\n")
    
    for i, table in enumerate(tables, 1):
        print(f"\n{i}️⃣  TABLE: {table.upper()}")
        print("-" * 100)
        
        # Get columns
        cursor.execute(f"""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, (table,))
        
        for col_name, col_type, nullable, default in cursor.fetchall():
            null_str = "✓" if nullable == "YES" else "✗"
            default_str = default if default else ""
            print(f"  {col_name:30} {col_type:25} NULL:{null_str} DEFAULT:{default_str}")
        
        # Get foreign keys
        cursor.execute(f"""
            SELECT 
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s;
        """, (table,))
        
        fks = cursor.fetchall()
        if fks:
            print("\n  🔗 Foreign Keys:")
            for col, fk_table, fk_col in fks:
                print(f"     • {col} → {fk_table}.{fk_col}")
    
    print("\n" + "="*100)
    print(f"✅ TOTAL TABLES: {len(tables)}")
    print("="*100)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
