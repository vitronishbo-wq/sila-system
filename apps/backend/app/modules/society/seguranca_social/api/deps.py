from __future__ import annotations
from fastapi import Depends
from app.api.deps import get_db
from app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from app.core.bridges.emprego_bridge import SQLAlchemyCandidatoRepository
from apps.backend.app.modules.society.seguranca_social.application.services import BeneficiarioService, PensaoService
from apps.backend.app.modules.society.seguranca_social.infrastructure.adapters import CitizenServiceAdapter, EmpregoServiceAdapter, RequestServiceAdapter
from apps.backend.app.modules.society.seguranca_social.infrastructure.repositories import SQLAlchemyBeneficiarioRepository, SQLAlchemyPensaoRepository

def _bridges(session):
    citizen = CitizenServiceAdapter(CitizenRepository(session))
    request = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    emprego = EmpregoServiceAdapter(SQLAlchemyCandidatoRepository(session))
    return (citizen, request, emprego)

async def get_beneficiario_service(session=Depends(get_db)) -> BeneficiarioService:
    citizen, request, emprego = _bridges(session)
    return BeneficiarioService(beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), citizen_repo=citizen, emprego_service=emprego, request_service=request)

async def get_pensao_service(session=Depends(get_db)) -> PensaoService:
    _, request, _ = _bridges(session)
    return PensaoService(pensao_repo=SQLAlchemyPensaoRepository(session), beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), request_service=request)