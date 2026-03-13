from __future__ import annotations
import asyncio
from app.modules.society.cultura.application.services.bem_cultural_service import BemCulturalService
from app.modules.society.cultura.domain.enums import StatusTombamento, TipoPatrimonio
from app.modules.society.cultura.tests._fakes import FakeRequestService, InMemoryBemCulturalRepository

def test_bem_cultural_fluxo_cadastro_tombamento() -> None:

    async def scenario() -> None:
        service = BemCulturalService(bem_repo=InMemoryBemCulturalRepository(), request_service=FakeRequestService())
        bem = await service.cadastrar_bem(nome='Fortaleza de Sao Miguel', tipo=TipoPatrimonio.HISTORICO, descricao='Fortificacao historica de Luanda.', localizacao='Ingombota', municipio='Luanda', provincia='Luanda')
        assert bem.registro_ipat.startswith('IPAT/')
        assert bem.status_tombamento == StatusTombamento.PROPOSTO
        tombado = await service.tombar_bem(bem.id)
        assert tombado.status_tombamento == StatusTombamento.TOMBADO
        assert tombado.tombamento_id is not None
    asyncio.run(scenario())

def test_bem_cultural_filtro_por_municipio() -> None:

    async def scenario() -> None:
        service = BemCulturalService(bem_repo=InMemoryBemCulturalRepository())
        await service.cadastrar_bem(nome='Bem Luanda', tipo=TipoPatrimonio.ARTISTICO, descricao='Descricao A', localizacao='Local A', municipio='Luanda', provincia='Luanda')
        await service.cadastrar_bem(nome='Bem Benguela', tipo=TipoPatrimonio.MATERIAL, descricao='Descricao B', localizacao='Local B', municipio='Benguela', provincia='Benguela')
        luanda = await service.listar_bens(municipio='luanda')
        assert len(luanda) == 1
        assert luanda[0].nome == 'Bem Luanda'
    asyncio.run(scenario())