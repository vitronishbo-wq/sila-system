import pytest
from unittest.mock import AsyncMock, MagicMock
from app.modules.financas.integrations.webhook_handler import WebhookHandler
from app.modules.financas.domain.models.enums import InvoiceStatus
from app.modules.financas.domain.models.invoice import Invoice
from datetime import datetime, timezone, timedelta
import json

@pytest.mark.asyncio
async def test_payment_idempotency_duplicate_nonce():
    """Pagamento com nonce duplicado deve ser idempotente (retorna sucesso sem reprocessar)."""
    # Mock repositories
    mock_payment_repo = MagicMock()
    mock_invoice_repo = MagicMock()
    
    # Criar uma Invoice real para o domínio
    invoice = Invoice(
        id="inv_123",
        citizen_id="cit_456",
        reference="SILA-2024-TEST",
        revenue_code="1.1",
        cost_center="CC",
        service_code="S",
        service_name="S",
        amount=1000.00,
        currency="AOA",
        due_date=datetime.now(timezone.utc) + timedelta(days=30),
        status=InvoiceStatus.PENDING
    )
    
    mock_invoice_repo.get_by_id = AsyncMock(return_value=invoice)
    mock_invoice_repo.save = AsyncMock(return_value=invoice)
    
    # Payment mock
    mock_payment_repo.create = AsyncMock(return_value=MagicMock())
    
    # Webhook handler
    handler = WebhookHandler(mock_payment_repo, mock_invoice_repo)
    
    # Payload do webhook
    now = datetime.now(timezone.utc).isoformat()
    nonce = "unique_nonce_12345"
    
    payload = {
        "event": "payment.success",
        "timestamp": now,
        "nonce": nonce,
        "data": {
            "invoice_id": "inv_123",
            "citizen_id": "cit_456",
            "amount": 1000.00,
            "currency": "AOA",
            "gateway_reference": "gw_ref_789",
            "provider": "MultiCaixa"
        }
    }
    
    # Calcular assinatura
    import hmac
    import hashlib
    payload_str = json.dumps({k: v for k, v in payload.items() if k != "signature"}, sort_keys=True, separators=(",", ":"))
    signature = "sha256=" + hmac.new(
        b"your_webhook_secret_key",
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Primeira chamada — processar normalmente
    result1 = await handler.process_gateway_notification(payload, signature)
    assert result1 is True
    mock_payment_repo.create.assert_called_once()
    assert invoice.status == InvoiceStatus.PAID
    
    # Segunda chamada com mesmo nonce — deve ser idempotente
    result2 = await handler.process_gateway_notification(payload, signature)
    assert result2 is True  # Retorna sucesso
    # Mas create() NÃO deve ser chamado de novo
    mock_payment_repo.create.assert_called_once()  # Ainda 1, não 2

@pytest.mark.asyncio
async def test_payment_requires_idempotency_key():
    """Pagamento SEM nonce deve ser rejeitado."""
    mock_payment_repo = MagicMock()
    mock_invoice_repo = MagicMock()
    handler = WebhookHandler(mock_payment_repo, mock_invoice_repo)
    
    now = datetime.now(timezone.utc).isoformat()
    
    payload = {
        "event": "payment.success",
        "timestamp": now,
        "data": {
            "invoice_id": "inv_123",
            "citizen_id": "cit_456",
            "amount": 1000.00,
            "gateway_reference": "gw_ref_789",
        }
    }
    
    import hmac
    import hashlib
    payload_str = json.dumps({k: v for k, v in payload.items() if k != "signature"}, sort_keys=True, separators=(",", ":"))
    signature = "sha256=" + hmac.new(
        b"your_webhook_secret_key",
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()
    
    result = await handler.process_gateway_notification(payload, signature)
    
    assert result is False
    mock_payment_repo.create.assert_not_called()
