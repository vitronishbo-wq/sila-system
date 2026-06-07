from fastapi import APIRouter, HTTPException

from ..api.schemas import (
    MoradaNormalizadaResponse,
    MoradaNormalizarRequest,
    MoradaValidacaoResponse,
    MoradaValidarRequest,
)
from ..application.services.morada_service import (
    MoradaService,
)
from ..domain.exceptions import MoradaInvalidaError
from ..infrastructure.adapters import MoradaGeoAdapter

router = APIRouter(prefix="/integracao-nacional/moradas", tags=["Moradas - Normalizacao de Enderecos"])
_service: MoradaService | None = None


def get_morada_service() -> MoradaService:
    global _service
    if _service is None:
        _service = MoradaService(provider=MoradaGeoAdapter())
    return _service


@router.post("/normalizar", response_model=MoradaNormalizadaResponse)
async def normalizar_morada(request: MoradaNormalizarRequest):
    try:
        service = get_morada_service()
        result = await service.normalizar(request.endereco)
        return MoradaNormalizadaResponse(
            original=result.original,
            linha1=result.linha1,
            bairro=result.bairro,
            comuna=result.comuna,
            municipio=result.municipio,
            provincia=result.provincia,
            confidence=result.confidence,
        )
    except MoradaInvalidaError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validar", response_model=MoradaValidacaoResponse)
async def validar_morada(request: MoradaValidarRequest):
    try:
        service = get_morada_service()
        result = await service.validar(request.endereco)
        return MoradaValidacaoResponse(
            valida=result.valida,
            confianca=result.confianca,
            problemas=result.problemas,
            sugestoes=result.sugestoes,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
