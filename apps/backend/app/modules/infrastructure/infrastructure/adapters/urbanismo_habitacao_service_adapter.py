from __future__ import annotations
from apps.backend.app.modules.infrastructure.application.ports.urbanismo_habitacao_service_port import UrbanismoHabitacaoServicePort
from apps.backend.app.modules.infrastructure.domain.enums import TipoObra

class UrbanismoHabitacaoServiceAdapter(UrbanismoHabitacaoServicePort):

    async def validar_conformidade_urbanistica(self, *, endereco: str, bairro: str, municipio: str, provincia: str, tipo_obra: TipoObra) -> bool:
        _ = tipo_obra
        return all([endereco.strip(), bairro.strip(), municipio.strip(), provincia.strip()])