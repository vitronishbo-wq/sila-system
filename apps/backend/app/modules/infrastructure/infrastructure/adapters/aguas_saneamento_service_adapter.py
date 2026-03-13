from __future__ import annotations
from apps.backend.app.modules.infrastructure.application.ports.aguas_saneamento_service_port import AguasSaneamentoServicePort
from apps.backend.app.modules.infrastructure.domain.enums import TipoObra

class AguasSaneamentoServiceAdapter(AguasSaneamentoServicePort):

    async def validar_capacidade_rede(self, *, municipio: str, provincia: str, tipo_obra: TipoObra) -> bool:
        _ = tipo_obra
        return bool(municipio.strip() and provincia.strip())
