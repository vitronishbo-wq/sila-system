"""
Central pytest configuration for SILA Backend - PHASE 3
======================================================

ÚNICO arquivo de configuração para TODOS os testes.
Centraliza:
- Python path setup
- Environment configuration
- Shared fixtures
- Database setup
- HTTP clients

OBJETIVO: Eliminar conflitos e duplicação de 28+ conftest.py espalhados
"""

import sys
import os
from pathlib import Path
import pytest
import asyncio
from typing import AsyncGenerator, Generator
import logging

# ============================================================================
# 1. PATH CONFIGURATION (Executado PRIMEIRO)
# ============================================================================

BACKEND_DIR = Path(__file__).parent.resolve()

# Add to sys.path FIRST, before any other imports
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Also add parent for accessing 'apps.backend'
if str(BACKEND_DIR.parent) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR.parent))


# ============================================================================
# 2. ENVIRONMENT SETUP
# ============================================================================


def pytest_configure(config):
    """
    Pytest hook - executado antes da coleta de testes.
    Configurar environment, logging, e markers.
    """
    # Ensure backend is in path
    if str(BACKEND_DIR) not in sys.path:
        sys.path.insert(0, str(BACKEND_DIR))

    # Load test environment from .env.test if available
    env_test_file = Path(__file__).parent.parent.parent / ".env.test"
    if env_test_file.exists():
        from dotenv import load_dotenv

        load_dotenv(env_test_file)

    # Test environment variables (override with .env.test values if available)
    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://localhost/sila_test")
    os.environ.setdefault("ASYNC_DATABASE_URL", "postgresql+asyncpg://localhost/sila_test")
    os.environ.setdefault("LOG_LEVEL", "DEBUG")
    os.environ.setdefault("SKIP_EXTERNAL_API", "true")
    os.environ.setdefault("DEBUG", "true")
    os.environ.setdefault("PYTHONPATH", str(BACKEND_DIR))

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Register markers
    config.addinivalue_line("markers", "unit: Unit tests (isolated functions)")
    config.addinivalue_line(
        "markers", "integration: Integration tests (with DB/services)"
    )
    config.addinivalue_line("markers", "e2e: End-to-end tests (full flows)")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "requires_db: Tests requiring database")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests."""
    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://localhost/sila_test")
    os.environ.setdefault("ASYNC_DATABASE_URL", "postgresql+asyncpg://localhost/sila_test")
    yield


# ============================================================================
# 3. EVENT LOOP (para testes async)
# ============================================================================


@pytest.fixture(scope="session")
def event_loop():
    """
    Create event loop for entire test session.
    Permite usar @pytest.mark.asyncio nos testes.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop
    loop.close()


# ============================================================================
# 4. SESSION-LEVEL FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def test_settings():
    """Test configuration constants"""
    return {
        "timeout": 30,
        "retry_attempts": 3,
        "expected_status_codes": [200, 201, 202, 204],
        "database_url": "postgresql+asyncpg://localhost/sila_test",
        "async_database_url": "postgresql+asyncpg://sila_user:Truman1%2AMarcelo1%2A@localhost:5432/sila_test",
    }


@pytest.fixture(scope="session")
def backend_dir():
    """Get backend directory path"""
    return BACKEND_DIR


# ============================================================================
# 5. SAMPLE DATA FIXTURES
# ============================================================================


@pytest.fixture
def sample_payment_data():
    """Sample payment data for tests"""
    return {
        "amount": 100.0,
        "currency": "AOA",
        "method": "bna",
        "description": "Test payment",
        "status": "pending",
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for tests"""
    return {
        "email": "test@sila.co.ao",
        "username": "testuser",
        "full_name": "Test User",
        "id": 1,
    }


@pytest.fixture
def sample_payment_create():
    """Pydantic PaymentCreate model for tests"""
    from modules.payment.schemas.payment import PaymentCreate
    from modules.payment.models.enums import PaymentMethod

    return PaymentCreate(
        amount=150.00,
        currency="AOA",
        method=PaymentMethod.BNA,
        description="Test payment creation",
    )


# ============================================================================
# 6. HTTP CLIENT FIXTURES
# ============================================================================


@pytest.fixture
def base_url() -> str:
    """Base URL for API tests"""
    return "http://localhost:8004"


try:
    import httpx

    @pytest.fixture
    def http_client(base_url: str) -> Generator[httpx.Client, None, None]:
        """Synchronous HTTP client for API tests"""
        with httpx.Client(base_url=base_url, timeout=30.0) as client:
            yield client

    @pytest.fixture
    async def async_http_client(
        base_url: str,
    ) -> AsyncGenerator[httpx.AsyncClient, None]:
        """Asynchronous HTTP client for API tests"""
        async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
            yield client

except ImportError:
    pass  # httpx not installed


# ============================================================================
# 7. MODULES LIST FIXTURES
# ============================================================================


@pytest.fixture
def expected_modules():
    """List of modules that should exist in the system"""
    return [
        "auth",
        "payment",
        "citizenship",
        "health",
        "finance",
        "justice",
        "commercial",
        "education",
        "urbanism",
        "social",
        "documents",
        "registry",
        "address",
        "monitoring",
        "integration",
        "service_hub",
        "complaints",
        "common",
    ]


@pytest.fixture
def critical_modules():
    """Modules that MUST be tested and working"""
    return ["auth", "payment", "citizenship", "service_hub"]
