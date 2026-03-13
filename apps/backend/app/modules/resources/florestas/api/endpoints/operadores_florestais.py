from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from apps.backend.app.modules.resources.florestas.api.deps import get_operador_florestal_service
from apps.backend.app.modules.resources.florestas.api.schemas.operador_florestal_schema import OperadorFlorestalCreate, OperadorFlorestalResponse
from apps.backend.app.modules.resources.florestas.application.services.operador_florestal_service import OperadorFlorestalService
router = APIRouter(prefix='/operadores-florestais', tags=['Florestas - Operadores Florestais'])

@router.post('/', response_model=OperadorFlorestalResponse, status_code=201)
async def cadastrar_operador(data: OperadorFlorestalCreate, service: OperadorFlorestalService=Depends(get_operador_florestal_service)):
    try:
        return await service.cadastrar_operador(nome=data.nome, nif=data.nif, tipo_operador=data.tipo_operador)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.get('/', response_model=list[OperadorFlorestalResponse])
async def listar_operadores(service: OperadorFlorestalService=Depends(get_operador_florestal_service)):
    return await service.listar_operadores()