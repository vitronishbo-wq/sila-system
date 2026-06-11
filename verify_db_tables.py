
import psycopg2
import os

try:
    conn = psycopg2.connect(
        dbname="sila_db",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name LIKE 'educacao_%'
    """)
    tables = cursor.fetchall()
    print("Tabelas de educação encontradas:")
    for table in tables:
        print(table[0])
    print(f"Total: {len(tables)} tabelas")
except Exception as e:
    print(f"Erro ao conectar ou consultar o banco de dados: {e}")
finally:
    if 'conn' in locals() and conn is not None:
        conn.close()
