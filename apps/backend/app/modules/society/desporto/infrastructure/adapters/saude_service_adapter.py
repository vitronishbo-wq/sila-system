from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.desporto.application.ports.saude_service_port import (
    SaudeServicePort,
)


class SaudeServiceAdapter(SaudeServicePort):
    def __init__(self, exame_service):
        self._exame_service = exame_service

    async def exame_exists(self, exame_id: UUID) -> bool:
        try:
            lab = await self._exame_service.get_laboratorial(exame_id)
            if lab is not None:
                return True
            img = await self._exame_service.get_imagem(exame_id)
            return img is not None
        except Exception:
            return False
