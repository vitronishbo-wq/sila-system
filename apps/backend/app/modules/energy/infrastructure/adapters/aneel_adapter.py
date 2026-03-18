from __future__ import annotations
from apps.backend.app.modules.energy.infrastructure.resilience.circuit_breaker import circuit_breaker

class ANEELAdapter:

    @circuit_breaker('aneel_adapter')
    async def registrar_evento_qualidade(self, payload: dict) -> str:
        _ = payload
        return 'ANEEL-EVENT-ACCEPTED'