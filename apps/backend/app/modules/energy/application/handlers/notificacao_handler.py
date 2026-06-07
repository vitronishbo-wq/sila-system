from __future__ import annotations

from apps.backend.app.modules.energy.application.events.definitions import (
    DemandaCriticaEvent,
    InterrupcaoEvent,
)


class NotificacaoHandler:
    def __init__(self) -> None:
        self.last_notification: dict | None = None

    async def on_interrupcao(self, event: InterrupcaoEvent) -> None:
        self.last_notification = {
            "tipo": "interrupcao",
            "causa": event.causa,
            "consumidores_afetados": event.consumidores_afetados,
        }

    async def on_demanda_critica(self, event: DemandaCriticaEvent) -> None:
        self.last_notification = {
            "tipo": "demanda_critica",
            "subestacao_id": str(event.subestacao_id),
            "alerta_nivel": event.alerta_nivel,
        }
