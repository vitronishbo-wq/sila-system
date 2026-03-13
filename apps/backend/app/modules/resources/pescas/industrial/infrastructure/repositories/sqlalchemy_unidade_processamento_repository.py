from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.resources.pescas.industrial.application.ports.unidade_processamento_repository_port import UnidadeProcessamentoRepositoryPort
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import ClassificacaoIndustrial, TipoProcessamento
from apps.backend.app.modules.resources.pescas.industrial.domain.models.unidade_processamento import UnidadeProcessamento
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.unidade_processamento_model import UnidadeProcessamentoModel

class SQLAlchemyUnidadeProcessamentoRepository(UnidadeProcessamentoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, unidade: UnidadeProcessamento) -> UnidadeProcessamento:
        model = await self.session.get(UnidadeProcessamentoModel, unidade.id)
        if not model:
            model = UnidadeProcessamentoModel(id=unidade.id)
            self.session.add(model)
        model.cnpj = unidade.cnpj
        model.razao_social = unidade.razao_social
        model.nome_fantasia = unidade.nome_fantasia
        model.inscricao_estadual = unidade.inscricao_estadual
        model.inscricao_municipal = unidade.inscricao_municipal
        model.tipo_processamento = [item.value for item in unidade.tipo_processamento]
        model.classificacao = unidade.classificacao.value
        model.capacidade_kg_dia = unidade.capacidade_kg_dia
        model.area_total_m2 = unidade.area_total_m2
        model.area_producao_m2 = unidade.area_producao_m2
        model.area_armazenagem_m2 = unidade.area_armazenagem_m2
        model.capacidade_frigorifica_m3 = unidade.capacidade_frigorifica_m3
        model.temperatura_media = unidade.temperatura_media
        model.numero_funcionarios = unidade.numero_funcionarios
        model.responsavel_tecnico_id = unidade.responsavel_tecnico_id
        model.responsavel_tecnico_registro = unidade.responsavel_tecnico_registro
        model.endereco = unidade.endereco
        model.municipio = unidade.municipio
        model.provincia = unidade.provincia
        model.coordenadas_lat = unidade.coordenadas_lat
        model.coordenadas_long = unidade.coordenadas_long
        model.armador_id = unidade.armador_id
        model.data_inauguracao = unidade.data_inauguracao
        model.licenca_operacao_id = unidade.licenca_operacao_id
        model.alvara_sanitario_id = unidade.alvara_sanitario_id
        model.certificacoes = [str(item) for item in unidade.certificacoes] if unidade.certificacoes else None
        model.observacoes = unidade.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, unidade_id: UUID) -> UnidadeProcessamento | None:
        model = await self.session.get(UnidadeProcessamentoModel, unidade_id)
        return self._to_domain(model) if model else None

    async def get_by_cnpj(self, cnpj: str) -> UnidadeProcessamento | None:
        stmt = select(UnidadeProcessamentoModel).where(UnidadeProcessamentoModel.cnpj == cnpj.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_municipio(self, municipio: str) -> list[UnidadeProcessamento]:
        stmt = select(UnidadeProcessamentoModel).where(func.lower(UnidadeProcessamentoModel.municipio) == municipio.strip().lower()).order_by(UnidadeProcessamentoModel.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoProcessamento) -> list[UnidadeProcessamento]:
        stmt = select(UnidadeProcessamentoModel).where(UnidadeProcessamentoModel.tipo_processamento.contains([tipo.value])).order_by(UnidadeProcessamentoModel.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_all(self) -> list[UnidadeProcessamento]:
        stmt = select(UnidadeProcessamentoModel).order_by(UnidadeProcessamentoModel.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, unidade_id: UUID) -> bool:
        model = await self.session.get(UnidadeProcessamentoModel, unidade_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self, provincia: str) -> str:
        ano = date.today().year
        prefix = f'{provincia.strip().upper()}/{ano}/'
        stmt = select(func.count()).select_from(UnidadeProcessamentoModel).where(UnidadeProcessamentoModel.cnpj.like('%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:05d}'

    @staticmethod
    def _to_domain(model: UnidadeProcessamentoModel) -> UnidadeProcessamento:
        return UnidadeProcessamento(id=model.id, cnpj=model.cnpj, razao_social=model.razao_social, nome_fantasia=model.nome_fantasia, inscricao_estadual=model.inscricao_estadual, inscricao_municipal=model.inscricao_municipal, tipo_processamento=[TipoProcessamento(item) for item in model.tipo_processamento], classificacao=ClassificacaoIndustrial(model.classificacao), capacidade_kg_dia=model.capacidade_kg_dia, area_total_m2=model.area_total_m2, area_producao_m2=model.area_producao_m2, area_armazenagem_m2=model.area_armazenagem_m2, capacidade_frigorifica_m3=model.capacidade_frigorifica_m3, temperatura_media=model.temperatura_media, numero_funcionarios=model.numero_funcionarios, responsavel_tecnico_id=model.responsavel_tecnico_id, responsavel_tecnico_registro=model.responsavel_tecnico_registro, endereco=model.endereco, municipio=model.municipio, provincia=model.provincia, coordenadas_lat=model.coordenadas_lat, coordenadas_long=model.coordenadas_long, armador_id=model.armador_id, data_inauguracao=model.data_inauguracao, licenca_operacao_id=model.licenca_operacao_id, alvara_sanitario_id=model.alvara_sanitario_id, certificacoes=[UUID(item) for item in model.certificacoes] if model.certificacoes else None, observacoes=model.observacoes)