from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.tourism.api.deps import get_agencia_service
from apps.backend.app.modules.tourism.api.schemas.agencia_viagens_schema import AgenciaViagensCreate, AgenciaViagensResponse, AgenciaViagensUpdate
from apps.backend.app.modules.tourism.application.services.agencia_viagens_service import AgenciaViagensService
router = APIRouter(prefix='/agencias-viagens', tags=['Turismo - Agencias Viagens'])

@router.post('/', response_model=AgenciaViagensResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_agencia(data: AgenciaViagensCreate, service: AgenciaViagensService=Depends(get_agencia_service)) -> AgenciaViagensResponse:
    try:
        return await service.cadastrar(nome_fantasia=data.nome_fantasia, razao_social=data.razao_social, cnpj=data.cnpj, email=data.email, telefone=data.telefone, endereco=data.endereco, numero=data.numero, bairro=data.bairro, municipio=data.municipio, provincia=data.provincia, cep=data.cep, proprietario_id=data.proprietario_id, especialidades=data.especialidades, site=data.site, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{agencia_id}', response_model=AgenciaViagensResponse)
async def obter_agencia(agencia_id: UUID, service: AgenciaViagensService=Depends(get_agencia_service)) -> AgenciaViagensResponse:
    try:
        return await service.obter(agencia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/')
async def listar_agencias(municipio: str | None=None, ativa: bool | None=None, service: AgenciaViagensService=Depends(get_agencia_service)) -> list[AgenciaViagensResponse]:
    return await service.listar(municipio=municipio, ativa=ativa)

@router.put('/{agencia_id}', response_model=AgenciaViagensResponse)
async def atualizar_agencia(agencia_id: UUID, data: AgenciaViagensUpdate, service: AgenciaViagensService=Depends(get_agencia_service)) -> AgenciaViagensResponse:
    try:
        return await service.atualizar(agencia_id, nome_fantasia=data.nome_fantasia, razao_social=data.razao_social, email=data.email, telefone=data.telefone, endereco=data.endereco, numero=data.numero, bairro=data.bairro, municipio=data.municipio, provincia=data.provincia, cep=data.cep, especialidades=data.especialidades, site=data.site, observacoes=data.observacoes, ativa=data.ativa)
    except ValueError as exc:
        status_code = status.HTTP_404_NOT_FOUND if 'nao encontrada' in str(exc).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(exc))

@router.delete('/{agencia_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_agencia(agencia_id: UUID, service: AgenciaViagensService=Depends(get_agencia_service)) -> None:
    try:
        await service.remover(agencia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
