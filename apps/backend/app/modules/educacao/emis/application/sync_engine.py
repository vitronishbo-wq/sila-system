from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.database.session import AsyncSessionLocal
from apps.backend.app.modules.educacao.emis.domain.models import (
    EmisEnrollment,
    EmisInstitution,
    EmisStudent,
    SyncDirection,
    SyncLogEntry,
    SyncStatus,
)
from apps.backend.app.modules.educacao.emis.infrastructure.emis_client import EmisClient
from apps.backend.app.modules.educacao.emis.infrastructure.sync_log_model import (
    EmisSyncLogModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.academic_identity_model import (
    AcademicIdentityModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.enrollment_model import (
    EnrollmentModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.marketplace_institution_model import (
    MarketplaceInstitutionModel,
)

logger = logging.getLogger(__name__)


class SyncLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entry: SyncLogEntry) -> None:
        stmt = pg_insert(EmisSyncLogModel).values(
            entity_type=entry.entity_type.value,
            entity_id=entry.entity_id,
            direction=entry.direction.value,
            status=entry.status.value,
            payload=entry.payload,
            response=entry.response,
            error=entry.error,
            duration_ms=entry.duration_ms,
            retry_count=entry.retry_count,
            next_retry_at=entry.next_retry_at,
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def list_logs(
        self,
        entity_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[EmisSyncLogModel]:
        query = select(EmisSyncLogModel).order_by(EmisSyncLogModel.created_at.desc())
        if entity_type:
            query = query.where(EmisSyncLogModel.entity_type == entity_type)
        if status:
            query = query.where(EmisSyncLogModel.status == status)
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_stats(self) -> dict[str, Any]:
        total = await self.session.execute(
            select(func.count(EmisSyncLogModel.id))
        )
        success = await self.session.execute(
            select(func.count(EmisSyncLogModel.id)).where(
                EmisSyncLogModel.status == SyncStatus.SUCCESS.value
            )
        )
        failed = await self.session.execute(
            select(func.count(EmisSyncLogModel.id)).where(
                EmisSyncLogModel.status == SyncStatus.FAILED.value
            )
        )
        retry = await self.session.execute(
            select(func.count(EmisSyncLogModel.id)).where(
                EmisSyncLogModel.status == SyncStatus.RETRY.value
            )
        )
        dead_letter = await self.session.execute(
            select(func.count(EmisSyncLogModel.id)).where(
                EmisSyncLogModel.status == SyncStatus.DEAD_LETTER.value
            )
        )
        pending = await self.session.execute(
            select(func.count(EmisSyncLogModel.id)).where(
                EmisSyncLogModel.status == SyncStatus.PENDING.value
            )
        )
        last = await self.session.execute(
            select(EmisSyncLogModel.created_at)
            .where(EmisSyncLogModel.status == SyncStatus.SUCCESS.value)
            .order_by(EmisSyncLogModel.created_at.desc())
            .limit(1)
        )
        last_sync = last.scalar_one_or_none()
        return {
            "total_synced": total.scalar() or 0,
            "success_count": success.scalar() or 0,
            "failed_count": failed.scalar() or 0,
            "retry_count": retry.scalar() or 0,
            "dead_letter_count": dead_letter.scalar() or 0,
            "pending_count": pending.scalar() or 0,
            "last_sync_at": last_sync.isoformat() if last_sync else None,
        }


class EmisSyncEngine:
    def __init__(
        self,
        emis_client: Optional[EmisClient] = None,
        session: Optional[AsyncSession] = None,
    ):
        self.emis_client = emis_client or EmisClient()
        self.session = session

    async def _get_session(self) -> AsyncSession:
        if self.session:
            return self.session
        return AsyncSessionLocal()

    async def _log(
        self,
        session: AsyncSession,
        entry: SyncLogEntry,
    ) -> None:
        repo = SyncLogRepository(session)
        await repo.save(entry)

    async def _log_result(
        self,
        session: AsyncSession,
        entity_type: SyncEntityType,
        entity_id: str,
        payload: dict,
        result: Optional[dict],
        elapsed: int,
        exc: Optional[Exception] = None,
    ) -> None:
        if exc is None:
            await self._log(
                session,
                SyncLogEntry(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    direction=SyncDirection.PUSH,
                    status=SyncStatus.SUCCESS,
                    payload=payload,
                    response=result,
                    duration_ms=elapsed,
                ),
            )
            return

        from apps.backend.app.modules.educacao.emis.infrastructure.emis_client import (
            _is_retryable,
        )
        if _is_retryable(exc):
            entry = SyncLogEntry(
                entity_type=entity_type,
                entity_id=entity_id,
                direction=SyncDirection.PUSH,
                status=SyncStatus.RETRY,
                payload=payload,
                error=str(exc),
                duration_ms=elapsed,
            )
            backoff = entry.retry_count * 60
            entry.mark_retry(str(exc), datetime.utcnow().replace(second=backoff))
            await self._log(session, entry)
        else:
            await self._log(
                session,
                SyncLogEntry(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    direction=SyncDirection.PUSH,
                    status=SyncStatus.DEAD_LETTER,
                    payload=payload,
                    error=str(exc),
                    duration_ms=elapsed,
                ),
            )

    # ── Push: Enrollment ──────────────────────────────────────────

    async def push_enrollment(self, enrollment_id: UUID) -> dict[str, Any]:
        session = await self._get_session()
        try:
            model = await session.get(EnrollmentModel, enrollment_id)
            if not model:
                raise ValueError(f"Enrollment {enrollment_id} not found")

            identity = await session.get(AcademicIdentityModel, model.student_id)
            institution = await session.get(
                MarketplaceInstitutionModel, model.institution_id
            )

            emis_enrollment = EmisEnrollment(
                enrollment_id=model.id,
                student_id=model.student_id,
                institution_id=model.institution_id,
                institution_name=institution.nome if institution else "Unknown",
                academic_year=model.academic_year,
                grade=model.grade or "",
                shift="manha",
                status=model.status,
                started_at=model.started_at or datetime.utcnow(),
                ended_at=model.ended_at,
            )

            t0 = time.monotonic()
            result = await self.emis_client.create_enrollment(emis_enrollment)
            elapsed = int((time.monotonic() - t0) * 1000)

            await self._log_result(
                session, SyncEntityType.ENROLLMENT, str(enrollment_id),
                {"academic_year": model.academic_year, "status": model.status},
                result, elapsed,
            )
            return result
        except Exception as exc:
            await self._log_result(
                session, SyncEntityType.ENROLLMENT, str(enrollment_id),
                {"academic_year": getattr(model, "academic_year", ""), "status": getattr(model, "status", "")},
                None, 0, exc=exc,
            )
            raise

    # ── Push: Student ────────────────────────────────────────────

    async def push_student(self, student_id: UUID) -> dict[str, Any]:
        session = await self._get_session()
        try:
            model = await session.get(AcademicIdentityModel, student_id)
            if not model:
                raise ValueError(f"Student {student_id} not found")

            emis_student = EmisStudent(
                student_id=model.id,
                full_name=model.full_name,
                document_id=model.national_student_number,
                birth_date=model.birth_date,
                gender=model.gender or "N/A",
                province="",
                municipio="",
                nacionalidade="ANGOLANA",
            )

            t0 = time.monotonic()
            result = await self.emis_client.create_student(emis_student)
            elapsed = int((time.monotonic() - t0) * 1000)

            await self._log_result(
                session, SyncEntityType.STUDENT, str(student_id),
                {"full_name": model.full_name, "document": model.national_student_number},
                result, elapsed,
            )
            return result
        except Exception as exc:
            await self._log_result(
                session, SyncEntityType.STUDENT, str(student_id),
                {"full_name": getattr(model, "full_name", ""), "document": getattr(model, "national_student_number", "")},
                None, 0, exc=exc,
            )
            raise

    # ── Push: Institution ────────────────────────────────────────

    async def push_institution(self, institution_id: UUID) -> dict[str, Any]:
        session = await self._get_session()
        try:
            model = await session.get(MarketplaceInstitutionModel, institution_id)
            if not model:
                raise ValueError(f"Institution {institution_id} not found")

            emis_inst = EmisInstitution(
                institution_id=model.institution_id,
                name=model.nome,
                institution_type=model.tipo,
                nivel_ensino=model.nivel_ensino,
                province=model.provincia,
                municipio=model.municipio,
                bairro=model.bairro,
                contactos=model.contactos,
                turnos=model.turnos,
            )

            t0 = time.monotonic()
            result = await self.emis_client.sync_institution(emis_inst)
            elapsed = int((time.monotonic() - t0) * 1000)

            await self._log_result(
                session, SyncEntityType.INSTITUTION, str(institution_id),
                {"name": model.nome, "type": model.tipo},
                result, elapsed,
            )
            return result
        except Exception as exc:
            await self._log_result(
                session, SyncEntityType.INSTITUTION, str(institution_id),
                {"name": getattr(model, "nome", ""), "type": getattr(model, "tipo", "")},
                None, 0, exc=exc,
            )
            raise

    # ── Bulk Sync ────────────────────────────────────────────────

    async def sync_all_pending_enrollments(
        self, limit: int = 100
    ) -> dict[str, Any]:
        session = await self._get_session()
        query = (
            select(EnrollmentModel)
            .order_by(EnrollmentModel.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        enrollments = list(result.scalars().all())

        success = 0
        failed = 0
        for model in enrollments:
            try:
                await self.push_enrollment(model.id)
                success += 1
            except Exception as exc:
                logger.warning("Sync failed for enrollment %s: %s", model.id, exc)
                failed += 1

        return {"total": len(enrollments), "success": success, "failed": failed}

    async def sync_all_institutions(self, limit: int = 100) -> dict[str, Any]:
        session = await self._get_session()
        query = (
            select(MarketplaceInstitutionModel)
            .order_by(MarketplaceInstitutionModel.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        institutions = list(result.scalars().all())

        success = 0
        failed = 0
        for model in institutions:
            try:
                await self.push_institution(model.institution_id)
                success += 1
            except Exception as exc:
                logger.warning("Sync failed for institution %s: %s", model.institution_id, exc)
                failed += 1

        return {"total": len(institutions), "success": success, "failed": failed}
