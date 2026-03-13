from __future__ import annotations
from copy import deepcopy
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.logistics.application.ports import LinhaRepositoryPort
from apps.backend.app.modules.logistics.domain.enums import ModalTransporte, StatusLinha, TipoViagem
from apps.backend.app.modules.logistics.domain.models import Linha
from apps.backend.app.modules.logistics.infrastructure.models import LinhaModel

class SQLAlchemyLinhaRepository(LinhaRepositoryPort):

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, Linha] = {}
        self._seq = 0

    async def save(self, item: Linha) -> Linha:
        if self._session:
            existing = await self._session.execute(select(LinhaModel).where(LinhaModel.codigo == item.codigo))
            model = existing.scalars().first()
            if model is None:
                model = self._to_model(item)
                self._session.add(model)
            else:
                self._update_model(model, item)
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo] = item
        return item

    async def get_by_codigo(self, codigo: str) -> Linha | None:
        if self._session:
            result = await self._session.execute(select(LinhaModel).where(LinhaModel.codigo == codigo))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo)

    async def get_by_id(self, linha_id: UUID) -> Linha | None:
        if self._session:
            result = await self._session.execute(select(LinhaModel).where(LinhaModel.id == linha_id))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        for item in self._items.values():
            if item.id == linha_id:
                return item
        return None

    async def list(self, *, status: StatusLinha | None=None, modal: ModalTransporte | None=None, operadora_id: UUID | None=None, origem: str | None=None, destino: str | None=None) -> list[Linha]:
        if self._session:
            statement = select(LinhaModel)
            if status:
                statement = statement.where(LinhaModel.status == status.value)
            if modal:
                statement = statement.where(LinhaModel.modal == modal.value)
            if operadora_id:
                statement = statement.where(LinhaModel.operadora_id == operadora_id)
            if origem:
                statement = statement.where(func.lower(LinhaModel.origem) == origem.strip().lower())
            if destino:
                statement = statement.where(func.lower(LinhaModel.destino) == destino.strip().lower())
            result = await self._session.execute(statement.order_by(LinhaModel.codigo.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if modal:
            values = [item for item in values if item.modal == modal]
        if operadora_id:
            values = [item for item in values if item.operadora_id == operadora_id]
        if origem:
            ori = origem.strip().lower()
            values = [item for item in values if item.origem.lower() == ori]
        if destino:
            des = destino.strip().lower()
            values = [item for item in values if item.destino.lower() == des]
        return sorted(values, key=lambda item: item.codigo)

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'LIN/{year}/'
            result = await self._session.execute(select(func.count()).select_from(LinhaModel).where(LinhaModel.codigo.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'LIN/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _update_model(model: LinhaModel, item: Linha) -> None:
        model.nome = item.nome
        model.modal = item.modal.value
        model.tipo_viagem = item.tipo_viagem.value
        model.origem = item.origem
        model.destino = item.destino
        model.itinerario = deepcopy(item.itinerario)
        model.extensao_km = item.extensao_km
        model.tempo_estimado_minutos = item.tempo_estimado_minutos
        model.dias_operacao = list(item.dias_operacao)
        model.horario_inicio = item.horario_inicio
        model.horario_fim = item.horario_fim
        model.tarifa_base = item.tarifa_base
        model.operadora_id = item.operadora_id
        model.status = item.status.value
        model.data_cadastro = item.data_cadastro
        model.frequencia_media_minutos = item.frequencia_media_minutos
        model.concessionaria_id = item.concessionaria_id
        model.outorga_id = item.outorga_id
        model.data_inicio_operacao = item.data_inicio_operacao
        model.data_autorizacao = item.data_autorizacao
        model.data_validade_autorizacao = item.data_validade_autorizacao
        model.frota_necessaria = item.frota_necessaria
        model.frota_operante = item.frota_operante
        model.demanda_media_diaria = item.demanda_media_diaria
        model.oferta_media_diaria = item.oferta_media_diaria
        model.ocupacao_media = item.ocupacao_media
        model.regularidade = item.regularidade
        model.pontualidade = item.pontualidade
        model.acessivel = item.acessivel
        model.ar_condicionado = item.ar_condicionado
        model.wifi = item.wifi
        model.sanitario = item.sanitario
        model.observacoes = item.observacoes
        model.data_atualizacao = item.data_atualizacao
        model.veiculos_ativos = deepcopy(item.veiculos_ativos)
        model.trilha_auditoria = deepcopy(item.trilha_auditoria)

    @staticmethod
    def _to_model(item: Linha) -> LinhaModel:
        return LinhaModel(id=item.id, codigo=item.codigo, nome=item.nome, modal=item.modal.value, tipo_viagem=item.tipo_viagem.value, origem=item.origem, destino=item.destino, itinerario=deepcopy(item.itinerario), extensao_km=item.extensao_km, tempo_estimado_minutos=item.tempo_estimado_minutos, dias_operacao=list(item.dias_operacao), horario_inicio=item.horario_inicio, horario_fim=item.horario_fim, tarifa_base=item.tarifa_base, operadora_id=item.operadora_id, status=item.status.value, data_cadastro=item.data_cadastro, frequencia_media_minutos=item.frequencia_media_minutos, concessionaria_id=item.concessionaria_id, outorga_id=item.outorga_id, data_inicio_operacao=item.data_inicio_operacao, data_autorizacao=item.data_autorizacao, data_validade_autorizacao=item.data_validade_autorizacao, frota_necessaria=item.frota_necessaria, frota_operante=item.frota_operante, demanda_media_diaria=item.demanda_media_diaria, oferta_media_diaria=item.oferta_media_diaria, ocupacao_media=item.ocupacao_media, regularidade=item.regularidade, pontualidade=item.pontualidade, acessivel=item.acessivel, ar_condicionado=item.ar_condicionado, wifi=item.wifi, sanitario=item.sanitario, observacoes=item.observacoes, data_atualizacao=item.data_atualizacao, veiculos_ativos=deepcopy(item.veiculos_ativos), trilha_auditoria=deepcopy(item.trilha_auditoria))

    @staticmethod
    def _to_domain(model: LinhaModel) -> Linha:
        return Linha(id=model.id, codigo=model.codigo, nome=model.nome, modal=ModalTransporte(model.modal), tipo_viagem=TipoViagem(model.tipo_viagem), origem=model.origem, destino=model.destino, itinerario=deepcopy(model.itinerario or []), extensao_km=Decimal(model.extensao_km), tempo_estimado_minutos=model.tempo_estimado_minutos, dias_operacao=list(model.dias_operacao or []), horario_inicio=model.horario_inicio, horario_fim=model.horario_fim, tarifa_base=Decimal(model.tarifa_base), operadora_id=model.operadora_id, status=StatusLinha(model.status), data_cadastro=model.data_cadastro, frequencia_media_minutos=model.frequencia_media_minutos, concessionaria_id=model.concessionaria_id, outorga_id=model.outorga_id, data_inicio_operacao=model.data_inicio_operacao, data_autorizacao=model.data_autorizacao, data_validade_autorizacao=model.data_validade_autorizacao, frota_necessaria=model.frota_necessaria, frota_operante=model.frota_operante, demanda_media_diaria=model.demanda_media_diaria, oferta_media_diaria=model.oferta_media_diaria, ocupacao_media=Decimal(model.ocupacao_media) if model.ocupacao_media is not None else None, regularidade=Decimal(model.regularidade) if model.regularidade is not None else None, pontualidade=Decimal(model.pontualidade) if model.pontualidade is not None else None, acessivel=model.acessivel, ar_condicionado=model.ar_condicionado, wifi=model.wifi, sanitario=model.sanitario, observacoes=model.observacoes, data_atualizacao=model.data_atualizacao, veiculos_ativos=deepcopy(model.veiculos_ativos or []), trilha_auditoria=deepcopy(model.trilha_auditoria or []))
