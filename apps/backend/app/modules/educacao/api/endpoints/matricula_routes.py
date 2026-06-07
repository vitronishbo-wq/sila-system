from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status

from apps.backend.app.api.deps import get_current_user
from apps.backend.app.modules.educacao.api.deps import get_matricula_service
from apps.backend.app.modules.educacao.api.schemas import (
    MatriculaAtivar,
    MatriculaCreate,
    MatriculaResponse,
)
from apps.backend.app.modules.educacao.application.matricula_service import MatriculaService
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
    _: dict = current_user_dep,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
):
    try:
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
    _: dict = current_user_dep,
):
    if not data.confirmacao_documental:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Confirmacao documental obrigatoria"
        )
    try:
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