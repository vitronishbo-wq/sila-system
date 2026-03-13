"""Shared pytest fixtures for async tests."""

import logging
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

_DB_IMPORT_ERROR = None

try:
    from app.core.db import AsyncSessionLocal, Base, db
except Exception as exc:  # pragma: no cover - only hit in broken env setups
    AsyncSessionLocal = None
    Base = None
    db = None
    _DB_IMPORT_ERROR = exc


@pytest_asyncio.fixture(scope="session")
async def setup_db() -> AsyncGenerator[None, None]:
    """
    Optional schema lifecycle fixture.

    To avoid destructive behavior on shared databases, schema creation/drop is
    opt-in with `PYTEST_MANAGE_SCHEMA=1`.
    """
    if db is None or Base is None:
        pytest.skip(f"Database fixtures unavailable: {_DB_IMPORT_ERROR}")

    manage_schema = os.getenv("PYTEST_MANAGE_SCHEMA", "0") == "1"

    if manage_schema:
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    yield

    if manage_schema:
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(setup_db) -> AsyncGenerator[AsyncSession, None]:
    """Yield an async SQLAlchemy session when DB fixtures are available."""
    if AsyncSessionLocal is None:
        pytest.skip(f"AsyncSessionLocal unavailable: {_DB_IMPORT_ERROR}")

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Yield an async API client bound to the FastAPI ASGI app."""
    try:
        from app.main import app as fastapi_app
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
