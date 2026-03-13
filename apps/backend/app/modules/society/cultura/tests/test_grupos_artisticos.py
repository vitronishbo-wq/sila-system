from __future__ import annotations
import asyncio
from uuid import uuid4
import pytest
from app.modules.society.cultura.application.services.artista_service import ArtistaService
from app.modules.society.cultura.application.services.grupo_artistico_service import GrupoArtisticoService
from app.modules.society.cultura.domain.enums import TipoArtista, TipoGrupoArtistico
from app.modules.society.cultura.tests._fakes import FakeEducacaoService, FakeRequestService, InMemoryArtistaRepository, InMemoryGrupoArtisticoRepository

async def _seed_artista(artista_repo: InMemoryArtistaRepository):
    artista_service = ArtistaService(artista_repo=artista_repo)
    return await artista_service.cadastrar_artista(nome='Lider Grupo', tipo=[TipoArtista.MUSICO])

def test_grupo_artistico_cadastro_sucesso() -> None:

    async def scenario() -> None:
        artista_repo = InMemoryArtistaRepository()
        grupo_repo = InMemoryGrupoArtisticoRepository()
        lider = await _seed_artista(artista_repo)
        service = GrupoArtisticoService(grupo_repo=grupo_repo, artista_repo=artista_repo, educacao_service=FakeEducacaoService(exists=True), request_service=FakeRequestService())
        grupo = await service.cadastrar_grupo(nome='Coletivo Kilamba', tipo=TipoGrupoArtistico.COLETIVO, lider_artista_id=lider.id, municipio='Luanda', provincia='Luanda', instituicao_educacional_id=uuid4())
        assert grupo.codigo_grupo.startswith('GRP/')
        assert grupo.nome == 'Coletivo Kilamba'
        assert grupo.ativo is True
    asyncio.run(scenario())

def test_grupo_artistico_rejeita_lider_inexistente() -> None:

    async def scenario() -> None:
        service = GrupoArtisticoService(grupo_repo=InMemoryGrupoArtisticoRepository(), artista_repo=InMemoryArtistaRepository())
        with pytest.raises(ValueError, match='Artista lider'):
            await service.cadastrar_grupo(nome='Grupo Sem Lider', tipo=TipoGrupoArtistico.BANDA, lider_artista_id=uuid4())
    asyncio.run(scenario())

def test_grupo_artistico_filtro_tipo() -> None:

    async def scenario() -> None:
        artista_repo = InMemoryArtistaRepository()
        grupo_repo = InMemoryGrupoArtisticoRepository()
        lider = await _seed_artista(artista_repo)
        service = GrupoArtisticoService(grupo_repo=grupo_repo, artista_repo=artista_repo)
        await service.cadastrar_grupo(nome='Orquestra Nacional', tipo=TipoGrupoArtistico.ORQUESTRA, lider_artista_id=lider.id)
        await service.cadastrar_grupo(nome='Companhia Teatral', tipo=TipoGrupoArtistico.COMPANHIA, lider_artista_id=lider.id)
        orquestras = await service.listar_grupos(tipo=TipoGrupoArtistico.ORQUESTRA)
        assert len(orquestras) == 1
        assert orquestras[0].nome == 'Orquestra Nacional'
    asyncio.run(scenario())