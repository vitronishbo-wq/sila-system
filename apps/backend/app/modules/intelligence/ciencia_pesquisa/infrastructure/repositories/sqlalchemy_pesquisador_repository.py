from __future__ import annotations
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.intelligence.ciencia_pesquisa.application.ports.pesquisador_repository_port import PesquisadorRepositoryPort
from app.modules.intelligence.ciencia_pesquisa.domain.enums import AreaConhecimento, NivelFormacao, StatusVinculoPesquisador, TipoVinculoPesquisador
from app.modules.intelligence.ciencia_pesquisa.domain.models.pesquisador import Pesquisador
from app.modules.intelligence.ciencia_pesquisa.infrastructure.models.pesquisador_model import PesquisadorModel

class SQLAlchemyPesquisadorRepository(PesquisadorRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, pesquisador: Pesquisador) -> Pesquisador:
        model = await self.session.get(PesquisadorModel, pesquisador.id)
        if not model:
            model = PesquisadorModel(id=pesquisador.id)
            self.session.add(model)
        model.nome_completo = pesquisador.nome_completo
        model.documento_identificacao = pesquisador.documento_identificacao
        model.email_institucional = pesquisador.email_institucional
        model.instituicao_id = pesquisador.instituicao_id
        model.unidade_pesquisa_id = pesquisador.unidade_pesquisa_id
        model.area_conhecimento = pesquisador.area_conhecimento.value
        model.nivel_formacao = pesquisador.nivel_formacao.value
        model.tipo_vinculo = pesquisador.tipo_vinculo.value
        model.status_vinculo = pesquisador.status_vinculo.value
        model.data_inicio_vinculo = pesquisador.data_inicio_vinculo
        model.data_fim_vinculo = pesquisador.data_fim_vinculo
        model.telefone = pesquisador.telefone
        model.orcid = pesquisador.orcid
        model.lattes_url = pesquisador.lattes_url
        model.researcher_id = pesquisador.researcher_id
        model.scopus_id = pesquisador.scopus_id
        model.ativo = pesquisador.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, pesquisador_id: UUID) -> Pesquisador | None:
        model = await self.session.get(PesquisadorModel, pesquisador_id)
        return self._to_domain(model) if model else None

    async def get_by_documento(self, documento_identificacao: str) -> Pesquisador | None:
        stmt = select(PesquisadorModel).where(PesquisadorModel.documento_identificacao == documento_identificacao.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_email(self, email_institucional: str) -> Pesquisador | None:
        normalized = email_institucional.strip().lower()
        stmt = select(PesquisadorModel).where(func.lower(PesquisadorModel.email_institucional) == normalized)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Pesquisador]:
        stmt = select(PesquisadorModel).order_by(PesquisadorModel.nome_completo.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_instituicao(self, instituicao_id: UUID) -> list[Pesquisador]:
        stmt = select(PesquisadorModel).where(PesquisadorModel.instituicao_id == instituicao_id).order_by(PesquisadorModel.nome_completo.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def vincular_instituicao(self, *, pesquisador_id: UUID, instituicao_id: UUID, unidade_pesquisa_id: UUID | None=None) -> Pesquisador | None:
        model = await self.session.get(PesquisadorModel, pesquisador_id)
        if not model:
            return None
        model.instituicao_id = instituicao_id
        model.unidade_pesquisa_id = unidade_pesquisa_id
        model.status_vinculo = StatusVinculoPesquisador.ATIVO.value
        model.ativo = True
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def delete(self, pesquisador_id: UUID) -> bool:
        model = await self.session.get(PesquisadorModel, pesquisador_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: PesquisadorModel) -> Pesquisador:
        return Pesquisador(id=model.id, nome_completo=model.nome_completo, documento_identificacao=model.documento_identificacao, email_institucional=model.email_institucional, instituicao_id=model.instituicao_id, unidade_pesquisa_id=model.unidade_pesquisa_id, area_conhecimento=AreaConhecimento(model.area_conhecimento), nivel_formacao=NivelFormacao(model.nivel_formacao), tipo_vinculo=TipoVinculoPesquisador(model.tipo_vinculo), status_vinculo=StatusVinculoPesquisador(model.status_vinculo), data_inicio_vinculo=model.data_inicio_vinculo, data_fim_vinculo=model.data_fim_vinculo, telefone=model.telefone, orcid=model.orcid, lattes_url=model.lattes_url, researcher_id=model.researcher_id, scopus_id=model.scopus_id, ativo=model.ativo)