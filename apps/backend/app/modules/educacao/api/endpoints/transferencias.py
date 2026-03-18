from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.api.deps import get_current_user
from apps.backend.app.modules.educacao.api.deps import get_transferencia_service
from apps.backend.app.modules.educacao.api.schemas.transferencia_schema import TransferenciaAprovar, TransferenciaCreate, TransferenciaRejeitar, TransferenciaResponse
from apps.backend.app.modules.educacao.application.transferencia_service import TransferenciaService
from apps.backend.app.modules.educacao.exceptions import CitizenNotFoundError, EscolaNotFoundError, InvalidMatriculaStateError, MatriculaNotFoundError, TransferenciaDuplicadaError, TransferenciaEstadoInvalidoError, TransferenciaNotFoundError, TurmaNotFoundError, TurmaSemVagasError
router = APIRouter(prefix='/transferencias', tags=['Educacao - Transferencias'])

def _actor_id(user: dict) -> UUID:
    user_id = user.get('user_id') if user else None
    if not user_id:
        return UUID(int=0)
    return UUID(user_id)

@router.post('/', response_model=TransferenciaResponse, status_code=status.HTTP_201_CREATED)
async def solicitar_transferencia(data: TransferenciaCreate, service: TransferenciaService=Depends(get_transferencia_service), _: dict=Depends(get_current_user)):
    try:
        return await service.solicitar_transferencia(matricula_id=data.matricula_id, escola_destino_id=data.escola_destino_id, turma_destino_id=data.turma_destino_id, motivo=data.motivo, observacoes=data.observacoes)
    except (MatriculaNotFoundError, EscolaNotFoundError, TurmaNotFoundError, CitizenNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except (TransferenciaDuplicadaError, TurmaSemVagasError) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except (InvalidMatriculaStateError, TransferenciaEstadoInvalidoError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{transferencia_id}/aprovar', response_model=TransferenciaResponse)
async def aprovar_transferencia(transferencia_id: UUID, data: TransferenciaAprovar, service: TransferenciaService=Depends(get_transferencia_service), user: dict=Depends(get_current_user)):
    try:
        return await service.aprovar_transferencia(transferencia_id=transferencia_id, actor_id=_actor_id(user), resumo=data.resumo)
    except (TransferenciaNotFoundError, MatriculaNotFoundError, EscolaNotFoundError, TurmaNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TurmaSemVagasError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except (InvalidMatriculaStateError, TransferenciaEstadoInvalidoError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{transferencia_id}/rejeitar', response_model=TransferenciaResponse)
async def rejeitar_transferencia(transferencia_id: UUID, data: TransferenciaRejeitar, service: TransferenciaService=Depends(get_transferencia_service), user: dict=Depends(get_current_user)):
    try:
        return await service.rejeitar_transferencia(transferencia_id=transferencia_id, actor_id=_actor_id(user), motivo=data.motivo)
    except TransferenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TransferenciaEstadoInvalidoError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{transferencia_id}', response_model=TransferenciaResponse)
async def obter_transferencia(transferencia_id: UUID, service: TransferenciaService=Depends(get_transferencia_service), _: dict=Depends(get_current_user)):
    item = await service.get_record(transferencia_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Transferencia nao encontrada')
    return item

@router.get('/citizen/{citizen_id}', response_model=list[TransferenciaResponse])
async def listar_transferencias_cidadao(citizen_id: UUID, service: TransferenciaService=Depends(get_transferencia_service), _: dict=Depends(get_current_user)):
    return await service.list_records(citizen_id)