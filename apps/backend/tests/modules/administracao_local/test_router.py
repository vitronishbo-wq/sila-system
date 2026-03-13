import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from unittest.mock import AsyncMock
from apps.backend.app.modules.governance.administracao_local.application.service import AdministracaoLocalService
from apps.backend.app.modules.governance.administracao_local.presentation.router import router
from apps.backend.app.modules.governance.administracao_local.presentation.dependencies import get_administracao_service
from apps.backend.app.modules.governance.administracao_local.domain.entities import AdministradorLocal

@pytest.fixture
def mock_service():
    return AsyncMock(spec=AdministracaoLocalService)

@pytest.fixture
def app(mock_service):
    _app = FastAPI()
    _app.include_router(router)
    # Override dependency to use mock
    _app.dependency_overrides[get_administracao_service] = lambda: mock_service
    return _app

def test_get_administrador_endpoint(app, mock_service):
    async def run_test():
        # Setup mock
        mock_service.get_administrador.return_value = AdministradorLocal(
            id="123", nome="Admin Teste", cargo="Tester"
        )
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/administracao-local/administradores/123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "123"
        assert data["nome"] == "Admin Teste"
    
    import asyncio
    asyncio.run(run_test())
