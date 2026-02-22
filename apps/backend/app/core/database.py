from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.core.settings import settings

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import citizen/territory models (these should NOT cause circular imports)
from app.citizen.core import models  # noqa
from app.core.territory.models import territory  # noqa

# Create engine BEFORE loading app.db.base to avoid circular imports
# When app.db.base is imported, it will trigger module imports that may depend on get_db
engine = create_async_engine(
    settings.DATABASE_URL, echo=False, poolclass=NullPool
)
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, autocommit=False
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

# Alias for get_session (MUST be defined before importing app.db.base)
get_db = get_session

__all__ = ["get_db", "get_session", "engine", "AsyncSessionLocal", "Base"]


def register_models() -> None:
    """Lazily import and register all model modules.

    Importing `app.db.base` at module import time can cause circular import
    issues and duplicate class registration during pytest collection. Call
    this function early during app startup to ensure models are registered
    exactly once.
    """
    # Import inside function to avoid top-level side-effects
    try:
        import app.db.base  # noqa: F401 - module import registers models
    except Exception:
        # Import failures should propagate in runtime, but during test collection
        # it's safer to surface them explicitly.
        raise

# NOTE: Removed SQLite compatibility shims. Tests must run against Postgres
# and the application should not rely on SQLite fallbacks. If SQLite support
# is required in the future, add explicit, audited shims here.
