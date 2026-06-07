from fastapi import APIRouter, HTTPException

from ..api.schemas import (
    BiConsultarRequest,
    BiConsultaResponse,
    BiValidarRequest,
    BiVerificacaoResponse,
)
from ..application.services.bi_service import BiService
from ..domain.exceptions import (
    BiNaoEncontradoError,
    BiNumeroInvalidoError,
)
from ..infrastructure.adapters import BiMockAdapter

router = APIRouter(prefix="/integracao-nacional/bi", tags=["BI - Bilhete de Identidade"])
_service: BiService | None = None


def get_bi_service() -> BiService:
    global _service
    if _service is None:
        _service = BiService(provider=BiMockAdapter())
    return _service


@router.post("/validar", response_model=BiVerificacaoResponse)
async def validar_bi(request: BiValidarRequest):
    try:
        service = get_bi_service()
        result = await service.validar(request.bi_numero)
        return BiVerificacaoResponse(
            bi_numero=result.bi_numero,
            valido=result.valido,
            status=result.status.value,
            cidadao_encontrado=result.cidadao_encontrado,
            verificacao_timestamp=result.verificacao_timestamp,
        )
    except BiNumeroInvalidoError:
        raise HTTPException(status_code=400, detail="Numero de BI invalido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/consultar", response_model=BiConsultaResponse)
async def consultar_bi(request: BiConsultarRequest):
    try:
        service = get_bi_service()
        dados = await service.consultar(request.bi_numero)
        return BiConsultaResponse(
            bi_numero=dados.numero,
            encontrado=True,
            full_name=dados.full_name,
            birth_date=dados.birth_date,
            gender=dados.gender,
            filiation_pai=dados.filiation_pai,
            filiation_mae=dados.filiation_mae,
            nationality=dados.nationality,
            tipo=dados.tipo.value if dados.tipo else None,
            status=dados.status.value if dados.status else None,
            emission_date=dados.emission_date,
            expiration_date=dados.expiration_date,
        )
    except BiNaoEncontradoError:
        raise HTTPException(status_code=404, detail="BI nao encontrado")
    except BiNumeroInvalidoError:
        raise HTTPException(status_code=400, detail="Numero de BI invalido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
