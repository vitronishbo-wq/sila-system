"""
Testes de proteção contra replay attacks em webhooks.
Garante que webhooks fora da janela temporal são rejeitados.
"""
import pytest
from unittest.mock import MagicMock, AsyncMock
from app.modules.financas.integrations.webhook_handler import WebhookHandler
from datetime import datetime, timezone, timedelta
import json
import hmac
import hashlib


@pytest.mark.asyncio
async def test_webhook_replay_old_timestamp():
    """Webhook com timestamp muito antigo deve ser rejeitado (replay attack)."""
    mock_payment_repo = MagicMock()
    mock_invoice_repo = MagicMock()
    handler = WebhookHandler(mock_payment_repo, mock_invoice_repo)
    
    # Timestamp de 1 hora atrás
    old_timestamp = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    
    payload = {
        "event": "payment.success",
        "timestamp": old_timestamp,
        "nonce": "nonce_123",
        "data": {
            "invoice_id": "inv_123",
            "amount": 1000.00,
            "gateway_reference": "gw_ref",
        }
    }
    
    payload_str = json.dumps({k: v for k, v in payload.items() if k != "signature"}, sort_keys=True, separators=(",", ":"))
    signature = "sha256=" + hmac.new(b"your_webhook_secret_key", payload_str.encode(), hashlib.sha256).hexdigest()
    
    result = await handler.process_gateway_notification(payload, signature)
    
    # Deve rejeitar (timestamp fora da janela)
    assert result is False
    mock_payment_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_webhook_replay_future_timestamp():
    """Webhook com timestamp no futuro deve ser rejeitado."""
    mock_payment_repo = MagicMock()
    mock_invoice_repo = MagicMock()
    handler = WebhookHandler(mock_payment_repo, mock_invoice_repo)
    
    # Timestamp 1 hora no futuro
    future_timestamp = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    
    payload = {
        "event": "payment.success",
        "timestamp": future_timestamp,
        "nonce": "nonce_456",
        "data": {
            "invoice_id": "inv_123",
            "amount": 1000.00,
            "gateway_reference": "gw_ref",
        }
    }
    
    payload_str = json.dumps({k: v for k, v in payload.items() if k != "signature"}, sort_keys=True, separators=(",", ":"))
    signature = "sha256=" + hmac.new(b"your_webhook_secret_key", payload_str.encode(), hashlib.sha256).hexdigest()
    
    result = await handler.process_gateway_notification(payload, signature)
    
    # Deve rejeitar (timestamp inválido)
    assert result is False


@pytest.mark.asyncio
async def test_webhook_hmac_invalid_signature():
    """Webhook com assinatura HMAC inválida deve ser rejeitado."""
    mock_payment_repo = MagicMock()
    mock_invoice_repo = MagicMock()
    handler = WebhookHandler(mock_payment_repo, mock_invoice_repo)
    
    now = datetime.now(timezone.utc).isoformat()
    
    payload = {
        "event": "payment.success",
        "timestamp": now,
        "nonce": "nonce_789",
        "data": {
            "invoice_id": "inv_123",
            "amount": 1000.00,
            "gateway_reference": "gw_ref",
        }
    }
    
    # Assinatura inválida/fake
    invalid_signature = "sha256=invalid_hex_digest_here_123456789"
    
    result = await handler.process_gateway_notification(payload, invalid_signature)
    
    # Deve rejeitar (assinatura inválida)
    assert result is False
    mock_payment_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_webhook_tampered_payload():
    """Webhook com payload modificado deve falhar validação HMAC."""
    mock_payment_repo = MagicMock()
    mock_invoice_repo = MagicMock()
    handler = WebhookHandler(mock_payment_repo, mock_invoice_repo)
    
    now = datetime.now(timezone.utc).isoformat()
    
    payload_original = {
        "event": "payment.success",
        "timestamp": now,
        "nonce": "nonce_999",
        "data": {
            "invoice_id": "inv_123",
            "amount": 1000.00,
            "gateway_reference": "gw_ref",
        }
    }
    
    # Calcular assinatura para payload original
    payload_str = json.dumps({k: v for k, v in payload_original.items() if k != "signature"}, sort_keys=True, separators=(",", ":"))
    signature = "sha256=" + hmac.new(b"your_webhook_secret_key", payload_str.encode(), hashlib.sha256).hexdigest()
    
    # TAMPAR: modificar o amount no payload
    payload_tampered = payload_original.copy()
    payload_tampered["data"]["amount"] = 9999.99  # Valor alterado!
    
    result = await handler.process_gateway_notification(payload_tampered, signature)
    
    # Deve rejeitar (assinatura não corresponde ao payload modificado)
    assert result is False
    mock_payment_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_webhook_requires_timestamp():
    """Webhook sem timestamp deve ser rejeitado."""
    mock_payment_repo = MagicMock()
    mock_invoice_repo = MagicMock()
    handler = WebhookHandler(mock_payment_repo, mock_invoice_repo)
    
    payload = {
        "event": "payment.success",
        # FALTA: "timestamp": "..."
        "nonce": "nonce_aaa",
        "data": {
            "invoice_id": "inv_123",
            "amount": 1000.00,
            "gateway_reference": "gw_ref",
        }
    }
    
    payload_str = json.dumps({k: v for k, v in payload.items() if k != "signature"}, sort_keys=True, separators=(",", ":"))
    signature = "sha256=" + hmac.new(b"your_webhook_secret_key", payload_str.encode(), hashlib.sha256).hexdigest()
    
    result = await handler.process_gateway_notification(payload, signature)
    
    # Deve rejeitar (timestamp obrigatório)
    assert result is False
