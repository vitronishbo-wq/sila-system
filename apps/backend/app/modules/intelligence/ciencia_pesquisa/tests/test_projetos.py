from __future__ import annotations

import asyncio
from datetime import date
from uuid import uuid4

import pytest

from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.services.projeto_pesquisa_service import (
    ProjetoPesquisaService,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import (
    AreaConhecimento,
    NaturezaJuridicaInstituicao,
    StatusProjetoPesquisa,
    TipoInstituicaoPesquisa,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.tests._fakes import (
    InMemoryInstituicaoPesquisaRepository,
    InMemoryPesquisadorRepository,
    InMemoryProjetoPesquisaRepository,
)


async def _seed_instituicao(instituicao_repo: InMemoryInstituicaoPesquisaRepository):
    from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.models.instituicao_pesquisa import (
        InstituicaoPesquisa,
    )

    instituicao = InstituicaoPesquisa.cadastrar(
        sigla="INCP",
        nome="Instituto Nacional de Ciencia Publica",
        nif="500000020",
        tipo=TipoInstituicaoPesquisa.INSTITUTO,
        natureza_juridica=NaturezaJuridicaInstituicao.PUBLICA,
        pais="Angola",
        provincia="Luanda",
        municipio="Luanda",
        endereco="Rua das Academias, 22",
        email_institucional="contato@incp.ao",
    )
    return await instituicao_repo.save(instituicao)


async def _seed_pesquisador(
    pesquisador_repo: InMemoryPesquisadorRepository, nome: str, documento: str, email: str
):
    from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.models.pesquisador import (
        Pesquisador,
    )

    pesquisador = Pesquisador.cadastrar(
        nome_completo=nome, documento_identificacao=documento, email_institucional=email
    )
    return await pesquisador_repo.save(pesquisador)


def test_cadastrar_projeto_sucesso() -> None:

    async def scenario() -> None:
        instituicao_repo = InMemoryInstituicaoPesquisaRepository()
        pesquisador_repo = InMemoryPesquisadorRepository()
        projeto_repo = InMemoryProjetoPesquisaRepository()
        service = ProjetoPesquisaService(
            projeto_repo=projeto_repo,
            instituicao_repo=instituicao_repo,
            pesquisador_repo=pesquisador_repo,
        )
        instituicao = await _seed_instituicao(instituicao_repo)
        coordenador = await _seed_pesquisador(
            pesquisador_repo, "Laura Mendes", "BI010101", "laura@incp.ao"
        )
        projeto = await service.cadastrar_projeto(
            titulo="Projeto Integrado de Biotecnologia",
            resumo="Pesquisa aplicada para desenvolvimento de biotecnologia em saude.",
            instituicao_id=instituicao.id,
            coordenador_id=coordenador.id,
            area_conhecimento=AreaConhecimento.CIENCIAS_BIOLOGICAS,
            data_inicio=date(2026, 3, 2),
            data_fim_prevista=date(2027, 3, 2),
            palavras_chave=["biotecnologia", "inovacao"],
        )
        assert projeto.codigo_projeto.startswith("PROJ/")
        assert projeto.coordenador_id in projeto.equipe_pesquisadores_ids
        assert projeto.status == StatusProjetoPesquisa.SUBMETIDO

    asyncio.run(scenario())


def test_cadastrar_projeto_falha_sem_instituicao() -> None:

    async def scenario() -> None:
        service = ProjetoPesquisaService(
            projeto_repo=InMemoryProjetoPesquisaRepository(),
            instituicao_repo=InMemoryInstituicaoPesquisaRepository(),
            pesquisador_repo=InMemoryPesquisadorRepository(),
        )
        coordenador_repo = service.pesquisador_repo
        coordenador = await _seed_pesquisador(
            coordenador_repo, "Paulo Costa", "BI020202", "paulo@incp.ao"
        )
        with pytest.raises(ValueError, match="Instituicao"):
            await service.cadastrar_projeto(
                titulo="Projeto sem Instituicao",
                resumo="Resumo valido para o cadastro do projeto.",
                instituicao_id=uuid4(),
                coordenador_id=coordenador.id,
            )

    asyncio.run(scenario())


def test_vincular_e_encerrar_projeto() -> None:

    async def scenario() -> None:
        instituicao_repo = InMemoryInstituicaoPesquisaRepository()
        pesquisador_repo = InMemoryPesquisadorRepository()
        projeto_repo = InMemoryProjetoPesquisaRepository()
        service = ProjetoPesquisaService(
            projeto_repo=projeto_repo,
            instituicao_repo=instituicao_repo,
            pesquisador_repo=pesquisador_repo,
        )
        instituicao = await _seed_instituicao(instituicao_repo)
        coordenador = await _seed_pesquisador(
            pesquisador_repo, "Rita Dias", "BI030303", "rita@incp.ao"
        )
        pesquisador2 = await _seed_pesquisador(
            pesquisador_repo, "Joao Pires", "BI040404", "joao@incp.ao"
        )
        projeto = await service.cadastrar_projeto(
            titulo="Projeto de Agricultura de Precisao",
            resumo="Pesquisa de tecnicas e sensores para agricultura de precisao.",
            instituicao_id=instituicao.id,
            coordenador_id=coordenador.id,
            area_conhecimento=AreaConhecimento.CIENCIAS_AGRARIAS,
        )
        atualizado = await service.vincular_pesquisadores(
            projeto_id=projeto.id, pesquisador_ids=[pesquisador2.id]
        )
        assert pesquisador2.id in atualizado.equipe_pesquisadores_ids
        encerrado = await service.encerrar_projeto(
            projeto_id=projeto.id, data_fim_real=date(2026, 12, 31)
        )
        assert encerrado.status == StatusProjetoPesquisa.ENCERRADO
        assert encerrado.ativo is False

    asyncio.run(scenario())


def test_fluxo_status_projeto() -> None:

    async def scenario() -> None:
        instituicao_repo = InMemoryInstituicaoPesquisaRepository()
        pesquisador_repo = InMemoryPesquisadorRepository()
        projeto_repo = InMemoryProjetoPesquisaRepository()
        service = ProjetoPesquisaService(
            projeto_repo=projeto_repo,
            instituicao_repo=instituicao_repo,
            pesquisador_repo=pesquisador_repo,
        )
        instituicao = await _seed_instituicao(instituicao_repo)
        coordenador = await _seed_pesquisador(
            pesquisador_repo, "Andre Lima", "BI050505", "andre@incp.ao"
        )
        projeto = await service.cadastrar_projeto(
            titulo="Projeto de Energia Limpa",
            resumo="Pesquisa sobre modelos sustentaveis de energia limpa.",
            instituicao_id=instituicao.id,
            coordenador_id=coordenador.id,
            area_conhecimento=AreaConhecimento.ENGENHARIAS,
        )
        aprovado = await service.aprovar_projeto(projeto.id)
        assert aprovado.status == StatusProjetoPesquisa.APROVADO
        em_execucao = await service.iniciar_execucao_projeto(projeto.id)
        assert em_execucao.status == StatusProjetoPesquisa.EM_EXECUCAO
        suspenso = await service.suspender_projeto(projeto.id)
        assert suspenso.status == StatusProjetoPesquisa.SUSPENSO

    asyncio.run(scenario())
