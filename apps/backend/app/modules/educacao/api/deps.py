from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from app.modules.educacao.application.services import InscricaoService, MatriculaService
from app.modules.educacao.infrastructure.repositories import (
    SQLAlchemyEscolaRepository,
    SQLAlchemyInscricaoRepository,
    SQLAlchemyMatriculaRepository,
)


async def get_matricula_service(session: AsyncSession = Depends(get_db)) -> MatriculaService:
    matricula_repo = SQLAlchemyMatriculaRepository(session)
    escola_repo = SQLAlchemyEscolaRepository(session)
    citizen_repo = CitizenRepository(session)
    request_service = ServiceRequestLifecycleBridge(session)
    return MatriculaService(
        matricula_repo=matricula_repo,
        escola_repo=escola_repo,
        citizen_repo=citizen_repo,
        request_service=request_service,
    )


async def get_inscricao_service(session: AsyncSession = Depends(get_db)) -> InscricaoService:
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
