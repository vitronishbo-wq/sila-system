from __future__ import annotations

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.events.definitions import (
    QualidadeServicoAferidaEvent,
    ReclamacaoTelecomAbertaEvent,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.adapters.anatel_adapter import (
    AnatelAdapter,
)


class AnatelHandler:
    def __init__(self, *, anatel_adapter: AnatelAdapter | None = None) -> None:
        self._anatel_adapter = anatel_adapter
        self.records: list[dict] = []

    async def on_reclamacao_aberta(self, event: ReclamacaoTelecomAbertaEvent) -> None:
        payload = {
            "tipo": "reclamacao",
            "protocolo": event.protocolo,
            "assinante_id": str(event.assinante_id),
            "prioridade": event.prioridade,
            "categoria": event.tipo,
        }
        self.records.append(payload)
        if self._anatel_adapter is None:
            return
        await self._anatel_adapter.registrar_reclamacao(payload)

    async def on_qualidade_aferida(self, event: QualidadeServicoAferidaEvent) -> None:
        if event.conforme:
            return
        payload = {
            "tipo": "qualidade",
            "assinante_id": str(event.assinante_id),
            "referencia": event.referencia,
            "latencia_ms": str(event.latencia_ms),
            "download_mbps": str(event.download_mbps),
            "upload_mbps": str(event.upload_mbps),
        }
        self.records.append(payload)
        if self._anatel_adapter is None:
            return
        await self._anatel_adapter.registrar_alerta_qualidade(payload)
