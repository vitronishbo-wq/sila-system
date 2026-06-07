from __future__ import annotations

from apps.backend.app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.alvara_service import (
    AlvaraService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.habite_se_service import (
    HabiteSeService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.licenciamento_urbano_service import (
    LicenciamentoUrbanoService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.loteamento_service import (
    LoteamentoService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.operacao_urbana_service import (
    OperacaoUrbanaService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.parcelamento_service import (
    ParcelamentoService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.plano_diretor_service import (
    PlanoDiretorService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.zoneamento_service import (
    ZoneamentoService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.adapters import (
    AguasSaneamentoServiceAdapter,
    AmbienteServiceAdapter,
    FinancasServiceAdapter,
    GestaoFundiariaServiceAdapter,
    ObrasPublicasServiceAdapter,
    RequestServiceAdapter,
    TransportesServiceAdapter,
    WorkflowServiceAdapter,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.repositories import (
    SQLAlchemyAlvaraRepository,
    SQLAlchemyHabiteSeRepository,
    SQLAlchemyLicencaUrbanisticaRepository,
    SQLAlchemyLoteamentoRepository,
    SQLAlchemyOperacaoUrbanaRepository,
    SQLAlchemyParcelamentoRepository,
    SQLAlchemyPlanoDiretorRepository,
    SQLAlchemyZoneamentoRepository,
)

db_dep = Depends(get_db)


async def get_plano_diretor_service(session: AsyncSession = db_dep) -> PlanoDiretorService:
    return PlanoDiretorService(plano_diretor_repo=SQLAlchemyPlanoDiretorRepository(session))


async def get_zoneamento_service(session: AsyncSession = db_dep) -> ZoneamentoService:
    return ZoneamentoService(zoneamento_repo=SQLAlchemyZoneamentoRepository(session))


async def get_operacao_urbana_service(
    session: AsyncSession = db_dep,
) -> OperacaoUrbanaService:
    return OperacaoUrbanaService(operacao_urbana_repo=SQLAlchemyOperacaoUrbanaRepository(session))


async def get_parcelamento_service(session: AsyncSession = db_dep) -> ParcelamentoService:
    return ParcelamentoService(parcelamento_repo=SQLAlchemyParcelamentoRepository(session))


async def get_loteamento_service(session: AsyncSession = db_dep) -> LoteamentoService:
    return LoteamentoService(
        loteamento_repo=SQLAlchemyLoteamentoRepository(session),
        gestao_fundiaria_adapter=GestaoFundiariaServiceAdapter(),
        ambiente_adapter=AmbienteServiceAdapter(),
        obras_publicas_adapter=ObrasPublicasServiceAdapter(),
        aguas_saneamento_adapter=AguasSaneamentoServiceAdapter(),
        transportes_adapter=TransportesServiceAdapter(),
        workflow_adapter=WorkflowServiceAdapter(),
        financas_adapter=FinancasServiceAdapter(),
    )


async def get_licenciamento_urbano_service(
    session: AsyncSession = db_dep,
) -> LicenciamentoUrbanoService:
    return LicenciamentoUrbanoService(
        licenca_repo=SQLAlchemyLicencaUrbanisticaRepository(session),
        ambiente_adapter=AmbienteServiceAdapter(),
        request_service=RequestServiceAdapter(),
        workflow_adapter=WorkflowServiceAdapter(),
        financas_adapter=FinancasServiceAdapter(),
    )


async def get_alvara_service(session: AsyncSession = db_dep) -> AlvaraService:
    return AlvaraService(alvara_repo=SQLAlchemyAlvaraRepository(session))


async def get_habite_se_service(session: AsyncSession = db_dep) -> HabiteSeService:
    return HabiteSeService(habite_se_repo=SQLAlchemyHabiteSeRepository(session))