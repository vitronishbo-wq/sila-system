from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.resources.pescas.application.ports import ComercioExternoServicePort


class ComercioExternoServiceAdapter(ComercioExternoServicePort):
    def __init__(self, service: ComercioExternoServicePort):
        self._service = service

    async def registrar_exportacao_pescado(
        self, *, captura_id: UUID, destino: str, quantidade_kg: Decimal
    ) -> bool:
        return await self._service.registrar_exportacao_pescado(
            captura_id=captura_id, destino=destino, quantidade_kg=quantidade_kg
        )
