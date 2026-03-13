from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.logistics.api.deps import get_linha_service
from apps.backend.app.modules.logistics.api.schemas.linha_schema import LinhaCreate, LinhaIndicadoresInput, LinhaResponse, LinhaTarifaInput, LinhaVincularVeiculoInput, VeiculoCreate, VeiculoResponse
from apps.backend.app.modules.logistics.application.services import LinhaService
from apps.backend.app.modules.logistics.domain.enums import ModalTransporte, StatusLinha, StatusVeiculoOperacional, TipoVeiculo
from apps.backend.app.modules.logistics.core.exceptions import LinhaAlreadyExistsError, LinhaNotFoundError, VeiculoAlreadyExistsError, VeiculoNotFoundError
router = APIRouter(prefix='/linhas', tags=['Transportes Logistica - Linhas'])

def _has_capability(service: LinhaService, method_name: str) -> bool:
    checker = getattr(service, method_name, None)
    if checker is None:
        return True
    return bool(checker())

def _ensure_criacao_adapters(service: LinhaService) -> None:
    if not _has_capability(service, 'has_geosampa_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter Geosampa indisponivel para criacao da linha.')
    if not _has_capability(service, 'has_urbanismo_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter Urbanismo indisponivel para criacao da linha.')
    if not _has_capability(service, 'has_workflow_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter Workflow indisponivel para trilha da linha.')

@router.post('/', response_model=LinhaResponse, status_code=status.HTTP_201_CREATED)
async def criar_linha(data: LinhaCreate, service: LinhaService=Depends(get_linha_service)):
    _ensure_criacao_adapters(service)
    try:
        return await service.criar_linha(nome=data.nome, modal=data.modal, tipo_viagem=data.tipo_viagem, origem=data.origem, destino=data.destino, itinerario=data.itinerario, extensao_km=data.extensao_km, tempo_estimado_minutos=data.tempo_estimado_minutos, dias_operacao=data.dias_operacao, horario_inicio=data.horario_inicio, horario_fim=data.horario_fim, tarifa_base=data.tarifa_base, operadora_id=data.operadora_id, codigo=data.codigo, frequencia_media_minutos=data.frequencia_media_minutos, codigo_corredor=data.codigo_corredor, observacoes=data.observacoes)
    except LinhaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/veiculos', response_model=VeiculoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_veiculo(data: VeiculoCreate, service: LinhaService=Depends(get_linha_service)):
    try:
        return await service.cadastrar_veiculo(placa=data.placa, tipo=data.tipo, marca=data.marca, modelo=data.modelo, ano_fabricacao=data.ano_fabricacao, ano_modelo=data.ano_modelo, proprietario_id=data.proprietario_id, proprietario_tipo=data.proprietario_tipo, data_aquisicao=data.data_aquisicao, capacidade_passageiros=data.capacidade_passageiros, operadora_id=data.operadora_id, observacoes=data.observacoes)
    except VeiculoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_linha:path}/veiculos', response_model=LinhaResponse)
async def vincular_veiculo(codigo_linha: str, data: LinhaVincularVeiculoInput, service: LinhaService=Depends(get_linha_service)):
    try:
        return await service.vincular_veiculo(codigo_linha, placa=data.placa)
    except LinhaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except VeiculoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{codigo_linha:path}/tarifa', response_model=LinhaResponse)
async def atualizar_tarifa(codigo_linha: str, data: LinhaTarifaInput, service: LinhaService=Depends(get_linha_service)):
    try:
        return await service.atualizar_tarifa(codigo_linha, valor=data.valor)
    except LinhaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{codigo_linha:path}/indicadores', response_model=LinhaResponse)
async def registrar_indicadores(codigo_linha: str, data: LinhaIndicadoresInput, service: LinhaService=Depends(get_linha_service)):
    try:
        return await service.registrar_indicadores(codigo_linha, demanda_media_diaria=data.demanda_media_diaria, ocupacao_media=data.ocupacao_media, regularidade=data.regularidade, pontualidade=data.pontualidade)
    except LinhaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/', response_model=list[LinhaResponse])
async def listar_linhas(status_linha: StatusLinha | None=None, modal: ModalTransporte | None=None, operadora_id: UUID | None=None, origem: str | None=None, destino: str | None=None, service: LinhaService=Depends(get_linha_service)):
    return await service.listar_linhas(status=status_linha, modal=modal, operadora_id=operadora_id, origem=origem, destino=destino)

@router.get('/veiculos/{placa}', response_model=VeiculoResponse)
async def obter_veiculo(placa: str, service: LinhaService=Depends(get_linha_service)):
    try:
        return await service.obter_veiculo(placa)
    except VeiculoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/veiculos/', response_model=list[VeiculoResponse])
async def listar_veiculos(status_veiculo: StatusVeiculoOperacional | None=None, tipo: TipoVeiculo | None=None, operadora_id: UUID | None=None, service: LinhaService=Depends(get_linha_service)):
    return await service.listar_veiculos(status=status_veiculo, tipo=tipo, operadora_id=operadora_id)

@router.get('/{codigo_linha:path}', response_model=LinhaResponse)
async def obter_linha(codigo_linha: str, service: LinhaService=Depends(get_linha_service)):
    try:
        return await service.obter_linha(codigo_linha)
    except LinhaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
