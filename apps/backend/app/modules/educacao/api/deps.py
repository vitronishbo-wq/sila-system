from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.api.deps import get_db
from apps.backend.app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from apps.backend.app.modules.educacao.application.boletim_service import BoletimService
from apps.backend.app.modules.educacao.application.certificado_service import CertificadoService
from apps.backend.app.modules.educacao.application.concurso_service import ConcursoService
from apps.backend.app.modules.educacao.application.emprego_service import EmpregoService
from apps.backend.app.modules.educacao.application.formacao_service import FormacaoService
from apps.backend.app.modules.educacao.application.inscricao_service import InscricaoService
from apps.backend.app.modules.educacao.application.matricula_service import MatriculaService
from apps.backend.app.modules.educacao.application.propina_service import PropinaService
from apps.backend.app.modules.educacao.application.transferencia_service import TransferenciaService
from apps.backend.app.modules.educacao.application.universidade_service import UniversidadeService
from apps.backend.app.modules.educacao.infrastructure.repositories import SQLAlchemyBoletimRepository, SQLAlchemyCertificadoRepository, SQLAlchemyConcursoRepository, SQLAlchemyEmpregoRepository, SQLAlchemyEscolaRepository, SQLAlchemyFormacaoRepository, SQLAlchemyInscricaoRepository, SQLAlchemyMatriculaRepository, SQLAlchemyPropinaRepository, SQLAlchemyTurmaRepository, SQLAlchemyTransferenciaRepository, SQLAlchemyUniversidadeRepository

async def get_matricula_service(session: AsyncSession=Depends(get_db)) -> MatriculaService:
    matricula_repo = SQLAlchemyMatriculaRepository(session)
    turma_repo = SQLAlchemyTurmaRepository(session)
    escola_repo = SQLAlchemyEscolaRepository(session)
    citizen_repo = CitizenRepository(session)
    request_service = ServiceRequestLifecycleBridge(session)
    return MatriculaService(matricula_repo=matricula_repo, turma_repo=turma_repo, escola_repo=escola_repo, citizen_repo=citizen_repo, request_service=request_service)

async def get_inscricao_service(session: AsyncSession=Depends(get_db)) -> InscricaoService:
    inscricao_repo = SQLAlchemyInscricaoRepository(session)
    escola_repo = SQLAlchemyEscolaRepository(session)
    citizen_repo = CitizenRepository(session)
    request_service = ServiceRequestLifecycleBridge(session)
    return InscricaoService(inscricao_repo=inscricao_repo, escola_repo=escola_repo, citizen_repo=citizen_repo, request_service=request_service)

def _bridge_services(session: AsyncSession):
    return (CitizenRepository(session), ServiceRequestLifecycleBridge(session))

async def get_boletim_service(session: AsyncSession=Depends(get_db)) -> BoletimService:
    citizen_repo, request_service = _bridge_services(session)
    return BoletimService(repository=SQLAlchemyBoletimRepository(session), citizen_repo=citizen_repo, request_service=request_service)

async def get_certificado_service(session: AsyncSession=Depends(get_db)) -> CertificadoService:
    citizen_repo, request_service = _bridge_services(session)
    return CertificadoService(repository=SQLAlchemyCertificadoRepository(session), citizen_repo=citizen_repo, request_service=request_service)

async def get_transferencia_service(session: AsyncSession=Depends(get_db)) -> TransferenciaService:
    citizen_repo, request_service = _bridge_services(session)
    return TransferenciaService(repository=SQLAlchemyTransferenciaRepository(session), matricula_repo=SQLAlchemyMatriculaRepository(session), escola_repo=SQLAlchemyEscolaRepository(session), turma_repo=SQLAlchemyTurmaRepository(session), citizen_repo=citizen_repo, request_service=request_service)

async def get_propina_service(session: AsyncSession=Depends(get_db)) -> PropinaService:
    citizen_repo, request_service = _bridge_services(session)
    return PropinaService(repository=SQLAlchemyPropinaRepository(session), citizen_repo=citizen_repo, request_service=request_service)

async def get_emprego_service(session: AsyncSession=Depends(get_db)) -> EmpregoService:
    citizen_repo, request_service = _bridge_services(session)
    return EmpregoService(repository=SQLAlchemyEmpregoRepository(session), citizen_repo=citizen_repo, request_service=request_service)

async def get_concurso_service(session: AsyncSession=Depends(get_db)) -> ConcursoService:
    citizen_repo, request_service = _bridge_services(session)
    return ConcursoService(repository=SQLAlchemyConcursoRepository(session), citizen_repo=citizen_repo, request_service=request_service)

async def get_formacao_service(session: AsyncSession=Depends(get_db)) -> FormacaoService:
    citizen_repo, request_service = _bridge_services(session)
    return FormacaoService(repository=SQLAlchemyFormacaoRepository(session), citizen_repo=citizen_repo, request_service=request_service)

async def get_universidade_service(session: AsyncSession=Depends(get_db)) -> UniversidadeService:
    citizen_repo, request_service = _bridge_services(session)
    return UniversidadeService(repository=SQLAlchemyUniversidadeRepository(session), citizen_repo=citizen_repo, request_service=request_service)
