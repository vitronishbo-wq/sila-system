from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.infrastructure.models import AcademicRecordModel


class AcademicRecordService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def ensure_record(self, identity_id: uuid.UUID) -> AcademicRecordModel:
        stmt = select(AcademicRecordModel).where(
            AcademicRecordModel.academic_identity_id == identity_id
        )
        result = await self.session.execute(stmt)
        record = result.scalars().first()
        if record:
            return record
        record = AcademicRecordModel(
            id=uuid.uuid4(),
            academic_identity_id=identity_id,
            completed_classes=[],
            sanctions=[],
            debts=[],
            history_json={},
        )
        self.session.add(record)
        await self.session.flush()
        return record

    async def record_enrollment(
        self,
        identity_id: uuid.UUID,
        enrollment_id: uuid.UUID,
        institution_id: uuid.UUID,
        academic_year: str,
        grade: str,
    ) -> dict:
        record = await self.ensure_record(identity_id)
        entry = {
            "type": "enrollment",
            "id": str(enrollment_id),
            "institution_id": str(institution_id),
            "academic_year": academic_year,
            "grade": grade,
            "status": "ACTIVE",
            "timestamp": datetime.utcnow().isoformat(),
        }
        history = dict(record.history_json or {})
        history.setdefault("enrollments", []).append(entry)
        record.current_class = grade
        stmt = (
            update(AcademicRecordModel)
            .where(AcademicRecordModel.academic_identity_id == identity_id)
            .values(history_json=history, current_class=grade)
        )
        await self.session.execute(stmt)
        return entry

    async def record_transfer(
        self,
        identity_id: uuid.UUID,
        from_enrollment_id: uuid.UUID,
        to_enrollment_id: uuid.UUID,
        from_institution_id: uuid.UUID,
        to_institution_id: uuid.UUID,
        academic_year: str,
        grade: str,
    ) -> dict:
        record = await self.ensure_record(identity_id)
        entry = {
            "type": "transfer",
            "from_enrollment_id": str(from_enrollment_id),
            "to_enrollment_id": str(to_enrollment_id),
            "from_institution_id": str(from_institution_id),
            "to_institution_id": str(to_institution_id),
            "academic_year": academic_year,
            "grade": grade,
            "status": "COMPLETED",
            "timestamp": datetime.utcnow().isoformat(),
        }
        history = dict(record.history_json or {})
        history.setdefault("transfers", []).append(entry)
        history.setdefault("enrollments", []).append({
            "type": "enrollment",
            "id": str(to_enrollment_id),
            "institution_id": str(to_institution_id),
            "academic_year": academic_year,
            "grade": grade,
            "status": "ACTIVE",
            "timestamp": datetime.utcnow().isoformat(),
        })
        record.current_class = grade
        stmt = (
            update(AcademicRecordModel)
            .where(AcademicRecordModel.academic_identity_id == identity_id)
            .values(history_json=history, current_class=grade)
        )
        await self.session.execute(stmt)
        return entry

    async def record_certificate(
        self,
        identity_id: uuid.UUID,
        certificate_type: str,
        institution_id: uuid.UUID,
        grade: str | None = None,
    ) -> dict:
        record = await self.ensure_record(identity_id)
        entry = {
            "type": "certificate",
            "certificate_type": certificate_type,
            "institution_id": str(institution_id),
            "grade": grade,
            "status": "CONCLUDED",
            "timestamp": datetime.utcnow().isoformat(),
        }
        history = dict(record.history_json or {})
        history.setdefault("certificates", []).append(entry)
        if grade:
            completed = list(record.completed_classes or [])
            if grade not in completed:
                completed.append(grade)
            stmt = (
                update(AcademicRecordModel)
                .where(AcademicRecordModel.academic_identity_id == identity_id)
                .values(history_json=history, completed_classes=completed)
            )
        else:
            stmt = (
                update(AcademicRecordModel)
                .where(AcademicRecordModel.academic_identity_id == identity_id)
                .values(history_json=history)
            )
        await self.session.execute(stmt)
        return entry

    async def get_history(self, identity_id: uuid.UUID) -> dict | None:
        stmt = select(AcademicRecordModel).where(
            AcademicRecordModel.academic_identity_id == identity_id
        )
        result = await self.session.execute(stmt)
        record = result.scalars().first()
        if not record:
            return None
        return {
            "identity_id": str(identity_id),
            "current_class": record.current_class,
            "completed_classes": record.completed_classes,
            "sanctions": record.sanctions,
            "history": record.history_json,
            "created_at": str(record.created_at) if record.created_at else None,
            "updated_at": str(record.updated_at) if record.updated_at else None,
        }
