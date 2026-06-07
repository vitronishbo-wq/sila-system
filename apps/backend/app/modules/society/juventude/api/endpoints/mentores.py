from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.juventude.api.deps import get_mentor_service
from apps.backend.app.modules.society.juventude.api.schemas.mentor_schema import (
    MentorAtribuirJovem,
    MentorCreate,
    MentorResponse,
    MentorStatusUpdate,
)
from apps.backend.app.modules.society.juventude.application.services.mentor_service import (
    MentorService,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusMentoria

router = APIRouter(prefix="/mentores", tags=["Juventude - Mentores"])

mentor_service_dep = Depends(get_mentor_service)


@router.post("/", response_model=MentorResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_mentor(
    data: MentorCreate, service: MentorService = mentor_service_dep
) -> MentorResponse:
    try:
        return await service.cadastrar_mentor(
            nome=data.nome,
            tipo_mentoria=data.tipo_mentoria,
            area_interesse=data.area_interesse,
            email=data.email,
            telefone=data.telefone,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{mentor_id}", response_model=MentorResponse)
async def obter_mentor(
    mentor_id: UUID, service: MentorService = mentor_service_dep
) -> MentorResponse:
    try:
        return await service.buscar_mentor(mentor_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[MentorResponse])
async def listar_mentores(
    status_filtro: StatusMentoria | None = None,
    service: MentorService = mentor_service_dep,
) -> list[MentorResponse]:
    return await service.listar_mentores(status=status_filtro)


@router.patch("/{mentor_id}/atribuir-jovem", response_model=MentorResponse)
async def atribuir_jovem(
    mentor_id: UUID, data: MentorAtribuirJovem, service: MentorService = mentor_service_dep
) -> MentorResponse:
    try:
        return await service.atribuir_jovem(mentor_id=mentor_id, jovem_id=data.jovem_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{mentor_id}/status", response_model=MentorResponse)
async def atualizar_status_mentor(
    mentor_id: UUID, data: MentorStatusUpdate, service: MentorService = mentor_service_dep
) -> MentorResponse:
    try:
        return await service.atualizar_status(mentor_id=mentor_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{mentor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_mentor(
    mentor_id: UUID, service: MentorService = mentor_service_dep
) -> None:
    try:
        await service.remover_mentor(mentor_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc