import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 1. Importa a Base e o Modelo para o Alembic "vê-los"
from config.database import Base
from config.settings import settings
from modules.identity.models.user import User # Garante o registro do modelo

# Configuração de log do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Define o Target Metadata para Autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Executa migrações em modo 'offline'."""
    url = settings.ASYNC_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Executa migrações em modo 'online' (Assíncrono)."""
    
    # Força a URL correta do settings se não estiver no alembic.ini
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.ASYNC_DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())