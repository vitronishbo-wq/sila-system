from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.infrastructure_sector.telecomunicacoes.api.deps import get_indicador_qualidade_service
from app.modules.infrastructure_sector.telecomunicacoes.api.schemas.indicador_qualidade_schema import IndicadorQualidadeGerar, IndicadorQualidadeResponse
from app.modules.infrastructure_sector.telecomunicacoes.application.services.indicador_qualidade_service import IndicadorQualidadeService
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusIndicadorQualidade
router = APIRouter(prefix='/indicadores-qualidade', tags=['Telecomunicacoes - Indicadores Qualidade'])

@router.post('/gerar', response_model=IndicadorQualidadeResponse, status_code=status.HTTP_201_CREATED)
async def gerar_indicador(data: IndicadorQualidadeGerar, service: IndicadorQualidadeService=Depends(get_indicador_qualidade_service)) -> IndicadorQualidadeResponse:
    try:
        return await service.gerar_indicador_operadora(operadora_id=data.operadora_id, referencia_ano=data.referencia_ano, referencia_mes=data.referencia_mes, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{indicador_id}', response_model=IndicadorQualidadeResponse)
async def obter_indicador(indicador_id: UUID, service: IndicadorQualidadeService=Depends(get_indicador_qualidade_service)) -> IndicadorQualidadeResponse:
    try:
        return await service.buscar_indicador(indicador_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[IndicadorQualidadeResponse])
async def listar_indicadores(operadora_id: UUID | None=None, status_filtro: StatusIndicadorQualidade | None=None, service: IndicadorQualidadeService=Depends(get_indicador_qualidade_service)) -> list[IndicadorQualidadeResponse]:
    return await service.listar_indicadores(operadora_id=operadora_id, status=status_filtro)

@router.delete('/{indicador_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_indicador(indicador_id: UUID, service: IndicadorQualidadeService=Depends(get_indicador_qualidade_service)) -> None:
    try:
        await service.remover_indicador(indicador_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))