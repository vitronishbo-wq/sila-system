from __future__ import annotations
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.intelligence.ciencia_pesquisa.application.ports.instituicao_pesquisa_repository_port import InstituicaoPesquisaRepositoryPort
from app.modules.intelligence.ciencia_pesquisa.domain.enums import NaturezaJuridicaInstituicao, StatusCredenciamentoInstituicao, TipoInstituicaoPesquisa
from app.modules.intelligence.ciencia_pesquisa.domain.models.instituicao_pesquisa import InstituicaoPesquisa
from app.modules.intelligence.ciencia_pesquisa.infrastructure.models.instituicao_pesquisa_model import InstituicaoPesquisaModel

class SQLAlchemyInstituicaoPesquisaRepository(InstituicaoPesquisaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, instituicao: InstituicaoPesquisa) -> InstituicaoPesquisa:
        model = await self.session.get(InstituicaoPesquisaModel, instituicao.id)
        if not model:
            model = InstituicaoPesquisaModel(id=instituicao.id)
            self.session.add(model)
        model.sigla = instituicao.sigla
        model.nome = instituicao.nome
        model.nif = instituicao.nif
        model.tipo = instituicao.tipo.value
        model.natureza_juridica = instituicao.natureza_juridica.value
        model.pais = instituicao.pais
        model.provincia = instituicao.provincia
        model.municipio = instituicao.municipio
        model.endereco = instituicao.endereco
        model.email_institucional = instituicao.email_institucional
        model.telefone = instituicao.telefone
        model.website = instituicao.website
        model.status_credenciamento = instituicao.status_credenciamento.value
        model.data_credenciamento = instituicao.data_credenciamento
        model.data_validade_credenciamento = instituicao.data_validade_credenciamento
        model.comite_etica_ativo = instituicao.comite_etica_ativo
        model.nucleo_inovacao_ativo = instituicao.nucleo_inovacao_ativo
        model.ativa = instituicao.ativa
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, instituicao_id: UUID) -> InstituicaoPesquisa | None:
        model = await self.session.get(InstituicaoPesquisaModel, instituicao_id)
        return self._to_domain(model) if model else None

    async def get_by_sigla(self, sigla: str) -> InstituicaoPesquisa | None:
        stmt = select(InstituicaoPesquisaModel).where(func.upper(InstituicaoPesquisaModel.sigla) == sigla.strip().upper())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_nif(self, nif: str) -> InstituicaoPesquisa | None:
        stmt = select(InstituicaoPesquisaModel).where(InstituicaoPesquisaModel.nif == nif.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[InstituicaoPesquisa]:
        stmt = select(InstituicaoPesquisaModel).order_by(InstituicaoPesquisaModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_ativas(self) -> list[InstituicaoPesquisa]:
        stmt = select(InstituicaoPesquisaModel).where(InstituicaoPesquisaModel.ativa.is_(True)).order_by(InstituicaoPesquisaModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, instituicao_id: UUID) -> bool:
        model = await self.session.get(InstituicaoPesquisaModel, instituicao_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: InstituicaoPesquisaModel) -> InstituicaoPesquisa:
        return InstituicaoPesquisa(id=model.id, sigla=model.sigla, nome=model.nome, nif=model.nif, tipo=TipoInstituicaoPesquisa(model.tipo), natureza_juridica=NaturezaJuridicaInstituicao(model.natureza_juridica), pais=model.pais, provincia=model.provincia, municipio=model.municipio, endereco=model.endereco, email_institucional=model.email_institucional, telefone=model.telefone, website=model.website, status_credenciamento=StatusCredenciamentoInstituicao(model.status_credenciamento), data_credenciamento=model.data_credenciamento, data_validade_credenciamento=model.data_validade_credenciamento, comite_etica_ativo=model.comite_etica_ativo, nucleo_inovacao_ativo=model.nucleo_inovacao_ativo, ativa=model.ativa)