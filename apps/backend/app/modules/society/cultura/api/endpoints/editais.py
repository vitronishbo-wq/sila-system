from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.cultura.api.deps import get_edital_service
from apps.backend.app.modules.society.cultura.api.schemas.edital_schema import (
    EditalCreate,
    EditalInscricaoRequest,
    EditalResponse,
    EditalSelecaoRequest,
)
from apps.backend.app.modules.society.cultura.application.services.edital_service import (
    EditalService,
)
from apps.backend.app.modules.society.cultura.domain.enums import (
    FaseEditalCultural,
    TipoEditalCultural,
)

router = APIRouter(prefix="/editais", tags=["Cultura - Editais"])

edital_service_dep = Depends(get_edital_service)


@router.post("/", response_model=EditalResponse, status_code=status.HTTP_201_CREATED)
async def publicar_edital(
    data: EditalCreate, service: EditalService = edital_service_dep
) -> EditalResponse:
    try:
        return await service.publicar_edital(
            numero=data.numero,
            titulo=data.titulo,
            tipo=data.tipo,
            orgao_responsavel_id=data.orgao_responsavel_id,
            valor_total=data.valor_total,
            data_publicacao=data.data_publicacao,
            data_inicio_inscricoes=data.data_inicio_inscricoes,
            data_fim_inscricoes=data.data_fim_inscricoes,
            vagas=data.vagas,
            descricao=data.descricao,
            criterios=data.criterios,
            documentos_necessarios=data.documentos_necessarios,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{edital_id}", response_model=EditalResponse)
async def obter_edital(
    edital_id: UUID, service: EditalService = edital_service_dep
) -> EditalResponse:
    try:
        return await service.buscar_edital(edital_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[EditalResponse])
async def listar_editais(
    tipo: TipoEditalCultural | None = None,
    fase: FaseEditalCultural | None = None,
    data_inicio: datetime | None = None,
    data_fim: datetime | None = None,
    somente_ativos: bool = True,
    service: EditalService = edital_service_dep,
) -> list[EditalResponse]:
    return await service.listar_editais(
        tipo=tipo,
        fase=fase,
        data_inicio=data_inicio,
        data_fim=data_fim,
        somente_ativos=somente_ativos,
    )


@router.patch("/{edital_id}/abrir-inscricoes", response_model=EditalResponse)
async def abrir_inscricoes(
    edital_id: UUID, service: EditalService = edital_service_dep
) -> EditalResponse:
    try:
        return await service.abrir_inscricoes(edital_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{edital_id}/encerrar-inscricoes", response_model=EditalResponse)
async def encerrar_inscricoes(
    edital_id: UUID, service: EditalService = edital_service_dep
) -> EditalResponse:
    try:
        return await service.encerrar_inscricoes(edital_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{edital_id}/inscrever", response_model=EditalResponse)
async def inscrever_projeto(
    edital_id: UUID,
    data: EditalInscricaoRequest,
    service: EditalService = edital_service_dep,
) -> EditalResponse:
    try:
        return await service.inscrever_projeto(edital_id=edital_id, projeto_id=data.projeto_id)
    except ValueError as exc:
        message = str(exc).lower()
        code = (
            status.HTTP_404_NOT_FOUND
            if "nao encontrado" in message
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=str(exc)) from exc


@router.patch("/{edital_id}/selecionar", response_model=EditalResponse)
async def selecionar_projetos(
    edital_id: UUID,
    data: EditalSelecaoRequest,
    service: EditalService = edital_service_dep,
) -> EditalResponse:
    try:
        return await service.selecionar_projetos(
            edital_id=edital_id, projetos_ids=data.projetos_ids
        )
    except ValueError as exc:
        message = str(exc).lower()
        code = (
            status.HTTP_404_NOT_FOUND
            if "nao encontrado" in message
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=str(exc)) from exc


@router.delete("/{edital_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_edital(
    edital_id: UUID, service: EditalService = edital_service_dep
) -> None:
    try:
        await service.remover_edital(edital_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc