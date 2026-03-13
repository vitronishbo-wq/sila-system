from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.public_security.api.deps import get_policial_service
from app.modules.public_security.api.schemas.policial_schema import PolicialCreate, PolicialPorteUpdate, PolicialResponse, PolicialStatusUpdate
from app.modules.public_security.application.services.policial_service import PolicialService
from app.modules.public_security.domain.enums import StatusAgente, TipoAgente
router = APIRouter(prefix='/policiais', tags=['Seguranca Publica - Policiais'])

@router.post('/', response_model=PolicialResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_policial(data: PolicialCreate, service: PolicialService=Depends(get_policial_service)) -> PolicialResponse:
    try:
        return await service.cadastrar_policial(unidade_id=data.unidade_id, nome=data.nome, data_nascimento=data.data_nascimento, cpf=data.cpf, rg=data.rg, tipo=data.tipo, vinculo=data.vinculo, cargo=data.cargo, patente=data.patente, telefone=data.telefone, email=data.email, endereco=data.endereco, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{policial_id}', response_model=PolicialResponse)
async def obter_policial(policial_id: UUID, service: PolicialService=Depends(get_policial_service)) -> PolicialResponse:
    try:
        return await service.buscar_policial(policial_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[PolicialResponse])
async def listar_policiais(unidade_id: UUID | None=None, tipo: TipoAgente | None=None, status_policial: StatusAgente | None=None, service: PolicialService=Depends(get_policial_service)) -> list[PolicialResponse]:
    return await service.listar_policiais(unidade_id=unidade_id, tipo=tipo, status=status_policial)

@router.patch('/{policial_id}/status', response_model=PolicialResponse)
async def atualizar_status_policial(policial_id: UUID, data: PolicialStatusUpdate, service: PolicialService=Depends(get_policial_service)) -> PolicialResponse:
    try:
        return await service.atualizar_status(policial_id=policial_id, status=data.status, motivo=data.motivo)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{policial_id}/porte', response_model=PolicialResponse)
async def ativar_porte_policial(policial_id: UUID, data: PolicialPorteUpdate, service: PolicialService=Depends(get_policial_service)) -> PolicialResponse:
    try:
        return await service.ativar_porte(policial_id=policial_id, numero_porte=data.numero_porte, data_validade=data.data_validade)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.delete('/{policial_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_policial(policial_id: UUID, service: PolicialService=Depends(get_policial_service)) -> None:
    try:
        await service.remover_policial(policial_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))