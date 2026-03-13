from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.deps import get_ocorrencia_service
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.schemas.ocorrencia_schema import OcorrenciaCreate, OcorrenciaResponse
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.services.ocorrencia_service import OcorrenciaService
router = APIRouter(prefix='/ocorrencias', tags=['Aviacao Civil - Ocorrencias'])

@router.post('/', response_model=OcorrenciaResponse, status_code=status.HTTP_201_CREATED)
async def criar_ocorrencia(payload: OcorrenciaCreate, service: OcorrenciaService=Depends(get_ocorrencia_service)) -> OcorrenciaResponse:
    try:
        ocorrencia = await service.registrar_ocorrencia(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return OcorrenciaResponse.model_validate(ocorrencia)

@router.get('/', response_model=list[OcorrenciaResponse])
async def listar_ocorrencias(service: OcorrenciaService=Depends(get_ocorrencia_service)) -> list[OcorrenciaResponse]:
    ocorrencias = await service.listar_ocorrencias()
    return [OcorrenciaResponse.model_validate(item) for item in ocorrencias]