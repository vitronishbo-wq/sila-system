from __future__ import annotations
from typing import Any
from uuid import UUID
from app.modules.governance.service_requests.application.ports import EducacaoClientPort
from app.modules.governance.service_requests.domain.enums import ServiceType
from app.modules.governance.service_requests.infrastructure.clients._helpers import parse_uuid

class EducacaoClient(EducacaoClientPort):
    """Client para pré-validação e roteamento de pedidos de Educação."""

    def __init__(self, turma_repo: Any):
        self._turma_repo = turma_repo

    async def validate_payload(self, *, service_type: str, citizen_id: UUID, payload: dict[str, Any]) -> tuple[bool, str | None]:
        _ = citizen_id
        if service_type != ServiceType.EDUCATION_ENROLLMENT.value:
            return (True, None)
        turma_id, turma_err = parse_uuid(payload.get('turma_id'), 'turma_id')
        if turma_err:
            return (False, turma_err)
        ano_letivo_id, ano_err = parse_uuid(payload.get('ano_letivo_id'), 'ano_letivo_id')
        if ano_err:
            return (False, ano_err)
        turma = await self._turma_repo.get_by_id(turma_id)
        if turma is None:
            return (False, 'Turma não encontrada')
        if not turma.ativa:
            return (False, 'Turma inativa')
        if turma.ano_letivo_id != ano_letivo_id:
            return (False, 'Turma não pertence ao ano letivo informado')
        ocupacao = await self._turma_repo.count_matriculas_ativas(turma_id, ano_letivo_id)
        if ocupacao >= turma.capacidade:
            return (False, 'Turma sem vagas disponíveis')
        return (True, None)

    async def submit(self, *, service_type: str, request_id: UUID, citizen_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
        response = {'module': 'educacao', 'service_type': service_type, 'request_id': str(request_id), 'citizen_id': str(citizen_id), 'accepted': True}
        if service_type == ServiceType.EDUCATION_ENROLLMENT.value:
            turma_id, _ = parse_uuid(payload.get('turma_id'), 'turma_id')
            ano_letivo_id, _ = parse_uuid(payload.get('ano_letivo_id'), 'ano_letivo_id')
            if turma_id and ano_letivo_id:
                turma = await self._turma_repo.get_by_id(turma_id)
                ocupacao = await self._turma_repo.count_matriculas_ativas(turma_id, ano_letivo_id)
                response['vaga_disponivel'] = bool(turma and ocupacao < turma.capacidade)
                if turma:
                    response['vagas_restantes'] = max(turma.capacidade - ocupacao, 0)
        return response