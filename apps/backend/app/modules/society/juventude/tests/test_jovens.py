from __future__ import annotations
import asyncio
from datetime import date, timedelta
from uuid import uuid4
import pytest
from app.modules.society.juventude.application.services.jovem_service import JovemService
from app.modules.society.juventude.domain.enums import Escolaridade, SituacaoOcupacional, TipoVulnerabilidade
from app.modules.society.juventude.tests._fakes import FakeCitizenService, FakeEducacaoService, FakeEmpregoService, FakeRequestService, InMemoryJovemRepository

def test_cadastrar_jovem_sucesso() -> None:

    async def scenario() -> None:
        service = JovemService(jovem_repo=InMemoryJovemRepository(), citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True), request_service=FakeRequestService())
        result = await service.cadastrar_jovem(nome='Joao Jovem', data_nascimento=date.today() - timedelta(days=365 * 20), genero='M', naturalidade='Luanda', escolaridade=Escolaridade.MEDIO_COMPLETO, situacao_ocupacional=SituacaoOcupacional.ESTUDA, endereco='Rua A', municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
        assert result.numero_registro.startswith('JOV/')
        assert result.faixa_etaria.value == '18_24'
    asyncio.run(scenario())

def test_cadastrar_jovem_falha_sem_matricula() -> None:

    async def scenario() -> None:
        service = JovemService(jovem_repo=InMemoryJovemRepository(), citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=False))
        with pytest.raises(ValueError, match='matricula'):
            await service.cadastrar_jovem(nome='Joao Sem Matricula', data_nascimento=date.today() - timedelta(days=365 * 17), genero='M', naturalidade='Benguela', escolaridade=Escolaridade.MEDIO_INCOMPLETO, situacao_ocupacional=SituacaoOcupacional.ESTUDA, endereco='Rua B', municipio='Benguela', provincia='Benguela', citizen_id=uuid4())
    asyncio.run(scenario())

def test_adicionar_vulnerabilidade() -> None:

    async def scenario() -> None:
        service = JovemService(jovem_repo=InMemoryJovemRepository(), citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        jovem = await service.cadastrar_jovem(nome='Maria Jovem', data_nascimento=date.today() - timedelta(days=365 * 24), genero='F', naturalidade='Huambo', escolaridade=Escolaridade.SUPERIOR_INCOMPLETO, situacao_ocupacional=SituacaoOcupacional.PROCURA_EMPREGO, endereco='Rua C', municipio='Huambo', provincia='Huambo', citizen_id=uuid4())
        atualizado = await service.adicionar_vulnerabilidade(jovem_id=jovem.id, vulnerabilidade=TipoVulnerabilidade.BAIXA_RENDA)
        assert atualizado.vulnerabilidades is not None
        assert TipoVulnerabilidade.BAIXA_RENDA in atualizado.vulnerabilidades
    asyncio.run(scenario())