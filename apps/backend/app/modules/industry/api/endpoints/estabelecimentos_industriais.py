from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.industry.api.deps import get_estabelecimento_industrial_service
from apps.backend.app.modules.industry.api.schemas.estabelecimento_industrial_schema import (
    DataInput,
    EstabelecimentoIndustrialCreate,
    EstabelecimentoIndustrialResponse,
    MotivoInput,
    PorteInput,
    RamoInput,
)
from apps.backend.app.modules.industry.application.services import EstabelecimentoIndustrialService
from apps.backend.app.modules.industry.domain.enums import RamoIndustrial, StatusEstabelecimento
from apps.backend.app.modules.industry.domain.exceptions import (
    EstabelecimentoIndustrialAlreadyExistsError,
    EstabelecimentoIndustrialNotFoundError,
    InvalidEstabelecimentoIndustrialStateError,
)

router = APIRouter(
    prefix="/estabelecimentos_industriais", tags=["Industria - Estabelecimentos Industriais"]
)

estabelecimento_industrial_service_dep = Depends(get_estabelecimento_industrial_service)


@router.post(
    "/", response_model=EstabelecimentoIndustrialResponse, status_code=status.HTTP_201_CREATED
)
async def cadastrar_estabelecimento_industrial(
    data: EstabelecimentoIndustrialCreate,
    service: EstabelecimentoIndustrialService = estabelecimento_industrial_service_dep,
):
    try:
        return await service.cadastrar(
            cnpj=data.cnpj,
            razao_social=data.razao_social,
            ramo=data.ramo,
            porte=data.porte,
            tipo=data.tipo,
            cnae_principal=data.cnae_principal,
            data_abertura=data.data_abertura,
            endereco=data.endereco,
            bairro=data.bairro,
            municipio=data.municipio,
            provincia=data.provincia,
        )
    except EstabelecimentoIndustrialAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{item_id}/iniciar_atividades", response_model=EstabelecimentoIndustrialResponse)
async def iniciar_atividades(
    item_id: UUID,
    data: DataInput,
    service: EstabelecimentoIndustrialService = estabelecimento_industrial_service_dep,
):
    try:
        return await service.iniciar_atividades(item_id, data_inicio=data.data)
    except EstabelecimentoIndustrialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidEstabelecimentoIndustrialStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{item_id}/suspender_atividades", response_model=EstabelecimentoIndustrialResponse)
async def suspender_atividades(
    item_id: UUID,
    data: MotivoInput,
    service: EstabelecimentoIndustrialService = estabelecimento_industrial_service_dep,
):
    try:
        return await service.suspender_atividades(item_id, motivo=data.motivo)
    except EstabelecimentoIndustrialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidEstabelecimentoIndustrialStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{item_id}/paralisar", response_model=EstabelecimentoIndustrialResponse)
async def paralisar(
    item_id: UUID,
    data: MotivoInput,
    service: EstabelecimentoIndustrialService = estabelecimento_industrial_service_dep,
):
    try:
        return await service.paralisar(item_id, motivo=data.motivo)
    except EstabelecimentoIndustrialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidEstabelecimentoIndustrialStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{item_id}/reativar", response_model=EstabelecimentoIndustrialResponse)
async def reativar(
    item_id: UUID,
    service: EstabelecimentoIndustrialService = estabelecimento_industrial_service_dep,
):
    try:
        return await service.reativar(item_id)
    except EstabelecimentoIndustrialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidEstabelecimentoIndustrialStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{item_id}/associar_ramo", response_model=EstabelecimentoIndustrialResponse)
async def associar_ramo(
    item_id: UUID,
    data: RamoInput,
    service: EstabelecimentoIndustrialService = estabelecimento_industrial_service_dep,
):
    try:
        return await service.associar_ramo(item_id, ramo=data.ramo)
    except EstabelecimentoIndustrialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{item_id}/definir_porte", response_model=EstabelecimentoIndustrialResponse)
async def definir_porte(
    item_id: UUID,
    data: PorteInput,
    service: EstabelecimentoIndustrialService = estabelecimento_industrial_service_dep,
):
    try:
        return await service.definir_porte(item_id, porte=data.porte)
    except EstabelecimentoIndustrialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{item_id}", response_model=EstabelecimentoIndustrialResponse)
async def obter_por_id(
    item_id: UUID,
    service: EstabelecimentoIndustrialService = estabelecimento_industrial_service_dep,
):
    try:
        return await service.obter_por_id(item_id)
    except EstabelecimentoIndustrialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[EstabelecimentoIndustrialResponse])
async def listar(
    status_estabelecimento: StatusEstabelecimento | None = None,
    ramo: RamoIndustrial | None = None,
    municipio: str | None = None,
    service: EstabelecimentoIndustrialService = estabelecimento_industrial_service_dep,
):
    return await service.listar(status=status_estabelecimento, ramo=ramo, municipio=municipio)