from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.ports.instituicao_pesquisa_repository_port import InstituicaoPesquisaRepositoryPort
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import NaturezaJuridicaInstituicao, TipoInstituicaoPesquisa
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.models.instituicao_pesquisa import InstituicaoPesquisa

class InstituicaoPesquisaService:

    def __init__(self, *, instituicao_repo: InstituicaoPesquisaRepositoryPort) -> None:
        self.instituicao_repo = instituicao_repo

    async def cadastrar_instituicao(self, *, sigla: str, nome: str, nif: str, tipo: TipoInstituicaoPesquisa, natureza_juridica: NaturezaJuridicaInstituicao, pais: str, provincia: str, municipio: str, endereco: str, email_institucional: str, telefone: str | None=None, website: str | None=None) -> InstituicaoPesquisa:
        existente_sigla = await self.instituicao_repo.get_by_sigla(sigla)
        if existente_sigla is not None:
            raise ValueError('Instituicao ja cadastrada com esta sigla')
        existente_nif = await self.instituicao_repo.get_by_nif(nif)
        if existente_nif is not None:
            raise ValueError('Instituicao ja cadastrada com este NIF')
        instituicao = InstituicaoPesquisa.cadastrar(sigla=sigla, nome=nome, nif=nif, tipo=tipo, natureza_juridica=natureza_juridica, pais=pais, provincia=provincia, municipio=municipio, endereco=endereco, email_institucional=email_institucional, telefone=telefone, website=website)
        return await self.instituicao_repo.save(instituicao)

    async def buscar_instituicao(self, instituicao_id: UUID) -> InstituicaoPesquisa:
        instituicao = await self.instituicao_repo.get_by_id(instituicao_id)
        if instituicao is None:
            raise ValueError('Instituicao de pesquisa nao encontrada')
        return instituicao

    async def listar_instituicoes(self, *, somente_ativas: bool=False) -> list[InstituicaoPesquisa]:
        if somente_ativas:
            return await self.instituicao_repo.list_ativas()
        return await self.instituicao_repo.list_all()

    async def credenciar_instituicao(self, *, instituicao_id: UUID, data_credenciamento: date | None=None, data_validade_credenciamento: date | None=None) -> InstituicaoPesquisa:
        instituicao = await self.buscar_instituicao(instituicao_id)
        instituicao.credenciar(data_credenciamento=data_credenciamento, data_validade_credenciamento=data_validade_credenciamento)
        return await self.instituicao_repo.save(instituicao)

    async def suspender_instituicao(self, instituicao_id: UUID) -> InstituicaoPesquisa:
        instituicao = await self.buscar_instituicao(instituicao_id)
        instituicao.suspender()
        return await self.instituicao_repo.save(instituicao)

    async def descredenciar_instituicao(self, instituicao_id: UUID) -> InstituicaoPesquisa:
        instituicao = await self.buscar_instituicao(instituicao_id)
        instituicao.descredenciar()
        return await self.instituicao_repo.save(instituicao)

    async def remover_instituicao(self, instituicao_id: UUID) -> None:
        deleted = await self.instituicao_repo.delete(instituicao_id)
        if not deleted:
            raise ValueError('Instituicao de pesquisa nao encontrada')