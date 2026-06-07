from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.juventude.api.deps import get_formacao_service
from apps.backend.app.modules.society.juventude.api.schemas.formacao_schema import (
    FormacaoCreate,
    FormacaoResponse,
    FormacaoStatusUpdate,
)
from apps.backend.app.modules.society.juventude.application.services.formacao_service import (
    FormacaoService,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusFormacao

router = APIRouter(prefix="/formacoes", tags=["Juventude - Formacoes"])

formacao_service_dep = Depends(get_formacao_service)


@router.post("/", response_model=FormacaoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_formacao(
    data: FormacaoCreate, service: FormacaoService = formacao_service_dep
) -> FormacaoResponse:
    try:
        return await service.registrar_formacao(
            jovem_id=data.jovem_id,
            programa_id=data.programa_id,
            nome_curso=data.nome_curso,
            instituicao=data.instituicao,
            carga_horaria=data.carga_horaria,
            data_inicio=data.data_inicio,
            data_fim=data.data_fim,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{formacao_id}", response_model=FormacaoResponse)
async def obter_formacao(
    formacao_id: UUID, service: FormacaoService = formacao_service_dep
) -> FormacaoResponse:
    try:
        return await service.buscar_formacao(formacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[FormacaoResponse])
async def listar_formacoes(
    jovem_id: UUID | None = None,
    programa_id: UUID | None = None,
    status_filtro: StatusFormacao | None = None,
    service: FormacaoService = formacao_service_dep,
) -> list[FormacaoResponse]:
    return await service.listar_formacoes(
        jovem_id=jovem_id, programa_id=programa_id, status=status_filtro
    )


@router.patch("/{formacao_id}/status", response_model=FormacaoResponse)
async def atualizar_status_formacao(
    formacao_id: UUID,
    data: FormacaoStatusUpdate,
    service: FormacaoService = formacao_service_dep,
) -> FormacaoResponse:
    try:
        return await service.atualizar_status(
            formacao_id=formacao_id,
            status=data.status,
            certificado_emitido=data.certificado_emitido,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{formacao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_formacao(
    formacao_id: UUID, service: FormacaoService = formacao_service_dep
) -> None:
    try:
        await service.remover_formacao(formacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc