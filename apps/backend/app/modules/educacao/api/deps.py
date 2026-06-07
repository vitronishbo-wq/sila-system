from __future__ import annotations

import os

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_db as db_dep
from apps.backend.app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from apps.backend.app.modules.educacao.application.boletim_service import BoletimService
from apps.backend.app.modules.educacao.application.certificado_service import CertificadoService
from apps.backend.app.modules.educacao.application.concurso_service import ConcursoService
from apps.backend.app.modules.educacao.application.emprego_service import EmpregoService
from apps.backend.app.modules.educacao.application.formacao_service import FormacaoService
from apps.backend.app.modules.educacao.application.inscricao_service import InscricaoService
from apps.backend.app.modules.educacao.application.matricula_service import MatriculaService
from apps.backend.app.modules.educacao.application.propina_service import PropinaService
from apps.backend.app.modules.educacao.application.transfer_transaction_service import (
    TransferTransactionService,
)
from apps.backend.app.modules.educacao.application.transferencia_service import TransferenciaService
from apps.backend.app.modules.educacao.application.universidade_service import UniversidadeService
from apps.backend.app.modules.educacao.infrastructure.repositories import (
    SQLAlchemyAcademicIdentityRepository,
    SQLAlchemyBoletimRepository,
    SQLAlchemyCapacityRepository,
    SQLAlchemyCertificadoRepository,
    SQLAlchemyConcursoRepository,
    SQLAlchemyEmpregoRepository,
    SQLAlchemyEnrollmentRepository,
    SQLAlchemyEscolaRepository,
    SQLAlchemyFormacaoRepository,
    SQLAlchemyInscricaoRepository,
    SQLAlchemyMatriculaRepository,
    SQLAlchemyPropinaRepository,
    SQLAlchemyTransferenciaRepository,
    SQLAlchemyTurmaRepository,
    SQLAlchemyUniversidadeRepository,
)
from apps.backend.app.core.bridges.society_repository_bridges import (
    make_emprego_candidato_repository,
    make_juventude_bolsa_estudo_repository,
)
from foundation.resilience.idempotency import (
    RedisIdempotencyStore,
    create_redis_idempotency_store,
    idempotent,
)

_idempotency_store: RedisIdempotencyStore | None = None


def _get_idempotency_store() -> RedisIdempotencyStore:
    global _idempotency_store
    if _idempotency_store is None:
        redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
        _idempotency_store = create_redis_idempotency_store(redis_url)
    return _idempotency_store


async def get_matricula_service(session: AsyncSession = Depends(db_dep)) -> MatriculaService:
    matricula_repo = SQLAlchemyMatriculaRepository(session)
    turma_repo = SQLAlchemyTurmaRepository(session)
    escola_repo = SQLAlchemyEscolaRepository(session)
    citizen_repo = CitizenRepository(session)
    request_service = ServiceRequestLifecycleBridge(session)
    service = MatriculaService(
        matricula_repo=matricula_repo,
        turma_repo=turma_repo,
        escola_repo=escola_repo,
        citizen_repo=citizen_repo,
        request_service=request_service,
    )
    service.criar_matricula = idempotent(
        operation_name="matricula.create",
        store=_get_idempotency_store(),
    )(service.criar_matricula)
    return service


