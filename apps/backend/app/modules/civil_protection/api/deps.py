from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.bridges import ServiceRequestLifecycleBridge
from app.modules.civil_protection.application.services.atendimento_service import AtendimentoService
from app.modules.civil_protection.application.services.bombeiro_service import BombeiroService
from app.modules.civil_protection.application.services.corporacao_service import CorporacaoService
from app.modules.civil_protection.application.services.despacho_service import DespachoService
from app.modules.civil_protection.application.services.ocorrencia_emergencial_service import OcorrenciaEmergencialService
from app.modules.civil_protection.infrastructure.repositories.sqlalchemy_atendimento_repository import SQLAlchemyAtendimentoRepository
from app.modules.civil_protection.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from app.modules.civil_protection.infrastructure.repositories.sqlalchemy_bombeiro_repository import SQLAlchemyBombeiroRepository
from app.modules.civil_protection.infrastructure.repositories.sqlalchemy_corporacao_repository import SQLAlchemyCorporacaoRepository
from app.modules.civil_protection.infrastructure.repositories.sqlalchemy_despacho_repository import SQLAlchemyDespachoRepository
from app.modules.civil_protection.infrastructure.repositories.sqlalchemy_ocorrencia_emergencial_repository import SQLAlchemyOcorrenciaEmergencialRepository

async def get_corporacao_service(session: AsyncSession=Depends(get_db)) -> CorporacaoService:
    return CorporacaoService(corporacao_repo=SQLAlchemyCorporacaoRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_bombeiro_service(session: AsyncSession=Depends(get_db)) -> BombeiroService:
    corporacao_repo = SQLAlchemyCorporacaoRepository(session)
    return BombeiroService(bombeiro_repo=SQLAlchemyBombeiroRepository(session), corporacao_repo=corporacao_repo, request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_ocorrencia_emergencial_service(session: AsyncSession=Depends(get_db)) -> OcorrenciaEmergencialService:
    corporacao_repo = SQLAlchemyCorporacaoRepository(session)
    bombeiro_repo = SQLAlchemyBombeiroRepository(session)
    return OcorrenciaEmergencialService(ocorrencia_repo=SQLAlchemyOcorrenciaEmergencialRepository(session), corporacao_repo=corporacao_repo, bombeiro_repo=bombeiro_repo, request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_despacho_service(session: AsyncSession=Depends(get_db)) -> DespachoService:
    return DespachoService(despacho_repo=SQLAlchemyDespachoRepository(session), ocorrencia_repo=SQLAlchemyOcorrenciaEmergencialRepository(session), bombeiro_repo=SQLAlchemyBombeiroRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_atendimento_service(session: AsyncSession=Depends(get_db)) -> AtendimentoService:
    return AtendimentoService(atendimento_repo=SQLAlchemyAtendimentoRepository(session), despacho_repo=SQLAlchemyDespachoRepository(session), ocorrencia_repo=SQLAlchemyOcorrenciaEmergencialRepository(session), bombeiro_repo=SQLAlchemyBombeiroRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))