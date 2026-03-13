from __future__ import annotations
from copy import deepcopy
from decimal import Decimal
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.logistics.application.ports import VeiculoRepositoryPort
from apps.backend.app.modules.logistics.domain.enums import StatusVeiculoOperacional, TipoVeiculo
from apps.backend.app.modules.logistics.domain.models import Veiculo
from apps.backend.app.modules.logistics.infrastructure.models import VeiculoModel

class SQLAlchemyVeiculoRepository(VeiculoRepositoryPort):

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, Veiculo] = {}

    async def save(self, item: Veiculo) -> Veiculo:
        if self._session:
            existing = await self._session.execute(select(VeiculoModel).where(VeiculoModel.placa == item.placa))
            model = existing.scalars().first()
            if model is None:
                model = self._to_model(item)
                self._session.add(model)
            else:
                self._update_model(model, item)
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.placa] = item
        return item

    async def get_by_id(self, veiculo_id: UUID) -> Veiculo | None:
        if self._session:
            result = await self._session.execute(select(VeiculoModel).where(VeiculoModel.id == veiculo_id))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        for item in self._items.values():
            if item.id == veiculo_id:
                return item
        return None

    async def get_by_placa(self, placa: str) -> Veiculo | None:
        normalized = placa.strip().upper()
        if self._session:
            result = await self._session.execute(select(VeiculoModel).where(VeiculoModel.placa == normalized))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(normalized)

    async def list(self, *, status: StatusVeiculoOperacional | None=None, tipo: TipoVeiculo | None=None, operadora_id: UUID | None=None) -> list[Veiculo]:
        if self._session:
            statement = select(VeiculoModel)
            if status:
                statement = statement.where(VeiculoModel.status == status.value)
            if tipo:
                statement = statement.where(VeiculoModel.tipo == tipo.value)
            if operadora_id:
                statement = statement.where(VeiculoModel.operadora_id == operadora_id)
            result = await self._session.execute(statement.order_by(VeiculoModel.placa.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if operadora_id:
            values = [item for item in values if item.operadora_id == operadora_id]
        return sorted(values, key=lambda item: item.placa)

    @staticmethod
    def _update_model(model: VeiculoModel, item: Veiculo) -> None:
        model.tipo = item.tipo.value
        model.marca = item.marca
        model.modelo = item.modelo
        model.ano_fabricacao = item.ano_fabricacao
        model.ano_modelo = item.ano_modelo
        model.proprietario_id = item.proprietario_id
        model.proprietario_tipo = item.proprietario_tipo
        model.data_aquisicao = item.data_aquisicao
        model.status = item.status.value
        model.capacidade_passageiros = item.capacidade_passageiros
        model.capacidade_carga_kg = item.capacidade_carga_kg
        model.capacidade_carga_m3 = item.capacidade_carga_m3
        model.comprimento = item.comprimento
        model.largura = item.largura
        model.altura = item.altura
        model.peso_bruto_total = item.peso_bruto_total
        model.numero_eixos = item.numero_eixos
        model.combustivel = item.combustivel
        model.consumo_medio = item.consumo_medio
        model.operadora_id = item.operadora_id
        model.licenciamento = deepcopy(item.licenciamento)
        model.seguro = deepcopy(item.seguro)
        model.rastreador_id = item.rastreador_id
        model.data_ultima_manutencao = item.data_ultima_manutencao
        model.data_proxima_manutencao = item.data_proxima_manutencao
        model.quilometragem = item.quilometragem
        model.observacoes = item.observacoes
        model.data_atualizacao = item.data_atualizacao

    @staticmethod
    def _to_model(item: Veiculo) -> VeiculoModel:
        return VeiculoModel(id=item.id, placa=item.placa, tipo=item.tipo.value, marca=item.marca, modelo=item.modelo, ano_fabricacao=item.ano_fabricacao, ano_modelo=item.ano_modelo, proprietario_id=item.proprietario_id, proprietario_tipo=item.proprietario_tipo, data_aquisicao=item.data_aquisicao, status=item.status.value, capacidade_passageiros=item.capacidade_passageiros, capacidade_carga_kg=item.capacidade_carga_kg, capacidade_carga_m3=item.capacidade_carga_m3, comprimento=item.comprimento, largura=item.largura, altura=item.altura, peso_bruto_total=item.peso_bruto_total, numero_eixos=item.numero_eixos, combustivel=item.combustivel, consumo_medio=item.consumo_medio, operadora_id=item.operadora_id, licenciamento=deepcopy(item.licenciamento), seguro=deepcopy(item.seguro), rastreador_id=item.rastreador_id, data_ultima_manutencao=item.data_ultima_manutencao, data_proxima_manutencao=item.data_proxima_manutencao, quilometragem=item.quilometragem, observacoes=item.observacoes, data_atualizacao=item.data_atualizacao)

    @staticmethod
    def _to_domain(model: VeiculoModel) -> Veiculo:
        return Veiculo(id=model.id, placa=model.placa, tipo=TipoVeiculo(model.tipo), marca=model.marca, modelo=model.modelo, ano_fabricacao=model.ano_fabricacao, ano_modelo=model.ano_modelo, proprietario_id=model.proprietario_id, proprietario_tipo=model.proprietario_tipo, data_aquisicao=model.data_aquisicao, status=StatusVeiculoOperacional(model.status), capacidade_passageiros=model.capacidade_passageiros, capacidade_carga_kg=Decimal(model.capacidade_carga_kg) if model.capacidade_carga_kg is not None else None, capacidade_carga_m3=Decimal(model.capacidade_carga_m3) if model.capacidade_carga_m3 is not None else None, comprimento=Decimal(model.comprimento) if model.comprimento is not None else None, largura=Decimal(model.largura) if model.largura is not None else None, altura=Decimal(model.altura) if model.altura is not None else None, peso_bruto_total=Decimal(model.peso_bruto_total) if model.peso_bruto_total is not None else None, numero_eixos=model.numero_eixos, combustivel=model.combustivel, consumo_medio=Decimal(model.consumo_medio) if model.consumo_medio is not None else None, operadora_id=model.operadora_id, licenciamento=deepcopy(model.licenciamento), seguro=deepcopy(model.seguro), rastreador_id=model.rastreador_id, data_ultima_manutencao=model.data_ultima_manutencao, data_proxima_manutencao=model.data_proxima_manutencao, quilometragem=model.quilometragem, observacoes=model.observacoes, data_atualizacao=model.data_atualizacao)
