from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.resources.agricultura.api.deps import get_assistencia_service
from apps.backend.app.modules.resources.agricultura.api.schemas.assistencia_schema import AssistenciaCancelamentoInput, AssistenciaConclusaoInput, AssistenciaCreate, AssistenciaResponse
from apps.backend.app.modules.resources.agricultura.application.services.assistencia_service import AssistenciaService
from apps.backend.app.modules.resources.agricultura.exceptions import AssistenciaNotFoundError, PropriedadeNotFoundError
router = APIRouter(prefix='/assistencia', tags=['Agricultura - assistencia'])

@router.post('/', response_model=AssistenciaResponse, status_code=status.HTTP_201_CREATED)
async def agendar_assistencia(data: AssistenciaCreate, service: AssistenciaService=Depends(get_assistencia_service)):
    try:
        return await service.agendar(codigo_propriedade=data.codigo_propriedade, tecnico_nome=data.tecnico_nome, objetivo=data.objetivo)
    except PropriedadeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_assistencia:path}/concluir', response_model=AssistenciaResponse)
async def concluir_assistencia(codigo_assistencia: str, data: AssistenciaConclusaoInput, service: AssistenciaService=Depends(get_assistencia_service)):
    try:
        return await service.concluir(codigo_assistencia, recomendacoes=data.recomendacoes)
    except AssistenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_assistencia:path}/cancelar', response_model=AssistenciaResponse)
async def cancelar_assistencia(codigo_assistencia: str, data: AssistenciaCancelamentoInput, service: AssistenciaService=Depends(get_assistencia_service)):
    try:
        return await service.cancelar(codigo_assistencia, motivo=data.motivo)
    except AssistenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_assistencia:path}', response_model=AssistenciaResponse)
async def obter_assistencia(codigo_assistencia: str, service: AssistenciaService=Depends(get_assistencia_service)):
    try:
        return await service.obter(codigo_assistencia)
    except AssistenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[AssistenciaResponse])
async def listar_assistencias(codigo_propriedade: str | None=None, service: AssistenciaService=Depends(get_assistencia_service)):
    return await service.listar(codigo_propriedade=codigo_propriedade)