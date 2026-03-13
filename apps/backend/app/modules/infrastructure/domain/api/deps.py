from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from apps.backend.app.modules.infrastructure.application.services.edital_service import EditalService
from apps.backend.app.modules.infrastructure.application.services.licitacao_service import LicitacaoService
from apps.backend.app.modules.infrastructure.application.services.dashboard_query_service import DashboardQueryService
from apps.backend.app.modules.infrastructure.application.services.obra_service import ObraService
from apps.backend.app.modules.infrastructure.application.services.projeto_service import ProjetoService
from apps.backend.app.modules.infrastructure.infrastructure.adapters import AguasSaneamentoServiceAdapter, AmbienteServiceAdapter, FinancasPublicasServiceAdapter, GestaoFundiariaServiceAdapter, ServiceRequestsServiceAdapter, TransportesServiceAdapter, UrbanismoHabitacaoServiceAdapter, WorkflowServiceAdapter
from apps.backend.app.modules.infrastructure.infrastructure.repositories import SQLAlchemyEditalRepository, SQLAlchemyLicitacaoRepository, SQLAlchemyObraRepository, SQLAlchemyProjetoRepository
from apps.backend.app.modules.infrastructure.infrastructure.persistence.outbox_repository import SQLAlchemyOutboxRepository
from apps.backend.app.modules.infrastructure.infrastructure.eventsourcing.event_store_repository import SQLAlchemyEventStoreRepository
from apps.backend.app.modules.infrastructure.infrastructure.read_model.session import get_read_session

async def get_obra_service(session: AsyncSession=Depends(get_db)) -> ObraService:
    return ObraService(obra_repo=SQLAlchemyObraRepository(session), gestao_fundiaria_adapter=GestaoFundiariaServiceAdapter(), financas_publicas_adapter=FinancasPublicasServiceAdapter(), ambiente_adapter=AmbienteServiceAdapter(), urbanismo_habitacao_adapter=UrbanismoHabitacaoServiceAdapter(), transportes_adapter=TransportesServiceAdapter(), aguas_saneamento_adapter=AguasSaneamentoServiceAdapter(), workflow_adapter=WorkflowServiceAdapter(), service_requests_adapter=ServiceRequestsServiceAdapter(), outbox_repo=SQLAlchemyOutboxRepository(session=session), event_store_repo=SQLAlchemyEventStoreRepository(session=session))

async def get_projeto_service(session: AsyncSession=Depends(get_db)) -> ProjetoService:
    return ProjetoService(projeto_repo=SQLAlchemyProjetoRepository(session))

async def get_licitacao_service(session: AsyncSession=Depends(get_db)) -> LicitacaoService:
    return LicitacaoService(licitacao_repo=SQLAlchemyLicitacaoRepository(session))

async def get_edital_service(session: AsyncSession=Depends(get_db)) -> EditalService:
    return EditalService(edital_repo=SQLAlchemyEditalRepository(session))

async def get_dashboard_query_service(read_session: AsyncSession=Depends(get_read_session)) -> DashboardQueryService:
    return DashboardQueryService(read_session)
