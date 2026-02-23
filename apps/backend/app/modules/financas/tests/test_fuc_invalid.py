"""
Testes para validação obrigatória de FUC.
Garante que invoices NUNCA podem ser criadas sem validação FUC.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.modules.financas.application.services.invoice_service import InvoiceService
from app.modules.financas.api.schemas.invoice_schema import CreateInvoiceSchema
from app.modules.financas.exceptions import DomainValidationError
from app.modules.financas.application.services.citizen_service import CitizenService


@pytest.mark.asyncio
async def test_create_invoice_fuc_invalid():
    """Invoice NUNCA deve ser criada com cidadão inválido (FUC)."""
    mock_repo = MagicMock()

    with patch('app.modules.financas.application.services.invoice_service.FUCClient') as mock_fuc_class:
        mock_fuc = MagicMock()
        mock_fuc.validate_citizen = AsyncMock(return_value=False)
        mock_fuc_class.return_value = mock_fuc

        service = InvoiceService(mock_repo)

        with pytest.raises(DomainValidationError):
            await service.create_invoice(CreateInvoiceSchema(
                citizen_id="INVALID_CITIZEN_ID",
                revenue_code="1.1.1.1",
                cost_center="MINFIN",
                service_code="SERV001",
                service_name="Test Service",
                amount=1000.00,
                currency="AOA",
                due_date="2026-03-10"
            ))

    mock_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_create_invoice_fuc_valid():
    """Invoice pode ser criada se FUC validation passar."""
    mock_repo = MagicMock()
    mock_invoice = MagicMock()
    mock_repo.create = AsyncMock(return_value=mock_invoice)

    with patch('app.modules.financas.application.services.invoice_service.FUCClient') as mock_fuc_class:
        mock_fuc = MagicMock()
        mock_fuc.validate_citizen = AsyncMock(return_value=True)
        mock_fuc_class.return_value = mock_fuc

        service = InvoiceService(mock_repo)

        result = await service.create_invoice(CreateInvoiceSchema(
            citizen_id="VALID_CITIZEN_ID",
            revenue_code="1.1.1.1",
            cost_center="MINFIN",
            service_code="SERV001",
            service_name="Test Service",
            amount=1000.00,
            currency="AOA",
            due_date="2026-03-10"
        ))

    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_citizen_service_validate_nonexistent():
    """CitizenService.validate_for_billing retorna False para cidadão inexistente (simulado)."""
    service = CitizenService()
    # No novo service, IDs com DECEASED/INACTIVE/SUSPENDED retornam False
    result = await service.validate_for_billing("INACTIVE_000")
    assert result is False


@pytest.mark.asyncio
async def test_citizen_service_validate_inactive(monkeypatch):
    """CitizenService rejeita cidadão com status INACTIVE."""
    from app.citizen.enums import CitizenStatus

    service = CitizenService()

    async def mock_get_citizen_data(citizen_id):
        return {"citizen_id": citizen_id, "status": CitizenStatus.INACTIVE, "full_name": "Exemplo"}

    monkeypatch.setattr(service, "get_citizen_data", mock_get_citizen_data)

    result = await service.validate_for_billing("cit_001")
    assert result is False
