from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.api.deps import get_matricula_service
from apps.backend.app.modules.educacao.api.schemas import (
    MatriculaAtivar,
    MatriculaCreate,
    MatriculaResponse,
)
from apps.backend.app.modules.educacao.application.matricula_service import MatriculaService
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.modules.educacao.infrastructure.models.matricula_model import MatriculaModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.educacao.exceptions import (
    CitizenNotFoundError,
    EscolaNotFoundError,
    IdadeMinimaNaoAtendidaError,
    InvalidMatriculaStateError,
    MatriculaAlreadyExistsError,
    TurmaNotFoundError,
    TurmaSemVagasError,
)
from foundation.resilience import (
    DuplicateRequestError,
    IdempotencyKeyMissingError,
    create_redis_idempotency_store,
    idempotent,
)

router = APIRouter(prefix="/matriculas", tags=["Educacao - Matriculas"])

# shared idempotency store for endpoints in this module
_IDEMPOTENCY_STORE = create_redis_idempotency_store()

current_user_dep = Depends(get_current_user)
matricula_service_dep = Depends(get_matricula_service)


@router.post("/", response_model=MatriculaResponse, status_code=status.HTTP_201_CREATED)
@idempotent(operation_name="educacao.criar_matricula", store=_IDEMPOTENCY_STORE, ttl_seconds=3600)
async def criar_matricula(
    data: MatriculaCreate,
    service: MatriculaService = matricula_service_dep,
    user: dict = current_user_dep,
    session: AsyncSession = Depends(get_db),
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
):
    try:
        # territorial check: ensure user can act on the escola's territory
        escola_model = await session.get(EscolaModel, data.escola_id)
        if not escola_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Escola {data.escola_id} nao encontrada")
        await verify_territorial_access(user=user, resource_territory_id=getattr(escola_model, "territory_id", None), db=session)
        return await service.criar_matricula(
            citizen_id=data.citizen_id,
            escola_id=data.escola_id,
            turma_id=data.turma_id,
            ano_letivo_id=data.ano_letivo_id,
            observacoes=data.observacoes,
            idempotency_key=idempotency_key,
        )
    except CitizenNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except EscolaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except TurmaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except IdadeMinimaNaoAtendidaError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except TurmaSemVagasError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except InvalidMatriculaStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except MatriculaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except IdempotencyKeyMissingError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except DuplicateRequestError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/{matricula_id}/ativar", response_model=MatriculaResponse)
async def ativar_matricula(
    matricula_id: UUID,
    data: MatriculaAtivar,
    service: MatriculaService = matricula_service_dep,
    user: dict = current_user_dep,
    session: AsyncSession = Depends(get_db),
):
    if not data.confirmacao_documental:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Confirmacao documental obrigatoria"
        )
    try:
        # territorial check: ensure user can act on the matricula's escola territory
        matricula_model = await session.get(MatriculaModel, matricula_id)
        if not matricula_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matricula nao encontrada")
        escola_model = await session.get(EscolaModel, matricula_model.escola_id)
        await verify_territorial_access(user=user, resource_territory_id=getattr(escola_model, "territory_id", None), db=session)
        return await service.ativar_matricula(matricula_id)
    except InvalidMatriculaStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/citizen/{citizen_id}", response_model=list[MatriculaResponse])
async def listar_matriculas_cidadao(
    citizen_id: UUID,
    ano_letivo_id: UUID | None = None,
    service: MatriculaService = matricula_service_dep,
    _: dict = current_user_dep,
):
    return await service.listar_por_cidadao(citizen_id, ano_letivo_id)