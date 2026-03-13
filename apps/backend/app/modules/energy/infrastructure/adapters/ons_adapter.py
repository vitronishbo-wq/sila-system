from __future__ import annotations
import os
from apps.backend.app.modules.energy.application.ports.ons_service_port import ONSServicePort
from apps.backend.app.modules.energy.domain.enums import BandeiraTarifaria
from apps.backend.app.modules.energy.infrastructure.resilience.circuit_breaker import circuit_breaker

class ONSAdapter(ONSServicePort):

    @circuit_breaker('ons_adapter')
    async def get_bandeira_tarifaria(self) -> BandeiraTarifaria:
        raw = os.getenv('ENERGIA_BANDEIRA_TARIFARIA', 'verde').strip().lower()
        mapping = {'verde': BandeiraTarifaria.VERDE, 'amarela': BandeiraTarifaria.AMARELA, 'vermelha_patamar_1': BandeiraTarifaria.VERMELHA_PATAMAR_1, 'vermelha_patamar_2': BandeiraTarifaria.VERMELHA_PATAMAR_2, 'escassez_hidrica': BandeiraTarifaria.ESCASSEZ_HIDRICA}
        return mapping.get(raw, BandeiraTarifaria.VERDE)