async def get_inscricao_service(session: AsyncSession = Depends(db_dep)) -> InscricaoService:
    inscricao_repo = SQLAlchemyInscricaoRepository(session)
    escola_repo = SQLAlchemyEscolaRepository(session)
    citizen_repo = CitizenRepository(session)
    request_service = ServiceRequestLifecycleBridge(session)
    return InscricaoService(
        inscricao_repo=inscricao_repo,
        escola_repo=escola_repo,
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


def _bridge_services(session: AsyncSession):
    return (CitizenRepository(session), ServiceRequestLifecycleBridge(session))


async def get_boletim_service(session: AsyncSession = Depends(db_dep)) -> BoletimService:
    citizen_repo, request_service = _bridge_services(session)
    return BoletimService(
        repository=SQLAlchemyBoletimRepository(session),
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


async def get_certificado_service(session: AsyncSession = Depends(db_dep)) -> CertificadoService:
    citizen_repo, request_service = _bridge_services(session)
    return CertificadoService(
        repository=SQLAlchemyCertificadoRepository(session),
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


async def get_transferencia_service(
    session: AsyncSession = Depends(db_dep),
) -> TransferenciaService:
    citizen_repo, request_service = _bridge_services(session)
    return TransferenciaService(
        repository=SQLAlchemyTransferenciaRepository(session),
        matricula_repo=SQLAlchemyMatriculaRepository(session),
        escola_repo=SQLAlchemyEscolaRepository(session),
        turma_repo=SQLAlchemyTurmaRepository(session),
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


async def get_transfer_transaction_service(
    session: AsyncSession = Depends(db_dep),
) -> TransferTransactionService:
    citizen_repo = CitizenRepository(session)
    candidate_repo = make_emprego_candidato_repository(session)
    bolsa_repo = make_juventude_bolsa_estudo_repository(session)
    propina_repo = SQLAlchemyPropinaRepository(session)
    request_service = ServiceRequestLifecycleBridge(session)
    service = TransferTransactionService(
        session=session,
        turma_repo=SQLAlchemyTurmaRepository(session),
        capacity_repo=SQLAlchemyCapacityRepository(session),
        enrollment_repo=SQLAlchemyEnrollmentRepository(session),
        academic_identity_repo=SQLAlchemyAcademicIdentityRepository(session),
        citizen_repo=citizen_repo,
        candidate_repo=candidate_repo,
        bolsa_repo=bolsa_repo,
        propina_repo=propina_repo,
        request_service=request_service,
    )
    service.execute_transfer = idempotent(
        operation_name="transfer.execute",
        store=_get_idempotency_store(),
    )(service.execute_transfer)
    return service


async def get_propina_service(session: AsyncSession = Depends(db_dep)) -> PropinaService:
    citizen_repo, request_service = _bridge_services(session)
    return PropinaService(
        repository=SQLAlchemyPropinaRepository(session),
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


async def get_emprego_service(session: AsyncSession = Depends(db_dep)) -> EmpregoService:
    citizen_repo, request_service = _bridge_services(session)
    return EmpregoService(
        repository=SQLAlchemyEmpregoRepository(session),
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


async def get_concurso_service(session: AsyncSession = Depends(db_dep)) -> ConcursoService:
    citizen_repo, request_service = _bridge_services(session)
    return ConcursoService(
        repository=SQLAlchemyConcursoRepository(session),
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


async def get_formacao_service(session: AsyncSession = Depends(db_dep)) -> FormacaoService:
    citizen_repo, request_service = _bridge_services(session)
    return FormacaoService(
        repository=SQLAlchemyFormacaoRepository(session),
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


async def get_universidade_service(session: AsyncSession = Depends(db_dep)) -> UniversidadeService:
    citizen_repo, request_service = _bridge_services(session)
    return UniversidadeService(
        repository=SQLAlchemyUniversidadeRepository(session),
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


async def get_wizard_matricula_service(
    session: AsyncSession = Depends(db_dep),
):
    from apps.backend.app.modules.educacao.application.canonical.wizard_matricula_service import (
        WizardMatriculaService,
    )
    from apps.backend.app.modules.educacao.infrastructure.repositories.sqlalchemy_wizard_session_repository import (
        SQLAlchemyWizardSessionRepository,
    )

    wizard_repo = SQLAlchemyWizardSessionRepository(session)
    matricula_service = await get_matricula_service(session)
    return WizardMatriculaService(
        wizard_repo=wizard_repo,
        matricula_service=matricula_service,
    )