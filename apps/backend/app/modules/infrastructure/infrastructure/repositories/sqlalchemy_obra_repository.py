from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure.application.ports.obra_repository_port import ObraRepositoryPort
from apps.backend.app.modules.infrastructure.domain.enums import NaturezaObra, StatusObra, TipoObra
from apps.backend.app.modules.infrastructure.domain.models.obra import Obra
from apps.backend.app.modules.infrastructure.infrastructure.models.obra_model import ObraModel

class SQLAlchemyObraRepository(ObraRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, Obra] = {}
        self._seq = 0

    async def save(self, item: Obra) -> Obra:
        if self._session:
            existing = await self._session.execute(select(ObraModel).where(ObraModel.codigo_obra == item.codigo_obra))
            model = existing.scalars().first()
            if model is None:
                model = ObraModel(id=item.id, codigo_obra=item.codigo_obra, nome=item.nome, tipo=item.tipo.value, natureza=item.natureza.value, status=item.status.value, orgao_responsavel_id=item.orgao_responsavel_id, orgao_responsavel_tipo=item.orgao_responsavel_tipo, valor_orcado=item.valor_orcado, data_inicio_prevista=item.data_inicio_prevista, data_fim_prevista=item.data_fim_prevista, endereco=item.endereco, bairro=item.bairro, municipio=item.municipio, provincia=item.provincia, prazo_original_dias=item.prazo_original_dias, data_cadastro=item.data_cadastro, descricao=item.descricao, gestor_responsavel_id=item.gestor_responsavel_id, fiscal_responsavel_id=item.fiscal_responsavel_id, empreiteira_id=item.empreiteira_id, contrato_id=item.contrato_id, projeto_id=item.projeto_id, valor_contratado=item.valor_contratado, valor_executado=item.valor_executado, valor_pago=item.valor_pago, data_inicio_real=item.data_inicio_real, data_fim_real=item.data_fim_real, data_entrega=item.data_entrega, coordenadas_lat=item.coordenadas_lat, coordenadas_long=item.coordenadas_long, imovel_id=item.imovel_id, percentual_executado=item.percentual_executado, prazo_adicionado_dias=item.prazo_adicionado_dias, dias_corridos=item.dias_corridos, dias_atraso=item.dias_atraso, data_atualizacao=item.data_atualizacao, observacoes=item.observacoes, medicoes=item.medicoes, aditivos=item.aditivos, fiscalizacoes=item.fiscalizacoes, termos_recebimento=item.termos_recebimento, trilha_auditoria=item.trilha_auditoria)
                self._session.add(model)
            else:
                model.nome = item.nome
                model.tipo = item.tipo.value
                model.natureza = item.natureza.value
                model.status = item.status.value
                model.orgao_responsavel_id = item.orgao_responsavel_id
                model.orgao_responsavel_tipo = item.orgao_responsavel_tipo
                model.valor_orcado = item.valor_orcado
                model.data_inicio_prevista = item.data_inicio_prevista
                model.data_fim_prevista = item.data_fim_prevista
                model.endereco = item.endereco
                model.bairro = item.bairro
                model.municipio = item.municipio
                model.provincia = item.provincia
                model.prazo_original_dias = item.prazo_original_dias
                model.data_cadastro = item.data_cadastro
                model.descricao = item.descricao
                model.gestor_responsavel_id = item.gestor_responsavel_id
                model.fiscal_responsavel_id = item.fiscal_responsavel_id
                model.empreiteira_id = item.empreiteira_id
                model.contrato_id = item.contrato_id
                model.projeto_id = item.projeto_id
                model.valor_contratado = item.valor_contratado
                model.valor_executado = item.valor_executado
                model.valor_pago = item.valor_pago
                model.data_inicio_real = item.data_inicio_real
                model.data_fim_real = item.data_fim_real
                model.data_entrega = item.data_entrega
                model.coordenadas_lat = item.coordenadas_lat
                model.coordenadas_long = item.coordenadas_long
                model.imovel_id = item.imovel_id
                model.percentual_executado = item.percentual_executado
                model.prazo_adicionado_dias = item.prazo_adicionado_dias
                model.dias_corridos = item.dias_corridos
                model.dias_atraso = item.dias_atraso
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
                model.medicoes = item.medicoes
                model.aditivos = item.aditivos
                model.fiscalizacoes = item.fiscalizacoes
                model.termos_recebimento = item.termos_recebimento
                model.trilha_auditoria = item.trilha_auditoria
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_obra] = item
        return item

    async def get_by_codigo(self, codigo_obra: str) -> Obra | None:
        if self._session:
            result = await self._session.execute(select(ObraModel).where(ObraModel.codigo_obra == codigo_obra))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_obra)

    async def list(self, *, status: StatusObra | None=None, orgao_responsavel_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None) -> list[Obra]:
        if self._session:
            statement = select(ObraModel)
            if status:
                statement = statement.where(ObraModel.status == status.value)
            if orgao_responsavel_id:
                statement = statement.where(ObraModel.orgao_responsavel_id == orgao_responsavel_id)
            if municipio:
                statement = statement.where(func.lower(ObraModel.municipio) == municipio.strip().lower())
            if provincia:
                statement = statement.where(func.lower(ObraModel.provincia) == provincia.strip().lower())
            result = await self._session.execute(statement.order_by(ObraModel.codigo_obra.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if orgao_responsavel_id:
            values = [item for item in values if item.orgao_responsavel_id == orgao_responsavel_id]
        if municipio:
            mun = municipio.strip().lower()
            values = [item for item in values if item.municipio.lower() == mun]
        if provincia:
            prov = provincia.strip().lower()
            values = [item for item in values if item.provincia.lower() == prov]
        return values

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'OBR/{year}/'
            result = await self._session.execute(select(func.count()).select_from(ObraModel).where(ObraModel.codigo_obra.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'OBR/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: ObraModel) -> Obra:
        return Obra(id=model.id, codigo_obra=model.codigo_obra, nome=model.nome, tipo=TipoObra(model.tipo), natureza=NaturezaObra(model.natureza), status=StatusObra(model.status), orgao_responsavel_id=model.orgao_responsavel_id, orgao_responsavel_tipo=model.orgao_responsavel_tipo, valor_orcado=Decimal(model.valor_orcado), data_inicio_prevista=model.data_inicio_prevista, data_fim_prevista=model.data_fim_prevista, endereco=model.endereco, bairro=model.bairro, municipio=model.municipio, provincia=model.provincia, prazo_original_dias=model.prazo_original_dias, data_cadastro=model.data_cadastro, descricao=model.descricao, gestor_responsavel_id=model.gestor_responsavel_id, fiscal_responsavel_id=model.fiscal_responsavel_id, empreiteira_id=model.empreiteira_id, contrato_id=model.contrato_id, projeto_id=model.projeto_id, valor_contratado=Decimal(model.valor_contratado) if model.valor_contratado is not None else None, valor_executado=Decimal(model.valor_executado) if model.valor_executado is not None else None, valor_pago=Decimal(model.valor_pago) if model.valor_pago is not None else None, data_inicio_real=model.data_inicio_real, data_fim_real=model.data_fim_real, data_entrega=model.data_entrega, coordenadas_lat=Decimal(model.coordenadas_lat) if model.coordenadas_lat is not None else None, coordenadas_long=Decimal(model.coordenadas_long) if model.coordenadas_long is not None else None, imovel_id=model.imovel_id, percentual_executado=Decimal(model.percentual_executado), prazo_adicionado_dias=model.prazo_adicionado_dias, dias_corridos=model.dias_corridos, dias_atraso=model.dias_atraso, data_atualizacao=model.data_atualizacao, observacoes=model.observacoes, medicoes=list(model.medicoes or []), aditivos=list(model.aditivos or []), fiscalizacoes=list(model.fiscalizacoes or []), termos_recebimento=list(model.termos_recebimento or []), trilha_auditoria=list(model.trilha_auditoria or []))
