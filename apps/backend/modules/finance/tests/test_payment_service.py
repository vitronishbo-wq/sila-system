import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.modules.financas.application.services.payment_service import PaymentService
from app.modules.financas.schemas.payment_schema import CreatePaymentSchema
from app.modules.financas.exceptions import DuplicatePaymentError, InvoiceNotFoundError
from app.modules.financas.domain.models.enums import PaymentStatus, InvoiceStatus
from app.modules.financas.domain.models.invoice import Invoice
from datetime import datetime, timezone, timedelta

@pytest.mark.asyncio
async def test_register_payment_duplicate_reference():
    mock_payment_repo = AsyncMock() # Use AsyncMock for the repo
    mock_invoice_repo = AsyncMock()
    service = PaymentService(mock_payment_repo, mock_invoice_repo)
    
    # Simular que a referência já existe
    mock_payment_repo.exists_by_gateway_ref.return_value = True
    
    data = CreatePaymentSchema(
        invoice_id="inv_123",
        citizen_id="cit_123",
        amount=1000.0,
        payment_method="MULTICAIXA",
        gateway_reference="EXT-REF-DUP"
    )
    
    with pytest.raises(DuplicatePaymentError):
        await service.register_payment(data)

@pytest.mark.asyncio
async def test_register_payment_invoice_not_found():
    mock_payment_repo = AsyncMock()
    mock_invoice_repo = AsyncMock()
    service = PaymentService(mock_payment_repo, mock_invoice_repo)
    
    mock_payment_repo.exists_by_gateway_ref.return_value = False
    mock_invoice_repo.get_by_id.return_value = None
    
    data = CreatePaymentSchema(
        invoice_id="invalid_id",
        citizen_id="cit_123",
        amount=1000.0,
        payment_method="MULTICAIXA",
        gateway_reference="EXT-REF-NEW"
    )
    
    with pytest.raises(InvoiceNotFoundError):
        await service.register_payment(data)

@pytest.mark.asyncio
async def test_register_payment_success():
    """Teste de sucesso garantindo mudança de estado da invoice."""
    mock_payment_repo = AsyncMock()
    mock_invoice_repo = AsyncMock()
    service = PaymentService(mock_payment_repo, mock_invoice_repo)
    
    mock_payment_repo.exists_by_gateway_ref.return_value = False
    
    # Criar invoice pendente
    invoice = Invoice(
        id="inv_123",
        citizen_id="cit_123",
        reference="SILA-REF",
        revenue_code="1.1",
        cost_center="CC",
        service_code="S",
        service_name="S",
        amount=1000.0,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        status=InvoiceStatus.PENDING
    )
    mock_invoice_repo.get_by_id.return_value = invoice
    mock_payment_repo.create.return_value = MagicMock(id="pay_123")
    
    data = CreatePaymentSchema(
        invoice_id="inv_123",
        citizen_id="cit_123",
        amount=1000.0,
        payment_method="MULTICAIXA",
        gateway_reference="EXT-REF-OK"
    )
    
    result = await service.register_payment(data)
    
    assert invoice.status == InvoiceStatus.PAID
    mock_invoice_repo.save.assert_called_once()
    mock_payment_repo.create.assert_called_once()
    assert result.id == "pay_123"