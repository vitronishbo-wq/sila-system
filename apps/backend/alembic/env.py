import os
import sys
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_engine_from_config

# Add backend directory to sys.path so imports work when running from backend directory
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.db import Base

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    return os.getenv("DATABASE_URL", "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db")

def run_migrations_offline():
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    from sqlalchemy.pool import NullPool
    connectable = async_engine_from_config(configuration, prefix="sqlalchemy.", poolclass=NullPool)
    
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def do_run_migrations(connection):
    # Alembic defaults `alembic_version.version_num` to VARCHAR(32), but this
    # repository uses longer revision IDs. Ensure capacity before running.
    with connection.begin():
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS alembic_version (
                    version_num VARCHAR(128) NOT NULL PRIMARY KEY
                )
                """
            )
        )
        connection.execute(
            text("ALTER TABLE alembic_version ALTER COLUMN version_num TYPE VARCHAR(128)")
        )

    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
