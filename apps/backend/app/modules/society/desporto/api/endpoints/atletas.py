from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.desporto.api.deps import get_atleta_service
from apps.backend.app.modules.society.desporto.api.schemas.atleta_schema import AtletaCreate, AtletaResponse, AtletaUpdate
from apps.backend.app.modules.society.desporto.application.services.atleta_service import AtletaService
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusAtleta, TipoAtleta
router = APIRouter(prefix='/atletas', tags=['Desporto - Atletas'])

@router.post('/', response_model=AtletaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_atleta(data: AtletaCreate, service: AtletaService=Depends(get_atleta_service)) -> AtletaResponse:
    try:
        return await service.cadastrar_atleta(nome=data.nome, data_nascimento=data.data_nascimento, naturalidade=data.naturalidade, nacionalidade=data.nacionalidade, tipo=data.tipo, modalidades=data.modalidades, citizen_id=data.citizen_id, posicoes=data.posicoes, pe_preferencial=data.pe_preferencial, altura_cm=data.altura_cm, peso_kg=data.peso_kg, clube_atual_id=data.clube_atual_id, numero_camisola=data.numero_camisola, ultimo_exame_id=data.ultimo_exame_id, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{atleta_id}', response_model=AtletaResponse)
async def obter_atleta(atleta_id: UUID, service: AtletaService=Depends(get_atleta_service)) -> AtletaResponse:
    try:
        return await service.buscar_atleta(atleta_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[AtletaResponse])
async def listar_atletas(tipo: TipoAtleta | None=None, modalidade: ModalidadeDesportiva | None=None, status_filtro: StatusAtleta | None=None, clube_id: UUID | None=None, somente_ativos: bool=True, service: AtletaService=Depends(get_atleta_service)) -> list[AtletaResponse]:
    return await service.listar_atletas(tipo=tipo, modalidade=modalidade, status=status_filtro, clube_id=clube_id, somente_ativos=somente_ativos)

@router.patch('/{atleta_id}', response_model=AtletaResponse)
async def atualizar_atleta(atleta_id: UUID, data: AtletaUpdate, service: AtletaService=Depends(get_atleta_service)) -> AtletaResponse:
    try:
        return await service.atualizar_atleta(atleta_id=atleta_id, nome=data.nome, tipo=data.tipo, modalidades=data.modalidades, posicoes=data.posicoes, pe_preferencial=data.pe_preferencial, altura_cm=data.altura_cm, peso_kg=data.peso_kg, clube_atual_id=data.clube_atual_id, numero_camisola=data.numero_camisola, status=data.status, ultimo_exame_id=data.ultimo_exame_id, ativo=data.ativo, observacoes=data.observacoes)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.post('/{atleta_id}/lesao', response_model=AtletaResponse)
async def registrar_lesao(atleta_id: UUID, service: AtletaService=Depends(get_atleta_service)) -> AtletaResponse:
    try:
        return await service.registrar_lesao(atleta_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/{atleta_id}/recuperar', response_model=AtletaResponse)
async def recuperar_atleta(atleta_id: UUID, service: AtletaService=Depends(get_atleta_service)) -> AtletaResponse:
    try:
        return await service.recuperar_atleta(atleta_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{atleta_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_atleta(atleta_id: UUID, service: AtletaService=Depends(get_atleta_service)) -> None:
    try:
        await service.remover_atleta(atleta_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))