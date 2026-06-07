from __future__ import annotations

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.events.definitions import (
    QualidadeServicoAferidaEvent,
)


class QualidadeHandler:
    def __init__(self) -> None:
        self.last_quality_event: QualidadeServicoAferidaEvent | None = None

    async def on_qualidade_aferida(self, event: QualidadeServicoAferidaEvent) -> None:
        self.last_quality_event = event
