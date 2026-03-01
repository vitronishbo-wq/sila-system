from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from app.modules.turismo.application.services.meio_hospedagem_service import MeioHospedagemService
from app.modules.turismo.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from app.modules.turismo.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from app.modules.turismo.infrastructure.repositories.sqlalchemy_hotel_repository import (
    SQLAlchemyHotelRepository,
)

_hotel_repo_singleton = SQLAlchemyHotelRepository()


async def get_hotel_service(session: AsyncSession = Depends(get_db)) -> MeioHospedagemService:
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return MeioHospedagemService(
        hotel_repo=_hotel_repo_singleton,
        citizen_service=citizen_service,
        request_service=request_service,
    )
