from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from app.modules.turismo.application.services.atracao_service import AtracaoService
from app.modules.turismo.application.services.meio_hospedagem_service import MeioHospedagemService
from app.modules.turismo.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from app.modules.turismo.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from app.modules.turismo.infrastructure.repositories.sqlalchemy_atracao_turistica_repository import (
    SQLAlchemyAtracaoTuristicaRepository,
)
from app.modules.turismo.infrastructure.repositories.sqlalchemy_hotel_repository import (
    SQLAlchemyHotelRepository,
)
from app.modules.turismo.infrastructure.repositories.sqlalchemy_pousada_repository import (
    SQLAlchemyPousadaRepository,
)

_hotel_repo_singleton = SQLAlchemyHotelRepository()
_pousada_repo_singleton = SQLAlchemyPousadaRepository()
_atracao_repo_singleton = SQLAlchemyAtracaoTuristicaRepository()


async def get_hotel_service(session: AsyncSession = Depends(get_db)) -> MeioHospedagemService:
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return MeioHospedagemService(
        hotel_repo=_hotel_repo_singleton,
        pousada_repo=_pousada_repo_singleton,
        citizen_service=citizen_service,
        request_service=request_service,
    )


async def get_pousada_service(session: AsyncSession = Depends(get_db)) -> MeioHospedagemService:
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return MeioHospedagemService(
        hotel_repo=_hotel_repo_singleton,
        pousada_repo=_pousada_repo_singleton,
        citizen_service=citizen_service,
        request_service=request_service,
    )


async def get_atracao_service() -> AtracaoService:
    return AtracaoService(repository=_atracao_repo_singleton)
