from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.resources.agricultura.application.ports import FinancasServicePort

class FinancasServiceAdapter(FinancasServicePort):

    async def registrar_credito_rural(self, produtor_id: UUID, valor: float) -> bool:
        return bool(produtor_id) and valor >= 0