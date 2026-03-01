from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.turismo.api.deps import get_pousada_service
from app.modules.turismo.api.schemas.pousada_schema import (
    PousadaCreate,
    PousadaResponse,
    PousadaUpdate,
)
from app.modules.turismo.application.services.meio_hospedagem_service import MeioHospedagemService
from app.modules.turismo.domain.enums import ClassificacaoHoteleira

router = APIRouter(prefix="/pousadas", tags=["Turismo - Pousadas"])


@router.post("/", response_model=PousadaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_pousada(
    data: PousadaCreate,
    service: MeioHospedagemService = Depends(get_pousada_service),
) -> PousadaResponse:
    try:
        return await service.cadastrar_pousada(
            nome=data.nome,
            classificacao=data.classificacao,
            cnpj=data.cnpj,
            endereco=data.endereco,
            numero=data.numero,
            bairro=data.bairro,
            municipio=data.municipio,
            provincia=data.provincia,
            cep=data.cep,
            telefone=data.telefone,
            email=data.email,
            quartos=data.quartos,
            capacidade_maxima=data.capacidade_maxima,
            proprietario_id=data.proprietario_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{pousada_id}", response_model=PousadaResponse)
async def obter_pousada(
    pousada_id: UUID,
    service: MeioHospedagemService = Depends(get_pousada_service),
) -> PousadaResponse:
    try:
        return await service.buscar_pousada(pousada_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/")
async def listar_pousadas(
    municipio: str | None = None,
    classificacao: ClassificacaoHoteleira | None = None,
    ativa: bool | None = None,
    service: MeioHospedagemService = Depends(get_pousada_service),
) -> list[PousadaResponse]:
    return await service.listar_pousadas(
        municipio=municipio,
        classificacao=classificacao,
        ativa=ativa,
    )


@router.put("/{pousada_id}", response_model=PousadaResponse)
async def atualizar_pousada(
    pousada_id: UUID,
    data: PousadaUpdate,
    service: MeioHospedagemService = Depends(get_pousada_service),
) -> PousadaResponse:
    try:
        return await service.atualizar_pousada(
            pousada_id,
            nome=data.nome,
            classificacao=data.classificacao,
            endereco=data.endereco,
            numero=data.numero,
            bairro=data.bairro,
            municipio=data.municipio,
            provincia=data.provincia,
            cep=data.cep,
            telefone=data.telefone,
            email=data.email,
            site=data.site,
            observacoes=data.observacoes,
            ativa=data.ativa,
        )
    except ValueError as exc:
        status_code = status.HTTP_404_NOT_FOUND if "nao encontrada" in str(exc).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(exc))


@router.delete("/{pousada_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_pousada(
    pousada_id: UUID,
    service: MeioHospedagemService = Depends(get_pousada_service),
) -> None:
    try:
        await service.remover_pousada(pousada_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
