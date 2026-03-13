from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, status
from apps.backend.app.modules.resources.pecuaria.api.deps import get_sanidade_service
from apps.backend.app.modules.resources.pecuaria.api.schemas.sanidade_schema import VacinaCreate, VacinaResponse
from apps.backend.app.modules.resources.pecuaria.application.services.sanidade_service import SanidadeService
router = APIRouter(prefix='/sanidade', tags=['Pecuaria - Sanidade'])

@router.post('/vacinas', response_model=VacinaResponse, status_code=status.HTTP_201_CREATED)
async def aplicar_vacina(data: VacinaCreate, service: SanidadeService=Depends(get_sanidade_service)):
    return await service.aplicar_vacina(animal_id=data.animal_id, nome=data.nome, data_aplicacao=data.data_aplicacao, proxima_dose=data.proxima_dose)

@router.get('/vacinas', response_model=list[VacinaResponse])
async def listar_vacinas(animal_id: UUID | None=None, service: SanidadeService=Depends(get_sanidade_service)):
    return await service.listar_vacinas(animal_id=animal_id)