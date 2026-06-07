from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.civil_protection.api.deps import get_bombeiro_service
from apps.backend.app.modules.civil_protection.application.dto.bombeiro_schema import (
    BombeiroCreate,
    BombeiroResponse,
    BombeiroStatusUpdate,
)
from apps.backend.app.modules.civil_protection.application.services.bombeiro_service import (
    BombeiroService,
)
from apps.backend.app.modules.civil_protection.domain.enums import StatusAgenteProtecao

router = APIRouter(prefix="/bombeiros", tags=["Protecao Civil - Bombeiros"])

bombeiro_service_dep = Depends(get_bombeiro_service)


@router.post("/", response_model=BombeiroResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_bombeiro(
    data: BombeiroCreate, service: BombeiroService = bombeiro_service_dep
) -> BombeiroResponse:
    try:
        return await service.cadastrar_bombeiro(
            corporacao_id=data.corporacao_id,
            nome=data.nome,
            data_nascimento=data.data_nascimento,
            cpf=data.cpf,
            rg=data.rg,
            cargo=data.cargo,
            telefone=data.telefone,
            email=data.email,
            endereco=data.endereco,
            observacoes=data.observacoes,
            citizen_id=data.citizen_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{bombeiro_id}", response_model=BombeiroResponse)
async def obter_bombeiro(
    bombeiro_id: UUID, service: BombeiroService = bombeiro_service_dep
) -> BombeiroResponse:
    try:
        return await service.buscar_bombeiro(bombeiro_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[BombeiroResponse])
async def listar_bombeiros(
    corporacao_id: UUID | None = None,
    status_agente: StatusAgenteProtecao | None = None,
    service: BombeiroService = bombeiro_service_dep,
) -> list[BombeiroResponse]:
    return await service.listar_bombeiros(corporacao_id=corporacao_id, status=status_agente)


@router.patch("/{bombeiro_id}/status", response_model=BombeiroResponse)
async def atualizar_status_bombeiro(
    bombeiro_id: UUID,
    data: BombeiroStatusUpdate,
    service: BombeiroService = bombeiro_service_dep,
) -> BombeiroResponse:
    try:
        return await service.atualizar_status(
            bombeiro_id=bombeiro_id, status=data.status, motivo=data.motivo
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{bombeiro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_bombeiro(
    bombeiro_id: UUID, service: BombeiroService = bombeiro_service_dep
) -> None:
    try:
        await service.remover_bombeiro(bombeiro_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc