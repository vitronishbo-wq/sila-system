from __future__ import annotations

from apps.backend.app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.bridges import ServiceRequestLifecycleBridge
from apps.backend.app.modules.infrastructure_sector.meteorologia.application.services import (
    AlertaMeteorologicoService,
    EstacaoService,
    ProcessamentoService,
)
from apps.backend.app.modules.infrastructure_sector.meteorologia.infrastructure.adapters import (
    RequestServiceAdapter,
)
from apps.backend.app.modules.infrastructure_sector.meteorologia.infrastructure.repositories import (
    SQLAlchemyEstacaoRepository,
    SQLAlchemyObservacaoRepository,
)

db_dep = Depends(get_db)


async def get_db_session(session: AsyncSession = db_dep) -> AsyncSession:
    return session


async def get_estacao_service(session: AsyncSession = db_dep) -> EstacaoService:
    return EstacaoService(estacao_repository=SQLAlchemyEstacaoRepository(session))


async def get_processamento_service(
    session: AsyncSession = db_dep,
) -> ProcessamentoService:
    request_adapter = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    alerta_service = AlertaMeteorologicoService(request_service=request_adapter)
    return ProcessamentoService(
        observacao_repository=SQLAlchemyObservacaoRepository(session),
        estacao_repository=SQLAlchemyEstacaoRepository(session),
        alerta_service=alerta_service,
    )