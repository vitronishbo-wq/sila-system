from __future__ import annotations

from apps.backend.app.modules.infrastructure.application.ports.transportes_service_port import (
    TransportesServicePort,
)
from apps.backend.app.modules.infrastructure.domain.enums import TipoObra


class TransportesServiceAdapter(TransportesServicePort):
    async def validar_impacto_viario(
        self, *, municipio: str, provincia: str, tipo_obra: TipoObra
    ) -> bool:
        _ = tipo_obra
        return bool(municipio.strip() and provincia.strip())
