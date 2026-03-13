from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.bridges import ServiceRequestLifecycleBridge
from app.modules.infrastructure_sector.meteorologia.application.services import AlertaMeteorologicoService, EstacaoService, ProcessamentoService
from app.modules.infrastructure_sector.meteorologia.infrastructure.adapters import RequestServiceAdapter
from app.modules.infrastructure_sector.meteorologia.infrastructure.repositories import SQLAlchemyEstacaoRepository, SQLAlchemyObservacaoRepository

async def get_db_session(session: AsyncSession=Depends(get_db)) -> AsyncSession:
    return session

async def get_estacao_service(session: AsyncSession=Depends(get_db)) -> EstacaoService:
    return EstacaoService(estacao_repository=SQLAlchemyEstacaoRepository(session))

async def get_processamento_service(session: AsyncSession=Depends(get_db)) -> ProcessamentoService:
    request_adapter = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    alerta_service = AlertaMeteorologicoService(request_service=request_adapter)
    return ProcessamentoService(observacao_repository=SQLAlchemyObservacaoRepository(session), estacao_repository=SQLAlchemyEstacaoRepository(session), alerta_service=alerta_service)