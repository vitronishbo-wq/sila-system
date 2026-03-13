from __future__ import annotations
import asyncio
import pytest
from app.modules.civil_protection.application.services.corporacao_service import CorporacaoService
from app.modules.civil_protection.domain.enums import StatusCorporacao
from app.modules.civil_protection.tests._fakes import FakeRequestService, InMemoryCorporacaoRepository

def test_cadastrar_corporacao_sucesso() -> None:

    async def scenario() -> None:
        service = CorporacaoService(corporacao_repo=InMemoryCorporacaoRepository(), request_service=FakeRequestService())
        corporacao = await service.cadastrar_corporacao(nome='Corpo de Bombeiros Luanda Centro', municipio='Luanda', provincia='Luanda', endereco='Rua da Prevencao, 10', comandante='Comandante Silva', telefone='222100200')
        assert corporacao.codigo_corporacao.startswith('COR/')
        assert corporacao.status == StatusCorporacao.ATIVA
    asyncio.run(scenario())

def test_cadastrar_corporacao_falha_nome_curto() -> None:

    async def scenario() -> None:
        service = CorporacaoService(corporacao_repo=InMemoryCorporacaoRepository())
        with pytest.raises(ValueError, match='Nome'):
            await service.cadastrar_corporacao(nome='CB', municipio='Luanda', provincia='Luanda', endereco='Rua X', comandante='Comandante Y')
    asyncio.run(scenario())

def test_atualizar_status_corporacao() -> None:

    async def scenario() -> None:
        service = CorporacaoService(corporacao_repo=InMemoryCorporacaoRepository())
        corporacao = await service.cadastrar_corporacao(nome='Corpo de Bombeiros Norte', municipio='Bengo', provincia='Bengo', endereco='Av Norte', comandante='Comandante Norte')
        atualizada = await service.atualizar_status(corporacao_id=corporacao.id, status=StatusCorporacao.EM_REESTRUTURACAO, motivo='Reforma estrutural')
        assert atualizada.status == StatusCorporacao.EM_REESTRUTURACAO
        assert atualizada.ativo is True
    asyncio.run(scenario())