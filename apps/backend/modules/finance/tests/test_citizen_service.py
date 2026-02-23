"""
Testes unitários para CitizenService (Refatorados).
Valida get_citizen_data e validate_for_billing com cenários de sucesso e falha.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.modules.financas.application.services.citizen_service import CitizenService
from app.citizen.enums import CitizenStatus
from app.citizen.exceptions import CitizenNotFoundError


@pytest.mark.asyncio
async def test_get_citizen_data_returns_valid_structure():
    """get_citizen_data deve retornar dicionário com citizen_id, full_name e status."""
    service = CitizenService()
    data = await service.get_citizen_data("cit_123")

    assert "citizen_id" in data
    assert "full_name" in data
    assert "status" in data
    assert data["citizen_id"] == "cit_123"
    assert data["status"] == CitizenStatus.ACTIVE


@pytest.mark.asyncio
async def test_get_citizen_data_not_found():
    """get_citizen_data deve lançar CitizenNotFoundError para ID vazio (regra do novo service)."""
    service = CitizenService()

    with pytest.raises(CitizenNotFoundError):
        await service.get_citizen_data("")


@pytest.mark.asyncio
async def test_validate_active_citizen():
    """Cidadão ACTIVE deve passar validação."""
    service = CitizenService()
    result = await service.validate_for_billing("cit_active_001")
    assert result is True


@pytest.mark.asyncio
async def test_validate_deceased_citizen():
    """Cidadão DECEASED não deve passar validação."""
    service = CitizenService()
    result = await service.validate_for_billing("DECEASED_001")
    assert result is False


@pytest.mark.asyncio
async def test_validate_suspended_citizen():
    """Cidadão SUSPENDED não deve passar validação."""
    service = CitizenService()
    result = await service.validate_for_billing("SUSPENDED_001")
    assert result is False


@pytest.mark.asyncio
async def test_validate_citizen_with_monkeypatch(monkeypatch):
    """Teste com mock de get_citizen_data retornando status INACTIVE."""
    service = CitizenService()

    async def mock_get_citizen_data(citizen_id):
        return {"citizen_id": citizen_id, "status": CitizenStatus.INACTIVE, "full_name": "Exemplo"}

    monkeypatch.setattr(service, "get_citizen_data", mock_get_citizen_data)
    result = await service.validate_for_billing("cit_001")
    assert result is False
