from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.resources.ambiente.api.deps import get_cadastro_service
from apps.backend.app.modules.resources.ambiente.api.schemas.car_schema import CARAprovacaoInput, CARAreasInput, CARCreate, CARPendenciaInput, CARResponse, ImovelCreate, ImovelResponse, ProprietarioCreate, ProprietarioResponse
from apps.backend.app.modules.resources.ambiente.application.services.cadastro_service import CadastroService
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusCAR
from apps.backend.app.modules.resources.ambiente.exceptions import CARAlreadyExistsError, CARNotFoundError, ImovelNotFoundError, ProprietarioAlreadyExistsError, ProprietarioNotFoundError
router = APIRouter(prefix='/car', tags=['Ambiente - CAR'])

@router.post('/proprietarios', response_model=ProprietarioResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_proprietario(data: ProprietarioCreate, service: CadastroService=Depends(get_cadastro_service)):
    try:
        return await service.cadastrar_proprietario(nome=data.nome, documento=data.documento, telefone=data.telefone, email=data.email)
    except ProprietarioAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/imoveis', response_model=ImovelResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_imovel(data: ImovelCreate, service: CadastroService=Depends(get_cadastro_service)):
    try:
        return await service.cadastrar_imovel(proprietario_id=data.proprietario_id, nome=data.nome, provincia=data.provincia, municipio=data.municipio, area_total=data.area_total, bioma=data.bioma, tipo_imovel=data.tipo_imovel, coordenadas=data.coordenadas)
    except ProprietarioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/', response_model=CARResponse, status_code=status.HTTP_201_CREATED)
async def criar_car(data: CARCreate, service: CadastroService=Depends(get_cadastro_service)):
    try:
        return await service.criar_car(imovel_id=data.imovel_id, proprietario_id=data.proprietario_id, area_total=data.area_total, bioma=data.bioma, tipo_imovel=data.tipo_imovel)
    except (ProprietarioNotFoundError, ImovelNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except CARAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_car:path}/areas', response_model=CARResponse)
async def atualizar_areas_car(numero_car: str, data: CARAreasInput, service: CadastroService=Depends(get_cadastro_service)):
    try:
        return await service.atualizar_areas(numero_car=numero_car, area_preservacao_permanente=data.area_preservacao_permanente, area_reserva_legal=data.area_reserva_legal, area_uso_alternativo=data.area_uso_alternativo, area_consolidada=data.area_consolidada)
    except CARNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_car:path}/submeter', response_model=CARResponse)
async def submeter_car(numero_car: str, service: CadastroService=Depends(get_cadastro_service)):
    try:
        return await service.submeter_para_analise(numero_car)
    except CARNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_car:path}/aprovar', response_model=CARResponse)
async def aprovar_car(numero_car: str, data: CARAprovacaoInput, service: CadastroService=Depends(get_cadastro_service)):
    try:
        return await service.aprovar(numero_car, data.analista_id)
    except CARNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_car:path}/pendencia', response_model=CARResponse)
async def solicitar_pendencia_car(numero_car: str, data: CARPendenciaInput, service: CadastroService=Depends(get_cadastro_service)):
    try:
        return await service.solicitar_pendencia(numero_car, data.motivo, data.analista_id)
    except CARNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_car:path}', response_model=CARResponse)
async def obter_car(numero_car: str, service: CadastroService=Depends(get_cadastro_service)):
    try:
        return await service.obter_por_numero(numero_car)
    except CARNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[CARResponse])
async def listar_cars(status_car: StatusCAR | None=None, service: CadastroService=Depends(get_cadastro_service)):
    return await service.listar(status=status_car)