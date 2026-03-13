from __future__ import annotations
from typing import Any
from uuid import UUID
from app.core.bridges import CitizenRepositoryPort
from apps.backend.app.modules.governance.service_requests.application.ports import IdentidadeClientPort

class IdentidadeClient(IdentidadeClientPort):
    """Client de validação com Identidade Civil/FUC."""

    def __init__(self, citizen_repo: CitizenRepositoryPort):
        self._citizen_repo = citizen_repo

    async def validate_payload(self, *, service_type: str, citizen_id: UUID, payload: dict[str, Any]) -> tuple[bool, str | None]:
        _ = (service_type, payload)
        citizen = await self._citizen_repo.get_by_id(citizen_id)
        if citizen is None:
            return (False, 'Cidadão não encontrado na base de Identidade Civil')
        if getattr(citizen, 'is_active', True) is False:
            return (False, 'Cidadão inativo na base de Identidade Civil')
        vital_status = getattr(citizen, 'vital_status', None)
        if isinstance(vital_status, str) and vital_status.lower() in {'inactive', 'deceased'}:
            return (False, 'Cidadão com estado vital inativo')
        return (True, None)

    async def submit(self, *, service_type: str, request_id: UUID, citizen_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
        _ = payload
        return {'module': 'identidade_civil', 'service_type': service_type, 'request_id': str(request_id), 'citizen_id': str(citizen_id), 'accepted': True}