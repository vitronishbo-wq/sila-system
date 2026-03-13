from __future__ import annotations
from typing import Any
from uuid import UUID
from apps.backend.app.modules.governance.service_requests.application.ports import EmpregoClientPort
from apps.backend.app.modules.governance.service_requests.domain.enums import ServiceType

class EmpregoClient(EmpregoClientPort):
    """Client para validação de solicitações de Emprego."""

    def __init__(self, candidato_repo: Any) -> None:
        self._candidato_repo = candidato_repo

    async def validate_payload(self, *, service_type: str, citizen_id: UUID, payload: dict[str, Any]) -> tuple[bool, str | None]:
        _ = payload
        if service_type != ServiceType.EMPLOYMENT_APPLICATION.value:
            return (True, None)
        candidato = await self._candidato_repo.get_by_citizen(citizen_id)
        if candidato is None:
            return (False, 'Cidadão não possui cadastro de candidato no módulo de Emprego')
        status = str(getattr(candidato.status, 'value', candidato.status)).lower()
        if status != 'ativo':
            return (False, 'Cadastro de candidato não está ativo')
        return (True, None)

    async def submit(self, *, service_type: str, request_id: UUID, citizen_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
        candidato = await self._candidato_repo.get_by_citizen(citizen_id)
        return {'module': 'emprego', 'service_type': service_type, 'request_id': str(request_id), 'citizen_id': str(citizen_id), 'candidato_id': str(candidato.id) if candidato else None, 'vaga_id': str(payload.get('vaga_id')) if payload.get('vaga_id') else None, 'accepted': True}