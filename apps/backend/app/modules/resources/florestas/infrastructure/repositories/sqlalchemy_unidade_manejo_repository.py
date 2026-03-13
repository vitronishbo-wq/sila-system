from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.resources.florestas.application.ports.unidade_manejo_repository_port import UnidadeManejoRepositoryPort
from app.modules.resources.florestas.domain.enums import TipoCicloCorte, TipoManejo
from app.modules.resources.florestas.domain.models.unidade_manejo import UnidadeManejo
from app.modules.resources.florestas.infrastructure.models.unidade_manejo_model import UnidadeManejoModel

class SQLAlchemyUnidadeManejoRepository(UnidadeManejoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, unidade: UnidadeManejo) -> UnidadeManejo:
        model = await self.session.get(UnidadeManejoModel, unidade.id)
        if not model:
            model = UnidadeManejoModel(id=unidade.id)
            self.session.add(model)
        model.codigo_um = unidade.codigo_um
        model.nome = unidade.nome
        model.area_total_ha = unidade.area_total_ha
        model.area_manejo_ha = unidade.area_manejo_ha
        model.area_preservacao_ha = unidade.area_preservacao_ha
        model.tipo_manejo = unidade.tipo_manejo.value
        model.ciclo_corte = unidade.ciclo_corte.value
        model.operador_id = unidade.operador_id
        model.imovel_id = unidade.imovel_id
        model.plano_manejo_id = unidade.plano_manejo_id
        model.licenca_id = unidade.licenca_id
        model.data_criacao = unidade.data_criacao
        model.data_aprovacao = unidade.data_aprovacao
        model.data_validade = unidade.data_validade
        model.coordenadas_centroide = unidade.coordenadas_centroide
        model.arquivo_shp = unidade.arquivo_shp
        model.observacoes = unidade.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, unidade_id: UUID) -> UnidadeManejo | None:
        model = await self.session.get(UnidadeManejoModel, unidade_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_um: str) -> UnidadeManejo | None:
        stmt = select(UnidadeManejoModel).where(UnidadeManejoModel.codigo_um == codigo_um)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_operador(self, operador_id: UUID) -> list[UnidadeManejo]:
        stmt = select(UnidadeManejoModel).where(UnidadeManejoModel.operador_id == operador_id)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_by_tipo(self, tipo_manejo: TipoManejo) -> list[UnidadeManejo]:
        stmt = select(UnidadeManejoModel).where(UnidadeManejoModel.tipo_manejo == tipo_manejo.value)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def next_codigo(self, operador_id: UUID) -> str:
        ano = date.today().year
        prefixo = f'UM/{operador_id}/{ano}/'
        stmt = select(func.count()).select_from(UnidadeManejoModel).where(UnidadeManejoModel.codigo_um.like(f'{prefixo}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefixo}{count + 1:04d}'

    @staticmethod
    def _to_domain(model: UnidadeManejoModel) -> UnidadeManejo:
        return UnidadeManejo(id=model.id, codigo_um=model.codigo_um, nome=model.nome, area_total_ha=model.area_total_ha, area_manejo_ha=model.area_manejo_ha, area_preservacao_ha=model.area_preservacao_ha, tipo_manejo=TipoManejo(model.tipo_manejo), ciclo_corte=TipoCicloCorte(model.ciclo_corte), operador_id=model.operador_id, imovel_id=model.imovel_id, plano_manejo_id=model.plano_manejo_id, licenca_id=model.licenca_id, data_criacao=model.data_criacao, data_aprovacao=model.data_aprovacao, data_validade=model.data_validade, coordenadas_centroide=model.coordenadas_centroide, arquivo_shp=model.arquivo_shp, observacoes=model.observacoes)
SqlalchemyUnidadeManejoRepository = SQLAlchemyUnidadeManejoRepository