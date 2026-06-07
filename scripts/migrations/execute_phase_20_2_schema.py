#!/usr/bin/env python3
import argparse
import os
import sys

import psycopg2


class Phase20_2SchemaExecutor:
    def __init__(
        self,
        host="localhost",
        user="sila_user",
        password="Trumanmarcelo_1983",
        dbname="sila_db",
        port=5432,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                dbname=self.dbname,
                port=self.port,
            )
            print("✓ Database connection successful")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False

    def execute_schema(self):
        try:
            if not os.path.exists("schema_phase_20_2.sql"):
                print("✗ schema_phase_20_2.sql not found")
                return False

            with open("schema_phase_20_2.sql") as f:
                schema_sql = f.read()

            cursor = self.conn.cursor()
            cursor.execute(schema_sql)
            self.conn.commit()
            cursor.close()
            print("✓ Schema created successfully")
            return True
        except Exception as e:
            print(f"✗ Schema execution failed: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 20.2 Schema Executor")
    parser.add_argument("--host", default="localhost", help="Database host")
    parser.add_argument("--user", default="sila_user", help="Database user")
    parser.add_argument("--password", default="Trumanmarcelo_1983", help="Database password")
    parser.add_argument("--dbname", default="sila_db", help="Database name")
    parser.add_argument("--port", type=int, default=5432, help="Database port")

    args = parser.parse_args()

    executor = Phase20_2SchemaExecutor(
        host=args.host, user=args.user, password=args.password, dbname=args.dbname, port=args.port
    )

    if executor.connect():
        executor.execute_schema()
        executor.close()
        sys.exit(0)
    else:
        sys.exit(1)
