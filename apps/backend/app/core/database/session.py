from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
DATABASE_URL = 'postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_db'
engine = create_async_engine(DATABASE_URL, pool_size=50, max_overflow=100, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)