from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.pecuaria.api.deps import get_animal_service
from apps.backend.app.modules.resources.pecuaria.api.schemas.animal_schema import (
    AnimalCreate,
    AnimalFilter,
    AnimalResponse,
)
from apps.backend.app.modules.resources.pecuaria.application.services.animal_service import (
    AnimalService,
)

router = APIRouter(prefix="/animais", tags=["Pecuaria - Animais"])

animal_service_dep = Depends(get_animal_service)
filtros_dep = Depends()


@router.post("/", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_animal(
    data: AnimalCreate, service: AnimalService = animal_service_dep
):
    try:
        return await service.cadastrar_animal(
            brinco=data.brinco,
            tipo=data.tipo,
            raca_id=data.raca_id,
            sexo=data.sexo,
            data_nascimento=data.data_nascimento,
            proprietario_id=data.proprietario_id,
            propriedade_id=data.propriedade_id,
            rebanho_id=data.rebanho_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{animal_id}", response_model=AnimalResponse)
async def obter_animal(animal_id: UUID, service: AnimalService = animal_service_dep):
    try:
        return await service.buscar_animal(animal_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[AnimalResponse])
async def listar_animais(
    filtros: AnimalFilter = filtros_dep, service: AnimalService = animal_service_dep
):
    return await service.listar_animais(
        propriedade_id=filtros.propriedade_id, tipo=filtros.tipo, status=filtros.status
    )