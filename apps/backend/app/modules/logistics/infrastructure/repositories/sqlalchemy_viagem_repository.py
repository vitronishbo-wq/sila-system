from __future__ import annotations
from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.logistics.domain.ports import ViagemRepositoryPort
from apps.backend.app.modules.logistics.domain.enums import StatusViagem
from apps.backend.app.modules.logistics.domain.models import Viagem
from apps.backend.app.modules.logistics.infrastructure.orm import ViagemModel

class SQLAlchemyViagemRepository(ViagemRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[UUID, ViagemModel] = {}

    async def save(self, viagem: Viagem) -> Viagem:
        if self._session:
            existing = await self._session.execute(select(ViagemModel).where(ViagemModel.id == viagem.id))
            model = existing.scalars().first()
            if model is None:
                model = ViagemModel(id=viagem.id, linha_id=viagem.linha_id, veiculo_id=viagem.veiculo_id, motorista_id=viagem.motorista_id, data_hora_saida=viagem.data_hora_saida, data_hora_chegada_prevista=viagem.data_hora_chegada_prevista, origem=viagem.origem, destino=viagem.destino, itinerario=deepcopy(viagem.itinerario), status=viagem.status.value, data_hora_chegada_real=viagem.data_hora_chegada_real, paradas=deepcopy(viagem.paradas), passageiros_embarcados=viagem.passageiros_embarcados, passageiros_desembarcados=viagem.passageiros_desembarcados, passageiros_transbordo=viagem.passageiros_transbordo, carga=deepcopy(viagem.carga), volume_carga=viagem.volume_carga, peso_carga=viagem.peso_carga, valor_frete=viagem.valor_frete, quilometragem_inicial=viagem.quilometragem_inicial, quilometragem_final=viagem.quilometragem_final, consumo_combustivel=viagem.consumo_combustivel, observacoes=viagem.observacoes)
                self._session.add(model)
            else:
                model.linha_id = viagem.linha_id
                model.veiculo_id = viagem.veiculo_id
                model.motorista_id = viagem.motorista_id
                model.data_hora_saida = viagem.data_hora_saida
                model.data_hora_chegada_prevista = viagem.data_hora_chegada_prevista
                model.origem = viagem.origem
                model.destino = viagem.destino
                model.itinerario = deepcopy(viagem.itinerario)
                model.status = viagem.status.value
                model.data_hora_chegada_real = viagem.data_hora_chegada_real
                model.paradas = deepcopy(viagem.paradas)
                model.passageiros_embarcados = viagem.passageiros_embarcados
                model.passageiros_desembarcados = viagem.passageiros_desembarcados
                model.passageiros_transbordo = viagem.passageiros_transbordo
                model.carga = deepcopy(viagem.carga)
                model.volume_carga = viagem.volume_carga
                model.peso_carga = viagem.peso_carga
                model.valor_frete = viagem.valor_frete
                model.quilometragem_inicial = viagem.quilometragem_inicial
                model.quilometragem_final = viagem.quilometragem_final
                model.consumo_combustivel = viagem.consumo_combustivel
                model.observacoes = viagem.observacoes
            await self._session.flush()
            return self._to_domain(model)
        model = self._to_model(viagem)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> Viagem | None:
        if self._session:
            result = await self._session.execute(select(ViagemModel).where(ViagemModel.id == id))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        model = self._items.get(id)
        return self._to_domain(model) if model else None

    async def list(self, *, status: StatusViagem | None=None, linha_id: UUID | None=None, veiculo_id: UUID | None=None) -> list[Viagem]:
        if self._session:
            statement = select(ViagemModel)
            if status:
                statement = statement.where(ViagemModel.status == status.value)
            if linha_id:
                statement = statement.where(ViagemModel.linha_id == linha_id)
            if veiculo_id:
                statement = statement.where(ViagemModel.veiculo_id == veiculo_id)
            result = await self._session.execute(statement.order_by(ViagemModel.data_hora_saida.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status.value]
        if linha_id:
            values = [item for item in values if item.linha_id == linha_id]
        if veiculo_id:
            values = [item for item in values if item.veiculo_id == veiculo_id]
        values.sort(key=lambda item: item.data_hora_saida)
        return [self._to_domain(item) for item in values]

    async def has_active_for_veiculo(self, *, veiculo_id: UUID, inicio: datetime, fim: datetime, ignore_viagem_id: UUID | None=None) -> bool:
        statuses_ativos = {StatusViagem.PROGRAMADA.value, StatusViagem.CONFIRMADA.value, StatusViagem.EM_ANDAMENTO.value, StatusViagem.ATRASADA.value}
        if self._session:
            statement = select(ViagemModel).where(ViagemModel.veiculo_id == veiculo_id)
            if ignore_viagem_id:
                statement = statement.where(ViagemModel.id != ignore_viagem_id)
            result = await self._session.execute(statement)
            for item in result.scalars().all():
                if item.status not in statuses_ativos:
                    continue
                if inicio < item.data_hora_chegada_prevista and fim > item.data_hora_saida:
                    return True
            return False
        for item in self._items.values():
            if item.veiculo_id != veiculo_id:
                continue
            if ignore_viagem_id and item.id == ignore_viagem_id:
                continue
            if item.status not in statuses_ativos:
                continue
            if inicio < item.data_hora_chegada_prevista and fim > item.data_hora_saida:
                return True
        return False

    @staticmethod
    def _to_model(viagem: Viagem) -> ViagemModel:
        return ViagemModel(id=viagem.id, linha_id=viagem.linha_id, veiculo_id=viagem.veiculo_id, motorista_id=viagem.motorista_id, data_hora_saida=viagem.data_hora_saida, data_hora_chegada_prevista=viagem.data_hora_chegada_prevista, origem=viagem.origem, destino=viagem.destino, itinerario=deepcopy(viagem.itinerario), status=viagem.status.value, data_hora_chegada_real=viagem.data_hora_chegada_real, paradas=deepcopy(viagem.paradas), passageiros_embarcados=viagem.passageiros_embarcados, passageiros_desembarcados=viagem.passageiros_desembarcados, passageiros_transbordo=viagem.passageiros_transbordo, carga=deepcopy(viagem.carga), volume_carga=viagem.volume_carga, peso_carga=viagem.peso_carga, valor_frete=viagem.valor_frete, quilometragem_inicial=viagem.quilometragem_inicial, quilometragem_final=viagem.quilometragem_final, consumo_combustivel=viagem.consumo_combustivel, observacoes=viagem.observacoes)

    @staticmethod
    def _to_domain(model: ViagemModel) -> Viagem:
        return Viagem(id=model.id, linha_id=model.linha_id, veiculo_id=model.veiculo_id, motorista_id=model.motorista_id, data_hora_saida=model.data_hora_saida, data_hora_chegada_prevista=model.data_hora_chegada_prevista, origem=model.origem, destino=model.destino, itinerario=deepcopy(model.itinerario), status=StatusViagem(model.status), data_hora_chegada_real=model.data_hora_chegada_real, paradas=deepcopy(model.paradas), passageiros_embarcados=model.passageiros_embarcados, passageiros_desembarcados=model.passageiros_desembarcados, passageiros_transbordo=model.passageiros_transbordo, carga=deepcopy(model.carga), volume_carga=Decimal(model.volume_carga) if model.volume_carga is not None else None, peso_carga=Decimal(model.peso_carga) if model.peso_carga is not None else None, valor_frete=Decimal(model.valor_frete) if model.valor_frete is not None else None, quilometragem_inicial=model.quilometragem_inicial, quilometragem_final=model.quilometragem_final, consumo_combustivel=Decimal(model.consumo_combustivel) if model.consumo_combustivel is not None else None, observacoes=model.observacoes)