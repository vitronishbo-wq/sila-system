from __future__ import annotations
import asyncio
from datetime import date, timedelta
from uuid import uuid4
import pytest
from app.modules.society.desporto.application.services.atleta_service import AtletaService
from app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusAtleta, TipoAtleta
from app.modules.society.desporto.tests._fakes import FakeCitizenService, FakeRequestService, FakeSaudeService, InMemoryAtletaRepository

def test_cadastrar_atleta_sucesso() -> None:

    async def scenario() -> None:
        service = AtletaService(atleta_repo=InMemoryAtletaRepository(), citizen_service=FakeCitizenService(active=True), saude_service=FakeSaudeService(exists=True), request_service=FakeRequestService())
        result = await service.cadastrar_atleta(nome='Joao Atleta', data_nascimento=date.today() - timedelta(days=365 * 20), naturalidade='Luanda', nacionalidade='Angolana', tipo=TipoAtleta.PROFISSIONAL, modalidades=[ModalidadeDesportiva.FUTEBOL], citizen_id=uuid4(), ultimo_exame_id=uuid4())
        assert result.numero_registro.startswith('ATL/')
        assert result.status == StatusAtleta.ATIVO
    asyncio.run(scenario())

def test_cadastrar_atleta_falha_cidadao_inativo() -> None:

    async def scenario() -> None:
        service = AtletaService(atleta_repo=InMemoryAtletaRepository(), citizen_service=FakeCitizenService(active=False), saude_service=FakeSaudeService(exists=True), request_service=FakeRequestService())
        with pytest.raises(ValueError, match='Cidadao'):
            await service.cadastrar_atleta(nome='Atleta Invalido', data_nascimento=date.today() - timedelta(days=365 * 20), naturalidade='Luanda', nacionalidade='Angolana', tipo=TipoAtleta.AMADOR, modalidades=[ModalidadeDesportiva.ATLETISMO], citizen_id=uuid4())
    asyncio.run(scenario())

def test_registrar_lesao_e_recuperar() -> None:

    async def scenario() -> None:
        service = AtletaService(atleta_repo=InMemoryAtletaRepository(), citizen_service=FakeCitizenService(active=True), saude_service=FakeSaudeService(exists=True), request_service=FakeRequestService())
        atleta = await service.cadastrar_atleta(nome='Atleta Teste', data_nascimento=date.today() - timedelta(days=365 * 25), naturalidade='Benguela', nacionalidade='Angolana', tipo=TipoAtleta.PROFISSIONAL, modalidades=[ModalidadeDesportiva.BASQUETEBOL])
        lesionado = await service.registrar_lesao(atleta.id)
        assert lesionado.status == StatusAtleta.LESIONADO
        recuperado = await service.recuperar_atleta(atleta.id)
        assert recuperado.status == StatusAtleta.ATIVO
    asyncio.run(scenario())