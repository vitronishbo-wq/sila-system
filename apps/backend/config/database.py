from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config.settings import settings

# Motor de conexão assíncrona com otimização de Pool
# Usa o driver asyncpg (postgresql+asyncpg://...) definido no seu .env
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verifica se a conexão caiu antes de cada operação
    future=True
)

# Fábrica de sessões assíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Definição Moderna da Base Declarativa (SQLAlchemy 2.0+)
class Base(DeclarativeBase):
    pass

# Dependência para injeção de dependência no FastAPI e Scripts
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Alias para compatibilidade
get_db = get_session