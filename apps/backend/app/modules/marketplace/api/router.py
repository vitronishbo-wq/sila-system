"""Marketplace - Instant Transfer orchestration router (stub)

This file contains a lightweight stub implementation for the
`POST /marketplace/instant-transfer` endpoint used by TASK-015.

The real implementation should move orchestration into an application
service with injected dependencies for matching, eligibility, reservation,
payment, transfer/enrollment and notification services.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from foundation.matching.engine import MatchingEngine, StudentProfile
from apps.backend.app.api.deps import get_db
from ..application.dto import InstantTransferRequestDTO
from ..application.adapters import (
    MatchingAdapter,
    RealMatchingAdapter,
    ReservationAdapter,
    RealReservationAdapter,
    RealPaymentAdapter,
    RealTransferAdapter,
    NotificationAdapter,
)
from ..application.service import InstantTransferOrchestrator
import os
from ..infrastructure.redis_store import InMemoryOrchestrationStore
from ..infrastructure.redis_orchestration_store import RedisOrchestrationStore


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/marketplace", tags=["marketplace-api"]) 


class InstantTransferRequest(BaseModel):
    student_id: str
    student_profile: Optional[Dict[str, Any]] = None
    preferred_institution_id: Optional[str] = None
    current_enrollment_id: Optional[str] = None
    target_grade: Optional[str] = None
    target_shift: Optional[str] = None
    academic_year: Optional[str] = None
    reason: Optional[str] = None
    actor_id: Optional[str] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    idempotency_key: Optional[str] = Field(None, alias="Idempotency-Key")


class StepStatus(BaseModel):
    status: str
    detail: Optional[Dict[str, Any]] = None


class InstantTransferResponse(BaseModel):
    status: str
    transfer_id: Optional[str] = None
    message: Optional[str] = None
    steps: Dict[str, Any] = {}


async def _reserve_slot(institution_id: str, student_id: str) -> Dict[str, Any]:
    """Stub reservation: reserve a slot for student at institution."""
    # TODO: integrate with reservation repository/service
    return {"reservation_id": f"res_{institution_id}_{student_id}", "status": "reserved"}


async def _process_payment(amount: float | None, method: Optional[str]) -> Dict[str, Any]:
    """Stub payment processing."""
    # TODO: integrate with payment gateway/service
    return {"payment_id": "pay_stub_123", "status": "paid"}


async def _perform_transfer(student_id: str, institution_id: str) -> Dict[str, Any]:
    """Stub transfer/enrollment operation."""
    # TODO: call transfer and enrollment services
    return {"transfer_id": f"tr_{student_id}_{institution_id}", "status": "enrolled"}


async def _notify_student(student_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Stub notification."""
    # TODO: integrate with notifications module
    return {"notification_id": f"not_{student_id}", "status": "sent"}


async def orchestrate_instant_transfer(session, payload: InstantTransferRequest) -> InstantTransferResponse:
    """Orchestrator for instant transfer (stub).

    This is intentionally minimal: in production each step is delegated to
    an application service with proper transactions, idempotency and
    compensation logic.
    """
    steps: Dict[str, Any] = {}

    try:
        student_id = payload.student_id

        # 1) Matching (optional if preferred_institution_id provided)
        if payload.preferred_institution_id:
            selected_institution = payload.preferred_institution_id
            steps["matching"] = {"status": "skipped", "institution_id": selected_institution}
        else:
            # If student_profile provided, attempt to find best match
            if payload.student_profile:
                # Build StudentProfile for matching engine
                sp = StudentProfile(
                    student_id=student_id,
                    age=payload.student_profile.get("age", 18),
                    academic_performance=payload.student_profile.get("academic_performance", 0.0),
                    special_needs=payload.student_profile.get("special_needs", []),
                    location=payload.student_profile.get("location", {}),
                    available_budget=payload.student_profile.get("available_budget", 0.0),
                    previous_transfers=payload.student_profile.get("previous_transfers", 0),
                )
                matching_engine = MatchingEngine()
                matches = await matching_engine.find_matches(session, sp, [], max_results=1)
                if not matches:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches found")
                selected_institution = matches[0].institution_id
                steps["matching"] = {"status": "found", "institution_id": selected_institution}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="preferred_institution_id or student_profile required")

        # 2) Eligibility check (simplified - use matching compatibility)
        # In real flow call MatchingEngine.check_eligibility
        steps["eligibility"] = {"status": "assumed_ok"}

        # 3) Reservation
        reservation = await _reserve_slot(selected_institution, student_id)
        steps["reservation"] = reservation

        # 4) Payment
        payment = await _process_payment(payload.amount, payload.payment_method)
        steps["payment"] = payment

        # 5) Transfer / Enrollment
        transfer = await _perform_transfer(student_id, selected_institution)
        steps["transfer"] = transfer

        # 6) Notification
        notify = await _notify_student(student_id, {"transfer": transfer, "payment": payment})
        steps["notification"] = notify

        return InstantTransferResponse(
            status="success",
            transfer_id=transfer.get("transfer_id"),
            message="Instant transfer orchestration completed (stub)",
            steps=steps,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Instant transfer orchestration failed")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/instant-transfer",
    response_model=InstantTransferResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Orchestrate an instant transfer from search to enrollment (scaffold)",
)
async def post_instant_transfer(
    payload: InstantTransferRequest,
    orchestrator: InstantTransferOrchestrator = Depends(get_default_orchestrator),
):
    """API entrypoint for instant transfers.

    Uses DI to receive an `InstantTransferOrchestrator`. Default orchestrator is a scaffold
    wiring in-memory adapters. Production should replace with DI providers.
    """
    dto = InstantTransferRequestDTO(
        student_id=payload.student_id,
        student_profile=payload.student_profile,
        preferred_institution_id=payload.preferred_institution_id,
        amount=payload.amount,
        payment_method=payload.payment_method,
        metadata={
            "current_enrollment_id": payload.current_enrollment_id,
            "grade": payload.target_grade,
            "shift": payload.target_shift,
            "academic_year": payload.academic_year,
            "reason": payload.reason,
            "actor_id": payload.actor_id,
        },
    )

    resp = await orchestrator.orchestrate(dto, idempotency_key=payload.idempotency_key)
    return InstantTransferResponse(**resp.dict())


async def get_default_orchestrator(session: AsyncSession = Depends(get_db)) -> InstantTransferOrchestrator:
    matching = RealMatchingAdapter(session)
    reservation = RealReservationAdapter(session)
    payment = RealPaymentAdapter(session)
    transfer = RealTransferAdapter(session)
    notification = NotificationAdapter()
    # Prefer Redis store when REDIS_URL is set; otherwise fall back to in-memory store for tests
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        try:
            store = RedisOrchestrationStore.from_url(redis_url)
        except Exception:
            store = InMemoryOrchestrationStore()
    else:
        store = InMemoryOrchestrationStore()

    return InstantTransferOrchestrator(matching, reservation, payment, transfer, notification, store)
