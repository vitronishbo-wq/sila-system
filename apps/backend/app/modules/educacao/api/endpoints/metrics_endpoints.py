from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.infrastructure.models.seat_reservation_model import (
    ReservationStatus,
    SeatReservationModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.transfer_wizard_model import (
    TransferWizardModel,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.seat_reservation_repository import (
    SeatReservationRepository,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.sqlalchemy_enrollment_repository import (
    SQLAlchemyEnrollmentRepository,
)

router = APIRouter(
    prefix="/metrics",
    tags=["Educacao - Metricas Operacionais"],
)


@router.get("/reservations")
async def metrics_reservations(
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    repo = SeatReservationRepository(session)
    active = await repo.count_by_status(ReservationStatus.PENDING.value)
    confirmed = await repo.count_by_status(ReservationStatus.CONFIRMED.value)
    expired = await repo.count_by_status(ReservationStatus.EXPIRED.value)
    cancelled = await repo.count_by_status(ReservationStatus.CANCELLED.value)
    total = await repo.count_total()
    conversion = await repo.count_conversion_rate()
    avg_time = await repo.avg_pending_time_seconds()
    return {
        "active": active,
        "confirmed": confirmed,
        "expired": expired,
        "cancelled": cancelled,
        "total": total,
        "conversion_rate_pct": conversion,
        "avg_confirmation_time_seconds": avg_time,
        "ttl_minutes": 10,
    }


@router.get("/transfers")
async def metrics_transfers(
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    stmt = select(TransferWizardModel.status)
    result = await session.execute(stmt)
    statuses = [row[0] for row in result.fetchall()]
    total = len(statuses)
    concluded = sum(1 for s in statuses if s == "concluido")
    cancelled = sum(1 for s in statuses if s == "cancelado")
    return {
        "total": total,
        "concluded": concluded,
        "cancelled": cancelled,
        "in_progress": total - concluded - cancelled,
    }


@router.get("/enrollments")
async def metrics_enrollments(
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    repo = SQLAlchemyEnrollmentRepository(session)
    active = await repo.get_by_status("ACTIVE")
    transferred = await repo.get_by_status("TRANSFERRED")
    completed = await repo.get_by_status("COMPLETED")
    return {
        "active": len(active),
        "transferred": len(transferred),
        "completed": len(completed),
        "total": len(active) + len(transferred) + len(completed),
    }
