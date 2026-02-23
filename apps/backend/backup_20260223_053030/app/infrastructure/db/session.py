from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/sila_system"

# Use NullPool to avoid keeping connections bound to an event loop across test
# boundaries which can cause "Future attached to a different loop" errors.
engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
