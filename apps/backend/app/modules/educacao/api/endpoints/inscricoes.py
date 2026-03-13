from __future__ import annotations
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_user
from app.modules.educacao.api.deps import get_inscricao_service
from app.modules.educacao.api.schemas.inscricao_schema import InscricaoCancelar, InscricaoConfirmar, InscricaoCreate, InscricaoResponse
from app.modules.educacao.application.inscricao_service import InscricaoService
from app.modules.educacao.domain.enums import TipoInscricao
from app.modules.educacao.exceptions import CitizenNotFoundError, EscolaNotFoundError
router = APIRouter(prefix='/inscricoes', tags=['Educacao - Inscricoes'])

@router.post('/basica', response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_inscricao_basica(data: InscricaoCreate, service: InscricaoService=Depends(get_inscricao_service), _: dict=Depends(get_current_user)):
    try:
        return await service.criar_inscricao_basica(citizen_id=data.citizen_id, escola_id=data.escola_id, observacoes=data.observacoes)
    except (CitizenNotFoundError, EscolaNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/secundaria', response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_inscricao_secundaria(data: InscricaoCreate, service: InscricaoService=Depends(get_inscricao_service), _: dict=Depends(get_current_user)):
    try:
        return await service.criar_inscricao_secundaria(citizen_id=data.citizen_id, escola_id=data.escola_id, observacoes=data.observacoes)
    except (CitizenNotFoundError, EscolaNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/superior', response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_inscricao_superior(data: InscricaoCreate, service: InscricaoService=Depends(get_inscricao_service), _: dict=Depends(get_current_user)):
    try:
        return await service.criar_inscricao_superior(citizen_id=data.citizen_id, escola_id=data.escola_id, observacoes=data.observacoes)
    except (CitizenNotFoundError, EscolaNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/tecnico', response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_inscricao_tecnico(data: InscricaoCreate, service: InscricaoService=Depends(get_inscricao_service), _: dict=Depends(get_current_user)):
    try:
        return await service.criar_inscricao_tecnico(citizen_id=data.citizen_id, escola_id=data.escola_id, observacoes=data.observacoes)
    except (CitizenNotFoundError, EscolaNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{inscricao_id}/confirmar', response_model=InscricaoResponse)
async def confirmar_inscricao(inscricao_id: UUID, data: InscricaoConfirmar, service: InscricaoService=Depends(get_inscricao_service), user: dict=Depends(get_current_user)):
    if not data.confirmacao_documental:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Confirmacao documental obrigatoria')
    actor_id = UUID(user.get('user_id'))
    try:
        return await service.confirmar_inscricao(inscricao_id, actor_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{inscricao_id}/cancelar', response_model=InscricaoResponse)
async def cancelar_inscricao(inscricao_id: UUID, data: InscricaoCancelar, service: InscricaoService=Depends(get_inscricao_service), user: dict=Depends(get_current_user)):
    actor_id = UUID(user.get('user_id'))
    try:
        return await service.cancelar_inscricao(inscricao_id, actor_id, data.motivo)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/citizen/{citizen_id}', response_model=list[InscricaoResponse])
async def listar_inscricoes_cidadao(citizen_id: UUID, tipo: Optional[TipoInscricao]=None, service: InscricaoService=Depends(get_inscricao_service), _: dict=Depends(get_current_user)):
    return await service.listar_por_cidadao(citizen_id, tipo)
