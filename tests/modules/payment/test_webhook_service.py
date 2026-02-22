"""
Tests for Payment Webhook Service.
"""

import hmac
import hashlib
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from modules.payment.services.webhook_service import PaymentWebhookService
from modules.payment.models.enums import PaymentStatus
from modules.payment.models.webhook import PaymentWebhook
from modules.payment.models.payment import Payment


@pytest.fixture
def mock_db_session():
    """Mock async database session."""
    session = AsyncMock()
    # Mock return values for scalar execution
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    session.execute = AsyncMock(return_value=mock_result)

    session._mock_scalars = mock_scalars  # Helper for setting returns
    return session


@pytest.fixture
def mock_payment_service():
    """Mock payment service."""
    return AsyncMock()


@pytest.fixture
def webhook_service(mock_db_session, mock_payment_service):
    """WebhookService instance."""
    return PaymentWebhookService(db=mock_db_session, payment_service=mock_payment_service)


@pytest.mark.asyncio
async def test_process_webhook_success(
    webhook_service, mock_db_session, mock_payment_service
):
    """Test successful webhook processing."""
    # 1. Setup Data
    secret = "secret123"
    webhook_id = 1
    reference = "PAY-123"

    payload_dict = {
        "event": "payment.completed",
        "data": {
            "reference": reference,
            "status": "completed",
            "provider_id": "PROV-999"
        }
    }
    payload_body = json.dumps(payload_dict).encode()

    # Generate signature
    signature = hmac.new(secret.encode(), payload_body, hashlib.sha256).hexdigest()
    headers = {"X-Signature": signature}

    # 2. Mock DB Lookups
    # Webhook config lookup
    mock_config = PaymentWebhook(id=webhook_id, active=True, secret_key=secret)
    # Payment lookup
    mock_payment = Payment(id=10, reference=reference, status=PaymentStatus.PENDING)

    # We need side_effect to return different values for different calls if needed
    # But simple mock return_value sequence is easier for simple tests
    mock_db_session._mock_scalars.first.side_effect = [mock_config, mock_payment]

    # 3. Execute
    result = await webhook_service.process_webhook(webhook_id, payload_body, headers)

    # 4. Verify
    assert result["status"] == "success"

    # Verify payment update called
    mock_payment_service.update_payment_status.assert_called_once_with(
        payment_id=10,
        status=PaymentStatus.COMPLETED,
        provider_reference="PROV-999"
    )

    # Verify event logged
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_process_webhook_invalid_signature(webhook_service, mock_db_session):
    """Test webhook with invalid signature."""
    secret = "secret123"
    webhook_id = 1
    payload_body = b'{"data": "fake"}'

    # Mock config
    mock_config = PaymentWebhook(id=webhook_id, active=True, secret_key=secret)
    mock_db_session._mock_scalars.first.return_value = mock_config

    headers = {"X-Signature": "invalid-signature"}

    with pytest.raises(ValueError, match="Invalid webhook signature"):
        await webhook_service.process_webhook(webhook_id, payload_body, headers)

    # Verify we logged the failure
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_process_webhook_missing_config(webhook_service, mock_db_session):
    """Test webhook processing when config is missing."""
    mock_db_session._mock_scalars.first.return_value = None

    with pytest.raises(ValueError, match="not found or inactive"):
        await webhook_service.process_webhook(1, b"{}", {})


@pytest.mark.asyncio
async def test_process_webhook_payment_not_found(webhook_service, mock_db_session):
    """Test webhook when referenced payment doesn't exist."""
    # Mock config
    mock_config = PaymentWebhook(id=1, active=True, secret_key=None)  # No secret = no sig check
    mock_db_session._mock_scalars.first.side_effect = [
        mock_config, None]  # Config found, Payment NOT found

    payload = json.dumps({"data": {"reference": "PAY-MISSING"}}).encode()

    result = await webhook_service.process_webhook(1, payload, {})

    assert result["status"] == "skipped"
    assert "Payment not found" in result["reason"]
    # Event should still be logged as error
    mock_db_session.add.assert_called()


@pytest.mark.asyncio
async def test_process_webhook_invalid_json(webhook_service, mock_db_session):
    """Test handling of invalid JSON body."""
    mock_config = PaymentWebhook(id=1, active=True, secret_key=None)
    mock_db_session._mock_scalars.first.return_value = mock_config

    with pytest.raises(ValueError, match="Invalid JSON payload"):
        await webhook_service.process_webhook(1, b"invalid-json", {})

    mock_db_session.add.assert_called()
