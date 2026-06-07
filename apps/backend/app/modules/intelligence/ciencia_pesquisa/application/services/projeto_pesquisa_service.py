from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.ports.instituicao_pesquisa_repository_port import (
    InstituicaoPesquisaRepositoryPort,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.ports.pesquisador_repository_port import (
    PesquisadorRepositoryPort,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.ports.projeto_pesquisa_repository_port import (
    ProjetoPesquisaRepositoryPort,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import AreaConhecimento
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.models.projeto_pesquisa import (
    ProjetoPesquisa,
)


class ProjetoPesquisaService:
    def __init__(
        self,
        *,
        projeto_repo: ProjetoPesquisaRepositoryPort,
        instituicao_repo: InstituicaoPesquisaRepositoryPort,
        pesquisador_repo: PesquisadorRepositoryPort,
    ) -> None:
        self.projeto_repo = projeto_repo
        self.instituicao_repo = instituicao_repo
        self.pesquisador_repo = pesquisador_repo

    async def cadastrar_projeto(
        self,
        *,
        titulo: str,
        resumo: str,
        instituicao_id: UUID,
        coordenador_id: UUID,
        equipe_pesquisadores_ids: list[UUID] | None = None,
        area_conhecimento: AreaConhecimento = AreaConhecimento.MULTIDISCIPLINAR,
        data_inicio: date | None = None,
        data_fim_prevista: date | None = None,
        palavras_chave: list[str] | None = None,
        orcamento_previsto: float | None = None,
        codigo_projeto: str | None = None,
    ) -> ProjetoPesquisa:
        instituicao = await self.instituicao_repo.get_by_id(instituicao_id)
        if instituicao is None:
            raise ValueError("Instituicao de pesquisa nao encontrada")
        coordenador = await self.pesquisador_repo.get_by_id(coordenador_id)
        if coordenador is None:
            raise ValueError("Coordenador do projeto nao encontrado")
        codigo = (codigo_projeto or "").strip() or await self.projeto_repo.next_codigo()
        existente = await self.projeto_repo.get_by_codigo(codigo)
        if existente is not None:
            raise ValueError("Projeto ja cadastrado com este codigo")
        equipe_ids = list(dict.fromkeys(equipe_pesquisadores_ids or []))
        if coordenador_id not in equipe_ids:
            equipe_ids.append(coordenador_id)
        for pesquisador_id in equipe_ids:
            pesquisador = await self.pesquisador_repo.get_by_id(pesquisador_id)
            if pesquisador is None:
                raise ValueError("Pesquisador da equipe nao encontrado")
        projeto = ProjetoPesquisa.cadastrar(
            codigo_projeto=codigo,
            titulo=titulo,
            resumo=resumo,
            instituicao_id=instituicao_id,
            coordenador_id=coordenador_id,
            equipe_pesquisadores_ids=equipe_ids,
            area_conhecimento=area_conhecimento,
            data_inicio=data_inicio,
            data_fim_prevista=data_fim_prevista,
            palavras_chave=palavras_chave,
            orcamento_previsto=orcamento_previsto,
        )
        return await self.projeto_repo.save(projeto)

    async def buscar_projeto(self, projeto_id: UUID) -> ProjetoPesquisa:
        projeto = await self.projeto_repo.get_by_id(projeto_id)
        if projeto is None:
            raise ValueError("Projeto de pesquisa nao encontrado")
        return projeto

    async def listar_projetos(
        self, *, instituicao_id: UUID | None = None, pesquisador_id: UUID | None = None
    ) -> list[ProjetoPesquisa]:
        if instituicao_id is not None:
            return await self.projeto_repo.list_by_instituicao(instituicao_id)
        if pesquisador_id is not None:
            return await self.projeto_repo.list_by_pesquisador(pesquisador_id)
        return await self.projeto_repo.list_all()

    async def vincular_pesquisadores(
        self, *, projeto_id: UUID, pesquisador_ids: list[UUID]
    ) -> ProjetoPesquisa:
        for pesquisador_id in pesquisador_ids:
            pesquisador = await self.pesquisador_repo.get_by_id(pesquisador_id)
            if pesquisador is None:
                raise ValueError("Pesquisador da equipe nao encontrado")
        atualizado = await self.projeto_repo.vincular_pesquisadores(
            projeto_id=projeto_id, pesquisador_ids=pesquisador_ids
        )
        if atualizado is not None:
            return atualizado
        projeto = await self.buscar_projeto(projeto_id)
        projeto.vincular_pesquisadores(pesquisador_ids)
        return await self.projeto_repo.save(projeto)

    async def encerrar_projeto(
        self, *, projeto_id: UUID, data_fim_real: date | None = None
    ) -> ProjetoPesquisa:
        projeto = await self.buscar_projeto(projeto_id)
        projeto.encerrar(data_fim_real=data_fim_real)
        return await self.projeto_repo.save(projeto)

    async def aprovar_projeto(self, projeto_id: UUID) -> ProjetoPesquisa:
        projeto = await self.buscar_projeto(projeto_id)
        projeto.aprovar()
        return await self.projeto_repo.save(projeto)

    async def iniciar_execucao_projeto(self, projeto_id: UUID) -> ProjetoPesquisa:
        projeto = await self.buscar_projeto(projeto_id)
        projeto.iniciar_execucao()
        return await self.projeto_repo.save(projeto)

    async def suspender_projeto(self, projeto_id: UUID) -> ProjetoPesquisa:
        projeto = await self.buscar_projeto(projeto_id)
        projeto.suspender()
        return await self.projeto_repo.save(projeto)

    async def remover_projeto(self, projeto_id: UUID) -> None:
        deleted = await self.projeto_repo.delete(projeto_id)
        if not deleted:
            raise ValueError("Projeto de pesquisa nao encontrado")
