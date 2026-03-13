from __future__ import annotations
import asyncio
from datetime import date, timedelta
import pytest
from apps.backend.app.modules.civil_protection.application.services.bombeiro_service import BombeiroService
from apps.backend.app.modules.civil_protection.application.services.corporacao_service import CorporacaoService
from apps.backend.app.modules.civil_protection.domain.enums import CargoBombeiro, StatusAgenteProtecao
from apps.backend.app.modules.civil_protection.tests._fakes import InMemoryBombeiroRepository, InMemoryCorporacaoRepository

def test_cadastrar_bombeiro_sucesso() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        corporacao_service = CorporacaoService(corporacao_repo=corporacao_repo)
        bombeiro_service = BombeiroService(bombeiro_repo=bombeiro_repo, corporacao_repo=corporacao_repo)
        corporacao = await corporacao_service.cadastrar_corporacao(nome='Corpo de Bombeiros Sul', municipio='Benguela', provincia='Benguela', endereco='Rua Sul', comandante='Comandante Sul')
        bombeiro = await bombeiro_service.cadastrar_bombeiro(corporacao_id=corporacao.id, nome='Joao Costa', data_nascimento=date.today() - timedelta(days=365 * 29), cpf='123.456.789-00', rg='RG123456', cargo=CargoBombeiro.SARGENTO)
        assert bombeiro.matricula.startswith('BOM/')
        assert bombeiro.status == StatusAgenteProtecao.ATIVO
    asyncio.run(scenario())

def test_cadastrar_bombeiro_falha_cpf_duplicado() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        corporacao_service = CorporacaoService(corporacao_repo=corporacao_repo)
        bombeiro_service = BombeiroService(bombeiro_repo=bombeiro_repo, corporacao_repo=corporacao_repo)
        corporacao = await corporacao_service.cadastrar_corporacao(nome='Corpo de Bombeiros Oeste', municipio='Huambo', provincia='Huambo', endereco='Rua Oeste', comandante='Comandante Oeste')
        payload = dict(corporacao_id=corporacao.id, nome='Ana Rocha', data_nascimento=date.today() - timedelta(days=365 * 28), cpf='987.654.321-00', rg='RG998877')
        await bombeiro_service.cadastrar_bombeiro(**payload)
        with pytest.raises(ValueError, match='CPF'):
            await bombeiro_service.cadastrar_bombeiro(**payload)
    asyncio.run(scenario())

def test_atualizar_status_bombeiro() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        corporacao_service = CorporacaoService(corporacao_repo=corporacao_repo)
        bombeiro_service = BombeiroService(bombeiro_repo=bombeiro_repo, corporacao_repo=corporacao_repo)
        corporacao = await corporacao_service.cadastrar_corporacao(nome='Corpo de Bombeiros Centro', municipio='Malanje', provincia='Malanje', endereco='Rua Centro', comandante='Comandante Centro')
        bombeiro = await bombeiro_service.cadastrar_bombeiro(corporacao_id=corporacao.id, nome='Carlos Lima', data_nascimento=date.today() - timedelta(days=365 * 32), cpf='321.654.987-10', rg='RG445566')
        atualizado = await bombeiro_service.atualizar_status(bombeiro_id=bombeiro.id, status=StatusAgenteProtecao.LICENCA, motivo='Licenca medica')
        assert atualizado.status == StatusAgenteProtecao.LICENCA
        assert atualizado.ativo is True
    asyncio.run(scenario())