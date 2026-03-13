from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.deps import get_matricula_service
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.schemas.matricula_schema import MatriculaCreate, MatriculaMotivoInput, MatriculaResponse, MatriculaTransferenciaInput
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.matricula_imovel_service import MatriculaImovelService
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusMatriculaImovel
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.exceptions import ImovelNotFoundError, MatriculaImovelAlreadyExistsError, MatriculaImovelNotFoundError
router = APIRouter(prefix='/matriculas', tags=['Gestao Fundiaria - Matriculas'])

def _ensure_justica_adapter(service: MatriculaImovelService) -> None:
    if not service.has_justica_adapter():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Justica indisponivel para operacoes de matricula imobiliaria. Verifique a integracao do modulo.')

@router.post('/', response_model=MatriculaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_matricula(data: MatriculaCreate, service: MatriculaImovelService=Depends(get_matricula_service)):
    _ensure_justica_adapter(service)
    try:
        return await service.registrar(imovel_inscricao=data.imovel_inscricao, tipo_registro=data.tipo_registro, cartorio_nome=data.cartorio_nome, livro=data.livro, folha=data.folha, comarca=data.comarca, provincia=data.provincia, proprietario_documento=data.proprietario_documento, numero_matricula=data.numero_matricula)
    except ImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except MatriculaImovelAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_matricula:path}/transferir', response_model=MatriculaResponse)
async def transferir_matricula(numero_matricula: str, data: MatriculaTransferenciaInput, service: MatriculaImovelService=Depends(get_matricula_service)):
    try:
        return await service.transferir(numero_matricula, novo_documento=data.novo_documento)
    except MatriculaImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_matricula:path}/cancelar', response_model=MatriculaResponse)
async def cancelar_matricula(numero_matricula: str, data: MatriculaMotivoInput, service: MatriculaImovelService=Depends(get_matricula_service)):
    try:
        return await service.cancelar(numero_matricula, motivo=data.motivo)
    except MatriculaImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_matricula:path}', response_model=MatriculaResponse)
async def obter_matricula(numero_matricula: str, service: MatriculaImovelService=Depends(get_matricula_service)):
    try:
        return await service.obter_por_numero(numero_matricula)
    except MatriculaImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[MatriculaResponse])
async def listar_matriculas(imovel_inscricao: str | None=None, status: StatusMatriculaImovel | None=None, ativo: bool | None=None, service: MatriculaImovelService=Depends(get_matricula_service)):
    return await service.listar(imovel_inscricao=imovel_inscricao, status=status, ativo=ativo)