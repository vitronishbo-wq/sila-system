"""Service requests lifecycle bridge for cross-module orchestration.

This bridge exposes a stable interface to create and complete tracking requests
without importing `app.modules.governance.service_requests` directly from feature modules.
"""

from __future__ import annotations

from datetime import date, datetime, time
from typing import Any
from uuid import UUID

from sqlalchemy import String, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.governance.service_requests.domain.enums import (
    RequestChannel,
    RequestPriority,
    ServiceRequestStatus,
    ServiceType,
)
from apps.backend.app.modules.governance.service_requests.infrastructure.models.service_request_model import (
    ServiceRequestModel,
)


class ServiceRequestLifecycleBridge:
    """Facade for education and other modules to track institutional requests."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _next_request_number(self) -> str:
        year = datetime.now().year
        sequence_stmt = (
            select(func.count())
            .select_from(ServiceRequestModel)
            .where(ServiceRequestModel.request_number.like(f"SR/{year}/%"))
        )
        sequence = (await self.db.execute(sequence_stmt)).scalar() or 0
        return f"SR/{year}/{sequence + 1:06d}"

    async def create_education_request(
        self,
        *,
        entity_id: UUID,
        citizen_id: UUID,
        numero_processo: str,
        escola_nome: str,
        ano_letivo: str,
    ) -> UUID:
        """Create a core service request linked to an education enrollment entity."""
        request_number = await self._next_request_number()
        created = ServiceRequestModel(
            request_number=request_number,
            citizen_id=citizen_id,
            created_by_user_id=citizen_id,
            service_type=ServiceType.EDUCATION_ENROLLMENT.value,
            title=f"Matricula Escolar {numero_processo}",
            description=f"Matricula na escola {escola_nome}",
            channel=RequestChannel.WEB.value,
            priority=RequestPriority.MEDIUM.value,
            status=ServiceRequestStatus.SUBMITTED.value,
            metadata_={
                "entity_type": "educacao_matricula",
                "entity_id": str(entity_id),
                "numero_processo": numero_processo,
                "ano_letivo": ano_letivo,
            },
            tags=["educacao", "matricula", f"entity:{entity_id}"],
        )
        self.db.add(created)
        await self.db.flush()
        await self.db.commit()
        return created.id

    async def create_health_request(
        self,
        *,
        entity_id: UUID,
        citizen_id: UUID,
        created_by: UUID,
        health_unit_id: UUID,
        appointment_type: str,
        specialty: str,
        appointment_date: date,
        appointment_time: time,
        reason: str,
        priority: str,
    ) -> UUID:
        """Create a core service request linked to a health appointment entity."""
        request_number = await self._next_request_number()
        try:
            request_priority = RequestPriority(priority)
        except ValueError:
            request_priority = RequestPriority.MEDIUM
        created = ServiceRequestModel(
            request_number=request_number,
            citizen_id=citizen_id,
            created_by_user_id=created_by,
            service_type=ServiceType.HEALTH_APPOINTMENT.value,
            title=f"Consulta Saude Primaria {request_number}",
            description=reason,
            channel=RequestChannel.WEB.value,
            priority=request_priority.value,
            status=ServiceRequestStatus.SUBMITTED.value,
            metadata_={
                "entity_type": "saude_primaria_appointment",
                "entity_id": str(entity_id),
                "health_unit_id": str(health_unit_id),
                "appointment_type": appointment_type,
                "specialty": specialty,
                "appointment_date": str(appointment_date),
                "appointment_time": str(appointment_time),
            },
            tags=["saude_primaria", "appointment", f"entity:{entity_id}"],
        )
        self.db.add(created)
        await self.db.flush()
        await self.db.commit()
        return created.id

    async def mark_education_request_completed(
        self, *, entity_id: UUID, actor_id: UUID, metadata: dict[str, Any] | None = None
    ) -> bool:
        """Progress request lifecycle to COMPLETED for the given education entity."""
        request = await self._find_education_request_model(entity_id)
        if request is None:
            return False
        final_status = ServiceRequestStatus.COMPLETED
        current = request.status
        if current == final_status.value:
            return True
        request.status = ServiceRequestStatus.COMPLETED.value
        current = ServiceRequestStatus.COMPLETED.value
        if metadata:
            payload = dict(request.metadata_ or {})
            payload["completion"] = {"actor_id": str(actor_id), **metadata}
            request.metadata_ = payload
        await self.db.commit()
        return current == final_status.value

    async def update_health_request_status(
        self,
        *,
        entity_id: UUID,
        status: ServiceRequestStatus | str,
        actor_id: UUID,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Update lifecycle status for the request linked to a health appointment."""
        request = await self._find_health_request_model(entity_id)
        if request is None:
            return False
        if isinstance(status, str):
            try:
                status = ServiceRequestStatus(status)
            except ValueError as exc:
                raise ValueError(f"Invalid service request status: {status}") from exc
        if request.status == status.value:
            return True
        previous_status = request.status
        request.status = status.value
        payload = dict(request.metadata_ or {})
        payload["status_update"] = {
            "previous_status": previous_status,
            "new_status": status.value,
            "actor_id": str(actor_id),
            **(metadata or {}),
        }
        request.metadata_ = payload
        if status in {ServiceRequestStatus.COMPLETED, ServiceRequestStatus.CANCELLED}:
            request.completed_at = datetime.utcnow()
        await self.db.commit()
        return True

    async def get_requests_by_entity(self, entity_id: UUID) -> list[dict[str, Any]]:
        """Return basic request tracking list for an education entity."""
        stmt = (
            select(ServiceRequestModel)
            .where(
                ServiceRequestModel.service_type == ServiceType.EDUCATION_ENROLLMENT.value,
                cast(ServiceRequestModel.metadata_, String).like(f'%"entity_id": "{entity_id}"%'),
            )
            .order_by(ServiceRequestModel.created_at.desc())
        )
        rows = (await self.db.execute(stmt)).scalars().all()
        return [
            {
                "id": str(row.id),
                "type": row.service_type,
                "status": row.status,
                "entity_id": str(entity_id),
                "request_number": row.request_number,
            }
            for row in rows
        ]

    async def _find_education_request_model(self, entity_id: UUID):
        return await self._find_request_model_by_entity(
            entity_id=entity_id, service_type=ServiceType.EDUCATION_ENROLLMENT
        )

    async def _find_health_request_model(self, entity_id: UUID):
        return await self._find_request_model_by_entity(
            entity_id=entity_id, service_type=ServiceType.HEALTH_APPOINTMENT
        )

    async def _find_request_model_by_entity(self, *, entity_id: UUID, service_type: ServiceType):
        stmt = (
            select(ServiceRequestModel)
            .where(
                ServiceRequestModel.service_type == service_type.value,
                cast(ServiceRequestModel.metadata_, String).like(f'%"entity_id": "{entity_id}"%'),
            )
            .order_by(ServiceRequestModel.created_at.desc())
            .limit(1)
        )
        return (await self.db.execute(stmt)).scalars().first()
