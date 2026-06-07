from __future__ import annotations

import asyncio
from datetime import date

import pytest

from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.services.instituicao_pesquisa_service import (
    InstituicaoPesquisaService,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import (
    NaturezaJuridicaInstituicao,
    StatusCredenciamentoInstituicao,
    TipoInstituicaoPesquisa,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.tests._fakes import (
    InMemoryInstituicaoPesquisaRepository,
)


def test_cadastrar_instituicao_sucesso() -> None:

    async def scenario() -> None:
        service = InstituicaoPesquisaService(
            instituicao_repo=InMemoryInstituicaoPesquisaRepository()
        )
        saved = await service.cadastrar_instituicao(
            sigla="INPA",
            nome="Instituto Nacional de Pesquisa Aplicada",
            nif="500000003",
            tipo=TipoInstituicaoPesquisa.INSTITUTO,
            natureza_juridica=NaturezaJuridicaInstituicao.PUBLICA,
            pais="Angola",
            provincia="Luanda",
            municipio="Luanda",
            endereco="Rua do Saber, 9",
            email_institucional="contato@inpa.ao",
        )
        assert saved.sigla == "INPA"
        assert saved.status_credenciamento == StatusCredenciamentoInstituicao.EM_ANALISE

    asyncio.run(scenario())


def test_cadastrar_instituicao_duplicada() -> None:

    async def scenario() -> None:
        service = InstituicaoPesquisaService(
            instituicao_repo=InMemoryInstituicaoPesquisaRepository()
        )
        payload = dict(
            sigla="INPA",
            nome="Instituto Nacional de Pesquisa Aplicada",
            nif="500000003",
            tipo=TipoInstituicaoPesquisa.INSTITUTO,
            natureza_juridica=NaturezaJuridicaInstituicao.PUBLICA,
            pais="Angola",
            provincia="Luanda",
            municipio="Luanda",
            endereco="Rua do Saber, 9",
            email_institucional="contato@inpa.ao",
        )
        await service.cadastrar_instituicao(**payload)
        with pytest.raises(ValueError, match="sigla"):
            await service.cadastrar_instituicao(
                sigla="INPA",
                nome="Instituto Diferente",
                nif="500000099",
                tipo=TipoInstituicaoPesquisa.INSTITUTO,
                natureza_juridica=NaturezaJuridicaInstituicao.PUBLICA,
                pais="Angola",
                provincia="Luanda",
                municipio="Luanda",
                endereco="Outra rua",
                email_institucional="novo@instituto.ao",
            )

    asyncio.run(scenario())


def test_credenciar_e_suspender_instituicao() -> None:

    async def scenario() -> None:
        service = InstituicaoPesquisaService(
            instituicao_repo=InMemoryInstituicaoPesquisaRepository()
        )
        instituicao = await service.cadastrar_instituicao(
            sigla="CNPQ",
            nome="Centro Nacional de Pesquisa e Qualidade",
            nif="500000004",
            tipo=TipoInstituicaoPesquisa.CENTRO_PESQUISA,
            natureza_juridica=NaturezaJuridicaInstituicao.PUBLICA,
            pais="Angola",
            provincia="Huambo",
            municipio="Huambo",
            endereco="Rua Principal, 1",
            email_institucional="contato@cnpq.ao",
        )
        credenciada = await service.credenciar_instituicao(
            instituicao_id=instituicao.id,
            data_credenciamento=date(2026, 3, 2),
            data_validade_credenciamento=date(2028, 3, 2),
        )
        assert credenciada.status_credenciamento == StatusCredenciamentoInstituicao.CREDENCIADA
        suspensa = await service.suspender_instituicao(instituicao.id)
        assert suspensa.status_credenciamento == StatusCredenciamentoInstituicao.SUSPENSA
        assert suspensa.ativa is False

    asyncio.run(scenario())
