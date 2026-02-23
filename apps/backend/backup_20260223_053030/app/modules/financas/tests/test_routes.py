import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import MagicMock, AsyncMock
from app.modules.financas.application.api.routes import router
from app.api.deps import get_current_user, get_db
from fastapi import FastAPI

# Mock user for tests
mock_user = MagicMock()
mock_user.id = "test-user"
mock_user.username = "testuser"
mock_user.email = "test@example.com"
mock_user.role = "admin_central"
mock_user.citizen_id = "CIT-123"

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_get_invoice_not_found():
    # Mock do DB
    mock_db = AsyncMock()
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Mock execute result para retornar vazio
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result
            
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/financas/invoices/non_existent_id")
    
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"]
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_list_citizen_invoices_empty():
    mock_db = AsyncMock()
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Mock execute result
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_db.execute.return_value = mock_result
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/financas/invoices/citizen/CIT-123")
        
    assert response.status_code == 200
    assert response.json() == []
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_invoice_forbidden_for_other_citizen():
    """Cidadão não pode ver fatura de outro cidadão."""
    mock_db = AsyncMock()
    
    # User é cidadão
    mock_citizen = MagicMock()
    mock_citizen.role = "citizen"
    mock_citizen.citizen_id = "CIT-MY-OWN"
    
    app.dependency_overrides[get_current_user] = lambda: mock_citizen
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Mock da fatura de OUTRO cidadão
    from app.modules.financas.infrastructure.models.invoice_model import InvoiceModel
    from app.modules.financas.domain.models.enums import InvoiceStatus
    from datetime import datetime
    
    mock_invoice_model = InvoiceModel(
        id="inv-other",
        citizen_id="CIT-OTHER",
        reference="REF-OTHER",
        revenue_code="1.1",
        cost_center="CC",
        service_code="S",
        service_name="S",
        amount=100.0,
        currency="AOA",
        due_date=datetime.now(),
        status=InvoiceStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_invoice_model
    mock_db.execute.return_value = mock_result
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/financas/invoices/inv-other")
    
    assert response.status_code == 403
    assert "Acesso negado" in response.json()["detail"]
    
    app.dependency_overrides.clear()