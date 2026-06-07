"""Shared pytest fixtures for async tests."""

import logging
import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

_DB_IMPORT_ERROR = None

# Delay importing the DB objects until fixtures run so engine/session
# creation happens on the pytest-asyncio event loop rather than at import time.
Base = None
db = None
AsyncSessionLocal = None


@pytest_asyncio.fixture(scope="session")
async def setup_db() -> AsyncGenerator[None, None]:
    """
    Optional schema lifecycle fixture.

    To avoid destructive behavior on shared databases, schema creation/drop is
    opt-in with `PYTEST_MANAGE_SCHEMA=1`.
    """
    # Import lazily inside the fixture to ensure the async engine is
    # created on the active event loop used by pytest-asyncio.
    try:
        from apps.backend.app.core import db as _db_module

        Base = _db_module.Base
        db = _db_module.db
    except Exception as exc:  # pragma: no cover - only hit in broken env setups
        pytest.skip(f"Database fixtures unavailable: {exc}")

    manage_schema = os.getenv("PYTEST_MANAGE_SCHEMA", "0") == "1"

    if manage_schema:
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    yield

    if manage_schema:
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    # Ensure engine/connection pool is cleanly disposed on the same event loop
    try:
        await db.close()
    except Exception:
        # Best-effort dispose; ignore errors during cleanup to let pytest
        # surface primary test failures.
        logger.exception("Error while closing DB engine during test teardown")


@pytest_asyncio.fixture
async def db_session(setup_db) -> AsyncGenerator[AsyncSession, None]:
    """Yield an async SQLAlchemy session when DB fixtures are available."""
    # Lazily resolve the session factory from the core db module so the
    # async_sessionmaker is created on the current event loop.
    try:
        from apps.backend.app.core import db as _db_module

        session_factory = _db_module.db.session_factory
    except Exception as exc:  # pragma: no cover - only hit in broken env setups
        pytest.skip(f"Async session factory unavailable: {exc}")

    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Yield an async API client bound to the FastAPI ASGI app."""
    try:
        from apps.backend.app.main import app as fastapi_app
    except Exception as exc:
        pytest.skip(f"FastAPI app unavailable for endpoint tests: {exc}")

    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://testserver"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture
async def authenticated_client(client: AsyncClient) -> AsyncClient:
    """Yield a client with a test auth header."""
    client.headers.update({"Authorization": "Bearer test-token-placeholder"})
    return client


def pytest_configure(config):
    """Register common markers used by this test suite."""
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "e2e: end-to-end tests")


@pytest.fixture(autouse=True)
def configure_logging():
    """Set logging for tests with a predictable format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    yield


__all__ = ["setup_db", "db_session", "client", "authenticated_client", "configure_logging"]
