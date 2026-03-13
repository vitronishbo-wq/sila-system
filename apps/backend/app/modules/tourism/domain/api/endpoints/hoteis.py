from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.tourism.api.deps import get_hotel_service
from apps.backend.app.modules.tourism.api.schemas.hotel_schema import HotelCreate, HotelResponse
from apps.backend.app.modules.tourism.application.services.meio_hospedagem_service import MeioHospedagemService
from apps.backend.app.modules.tourism.domain.enums import ClassificacaoHoteleira
router = APIRouter(prefix='/hoteis', tags=['Turismo - Hoteis'])

@router.post('/', response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_hotel(data: HotelCreate, service: MeioHospedagemService=Depends(get_hotel_service)) -> HotelResponse:
    try:
        return await service.cadastrar_hotel(nome=data.nome, tipo=data.tipo, classificacao=data.classificacao, cnpj=data.cnpj, endereco=data.endereco, numero=data.numero, bairro=data.bairro, municipio=data.municipio, provincia=data.provincia, cep=data.cep, telefone=data.telefone, email=data.email, quartos=data.quartos, capacidade_maxima=data.capacidade_maxima, proprietario_id=data.proprietario_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{hotel_id}', response_model=HotelResponse)
async def obter_hotel(hotel_id: UUID, service: MeioHospedagemService=Depends(get_hotel_service)) -> HotelResponse:
    try:
        return await service.buscar_hotel(hotel_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[HotelResponse])
async def listar_hoteis(municipio: str | None=None, classificacao: ClassificacaoHoteleira | None=None, service: MeioHospedagemService=Depends(get_hotel_service)) -> list[HotelResponse]:
    if classificacao is not None:
        return await service.listar_hoteis_por_classificacao(classificacao)
    return await service.listar_hoteis(municipio=municipio)
