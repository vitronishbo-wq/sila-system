from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.bridges import ServiceRequestLifecycleBridge
from apps.backend.app.modules.public_security.application.services.cadeia_custodia_service import (
    CadeiaCustodiaService,
)
from apps.backend.app.modules.public_security.application.services.evidencia_service import (
    EvidenciaService,
)
from apps.backend.app.modules.public_security.application.services.investigacao_service import (
    InvestigacaoService,
)
from apps.backend.app.modules.public_security.application.services.laudo_pericial_service import (
    LaudoPericialService,
)
from apps.backend.app.modules.public_security.application.services.mandado_service import (
    MandadoService,
)
from apps.backend.app.modules.public_security.application.services.ocorrencia_service import (
    OcorrenciaService,
)
from apps.backend.app.modules.public_security.application.services.policial_service import (
    PolicialService,
)
from apps.backend.app.modules.public_security.application.services.prova_pericial_service import (
    ProvaPericialService,
)
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import (
    UnidadePolicialService,
)
from apps.backend.app.modules.public_security.application.services.vestigio_service import (
    VestigioService,
)
from apps.backend.app.modules.public_security.infrastructure.adapters.request_service_adapter import (
    RequestServiceAdapter,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_cadeia_custodia_repository import (
    SQLAlchemyCadeiaCustodiaRepository,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_evidencia_repository import (
    SQLAlchemyEvidenciaRepository,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_investigacao_repository import (
    SQLAlchemyInvestigacaoRepository,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_laudo_pericial_repository import (
    SQLAlchemyLaudoPericialRepository,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_mandado_repository import (
    SQLAlchemyMandadoRepository,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_ocorrencia_repository import (
    SQLAlchemyOcorrenciaRepository,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_policial_repository import (
    SQLAlchemyPolicialRepository,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_prova_pericial_repository import (
    SQLAlchemyProvaPericialRepository,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_unidade_policial_repository import (
    SQLAlchemyUnidadePolicialRepository,
)
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_vestigio_repository import (
    SQLAlchemyVestigioRepository,
)

db_dep = db_dep

async def get_unidade_policial_service(
    session: AsyncSession = db_dep,
) -> UnidadePolicialService:
    return UnidadePolicialService(
        unidade_repo=SQLAlchemyUnidadePolicialRepository(session),
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )


async def get_policial_service(session: AsyncSession = db_dep) -> PolicialService:
    unidade_repo = SQLAlchemyUnidadePolicialRepository(session)
    return PolicialService(
        policial_repo=SQLAlchemyPolicialRepository(session),
        unidade_repo=unidade_repo,
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )


async def get_ocorrencia_service(session: AsyncSession = db_dep) -> OcorrenciaService:
    unidade_repo = SQLAlchemyUnidadePolicialRepository(session)
    policial_repo = SQLAlchemyPolicialRepository(session)
    return OcorrenciaService(
        ocorrencia_repo=SQLAlchemyOcorrenciaRepository(session),
        unidade_repo=unidade_repo,
        policial_repo=policial_repo,
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )


async def get_mandado_service(session: AsyncSession = db_dep) -> MandadoService:
    return MandadoService(
        mandado_repo=SQLAlchemyMandadoRepository(session),
        ocorrencia_repo=SQLAlchemyOcorrenciaRepository(session),
        policial_repo=SQLAlchemyPolicialRepository(session),
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )


async def get_investigacao_service(session: AsyncSession = db_dep) -> InvestigacaoService:
    return InvestigacaoService(
        investigacao_repo=SQLAlchemyInvestigacaoRepository(session),
        ocorrencia_repo=SQLAlchemyOcorrenciaRepository(session),
        policial_repo=SQLAlchemyPolicialRepository(session),
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )


async def get_prova_pericial_service(
    session: AsyncSession = db_dep,
) -> ProvaPericialService:
    return ProvaPericialService(
        prova_repo=SQLAlchemyProvaPericialRepository(session),
        ocorrencia_repo=SQLAlchemyOcorrenciaRepository(session),
        policial_repo=SQLAlchemyPolicialRepository(session),
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )


async def get_cadeia_custodia_service(
    session: AsyncSession = db_dep,
) -> CadeiaCustodiaService:
    return CadeiaCustodiaService(
        cadeia_repo=SQLAlchemyCadeiaCustodiaRepository(session),
        prova_repo=SQLAlchemyProvaPericialRepository(session),
        policial_repo=SQLAlchemyPolicialRepository(session),
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )


async def get_laudo_pericial_service(
    session: AsyncSession = db_dep,
) -> LaudoPericialService:
    return LaudoPericialService(
        laudo_repo=SQLAlchemyLaudoPericialRepository(session),
        prova_repo=SQLAlchemyProvaPericialRepository(session),
        policial_repo=SQLAlchemyPolicialRepository(session),
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )


async def get_vestigio_service(session: AsyncSession = db_dep) -> VestigioService:
    return VestigioService(
        vestigio_repo=SQLAlchemyVestigioRepository(session),
        cadeia_repo=SQLAlchemyCadeiaCustodiaRepository(session),
        policial_repo=SQLAlchemyPolicialRepository(session),
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )


async def get_evidencia_service(session: AsyncSession = db_dep) -> EvidenciaService:
    return EvidenciaService(
        evidencia_repo=SQLAlchemyEvidenciaRepository(session),
        vestigio_repo=SQLAlchemyVestigioRepository(session),
        cadeia_repo=SQLAlchemyCadeiaCustodiaRepository(session),
        policial_repo=SQLAlchemyPolicialRepository(session),
        request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)),
    )