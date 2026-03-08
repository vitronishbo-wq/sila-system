from app.core.db import AsyncSessionLocal, Base, db, get_db

engine = db.engine


async def get_session():
    async for session in get_db():
        yield session


def register_models() -> None:
    # Lazy import to avoid circular dependencies at module import time.
    import app.db.base  # noqa: F401


__all__ = [
    "Base",
    "engine",
    "AsyncSessionLocal",
    "get_db",
    "get_session",
    "register_models",
]
