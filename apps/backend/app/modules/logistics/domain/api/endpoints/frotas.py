from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.logistics.api.deps import get_frota_service
from apps.backend.app.modules.logistics.api.schemas.frota_schema import FrotaAdicionarVeiculoInput, FrotaCreate, FrotaFiscalizacaoInput, FrotaManutencaoInput, FrotaResponse, FrotaTarifaInput
from apps.backend.app.modules.logistics.application.services import FrotaService
from apps.backend.app.modules.logistics.domain.enums import StatusFrota
from apps.backend.app.modules.logistics.domain.exceptions import FrotaAlreadyExistsError, FrotaNotFoundError
router = APIRouter(prefix='/frotas', tags=['Transportes Logistica - Frotas'])

def _has_capability(service: FrotaService, method_name: str) -> bool:
    checker = getattr(service, method_name, None)
    if checker is None:
        return True
    return bool(checker())

def _ensure_criacao_adapters(service: FrotaService) -> None:
    if not _has_capability(service, 'has_workflow_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Workflow indisponivel para criacao da frota.')
    if not _has_capability(service, 'has_service_requests_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Service Requests indisponivel para criacao da frota.')

@router.post('/', response_model=FrotaResponse, status_code=status.HTTP_201_CREATED)
async def criar_frota(data: FrotaCreate, service: FrotaService=Depends(get_frota_service)):
    _ensure_criacao_adapters(service)
    try:
        return await service.criar_frota(nome=data.nome, operadora_id=data.operadora_id, municipio=data.municipio, provincia=data.provincia, codigo_frota=data.codigo_frota, observacoes=data.observacoes)
    except FrotaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_frota:path}/veiculos', response_model=FrotaResponse)
async def adicionar_veiculo_frota(codigo_frota: str, data: FrotaAdicionarVeiculoInput, service: FrotaService=Depends(get_frota_service)):
    try:
        return await service.adicionar_veiculo(codigo_frota, veiculo_id=data.veiculo_id, placa=data.placa, tipo=data.tipo, capacidade=data.capacidade)
    except FrotaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_frota:path}/manutencoes', response_model=FrotaResponse)
async def registrar_manutencao_frota(codigo_frota: str, data: FrotaManutencaoInput, service: FrotaService=Depends(get_frota_service)):
    try:
        return await service.registrar_manutencao(codigo_frota, veiculo_id=data.veiculo_id, tipo=data.tipo, oficina=data.oficina, custo=data.custo, data_manutencao=data.data_manutencao, observacoes=data.observacoes)
    except FrotaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_frota:path}/tarifas', response_model=FrotaResponse)
async def atualizar_tarifa_frota(codigo_frota: str, data: FrotaTarifaInput, service: FrotaService=Depends(get_frota_service)):
    try:
        return await service.atualizar_tarifa(codigo_frota, tipo_tarifa=data.tipo_tarifa, valor=data.valor, motivo=data.motivo, data_inicio_vigencia=data.data_inicio_vigencia, data_fim_vigencia=data.data_fim_vigencia)
    except FrotaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_frota:path}/fiscalizacoes', response_model=FrotaResponse)
async def registrar_fiscalizacao_frota(codigo_frota: str, data: FrotaFiscalizacaoInput, service: FrotaService=Depends(get_frota_service)):
    try:
        return await service.registrar_fiscalizacao(codigo_frota, fiscal_id=data.fiscal_id, conformidade=data.conformidade, apontamentos=data.apontamentos, data_fiscalizacao=data.data_fiscalizacao, auto_infracao=data.auto_infracao, observacoes=data.observacoes)
    except FrotaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_frota:path}', response_model=FrotaResponse)
async def obter_frota(codigo_frota: str, service: FrotaService=Depends(get_frota_service)):
    try:
        return await service.obter_por_codigo(codigo_frota)
    except FrotaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[FrotaResponse])
async def listar_frotas(status_frota: StatusFrota | None=None, operadora_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None, service: FrotaService=Depends(get_frota_service)):
    return await service.listar(status=status_frota, operadora_id=operadora_id, municipio=municipio, provincia=provincia)
