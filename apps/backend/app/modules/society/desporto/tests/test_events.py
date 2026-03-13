from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
from apps.backend.app.modules.society.desporto.application.events import JogoAgendadoEvent, JogoResultadoRegistradoEvent
from apps.backend.app.modules.society.desporto.application.services.clube_service import ClubeService
from apps.backend.app.modules.society.desporto.application.services.competicao_service import CompeticaoService
from apps.backend.app.modules.society.desporto.application.services.jogo_service import JogoService
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, TipoClube, TipoCompeticao
from apps.backend.app.modules.society.desporto.tests._fakes import FakeEducacaoService, FakeEventBus, FakeObrasPublicasService, FakeRequestService, FakeTurismoService, InMemoryClubeRepository, InMemoryCompeticaoRepository, InMemoryJogoRepository, InMemoryOutboxRepository

def test_jogo_service_publica_eventos_em_bus_e_outbox() -> None:

    async def scenario() -> None:
        clube_repo = InMemoryClubeRepository()
        competicao_repo = InMemoryCompeticaoRepository()
        jogo_repo = InMemoryJogoRepository()
        event_bus = FakeEventBus()
        outbox = InMemoryOutboxRepository()
        clube_service = ClubeService(clube_repo=clube_repo, educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        competicao_service = CompeticaoService(competicao_repo=competicao_repo, turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService())
        jogo_service = JogoService(jogo_repo=jogo_repo, competicao_repo=competicao_repo, clube_repo=clube_repo, turismo_service=FakeTurismoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True), request_service=FakeRequestService(), event_bus=event_bus, outbox_repo=outbox)
        clube_a = await clube_service.cadastrar_clube(nome='Clube Eventos A', sigla='CEA', tipo=TipoClube.PROFISSIONAL, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Luanda', provincia='Luanda')
        clube_b = await clube_service.cadastrar_clube(nome='Clube Eventos B', sigla='CEB', tipo=TipoClube.PROFISSIONAL, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Luanda', provincia='Luanda')
        competicao = await competicao_service.cadastrar_competicao(nome='Liga Eventos', tipo=TipoCompeticao.LIGA, modalidade=ModalidadeDesportiva.FUTEBOL, data_inicio=date(2026, 1, 1), data_fim=date(2026, 12, 31), municipio='Luanda', provincia='Luanda', organizador_id=uuid4())
        jogo = await jogo_service.agendar_jogo(competicao_id=competicao.id, clube_casa_id=clube_a.id, clube_fora_id=clube_b.id, data_jogo=date(2026, 3, 20), local='Arena Central', municipio='Luanda', provincia='Luanda')
        await jogo_service.registrar_resultado(jogo_id=jogo.id, placar_casa=1, placar_fora=0)
        assert len(event_bus.events) == 2
        assert isinstance(event_bus.events[0], JogoAgendadoEvent)
        assert isinstance(event_bus.events[1], JogoResultadoRegistradoEvent)
        assert len(outbox.events) == 2
    asyncio.run(scenario())