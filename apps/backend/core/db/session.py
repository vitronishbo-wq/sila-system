from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Engine assíncrono centralizado
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Função padrão (usada pela maioria dos módulos novos)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Alias explícito para compatibilidade com módulos legados (payment, notifications, etc.)
get_async_db = get_db
async_session_factory = AsyncSessionLocal
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
SessionLocal = AsyncSessionLocal
engine = async_engine
