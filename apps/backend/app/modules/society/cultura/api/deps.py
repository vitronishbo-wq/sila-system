from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from importlib import import_module
from app.api.deps import get_db
from app.domain.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from app.domain.bridges.society_repository_bridges import make_educacao_escola_repository
from apps.backend.app.modules.society.cultura.application.services.artista_service import ArtistaService
from apps.backend.app.modules.society.cultura.application.services.bem_cultural_service import BemCulturalService
from apps.backend.app.modules.society.cultura.application.services.edital_service import EditalService
from apps.backend.app.modules.society.cultura.application.services.espaco_cultural_service import EspacoCulturalService
from apps.backend.app.modules.society.cultura.application.services.evento_cultural_service import EventoCulturalService
from apps.backend.app.modules.society.cultura.application.services.grupo_artistico_service import GrupoArtisticoService
from apps.backend.app.modules.society.cultura.application.services.patrimonio_imaterial_service import PatrimonioImaterialService
from apps.backend.app.modules.society.cultura.application.services.projeto_cultural_service import ProjetoCulturalService
from apps.backend.app.modules.society.cultura.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from apps.backend.app.modules.society.cultura.infrastructure.adapters.educacao_service_adapter import EducacaoServiceAdapter
from apps.backend.app.modules.society.cultura.infrastructure.adapters.minc_adapter import MincAdapter
from apps.backend.app.modules.society.cultura.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from apps.backend.app.modules.society.cultura.infrastructure.adapters.turismo_service_adapter import TurismoServiceAdapter
from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_artista_repository import SQLAlchemyArtistaRepository
from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_bem_cultural_repository import SQLAlchemyBemCulturalRepository
from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_edital_repository import SQLAlchemyEditalRepository
from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_espaco_cultural_repository import SQLAlchemyEspacoCulturalRepository
from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_evento_cultural_repository import SQLAlchemyEventoCulturalRepository
from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_grupo_artistico_repository import SQLAlchemyGrupoArtisticoRepository
from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_patrimonio_imaterial_repository import SQLAlchemyPatrimonioImaterialRepository
from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_projeto_cultural_repository import SQLAlchemyProjetoCulturalRepository

async def get_artista_service(session: AsyncSession=Depends(get_db)) -> ArtistaService:
    return ArtistaService(artista_repo=SQLAlchemyArtistaRepository(session), citizen_service=CitizenServiceAdapter(CitizenRepository(session)), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_bem_cultural_service(session: AsyncSession=Depends(get_db)) -> BemCulturalService:
    return BemCulturalService(bem_repo=SQLAlchemyBemCulturalRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_espaco_cultural_service(session: AsyncSession=Depends(get_db)) -> EspacoCulturalService:
    return EspacoCulturalService(espaco_repo=SQLAlchemyEspacoCulturalRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_projeto_cultural_service(session: AsyncSession=Depends(get_db)) -> ProjetoCulturalService:
    return ProjetoCulturalService(projeto_repo=SQLAlchemyProjetoCulturalRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_edital_service(session: AsyncSession=Depends(get_db)) -> EditalService:
    turismo_module = import_module('app.modules.economy.turismo.api.deps')
    get_atracao_service = getattr(turismo_module, 'get_atracao_service')
    return EditalService(edital_repo=SQLAlchemyEditalRepository(session), projeto_repo=SQLAlchemyProjetoCulturalRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)), minc_adapter=MincAdapter(), turismo_adapter=TurismoServiceAdapter(await get_atracao_service()))

async def get_evento_cultural_service(session: AsyncSession=Depends(get_db)) -> EventoCulturalService:
    turismo_module = import_module('app.modules.economy.turismo.api.deps')
    get_atracao_service = getattr(turismo_module, 'get_atracao_service')
    return EventoCulturalService(evento_repo=SQLAlchemyEventoCulturalRepository(session), artista_repo=SQLAlchemyArtistaRepository(session), turismo_service=TurismoServiceAdapter(await get_atracao_service()), educacao_service=EducacaoServiceAdapter(make_educacao_escola_repository(session)), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_grupo_artistico_service(session: AsyncSession=Depends(get_db)) -> GrupoArtisticoService:
    return GrupoArtisticoService(grupo_repo=SQLAlchemyGrupoArtisticoRepository(session), artista_repo=SQLAlchemyArtistaRepository(session), educacao_service=EducacaoServiceAdapter(make_educacao_escola_repository(session)), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_patrimonio_imaterial_service(session: AsyncSession=Depends(get_db)) -> PatrimonioImaterialService:
    return PatrimonioImaterialService(patrimonio_repo=SQLAlchemyPatrimonioImaterialRepository(session), turismo_service=TurismoServiceAdapter(await get_atracao_service()), educacao_service=EducacaoServiceAdapter(make_educacao_escola_repository(session)), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))