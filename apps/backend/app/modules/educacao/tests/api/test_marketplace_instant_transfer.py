from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, patch
from uuid import UUID, uuid4

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from apps.backend.app.api.deps import get_current_user
from apps.backend.app.modules.educacao.api.deps import get_transfer_transaction_service
from apps.backend.app.modules.educacao.marketplace.router import router as marketplace_router


@pytest.mark.asyncio
async def test_instant_transfer_route_calls_transfer_service() -> None:
    app = FastAPI()
    app.include_router(marketplace_router, prefix="/api/v1/educacao")

    mock_service = AsyncMock()
    receipt = {
        "transfer_id": str(uuid4()),
        "student_id": str(uuid4()),
        "old_enrollment_id": str(uuid4()),
        "new_enrollment_id": str(uuid4()),
        "target_institution_id": str(uuid4()),
        "target_grade": "10A",
        "target_shift": "MORNING",
        "academic_year": "2026",
        "issued_at": "2026-01-01T00:00:00Z",
    }
    expected_response = {
        "status": "success",
        "transfer_id": receipt["transfer_id"],
        "old_enrollment_id": receipt["old_enrollment_id"],
        "new_enrollment_id": receipt["new_enrollment_id"],
        "academic_year": receipt["academic_year"],
        "steps_completed": ["lock_vacancy", "validate_eligibility", "reserve_capacity"],
        "audit_trail": [],
        "audit_event": {},
        "domain_event": {},
        "receipt": receipt,
    }
    mock_service.execute_transfer.return_value = expected_response

    fake_user_id = str(uuid4())

    async def fake_current_user() -> dict[str, str]:
        return {"user_id": fake_user_id}

    request_payload = {
        "student_id": str(uuid4()),
        "current_enrollment_id": str(uuid4()),
        "target_institution_id": str(uuid4()),
        "target_grade": "10A",
        "target_shift": "MORNING",
        "academic_year": "2026",
        "reason": "Student requested instant transfer",
    }

    app.dependency_overrides[get_transfer_transaction_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = fake_current_user
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
        ) as client:
            response = await client.post(
                "/api/v1/educacao/marketplace/instant-transfer",
                json=request_payload,
                headers={
                    "Authorization": "Bearer testtoken",
                    "Idempotency-Key": "key-123",
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json() == expected_response
    mock_service.execute_transfer.assert_awaited_once_with(
        student_id=UUID(request_payload["student_id"]),
        current_enrollment_id=UUID(request_payload["current_enrollment_id"]),
        target_institution_id=UUID(request_payload["target_institution_id"]),
        target_grade=request_payload["target_grade"],
        target_shift=request_payload["target_shift"],
        academic_year=request_payload["academic_year"],
        reason=request_payload["reason"],
        actor_id=UUID(fake_user_id),
        idempotency_key="key-123",
    )
