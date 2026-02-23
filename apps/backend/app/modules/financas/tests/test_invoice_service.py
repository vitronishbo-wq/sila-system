"""
Testes de integração InvoiceService ↔ CitizenService (FUC).
Garante que a criação de invoice respeita a validação FUC obrigatória.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta, timezone

from app.modules.financas.application.services.invoice_service import InvoiceService
from app.modules.financas.api.schemas.invoice_schema import CreateInvoiceSchema
from app.modules.financas.domain.models.invoice import Invoice
from app.modules.financas.domain.models.enums import InvoiceStatus
from app.modules.financas.exceptions import DomainValidationError, InvalidInvoiceStateError, FUCError


@pytest.mark.asyncio
async def test_create_invoice_success_with_fuc():
    """Invoice criada com sucesso quando FUC validation passa."""
    mock_repo = MagicMock()
    # No novo modelo, create retorna a entidade
    mock_invoice = MagicMock(spec=Invoice)
    mock_invoice.reference = "SILA-2024-TEST"
    mock_invoice.id = "123"
    mock_repo.create = AsyncMock(return_value=mock_invoice)

    with patch('app.modules.financas.application.services.invoice_service.FUCClient') as mock_fuc_class:
        mock_fuc = MagicMock()
        mock_fuc.validate_citizen = AsyncMock(return_value=True)
        mock_fuc_class.return_value = mock_fuc

        service = InvoiceService(mock_repo)

        result = await service.create_invoice(CreateInvoiceSchema(
            citizen_id="BI123456",
            service_code="REG_CIVIL",
            service_name="Assento de Nascimento",
            revenue_code="1.2.1.0.1",
            cost_center="MINIC-01",
            amount=2500.0,
            currency="AOA",
            due_date=datetime.now(timezone.utc) + timedelta(days=30)
        ))

    mock_repo.create.assert_called_once()
    assert result.reference == "SILA-2024-TEST"


@pytest.mark.asyncio
async def test_create_invoice_blocked_by_fuc():
    """Invoice NUNCA deve ser criada quando FUC rejeita o cidadão."""
    mock_repo = MagicMock()

    with patch('app.modules.financas.application.services.invoice_service.FUCClient') as mock_fuc_class:
        mock_fuc = MagicMock()
        mock_fuc.validate_citizen = AsyncMock(return_value=False)
        mock_fuc_class.return_value = mock_fuc

        service = InvoiceService(mock_repo)

        with pytest.raises(DomainValidationError, match="não habilitado para emissão"):
            await service.create_invoice(CreateInvoiceSchema(
                citizen_id="cit_999_bloqueado",
                revenue_code="1.1.1.1",
                cost_center="MINFIN",
                service_code="SERV001",
                service_name="Serviço Teste",
                amount=100.00,
                currency="AOA",
                due_date=datetime.now(timezone.utc) + timedelta(days=15)
            ))

    mock_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_create_invoice_fuc_error_propagates():
    """Se a validação FUC falhar com excepção, deve propagar como FUCError."""
    mock_repo = MagicMock()

    with patch('app.modules.financas.application.services.invoice_service.FUCClient') as mock_fuc_class:
        mock_fuc = MagicMock()
        mock_fuc.validate_citizen = AsyncMock(side_effect=Exception("FUC connection error"))
        mock_fuc_class.return_value = mock_fuc

        service = InvoiceService(mock_repo)

        with pytest.raises(FUCError, match="Serviço de validação de identidade indisponível"):
            await service.create_invoice(CreateInvoiceSchema(
                citizen_id="BI999999",
                revenue_code="1.1.1.1",
                cost_center="MINFIN",
                service_code="SERV002",
                service_name="Serviço Teste 2",
                amount=500.00,
                currency="AOA",
                due_date=datetime.now(timezone.utc) + timedelta(days=30)
            ))

    mock_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_cancel_paid_invoice_fails():
    """Não se pode cancelar uma fatura já paga."""
    mock_repo = MagicMock()
    mock_repo.save = AsyncMock()
    service = InvoiceService(mock_repo)

    # Criar uma fatura real para testar regras de negócio
    invoice = Invoice(
        id="inv_123",
        citizen_id="BI123",
        reference="REF-1",
        revenue_code="1.1",
        cost_center="C-1",
        service_code="S-1",
        service_name="S1",
        amount=100.0,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        status=InvoiceStatus.PAID
    )
    
    service.repository.get_by_id = AsyncMock(return_value=invoice)

    with pytest.raises(InvalidInvoiceStateError):
        await service.cancel_invoice("inv_123")
    
    mock_repo.save.assert_not_called()