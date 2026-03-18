from __future__ import annotations
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.api.deps import get_current_user
from apps.backend.app.modules.educacao.api.deps import get_matricula_service
from apps.backend.app.modules.educacao.api.schemas import MatriculaAtivar, MatriculaCreate, MatriculaResponse
from apps.backend.app.modules.educacao.application.matricula_service import MatriculaService
from apps.backend.app.modules.educacao.exceptions import CitizenNotFoundError, IdadeMinimaNaoAtendidaError, EscolaNotFoundError, InvalidMatriculaStateError, MatriculaAlreadyExistsError, TurmaNotFoundError, TurmaSemVagasError
router = APIRouter(prefix='/matriculas', tags=['Educacao - Matriculas'])

@router.post('/', response_model=MatriculaResponse, status_code=status.HTTP_201_CREATED)
async def criar_matricula(data: MatriculaCreate, service: MatriculaService=Depends(get_matricula_service), _: dict=Depends(get_current_user)):
    try:
        return await service.criar_matricula(citizen_id=data.citizen_id, escola_id=data.escola_id, turma_id=data.turma_id, ano_letivo_id=data.ano_letivo_id, observacoes=data.observacoes)
    except CitizenNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except EscolaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TurmaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except IdadeMinimaNaoAtendidaError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except TurmaSemVagasError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except InvalidMatriculaStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except MatriculaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

@router.post('/{matricula_id}/ativar', response_model=MatriculaResponse)
async def ativar_matricula(matricula_id: UUID, data: MatriculaAtivar, service: MatriculaService=Depends(get_matricula_service), _: dict=Depends(get_current_user)):
    if not data.confirmacao_documental:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Confirmacao documental obrigatoria')
    try:
        return await service.ativar_matricula(matricula_id)
    except InvalidMatriculaStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/citizen/{citizen_id}', response_model=list[MatriculaResponse])
async def listar_matriculas_cidadao(citizen_id: UUID, ano_letivo_id: Optional[UUID]=None, service: MatriculaService=Depends(get_matricula_service), _: dict=Depends(get_current_user)):
    return await service.listar_por_cidadao(citizen_id, ano_letivo_id)