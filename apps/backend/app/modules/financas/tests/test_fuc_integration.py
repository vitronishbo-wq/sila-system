"""Testes da integração com FUC - casos de falha essenciais.

Refatorado para alinhar com o novo CitizenService (SILA-2026).
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.modules.financas.application.services.citizen_service import CitizenService
from app.citizen.enums import CitizenStatus
from app.core.audit import ImmutableAuditLog

@pytest.fixture
def citizen_service():
    """Fixture para o serviço de cidadão com cache limpo."""
    service = CitizenService()
    yield service
    service.invalidate_cache()
    ImmutableAuditLog.clear()

@pytest.mark.fuc
@pytest.mark.asyncio
async def test_validate_nonexistent_citizen(citizen_service, monkeypatch):
    """Deve rejeitar cidadão que não existe (via status simulado)."""
    # No novo CitizenService, o mock é feito via strings no ID se não houver DB
    result = await citizen_service.validate_for_billing("DECEASED_999")
    assert result is False

@pytest.mark.fuc
@pytest.mark.asyncio
async def test_validate_inactive_citizen(citizen_service):
    """Deve rejeitar cidadão inativo."""
    result = await citizen_service.validate_for_billing("INACTIVE_001")
    assert result is False

@pytest.mark.fuc
@pytest.mark.asyncio
async def test_validate_deceased_citizen(citizen_service):
    """Deve rejeitar cidadão falecido."""
    result = await citizen_service.validate_for_billing("DECEASED_001")
    assert result is False

@pytest.mark.fuc
@pytest.mark.asyncio
async def test_validate_suspended_citizen(citizen_service):
    """Deve rejeitar cidadão suspenso."""
    result = await citizen_service.validate_for_billing("SUSPENDED_001")
    assert result is False

@pytest.mark.fuc
@pytest.mark.asyncio
async def test_get_citizen_data_structure(citizen_service):
    """Verifica que dados de cidadão têm estrutura correta no novo modelo."""
    data = await citizen_service.get_citizen_data("CIT-TEST-001")
    
    assert "citizen_id" in data
    assert "full_name" in data
    assert "status" in data
    assert "is_eligible_for_finance" in data
    assert data["status"] == CitizenStatus.ACTIVE
    assert data["is_eligible_for_finance"] is True

@pytest.mark.fuc
@pytest.mark.asyncio
async def test_citizen_data_caching(citizen_service):
    """Dados de cidadão devem ser cacheados após primeira chamada."""
    citizen_id = "CIT-CACHE-TEST"
    
    # Primeira chamada (preenche cache)
    await citizen_service.get_citizen_data(citizen_id)
    
    # Verifica manualmente no cache interno
    assert citizen_id in citizen_service._cache
    assert citizen_service._cache[citizen_id]["data"]["citizen_id"] == citizen_id

@pytest.mark.fuc
@pytest.mark.audit
@pytest.mark.asyncio
async def test_failed_validation_audited(citizen_service):
    """
    Validação falhada deve ser registrada em auditoria.
    Nota: O mock do audit_log global é necessário se não houver DB.
    """
    mock_audit = AsyncMock()
    
    with patch("app.modules.financas.application.services.citizen_service.audit_log", new=mock_audit):
        # Injetamos um mock de DB para forçar a chamada ao audit_log
        citizen_service.db = MagicMock()
        
        result = await citizen_service.validate_for_billing("SUSPENDED_999")
        
        assert result is False
        mock_audit.assert_called_once()
        args, kwargs = mock_audit.call_args
        assert kwargs["action"] == "FINANCIAL_VALIDATION_FAILED"
        assert kwargs["resource_id"] == "SUSPENDED_999"
