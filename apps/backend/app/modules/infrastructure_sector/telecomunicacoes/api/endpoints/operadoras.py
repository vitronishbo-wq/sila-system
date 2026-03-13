from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.infrastructure_sector.telecomunicacoes.api.deps import get_operadora_service
from app.modules.infrastructure_sector.telecomunicacoes.api.schemas.operadora_schema import OperadoraAuthorize, OperadoraCreate, OperadoraResponse
from app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import TipoServico
router = APIRouter(prefix='/operadoras', tags=['Telecomunicacoes - Operadoras'])

@router.post('/', response_model=OperadoraResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_operadora(data: OperadoraCreate, service: OperadoraService=Depends(get_operadora_service)) -> OperadoraResponse:
    try:
        return await service.cadastrar_operadora(cnpj=data.cnpj, razao_social=data.razao_social, tipo=data.tipo, servicos_autorizados=data.servicos_autorizados, endereco=data.endereco, municipio=data.municipio, provincia=data.provincia, telefone=data.telefone, email=data.email, representante_legal=data.representante_legal, representante_documento=data.representante_documento, representante_cargo=data.representante_cargo, nome_fantasia=data.nome_fantasia, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{operadora_id}', response_model=OperadoraResponse)
async def obter_operadora(operadora_id: UUID, service: OperadoraService=Depends(get_operadora_service)) -> OperadoraResponse:
    try:
        return await service.buscar_operadora(operadora_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[OperadoraResponse])
async def listar_operadoras(servico: TipoServico | None=None, municipio: str | None=None, somente_ativas: bool=False, service: OperadoraService=Depends(get_operadora_service)) -> list[OperadoraResponse]:
    return await service.listar_operadoras(servico=servico, municipio=municipio, somente_ativas=somente_ativas)

@router.patch('/{operadora_id}/autorizar', response_model=OperadoraResponse)
async def autorizar_operadora(operadora_id: UUID, data: OperadoraAuthorize, service: OperadoraService=Depends(get_operadora_service)) -> OperadoraResponse:
    try:
        return await service.autorizar_operadora(operadora_id=operadora_id, outorga_id=data.outorga_id, data_autorizacao=data.data_autorizacao, data_validade=data.data_validade)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrada' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.delete('/{operadora_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_operadora(operadora_id: UUID, service: OperadoraService=Depends(get_operadora_service)) -> None:
    try:
        await service.remover_operadora(operadora_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))