from __future__ import annotations
import asyncio
from uuid import uuid4
import pytest
from apps.backend.app.modules.society.cultura.application.services.artista_service import ArtistaService
from apps.backend.app.modules.society.cultura.domain.enums import TipoArtista
from apps.backend.app.modules.society.cultura.tests._fakes import FakeCitizenService, FakeRequestService, InMemoryArtistaRepository

def test_cadastrar_artista_sucesso() -> None:

    async def scenario() -> None:
        service = ArtistaService(artista_repo=InMemoryArtistaRepository(), citizen_service=FakeCitizenService(active=True), request_service=FakeRequestService())
        result = await service.cadastrar_artista(nome='Teta Lando', tipo=[TipoArtista.MUSICO], citizen_id=uuid4(), municipio='Luanda', provincia='Luanda')
        assert result.registro_cultural.startswith('ART/')
        assert result.nome == 'Teta Lando'
        assert result.ativo is True
    asyncio.run(scenario())

def test_cadastrar_artista_rejeita_cidadao_inativo() -> None:

    async def scenario() -> None:
        service = ArtistaService(artista_repo=InMemoryArtistaRepository(), citizen_service=FakeCitizenService(active=False))
        with pytest.raises(ValueError, match='Cidadao'):
            await service.cadastrar_artista(nome='Artista X', tipo=[TipoArtista.ATOR], citizen_id=uuid4())
    asyncio.run(scenario())

def test_listar_artistas_por_tipo() -> None:

    async def scenario() -> None:
        repo = InMemoryArtistaRepository()
        service = ArtistaService(artista_repo=repo)
        await service.cadastrar_artista(nome='Artista 1', tipo=[TipoArtista.MUSICO])
        await service.cadastrar_artista(nome='Artista 2', tipo=[TipoArtista.PINTOR])
        musicos = await service.listar_artistas(tipo=TipoArtista.MUSICO)
        assert len(musicos) == 1
        assert musicos[0].nome == 'Artista 1'
    asyncio.run(scenario())