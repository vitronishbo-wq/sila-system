from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.desporto.api.deps import get_clube_service
from apps.backend.app.modules.society.desporto.api.schemas.clube_schema import (
    ClubeCreate,
    ClubeResponse,
    ClubeUpdate,
)
from apps.backend.app.modules.society.desporto.application.services.clube_service import (
    ClubeService,
)
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, TipoClube

router = APIRouter(prefix="/clubes", tags=["Desporto - Clubes"])

clube_service_dep = Depends(get_clube_service)


@router.post("/", response_model=ClubeResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_clube(
    data: ClubeCreate, service: ClubeService = clube_service_dep
) -> ClubeResponse:
    try:
        return await service.cadastrar_clube(
            nome=data.nome,
            sigla=data.sigla,
            tipo=data.tipo,
            modalidade_principal=data.modalidade_principal,
            municipio=data.municipio,
            provincia=data.provincia,
            data_fundacao=data.data_fundacao,
            codigo_obra_instalacao=data.codigo_obra_instalacao,
            instituicao_educacional_id=data.instituicao_educacional_id,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{clube_id}", response_model=ClubeResponse)
async def obter_clube(
    clube_id: UUID, service: ClubeService = clube_service_dep
) -> ClubeResponse:
    try:
        return await service.buscar_clube(clube_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ClubeResponse])
async def listar_clubes(
    tipo: TipoClube | None = None,
    modalidade: ModalidadeDesportiva | None = None,
    municipio: str | None = None,
    somente_ativos: bool = True,
    service: ClubeService = clube_service_dep,
) -> list[ClubeResponse]:
    return await service.listar_clubes(
        tipo=tipo, modalidade=modalidade, municipio=municipio, somente_ativos=somente_ativos
    )


@router.patch("/{clube_id}", response_model=ClubeResponse)
async def atualizar_clube(
    clube_id: UUID, data: ClubeUpdate, service: ClubeService = clube_service_dep
) -> ClubeResponse:
    try:
        return await service.atualizar_clube(
            clube_id=clube_id,
            nome=data.nome,
            sigla=data.sigla,
            tipo=data.tipo,
            modalidade_principal=data.modalidade_principal,
            municipio=data.municipio,
            provincia=data.provincia,
            data_fundacao=data.data_fundacao,
            codigo_obra_instalacao=data.codigo_obra_instalacao,
            instituicao_educacional_id=data.instituicao_educacional_id,
            ativo=data.ativo,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        message = str(exc).lower()
        code = (
            status.HTTP_404_NOT_FOUND
            if "nao encontrado" in message
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=str(exc)) from exc


@router.delete("/{clube_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_clube(clube_id: UUID, service: ClubeService = clube_service_dep) -> None:
    try:
        await service.remover_clube(clube_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc