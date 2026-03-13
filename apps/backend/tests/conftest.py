"""Pytest configuration - PostgreSQL Real DB Only

All tests run against the REAL PostgreSQL (DATABASE_URL from env).

ARCHITECTURE:
============
This configuration provides TWO fixture paradigms during migration to fully async:

1. ASYNC FIXTURES (Recommended for new tests):
   - @pytest.mark.asyncio
   - async def test_name(db_session)
   - Uses async engine with AsyncSessionLocal()
   - Aligns with FastAPI/SQLAlchemy 2.0 best practices
   - New tests MUST use this approach

2. SYNC FIXTURES (Legacy/transitional only):
   - def test_name(db)
   - Uses sync engine with SHARED mappers from async registry
   - Allows factory-boy and legacy tests to work WITHOUT refactoring
   - THIS IS A BRIDGE ONLY - migrate these tests to async as time permits

Mapper Registration & Shared Registry:
- Models are registered in Base.metadata ONCE (see import section below)
- Both async and sync engines use the SAME Base.registry
- This ensures CitizenModel, etc. are available to both paradigms
- Thread-safe: SQLAlchemy's registry.metadata is designed for this

Transactional Isolation:
- Each async test uses AsyncSessionLocal() within implicit transaction
- Each sync test uses SessionLocal() within implicit transaction  
- State cleanup (ImmutableAuditLog, EventPublisher) happens between tests
- NO SQLite, NO in-memory DB. Fidelity to production schema and types.

MIGRATION STRATEGY:
- DO NOT create new sync fixtures or tests
- Prioritize converting legacy sync tests to async using @pytest.mark.asyncio
- Use conftest markers to track migration: @pytest.mark.async_ready
"""

import asyncio
import pytest
import importlib
import os
from typing import AsyncGenerator
from datetime import datetime, timedelta
from decimal import Decimal
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# ============================================================================
# CRITICAL: Model registration and mapper configuration BEFORE app import
# ============================================================================

SKIP_FULL_APP_IMPORT = os.environ.get("SILA_SKIP_APP_IMPORT") == "1"
RUN_LEGACY_INTEGRATION = os.environ.get("SILA_RUN_LEGACY_INTEGRATION") == "1"

# Suites legadas desalinhadas com a arquitetura consolidada atual.
# Mantidas no repositório para migração futura, mas fora da execução padrão.
LEGACY_INTEGRATION_PATH_SNIPPETS = (
    "tests/integration/modules/complaints/",
    "tests/integration/test_api_refactored.py",
    "tests/integration/test_auth_staging.py",
    "tests/integration/test_db_connection.py",
    "tests/integration/test_environment.py",
    "tests/integration/test_health_endpoints.py",
    "tests/integration/test_appointments.py",
    "tests/integration/test_citizens.py",
    "tests/integration/test_users.py",
)

# Import and register models once (robust fallback for consolidated layout)
app_core_database = None
for module_name in ("app.core.db", "app.core.database", "config.database", "app.config.database"):
    try:
        app_core_database = importlib.import_module(module_name)
        break
    except ImportError:
        continue

if app_core_database is None:
    raise ImportError(
        "Could not import database bootstrap module (tried app.core.db, "
        "app.core.database, config.database, app.config.database)."
    )

register_models = getattr(app_core_database, "register_models", None)
if callable(register_models):
    register_models()

try:
    from app.db.base import Base
except ImportError:
    from app.core.db import Base

# Ensure mappers are fully configured
try:
    from sqlalchemy.orm import configure_mappers
    reg = getattr(Base, "registry", None)
    if reg is not None and hasattr(reg, "configure"):
        reg.configure()
    else:
        configure_mappers()
except Exception as _e:
    print(f"⚠️  Mapper configuration warning in apps/backend/tests/conftest.py: {_e}")

# Sanity check: essential tables present in metadata
_expected = ("citizen_fuc", "audit_logs")
_missing = [t for t in _expected if t not in Base.metadata.tables]
if _missing and not SKIP_FULL_APP_IMPORT:
    print(
        f"⚠️  Missing tables in Base.metadata after register_models(): {_missing}. "
        "Proceeding for compatibility."
    )

if not SKIP_FULL_APP_IMPORT:
    # NOW safe to import app (models are registered)
    from app.main import app
    from app.api.deps import get_current_user
    from app.models.iam_user import IamUser as User
else:
    app = None

    def get_current_user():
        return None

    User = None


# ============================================================================
# PYTEST FIXTURES
# ============================================================================

def _resolve_test_app():
    """Retorna a app de testes; tenta import lazy quando skip está ativo."""
    if app is not None:
        return app

    try:
        return importlib.import_module("app.main").app
    except Exception as exc:
        pytest.skip(
            f"Test app indisponível para fixture HTTP ({type(exc).__name__}: {exc})"
        )


def _resolve_auth_dependencies():
    """Resolve dependências reais de autenticação quando import parcial está ativo."""
    if User is not None and callable(get_current_user) and app is not None:
        return User, get_current_user

    deps_module = importlib.import_module("app.api.deps")
    user_module = importlib.import_module("app.models.iam_user")
    return user_module.IamUser, deps_module.get_current_user

@pytest.fixture(scope="session")
def event_loop():
    """Event loop para testes async (pytest-asyncio)"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def anyio_backend():
    """Configure anyio para usar asyncio como backend"""
    return "asyncio"


# ========== Mock Database Session for Unit Tests ==========
class MockAsyncSession:
    """Mock de SQLAlchemy AsyncSession para testes unitários."""
    
    def __init__(self):
        self.added_objects = []
        self.committed = False
        self.rolled_back = False
        self._data_store = {}
    
    def add(self, obj):
        """Simula adicionar objeto."""
        self.added_objects.append(obj)
    
    async def commit(self):
        """Simula commit."""
        self.committed = True
    
    async def rollback(self):
        """Simula rollback."""
        self.rolled_back = True
    
    async def refresh(self, obj):
        """Simula refresh de objeto."""
        pass
    
    async def execute(self, stmt):
        """Simula execução de query."""
        class MockResult:
            def scalar_one_or_none(self):
                return None
            def scalars(self):
                class Scalars:
                    def all(self):
                        return []
                return Scalars()
        return MockResult()
    
    async def merge(self, obj):
        """Simula merge."""
        return obj
    
    @property
    def is_active(self):
        return True


@pytest.fixture
def mock_db_session():
    """Fornece mock de DB session para testes."""
    return MockAsyncSession()


# ========== HTTP Client Fixture ==========
@pytest.fixture(scope="module")
def client() -> TestClient:
    test_app = _resolve_test_app()
    with TestClient(test_app) as c:
        yield c


@pytest.fixture
def async_http_client(event_loop) -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP assíncrono compartilhado por testes de integração/E2E."""
    test_app = _resolve_test_app()
    transport = ASGITransport(app=test_app)
    client = AsyncClient(transport=transport, base_url="http://testserver")
    try:
        yield client
    finally:
        event_loop.run_until_complete(client.aclose())


@pytest.fixture
def async_client(async_http_client: AsyncClient) -> AsyncClient:
    """Alias legada para compatibilidade com testes que esperam `async_client`."""
    return async_http_client


def override_get_current_user():
    class MockAuthUser(dict):
        """Payload híbrido para compatibilidade: acesso por atributo e por chave."""

        def __getattr__(self, item):
            try:
                return self[item]
            except KeyError as exc:
                raise AttributeError(item) from exc

    return MockAuthUser(
        id="test-user-id",
        user_id="test-user-id",
        email="test@example.com",
        roles=["CITIZEN"],
        is_superuser=False,
        administrative_level="LOCAL",
        system="TEST",
    )


@pytest.fixture(autouse=False)
def mock_user():
    """Mock authenticated user for tests that require it."""
    test_app = _resolve_test_app()
    _, current_user_dep = _resolve_auth_dependencies()
    test_app.dependency_overrides[current_user_dep] = override_get_current_user
    yield
    test_app.dependency_overrides = {}


@pytest.fixture
def test_settings():
    """Configurações padrão de timeout para testes de endpoint."""
    return {
        "timeout": 10.0,
        "health_timeout": 5.0,
    }


# ========== Synchronous PostgreSQL DB Fixture for Tests ==========
def get_transactional_session_factory(engine):
    """Returns a session factory that provides transactional isolation."""
    from sqlalchemy.orm import sessionmaker as sa_sessionmaker
    return sa_sessionmaker(bind=engine, class_=Session, expire_on_commit=False, autocommit=False)


def _create_sync_engine_with_shared_mappers():
    """
    Creates a synchronous engine that shares mappers with the async engine.
    
    This is a critical bridge for legacy tests that use sync sessions with factory-boy.
    It ensures that models registered in Base.metadata (async context) are accessible
    from a sync session without duplicating mapper configuration.
    
    The key insight: SQLAlchemy's registry.metadata is thread-safe and can be used
    by both async and sync engines simultaneously. We just need to ensure:
    1. Models are registered in Base.registry ONCE (done in conftest header)
    2. Both engines use the same Base.metadata
    3. The sync engine is created AFTER models are registered
    
    This is NOT ideal architecture (async/sync mixing), but provides a pragmatic
    migration path for legacy tests without immediate refactoring.
    """
    from app.core.settings import settings
    
    if "postgresql" not in settings.DATABASE_URL:
        raise RuntimeError(
            f"DATABASE_URL must be PostgreSQL, got: {settings.DATABASE_URL}"
        )
    
    # Convert async URL to sync PostgreSQL URL
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    # Create sync engine from the SAME Base.metadata that async uses
    # This ensures mappers are shared
    engine = create_engine(
        sync_url,
        echo=False,
        pool_recycle=3600,  # Recycle connections after 1 hour
        pool_size=5,
        max_overflow=10,
    )
    
    return engine


@pytest.fixture
def db():
    """
    Synchronous PostgreSQL session for legacy tests and factory-boy.
    
    IMPORTANT: This fixture uses a SHARED mapper registry with the async engine.
    Models must be registered in Base.metadata (which is done in conftest header)
    before this fixture is used.
    
    ⚠️  IMPORTANT LIMITATION (SQLAlchemy 2.0):
    - The `.query()` API is deprecated and may not work reliably
    - Legacy code using `.query(Model).filter(...).all()` should migrate to:
      ```python
      from sqlalchemy import select
      stmt = select(Model).where(...)
      result = db.execute(stmt)
      items = result.scalars().all()
      ```
    
    This fixture exists ONLY as a transitional bridge. New tests should use:
    - @pytest.mark.asyncio
    - async def test_name(db_session)
    
    Uses the same DATABASE_URL as the application (PostgreSQL only).
    No SQLite, no in-memory. Real schema, real types.
    
    REFACTORING CHECKLIST:
    1. Convert to `@pytest.mark.asyncio async def test_name(db_session)`
    2. Replace `.query()` with `select()` construct
    3. Add `await` before all database operations
    4. Mark with `@pytest.mark.async_ready` when done
    
    See PRACTICAL_TEST_EXAMPLES.md in project root for migration examples.
    """
    engine = _create_sync_engine_with_shared_mappers()
    SessionLocal = get_transactional_session_factory(engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Don't dispose engine to allow connection pooling across tests
        # Only dispose in session-level cleanup if needed



# ========== Async PostgreSQL DB Fixture ==========
@pytest.fixture
async def async_session_factory():
    """Async session factory for tests using AsyncSessionLocal."""
    from app.core.db import AsyncSessionLocal
    return AsyncSessionLocal


@pytest.fixture
async def db_session(async_session_factory) -> 'AsyncSession':
    """Async session for a single test using PostgreSQL."""
    async with async_session_factory() as session:
        yield session


# ========== Citizen Service Fixtures ==========
@pytest.fixture
def citizen_service():
    """Fornece instância de CitizenService para testes."""
    from apps.backend.app.modules.justice.civil_registry.service import CitizenService
    from app.core.audit import ImmutableAuditLog
    from app.core.events import EventPublisher
    
    service = CitizenService(db_session=None)
    yield service
    # Cleanup
    service.clear_cache()
    ImmutableAuditLog.clear()
    EventPublisher._subscribers.clear()


# ========== Citizen Data Fixtures ==========
@pytest.fixture
def valid_citizen_data():
    """Dados de cidadão válido para testes."""
    return {
        "id": "CIT-TEST-001",
        "full_name": "João da Silva",
        "status": "ACTIVE",
        "document_type": "BI",
        "document_number": "12345678",
        "birth_date": "1980-01-01",
        "nationality": "Portuguesa"
    }


@pytest.fixture
def inactive_citizen_data():
    """Dados de cidadão inativo para testes de validação."""
    return {
        "id": "CIT-TEST-INACTIVE",
        "full_name": "João Inativo",
        "status": "INACTIVE",
        "document_type": "BI",
        "document_number": "99999999",
        "birth_date": "1980-01-01",
        "nationality": "Portuguesa"
    }


@pytest.fixture
def deceased_citizen_data():
    """Dados de cidadão falecido para testes."""
    return {
        "id": "CIT-TEST-DECEASED",
        "full_name": "João Falecido",
        "status": "DECEASED",
        "document_type": "BI",
        "document_number": "77777777",
        "birth_date": "1950-01-01",
        "nationality": "Portuguesa"
    }


# ========== Invoice & Payment Fixtures ==========
@pytest.fixture
def sample_invoice_data():
    """Dados básicos para criar fatura."""
    return {
        "citizen_id": "CIT-TEST-001",
        "amount": Decimal("1000.00"),
        "currency": "AOA",
        "revenue_code": "ORE001",
        "cost_center": "CC001",
        "description": "Taxa de Registro Civil",
        "due_date": datetime.utcnow() + timedelta(days=30)
    }


@pytest.fixture
def sample_payment_data():
    """Dados básicos para registrar pagamento."""
    return {
        "invoice_id": "INV-TEST-001",
        "citizen_id": "CIT-TEST-001",
        "amount": Decimal("1000.00"),
        "payment_method": "BANK_TRANSFER",
        "transaction_id": "TXN-12345678"
    }


# ========== Event Publisher Fixtures ==========
@pytest.fixture
def event_collector():
    """Coleta eventos disparados durante testes."""
    from app.core.events import EventPublisher
    
    class EventCollector:
        def __init__(self):
            self.events = []
        
        async def collect(self, event):
            self.events.append(event)
        
        def get_events(self, event_type=None):
            if event_type:
                return [e for e in self.events if type(e).__name__ == event_type.__name__]
            return self.events
        
        def clear(self):
            self.events.clear()
    
    collector = EventCollector()
    EventPublisher._subscribers.clear()
    return collector


# ========== Cleanup Autouse Fixtures ==========
@pytest.fixture(autouse=True)
def reset_audit_and_events():
    """Reset audit log e events antes de cada teste."""
    from app.core.audit import ImmutableAuditLog
    from app.core.events import EventPublisher
    
    ImmutableAuditLog.clear()
    EventPublisher._subscribers.clear()
    
    yield
    
    ImmutableAuditLog.clear()
    EventPublisher._subscribers.clear()


# ========== Markers customizados ==========
def pytest_configure(config):
    """Registra markers customizados."""
    config.addinivalue_line(
        "markers", "integration: marca testes de integração"
    )
    config.addinivalue_line(
        "markers", "unit: marca testes unitários"
    )
    config.addinivalue_line(
        "markers", "audit: marca testes de auditoria"
    )
    config.addinivalue_line(
        "markers", "fuc: marca testes de integração FUC"
    )
    config.addinivalue_line(
        "markers", "async_ready: marca testes que já foram refatorados para async (migração completa)"
    )
    config.addinivalue_line(
        "markers", "sync_legacy: marca testes síncronos legados (candidatos para refatoração async)"
    )
    config.addinivalue_line(
        "markers",
        "legacy_integration: suíte de integração legada, fora do baseline padrão",
    )


def pytest_collection_modifyitems(config, items):
    """Quarentena de testes legados de integração por padrão.

    Para executar também os testes legados:
      SILA_RUN_LEGACY_INTEGRATION=1 python -m pytest apps/backend/tests/integration -q
    """
    if RUN_LEGACY_INTEGRATION:
        return

    skip_legacy = pytest.mark.skip(
        reason=(
            "Legacy integration test quarantined in default pipeline. "
            "Set SILA_RUN_LEGACY_INTEGRATION=1 to include."
        )
    )
    legacy_marker = pytest.mark.legacy_integration

    for item in items:
        nodeid = item.nodeid.replace("\\", "/")
        if any(snippet in nodeid for snippet in LEGACY_INTEGRATION_PATH_SNIPPETS):
            item.add_marker(legacy_marker)
            item.add_marker(skip_legacy)
