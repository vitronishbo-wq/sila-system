from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.juventude.api.deps import get_jovem_service
from apps.backend.app.modules.society.juventude.api.schemas.jovem_schema import JovemCreate, JovemResponse, JovemUpdate, VulnerabilidadeAdd
from apps.backend.app.modules.society.juventude.application.services.jovem_service import JovemService
from apps.backend.app.modules.society.juventude.domain.enums import Escolaridade, FaixaEtaria, SituacaoOcupacional
router = APIRouter(prefix='/jovens', tags=['Juventude - Jovens'])

@router.post('/', response_model=JovemResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_jovem(data: JovemCreate, service: JovemService=Depends(get_jovem_service)) -> JovemResponse:
    try:
        return await service.cadastrar_jovem(nome=data.nome, data_nascimento=data.data_nascimento, genero=data.genero, naturalidade=data.naturalidade, nacionalidade=data.nacionalidade, escolaridade=data.escolaridade, situacao_ocupacional=data.situacao_ocupacional, endereco=data.endereco, municipio=data.municipio, provincia=data.provincia, telefone=data.telefone, email=data.email, citizen_id=data.citizen_id, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{jovem_id}', response_model=JovemResponse)
async def obter_jovem(jovem_id: UUID, service: JovemService=Depends(get_jovem_service)) -> JovemResponse:
    try:
        return await service.buscar_jovem(jovem_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[JovemResponse])
async def listar_jovens(faixa_etaria: FaixaEtaria | None=None, escolaridade: Escolaridade | None=None, situacao: SituacaoOcupacional | None=None, municipio: str | None=None, vulneravel: bool | None=None, service: JovemService=Depends(get_jovem_service)) -> list[JovemResponse]:
    return await service.listar_jovens(faixa_etaria=faixa_etaria, escolaridade=escolaridade, situacao=situacao, municipio=municipio, vulneravel=vulneravel)

@router.patch('/{jovem_id}', response_model=JovemResponse)
async def atualizar_jovem(jovem_id: UUID, data: JovemUpdate, service: JovemService=Depends(get_jovem_service)) -> JovemResponse:
    try:
        return await service.atualizar_jovem(jovem_id=jovem_id, escolaridade=data.escolaridade, situacao_ocupacional=data.situacao_ocupacional, telefone=data.telefone, email=data.email, endereco=data.endereco, municipio=data.municipio, provincia=data.provincia, observacoes=data.observacoes, ativo=data.ativo)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.post('/{jovem_id}/vulnerabilidades', response_model=JovemResponse)
async def adicionar_vulnerabilidade(jovem_id: UUID, data: VulnerabilidadeAdd, service: JovemService=Depends(get_jovem_service)) -> JovemResponse:
    try:
        return await service.adicionar_vulnerabilidade(jovem_id=jovem_id, vulnerabilidade=data.vulnerabilidade)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{jovem_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_jovem(jovem_id: UUID, service: JovemService=Depends(get_jovem_service)) -> None:
    try:
        await service.remover_jovem(jovem_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))