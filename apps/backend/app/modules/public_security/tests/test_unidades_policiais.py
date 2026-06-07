from __future__ import annotations

import asyncio

import pytest

from apps.backend.app.modules.public_security.application.services.unidade_policial_service import (
    UnidadePolicialService,
)
from apps.backend.app.modules.public_security.domain.enums import (
    StatusUnidadePolicial,
    TipoUnidadePolicial,
)
from apps.backend.app.modules.public_security.tests._fakes import (
    FakeRequestService,
    InMemoryUnidadePolicialRepository,
)


def test_cadastrar_unidade_sucesso() -> None:

    async def scenario() -> None:
        service = UnidadePolicialService(
            unidade_repo=InMemoryUnidadePolicialRepository(), request_service=FakeRequestService()
        )
        unidade = await service.cadastrar_unidade(
            nome="1a Delegacia Central",
            tipo=TipoUnidadePolicial.DELEGACIA,
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua da Seguranca, 100",
            comandante="Comissario Silva",
            telefone="222000111",
        )
        assert unidade.codigo_unidade.startswith("UND/")
        assert unidade.status == StatusUnidadePolicial.ATIVA

    asyncio.run(scenario())


def test_cadastrar_unidade_falha_nome_curto() -> None:

    async def scenario() -> None:
        service = UnidadePolicialService(unidade_repo=InMemoryUnidadePolicialRepository())
        with pytest.raises(ValueError, match="Nome"):
            await service.cadastrar_unidade(
                nome="DP",
                tipo=TipoUnidadePolicial.DELEGACIA,
                municipio="Luanda",
                provincia="Luanda",
                endereco="Rua X",
                comandante="Comissario X",
            )

    asyncio.run(scenario())


def test_atualizar_status_unidade() -> None:

    async def scenario() -> None:
        service = UnidadePolicialService(unidade_repo=InMemoryUnidadePolicialRepository())
        unidade = await service.cadastrar_unidade(
            nome="Batalhao Norte",
            tipo=TipoUnidadePolicial.BATALHAO,
            municipio="Bengo",
            provincia="Bengo",
            endereco="Avenida Norte",
            comandante="Capitao Norte",
        )
        atualizada = await service.atualizar_status(
            unidade_id=unidade.id, status=StatusUnidadePolicial.MANUTENCAO, motivo="Reforma predial"
        )
        assert atualizada.status == StatusUnidadePolicial.MANUTENCAO
        assert atualizada.ativo is True

    asyncio.run(scenario())
