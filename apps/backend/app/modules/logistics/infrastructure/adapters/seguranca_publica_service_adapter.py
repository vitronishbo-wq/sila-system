from __future__ import annotations
from apps.backend.app.modules.logistics.domain.ports.seguranca_publica_service_port import SegurancaPublicaServicePort

class SegurancaPublicaServiceAdapter(SegurancaPublicaServicePort):

    async def validar_regularidade_veiculo(self, *, placa: str) -> bool:
        normalized = placa.strip().upper()
        return len(normalized) >= 6