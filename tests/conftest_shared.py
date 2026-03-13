"""
Shared test fixtures and utilities for SILA system tests.
Consolidates common fixtures, mocks, and database setup across all test files.
"""

import pytest
import asyncio
import logging
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db_config():
    """Test database configuration."""
    return {
        'user': 'sila_user',
        'password': 'Trumanmarcelo_1983',
        'host': 'localhost',
        'port': 5432,
        'database': 'sila_db_test'
    }


@pytest.fixture
async def test_db_engine(test_db_config) -> AsyncEngine:
    """Create test database engine."""
    url = f"postgresql+asyncpg://{test_db_config['user']}:{test_db_config['password']}@{test_db_config['host']}:{test_db_config['port']}/{test_db_config['database']}"
    engine = create_async_engine(url, echo=False, pool_pre_ping=True)
    
    logger.info(f"Created test engine for {test_db_config['host']}:{test_db_config['port']}/{test_db_config['database']}")
    
    yield engine
    
    await engine.dispose()
    logger.info("Disposed test engine")


@pytest.fixture
async def test_db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session_maker = sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session
        await session.rollback()


# ============================================================================
# MOCK DATA FIXTURES
# ============================================================================

@pytest.fixture
def admin_user_data():
    """Mock admin user data."""
    return {
        'email': 'admin.test@sila.gov.ao',
        'full_name': 'Test Admin',
        'password_hash': '$2b$12$hashedpasswordfortesting',
        'roles': '["ADMIN"]',
        'administrative_level': 'SUPER',
        'region_id': None
    }


@pytest.fixture
def manager_user_data():
    """Mock manager user data."""
    return {
        'email': 'manager.test@sila.gov.ao',
        'full_name': 'Test Manager',
        'password_hash': '$2b$12$hashedpasswordfortesting',
        'roles': '["MANAGER"]',
        'administrative_level': 'PROVINCIAL',
        'region_id': 1  # Huambo
    }


@pytest.fixture
def citizen_user_data():
    """Mock citizen user data."""
    return {
        'email': 'citizen.test@sila.gov.ao',
        'full_name': 'Test Citizen',
        'password_hash': '$2b$12$hashedpasswordfortesting',
        'roles': '["CITIZEN"]',
        'administrative_level': 'CITIZEN',
        'bi_number': 'BI123456789'
    }


@pytest.fixture
def province_data():
    """Mock province data (Huambo)."""
    return {
        'name': 'Huambo',
        'code': 'HA',
        'type': 'province'
    }


@pytest.fixture
def municipality_data(province_data):
    """Mock municipality data."""
    return {
        'name': 'Huambo (city)',
        'code': 'HM01',
        'type': 'municipality',
        'parent_name': province_data['name']
    }


@pytest.fixture
def commune_data(municipality_data):
    """Mock commune data."""
    return {
        'name': 'Bailundo',
        'code': 'CO01',
        'type': 'commune',
        'parent_name': municipality_data['name']
    }


# ============================================================================
# API CLIENT FIXTURES (for endpoint tests)
# ============================================================================

@pytest.fixture
def mock_http_client():
    """Mock HTTP client for endpoint testing."""
    import httpx
    return httpx.AsyncClient()


@pytest.fixture
def api_base_url():
    """Base API URL for tests."""
    return "http://localhost:8000/api/v1"


@pytest.fixture
def jwt_token_admin():
    """Mock JWT token for admin user."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbi50ZXN0QHNpbGEuZ292LmFvIiwicm9sZXMiOlsiQURNSU4iXSwiZXhwIjo5OTk5OTk5OTk5fQ.ADMIN_TOKEN_MOCK"


@pytest.fixture
def jwt_token_manager():
    """Mock JWT token for manager user."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYW5hZ2VyLnRlc3RAc2lsYS5nb3YuYW8iLCJyb2xlcyI6WyJNQU5BR0VSIl0sImV4cCI6OTk5OTk5OTk5OX0.MANAGER_TOKEN_MOCK"


@pytest.fixture
def jwt_token_citizen():
    """Mock JWT token for citizen user."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjaXRpemVuLnRlc3RAc2lsYS5nb3YuYW8iLCJyb2xlcyI6WyJDSVRJWkVOIl0sImV4cCI6OTk5OTk5OTk5OX0.CITIZEN_TOKEN_MOCK"


# ============================================================================
# MARKER DEFINITIONS
# ============================================================================

def pytest_configure(config):
    """Register pytest markers."""
    config.addinivalue_line(
        "markers", "hierarchy: Mark test as hierarchy-related"
    )
    config.addinivalue_line(
        "markers", "territory: Mark test as territory/citizen-related"
    )
    config.addinivalue_line(
        "markers", "database: Mark test as database integrity test"
    )
    config.addinivalue_line(
        "markers", "integration: Mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: Mark test as slow running"
    )
