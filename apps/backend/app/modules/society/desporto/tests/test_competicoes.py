from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from app.modules.society.desporto.application.services.competicao_service import CompeticaoService
from app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusCompeticao, TipoCompeticao
from app.modules.society.desporto.tests._fakes import FakeEducacaoService, FakeObrasPublicasService, FakeRequestService, FakeTurismoService, InMemoryCompeticaoRepository

def test_cadastrar_competicao_sucesso() -> None:

    async def scenario() -> None:
        service = CompeticaoService(competicao_repo=InMemoryCompeticaoRepository(), turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        result = await service.cadastrar_competicao(nome='Liga Provincial', tipo=TipoCompeticao.LIGA, modalidade=ModalidadeDesportiva.FUTEBOL, data_inicio=date(2026, 5, 1), data_fim=date(2026, 7, 1), municipio='Luanda', provincia='Luanda', organizador_id=uuid4(), codigo_obra_instalacao='OBR/2026/000001', atracao_turistica_id=uuid4(), instituicao_educacional_id=uuid4())
        assert result.codigo_competicao.startswith('CMP/')
        assert result.status == StatusCompeticao.PLANEADA
    asyncio.run(scenario())

def test_cadastrar_competicao_falha_obra_inexistente() -> None:

    async def scenario() -> None:
        service = CompeticaoService(competicao_repo=InMemoryCompeticaoRepository(), turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=False), request_service=FakeRequestService())
        with pytest.raises(ValueError, match='Obra'):
            await service.cadastrar_competicao(nome='Copa Teste', tipo=TipoCompeticao.COPA, modalidade=ModalidadeDesportiva.ANDEBOL, data_inicio=date(2026, 8, 1), data_fim=date(2026, 8, 10), municipio='Huambo', provincia='Huambo', organizador_id=uuid4(), codigo_obra_instalacao='OBR/2026/999999')
    asyncio.run(scenario())

def test_listar_competicoes_por_periodo() -> None:

    async def scenario() -> None:
        service = CompeticaoService(competicao_repo=InMemoryCompeticaoRepository(), turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        await service.cadastrar_competicao(nome='Torneio 1', tipo=TipoCompeticao.TORNEIO, modalidade=ModalidadeDesportiva.BOXE, data_inicio=date(2026, 1, 10), data_fim=date(2026, 1, 12), municipio='Lobito', provincia='Benguela', organizador_id=uuid4())
        await service.cadastrar_competicao(nome='Torneio 2', tipo=TipoCompeticao.TORNEIO, modalidade=ModalidadeDesportiva.BOXE, data_inicio=date(2026, 3, 10), data_fim=date(2026, 3, 12), municipio='Lobito', provincia='Benguela', organizador_id=uuid4())
        items = await service.listar_competicoes(data_inicio=date(2026, 1, 1), data_fim=date(2026, 2, 1))
        assert len(items) == 1
        assert items[0].nome == 'Torneio 1'
    asyncio.run(scenario())