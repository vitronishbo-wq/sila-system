from __future__ import annotations
from apps.backend.app.modules.logistics.application.ports.ambiente_service_port import AmbienteServicePort

class AmbienteServiceAdapter(AmbienteServicePort):

    async def validar_restricao_ambiental(self, origem: str, destino: str) -> bool:
        return bool(origem.strip() and destino.strip())
