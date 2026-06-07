from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.resources.aguas_saneamento.application.ports.ambiente_service_port import (
    AmbienteServicePort,
)


class AmbienteServiceAdapter(AmbienteServicePort):
    async def validar_corpo_hidrico(self, corpo_hidrico_id: UUID) -> bool:
        return corpo_hidrico_id is not None
