from __future__ import annotations
from typing import Any
from uuid import UUID
from app.modules.justice.bounded_contexts.application.ports.assistencia_social_service_port import AssistenciaSocialServicePort

class AssistenciaSocialServiceAdapter(AssistenciaSocialServicePort):

    def __init__(self, beneficiario_repo: Any):
        self._beneficiario_repo = beneficiario_repo

    async def get_beneficiario(self, citizen_id: UUID) -> dict[str, Any] | None:
        beneficiario = await self._beneficiario_repo.get_by_citizen(citizen_id)
        if beneficiario is None:
            return None
        return {'id': str(beneficiario.id), 'numero_registro': beneficiario.numero_registro, 'situacao': str(getattr(beneficiario.situacao, 'value', beneficiario.situacao)), 'faixa_vulnerabilidade': str(getattr(beneficiario.faixa_vulnerabilidade, 'value', beneficiario.faixa_vulnerabilidade)), 'ativo': beneficiario.ativo, 'cadastro_unico_id': str(beneficiario.cadastro_unico_id) if beneficiario.cadastro_unico_id else None}

    async def is_beneficiario_ativo(self, citizen_id: UUID) -> bool:
        beneficiario = await self._beneficiario_repo.get_by_citizen(citizen_id)
        if beneficiario is None:
            return False
        return bool(beneficiario.ativo)