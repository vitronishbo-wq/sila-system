from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from apps.backend.app.modules.governance.workflow.application.ports.assistencia_social_adapter_port import (
    AssistenciaSocialAdapterPort,
)


class AssistenciaSocialAdapter(AssistenciaSocialAdapterPort):
    def __init__(self, beneficiario_repo: Any, visita_repo: Any):
        self._beneficiario_repo = beneficiario_repo
        self._visita_repo = visita_repo

    async def is_beneficiario_ativo(self, citizen_id: UUID) -> bool:
        beneficiario = await self._beneficiario_repo.get_by_citizen(citizen_id)
        if beneficiario is None:
            return False
        situacao = str(getattr(beneficiario.situacao, "value", beneficiario.situacao)).lower()
        return beneficiario.ativo is True and situacao == "ativo"

    async def has_visita_recente(self, citizen_id: UUID, days: int = 90) -> bool:
        beneficiario = await self._beneficiario_repo.get_by_citizen(citizen_id)
        if beneficiario is None:
            return False
        visitas = await self._visita_repo.list_by_beneficiario(beneficiario.id)
        if not visitas:
            return False
        limite = datetime.utcnow() - timedelta(days=max(days, 1))
        ultima_visita = max(visita.data_visita for visita in visitas)
        return ultima_visita >= limite
