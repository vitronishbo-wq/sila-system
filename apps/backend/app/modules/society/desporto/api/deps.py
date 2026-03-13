from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from importlib import import_module
from app.api.deps import get_db
from app.domain.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from app.domain.bridges.society_repository_bridges import make_educacao_escola_repository
from apps.backend.app.modules.society.desporto.application.events import event_bus
from apps.backend.app.modules.society.desporto.application.services.atleta_service import AtletaService
from apps.backend.app.modules.society.desporto.application.services.clube_service import ClubeService
from apps.backend.app.modules.society.desporto.application.services.competicao_service import CompeticaoService
from apps.backend.app.modules.society.desporto.application.services.estadio_service import EstadioService
from apps.backend.app.modules.society.desporto.application.services.jogo_service import JogoService
from apps.backend.app.modules.society.desporto.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from apps.backend.app.modules.society.desporto.infrastructure.adapters.educacao_service_adapter import EducacaoServiceAdapter
from apps.backend.app.modules.society.desporto.infrastructure.adapters.obras_publicas_service_adapter import ObrasPublicasServiceAdapter
from apps.backend.app.modules.society.desporto.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from apps.backend.app.modules.society.desporto.infrastructure.adapters.saude_service_adapter import SaudeServiceAdapter
from apps.backend.app.modules.society.desporto.infrastructure.adapters.turismo_service_adapter import TurismoServiceAdapter
from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_atleta_repository import SQLAlchemyAtletaRepository
from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_clube_repository import SQLAlchemyClubeRepository
from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_competicao_repository import SQLAlchemyCompeticaoRepository
from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_estadio_repository import SQLAlchemyEstadioRepository
from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_jogo_repository import SQLAlchemyJogoRepository
from apps.backend.app.modules.society.desporto.infrastructure.persistence.outbox import InMemoryOutboxRepository
from apps.backend.app.modules.saude.api.deps import get_exame_service
_outbox_repo = InMemoryOutboxRepository()

async def get_atleta_service(session: AsyncSession=Depends(get_db)) -> AtletaService:
    return AtletaService(atleta_repo=SQLAlchemyAtletaRepository(session), citizen_service=CitizenServiceAdapter(CitizenRepository(session)), saude_service=SaudeServiceAdapter(await get_exame_service(session)), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_competicao_service(session: AsyncSession=Depends(get_db)) -> CompeticaoService:
    turismo_module = import_module('app.modules.economy.turismo.api.deps')
    get_atracao_service = getattr(turismo_module, 'get_atracao_service')
    obras_module = import_module('app.modules.infrastructure.domain.api.deps')
    get_obra_service = getattr(obras_module, 'get_obra_service')
    return CompeticaoService(competicao_repo=SQLAlchemyCompeticaoRepository(session), turismo_service=TurismoServiceAdapter(await get_atracao_service()), educacao_service=EducacaoServiceAdapter(make_educacao_escola_repository(session)), obras_publicas_service=ObrasPublicasServiceAdapter(get_obra_service()), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_clube_service(session: AsyncSession=Depends(get_db)) -> ClubeService:
    obras_module = import_module('app.modules.infrastructure.domain.api.deps')
    get_obra_service = getattr(obras_module, 'get_obra_service')
    return ClubeService(clube_repo=SQLAlchemyClubeRepository(session), educacao_service=EducacaoServiceAdapter(make_educacao_escola_repository(session)), obras_publicas_service=ObrasPublicasServiceAdapter(get_obra_service()), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_jogo_service(session: AsyncSession=Depends(get_db)) -> JogoService:
    turismo_module = import_module('app.modules.economy.turismo.api.deps')
    get_atracao_service = getattr(turismo_module, 'get_atracao_service')
    obras_module = import_module('app.modules.infrastructure.domain.api.deps')
    get_obra_service = getattr(obras_module, 'get_obra_service')
    return JogoService(jogo_repo=SQLAlchemyJogoRepository(session), competicao_repo=SQLAlchemyCompeticaoRepository(session), clube_repo=SQLAlchemyClubeRepository(session), turismo_service=TurismoServiceAdapter(await get_atracao_service()), obras_publicas_service=ObrasPublicasServiceAdapter(get_obra_service()), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)), event_bus=event_bus, outbox_repo=_outbox_repo)

async def get_estadio_service(session: AsyncSession=Depends(get_db)) -> EstadioService:
    obras_module = import_module('app.modules.infrastructure.domain.api.deps')
    get_obra_service = getattr(obras_module, 'get_obra_service')
    return EstadioService(estadio_repo=SQLAlchemyEstadioRepository(session), obras_publicas_service=ObrasPublicasServiceAdapter(get_obra_service()), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)), event_bus=event_bus, outbox_repo=_outbox_repo)
