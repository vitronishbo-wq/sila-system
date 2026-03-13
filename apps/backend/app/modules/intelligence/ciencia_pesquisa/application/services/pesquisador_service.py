from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.intelligence.ciencia_pesquisa.application.ports.instituicao_pesquisa_repository_port import InstituicaoPesquisaRepositoryPort
from app.modules.intelligence.ciencia_pesquisa.application.ports.pesquisador_repository_port import PesquisadorRepositoryPort
from app.modules.intelligence.ciencia_pesquisa.domain.enums import AreaConhecimento, NivelFormacao, StatusVinculoPesquisador, TipoVinculoPesquisador
from app.modules.intelligence.ciencia_pesquisa.domain.models.pesquisador import Pesquisador

class PesquisadorService:

    def __init__(self, *, pesquisador_repo: PesquisadorRepositoryPort, instituicao_repo: InstituicaoPesquisaRepositoryPort | None=None) -> None:
        self.pesquisador_repo = pesquisador_repo
        self.instituicao_repo = instituicao_repo

    async def cadastrar_pesquisador(self, *, nome_completo: str, documento_identificacao: str, email_institucional: str, instituicao_id: UUID | None=None, unidade_pesquisa_id: UUID | None=None, area_conhecimento: AreaConhecimento=AreaConhecimento.MULTIDISCIPLINAR, nivel_formacao: NivelFormacao=NivelFormacao.GRADUADO, tipo_vinculo: TipoVinculoPesquisador=TipoVinculoPesquisador.EFETIVO, data_inicio_vinculo: date | None=None, telefone: str | None=None, orcid: str | None=None, lattes_url: str | None=None, researcher_id: str | None=None, scopus_id: str | None=None) -> Pesquisador:
        existente_documento = await self.pesquisador_repo.get_by_documento(documento_identificacao)
        if existente_documento is not None:
            raise ValueError('Pesquisador ja cadastrado com este documento')
        existente_email = await self.pesquisador_repo.get_by_email(email_institucional)
        if existente_email is not None:
            raise ValueError('Pesquisador ja cadastrado com este email institucional')
        if instituicao_id is not None and self.instituicao_repo is not None:
            instituicao = await self.instituicao_repo.get_by_id(instituicao_id)
            if instituicao is None:
                raise ValueError('Instituicao de pesquisa nao encontrada')
        pesquisador = Pesquisador.cadastrar(nome_completo=nome_completo, documento_identificacao=documento_identificacao, email_institucional=email_institucional, instituicao_id=instituicao_id, unidade_pesquisa_id=unidade_pesquisa_id, area_conhecimento=area_conhecimento, nivel_formacao=nivel_formacao, tipo_vinculo=tipo_vinculo, data_inicio_vinculo=data_inicio_vinculo, telefone=telefone, orcid=orcid, lattes_url=lattes_url, researcher_id=researcher_id, scopus_id=scopus_id)
        return await self.pesquisador_repo.save(pesquisador)

    async def buscar_pesquisador(self, pesquisador_id: UUID) -> Pesquisador:
        pesquisador = await self.pesquisador_repo.get_by_id(pesquisador_id)
        if pesquisador is None:
            raise ValueError('Pesquisador nao encontrado')
        return pesquisador

    async def listar_pesquisadores(self, *, instituicao_id: UUID | None=None) -> list[Pesquisador]:
        if instituicao_id is not None:
            return await self.pesquisador_repo.list_by_instituicao(instituicao_id)
        return await self.pesquisador_repo.list_all()

    async def vincular_instituicao(self, *, pesquisador_id: UUID, instituicao_id: UUID, unidade_pesquisa_id: UUID | None=None) -> Pesquisador:
        if self.instituicao_repo is not None:
            instituicao = await self.instituicao_repo.get_by_id(instituicao_id)
            if instituicao is None:
                raise ValueError('Instituicao de pesquisa nao encontrada')
        atualizado = await self.pesquisador_repo.vincular_instituicao(pesquisador_id=pesquisador_id, instituicao_id=instituicao_id, unidade_pesquisa_id=unidade_pesquisa_id)
        if atualizado is not None:
            return atualizado
        pesquisador = await self.buscar_pesquisador(pesquisador_id)
        pesquisador.instituicao_id = instituicao_id
        pesquisador.atualizar_vinculo(status_vinculo=StatusVinculoPesquisador.ATIVO, unidade_pesquisa_id=unidade_pesquisa_id)
        return await self.pesquisador_repo.save(pesquisador)

    async def encerrar_vinculo(self, *, pesquisador_id: UUID, data_fim_vinculo: date | None=None) -> Pesquisador:
        pesquisador = await self.buscar_pesquisador(pesquisador_id)
        pesquisador.encerrar_vinculo(data_fim_vinculo=data_fim_vinculo)
        return await self.pesquisador_repo.save(pesquisador)

    async def remover_pesquisador(self, pesquisador_id: UUID) -> None:
        deleted = await self.pesquisador_repo.delete(pesquisador_id)
        if not deleted:
            raise ValueError('Pesquisador nao encontrado')