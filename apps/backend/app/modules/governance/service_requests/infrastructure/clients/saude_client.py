from __future__ import annotations
from typing import Any
from uuid import UUID
from app.modules.governance.service_requests.application.ports import SaudeClientPort
from app.modules.governance.service_requests.domain.enums import ServiceType
from app.modules.governance.service_requests.infrastructure.clients._helpers import parse_uuid

class SaudeClient(SaudeClientPort):
    """Client para validação de solicitações de Saúde."""

    def __init__(self, health_unit_repo: Any) -> None:
        self._health_unit_repo = health_unit_repo

    async def validate_payload(self, *, service_type: str, citizen_id: UUID, payload: dict[str, Any]) -> tuple[bool, str | None]:
        _ = citizen_id
        if service_type not in {ServiceType.HEALTH_APPOINTMENT.value, ServiceType.HEALTH_EXAM.value, ServiceType.HEALTH_PRESCRIPTION.value}:
            return (True, None)
        health_unit_id, err = parse_uuid(payload.get('health_unit_id'), 'health_unit_id')
        if err:
            return (False, err)
        unit = await self._health_unit_repo.get_unit_by_id(health_unit_id)
        if unit is None:
            return (False, 'Unidade de saúde não encontrada')
        if not unit.is_active:
            return (False, 'Unidade de saúde está inativa')
        return (True, None)

    async def submit(self, *, service_type: str, request_id: UUID, citizen_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
        return {'module': 'saude', 'service_type': service_type, 'request_id': str(request_id), 'citizen_id': str(citizen_id), 'health_unit_id': str(payload.get('health_unit_id')) if payload.get('health_unit_id') else None, 'accepted': True}