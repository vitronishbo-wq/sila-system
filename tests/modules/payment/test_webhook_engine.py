"""
Tests for WebhookEngine.
"""
import hmac
import hashlib
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

from apps.backend.app.modules.payment.application.services.webhook_service import (
    WebhookEngine,
)
from apps.backend.app.modules.payment.domain.enums import PaymentStatus
from apps.backend.app.modules.payment.domain.models.payment import Payment


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def engine(mock_db):
    return WebhookEngine(db=mock_db, secret="test_secret")


@pytest.mark.asyncio
async def test_verify_signature_valid(engine):
    payload = b'{"test": "data"}'
    signature = hmac.new(b"test_secret", payload, hashlib.sha256).hexdigest()
    assert engine.verify_signature(payload, signature) is True


@pytest.mark.asyncio
async def test_verify_signature_invalid(engine):
    payload = b'{"test": "data"}'
    assert engine.verify_signature(payload, "wrong_signature") is False


@pytest.mark.asyncio
async def test_process_event_success(engine, mock_db):
    """Test successful event processing with status update."""
    reference = "PAY-123"
    payload = {
        "reference": reference,
        "event": "success"
    }
    raw_payload = json.dumps(payload).encode()
    signature = hmac.new(b"test_secret", raw_payload, hashlib.sha256).hexdigest()

    # Mock Payment lookup
    mock_payment = MagicMock(spec=Payment)
    mock_payment.id = 1
    mock_payment.reference = reference
    mock_payment.status = PaymentStatus.PENDING

    # Patch PaymentService's get_by_reference (used by engine)
    with patch.object(engine.payment_service, 'get_by_reference', return_value=mock_payment):
        # Patch PaymentService's update_status
        with patch.object(engine.payment_service, 'update_status', return_value=None) as mock_update:
            result = await engine.process_event("generic", payload, signature, raw_payload)

            assert "updated to completed" in result["detail"]
            mock_update.assert_called_once_with(1, PaymentStatus.COMPLETED)


@pytest.mark.asyncio
async def test_process_event_idempotency(engine, mock_db):
    """Test idempotency: same event doesn't trigger update."""
    reference = "PAY-123"
    payload = {"reference": reference, "event": "success"}
    raw_payload = json.dumps(payload).encode()
    signature = hmac.new(b"test_secret", raw_payload, hashlib.sha256).hexdigest()

    # Payment is already COMPLETED
    mock_payment = MagicMock(spec=Payment)
    mock_payment.status = PaymentStatus.COMPLETED

    with patch.object(engine.payment_service, 'get_by_reference', return_value=mock_payment):
        with patch.object(engine.payment_service, 'update_status') as mock_update:
            result = await engine.process_event("generic", payload, signature, raw_payload)

            assert result["detail"] == "Event already processed"
            mock_update.assert_not_called()


@pytest.mark.asyncio
async def test_process_event_invalid_signature_raises(engine):
    payload = {"reference": "any"}
    raw_payload = json.dumps(payload).encode()

    with pytest.raises(HTTPException) as excinfo:
        await engine.process_event("generic", payload, "invalid", raw_payload)
    assert excinfo.value.status_code == 401
