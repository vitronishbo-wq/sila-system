from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.logistics.application.ports import BilhetagemRepositoryPort, FinancasServicePort, WorkflowServicePort
from apps.backend.app.modules.logistics.domain.enums import StatusReconciliacaoFinanceira, TipoTarifa
from apps.backend.app.modules.logistics.domain.models import BilhetagemEletronica
from apps.backend.app.modules.logistics.core.exceptions import BilhetagemNotFoundError

class BilhetagemService:

    def __init__(self, *, bilhetagem_repo: BilhetagemRepositoryPort, financas_adapter: FinancasServicePort | None=None, workflow_adapter: WorkflowServicePort | None=None) -> None:
        self._bilhetagem_repo = bilhetagem_repo
        self._financas_adapter = financas_adapter
        self._workflow_adapter = workflow_adapter

    def has_financas_adapter(self) -> bool:
        return self._financas_adapter is not None

    def has_workflow_adapter(self) -> bool:
        return self._workflow_adapter is not None

    async def registrar_evento(self, *, codigo_bilhete: str, viagem_id: UUID, tipo_tarifa: TipoTarifa, valor_pago: Decimal, forma_pagamento: str, metadata: dict | None=None) -> BilhetagemEletronica:
        evento_anterior = await self._bilhetagem_repo.get_by_codigo_bilhete(codigo_bilhete)
        if evento_anterior and evento_anterior.status_reconciliacao != StatusReconciliacaoFinanceira.REJEITADO:
            raise ValueError('Codigo de bilhete ja processado para conciliacao financeira')
        evento = BilhetagemEletronica.registrar_evento(codigo_bilhete=codigo_bilhete, viagem_id=viagem_id, tipo_tarifa=tipo_tarifa, valor_pago=valor_pago, forma_pagamento=forma_pagamento, metadata=metadata)
        if self._financas_adapter:
            lancamento_id = await self._financas_adapter.registrar_receita_bilhetagem(evento_id=evento.id, valor=evento.valor_pago, forma_pagamento=evento.forma_pagamento)
            evento.vincular_lancamento(lancamento_financeiro_id=lancamento_id)
        saved = await self._bilhetagem_repo.save(evento)
        await self._registrar_evento_workflow(workflow_id=f'ticket:{saved.codigo_bilhete}', evento='bilhetagem_evento_registrado', payload={'evento_id': str(saved.id), 'valor_pago': str(saved.valor_pago), 'forma_pagamento': saved.forma_pagamento})
        return saved

    async def reconciliar_evento(self, evento_id: UUID, *, confirmado: bool, referencia_externa: str | None=None) -> BilhetagemEletronica:
        evento = await self._bilhetagem_repo.get_by_id(evento_id)
        if not evento:
            raise BilhetagemNotFoundError('Evento de bilhetagem nao encontrado')
        if not evento.lancamento_financeiro_id:
            raise ValueError('Evento sem lancamento financeiro vinculado')
        if self._financas_adapter:
            reconciliado = await self._financas_adapter.reconciliar_lancamento(lancamento_id=evento.lancamento_financeiro_id, confirmado=confirmado, referencia_externa=referencia_externa)
            if not reconciliado:
                raise ValueError('Falha na conciliacao financeira do evento')
        if confirmado:
            evento.confirmar_reconciliacao(referencia_externa=referencia_externa)
        else:
            evento.rejeitar_reconciliacao(referencia_externa=referencia_externa)
        saved = await self._bilhetagem_repo.save(evento)
        await self._registrar_evento_workflow(workflow_id=f'ticket:{saved.codigo_bilhete}', evento='bilhetagem_evento_reconciliado', payload={'evento_id': str(saved.id), 'status_reconciliacao': saved.status_reconciliacao.value, 'referencia_externa': referencia_externa})
        return saved

    async def obter_evento(self, evento_id: UUID) -> BilhetagemEletronica:
        item = await self._bilhetagem_repo.get_by_id(evento_id)
        if not item:
            raise BilhetagemNotFoundError('Evento de bilhetagem nao encontrado')
        return item

    async def listar_eventos(self, *, viagem_id: UUID | None=None, codigo_bilhete: str | None=None, status_reconciliacao: StatusReconciliacaoFinanceira | None=None, data_inicio: datetime | None=None, data_fim: datetime | None=None) -> list[BilhetagemEletronica]:
        return await self._bilhetagem_repo.list(viagem_id=viagem_id, codigo_bilhete=codigo_bilhete, status_reconciliacao=status_reconciliacao, data_inicio=data_inicio, data_fim=data_fim)

    async def _registrar_evento_workflow(self, *, workflow_id: str, evento: str, payload: dict) -> None:
        if not self._workflow_adapter:
            return
        await self._workflow_adapter.registrar_evento(workflow_id=workflow_id, evento=evento, payload=payload)
