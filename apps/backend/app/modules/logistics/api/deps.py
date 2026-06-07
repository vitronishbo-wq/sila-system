from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.logistics.application.services import (
    BilhetagemService,
    FrotaService,
    LinhaService,
    OperacaoAnalyticsService,
    ViagemService,
)
from apps.backend.app.modules.logistics.infrastructure.adapters import (
    FinancasServiceAdapter,
    GeosampaServiceAdapter,
    ObrasPublicasServiceAdapter,
    SegurancaPublicaServiceAdapter,
    ServiceRequestsServiceAdapter,
    UrbanismoServiceAdapter,
    WorkflowServiceAdapter,
)
from apps.backend.app.modules.logistics.infrastructure.repositories import (
    SQLAlchemyBilhetagemRepository,
    SQLAlchemyFrotaRepository,
    SQLAlchemyLinhaRepository,
    SQLAlchemyVeiculoRepository,
    SQLAlchemyViagemRepository,
)

db_dep = db_dep


async def get_viagem_service(session: AsyncSession = db_dep) -> ViagemService:
    return ViagemService(viagem_repo=SQLAlchemyViagemRepository(session))


async def get_frota_service(session: AsyncSession = db_dep) -> FrotaService:
    return FrotaService(
        frota_repo=SQLAlchemyFrotaRepository(session),
        workflow_adapter=WorkflowServiceAdapter(),
        service_requests_adapter=ServiceRequestsServiceAdapter(),
        financas_adapter=FinancasServiceAdapter(),
        seguranca_publica_adapter=SegurancaPublicaServiceAdapter(),
    )


async def get_linha_service(session: AsyncSession = db_dep) -> LinhaService:
    return LinhaService(
        linha_repo=SQLAlchemyLinhaRepository(session),
        veiculo_repo=SQLAlchemyVeiculoRepository(session),
        geosampa_adapter=GeosampaServiceAdapter(),
        urbanismo_adapter=UrbanismoServiceAdapter(),
        obras_publicas_adapter=ObrasPublicasServiceAdapter(),
        workflow_adapter=WorkflowServiceAdapter(),
    )


async def get_bilhetagem_service(session: AsyncSession = db_dep) -> BilhetagemService:
    return BilhetagemService(
        bilhetagem_repo=SQLAlchemyBilhetagemRepository(session),
        financas_adapter=FinancasServiceAdapter(),
        workflow_adapter=WorkflowServiceAdapter(),
    )


async def get_operacao_analytics_service(
    session: AsyncSession = db_dep,
) -> OperacaoAnalyticsService:
    return OperacaoAnalyticsService(
        viagem_repo=SQLAlchemyViagemRepository(session),
        bilhetagem_repo=SQLAlchemyBilhetagemRepository(session),
    )