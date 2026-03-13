from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from app.modules.society.desporto.application.services.clube_service import ClubeService
from app.modules.society.desporto.application.services.competicao_service import CompeticaoService
from app.modules.society.desporto.application.services.jogo_service import JogoService
from app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusJogo, TipoClube, TipoCompeticao
from app.modules.society.desporto.tests._fakes import FakeEducacaoService, FakeObrasPublicasService, FakeRequestService, FakeTurismoService, InMemoryClubeRepository, InMemoryCompeticaoRepository, InMemoryJogoRepository

def test_agendar_jogo_sucesso() -> None:

    async def scenario() -> None:
        clube_repo = InMemoryClubeRepository()
        competicao_repo = InMemoryCompeticaoRepository()
        jogo_repo = InMemoryJogoRepository()
        clube_service = ClubeService(clube_repo=clube_repo, educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        competicao_service = CompeticaoService(competicao_repo=competicao_repo, turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        jogo_service = JogoService(jogo_repo=jogo_repo, competicao_repo=competicao_repo, clube_repo=clube_repo, turismo_service=FakeTurismoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        clube_a = await clube_service.cadastrar_clube(nome='Clube A', sigla='CLA', tipo=TipoClube.PROFISSIONAL, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Luanda', provincia='Luanda')
        clube_b = await clube_service.cadastrar_clube(nome='Clube B', sigla='CLB', tipo=TipoClube.PROFISSIONAL, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Luanda', provincia='Luanda')
        competicao = await competicao_service.cadastrar_competicao(nome='Liga Nacional', tipo=TipoCompeticao.LIGA, modalidade=ModalidadeDesportiva.FUTEBOL, data_inicio=date(2026, 2, 1), data_fim=date(2026, 6, 1), municipio='Luanda', provincia='Luanda', organizador_id=uuid4())
        jogo = await jogo_service.agendar_jogo(competicao_id=competicao.id, clube_casa_id=clube_a.id, clube_fora_id=clube_b.id, data_jogo=date(2026, 3, 10), local='Estadio Central', municipio='Luanda', provincia='Luanda', codigo_obra_instalacao='OBR/2026/000001', atracao_turistica_id=uuid4())
        assert jogo.codigo_jogo.startswith('JOG/')
        assert jogo.status == StatusJogo.AGENDADO
    asyncio.run(scenario())

def test_agendar_jogo_falha_clubes_iguais() -> None:

    async def scenario() -> None:
        clube_repo = InMemoryClubeRepository()
        competicao_repo = InMemoryCompeticaoRepository()
        jogo_service = JogoService(jogo_repo=InMemoryJogoRepository(), competicao_repo=competicao_repo, clube_repo=clube_repo, turismo_service=FakeTurismoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        clube_service = ClubeService(clube_repo=clube_repo, educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        competicao_service = CompeticaoService(competicao_repo=competicao_repo, turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        clube = await clube_service.cadastrar_clube(nome='Clube Unico', sigla='CU', tipo=TipoClube.COMUNITARIO, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Huambo', provincia='Huambo')
        competicao = await competicao_service.cadastrar_competicao(nome='Copa Local', tipo=TipoCompeticao.COPA, modalidade=ModalidadeDesportiva.FUTEBOL, data_inicio=date(2026, 1, 1), data_fim=date(2026, 1, 30), municipio='Huambo', provincia='Huambo', organizador_id=uuid4())
        with pytest.raises(ValueError, match='diferentes'):
            await jogo_service.agendar_jogo(competicao_id=competicao.id, clube_casa_id=clube.id, clube_fora_id=clube.id, data_jogo=date(2026, 1, 10), local='Campo Municipal', municipio='Huambo', provincia='Huambo')
    asyncio.run(scenario())

def test_registrar_resultado_encerrar_jogo() -> None:

    async def scenario() -> None:
        clube_repo = InMemoryClubeRepository()
        competicao_repo = InMemoryCompeticaoRepository()
        jogo_repo = InMemoryJogoRepository()
        clube_service = ClubeService(clube_repo=clube_repo, educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        competicao_service = CompeticaoService(competicao_repo=competicao_repo, turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        jogo_service = JogoService(jogo_repo=jogo_repo, competicao_repo=competicao_repo, clube_repo=clube_repo, turismo_service=FakeTurismoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        clube_a = await clube_service.cadastrar_clube(nome='Clube C', sigla='CLC', tipo=TipoClube.PROFISSIONAL, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Luanda', provincia='Luanda')
        clube_b = await clube_service.cadastrar_clube(nome='Clube D', sigla='CLD', tipo=TipoClube.PROFISSIONAL, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Luanda', provincia='Luanda')
        competicao = await competicao_service.cadastrar_competicao(nome='Taca Cidade', tipo=TipoCompeticao.COPA, modalidade=ModalidadeDesportiva.FUTEBOL, data_inicio=date(2026, 5, 1), data_fim=date(2026, 5, 31), municipio='Luanda', provincia='Luanda', organizador_id=uuid4())
        jogo = await jogo_service.agendar_jogo(competicao_id=competicao.id, clube_casa_id=clube_a.id, clube_fora_id=clube_b.id, data_jogo=date(2026, 5, 10), local='Estadio 11 de Novembro', municipio='Luanda', provincia='Luanda')
        atualizado = await jogo_service.registrar_resultado(jogo_id=jogo.id, placar_casa=2, placar_fora=1)
        assert atualizado.status == StatusJogo.ENCERRADO
        assert atualizado.placar_casa == 2
        assert atualizado.placar_fora == 1
    asyncio.run(scenario())