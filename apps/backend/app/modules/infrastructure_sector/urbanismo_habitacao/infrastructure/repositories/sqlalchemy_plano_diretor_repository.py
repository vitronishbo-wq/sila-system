from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.plano_diretor_repository_port import PlanoDiretorRepositoryPort
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusPlanoDiretor, TipoPlanoDiretor
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.plano_diretor import PlanoDiretor
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.plano_diretor_model import PlanoDiretorModel

class SQLAlchemyPlanoDiretorRepository(PlanoDiretorRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, PlanoDiretor] = {}
        self._seq = 0

    async def save(self, item: PlanoDiretor) -> PlanoDiretor:
        if self._session:
            existing = await self._session.execute(select(PlanoDiretorModel).where(PlanoDiretorModel.codigo_plano == item.codigo_plano))
            model = existing.scalars().first()
            if model is None:
                model = PlanoDiretorModel(id=item.id, codigo_plano=item.codigo_plano, nome=item.nome, tipo=item.tipo.value, status=item.status.value, provincia=item.provincia, ano_elaboracao=item.ano_elaboracao, orgao_responsavel_id=item.orgao_responsavel_id, municipio=item.municipio, ano_aprovacao=item.ano_aprovacao, ano_publicacao=item.ano_publicacao, periodo_validade_inicio=item.periodo_validade_inicio, periodo_validade_fim=item.periodo_validade_fim, lei_aprovacao=item.lei_aprovacao, participantes_consulta=item.participantes_consulta, audiencias_publicas=item.audiencias_publicas, documento_url=item.documento_url, mapa_url=item.mapa_url, area_total_urbana=item.area_total_urbana, area_total_rural=item.area_total_rural, populacao_estimada=item.populacao_estimada, densidade_media=item.densidade_media, macrozoneamento=item.macrozoneamento, diretrizes_gerais=item.diretrizes_gerais, objetivos_estrategicos=item.objetivos_estrategicos, observacoes=item.observacoes, data_publicacao=item.data_publicacao)
                self._session.add(model)
            else:
                model.nome = item.nome
                model.tipo = item.tipo.value
                model.status = item.status.value
                model.provincia = item.provincia
                model.ano_elaboracao = item.ano_elaboracao
                model.orgao_responsavel_id = item.orgao_responsavel_id
                model.municipio = item.municipio
                model.ano_aprovacao = item.ano_aprovacao
                model.ano_publicacao = item.ano_publicacao
                model.periodo_validade_inicio = item.periodo_validade_inicio
                model.periodo_validade_fim = item.periodo_validade_fim
                model.lei_aprovacao = item.lei_aprovacao
                model.participantes_consulta = item.participantes_consulta
                model.audiencias_publicas = item.audiencias_publicas
                model.documento_url = item.documento_url
                model.mapa_url = item.mapa_url
                model.area_total_urbana = item.area_total_urbana
                model.area_total_rural = item.area_total_rural
                model.populacao_estimada = item.populacao_estimada
                model.densidade_media = item.densidade_media
                model.macrozoneamento = item.macrozoneamento
                model.diretrizes_gerais = item.diretrizes_gerais
                model.objetivos_estrategicos = item.objetivos_estrategicos
                model.observacoes = item.observacoes
                model.data_publicacao = item.data_publicacao
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_plano] = item
        return item

    async def get_by_codigo(self, codigo_plano: str) -> PlanoDiretor | None:
        if self._session:
            result = await self._session.execute(select(PlanoDiretorModel).where(PlanoDiretorModel.codigo_plano == codigo_plano))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_plano)

    async def list(self, *, status: StatusPlanoDiretor | None=None, tipo: TipoPlanoDiretor | None=None, provincia: str | None=None) -> list[PlanoDiretor]:
        if self._session:
            statement = select(PlanoDiretorModel)
            if status:
                statement = statement.where(PlanoDiretorModel.status == status.value)
            if tipo:
                statement = statement.where(PlanoDiretorModel.tipo == tipo.value)
            if provincia:
                statement = statement.where(func.lower(PlanoDiretorModel.provincia) == provincia.strip().lower())
            result = await self._session.execute(statement.order_by(PlanoDiretorModel.codigo_plano.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if provincia:
            values = [item for item in values if item.provincia.lower() == provincia.lower()]
        return values

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'PD/{year}/'
            result = await self._session.execute(select(func.count()).select_from(PlanoDiretorModel).where(PlanoDiretorModel.codigo_plano.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'PD/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: PlanoDiretorModel) -> PlanoDiretor:
        return PlanoDiretor(id=model.id, codigo_plano=model.codigo_plano, nome=model.nome, tipo=TipoPlanoDiretor(model.tipo), status=StatusPlanoDiretor(model.status), provincia=model.provincia, ano_elaboracao=model.ano_elaboracao, orgao_responsavel_id=model.orgao_responsavel_id, municipio=model.municipio, ano_aprovacao=model.ano_aprovacao, ano_publicacao=model.ano_publicacao, periodo_validade_inicio=model.periodo_validade_inicio, periodo_validade_fim=model.periodo_validade_fim, lei_aprovacao=model.lei_aprovacao, participantes_consulta=model.participantes_consulta, audiencias_publicas=model.audiencias_publicas, documento_url=model.documento_url, mapa_url=model.mapa_url, area_total_urbana=Decimal(model.area_total_urbana) if model.area_total_urbana is not None else None, area_total_rural=Decimal(model.area_total_rural) if model.area_total_rural is not None else None, populacao_estimada=model.populacao_estimada, densidade_media=Decimal(model.densidade_media) if model.densidade_media is not None else None, macrozoneamento=model.macrozoneamento, diretrizes_gerais=model.diretrizes_gerais, objetivos_estrategicos=model.objetivos_estrategicos, observacoes=model.observacoes, data_publicacao=model.data_publicacao)