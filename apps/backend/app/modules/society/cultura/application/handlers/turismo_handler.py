from __future__ import annotations

from apps.backend.app.modules.society.cultura.application.events import EventoProgramadoEvent


def build_turismo_handler(turismo_adapter):

    async def _handler(event: EventoProgramadoEvent) -> None:
        await turismo_adapter.notificar_evento(
            {
                "evento_id": str(event.evento_id),
                "nome": event.nome,
                "tipo": event.tipo,
                "inicio": event.data_inicio,
                "fim": event.data_fim,
                "local": event.local,
            }
        )

    return _handler
