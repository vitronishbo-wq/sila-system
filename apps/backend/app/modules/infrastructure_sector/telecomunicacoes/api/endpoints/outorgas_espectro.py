from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.infrastructure_sector.telecomunicacoes.api.deps import get_outorga_espectro_service
from app.modules.infrastructure_sector.telecomunicacoes.api.schemas.outorga_espectro_schema import OutorgaEspectroCreate, OutorgaEspectroResponse, OutorgaEspectroStatusUpdate
from app.modules.infrastructure_sector.telecomunicacoes.application.services.outorga_espectro_service import OutorgaEspectroService
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga
router = APIRouter(prefix='/outorgas-espectro', tags=['Telecomunicacoes - Outorgas'])

@router.post('/', response_model=OutorgaEspectroResponse, status_code=status.HTTP_201_CREATED)
async def emitir_outorga(data: OutorgaEspectroCreate, service: OutorgaEspectroService=Depends(get_outorga_espectro_service)) -> OutorgaEspectroResponse:
    try:
        return await service.emitir_outorga(operadora_id=data.operadora_id, tipo_outorga=data.tipo_outorga, faixa_inicio_mhz=data.faixa_inicio_mhz, faixa_fim_mhz=data.faixa_fim_mhz, data_outorga=data.data_outorga, data_validade=data.data_validade, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{outorga_id}', response_model=OutorgaEspectroResponse)
async def obter_outorga(outorga_id: UUID, service: OutorgaEspectroService=Depends(get_outorga_espectro_service)) -> OutorgaEspectroResponse:
    try:
        return await service.buscar_outorga(outorga_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[OutorgaEspectroResponse])
async def listar_outorgas(operadora_id: UUID | None=None, status_filtro: StatusOutorga | None=None, service: OutorgaEspectroService=Depends(get_outorga_espectro_service)) -> list[OutorgaEspectroResponse]:
    return await service.listar_outorgas(operadora_id=operadora_id, status=status_filtro)

@router.patch('/{outorga_id}/status', response_model=OutorgaEspectroResponse)
async def atualizar_status_outorga(outorga_id: UUID, data: OutorgaEspectroStatusUpdate, service: OutorgaEspectroService=Depends(get_outorga_espectro_service)) -> OutorgaEspectroResponse:
    try:
        return await service.atualizar_status(outorga_id=outorga_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{outorga_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_outorga(outorga_id: UUID, service: OutorgaEspectroService=Depends(get_outorga_espectro_service)) -> None:
    try:
        await service.remover_outorga(outorga_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))