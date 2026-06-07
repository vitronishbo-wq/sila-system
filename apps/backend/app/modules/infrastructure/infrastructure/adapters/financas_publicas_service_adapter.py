from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.infrastructure.application.ports.financas_publicas_service_port import (
    FinancasPublicasServicePort,
)


class FinancasPublicasServiceAdapter(FinancasPublicasServicePort):
    async def reservar_dotacao(self, orgao_id: UUID, valor: Decimal) -> bool:
        return True
