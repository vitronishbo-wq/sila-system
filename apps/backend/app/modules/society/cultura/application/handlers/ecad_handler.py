from __future__ import annotations

from apps.backend.app.modules.society.cultura.application.events import EventoProgramadoEvent


def build_ecad_handler(ecad_adapter):

    async def _handler(event: EventoProgramadoEvent) -> None:
        await ecad_adapter.registrar_execucao_publica(
            {
                "evento_id": str(event.evento_id),
                "nome": event.nome,
                "tipo": event.tipo,
                "local": event.local,
                "data_inicio": event.data_inicio,
                "data_fim": event.data_fim,
                "capacidade": event.capacidade,
            }
        )

    return _handler
