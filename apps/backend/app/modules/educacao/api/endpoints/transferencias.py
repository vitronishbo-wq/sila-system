from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status

from apps.backend.app.api.deps import get_current_user
from apps.backend.app.modules.educacao.api.deps import (
    get_transfer_transaction_service,
    get_transferencia_service,
)
from apps.backend.app.modules.educacao.api.schemas.transferencia_schema import (
    TransferenciaAprovar,
    TransferenciaCreate,
    TransferenciaRejeitar,
    TransferenciaResponse,
    TransferTransactionCreate,
    TransferTransactionResponse,
)
from apps.backend.app.modules.educacao.application.transfer_transaction_service import (
    TransferTransactionService,
)
from apps.backend.app.modules.educacao.application.transferencia_service import TransferenciaService
from apps.backend.app.modules.educacao.exceptions import (
    CitizenNotFoundError,
    EscolaNotFoundError,
    InvalidMatriculaStateError,
    MatriculaNotFoundError,
    TransferenciaDuplicadaError,
    TransferenciaEstadoInvalidoError,
    TransferenciaNotFoundError,
    TurmaNotFoundError,
    TurmaSemVagasError,
)
from foundation.resilience import (
    DuplicateRequestError,
    IdempotencyKeyMissingError,
    create_redis_idempotency_store,
    idempotent,
)

router = APIRouter(prefix="/transferencias", tags=["Educacao - Transferencias"])

# shared idempotency store for transfer endpoints
_IDEMPOTENCY_STORE = create_redis_idempotency_store()

current_user_dep = Depends(get_current_user)
transferencia_service_dep = Depends(get_transferencia_service)
transfer_transaction_service_dep = Depends(get_transfer_transaction_service)


def _actor_id(user: dict) -> UUID:
    user_id = user.get("user_id") if user else None
    if not user_id:
        return UUID(int=0)
    return UUID(user_id)


@router.post("/", response_model=TransferenciaResponse, status_code=status.HTTP_201_CREATED)
@idempotent(operation_name="educacao.solicitar_transferencia", store=_IDEMPOTENCY_STORE, ttl_seconds=3600)
async def solicitar_transferencia(
    data: TransferenciaCreate,
    service: TransferenciaService = transferencia_service_dep,
    _: dict = current_user_dep,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
):
    try:
        return await service.solicitar_transferencia(
            matricula_id=data.matricula_id,
            escola_destino_id=data.escola_destino_id,
            turma_destino_id=data.turma_destino_id,
            motivo=data.motivo,
            observacoes=data.observacoes,
        )
    except (
        MatriculaNotFoundError,
        EscolaNotFoundError,
        TurmaNotFoundError,
        CitizenNotFoundError,
    ) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except (TransferenciaDuplicadaError, TurmaSemVagasError) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (InvalidMatriculaStateError, TransferenciaEstadoInvalidoError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/transacional", response_model=TransferTransactionResponse, status_code=status.HTTP_201_CREATED)
@idempotent(operation_name="educacao.executar_transferencia_transacional", store=_IDEMPOTENCY_STORE, ttl_seconds=3600)
async def executar_transferencia_transacional(
    data: TransferTransactionCreate,
    service: TransferTransactionService = transfer_transaction_service_dep,
    user: dict = current_user_dep,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
):
    try:
        return await service.execute_transfer(
            student_id=data.student_id,
            current_enrollment_id=data.current_enrollment_id,
            target_institution_id=data.target_institution_id,
            target_grade=data.target_grade,
            target_shift=data.target_shift,
            academic_year=data.academic_year,
            reason=data.reason,
            actor_id=_actor_id(user),
            idempotency_key=idempotency_key,
        )
    except EscolaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except TurmaSemVagasError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except IdempotencyKeyMissingError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except DuplicateRequestError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (InvalidMatriculaStateError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{transferencia_id}/aprovar", response_model=TransferenciaResponse)
async def aprovar_transferencia(
    transferencia_id: UUID,
    data: TransferenciaAprovar,
    service: TransferenciaService = transferencia_service_dep,
    user: dict = current_user_dep,
):
    try:
        return await service.aprovar_transferencia(
            transferencia_id=transferencia_id, actor_id=_actor_id(user), resumo=data.resumo
        )
    except (
        TransferenciaNotFoundError,
        MatriculaNotFoundError,
        EscolaNotFoundError,
        TurmaNotFoundError,
    ) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except TurmaSemVagasError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (InvalidMatriculaStateError, TransferenciaEstadoInvalidoError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{transferencia_id}/rejeitar", response_model=TransferenciaResponse)
async def rejeitar_transferencia(
    transferencia_id: UUID,
    data: TransferenciaRejeitar,
    service: TransferenciaService = transferencia_service_dep,
    user: dict = current_user_dep,
):
    try:
        return await service.rejeitar_transferencia(
            transferencia_id=transferencia_id, actor_id=_actor_id(user), motivo=data.motivo
        )
    except TransferenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except TransferenciaEstadoInvalidoError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{transferencia_id}", response_model=TransferenciaResponse)
async def obter_transferencia(
    transferencia_id: UUID,
    service: TransferenciaService = transferencia_service_dep,
    _: dict = current_user_dep,
):
    item = await service.get_record(transferencia_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transferencia nao encontrada"
        )
    return item


@router.get("/citizen/{citizen_id}", response_model=list[TransferenciaResponse])
async def listar_transferencias_cidadao(
    citizen_id: UUID,
    service: TransferenciaService = transferencia_service_dep,
    _: dict = current_user_dep,
):
    return await service.list_records(citizen_id)
