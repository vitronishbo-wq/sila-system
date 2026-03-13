from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.agricultura.api.deps import get_zoneamento_service
from app.modules.resources.agricultura.api.schemas.zoneamento_schema import CadastroAmbientalCreate, CadastroAmbientalPendenciaInput, CadastroAmbientalResponse, CadastroAmbientalValidacaoInput, ZoneamentoCreate, ZoneamentoResponse, ZoneamentoRevogacaoInput
from app.modules.resources.agricultura.application.services.zoneamento_service import ZoneamentoService
from app.modules.resources.agricultura.domain.enums import StatusCadastroAmbiental, StatusZoneamento
from app.modules.resources.agricultura.exceptions import CadastroAmbientalNotFoundError, PropriedadeNotFoundError, ZoneamentoNotFoundError
router = APIRouter(prefix='/zoneamento', tags=['Agricultura - zoneamento'])

@router.post('/', response_model=ZoneamentoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_zoneamento(data: ZoneamentoCreate, service: ZoneamentoService=Depends(get_zoneamento_service)):
    try:
        return await service.registrar_zoneamento(codigo_propriedade=data.codigo_propriedade, zona=data.zona, aptidao_solo=data.aptidao_solo, area_zoneada_ha=data.area_zoneada_ha, culturas_recomendadas=data.culturas_recomendadas, restricoes=data.restricoes, validade_ate=data.validade_ate, observacoes=data.observacoes)
    except PropriedadeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_zoneamento:path}/revisao', response_model=ZoneamentoResponse)
async def entrar_revisao(codigo_zoneamento: str, service: ZoneamentoService=Depends(get_zoneamento_service)):
    try:
        return await service.entrar_revisao(codigo_zoneamento)
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_zoneamento:path}/revogar', response_model=ZoneamentoResponse)
async def revogar_zoneamento(codigo_zoneamento: str, data: ZoneamentoRevogacaoInput, service: ZoneamentoService=Depends(get_zoneamento_service)):
    try:
        return await service.revogar(codigo_zoneamento, motivo=data.motivo)
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/', response_model=list[ZoneamentoResponse])
async def listar_zoneamentos(codigo_propriedade: str | None=None, status_zoneamento: StatusZoneamento | None=None, service: ZoneamentoService=Depends(get_zoneamento_service)):
    return await service.listar_zoneamentos(codigo_propriedade=codigo_propriedade, status=status_zoneamento)

@router.post('/{codigo_zoneamento:path}/cadastro-ambiental', response_model=CadastroAmbientalResponse, status_code=status.HTTP_201_CREATED)
async def registrar_cadastro_ambiental(codigo_zoneamento: str, data: CadastroAmbientalCreate, service: ZoneamentoService=Depends(get_zoneamento_service)):
    try:
        return await service.registrar_cadastro_ambiental(codigo_zoneamento=codigo_zoneamento, reserva_legal_percentual=data.reserva_legal_percentual, app_percentual=data.app_percentual, area_protecao_ha=data.area_protecao_ha, numero_processo=data.numero_processo)
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/cadastro-ambiental/{codigo_cadastro_ambiental:path}/validar', response_model=CadastroAmbientalResponse)
async def validar_cadastro_ambiental(codigo_cadastro_ambiental: str, data: CadastroAmbientalValidacaoInput, service: ZoneamentoService=Depends(get_zoneamento_service)):
    try:
        return await service.validar_cadastro(codigo_cadastro_ambiental, numero_processo=data.numero_processo)
    except CadastroAmbientalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/cadastro-ambiental/{codigo_cadastro_ambiental:path}/pendencias', response_model=CadastroAmbientalResponse)
async def registrar_pendencia_cadastro_ambiental(codigo_cadastro_ambiental: str, data: CadastroAmbientalPendenciaInput, service: ZoneamentoService=Depends(get_zoneamento_service)):
    try:
        return await service.registrar_pendencia(codigo_cadastro_ambiental, pendencia=data.pendencia)
    except CadastroAmbientalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/cadastro-ambiental/{codigo_cadastro_ambiental:path}/sanear-pendencias', response_model=CadastroAmbientalResponse)
async def sanar_pendencias_cadastro_ambiental(codigo_cadastro_ambiental: str, service: ZoneamentoService=Depends(get_zoneamento_service)):
    try:
        return await service.sanar_pendencias(codigo_cadastro_ambiental)
    except CadastroAmbientalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/cadastro-ambiental/{codigo_cadastro_ambiental:path}', response_model=CadastroAmbientalResponse)
async def obter_cadastro_ambiental(codigo_cadastro_ambiental: str, service: ZoneamentoService=Depends(get_zoneamento_service)):
    try:
        return await service.obter_cadastro_ambiental(codigo_cadastro_ambiental)
    except CadastroAmbientalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/cadastro-ambiental/', response_model=list[CadastroAmbientalResponse])
async def listar_cadastros_ambientais(codigo_propriedade: str | None=None, status_cadastro: StatusCadastroAmbiental | None=None, service: ZoneamentoService=Depends(get_zoneamento_service)):
    return await service.listar_cadastros_ambientais(codigo_propriedade=codigo_propriedade, status=status_cadastro)

@router.get('/{codigo_zoneamento:path}', response_model=ZoneamentoResponse)
async def obter_zoneamento(codigo_zoneamento: str, service: ZoneamentoService=Depends(get_zoneamento_service)):
    try:
        return await service.obter_zoneamento(codigo_zoneamento)
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))