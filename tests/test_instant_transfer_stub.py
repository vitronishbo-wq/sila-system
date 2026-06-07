import asyncio

import pytest

from apps.backend.app.modules.marketplace.api.router import (
    InstantTransferRequest,
    orchestrate_instant_transfer,
)


@pytest.mark.asyncio
async def test_orchestrator_with_preferred_institution():
    payload = InstantTransferRequest(
        student_id="s123",
        preferred_institution_id="i-preferred",
        amount=100.0,
        payment_method="card",
    )

    resp = await orchestrate_instant_transfer(None, payload)
    assert resp.status == "success"
    assert resp.transfer_id is not None
    assert "reservation" in resp.steps
    assert "payment" in resp.steps
    assert "transfer" in resp.steps
    assert "notification" in resp.steps


@pytest.mark.asyncio
async def test_orchestrator_requires_profile_or_preference():
    payload = InstantTransferRequest(student_id="s123")

    with pytest.raises(Exception):
        await orchestrate_instant_transfer(None, payload)
