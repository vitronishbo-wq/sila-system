from __future__ import annotations

import asyncio
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.transfer_policy import TransferRequest


class PersistenceError(Exception):
    """Raised when persistence operations fail."""


class InfrastructureUnavailableError(PersistenceError):
    """Raised when the backing database infrastructure is unavailable."""


class BusinessPersistenceError(PersistenceError):
    """Raised for data-related persistence failures."""


def _run_sync(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


def _load_db_transaction():
    try:
        from apps.backend.app.core.db import transaction

        return transaction
    except Exception as exc:
        raise InfrastructureUnavailableError("Database infrastructure is unavailable") from exc


def _load_models():
    try:
        from apps.backend.app.modules.educacao.infrastructure.models import (
            AcademicIdentityModel,
            AcademicRecordModel,
            EnrollmentModel,
            InstitutionCapacityModel,
            TransferModel,
        )

        return AcademicIdentityModel, AcademicRecordModel, EnrollmentModel, InstitutionCapacityModel, TransferModel
    except Exception as exc:
        raise PersistenceError("Academic education models are unavailable") from exc


class EducacaoRepository:
    def __init__(self):
        self._default_capacity = 0

    async def _get_identity_by_student_id(self, student_id: str, session: AsyncSession):
        AcademicIdentityModel, _, _, _, _ = _load_models()
        stmt = select(AcademicIdentityModel).where(AcademicIdentityModel.national_student_number == student_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_academic_record(self, academic_identity_id: uuid.UUID, session: AsyncSession):
        _, AcademicRecordModel, _, _, _ = _load_models()
        stmt = select(AcademicRecordModel).where(AcademicRecordModel.academic_identity_id == academic_identity_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_active_enrollment(self, academic_identity_id: uuid.UUID, academic_year: str, session: AsyncSession):
        _, _, EnrollmentModel, _, _ = _load_models()
        stmt = (
            select(EnrollmentModel)
            .where(
                and_(
                    EnrollmentModel.student_id == academic_identity_id,
                    EnrollmentModel.academic_year == academic_year,
                    EnrollmentModel.status.in_(["ACTIVE", "PENDING"]),
                )
            )
            .with_for_update()
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    async def _get_capacity_row(
        self,
        institution_id: str,
        class_name: str,
        academic_year: str,
        session: AsyncSession,
    ):
        _, _, _, InstitutionCapacityModel, _ = _load_models()
        stmt = (
            select(InstitutionCapacityModel)
            .where(
                and_(
                    InstitutionCapacityModel.institution_id == institution_id,
                    InstitutionCapacityModel.grade == class_name,
                )
            )
            .with_for_update()
        )
        result = await session.execute(stmt)
        rows = result.scalars().all()
        if not rows:
            return None
        for row in rows:
            if getattr(row, "shift", None) == "ALL":
                return row
        return rows[0]

    async def get_available_capacity(
        self,
        institution_id: str,
        class_name: str,
        academic_year: str,
    ) -> int:
        transaction = _load_db_transaction()
        _, _, _, InstitutionCapacityModel, _ = _load_models()
        async with transaction() as session:
            capacity = await self._get_capacity_row(institution_id, class_name, academic_year, session)
            if capacity is None:
                return self._default_capacity
            if hasattr(capacity, "capacity_total"):
                return max(0, capacity.capacity_total - capacity.capacity_used - capacity.capacity_reserved)
            return max(0, capacity.capacity - capacity.occupied)

    async def list_vacancies(
        self,
        institution_id: str | None = None,
        class_name: str | None = None,
        academic_year: str | None = None,
    ) -> list[dict[str, Any]]:
        transaction = _load_db_transaction()
        _, _, _, InstitutionCapacityModel, _ = _load_models()
        async with transaction() as session:
            stmt = select(InstitutionCapacityModel)
            if institution_id:
                stmt = stmt.where(InstitutionCapacityModel.institution_id == institution_id)
            if class_name:
                stmt = stmt.where(InstitutionCapacityModel.grade == class_name)
            # The current capacity model does not store academic_year; preserve filter signature for compatibility.
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [
                {
                    "institution": str(row.institution_id),
                    "grade": row.grade,
                    "available_slots": (
                        max(0, row.capacity_total - row.capacity_used - row.capacity_reserved)
                        if hasattr(row, "capacity_total")
                        else max(0, row.capacity - row.occupied)
                    ),
                }
                for row in rows
            ]

    async def reserve_capacity(
        self,
        institution_id: str,
        class_name: str,
        academic_year: str,
        quantity: int = 1,
        session: AsyncSession | None = None,
    ) -> None:
        if session is None:
            transaction = _load_db_transaction()
            async with transaction() as session:
                await self.reserve_capacity(institution_id, class_name, academic_year, quantity, session=session)
            return

        row = await self._get_capacity_row(institution_id, class_name, academic_year, session)
        if row is None:
            raise BusinessPersistenceError(
                f"Capacity information not found for {institution_id}/{class_name}/{academic_year}"
            )
        if hasattr(row, "capacity_total"):
            available = row.capacity_total - row.capacity_used - row.capacity_reserved
            if available < quantity:
                raise BusinessPersistenceError(
                    f"Insufficient capacity for {institution_id}/{class_name}/{academic_year}"
                )
            row.capacity_reserved += quantity
        else:
            if row.capacity - row.occupied < quantity:
                raise BusinessPersistenceError(
                    f"Insufficient capacity for {institution_id}/{class_name}/{academic_year}"
                )
            row.occupied += quantity

    async def create_transfer_record(
        self,
        transfer_request: TransferRequest,
        status: str = "executed",
        reason: str | None = None,
        from_institution_id: str | None = None,
        from_enrollment_id: uuid.UUID | None = None,
        to_enrollment_id: uuid.UUID | None = None,
        session: AsyncSession | None = None,
    ):
        transaction = _load_db_transaction()
        AcademicIdentityModel, _, _, _, TransferModel = _load_models()
        if session is None:
            async with transaction() as session:
                return await self.create_transfer_record(
                    transfer_request,
                    status,
                    reason,
                    from_institution_id=from_institution_id,
                    from_enrollment_id=from_enrollment_id,
                    to_enrollment_id=to_enrollment_id,
                    session=session,
                )

        identity = await self._get_identity_by_student_id(transfer_request.student_id, session)
        if identity is None:
            raise BusinessPersistenceError(f"Academic identity not found for {transfer_request.student_id}")

        metadata = getattr(transfer_request, "metadata", {}) or {}
        transfer = TransferModel(
            transfer_number=f"TR-{uuid.uuid4().hex}",
            academic_identity_id=identity.id,
            from_institution_id=from_institution_id,
            to_institution_id=transfer_request.target_school_id,
            from_enrollment_id=from_enrollment_id,
            to_enrollment_id=to_enrollment_id,
            status=status,
            requested_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            reason=reason,
            metadata_json=metadata,
        )
        session.add(transfer)
        await session.flush()
        return transfer

    async def update_academic_record_for_transfer(
        self,
        academic_identity_id: uuid.UUID,
        target_class: str | None,
        academic_year: str,
        session: AsyncSession,
    ) -> None:
        _, AcademicRecordModel, _, _, _ = _load_models()
        record = await self._get_academic_record(academic_identity_id, session)
        if record is None:
            record = AcademicRecordModel(
                academic_identity_id=academic_identity_id,
                current_class=target_class,
                history_json={},
            )
            session.add(record)
            await session.flush()
        if target_class is not None:
            record.current_class = target_class
        history = record.history_json or {}
        transfers = history.get("transfers", [])
        transfers.append(
            {
                "target_class": target_class,
                "academic_year": academic_year,
                "changed_at": datetime.utcnow().isoformat(),
            }
        )
        history["transfers"] = transfers
        record.history_json = history

    async def _publish_outbox_event(
        self,
        event_name: str,
        event_id: str,
        payload: dict,
        session: AsyncSession,
    ):
        from apps.backend.app.core.events.outbox.outbox_repository import OutboxRepository

        outbox = OutboxRepository(session)
        await outbox.save(event_name, event_id, payload)

    async def update_academic_identity_for_transfer(
        self,
        identity,
        target_school_id: str,
        target_class: str | None,
        session: AsyncSession,
    ) -> None:
        if target_school_id is not None:
            identity.current_institution_id = target_school_id
        if target_class is not None:
            identity.current_grade = target_class

    async def execute_transfer(
        self,
        transfer_request: TransferRequest,
        force: bool = False,
    ):
        transaction = _load_db_transaction()
        AcademicIdentityModel, _, EnrollmentModel, _, TransferModel = _load_models()
        async with transaction() as session:
            identity = await self._get_identity_by_student_id(transfer_request.student_id, session)
            if identity is None:
                raise BusinessPersistenceError(f"Academic identity not found for {transfer_request.student_id}")

            if transfer_request.target_class:
                await self.reserve_capacity(
                    transfer_request.target_school_id,
                    transfer_request.target_class,
                    transfer_request.academic_year,
                    quantity=1,
                    session=session,
                )
                await self._publish_outbox_event(
                    "capacity_reserved",
                    str(uuid.uuid4()),
                    {
                        "student_id": transfer_request.student_id,
                        "institution_id": transfer_request.target_school_id,
                        "academic_year": transfer_request.academic_year,
                        "target_class": transfer_request.target_class,
                        "quantity": 1,
                    },
                    session,
                )

            active_enrollment = await self._get_active_enrollment(identity.id, transfer_request.academic_year, session)
            if active_enrollment is not None:
                active_enrollment.status = "TRANSFERRED"
                active_enrollment.ended_at = datetime.utcnow()
                await self._publish_outbox_event(
                    "enrollment_closed",
                    str(uuid.uuid4()),
                    {
                        "student_id": transfer_request.student_id,
                        "academic_identity_id": str(identity.id),
                        "enrollment_id": str(active_enrollment.id),
                        "institution_id": str(active_enrollment.institution_id),
                        "academic_year": active_enrollment.academic_year,
                        "previous_status": "ACTIVE",
                    },
                    session,
                )

            new_enrollment = EnrollmentModel(
                student_id=identity.id,
                institution_id=transfer_request.target_school_id,
                academic_year=transfer_request.academic_year,
                grade=transfer_request.target_class,
                status="ACTIVE",
                started_at=datetime.utcnow(),
                transfer_origin_id=active_enrollment.id if active_enrollment is not None else None,
            )
            session.add(new_enrollment)
            await session.flush()

            if active_enrollment is not None:
                active_enrollment.transfer_destination_id = new_enrollment.id

            previous_institution_id = (
                active_enrollment.institution_id if active_enrollment is not None else identity.current_institution_id
            )

            await self.update_academic_identity_for_transfer(
                identity,
                transfer_request.target_school_id,
                transfer_request.target_class,
                session=session,
            )

            await self.update_academic_record_for_transfer(
                identity.id,
                transfer_request.target_class,
                transfer_request.academic_year,
                session=session,
            )

            metadata = getattr(transfer_request, "metadata", {}) or {}
            transfer = TransferModel(
                transfer_number=f"TR-{uuid.uuid4().hex}",
                academic_identity_id=identity.id,
                from_institution_id=previous_institution_id,
                to_institution_id=transfer_request.target_school_id,
                from_enrollment_id=(active_enrollment.id if active_enrollment is not None else None),
                to_enrollment_id=new_enrollment.id,
                status="executed",
                requested_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
                reason=None,
                metadata_json=metadata,
            )
            session.add(transfer)
            await session.flush()

            from foundation.eligibility.audit import audit_event_async

            await audit_event_async(
                "transfer_completed",
                {
                    "student_id": transfer_request.student_id,
                    "academic_identity_id": str(identity.id),
                    "from_institution_id": str(transfer.from_institution_id) if transfer.from_institution_id else None,
                    "to_institution_id": str(transfer.to_institution_id),
                    "from_enrollment_id": str(transfer.from_enrollment_id) if transfer.from_enrollment_id else None,
                    "to_enrollment_id": str(transfer.to_enrollment_id),
                    "academic_year": transfer_request.academic_year,
                    "target_class": transfer_request.target_class,
                    "status": transfer.status,
                    "metadata": getattr(transfer_request, "metadata", {}) or {},
                },
                aggregate_type="transfer",
                aggregate_id=str(transfer.transfer_number),
                actor_id=None,
                correlation_id=None,
                session=session,
            )

            await self._publish_outbox_event(
                "enrollment_created",
                str(uuid.uuid4()),
                {
                    "student_id": transfer_request.student_id,
                    "academic_identity_id": str(identity.id),
                    "enrollment_id": str(new_enrollment.id),
                    "institution_id": str(new_enrollment.institution_id),
                    "academic_year": new_enrollment.academic_year,
                    "target_class": new_enrollment.grade,
                    "transfer_origin_id": str(new_enrollment.transfer_origin_id)
                    if new_enrollment.transfer_origin_id is not None
                    else None,
                },
                session,
            )

            await self._publish_outbox_event(
                "student_transferred",
                str(uuid.uuid4()),
                {
                    "transfer_number": transfer.transfer_number,
                    "student_id": transfer_request.student_id,
                    "academic_identity_id": str(identity.id),
                    "from_institution_id": str(transfer.from_institution_id) if transfer.from_institution_id else None,
                    "to_institution_id": str(transfer.to_institution_id),
                    "from_enrollment_id": str(transfer.from_enrollment_id) if transfer.from_enrollment_id else None,
                    "to_enrollment_id": str(transfer.to_enrollment_id),
                    "academic_year": transfer_request.academic_year,
                    "target_class": transfer_request.target_class,
                    "status": transfer.status,
                    "metadata": getattr(transfer_request, "metadata", {}) or {},
                },
                session,
            )
            return transfer

    def get_available_capacity_sync(
        self,
        institution_id: str,
        class_name: str,
        academic_year: str,
    ) -> int:
        return _run_sync(self.get_available_capacity(institution_id, class_name, academic_year))

    def list_vacancies_sync(
        self,
        institution_id: str | None = None,
        class_name: str | None = None,
        academic_year: str | None = None,
    ) -> list[dict[str, Any]]:
        return _run_sync(self.list_vacancies(institution_id, class_name, academic_year))

    def execute_transfer_sync(self, transfer_request: TransferRequest, force: bool = False):
        return _run_sync(self.execute_transfer(transfer_request, force))
