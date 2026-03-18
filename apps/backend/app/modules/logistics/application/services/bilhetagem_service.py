from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.logistics.domain.ports import BilhetagemRepositoryPort, FinancasServicePort, WorkflowServicePort
from apps.backend.app.modules.logistics.domain.enums import StatusReconciliacaoFinanceira, TipoTarifa
from apps.backend.app.modules.logistics.domain.models import BilhetagemEletronica
from apps.backend.app.modules.logistics.domain.services import BilhetagemDomainService

class BilhetagemService:

    def __init__(self, *, bilhetagem_repo: BilhetagemRepositoryPort, financas_adapter: FinancasServicePort | None=None, workflow_adapter: WorkflowServicePort | None=None) -> None:
        self._domain = BilhetagemDomainService(bilhetagem_repo=bilhetagem_repo, financas_adapter=financas_adapter, workflow_adapter=workflow_adapter)

    def has_financas_adapter(self) -> bool:
        return self._domain.has_financas_adapter()

    def has_workflow_adapter(self) -> bool:
        return self._domain.has_workflow_adapter()

    async def registrar_evento(self, *, codigo_bilhete: str, viagem_id: UUID, tipo_tarifa: TipoTarifa, valor_pago: Decimal, forma_pagamento: str, metadata: dict | None=None) -> BilhetagemEletronica:
        return await self._domain.registrar_evento(codigo_bilhete=codigo_bilhete, viagem_id=viagem_id, tipo_tarifa=tipo_tarifa, valor_pago=valor_pago, forma_pagamento=forma_pagamento, metadata=metadata)

    async def reconciliar_evento(self, evento_id: UUID, *, confirmado: bool, referencia_externa: str | None=None) -> BilhetagemEletronica:
        return await self._domain.reconciliar_evento(evento_id, confirmado=confirmado, referencia_externa=referencia_externa)

    async def obter_evento(self, evento_id: UUID) -> BilhetagemEletronica:
        return await self._domain.obter_evento(evento_id)

    async def listar_eventos(self, *, viagem_id: UUID | None=None, codigo_bilhete: str | None=None, status_reconciliacao: StatusReconciliacaoFinanceira | None=None, data_inicio: datetime | None=None, data_fim: datetime | None=None) -> list[BilhetagemEletronica]:
        return await self._domain.listar_eventos(viagem_id=viagem_id, codigo_bilhete=codigo_bilhete, status_reconciliacao=status_reconciliacao, data_inicio=data_inicio, data_fim=data_fim)