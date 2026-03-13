from __future__ import annotations
from datetime import datetime
from typing import Any
from uuid import UUID
from app.modules.justice.bounded_contexts.application.ports.saude_service_port import SaudeServicePort
from app.core.resilience import circuit_breaker, with_retry

class SaudeServiceAdapter(SaudeServicePort):

    def __init__(self, medical_record_repo: Any):
        self._medical_record_repo = medical_record_repo

    @with_retry()
    @circuit_breaker()
    async def get_resumo_saude(self, citizen_id: UUID) -> dict[str, Any] | None:
        registros = await self._medical_record_repo.get_by_citizen(citizen_id, skip=0, limit=20)
        if not registros:
            return None

        def _stamp(item) -> datetime:
            return item.updated_at or item.created_at or datetime.min
        ultimo = max(registros, key=_stamp)
        return {'total_registros': len(registros), 'ultimo_registro_id': str(ultimo.id), 'ultimo_numero': ultimo.record_number, 'ultimo_diagnostico': ultimo.diagnosis, 'ultimo_retorno': ultimo.follow_up_date.isoformat() if ultimo.follow_up_date else None}

    @with_retry()
    @circuit_breaker()
    async def has_registro_medico(self, citizen_id: UUID) -> bool:
        registros = await self._medical_record_repo.get_by_citizen(citizen_id, skip=0, limit=1)
        return bool(registros)