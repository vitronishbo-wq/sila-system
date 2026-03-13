"""Tests for PaymentWebhookService with isolated dependencies."""

import hashlib
import hmac
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from apps.backend.app.modules.payment.models.enums import PaymentStatus
from apps.backend.app.modules.payment.services.webhook_service import PaymentWebhookService


@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    session.execute = AsyncMock(return_value=mock_result)
    session._mock_scalars = mock_scalars
    return session


@pytest.fixture
def mock_payment_service():
    return AsyncMock()


@pytest.fixture
def webhook_service(mock_db_session, mock_payment_service):
    service = PaymentWebhookService(db=mock_db_session, payment_service=mock_payment_service)
    service._log_event = AsyncMock(return_value=SimpleNamespace(id=999))
    return service


@pytest.mark.asyncio
async def test_process_webhook_success(webhook_service, mock_db_session, mock_payment_service):
    secret = "secret123"
    webhook_id = 1
    reference = "PAY-123"

    payload_dict = {
        "event": "payment.completed",
        "data": {"reference": reference, "status": "completed", "provider_id": "PROV-999"},
    }
    payload_body = json.dumps(payload_dict).encode()
    signature = hmac.new(secret.encode(), payload_body, hashlib.sha256).hexdigest()
    headers = {"X-Signature": signature}

    mock_config = SimpleNamespace(id=webhook_id, active=True, secret_key=secret)
    mock_payment = SimpleNamespace(id=10, reference=reference, status=PaymentStatus.PENDING)
    mock_db_session._mock_scalars.first.side_effect = [mock_config, mock_payment]

    result = await webhook_service.process_webhook(webhook_id, payload_body, headers)

    assert result["status"] == "success"
    mock_payment_service.update_payment_status.assert_awaited_once_with(
        payment_id=10,
        status=PaymentStatus.COMPLETED,
        provider_reference="PROV-999",
    )
    webhook_service._log_event.assert_awaited()


@pytest.mark.asyncio
async def test_process_webhook_invalid_signature(webhook_service, mock_db_session):
    secret = "secret123"
    webhook_id = 1
    payload_body = b'{"data":"fake"}'
    headers = {"X-Signature": "invalid-signature"}

    mock_config = SimpleNamespace(id=webhook_id, active=True, secret_key=secret)
    mock_db_session._mock_scalars.first.return_value = mock_config

    with pytest.raises(ValueError, match="Invalid webhook signature"):
        await webhook_service.process_webhook(webhook_id, payload_body, headers)

    webhook_service._log_event.assert_awaited()


@pytest.mark.asyncio
async def test_process_webhook_missing_config(webhook_service, mock_db_session):
    mock_db_session._mock_scalars.first.return_value = None

    with pytest.raises(ValueError, match="not found or inactive"):
        await webhook_service.process_webhook(1, b"{}", {})


@pytest.mark.asyncio
async def test_process_webhook_payment_not_found(webhook_service, mock_db_session):
    mock_config = SimpleNamespace(id=1, active=True, secret_key=None)
    mock_db_session._mock_scalars.first.side_effect = [mock_config, None]
    payload = json.dumps({"data": {"reference": "PAY-MISSING"}}).encode()

    result = await webhook_service.process_webhook(1, payload, {})

    assert result["status"] == "skipped"
    assert "Payment not found" in result["reason"]
    webhook_service._log_event.assert_awaited()


@pytest.mark.asyncio
async def test_process_webhook_invalid_json(webhook_service, mock_db_session):
    mock_config = SimpleNamespace(id=1, active=True, secret_key=None)
    mock_db_session._mock_scalars.first.return_value = mock_config

    with pytest.raises(ValueError, match="Invalid JSON payload"):
        await webhook_service.process_webhook(1, b"invalid-json", {})

    webhook_service._log_event.assert_awaited()
