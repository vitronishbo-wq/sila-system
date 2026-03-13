from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.domain.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from apps.backend.app.modules.resources.pecuaria.application.services.animal_service import AnimalService
from apps.backend.app.modules.resources.pecuaria.application.services.pecuarista_service import PecuaristaService
from apps.backend.app.modules.resources.pecuaria.application.services.producao_service import ProducaoService
from apps.backend.app.modules.resources.pecuaria.application.services.propriedade_service import PropriedadeService
from apps.backend.app.modules.resources.pecuaria.application.services.rebanho_service import RebanhoService
from apps.backend.app.modules.resources.pecuaria.application.services.sanidade_service import SanidadeService
from apps.backend.app.modules.resources.pecuaria.infrastructure.adapters import CitizenServiceAdapter, RequestServiceAdapter
from apps.backend.app.modules.resources.pecuaria.infrastructure.repositories import SQLAlchemyAnimalRepository, SQLAlchemyPecuaristaRepository, SQLAlchemyPropriedadePecuariaRepository, SQLAlchemyRebanhoRepository
_producao_service_singleton = ProducaoService()
_sanidade_service_singleton = SanidadeService()

async def get_pecuarista_service(session: AsyncSession=Depends(get_db)) -> PecuaristaService:
    repository = SQLAlchemyPecuaristaRepository(session)
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return PecuaristaService(pecuarista_repo=repository, citizen_service=citizen_service, request_service=request_service)

async def get_propriedade_service(session: AsyncSession=Depends(get_db)) -> PropriedadeService:
    repository = SQLAlchemyPropriedadePecuariaRepository(session)
    return PropriedadeService(repository=repository)

async def get_rebanho_service(session: AsyncSession=Depends(get_db)) -> RebanhoService:
    repository = SQLAlchemyRebanhoRepository(session)
    return RebanhoService(repository=repository)

async def get_animal_service(session: AsyncSession=Depends(get_db)) -> AnimalService:
    animal_repo = SQLAlchemyAnimalRepository(session)
    propriedade_repo = SQLAlchemyPropriedadePecuariaRepository(session)
    rebanho_repo = SQLAlchemyRebanhoRepository(session)
    return AnimalService(animal_repo=animal_repo, propriedade_repo=propriedade_repo, rebanho_repo=rebanho_repo)

def get_producao_service() -> ProducaoService:
    return _producao_service_singleton

def get_sanidade_service() -> SanidadeService:
    return _sanidade_service_singleton