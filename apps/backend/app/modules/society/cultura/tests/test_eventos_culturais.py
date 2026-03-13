from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from app.modules.society.cultura.application.services.artista_service import ArtistaService
from app.modules.society.cultura.application.services.evento_cultural_service import EventoCulturalService
from app.modules.society.cultura.domain.enums import StatusEventoCultural, TipoArtista, TipoEventoCultural
from app.modules.society.cultura.tests._fakes import FakeEducacaoService, FakeRequestService, FakeTurismoService, InMemoryArtistaRepository, InMemoryEventoCulturalRepository

async def _seed_artista(repo: InMemoryArtistaRepository):
    artista_service = ArtistaService(artista_repo=repo)
    return await artista_service.cadastrar_artista(nome='Bonga', tipo=[TipoArtista.MUSICO])

def test_evento_cultural_cadastro_sucesso() -> None:

    async def scenario() -> None:
        artista_repo = InMemoryArtistaRepository()
        evento_repo = InMemoryEventoCulturalRepository()
        artista = await _seed_artista(artista_repo)
        service = EventoCulturalService(evento_repo=evento_repo, artista_repo=artista_repo, turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), request_service=FakeRequestService())
        evento = await service.cadastrar_evento(nome='Festival Kizomba', tipo=TipoEventoCultural.FESTIVAL, descricao='Festival de musica e danca', data_inicio=date(2026, 3, 10), data_fim=date(2026, 3, 12), local='Marginal de Luanda', municipio='Luanda', provincia='Luanda', realizador_id=artista.id, atracao_turistica_id=uuid4(), instituicao_educacional_id=uuid4(), entrada_gratuita=False, valor_ingresso=1000)
        assert evento.codigo_evento.startswith('EVT/')
        assert evento.entrada_gratuita is False
    asyncio.run(scenario())

def test_evento_cultural_rejeita_atracao_inexistente() -> None:

    async def scenario() -> None:
        artista_repo = InMemoryArtistaRepository()
        evento_repo = InMemoryEventoCulturalRepository()
        artista = await _seed_artista(artista_repo)
        service = EventoCulturalService(evento_repo=evento_repo, artista_repo=artista_repo, turismo_service=FakeTurismoService(exists=False))
        with pytest.raises(ValueError, match='Atracao turistica'):
            await service.cadastrar_evento(nome='Mostra Tradicional', tipo=TipoEventoCultural.MOSTRA, descricao='Mostra regional', data_inicio=date(2026, 4, 1), data_fim=date(2026, 4, 2), local='Centro Cultural', municipio='Huambo', provincia='Huambo', realizador_id=artista.id, atracao_turistica_id=uuid4())
    asyncio.run(scenario())

def test_evento_cultural_atualiza_status() -> None:

    async def scenario() -> None:
        artista_repo = InMemoryArtistaRepository()
        evento_repo = InMemoryEventoCulturalRepository()
        artista = await _seed_artista(artista_repo)
        service = EventoCulturalService(evento_repo=evento_repo, artista_repo=artista_repo)
        evento = await service.cadastrar_evento(nome='Oficina de Artes', tipo=TipoEventoCultural.OFICINA, descricao='Oficina comunitaria', data_inicio=date(2026, 5, 2), data_fim=date(2026, 5, 2), local='Casa da Cultura', municipio='Lubango', provincia='Huila', realizador_id=artista.id)
        atualizado = await service.atualizar_evento(evento_id=evento.id, status=StatusEventoCultural.PUBLICADO)
        assert atualizado.status == StatusEventoCultural.PUBLICADO
    asyncio.run(scenario())