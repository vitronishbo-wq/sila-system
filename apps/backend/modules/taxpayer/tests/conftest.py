import pytest
import asyncio
from typing import Generator, AsyncGenerator, Dict, Any
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from unittest.mock import Mock, AsyncMock

from ....main import app
from ....core.database import Base, get_db
from ....core.config import settings


# Database de teste
TEST_DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/sila_test"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    """Override da dependência get_db para testes"""
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    """Cria event loop para testes assíncronos"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Configura banco de dados para testes"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fixture para sessão do banco"""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def async_client() -> AsyncGenerator:
    """Fixture para cliente HTTP assíncrono"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def test_user() -> Dict[str, Any]:
    """Fixture para usuário de teste"""
    return {
        "id": str(uuid4()),
        "username": "test_user",
        "email": "test@example.com",
        "roles": ["operator"],
        "permissions": ["taxpayer:view", "taxpayer:create"],
        "is_superuser": False
    }


@pytest.fixture
def admin_user() -> Dict[str, Any]:
    """Fixture para administrador de teste"""
    return {
        "id": str(uuid4()),
        "username": "admin",
        "email": "admin@sila.gov.ao",
        "roles": ["admin"],
        "permissions": ["*"],
        "is_superuser": True
    }


@pytest.fixture
def mock_agt_client():
    """Fixture para cliente AGT mockado"""
    client = AsyncMock()
    client.validate_nif = AsyncMock(return_value=True)
    client.get_taxpayer_data = AsyncMock(return_value={
        "name": "Empresa Teste",
        "email": "empresa@teste.ao"
    })
    client.get_tax_debts = AsyncMock(return_value=[])
    client.submit_declaration = AsyncMock(return_value="PROTOCOL-123")
    return client


@pytest.fixture
def mock_cache():
    """Fixture para cache mockado"""
    class MockCache:
        def __init__(self):
            self._store = {}
        
        async def get(self, key):
            return self._store.get(key)
        
        async def set(self, key, value, ttl=None):
            self._store[key] = value
            return True
        
        async def delete(self, key):
            if key in self._store:
                del self._store[key]
            return True
        
        async def clear(self):
            self._store.clear()
    
    return MockCache()


@pytest.fixture
def mock_notification():
    """Fixture para notificação mockada"""
    class MockNotification:
        def __init__(self):
            self.sent = []
        
        async def notify_taxpayer(self, *args, **kwargs):
            self.sent.append(("taxpayer", args, kwargs))
        
        async def notify_admin(self, *args, **kwargs):
            self.sent.append(("admin", args, kwargs))
        
        async def send_email(self, *args, **kwargs):
            self.sent.append(("email", args, kwargs))
    
    return MockNotification()


@pytest.fixture
def mock_audit():
    """Fixture para auditoria mockada"""
    class MockAudit:
        def __init__(self):
            self.logs = []
        
        async def log(self, *args, **kwargs):
            self.logs.append((args, kwargs))
        
        async def get_logs(self):
            return self.logs
    
    return MockAudit()
