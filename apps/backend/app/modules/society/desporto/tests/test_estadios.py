from __future__ import annotations
import asyncio
import pytest
from apps.backend.app.modules.society.desporto.application.services.estadio_service import EstadioService
from apps.backend.app.modules.society.desporto.domain.enums import EstadoRelvado, TipoEstadio
from apps.backend.app.modules.society.desporto.tests._fakes import FakeEventBus, FakeObrasPublicasService, FakeRequestService, InMemoryEstadioRepository, InMemoryOutboxRepository

def test_cadastrar_estadio_publica_evento() -> None:

    async def scenario() -> None:
        event_bus = FakeEventBus()
        outbox = InMemoryOutboxRepository()
        service = EstadioService(estadio_repo=InMemoryEstadioRepository(), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService(), event_bus=event_bus, outbox_repo=outbox)
        estadio = await service.cadastrar_estadio(nome='Estadio Nacional', tipo=TipoEstadio.ESTADIO, municipio='Luanda', provincia='Luanda', capacidade=50000, estado_relvado=EstadoRelvado.NATURAL, codigo_obra_instalacao='OBR/2026/001111')
        assert estadio.codigo_estadio.startswith('EST/')
        assert len(event_bus.events) == 1
        assert len(outbox.events) == 1
    asyncio.run(scenario())

def test_cadastrar_estadio_falha_quando_obra_invalida() -> None:

    async def scenario() -> None:
        service = EstadioService(estadio_repo=InMemoryEstadioRepository(), obras_publicas_service=FakeObrasPublicasService(exists=False), request_service=FakeRequestService())
        with pytest.raises(ValueError, match='Obra de instalacao'):
            await service.cadastrar_estadio(nome='Arena Provincial', tipo=TipoEstadio.ARENA, municipio='Benguela', provincia='Benguela', capacidade=18000, estado_relvado=EstadoRelvado.SINTETICO, codigo_obra_instalacao='OBR/2026/404404')
    asyncio.run(scenario())