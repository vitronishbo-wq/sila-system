from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.infrastructure_sector.gestao_fundiaria.api.deps import get_georreferenciamento_service
from app.modules.infrastructure_sector.gestao_fundiaria.api.schemas.georreferenciamento_schema import GeorreferenciamentoCreate, GeorreferenciamentoMotivoInput, GeorreferenciamentoPontoInput, GeorreferenciamentoResponse
from app.modules.infrastructure_sector.gestao_fundiaria.application.services.georreferenciamento_service import GeorreferenciamentoService
from app.modules.infrastructure_sector.gestao_fundiaria.exceptions import GeorreferenciamentoAlreadyExistsError, GeorreferenciamentoNotFoundError, ImovelNotFoundError
router = APIRouter(prefix='/georreferenciamentos', tags=['Gestao Fundiaria - Georreferenciamentos'])

def _ensure_geosampa_adapter(service: GeorreferenciamentoService) -> None:
    if not service.has_geosampa_adapter():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Geosampa indisponivel para operacoes de georreferenciamento. Verifique a integracao do modulo.')

@router.post('/', response_model=GeorreferenciamentoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_georreferenciamento(data: GeorreferenciamentoCreate, service: GeorreferenciamentoService=Depends(get_georreferenciamento_service)):
    _ensure_geosampa_adapter(service)
    try:
        return await service.registrar(imovel_inscricao=data.imovel_inscricao, latitude=data.latitude, longitude=data.longitude, sistema_referencia=data.sistema_referencia, precisao_metros=data.precisao_metros, area_calculada=data.area_calculada, codigo_geo=data.codigo_geo)
    except ImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except GeorreferenciamentoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_geo:path}/ponto', response_model=GeorreferenciamentoResponse)
async def atualizar_ponto_georreferenciado(codigo_geo: str, data: GeorreferenciamentoPontoInput, service: GeorreferenciamentoService=Depends(get_georreferenciamento_service)):
    _ensure_geosampa_adapter(service)
    try:
        return await service.atualizar_ponto(codigo_geo, latitude=data.latitude, longitude=data.longitude)
    except GeorreferenciamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_geo:path}/invalidar', response_model=GeorreferenciamentoResponse)
async def invalidar_georreferenciamento(codigo_geo: str, data: GeorreferenciamentoMotivoInput, service: GeorreferenciamentoService=Depends(get_georreferenciamento_service)):
    try:
        return await service.invalidar(codigo_geo, motivo=data.motivo)
    except GeorreferenciamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_geo:path}', response_model=GeorreferenciamentoResponse)
async def obter_georreferenciamento(codigo_geo: str, service: GeorreferenciamentoService=Depends(get_georreferenciamento_service)):
    try:
        return await service.obter_por_codigo(codigo_geo)
    except GeorreferenciamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[GeorreferenciamentoResponse])
async def listar_georreferenciamentos(imovel_inscricao: str | None=None, validado: bool | None=None, ativo: bool | None=None, service: GeorreferenciamentoService=Depends(get_georreferenciamento_service)):
    return await service.listar(imovel_inscricao=imovel_inscricao, validado=validado, ativo=ativo)