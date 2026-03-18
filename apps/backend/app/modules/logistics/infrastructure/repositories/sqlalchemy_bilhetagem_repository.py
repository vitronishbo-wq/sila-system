from __future__ import annotations
from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.logistics.domain.ports import BilhetagemRepositoryPort
from apps.backend.app.modules.logistics.domain.enums import StatusReconciliacaoFinanceira, TipoTarifa
from apps.backend.app.modules.logistics.domain.models import BilhetagemEletronica
from apps.backend.app.modules.logistics.infrastructure.orm import BilhetagemEventoModel

class SQLAlchemyBilhetagemRepository(BilhetagemRepositoryPort):

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[UUID, BilhetagemEletronica] = {}

    async def save(self, item: BilhetagemEletronica) -> BilhetagemEletronica:
        if self._session:
            existing = await self._session.execute(select(BilhetagemEventoModel).where(BilhetagemEventoModel.id == item.id))
            model = existing.scalars().first()
            if model is None:
                model = self._to_model(item)
                self._session.add(model)
            else:
                self._update_model(model, item)
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.id] = item
        return item

    async def get_by_id(self, evento_id: UUID) -> BilhetagemEletronica | None:
        if self._session:
            result = await self._session.execute(select(BilhetagemEventoModel).where(BilhetagemEventoModel.id == evento_id))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(evento_id)

    async def get_by_codigo_bilhete(self, codigo_bilhete: str) -> BilhetagemEletronica | None:
        normalized = codigo_bilhete.strip()
        if self._session:
            result = await self._session.execute(select(BilhetagemEventoModel).where(BilhetagemEventoModel.codigo_bilhete == normalized).order_by(BilhetagemEventoModel.data_evento.desc()))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        candidates = [item for item in self._items.values() if item.codigo_bilhete == normalized]
        if not candidates:
            return None
        candidates.sort(key=lambda item: item.data_evento, reverse=True)
        return candidates[0]

    async def list(self, *, viagem_id: UUID | None=None, codigo_bilhete: str | None=None, status_reconciliacao: StatusReconciliacaoFinanceira | None=None, data_inicio: datetime | None=None, data_fim: datetime | None=None) -> list[BilhetagemEletronica]:
        if self._session:
            statement = select(BilhetagemEventoModel)
            if viagem_id:
                statement = statement.where(BilhetagemEventoModel.viagem_id == viagem_id)
            if codigo_bilhete:
                statement = statement.where(BilhetagemEventoModel.codigo_bilhete == codigo_bilhete.strip())
            if status_reconciliacao:
                statement = statement.where(BilhetagemEventoModel.status_reconciliacao == status_reconciliacao.value)
            if data_inicio:
                statement = statement.where(BilhetagemEventoModel.data_evento >= data_inicio)
            if data_fim:
                statement = statement.where(BilhetagemEventoModel.data_evento <= data_fim)
            result = await self._session.execute(statement.order_by(BilhetagemEventoModel.data_evento.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if viagem_id:
            values = [item for item in values if item.viagem_id == viagem_id]
        if codigo_bilhete:
            normalized = codigo_bilhete.strip()
            values = [item for item in values if item.codigo_bilhete == normalized]
        if status_reconciliacao:
            values = [item for item in values if item.status_reconciliacao == status_reconciliacao]
        if data_inicio:
            values = [item for item in values if item.data_evento >= data_inicio]
        if data_fim:
            values = [item for item in values if item.data_evento <= data_fim]
        return sorted(values, key=lambda item: item.data_evento)

    @staticmethod
    def _update_model(model: BilhetagemEventoModel, item: BilhetagemEletronica) -> None:
        model.codigo_bilhete = item.codigo_bilhete
        model.viagem_id = item.viagem_id
        model.tipo_tarifa = item.tipo_tarifa.value
        model.valor_pago = item.valor_pago
        model.forma_pagamento = item.forma_pagamento
        model.data_evento = item.data_evento
        model.status_reconciliacao = item.status_reconciliacao.value
        model.lancamento_financeiro_id = item.lancamento_financeiro_id
        model.referencia_externa = item.referencia_externa
        model.metadata_json = deepcopy(item.metadata)

    @staticmethod
    def _to_model(item: BilhetagemEletronica) -> BilhetagemEventoModel:
        return BilhetagemEventoModel(id=item.id, codigo_bilhete=item.codigo_bilhete, viagem_id=item.viagem_id, tipo_tarifa=item.tipo_tarifa.value, valor_pago=item.valor_pago, forma_pagamento=item.forma_pagamento, data_evento=item.data_evento, status_reconciliacao=item.status_reconciliacao.value, lancamento_financeiro_id=item.lancamento_financeiro_id, referencia_externa=item.referencia_externa, metadata_json=deepcopy(item.metadata))

    @staticmethod
    def _to_domain(model: BilhetagemEventoModel) -> BilhetagemEletronica:
        return BilhetagemEletronica(id=model.id, codigo_bilhete=model.codigo_bilhete, viagem_id=model.viagem_id, tipo_tarifa=TipoTarifa(model.tipo_tarifa), valor_pago=Decimal(model.valor_pago), forma_pagamento=model.forma_pagamento, data_evento=model.data_evento, status_reconciliacao=StatusReconciliacaoFinanceira(model.status_reconciliacao), lancamento_financeiro_id=model.lancamento_financeiro_id, referencia_externa=model.referencia_externa, metadata=deepcopy(model.metadata_json or {}))