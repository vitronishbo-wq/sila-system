from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.infrastructure.models.seat_reservation_model import (
    ReservationStatus,
    SeatReservationModel,
)

TTL_MINUTES = 10


class SeatReservationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, student_id: uuid.UUID, institution_id: uuid.UUID, classe: str, turno: str, ano_letivo: str
    ) -> SeatReservationModel:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=TTL_MINUTES)
        model = SeatReservationModel(
            student_id=student_id,
            institution_id=institution_id,
            classe=classe,
            turno=turno,
            ano_letivo=ano_letivo,
            expires_at=expires_at,
            status=ReservationStatus.PENDING.value,
        )
        self.session.add(model)
        return model

    async def get_by_id(self, reservation_id: uuid.UUID) -> Optional[SeatReservationModel]:
        stmt = select(SeatReservationModel).where(SeatReservationModel.id == reservation_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active(self, reservation_id: uuid.UUID) -> Optional[SeatReservationModel]:
        now = datetime.now(timezone.utc)
        stmt = select(SeatReservationModel).where(
            SeatReservationModel.id == reservation_id,
            SeatReservationModel.status == ReservationStatus.PENDING.value,
            SeatReservationModel.expires_at > now,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_active_by_student(self, student_id: uuid.UUID) -> list[SeatReservationModel]:
        now = datetime.now(timezone.utc)
        stmt = (
            select(SeatReservationModel)
            .where(
                SeatReservationModel.student_id == student_id,
                SeatReservationModel.status == ReservationStatus.PENDING.value,
                SeatReservationModel.expires_at > now,
            )
            .order_by(SeatReservationModel.expires_at)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def confirm(self, reservation_id: uuid.UUID) -> bool:
        now = datetime.now(timezone.utc)
        stmt = (
            update(SeatReservationModel)
            .where(
                SeatReservationModel.id == reservation_id,
                SeatReservationModel.status == ReservationStatus.PENDING.value,
                SeatReservationModel.expires_at > now,
            )
            .values(status=ReservationStatus.CONFIRMED.value, confirmed_at=now)
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def expire_stale(self) -> int:
        now = datetime.now(timezone.utc)
        stmt = (
            update(SeatReservationModel)
            .where(
                SeatReservationModel.status == ReservationStatus.PENDING.value,
                SeatReservationModel.expires_at <= now,
            )
            .values(status=ReservationStatus.EXPIRED.value)
        )
        result = await self.session.execute(stmt)
        return result.rowcount or 0

    async def cancel(self, reservation_id: uuid.UUID) -> bool:
        now = datetime.now(timezone.utc)
        stmt = (
            update(SeatReservationModel)
            .where(
                SeatReservationModel.id == reservation_id,
                SeatReservationModel.status == ReservationStatus.PENDING.value,
            )
            .values(status=ReservationStatus.CANCELLED.value, cancelled_at=now)
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def count_by_status(self, status: str) -> int:
        stmt = select(SeatReservationModel.id).where(SeatReservationModel.status == status)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

    async def count_total(self) -> int:
        stmt = select(SeatReservationModel.id)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

    async def count_conversion_rate(self) -> float:
        total = await self.count_total()
        if total == 0:
            return 0.0
        confirmed = await self.count_by_status(ReservationStatus.CONFIRMED.value)
        return round(confirmed / total * 100, 2)

    async def avg_pending_time_seconds(self) -> float:
        stmt = select(SeatReservationModel.created_at, SeatReservationModel.confirmed_at).where(
            SeatReservationModel.status == ReservationStatus.CONFIRMED.value,
            SeatReservationModel.confirmed_at.isnot(None),
        )
        result = await self.session.execute(stmt)
        rows = result.fetchall()
        if not rows:
            return 0.0
        durations = [(row.confirmed_at - row.created_at).total_seconds() for row in rows]
        return round(sum(durations) / len(durations), 2)
