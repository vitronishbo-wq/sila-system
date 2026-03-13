from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from app.modules.society.desporto.application.services.clube_service import ClubeService
from app.modules.society.desporto.domain.enums import ModalidadeDesportiva, TipoClube
from app.modules.society.desporto.tests._fakes import FakeEducacaoService, FakeObrasPublicasService, FakeRequestService, InMemoryClubeRepository

def test_cadastrar_clube_sucesso() -> None:

    async def scenario() -> None:
        service = ClubeService(clube_repo=InMemoryClubeRepository(), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        result = await service.cadastrar_clube(nome='Clube Atletico Luanda', sigla='CAL', tipo=TipoClube.PROFISSIONAL, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Luanda', provincia='Luanda', data_fundacao=date(1974, 1, 1), codigo_obra_instalacao='OBR/2026/000001', instituicao_educacional_id=uuid4())
        assert result.codigo_clube.startswith('CLB/')
        assert result.sigla == 'CAL'
    asyncio.run(scenario())

def test_cadastrar_clube_falha_obra_inexistente() -> None:

    async def scenario() -> None:
        service = ClubeService(clube_repo=InMemoryClubeRepository(), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=False), request_service=FakeRequestService())
        with pytest.raises(ValueError, match='Obra'):
            await service.cadastrar_clube(nome='Clube Teste', sigla='CTE', tipo=TipoClube.COMUNITARIO, modalidade_principal=ModalidadeDesportiva.BASQUETEBOL, municipio='Huambo', provincia='Huambo', codigo_obra_instalacao='OBR/2026/999999')
    asyncio.run(scenario())